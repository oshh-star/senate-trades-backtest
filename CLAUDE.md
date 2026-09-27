# CLAUDE.md: Senate trades backtest (LBS CA01)

## Project summary
LBS CA01 Investment Fundamentals group project, due **Monday 19 October 2026, 23:59**.
We backtest a "copy the US Senate" strategy. When a senator's stock trade is publicly disclosed
on the Senate eFD site (efdsearch.senate.gov), we copy it: buy when a purchase is disclosed, sell
when that same senator discloses a sale. The professor marks the **quality of the argument**,
not whether the strategy makes money (docs/CA01AUT26_GroupProject_Guidance.pdf). The rules must be
precise enough to reproduce, every performance number needs a benchmark over identical dates, and
one command (`python run_all.py`) must rebuild every number.

## Where the spec lives
- **config/config.yaml** holds every locked parameter (the single source of truth for code).
- **docs/DECISIONS.md** holds the dated reason for every decision, every change and every variant run.
- **docs/HANDOVER.md** holds the current state, the exact next step and the open questions.

### Locked spec in brief (details and reasons in DECISIONS.md)
- **Data**: scrape Senate eFD PTRs directly (never the frozen senate-stock-watcher-data repo).
  PTRs received 2016-01-01 to 2026-09-30, ALL filer types (1 Senator, 4 Candidate, 5 Former Senator),
  with the date AND time received. **Scope (A05)**: a transaction is in scope if and only if its
  transaction date falls within that person's Senate service (unitedstates/congress-legislators
  dates, data/interim/senate_terms.csv); the eFD filer-type label is today's status and is not used.
  Paper filings are logged (senator, date, link) and excluded. Amendments: keep the latest version
  and log the replaced originals. Raw downloads are cached in data/raw/ and committed.
- **Analysis window (A06)**: ends 2026-08-31 (Ken French data ends there). `analysis.window_years`
  (default 5, i.e. disclosures 2021-09-01 to 2026-08-31, 60 months; 3 and 10 are a one-line change).
- **Universe**: US common stocks **and US-listed ETFs** (every trade flagged `is_etf`;
  `universe.include_etfs: false` is the ETF-excluded variant). Options, bonds, crypto and mutual
  funds are excluded.
- **Owners**: `universe.owners: [Self, Joint]`. Spouse and Child trades stay in the raw cache and
  are counted by owner type in the exclusions log; adding them is a one-line variant.
- **Sizing**: midpoint of the disclosed range (open top band uses its lower bound). Variants:
  lower_bound, equal_dollar.
- **Prices**: adjusted close on the first trading day AFTER the disclosure (date received).
  Variant: same-day close. `prices.price_source: yahoo | crsp` (CRSP is a robustness check).
- **Matching**: a sale is matched FIFO to that senator's open copied positions in the same ticker,
  regardless of owner. Sale (Full) closes it; Sale (Partial) sells the midpoint amount, capped at
  the holding. Sales of anything we do not hold (for example, bought before the window) are ignored
  and logged. No shorting. Exchanges are ignored and logged. Open positions are marked at the last price.
- **Senator vs copier**: every trade's return is also measured from the transaction date. The gap
  between the two is a core result.
- **Portfolio**: calendar-time, daily; dollar-weighted average return of open positions (equal-weight
  rebalanced at each filing date is a variant); idle days earn the risk-free rate. USD total returns.
  Ken French US RF. Sharpe ratios and regressions on monthly returns. Event study at 5, 21, 63, 126
  and 252 trading days.
- **Benchmarks** (Phase 5): SPY; SPY scaled to strategy volatility; equal-weighted universe;
  FF3 plus momentum (US); NANC and KRUZ from February 2023.
- **Out-of-sample firewall**: the window splits at its midpoint in whole months (5y: in-sample to
  2024-02-29, out-of-sample from 2024-03-01). Code refuses to compute
  out-of-sample results unless `oos.oos_unlocked: true` AND `project.frozen_rules_commit` is set,
  and flipping them requires a DECISIONS.md entry naming the frozen commit.

## Repo map
```
run_all.py            one command: scrape > clean > prices > engine > metrics > report (--skip-<stage>, --only)
config/config.yaml    locked parameters
src/config.py         config loader, analysis window, sample split, OOS firewall guard
src/scrape/efd.py     eFD client (terms agreement, search, PTR fetch) and HTML parsers
src/{scrape,clean,prices,engine,metrics,report}/   one package per stage, each exposes run(cfg)
data/raw/             cached raw downloads (committed); data/raw/_dryrun/ holds Phase 0 test output
data/raw/crsp/        CRSP daily CSV goes here once WRDS access is approved
data/interim/, data/processed/   derived data, rebuilt by run_all.py
outputs/tables/, outputs/figures/, outputs/data_quality.md   report outputs
docs/                 DECISIONS.md, HANDOVER.md, the course guidance PDF
scripts/install_pkgs.sh   SessionStart hook: pip install in cloud sessions
scripts/phase0_checks.py  environment checks (connectivity, eFD, counts, prices, factors)
tests/                pytest suite (run: python -m pytest)
```

## Phase plan
| Phase | Work | Status |
|---|---|---|
| 0 | Set-up and environment checks | Done (2026-09-27) |
| 1 | Scrape eFD PTRs 2016-01-01 to 2026-09-30 into data/raw/ (resumable) | Not started |
| 2 | Clean: parse, filter universe and owners, amendments, matching, exclusions log | Not started |
| 3 | Prices (Yahoo, or CRSP CSV) and Ken French factors | Not started |
| 4 | Engine: trade-level and calendar-time portfolio returns | Not started |
| 5 | Metrics and benchmarks | Not started |
| 6 | Robustness and mechanism tests (variants, OOS) | Not started |
| 7 | Report outputs (tables, figures, data_quality.md) | Not started |

## RULES FOR EVERY SESSION
1. At the start of every session, read CLAUDE.md, docs/HANDOVER.md and docs/DECISIONS.md before
   doing anything.
2. Never change a locked parameter without a DECISIONS.md entry (date, who, what, why).
3. Log every variant ever run in DECISIONS.md. The professor asks how many variants were tried.
4. Commit and push after every meaningful step. The cloud machine can be reclaimed at any time and
   uncommitted work is lost.
5. Long jobs must be resumable and checkpoint to disk.
6. Relative paths only. Everything runs from the repo root with: `python run_all.py`
7. Every data exclusion is counted and explained in outputs/data_quality.md.
8. No look-ahead: every input is keyed to the date it became public.
9. Respect the out-of-sample firewall.
10. Scraping etiquette: at most 1 request per second, a descriptive User-Agent. SEC requests need a
    contact email in the User-Agent; it is a placeholder in config (`scrape.contact_email`), so ask
    the user for it when needed.
11. The user is non-technical: plain English, exact clicks.
12. End every session by updating docs/HANDOVER.md, committing, pushing and opening a pull request.
