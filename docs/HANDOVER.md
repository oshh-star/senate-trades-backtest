# Handover

## Read this first (2026-10-09)
- **Status in one line**: the analysis is finished and **a first draft of the report is written**
  (`docs/REPORT_DRAFT.md`, every number from the committed tables). What is left: the group edits it into the final
  10-page report, then builds and uploads the submission.
- **Not merged yet**: all work from the 2026-10-09 session is on branch `claude/magical-dijkstra-3poiyr`, pull request
  https://github.com/oshh-star/senate-trades-backtest/pull/15. `main` does not have it until that pull request is merged
  (on GitHub: open the link, click **Merge pull request**, then **Confirm merge**). To see the files before merging,
  pick that branch in the branch menu (it says **main**) above the file list.
- **Frozen and unlocked**: rules frozen at `348318447daa58a91af14ae65c8ee3c98522d896` (F1), out-of-sample unlocked (U1).
  No rule, parameter, scope, test or prediction may change; a fix is a logged post-unlock correction.
- **C1 (2026-10-09), post-unlock correction: the headline now uses Bloomberg prices** for the 8 delisted stocks Yahoo
  lacks (`prices.sources: [yahoo, manual]`; group decision given in the Claude session of 2026-10-09). Every before and
  after value is in docs/DECISIONS.md, "Post-unlock corrections", C1. The Yahoo-only result is variant V18. Full-window
  and second-half tables are now tagged `_bloomberg`; the in-sample design record keeps its `_yahoo` files.
- **Main result (full window 2021-09 to 2026-08, outputs/tables/phase5_full_results.md)**: series A 13.41% a year
  (volatility 23.41%, Sharpe 0.50) against SPY 12.69% (Sharpe 0.61) and risk-matched SPY 16.30%; CAPM alpha +1.07%
  (NW t 0.18), Carhart +2.26% (t 0.37), beta 1.21, SMB 0.33; maximum drawdown -32.16% (2022-03-25 to 2022-07-14,
  recovered 2024-03-01); excess over risk-matched SPY -2.58% a year, so no break-even cost. Senate universe 13.56%.
- **Second half (phase5_oos_results.md)**: series A 22.94% against SPY 19.32% and risk-matched SPY 26.02%; CAPM alpha
  +1.69% (t 0.29).
- **H0-H4 (confirmatory_oos.md)**: every verdict unchanged by C1. H0, H3, H4 not distinguishable from zero; H1
  purchases significantly NEGATIVE (-3.22%, t -2.98, Holm p 0.017); H2 positive (+1.74%, t 3.54). Both significant
  results rest on Armstrong's 2026-07-21 filing (654 purchases, 67% of the half's); without bulk filings H1 -0.11%
  (t -0.18), H2 +1.12% (t 0.81). The H2 reversal reading at 126 days is now "partly reversed" (+1.73% against the
  21-day +1.74%).
- **Survivorship**: the 178 still-unpriced symbols are at most 2.2% of capital (was 67.2% with Yahoo only).
- **Variants** (variants_full_bloomberg.md): 9.43% (V3) to 25.50% (V11); no alpha reaches |t| = 2 in the full window
  or any variant's own second half.

## Current state
_Last updated: 2026-10-09 (Claude). Phase 7: report first draft written; submission tooling ready._

- **Done in the 2026-10-09 session** (pull request #15):
  - **C1**: Bloomberg prices for 8 delisted stocks in the headline; code, config and tests changed; every output
    rebuilt; before and after values in DECISIONS.md.
  - **Variants** rerun with the Bloomberg prices (C1-V; V2.2 no Armstrong 13.15%, V4 no bulk filings 11.38%, V15 13.42%).
  - **Survivorship wording** fixed everywhere: the missing stocks pushed the return DOWN (Yahoo only 10.81%,
    Bloomberg-filled 13.41%), so V15 (SPY fill) is not a bound.
  - **Report first draft**: `docs/REPORT_DRAFT.md`. The full 5 years is the main result, the second half is the check,
    and H0-H4 carry the Armstrong caveat with the ex-bulk values beside them. It follows the course guidance's
    structure, is longer than 10 pages (to be cut), and has **[GROUP]** marks where a decision is needed.
  - **Exploratory recount**: 81 of 516 cells reach |t| = 2 on the corrected tables (78 with Yahoo only); the draft's
    Section 6.3 says where they sit.
  - **Takeovers checked**: 7 of the 8 Bloomberg stocks were taken over; their files end one day before delisting, at
    the deal price. Every copied lot in them was closed by the senator's own sale before the takeover, so the end dates
    do not affect the portfolio (the draft says so in Section 4).
  - **Two submission zips (S4)**: `python scripts/make_submission.py` builds dist/submission.zip (26 MB) and
    dist/submission_prices.zip (86 MB).
  - The teammate's first Bloomberg run is logged (BBG, BBG-V).
- **Clean-room test** on commit cf5acae (both zips unzipped into an empty folder, `python run_all.py --skip-scrape`,
  `sha256sum -c`): all 6,484 files identical, byte for byte. On another machine the 3 PNG figures can differ in font
  rendering only (the README warns about it). Later commits changed only documents, not results.
- Tests: `python -m pytest` (183 pass). `python run_all.py --skip-scrape` about 2.5 minutes; `python run_variants.py`
  about 8 minutes.
- docs/BLOOMBERG_UPDATE.md and outputs/tables/bloomberg_fill/ are the record of the teammate's first Bloomberg run; the
  main tables now carry the same numbers.
- **Considered and not done**: pricing everything from Bloomberg (about 1,300 symbols; little effect expected, and a
  second post-unlock change). A cheaper option if the group wants it: pull Bloomberg for the 35 largest positions (half
  the dollars) plus SPY, and the prices stage compares the two sources automatically.

## Exact next step
0. **Merge pull request #15** (link above) so `main` has this work, ONLY when the group decides to (as of 2026-10-09 the user asked for it NOT to be merged yet).
1. **The group: edit docs/REPORT_DRAFT.md** into the 10-page report. Every **[GROUP]** mark needs a decision or check:
   group names; the Armstrong framing (H1, H2); the wording on C1 (why the corrected number is the headline); NANC and
   KRUZ descriptions. (The exploratory count is redone: 81 of 516 cells reach |t| = 2 on the corrected tables, was 78.)
2. **Put the puller's name in data/raw/manual_prices/SOURCES.md** (every row says "name TBC"; not known on 2026-10-09:
   the files were uploaded by the GitHub account esun1019, which shows who uploaded them, not who pulled them).
3. **Submission (S4)**: only once the report is final, on the FINAL commit, run `python scripts/make_submission.py`, then the clean-room test (unzip
   both into an empty folder, `python run_all.py --skip-scrape`, `sha256sum -c CHECKSUMS.sha256 --quiet`). Only the
   3 PNGs may differ (fonts). Upload the report, submission.zip and submission_prices.zip to Canvas before Monday
   19 October 2026, 23:59.
4. **If WRDS access arrives**: V20 is now `[yahoo, manual, crsp]`; run `python run_variants.py --only V20`. It cannot
   change the headline.

## Known limitations
- **K7: spin-offs in renamed tickers.** UTX -> RTX (Carrier and Otis spun off in April 2020) and DWDP -> DD (Dow in
  April 2019, Corteva in June 2019): a lot held across a spin-off date is priced with RTX's or DD's history, which may
  not credit the spun-off shares. Both dates are before the 5-year window, so only the 10-year variant (V12) is
  affected. Not fixed.
- **Survivorship ledger** (L3): with the Bloomberg files (C1) the 178 unpriced symbols are at most 2.2% of capital
  (Yahoo only: up to 67%). V15 (SPY fill) gives 13.42%; it is not a bound, because the priced ledger stocks beat SPY. The Senate-universe benchmark also leaves these symbols out (15 symbols, 181 symbol-months).
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
- [x] Rules frozen (F1) and out-of-sample unlocked (U1); full backtest and second half run (2026-10-06).
- [x] Bloomberg prices for the 8 MUST-HAVE stocks in the headline (C1, 2026-10-09), before/after logged.
- [x] Every variant run logged in DECISIONS.md "Variants run" (latest: C1-V).
- [x] Two-zip submission script (S4) and a clean-room test (2026-10-09, cf5acae: every file identical).
- [x] Report first draft written (docs/REPORT_DRAFT.md, 2026-10-09).
- [ ] The final report: edit the draft (the **[GROUP]** marks), cut to 10 pages, label every table and figure.
- [ ] Puller's name in data/raw/manual_prices/SOURCES.md.
- [ ] Two zips built from the FINAL commit; clean-room rebuild and `sha256sum -c` on it.

## Open questions
1. **How to frame H1 and H2** (one filing, 67% of the half's purchases). The draft keeps the registered verdicts and
   puts the ex-bulk values beside them.
2. **Who decided C1?** It was given in the Claude session of 2026-10-09; add the name(s) to DECISIONS.md C1 if the
   group wants it recorded.
3. **Ledger symbols marked "unknown"**: AHL-C (out of the headline as a preferred), and variant-only AQFH, CEM, HYH,
   TWO, HIYS.
4. **WRDS access** requested 27 Sep 2026, still awaiting approval (A04). Only V20 would use it.

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
