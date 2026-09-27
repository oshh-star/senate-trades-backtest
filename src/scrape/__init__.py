"""Stage 'scrape' (Phase 1): Senate service dates, eFD PTR listing and pages, raw parse,
filer-to-senator name matching and the first-look counts. No filtering happens here."""
from __future__ import annotations

from src.config import user_agent

STEPS = ["legislators", "listing", "download", "manifest", "parse", "names", "summary"]
# Default window first (A06), then the older years.
YEAR_ORDER = [2021, 2022, 2023, 2024, 2025, 2026, 2016, 2017, 2018, 2019, 2020]


def run(cfg: dict, years: list[int] | None = None, steps: list[str] | None = None,
        refresh_listing: bool = False) -> None:
    from . import download, legislators, listing
    from .efd import EfdClient

    steps = steps or STEPS
    first, last = cfg["data"]["scrape_start"].year, cfg["data"]["scrape_end"].year
    years = years or [y for y in YEAR_ORDER if first <= y <= last]
    ua = user_agent(cfg)
    client = EfdClient(ua, min_interval=float(cfg["scrape"]["min_seconds_between_requests"]))

    if "legislators" in steps:
        legislators.run(cfg, ua)
    for year in years:
        if "listing" not in steps and "download" not in steps:
            break
        recs = listing.fetch_year(client, cfg, year, refresh=refresh_listing)
        n_e = sum(r["kind"] == "electronic" for r in recs)
        print(f"  [listing] {year}: {len(recs)} filings ({n_e} electronic, {len(recs) - n_e} other)")
        if "download" in steps:
            c = download.download(client, recs)
            print(f"  [download] {year}: {c}")
    if "manifest" in steps:
        recs, dups = listing.load_all_cached(cfg)
        rows = download.build_manifest(recs)
        download.write_manifest(rows)
        print(f"  [manifest] {len(rows)} filings -> {download.MANIFEST} ({len(dups)} duplicate listings)")
    if "parse" in steps:
        from . import parse
        parse.run(cfg)
    if "names" in steps:
        from . import names
        names.run(cfg)
    if "summary" in steps:
        from . import summary
        summary.run(cfg)
