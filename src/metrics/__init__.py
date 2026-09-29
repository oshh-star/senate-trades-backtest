"""Stage 'metrics' (Phase 5): performance statistics for series A and B and every benchmark, over identical dates,
and the event study. Definitions: stats.py (statistics), benchmarks.py (benchmark series), event_study.py.

Reads data/processed/daily_book.csv, lots.csv, event_panel.csv, engine_metadata.json (engine stage),
factors_monthly.csv, prices.csv.gz, trading_calendar.csv, price_coverage.csv, trade_records.csv.
Writes:
  outputs/tables/phase5_insample_results.csv and .md   ONE table: strategy and benchmarks side by side
  outputs/tables/phase5_event_study.csv and .md
  outputs/figures/phase5_cumulative_value.png, phase5_drawdowns.png
  data/processed/monthly_returns.csv, daily_returns.csv, universe_members.csv, metrics_insample.json
  the Phase 5 section of outputs/data_quality.md

OUT-OF-SAMPLE FIREWALL: the sample is src.engine.sample_bounds(cfg) (in-sample unless the firewall is open);
prices and factors are cut at its last day before anything is computed, and the engine's output must cover the
same sample (otherwise the stage stops and asks for the engine to be rerun).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.quality import write_section

from . import benchmarks as bm
from . import event_study as es
from . import stats as st

PROCESSED = Path("data/processed")
TABLES = Path("outputs/tables")
FIGS = Path("outputs/figures")
RESULTS = TABLES / "phase5_insample_results"
EVENTS = TABLES / "phase5_event_study"
FIG_CUM = FIGS / "phase5_cumulative_value.png"
FIG_DD = FIGS / "phase5_drawdowns.png"
FACTORS = ["mkt_rf", "smb", "hml", "mom"]


def _months(days: list[str]) -> list[str]:
    return sorted({d[:7] for d in days})


def load_inputs(cfg: dict) -> dict:
    from src.engine import sample_bounds
    first, last_day, label = sample_bounds(cfg)
    meta = json.loads((PROCESSED / "engine_metadata.json").read_text())
    if meta["first_day"] != first or meta["last_day"] > last_day or meta["sample"] != label:
        raise RuntimeError(f"engine output covers {meta['sample']} {meta['first_day']}..{meta['last_day']}, but the "
                           f"config asks for {label} {first}..{last_day}: rerun the engine stage first.")
    daily = pd.read_csv(PROCESSED / "daily_book.csv", dtype={"date": str})
    daily = daily[daily["date"] <= last_day].reset_index(drop=True)
    cal_all = pd.read_csv(PROCESSED / "trading_calendar.csv", dtype=str)["date"].tolist()
    cal = [d for d in cal_all if d <= last_day]
    fm = pd.read_csv(PROCESSED / "factors_monthly.csv", dtype={"month": str}).set_index("month")
    fm = pd.DataFrame({"mkt_rf": fm["mkt_rf_pct"], "smb": fm["smb_pct"], "hml": fm["hml_pct"], "mom": fm["mom_pct"],
                       "rf": fm["rf_pct"]}) / 100.0                      # E25: stored in percent
    cov = pd.read_csv(PROCESSED / "price_coverage.csv", keep_default_na=False)
    cov = cov[cov["has_data"].astype(str) == "True"]
    return {"first": first, "last_day": last_day, "label": label, "meta": meta, "daily": daily, "cal_all": cal_all,
            "cal": cal, "fm": fm, "last_dates": dict(zip(cov["ticker"], cov["last_date"])),
            "first_dates": dict(zip(cov["ticker"], cov["first_date"])),
            "pieces": pd.read_csv(PROCESSED / "lots.csv", dtype={"entry_date": str, "exit_date": str}),
            "panel": pd.read_csv(PROCESSED / "event_panel.csv", dtype={"entry_date": str}, low_memory=False)}


def universe_records(cfg: dict, cal_all: list[str]) -> pd.DataFrame:
    from src.engine import events as evm
    u = evm.load_units(cfg)
    u = u[u["in_scope_ex_window"] & ~u["dropped_by_variant"] & (u["transaction_type"] == "Purchase")
          & (u["price_ticker"] != "")].copy()
    u["entry_date"] = evm.entry_dates(u, cal_all, cfg)
    return u[u["entry_date"] != ""]


def series_stats(r_m: pd.Series, rf_m: pd.Series, F: pd.DataFrame, spy_m: pd.Series, r_d: pd.Series, days: list[str],
                 base: str) -> dict:
    ex = r_m - rf_m
    out = {"months": f"{r_m.index[0]} to {r_m.index[-1]}", "n_months": len(r_m), "ann_return": st.ann_return(r_m),
           "ann_vol": st.ann_vol(r_m), "sharpe": st.sharpe(r_m, rf_m)}
    out.update({f"capm_{k}": v for k, v in st.regress(ex, F, ["mkt_rf"]).items()})
    out.update({f"c4_{k}": v for k, v in st.regress(ex, F, FACTORS).items()})
    dd = st.max_drawdown(r_d, days, base)
    out.update({f"dd_{k}": v for k, v in dd.items() if k not in ("value_index", "drawdown", "dates")})
    out.update(st.correlations(r_m, spy_m))
    return out, dd


def run(cfg: dict) -> dict:
    I = load_inputs(cfg)
    daily, cal, first, last_day = I["daily"], I["cal"], I["first"], I["last_day"]
    days = daily["date"].tolist()
    base = cal[cal.index(days[0]) - 1]                               # the close before the first measured return
    months = _months(days)
    fm = I["fm"]
    missing = [m for m in months if m not in fm.index]
    if missing:
        raise RuntimeError(f"Ken French monthly factors missing for {missing}")
    F, rf_m = fm.loc[months, FACTORS], fm.loc[months, "rf"]
    rf_d = daily.set_index("date")["rf"]

    # ---- prices for benchmarks and holdings (cut at last_day)
    pieces = I["pieces"]
    recs = universe_records(cfg, I["cal_all"])
    kruz = next((b.get("price_symbol", "KRUZ") for b in cfg["benchmarks"] if isinstance(b, dict) and b.get("ticker") == "KRUZ"), "KRUZ")
    need = {"SPY", "NANC", kruz, "GBPUSD=X"} | set(pieces["val_symbol"]) | set(recs["price_ticker"])
    wide = bm.load_prices(need, last_day)
    P = wide.reindex(sorted(set(wide.index) | set(cal))).ffill().reindex(cal)

    # ---- daily series on the window days
    D = {"A": daily.set_index("date")["series_a_return"], "B": daily.set_index("date")["series_b_return"],
         "SPY": daily.set_index("date")["spy_return"]}
    chk = bm.daily_returns(P, "SPY", days)
    assert np.allclose(chk.to_numpy(), D["SPY"].to_numpy(), atol=1e-12), "SPY returns differ from the engine's"
    M = {k: st.monthly(v, days) for k, v in D.items()}
    ex_spy = M["SPY"] - rf_m
    k = {s: st.risk_match_k(M[s] - rf_m, ex_spy) for s in ("A", "B")}
    for s in ("A", "B"):
        M[f"RM_{s}"] = st.risk_matched(M["SPY"], rf_m, k[s])                     # monthly: exact volatility match
        D[f"RM_{s}"] = st.risk_matched(D["SPY"], rf_d, k[s])                     # daily, same k: drawdown and chart
    D["EW"], members = bm.universe_ew(recs, P, cal, days, I["last_dates"], I["first_dates"])
    M["EW"] = st.monthly(D["EW"], days)
    for name, sym in (("NANC", "NANC"), ("KRUZ", kruz)):
        D[name] = bm.daily_returns(P, sym, days)
    fx = P["GBPUSD=X"].reindex([base] + days).to_numpy()
    D["A_GBP"], D["SPY_GBP"] = bm.to_gbp(D["A"], fx), bm.to_gbp(D["SPY"], fx)
    for s in ("A_GBP", "SPY_GBP"):
        M[s] = st.monthly(D[s], days)

    # ---- the overlap sample for NANC and KRUZ: months whose previous close exists for both
    def has_prior_close(sym, m):
        form = cal[cal.index(next(d for d in days if d[:7] == m)) - 1]
        return np.isfinite(wide[sym].get(form, np.nan)) if sym in wide else False
    ov_months = [m for m in months if has_prior_close("NANC", m) and has_prior_close(kruz, m)]
    ov_days = [d for d in days if d[:7] in set(ov_months)]
    ov_base = cal[cal.index(ov_days[0]) - 1] if ov_days else None
    for name in ("NANC", "KRUZ"):
        M[name] = st.monthly(D[name].reindex(ov_days), ov_days) if ov_days else pd.Series(dtype=float)

    # ---- statistics, one column each
    cols = [("Series A (headline)", "A", months), ("Series B (fixed pot)", "B", months), ("SPY", "SPY", months),
            (f"SPY risk-matched to A (k = {k['A']:.2f})", "RM_A", months),
            (f"SPY risk-matched to B (k = {k['B']:.2f})", "RM_B", months), ("Senate universe, equal weight", "EW", months),
            ("NANC", "NANC", ov_months), ("KRUZ (as GOP)", "KRUZ", ov_months),
            ("Series A, NANC/KRUZ months", "A", ov_months), ("Series B, NANC/KRUZ months", "B", ov_months),
            ("SPY, NANC/KRUZ months", "SPY", ov_months)]
    rm_title = {s: f"SPY risk-matched to {s} (k = {k[s]:.2f})" for s in ("A", "B")}
    res, dds = {}, {}
    for title, key, ms in cols:
        if not ms:
            continue
        dsub = [d for d in days if d[:7] in set(ms)]
        b0 = cal[cal.index(dsub[0]) - 1]
        res[title], dds[title] = series_stats(M[key].loc[ms], rf_m.loc[ms], F.loc[ms], M["SPY"].loc[ms],
                                              D[key].reindex(dsub), dsub, b0)
    # ---- turnover and break-even (series A and B)
    book_days = [d for d in cal if d >= I["meta"]["warmup"]["book_first_day"]]
    pre, post, _ = bm.holdings_values(pieces, P, book_days, first)
    to_d = {"A": st.turnover(pre, post)}
    c0 = I["meta"]["reconciliation"]["K_cash"]
    cash_post = daily["pot_cash"].to_numpy()
    cash_pre = np.concatenate([[c0], cash_post[:-1]]) * (1 + daily["rf"].to_numpy())
    to_d["B"] = st.turnover(np.column_stack([pre, cash_pre]), np.column_stack([post, cash_post]))
    turnover_m = {}
    for s, title in (("A", "Series A (headline)"), ("B", "Series B (fixed pot)")):
        tm = pd.Series(to_d[s], index=pd.Index(days).str[:7]).groupby(level=0).sum()
        turnover_m[s] = tm
        ex_rm = float((M[s] - M[f"RM_{s}"]).mean() * 12)
        res[title].update({"turnover_monthly_mean": float(tm.mean()), "turnover_ann": float(tm.mean() * 12),
                           "excess_vs_risk_matched_ann": ex_rm,
                           "excess_vs_risk_matched_geo": res[title]["ann_return"] - res[rm_title[s]]["ann_return"],
                           "break_even_bps": st.break_even_bps(ex_rm, float(tm.mean() * 12))})
    # ---- the event study
    hz = list(cfg["portfolio"]["event_study_horizons"])
    evt = es.table(I["panel"], hz)

    # ---- write everything
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGS.mkdir(parents=True, exist_ok=True)
    tab = results_table(res)
    tab.to_csv(RESULTS.with_suffix(".csv"), index=False)
    gbp = {"A": (st.ann_return(M["A_GBP"]), st.ann_vol(M["A_GBP"])), "SPY": (st.ann_return(M["SPY_GBP"]), st.ann_vol(M["SPY_GBP"]))}
    RESULTS.with_suffix(".md").write_text(results_md(tab, res, k, I, gbp, ov_months, base))
    evt.to_csv(EVENTS.with_suffix(".csv"), index=False)
    EVENTS.with_suffix(".md").write_text(events_md(evt, I, hz))
    mret = pd.DataFrame({"rf": rf_m, **{c: F[c] for c in FACTORS}, **{f"r_{s}": M[s] for s in
                         ("A", "B", "SPY", "RM_A", "RM_B", "EW", "A_GBP", "SPY_GBP")},
                         "r_NANC": M["NANC"], "r_KRUZ": M["KRUZ"], "turnover_A": turnover_m["A"], "turnover_B": turnover_m["B"]})
    mret.index.name = "month"
    mret.to_csv(PROCESSED / "monthly_returns.csv", float_format="%.10g")
    dret = pd.DataFrame({f"r_{s}": D[s] for s in ("A", "B", "SPY", "RM_A", "RM_B", "EW", "NANC", "KRUZ", "A_GBP", "SPY_GBP")})
    dret["rf"], dret["turnover_A"], dret["turnover_B"] = rf_d, to_d["A"], to_d["B"]
    dret.index.name = "date"
    dret.to_csv(PROCESSED / "daily_returns.csv", float_format="%.10g")
    members.to_csv(PROCESSED / "universe_members.csv", index=False)
    (PROCESSED / "metrics_insample.json").write_text(json.dumps(
        {"sample": I["label"], "first_day": first, "last_day": last_day, "base_date": base, "k": k,
         "overlap_months": ov_months, "results": res, "gbp": gbp}, indent=1, default=str))
    figures(D, dds, days, base, k)
    quality_section(I, members, res, ov_months, evt, k)
    a = res["Series A (headline)"]
    print(f"  [metrics] {I['label']} {months[0]}..{months[-1]} ({len(months)} months): series A {a['ann_return']:.2%} a year, "
          f"Sharpe {a['sharpe']:.2f}, CAPM alpha {a['capm_alpha_ann']:.2%} (t {a['capm_t_alpha_ols']:.2f}), Carhart alpha "
          f"{a['c4_alpha_ann']:.2%} (t {a['c4_t_alpha_ols']:.2f}); SPY {res['SPY']['ann_return']:.2%}; -> {RESULTS}.md")
    return {"results": res, "events": evt, "monthly": mret, "daily": dret, "members": members, "k": k}


# ------------------------------------------------------------------ tables
ROWS = [  # (section, label, key, format)
    ("Sample", "Months", "months", "s"), ("Sample", "N months", "n_months", "d"),
    ("Return and risk", "Annualised geometric return", "ann_return", "%"),
    ("Return and risk", "Annualised volatility (monthly sd x sqrt 12)", "ann_vol", "%"),
    ("Return and risk", "Sharpe ratio (excess over RF, x sqrt 12)", "sharpe", "2"),
    ("CAPM", "Alpha, annualised (monthly x 12)", "capm_alpha_ann", "%"), ("CAPM", "t(alpha), OLS", "capm_t_alpha_ols", "2"),
    ("CAPM", "t(alpha), Newey-West 3 lags", "capm_t_alpha_nw", "2"), ("CAPM", "Beta (Mkt-RF)", "capm_b_mkt_rf", "2"),
    ("CAPM", "t(beta), OLS", "capm_t_mkt_rf_ols", "2"), ("CAPM", "t(beta), Newey-West", "capm_t_mkt_rf_nw", "2"),
    ("CAPM", "R-squared", "capm_r2", "2"), ("CAPM", "Minimum detectable alpha (t = 2), annualised", "capm_mda_ann", "%"),
    ("Carhart 4-factor", "Alpha, annualised", "c4_alpha_ann", "%"), ("Carhart 4-factor", "t(alpha), OLS", "c4_t_alpha_ols", "2"),
    ("Carhart 4-factor", "t(alpha), Newey-West 3 lags", "c4_t_alpha_nw", "2"),
    ("Carhart 4-factor", "Mkt-RF loading", "c4_b_mkt_rf", "2"), ("Carhart 4-factor", "t(Mkt-RF), OLS", "c4_t_mkt_rf_ols", "2"),
    ("Carhart 4-factor", "t(Mkt-RF), Newey-West", "c4_t_mkt_rf_nw", "2"),
    ("Carhart 4-factor", "SMB loading", "c4_b_smb", "2"), ("Carhart 4-factor", "t(SMB), OLS", "c4_t_smb_ols", "2"),
    ("Carhart 4-factor", "t(SMB), Newey-West", "c4_t_smb_nw", "2"),
    ("Carhart 4-factor", "HML loading", "c4_b_hml", "2"), ("Carhart 4-factor", "t(HML), OLS", "c4_t_hml_ols", "2"),
    ("Carhart 4-factor", "t(HML), Newey-West", "c4_t_hml_nw", "2"),
    ("Carhart 4-factor", "MOM loading", "c4_b_mom", "2"), ("Carhart 4-factor", "t(MOM), OLS", "c4_t_mom_ols", "2"),
    ("Carhart 4-factor", "t(MOM), Newey-West", "c4_t_mom_nw", "2"),
    ("Carhart 4-factor", "R-squared", "c4_r2", "2"),
    ("Carhart 4-factor", "Minimum detectable alpha (t = 2), annualised", "c4_mda_ann", "%"),
    ("Drawdown (daily)", "Maximum drawdown", "dd_depth", "%"), ("Drawdown (daily)", "Peak date", "dd_peak_date", "s"),
    ("Drawdown (daily)", "Trough date", "dd_trough_date", "s"), ("Drawdown (daily)", "Recovery date", "dd_recovery_date", "s"),
    ("Drawdown (daily)", "Peak to trough (trading days)", "dd_peak_to_trough_days", "d"),
    ("Drawdown (daily)", "Trough to recovery (trading days)", "dd_trough_to_recovery_days", "d"),
    ("Correlation with SPY (monthly)", "All months", "corr_all", "2"),
    ("Correlation with SPY (monthly)", "SPY's worst 20% of months", "corr_worst", "2"),
    ("Correlation with SPY (monthly)", "N months in SPY's worst 20%", "n_worst", "d"),
    ("Trading", "One-sided turnover, annualised", "turnover_ann", "%0"),
    ("Trading", "Excess return over risk-matched SPY, annualised (mean monthly x 12)", "excess_vs_risk_matched_ann", "%"),
    ("Trading", "Break-even one-way cost (bps)", "break_even_bps", "be"),
]


def fmt(v, f: str, key: str = "") -> str:
    if isinstance(v, str):
        return v
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        if f == "be":
            return "none: excess return <= 0"
        return ""
    if f == "%":
        return f"{v:.2%}"
    if f == "%0":
        return f"{v:.0%}"
    if f == "2":
        return f"{v:.2f}"
    if f == "d":
        return f"{int(v):d}"
    if f == "be":
        return f"{v:,.0f}"
    return str(v)


def results_table(res: dict) -> pd.DataFrame:
    rows = []
    for sec, lab, key, f in ROWS:
        row = {"section": sec, "statistic": lab, "key": key}
        for c, r in res.items():
            if key.startswith(("turnover", "excess_vs", "break_even")) and key not in r:
                row[c] = ""
            elif key == "break_even_bps" and r.get(key) is None:
                row[c] = "none: excess return <= 0"
            else:
                row[c] = r.get(key, "")
        rows.append(row)
    return pd.DataFrame(rows)


def results_md(tab: pd.DataFrame, res: dict, k: dict, I: dict, gbp: dict, ov: list[str], base: str) -> str:
    view = tab.copy()
    fmts = {key: f for _, _, key, f in ROWS}
    for c in res:
        view[c] = [fmt(v, fmts[kk], kk) if v != "" else "" for v, kk in zip(tab[c], tab["key"])]
    view = view.drop(columns=["key"])
    main = [c for c in res if "NANC/KRUZ" not in c and c not in ("NANC", "KRUZ (as GOP)")]
    over = [c for c in res if c not in main]
    L = [f"# Phase 5: in-sample results ({I['label']}, {I['first']} to {I['last_day']})", "",
         "_Built by the `metrics` stage of `python run_all.py` (src/metrics/). Out-of-sample firewall shut: nothing after "
         f"{I['last_day']} is used. Monthly returns are compounded from daily returns; Sharpe ratios, volatilities and "
         "regressions use monthly returns; drawdowns use the daily value index (1 at the close of "
         f"{base}). RF = Ken French US RF (monthly file, converted from percent). Every column in a panel covers "
         "identical dates. Both factor models are always reported. All numbers are also in "
         f"`{RESULTS.with_suffix('.csv')}` (unrounded)._", "",
         "## Panel 1: full in-sample period", "",
         view[["section", "statistic"] + main].to_markdown(index=False), "",
         f"## Panel 2: NANC and KRUZ, the months their history covers ({ov[0] if ov else '-'} to {ov[-1] if ov else '-'}, "
         f"{len(ov)} months)", "",
         "Both ETFs launched on 2023-02-07; a month is included when both have a close on the previous month's last "
         "trading day. KRUZ is priced with Yahoo symbol GOP (renamed 2025-03-21, E34). Series A, B and SPY are "
         "recomputed over exactly these months. With 12 monthly observations the regressions (5 parameters in "
         "Carhart) have very few degrees of freedom: read them as descriptive.", "",
         view[["section", "statistic"] + over].to_markdown(index=False) if over else "_No overlap._", "",
         "## Notes", "",
         f"- **Risk-matched SPY** = RF + k (SPY - RF) with k = sd(strategy monthly excess return) / sd(SPY monthly excess "
         f"return): k = {k['A']:.3f} for series A, {k['B']:.3f} for series B (k > 1 means borrowing at RF). Built monthly "
         "(its monthly volatility matches the strategy's exactly); its drawdown uses the daily version with the same k.",
         "- **Senate universe, equal weight**: each month, every symbol with an in-scope senator purchase whose entry "
         "date (first trading day after disclosure) is in the 12 months up to the previous month's last trading day, "
         "equally weighted at that close and held for the month. Symbols without prices are left out (Phase 5 section "
         "of outputs/data_quality.md). It separates WHICH stocks senators buy from WHEN they trade them.",
         "- **Turnover** (series A and B only): each day, 0.5 x sum of |weight after trades - weight before trades "
         "(after drift)|; series B's weights include its cash; summed within each month, annualised as mean x 12. "
         "**Break-even one-way cost** = (mean monthly return of the strategy minus its risk-matched SPY) x 12 / "
         "(2 x annual turnover), in basis points; when that excess return is not positive, there is no break-even cost.",
         "- **Minimum detectable alpha** = 2 x OLS standard error of the monthly alpha x 12: the annualised alpha that "
         "would have produced t = 2 with this residual volatility and number of months.",
         "- **Newey-West**: Bartlett kernel, 3 lags (statsmodels HAC).",
         f"- **Sterling check** (series A for a UK investor, GBPUSD=X): series A {gbp['A'][0]:.2%} a year in GBP "
         f"(volatility {gbp['A'][1]:.2%}), against {res['Series A (headline)']['ann_return']:.2%} in USD; SPY "
         f"{gbp['SPY'][0]:.2%} in GBP (volatility {gbp['SPY'][1]:.2%}) against {res['SPY']['ann_return']:.2%} in USD.",
         f"- **Warm-up (L2)**: the book was built from disclosures from {I['meta']['warmup']['warmup_first_disclosure_date']}; "
         f"returns are measured from {I['first']}. The Phase 4 empty start is variant V17 (not run through these metrics).",
         ""]
    return "\n".join(L)


def events_md(evt: pd.DataFrame, I: dict, hz: list[int]) -> str:
    L = [f"# Phase 5: event study ({I['label']}, entry dates {I['first']} to {I['last_day']})", "",
         "_From `data/processed/event_panel.csv`. Returns are SPY-adjusted (stock minus SPY over exactly the same trading "
         "days, total returns). t-statistics use standard errors clustered by calendar month of entry; the iid t is "
         "shown for comparison. Horizons past the last in-sample day are censored, so N falls with the horizon._", "",
         "**Sign convention: every number is the STOCK's return minus SPY's, whatever the side. After a PURCHASE a "
         "positive mean means the stock beat SPY (an informative purchase). After a SALE a NEGATIVE mean means the "
         "stock trailed SPY (an informative sale).**", "",
         "- *senator*: from the close on the transaction date (the first trading day on or after it).",
         "- *copier*: from the close on the entry date (the first trading day after the disclosure).",
         "- *gap*: senator minus copier, event by event, on events with both; what the disclosure delay costs "
         "(for sales, a negative gap means the senator sold before a fall the copier partly missed).",
         "- *pre-disclosure move*: SPY-adjusted return from the transaction-date close to the entry-date close.", ""]
    for side in ("purchase", "sale"):
        q = evt[evt["side"] == side].copy()
        q["mean"] = q["mean"].map(lambda v: f"{v:.2%}" if np.isfinite(v) else "")
        q["median"] = q["median"].map(lambda v: f"{v:.2%}" if np.isfinite(v) else "")
        for c in ("t_cluster", "t_iid"):
            q[c] = q[c].map(lambda v: f"{v:.2f}" if np.isfinite(v) else "")
        q = q.rename(columns={"horizon_days": "horizon (trading days)", "n": "N", "clusters": "months (clusters)",
                              "t_cluster": "t (clustered by entry month)", "t_iid": "t (iid)"})
        L += [f"## {'Purchases' if side == 'purchase' else 'Sales'}", "",
              q.drop(columns=["side"]).to_markdown(index=False), ""]
    return "\n".join(L)


# ------------------------------------------------------------------ figures
SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]     # reference categorical order, light surface


def _style(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)


def figures(D: dict, dds: dict, days: list[str], base: str, k: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    x = pd.to_datetime([base] + days)
    lines = [("Series A (headline)", "A"), ("SPY", "SPY"), (f"SPY risk-matched to A (k = {k['A']:.2f})", "RM_A"),
             ("Senate universe, equal weight", "EW"), ("Series B (fixed pot)", "B")]
    fig, ax = plt.subplots(figsize=(9, 5.2), facecolor=SURFACE)
    _style(ax)
    ends = []
    for (lab, key), c in zip(lines, SLOTS):
        v = np.concatenate([[1.0], np.cumprod(1 + D[key].reindex(days).to_numpy())])
        ax.plot(x, v, color=c, linewidth=2 if key == "A" else 1.6, label=lab, zorder=3 if key == "A" else 2)
        ends.append([v[-1], v[-1], c])
    lo, hi = ax.get_ylim()
    gap = 0.035 * (hi - lo)                                   # spread end labels so they never overlap
    ends.sort(key=lambda e: e[0])
    for i in range(1, len(ends)):
        ends[i][1] = max(ends[i][1], ends[i - 1][1] + gap)
    for val, ypos, c in ends:
        ax.annotate(f"{val:.2f}", (x[-1], val), xytext=(x[-1] + pd.Timedelta(days=12), ypos), fontsize=8, color=INK2,
                    va="center", arrowprops={"arrowstyle": "-", "color": c, "linewidth": 0.8})
    ax.set_xlim(right=x[-1] + pd.Timedelta(days=45))
    ax.axhline(1, color=MUTED, linewidth=0.8, zorder=1)
    ax.set_ylabel("Value of $1 invested at the close of " + base + " (USD, total return)", color=INK2, fontsize=9)
    ax.set_xlabel("Date", color=INK2, fontsize=9)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", labelcolor=INK)
    ax.set_title(f"Cumulative value, in-sample {days[0]} to {days[-1]} (daily)", loc="left", color=INK, fontsize=12)
    fig.text(0.01, 0.01, "NANC and KRUZ start in March 2023 and are compared over their own months in the results table.",
             fontsize=7.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(FIG_CUM, dpi=150, facecolor=SURFACE)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.0), facecolor=SURFACE)
    _style(ax)
    for (lab, title), c in zip((("Series A (headline)", "Series A (headline)"), ("SPY", "SPY")), SLOTS):
        dd = dds[title]
        xx = pd.to_datetime(dd["dates"])
        ax.plot(xx, dd["drawdown"] * 100, color=c, linewidth=2 if lab.startswith("Series") else 1.6,
                label=f"{lab}: maximum {dd['depth']:.1%}, trough {dd['trough_date']}")
        t = dd["dates"].index(dd["trough_date"])
        ax.plot([xx[t]], [dd["depth"] * 100], marker="o", markersize=8, color=c, markeredgecolor=SURFACE,
                markeredgewidth=2, zorder=4)
    ax.axhline(0, color=MUTED, linewidth=0.8)
    ax.set_ylabel("Drawdown from previous peak (%)", color=INK2, fontsize=9)
    ax.set_xlabel("Date", color=INK2, fontsize=9)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", bbox_to_anchor=(0, -0.14), ncol=2, labelcolor=INK)
    ax.set_title(f"Drawdowns of the daily value index, in-sample {days[0]} to {days[-1]}", loc="left", color=INK, fontsize=12)
    fig.tight_layout()
    fig.savefig(FIG_DD, dpi=150, facecolor=SURFACE)
    plt.close(fig)


# ------------------------------------------------------------------ data quality
def quality_section(I: dict, members: pd.DataFrame, res: dict, ov: list[str], evt: pd.DataFrame, k: dict) -> None:
    left = members["left_out_symbols"].str.split().explode().dropna()
    left_t = left.value_counts().rename_axis("symbol").reset_index(name="months left out")
    panel = I["panel"]
    L = ["## Phase 5: metrics and benchmarks (in-sample only)", "",
         f"_Stage `metrics`. Sample {I['label']} {I['first']} to {I['last_day']}; prices and factors cut there. Results: "
         f"`{RESULTS.with_suffix('.md')}`, `{EVENTS.with_suffix('.md')}`._", "",
         "### 1. Senate universe (equal weight): members and symbols left out", "",
         f"Members per month: min {members['members_priced'].min()}, median {members['members_priced'].median():.0f}, "
         f"max {members['members_priced'].max()}. Symbols with a qualifying purchase but no usable price at the formation "
         f"close (survivorship ledger, or a series not yet started / already ended) are left out: "
         f"{members['left_out_no_price'].sum()} symbol-months, {left.nunique()} symbols. Month by month in "
         "`data/processed/universe_members.csv`.", "",
         left_t.to_markdown(index=False) if len(left_t) else "_None._", "",
         "### 2. NANC and KRUZ", "",
         f"Both launched 2023-02-07; in-sample months with a full month of returns: {len(ov)} "
         f"({ov[0] if ov else '-'} to {ov[-1] if ov else '-'}). Yahoo serves no history for KRUZ (renamed GOP on "
         "2025-03-21), so KRUZ is priced with GOP (E34).", "",
         "### 3. Event study sample", "",
         f"{len(panel)} in-scope purchase and sale records with an in-sample entry date; {int(panel['no_price'].astype(str).eq('True').sum())} "
         "have no price on the entry date and drop out of every horizon; longer horizons lose events to censoring at the "
         "last in-sample day (N per row in the event study table).", ""]
    write_section(5, L)
