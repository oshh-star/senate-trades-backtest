# Copying the US Senate: a backtest

LBS CA01 Investment Fundamentals, Autumn 2026, group project.

## The project in three sentences
US senators must disclose their stock trades publicly, usually weeks after they trade, and we test whether an investor
who copies each trade as soon as it becomes public (buying on a disclosed purchase, selling when the same senator
discloses a sale) beats simple alternatives over identical dates: SPY, SPY scaled to the same volatility, the
equal-weighted universe of stocks senators bought, the Fama-French-Carhart factors, and the NANC and KRUZ ETFs that sell
this exact idea. We also measure what the senators themselves earned from the transaction date, so the gap shows how
much any edge is lost to the disclosure delay. The rules were fixed on the first half of the window (September 2021 to
February 2024), and the tests for the second half were registered before any second-half number existed
(`docs/DECISIONS.md`, "Out-of-sample test plan").

## Install (once)
You need **Python 3.11** (tested on 3.11.15) and about 1 GB of disk space (the packages take about 560 MB). No internet connection is needed after the
packages are installed: every raw download is included.

```bash
cd senate-trades-backtest
python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Rebuild every number: one command
From the folder that contains this README:

```bash
python run_all.py --skip-scrape
```

This takes about **2.5 minutes** (153 seconds in our clean-room test). It works offline. On Windows it switches
itself into Python's UTF-8 mode, because the tables contain characters such as Δ and ±. It
reads the raw data in `data/raw/` and rebuilds every table in `outputs/tables/`, every figure in `outputs/figures/`, the
data-quality log `outputs/data_quality.md` and the derived data in `data/processed/`. No file path needs editing:
everything runs relative to this folder.

The robustness variants (V1 to V19, each run alone against the headline) are a second command, run after the first:

```bash
python run_variants.py             # about 4 minutes; writes outputs/tables/variants_insample_prefill.*
```

**Checking the rebuild.** If you unpacked `submission.zip`, compare the rebuilt files with the submitted ones:

```bash
sha256sum -c CHECKSUMS.sha256 --quiet          # on a Mac: shasum -a 256 -c CHECKSUMS.sha256 --quiet
```

No output means every file is identical (Windows: run it in Git Bash). From a git clone, `git status` should show no
changes instead. Our clean-room test (a fresh clone, a fresh virtual environment, the network switched off) reproduced
every committed output byte for byte on Linux with Python 3.11.15. On macOS or Windows the numbers should agree to every
digit shown in the tables, but the check can still report differences that are not differences in the results: the
last digit of a long decimal in a CSV (different maths libraries), the bytes of the PNG figures (font rendering), and,
on Windows, every text file (Windows ends lines with CR LF).

Tests: `python -m pytest` (about 5 seconds; on Windows `python -X utf8 -m pytest`).

## Which file feeds each table and figure in the report
| In the report | File | Built by |
|---|---|---|
| Main results: strategy (series A and B) against every benchmark, identical dates (return, volatility, Sharpe, CAPM and Carhart alphas, drawdown, turnover, break-even cost) | `outputs/tables/phase5_insample_results.md` (and `.csv`) | `src/metrics/` |
| Confirmatory tests H0-H4 (Holm-adjusted p-values, minimum detectable effects, ex-bulk sensitivity, reversal check), calendar-year returns, worst 12 months | `outputs/tables/confirmatory_insample.md` (and `.csv`); `confirmatory_oos.md` once the out-of-sample half is opened | `src/metrics/confirmatory.py` |
| Event study: senator vs copier at 5, 21, 63, 126 and 252 trading days | `outputs/tables/phase5_event_study.md` | `src/metrics/event_study.py` |
| Pre-disclosure drift (what the delay costs a copier) | `outputs/tables/phase5_predisclosure_drift.md` | `src/metrics/event_study.py` |
| Mechanism splits (trade size, party, filing lag, senator) | `outputs/tables/mechanism_insample_prefill.md` | `src/metrics/mechanism.py` |
| Committee test (trades in industries the senator's committee oversees) | `outputs/tables/committee_insample_prefill.md` | `src/metrics/committee.py` |
| Robustness variants V1-V19 | `outputs/tables/variants_insample_prefill.md` | `run_variants.py` |
| Warm-up before/after (the book's first year) | `outputs/tables/phase5_warmup_before_after.csv` | `src/engine/warmup.py` |
| Figure: cumulative value, strategy and benchmarks | `outputs/figures/phase5_cumulative_value.png` | `src/metrics/` |
| Figure: drawdowns | `outputs/figures/phase5_drawdowns.png` | `src/metrics/` |
| Figure: open positions and capital deployed over time | `outputs/figures/phase4_open_lots_capital.png` | `src/engine/diagnostics.py` |
| Three copied trades traced step by step | `outputs/phase4_worked_examples.md` | `src/engine/diagnostics.py` |
| Data appendix: every exclusion counted and explained | `outputs/data_quality.md` | every stage |
| Raw data first look (filings, transactions, owners by year) | `outputs/phase1_summary.md` | `src/scrape/summary.py` |

"prefill" in a file name means the survivorship-ledger stocks (delisted names Yahoo no longer serves) have no prices
and are skipped: no CRSP or terminal price file was available, so every price is Yahoo's. Each table says so in its
header, and variant V15 bounds the effect.

## Where the rules and the reasons are
- `config/config.yaml`: every rule, as a parameter (the single source of truth for the code).
- `docs/DECISIONS.md`: the dated reason for every rule, every change, and every variant ever run.
- `docs/HANDOVER.md`: the current state of the project.
- `CLAUDE.md`: the map of the code and the phase plan.

## Data sources
| Data | Source | Notes |
|---|---|---|
| Senate trades | Senate eFD (efdsearch.senate.gov), Periodic Transaction Reports received 2016-01-01 to 2026-09-30, scraped directly | Keyed to the date and time each report was **received** (made public). In scope only if the transaction date falls within the filer's Senate service (unitedstates/congress-legislators). Paper filings, amendments, owners and every other exclusion are counted in `outputs/data_quality.md`. |
| Prices | Yahoo Finance daily adjusted close (dividends reinvested), USD; hierarchy CRSP, then terminal exports, then Yahoo (`prices.sources`) | Delisted stocks are missing from Yahoo (survivorship bias); they are listed with a reason in `data/interim/survivorship_ledger.csv`. |
| Factors and risk-free rate | Kenneth French Data Library: US Fama-French 3 factors, momentum, RF (daily and monthly) | One risk-free series throughout. |
| Company names, renames, industries | SEC EDGAR (company tickers, submissions, Form 25 delisting filings) | Cached in `data/raw/sec/`. |
| Committee memberships | unitedstates/congress-legislators, every version of the committee membership file | Cached in `data/raw/legislators/`. |

## Re-running the live scrape (optional, needs internet)
Not needed to reproduce the results; the cached downloads are what the results were built from, and the live site can
change. To refresh from the live eFD site:

```bash
python run_all.py                  # full pipeline; the scrape stage fetches only what is not cached yet
python -m src.scrape --years 2026 --refresh-listing    # re-fetch one year's search listing
```

To re-download everything from scratch, move `data/raw/efd/` out of the folder first, then run `python run_all.py`.
The scraper agrees to the site's terms, waits one second between requests and identifies itself; a full re-download of
about 1,900 filings and their search listings takes at least 30 minutes. The SEC asks for a contact email in the User-Agent (`scrape.contact_email`
in `config/config.yaml`). Prices and factors are re-downloaded only for symbols with no cached file (delete a file in
`data/raw/prices/yahoo/` to refresh it); the results would then differ, because Yahoo revises its history.
