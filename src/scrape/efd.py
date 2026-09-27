"""Client for the US Senate Electronic Financial Disclosure (eFD) search site.

Flow (verified against the live site on 2026-09-27):
  1. GET  /search/home/  -> page with a terms-of-use form and a csrfmiddlewaretoken.
  2. POST /search/home/  with prohibition_agreement=1 + the token -> redirects to /search/.
     The session cookie now carries the agreement.
  3. POST /search/report/data/  (DataTables server-side endpoint) returns JSON:
     {"recordsTotal": n, "data": [[first, last, office, link_html, date_received], ...]}
  4. GET  /search/view/ptr/<uuid>/    -> electronic PTR (HTML transactions table)
     GET  /search/view/paper/<uuid>/  -> scanned paper filing (GIF images, not parseable)

Form codes (read from the live search form, not assumed):
  filer_type: 1 = Senator, 4 = Candidate, 5 = Former Senator
  report_type: 11 = Periodic Transactions

Every request goes through a rate limiter (config: scrape.min_seconds_between_requests).
"""
from __future__ import annotations

import re
import time
from html.parser import HTMLParser

import requests

BASE_URL = "https://efdsearch.senate.gov"
FILER_TYPES = {"senator": 1, "candidate": 4, "former_senator": 5}
REPORT_TYPE_PTR = 11


class EfdClient:
    def __init__(self, user_agent: str, min_interval: float = 1.0, timeout: int = 60):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = user_agent
        self.min_interval = min_interval
        self.timeout = timeout
        self._last = 0.0
        self.n_requests = 0
        self.agreed = False

    def _wait(self):
        gap = time.monotonic() - self._last
        if gap < self.min_interval:
            time.sleep(self.min_interval - gap)
        self._last = time.monotonic()
        self.n_requests += 1

    def _get(self, path: str) -> requests.Response:
        self._wait()
        r = self.session.get(BASE_URL + path, timeout=self.timeout)
        r.raise_for_status()
        return r

    def _post(self, path: str, data: dict, referer: str) -> requests.Response:
        self._wait()
        headers = {"Referer": BASE_URL + referer}
        token = self.session.cookies.get("csrftoken")
        if token:
            headers["X-CSRFToken"] = token
        r = self.session.post(BASE_URL + path, data=data, headers=headers, timeout=self.timeout)
        r.raise_for_status()
        return r

    def agree(self) -> None:
        """Accept the eFD terms of use; the session cookie then unlocks search."""
        home = self._get("/search/home/").text
        m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', home)
        if not m:
            raise RuntimeError("eFD home page has no csrfmiddlewaretoken; site layout changed?")
        r = self._post("/search/home/",
                       {"prohibition_agreement": "1", "csrfmiddlewaretoken": m.group(1)},
                       referer="/search/home/")
        if not r.url.rstrip("/").endswith("/search"):
            raise RuntimeError(f"Terms agreement did not reach the search page (landed on {r.url})")
        self.agreed = True

    def search_page(self, filer_types: list[int], start: str, end: str,
                    offset: int = 0, length: int = 100,
                    report_types: list[int] = (REPORT_TYPE_PTR,)) -> dict:
        """One page of search results. Dates are MM/DD/YYYY (date received)."""
        if not self.agreed:
            self.agree()
        data = {
            "draw": "1", "start": str(offset), "length": str(length),
            "report_types": "[" + ",".join(str(x) for x in report_types) + "]",
            "filer_types": "[" + ",".join(str(x) for x in filer_types) + "]",
            "submitted_start_date": f"{start} 00:00:00",
            "submitted_end_date": f"{end} 23:59:59",
            "candidate_state": "", "senator_state": "", "office_id": "",
            "first_name": "", "last_name": "",
        }
        return self._post("/search/report/data/", data, referer="/search/").json()

    def search_all(self, filer_types: list[int], start: str, end: str, length: int = 100):
        """All result rows for a query, following pagination."""
        rows, offset = [], 0
        while True:
            page = self.search_page(filer_types, start, end, offset=offset, length=length)
            rows.extend(page["data"])
            offset += length
            if offset >= page["recordsTotal"] or not page["data"]:
                return rows, page["recordsTotal"]

    def count(self, filer_types: list[int], start: str, end: str) -> int:
        return self.search_page(filer_types, start, end, length=1)["recordsTotal"]

    def fetch_report(self, link: str) -> str:
        return self._get(link).text


def parse_search_row(row: list) -> dict:
    """Turn one DataTables row into a flat record."""
    first, last, office, link_html, date_received = row
    m = re.search(r'href="([^"]+)"[^>]*>([^<]*)<', link_html)
    link, title = (m.group(1), m.group(2).strip()) if m else ("", link_html)
    kind = "electronic" if "/view/ptr/" in link else "paper" if "/view/paper/" in link else "other"
    uuid = link.rstrip("/").rsplit("/", 1)[-1] if link else ""
    return {
        "first_name": " ".join(first.split()), "last_name": " ".join(last.split()),
        "office": " ".join(office.split()), "title": title, "link": link,
        "report_id": uuid, "kind": kind, "date_received": date_received,
        "is_amendment": "amendment" in title.lower(),
    }


class _TableParser(HTMLParser):
    """Collects header and body cells of every <table> on a page (stdlib only)."""

    def __init__(self):
        super().__init__()
        self.tables, self._cell, self._row, self._in_cell = [], [], None, False

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.tables.append({"header": [], "rows": []})
        elif tag == "tr" and self.tables:
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._in_cell, self._cell = True, []
        elif tag == "br" and self._in_cell:
            self._cell.append(" ")

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._in_cell:
            self._row.append((tag, " ".join("".join(self._cell).split())))
            self._in_cell = False
        elif tag == "tr" and self._row is not None:
            if self._row and all(t == "th" for t, _ in self._row):
                self.tables[-1]["header"] = [v for _, v in self._row]
            elif self._row:
                self.tables[-1]["rows"].append([v for _, v in self._row])
            self._row = None

    def handle_data(self, data):
        if self._in_cell:
            self._cell.append(data)


def parse_ptr(html: str) -> dict:
    """Extract filing metadata and the transactions table from an electronic PTR page."""
    p = _TableParser()
    p.feed(html)
    txn = next((t for t in p.tables if "Transaction Date" in t["header"]), None)
    filed = re.search(r"Filed\s+(\d{2}/\d{2}/\d{4})\s*@\s*([\d:]+\s*[AP]M)", html)
    name = re.search(r'<h2 class="filedReport">(.*?)</h2>', html, re.S)
    title = re.search(r'<h1 class="mb-2">(.*?)</h1>', html, re.S)
    return {
        "filer": " ".join(name.group(1).split()) if name else "",
        "title": " ".join(title.group(1).split()) if title else "",
        "filed_date": filed.group(1) if filed else "",
        "filed_time": " ".join(filed.group(2).split()) if filed else "",
        "columns": txn["header"] if txn else [],
        "transactions": [dict(zip(txn["header"], r)) for r in txn["rows"]] if txn else [],
    }
