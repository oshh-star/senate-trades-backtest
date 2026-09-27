# Handover

## Current state
_Last updated: 2026-09-27, end of Phase 1 (Claude, for Harry)._

- **Phase 1 (scrape and raw parse) is done.** Run it with `python run_all.py --only scrape` (about a
  minute from the cache), or year by year with `python -m src.scrape --years 2024 --steps listing download`.
- **Environment**: PyPI works. Every pin in requirements.txt installs as-is; `python -m pytest` passes
  (47 tests).
- **Decisions A05 to A07** (Harry, 2026-09-27) are logged and implemented: scope by Senate service
  dates, analysis window 2021-09-01 to 2026-08-31 (split 2024-02-29 / 2024-03-01), and time received
  recorded. Engineering interpretations **E03 to E08** need Harry's confirmation (DECISIONS.md).
- **Service dates**: data/interim/senate_terms.csv, 407 Senate terms (208 senators) ending on or after
  2010-01-01. 42 ended early; the dataset records the actual departure date for all of them; 0 cases
  found where a departure looks unrecorded.
- **Scrape**: 1,874 PTRs received 2016-01-01 to 2026-09-27 (all filer types): 1,566 electronic (all
  downloaded, 0 failures) and 308 paper (metadata only). 169 are amendments. Manifest:
  data/interim/filings_manifest.csv. Paper list: data/interim/paper_filings.csv.
- **Parse**: 14,558 transaction rows in data/interim/transactions_raw.csv. Every PTR passes the
  three-way row check (parser rows = `<tbody>` rows = the page's stated total) and the per-owner count
  check: 0 mismatches.
- **Names**: 82 distinct filer names, 80 exact matches, 2 fuzzy (Mitch McConnell high confidence;
  **Jim Banks low confidence, awaiting Harry**). 0 unmatched.
- **First look**: outputs/phase1_summary.md. Key number: 2,520 copyable stock/ETF-proxy transactions
  in the default window (1,280 purchases, 1,225 sales), before amendment de-duplication (up to 350 of
  them come from amendment filings). The top 5 senators make up 88.5% (Tuberville alone 36.6%).
- Notable: Jeff Sessions's five 2016 PTRs (filed while he was a sitting senator) are labelled
  "Candidate" today, which confirms A05. Alan Armstrong (appointed to Mullin's Oklahoma seat
  2026-03-24) filed 707 rows in 2026, probably an incoming portfolio reshuffle; worth a look in Phase 2.

## Exact next step
1. **Harry**: settle Jim Banks in config/name_overrides.yaml (see Open questions 1) and confirm E03 to E08.
2. **On or after 1 October 2026**: run `python run_all.py --only scrape` once. The 2026 listing was
   fetched before the 2026-09-30 cutoff, so it is re-fetched automatically and any PTRs received
   28 to 30 September are downloaded. Commit the result. (It cannot change the default window,
   which ends 2026-08-31.)
3. **Phase 2: clean.** Build `src/clean/run()` from data/interim/transactions_raw.csv:
   in-scope filter by service dates (A05); owners Self and Joint; asset universe (stocks and ETFs,
   `is_etf` from Yahoo's instrumentType; exclude options, bonds, crypto, mutual funds); amendments
   (link each amendment to its original by filer and title date, keep the latest, log replaced
   originals); parse amounts into ranges and midpoints; FIFO sale matching; exclusions log in
   outputs/data_quality.md.

## Open questions
1. **Jim Banks (low-confidence name match).** eFD lists "James Banks" / office "Banks, James E.
   (Senator)", 5 PTRs 2025-03-10 to 2026-06-07. congress-legislators has "Jim Banks" (B001299,
   R-IN, Senate from 2025-01-03), with no "James" on record. It looks like the same person, but by
   the "do not guess" rule it is left for Harry. If confirmed, add to config/name_overrides.yaml:
   `"James|Banks": {bioguide_id: B001299, note: "confirmed by Harry <date>"}`. It adds 3 key-number rows.
2. **WRDS access requested 27 Sep 2026, awaiting approval.** When it is approved, a teammate will
   download CRSP daily stock data as a CSV from the WRDS website and add it to `data/raw/crsp/`
   (DECISIONS.md A04).
3. **SEC contact email.** `scrape.contact_email` in config is a placeholder. It is needed before any
   request to www.sec.gov. Probably needed in Phase 2 or 3 for the ticker/CIK list.
4. **Amendment inflation.** Up to 350 of the 2,520 key-number rows come from amendment filings (191
   in 2026 alone). Phase 2's keep-latest rule will remove the replaced originals' duplicates.
5. **Concentration.** Five senators make up 88.5% of the key-number transactions. The report should
   show results with and without the top name (a variant, to be logged).
6. **Stooq and theunitedstates.io are unreachable** from the cloud; not needed on the current plan.
7. **ETF flag (Phase 2).** eFD's "Asset Type" does not separate ETFs: some are "Stock" (IVV), most
   are "Other" alongside mutual funds. Plan: `is_etf` from Yahoo's `instrumentType`.
8. **Timing.** The listing's report title date can be one day later than the date received (Rick
   Scott: received 09/18/2025, page says "Filed 09/18/2025 @ 9:09 PM", title "for 09/19/2025",
   consistent with the title using UTC). We key on the date received; the time is in the manifest.

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
