"""Phase 3 (prices): J3 records, overrides, renames, Yahoo parsing, Ken French parsing, checks."""
import io
import zipfile

import numpy as np
import pandas as pd

from src.clean import amendments as am
from src.clean.build import override_matches, price_symbol
from src.prices import checks, french, resolve
from src.prices import yahoo_prices as yp
from tests.test_phase2 import filing, row, run_book


# ---------------------------------------------------------------- J3 records
def test_correction_creates_a_record_at_the_amendment_datetime():
    fs = [filing("O", "2024-01-10T10:00:00"), filing("A", "2024-03-01T09:00:00", title="2024-01-10", amend=1)]
    rs = [row("O", 1, "AAPL", owner="Spouse"), row("O", 2, "MSFT"),
          row("A", 1, "AAPL", owner="Self"), row("A", 2, "MSFT")]
    book, _, tr = run_book(fs, rs)
    aapl = tr[("AAPL", "2024-01-02", "Self")]
    recs = aapl["records"]
    assert [r["owner"] for r in recs] == ["Spouse", "Self"]                       # as first published, then corrected
    assert [r["effective_datetime"] for r in recs] == ["2024-01-10T10:00:00", "2024-03-01T09:00:00"]
    assert recs[1]["changed_fields"] == "owner"
    assert len(tr[("MSFT", "2024-01-02", "Self")]["records"]) == 1                # restated unchanged: one record


def test_rewording_the_asset_name_is_not_a_new_record():
    fs = [filing("O", "2024-01-10T10:00:00"), filing("A", "2024-03-01T09:00:00", title="2024-01-10", amend=1)]
    rs = [row("O", 1, "AAPL", name="Apple Inc"), row("A", 1, "AAPL", name="Apple Inc. Common Stock")]
    book, _, tr = run_book(fs, rs)
    t = tr[("AAPL", "2024-01-02", "Self")]
    assert len(t["records"]) == 1 and t["records"][0]["asset_name"] == "Apple Inc. Common Stock"


# ---------------------------------------------------------------- overrides and renames
def test_override_matching():
    assert override_matches({"equals": "starbuck"}, " Starbuck ")
    assert not override_matches({"equals": "starbuck"}, "SBUX.SW-STARBUCKS (Swiss)")
    assert override_matches({"contains": "(bk)"}, "Bank of New York Mellon Corp (BK)")


def test_price_symbol_follows_chains_and_stops_on_loops():
    ren = {"A": {"new": "B"}, "B": {"new": "C"}, "X": {"new": "Y"}, "Y": {"new": "X"}}
    assert price_symbol("A", ren) == "C" and price_symbol("Z", ren) == "Z"
    assert price_symbol("X", ren) in {"X", "Y"}


def test_strict_names_keep_distinctive_words():
    s = resolve.strict_name
    assert s("Vector Group Ltd.") != s("VECTOR HOLDING, LLC")
    assert s("Facebook, Inc. - Class A Common Stock") == s("FACEBOOK INC")
    assert s("Harris Corporation") == s("HARRIS CORP /DE/")
    assert s("Boulder Growth & Income Fund, Inc.") == s("BOULDER GROWTH & INCOME FUND")
    assert resolve.US_SYMBOL.match("BRK-B") and not resolve.US_SYMBOL.match("COLPAL")


# ---------------------------------------------------------------- Yahoo parsing
def chart(ts, close, adj, events=None, tz="America/New_York"):
    return {"status": 200, "body": {"chart": {"result": [{
        "meta": {"symbol": "X", "exchangeTimezoneName": tz, "currency": "USD"}, "timestamp": ts,
        "indicators": {"quote": [{"close": close, "volume": [1] * len(ts)}], "adjclose": [{"adjclose": adj}]},
        "events": events or {}}]}}}


def test_parse_yahoo_chart():
    ts = [1704205800, 1704292200, 1704378600]                    # 2 to 4 Jan 2024, 09:30 New York
    ev = {"dividends": {"1": {"date": 1704292200, "amount": 0.24}},
          "splits": {"2": {"date": 1704378600, "numerator": 2, "denominator": 1, "splitRatio": "2:1"}}}
    d = yp.parse(chart(ts, [10.0, None, 11.0], [9.5, 9.6, 10.9], ev))
    assert d["prices"]["date"].tolist() == ["2024-01-02", "2024-01-04"]          # the missing close is dropped
    assert d["dividends"].iloc[0].to_dict() == {"date": "2024-01-03", "dividend": 0.24}
    assert d["splits"].iloc[0]["ratio"] == "2:1"
    assert yp.parse({"status": 404, "body": {}})["prices"].empty


# ---------------------------------------------------------------- Ken French parsing
def zipped(text: str) -> io.BytesIO:
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr("f.CSV", text)
    b.seek(0)
    return b


def test_read_french_monthly_stops_before_annual_block(tmp_path):
    text = ("This file was created ...\n\n,Mkt-RF,SMB,HML,RF\n202607,  -0.61, -1.92, 2.11, 0.33\n"
            "202608,   2.56,  0.34,-3.54, 0.29\n\n Annual Factors: January-December \n,Mkt-RF,SMB,HML,RF\n"
            "2025,  12.0, 1.0, 2.0, 4.0\n")
    p = tmp_path / "m.zip"
    p.write_bytes(zipped(text).getvalue())
    df = french.read_table(p, monthly=True)
    assert df["period"].tolist() == [202607, 202608] and list(df.columns) == ["period", "Mkt-RF", "SMB", "HML", "RF"]


def test_read_french_daily(tmp_path):
    p = tmp_path / "d.zip"
    p.write_bytes(zipped("header\n\n,Mom   \n20260828, -1.47\n20260831, -0.14\n\nCopyright\n").getvalue())
    df = french.read_table(p, monthly=False)
    assert df["Mom"].tolist() == [-1.47, -0.14]


# ---------------------------------------------------------------- checks
def test_next_trading_day_is_strictly_after():
    cal = pd.Series(["2024-01-02", "2024-01-03", "2024-01-05"])
    got = checks.next_trading_day(cal, pd.Series(["2024-01-02", "2024-01-04", "2024-01-05"]))
    assert got.tolist()[:2] == ["2024-01-03", "2024-01-05"] and pd.isna(got.iloc[2])


def test_daily_checks_flag_moves_staleness_and_gaps():
    cal = pd.Series([f"2024-01-{d:02d}" for d in range(2, 20)])
    px = pd.DataFrame({"ticker": "A", "date": cal.iloc[:5], "close": [10, 30, 10, 10, 10], "adj_close": [10, 30, 10, 10, 10]})
    px = pd.concat([px, pd.DataFrame({"ticker": "B", "date": [cal.iloc[0], cal.iloc[8]], "close": [5, 5], "adj_close": [5, 5]})])
    out = checks.daily_checks(px, pd.DataFrame(columns=["date", "ticker", "ratio"]), cal)
    big = out["large"]
    assert big["date"].tolist() == ["2024-01-03", "2024-01-04"]
    assert big.iloc[0]["explanation"].startswith("reverses")
    st = out["stale"].set_index("ticker")
    assert st.loc["A", "zero_return_days"] == 2 and st.loc["B", "zero_share"] == 1.0
    assert out["gaps"]["missing_trading_days"].tolist() == [7]


def test_ticker_in_name_is_case_sensitive():
    from src.clean.tickers import ticker_in_name
    assert ticker_in_name("TACO", "Taco Co (TACO)") and ticker_in_name("AAPL", "AAPL-Apple Inc.")
    assert not ticker_in_name("TACO", "Del Taco Restaurants, Inc.")
    assert not ticker_in_name("BK", "BKNG Holdings")
