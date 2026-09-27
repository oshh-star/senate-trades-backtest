"""Run Phase 1 steps by hand, in chunks, from the repo root:

    python -m src.scrape --years 2021 2022      # listing + download for these years only
    python -m src.scrape --steps legislators
    python -m src.scrape --steps manifest parse names summary   # offline, from the cache
"""
import argparse

from src.config import load_config
from src.scrape import STEPS, run

ap = argparse.ArgumentParser()
ap.add_argument("--years", nargs="+", type=int, help="received years to list and download")
ap.add_argument("--steps", nargs="+", choices=STEPS, help="default: every step")
ap.add_argument("--refresh-listing", action="store_true", help="re-fetch cached search listings")
a = ap.parse_args()
run(load_config(), years=a.years, steps=a.steps, refresh_listing=a.refresh_listing)
