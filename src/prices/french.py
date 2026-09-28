"""Ken French US factors: Fama-French 3 factors (Mkt-RF, SMB, HML, RF) and momentum (Mom), daily
and monthly. The zip files are cached in data/raw/french/ (with a download log); the processed
files keep every date from FROM_DATE on.

UNITS: Ken French publishes returns in PERCENT (1.23 = 1.23%). The processed files keep percent,
say so in their column names (`_pct`) and in a `units` column, and the engine must divide by 100.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import re
import time
import zipfile
from pathlib import Path

import pandas as pd
import requests

RAW = Path("data/raw/french")
DAILY = Path("data/processed/factors_daily.csv")
MONTHLY = Path("data/processed/factors_monthly.csv")
FROM_DATE = "2015-01-01"
FILES = {"ff3_daily": "daily_3factor_url", "mom_daily": "daily_momentum_url",
         "ff3_monthly": "monthly_3factor_url", "mom_monthly": "monthly_momentum_url"}
RENAME = {"Mkt-RF": "mkt_rf_pct", "SMB": "smb_pct", "HML": "hml_pct", "RF": "rf_pct", "Mom": "mom_pct", "WML": "mom_pct"}


def download(cfg: dict, user_agent: str, refresh: bool = False) -> dict[str, Path]:
    RAW.mkdir(parents=True, exist_ok=True)
    log_path = RAW / "download_log.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else {}
    out = {}
    for name, key in FILES.items():
        url = cfg["factors"][key]
        p = RAW / Path(url).name
        if refresh or not p.exists():
            r = requests.get(url, headers={"User-Agent": user_agent}, timeout=120)
            r.raise_for_status()
            p.write_bytes(r.content)
            log[p.name] = {"url": url, "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                           "bytes": len(r.content)}
            print(f"  [factors] downloaded {p.name} ({len(r.content):,} bytes)")
            time.sleep(1.0)
        out[name] = p
    log_path.write_text(json.dumps(log, indent=1, sort_keys=True))
    return out


def read_table(path: Path, monthly: bool) -> pd.DataFrame:
    """The first data block of a Ken French CSV (monthly files also carry an annual block after it)."""
    with zipfile.ZipFile(path) as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    lines = text.splitlines()
    date_re = re.compile(r"^\s*(\d{6})\s*," if monthly else r"^\s*(\d{8})\s*,")
    header, rows = None, []
    for i, line in enumerate(lines):
        if header is None:
            if date_re.match(line) and i > 0:
                header = [c.strip() for c in lines[i - 1].split(",")]
                rows.append(line)
            continue
        if date_re.match(line):
            rows.append(line)
        elif rows:
            break                                   # end of the first block (monthly: annual block follows)
    df = pd.read_csv(io.StringIO("\n".join(rows)), header=None)
    df.columns = ["period"] + [c for c in header[1:] if c][: df.shape[1] - 1]
    df.columns = [c.strip() for c in df.columns]
    return df


def build(paths: dict[str, Path]) -> tuple[pd.DataFrame, pd.DataFrame]:
    d3 = read_table(paths["ff3_daily"], False)
    dm = read_table(paths["mom_daily"], False)
    daily = d3.merge(dm, on="period", how="left").rename(columns=RENAME)
    daily.insert(0, "date", pd.to_datetime(daily.pop("period").astype(str), format="%Y%m%d").dt.strftime("%Y-%m-%d"))
    daily = daily[daily["date"] >= FROM_DATE]
    m3 = read_table(paths["ff3_monthly"], True)
    mm = read_table(paths["mom_monthly"], True)
    monthly = m3.merge(mm, on="period", how="left").rename(columns=RENAME)
    per = pd.to_datetime(monthly.pop("period").astype(str), format="%Y%m")
    monthly.insert(0, "month", per.dt.strftime("%Y-%m"))
    monthly.insert(1, "month_end", (per + pd.offsets.MonthEnd(0)).dt.strftime("%Y-%m-%d"))
    monthly = monthly[monthly["month"] >= FROM_DATE[:7]]
    cols = ["mkt_rf_pct", "smb_pct", "hml_pct", "rf_pct", "mom_pct"]
    for df in (daily, monthly):
        for c in cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df["units"] = "percent"
    return daily[["date"] + cols + ["units"]].reset_index(drop=True), \
        monthly[["month", "month_end"] + cols + ["units"]].reset_index(drop=True)


def run(cfg: dict, user_agent: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    daily, monthly = build(download(cfg, user_agent))
    DAILY.parent.mkdir(parents=True, exist_ok=True)
    daily.to_csv(DAILY, index=False)
    monthly.to_csv(MONTHLY, index=False)
    print(f"  [factors] daily {daily['date'].min()}..{daily['date'].max()} ({len(daily)} rows); "
          f"monthly {monthly['month'].min()}..{monthly['month'].max()} ({len(monthly)} rows); units: percent")
    return daily, monthly
