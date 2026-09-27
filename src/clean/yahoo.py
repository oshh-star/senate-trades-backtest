"""Yahoo instrument type and listing exchange for each ticker, cached in data/raw/yahoo_meta/.

For each symbol we ask Yahoo's chart endpoint (the one yfinance uses) and keep ONLY descriptive
fields (instrument type, exchange, currency, names, first trade date). Price fields are dropped
before the response is cached: Phase 2 computes no prices. If the chart endpoint does not know the
symbol (typically delisted or renamed), Yahoo's search endpoint is tried and only a quote whose
symbol is exactly the one asked for is used. A symbol neither endpoint knows is "unresolved";
Phase 3 resolves renames and delistings.

Caveat: Yahoo describes whoever owns the symbol TODAY. A recycled symbol can describe a different
company from the one the senator traded, so name_mismatch flags symbols whose Yahoo name shares no
word with any eFD asset name seen for that ticker (Phase 3 checks these).

Resumable: one JSON file per symbol; delete a file to re-query it.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import requests

CACHE = Path("data/raw/yahoo_meta")
CHART = "https://query2.finance.yahoo.com/v8/finance/chart/{sym}?range=1d&interval=1d"
SEARCH = "https://query1.finance.yahoo.com/v1/finance/search?q={sym}&quotesCount=10&newsCount=0"
KEEP_META = ["symbol", "currency", "exchangeName", "fullExchangeName", "instrumentType", "firstTradeDate",
             "longName", "shortName", "exchangeTimezoneName"]
KEEP_QUOTE = ["symbol", "quoteType", "typeDisp", "exchange", "exchDisp", "longname", "shortname"]
# Yahoo exchange codes. US national exchanges; US OTC markets. Anything else is non-US.
US_EXCHANGES = {"NYQ", "NYS", "NYSE", "NMS", "NGM", "NCM", "NAS", "NIM", "NASDAQ", "ASE", "AMEX", "PCX",
                "BTS", "BATS", "CXI", "PSE", "WCB", "NCMX", "NGMX", "NMSX"}
US_OTC = {"PNK", "OQB", "OQX", "OBB", "OEM", "OGM", "OTC", "OPR", "PINK", "OTCBB"}
TYPE_MAP = {"EQUITY": "equity", "ETF": "etf", "MUTUALFUND": "mutual_fund"}


def cache_path(sym: str) -> Path:
    return CACHE / (re.sub(r"[^A-Za-z0-9.\-]", lambda m: f"_{ord(m.group()):x}_", sym) + ".json")


class Throttle:
    def __init__(self, interval: float):
        self.interval, self.last = interval, 0.0

    def wait(self):
        d = time.time() - self.last
        if d < self.interval:
            time.sleep(self.interval - d)
        self.last = time.time()


def _get(session, url, throttle, tries=4):
    for k in range(tries):
        throttle.wait()
        try:
            r = session.get(url, timeout=30)
            if r.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"HTTP {r.status_code}")
            return r
        except requests.RequestException:
            if k == tries - 1:
                raise
            time.sleep(2 ** (k + 1))


def fetch(sym: str, session, throttle) -> dict:
    rec = {"symbol": sym, "queried_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    r = _get(session, CHART.format(sym=requests.utils.quote(sym, safe="")), throttle)
    try:
        body = r.json()
    except ValueError:
        body = {}
    res = ((body.get("chart") or {}).get("result") or [None])[0]
    if r.status_code == 200 and res:
        rec["chart"] = {k: res["meta"].get(k) for k in KEEP_META}
    else:
        rec["chart_error"] = {"status": r.status_code, "error": (body.get("chart") or {}).get("error")}
        r2 = _get(session, SEARCH.format(sym=requests.utils.quote(sym, safe="")), throttle)
        try:
            quotes = r2.json().get("quotes", [])
        except ValueError:
            quotes = []
        rec["search"] = [{k: q.get(k) for k in KEEP_QUOTE} for q in quotes]
    return rec


def lookup(symbols: list[str], user_agent: str, min_interval: float) -> dict[str, dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = user_agent
    throttle = Throttle(min_interval)
    out, n_new = {}, 0
    todo = [s for s in sorted(set(symbols)) if s]
    for i, sym in enumerate(todo, 1):
        p = cache_path(sym)
        if p.exists():
            out[sym] = json.loads(p.read_text())
            continue
        rec = fetch(sym, session, throttle)
        p.write_text(json.dumps(rec, indent=1, sort_keys=True))
        out[sym] = rec
        n_new += 1
        if n_new % 100 == 0:
            print(f"  [yahoo] {i}/{len(todo)} symbols ({n_new} fetched this run)", flush=True)
    print(f"  [yahoo] {len(todo)} symbols: {len(todo) - n_new} from cache, {n_new} fetched")
    return out


def classify(rec: dict | None) -> dict:
    """instrument_type (equity | etf | mutual_fund | other | unresolved), exchange, listing, flags."""
    out = {"recognised": False, "instrument_type": "unresolved", "yahoo_type": "", "exchange": "",
           "exchange_name": "", "currency": "", "name": "", "short_name": "", "listing": "unknown",
           "is_otc": False, "yahoo_source": ""}
    if not rec:
        return out
    if rec.get("chart"):
        m = rec["chart"]
        out.update(recognised=True, yahoo_type=m.get("instrumentType") or "", exchange=m.get("exchangeName") or "",
                   exchange_name=m.get("fullExchangeName") or "", currency=m.get("currency") or "",
                   name=m.get("longName") or "", short_name=m.get("shortName") or "", yahoo_source="chart")
    else:
        q = [q for q in rec.get("search", []) if (q.get("symbol") or "").upper() == rec["symbol"].upper()]
        if not q:
            return out
        q = q[0]
        out.update(recognised=True, yahoo_type=q.get("quoteType") or "", exchange=q.get("exchange") or "",
                   exchange_name=q.get("exchDisp") or "", name=q.get("longname") or "",
                   short_name=q.get("shortname") or "", yahoo_source="search")
    out["instrument_type"] = TYPE_MAP.get(out["yahoo_type"], "other")
    ex = out["exchange"].upper()
    full = out["exchange_name"].upper()
    if ex in US_OTC or "OTC" in full or "PINK" in full:
        out["listing"], out["is_otc"] = "us_otc", True
    elif ex in US_EXCHANGES and out["currency"] in ("", "USD"):
        out["listing"] = "us_exchange"
    else:
        out["listing"] = "non_us"
    return out
