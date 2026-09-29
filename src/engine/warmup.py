"""Warm-up diagnostics (L2) and the ledger exposure diagnostic (L3).

book_summary       the book measures Harry asked to compare before and after the warm-up: sales ignored because
                   nothing was held, open lots and capital deployed (min / median / max over the window), and the
                   share of dollars still held on the last day.
empty_start_book   the V17 book (the Phase 4 rule: empty on the window's first day), rebuilt from the same events,
                   for that comparison only (book counts, no returns).
ledger_exposure    L3: the cost basis of skipped survivorship-ledger purchases that would still be held, applying the
                   senators' disclosed sales, as a share of capital deployed at each close. Phantom lots are kept at
                   COST: a purchase adds its size; Sale (Full) removes every phantom lot of that senator and symbol; Sale
                   (Partial) removes its size at cost, oldest first, capped at what is held; a J3 correction of a phantom
                   purchase removes what is left of it. Nothing closes a phantom lot at the company's delisting, so this
                   is an UPPER bound on the dollars that would still be held. A second column also drops each phantom
                   lot after its symbol's LAST SEC Form 25 delisting date where one is known (earlier Form 25s can be
                   exchange moves; data/interim/ledger_sec_evidence.csv).
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from . import book as bk
from . import portfolio as pf


def book_summary(pieces: pd.DataFrame, log: pd.DataFrame, daily: pd.DataFrame, first: str) -> dict:
    lw = log[log["entry_date"] >= first]
    sales = lw[lw["transaction_type"].isin(["Sale (Full)", "Sale (Partial)"]) & ~lw["action"].str.startswith("reversal")]
    ign = sales[sales["action"].str.startswith("ignored: nothing held")]
    eow = pieces[pieces["exit_reason"] == "end of window"]
    in_win = pieces[pieces["entry_date"] >= first]
    eow_win = in_win[in_win["exit_reason"] == "end of window"]
    return {"sale records in the window": len(sales), "sales ignored: nothing held": len(ign),
            "sales ignored (share)": len(ign) / max(len(sales), 1),
            "sales matched to a copied position": int(sales["action"].str.startswith("sold").sum()),
            "open lots: min": daily["open_lots"].min(), "open lots: median": daily["open_lots"].median(),
            "open lots: max": daily["open_lots"].max(),
            "capital deployed: min ($)": daily["capital_deployed"].min(),
            "capital deployed: median ($)": daily["capital_deployed"].median(),
            "capital deployed: max ($)": daily["capital_deployed"].max(),
            "days with no open lot": int(daily["idle_day"].sum()),
            "lots held on the last day": eow["lot_id"].nunique(),
            "share of dollars ever invested still held on the last day (at cost)":
                eow["entry_dollars"].sum() / pieces["entry_dollars"].sum(),
            "share still held on the last day, lots bought inside the window only (at cost)": eow_win["entry_dollars"].sum() / max(in_win["entry_dollars"].sum(), 1e-9),
            "value held on the last day ($)": eow["exit_value"].sum()}


def empty_start_book(events: pd.DataFrame, prices: bk.Prices, days: list[str], ledger_mode: str) -> dict:
    """V17: the book from the window's events only, empty on the first day."""
    pieces, log = bk.simulate(events, prices, days, ledger_mode=ledger_mode)
    m = pf._matrix(pieces, prices.ffill, days)
    daily = pd.DataFrame({"date": days, "open_lots": pf.open_lot_counts(pieces, days), "capital_deployed": m["capital"],
                          "idle_day": ~(m["vprev"] > 0)})
    return {"pieces": pieces, "log": log, "daily": daily}


SEC_EVIDENCE = Path("data/interim/ledger_sec_evidence.csv")


def delisting_dates(path: Path = SEC_EVIDENCE) -> dict[str, str]:
    """Last Form 25 (25-NSE / 25) date per ledger symbol, from the SEC evidence file (K4)."""
    if not path.exists():
        return {}
    ev = pd.read_csv(path, dtype=str, keep_default_na=False)
    out = {}
    for t, txt in zip(ev["price_ticker"], ev["evidence"]):
        ds = re.findall(r"\b25(?:-NSE)? (\d{4}-\d{2}-\d{2})", txt)
        if ds:
            out[t] = max(ds)
    return out


def ledger_exposure(events: pd.DataFrame, log: pd.DataFrame, book_days: list[str], daily: pd.DataFrame,
                    delisted: dict[str, str] | None = None) -> pd.DataFrame:
    """Daily phantom cost basis (at each close) over the window days of `daily`."""
    delisted = delisting_dates() if delisted is None else delisted
    skipped = set(log.loc[log["action"].str.startswith("skipped: survivorship ledger"), "record_id"])
    lots: dict[tuple, list[list]] = {}                 # key -> [[record_id, cost], ...]
    held = {}
    by_day = {d: g for d, g in events.groupby("entry_date", sort=False)}
    for d in book_days:
        for e in (by_day[d].itertuples() if d in by_day else []):
            key = (e.bioguide_id, e.price_ticker)
            if e.reverse_prev and e.prev_record_id:
                for k, ls in lots.items():
                    lots[k] = [l for l in ls if l[0] != e.prev_record_id]
            if not e.act:
                continue
            if e.transaction_type == "Purchase" and e.record_id in skipped:
                lots.setdefault(key, []).append([e.record_id, float(e.size)])
            elif e.transaction_type == "Sale (Full)" and lots.get(key):
                lots[key] = []
            elif e.transaction_type == "Sale (Partial)" and lots.get(key):
                left = float(e.size)
                for l in lots[key]:
                    take = min(l[1], left)
                    l[1] -= take
                    left -= take
                    if left <= 0:
                        break
                lots[key] = [l for l in lots[key] if l[1] > 1e-9]
        alive = [l[1] for k, ls in lots.items() for l in ls if not (delisted.get(k[1]) and delisted[k[1]] < d)]
        held[d] = (sum(l[1] for ls in lots.values() for l in ls), sum(len(ls) for ls in lots.values()), sum(alive))
    out = daily[["date", "capital_deployed"]].copy()
    out["ledger_cost_held"] = [held[d][0] for d in out["date"]]
    out["ledger_lots_held"] = [held[d][1] for d in out["date"]]
    out["share_of_capital_deployed"] = out["ledger_cost_held"] / out["capital_deployed"].where(out["capital_deployed"] > 0)
    out["ledger_cost_held_to_delisting"] = [held[d][2] for d in out["date"]]
    out["share_to_delisting"] = out["ledger_cost_held_to_delisting"] / out["capital_deployed"].where(out["capital_deployed"] > 0)
    return out
