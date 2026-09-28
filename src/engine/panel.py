"""Trade-level panel for the Phase 5 event study (D14, D16).

One row per in-scope PURCHASE and SALE record whose entry date falls in the sample (whether or not the
copier could act on it: an ignored sale is still a signal). Prices are adjusted closes (total return).
  r_entry_h   return from the close on the ENTRY date to the close h NYSE trading days later (the copier)
  r_txn_h     the same from the close on the TRANSACTION date (what the senator earned); a transaction
              date that is not a trading day uses the first trading day on or after it
  gap         return from the transaction-date close to the entry-date close: what the disclosure lag
              costs a copier
  x_*         the same minus SPY's return over exactly the same days (simple difference)
A horizon that runs past the last day of the sample is censored (blank); N per horizon is reported. If a
symbol's series ends before the horizon, its last close is carried forward (flag series_ended_in_horizon).
Records with no price on the start date are left blank (flag no_price).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def build(events: pd.DataFrame, log: pd.DataFrame, P_exact: pd.DataFrame, P_ffill: pd.DataFrame, calendar: list[str],
          last_day: str, horizons: list[int], last_dates: dict[str, str], bench: str = "SPY") -> pd.DataFrame:
    cal = np.array(calendar)
    pos = {d: i for i, d in enumerate(calendar)}
    last_i = pos[last_day]
    ev = events[events["act"] & events["transaction_type"].isin(["Purchase", "Sale (Full)", "Sale (Partial)"])].copy()
    act = log.drop_duplicates("record_id", keep="last").set_index("record_id")["action"] if len(log) else pd.Series(dtype=str)
    rev = set(log.loc[log["action"].str.startswith("reversal"), "reversed_record_id"].dropna()) if len(log) else set()
    rows = []
    B = P_ffill[bench].to_numpy() if bench in P_ffill else None

    def px(sym, i, exact=True):
        if sym not in P_exact.columns or i is None or i < 0:
            return np.nan
        return float((P_exact if exact else P_ffill)[sym].iat[i])

    for e in ev.itertuples():
        s = e.price_ticker
        ie = pos[e.entry_date]
        it = int(np.searchsorted(cal, e.transaction_date, side="left"))
        it = it if it < len(cal) and it <= last_i else None
        row = {"record_id": e.record_id, "trade_id": e.trade_id, "senator": e.senator, "bioguide_id": e.bioguide_id,
               "ticker": e.ticker, "price_ticker": s, "transaction_type": e.transaction_type,
               "side": "purchase" if e.transaction_type == "Purchase" else "sale", "size": e.size,
               "transaction_date": e.transaction_date, "disclosure_date": e.disclosure_date, "entry_date": e.entry_date,
               "txn_price_date": cal[it] if it is not None else "", "lag_trading_days": ie - it if it is not None else np.nan,
               "is_etf": e.is_etf, "is_otc": e.is_otc, "copier_action": act.get(e.record_id, ""),
               "reversed_later": e.record_id in rev}
        p_e, p_t = px(s, ie), px(s, it) if it is not None else np.nan
        row["no_price"] = not np.isfinite(p_e)
        ld = last_dates.get(s, "")
        row["gap_raw"] = p_e / p_t - 1 if np.isfinite(p_e) and np.isfinite(p_t) and it <= ie else np.nan
        row["gap_spy"] = B[ie] / B[it] - 1 if B is not None and it is not None and it <= ie else np.nan
        row["gap_x"] = row["gap_raw"] - row["gap_spy"]
        ended = False
        for h in horizons:
            for tag, i0, p0 in (("entry", ie, p_e), ("txn", it, p_t)):
                if i0 is None or i0 + h > last_i or not np.isfinite(p0):
                    row[f"r_{tag}_{h}"] = row[f"x_{tag}_{h}"] = np.nan
                    continue
                p1 = px(s, i0 + h, exact=False)
                if ld and cal[i0 + h] > ld:
                    ended = True
                r = p1 / p0 - 1
                row[f"r_{tag}_{h}"] = r
                row[f"x_{tag}_{h}"] = r - (B[i0 + h] / B[i0] - 1) if B is not None else np.nan
        row["series_ended_in_horizon"] = ended
        rows.append(row)
    return pd.DataFrame(rows)


def n_by_horizon(panel: pd.DataFrame, horizons: list[int]) -> pd.DataFrame:
    out = []
    for side in ("purchase", "sale"):
        p = panel[panel["side"] == side]
        for h in horizons:
            out.append({"side": side, "horizon_days": h, "N_from_entry": int(p[f"r_entry_{h}"].notna().sum()),
                        "N_from_transaction": int(p[f"r_txn_{h}"].notna().sum()),
                        "censored_entry": int((p[f"r_entry_{h}"].isna() & ~p["no_price"]).sum()),
                        "no_price": int(p["no_price"].sum())})
    return pd.DataFrame(out)
