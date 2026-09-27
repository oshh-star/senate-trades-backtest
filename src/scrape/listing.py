"""PTR search listing: every filing received in a year, for every filer type (decision A05).

The search endpoint returns at most 100 rows per page and does not say which filer type a row
belongs to, so each filer type is queried separately. A year with more than 100 filings of one type
is re-queried month by month (each month fits in one page), which avoids relying on the site's
ordering to page through results. Every response is cached as JSON under
data/raw/efd/search/<year>/ and committed.

A cached listing whose query end date had not yet passed when it was fetched is incomplete (for
example 2026, scraped before the 2026-09-30 cutoff) and is fetched again on the next run.
"""
from __future__ import annotations

import calendar
import datetime as dt
import json
from pathlib import Path

from .efd import EfdClient, parse_search_row

SEARCH_DIR = Path("data/raw/efd/search")
FILER_TYPE_LABELS = {1: "Senator", 4: "Candidate", 5: "Former Senator"}
PAGE = 100


def _mdy(d: dt.date) -> str:
    return d.strftime("%m/%d/%Y")


def year_range(cfg: dict, year: int) -> tuple[dt.date, dt.date]:
    start = max(dt.date(year, 1, 1), cfg["data"]["scrape_start"])
    end = min(dt.date(year, 12, 31), cfg["data"]["scrape_end"])
    return start, end


def _is_complete(cached: dict) -> bool:
    fetched = dt.datetime.fromisoformat(cached["fetched_at"]).date()
    return fetched > dt.date.fromisoformat(cached["query"]["end"])


def _fetch(client: EfdClient, path: Path, filer_type: int, start: dt.date, end: dt.date,
           refresh: bool) -> dict:
    if path.exists() and not refresh:
        cached = json.loads(path.read_text())
        if _is_complete(cached):
            return cached
    page = client.search_page([filer_type], _mdy(start), _mdy(end), length=PAGE)
    out = {"query": {"filer_type": filer_type, "start": start.isoformat(), "end": end.isoformat(),
                     "report_type": 11, "date_field": "date received"},
           "fetched_at": dt.datetime.now().replace(microsecond=0).isoformat(),
           "recordsTotal": page["recordsTotal"], "data": page["data"]}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    return out


def fetch_year(client: EfdClient, cfg: dict, year: int, refresh: bool = False) -> list[dict]:
    """Fetch (or load from cache) the listing for one year; returns flat filing records."""
    start, end = year_range(cfg, year)
    records = []
    for ft in cfg["data"]["scrape_filer_types"]:
        whole = _fetch(client, SEARCH_DIR / str(year) / f"type{ft}_{year}.json", ft, start, end, refresh)
        chunks = [whole]
        if whole["recordsTotal"] > PAGE:
            chunks = []
            for m in range(start.month, end.month + 1):
                ms = max(dt.date(year, m, 1), start)
                me = min(dt.date(year, m, calendar.monthrange(year, m)[1]), end)
                c = _fetch(client, SEARCH_DIR / str(year) / f"type{ft}_{year}-{m:02d}.json", ft, ms, me, refresh)
                if c["recordsTotal"] > PAGE:
                    raise RuntimeError(f"{year}-{m:02d} type {ft} has {c['recordsTotal']} filings (> {PAGE})")
                chunks.append(c)
            if sum(c["recordsTotal"] for c in chunks) != whole["recordsTotal"]:
                raise RuntimeError(f"{year} type {ft}: monthly totals do not add up to the yearly total")
        for c in chunks:
            if len(c["data"]) != c["recordsTotal"]:
                raise RuntimeError(f"Listing {c['query']} returned {len(c['data'])} of {c['recordsTotal']} rows")
            for row in c["data"]:
                rec = parse_search_row(row)
                rec.update(filer_type_code=ft, filer_type_label=FILER_TYPE_LABELS.get(ft, str(ft)),
                           listing_year=year)
                records.append(rec)
    return records


def load_all_cached(cfg: dict) -> tuple[list[dict], list[dict]]:
    """Every filing in the cached listings (no network), de-duplicated by report id.
    Returns (filings, duplicates); a duplicate is a report id listed under a second filer type."""
    seen, out, dups = set(), [], []
    for year in range(cfg["data"]["scrape_start"].year, cfg["data"]["scrape_end"].year + 1):
        ydir = SEARCH_DIR / str(year)
        if not ydir.exists():
            continue
        for ft in cfg["data"]["scrape_filer_types"]:
            whole = ydir / f"type{ft}_{year}.json"
            if not whole.exists():
                continue
            files = [whole]
            if json.loads(whole.read_text())["recordsTotal"] > PAGE:
                files = sorted(ydir.glob(f"type{ft}_{year}-*.json"))
            for f in files:
                for row in json.loads(f.read_text())["data"]:
                    rec = parse_search_row(row)
                    if rec["report_id"] in seen:
                        dups.append({**rec, "filer_type_code": ft})
                        continue
                    seen.add(rec["report_id"])
                    rec.update(filer_type_code=ft, filer_type_label=FILER_TYPE_LABELS.get(ft, str(ft)),
                               listing_year=year)
                    out.append(rec)
    return out, dups
