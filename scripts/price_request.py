"""Write docs/PRICE_REQUEST.md (M2, Phase 5A.2): the survivorship-ledger symbols to pull from a Bloomberg or FactSet
terminal, and the WRDS settings and ticker lists for CRSP. Run by hand from the repo root after the prices stage:

    python scripts/price_request.py

Rows: every ledger symbol (data/interim/survivorship_ledger.csv) that a trade of ANY window or variant uses (the
headline with its warm-up, V6 family owners, V11 3 years, V12 10 years, V16 all ETFs, first-published J3 records),
sorted by the headline's midpoint purchase dollars (warm-up included), then by all-variant dollars. MUST-HAVE = the
smallest set of rows, from the top, that covers 95% of the headline dollars.
Also writes docs/crsp_tickers_ledger.txt (ledger symbols and their eFD tickers) and docs/crsp_tickers_all.txt (every
symbol any trade uses), one ticker per line, for the WRDS upload.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import load_config  # noqa: E402
from src.prices import delisting_dates_for_request  # noqa: E402
from src.prices.sources import needed  # noqa: E402

OUT = Path("docs/PRICE_REQUEST.md")
TICKERS_LEDGER = Path("docs/crsp_tickers_ledger.txt")
TICKERS_ALL = Path("docs/crsp_tickers_all.txt")
MUST_SHARE = 0.95


# Where the MUST-HAVE stocks were listed while the senators held them: written by hand (Claude, 2026-09-29, from
# memory; confirm at the terminal). Yahoo's exchange is not used for a recycled symbol (it is the new owner's).
EXCHANGE_HAND = {"X": "NYSE", "ECOM": "NYSE", "ATVI": "NASDAQ", "SSBK": "NASDAQ", "PARA": "NASDAQ", "WBA": "NASDAQ",
                 "GOGL": "NASDAQ (and Oslo)", "QRTEP": "NASDAQ", "TOELY": "US OTC (ADR)"}


def exchange_of(sym: str, names: str, tick: pd.DataFrame) -> str:
    if sym in EXCHANGE_HAND:
        return EXCHANGE_HAND[sym] + " (by hand)"
    r = tick[tick["price_ticker"] == sym]
    if len(r) and str(r["yahoo_name_mismatch"].iat[0]) == "True":
        r = r.iloc[0:0]
    if len(r) and str(r["is_otc"].iat[0]) == "True":
        return "US OTC (ADR)"
    m = re.search(r"\((NYSE|NASDAQ|Nasdaq|AMEX|NYSE American|NYSE Arca|OTC)\)", names or "")
    if m:
        return m.group(1).upper()
    if len(r) and r["exchange_name"].iat[0]:
        return str(r["exchange_name"].iat[0])
    return "US (check)"


def main() -> None:
    cfg = load_config()
    end = cfg["prices"]["end"].isoformat()
    cal = pd.read_csv("data/processed/trading_calendar.csv", dtype=str)["date"].tolist()
    delisted = delisting_dates_for_request()
    nd = needed(cfg, cal, end, delisted)
    led = pd.read_csv("data/interim/survivorship_ledger.csv", keep_default_na=False)
    tick = pd.read_csv("data/processed/tickers.csv", keep_default_na=False, dtype=str)
    recs = pd.read_csv("data/processed/trade_records.csv", keep_default_na=False, low_memory=False, dtype=str)
    # ledger symbols no in-scope-but-for-window-and-owner record uses (V16 bond funds, J3-only records): dates from any record
    extra = []
    for sym in sorted(set(led["price_ticker"]) - set(nd["symbol"])):
        g = recs[recs["price_ticker"] == sym]
        if not len(g):
            continue
        d0 = g["disclosure_date"].min()
        i0 = int(np.searchsorted(cal, d0, side="right"))
        extra.append({"symbol": sym, "efd_tickers": " ".join(sorted(set(g["ticker"]) - {""})),
                      "first_needed": cal[max(i0 - 5, 0)], "last_needed": min(delisted.get(sym, end), end),
                      "headline_trades": 0, "all_trades": int(g["trade_id"].nunique()), "headline_purchase_dollars": 0.0,
                      "all_purchase_dollars": float(pd.to_numeric(g.loc[g["transaction_type"] == "Purchase", "amount_mid"]).sum())})
    x = pd.concat([nd[nd["symbol"].isin(led["price_ticker"])], pd.DataFrame(extra)], ignore_index=True)
    L = led.set_index("price_ticker")
    x["company"] = x["symbol"].map(lambda s: (L.at[s, "efd_asset_names"].split(" | ")[0] if s in L.index else ""))
    x["exchange"] = [exchange_of(s, L.at[s, "efd_asset_names"] if s in L.index else "", tick) for s in x["symbol"]]
    x["reason"] = x["symbol"].map(lambda s: L.at[s, "reason"] if s in L.index else "")
    x["terms"] = x["symbol"].map(lambda s: L.at[s, "reason_source"] if s in L.index else "")
    x = x.sort_values(["headline_purchase_dollars", "all_purchase_dollars", "symbol"], ascending=[False, False, True]).reset_index(drop=True)
    tot = x["headline_purchase_dollars"].sum()
    cum = x["headline_purchase_dollars"].cumsum() / tot
    n_must = int((cum < MUST_SHARE).sum()) + 1
    x["priority"] = ["MUST-HAVE" if i < n_must else ("nice to have (headline)" if x.at[i, "headline_purchase_dollars"] > 0
                                                     else "variants only") for i in range(len(x))]
    x["cum_share"] = cum
    must = x.iloc[:n_must]
    # ticker lists for WRDS
    TICKERS_LEDGER.write_text("\n".join(sorted({t for s, e in zip(x["symbol"], x["efd_tickers"]) for t in [s, *e.split()]
                                                if re.fullmatch(r"[A-Z0-9.\-]+", t)})) + "\n")
    all_syms = pd.read_csv("data/processed/price_coverage.csv", keep_default_na=False)["ticker"]
    efd_all = set(recs["ticker"]) | set(recs["price_ticker"])
    TICKERS_ALL.write_text("\n".join(sorted({t for t in set(all_syms) | efd_all
                                             if t and re.fullmatch(r"[A-Z0-9.\-]+", t) and "=" not in t})) + "\n")

    def fmt_rows(d: pd.DataFrame) -> str:
        v = pd.DataFrame({"#": range(1, len(d) + 1), "priority": d["priority"], "ticker as traded": d["efd_tickers"],
                          "project symbol": d["symbol"], "company (eFD name)": d["company"].str.slice(0, 45),
                          "exchange": d["exchange"], "first date needed": d["first_needed"],
                          "last date needed": d["last_needed"], "why no prices": d["reason"],
                          "deal terms / source": d["terms"].str.slice(0, 140),
                          "in-scope trades (headline)": d["headline_trades"], "trades (all variants)": d["all_trades"],
                          "headline $": d["headline_purchase_dollars"].map(lambda v: f"{v:,.0f}"),
                          "all-variant $": d["all_purchase_dollars"].map(lambda v: f"{v:,.0f}")})
        return v.to_markdown(index=False)

    T = f"""# Price request: the survivorship-ledger stocks (Phase 5A.2)

_Generated by `python scripts/price_request.py` from the ledger (data/interim/survivorship_ledger.csv). Decision M2
(2026-09-29): the headline prices every trade from CRSP first, then a Bloomberg or FactSet export, then Yahoo._

**Why this matters.** Yahoo no longer has prices for {len(x)} stocks the senators traded, mostly companies that were
taken over. The strategy currently skips them, and in-sample they are up to 69% of the money invested. We need their
real prices.

**The {n_must} MUST-HAVE rows cover {must['headline_purchase_dollars'].sum() / tot:.1%} of the headline dollars at stake
(${must['headline_purchase_dollars'].sum():,.0f} of ${tot:,.0f}).** Please pull those first. The others are
nice to have: they are small, or only needed by robustness variants.

## What to do at the terminal (Bloomberg or FactSet, LBS library)

For each MUST-HAVE row:

1. **Find the right company.** Search by the **company name** in the table, not only the ticker. Old tickers are
   often reused by other companies (for example, Yahoo's "PARA" and "GOGL" now belong to someone else). On Bloomberg,
   type the company name and press the search key, then pick the security that shows **"Delisted"** or
   **"Acquired"** with the right company name. Write down its identifier (for example "ECOM US Equity", or the
   Bloomberg ID / ISIN it shows).
2. **Export DAILY data** from the **first date needed** to the **last date needed** in the table, with two fields:
   - the **closing price** (Bloomberg: `PX_LAST`);
   - a **daily total return index**, dividends reinvested (Bloomberg: `TOT_RETURN_INDEX_GROSS_DVDS`; on FactSet
     choose the total return index with dividends reinvested, and ask the librarian if unsure).
   In Excel with the Bloomberg add-in, one formula does it:
   `=BDH("ECOM US Equity","PX_LAST,TOT_RETURN_INDEX_GROSS_DVDS","2021-07-19","2022-11-15","Days=T")`
   (replace the identifier and the two dates with the row's).
3. **Check the last date.** The history should end on (or within a few days of) the **last date needed**, which is
   the delisting date for a company that was taken over. If it runs on for years after that, or stops much earlier,
   you probably have the wrong company: search again by name.
4. **Save one CSV per stock** as `data/raw/manual_prices/<TICKER>.csv`, where `<TICKER>` is the **project symbol**
   column (for example `data/raw/manual_prices/ECOM.csv`), with **exactly these three columns** and one row per
   trading day:

   ```
   date,close,total_return_index
   2021-07-19,17.03,100.00
   2021-07-20,17.41,102.23
   ```

   - `date` must be written YYYY-MM-DD (in Excel: select the column, Format Cells, Custom, type `yyyy-mm-dd`).
   - No extra columns, no title rows, no totals. Leave a cell empty rather than typing "N/A".
   - Save as "CSV (Comma delimited)".
5. **Record where it came from** in `data/raw/manual_prices/SOURCES.md` (one line per file, the table is already
   there): your name, Bloomberg or FactSet, the date you pulled it, and the identifier you used.

### Uploading the files to GitHub (in the browser)

1. Open https://github.com/oshh-star/senate-trades-backtest and go into the folder `data/raw/manual_prices`.
2. Click **Add file**, then **Upload files**.
3. Drag the CSV files (and the updated SOURCES.md) into the page.
4. Under "Commit changes", write a short note (for example "Bloomberg prices for X, ECOM, ATVI"), keep "Commit
   directly to the main branch" selected, and click **Commit changes**.

Then tell Claude: the next run checks every file (columns, dates, the last date against the delisting date) and
reports any problem.

## CRSP through WRDS (whoever gets WRDS access)

CRSP comes first in the hierarchy and covers every US stock, delisted ones included. Settings for the web query:

1. Log in at https://wrds-www.wharton.upenn.edu and choose **Get Data > CRSP > Annual Update > Stock / Security
   Files > Daily Stock File**.
2. **Date range**: start `2015-12-01`, end `2026-08-31`. (If the query form does not go that far, take the latest end
   date it allows and say so: the legacy files may stop at the end of 2024; see step 7.)
3. **Company codes**: choose **TICKER**, then **Upload a plain text file** and upload
   `docs/crsp_tickers_ledger.txt` ({len(TICKERS_LEDGER.read_text().split())} tickers, the ledger only). If WRDS
   accepts a bigger request, use `docs/crsp_tickers_all.txt` ({len(TICKERS_ALL.read_text().split())} tickers, every
   stock any trade uses) instead: CRSP then replaces Yahoo for all of them.
4. **Variables**: tick **TICKER** (Ticker Symbol), **COMNAM** (Company Name), **PRC** (Price or Bid/Ask Average),
   **RET** (Returns) and **DLRET** (Delisting Return). PERMNO and the date are always included.
5. **Output**: format **comma-delimited text (.csv)**; date format **YYYY-MM-DD** or **YYYYMMDD** (both work);
   no compression, or unzip it afterwards.
6. Click **Submit Query**, download the file, rename it `crsp_daily.csv`, and upload it to `data/raw/crsp/` the same
   way as above (Add file, Upload files, Commit changes).
7. If WRDS only offers the newer **CRSP Stock Version 2** files, use **Daily Stock File (v2)** with the same dates and
   ticker file, and the variables **PERMNO, DlyCalDt, Ticker, IssuerNm, DlyPrc, DlyRet** (the loader accepts these
   names; v2's DlyRet already includes the delisting return).

The loader (src/prices/crsp.py) matches CRSP's PERMNO (the security) to our symbols by ticker AND date, because
tickers are reused; any doubtful match is listed in data/interim/crsp_permno_map.csv and can be fixed by hand in
config/crsp_permnos.yaml.

## The list

Sorted by the headline's midpoint purchase dollars (the 5-year window with its 12-month warm-up), then by the
dollars in any variant (V6 family owners, V11, V12 with its 2016 warm-up, V16 all ETFs). "First date needed" is the
earliest entry date minus 5 trading days; "last date needed" is the delisting date (last SEC Form 25) for a company
that was acquired, went bankrupt or was liquidated, otherwise 2026-08-31. Dollars count purchases at the midpoint of
the disclosed range, in every period (they are trade sizes, not results).

### MUST-HAVE ({n_must} rows, {must['headline_purchase_dollars'].sum() / tot:.1%} of headline dollars)

{fmt_rows(must)}

### Everything else ({len(x) - n_must} rows)

{fmt_rows(x.iloc[n_must:])}
"""
    OUT.write_text(T)
    x.to_csv("data/interim/price_request.csv", index=False)
    print(f"{OUT}: {len(x)} symbols, {n_must} MUST-HAVE covering {must['headline_purchase_dollars'].sum() / tot:.1%} "
          f"of ${tot:,.0f}; {TICKERS_LEDGER} and {TICKERS_ALL} written")


if __name__ == "__main__":
    main()
