import datetime as dt
from pathlib import Path

import pandas as pd
import pytest

from src.config import load_config
from src.scrape.download import filed_timestamp, normalise_time
from src.scrape.efd import amendment_number, count_table_rows, parse_search_row
from src.scrape.legislators import check_departures, scheduled_end
from src.scrape.listing import _is_complete
from src.scrape.names import match_one, norm, office_names
from src.scrape.parse import parse_filing
from src.scrape.summary import in_service, key_filter, type_group

FIXTURE = Path(__file__).parent / "fixtures" / "ptr_schiff_2025-09-30.html"
META = {k: "" for k in ("ptr_id", "filer_name", "first_name", "last_name", "office_text", "filer_type_code",
                        "filer_type_label", "date_received", "time_received", "datetime_received",
                        "is_amendment", "amendment_number", "url")}


# ---------------------------------------------------------------- parse validation
def test_fixture_parses_and_validates():
    rows, val = parse_filing(META, FIXTURE.read_text())
    assert len(rows) == 1 == val["tbody_rows"] == val["stated_total"]
    assert val["row_count_ok"] and val["owner_counts_ok"]
    r = rows[0]
    assert (r["ticker"], r["owner"], r["transaction_type"], r["transaction_date_iso"]) == (
        "AAPL", "Spouse", "Sale (Partial)", "2025-09-22")


def test_row_count_mismatch_is_caught():
    html = FIXTURE.read_text().replace("(1 transaction total)", "(2 transactions total)")
    _, val = parse_filing(META, html)
    assert not val["row_count_ok"]


def test_owner_count_mismatch_is_caught():
    html = FIXTURE.read_text().replace("1 Spouse", "0 Spouse").replace("0 Self", "1 Self")
    _, val = parse_filing(META, html)
    assert val["row_count_ok"] and not val["owner_counts_ok"]


def test_page_without_table_fails_validation():
    html = FIXTURE.read_text()
    html = html[:html.index("<table")] + html[html.index("</table>") + 8:]
    rows, val = parse_filing(META, html)
    assert rows == [] and count_table_rows(html) is None and not val["row_count_ok"]


def test_every_row_is_kept_including_missing_ticker():
    html = FIXTURE.read_text()
    start = html.index("<tr>", html.index("<tbody>"))
    end = html.index("</tr>", start) + 5
    row2 = html[start:end].replace(">1<", ">2<").replace("AAPL</a>", "--</a>").replace("Spouse", "Self")
    html = html[:end] + row2 + html[end:]
    html = html.replace("(1 transaction total)", "(2 transactions total)")
    html = html.replace("0 Self", "1 Self")
    rows, val = parse_filing(META, html)
    assert [r["ticker"] for r in rows] == ["AAPL", "--"]
    assert val["row_count_ok"] and val["owner_counts_ok"]


# ---------------------------------------------------------------- timestamps and titles
@pytest.mark.parametrize("raw,out", [("10 AM", "10:00 AM"), ("9:09 PM", "9:09 PM"), ("9:09 p.m.", "9:09 PM"),
                                     ("noon", "12:00 PM"), ("midnight", "12:00 AM")])
def test_normalise_time(raw, out):
    assert normalise_time(raw) == out


def test_filed_timestamp_from_fixture():
    assert filed_timestamp(FIXTURE.read_text()) == ("09/30/2025", "11:20 AM")


def test_filed_timestamp_on_the_hour():
    assert filed_timestamp('<strong>Filed 02/24/2021 @ 10 AM</strong>') == ("02/24/2021", "10:00 AM")


@pytest.mark.parametrize("title,n", [("Periodic Transaction Report for 11/19/2020", 0),
                                     ("Periodic Transaction Report for 11/19/2020 (Amendment 1)", 1),
                                     ("Periodic Transaction Report for 11/19/2020 (Amendment 12)", 12)])
def test_amendment_number(title, n):
    assert amendment_number(title) == n


def test_search_row_title_date():
    r = parse_search_row(["A", "B", "B, A (Senator)",
                          '<a href="/search/view/ptr/x1/">Periodic Transaction Report for 01/09/2021 (Amendment 2)</a>',
                          "08/05/2021"])
    assert (r["title_date"], r["amendment_number"], r["is_amendment"]) == ("01/09/2021", 2, True)


def test_listing_complete_only_after_end_date():
    q = {"query": {"end": "2026-09-30"}}
    assert not _is_complete({**q, "fetched_at": "2026-09-27T12:00:00"})
    assert not _is_complete({**q, "fetched_at": "2026-09-30T23:00:00"})
    assert _is_complete({**q, "fetched_at": "2026-10-01T00:00:01"})


# ---------------------------------------------------------------- service dates
@pytest.mark.parametrize("cls,start,end", [(2, "2021-01-03", "2027-01-03"), (1, "2019-01-03", "2025-01-03"),
                                           (3, "2020-01-06", "2023-01-03"), (1, "2023-10-03", "2025-01-03")])
def test_scheduled_end(cls, start, end):
    assert scheduled_end(cls, dt.date.fromisoformat(start)) == dt.date.fromisoformat(end)


def test_check_departures_flags_overlap():
    rows = [{"bioguide_id": "A1", "full_name": "A", "state": "XX", "senate_class": 1, "term_start": "2019-01-03",
             "term_end": "2025-01-03", "source_file": "legislators-historical.yaml"},
            {"bioguide_id": "B1", "full_name": "B", "state": "XX", "senate_class": 1, "term_start": "2023-05-01",
             "term_end": "2025-01-03", "source_file": "legislators-historical.yaml"}]
    issues = check_departures(rows, dt.date(2026, 9, 27))
    assert len(issues) == 1 and "departure may be missing" in issues[0]


def test_in_service_is_inclusive_and_per_senator():
    terms = pd.DataFrame({"bioguide_id": ["A1", "A1"], "term_start": ["2019-01-03", "2025-01-03"],
                          "term_end": ["2025-01-03", "2026-03-23"]})
    tx = pd.DataFrame({"bioguide_id": ["A1", "A1", "A1", "B1", "A1"],
                       "transaction_date_iso": ["2019-01-03", "2026-03-23", "2026-03-24", "2020-01-01", ""]})
    assert in_service(tx, terms).tolist() == [True, True, False, False, False]


# ---------------------------------------------------------------- name matching
PEOPLE = {
    "M000355": {"full_name": "Mitch McConnell", "last_n": "mcconnell", "first_tokens": {"mitch"},
                "full_n": "mitch mcconnell"},
    "H000601": {"full_name": "Bill Hagerty", "last_n": "hagerty", "first_tokens": {"bill", "william"},
                "full_n": "bill hagerty"},
    "S001217": {"full_name": "Rick Scott", "last_n": "scott", "first_tokens": {"rick", "richard"},
                "full_n": "rick scott"},
    "S001184": {"full_name": "Tim Scott", "last_n": "scott", "first_tokens": {"tim", "timothy"},
                "full_n": "tim scott"},
}


def test_norm_and_office_names():
    assert norm("McConnell, Jr.") == "mcconnell"
    assert norm("Hyde-Smith") == "hyde smith"
    assert office_names("Hagerty, Bill (Senator)") == ("bill", "hagerty")
    assert office_names("Senator") == ("", "")


def test_exact_match_uses_office_nickname():
    m = match_one("William F", "Hagerty, IV", {"Hagerty, Bill (Senator)"}, PEOPLE, {})
    assert (m["bioguide_id"], m["method"], m["confidence"]) == ("H000601", "exact", "high")


def test_same_last_name_needs_first_name():
    m = match_one("Rick", "Scott", {"Scott, Rick (Senator)"}, PEOPLE, {})
    assert m["bioguide_id"] == "S001217" and m["method"] == "exact"


def test_unknown_name_is_not_guessed():
    m = match_one("Zebediah", "Quimby", {"Candidate"}, PEOPLE, {})
    assert m["bioguide_id"] == "" and m["confidence"] == "none"


def test_override_wins_and_can_say_not_a_senator():
    ov = {"zebediah|quimby": {"bioguide_id": None, "note": "2016 candidate"},
          "rick|scott": "S001184"}
    assert match_one("Zebediah", "Quimby", set(), PEOPLE, ov)["confidence"] == "none"
    assert match_one("Rick", "Scott", set(), PEOPLE, ov)["bioguide_id"] == "S001184"


# ---------------------------------------------------------------- key number
def test_key_filter_conditions():
    cfg = load_config()
    base = {"date_received": "2023-05-01", "confidence": "high", "in_service": True, "owner": "Self",
            "ticker": "AAPL", "asset_type": "Stock"}
    variants = [{}, {"date_received": "2021-08-31"}, {"date_received": "2026-09-01"}, {"confidence": "low"},
                {"in_service": False}, {"owner": "Spouse"}, {"ticker": "--"}, {"asset_type": "Stock Option"},
                {"asset_type": "Other", "ticker": "SPY"}, {"asset_type": "Other", "ticker": "--"}]
    tx = pd.DataFrame([{**base, **v} for v in variants])
    kept, waterfall = key_filter(tx, cfg)
    assert kept.index.tolist() == [0, 8]
    assert waterfall["Rows left"].iloc[0] == len(tx) and waterfall["Rows left"].iloc[-1] == 2


@pytest.mark.parametrize("t,g", [("Purchase", "Purchase"), ("Sale (Full)", "Sale (Full)"),
                                 ("Sale (Partial)", "Sale (Partial)"), ("Sale", "Sale (other)"),
                                 ("Exchange", "Exchange"), ("", "Other")])
def test_type_group(t, g):
    assert type_group(t) == g
