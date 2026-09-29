"""Phase 5A.2: terminal-export (manual) and CRSP loaders, the source hierarchy (M2) and the pre-disclosure drift."""
import warnings

import numpy as np
import pandas as pd
import pytest

from src.prices import crsp, manual
from src.prices import sources as sc


# ---------------------------------------------------------------- manual (Bloomberg / FactSet) files
def write(path, text):
    path.write_text(text.strip() + "\n")
    return path


def test_manual_loader_reads_validates_and_derives_returns(tmp_path):
    write(tmp_path / "ECOM.csv", """
date,close,total_return_index
2022-11-10,22.90,100.0
2022-11-11,23.00,101.0
2022-11-14,,
2022-11-15,23.05,102.01
""")
    write(tmp_path / "SOURCES.md", "| ECOM | Harry | Bloomberg | 2026-10-01 | ECOM US Equity |")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        frames, rep = manual.load(tmp_path, delisted={"ECOM": "2022-11-15"})
    f = frames["ECOM"]
    assert f["date"].tolist() == ["2022-11-10", "2022-11-11", "2022-11-15"]           # the empty row is dropped
    assert f["ret"].tolist()[1:] == pytest.approx([0.01, 0.01])
    assert rep.loc[0, "blank_rows_dropped"] == 1 and rep.loc[0, "days_from_delisting"] == 0
    assert not any("SOURCES.md" in str(x.message) for x in w)


def test_manual_loader_warns_on_a_history_that_ends_far_from_the_delisting_and_missing_sources(tmp_path):
    write(tmp_path / "X.csv", "date,close,total_return_index\n2021-01-04,10,1\n2021-01-05,11,1.1")
    with pytest.warns(UserWarning) as w:
        manual.load(tmp_path, delisted={"X": "2025-06-18"})
    msgs = " ".join(str(x.message) for x in w)
    assert "not listed in SOURCES.md" in msgs and "tickers are reused" in msgs


@pytest.mark.parametrize("text, problem", [
    ("date,close,tri\n2021-01-04,10,1", "columns must be exactly"),
    ("date,close,total_return_index\n04/01/2021,10,1", "YYYY-MM-DD"),
    ("date,close,total_return_index\n2021-01-05,10,1\n2021-01-04,10,1", "increasing order"),
    ("date,close,total_return_index\n2021-01-04,10,1\n2021-01-04,10,1", "repeated date"),
    ("date,close,total_return_index\n2021-01-04,10,-1", "positive number"),
    ("date,close,total_return_index\n2021-02-30,10,1", "not a real date"),
])
def test_manual_loader_rejects_bad_files(tmp_path, text, problem):
    write(tmp_path / "BAD.csv", text)
    with pytest.raises(manual.ManualPriceError, match=problem):
        manual.read_file(tmp_path / "BAD.csv")


# ---------------------------------------------------------------- CRSP (WRDS export)
CRSP_CSV = """
PERMNO,date,TICKER,COMNAM,PRC,RET,DLRET
11111,20221110,ECOM,CHANNELADVISOR CORP,22.90,C,
11111,20221111,ECOM,CHANNELADVISOR CORP,-23.00,0.010000,
11111,20221114,ECOM,CHANNELADVISOR CORP,23.10,B,
11111,20221115,ECOM,CHANNELADVISOR CORP,,,0.002000
22222,20221110,ECOM,OTHER CO (TICKER REUSED LATER),5.00,0.0,
22222,20150105,ECOM,OLD OTHER CO,5.00,0.0,
22222,20150106,ECOM,OLD OTHER CO,5.00,0.0,
"""


def test_crsp_loader_uses_ret_and_dlret_and_picks_the_permno_trading_in_the_dates_needed(tmp_path):
    write(tmp_path / "crsp.csv", CRSP_CSV)
    wanted = {"ECOM": {"tickers": {"ECOM"}, "first": "2022-11-01", "last": "2022-11-15"}}
    frames, rep = crsp.load(wanted, tmp_path)
    assert rep.loc[0, "permno"] == "11111" and bool(rep.loc[0, "several_candidates"])
    f = frames["ECOM"]
    assert f["close"].tolist()[:2] == pytest.approx([22.90, 23.00])                 # negative PRC = bid/ask midpoint
    tri = f["adj_close"].to_numpy()
    assert tri[0] == pytest.approx(22.90)                                           # the index starts at |PRC|
    assert tri[1] / tri[0] - 1 == pytest.approx(0.01)
    assert tri[2] == pytest.approx(tri[1]) and rep.loc[0, "flat_days"] == 1          # RET 'B' = missing: flat
    assert tri[3] / tri[2] - 1 == pytest.approx(0.002)                               # delisting day: DLRET alone
    assert np.isnan(f["close"].iat[3])


def test_crsp_delisting_day_compounds_ret_and_dlret():
    x = pd.DataFrame({"permno": ["1", "1"], "date": ["2023-01-03", "2023-01-04"], "ticker": ["A", "A"], "comnam": ["A", "A"],
                      "close": [10.0, 11.0], "ret": [np.nan, 0.10], "dlret": [np.nan, -0.5]})
    x["ret_total"] = np.where(x["dlret"].notna(), (1 + x["ret"].fillna(0)) * (1 + x["dlret"]) - 1, x["ret"])
    s = crsp.index_series(x)
    assert s["adj_close"].iat[1] / s["adj_close"].iat[0] - 1 == pytest.approx(1.1 * 0.5 - 1)


def test_crsp_v2_column_names_and_iso_dates(tmp_path):
    write(tmp_path / "v2.csv", "PERMNO,DlyCalDt,Ticker,IssuerNm,DlyPrc,DlyRet\n7,2023-01-03,ZZ,ZED,10,\n7,2023-01-04,ZZ,ZED,10.5,0.05")
    frames, _ = crsp.load({"ZZ": {"tickers": {"ZZ"}, "first": "2023-01-01", "last": "2023-12-31"}}, tmp_path)
    assert frames["ZZ"]["adj_close"].tolist() == pytest.approx([10, 10.5])


def test_crsp_rejects_a_file_without_the_needed_columns(tmp_path):
    write(tmp_path / "bad.csv", "PERMNO,date,PRC\n1,20230103,10")
    with pytest.raises(crsp.CrspError, match="missing columns"):
        crsp.load({}, tmp_path)


# ---------------------------------------------------------------- the hierarchy
def frame(dates, levels, close=None):
    return pd.DataFrame({"date": dates, "close": close or levels, "adj_close": levels, "volume": np.nan})


def test_yahoo_only_passes_through_unchanged():
    y = frame(["d1", "d2"], [1.0, 2.0])
    m, info = sc.merge({"yahoo": y}, ["crsp", "manual", "yahoo"])
    assert m["adj_close"].tolist() == [1.0, 2.0] and set(m["source"]) == {"yahoo"} and info["unbridged_days"] == 0


def test_merge_takes_each_days_return_from_the_best_source_that_bridges_it():
    # CRSP covers d1-d3, Yahoo d2-d5, manual d4-d5 (all at different levels)
    c = frame(["d1", "d2", "d3"], [100, 110, 121])              # +10%, +10%
    mnl = frame(["d4", "d5"], [50, 55])                         # d4 -> d5: +10%
    y = frame(["d2", "d3", "d4", "d5"], [1.0, 1.0, 2.0, 2.2])   # d3 -> d4: +100%, d4 -> d5: +10%
    m, info = sc.merge({"crsp": c, "manual": mnl, "yahoo": y}, ["crsp", "manual", "yahoo"])
    assert m["source"].tolist() == ["crsp", "crsp", "crsp", "yahoo", "manual"]
    assert m["adj_close"].tolist() == pytest.approx([100, 110, 121, 242, 266.2])
    assert info["unbridged_days"] == 0
    m18, _ = sc.merge({"crsp": c, "manual": mnl, "yahoo": y}, ["yahoo"])     # V18
    assert m18["adj_close"].tolist() == [1.0, 1.0, 2.0, 2.2]


def test_merge_counts_a_day_no_source_bridges():
    c = frame(["d1", "d2"], [10, 11])
    y = frame(["d3", "d4"], [5, 6])
    m, info = sc.merge({"crsp": c, "yahoo": y}, ["crsp", "yahoo"])
    assert info["unbridged_days"] == 1 and m["adj_close"].tolist() == pytest.approx([10, 11, 11, 13.2])


def test_validation_compares_overlapping_daily_returns():
    a = frame(["d1", "d2", "d3", "d4"], [10, 11, 12.1, 12.1])
    b = frame(["d1", "d2", "d3", "d4"], [1, 1.1, 1.21, 1.3])
    r = sc.validate("S", {"crsp": a, "yahoo": b})[0]
    assert r["days"] == 3 and r["max_gap_date"] == "d4"
    assert r["max_abs_gap"] == pytest.approx(1.3 / 1.21 - 1)


# ---------------------------------------------------------------- pre-disclosure drift
def test_predisclosure_drift_table_signs_the_copiers_cost():
    from src.metrics.event_study import drift_table
    panel = pd.DataFrame({"side": ["purchase", "purchase", "sale", "sale", "sale"],
                          "entry_date": ["2022-01-03", "2022-02-01", "2022-01-03", "2022-02-01", "2022-03-01"],
                          "gap_x": [0.02, 0.04, -0.03, -0.01, np.nan], "gap_raw": [0.03, 0.05, -0.02, 0.0, np.nan],
                          "gap_spy": [0.01, 0.01, 0.01, 0.01, np.nan], "lag_trading_days": [10, 20, 5, 15, 7]})
    d = drift_table(panel).set_index("side")
    assert d.at["purchase", "N"] == 2 and d.at["purchase", "mean SPY-adjusted drift"] == pytest.approx(0.03)
    assert d.at["sale", "N"] == 2 and d.at["sale", "mean cost to the copier"] == pytest.approx(0.02)   # a fall is a cost
    assert d.at["sale", "share of events against the copier"] == pytest.approx(1.0)
    assert d.at["purchase", "median lag (trading days)"] == pytest.approx(15)
