"""Price-source hierarchy (M2): CRSP, then a terminal export (manual), then Yahoo, symbol by symbol and day by day.

merge(): for one symbol, the merged daily series lives on the union of the sources' dates. Its first price comes
from the highest-priority source with a price that day. Each later day t takes its RETURN from the highest-priority
source that has a price on both t and the previous merged date, so a return is never measured across a gap in one
source and spliced onto another's level. The merged `adj_close` is a total return index that compounds those returns
(only ratios are ever used); `close` and `source` come from the source that supplied the day. A day that no source
bridges carries the index flat and is counted (`unbridged_days`). When Yahoo supplies every day, the Yahoo rows are
returned unchanged, so V18 (prices.sources: [yahoo]) reproduces the Yahoo-only files exactly.

validate(): where two sources both bridge the same days, their daily returns are compared: N days, correlation, mean
and largest absolute gap and its date (data/interim/price_source_validation.csv).

needed(): for each symbol a trade of any window or variant uses, the dates prices are needed (earliest entry date
minus 5 trading days, to the delisting date or the end of the data) and the eFD tickers that map to it; used to map
CRSP PERMNOs and to write the price request (docs/archive/PRICE_REQUEST.md).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SOURCE_NAMES = ("crsp", "manual", "yahoo")


def merge(series: dict[str, pd.DataFrame], order: list[str]) -> tuple[pd.DataFrame, dict]:
    """series: {source: frame with date, close, adj_close (and volume for yahoo)} -> (merged frame, info)."""
    have = [s for s in order if s in series and len(series[s])]
    if not have:
        return pd.DataFrame(columns=["date", "close", "adj_close", "volume", "source"]), {"sources": [], "unbridged_days": 0}
    if have == ["yahoo"]:
        y = series["yahoo"].copy()
        y["source"] = "yahoo"
        return y, {"sources": ["yahoo"], "unbridged_days": 0, "days_by_source": {"yahoo": len(y)}}
    idx = {s: series[s].set_index("date") for s in have}
    dates = sorted(set().union(*[set(f.index) for f in idx.values()]))
    level = np.empty(len(dates))
    close = np.full(len(dates), np.nan)
    vol = np.full(len(dates), np.nan)
    src = np.empty(len(dates), dtype=object)
    unbridged = 0
    for i, d in enumerate(dates):
        if i == 0:
            s0 = next(s for s in have if d in idx[s].index)
            level[0], src[0] = float(idx[s0].at[d, "adj_close"]), s0
        else:
            p = dates[i - 1]
            s0 = next((s for s in have if d in idx[s].index and p in idx[s].index
                       and np.isfinite(idx[s].at[d, "adj_close"]) and np.isfinite(idx[s].at[p, "adj_close"])), None)
            if s0 is None:
                s0 = next(s for s in have if d in idx[s].index)
                level[i], unbridged = level[i - 1], unbridged + 1
            else:
                level[i] = level[i - 1] * float(idx[s0].at[d, "adj_close"]) / float(idx[s0].at[p, "adj_close"])
            src[i] = s0
        close[i] = idx[s0].at[d, "close"] if "close" in idx[s0].columns else np.nan
        if "volume" in idx[s0].columns:
            vol[i] = idx[s0].at[d, "volume"]
    out = pd.DataFrame({"date": dates, "close": close, "adj_close": level, "volume": vol, "source": src})
    return out, {"sources": have, "unbridged_days": unbridged,
                 "days_by_source": out["source"].value_counts().to_dict()}


def validate(sym: str, series: dict[str, pd.DataFrame]) -> list[dict]:
    """Every pair of sources that overlap: compare daily returns on the days both bridge."""
    rows = []
    names = [s for s in SOURCE_NAMES if s in series and len(series[s])]
    rets = {}
    for s in names:
        f = series[s].sort_values("date").reset_index(drop=True)
        r = f["adj_close"] / f["adj_close"].shift(1) - 1
        rets[s] = pd.Series(r.to_numpy(), index=pd.MultiIndex.from_arrays([f["date"].shift(1), f["date"]]))
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            j = pd.concat([rets[a], rets[b]], axis=1, join="inner").dropna()
            if len(j) < 2:
                continue
            gap = (j.iloc[:, 0] - j.iloc[:, 1]).abs()
            k = gap.idxmax()
            rows.append({"symbol": sym, "source_a": a, "source_b": b, "days": len(j),
                         "first_date": j.index[0][1], "last_date": j.index[-1][1],
                         "correlation": float(np.corrcoef(j.iloc[:, 0], j.iloc[:, 1])[0, 1]),
                         "mean_abs_gap": float(gap.mean()), "max_abs_gap": float(gap.max()), "max_gap_date": k[1]})
    return rows


def needed(cfg: dict, calendar: list[str], end: str, delisted: dict[str, str] | None = None) -> pd.DataFrame:
    """One row per price symbol used by any window or variant: dates needed and the eFD tickers mapping to it.
    Headline dollars = in-scope purchases of the headline, warm-up included (engine.warmup_months)."""
    from src.config import analysis_window
    from src.engine import events as evm
    from src.engine import warmup_start
    recs = pd.read_csv("data/processed/trade_records.csv", keep_default_na=False, low_memory=False,
                       dtype={"ticker": str, "price_ticker": str})
    for c in ("in_scope", "in_scope_ex_window", "in_scope_ex_window_owner"):
        recs[c] = recs[c].astype(str) == "True"
    recs["amount_mid"] = pd.to_numeric(recs["amount_mid"], errors="coerce")
    first = analysis_window(cfg)[0].isoformat()
    w_start = warmup_start(cfg, first)[0]
    recs["headline"] = recs["in_scope"] | (recs["in_scope_ex_window"] & (recs["disclosure_date"] >= w_start)
                                           & (recs["disclosure_date"] < first))
    use = recs[recs["in_scope_ex_window_owner"] & (recs["price_ticker"] != "") & (recs["disclosure_date"] <= end)].copy()
    use["entry_date"] = evm.entry_dates(use, calendar, cfg)
    cal = list(calendar)
    pos = {d: i for i, d in enumerate(cal)}
    delisted = delisted or {}
    rows = []
    for sym, g in use.groupby("price_ticker"):
        e = g.loc[g["entry_date"] != "", "entry_date"]
        e0 = e.min() if len(e) else g["disclosure_date"].min()
        i0 = pos.get(e0, int(np.searchsorted(cal, e0)))
        h = g[g["headline"]]
        rows.append({"symbol": sym, "efd_tickers": " ".join(sorted(set(g["ticker"]) - {""})),
                     "first_needed": cal[max(i0 - 5, 0)], "last_needed": min(delisted.get(sym, end), end),
                     "headline_trades": int(h["trade_id"].nunique()), "all_trades": int(g["trade_id"].nunique()),
                     "headline_purchase_dollars": float(h.loc[h["transaction_type"] == "Purchase", "amount_mid"].sum()),
                     "all_purchase_dollars": float(g.loc[g["transaction_type"] == "Purchase", "amount_mid"].sum())})
    return pd.DataFrame(rows)
