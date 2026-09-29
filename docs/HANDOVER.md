# Handover

## Current state
_Last updated: 2026-09-29, end of Phase 5 part A (Claude, for Harry)._

- **Phase 5A (metrics and benchmarks) is done, IN-SAMPLE ONLY** (2021-09-01 to 2024-02-29; the OOS firewall is shut).
  `python run_all.py --skip-scrape` rebuilds clean, prices, engine and metrics from the caches in about 2.5 minutes and
  reproduces every committed file. Tests: `python -m pytest` (145 pass).
- **Decisions**: L1-L3 logged (2026-09-29); E28-E33 confirmed (L1). **V17 "empty start" registered at commit 8adeaca**
  (after the Phase 4 results were seen; logged as such). New engineering interpretations **E34-E43 need Harry's
  confirmation** (KRUZ priced as GOP; warm-up, ledger, metric, turnover, benchmark and event-study details).
- **Warm-up (L2)**: the book is built from disclosures from 2020-09-01 (135 warm-up events; 65 lots worth $1,196,060 at
  the close of 2021-08-31); returns are measured from 2021-09-01. Sales ignored because nothing was held: 310 -> 265 of
  448. Series B: K = $8,406,633 (warm-up book + $7,210,573 cash). V17 reproduces the Phase 4 files exactly.
  Before/after table: outputs/tables/phase5_warmup_before_after.csv.
- **The warm-up changed the headline a lot**: series A 7.61% a year (Phase 4, empty start) -> **-0.14%**; series B
  7.04% -> 6.06%. The warm-up book (stock bought in 2020-21) was fully invested through the 2022 fall.
- **In-sample results** (outputs/tables/phase5_insample_results.md, 30 months): series A -0.14% a year, volatility 26.4%,
  Sharpe 0.02, CAPM alpha -3.95% (t -0.51), Carhart alpha -1.86% (t -0.24), minimum detectable alpha about 15.6% a
  year; series B 6.06%, Sharpe 0.31; SPY 6.43%, Sharpe 0.27; equal-weight Senate universe 4.05%. NANC and KRUZ over
  their 12 in-sample months: 38.5% and 19.8% against SPY 30.2% and series A 18.3%. Event study:
  outputs/tables/phase5_event_study.md. Figures: outputs/figures/phase5_cumulative_value.png, phase5_drawdowns.png.
- **Ledger exposure (L3)**: skipped ledger purchases still held (at cost) are 2.6% to 68.6% of capital deployed (median
  32.7%); dropping each at its SEC delisting barely changes it (US Steel, ChannelAdvisor, Activision, Paramount and
  Walgreens were still listed in-sample). The headline therefore omits a large, real part of what senators bought.

## Exact next step
1. **Harry**: confirm E34-E43 (DECISIONS.md). Decide whether the ledger exposure (L3, up to 69% of capital) changes
   the plan: CRSP (A04) or V15 (neutral fill) now matters for the headline, not only as a robustness check.
2. **Phase 5 part B / Phase 6** (Harry's next brief): freeze the rules (set `project.frozen_rules_commit`, a
   DECISIONS.md entry), then unlock out-of-sample; run the pre-registered variants V1-V17, each logged in "Variants run".
3. Before V12 (10-year window) can run with the warm-up, extend the clean stage's classification range to the scrape
   start (E35f); the engine refuses until then.

## Known limitations
- **K7: spin-offs in renamed tickers.** UTX -> RTX (Carrier and Otis spun off in April 2020) and DWDP -> DD (Dow in
  April 2019, Corteva in June 2019): a lot held across a spin-off date is priced with RTX's or DD's history, which may
  not credit the spun-off shares. Both dates are before the 5-year window, so only the 10-year variant (V12) is
  affected. Not fixed.
- **Survivorship ledger is large in-sample** (L3): up to 69% of capital deployed at cost. The Senate-universe benchmark
  also leaves these symbols out (15 symbols, 181 symbol-months; outputs/data_quality.md Phase 5 section).
- **Yahoo drops delisted names entirely**, so E20 (series ending early) almost never fires (LBRDA only); the
  survivorship problem sits in the ledger instead, which is why V15 and CRSP matter.
- **Short samples**: 30 months in-sample (12 for NANC/KRUZ); minimum detectable alphas of 10-16% a year for series A and
  B mean the in-sample regressions cannot distinguish a zero alpha from a large one.
- Preferred shares (AHL-C, BKEPP) passed Yahoo's EQUITY classification in Phase 2; both are in the ledger and skipped.

## Pre-submission checklist (before Monday 19 October 2026, 23:59)
- [ ] **On or after 1 October 2026**: run `python run_all.py --only scrape clean` once to finalise the 2026
      listing (PTRs received up to 30 September), then `python run_all.py --only prices engine` and commit.
- [ ] If WRDS access arrives: add the CRSP daily CSV to data/raw/crsp/ and run the CRSP robustness check (A04).
- [ ] Every variant run is logged in DECISIONS.md "Variants run" (the professor asks how many were tried).
- [ ] `python run_all.py` rebuilds every number from the committed caches.

## Open questions
1. **E34-E43** need confirmation (DECISIONS.md), in particular E35(b) (the warm-up book is marked at the close of
   2021-08-31, so September 2021 is a whole month) and E38 (turnover and break-even definitions).
2. **The ledger (L3)**: with up to 69% of capital deployed in skipped names, should V15 or CRSP become the headline, or
   stay a robustness check? It must be decided before any out-of-sample number is seen.
3. **Ledger symbols marked "unknown"**: AHL-C (in scope, $32,500), and variant-only AQFH, CEM, HYH, TWO, HIYS.
4. **WRDS access requested 27 Sep 2026, awaiting approval** (A04).
5. **Stooq and theunitedstates.io are unreachable** from the cloud; not needed on the current plan.
6. **Timing.** The listing's report title date can be one day later than the date received (UTC); we key on
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
