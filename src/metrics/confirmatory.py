"""Confirmatory tests H0-H4 for ONE half of the window (docs/DECISIONS.md, "Out-of-sample test plan": Q2, E55, R1,
R2, R4), plus calendar-year returns and the worst rolling 12 months.

`half_report(panel, monthly, calendar, first, last)` builds everything for the half [first, last] from:
  panel     the engine's event panel (data/processed/event_panel.csv), in-sample or full window
  monthly   the metrics stage's monthly returns (data/processed/monthly_returns.csv, index 'YYYY-MM')
  calendar  the NYSE trading days (data/processed/trading_calendar.csv)
Events are kept when their ENTRY date is inside the half, and every horizon (and the transaction-date start of the
senator measure) that runs past the half's last trading day is censored, exactly as the engine censors at the end
of its sample (E32). Applied to the in-sample panel this changes nothing; applied to a full-window panel it gives
each half on its own. Part B points the same function at the out-of-sample half.

The seven confirmatory statistics (the Holm family, R1):
  H0a  series A, CAPM alpha (monthly, annualised x 12)          t: Newey-West, 3 lags      two-sided
  H0b  series A, Carhart 4-factor alpha                          t: Newey-West, 3 lags      two-sided
  H1p  purchases, pre-disclosure drift (event panel gap_x)       t: clustered by entry month  two-sided
  H1s  sales, pre-disclosure drift                               t: clustered               two-sided
  H2   copier purchases, 21-day SPY-adjusted return              t: clustered               ONE-sided (> 0)
  H3   SALES, senator measure 63 days: overseen minus not        t: clustered (group dummy) two-sided
  H4   PURCHASES, copier 126 days: <= $50,000 minus larger       t: clustered (group dummy) two-sided
p-values use the normal distribution, matching the registered thresholds (|t| 1.96; 1.645 one-sided for H2).
Holm (R1): sort the 7 p-values; the k-th smallest (k = 1..7) is multiplied by (7 - k + 1), a running maximum keeps
the order, capped at 1. A test that cannot be computed (fewer than 5 entry months, Q1) gets p = 1 and still counts in
the 7, so the family never shrinks after the data are seen. Verdicts use the Holm-adjusted p at 5%.
Minimum detectable effect (R1, R4) = z x SE, at the nominal z (1.960; 1.645 for H2) and at the Bonferroni z for
0.05 / 7 (2.690; 2.450 for H2), Holm's strictest step; "no effect larger than X" uses the Bonferroni figure.
Sensitivity (R2): H1, H2 and H4 without events from bulk filings (trades_clean.csv `bulk_ptr`, the V4 flag), shown
beside the full-sample tests and NOT part of the Holm family. Reversal check (E55 d): copier purchases at 126 and 252
days, reported whatever H2 shows.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import norm

from . import committee as cm
from . import mechanism as mc
from .stats import NW_LAGS

M_TESTS = 7
LEVEL = 0.05
Z_NOMINAL = {2: float(norm.ppf(1 - LEVEL / 2)), 1: float(norm.ppf(1 - LEVEL))}                       # 1.960, 1.645
Z_BONFERRONI = {2: float(norm.ppf(1 - LEVEL / M_TESTS / 2)), 1: float(norm.ppf(1 - LEVEL / M_TESTS))}  # 2.690, 2.450
MIN_CLUSTERS = mc.MIN_CLUSTERS
EXPLORATORY_NOTE = ("**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, \"Out-of-sample "
                    "test plan\"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few "
                    "cells in a table like this one will reach |t| = 2 by chance.**")


# ------------------------------------------------------------------ statistics
def holm(p) -> np.ndarray:
    """Holm-adjusted p-values, in the input order. Missing p-values count as 1 (cannot reject)."""
    p = np.where(np.isfinite(np.asarray(p, dtype=float)), np.asarray(p, dtype=float), 1.0)
    m = len(p)
    order = np.argsort(p, kind="stable")
    adj = np.empty(m)
    run = 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (m - k) * p[i]))
        adj[i] = run
    return adj


def p_value(t: float, sides: int) -> float:
    """Normal p-value: two-sided P(|Z| >= |t|), or one-sided P(Z >= t) (the registered direction is positive)."""
    if not np.isfinite(t):
        return np.nan
    return float(2 * norm.sf(abs(t))) if sides == 2 else float(norm.sf(t))


def cluster_mean(x: pd.Series, clusters: pd.Series) -> dict:
    """Mean with standard errors clustered by `clusters` (the same fit as stats.clustered_mean)."""
    ok = x.notna()
    x, g = x[ok].astype(float), clusters[ok]
    out = {"estimate": float(x.mean()) if len(x) else np.nan, "se": np.nan, "t": np.nan, "n": int(len(x)),
           "clusters": int(g.nunique())}
    if len(x) >= 2 and g.nunique() >= MIN_CLUSTERS:
        fit = sm.OLS(x.to_numpy(), np.ones((len(x), 1))).fit(cov_type="cluster",
                                                             cov_kwds={"groups": pd.factorize(g)[0]})
        out.update(se=float(fit.bse[0]), t=float(fit.tvalues[0]))
    return out


def cluster_diff(x: pd.Series, groups: pd.Series, clusters: pd.Series, a: str) -> dict:
    """Group a minus the rest: OLS on a group dummy, clustered (the same fit as mechanism.diff_t)."""
    ok = x.notna()
    x, d, c = x[ok].astype(float), (groups[ok] == a).astype(float), clusters[ok]
    est = float(x[d == 1].mean() - x[d == 0].mean()) if d.nunique() == 2 else np.nan
    out = {"estimate": est, "se": np.nan, "t": np.nan, "n": int(len(x)), "clusters": int(c.nunique())}
    if d.nunique() == 2 and len(x) >= 4 and c[d == 1].nunique() >= MIN_CLUSTERS and c[d == 0].nunique() >= MIN_CLUSTERS:
        fit = sm.OLS(x.to_numpy(), sm.add_constant(d.to_numpy())).fit(cov_type="cluster",
                                                                       cov_kwds={"groups": pd.factorize(c)[0]})
        out.update(estimate=float(fit.params[1]), se=float(fit.bse[1]), t=float(fit.tvalues[1]))
    return out


def alpha_nw(y_ex: pd.Series, factors: pd.DataFrame) -> dict:
    """Annualised alpha (monthly x 12) with its Newey-West (Bartlett, 3 lags) standard error, as stats.regress."""
    X = sm.add_constant(factors.to_numpy(dtype=float), has_constant="add")
    fit = sm.OLS(np.asarray(y_ex, dtype=float), X).fit(cov_type="HAC", cov_kwds={"maxlags": NW_LAGS})
    return {"estimate": float(fit.params[0] * 12), "se": float(fit.bse[0] * 12), "t": float(fit.tvalues[0]),
            "n": int(len(y_ex)), "clusters": np.nan}


# ------------------------------------------------------------------ the half
def restrict(panel: pd.DataFrame, calendar: list[str], first: str, last: str) -> pd.DataFrame:
    """Events with an entry date in [first, last], censored at the half's last trading day (E32)."""
    pos = {d: i for i, d in enumerate(calendar)}
    last_i = max(i for d, i in pos.items() if d <= last)
    p = panel[(panel["entry_date"].astype(str) >= first) & (panel["entry_date"].astype(str) <= last)].copy()
    i_e = p["entry_date"].astype(str).map(pos)
    i_t = p["txn_price_date"].fillna("").astype(str).map(pos)
    for h in sorted({int(c.rsplit("_", 1)[1]) for c in p.columns if c.startswith("x_entry_")}):
        for tag, i0 in (("entry", i_e), ("txn", i_t)):
            gone = i0.isna() | (i0 + h > last_i)
            p.loc[gone, [f"r_{tag}_{h}", f"x_{tag}_{h}"]] = np.nan
    p["entry_month"] = p["entry_date"].astype(str).str[:7]
    return p


def bulk_trade_ids(path: str = "data/processed/trades_clean.csv") -> set:
    tc = pd.read_csv(path, usecols=["trade_id", "bulk_ptr"], keep_default_na=False, low_memory=False)
    return set(tc.loc[tc["bulk_ptr"].astype(str) == "True", "trade_id"])


def event_tests(p: pd.DataFrame) -> dict:
    """H1-H4 on an already restricted panel; returns {test id: statistic dict}."""
    pur, sal = p[p["side"] == "purchase"], p[p["side"] == "sale"]
    out = {"H1p": cluster_mean(pur["gap_x"], pur["entry_month"]),
           "H1s": cluster_mean(sal["gap_x"], sal["entry_month"]),
           "H2": cluster_mean(pur["x_entry_21"], pur["entry_month"])}
    q = mc.attach(p)
    qp = q[q["side"] == "purchase"]
    out["H4"] = cluster_diff(qp["x_entry_126"], qp["size_group"], qp["entry_month"], "two smallest bands (<= $50,000)")
    if cm.available():
        c = cm.classify(p)
        cs = c[(c["side"] == "sale") & c["committee_group"].isin([cm.OVERSEEN, cm.NOT])]
        out["H3"] = cluster_diff(cs["x_txn_63"], cs["committee_group"], cs["entry_month"], cm.OVERSEEN)
    else:
        out["H3"] = {"estimate": np.nan, "se": np.nan, "t": np.nan, "n": 0, "clusters": 0}
    return out


TESTS = [  # id, hypothesis, what, sides, prediction
    ("H0a", "H0 (primary)", "Series A, CAPM alpha, annualised", 2, "Not distinguishable from zero"),
    ("H0b", "H0 (primary)", "Series A, Carhart 4-factor alpha, annualised", 2, "Not distinguishable from zero"),
    ("H1p", "H1 (information)", "Purchases: pre-disclosure drift (transaction close to entry close, SPY-adjusted)", 2,
     "Close to zero (positive if senators trade on information)"),
    ("H1s", "H1 (information)", "Sales: pre-disclosure drift", 2,
     "Close to zero (negative if senators trade on information)"),
    ("H2", "H2 (short-horizon drift)", "Copier purchases, 21-day SPY-adjusted return", 1,
     "One-sided test: is it positive?"),
    ("H3", "H3 (committee anomaly)", "Sales, senator measure, 63 days: overseen minus not overseen", 2,
     "It disappears (it was noise)"),
    ("H4", "H4 (size)", "Purchases, copier measure, 126 days: up to $50,000 minus larger", 2,
     "Negative if senators trade on information"),
]


def verdict(tid: str, est: float, t: float, p_holm: float) -> str:
    if not np.isfinite(t):
        return "not testable (fewer than 5 entry months)"
    sig = p_holm < LEVEL
    if tid == "H2":
        return "positive (significant)" if sig else "not shown to be positive"
    if not sig:
        return "not distinguishable from zero"
    return f"significantly {'positive' if est > 0 else 'negative'}"


def half_report(panel: pd.DataFrame, monthly: pd.DataFrame, calendar: list[str], first: str, last: str,
                bulk_ids: set | None = None) -> dict:
    """Everything for the half [first, last]: the confirmatory table, the ex-bulk sensitivity, the reversal check,
    calendar-year returns and the worst rolling 12 months."""
    p = restrict(panel, calendar, first, last)
    mon = monthly[(monthly.index >= first[:7]) & (monthly.index <= last[:7])]
    y = mon["r_A"] - mon["rf"]
    stats = {"H0a": alpha_nw(y, mon[["mkt_rf"]]), "H0b": alpha_nw(y, mon[["mkt_rf", "smb", "hml", "mom"]])}
    stats.update(event_tests(p))
    rows = []
    for tid, hyp, what, sides, pred in TESTS:
        s = stats[tid]
        rows.append({"id": tid, "hypothesis": hyp, "statistic": what, "sides": sides, "prediction": pred,
                     "estimate": s["estimate"], "se": s["se"], "t": s["t"], "n": s["n"], "clusters": s["clusters"],
                     "p": p_value(s["t"], sides), "z_nominal": Z_NOMINAL[sides], "z_bonferroni": Z_BONFERRONI[sides],
                     "mde_nominal": Z_NOMINAL[sides] * s["se"], "mde_bonferroni": Z_BONFERRONI[sides] * s["se"]})
    conf = pd.DataFrame(rows)
    conf["p_holm"] = holm(conf["p"])
    conf["verdict"] = [verdict(r.id, r.estimate, r.t, r.p_holm) for r in conf.itertuples()]

    bulk_ids = bulk_trade_ids() if bulk_ids is None else bulk_ids
    xb = event_tests(p[~p["trade_id"].isin(bulk_ids)])
    sens = pd.DataFrame([{"id": tid, "statistic": what, "sides": sides,
                          "estimate_all": stats[tid]["estimate"], "t_all": stats[tid]["t"], "n_all": stats[tid]["n"],
                          "estimate_ex_bulk": xb[tid]["estimate"], "t_ex_bulk": xb[tid]["t"], "n_ex_bulk": xb[tid]["n"],
                          "p_ex_bulk": p_value(xb[tid]["t"], sides)}
                         for tid, _, what, sides, _ in TESTS if tid in ("H1p", "H1s", "H2", "H4")])

    pur = p[p["side"] == "purchase"]
    base = stats["H2"]["estimate"]
    rev = []
    for h in (21, 126, 252):
        s = cluster_mean(pur[f"x_entry_{h}"], pur["entry_month"])
        if h == 21:
            label = "H2 itself"
        elif not np.isfinite(s["estimate"]):
            label = "no events (censored)"
        elif s["estimate"] <= 0:
            label = "fully reversed (at or below zero)"
        elif s["estimate"] < base:
            label = "partly reversed (below the 21-day mean)"
        else:
            label = "not reversed"
        rev.append({"horizon_days": h, "estimate": s["estimate"], "t": s["t"], "n": s["n"], "reading": label})
    return {"first": first, "last": last, "confirmatory": conf, "sensitivity": sens, "reversal": pd.DataFrame(rev),
            "calendar_years": calendar_years(mon), "worst_12m": worst_12m(mon), "n_events": len(p),
            "months": list(mon.index)}


# ------------------------------------------------------------------ calendar years and rolling 12 months
SERIES = [("r_A", "Series A (headline)"), ("r_B", "Series B (fixed pot)"), ("r_SPY", "SPY"),
          ("r_RM_A", "SPY risk-matched to A"), ("r_RM_B", "SPY risk-matched to B"),
          ("r_EW", "Senate universe, equal weight"), ("r_MKT", "Market (Ken French Mkt-RF + RF)"),
          ("r_NANC", "NANC"), ("r_KRUZ", "KRUZ (as GOP)"), ("rf", "Risk-free (Ken French RF)")]
MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _span(months: list[str]) -> str:
    a, b = months[0], months[-1]
    return f"{MONTH_ABBR[int(a[5:]) - 1]}-{MONTH_ABBR[int(b[5:]) - 1]}"


def calendar_years(mon: pd.DataFrame) -> pd.DataFrame:
    """Compounded return of every series in each calendar year (or part-year) of the half. A series that does not
    cover every month of that part-year (NANC, KRUZ before March 2023) is compounded over the months it has, and
    the months are named in `coverage`."""
    m = mon.copy()
    m["r_MKT"] = m["mkt_rf"] + m["rf"]
    rows = []
    for year, g in m.groupby(m.index.str[:4]):
        full = list(g.index)
        row = {"year": year, "months": f"{_span(full)} ({len(full)} months)" if len(full) < 12 else "full year"}
        cover = []
        for col, name in SERIES:
            s = g[col].dropna() if col in g else pd.Series(dtype=float)
            row[name] = float(np.prod(1 + s) - 1) if len(s) else np.nan
            if 0 < len(s) < len(full):
                cover.append(f"{name}: {_span(list(s.index))}")
        row["coverage"] = "; ".join(cover)
        rows.append(row)
    return pd.DataFrame(rows)


def worst_12m(mon: pd.DataFrame) -> pd.DataFrame:
    """Worst 12 consecutive months (compounded) for series A and for SPY, each with the other's return over the same
    months."""
    rows = []
    for col, name in (("r_A", "Series A (headline)"), ("r_SPY", "SPY")):
        r = mon[col]
        if len(r) < 12:
            rows.append({"series": name, "start": "", "end": "", "return": np.nan})
            continue
        roll = (1 + r).rolling(12).apply(np.prod, raw=True) - 1
        end = roll.idxmin()
        i = list(r.index).index(end)
        start = r.index[i - 11]
        win = r.index[i - 11:i + 1]
        rows.append({"series": name, "start": start, "end": end, "return": float(roll[end]),
                     "series A, same months": float(np.prod(1 + mon.loc[win, "r_A"]) - 1),
                     "SPY, same months": float(np.prod(1 + mon.loc[win, "r_SPY"]) - 1),
                     "windows": int(roll.notna().sum())})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ writing
def price_sources(coverage: str = "data/processed/price_coverage.csv") -> str:
    from src.variants import price_tag
    cov = pd.read_csv(coverage, keep_default_na=False)
    has = cov[cov["has_data"].astype(str) == "True"]
    by = has["source"].replace("", "unknown").value_counts().to_dict()
    parts = ", ".join(f"{k} {v:,}" for k, v in sorted(by.items()))
    n_none = int((cov["has_data"].astype(str) != "True").sum())
    files = [p.name for d in ("data/raw/crsp", "data/raw/manual_prices") for p in Path(d).glob("*.csv*")]
    s = (f"**Price sources in use** (`prices.sources`, M2): symbols priced by {parts}; {n_none:,} symbols have no prices "
         f"(the survivorship ledger; their purchases are skipped, K3). CRSP or terminal price files present: "
         f"{len(files)}{' (' + ', '.join(sorted(files)) + ')' if files else ''}. Price tag: **{price_tag()}**.")
    s += (" Since C1 (2026-10-09) the headline is Yahoo with the Bloomberg terminal files where Yahoo has no price; a "
          "CRSP file could only ever feed variant V20, never the headline (S3). The remaining survivorship gap is a stated "
          "limitation; V15 (SPY fill) shows its size but is not a bound (the priced ledger stocks beat SPY).")
    return s


def _pct(v, signed=True, nd=2) -> str:
    return "" if v is None or not np.isfinite(v) else (f"{v:+.{nd}%}" if signed else f"{v:.{nd}%}")


def _num(v, nd=2) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v:.{nd}f}"


def _p(v) -> str:
    return "" if v is None or not np.isfinite(v) else (f"{v:.3f}" if v >= 0.001 else "<0.001")


def to_md(R: dict, label: str, sources: str) -> str:
    c = R["confirmatory"]
    L = [f"# Confirmatory tests H0-H4, {label} ({R['first']} to {R['last']})", "", sources, "",
         "_Built by `src/metrics/confirmatory.py` (`half_report`), from the engine's event panel and "
         "data/processed/monthly_returns.csv. The tests are the ones registered in docs/DECISIONS.md, \"Out-of-sample test "
         "plan\" (Q2, E55, R1, R2, R4). Event returns are the stock's minus SPY's over the same trading days; events count "
         "once each, keyed to their entry date (first trading day after disclosure), with horizons past the half's last "
         "trading day censored. t: Newey-West (3 lags) for the alphas, clustered by calendar month of entry for H1-H4 "
         f"(blank below {MIN_CLUSTERS} entry months). p: normal; two-sided except H2 (one-sided, positive). Holm across the "
         "7 statistics (a test that cannot be computed counts as p = 1); **verdicts use the Holm p at 5%**. Minimum "
         "detectable effect (MDE) = z x SE: nominal z 1.960 (H2 1.645), Bonferroni z 2.690 (H2 2.450) for 0.05 / 7, "
         "Holm's strictest step._", "",
         "## The seven confirmatory statistics", ""]
    t = pd.DataFrame({
        "test": c["id"], "statistic": c["statistic"], "estimate": c["estimate"].map(_pct),
        "SE": c["se"].map(lambda v: _pct(v, False)), "t": c["t"].map(_num),
        "N (clusters)": [f"{n} months" if not np.isfinite(k) else f"{n} ({int(k)})" for n, k in zip(c["n"], c["clusters"])],
        "p": c["p"].map(_p), "p Holm": c["p_holm"].map(_p),
        "MDE nominal": c["mde_nominal"].map(lambda v: _pct(v, False)),
        "MDE Bonferroni": c["mde_bonferroni"].map(lambda v: _pct(v, False)),
        "prediction": c["prediction"], "verdict (Holm, 5%)": c["verdict"]})
    L += [t.to_markdown(index=False), ""]
    L += ["**Reading the nulls (R4: Bonferroni-level MDE).** "
          + " ".join(f"{r.id}: no effect larger than ±{_pct(r.mde_bonferroni, False)}." if r.sides == 2 else
                     f"{r.id}: no positive effect larger than {_pct(r.mde_bonferroni, False)}."
                     for r in c.itertuples() if np.isfinite(r.mde_bonferroni) and r.p_holm >= LEVEL), ""]
    s = R["sensitivity"]
    L += ["## Sensitivity: without bulk filings (R2; V4 flag `bulk_ptr`, a PTR with 50 or more in-scope trades)", "",
          "_Shown beside the confirmatory test, not instead of it, and not part of the Holm family (unadjusted p)._", "",
          pd.DataFrame({"test": s["id"], "statistic": s["statistic"], "all events": s["estimate_all"].map(_pct),
                        "t (all)": s["t_all"].map(_num), "N (all)": s["n_all"],
                        "without bulk filings": s["estimate_ex_bulk"].map(_pct), "t (ex-bulk)": s["t_ex_bulk"].map(_num),
                        "N (ex-bulk)": s["n_ex_bulk"], "p (ex-bulk, unadjusted)": s["p_ex_bulk"].map(_p)}
                       ).to_markdown(index=False), ""]
    r = R["reversal"]
    L += ["## H2 reversal check (E55 d; reported whatever H2 shows)", "",
          "_Copier purchases, mean SPY-adjusted return from the entry date. \"Partly reversed\" = below the 21-day mean; "
          "\"fully reversed\" = at or below zero. Descriptive: no threshold._", "",
          pd.DataFrame({"horizon (trading days)": r["horizon_days"], "mean": r["estimate"].map(_pct),
                        "t (clustered)": r["t"].map(_num), "N": r["n"], "reading": r["reading"]}).to_markdown(index=False), ""]
    cy = R["calendar_years"]
    show = cy.copy()
    for _, name in SERIES:
        show[name] = show[name].map(_pct)
    L += ["## Calendar-year returns (each calendar year or part-year of the half)", "",
          "_Monthly returns from data/processed/monthly_returns.csv compounded within each calendar year; total returns in "
          "USD. Risk-matched SPY is RF + k x (SPY - RF) with the k of the metrics run (outputs/tables/phase5_insample_results.md). NANC and KRUZ count only whole months whose "
          "previous month-end close exists for both (from March 2023, E41); where a series covers fewer months than "
          "the row, `coverage` names them._", "",
          show.rename(columns={"year": "year", "months": "months"}).to_markdown(index=False), ""]
    w = R["worst_12m"]
    L += ["## Worst rolling 12 months (compounded monthly returns)", "",
          "_The worst 12 consecutive calendar months of each series, with the other's return over the same months._", "",
          pd.DataFrame({"series": w["series"], "from": w["start"], "to": w["end"], "return": w["return"].map(_pct),
                        "series A, same months": w.get("series A, same months", pd.Series(dtype=float)).map(_pct),
                        "SPY, same months": w.get("SPY, same months", pd.Series(dtype=float)).map(_pct),
                        "12-month windows in the half": w.get("windows", pd.Series(dtype=float))}
                       ).to_markdown(index=False), ""]
    return "\n".join(L)


def write(panel: pd.DataFrame, monthly: pd.DataFrame, calendar: list[str], halves: list[tuple[str, str, str, str]],
          out_dir) -> dict:
    """halves: (file key, label, first, last), e.g. ("insample", "in-sample", "2021-09-01", "2024-02-29")."""
    sources = price_sources()
    out = {}
    for key, label, first, last in halves:
        R = half_report(panel, monthly, calendar, first, last)
        stem = Path(out_dir) / f"confirmatory_{key}"
        R["confirmatory"].to_csv(stem.with_suffix(".csv"), index=False, float_format="%.6g")
        stem.with_suffix(".md").write_text(to_md(R, label, sources))
        out[key] = R
    return out
