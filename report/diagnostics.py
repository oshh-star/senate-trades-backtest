"""Extra robustness diagnostics for the written report (Report V3).

Not registered tests: computed after the unlock from the committed monthly returns, to show how much the five-year
sample can and cannot say. Nothing here feeds the pipeline. Run from the repo root:

    python report/diagnostics.py

Writes report/diagnostics.json and report/diagnostics.md.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report"
M = pd.read_csv(ROOT / "data" / "processed" / "monthly_returns.csv", parse_dates=["month"])
M = M[(M.month >= "2021-09-01") & (M.month <= "2026-08-31")].reset_index(drop=True)
assert len(M) == 60, len(M)

ex_A = (M.r_A - M.rf).to_numpy()
ex_S = (M.r_SPY - M.rf).to_numpy()
mkt = M.mkt_rf.to_numpy()


def sharpe(x):
    return x.mean() / x.std(ddof=1) * np.sqrt(12)


def capm_alpha(y, x):
    X = sm.add_constant(x)
    return sm.OLS(y, X).fit().params[0] * 12


# 1. Sharpe ratio difference, Jobson-Korkie with Memmel (2003) correction, monthly
def memmel(a, b):
    T = len(a)
    sa, sb = a.std(ddof=1), b.std(ddof=1)
    ma, mb = a.mean(), b.mean()
    rho = np.corrcoef(a, b)[0, 1]
    SRa, SRb = ma / sa, mb / sb
    var = (2 - 2 * rho + 0.5 * (SRa**2 + SRb**2 - 2 * SRa * SRb * rho**2)) / T
    z = (SRa - SRb) / np.sqrt(var)
    return (SRa - SRb) * np.sqrt(12), z, 2 * (1 - stats.norm.cdf(abs(z)))


sr_diff, sr_z, sr_p = memmel(ex_A, ex_S)

# 2. Stationary block bootstrap (Politis-Romano), mean block 6 months, 10,000 draws, fixed seed
rng = np.random.default_rng(20261013)
B, L, T = 10_000, 6, 60
boot_sr_diff, boot_alpha, boot_combo = [], [], []
for _ in range(B):
    idx = np.empty(T, dtype=int)
    t = rng.integers(T)
    for i in range(T):
        idx[i] = t
        t = rng.integers(T) if rng.random() < 1 / L else (t + 1) % T
    a, s, m = ex_A[idx], ex_S[idx], mkt[idx]
    boot_sr_diff.append(sharpe(a) - sharpe(s))
    boot_alpha.append(capm_alpha(a, m))
    boot_combo.append(sharpe(0.9 * s + 0.1 * a) - sharpe(s))
ci = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]

# 3. Does a 10% slice of series A improve an SPY holding? (excess returns; the guidance's condition S_P > rho S_B)
rho = float(np.corrcoef(ex_A, ex_S)[0, 1])
combo_gain = sharpe(0.9 * ex_S + 0.1 * ex_A) - sharpe(ex_S)

# 4. Rolling 24-month CAPM alpha of series A
roll = []
for end in range(24, T + 1):
    y, x = ex_A[end - 24:end], mkt[end - 24:end]
    fit = sm.OLS(y, sm.add_constant(x)).fit()
    roll.append({"month": M.month.iloc[end - 1].strftime("%Y-%m"), "alpha": fit.params[0] * 12,
                 "se": fit.bse[0] * 12})
pd.DataFrame(roll).to_csv(OUT / "rolling_alpha_24m.csv", index=False)

# 5. Years of data needed for t = 2 at this residual volatility (t ~ IR x sqrt(years))
fit = sm.OLS(ex_A, sm.add_constant(mkt)).fit()
resid_vol = float(np.std(fit.resid, ddof=2) * np.sqrt(12))
years_needed = {f"{a:.0%}": (2 * resid_vol / a) ** 2 for a in (0.02, 0.03, 0.05, 0.10)}

# 6. The two halves under the headline prices (the committed design-half table is the frozen Yahoo record)
def half_stats(mask):
    h = M[mask]
    out = {}
    for col in ("r_A", "r_SPY", "r_RM_A"):
        r = h[col].to_numpy()
        ex = r - h.rf.to_numpy()
        out[col] = {"ann_return": float(np.prod(1 + r) ** (12 / len(r)) - 1), "ann_vol": float(r.std(ddof=1) * np.sqrt(12)),
                    "sharpe": float(sharpe(ex))}
    fit = sm.OLS((h.r_A - h.rf).to_numpy(), sm.add_constant(h.mkt_rf.to_numpy())).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    out["capm_alpha"] = float(fit.params[0] * 12)
    out["capm_t_nw"] = float(fit.tvalues[0])
    out["n_months"] = int(mask.sum())
    return out


halves = {"design_2021-09_to_2024-02": half_stats(M.month < "2024-03-01"),
          "test_2024-03_to_2026-08": half_stats(M.month >= "2024-03-01")}

res = {
    "sample": "2021-09 to 2026-08, 60 months, Bloomberg-filled headline (C1)",
    "halves": halves,
    "sharpe_A": sharpe(ex_A), "sharpe_SPY": sharpe(ex_S),
    "sharpe_diff_annual": sr_diff, "sharpe_diff_z_memmel": sr_z, "sharpe_diff_p_memmel": sr_p,
    "sharpe_diff_boot_ci95": ci(boot_sr_diff),
    "capm_alpha_annual": capm_alpha(ex_A, mkt), "capm_alpha_boot_ci95": ci(boot_alpha),
    "corr_A_SPY_excess": rho, "condition_rhs_rho_x_S_SPY": rho * sharpe(ex_S),
    "sharpe_gain_10pct_A_in_SPY": combo_gain, "sharpe_gain_10pct_boot_ci95": ci(boot_combo),
    "share_boot_gain_positive": float(np.mean(np.array(boot_combo) > 0)),
    "capm_resid_vol_annual": resid_vol, "years_needed_for_t2": years_needed,
    "bootstrap": {"draws": B, "mean_block_months": L, "seed": 20261013},
}


def sleeve_returns(lots, prices, days):
    """Series A's daily return rebuilt from the lots, for any subset of them: dollar-weighted return of the lots held
    from the previous close (the engine's definition, data/processed/lots.csv). Returns (return, capital) by day."""
    num, den = np.zeros(len(days)), np.zeros(len(days))
    for r in lots.itertuples():
        if r.val_symbol not in prices:
            continue
        p = prices[r.val_symbol].to_numpy()
        a = max(int(np.searchsorted(days, r.entry_date, side="right")), 1)
        b = int(np.searchsorted(days, r.exit_date, side="right"))
        if b <= a:
            continue
        prev, cur = p[a - 1:b - 1], p[a:b].copy()
        if days[b - 1] == r.exit_date:
            cur[-1] = r.exit_price
        num[a:b] += r.units * (cur - prev)
        den[a:b] += r.units * prev
    with np.errstate(invalid="ignore", divide="ignore"):
        ret = np.where(den > 0, num / den, 0.0)
    return pd.Series(ret[1:], index=days[1:]), pd.Series(den[1:], index=days[1:])


# Who drives series A: Mullin's positions against the rest, by calendar year (Section 6.4 of the report)
LOTS = pd.read_csv(ROOT / "data" / "processed" / "lots.csv")
PX = pd.read_csv(ROOT / "data" / "processed" / "prices.csv.gz", usecols=["ticker", "date", "adj_close"])
PX = PX[PX.ticker.isin(set(LOTS.val_symbol))].pivot(index="date", columns="ticker", values="adj_close").sort_index().ffill()
DAYS = np.array([d for d in PX.index if "2021-08-31" <= d <= "2026-08-31"])
PX = PX.loc[DAYS]
full, _ = sleeve_returns(LOTS, PX, DAYS)
book = pd.read_csv(ROOT / "data" / "processed" / "daily_book.csv").set_index("date")["series_a_return"]
assert np.nanmax(np.abs(full.to_numpy() - book.reindex(full.index).to_numpy())) < 1e-8   # same as the engine
sleeves = {}
for name, mask in {"mullin": LOTS.senator == "Markwayne Mullin", "rest": LOTS.senator != "Markwayne Mullin"}.items():
    r, c = sleeve_returns(LOTS[mask], PX, DAYS)
    yr = pd.to_datetime(r.index).year
    sleeves[name] = {"return_by_year": {int(y): float(v) for y, v in ((1 + r).groupby(yr).prod() - 1).items()},
                     "avg_capital_by_year": {int(y): float(v) for y, v in c.groupby(yr).mean().items()}}
pnl = LOTS.groupby("senator").pnl.sum()
moody = LOTS[LOTS.senator == "Ashley Moody"].sort_values("pnl", ascending=False)
res["concentration"] = {
    "sleeves": sleeves, "lot_pnl_total": float(LOTS.pnl.sum()),
    "pnl_share_mullin_plus_moody": float((pnl["Markwayne Mullin"] + pnl["Ashley Moody"]) / LOTS.pnl.sum()),
    "moody_top4": [{"ticker": t, "pnl": float(p)} for t, p in zip(moody.price_ticker.head(4), moody.pnl.head(4))],
    "moody_top4_share_of_all_pnl": float(moody.pnl.head(4).sum() / LOTS.pnl.sum()),
}

# V21 (exploratory): sell when the senator leaves office, against SPY at its own volatility
V21_BOOK = ROOT / "data" / "interim" / "variants" / "full_bloomberg" / "V21" / "daily_book.csv"
if V21_BOOK.exists():
    v = pd.read_csv(V21_BOOK, parse_dates=["date"])
    v = v[(v.date >= "2021-09-01") & (v.date <= "2026-08-31")]
    mv = (v.set_index("date").series_a_return.add(1).resample("ME").prod() - 1).to_numpy()
    ann = lambda r: float(np.prod(1 + r) ** (12 / len(r)) - 1)
    k = (mv - M.rf).std(ddof=1) / (M.r_SPY - M.rf).std(ddof=1)
    rm = (M.rf + k * (M.r_SPY - M.rf)).to_numpy()
    res["v21_departure_exit"] = {"return": ann(mv), "k": float(k), "risk_matched_spy": ann(rm),
                                 "gap_geometric": ann(mv) - ann(rm), "gap_arithmetic": float((mv - rm).mean() * 12)}
(OUT / "diagnostics.json").write_text(json.dumps(res, indent=1))

# Appendix E rows, rounded (not truncated) straight from the variants table, so the report cannot drift from it
V = pd.read_csv(ROOT / "outputs" / "tables" / "variants_full_bloomberg.csv")
f2 = lambda x: "" if pd.isna(x) else f"{x:.2f}"
pc = lambda x, d=2: "" if pd.isna(x) else f"{x * 100:.{d}f}%"
al = lambda a, t: "" if pd.isna(a) else f"{a * 100:+.2f} ({t:.2f})".replace("-", "−")
rows = []
for _, r in V.iterrows():
    rows.append({"id": r.id, "status": r.status, "ret": pc(r.A_ann_return), "sharpe": f2(r.A_sharpe),
                 "capm": al(r.A_capm_alpha, r.A_capm_t), "c4": al(r.A_c4_alpha, r.A_c4_t),
                 "mdd": pc(r.A_max_dd, 1).replace("-", "−"), "oos_ret": pc(r.oos_A_ann_return),
                 "oos_capm": al(r.oos_A_capm_alpha, r.oos_A_capm_t)})
(OUT / "variants_rows.json").write_text(json.dumps(rows, indent=1))
md = ["# Report diagnostics (not registered tests)", "", "_Built by report/diagnostics.py from data/processed/monthly_returns.csv._", ""]
md += [f"- {k}: {v}" for k, v in res.items()]
(OUT / "diagnostics.md").write_text("\n".join(md) + "\n")
print(json.dumps(res, indent=1))
