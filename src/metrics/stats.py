"""Performance statistics (Phase 5). Pure functions on numpy / pandas inputs; every return is a decimal
(0.01 = 1%), never percent.

Frequencies (D17): Sharpe ratios, volatilities and regressions use MONTHLY returns compounded from daily
returns; drawdowns use the DAILY value index.
  annualised geometric return  prod(1 + r_m)^(12/N) - 1
  annualised volatility        sd(r_m, ddof=1) x sqrt(12)
  Sharpe ratio                 mean(r_m - rf_m) / sd(r_m - rf_m) x sqrt(12)
  regressions                  r_m - rf_m = a + b'f_m + e_m by OLS; t-statistics from OLS and from Newey-West
                               (Bartlett kernel, 3 lags); alpha annualised as a x 12
  minimum detectable alpha     2 x SE_OLS(a) x 12: the annualised alpha that would have t = 2 given the residual
                               volatility, N and the factor data (SE(a) = s_e x sqrt([(X'X)^-1]_00))
  turnover                     one-sided: 0.5 x sum_i |w_i(after trades) - w_i(before trades, after drift)|
                               each day, summed within the month; annualised = mean monthly x 12
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm

NW_LAGS = 3


def monthly(daily_ret: pd.Series, dates: pd.Series) -> pd.Series:
    """Compound daily returns into calendar months ('YYYY-MM' index)."""
    s = pd.Series(np.asarray(daily_ret, dtype=float), index=pd.Index(np.asarray(dates, dtype=str)).str[:7])
    return (1 + s).groupby(level=0).prod() - 1


def ann_return(r_m: pd.Series) -> float:
    r = np.asarray(r_m, dtype=float)
    return float(np.prod(1 + r) ** (12 / len(r)) - 1)


def ann_vol(r_m: pd.Series) -> float:
    return float(np.std(np.asarray(r_m, dtype=float), ddof=1) * np.sqrt(12))


def sharpe(r_m: pd.Series, rf_m: pd.Series) -> float:
    x = np.asarray(r_m, dtype=float) - np.asarray(rf_m, dtype=float)
    return float(x.mean() / x.std(ddof=1) * np.sqrt(12))


def risk_match_k(strategy_ex: pd.Series, spy_ex: pd.Series) -> float:
    """k = volatility of the strategy's monthly excess return / volatility of SPY's."""
    return float(np.std(np.asarray(strategy_ex, float), ddof=1) / np.std(np.asarray(spy_ex, float), ddof=1))


def risk_matched(spy: pd.Series, rf: pd.Series, k: float) -> pd.Series:
    """RF + k x (SPY - RF): SPY levered (k > 1, borrowing at RF) or de-levered to the strategy's volatility."""
    return rf + k * (spy - rf)


def regress(y_ex: pd.Series, factors: pd.DataFrame, names: list[str]) -> dict:
    """OLS of monthly excess returns on the factors, with OLS and Newey-West t-statistics."""
    X = sm.add_constant(factors[names].to_numpy(dtype=float), has_constant="add")
    y = np.asarray(y_ex, dtype=float)
    ols = sm.OLS(y, X).fit()
    nw = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": NW_LAGS})
    out = {"alpha_ann": float(ols.params[0] * 12), "t_alpha_ols": float(ols.tvalues[0]), "t_alpha_nw": float(nw.tvalues[0]),
           "r2": float(ols.rsquared), "n": int(len(y)), "resid_vol_ann": float(np.sqrt(ols.mse_resid) * np.sqrt(12)),
           "mda_ann": float(2 * ols.bse[0] * 12)}
    for i, n in enumerate(names, start=1):
        out[f"b_{n}"] = float(ols.params[i])
        out[f"t_{n}_ols"] = float(ols.tvalues[i])
        out[f"t_{n}_nw"] = float(nw.tvalues[i])
    return out


def max_drawdown(daily_ret: pd.Series, dates: list[str], base_date: str) -> dict:
    """Deepest peak-to-trough fall of the daily value index (1 at the close of base_date, the day before the
    first return). Recovery = first close back at or above the peak."""
    v = np.concatenate([[1.0], np.cumprod(1 + np.asarray(daily_ret, dtype=float))])
    d = [base_date] + list(dates)
    peak = np.maximum.accumulate(v)
    dd = v / peak - 1
    t = int(np.argmin(dd))
    p = int(np.argmax(v[:t + 1]))
    rec = next((i for i in range(t + 1, len(v)) if v[i] >= v[p]), None)
    return {"depth": float(dd[t]), "peak_date": d[p], "trough_date": d[t],
            "recovery_date": d[rec] if rec is not None else "not recovered",
            "peak_to_trough_days": t - p, "trough_to_recovery_days": (rec - t) if rec is not None else None,
            "value_index": v, "drawdown": dd, "dates": d}


def correlations(r_m: pd.Series, spy_m: pd.Series, worst_share: float = 0.2) -> dict:
    """Pearson correlation of monthly returns with SPY: all months, and SPY's worst `worst_share` of months."""
    a, s = np.asarray(r_m, float), np.asarray(spy_m, float)
    n_bad = max(int(round(worst_share * len(s))), 3)
    bad = np.argsort(s, kind="stable")[:n_bad]
    return {"corr_all": float(np.corrcoef(a, s)[0, 1]), "corr_worst": float(np.corrcoef(a[bad], s[bad])[0, 1]),
            "n_worst": n_bad}


def turnover(pre: np.ndarray, post: np.ndarray) -> np.ndarray:
    """One-sided turnover each day. pre[t, i] = value of holding i at t's close BEFORE t's trades (after drift);
    post[t, i] = value after t's trades. Include cash as a column when the portfolio holds cash. A day on which
    nothing is held before (or after) the trades counts that side as 100% cash."""
    pre, post = np.asarray(pre, float), np.asarray(post, float)
    tp, tq = pre.sum(axis=1), post.sum(axis=1)
    wp = np.divide(pre, tp[:, None], out=np.zeros_like(pre), where=tp[:, None] > 0)
    wq = np.divide(post, tq[:, None], out=np.zeros_like(post), where=tq[:, None] > 0)
    cash_p, cash_q = (tp <= 0).astype(float), (tq <= 0).astype(float)
    return 0.5 * (np.abs(wq - wp).sum(axis=1) + np.abs(cash_q - cash_p))


def break_even_bps(excess_ann: float, turnover_ann: float) -> float | None:
    """One-way cost (basis points) that would erase the excess return: excess / (2 x annual one-sided turnover).
    None when the excess return is not positive (there is nothing to erase)."""
    if not np.isfinite(excess_ann) or excess_ann <= 0 or turnover_ann <= 0:
        return None
    return float(excess_ann / (2 * turnover_ann) * 1e4)


def clustered_mean(x: pd.Series, clusters: pd.Series) -> dict:
    """Mean, median, N and the t-statistic of the mean with standard errors clustered by `clusters`."""
    ok = x.notna()
    x, g = x[ok].astype(float), clusters[ok]
    n = int(len(x))
    if n < 2:
        return {"mean": np.nan, "median": np.nan, "n": n, "clusters": int(g.nunique()), "t_cluster": np.nan, "t_iid": np.nan}
    X = np.ones((n, 1))
    codes = pd.factorize(g)[0]
    fit = sm.OLS(x.to_numpy(), X).fit(cov_type="cluster", cov_kwds={"groups": codes})
    iid = sm.OLS(x.to_numpy(), X).fit()
    return {"mean": float(x.mean()), "median": float(x.median()), "n": n, "clusters": int(g.nunique()),
            "t_cluster": float(fit.tvalues[0]), "t_iid": float(iid.tvalues[0])}
