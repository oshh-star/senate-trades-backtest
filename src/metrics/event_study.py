"""Event study (Phase 5) from data/processed/event_panel.csv (built by the engine, panel.py).

For PURCHASES and SALES separately, at each horizon h (trading days), SPY-adjusted returns (stock minus SPY over
exactly the same days, simple difference):
  senator   from the close on the TRANSACTION date (x_txn_h): what the senator's trade earned
  copier    from the close on the ENTRY date, the first trading day after disclosure (x_entry_h): what a copier earns
  gap       senator minus copier, event by event (x_txn_h - x_entry_h), on events that have both
and, once per side, the pre-disclosure move: SPY-adjusted return from the transaction-date close to the
entry-date close (gap_x). Mean, median and N; t-statistics with standard errors clustered by calendar month of
ENTRY (overlapping events are not independent), and the plain iid t for comparison. Every event counts once
(equal weight), whether or not the copier could act on it (an ignored sale is still a signal). Horizons that run
past the last in-sample day are censored, so N falls with h.
SIGN CONVENTION: returns are the stock's, whatever the side. A POSITIVE mean after a purchase means the stock beat
SPY (informative purchase); a NEGATIVE mean after a sale means the stock trailed SPY (informative sale).
"""
from __future__ import annotations

import pandas as pd

from .stats import clustered_mean

VERSIONS = [("senator (from transaction date)", "x_txn_{h}"), ("copier (from entry date)", "x_entry_{h}")]


def table(panel: pd.DataFrame, horizons: list[int]) -> pd.DataFrame:
    rows = []
    p = panel.copy()
    p["entry_month"] = p["entry_date"].str[:7]
    for side in ("purchase", "sale"):
        q = p[p["side"] == side]
        pre = clustered_mean(q["gap_x"], q["entry_month"])
        rows.append({"side": side, "horizon_days": 0, "version": "pre-disclosure move (transaction close to entry close)", **pre})
        for h in horizons:
            for name, col in VERSIONS:
                rows.append({"side": side, "horizon_days": h, "version": name,
                             **clustered_mean(q[col.format(h=h)], q["entry_month"])})
            both = q[q[f"x_txn_{h}"].notna() & q[f"x_entry_{h}"].notna()]
            rows.append({"side": side, "horizon_days": h, "version": "gap (senator minus copier)",
                         **clustered_mean(both[f"x_txn_{h}"] - both[f"x_entry_{h}"], both["entry_month"])})
    return pd.DataFrame(rows)


def drift_table(panel: pd.DataFrame) -> pd.DataFrame:
    """Pre-disclosure drift (5A.2): the SPY-adjusted return from the transaction-date close to the entry-date close,
    for purchases and sales separately, with the raw stock and SPY returns over the same days and the lag. The
    copier's cost is the drift for a purchase (the price ran up before the copier could buy) and minus the drift for a
    sale (the price fell before the copier could sell); its t-statistic is the drift's with the sign flipped."""
    import numpy as np
    p = panel.copy()
    p["entry_month"] = p["entry_date"].str[:7]
    rows = []
    for side in ("purchase", "sale"):
        q = p[(p["side"] == side) & p["gap_x"].notna()]
        c = clustered_mean(q["gap_x"], q["entry_month"])
        sign = 1 if side == "purchase" else -1
        rows.append({"side": side, "N": c["n"], "months (clusters)": c["clusters"],
                     "mean SPY-adjusted drift": c["mean"], "median SPY-adjusted drift": c["median"],
                     "t (clustered by entry month)": c["t_cluster"], "t (iid)": c["t_iid"],
                     "mean stock return": float(q["gap_raw"].mean()), "mean SPY return": float(q["gap_spy"].mean()),
                     "median lag (trading days)": float(q["lag_trading_days"].median()),
                     "mean cost to the copier": sign * c["mean"],
                     "share of events against the copier": float((sign * q["gap_x"] > 0).mean()) if len(q) else np.nan})
    return pd.DataFrame(rows)
