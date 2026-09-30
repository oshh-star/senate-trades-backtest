# Handover

## Current state
_Last updated: 2026-09-30, end of Phase 5A.2b (scope fixes) (Claude, for Harry)._

- **CRITICAL PATH: the price request, now ready to send.** docs/PRICE_REQUEST.md: **8 MUST-HAVE stocks = 95.0% of the
  $2.41m headline dollars at stake** (X, ECOM, ATVI, SSBK, PARA, WBA, GOGL, TOELY), with terminal steps, upload steps
  and the WRDS settings for CRSP. Out-of-sample stays locked (M3) until these prices are in and in-sample is rerun.
- **Decisions**: N1-N3 logged (2026-09-30); E44-E49 confirmed (N1). **V19 "include preferred shares" registered at
  commit a3efd12** (after in-sample results were seen; logged as such). New interpretations **E50-E51 need confirmation**.
- **N2 (preferred shares out)**: QRTEP, AHL-C, BKEPP, NEE-PC, reviewed by hand (config/preferred_shares.yaml). Trades
  moved: 5-year 2 (plus QRTEP out of the warm-up), 3-year 1, 10-year 4. In-scope trades 2,342 -> 2,340. **Series A and B
  unchanged** (none of these was ever copied). HENOY (Henkel preference-share ADR) kept as equity: flagged for Harry.
  Exchange-listed notes CTAA and SOJA are excluded as bonds in every variant (E50).
- **N3 (renames)**: 9 variant-only symbols priced from Yahoo by hand renames (ACE -> CB, IRET -> CSR, WTR -> WTRG,
  CMCSK -> CMCSA, UA-C -> UA, RDS-A and RDSA -> SHEL, MCC -> PFX, ABB -> ABBNY). Survivorship ledger 196 -> 185.
- **Price-source hierarchy (M2)** and loaders are in place (src/prices/crsp.py, manual.py, sources.py); no CRSP or
  terminal file exists yet, so today's headline = V18 (Yahoo only).
- **In-sample headline (unchanged)**: series A -0.14% a year, series B 6.06%, SPY 6.43%
  (outputs/tables/phase5_insample_results.md). `python run_all.py --skip-scrape` reproduces every committed file.
  Tests: `python -m pytest` (164 pass).

## Exact next step
1. **Group**: pull the 8 MUST-HAVE stocks at a library terminal and upload them (docs/PRICE_REQUEST.md, step by step);
   if WRDS access arrives, run the CRSP query in the same document and upload the CSV to data/raw/crsp/.
2. **Claude**: run `python run_all.py --skip-scrape`, check data/interim/manual_prices_report.csv,
   crsp_permno_map.csv and price_source_validation.csv, then rerun the in-sample metrics with the filled prices, and
   log V18 (Yahoo only) as run for the before/after comparison.
3. **Harry**: confirm E50-E51 (and HENOY); then freeze the rules (`project.frozen_rules_commit`, a DECISIONS.md entry) and unlock
   out-of-sample (M3).

## Known limitations
- **K7: spin-offs in renamed tickers.** UTX -> RTX (Carrier and Otis spun off in April 2020) and DWDP -> DD (Dow in
  April 2019, Corteva in June 2019): a lot held across a spin-off date is priced with RTX's or DD's history, which may
  not credit the spun-off shares. Both dates are before the 5-year window, so only the 10-year variant (V12) is
  affected. Not fixed.
- **Survivorship ledger is large in-sample** (L3): up to 69% of capital deployed at cost, until the price request is
  filled. The Senate-universe benchmark also leaves these symbols out (15 symbols, 181 symbol-months).
- **V12 with V14**: trades_clean.csv (the "as revised" input) still starts at 2016-09-01, so that combination has no
  2016 warm-up (E44).
- **Yahoo drops delisted names entirely**, so E20 (series ending early) almost never fires (LBRDA only); the
  survivorship problem sits in the ledger instead, which is why V15 and CRSP matter.
- **Short samples**: 30 months in-sample (12 for NANC/KRUZ); minimum detectable alphas of 10-16% a year for series A and
  B mean the in-sample regressions cannot distinguish a zero alpha from a large one.
- Preferred shares (AHL-C, BKEPP) passed Yahoo's EQUITY classification in Phase 2; both are in the ledger and skipped.

## Pre-submission checklist (before Monday 19 October 2026, 23:59)
- [ ] **On or after 1 October 2026**: run `python run_all.py --only scrape clean` once to finalise the 2026
      listing (PTRs received up to 30 September), then `python run_all.py --only prices engine` and commit.
- [ ] **Price request (M2)**: terminal CSVs for the 8 MUST-HAVE stocks in data/raw/manual_prices/ (docs/PRICE_REQUEST.md);
      CRSP CSV in data/raw/crsp/ if WRDS access arrives. Then rerun in-sample, and only then unlock out-of-sample (M3).
- [ ] Every variant run is logged in DECISIONS.md "Variants run" (the professor asks how many were tried).
- [ ] `python run_all.py` rebuilds every number from the committed caches.

## Open questions
1. **E50-E51** need confirmation (DECISIONS.md), in particular HENOY: the Henkel preference-share ADR is kept as
   common equity (German Vorzugsaktien take full part in profits); say if it should count as preferred under N2.
2. **Who pulls the terminal data, and when?** The 8 MUST-HAVE stocks are 95.0% of the headline dollars.
3. **Ledger symbols marked "unknown"**: AHL-C (now out of the headline as a preferred), and variant-only AQFH, CEM, HYH,
   TWO, HIYS.
4. **WRDS access requested 27 Sep 2026, awaiting approval** (A04). The legacy CRSP files may end in December 2024;
   the loader also reads the v2 format (its column names are from memory: check on first use).
5. **Timing.** The listing's report title date can be one day later than the date received (UTC); we key on
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
