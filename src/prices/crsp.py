"""CRSP daily stock data from a WRDS web-query export (A04, M2: source 1 of 3). Settings: docs/PRICE_REQUEST.md.

Input: every *.csv / *.csv.gz in data/raw/crsp/, with (case-insensitive) columns
  PERMNO, date, TICKER, COMNAM, PRC, RET, DLRET          (CRSP legacy "Daily Stock File")
The CRSP v2 ("CIZ") names are accepted too: DlyCalDt -> date, DlyPrc -> PRC, DlyRet -> RET, Ticker -> TICKER,
IssuerNm -> COMNAM; v2 has no DLRET because DlyRet already includes the delisting return.
Rules:
  - date: YYYYMMDD or YYYY-MM-DD.
  - PRC: a negative price is CRSP's bid/ask midpoint (no trade that day); its absolute value is the close.
  - RET / DLRET: letter codes (A, B, C, P, S, T, ...) and the missing codes -66, -77, -88, -99 are missing.
  - the daily total return is RET; on the delisting day (a non-missing DLRET) it is (1 + RET)(1 + DLRET) - 1, or
    DLRET alone when RET is missing (the delisting row often has no price).
  - the total return index starts at |PRC| on the PERMNO's first row and compounds the daily total return; it becomes
    the `adj_close` of data/processed/prices.csv.gz (only ratios are ever used). A day with no return carries the
    index flat, and is counted.
Mapping to this project's symbols: a PERMNO is a security, a ticker is only a label that CRSP records by date and
that companies reuse. For each project symbol, the candidate tickers are the symbol and every eFD ticker that maps
to it; the PERMNO chosen is the one with the most rows carrying a candidate ticker INSIDE the dates the project needs
(docs/PRICE_REQUEST.md). config/crsp_permnos.yaml (symbol: PERMNO) overrides the choice by hand. Every choice, and
every symbol with more than one candidate PERMNO, is reported.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import yaml

CRSP_DIR = Path("data/raw/crsp")
PERMNO_OVERRIDES = Path("config/crsp_permnos.yaml")
ALIASES = {"dlycaldt": "date", "dlyprc": "prc", "dlyret": "ret", "issuernm": "comnam", "caldt": "date"}
REQUIRED = ["permno", "date", "ticker", "comnam", "prc", "ret"]
MISSING_CODES = {-66.0, -77.0, -88.0, -99.0}


class CrspError(ValueError):
    pass


def _num(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    return x.where(~x.isin(MISSING_CODES))


def read(paths: list[Path]) -> pd.DataFrame:
    """All export files -> one clean frame: permno, date, ticker, comnam, close, ret_total, dlret."""
    frames = []
    for p in paths:
        df = pd.read_csv(p, dtype=str, keep_default_na=False)
        df.columns = [ALIASES.get(c.strip().lower(), c.strip().lower()) for c in df.columns]
        missing = [c for c in REQUIRED if c not in df.columns]
        if missing:
            raise CrspError(f"{p}: missing columns {missing} (found {list(df.columns)})")
        if "dlret" not in df.columns:
            df["dlret"] = ""
        d = df["date"].str.replace("-", "", regex=False).str.strip()
        ok = d.str.fullmatch(r"\d{8}")
        if not ok.all():
            raise CrspError(f"{p}: dates must be YYYYMMDD or YYYY-MM-DD; first bad {df.loc[~ok, 'date'].iat[0]!r}")
        out = pd.DataFrame({"permno": df["permno"].str.strip(), "date": d.str[:4] + "-" + d.str[4:6] + "-" + d.str[6:],
                            "ticker": df["ticker"].str.strip().str.upper(), "comnam": df["comnam"].str.strip(),
                            "close": _num(df["prc"]).abs(), "ret": _num(df["ret"]), "dlret": _num(df["dlret"])})
        frames.append(out)
    if not frames:
        return pd.DataFrame(columns=["permno", "date", "ticker", "comnam", "close", "ret", "dlret", "ret_total"])
    x = pd.concat(frames, ignore_index=True).drop_duplicates(["permno", "date"], keep="last")
    x = x.sort_values(["permno", "date"]).reset_index(drop=True)
    has_dl = x["dlret"].notna()
    x["ret_total"] = np.where(has_dl, (1 + x["ret"].fillna(0)) * (1 + x["dlret"]) - 1, x["ret"])
    return x


def index_series(g: pd.DataFrame) -> pd.DataFrame:
    """One PERMNO's rows -> date, close, adj_close (total return index), ret, flat_days."""
    g = g.sort_values("date")
    r = g["ret_total"].to_numpy(dtype=float).copy()
    flat = np.isnan(r)
    flat[0] = False
    r[0] = 0.0
    r[np.isnan(r)] = 0.0
    start = g["close"].dropna()
    base = float(start.iat[0]) if len(start) else 1.0
    tri = base * np.cumprod(1 + r)
    out = pd.DataFrame({"date": g["date"].to_numpy(), "close": g["close"].to_numpy(), "adj_close": tri,
                        "ret": np.r_[np.nan, r[1:]]})
    out.attrs["flat_days"] = int(flat.sum())
    return out


def choose_permnos(x: pd.DataFrame, wanted: dict[str, dict]) -> tuple[dict, pd.DataFrame]:
    """wanted: {symbol: {"tickers": set, "first": date, "last": date}} -> ({symbol: permno}, report)."""
    hand = {}
    if PERMNO_OVERRIDES.exists():
        hand = {str(k).upper(): str(v) for k, v in (yaml.safe_load(PERMNO_OVERRIDES.read_text()) or {}).items()}
    chosen, rows = {}, []
    for sym, w in wanted.items():
        tick = {t.upper() for t in w["tickers"]} | {sym.upper()}
        hit = x[x["ticker"].isin(tick)]
        inside = hit[(hit["date"] >= w["first"]) & (hit["date"] <= w["last"])]
        counts = inside.groupby("permno").size().sort_values(ascending=False)
        cands = sorted(set(hit["permno"]))
        if sym in hand:
            pick, how = hand[sym], "by hand (config/crsp_permnos.yaml)"
        elif len(counts):
            pick, how = counts.index[0], "most rows with a matching ticker inside the dates needed"
        else:
            pick, how = None, "no PERMNO with a matching ticker inside the dates needed"
        if pick is not None:
            chosen[sym] = pick
        names = sorted(set(x.loc[x["permno"] == pick, "comnam"])) if pick is not None else []
        rows.append({"symbol": sym, "permno": pick or "", "how": how, "candidate_permnos": " ".join(cands),
                     "several_candidates": len(cands) > 1, "crsp_names": " | ".join(names[:3])})
    return chosen, pd.DataFrame(rows)


def load(wanted: dict[str, dict], directory: Path = CRSP_DIR, end: str | None = None) -> tuple[dict, pd.DataFrame]:
    """{symbol: frame (date, close, adj_close, ret)} for the symbols CRSP covers, and the mapping report."""
    paths = sorted(list(directory.glob("*.csv")) + list(directory.glob("*.csv.gz"))) if directory.exists() else []
    x = read(paths)
    if not len(x):
        return {}, pd.DataFrame(columns=["symbol", "permno", "how", "candidate_permnos", "several_candidates", "crsp_names"])
    chosen, rep = choose_permnos(x, wanted)
    frames = {}
    for sym, pn in chosen.items():
        s = index_series(x[x["permno"] == pn])
        if end:
            s = s[s["date"] <= end]
        if len(s):
            frames[sym] = s
    rep["flat_days"] = rep["symbol"].map({k: v.attrs.get("flat_days", 0) for k, v in frames.items()}).fillna(0).astype(int)
    return frames, rep
