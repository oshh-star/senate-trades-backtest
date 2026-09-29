"""Events: one row per record the copier acts on (or reverses), with its entry date and size.

Headline (J3, as first published): every in-scope record of data/processed/trade_records.csv acts on its
entry date. A record that corrects an earlier one (record_no > 1) first REVERSES its predecessor's copied
action, if there was one, and then acts itself if it is in scope; so an out-of-scope correction whose
predecessor was in scope is kept as a reversal-only event. V14 ("as revised", data.amendment_values:
as_revised) uses trades_clean.csv instead: one record per trade, corrected values, first datetime.

Entry date (D11, trades.price_timing):
  next_close_after_disclosure  the first NYSE trading day strictly AFTER the disclosure date (headline)
  same_day_close               V9: the disclosure date itself when the filing is timestamped before
                               trades.same_day_cutoff_et on a trading day; otherwise as the headline
Same-day ordering (logged in DECISIONS.md, E29): entry date, then disclosure datetime, then transaction
date, then row number in the input file.
Size (trades.sizing): midpoint (amount_mid; the open top band uses its lower bound, D10) | lower_bound |
equal_dollar (trades.equal_dollar_amount).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

RECORDS = "data/processed/trade_records.csv"
TRADES_CLEAN = "data/processed/trades_clean.csv"
EVENT_COLUMNS = ["event_no", "record_id", "trade_id", "record_no", "prev_record_id", "act", "reverse_prev",
                 "bioguide_id", "senator", "owner", "ticker", "price_ticker", "asset_name", "transaction_type",
                 "transaction_date", "disclosure_datetime", "disclosure_date", "entry_date", "size", "amount",
                 "amount_mid", "is_etf", "is_otc", "row_no"]


def _bool(s: pd.Series) -> pd.Series:
    return s.astype(str) == "True"


def load_units(cfg: dict) -> pd.DataFrame:
    """The records the engine sees, with `act` (in scope) and variant filters applied."""
    tr = pd.read_csv(TRADES_CLEAN, keep_default_na=False, low_memory=False, dtype={"ticker": str, "price_ticker": str})
    if cfg["data"].get("amendment_values", "as_first_published") == "as_revised":
        u = tr.assign(record_id=tr["trade_id"] + ".r", record_no=1, n_records=1,
                      in_scope=tr["in_scope_as_revised"], in_scope_ex_window=tr["in_scope_ex_window_as_revised"])
    else:
        u = pd.read_csv(RECORDS, keep_default_na=False, dtype={"ticker": str, "price_ticker": str})
    u = u.reset_index(drop=True)
    u["row_no"] = np.arange(len(u))
    u["in_scope"] = _bool(u["in_scope"])
    u["in_scope_ex_window"] = _bool(u["in_scope_ex_window"])
    for c in ("is_etf", "is_otc", "filed_before_1530_et"):
        u[c] = _bool(u[c]) if c in u else False
    for c in ("amount_mid", "amount_lower", "record_no"):
        u[c] = pd.to_numeric(u[c], errors="coerce")
    drop = set()
    flags = tr.set_index("trade_id")
    for f in cfg.get("engine", {}).get("drop_flags") or []:
        drop |= set(flags.index[_bool(flags[f])])
    ranks = cfg.get("engine", {}).get("drop_senator_ranks") or []
    if ranks:
        rk = pd.to_numeric(flags["senator_rank"], errors="coerce")
        drop |= set(flags.index[rk.isin(ranks)])
    u["dropped_by_variant"] = u["trade_id"].isin(drop)
    return u


def add_warmup(u: pd.DataFrame, warm_start: str, window_start: str) -> pd.DataFrame:
    """L2: records disclosed in [warm_start, window_start) that pass every scope filter except the window act too."""
    u = u.copy()
    warm = u["in_scope_ex_window"] & (u["disclosure_date"] >= warm_start) & (u["disclosure_date"] < window_start)
    u["warmup"] = warm & ~u["in_scope"]
    u["in_scope"] = u["in_scope"] | warm
    return u


def size_of(u: pd.DataFrame, cfg: dict) -> pd.Series:
    rule = cfg["trades"]["sizing"]
    if rule == "midpoint":
        return u["amount_mid"]
    if rule == "lower_bound":
        return u["amount_lower"]
    if rule == "equal_dollar":
        return pd.Series(float(cfg["trades"]["equal_dollar_amount"]), index=u.index)
    raise ValueError(f"unknown trades.sizing {rule!r}")


def entry_dates(u: pd.DataFrame, calendar: list[str], cfg: dict) -> pd.Series:
    cal = np.array(sorted(calendar))
    after = np.searchsorted(cal, u["disclosure_date"].to_numpy(dtype=str), side="right")
    nxt = pd.Series([cal[i] if i < len(cal) else "" for i in after], index=u.index)
    timing = cfg["trades"]["price_timing"]
    if timing == "next_close_after_disclosure":
        return nxt
    if timing == "same_day_close":
        cut = str(cfg["trades"].get("same_day_cutoff_et", "15:30"))
        t = u["disclosure_datetime"].str[11:16]
        same = (t != "") & (t < cut) & u["disclosure_date"].isin(set(cal))
        return pd.Series(np.where(same, u["disclosure_date"], nxt), index=u.index)
    raise ValueError(f"unknown trades.price_timing {timing!r}")


def build_events(u: pd.DataFrame, calendar: list[str], cfg: dict, last_entry: str) -> pd.DataFrame:
    """Events with entry date <= last_entry, in execution order."""
    u = u[~u["dropped_by_variant"]].copy()
    u["entry_date"] = entry_dates(u, calendar, cfg)
    u["size"] = size_of(u, cfg)
    u = u.sort_values(["trade_id", "record_no"])
    u["prev_record_id"] = u.groupby("trade_id")["record_id"].shift(1).fillna("")
    prev_in = u.groupby("trade_id")["in_scope"].shift(1).eq(True)
    u["act"] = u["in_scope"]
    u["reverse_prev"] = (u["record_no"] > 1) & prev_in
    ev = u[(u["act"] | u["reverse_prev"]) & (u["entry_date"] != "") & (u["entry_date"] <= last_entry)].copy()
    ev = ev.sort_values(["entry_date", "disclosure_datetime", "transaction_date", "row_no"]).reset_index(drop=True)
    ev["event_no"] = np.arange(1, len(ev) + 1)
    return ev[[c for c in EVENT_COLUMNS if c in ev.columns]]
