# Handover

## Out-of-sample: OPEN (rules frozen 2026-10-06). Read this first.
- **Frozen**: rules frozen at `348318447daa58a91af14ae65c8ee3c98522d896` (F1), unlocked in a separate commit (U1).
  From now on NO rule, parameter, scope, test or prediction may change. A bug is fixed and logged in DECISIONS.md,
  "Post-unlock corrections", with before and after values (none so far: C0 changed a test only).
- **Main result (S5)**: ONE continuous 5-year backtest, 2021-09-01 to 2026-08-31, with the 12-month warm-up
  (outputs/tables/phase5_full_results.md). Series A 10.81% a year (volatility 22.37%, Sharpe 0.41) against SPY 12.69%
  (Sharpe 0.61); CAPM alpha -1.48% (t -0.29), Carhart -0.74% (t -0.14), beta 1.21; maximum drawdown -32.15%
  (2022-03-29 to 2022-11-03, recovered 2025-06-09); excess over risk-matched SPY -4.48% a year, so no break-even cost.
  Series B (fixed pot) 8.78%, Sharpe 0.69. Senate universe 13.21%; NANC 24.75% and KRUZ 19.31% over their 42 months.
- **Second half** (2024-03 to 2026-08, read off the same run; phase5_oos_results.md): series A 22.95% against SPY
  19.32% and risk-matched SPY 26.03%; CAPM alpha +1.66% (t 0.24).
- **Confirmatory tests** (outputs/tables/confirmatory_oos.md; verdicts on Holm-adjusted p):
  - H0 (alphas): not distinguishable from zero, as predicted (CAPM +1.66%, Holm p 1; Carhart +0.35%).
    No effect larger than about ±16% (CAPM) or ±19% (Carhart) a year at the Bonferroni level.
  - H1 purchases: **-3.20%, t -2.94, Holm p 0.02: significantly NEGATIVE**. That breaks "close to zero", in the
    opposite direction to informed buying (the stocks lagged SPY before disclosure). H1 sales: -0.95%, not significant.
  - H2: **+1.75%, t 3.57, Holm p 0.001: positive**. Reversal check: not reversed at 126 days (+1.99%) or 252 days (+12.70%).
  - H3 (committee): +6.01%, not distinguishable from zero, as predicted ("it disappears").
  - H4 (size): +5.39%, not distinguishable from zero (informed trading would make it negative).
  - **Both significant results rest on ONE filing**: Alan Armstrong's PTR disclosed 2026-07-21, 654 purchases of 621
    stocks bought 27-31 March 2026, 67% of the half's purchases, all in one entry-month cluster. Without bulk filings
    (R2), H1 purchases is -0.05% (t -0.08) and H2 +1.09% (t 0.80). A clustered standard error with one cluster
    holding two-thirds of the events is fragile: the report should say so.
- **Exploratory** (every table labelled, with the 150-cells note): 78 cells reach |t| = 2 across the full-window and
  second-half event studies, drift, mechanism and committee tables. Most purchase cells are the same Armstrong filing
  (purchases filed after 30 days, Republican, small bands). Variants: every one ran over the full window and its own second half (outputs/tables/variants_full_yahoo.md;
  V11 ran for the first time; V20 not run: no CRSP data). Full window: series A from 6.41% (V3, no first 180 days) to
  25.80% (V11, a different 3-year window); no variant's alpha reaches |t| = 2. Leaving out Tuberville adds 2.51 points;
  leaving out Mullin adds 5.13. Second half: V12's own second half has a Carhart alpha of -6.27% (t -2.11), exploratory.

## Current state
_Last updated: 2026-10-06, Phase 5B: decisions S1-S5, freeze (F1), unlock (U1), full backtest, second half,
confirmatory and exploratory tables, variants (Claude, for Harry)._

- **Commits**: Step 0 (S1-S5) `49b1edc`; pre-freeze reporting code `3483184` (= the frozen commit, E58); freeze `be7c260`;
  unlock `bc6d2b4`; full run `74a45a3`.
- **No look-ahead check passed**: the full run's in-sample half reproduces the in-sample run exactly (series A, SPY and
  the Senate universe identical to the bit over all 627 in-sample days; H0-H4 in-sample values identical).
- **Prices**: Yahoo only, final (R3, S2); headline `prices.sources: [yahoo]` (S3). V20 (CRSP fills the ledger) is
  registered and reported as "not run: no CRSP data".
- **In-sample files** (`*_insample*`, phase5_event_study.md, phase5_predisclosure_drift.md) are the pre-unlock design
  record; the full-window run does not overwrite them (E58 d).
- **Series B caveat**: its pot is sized on the whole window's peak cash, so it was mostly cash in 2022 (maximum drawdown
  only -7.09%, in 2026). Report series A as the headline, as before.
- Tests: `python -m pytest` (183 pass). `python run_all.py --skip-scrape` about 2.5 minutes; `python run_variants.py`
  about 8 minutes.

## Exact next step
1. **Harry**: review the results above and the confirmatory table; decide how the report frames the one-filing
   dominance of H1 and H2 (the registered tests stand as computed; the ex-bulk values sit beside them, R2).
2. **Phase 7: the report.** The main result is the full window (S5); the file map is in README.md, "Which file feeds
   each table and figure".
3. **Phase 7: submission (S4)**: update scripts/make_submission.py to build two zips (code plus small data; the Yahoo
   price cache), then rerun the clean-room test on the final commit.
4. **If WRDS access arrives before submission**: build V20's price file and run V20 only. It cannot change the headline
   (S3).

## Known limitations
- **K7: spin-offs in renamed tickers.** UTX -> RTX (Carrier and Otis spun off in April 2020) and DWDP -> DD (Dow in
  April 2019, Corteva in June 2019): a lot held across a spin-off date is priced with RTX's or DD's history, which may
  not credit the spun-off shares. Both dates are before the 5-year window, so only the 10-year variant (V12) is
  affected. Not fixed.
- **Survivorship ledger is large in-sample** (L3): up to 69% of capital deployed at cost. No CRSP or terminal prices
  arrived (R3), so this is a stated limitation, with V15 as its bound. The Senate-universe benchmark also leaves these symbols out (15 symbols, 181 symbol-months).
- **V12 with V14**: trades_clean.csv (the "as revised" input) still starts at 2016-09-01, so that combination has no
  2016 warm-up (E44).
- **Yahoo drops delisted names entirely**, so E20 (series ending early) almost never fires (LBRDA only); the
  survivorship problem sits in the ledger instead, which is why V15 and CRSP matter.
- **One filing dominates the second half's purchases**: Armstrong's PTR of 2026-07-21 (654 purchases, one entry month).
  Equal-weighted event statistics in the second half are largely that one basket; clustered t-statistics with one
  cluster holding two-thirds of the events overstate precision. The ex-bulk values (R2) are the check.
- **Short samples**: 30 months in-sample (12 for NANC/KRUZ); minimum detectable alphas of 10-16% a year for series A and
  B mean the in-sample regressions cannot distinguish a zero alpha from a large one.
- Preferred shares (AHL-C, BKEPP) passed Yahoo's EQUITY classification in Phase 2; both are in the ledger and skipped.

## Pre-submission checklist (before Monday 19 October 2026, 23:59)
- [x] 2026 listing finalised (2026-10-02).
- [x] Price request closed by R3 (Yahoo only); headline fixed to Yahoo (S3).
- [x] Rules frozen (F1) and out-of-sample unlocked (U1); full backtest and second half run (2026-10-06).
- [x] Every variant run logged in DECISIONS.md "Variants run".
- [x] H0-H4 reported as the only confirmatory tests; every other table labelled EXPLORATORY with the 150-cells note.
- [ ] The report (Phase 7): the full window as the main result, the second half as the check, H0-H4 with the
      Armstrong caveat, the survivorship limitation with V15 as its bound.
- [ ] Two submission zips (S4), built from the final commit; clean-room rebuild and `sha256sum -c` on the final commit.

## Open questions
1. **How to frame H1 and H2** (one filing, one entry-month cluster, 67% of the half's purchases). The tests stand as
   registered; the report's wording is Harry's call.
2. **Ledger symbols marked "unknown"**: AHL-C (out of the headline as a preferred), and variant-only AQFH, CEM, HYH,
   TWO, HIYS.
3. **WRDS access requested 27 Sep 2026, still awaiting approval** (A04). Only V20 would use it (S3).
4. **Timing.** The listing's report title date can be one day later than the date received (UTC); we key on
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
