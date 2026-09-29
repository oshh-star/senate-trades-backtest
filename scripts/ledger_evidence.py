"""Collect SEC EDGAR evidence for every survivorship-ledger symbol (K4), to support the hand-written
reasons in config/ledger_reasons.yaml. Run by hand: python scripts/ledger_evidence.py

For each ledger symbol, the eFD asset names are matched to SEC filer CIKs through cik-lookup-data
(the same strict name rule as src/prices/resolve.py). For each CIK (at most 3), the filing index is
fetched once from data.sec.gov and cached, slimmed to form types and dates, in
data/raw/sec/filings/CIK##########.json.gz. Output: data/interim/ledger_sec_evidence.csv with the
dates of the forms that mark a company's exit (25 / 25-NSE delisting, 15 deregistration, merger
proxies DEFM14A / DEFM14C, tender offers SC TO-T / SC 14D9, going-private SC 13E3, fund
deregistration N-8F) and the last filing of any kind.
"""
from __future__ import annotations

import gzip
import json
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import load_config, user_agent  # noqa: E402
from src.prices import resolve as rv  # noqa: E402

FILINGS = Path("data/raw/sec/filings")
OUT = Path("data/interim/ledger_sec_evidence.csv")
EXIT_FORMS = ["25-NSE", "25", "15-12B", "15-12G", "15-15D", "DEFM14A", "DEFM14C", "SC TO-T", "SC 14D9", "SC 13E3", "N-8F"]


def filings(sec: rv.Sec, cik: str) -> dict:
    p = FILINGS / f"CIK{int(cik):010d}.json.gz"
    if not p.exists():
        FILINGS.mkdir(parents=True, exist_ok=True)
        d = sec._get(rv.SUBMISSIONS_URL.format(cik=int(cik))).json()
        rec = d.get("filings", {}).get("recent", {})
        keep = {"cik": d.get("cik"), "name": d.get("name"), "tickers": d.get("tickers"), "exchanges": d.get("exchanges"),
                "formerNames": d.get("formerNames"), "forms": rec.get("form", []), "dates": rec.get("filingDate", []),
                "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        with gzip.open(p, "wt") as f:
            json.dump(keep, f)
    with gzip.open(p, "rt") as f:
        return json.load(f)


def main() -> None:
    cfg = load_config()
    sec = rv.Sec(user_agent(cfg), float(cfg["scrape"]["min_seconds_between_requests"]))
    idx = sec.name_index()
    led = pd.read_csv(rv.LEDGER, keep_default_na=False)
    rows = []
    for r in led.itertuples():
        names = [n for n in r.efd_asset_names.split(" | ") if n]
        ciks = sorted({c for n in names for c in idx.get(rv.strict_name(n), set())}, key=int)[:3]
        if not ciks:
            rows.append({"price_ticker": r.price_ticker, "cik": "", "sec_name": "", "evidence": "no SEC filer with this name"})
            continue
        for c in ciks:
            f = filings(sec, c)
            ev = []
            for form in EXIT_FORMS:
                ds = [d for fm, d in zip(f["forms"], f["dates"]) if fm == form]
                if ds:
                    ev.append(f"{form} {max(ds)}")
            last = max(f["dates"]) if f["dates"] else ""
            rows.append({"price_ticker": r.price_ticker, "cik": c, "sec_name": f.get("name", ""),
                         "current_tickers": " ".join(f.get("tickers") or []), "last_filing": last,
                         "evidence": "; ".join(ev)})
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"{len(rows)} rows -> {OUT}")


if __name__ == "__main__":
    main()
