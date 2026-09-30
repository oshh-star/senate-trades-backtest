"""SIC industry codes for every stock the trades use (Phase 6 prep, committee test). Run by hand from the repo root:

    python scripts/sec_sic.py

Symbols: every price symbol of a record in scope but for the variant switches (trade_records.csv scope_base), except
ETFs (a fund has no industry). CIK: for a survivorship-ledger symbol, the CIK that data/interim/ledger_sec_evidence.csv
matched by company NAME (its ticker may now belong to someone else); otherwise SEC's company_tickers.json by the price
symbol, then by the eFD ticker. The SIC code comes from the company's SEC submissions file (data.sec.gov, cached in
data/raw/sec/submissions/, one request per second, contact e-mail in the User-Agent). Output:
data/interim/sic_codes.csv (symbol, cik, cik_source, sec_name, sic, sic_description). A symbol with no CIK or no SIC
is listed with an empty sic and left out of the committee test (counted there).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import load_config, user_agent  # noqa: E402
from src.prices import resolve as rv  # noqa: E402

OUT = Path("data/interim/sic_codes.csv")


def main() -> None:
    cfg = load_config()
    recs = pd.read_csv("data/processed/trade_records.csv", keep_default_na=False, dtype=str, low_memory=False)
    use = recs[(recs["scope_base"] == "True") & (recs["is_etf"] != "True") & (recs["price_ticker"] != "")]
    syms = use.groupby("price_ticker")["ticker"].apply(lambda s: sorted(set(s) - {""})).to_dict()
    ct = json.loads(Path("data/raw/sec/company_tickers.json").read_text())
    by_ticker = {v["ticker"].upper().replace(".", "-"): str(v["cik_str"]) for v in ct.values()}
    ev = pd.read_csv("data/interim/ledger_sec_evidence.csv", keep_default_na=False, dtype=str)
    ev = ev[ev["cik"] != ""].drop_duplicates("price_ticker")
    ledger = set(pd.read_csv("data/interim/survivorship_ledger.csv", keep_default_na=False)["price_ticker"])
    by_ledger = dict(zip(ev["price_ticker"], ev["cik"]))
    sec = rv.Sec(user_agent(cfg), float(cfg["scrape"]["min_seconds_between_requests"]))
    rows = []
    for i, (sym, efd) in enumerate(sorted(syms.items())):
        cik, how = "", ""
        if sym in ledger and sym in by_ledger:
            cik, how = by_ledger[sym], "ledger evidence (matched by company name)"
        elif sym in by_ticker:
            cik, how = by_ticker[sym], "SEC company_tickers.json (price symbol)"
        else:
            hit = next((t for t in efd if t in by_ticker), None)
            if hit:
                cik, how = by_ticker[hit], f"SEC company_tickers.json (eFD ticker {hit})"
        row = {"symbol": sym, "efd_tickers": " ".join(efd), "cik": cik, "cik_source": how or "none found",
               "sec_name": "", "sic": "", "sic_description": ""}
        if cik:
            try:
                d = sec.submissions(cik)
                row.update(sec_name=d.get("name") or "", sic=str(d.get("sic") or ""), sic_description=d.get("sicDescription") or "")
            except Exception as e:                                   # logged, never guessed
                row["cik_source"] += f"; submissions failed: {e}"
        rows.append(row)
        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{len(syms)}", flush=True)
    out = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(f"{OUT}: {len(out)} symbols, {int((out['sic'] != '').sum())} with a SIC code")


if __name__ == "__main__":
    main()
