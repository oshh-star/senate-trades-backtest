from pathlib import Path

from src.scrape.efd import parse_ptr, parse_search_row

FIXTURE = Path(__file__).parent / "fixtures" / "ptr_schiff_2025-09-30.html"


def test_parse_ptr_transactions():
    ptr = parse_ptr(FIXTURE.read_text())
    assert ptr["filed_date"] == "09/30/2025"
    assert ptr["columns"][:4] == ["#", "Transaction Date", "Owner", "Ticker"]
    t = ptr["transactions"][0]
    assert (t["Ticker"], t["Owner"], t["Type"], t["Amount"]) == (
        "AAPL", "Spouse", "Sale (Partial)", "$15,001 - $50,000")


def test_parse_search_row_electronic_and_paper():
    e = parse_search_row(["Adam B", "Schiff", "Schiff,  Adam B. (Senator)",
                          '<a href="/search/view/ptr/e8371653/" target="_blank">Periodic Transaction Report for 09/30/2025</a>',
                          "09/30/2025"])
    p = parse_search_row(["RICHARD ", "BLUMENTHAL", "Senator",
                          '<a href="/search/view/paper/387cefb6/" target="_blank">Periodic Transaction Report for 09/24/2025</a>',
                          "09/24/2025"])
    assert (e["kind"], e["report_id"], e["office"]) == ("electronic", "e8371653", "Schiff, Adam B. (Senator)")
    assert (p["kind"], p["first_name"]) == ("paper", "RICHARD")
