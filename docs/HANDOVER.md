# Handover

## Current state
_Last updated: 2026-09-28, end of Phase 3 (Claude, for Harry)._

- **Phase 3 (prices) is done.** `python run_all.py --only clean prices` rebuilds everything offline from the
  caches in about 2.5 minutes. Tests: `python -m pytest` (106 pass). No trade-level or portfolio-level return
  exists anywhere; per-ticker daily returns appear only inside the price sanity checks.
- **Decisions**: J1-J5 logged (2026-09-28). V13 (exclude OTC) and V14 (as revised) pre-registered at commit
  8666206 (main after the Phase 2 merge), logged in commit c5582bc. Engineering interpretations **E19-E27 need
  Harry's confirmation**; E20 (series that end early) is a proposed engine rule.
- **J3 (as first published)** is implemented in the clean stage: data/processed/trade_records.csv has one row per
  published record (2,540 in-scope records for **2,513 in-scope trades**; 2,511 under "as revised", V14).
  trades_clean.csv carries orig_* values, `corrected`, `correction_datetime`, `in_scope_as_revised`, `price_ticker`.
- **J5**: 8 of the 11 override lines confirmed against Yahoo's name (GSK, RYCEY x2, IWB, SBUX, MURGY, BK via BNY,
  PSTG via P). Not confirmed: WIZEY, HOLX, KYOCY (Yahoo no longer knows the symbols; no confirmed successor).
  In-scope trades went from 2,502 to 2,513 (+9 from J5, +2 from J3).
- **Renames**: 32 confirmed through SEC company histories (e.g. FB -> META, ANTM -> ELV, BK -> BNY, PSTG -> P,
  PCLN -> BKNG), 3 same-symbol name changes (RUM, SLB, UHAL), 3 rejected by hand (DVMT, ESV, WTW).
  config/ticker_renames.yaml.
- **Prices**: 1,453 symbols requested (every price_ticker in trades_clean.csv plus SPY, NANC, KRUZ, GBPUSD=X);
  1,278 with usable history. Raw responses and download dates in data/raw/prices/yahoo/. NYSE calendar
  2016-01-04 to 2026-08-31 (2,680 days).
- **Coverage**: 96.1% of in-scope records (93.5% of midpoint dollars) have a price on the entry date. The gap is
  the **survivorship ledger** (data/interim/survivorship_ledger.csv): 35 symbols with in-scope trades have no
  usable Yahoo history (X, ECOM, ATVI, WBA, SSBK, PARA ...; 94 trades, about $5.6m of midpoint dollars).
- **Factors**: Ken French daily 2015-01-02 to 2026-08-31 and monthly 2015-01 to 2026-08, in PERCENT.

## Exact next step
1. **Harry**: confirm E19-E27 (especially the E20 rule for series that end early), and decide WIZEY, HOLX and
   KYOCY (Open questions 1).
2. **Phase 4: engine.** From data/processed/trade_records.csv (J3) build copied positions: FIFO sale matching
   (E18), J3 reversals at correction datetimes, entry at the adjusted close on the first trading day after
   disclosure (D11), trades in the survivorship ledger logged and skipped (until CRSP), E20 for series that end
   early; then the trade-level returns (disclosure and transaction dates, D14) and the daily calendar-time
   portfolio (D15), in-sample only until the OOS firewall is lifted.

## Pre-submission checklist (before Monday 19 October 2026, 23:59)
- [ ] **On or after 1 October 2026**: run `python run_all.py --only scrape clean` once to finalise the 2026
      listing (PTRs received up to 30 September), then `python run_all.py --only prices` and commit.
- [ ] If WRDS access arrives: add the CRSP daily CSV to data/raw/crsp/ and run the CRSP robustness check (A04).
- [ ] Every variant run is logged in DECISIONS.md "Variants run" (the professor asks how many were tried).
- [ ] `python run_all.py` rebuilds every number from the committed caches.

## Open questions
1. **J5 overrides not confirmed**: WIZEY (Wise plc ADR; Yahoo lists the new US listing WSE, "Wise Group plc", a
   different security from 2026), HOLX (Hologic, taken private; no Yahoo data), KYOCY (Kyocera ADR; Yahoo lists
   KYOAY, a different ADR programme). All three stay out (NO_TICKER). Harry: keep out, or add by hand to
   config/ticker_renames.yaml with `hand: true` if you want WSE / KYOAY prices used.
2. **Survivorship ledger** (35 symbols with in-scope trades, 94 trades): the engine needs a rule for them until
   CRSP arrives. Proposal: log and skip (the report counts them). US Steel (X, 22 trades, $1.7m) and
   ChannelAdvisor (ECOM, $1.2m) are the largest.
3. **Yahoo data errors to watch** (outputs/data_quality.md, Phase 3 sections 5-6): some OTC ADRs show split
   moves Yahoo did not adjust (THLLY, QABSY, TRUMY, EVVTY, LYSDY) and one absurd print (TGOPY, 2016-11-30).
   43 symbols, mostly OTC ADRs, have an unchanged close on over 20% of days. V13 (exclude OTC) bounds this.
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
