"""Phase 5: warm-up (L2), ledger exposure (L3), metrics, benchmarks and the event study, on hand-built cases."""
import copy

import numpy as np
import pandas as pd
import pytest

from src.config import load_config
from src.engine import events as evm
from src.engine import portfolio as pf
from src.engine import warmup as wu
from src.engine import warmup_start
from tests.test_phase4 import DAYS, ev, prices, run


# ---------------------------------------------------------------- L2 warm-up
def test_warmup_start_dates_and_the_scrape_start_limit():
    cfg = copy.deepcopy(load_config())
    assert warmup_start(cfg, "2021-09-01") == ("2020-09-01", pytest.approx(12.0, abs=0.1), False)
    w, months, limited = warmup_start(cfg, "2016-09-01")                   # 10-year window
    assert w == "2016-01-01" and limited and months == pytest.approx(8.0, abs=0.1)
    cfg["engine"]["warmup_months"] = 0                                       # V17
    assert warmup_start(cfg, "2021-09-01") == ("2021-09-01", 0.0, False)


def test_add_warmup_only_admits_records_in_scope_but_for_the_window():
    u = pd.DataFrame({"in_scope": [False, False, False, True],
                      "in_scope_ex_window": [True, False, True, True],
                      "disclosure_date": ["2020-10-01", "2020-10-01", "2020-08-31", "2021-09-02"]})
    out = evm.add_warmup(u, "2020-09-01", "2021-09-01")
    assert out["in_scope"].tolist() == [True, False, False, True]
    assert out["warmup"].tolist() == [True, False, False, False]


def test_warmup_book_is_marked_at_the_close_before_the_window_and_sales_match_it():
    # a lot bought on day 0 (warm-up); the window starts on day 2; the senator sells in full on day 3
    px = prices({"AAA": [10, 12, 15, 18, 18, 18], "BBB": [10, 10, 10, 10, 11, 11]})
    pc, log = run([ev(0, "Purchase", 100), ev(3, "Sale (Full)", 1), ev(3, "Purchase", 50, sym="BBB")], px)
    assert log["action"].tolist()[1] == "sold all"                          # the warm-up lot is there to sell
    daily, rec = pf.series(pc, px.ffill, DAYS, np.zeros(6), start=DAYS[2])
    assert daily["date"].iloc[0] == DAYS[2] and len(daily) == 4
    a = daily["series_a_return"].to_numpy()
    assert a[0] == pytest.approx(15 / 12 - 1) and a[1] == pytest.approx(18 / 15 - 1)   # measured from day 1's close
    assert a[2] == pytest.approx(0.1)                                       # BBB bought on day 3 earns day 4
    # series B: K = the warm-up book at day 1's close ($120) + peak net cash invested in the window
    # (day 3: buy 50, receive 180 -> net -130; so the cash part is 0)
    assert rec["K_warmup_book"] == pytest.approx(120) and rec["K_cash"] == pytest.approx(0) and rec["K"] == pytest.approx(120)
    nav = daily["pot_nav"].to_numpy()
    assert nav.tolist() == pytest.approx([150, 180, 185, 185])
    # reconciliation counts only P&L inside the window: AAA 120 -> 180, BBB 50 -> 55
    assert rec["lot_pnl"] == pytest.approx(65) and rec["diff_book_minus_lots"] == pytest.approx(0, abs=1e-9)
    assert rec["diff_pot_minus_lots"] == pytest.approx(0, abs=1e-9)
    assert rec["lot_pnl_all_incl_warmup"] == pytest.approx(85)


def test_v17_empty_start_equals_the_old_series():
    px = prices({"AAA": [10, 11, 12, 12, 12, 12]})
    pc, _ = run([ev(0, "Purchase", 100), ev(2, "Sale (Full)", 1)], px)
    d0, r0 = pf.series(pc, px.ffill, DAYS, np.zeros(6))
    d1, r1 = pf.series(pc, px.ffill, DAYS, np.zeros(6), start=DAYS[0])
    pd.testing.assert_frame_equal(d0, d1)
    assert r0["K"] == r1["K"] == pytest.approx(100) and r1["K_warmup_book"] == 0


# ---------------------------------------------------------------- L3 ledger exposure
def test_ledger_exposure_applies_the_senators_sales_at_cost():
    px = prices({"AAA": [10] * 6})
    evs = [ev(0, "Purchase", 100, sym="GONE"), ev(0, "Purchase", 100), ev(1, "Purchase", 50, sym="GONE"),
           ev(2, "Sale (Partial)", 120, sym="GONE"), ev(4, "Sale (Full)", 1, sym="GONE")]
    pc, log = run(evs, px)
    daily, _ = pf.series(pc, px.ffill, DAYS, np.zeros(6))
    lx = wu.ledger_exposure(pd.DataFrame(evs), log, DAYS, daily, delisted={})
    assert lx["ledger_cost_held"].tolist() == pytest.approx([100, 150, 30, 30, 0, 0])
    assert lx["share_of_capital_deployed"].iloc[1] == pytest.approx(1.5)
    lx2 = wu.ledger_exposure(pd.DataFrame(evs), log, DAYS, daily, delisted={"GONE": DAYS[1]})
    assert lx2["ledger_cost_held_to_delisting"].tolist() == pytest.approx([100, 150, 0, 0, 0, 0])


# ---------------------------------------------------------------- metrics
from src.metrics import benchmarks as bm  # noqa: E402
from src.metrics import event_study as es  # noqa: E402
from src.metrics import stats as st  # noqa: E402


def test_monthly_compounding_and_annualisation():
    dates = ["2024-01-02", "2024-01-03", "2024-02-01", "2024-02-02"]
    m = st.monthly(pd.Series([0.1, 0.1, -0.5, 0.2]), pd.Series(dates))
    assert m.index.tolist() == ["2024-01", "2024-02"] and m.tolist() == pytest.approx([0.21, -0.4])
    r = pd.Series([0.01] * 12)
    assert st.ann_return(r) == pytest.approx(1.01 ** 12 - 1)
    assert st.ann_vol(pd.Series([0.01, 0.03] * 6)) == pytest.approx(np.std([0.01, 0.03] * 6, ddof=1) * np.sqrt(12))
    rf = pd.Series([0.001] * 4)
    x = pd.Series([0.02, 0.0, 0.03, -0.01])
    assert st.sharpe(x, rf) == pytest.approx((x - rf).mean() / (x - rf).std() * np.sqrt(12))


def test_risk_matched_spy_has_the_strategy_volatility_on_excess_returns():
    rng = np.random.default_rng(0)
    rf = pd.Series(rng.uniform(0.0, 0.004, 30))
    spy = pd.Series(rng.normal(0.008, 0.045, 30))
    strat = pd.Series(rng.normal(0.004, 0.07, 30))
    k = st.risk_match_k(strat - rf, spy - rf)
    assert k == pytest.approx((strat - rf).std() / (spy - rf).std())
    rm = st.risk_matched(spy, rf, k)
    assert (rm - rf).std() == pytest.approx((strat - rf).std(), rel=1e-12)     # identical excess volatility
    assert ((rm - rf) / (spy - rf)).to_numpy() == pytest.approx(np.full(30, k))  # SPY's excess return, scaled
    assert st.sharpe(rm, rf) == pytest.approx(st.sharpe(spy, rf))               # scaling leaves the Sharpe ratio


def test_turnover_on_a_hand_built_two_asset_case():
    # Day 0: $50 in A and $50 in B. Day 1: A rises 10%, B flat (pre-trade 55 / 50, weights 0.5238 / 0.4762);
    # the portfolio rebalances to 50/50 of $105: sells 2.5 of A, buys 2.5 of B -> one-sided turnover 2.5/105.
    # Day 2: no trade. Day 3: sells all of B into A (weights 0.5/0.5 -> 1/0): turnover 0.5.
    pre = np.array([[0, 0], [55, 50], [52.5, 52.5], [52.5, 52.5]], float)
    post = np.array([[50, 50], [52.5, 52.5], [52.5, 52.5], [105, 0]], float)
    t = st.turnover(pre, post)
    assert t[0] == pytest.approx(1.0)                     # from all cash into the book
    assert t[1] == pytest.approx(2.5 / 105) and t[2] == pytest.approx(0) and t[3] == pytest.approx(0.5)
    # the same trades with a cash column: buying $10 of A out of $100 cash moves 10% of the pot
    t2 = st.turnover(np.array([[0, 0, 100.0]]), np.array([[10, 0, 90.0]]))
    assert t2[0] == pytest.approx(0.10)
    assert st.break_even_bps(0.02, 1.0) == pytest.approx(100) and st.break_even_bps(-0.01, 1.0) is None


def test_regressions_recover_a_known_alpha_and_beta():
    rng = np.random.default_rng(1)
    F = pd.DataFrame(rng.normal(0, 0.04, (120, 4)), columns=["mkt_rf", "smb", "hml", "mom"])
    y = 0.002 + 1.2 * F["mkt_rf"] + 0.5 * F["smb"] - 0.3 * F["mom"] + rng.normal(0, 0.0001, 120)
    r = st.regress(y, F, ["mkt_rf", "smb", "hml", "mom"])
    assert r["alpha_ann"] == pytest.approx(0.024, abs=1e-3) and r["b_mkt_rf"] == pytest.approx(1.2, abs=1e-2)
    assert r["b_smb"] == pytest.approx(0.5, abs=1e-2) and r["b_mom"] == pytest.approx(-0.3, abs=1e-2) and r["n"] == 120
    # minimum detectable alpha = 2 x SE(alpha) x 12, so t(alpha) = alpha / (MDA / 2)
    assert r["t_alpha_ols"] == pytest.approx(r["alpha_ann"] / (r["mda_ann"] / 2))


def test_max_drawdown_dates_and_recovery():
    r = [0.1, -0.5, 0.2, 1.0, -0.1]           # index 1, 1.1, 0.55, 0.66, 1.32, 1.188
    d = st.max_drawdown(pd.Series(r), ["d1", "d2", "d3", "d4", "d5"], "d0")
    assert d["depth"] == pytest.approx(-0.5) and d["peak_date"] == "d1" and d["trough_date"] == "d2"
    assert d["recovery_date"] == "d4" and d["trough_to_recovery_days"] == 2
    d = st.max_drawdown(pd.Series([-0.2, 0.1]), ["d1", "d2"], "d0")
    assert d["peak_date"] == "d0" and d["recovery_date"] == "not recovered"


def test_correlation_in_spys_worst_months():
    spy = pd.Series(np.arange(10) / 100 - 0.05)                  # worst months are the first ones
    a = pd.Series(np.where(np.arange(10) < 3, -spy, spy))       # moves against SPY in its 3 worst months
    c = st.correlations(a, spy, worst_share=0.2)
    assert c["n_worst"] == 3 and c["corr_worst"] == pytest.approx(-1)


def test_universe_members_use_only_filings_public_before_the_formation_close():
    recs = pd.DataFrame({"price_ticker": ["OLD", "IN", "EDGE", "LATE"],
                         "entry_date": ["2022-12-29", "2023-06-01", "2023-12-29", "2024-01-02"]})     # 12 months back is out
    assert bm.universe_members(recs, "2023-12-29") == {"IN", "EDGE"}


def test_universe_equal_weight_return_with_drift():
    cal = ["2023-12-29", "2024-01-02", "2024-01-03"]
    P = pd.DataFrame({"AAA": [10, 11, 11], "BBB": [10, 10, 12]}, index=cal, dtype=float)
    recs = pd.DataFrame({"price_ticker": ["AAA", "BBB", "GONE"], "entry_date": ["2023-06-01"] * 3})
    last = {"AAA": "2024-12-31", "BBB": "2024-12-31"}
    r, info = bm.universe_ew(recs, P, cal, cal[1:], last, {"AAA": "2020-01-01", "BBB": "2020-01-01"})
    assert r.tolist() == pytest.approx([0.05, (1.1 + 1.2) / 2 / 1.05 - 1])
    assert info["members_priced"].iat[0] == 2 and info["left_out_symbols"].iat[0] == "GONE"


def test_sterling_conversion():
    # the dollar rises from 1.25 to 1.20 per pound: a flat USD asset gains 1.25/1.20 - 1 in sterling
    r = bm.to_gbp(pd.Series([0.0, 0.1]), pd.Series([1.25, 1.20, 1.20]))
    assert r.tolist() == pytest.approx([1.25 / 1.20 - 1, 0.1])


def test_event_study_gap_and_clustered_t():
    panel = pd.DataFrame({"side": ["purchase"] * 4, "entry_date": ["2022-01-03", "2022-01-04", "2022-02-01", "2022-03-01"],
                          "gap_x": [0.01, 0.02, 0.0, -0.01],
                          "x_txn_5": [0.03, 0.01, 0.02, np.nan], "x_entry_5": [0.01, 0.0, 0.01, 0.02]})
    t = es.table(panel, [5])
    t = t[t["side"] == "purchase"].set_index("version")
    assert t.loc["senator (from transaction date)", "n"] == 3 and t.loc["copier (from entry date)", "n"] == 4
    gap = t.loc["gap (senator minus copier)"]
    assert gap["mean"] == pytest.approx(np.mean([0.02, 0.01, 0.01])) and gap["clusters"] == 2
    c = st.clustered_mean(pd.Series([1.0, 1.0, 3.0, 3.0]), pd.Series(["a", "a", "b", "b"]))
    assert c["mean"] == 2 and c["clusters"] == 2 and np.isfinite(c["t_cluster"])


def test_metrics_stage_refuses_a_mismatched_engine_sample(tmp_path, monkeypatch):
    import json
    import src.metrics as mt
    cfg = copy.deepcopy(load_config())
    cfg["oos"]["oos_unlocked"], cfg["engine"]["sample"] = False, "in_sample"  # config asks in-sample, engine ran full
    (tmp_path / "engine_metadata.json").write_text(json.dumps({"first_day": "2021-09-01", "last_day": "2026-08-31",
                                                               "sample": "full window"}))
    monkeypatch.setattr(mt, "PROCESSED", tmp_path)
    with pytest.raises(RuntimeError, match="rerun the engine"):
        mt.load_inputs(cfg)
