"""The position book: FIFO lots per (senator, price symbol), built from the events day by day.

Rules (Phase 4 brief, D12, A03, E20/K1, J3, K3):
  Purchase        open a lot: dollars = the event's size, units = dollars / adjusted close on the entry
                  date. Adjusted closes include dividends, so every lot is a total-return position.
  Sale (Full)     close every open lot of that senator in that price symbol, regardless of owner.
  Sale (Partial)  sell units worth the event's size at that day's adjusted close, oldest lot first,
                  capped at what is held.
  Nothing held    a sale is ignored and logged (no shorting; this includes anything bought before the
                  window, because the book starts EMPTY on the window's first day).
  Reversal (J3)   a correction first undoes its predecessor's copied action: a purchase's lots still open
                  are sold ("reversal"); a sale's units are bought back as a new lot. Then the correction
                  acts itself if it is in scope.
  No price        a purchase needs an adjusted close on its exact entry date (E24). A symbol with no
                  usable history at all is in the survivorship ledger: skipped and logged (K3), or, with
                  engine.ledger_trades: spy_fill (V15), held as a lot that is valued with SPY. A symbol
                  with a history but no print that day is skipped and logged. A sale of a held symbol on
                  a day without a print uses the last available close (flagged).
  Series ends     a lot whose price series ends before the last day closes at the last available adjusted
                  close on that day ("series ended", E20).
  Last day        lots still open are marked at that day's close ("end of window").
Same-day order: the events' order (see events.py). Series that end are closed after the day's events.

Lots are written as PIECES: a partial sale splits a lot into a closed piece and the remainder, so every row
of lots.csv has one entry and one exit; entry dollars are split pro rata by units.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

EPS = 1e-9


@dataclass
class Lot:
    lot_id: str
    record_id: str
    bioguide_id: str
    senator: str
    price_ticker: str
    val_symbol: str
    entry_date: str
    entry_price: float
    units: float
    origin: str
    trade_id: str = ""
    open_units: float = field(init=False)
    pieces: int = field(default=0, init=False)

    def __post_init__(self):
        self.open_units = self.units


class Prices:
    """Adjusted closes by (symbol, date), exact and carried forward. Built only from rows up to the last
    day the engine may see (the OOS firewall trims the input before it gets here)."""

    def __init__(self, px: pd.DataFrame, calendar: list[str], last_dates: dict[str, str]):
        self.cal = list(calendar)
        self.pos = {d: i for i, d in enumerate(self.cal)}
        wide = px.pivot(index="date", columns="ticker", values="adj_close").reindex(self.cal)
        wide = wide.where(wide > 0)
        self.exact = wide
        self.ffill = wide.ffill()
        self.last_dates = dict(last_dates)
        self.symbols = set(wide.columns[wide.notna().any()])

    def has(self, sym: str) -> bool:
        return sym in self.symbols

    def at(self, sym: str, date: str) -> float:
        if sym not in self.exact.columns:
            return np.nan
        return float(self.exact.at[date, sym])

    def last(self, sym: str, date: str) -> float:
        if sym not in self.ffill.columns:
            return np.nan
        return float(self.ffill.at[date, sym])


def simulate(events: pd.DataFrame, prices: Prices, days: list[str], ledger_mode: str = "skip",
             fill_symbol: str = "SPY") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run the book over `days` (the trading days of the sample, in order). Returns (pieces, event_log)."""
    first, last_day = days[0], days[-1]
    open_lots: dict[tuple, list[Lot]] = {}
    acted: dict[str, tuple] = {}            # record_id -> ("bought", [Lot]) | ("sold", [(Lot, units)])
    pieces, log = [], []
    by_day = {d: g for d, g in events.groupby("entry_date", sort=False)}
    n_lot = 0

    def close_piece(lot: Lot, units: float, date: str, price: float, reason: str, record_id: str, flag: str = ""):
        lot.pieces += 1
        lot.open_units -= units
        if lot.open_units < EPS:
            lot.open_units = 0.0
        pieces.append({"lot_id": lot.lot_id, "piece": lot.pieces, "record_id": lot.record_id, "trade_id": lot.trade_id,
                       "bioguide_id": lot.bioguide_id, "senator": lot.senator, "price_ticker": lot.price_ticker,
                       "val_symbol": lot.val_symbol, "origin": lot.origin, "entry_date": lot.entry_date,
                       "entry_price": lot.entry_price, "units": units, "entry_dollars": units * lot.entry_price,
                       "exit_date": date, "exit_price": price, "exit_value": units * price, "exit_reason": reason,
                       "exit_record_id": record_id, "exit_flag": flag})

    def held(key) -> list[Lot]:
        return [l for l in open_lots.get(key, []) if l.open_units > EPS]

    def sell(key, units_wanted: float | None, date: str, reason: str, record_id: str) -> list[tuple]:
        """FIFO sale; units_wanted None = everything. Returns [(lot, units)]."""
        out = []
        lots = held(key)
        if not lots:
            return out
        sym = lots[0].val_symbol
        p = prices.at(sym, date)
        flag = ""
        if not np.isfinite(p):
            p, flag = prices.last(sym, date), "no print that day: last available close used"
        left = np.inf if units_wanted is None else units_wanted
        for lot in lots:
            if left <= EPS:
                break
            u = min(lot.open_units, left)
            close_piece(lot, u, date, p, reason, record_id, flag)
            out.append((lot, u))
            left -= u
        open_lots[key] = held(key)
        return out

    def new_lot(e, sym: str, val_sym: str, date: str, price: float, units: float, origin: str) -> Lot:
        nonlocal n_lot
        n_lot += 1
        lot = Lot(f"L{n_lot:05d}", e.record_id, e.bioguide_id, e.senator, sym, val_sym, date, price, units, origin, e.trade_id)
        open_lots.setdefault((e.bioguide_id, sym), []).append(lot)
        return lot

    for d in days:
        for e in (by_day[d].itertuples() if d in by_day else []):
            key = (e.bioguide_id, e.price_ticker)
            base = {"event_no": e.event_no, "record_id": e.record_id, "trade_id": e.trade_id, "entry_date": d,
                    "senator": e.senator, "price_ticker": e.price_ticker, "transaction_type": e.transaction_type}
            # (a) J3 reversal of the predecessor's copied action
            if e.reverse_prev and e.prev_record_id in acted:
                kind, what = acted.pop(e.prev_record_id)
                if kind == "bought":
                    n = 0.0
                    for lot in what:
                        if lot.open_units > EPS:
                            k2 = (lot.bioguide_id, lot.price_ticker)
                            p = prices.at(lot.val_symbol, d)
                            flag = ""
                            if not np.isfinite(p):
                                p, flag = prices.last(lot.val_symbol, d), "no print that day: last available close used"
                            n += lot.open_units * p
                            close_piece(lot, lot.open_units, d, p, "reversal", e.record_id, flag)
                            open_lots[k2] = held(k2)
                    log.append({**base, "action": "reversal: sold what was still held of the corrected purchase",
                                "reversed_record_id": e.prev_record_id, "dollars": n})
                else:
                    units = sum(u for _, u in what)
                    lot0 = what[0][0]
                    p = prices.at(lot0.val_symbol, d)
                    if not np.isfinite(p):
                        p = prices.last(lot0.val_symbol, d)
                    if units > EPS and np.isfinite(p):
                        lot = new_lot(e, lot0.price_ticker, lot0.val_symbol, d, p, units, f"reversal buy-back of {e.prev_record_id}")
                        lot.bioguide_id, lot.senator = lot0.bioguide_id, lot0.senator
                    log.append({**base, "action": "reversal: bought back the units the corrected sale sold",
                                "reversed_record_id": e.prev_record_id, "dollars": units * p if np.isfinite(p) else np.nan})
            elif e.reverse_prev:
                log.append({**base, "action": "reversal: nothing to undo (the corrected record was not acted on)",
                            "reversed_record_id": e.prev_record_id})
            if not e.act:
                continue
            # (b) act on the record
            if e.transaction_type == "Purchase":
                p = prices.at(e.price_ticker, d)
                if np.isfinite(p):
                    lot = new_lot(e, e.price_ticker, e.price_ticker, d, p, e.size / p, "purchase")
                    acted[e.record_id] = ("bought", [lot])
                    log.append({**base, "action": "bought", "dollars": e.size, "price": p, "lot_id": lot.lot_id})
                elif not prices.has(e.price_ticker):
                    if ledger_mode == "spy_fill" and np.isfinite(prices.at(fill_symbol, d)):
                        pf = prices.at(fill_symbol, d)
                        lot = new_lot(e, e.price_ticker, fill_symbol, d, pf, e.size / pf, f"V15 neutral fill ({fill_symbol})")
                        acted[e.record_id] = ("bought", [lot])
                        log.append({**base, "action": f"bought (V15: valued with {fill_symbol})", "dollars": e.size,
                                    "price": pf, "lot_id": lot.lot_id})
                    else:
                        log.append({**base, "action": "skipped: survivorship ledger (no usable prices)", "dollars": e.size})
                else:
                    log.append({**base, "action": "skipped: no price on the entry date", "dollars": e.size})
            elif e.transaction_type in ("Sale (Full)", "Sale (Partial)"):
                if not held(key):
                    why = "ignored: nothing held"
                    if any(pc["bioguide_id"] == e.bioguide_id and pc["price_ticker"] == e.price_ticker for pc in pieces):
                        why += " (earlier copied lots already closed)"
                    log.append({**base, "action": why, "dollars": e.size})
                    continue
                if e.transaction_type == "Sale (Full)":
                    sold = sell(key, None, d, "senator sale", e.record_id)
                else:
                    sym = held(key)[0].val_symbol
                    p = prices.at(sym, d)
                    if not np.isfinite(p):
                        p = prices.last(sym, d)
                    sold = sell(key, e.size / p, d, "senator sale", e.record_id)
                acted[e.record_id] = ("sold", sold)
                log.append({**base, "action": "sold " + ("all" if e.transaction_type == "Sale (Full)" else "part"),
                            "dollars": sum(u for _, u in sold) * pieces[-1]["exit_price"], "price": pieces[-1]["exit_price"],
                            "lots_touched": len(sold)})
            else:
                log.append({**base, "action": f"ignored: transaction type {e.transaction_type!r}"})
        # E20: series that end today close at today's (last) close
        for key, lots in list(open_lots.items()):
            for lot in held(key):
                ld = prices.last_dates.get(lot.val_symbol, "")
                if ld and ld == d and d < last_day:
                    close_piece(lot, lot.open_units, d, prices.at(lot.val_symbol, d), "series ended", "")
            open_lots[key] = held(key)
    # end of the sample: mark to market
    for key, lots in open_lots.items():
        for lot in held(key):
            p = prices.last(lot.val_symbol, last_day)
            close_piece(lot, lot.open_units, last_day, p, "end of window", "",
                        "" if np.isfinite(prices.at(lot.val_symbol, last_day)) else "no print that day: last available close used")
    cols = ["lot_id", "piece", "record_id", "trade_id", "bioguide_id", "senator", "price_ticker", "val_symbol", "origin",
            "entry_date", "entry_price", "units", "entry_dollars", "exit_date", "exit_price", "exit_value", "exit_reason",
            "exit_record_id", "exit_flag"]
    pc = pd.DataFrame(pieces, columns=cols)
    pc["pnl"] = pc["exit_value"] - pc["entry_dollars"]
    pc["return"] = pc["exit_price"] / pc["entry_price"] - 1
    pos = {dd: i for i, dd in enumerate(prices.cal)}
    pc["holding_trading_days"] = [pos[b] - pos[a] for a, b in zip(pc["entry_date"], pc["exit_date"])]
    pc["holding_calendar_days"] = (pd.to_datetime(pc["exit_date"]) - pd.to_datetime(pc["entry_date"])).dt.days
    lg = pd.DataFrame(log)
    for c in ("reversed_record_id", "dollars", "price", "lot_id", "lots_touched"):
        if c not in lg:
            lg[c] = np.nan
    return pc.sort_values(["lot_id", "piece"]).reset_index(drop=True), lg
