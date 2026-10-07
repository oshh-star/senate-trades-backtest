"""Stage 'metrics' (Phase 5): performance statistics for series A and B and every benchmark, over identical dates,
and the event study. Definitions: stats.py (statistics), benchmarks.py (benchmark series), event_study.py.

Reads data/processed/daily_book.csv, lots.csv, event_panel.csv, engine_metadata.json (engine stage),
factors_monthly.csv, prices.csv.gz, trading_calendar.csv, price_coverage.csv, trade_records.csv.
Writes:
  outputs/tables/phase5_insample_results.csv and .md   ONE table: strategy and benchmarks side by side
  outputs/tables/phase5_event_study.csv and .md
  outputs/tables/confirmatory_insample.csv and .md (and confirmatory_oos once the firewall is open): H0-H4,
    calendar-year returns, worst rolling 12 months (confirmatory.py)
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
DRIFT = TABLES / "phase5_predisclosure_drift"
FIG_CUM = FIGS / "phase5_cumulative_value.png"
FIG_DD = FIGS / "phase5_drawdowns.png"
FACTORS = ["mkt_rf", "smb", "hml", "mom"]


def _months(days: list[str]) -> list[str]:
    return sorted({d[:7] for d in days})


def load_inputs(cfg: dict, engine_dir: Path | None = None) -> dict:
    """engine_dir: where the engine's files are (default data/processed/; a variant's own folder for the runner)."""
    from src.engine import sample_bounds
    ed = Path(engine_dir) if engine_dir else PROCESSED
    first, last_day, label = sample_bounds(cfg)
    meta = json.loads((ed / "engine_metadata.json").read_text())
    if meta["first_day"] != first or meta["last_day"] > last_day or meta["sample"] != label:
        raise RuntimeError(f"engine output covers {meta['sample']} {meta['first_day']}..{meta['last_day']}, but the "
                           f"config asks for {label} {first}..{last_day}: rerun the engine stage first.")
    daily = pd.read_csv(ed / "daily_book.csv", dtype={"date": str})
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
            "pieces": pd.read_csv(ed / "lots.csv", dtype={"entry_date": str, "exit_date": str}),
            "panel": pd.read_csv(ed / "event_panel.csv", dtype={"entry_date": str}, low_memory=False)}


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


def run(cfg: dict, engine_dir: Path | None = None, write: bool = True) -> dict:
    """write=False (the variant runner): compute and return the statistics, write nothing.

    In-sample (firewall shut): one period, the in-sample half. Full window (firewall open, S5): the MAIN period is the
    whole window, one continuous run; the out-of-sample half is read off the same run as a second period (its own
    risk-matched k, NANC/KRUZ months, drawdown base and turnover months)."""
    I = load_inputs(cfg, engine_dir)
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
    D["EW"], members = bm.universe_ew(recs, P, cal, days, I["last_dates"], I["first_dates"])
    M["EW"] = st.monthly(D["EW"], days)
    for name, sym in (("NANC", "NANC"), ("KRUZ", kruz)):
        D[name] = bm.daily_returns(P, sym, days)
    fx = P["GBPUSD=X"].reindex([base] + days).to_numpy()
    D["A_GBP"], D["SPY_GBP"] = bm.to_gbp(D["A"], fx), bm.to_gbp(D["SPY"], fx)
    for s in ("A_GBP", "SPY_GBP"):
        M[s] = st.monthly(D[s], days)

    # ---- turnover (series A and B), daily over the whole sample
    book_days = [d for d in cal if d >= I["meta"]["warmup"]["book_first_day"]]
    pre, post, _ = bm.holdings_values(pieces, P, book_days, first)
    to_d = {"A": st.turnover(pre, post)}
    c0 = I["meta"]["reconciliation"]["K_cash"]
    cash_post = daily["pot_cash"].to_numpy()
    cash_pre = np.concatenate([[c0], cash_post[:-1]]) * (1 + daily["rf"].to_numpy())
    to_d["B"] = st.turnover(np.column_stack([pre, cash_pre]), np.column_stack([post, cash_post]))
    turnover_m = {s: pd.Series(to_d[s], index=pd.Index(days).str[:7]).groupby(level=0).sum() for s in ("A", "B")}

    def has_prior_close(sym, m):
        form = cal[cal.index(next(d for d in days if d[:7] == m)) - 1]
        return np.isfinite(wide[sym].get(form, np.nan)) if sym in wide else False

    def period(ms: list[str]) -> dict:
        """Every statistic over the months ms (all of them, or one half), identical dates in every column."""
        dsub = [d for d in days if d[:7] in set(ms)]
        b0 = cal[cal.index(dsub[0]) - 1]
        Mp = {key: M[key].loc[ms] for key in ("A", "B", "SPY", "EW", "A_GBP", "SPY_GBP")}
        Dp = {key: D[key].reindex(dsub) for key in ("A", "B", "SPY", "EW", "NANC", "KRUZ")}
        ex_spy = Mp["SPY"] - rf_m.loc[ms]
        k = {s: st.risk_match_k(Mp[s] - rf_m.loc[ms], ex_spy) for s in ("A", "B")}
        for s in ("A", "B"):
            Mp[f"RM_{s}"] = st.risk_matched(Mp["SPY"], rf_m.loc[ms], k[s])        # monthly: exact volatility match
            Dp[f"RM_{s}"] = st.risk_matched(D["SPY"], rf_d, k[s]).reindex(dsub)   # daily, same k: drawdown and chart
        # NANC and KRUZ: the months whose previous close exists for both
        ov = [m for m in ms if has_prior_close("NANC", m) and has_prior_close(kruz, m)]
        ov_days = [d for d in dsub if d[:7] in set(ov)]
        for name in ("NANC", "KRUZ"):
            Mp[name] = st.monthly(D[name].reindex(ov_days), ov_days) if ov_days else pd.Series(dtype=float)
        cols = [("Series A (headline)", "A", ms), ("Series B (fixed pot)", "B", ms), ("SPY", "SPY", ms),
                (f"SPY risk-matched to A (k = {k['A']:.2f})", "RM_A", ms),
                (f"SPY risk-matched to B (k = {k['B']:.2f})", "RM_B", ms), ("Senate universe, equal weight", "EW", ms),
                ("NANC", "NANC", ov), ("KRUZ (as GOP)", "KRUZ", ov),
                ("Series A, NANC/KRUZ months", "A", ov), ("Series B, NANC/KRUZ months", "B", ov),
                ("SPY, NANC/KRUZ months", "SPY", ov)]
        rm_title = {s: f"SPY risk-matched to {s} (k = {k[s]:.2f})" for s in ("A", "B")}
        res, dds = {}, {}
        for title, key, mm in cols:
            if not mm:
                continue
            ds = [d for d in dsub if d[:7] in set(mm)]
            bb = cal[cal.index(ds[0]) - 1]
            res[title], dds[title] = series_stats(Mp[key].loc[mm], rf_m.loc[mm], F.loc[mm], M["SPY"].loc[mm],
                                                  Dp[key].reindex(ds), ds, bb)
        for s, title in (("A", "Series A (headline)"), ("B", "Series B (fixed pot)")):
            tm = turnover_m[s].loc[ms]
            ex_rm = float((Mp[s] - Mp[f"RM_{s}"]).mean() * 12)
            res[title].update({"turnover_monthly_mean": float(tm.mean()), "turnover_ann": float(tm.mean() * 12),
                               "excess_vs_risk_matched_ann": ex_rm,
                               "excess_vs_risk_matched_geo": res[title]["ann_return"] - res[rm_title[s]]["ann_return"],
                               "break_even_bps": st.break_even_bps(ex_rm, float(tm.mean() * 12))})
        gbp = {"A": (st.ann_return(Mp["A_GBP"]), st.ann_vol(Mp["A_GBP"])),
               "SPY": (st.ann_return(Mp["SPY_GBP"]), st.ann_vol(Mp["SPY_GBP"]))}
        mon = pd.DataFrame({"rf": rf_m.loc[ms], **{c: F.loc[ms, c] for c in FACTORS},
                            **{f"r_{s}": Mp[s] for s in ("A", "B", "SPY", "RM_A", "RM_B", "EW", "A_GBP", "SPY_GBP")},
                            "r_NANC": Mp["NANC"], "r_KRUZ": Mp["KRUZ"], "turnover_A": turnover_m["A"].loc[ms],
                            "turnover_B": turnover_m["B"].loc[ms]})
        mon.index.name = "month"
        return {"res": res, "dds": dds, "k": k, "ov": ov, "gbp": gbp, "monthly": mon, "days": dsub, "base": b0,
                "D": Dp, "months": ms}

    full = I["label"] != "in-sample"
    halves = {}
    if full:                                                         # the firewall is open (sample_bounds)
        from src.config import sample_split
        sp = sample_split(cfg)
        halves = {"oos": ("out-of-sample half", *[d.isoformat() for d in sp["out_of_sample"]])}
    main_key = "full" if full else "insample"
    PER = {main_key: period(months)}
    for key, (_, a, b) in halves.items():
        PER[key] = period([m for m in months if a[:7] <= m <= b[:7]])
    main = PER[main_key]
    res, k, ov_months, gbp = main["res"], main["k"], main["ov"], main["gbp"]

    # ---- the event study
    hz = list(cfg["portfolio"]["event_study_horizons"])
    evt = es.table(I["panel"], hz)
    drift = es.drift_table(I["panel"])
    if not write:
        return {"results": res, "events": evt, "drift": drift, "k": k, "months": months, "meta": I["meta"],
                "periods": {key: p["res"] for key, p in PER.items()}}

    # ---- write everything
    from . import committee, confirmatory, mechanism
    from src.variants import price_tag
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGS.mkdir(parents=True, exist_ok=True)
    mret = main["monthly"]
    mret.to_csv(PROCESSED / "monthly_returns.csv", float_format="%.10g")
    dret = pd.DataFrame({f"r_{s}": (main["D"][s] if s in main["D"] else D[s])
                         for s in ("A", "B", "SPY", "RM_A", "RM_B", "EW", "NANC", "KRUZ", "A_GBP", "SPY_GBP")})
    dret["rf"], dret["turnover_A"], dret["turnover_B"] = rf_d, to_d["A"], to_d["B"]
    dret.index.name = "date"
    dret.to_csv(PROCESSED / "daily_returns.csv", float_format="%.10g")
    members.to_csv(PROCESSED / "universe_members.csv", index=False)
    (PROCESSED / f"metrics_{'full' if full else 'insample'}.json").write_text(json.dumps(
        {"sample": I["label"], "first_day": first, "last_day": last_day, "base_date": base, "k": k,
         "overlap_months": ov_months, "results": res, "gbp": gbp,
         **({"periods": {key: {"k": p["k"], "overlap_months": p["ov"], "results": p["res"], "gbp": p["gbp"]}
                         for key, p in PER.items() if key != main_key}} if full else {})}, indent=1, default=str))
    if not full:
        tab = results_table(res)
        tab.to_csv(RESULTS.with_suffix(".csv"), index=False)
        RESULTS.with_suffix(".md").write_text(results_md(tab, res, k, I, gbp, ov_months, base))
        evt.to_csv(EVENTS.with_suffix(".csv"), index=False)
        EVENTS.with_suffix(".md").write_text(events_md(evt, I, hz))
        drift.to_csv(DRIFT.with_suffix(".csv"), index=False)
        DRIFT.with_suffix(".md").write_text(drift_md(drift, I))
        figures({**D, **main["D"]}, main["dds"], days, base, k)
        mechanism.write(I["panel"], I["label"], first, last_day, price_tag(), TABLES)
        committee.write(I["panel"], I["label"], first, last_day, price_tag(), TABLES)
        confirmatory.write(I["panel"], mret, I["cal_all"], [("insample", "in-sample", first, last_day)], TABLES)
    else:
        spans = {"full": ("full window", first, last_day), **halves}
        for key, (label, a, b) in spans.items():
            p = PER[key]
            stem = TABLES / f"phase5_{key}_results"
            tab = results_table(p["res"])
            tab.to_csv(stem.with_suffix(".csv"), index=False)
            Ip = {**I, "label": label, "first": a, "last_day": b}
            stem.with_suffix(".md").write_text(
                results_md(tab, p["res"], p["k"], Ip, p["gbp"], p["ov"], p["base"], stem=stem, full_first=first)
                + period_years_md(p["monthly"], label))
            panel_p = confirmatory.restrict(I["panel"], I["cal_all"], a, b)
            e_p, d_p = es.table(panel_p, hz), es.drift_table(panel_p)
            e_stem, d_stem = TABLES / f"phase5_event_study_{key}", TABLES / f"phase5_predisclosure_drift_{key}"
            e_p.to_csv(e_stem.with_suffix(".csv"), index=False)
            e_stem.with_suffix(".md").write_text(events_md(e_p, Ip, hz, exploratory=True))
            d_p.to_csv(d_stem.with_suffix(".csv"), index=False)
            d_stem.with_suffix(".md").write_text(drift_md(d_p, Ip, exploratory=True))
            mechanism.write(panel_p, label, a, b, price_tag(), TABLES, key=key, exploratory=True)
            committee.write(panel_p, label, a, b, price_tag(), TABLES, key=key, exploratory=True)
        _, a, b = halves["oos"]
        confirmatory.write(I["panel"], PER["oos"]["monthly"], I["cal_all"], [("oos", "out-of-sample", a, b)], TABLES)
        figures({**D, **main["D"]}, main["dds"], days, base, k, boundary=halves["oos"][1])
    quality_section(I, members, res, ov_months, evt, k)
    a = res["Series A (headline)"]
    out_md = RESULTS if not full else TABLES / "phase5_full_results"
    print(f"  [metrics] {I['label']} {months[0]}..{months[-1]} ({len(months)} months): series A {a['ann_return']:.2%} a year, "
          f"Sharpe {a['sharpe']:.2f}, CAPM alpha {a['capm_alpha_ann']:.2%} (t {a['capm_t_alpha_ols']:.2f}), Carhart alpha "
          f"{a['c4_alpha_ann']:.2%} (t {a['c4_t_alpha_ols']:.2f}); SPY {res['SPY']['ann_return']:.2%}; -> {out_md}.md")
    return {"results": res, "events": evt, "monthly": mret, "daily": dret, "members": members, "k": k,
            "periods": {key: p["res"] for key, p in PER.items()}}


def period_years_md(mon: pd.DataFrame, label: str) -> str:
    """Calendar-year returns and the worst rolling 12 months for one period (confirmatory.py's definitions, E56)."""
    from . import confirmatory as cf
    cy = cf.calendar_years(mon)
    show = cy.copy()
    for _, name in cf.SERIES:
        show[name] = show[name].map(cf._pct)
    w = cf.worst_12m(mon)
    wv = pd.DataFrame({"series": w["series"], "from": w["start"], "to": w["end"], "return": w["return"].map(cf._pct),
                       "series A, same months": w.get("series A, same months", pd.Series(dtype=float)).map(cf._pct),
                       "SPY, same months": w.get("SPY, same months", pd.Series(dtype=float)).map(cf._pct),
                       "12-month windows": w.get("windows", pd.Series(dtype=float))})
    return "\n".join([
        f"## Calendar-year returns ({label})", "",
        "_Monthly returns compounded within each calendar year or part-year; USD total returns. Risk-matched SPY uses this "
        "table's k. NANC and KRUZ only over the months both have a previous month-end close (E41); `coverage` names them._",
        "", show.to_markdown(index=False), "",
        f"## Worst rolling 12 months ({label})", "",
        "_The worst 12 consecutive calendar months (compounded monthly returns) of series A and of SPY, with the other's "
        "return over the same months._", "", wv.to_markdown(index=False), ""])

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


def results_md(tab: pd.DataFrame, res: dict, k: dict, I: dict, gbp: dict, ov: list[str], base: str,
               stem: Path = RESULTS, full_first: str | None = None) -> str:
    """One results table. In-sample (stem RESULTS) the text is the Phase 5 one; for the full window and the
    out-of-sample half (Phase 5B, firewall open) the title and the firewall sentence say so."""
    view = tab.copy()
    fmts = {key: f for _, _, key, f in ROWS}
    for c in res:
        view[c] = [fmt(v, fmts[kk], kk) if v != "" else "" for v, kk in zip(tab[c], tab["key"])]
    view = view.drop(columns=["key"])
    main = [c for c in res if "NANC/KRUZ" not in c and c not in ("NANC", "KRUZ (as GOP)")]
    over = [c for c in res if c not in main]
    insample = stem == RESULTS
    title = (f"# Phase 5: in-sample results ({I['label']}, {I['first']} to {I['last_day']})" if insample else
             f"# Phase 5B: results, {I['label']} ({I['first']} to {I['last_day']})")
    fw = (f"Out-of-sample firewall shut: nothing after {I['last_day']} is used." if insample else
          "Out-of-sample firewall open (rules frozen at `project.frozen_rules_commit`). ONE continuous backtest of the "
          f"whole window from {full_first}, with the warm-up before it (S5); this table reads the period {I['first']} to "
          f"{I['last_day']} off that run (risk-matched k, NANC/KRUZ months and the drawdown base are this period's own).")
    L = [title, "",
         f"_Built by the `metrics` stage of `python run_all.py` (src/metrics/). {fw} Monthly returns are compounded from daily returns; Sharpe ratios, volatilities and "
         "regressions use monthly returns; drawdowns use the daily value index (1 at the close of "
         f"{base}). RF = Ken French US RF (monthly file, converted from percent). Every column in a panel covers "
         "identical dates. Both factor models are always reported. All numbers are also in "
         f"`{stem.with_suffix('.csv')}` (unrounded)._", "",
         "## Panel 1: full in-sample period" if insample else f"## Panel 1: the whole period ({I['label']})", "",
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
         f"returns are measured from {full_first or I['first']}. The Phase 4 empty start is variant V17"
         + (" (not run through these metrics)." if insample else " (in the variants table)."),
         ""]
    return "\n".join(L)


def events_md(evt: pd.DataFrame, I: dict, hz: list[int], exploratory: bool = False) -> str:
    from .confirmatory import EXPLORATORY_NOTE
    L = [f"# Phase {'5B' if exploratory else '5'}: event study ({I['label']}, entry dates {I['first']} to {I['last_day']})", "",
         *([EXPLORATORY_NOTE, ""] if exploratory else []),
         "_From `data/processed/event_panel.csv`. Returns are SPY-adjusted (stock minus SPY over exactly the same trading "
         "days, total returns). t-statistics use standard errors clustered by calendar month of entry; the iid t is "
         "shown for comparison. Horizons past the last " + ("day of the sample" if exploratory else "in-sample day")
         + " are censored, so N falls with the horizon._", "",
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


def drift_md(d: pd.DataFrame, I: dict, exploratory: bool = False) -> str:
    from .confirmatory import EXPLORATORY_NOTE
    v = d.copy()
    for c in ("mean SPY-adjusted drift", "median SPY-adjusted drift", "mean stock return", "mean SPY return",
              "mean cost to the copier", "share of events against the copier"):
        v[c] = v[c].map(lambda x: f"{x:.2%}")
    for c in ("t (clustered by entry month)", "t (iid)"):
        v[c] = v[c].map(lambda x: f"{x:.2f}")
    v["median lag (trading days)"] = v["median lag (trading days)"].map(lambda x: f"{x:.0f}")
    return "\n".join([
        f"# Phase {'5B' if exploratory else '5'}: pre-disclosure drift ({I['label']}, entry dates {I['first']} to {I['last_day']})", "",
        *([EXPLORATORY_NOTE, ""] if exploratory else []),
        "_What the disclosure lag costs a copier: the stock's return minus SPY's from the close on the TRANSACTION date "
        "(the senator's trade; the first trading day on or after it) to the close on the ENTRY date (the first trading day "
        "after the disclosure, when the copier acts). Every in-scope purchase and sale record with an "
        + ("entry date in the sample " if exploratory else "in-sample entry date ") +
        "and prices on both dates counts once. t-statistics cluster by calendar month of entry. From "
        "`data/processed/event_panel.csv` (column gap_x)._", "",
        "**Sign convention.** The drift is the stock's move, whatever the side. For a PURCHASE a positive drift means the "
        "price ran up before the copier could buy (a cost). For a SALE a negative drift means the price fell before the "
        "copier could sell (a cost). \"Mean cost to the copier\" flips the sign for sales so that positive always means "
        "the lag hurt the copier.", "",
        v.to_markdown(index=False), ""])


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


def _boundary(ax, day: str) -> None:
    """The in-sample / out-of-sample split: a dashed vertical line, labelled on both sides at the top."""
    x0 = pd.Timestamp(day)
    ax.axvline(x0, color=INK2, linewidth=1, linestyle=(0, (4, 3)), zorder=1)
    top = ax.get_ylim()[1]
    ax.annotate("in-sample  ", (x0, top), xytext=(-4, -4), textcoords="offset points", ha="right", va="top", fontsize=8,
                color=INK2)
    ax.annotate(f"  out-of-sample (from {day})", (x0, top), xytext=(4, -4), textcoords="offset points", ha="left",
                va="top", fontsize=8, color=INK2)


def figures(D: dict, dds: dict, days: list[str], base: str, k: dict, boundary: str | None = None) -> None:
    """boundary: the first day of the out-of-sample half (full window only): a dashed line marks the split."""
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
    span = "full window" if boundary else "in-sample"
    if boundary:
        _boundary(ax, boundary)
    ax.set_title(f"Cumulative value, {span} {days[0]} to {days[-1]} (daily)", loc="left", color=INK, fontsize=12)
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
    if boundary:
        _boundary(ax, boundary)
    ax.set_title(f"Drawdowns of the daily value index, {span} {days[0]} to {days[-1]}", loc="left", color=INK, fontsize=12)
    fig.tight_layout()
    fig.savefig(FIG_DD, dpi=150, facecolor=SURFACE)
    plt.close(fig)


# ------------------------------------------------------------------ data quality
def quality_section(I: dict, members: pd.DataFrame, res: dict, ov: list[str], evt: pd.DataFrame, k: dict) -> None:
    left = members["left_out_symbols"].str.split().explode().dropna()
    left_t = left.value_counts().rename_axis("symbol").reset_index(name="months left out")
    panel = I["panel"]
    insample = I["label"] == "in-sample"
    outs = (f"`{RESULTS.with_suffix('.md')}`, `{EVENTS.with_suffix('.md')}`" if insample else
            "`outputs/tables/phase5_full_results.md`, `outputs/tables/phase5_oos_results.md`, "
            "`outputs/tables/confirmatory_oos.md`")
    L = ["## Phase 5: metrics and benchmarks (" + ("in-sample only" if insample else "full window, firewall open") + ")", "",
         f"_Stage `metrics`. Sample {I['label']} {I['first']} to {I['last_day']}; prices and factors cut there. Results: "
         f"{outs}._", "",
         "### 1. Senate universe (equal weight): members and symbols left out", "",
         f"Members per month: min {members['members_priced'].min()}, median {members['members_priced'].median():.0f}, "
         f"max {members['members_priced'].max()}. Symbols with a qualifying purchase but no usable price at the formation "
         f"close (survivorship ledger, or a series not yet started / already ended) are left out: "
         f"{members['left_out_no_price'].sum()} symbol-months, {left.nunique()} symbols. Month by month in "
         "`data/processed/universe_members.csv`.", "",
         left_t.to_markdown(index=False) if len(left_t) else "_None._", "",
         "### 2. NANC and KRUZ", "",
         f"Both launched 2023-02-07; {'in-sample' if insample else 'sample'} months with a full month of returns: {len(ov)} "
         f"({ov[0] if ov else '-'} to {ov[-1] if ov else '-'}). Yahoo serves no history for KRUZ (renamed GOP on "
         "2025-03-21), so KRUZ is priced with GOP (E34).", "",
         "### 3. Event study sample", "",
         f"{len(panel)} in-scope purchase and sale records with an " + ("in-sample entry date" if insample else
                                                                         "entry date in the sample") + "; "
         f"{int(panel['no_price'].astype(str).eq('True').sum())} "
         "have no price on the entry date and drop out of every horizon; longer horizons lose events to censoring at the "
         + ("last in-sample day" if insample else "last day of the window") + " (N per row in the event study table).", ""]
    write_section(5, L)
