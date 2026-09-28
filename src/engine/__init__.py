"""Stage 'engine' (Phase 4): the copied position book, daily return series and the trade-level panel.

Reads data/processed/trade_records.csv (J3; trades_clean.csv for V14), prices.csv.gz, trading_calendar.csv,
factors_daily.csv (RF), price_coverage.csv (last date of each series) and data/interim/price_repairs_log.csv.
Writes (in-sample only while the OOS firewall is shut):
  data/processed/lots.csv          every copied lot piece: entry and exit, reason, holding days, return, P&L
  data/processed/daily_book.csv    date, open lots, capital deployed, series A and B returns, pot, RF, SPY
  data/processed/event_panel.csv   the trade-level panel (panel.py)
  data/processed/engine_events.csv what the book did with every event (bought, sold, ignored, skipped, reversed)
  data/processed/engine_metadata.json  definitions, sample, K, reconciliation, config snapshot
  outputs/figures/phase4_open_lots_capital.png, and the Phase 4 section of outputs/data_quality.md

Every setting comes from config/config.yaml; a variant is a config change, never a code change.

OUT-OF-SAMPLE FIREWALL: with engine.sample: in_sample (default), prices, RF and the calendar are cut at the
last in-sample day BEFORE anything is computed, and no event with a later entry date is used. sample: full
calls require_oos_unlocked(cfg) first.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import analysis_window, require_oos_unlocked, sample_split

PROCESSED = Path("data/processed")
LOTS = PROCESSED / "lots.csv"
DAILY = PROCESSED / "daily_book.csv"
PANEL = PROCESSED / "event_panel.csv"
EVENTS_OUT = PROCESSED / "engine_events.csv"
META = PROCESSED / "engine_metadata.json"


def sample_bounds(cfg: dict) -> tuple[str, str, str]:
    """(first day, last day, label) of the sample the engine may see."""
    start, end = analysis_window(cfg)
    mode = cfg.get("engine", {}).get("sample", "in_sample")
    if mode == "in_sample":
        a, b = sample_split(cfg)["in_sample"]
        return a.isoformat(), b.isoformat(), "in-sample"
    if mode == "full":
        require_oos_unlocked(cfg)
        return start.isoformat(), end.isoformat(), "full window"
    raise ValueError(f"unknown engine.sample {mode!r}")


def load_market(last_day: str) -> dict:
    """Prices, calendar and RF cut at last_day (the firewall)."""
    cal = pd.read_csv(PROCESSED / "trading_calendar.csv", dtype=str)["date"].tolist()
    px = pd.read_csv(PROCESSED / "prices.csv.gz", dtype={"ticker": str, "date": str}, keep_default_na=False,
                     na_values=[""])
    px = px[px["date"] <= last_day]
    cov = pd.read_csv(PROCESSED / "price_coverage.csv", keep_default_na=False)
    last_dates = {t: d for t, d, h in zip(cov["ticker"], cov["last_date"], cov["has_data"].astype(str)) if h == "True" and d}
    f = pd.read_csv(PROCESSED / "factors_daily.csv", dtype={"date": str})
    rf = dict(zip(f["date"], f["rf_pct"] / 100.0))
    return {"calendar_all": cal, "calendar": [d for d in cal if d <= last_day], "prices": px,
            "last_dates": last_dates, "rf": rf}


def run(cfg: dict) -> dict:
    from . import book as bk, diagnostics, events as evm, panel as pn, portfolio as pf
    first, last_day, label = sample_bounds(cfg)
    mk = load_market(last_day)
    days = [d for d in mk["calendar"] if d >= first]
    units = evm.load_units(cfg)
    ev = evm.build_events(units, mk["calendar_all"], cfg, last_entry=last_day)
    ev = ev[ev["entry_date"] >= first].reset_index(drop=True)
    prices = bk.Prices(mk["prices"], mk["calendar"], mk["last_dates"])
    mode = cfg.get("engine", {}).get("ledger_trades", "skip")
    pieces, log = bk.simulate(ev, prices, days, ledger_mode=mode)
    rf = np.array([mk["rf"].get(d, np.nan) for d in days])
    missing_rf = int(np.isnan(rf).sum())
    rf = np.nan_to_num(rf)
    spy = prices.ffill["SPY"].pct_change().reindex(days).to_numpy()
    daily, rec = pf.series(pieces, prices.ffill, days, rf, cfg["portfolio"]["weighting"], spy)
    hz = list(cfg["portfolio"]["event_study_horizons"])
    panel = pn.build(ev, log, prices.exact, prices.ffill, mk["calendar"], last_day, hz, mk["last_dates"])
    PROCESSED.mkdir(parents=True, exist_ok=True)
    pieces.to_csv(LOTS, index=False, float_format="%.6f")
    daily.to_csv(DAILY, index=False, float_format="%.10g")
    panel.to_csv(PANEL, index=False, float_format="%.8g")
    log.to_csv(EVENTS_OUT, index=False, float_format="%.6f")
    meta = {"stage": "engine (Phase 4)", "sample": label, "first_day": days[0], "last_day": days[-1], "trading_days": len(days),
            "oos_unlocked": bool(cfg["oos"]["oos_unlocked"]),
            "definitions": {"series_a": pf.DEFINITION_A if cfg["portfolio"]["weighting"] == "dollar" else pf.DEFINITION_A_EQUAL,
                            "series_b": pf.DEFINITION_B, "event_panel": pn.__doc__.strip(), "book_rules": bk.__doc__.strip(),
                            "events": evm.__doc__.strip()},
            "K_fixed_pot_dollars": rec["K"], "reconciliation": rec, "days_without_rf": missing_rf,
            "config": {k: cfg[k] for k in ("data", "analysis", "universe", "trades", "portfolio", "engine")}}
    META.write_text(json.dumps(meta, indent=1, default=str))
    out = {"events": ev, "pieces": pieces, "log": log, "daily": daily, "rec": rec, "panel": panel, "days": days,
           "prices": prices, "label": label, "horizons": hz, "missing_rf": missing_rf, "units": units}
    diagnostics.run(cfg, out)
    print(f"  [engine] {label} {days[0]}..{days[-1]} ({len(days)} days): {len(ev)} events -> {pieces['lot_id'].nunique()} lots "
          f"({len(pieces)} pieces); K = ${rec['K']:,.0f}; lot P&L ${rec['lot_pnl']:,.2f}; book - lots = "
          f"${rec['diff_book_minus_lots']:.6f}; panel {len(panel)} rows")
    return out
