# Handover

## Current state
_Last updated: 2026-09-30, end of Phase 6 prep (variants and mechanism, PREFILL) (Claude, for Harry)._

- **Still the critical path: the price request** (docs/PRICE_REQUEST.md, 8 MUST-HAVE stocks = 95.0% of headline
  dollars). Out-of-sample stays locked (M3). **Every Phase 6 prep number is PROVISIONAL ("prefill" in every file name
  and header)**: the survivorship-ledger stocks are still skipped.
- **Decisions**: P1 logged (E50-E51 confirmed; HENOY stays common equity). New interpretations **E52-E54 need
  confirmation** (runner rules, mechanism definitions, committee test inputs).
- **Variant runner**: `python run_variants.py` runs V1-V19 (V2 as five runs), each alone against the headline, and
  writes outputs/tables/variants_insample_prefill.md/.csv/.json. All ran except **V11 (3-year window), refused by the
  firewall**: its in-sample half (2023-09 to 2025-02) lies in the headline's locked period; it runs unchanged once
  out-of-sample is unlocked (engine.sample: full). Every run is logged in DECISIONS.md "Variants run" (commit a124f03),
  including the trial runs and V12's first failed attempt. Headline: series A -0.14%, Sharpe 0.02. The biggest moves:
  V17 empty start +7.71 points, V10 equal weight +3.95, V8 equal dollars +3.57, V6 family +3.33; V18 and V19 equal the
  headline (no terminal prices yet; the preferred shares were never copied); V13 too (both in-sample OTC events were
  sales of nothing held). V12 (2016-09 to 2021-08): 25.83% a year, Sharpe 0.90, CAPM alpha 0.76% (t 0.09).
- **Mechanism splits** (outputs/tables/mechanism_insample_prefill.md, rebuilt by the metrics stage): size, party, filing
  lag, senator. No split difference reaches |t| = 2; t is blank where a group spans fewer than 5 entry months.
- **Committee test** (outputs/tables/committee_insample_prefill.md): mapping committed at a124f03 BEFORE the split (E54);
  membership reconstructed from 206 versions of congress-legislators' committee file (checks passed); SIC codes from
  SEC for 861 of 868 non-ETF events. Overseen purchases: no edge (copier 21d -0.92%, t -0.61). Overseen SALES were
  followed by the stock BEATING SPY (senator 63d +2.92%, t 2.16; difference vs not overseen +3.95%, t 2.25): the wrong
  sign for informed selling, and one of many tests run.
- **Headline unchanged**: series A -0.14% a year, series B 6.06%, SPY 6.43%. `python run_all.py --skip-scrape` rebuilds
  everything (the variants: `python run_variants.py`, about 5 minutes). Tests: `python -m pytest` (170 pass).

## Exact next step
1. **Group**: pull the 8 MUST-HAVE stocks at a library terminal (docs/PRICE_REQUEST.md); upload to
   data/raw/manual_prices/. If WRDS access arrives, run the CRSP query in the same document.
2. **Claude** (when the prices are in): `python run_all.py --skip-scrape`, check the loader reports, then
   `python run_variants.py`: the files are then tagged "filled" instead of "prefill" automatically; log the runs.
3. **Harry**: confirm E52-E54; then freeze the rules (`project.frozen_rules_commit`, a DECISIONS.md entry) and unlock
   out-of-sample (M3). With `engine.sample: full`, `python run_variants.py` also runs V11.
4. **On or after 1 October 2026**: `python run_all.py --only scrape clean` to finalise the 2026 listing (checklist).

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
1. **E52-E54** need confirmation (DECISIONS.md): the runner's firewall rule (V11 not run in-sample), the top-4 senators
   by in-sample events, the 5-cluster minimum for a t-statistic, and the committee test's inputs.
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
