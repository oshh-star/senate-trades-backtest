# CLAUDE.md: Senate trades backtest (LBS CA01)

## Project summary
LBS CA01 Investment Fundamentals group project, due **Monday 19 October 2026, 23:59**.
We backtest a "copy the US Senate" strategy. When a senator's stock trade is publicly disclosed
on the Senate eFD site (efdsearch.senate.gov), we copy it: buy when a purchase is disclosed, sell
when that same senator discloses a sale. The professor marks the **quality of the argument**,
not whether the strategy makes money (docs/CA01AUT26_GroupProject_Guidance.pdf). The rules must be
precise enough to reproduce, every performance number needs a benchmark over identical dates, and
one command (`python run_all.py`) must rebuild every number.

## Where the spec lives
- **config/config.yaml** holds every locked parameter (the single source of truth for code).
- **docs/DECISIONS.md** holds the dated reason for every decision, every change and every variant run.
- **docs/HANDOVER.md** holds the current state, the exact next step and the open questions.

### Locked spec in brief (details and reasons in DECISIONS.md)
- **Data**: scrape Senate eFD PTRs directly (never the frozen senate-stock-watcher-data repo).
  PTRs received 2016-01-01 to 2026-09-30, ALL filer types (1 Senator, 4 Candidate, 5 Former Senator),
  with the date AND time received. **Scope (A05)**: a transaction is in scope if and only if its
  transaction date falls within that person's Senate service (unitedstates/congress-legislators
  dates, data/interim/senate_terms.csv); the eFD filer-type label is today's status and is not used.
  Paper filings are logged (senator, date, link) and excluded. Amendments (J3): every record enters
  the book AS FIRST PUBLISHED at its own datetime; a later correction reverses it and acts on the
  corrected record at the amendment's datetime ("as revised" is variant V14). Raw downloads are cached in data/raw/ and committed.
- **Analysis window (A06)**: ends 2026-08-31 (Ken French data ends there). `analysis.window_years`
  (default 5, i.e. disclosures 2021-09-01 to 2026-08-31, 60 months; 3 and 10 are a one-line change).
- **Universe**: US common stocks **and US-listed EQUITY ETFs** (K5: every ETF is classed equity,
  fixed_income, commodity or other from Yahoo's fund category; `universe.etf_classes: [equity]`; V16 keeps
  all). Every trade is flagged `is_etf`; `universe.include_etfs: false` is the ETF-excluded variant (V5).
  Options, bonds, crypto and mutual funds are excluded.
- **Owners**: `universe.owners: [Self, Joint]`. Spouse and Child trades stay in the raw cache and
  are counted by owner type in the exclusions log; adding them is a one-line variant.
- **Sizing**: midpoint of the disclosed range (open top band uses its lower bound). Variants:
  lower_bound, equal_dollar.
- **Prices**: adjusted close on the first trading day AFTER the disclosure (date received).
  Variant: same-day close. **Source hierarchy (M2)**: `prices.sources: [crsp, manual, yahoo]`, CRSP first, then a
  Bloomberg/FactSet export (data/raw/manual_prices/, docs/PRICE_REQUEST.md), then Yahoo, merged day by day; V18 = Yahoo
  only. V15 (SPY fill) is a bound, never the headline. OOS stays locked until the price hole is filled (M3).
- **Matching**: a sale is matched FIFO to that senator's open copied positions in the same ticker,
  regardless of owner. Sale (Full) closes it; Sale (Partial) sells the midpoint amount, capped at
  the holding. Sales of anything we do not hold (for example, bought before the window) are ignored
  and logged. No shorting. Exchanges are ignored and logged. Open positions are marked at the last price.
  A series that ends early closes the lot at its last price (E20, K1). Symbols with no usable prices
  (the survivorship ledger, data/interim/survivorship_ledger.csv, with a reason for each) are logged and
  skipped until CRSP arrives (K3); V15 fills their purchases with SPY.
- **Senator vs copier**: every trade's return is also measured from the transaction date. The gap
  between the two is a core result.
- **Warm-up (L2)**: the book is built from disclosures in the 12 months before the window (`engine.warmup_months: 12`);
  returns are measured from the window's first day. The empty start is variant V17.
- **Portfolio**: calendar-time, daily; dollar-weighted average return of open positions (equal-weight
  rebalanced at each filing date is a variant); idle days earn the risk-free rate. USD total returns.
  Ken French US RF. Sharpe ratios and regressions on monthly returns. Event study at 5, 21, 63, 126
  and 252 trading days.
- **Benchmarks** (Phase 5): SPY; SPY scaled to strategy volatility; equal-weighted universe;
  FF3 plus momentum (US); NANC and KRUZ from February 2023.
- **Out-of-sample firewall**: the window splits at its midpoint in whole months (5y: in-sample to
  2024-02-29, out-of-sample from 2024-03-01). Code refuses to compute
  out-of-sample results unless `oos.oos_unlocked: true` AND `project.frozen_rules_commit` is set,
  and flipping them requires a DECISIONS.md entry naming the frozen commit.

## Repo map
```
run_all.py            one command: scrape > clean > prices > engine > metrics > report (--skip-<stage>, --only)
config/config.yaml    locked parameters
src/config.py         config loader, analysis window, sample split, OOS firewall guard
src/scrape/efd.py     eFD client (terms agreement, search, PTR fetch, retries) and HTML parsers
src/scrape/           Phase 1: legislators.py (service dates), listing.py, download.py (manifest),
                      parse.py (transactions_raw + validation), names.py, summary.py;
                      run by hand in chunks with: python -m src.scrape --years 2024 --steps listing download
src/clean/             Phase 2: amendments.py (link, classify, de-duplicate), tickers.py (normalise,
                      recover from names via SEC), yahoo.py (instrument type/exchange, cached),
                      build.py (waterfall, flags), report.py (outputs, data_quality.md section)
src/prices/           Phase 3: resolve.py (renames via SEC company histories, survivorship ledger), yahoo_prices.py
                      (download, parse), repairs.py (K6), french.py (factors), checks.py (sanity checks);
                      5A.2 (M2): crsp.py (WRDS export), manual.py (terminal exports), sources.py (hierarchy merge,
                      overlap validation, dates needed)
src/clean/etf_class.py  K5: ETF asset class from Yahoo's fund category (cached in data/raw/yahoo_fund/)
src/engine/           Phase 4: events.py (entry dates, sizing, ordering, variant filters), book.py (FIFO lots,
                      J3 reversals, series ending early), portfolio.py (series A and B), panel.py (event
                      study panel), diagnostics.py (data_quality.md section, chart, worked examples)
                      warmup.py (L2 before/after against V17, L3 ledger exposure)
src/metrics/          Phase 5: stats.py (returns, Sharpe, CAPM/Carhart with OLS and Newey-West t, drawdown, turnover),
                      benchmarks.py (SPY, risk-matched SPY, Senate universe, NANC, KRUZ as GOP, sterling),
                      event_study.py (clustered by entry month); outputs/tables/phase5_*.md, outputs/figures/phase5_*.png
src/quality.py        each phase rewrites only its own section of outputs/data_quality.md
config/name_overrides.yaml   hand-checked eFD filer name -> bioguide_id
config/asset_name_overrides.yaml   hand-written asset name -> ticker (J5), confirmed against Yahoo
config/ticker_renames.yaml   renames (FB -> META, SQ -> XYZ), same-symbol name changes, hand-rejected cases,
                      hand non-US listings (BRK CDR, COLPAL), hand recycled symbols (USG)
config/ledger_reasons.yaml   K4: why each survivorship-ledger symbol has no prices, with a one-line source
config/price_repairs.yaml    K6: repairs to bad Yahoo prints (logged in data/interim/price_repairs_log.csv)
config/etf_class_overrides.yaml   K5: hand ETF classes (HIYS)
src/{scrape,clean,prices,engine,metrics,report}/   one package per stage, each exposes run(cfg)
data/raw/             cached raw downloads (committed); data/raw/_dryrun/ holds Phase 0 test output
data/raw/efd/         search/<year>/*.json listings, ptr/<year>/<ptr_id>.html.gz pages, download_failures.json
data/raw/legislators/ congress-legislators YAML (Senate service dates)
data/raw/crsp/        CRSP daily CSV goes here once WRDS access is approved
data/raw/yahoo_meta/  Yahoo instrument metadata per ticker (no prices); data/raw/sec/ SEC company_tickers.json
data/raw/prices/yahoo/  raw Yahoo daily price responses (gzipped JSON, with download date); data/raw/french/ factor zips
data/processed/       trades_clean.csv (one row per trade + variant flags), trade_records.csv (J3 records),
                      tickers.csv, exclusions.csv, prices.csv.gz (not committed: rebuilt by the prices stage),
                      dividends.csv, splits.csv, trading_calendar.csv, factors_daily.csv, factors_monthly.csv,
                      lots.csv, daily_book.csv, event_panel.csv, engine_events.csv, engine_metadata.json (Phase 4),
                      ledger_exposure.csv, monthly_returns.csv, daily_returns.csv, universe_members.csv,
                      metrics_insample.json (Phase 5)
data/interim/, data/processed/   derived data, rebuilt by run_all.py
outputs/tables/, outputs/figures/, outputs/data_quality.md   report outputs
outputs/phase1_summary.md   Phase 1 first-look counts (no prices or returns)
outputs/phase4_worked_examples.md   three copied lots traced step by step (Phase 4)
docs/                 DECISIONS.md, HANDOVER.md, the course guidance PDF
scripts/install_pkgs.sh   SessionStart hook: pip install in cloud sessions
scripts/phase0_checks.py  environment checks (connectivity, eFD, counts, prices, factors)
scripts/ledger_evidence.py  SEC delisting evidence for the ledger (K4), by hand; cached in data/raw/sec/filings/
scripts/price_request.py  writes docs/PRICE_REQUEST.md and docs/crsp_tickers_*.txt (M2), by hand after the prices stage
data/raw/manual_prices/  Bloomberg/FactSet CSVs (date, close, total_return_index) and SOURCES.md (who, where, when)
tests/                pytest suite (run: python -m pytest)
```

## Phase plan
| Phase | Work | Status |
|---|---|---|
| 0 | Set-up and environment checks | Done (2026-09-27) |
| 1 | Scrape eFD PTRs 2016-01-01 to 2026-09-30 into data/raw/ (resumable), parse, match names | Done (2026-09-27); re-run once after 30 Sep to finalise the 2026 listing |
| 2 | Clean: amendments, de-duplication, scope filters, tickers, instrument types, flags, exclusions log | Done (2026-09-27); FIFO sale matching moved to Phase 4 (E18) |
| 3 | Prices (Yahoo, or CRSP CSV) and Ken French factors | Done (2026-09-28); CRSP pending WRDS access |
| 4 | Engine: trade-level and calendar-time portfolio returns | Done (2026-09-28), in-sample only |
| 5 | Metrics and benchmarks | Part A done (2026-09-29), in-sample only: warm-up (L2), metrics, benchmarks, event study. A.2 done (2026-09-29): price-source hierarchy (M2), loaders, price request; **waiting on terminal/CRSP prices** |
| 6 | Robustness and mechanism tests (variants, OOS) | Not started |
| 7 | Report outputs (tables, figures, data_quality.md) | Not started |

## RULES FOR EVERY SESSION
1. At the start of every session, read CLAUDE.md, docs/HANDOVER.md and docs/DECISIONS.md before
   doing anything.
2. Never change a locked parameter without a DECISIONS.md entry (date, who, what, why).
3. Log every variant ever run in DECISIONS.md. The professor asks how many variants were tried.
4. Commit and push after every meaningful step. The cloud machine can be reclaimed at any time and
   uncommitted work is lost.
5. Long jobs must be resumable and checkpoint to disk.
6. Relative paths only. Everything runs from the repo root with: `python run_all.py`
7. Every data exclusion is counted and explained in outputs/data_quality.md.
8. No look-ahead: every input is keyed to the date it became public.
9. Respect the out-of-sample firewall.
10. Scraping etiquette: at most 1 request per second, a descriptive User-Agent. SEC requests need a
    contact email in the User-Agent; it is a placeholder in config (`scrape.contact_email`), so ask
    the user for it when needed.
11. The user is non-technical: plain English, exact clicks.
12. End every session by updating docs/HANDOVER.md, committing, pushing and opening a pull request.
