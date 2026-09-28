# Handover

## Current state
_Last updated: 2026-09-27, end of Phase 2 (Claude, for Harry)._

- **Phase 2 (clean) is done.** Run it with `python run_all.py --only clean` (about 10 seconds, fully
  offline from the caches in data/raw/). Tests: `python -m pytest` (95 pass). No prices, returns or
  performance numbers exist anywhere yet.
- **Decisions**: H1 (Jim Banks = B001299, override added), H2 (E03-E08 confirmed), H3 (headline unchanged;
  V1-V12 pre-registered at commit 622a455, logged in commit 184009a), H4 (SEC contact email). Engineering
  interpretations **E09-E18 need Harry's confirmation** (DECISIONS.md).
- **Headline sample: 2,502 in-scope trades** (1,514 purchases, 988 sales; 284 ETF trades) from 31
  senators, disclosed 2021-09-01 to 2026-08-31. Waterfall from the 14,558 raw rows, amendments,
  tickers, concentration, filing lags and variant counts: outputs/data_quality.md, "Phase 2".
- **Outputs**: data/processed/trades_clean.csv (8,380 rows: every trade in the 3/5/10-year windows that
  passes every filter except window and owner; `in_scope` marks the headline sample; flags for V1-V6 and V9),
  data/processed/tickers.csv (1,522 tickers checked with Yahoo), data/processed/exclusions.csv (every raw
  row that is not an in-scope trade, with a reason code). Audit files in data/interim/: amendments.csv,
  amendment_corrections.csv, ticker_recovery.csv, amount_strings.csv.
- **Amendments**: 155 electronic amendments: 97 full restatements, 4 additive, 40 AMBIGUOUS (2 received in
  the default window), 14 unlinked (all amend pre-2016 reports). 2,182 duplicate rows removed. No in-scope
  trade exists only in an amendment; 32 in-scope trades carry an amendment's correction (original datetime kept).
- **Concentration**: Tuberville 29.1% of trades, Alan Armstrong 27.9% (one PTR of 698 trades, filed
  2026-07-21, median lag 113 days: his onboarding portfolio), Boozman 15.5%, Mullin 12.9%, Whitehouse 3.2%.
  Top 5 = 88.7% of trades.
- **Caches added**: data/raw/sec/company_tickers.json; data/raw/yahoo_meta/ (1,560 symbols, descriptive
  fields only, no prices).

## Exact next step
1. **Harry**: confirm E09-E18, and decide the 2 in-window AMBIGUOUS amendments (Capito 2022-01-21,
   Sullivan 2023-07-26; see Open questions 1).
2. **On or after 1 October 2026**: run `python run_all.py --only scrape clean` once to finalise the 2026
   listing, and commit. (It cannot change the default window, which ends 2026-08-31.)
3. **Phase 3: prices.** For every ticker in data/processed/tickers.csv with an in-scope or variant trade:
   resolve the 206 `instrument_unresolved` tickers (renames such as FB -> META, delistings), then download
   adjusted daily closes (yfinance; CRSP CSV when WRDS is approved) and Ken French daily and monthly factors
   (3 factors + momentum, US RF) to 2026-08-31. Also the benchmarks' prices (SPY, NANC, KRUZ).
4. **Phase 4** starts with FIFO sale matching (moved from Phase 2, E18).

## Open questions
1. **AMBIGUOUS amendments (40; 2 in the default window).** These repeat some but not all trades of the report
   they amend. Rule applied for now: keep every version's trades once (nothing deleted); trades flagged
   `amendment_ambiguous` (18 in scope). In the window: Capito 2022-01-21 (repeats 4 of 5 trades; 1 not
   repeated) and Sullivan 2023-07-26 (repeats 17 of 41; the 24 not repeated are Child trades, 3 copies of the
   same 8 purchases). Harry: keep (current rule) or treat missing lines as withdrawn?
2. **Tickers not recovered** (47 Self/Joint trades in the default window; list in data_quality.md section 4):
   mostly private placements, T-bills and structured notes (correctly out), plus some ADRs whose ticker is
   in the name but Yahoo no longer knows it or names it differently (WIZEY, GSK "Glaxo Wellcome", MURGY,
   HOLX, BK, PSTG). Phase 3 can revisit these with price histories.
3. **Recycled symbols.** 206 tickers are `instrument_unresolved` (Yahoo does not know them, or Yahoo's
   current name shares no word with the eFD name; e.g. FB is now a ProShares ETF). 104 in-scope trades.
   Phase 3 must map them (renames) or mark them delisted.
4. **OTC names are kept** (`is_otc`: 303 tickers, 309 in-scope trades, mostly foreign ADRs). Harry: keep in
   the headline, or make "exclude OTC" a (new, to be logged) variant?
5. **Alan Armstrong's onboarding PTR** (698 trades, 27.9% of the sample, all filed 113 days after the
   trades on median). It is excluded by V3 (first 180 days) and V4 (bulk PTR). Worth a sentence in the report.
6. **WRDS access requested 27 Sep 2026, awaiting approval** (A04).
7. **Stooq and theunitedstates.io are unreachable** from the cloud; not needed on the current plan.
8. **Timing.** The listing's report title date can be one day later than the date received (UTC); we key on
   the date received and the time from the PTR page (E05).

## How to hand over
- **Finishing a session:** update this file (Current state, Exact next step, Open questions), update the
  phase status table in CLAUDE.md, commit, push and open a pull request.
- **Starting a session:** read CLAUDE.md, then this file, then docs/DECISIONS.md, before doing anything.
- **Changing a rule:** add a DECISIONS.md entry first (date, who, what, why). **Running a variant:** log it
  in the "Variants run" table.
- Never flip `oos.oos_unlocked` without a DECISIONS.md entry that names the frozen commit hash.

## Teammate set-up
To work on this project with Claude Code on the web (claude.ai/code), set up a cloud environment
exactly like this:

1. Go to **claude.ai/code** and open the environment menu (the cloud environment name in the session's
   title bar), then choose **Add environment** (or **Edit** on an existing one).
2. **Network access:** choose **Custom**.
3. **Allowed domains:** enter exactly these, one per line:
   ```
   efdsearch.senate.gov
   raw.githubusercontent.com
   *.yahoo.com
   stooq.com
   *.stooq.com
   mba.tuck.dartmouth.edu
   www.sec.gov
   data.sec.gov
   fred.stlouisfed.org
   theunitedstates.io
   ```
4. Tick **"Also include default list of common package managers"**. Without this, Python packages
   cannot be installed.
5. **Environment variables:** add these two lines:
   ```
   BASH_DEFAULT_TIMEOUT_MS=600000
   BASH_MAX_TIMEOUT_MS=1800000
   ```
6. Save, then start a session on the repository `oshh-star/senate-trades-backtest`. The SessionStart
   hook (`scripts/install_pkgs.sh`) installs `requirements.txt` automatically in cloud sessions.
7. Your first message to Claude in any session: *"Read CLAUDE.md, docs/HANDOVER.md and
   docs/DECISIONS.md, then continue with the exact next step."*
