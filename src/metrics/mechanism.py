"""Mechanism splits of the event study (Phase 6 prep): WHO and WHAT drives any senator or copier return.

From data/processed/event_panel.csv (every in-scope purchase and sale record with an entry date in the sample), for
purchases and sales separately, each split reports the SPY-adjusted return of the copier (from the entry date) and
of the senator (from the transaction date) at 21, 63 and 126 trading days, and the pre-disclosure drift (transaction
close to entry close): mean, N and the t-statistic with standard errors clustered by calendar month of entry. For a
two-way split, a "difference" row gives group 1 minus group 2 and its clustered t (OLS on a group dummy).
Splits:
  size    the two smallest disclosed bands ($1,001-$15,000 and $15,001-$50,000, midpoints 8,000.50 and 32,500.50)
          against every larger band
  party   the party of the senator's term covering the trade date (trades_clean.csv `party`)
  lag     filing lag = disclosure date minus transaction date, calendar days, of THIS record: 30 or less vs longer
  senator the top 4 senators by number of events IN THIS PANEL (the sample's in-scope purchase and sale records), one
          by one, and everyone else pooled (E17's senator_rank counts the whole window, and its rank-2 senator has no
          in-sample event)
A t-statistic is left blank when its events fall in fewer than MIN_CLUSTERS entry months (a clustered standard error
with one or two clusters is meaningless).
Sign convention as in the event study: returns are the stock's minus SPY's; after a sale a NEGATIVE number is an
informative sale.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm

from .stats import clustered_mean

HORIZONS = [21, 63, 126]
SMALL_BANDS = 32500.5          # midpoint of $15,001-$50,000; the smaller band's is 8,000.50
MIN_CLUSTERS = 5


def attach(panel: pd.DataFrame) -> pd.DataFrame:
    tc = pd.read_csv("data/processed/trades_clean.csv", keep_default_na=False, low_memory=False,
                     usecols=["trade_id", "party", "senator_rank"])
    p = panel.merge(tc, on="trade_id", how="left")
    p["entry_month"] = p["entry_date"].astype(str).str[:7]
    p["size_group"] = np.where(p["size"] <= SMALL_BANDS, "two smallest bands (<= $50,000)", "larger bands (> $50,000)")
    p["party_group"] = p["party"].replace("", "unknown").fillna("unknown")
    lag = (pd.to_datetime(p["disclosure_date"]) - pd.to_datetime(p["transaction_date"])).dt.days
    p["filing_lag_days"] = lag
    p["lag_group"] = np.where(lag <= 30, "filed within 30 days", "filed after 30 days")
    top = p["senator"].value_counts().head(4).index.tolist()
    p["senator_group"] = np.where(p["senator"].isin(top), p["senator"], "everyone else")
    p.attrs["top4"] = top
    return p


def diff_t(x: pd.Series, g: pd.Series, clusters: pd.Series, a: str) -> tuple[float, float, int]:
    ok = x.notna()
    x, d, c = x[ok].astype(float), (g[ok] == a).astype(float), clusters[ok]
    if d.nunique() < 2 or len(x) < 4 or c[d == 1].nunique() < MIN_CLUSTERS or c[d == 0].nunique() < MIN_CLUSTERS:
        return (float(x[d == 1].mean() - x[d == 0].mean()) if d.nunique() == 2 else np.nan), np.nan, int(len(x))
    fit = sm.OLS(x.to_numpy(), sm.add_constant(d.to_numpy())).fit(cov_type="cluster",
                                                                   cov_kwds={"groups": pd.factorize(c)[0]})
    return float(fit.params[1]), float(fit.tvalues[1]), int(len(x))


def split_table(p: pd.DataFrame, col: str, order: list[str] | None = None) -> pd.DataFrame:
    rows = []
    groups = order or sorted(p[col].dropna().unique())
    measures = [("copier", h, f"x_entry_{h}") for h in HORIZONS] + [("senator", h, f"x_txn_{h}") for h in HORIZONS] \
        + [("drift", 0, "gap_x")]
    for side in ("purchase", "sale"):
        q = p[p["side"] == side]
        for g in groups:
            s = q[q[col] == g]
            if not len(s):
                continue
            r = {"side": side, "group": g, "events": len(s)}
            for who, h, c in measures:
                m = clustered_mean(s[c], s["entry_month"])
                key = f"{who}_{h}" if h else "drift"
                t = m["t_cluster"] if m["clusters"] >= MIN_CLUSTERS else np.nan
                r[f"{key}_mean"], r[f"{key}_t"], r[f"{key}_n"] = m["mean"], t, m["n"]
                r[f"{key}_clusters"] = m["clusters"]
            rows.append(r)
        if len(groups) == 2 and len(q[q[col].isin(groups)]):
            a, b = groups
            r = {"side": side, "group": f"difference ({a} minus {b})", "events": len(q[q[col].isin(groups)])}
            for who, h, c in measures:
                key = f"{who}_{h}" if h else "drift"
                qq = q[q[col].isin(groups)]
                r[f"{key}_mean"], r[f"{key}_t"], r[f"{key}_n"] = diff_t(qq[c], qq[col], qq["entry_month"], a)
            rows.append(r)
    return pd.DataFrame(rows)


def all_splits(panel: pd.DataFrame) -> dict[str, pd.DataFrame]:
    p = attach(panel)
    top = p.attrs["top4"]
    return {"size": split_table(p, "size_group", ["two smallest bands (<= $50,000)", "larger bands (> $50,000)"]),
            "party": split_table(p, "party_group"),
            "lag": split_table(p, "lag_group", ["filed within 30 days", "filed after 30 days"]),
            "senator": split_table(p, "senator_group", top + ["everyone else"])}


def to_md(t: pd.DataFrame) -> str:
    cell = lambda m, tt: "" if pd.isna(m) else (f"{m:+.2%} ({tt:.2f})" if pd.notna(tt) else f"{m:+.2%} (t n/a)")
    v = pd.DataFrame({"side": t["side"], "group": t["group"], "events": t["events"]})
    for who in ("copier", "senator"):
        for h in HORIZONS:
            v[f"{who} {h}d"] = [cell(m, tt) for m, tt in zip(t[f"{who}_{h}_mean"], t[f"{who}_{h}_t"])]
    v["N (copier 21d / 126d)"] = [f"{int(a) if pd.notna(a) else 0} / {int(b) if pd.notna(b) else 0}"
                                  for a, b in zip(t["copier_21_n"], t["copier_126_n"])]
    v["pre-disclosure drift"] = [cell(m, tt) for m, tt in zip(t["drift_mean"], t["drift_t"])]
    return v.to_markdown(index=False)


def write(panel: pd.DataFrame, label: str, first: str, last: str, tag: str, out_dir) -> dict:
    from pathlib import Path
    S = all_splits(panel)
    out_dir = Path(out_dir)
    stem = out_dir / f"mechanism_{'insample' if label == 'in-sample' else 'full'}_{tag}"
    pd.concat([t.assign(split=k) for k, t in S.items()], ignore_index=True).to_csv(stem.with_suffix(".csv"), index=False,
                                                                                    float_format="%.6g")
    titles = {"size": "Trade size: the two smallest disclosed bands against every larger band",
              "party": "Party of the senator's term on the trade date",
              "lag": "Filing lag (disclosure date minus transaction date): 30 days or less against longer",
              "senator": "Senator: the top 4 by number of in-sample events, one by one, and everyone else pooled"}
    L = [f"# Mechanism splits, {label} ({first} to {last}), {tag.upper()}", ""]
    if tag == "yahoo":
        L += ["**Prices: Yahoo, the final headline source (R3, S2).** Stocks in the survivorship ledger (mostly delisted names Yahoo no longer serves) have no prices: their events drop out here and their purchases are skipped in the book; V15 (SPY fill) bounds the effect.", ""]
    L += ["_From `data/processed/event_panel.csv` (src/metrics/mechanism.py). Each cell: mean SPY-adjusted return "
          "(t-statistic, standard errors clustered by calendar month of entry). **copier** = from the close on the entry "
          "date (first trading day after the disclosure); **senator** = from the close on the transaction date; "
          "horizons in trading days. **Pre-disclosure drift** = transaction-date close to entry-date close. A "
          "\"difference\" row is group 1 minus group 2 (OLS on a group dummy, same clustering). \"t n/a\" = fewer than "
          f"{MIN_CLUSTERS} entry months, too few for a clustered standard error. Sign convention: the "
          "stock's return minus SPY's whatever the side; after a PURCHASE positive = informative, after a SALE "
          "NEGATIVE = informative. Horizons past the last in-sample day are censored, so N falls with the horizon._", ""]
    for k, t in S.items():
        L += [f"## {titles[k]}", "", to_md(t), ""]
    stem.with_suffix(".md").write_text("\n".join(L))
    return S
