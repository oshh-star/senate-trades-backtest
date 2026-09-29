"""Daily return series from the lot pieces (book.py).

A. HEADLINE, return on capital deployed (D15). With V_i(t) = units_i x adjusted close_i(t):
     r_A(t) = sum_i V_i(t-1) r_i(t) / sum_i V_i(t-1)
   over the pieces held INTO day t (entry date < t <= exit date): a lot bought on day t earns from t+1; a lot
   sold on day t earns day t's return, then leaves. On a day with no piece held into it, r_A(t) = RF(t)
   (Ken French daily RF). portfolio.weighting: equal (V10) replaces V_i(t-1) by equal weights per open LOT,
   reset to 1/N at the close of every day on which a lot was opened or closed, drifting with returns between.
B. FIXED POT, the investor framing. Cash C0 = the peak of cumulative net cash invested over the measurement
   period (purchases minus sale proceeds; end-of-window marks are not proceeds). The pot starts as the warm-up
   book at market value (L2; zero under V17) plus C0 in cash earning RF, so K = warm-up book + C0; purchases
   draw the cash down and sale proceeds refill it. NAV(t) = cash(t) + value of open lots; r_B(t) = NAV(t)/NAV(t-1) - 1.
WARM-UP (L2): the book may start before the measurement window (`start`). Every array is computed over the whole
book, then only days >= start are returned: the warm-up book is marked at the close of the last trading day before
`start`, so the first measured return is `start`'s own daily return and the first calendar month is complete.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

DEFINITION_A = ("Series A (headline): daily return on capital deployed. r_A(t) = sum_i V_i(t-1) r_i(t) / sum_i V_i(t-1) "
                "over copied lots held into day t (bought before t, sold on or after t); V = units x adjusted close, so "
                "returns include dividends. A lot bought on day t earns from t+1; a lot sold on day t earns day t's "
                "return, then leaves. Days with no open lot earn the Ken French daily risk-free rate.")
DEFINITION_A_EQUAL = ("Series A, equal weight (V10): as the headline, but each open lot gets weight 1/N, reset at the "
                      "close of every day on which a lot was opened or closed, drifting with returns in between.")
DEFINITION_B = ("Series B (fixed pot): one pot K = the warm-up book at market value at the start of the window (L2) plus "
                "C0 = peak cumulative net cash invested over the measurement period (purchases minus sale proceeds). "
                "The cash earns the risk-free rate; purchases draw it down, sale proceeds refill it. "
                "r_B(t) = NAV(t)/NAV(t-1) - 1 with NAV = cash + value of open lots.")


def _matrix(pieces: pd.DataFrame, px_ffill: pd.DataFrame, days: list[str]) -> dict:
    pos = {d: i for i, d in enumerate(days)}
    P = px_ffill.reindex(days)
    n = len(days)
    pnl, vprev, cap, buys, procs = (np.zeros(n) for _ in range(5))
    n_open_pieces = np.zeros(n)
    for r in pieces.itertuples():
        a, b = pos[r.entry_date], pos[r.exit_date]
        path = r.units * P[r.val_symbol].to_numpy()[a:b + 1]
        if b > a:
            pnl[a + 1:b + 1] += np.diff(path)
            vprev[a + 1:b + 1] += path[:-1]
        held_to = b + 1 if r.exit_reason == "end of window" else b    # still held at the close of day t
        cap[a:held_to] += path[:held_to - a]
        n_open_pieces[a:held_to] += 1
        buys[a] += r.entry_dollars
        if r.exit_reason != "end of window":
            procs[b] += r.exit_value
    return {"pnl": pnl, "vprev": vprev, "capital": cap, "buys": buys, "proceeds": procs, "P": P, "pos": pos}


def open_lot_counts(pieces: pd.DataFrame, days: list[str]) -> np.ndarray:
    pos = {d: i for i, d in enumerate(days)}
    lots = pieces.groupby("lot_id").agg(a=("entry_date", "min"), b=("exit_date", "max"),
                                        eow=("exit_reason", lambda s: (s == "end of window").any()))
    cnt = np.zeros(len(days))
    for r in lots.itertuples():
        a, b = pos[r.a], pos[r.b]
        cnt[a:(b + 1 if r.eow else b)] += 1
    return cnt


def equal_weight_returns(pieces: pd.DataFrame, P: pd.DataFrame, days: list[str], rf: np.ndarray) -> np.ndarray:
    pos = {d: i for i, d in enumerate(days)}
    lots = pieces.groupby("lot_id").agg(sym=("val_symbol", "first"), a=("entry_date", "min"), b=("exit_date", "max"))
    lots["ai"], lots["bi"] = lots["a"].map(pos), lots["b"].map(pos)
    change = set(lots["ai"]) | set(pieces["exit_date"].map(pos))
    Pn = {s: P[s].to_numpy() for s in lots["sym"].unique()}
    r = np.zeros(len(days))
    w: dict[str, float] = {}
    for t in range(len(days)):
        held = [l for l in w]                                        # lots held into day t
        if held:
            before = sum(w.values())
            for l in held:
                s = lots.at[l, "sym"]
                w[l] *= Pn[s][t] / Pn[s][t - 1]
            r[t] = sum(w.values()) / before - 1
        else:
            r[t] = rf[t]
        for l in [l for l in held if lots.at[l, "bi"] == t]:
            del w[l]
        for l in lots.index[(lots["ai"] == t)]:
            w[l] = 1.0
        if t in change and w:
            for l in w:
                w[l] = 1.0
    return r


def series(pieces: pd.DataFrame, px_ffill: pd.DataFrame, days: list[str], rf: np.ndarray, weighting: str = "dollar",
           spy: np.ndarray | None = None, start: str | None = None) -> tuple[pd.DataFrame, dict]:
    """Series A and B over days >= start (default: all days). `days` covers the whole book (warm-up included) and
    `rf`, `spy` are aligned with `days`."""
    m = _matrix(pieces, px_ffill, days)
    n = len(days)
    m0 = days.index(start) if start else 0
    held_all = m["vprev"] > 0
    a_all = np.where(held_all, np.divide(m["pnl"], m["vprev"], out=np.zeros_like(m["pnl"]), where=held_all), rf)
    a_dollar = a_all[m0:]
    held = held_all[m0:]
    a = a_dollar if weighting == "dollar" else equal_weight_returns(pieces, m["P"], days, rf)[m0:]
    w = slice(m0, n)
    buys, procs, cap, rfw = m["buys"][w], m["proceeds"][w], m["capital"][w], rf[w]
    V0 = float(m["capital"][m0 - 1]) if m0 > 0 else 0.0          # warm-up book at the close before the window
    net = np.cumsum(buys - procs)
    C0 = float(max(net.max(), 0.0))
    K = V0 + C0
    nw = n - m0
    cash, nav, interest = np.zeros(nw), np.zeros(nw), np.zeros(nw)
    c_prev, nav_prev = C0, K
    rb = np.zeros(nw)
    for t in range(nw):
        interest[t] = c_prev * rfw[t]
        cash[t] = c_prev + interest[t] - buys[t] + procs[t]
        nav[t] = cash[t] + cap[t]
        rb[t] = nav[t] / nav_prev - 1 if nav_prev > 0 else rfw[t]
        c_prev, nav_prev = cash[t], nav[t]
    wdays = days[m0:]
    book = pd.DataFrame({"date": wdays, "open_lots": open_lot_counts(pieces, days).astype(int)[m0:],
                         "capital_deployed": cap, "series_a_return": a, "series_b_return": rb,
                         "rf": rfw, "pot_cash": cash, "pot_nav": nav, "purchases": buys, "sale_proceeds": procs,
                         "dollar_pnl": m["pnl"][w], "capital_at_prior_close": m["vprev"][w], "idle_day": ~held})
    if weighting != "dollar":
        book["series_a_dollar_return"] = a_dollar
    if spy is not None:
        book["spy_return"] = np.asarray(spy)[m0:]
    # reconciliation over the measurement period: each piece's P&L from max(entry, the close before the window)
    pos = m["pos"]
    P = m["P"]
    lot_pnl = 0.0
    for r in pieces.itertuples():
        a_i, b_i = pos[r.entry_date], pos[r.exit_date]
        if b_i < m0:
            continue
        start_val = r.entry_dollars if a_i >= m0 - 1 else r.units * P[r.val_symbol].iat[m0 - 1]
        lot_pnl += r.exit_value - start_val
    book_pnl = float(m["pnl"][w].sum())
    a_implied = float((a_dollar[held] * m["vprev"][w][held]).sum())
    rec = {"K": K, "K_warmup_book": V0, "K_cash": C0, "lot_pnl": lot_pnl,
           "lot_pnl_all_incl_warmup": float(pieces["pnl"].sum()), "book_pnl": book_pnl,
           "diff_book_minus_lots": book_pnl - lot_pnl,
           "series_a_implied_pnl": a_implied, "diff_series_a_minus_lots": a_implied - lot_pnl,
           "pot_pnl_ex_interest": float(nav[-1] - K - interest.sum()),
           "diff_pot_minus_lots": float(nav[-1] - K - interest.sum()) - lot_pnl,
           "pot_interest": float(interest.sum()), "min_pot_cash": float(cash.min()),
           "idle_days": int((~held).sum()), "days": nw}
    return book, rec
