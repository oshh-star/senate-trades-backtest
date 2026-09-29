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
