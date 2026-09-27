"""Phase 2 (clean): amendments, tickers, amounts, instrument classification, flags."""
import datetime as dt

import pandas as pd
import pytest

from src.clean import amendments as am
from src.clean import tickers as tk
from src.clean import yahoo as yh
from src.clean.build import add_scope_flags, is_option_name, parse_amount
from src.quality import write_section
from src.scrape.legislators import service_spells

SCRAPE_START = dt.date(2016, 1, 1)


# ---------------------------------------------------------------- synthetic filings
def filing(ptr, when, title=None, amend=0, senator="S1"):
    return {"ptr_id": ptr, "bioguide_id": senator, "senator": senator, "datetime_received": when,
            "date_received": when[:10], "title_date": title or when[:10], "is_amendment": amend > 0,
            "amendment_number": str(amend)}


def row(ptr, i, ticker, date="2024-01-02", ttype="Purchase", amount="$1,001 - $15,000", owner="Self",
        name=None, senator="S1"):
    name = name or f"{ticker} Inc"
    t = tk.normalise_ticker(ticker)
    return {"ptr_id": ptr, "row_id": f"{ptr}:{i}", "bioguide_id": senator, "owner": owner,
            "transaction_date_iso": date, "ticker": t, "ticker_raw": ticker, "asset_name": name,
            "asset_type": "Stock", "transaction_type": ttype, "amount": amount, "comment": "",
            "asset_name_norm": am.norm_name(name), "asset_id": am.asset_id(t, name), "is_sale": ttype in am.SALES}


def run_book(filings, rows):
    f = pd.DataFrame(filings)
    r = pd.DataFrame(rows)
    by_ptr = {p: g.to_dict("records") for p, g in r.groupby("ptr_id")}
    links = am.link_amendments(f, by_ptr, pd.DataFrame(columns=["bioguide_id", "date_received"]), SCRAPE_START)
    book, classes = am.build_trades(r, f, links)
    trades = {(t["ticker"], t["transaction_date_iso"], t["owner"]): t for t in book.trades}
    return book, classes.set_index("ptr_id") if len(classes) else classes, trades


def test_full_restatement_with_correction_keeps_original_datetime():
    fs = [filing("O", "2024-01-10T10:00:00"), filing("A", "2024-03-01T09:00:00", title="2024-01-10", amend=1)]
    rs = [row("O", 1, "AAPL"), row("O", 2, "MSFT"),
          row("A", 1, "AAPL"), row("A", 2, "MSFT", amount="$15,001 - $50,000")]
    book, cls, tr = run_book(fs, rs)
    assert len(book.trades) == 2
    assert cls.loc["A", "class"] == "FULL_RESTATEMENT"
    msft = tr[("MSFT", "2024-01-02", "Self")]
    assert msft["amount"] == "$15,001 - $50,000"                 # corrected value used
    assert msft["first_datetime"] == "2024-01-10T10:00:00"      # original's datetime (no look-ahead)
    assert msft["corrected_fields"] == {"amount"}
    assert len(book.corrections) == 1


def test_additive_amendment_new_trade_takes_amendment_datetime():
    fs = [filing("O", "2024-01-10T10:00:00"), filing("A", "2024-02-01T16:00:00", title="2024-01-10", amend=1)]
    rs = [row("O", 1, "AAPL"), row("A", 1, "NVDA", date="2024-01-05")]
    book, cls, tr = run_book(fs, rs)
    assert cls.loc["A", "class"] == "ADDITIVE"
    assert tr[("NVDA", "2024-01-05", "Self")]["first_datetime"] == "2024-02-01T16:00:00"
    assert tr[("NVDA", "2024-01-05", "Self")]["first_is_amendment"]
    assert len(book.trades) == 2


def test_partial_repeat_is_ambiguous_and_nothing_is_deleted():
    fs = [filing("O", "2024-01-10T10:00:00"), filing("A", "2024-02-01T10:00:00", title="2024-01-10", amend=1)]
    rs = [row("O", 1, "AAPL"), row("O", 2, "MSFT"), row("O", 3, "GOOG"), row("A", 1, "AAPL")]
    book, cls, tr = run_book(fs, rs)
    assert cls.loc["A", "class"] == "AMBIGUOUS"
    assert len(book.trades) == 3
    assert all("AMBIGUOUS" in t["amendment_classes"] for t in book.trades)


def test_identical_lines_in_one_filing_are_separate_trades():
    fs = [filing("O", "2024-01-10T10:00:00"), filing("A", "2024-02-01T10:00:00", title="2024-01-10", amend=1)]
    rs = [row("O", 1, "AAPL"), row("O", 2, "AAPL"), row("A", 1, "AAPL"), row("A", 2, "AAPL")]
    book, cls, _ = run_book(fs, rs)
    assert len(book.trades) == 2                                  # two lots, restated once each
    assert cls.loc["A", "class"] == "FULL_RESTATEMENT"
    assert sum(m["role"] == "restated_in_amendment" for m in book.row_map) == 2


def test_lone_changed_line_is_not_guessed_as_a_correction():
    fs = [filing("O", "2024-01-10T10:00:00"), filing("A", "2024-02-01T10:00:00", title="2024-01-10", amend=1)]
    rs = [row("O", 1, "AAPL"), row("A", 1, "AAPL", ttype="Sale (Full)")]
    book, cls, _ = run_book(fs, rs)
    assert len(book.trades) == 2 and cls.loc["A", "class"] == "AMBIGUOUS"


def test_amendment_chain():
    fs = [filing("O", "2024-01-10T10:00:00"),
          filing("A1", "2024-02-01T10:00:00", title="2024-01-10", amend=1),
          filing("A2", "2024-03-01T10:00:00", title="2024-01-10", amend=2)]
    rs = [row("O", 1, "AAPL"), row("A1", 1, "NVDA", date="2024-01-05"),
          row("A2", 1, "AAPL"), row("A2", 2, "NVDA", date="2024-01-05", ttype="Sale (Full)")]
    book, cls, tr = run_book(fs, rs)
    assert cls.loc["A1", "class"] == "ADDITIVE"
    assert cls.loc["A2", "class"] == "FULL_RESTATEMENT"
    nvda = tr[("NVDA", "2024-01-05", "Self")]
    assert nvda["transaction_type"] == "Sale (Full)"             # corrected by A2 (unique type change)
    assert nvda["first_datetime"] == "2024-02-01T10:00:00"      # first public in A1
    assert len(book.trades) == 2


def test_unlinked_amendment_of_pre_scrape_report():
    fs = [filing("A", "2016-03-01T10:00:00", title="2015-12-24", amend=1)]
    rs = [row("A", 1, "AAPL", date="2015-12-20")]
    book, cls, _ = run_book(fs, rs)
    assert cls.loc["A", "class"] == "UNLINKED"
    assert "predates the scrape start" in cls.loc["A", "note"]
    assert book.trades[0]["first_datetime"] == "2016-03-01T10:00:00"


def test_trade_refiled_in_a_later_original_is_merged():
    fs = [filing("O1", "2024-01-10T10:00:00"), filing("O2", "2024-02-10T10:00:00")]
    rs = [row("O1", 1, "AAPL"), row("O2", 1, "AAPL"), row("O2", 2, "MSFT")]
    book, _, tr = run_book(fs, rs)
    assert len(book.trades) == 2
    assert tr[("AAPL", "2024-01-02", "Self")]["first_ptr_id"] == "O1"
    assert [m["role"] for m in book.row_map].count("repeated_from_other_filing") == 1


def test_other_senators_are_never_merged():
    fs = [filing("O1", "2024-01-10T10:00:00"), filing("O2", "2024-01-11T10:00:00", senator="S2")]
    rs = [row("O1", 1, "AAPL"), row("O2", 1, "AAPL", senator="S2")]
    book, _, _ = run_book(fs, rs)
    assert len(book.trades) == 2


def test_correction_pass_does_not_guess_between_two_candidates():
    fs = [filing("O", "2024-01-10T10:00:00"), filing("A", "2024-02-01T10:00:00", title="2024-01-10", amend=1)]
    rs = [row("O", 1, "AAPL", amount="$1,001 - $15,000"), row("O", 2, "AAPL", amount="$15,001 - $50,000"),
          row("A", 1, "AAPL", amount="$50,001 - $100,000"), row("A", 2, "AAPL", amount="$100,001 - $250,000")]
    book, cls, _ = run_book(fs, rs)
    assert len(book.trades) == 4                                  # ambiguous which line was corrected
    assert cls.loc["A", "class"] == "ADDITIVE"


def test_ticker_written_in_name_matches_ticker_column():
    fs = [filing("O", "2024-01-10T10:00:00"), filing("A", "2024-02-01T10:00:00", title="2024-01-10", amend=1)]
    o = row("O", 1, "--", name="AAPL-Apple Inc.")
    o["asset_id"] = am.asset_id("", o["asset_name"], tk.embedded_candidate(o["asset_name"])[0])
    rs = [o, row("A", 1, "AAPL", name="Apple Inc.")]
    book, cls, _ = run_book(fs, rs)
    assert len(book.trades) == 1 and cls.loc["A", "class"] == "FULL_RESTATEMENT"


def test_norm_name_harmonises_date_formats():
    assert am.norm_name("Bond Matures: 05/01/2030") == am.norm_name("Bond Matures: 2030-05-01")


# ---------------------------------------------------------------- tickers
@pytest.mark.parametrize("raw,expected", [
    ("aapl", "AAPL"), (" BRK.B ", "BRK-B"), ("BRK/B", "BRK-B"), ("BRK-B", "BRK-B"), ("--", ""), ("", ""),
    ("MSFT*", "MSFT"), ("ADT.F", "ADT.F"), ("LM09.SG", "LM09.SG"), ("NEE-PC", "NEE-PC")])
def test_normalise_ticker(raw, expected):
    assert tk.normalise_ticker(raw) == expected


@pytest.mark.parametrize("name,expected", [
    ("Wise plc Sponsored ADR (WIZEY)", ("WIZEY", "Wise plc Sponsored ADR")),
    ("GOOGL - Alphabet Inc. A", ("GOOGL", "Alphabet Inc. A")),
    ("JPM-JPMorgan Chase & Co.", ("JPM", "JPMorgan Chase & Co.")),
    ("NVDA", ("NVDA", "")),
    ("Bridger Technologies, Inc.", None),
])
def test_embedded_candidate(name, expected):
    assert tk.embedded_candidate(name) == expected


def test_verify_embedded_needs_yahoo_and_a_shared_word():
    rec = {"recognised": True, "name": "JPMorgan Chase & Co.", "short_name": ""}
    assert tk.verify_embedded("JPM", "JPMorgan Chase & Co.", rec, None)[0]
    assert not tk.verify_embedded("ROLLS", "ROYCE HOLDINGS PLC ADR", {"recognised": False}, None)[0]
    assert not tk.verify_embedded("XYZ", "Rolls Royce", {"recognised": True, "name": "Other Corp", "short_name": ""}, None)[0]
    assert tk.verify_embedded("NVDA", "", {"recognised": True, "name": "NVIDIA", "short_name": ""}, None)[0]


def test_sec_name_match_is_exact_and_unique():
    sec = tk.SecIndex([{"ticker": "QCOM", "title": "QUALCOMM INC/DE", "cik": "1"},
                       {"ticker": "GOOGL", "title": "Alphabet Inc.", "cik": "2"},
                       {"ticker": "GOOG", "title": "Alphabet Inc.", "cik": "2"}])
    assert sec.match_name("Qualcomm Inc")[0] == "QCOM"         # legal form and state suffix ignored
    assert sec.match_name("Qualcomm Technologies Inc")[0] == ""  # extra word: not exact
    sec2 = tk.SecIndex([{"ticker": "QCOM", "title": "QUALCOMM INC", "cik": "1"}])
    assert sec2.match_name("Qualcomm Inc")[0] == "QCOM"
    assert sec.match_name("Alphabet Inc.")[0] == ""            # two share classes: not guessed


# ---------------------------------------------------------------- amounts and options
def test_parse_amount():
    a = parse_amount("$1,001 - $15,000")
    assert (a["amount_lower"], a["amount_upper"], a["amount_mid"]) == (1001, 15000, 8000.5)
    b = parse_amount("Over $50,000,000")
    assert b["amount_mid"] == 50_000_000 and b["amount_open_top"]
    assert not parse_amount("Spouse/DC Over $1,000,000")["amount_parsed"]


@pytest.mark.parametrize("name,expected", [
    ("SMCI CALL", True), ("NVDA PUT", True), ("Option Care Health Inc", False), ("Putnam Growth Fund", False),
    ("Callaway Golf", False), ("AAPL option strike 150 expiring 1/19/2024", True)])
def test_option_names(name, expected):
    assert is_option_name(name) is expected


# ---------------------------------------------------------------- Yahoo classification
def test_classify():
    chart = lambda t, ex, full, cur="USD": {"symbol": "X", "chart": {"instrumentType": t, "exchangeName": ex,
                                                                    "fullExchangeName": full, "currency": cur}}
    assert yh.classify(chart("EQUITY", "NMS", "NasdaqGS"))["listing"] == "us_exchange"
    etf = yh.classify(chart("ETF", "PCX", "NYSEArca"))
    assert etf["instrument_type"] == "etf" and not etf["is_otc"]
    assert yh.classify(chart("MUTUALFUND", "NAS", "Nasdaq"))["instrument_type"] == "mutual_fund"
    otc = yh.classify(chart("EQUITY", "OID", "OTC Markets OTCID"))
    assert otc["is_otc"] and otc["listing"] == "us_otc"
    assert yh.classify(chart("EQUITY", "LSE", "London", "GBp"))["listing"] == "non_us"
    assert yh.classify(None)["instrument_type"] == "unresolved"
    s = {"symbol": "ABC", "chart_error": {}, "search": [{"symbol": "ABCD", "quoteType": "EQUITY", "exchange": "NYQ"}]}
    assert not yh.classify(s)["recognised"]                    # only an exact symbol counts
    s["search"].append({"symbol": "ABC", "quoteType": "ETF", "exchange": "PCX"})
    assert yh.classify(s)["instrument_type"] == "etf"


def test_cached_meta_has_no_prices():
    assert not {"regularMarketPrice", "chartPreviousClose", "fiftyTwoWeekHigh"} & set(yh.KEEP_META)


# ---------------------------------------------------------------- flags
def test_scope_flags():
    n = 60
    tr = pd.DataFrame({"trade_id": [f"T{i}" for i in range(n + 3)],
                       "in_scope": [True] * (n + 2) + [False],
                       "first_ptr_id": ["BIG"] * n + ["P1", "P2", "BIG"],
                       "bioguide_id": ["T000278"] * n + ["X1", "X2", "T000278"],
                       "senator": ["Tuberville"] * n + ["Ann", "Bob", "Tuberville"],
                       "days_since_service_start": [0, 179, 180] + [1000] * (n + 0),
                       "is_etf": False, "owner": ["Self"] * (n + 2) + ["Spouse"]})
    f = add_scope_flags(tr)
    assert f["bulk_ptr"].tolist() == [True] * n + [False, False, True]   # 60 in-scope trades in BIG
    assert f.loc[0, "senator_rank"] == 1 and f.loc[n, "senator_rank"] == 2 and f.loc[n + 1, "senator_rank"] == 3
    assert f["v3_first_180d"].tolist()[:3] == [True, True, False]
    assert f["v6_family_owner"].tolist()[-1] and f["v1_tuberville"].sum() == n + 1


def test_service_spells():
    d = dt.date
    spells = service_spells([(d(2015, 1, 6), d(2021, 1, 3)), (d(2021, 1, 3), d(2027, 1, 3)), (d(2030, 1, 3), d(2031, 1, 3))])
    assert spells == [(d(2015, 1, 6), d(2027, 1, 3)), (d(2030, 1, 3), d(2031, 1, 3))]


def test_write_section_keeps_other_phases(tmp_path):
    p = tmp_path / "dq.md"
    write_section(1, ["## Phase 1: scrape", "", "one"], p)
    write_section(2, ["## Phase 2: clean", "", "two"], p)
    write_section(1, ["## Phase 1: scrape", "", "ONE"], p)
    text = p.read_text()
    assert "ONE" in text and "two" in text and "one" not in text
    assert text.index("Phase 1") < text.index("Phase 2")
