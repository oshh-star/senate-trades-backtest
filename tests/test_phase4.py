"""Phase 4 (engine): hand-built synthetic cases with known answers."""
import copy

import numpy as np
import pandas as pd
import pytest

from src.clean.build import load_renames, price_symbol
from src.config import OutOfSampleLocked, load_config
from src.engine import book as bk
from src.engine import events as evm
from src.engine import panel as pn
from src.engine import portfolio as pf
from src.engine import sample_bounds

DAYS = ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08", "2024-01-09"]


def prices(series: dict, days=DAYS, last_dates=None):
    rows = [{"date": d, "ticker": s, "adj_close": p} for s, ps in series.items() for d, p in zip(days, ps) if p is not None]
    ld = last_dates or {s: max(d for d, p in zip(days, ps) if p is not None) for s, ps in series.items()}
    return bk.Prices(pd.DataFrame(rows), days, ld)


_N = [0]


def ev(day, kind, size, sym="AAA", sen="S1", rec=None, act=True, reverse_prev=False, prev="", record_no=1, trade=None):
    _N[0] += 1
    rec = rec or f"R{_N[0]}"
    return {"event_no": _N[0], "record_id": rec, "trade_id": trade or rec.split(".")[0], "record_no": record_no,
            "prev_record_id": prev, "act": act, "reverse_prev": reverse_prev, "bioguide_id": sen, "senator": sen,
            "ticker": sym, "price_ticker": sym, "transaction_type": kind, "entry_date": DAYS[day], "size": float(size)}


def run(events, px, days=DAYS, mode="skip"):
    return bk.simulate(pd.DataFrame(events), px, days, ledger_mode=mode)


# ---------------------------------------------------------------- the book
def test_buy_then_full_sale():
    px = prices({"AAA": [10, 11, 12, 13, 14, 15]})
    pc, log = run([ev(0, "Purchase", 100), ev(2, "Sale (Full)", 5000)], px)
    assert len(pc) == 1
    r = pc.iloc[0]
    assert r.units == pytest.approx(10) and r.exit_date == DAYS[2] and r.exit_reason == "senator sale"
    assert r.exit_value == pytest.approx(120) and r.pnl == pytest.approx(20) and r["return"] == pytest.approx(0.2)
    assert r.holding_trading_days == 2


def test_partial_sales_fifo_across_several_lots():
    px = prices({"AAA": [10, 11, 12, 12, 12, 12]})
    pc, _ = run([ev(0, "Purchase", 100), ev(1, "Purchase", 110), ev(2, "Sale (Partial)", 180),
                 ev(3, "Sale (Partial)", 1_000_000)], px)
    # day 2: $180 at 12 = 15 units: all 10 of the first lot, 5 of the second
    first = pc[pc["exit_date"] == DAYS[2]].sort_values("lot_id")
    assert first["units"].tolist() == pytest.approx([10, 5])
    assert first["entry_dollars"].tolist() == pytest.approx([100, 55])
    # day 3: a partial sale bigger than the holding is capped at the 5 units left
    last = pc[pc["exit_date"] == DAYS[3]]
    assert last["units"].tolist() == pytest.approx([5]) and pc["units"].sum() == pytest.approx(20)


def test_sale_with_nothing_held_is_ignored_and_logged():
    px = prices({"AAA": [10] * 6, "BBB": [5] * 6})
    pc, log = run([ev(0, "Purchase", 100, sym="BBB"), ev(1, "Sale (Full)", 100, sym="AAA"),
                   ev(1, "Sale (Full)", 100, sym="BBB", sen="S2")], px)
    assert (log["action"] == "ignored: nothing held").sum() == 2                  # other ticker; other senator
    assert pc["exit_reason"].tolist() == ["end of window"]


def test_j3_reversal_of_a_purchase_then_the_correction_acts():
    px = prices({"AAA": [10, 10, 20, 20, 20, 20]})
    e1 = ev(0, "Purchase", 100, rec="T1.1")
    e2 = ev(2, "Purchase", 200, rec="T1.2", prev="T1.1", reverse_prev=True, record_no=2)
    pc, log = run([e1, e2], px)
    rev = pc[pc["exit_reason"] == "reversal"]
    assert len(rev) == 1 and rev.iloc[0].exit_date == DAYS[2] and rev.iloc[0].pnl == pytest.approx(100)
    new = pc[pc["record_id"] == "T1.2"]
    assert new.iloc[0].entry_dollars == pytest.approx(200) and new.iloc[0].exit_reason == "end of window"


def test_j3_out_of_scope_correction_only_reverses():
    px = prices({"AAA": [10] * 6})
    pc, log = run([ev(0, "Purchase", 100, rec="T1.1"),
                   ev(1, "Purchase", 100, rec="T1.2", prev="T1.1", act=False, reverse_prev=True, record_no=2)], px)
    assert pc["exit_reason"].tolist() == ["reversal"] and len(pc) == 1


def test_j3_reversal_of_a_sale_buys_the_units_back():
    px = prices({"AAA": [10, 10, 10, 15, 15, 15]})
    pc, log = run([ev(0, "Purchase", 100), ev(1, "Sale (Full)", 100, rec="T9.1"),
                   ev(3, "Sale (Full)", 100, rec="T9.2", prev="T9.1", act=False, reverse_prev=True, record_no=2)], px)
    back = pc[pc["origin"].str.startswith("reversal buy-back")]
    assert len(back) == 1 and back.iloc[0].units == pytest.approx(10) and back.iloc[0].entry_price == 15


def test_rename_old_and_new_symbol_share_one_position():
    ren = load_renames()
    assert price_symbol("SQ", ren) == "XYZ" and price_symbol("FB", ren) == "META"
    px = prices({"XYZ": [50, 55, 60, 60, 60, 60]})
    buy = ev(0, "Purchase", 500, sym="XYZ")
    buy["ticker"] = "SQ"                                                  # disclosed under the old symbol
    pc, log = run([buy, ev(2, "Sale (Full)", 500, sym="XYZ")], px)
    assert pc.iloc[0].exit_reason == "senator sale" and pc.iloc[0].pnl == pytest.approx(100)


def test_series_ending_early_closes_at_the_last_price():
    px = prices({"AAA": [10, 12, None, None, None, None]}, last_dates={"AAA": DAYS[1]})
    pc, log = run([ev(0, "Purchase", 100), ev(3, "Sale (Full)", 100)], px)
    r = pc.iloc[0]
    assert r.exit_reason == "series ended" and r.exit_date == DAYS[1] and r.exit_price == 12
    assert log["action"].iloc[-1].startswith("ignored: nothing held (earlier copied lots already closed)")


def test_ledger_purchase_skipped_or_filled_with_spy():
    px = prices({"SPY": [100, 101, 102, 103, 104, 105]})
    pc, log = run([ev(0, "Purchase", 100, sym="GONE")], px)
    assert pc.empty and log["action"].iloc[0].startswith("skipped: survivorship ledger")
    pc, log = run([ev(0, "Purchase", 100, sym="GONE"), ev(2, "Sale (Full)", 1, sym="GONE")], px, mode="spy_fill")
    assert pc.iloc[0].val_symbol == "SPY" and pc.iloc[0]["return"] == pytest.approx(0.02)


# ---------------------------------------------------------------- events: dates and ordering
def units(rows):
    base = {"trade_id": "", "record_no": 1, "in_scope": True, "dropped_by_variant": False, "bioguide_id": "S1",
            "senator": "S1", "owner": "Self", "ticker": "AAA", "price_ticker": "AAA", "asset_name": "A",
            "transaction_date": "2024-01-01", "amount": "", "amount_mid": 100.0, "amount_lower": 1.0,
            "is_etf": False, "is_otc": False}
    out = [{**base, **r} for r in rows]
    df = pd.DataFrame(out)
    df["row_no"] = range(len(df))
    return df


def cfg_(**trades):
    c = copy.deepcopy(load_config())
    c["trades"].update(trades)
    return c


def test_entry_date_is_the_first_trading_day_after_disclosure_and_v9_same_day():
    u = units([{"record_id": "A.1", "trade_id": "A", "disclosure_date": "2024-01-03", "disclosure_datetime": "2024-01-03T10:00:00",
                "transaction_type": "Purchase"},
               {"record_id": "B.1", "trade_id": "B", "disclosure_date": "2024-01-06", "disclosure_datetime": "2024-01-06T10:00:00",
                "transaction_type": "Purchase"},                                          # Saturday
               {"record_id": "C.1", "trade_id": "C", "disclosure_date": "2024-01-03", "disclosure_datetime": "2024-01-03T16:10:00",
                "transaction_type": "Purchase"}])
    e = evm.build_events(u, DAYS, cfg_(), last_entry=DAYS[-1]).set_index("record_id")["entry_date"]
    assert e["A.1"] == "2024-01-04" and e["B.1"] == "2024-01-08" and e["C.1"] == "2024-01-04"
    e9 = evm.build_events(u, DAYS, cfg_(price_timing="same_day_close"), last_entry=DAYS[-1]).set_index("record_id")["entry_date"]
    assert e9["A.1"] == "2024-01-03" and e9["C.1"] == "2024-01-04" and e9["B.1"] == "2024-01-08"


def test_same_day_ordering_by_disclosure_datetime_then_transaction_date_then_row():
    u = units([{"record_id": "P.1", "trade_id": "P", "disclosure_date": "2024-01-03", "disclosure_datetime": "2024-01-03T15:00:00",
                "transaction_type": "Purchase"},
               {"record_id": "S.1", "trade_id": "S", "disclosure_date": "2024-01-03", "disclosure_datetime": "2024-01-03T09:00:00",
                "transaction_type": "Sale (Full)"},
               {"record_id": "Q.1", "trade_id": "Q", "disclosure_date": "2024-01-03", "disclosure_datetime": "2024-01-03T15:00:00",
                "transaction_date": "2023-12-01", "transaction_type": "Purchase"},
               {"record_id": "R.1", "trade_id": "R", "disclosure_date": "2024-01-03", "disclosure_datetime": "2024-01-03T15:00:00",
                "transaction_type": "Purchase"}])
    e = evm.build_events(u, DAYS, cfg_(), last_entry=DAYS[-1])
    assert e["record_id"].tolist() == ["S.1", "Q.1", "P.1", "R.1"]
    pc, log = bk.simulate(e, prices({"AAA": [10] * 6}), DAYS)
    assert log.iloc[0]["action"] == "ignored: nothing held"                       # the sale came first that day


def test_out_of_scope_correction_becomes_a_reversal_event_and_late_events_are_dropped():
    u = units([{"record_id": "T.1", "trade_id": "T", "record_no": 1, "disclosure_date": "2024-01-02",
                "disclosure_datetime": "2024-01-02T10:00:00", "transaction_type": "Purchase"},
               {"record_id": "T.2", "trade_id": "T", "record_no": 2, "in_scope": False, "disclosure_date": "2024-01-04",
                "disclosure_datetime": "2024-01-04T10:00:00", "transaction_type": "Purchase", "owner": "Spouse"},
               {"record_id": "L.1", "trade_id": "L", "disclosure_date": "2024-01-08", "disclosure_datetime": "2024-01-08T10:00:00",
                "transaction_type": "Purchase"}])
    e = evm.build_events(u, DAYS, cfg_(), last_entry="2024-01-08").set_index("record_id")
    assert e.loc["T.2", "reverse_prev"] and not e.loc["T.2", "act"] and e.loc["T.2", "prev_record_id"] == "T.1"
    assert "L.1" not in e.index                                                   # entry 2024-01-09 is past the last day


def test_sizing_rules():
    u = units([{"record_id": "A.1", "trade_id": "A", "disclosure_date": "2024-01-02", "disclosure_datetime": "2024-01-02T10:00:00",
                "transaction_type": "Purchase", "amount_mid": 8000.5, "amount_lower": 1001.0}])
    assert evm.size_of(u, cfg_())[0] == 8000.5
    assert evm.size_of(u, cfg_(sizing="lower_bound"))[0] == 1001.0
    assert evm.size_of(u, cfg_(sizing="equal_dollar", equal_dollar_amount=15000))[0] == 15000.0


# ---------------------------------------------------------------- return series
def test_idle_days_earn_rf_and_series_a_matches_hand_calculation():
    px = prices({"AAA": [10, 11, 12, 12, 12, 12]})
    pc, _ = run([ev(0, "Purchase", 100), ev(2, "Sale (Full)", 1)], px)
    rf = np.full(6, 0.0001)
    daily, rec = pf.series(pc, px.ffill, DAYS, rf)
    a = daily["series_a_return"].to_numpy()
    assert a[0] == pytest.approx(0.0001)                    # bought on day 0: earns from day 1
    assert a[1] == pytest.approx(0.1) and a[2] == pytest.approx(1 / 11)        # sold on day 2: earns day 2, then leaves
    assert a[3:] == pytest.approx([0.0001] * 3)
    assert daily["open_lots"].tolist() == [1, 1, 0, 0, 0, 0]
    assert daily["capital_deployed"].tolist() == pytest.approx([100, 110, 0, 0, 0, 0])
    assert rec["diff_book_minus_lots"] == pytest.approx(0, abs=1e-9)


def test_fixed_pot_series_b():
    px = prices({"AAA": [10, 11, 12, 12, 12, 12]})
    pc, _ = run([ev(0, "Purchase", 100), ev(2, "Sale (Full)", 1)], px)
    daily, rec = pf.series(pc, px.ffill, DAYS, np.zeros(6))
    assert rec["K"] == pytest.approx(100)
    nav = daily["pot_nav"].to_numpy()
    assert nav.tolist() == pytest.approx([100, 110, 120, 120, 120, 120])
    assert daily["series_b_return"].iloc[1] == pytest.approx(0.1)
    assert rec["diff_pot_minus_lots"] == pytest.approx(0, abs=1e-9)


def test_equal_weight_rebalances_at_each_event_date():
    px = prices({"AAA": [10, 10, 20, 20, 20, 20], "BBB": [10, 10, 10, 10, 20, 20]})
    # lot A $100 bought day 0; lot B $900 bought day 1; A doubles on day 2; B doubles on day 4
    pc, _ = run([ev(0, "Purchase", 100, sym="AAA"), ev(1, "Purchase", 900, sym="BBB")], px)
    d_dollar, _ = pf.series(pc, px.ffill, DAYS, np.zeros(6), "dollar")
    d_equal, _ = pf.series(pc, px.ffill, DAYS, np.zeros(6), "equal")
    assert d_dollar["series_a_return"].iloc[2] == pytest.approx(100 / 1000)       # dollar weights 10% / 90%
    assert d_equal["series_a_return"].iloc[2] == pytest.approx(0.5)               # equal weights after day 1's event
    # no event on days 2-3: weights drift to 2/3 A, 1/3 B, so B doubling on day 4 adds one third
    assert d_equal["series_a_return"].iloc[4] == pytest.approx(1 / 3)


def test_reconciliation_on_a_mixed_book():
    px = prices({"AAA": [10, 11, 9, 12, 13, 12], "BBB": [20, 21, 22, 19, 18, 25]})
    evs = [ev(0, "Purchase", 100), ev(0, "Purchase", 300, sym="BBB"), ev(1, "Purchase", 50),
           ev(2, "Sale (Partial)", 60), ev(3, "Sale (Full)", 1, sym="BBB"), ev(4, "Purchase", 70, sym="BBB")]
    pc, _ = run(evs, px)
    _, rec = pf.series(pc, px.ffill, DAYS, np.full(6, 0.0002))
    assert abs(rec["diff_book_minus_lots"]) < 0.005 and abs(rec["diff_series_a_minus_lots"]) < 0.005
    assert abs(rec["diff_pot_minus_lots"]) < 0.005


# ---------------------------------------------------------------- panel and firewall
def test_panel_horizons_and_censoring():
    cal = DAYS
    px = prices({"AAA": [10, 11, 12, 13, 14, 15], "SPY": [100, 100, 100, 110, 110, 110]})
    e = pd.DataFrame([{**ev(1, "Purchase", 100), "transaction_date": "2024-01-02", "disclosure_date": "2024-01-02",
                       "is_etf": False, "is_otc": False}])
    p = pn.build(e, pd.DataFrame(columns=["record_id", "action", "reversed_record_id"]), px.exact, px.ffill, cal, cal[-1],
                 [2, 5], {"AAA": cal[-1]})
    r = p.iloc[0]
    assert r.gap_raw == pytest.approx(0.1) and r.gap_spy == pytest.approx(0) and r.lag_trading_days == 1
    assert r.r_entry_2 == pytest.approx(13 / 11 - 1) and r.x_entry_2 == pytest.approx(13 / 11 - 1 - 0.1)
    assert r.r_txn_2 == pytest.approx(0.2) and np.isnan(r.r_entry_5) and r.r_txn_5 == pytest.approx(0.5)


def test_out_of_sample_is_refused_while_the_firewall_is_shut():
    c = copy.deepcopy(load_config())
    c["oos"]["oos_unlocked"], c["engine"]["sample"] = False, "in_sample"     # the locked state (the live config is U1)
    assert sample_bounds(c)[:2] == ("2021-09-01", "2024-02-29")
    c["engine"]["sample"] = "full"
    with pytest.raises(OutOfSampleLocked):
        sample_bounds(c)


# ---------------------------------------------------------------- K4-K6
def test_k6_repairs_scale_and_carry_forward():
    from src.prices import repairs as rp
    px = pd.DataFrame({"date": ["2019-03-12", "2019-03-13", "2019-03-14", "2019-04-02"],
                       "close": [24.6, 123.0, 123.0, 24.3], "adj_close": [21.3, 106.5, 106.5, 21.0]})
    fixed, log = rp.apply(px, "THLLY", [{"ticker": "THLLY", "type": "scale", "from": "2019-03-13", "to": "2019-03-14", "factor": 0.2}])
    assert fixed["close"].tolist() == pytest.approx([24.6, 24.6, 24.6, 24.3]) and len(log) == 2
    fixed, log = rp.apply(px, "THLLY", [{"ticker": "THLLY", "type": "carry_forward", "from": "2019-03-13", "to": "2019-03-14"}])
    assert fixed["adj_close"].tolist() == pytest.approx([21.3, 21.3, 21.3, 21.0])
    assert {r["ticker"] for r in rp.load()} == {"THLLY", "QABSY", "TRUMY", "EVVTY", "LYSDY", "TGOPY"}


def test_k5_etf_classes():
    from src.clean.etf_class import classify_text, load_overrides
    assert classify_text("Large Blend", "")[0] == "equity"
    assert classify_text("Ultrashort Bond", "")[0] == "fixed_income"
    assert classify_text("Target Maturity", "")[0] == "fixed_income"
    assert classify_text("Trading--Inverse Debt", "")[0] == "fixed_income"
    assert classify_text("Commodities Focused", "")[0] == "commodity"
    assert classify_text("Digital Assets", "")[0] == "other"
    assert classify_text("Equity Precious Metals", "")[0] == "equity"
    assert classify_text("", "iShares iBonds Dec 2025 Term Corporate ETF")[0] == "fixed_income"
    assert load_overrides()["HIYS"]["class"] == "fixed_income"


def test_k4_every_ledger_symbol_has_a_reason():
    from src.prices.resolve import LEDGER, REASON_CODES, load_ledger_reasons
    reasons = load_ledger_reasons()
    assert all(v["reason"] in REASON_CODES and v["source"] for v in reasons.values())
    for t in ("SQ", "BRK", "AVB", "EA", "HIYS", "WIZEY", "HOLX", "KYOCY"):
        assert t in reasons
    if LEDGER.exists():
        led = pd.read_csv(LEDGER, keep_default_na=False)
        assert (led["reason_source"] != "not researched").all()


def test_k4_hand_non_us_listings():
    from src.clean.build import load_non_us
    assert set(load_non_us()) >= {"BRK", "COLPAL"}
