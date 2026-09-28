"""K6: hand-listed repairs to Yahoo daily prices (config/price_repairs.yaml), applied before
data/processed/prices.csv.gz is written. Each changed row is logged."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

REPAIRS = Path("config/price_repairs.yaml")
LOG = Path("data/interim/price_repairs_log.csv")
LOG_COLUMNS = ["ticker", "date", "type", "close_before", "close_after", "adj_close_before", "adj_close_after", "note"]


def load(path: Path = REPAIRS) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for r in (yaml.safe_load(path.read_text()) or {}).get("repairs") or []:
        out.append({**r, "from": str(r["from"]), "to": str(r["to"])})
    return out


def apply(px: pd.DataFrame, ticker: str, repairs: list[dict]) -> tuple[pd.DataFrame, list[dict]]:
    """px: one symbol's rows (date, close, adj_close, ...) sorted by date. Returns (repaired px, log rows)."""
    mine = [r for r in repairs if r["ticker"] == ticker]
    if not mine or not len(px):
        return px, []
    px = px.sort_values("date").reset_index(drop=True).copy()
    log = []
    for r in mine:
        sel = (px["date"] >= r["from"]) & (px["date"] <= r["to"])
        for i in px.index[sel]:
            cb, ab = px.at[i, "close"], px.at[i, "adj_close"]
            if r["type"] == "scale":
                px.at[i, "close"], px.at[i, "adj_close"] = cb * r["factor"], ab * r["factor"]
            elif r["type"] == "carry_forward":
                if i == 0:
                    raise ValueError(f"{ticker}: cannot carry forward into the first row ({px.at[i, 'date']})")
                px.at[i, "close"], px.at[i, "adj_close"] = px.at[i - 1, "close"], px.at[i - 1, "adj_close"]
            else:
                raise ValueError(f"unknown repair type {r['type']!r}")
            log.append({"ticker": ticker, "date": px.at[i, "date"], "type": r["type"], "close_before": cb,
                        "close_after": px.at[i, "close"], "adj_close_before": ab, "adj_close_after": px.at[i, "adj_close"],
                        "note": r.get("note", "")})
    return px, log
