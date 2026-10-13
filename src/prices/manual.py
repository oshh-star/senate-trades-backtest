"""Terminal exports (Bloomberg or FactSet), pulled by hand in the LBS library (M2, source 2 of 3).

One CSV per symbol at data/raw/manual_prices/<TICKER>.csv (TICKER = the price symbol this project uses, as in
docs/archive/PRICE_REQUEST.md), with exactly these columns:
  date                YYYY-MM-DD, one row per trading day, strictly increasing
  close               the closing price (information only)
  total_return_index  a daily total return index, dividends reinvested (Bloomberg TOT_RETURN_INDEX_GROSS_DVDS)
Rows with an empty total_return_index (holidays in a terminal export) are dropped and counted. Anything else that is
wrong stops the load with the file name and the problem: a missing or extra column, a bad date, a repeated or
out-of-order date, a non-positive index. data/raw/manual_prices/SOURCES.md must name every file (who pulled it, from
which terminal, when, and the security identifier); a file it does not mention gives a warning.
The daily total return is total_return_index(t) / total_return_index(t-1) - 1; the index itself becomes the
`adj_close` column of data/processed/prices.csv.gz for that symbol (only ratios are ever used).
The last date is compared with the symbol's delisting date (the last SEC Form 25 in
data/interim/ledger_sec_evidence.csv): a history that ends more than MAX_GAP_DAYS calendar days away from it is
reported with a warning, because an old ticker is often reused by another company.
"""
from __future__ import annotations

import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

MANUAL_DIR = Path("data/raw/manual_prices")
COLUMNS = ["date", "close", "total_return_index"]
MAX_GAP_DAYS = 7          # a Form 25 is filed about ten days before the delisting takes effect; the last trade is near it


class ManualPriceError(ValueError):
    pass


def read_file(path: Path) -> tuple[pd.DataFrame, dict]:
    """One validated file -> (frame with date, close, adj_close, ret; info)."""
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    cols = [c.strip() for c in df.columns]
    if cols != COLUMNS:
        raise ManualPriceError(f"{path}: columns must be exactly {COLUMNS}, found {cols}")
    df.columns = cols
    df = df.apply(lambda s: s.str.strip())
    blank = df["total_return_index"] == ""
    df = df[~blank]
    bad = ~df["date"].str.fullmatch(r"\d{4}-\d{2}-\d{2}")
    if bad.any():
        raise ManualPriceError(f"{path}: dates must be YYYY-MM-DD; first bad value {df.loc[bad, 'date'].iat[0]!r}")
    try:
        pd.to_datetime(df["date"], format="%Y-%m-%d")
    except ValueError as e:
        raise ManualPriceError(f"{path}: not a real date ({e})") from None
    if df["date"].duplicated().any():
        raise ManualPriceError(f"{path}: repeated date {df.loc[df['date'].duplicated(), 'date'].iat[0]}")
    if not df["date"].is_monotonic_increasing:
        raise ManualPriceError(f"{path}: dates must be in increasing order")
    tri = pd.to_numeric(df["total_return_index"], errors="coerce")
    close = pd.to_numeric(df["close"].replace("", np.nan), errors="coerce")
    if tri.isna().any() or (tri <= 0).any():
        raise ManualPriceError(f"{path}: total_return_index must be a positive number on every row")
    out = pd.DataFrame({"date": df["date"].to_numpy(), "close": close.to_numpy(), "adj_close": tri.to_numpy()})
    out["ret"] = out["adj_close"] / out["adj_close"].shift(1) - 1
    info = {"file": str(path), "rows": len(out), "blank_rows_dropped": int(blank.sum()),
            "first_date": out["date"].iat[0] if len(out) else "", "last_date": out["date"].iat[-1] if len(out) else ""}
    return out, info


def load(directory: Path = MANUAL_DIR, delisted: dict[str, str] | None = None, end: str | None = None) -> tuple[dict, pd.DataFrame]:
    """{symbol: frame} for every CSV in `directory`, and a report (one row per file, with warnings)."""
    frames, report = {}, []
    if not directory.exists():
        return frames, pd.DataFrame(columns=["symbol", "file", "rows", "first_date", "last_date", "warnings"])
    sources_md = (directory / "SOURCES.md").read_text() if (directory / "SOURCES.md").exists() else ""
    delisted = delisted or {}
    for path in sorted(directory.glob("*.csv")):
        sym = path.stem.upper()
        df, info = read_file(path)
        if end:
            df = df[df["date"] <= end]
        warn = []
        if not re.search(rf"(?<![A-Z0-9.-]){re.escape(sym)}(?![A-Z0-9-])", sources_md, flags=re.I):
            warn.append("not listed in SOURCES.md")
        d = delisted.get(sym)
        if d and len(df):
            gap = abs((pd.Timestamp(df["date"].iat[-1]) - pd.Timestamp(d)).days)
            info["delisting_date"], info["days_from_delisting"] = d, gap
            if gap > MAX_GAP_DAYS:
                warn.append(f"history ends {df['date'].iat[-1]}, {gap} days from the delisting date {d}: check it is the "
                            "same company (tickers are reused)")
        if info["blank_rows_dropped"]:
            warn.append(f"{info['blank_rows_dropped']} rows with an empty total_return_index dropped")
        for w in warn:
            warnings.warn(f"manual prices {sym}: {w}", stacklevel=2)
        frames[sym] = df
        report.append({"symbol": sym, **info, "warnings": "; ".join(warn)})
    return frames, pd.DataFrame(report)
