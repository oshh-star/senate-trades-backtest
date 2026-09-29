"""Benchmark return series and holdings arrays (Phase 5). Every series is DAILY on the NYSE calendar of the
sample; monthly series are compounded from it (stats.monthly), so every statistic uses identical dates.

  SPY                 total return (adjusted close), from daily_book.csv
  risk-matched SPY    RF + k (SPY - RF), k = sd(strategy monthly excess) / sd(SPY monthly excess); built monthly for
                      the monthly statistics (so its volatility matches exactly) and daily with the same k for the
                      drawdown and the chart
  Senate universe EW  at each month's formation date (the last trading day of the previous month), an equal-weight
                      portfolio of every symbol with an in-scope senator PURCHASE whose entry date (the first trading
                      day after its disclosure, the copier's own rule) falls in the 12 calendar months up to and
                      including the formation date: so only filings public before the formation close count. Held
                      for the month (weights drift; rebalanced monthly). "In scope" = every scope filter except the
                      window (in_scope_ex_window), as first published (J3). A member needs a price at the formation
                      close from a series that has not ended; symbols without prices (the survivorship ledger) are
                      left out and counted
  NANC, KRUZ          ETF total return; KRUZ is priced with Yahoo symbol GOP (renamed 2025-03-21, E34). Only months
                      whose previous month-end close exists (launch 2023-02-07, so from March 2023)
  sterling            r_GBP = (1 + r_USD) x GBPUSD(t-1) / GBPUSD(t) - 1, GBPUSD=X carried forward on NYSE days
"""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd


def load_prices(symbols: set[str], last_day: str) -> pd.DataFrame:
    """Adjusted closes, dates x symbols, cut at last_day (the OOS firewall)."""
    px = pd.read_csv("data/processed/prices.csv.gz", dtype={"ticker": str, "date": str}, keep_default_na=False,
                     na_values=[""], usecols=["date", "ticker", "adj_close"])
    px = px[px["ticker"].isin(symbols) & (px["date"] <= last_day)]
    wide = px.pivot(index="date", columns="ticker", values="adj_close")
    return wide.where(wide > 0)


def daily_returns(P_ffill: pd.DataFrame, sym: str, days: list[str]) -> pd.Series:
    """Daily total return of one symbol on `days` (the first uses the previous calendar day's close)."""
    return P_ffill[sym].pct_change(fill_method=None).reindex(days)


def months_back(d: str, months: int) -> str:
    """The same day `months` calendar months earlier (the month's last day when that day does not exist)."""
    import calendar
    f = dt.date.fromisoformat(d)
    k = f.year * 12 + f.month - 1 - months
    y, m = k // 12, k % 12 + 1
    return dt.date(y, m, min(f.day, calendar.monthrange(y, m)[1])).isoformat()


def universe_members(records: pd.DataFrame, formation: str, lookback_months: int = 12) -> set[str]:
    start = months_back(formation, lookback_months)
    sel = records[(records["entry_date"] > start) & (records["entry_date"] <= formation)]
    return set(sel["price_ticker"])


def universe_ew(records: pd.DataFrame, P_ffill: pd.DataFrame, calendar: list[str], days: list[str],
                last_dates: dict[str, str], first_dates: dict[str, str]) -> tuple[pd.Series, pd.DataFrame]:
    """Daily returns of the equal-weight Senate universe on `days`, and one row per month (members, left out)."""
    cal = list(calendar)
    months = sorted({d[:7] for d in days})
    r = pd.Series(np.nan, index=days)
    info = []
    for m in months:
        mdays = [d for d in days if d[:7] == m]
        form = cal[cal.index(mdays[0]) - 1]
        members = sorted(universe_members(records, form))
        ok = [s for s in members if s in P_ffill.columns and first_dates.get(s, "9") <= form
              and last_dates.get(s, "") >= form and np.isfinite(P_ffill.at[form, s])]
        path = P_ffill.loc[[form] + mdays, ok]
        v = (path / path.iloc[0]).mean(axis=1).to_numpy()
        r.loc[mdays] = v[1:] / v[:-1] - 1
        info.append({"month": m, "formation_date": form, "symbols_with_purchase": len(members), "members_priced": len(ok),
                     "left_out_no_price": len(members) - len(ok),
                     "left_out_symbols": " ".join(s for s in members if s not in ok)})
    return r, pd.DataFrame(info)


def holdings_values(pieces: pd.DataFrame, P_ffill: pd.DataFrame, book_days: list[str], first: str):
    """(pre, post, symbols) over the window days: pre[t, i] = value of symbol i held INTO day t, at t's close
    (after drift, before t's trades); post[t, i] = value held at t's close after t's trades."""
    pos = {d: i for i, d in enumerate(book_days)}
    syms = sorted(pieces["val_symbol"].unique())
    col = {s: j for j, s in enumerate(syms)}
    P = P_ffill.reindex(book_days)
    pre = np.zeros((len(book_days), len(syms)))
    post = np.zeros_like(pre)
    for r in pieces.itertuples():
        a, b = pos[r.entry_date], pos[r.exit_date]
        path = r.units * P[r.val_symbol].to_numpy()[a:b + 1]
        j = col[r.val_symbol]
        pre[a + 1:b + 1, j] += path[1:]
        held_to = b + 1 if r.exit_reason == "end of window" else b
        post[a:held_to, j] += path[:held_to - a]
    m0 = pos[first]
    return pre[m0:], post[m0:], syms


def to_gbp(r_usd: pd.Series, fx: pd.Series) -> pd.Series:
    """USD daily returns -> GBP daily returns for a sterling investor. fx = USD per GBP on the same days, with
    the previous day's rate for the first day."""
    fx = np.asarray(fx, dtype=float)
    return pd.Series((1 + np.asarray(r_usd, float)) * fx[:-1] / fx[1:] - 1, index=r_usd.index)
