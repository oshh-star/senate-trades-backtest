"""Part B Step 1: the confirmatory statistics (src/metrics/confirmatory.py)."""
import numpy as np
import pandas as pd
import pytest

from src.metrics import confirmatory as cf
from src.metrics import mechanism as mc
from src.metrics import stats as st


def test_holm_on_a_hand_made_set_with_a_known_answer():
    # sorted: 0.005 x 4 = 0.02; 0.01 x 3 = 0.03; 0.03 x 2 = 0.06; 0.04 x 1 = 0.04 -> running max 0.06
    adj = cf.holm([0.01, 0.04, 0.03, 0.005])
    assert np.allclose(adj, [0.03, 0.06, 0.06, 0.02])


def test_holm_caps_at_one_and_counts_a_missing_test_as_p_one():
    adj = cf.holm([0.3, np.nan, 0.001])          # nan -> 1; sorted 0.001 x 3, 0.3 x 2, 1 x 1
    assert np.allclose(adj, [0.6, 1.0, 0.003])
    assert np.allclose(cf.holm([0.5, 0.6]), [1.0, 1.0])


def test_holm_matches_statsmodels():
    from statsmodels.stats.multitest import multipletests
    p = np.array([0.0285, 0.0243, 0.553, 0.784, 0.289, 0.586, 0.128])
    assert np.allclose(cf.holm(p), multipletests(p, method="holm")[1])


def test_thresholds_and_p_values():
    assert cf.Z_NOMINAL == pytest.approx({2: 1.959964, 1: 1.644854}, abs=1e-6)
    assert round(cf.Z_BONFERRONI[2], 3) == 2.690 and round(cf.Z_BONFERRONI[1], 3) == 2.450
    assert cf.p_value(1.959964, 2) == pytest.approx(0.05, abs=1e-6)
    assert cf.p_value(-1.959964, 2) == pytest.approx(0.05, abs=1e-6)
    assert cf.p_value(1.644854, 1) == pytest.approx(0.05, abs=1e-6)
    assert cf.p_value(-1.0, 1) > 0.5                              # one-sided: the registered direction is positive
    assert np.isnan(cf.p_value(np.nan, 2))


def test_alpha_and_cluster_statistics_match_the_existing_ones():
    rng = np.random.default_rng(0)
    F = pd.DataFrame(rng.normal(0, 0.04, (30, 4)), columns=["mkt_rf", "smb", "hml", "mom"])
    y = 0.002 + 1.2 * F["mkt_rf"] + rng.normal(0, 0.03, 30)
    a = cf.alpha_nw(y, F[["mkt_rf"]])
    r = st.regress(y, F, ["mkt_rf"])
    assert a["estimate"] == pytest.approx(r["alpha_ann"]) and a["t"] == pytest.approx(r["t_alpha_nw"])
    assert a["se"] == pytest.approx(a["estimate"] / a["t"])

    x = pd.Series(rng.normal(0.01, 0.05, 200))
    g = pd.Series(rng.integers(0, 12, 200)).astype(str)
    c = cf.cluster_mean(x, g)
    assert c["t"] == pytest.approx(st.clustered_mean(x, g)["t_cluster"]) and c["se"] == pytest.approx(c["estimate"] / c["t"])
    grp = pd.Series(np.where(rng.random(200) < 0.4, "a", "b"))
    d = cf.cluster_diff(x, grp, g, "a")
    est, t, n = mc.diff_t(x, grp, g, "a")
    assert d["estimate"] == pytest.approx(est) and d["t"] == pytest.approx(t) and d["n"] == n


def test_too_few_clusters_leaves_t_blank():
    x = pd.Series([0.01, 0.02, 0.03, 0.04])
    c = cf.cluster_mean(x, pd.Series(["2022-01", "2022-01", "2022-02", "2022-03"]))
    assert np.isnan(c["t"]) and np.isnan(c["se"]) and c["estimate"] == pytest.approx(0.025)


def test_restrict_keeps_the_half_and_censors_horizons_past_its_end():
    cal = [f"2024-01-{d:02d}" for d in range(1, 31)]
    panel = pd.DataFrame({"entry_date": ["2024-01-02", "2024-01-20", "2024-01-29"],
                          "txn_price_date": ["2024-01-01", "2024-01-10", "2024-01-25"],
                          "x_entry_5": [0.1, 0.2, 0.3], "r_entry_5": [0.1, 0.2, 0.3],
                          "x_txn_5": [0.1, 0.2, 0.3], "r_txn_5": [0.1, 0.2, 0.3]})
    p = cf.restrict(panel, cal, "2024-01-02", "2024-01-22")
    assert list(p["entry_date"]) == ["2024-01-02", "2024-01-20"]          # the 29th is outside the half
    assert p["x_entry_5"].tolist()[0] == 0.1 and np.isnan(p["x_entry_5"].tolist()[1])   # 20th + 5 > 22nd
    assert p["x_txn_5"].tolist() == [0.1, 0.2]                            # 10th + 5 = 15th, inside
    assert list(p["entry_month"]) == ["2024-01", "2024-01"]


def test_calendar_years_compound_within_each_year_and_name_partial_coverage():
    idx = ["2021-11", "2021-12", "2022-01", "2022-02"]
    mon = pd.DataFrame({"r_A": [0.1, -0.1, 0.05, 0.05], "r_SPY": [0.0, 0.0, 0.0, 0.0], "mkt_rf": [0.01] * 4,
                        "rf": [0.0] * 4, "r_NANC": [np.nan, 0.02, np.nan, np.nan]}, index=idx)
    cy = cf.calendar_years(mon).set_index("year")
    assert cy.loc["2021", "Series A (headline)"] == pytest.approx(1.1 * 0.9 - 1)
    assert cy.loc["2022", "Series A (headline)"] == pytest.approx(1.05 ** 2 - 1)
    assert cy.loc["2021", "months"] == "Nov-Dec (2 months)"
    assert cy.loc["2021", "NANC"] == pytest.approx(0.02) and "NANC: Dec-Dec" in cy.loc["2021", "coverage"]
    assert np.isnan(cy.loc["2022", "NANC"])
    assert cy.loc["2022", "Market (Ken French Mkt-RF + RF)"] == pytest.approx(1.01 ** 2 - 1)


def test_worst_12_months_finds_the_known_window():
    idx = pd.period_range("2021-01", periods=24, freq="M").astype(str)
    a = np.full(24, 0.01)
    a[5:17] = -0.02                                    # 2021-06 .. 2022-05 is the worst 12-month run
    mon = pd.DataFrame({"r_A": a, "r_SPY": np.full(24, 0.005)}, index=idx)
    w = cf.worst_12m(mon).set_index("series")
    assert w.loc["Series A (headline)", "start"] == "2021-06" and w.loc["Series A (headline)", "end"] == "2022-05"
    assert w.loc["Series A (headline)", "return"] == pytest.approx(0.98 ** 12 - 1)
    assert w.loc["Series A (headline)", "SPY, same months"] == pytest.approx(1.005 ** 12 - 1)
    assert w.loc["SPY", "windows"] == 13


def test_verdicts():
    assert cf.verdict("H2", 0.01, 2.5, 0.03) == "positive (significant)"
    assert cf.verdict("H2", 0.01, 1.9, 0.17) == "not shown to be positive"
    assert cf.verdict("H3", 0.04, 2.25, 0.17) == "not distinguishable from zero"
    assert cf.verdict("H4", -0.05, -3.0, 0.01) == "significantly negative"
    assert cf.verdict("H1p", 0.01, np.nan, 1.0).startswith("not testable")


def test_the_in_sample_half_reproduces_the_registered_values():
    """The test plan's in-sample values (Yahoo prices), from the committed engine and metrics outputs."""
    panel = pd.read_csv("data/processed/event_panel.csv", dtype={"entry_date": str, "txn_price_date": str},
                        low_memory=False)
    mon = pd.read_csv("data/processed/monthly_returns.csv", dtype={"month": str}).set_index("month")
    cal = pd.read_csv("data/processed/trading_calendar.csv", dtype=str)["date"].tolist()
    R = cf.half_report(panel, mon, cal, "2021-09-01", "2024-02-29")
    c = R["confirmatory"].set_index("id")
    assert round(c.loc["H2", "estimate"], 4) == 0.0116 and round(c.loc["H2", "t"], 2) == 1.91
    assert round(c.loc["H3", "estimate"], 4) == 0.0395 and round(c.loc["H3", "t"], 2) == 2.25
    assert round(c.loc["H4", "estimate"], 4) == 0.0398 and round(c.loc["H4", "t"], 2) == 1.52
    assert round(c.loc["H0a", "estimate"], 4) == -0.0395 and round(c.loc["H0a", "t"], 2) == -0.59
    assert round(c.loc["H1p", "t"], 2) == 1.06 and round(c.loc["H1s", "t"], 2) == 0.54
    assert np.allclose(c["mde_bonferroni"], c["se"] * c["z_bonferroni"])
    assert np.allclose(c["p_holm"], cf.holm(c["p"]))
    # censoring the in-sample panel at its own end changes nothing
    p = cf.restrict(panel, cal, "2021-09-01", "2024-02-29")
    xcols = [k for k in panel.columns if k.startswith("x_")]
    assert len(p) == len(panel) and (p[xcols].isna().to_numpy() == panel[xcols].isna().to_numpy()).all()
