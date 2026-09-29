# Handover

## Current state
_Last updated: 2026-09-28, end of Phase 4 (Claude, for Harry)._

- **Phase 4 (engine) is done, IN-SAMPLE ONLY** (disclosures 2021-09-01 to 2024-02-29; the OOS firewall is shut and
  the engine cuts prices, RF and the calendar at 2024-02-29 before computing anything). `python run_all.py --skip-scrape`
  rebuilds clean, prices and engine from the caches in about 2.5 minutes. Tests: `python -m pytest` (129 pass).
- **Decisions**: K1-K7 logged (2026-09-28). **V15 (neutral fill) and V16 (all ETFs) pre-registered at commit
  cd71368** (main after the Phase 3 merge), logged in commit 842025e before any return existed. Engineering
  interpretations **E28-E33 need Harry's confirmation** (BRK is a Canadian CDR, not BRK-B; same-day order; book,
  series and panel details; ETF class rules).
- **Scope now (K5 + K2 + K4)**: **2,342 in-scope trades** (2,365 records) against 2,513 before: 170 non-equity ETF
  trades left (123 bond/T-bill, 25 commodity, 22 other = BITB), 3 non-US listings left (BRK CDR, COLPAL), 2 K2 trades
  entered (HOLX, KYOCY; in the ledger, so skipped).
- **Prices**: 96.1% of in-scope records have an entry-date price (93.8% of midpoint dollars). SQ now priced as XYZ.
  K6: 20 bad Yahoo prints repaired in 6 OTC ADRs, all in 2016-2019, none inside a copied holding period.
- **Survivorship ledger**: 177 symbols, 32 with in-scope records (89 trades, $5.5m at midpoints; in-sample: 22
  purchases, $1.8m, skipped). Every symbol has a reason and source in config/ledger_reasons.yaml (in-scope: 13
  acquired for cash, 12 for stock, 4 ticker issues, 1 bankrupt, 1 liquidated, 1 unknown).
- **Engine results (in-sample)**: 884 events -> 413 copied lots; 310 of 448 sale records ignored (nothing held,
  mostly stock bought before the window; Tuberville 155); K = $7,755,442; lot P&L = book P&L to the cent.
  Annualised return / volatility over identical dates: series A 7.61% / 29.34%, series B 7.04% / 10.14%, SPY 6.46% /
  18.40%. Outputs: data/processed/lots.csv, daily_book.csv, event_panel.csv, engine_events.csv, engine_metadata.json;
  outputs/data_quality.md Phase 4 section; outputs/figures/phase4_open_lots_capital.png;
  outputs/phase4_worked_examples.md.

## Exact next step
1. **Harry**: confirm E28-E33 (DECISIONS.md), and check one worked example on Yahoo Finance
   (outputs/phase4_worked_examples.md).
2. **Phase 5: metrics and benchmarks, in-sample.** From daily_book.csv: monthly returns, Sharpe ratios, SPY,
   SPY scaled to series A's volatility, the equal-weighted universe, FF3 + momentum regressions; NANC and KRUZ from
   February 2023 (in-sample: February 2023 to February 2024 only). Event study from event_panel.csv (mean and t-stats
   by horizon, purchases and sales, copier vs senator, the gap). Still no variants and no out-of-sample numbers.

## Known limitations
- **K7: spin-offs in renamed tickers.** UTX -> RTX (Carrier and Otis spun off in April 2020) and DWDP -> DD (Dow in
  April 2019, Corteva in June 2019): a lot held across a spin-off date is priced with RTX's or DD's history, which may
  not credit the spun-off shares. Both dates are before the 5-year window, so only the 10-year variant (V12) is
  affected. Not fixed.
- **Series A in the first weeks**: from 2021-09-09 to mid-October 2021 the book holds a single lot, so series A's
  daily returns are one stock's (moves of +/-6% a day). This is what "return on capital deployed" means, but it
  inflates series A's volatility; Phase 5 should show it (and series B, which does not have the problem).
- **Yahoo drops delisted names entirely**, so E20 (series ending early) almost never fires (LBRDA only); the
  survivorship problem sits in the ledger instead, which is why V15 and CRSP matter.
- Preferred shares (AHL-C, BKEPP) passed Yahoo's EQUITY classification in Phase 2; both are in the ledger and skipped.

## Pre-submission checklist (before Monday 19 October 2026, 23:59)
- [ ] **On or after 1 October 2026**: run `python run_all.py --only scrape clean` once to finalise the 2026
      listing (PTRs received up to 30 September), then `python run_all.py --only prices engine` and commit.
- [ ] If WRDS access arrives: add the CRSP daily CSV to data/raw/crsp/ and run the CRSP robustness check (A04).
- [ ] Every variant run is logged in DECISIONS.md "Variants run" (the professor asks how many were tried).
- [ ] `python run_all.py` rebuilds every number from the committed caches.

## Open questions
1. **E28-E33** need confirmation. In particular E28(a): BRK is a CAD-hedged Canadian Depositary Receipt ("Bershire
   Hathaway Cdr [Cad Hedged]"), so it is now excluded as a non-US listing instead of being mapped to BRK-B.
2. **Ledger symbols marked "unknown"**: AHL-C (in scope, $32,500), and variant-only AQFH, CEM, HYH, TWO, HIYS
   (HIYS: Yahoo has no history; its record is out of scope anyway as a bond ETF).
3. **Should series A start once the book holds a minimum number of lots?** (See Known limitations.) It must be
   decided before any out-of-sample number is seen; currently it starts on the window's first day.
4. **WRDS access requested 27 Sep 2026, awaiting approval** (A04). CRSP should price the 27 in-scope ledger symbols
   that were acquired, went bankrupt or liquidated; not the 4 OTC ADRs (TOELY, DFKCY, WIZEY, KYOCY) or the
   preferred share (AHL-C).
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
