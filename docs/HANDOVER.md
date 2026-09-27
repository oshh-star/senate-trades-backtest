# Handover

_Last updated: 2026-09-27, end of Phase 0 (Claude, for Harry)._

## Current state
- **Phase 0 (set-up and environment checks) is done.** The repo structure, locked config, stage stubs,
  eFD client, tests and docs are in place. `python run_all.py` runs end to end, but every stage is
  still a stub that prints "not implemented yet".
- Environment checks (full output in data/raw/_dryrun/):
  - **eFD works.** The terms agreement, search and PTR parsing all work. September 2025 had 12 PTRs
    from senators (10 electronic, 2 paper).
  - PTR search counts by year are in data/raw/_dryrun/ptr_counts_by_year.md: 1,869 PTRs received
    from 2016-01-01 to 2026-09-27 (Senator plus Former Senator). Estimated full scrape time is about
    35 to 50 minutes at 1 request per second.
  - **Prices: Yahoo works** (chart API, called directly). **Stooq is unreachable** (connection reset).
  - **Ken French factors work.** The daily files currently end on **2026-08-31**.
  - **PyPI is blocked** by the cloud network settings, so pandas, yfinance and similar cannot be
    installed yet. The Phase 0 code uses only what is already installed (requests, PyYAML).
- The pytest suite (9 tests) passed using a stand-in runner, because pytest itself could not be installed.

## Exact next step
**Phase 1: scrape.** Build `src/scrape/run()`:
1. For each calendar year from 2016 to 2026 (received dates, cutoff 2026-09-30), page through the
   search for filer types 1, 4 and 5 (100 rows per page) and save each page's JSON to
   `data/raw/efd/search/`.
2. Fetch every electronic PTR and every amendment into `data/raw/efd/ptr/<report_id>.html`. Skip
   files that already exist, so the job is resumable and checkpoints naturally.
3. Write a manifest CSV (one row per filing: filer, filer type, office, date received, kind, link)
   and an exclusions log covering paper filings, candidate filings and replaced amendments.
4. Commit the raw cache in batches as it downloads.

**Before starting Phase 1**, the network setting must allow PyPI (see Open questions, item 1).
Otherwise later phases cannot use pandas.

## Open questions
1. **PyPI blocked.** In the environment's network settings, tick "Also include default list of
   common package managers" (see Teammate set-up below). Until then no Python packages can be installed.
2. **WRDS access requested 27 Sep 2026, awaiting approval.** When it is approved, a teammate will
   download CRSP daily stock data as a CSV from the WRDS website and add it to `data/raw/crsp/`.
   The Phase 3 prices stage must accept either source via `prices.price_source: yahoo | crsp` in
   config, so CRSP can be swapped in as a robustness check without rewriting anything
   (DECISIONS.md A04).
3. **Confirm the filer-type interpretation (DECISIONS.md E01).** eFD labels people by their
   *current* status, so "sitting Senators" is implemented as filer types Senator plus Former Senator,
   which means senators at the time they filed. Harry to confirm.
4. **SEC contact email.** `scrape.contact_email` in config is a placeholder. It is needed before any
   request to www.sec.gov (which currently returns 403 without it). Probably needed in Phase 2 or 3
   for the ticker/CIK list.
5. **September 2026 factor data.** Ken French's files end on 2026-08-31. September 2026 will probably
   not be published before the 19 October deadline. To decide in Phase 3: either end monthly
   regressions and Sharpe ratios at 2026-08-31, or proxy September's risk-free rate. This needs a
   DECISIONS.md entry either way.
6. **Stooq and theunitedstates.io are unreachable** from the cloud (the connection is reset), and
   FRED's data download fails. None is needed on the current plan: Yahoo is the price source, eFD
   itself identifies senators, and Ken French provides the risk-free rate.
7. **Timing detail to keep in mind.** The listing's report title date can be one day later than the
   date received (Rick Scott: received 09/18/2025, filed 9:09 PM, listed "for 09/19/2025"). We key
   on the **date received** column. The entry rule (first trading day after that date) already
   handles filings made after the close.
8. **ETF flag (Phase 2).** eFD's "Asset Type" does not reliably separate ETFs from stocks. Plan: flag
   `is_etf` from Yahoo's `instrumentType` field (it returns "ETF" for SPY).

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
