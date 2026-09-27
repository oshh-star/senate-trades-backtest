"""Rebuild every number in the project with one command, from the repo root:

    python run_all.py                  # run every stage in order
    python run_all.py --skip-scrape    # use the cached raw data in data/raw/
    python run_all.py --only metrics report
    python run_all.py --config config/config.yaml
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from src import clean, engine, metrics, prices, report, scrape
from src.config import analysis_window, load_config

STAGES = [("scrape", scrape), ("clean", clean), ("prices", prices),
          ("engine", engine), ("metrics", metrics), ("report", report)]


def main(argv=None) -> int:
    if not Path("config/config.yaml").exists():
        sys.exit("Run this from the repository root (config/config.yaml not found).")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="config/config.yaml")
    ap.add_argument("--only", nargs="+", choices=[n for n, _ in STAGES], help="run only these stages")
    for name, _ in STAGES:
        ap.add_argument(f"--skip-{name}", action="store_true", help=f"skip the {name} stage")
    args = ap.parse_args(argv)

    cfg = load_config(args.config)
    start, end = analysis_window(cfg)
    print(f"Config: {args.config} | analysis window {start} to {end} "
          f"({cfg['analysis']['window_years']} years) | OOS unlocked: {cfg['oos']['oos_unlocked']}")
    for name, module in STAGES:
        if (args.only and name not in args.only) or getattr(args, f"skip_{name}"):
            print(f"- {name}: skipped")
            continue
        t0 = time.time()
        print(f"- {name}: running")
        module.run(cfg)
        print(f"  done in {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
