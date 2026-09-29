"""Stage 'clean' (Phase 2): amendments and de-duplication, scope filters, tickers, Yahoo instrument
classification, amounts and the flags for the pre-registered variants V1-V6.

Reads data/interim/ (Phase 1); writes data/processed/trades_clean.csv, tickers.csv, exclusions.csv,
audit files in data/interim/ and the Phase 2 section of outputs/data_quality.md.
Network: SEC company_tickers.json (once, cached in data/raw/sec/) and Yahoo instrument metadata
(cached per symbol in data/raw/yahoo_meta/). No prices or returns are computed.
"""
from __future__ import annotations

from src.config import user_agent


def run(cfg: dict) -> dict:
    from . import build, etf_class, report, tickers, yahoo

    ua = user_agent(cfg)
    sec = tickers.SecIndex(tickers.load_sec(ua))
    interval = float(cfg["scrape"]["min_seconds_between_requests"])
    R = build.build(cfg, yahoo_lookup=lambda syms: yahoo.lookup(syms, ua, interval), sec_index=sec,
                    fund_lookup=lambda syms: etf_class.lookup(syms, ua, interval))
    report.run_report(cfg, R)
    return R
