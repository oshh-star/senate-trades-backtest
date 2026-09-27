# Decisions log

Every locked parameter, every change to one, and every variant run goes here: **date, who, what, why**.
Newest entries at the bottom. Never edit an old entry; add a new one that supersedes it.
Config keys refer to config/config.yaml.

## Locked specification (2026-09-27, Harry)

| # | Date | Who | Decision | Config key | Reason |
|---|---|---|---|---|---|
| D01 | 2026-09-27 | Harry | Data source: scrape Senate eFD Periodic Transaction Reports directly | `data.source` | Primary source, dated by receipt; the senate-stock-watcher-data repo is frozen and must not be used. |
| D02 | 2026-09-27 | Harry | Filers: sitting Senators only; log excluded candidate filings | `data.include_filer_types` | The strategy copies senators, and candidates are not in office. |
| D03 | 2026-09-27 | Harry | Scrape range: PTRs received 2016-01-01 to 2026-09-30 | `data.scrape_start`, `data.scrape_end` | Fixed cutoff so every run sees identical data and the 10-year window is covered. |
| D04 | 2026-09-27 | Harry | Analysis window: 5 years by default (disclosures 2021-10-01 to 2026-09-30); 3 and 10 years supported by a one-line change | `analysis.window_years` | Five years balances sample size against relevance; the others are robustness checks. |
| D05 | 2026-09-27 | Harry | Paper (scanned) filings are excluded and each is logged (senator, date, link) | `data.paper_filings` | They cannot be parsed reliably, and silent drops would hide a selection effect. |
| D06 | 2026-09-27 | Harry | Amended PTRs: keep the latest version only; log the replaced originals | `data.amendments` | The amendment is the senator's corrected record; the log keeps the change visible. |
| D07 | 2026-09-27 | Harry | All raw downloads are cached in data/raw/ and committed | `data.cache_raw_downloads` | The pipeline must reproduce every number without re-scraping a site that can change. |
| D08 | 2026-09-27 | Harry | Universe: US common stocks only; exclude options, bonds, crypto, mutual funds and ETFs (ETFs flagged so a switch can re-add them) | `universe.*` | Stocks are what a copier can trade cleanly and price reliably. **Superseded in part by A02.** |
| D09 | 2026-09-27 | Harry | Owners: include all owners (Self, Spouse, Joint, Child) and keep the owner field | `universe.owners` | Disclosure covers the household. **Superseded by A01.** |
| D10 | 2026-09-27 | Harry | Sizing: midpoint of the disclosed dollar range; open-ended top band uses its lower bound. Variants: lower_bound, equal_dollar | `trades.sizing`, `trades.open_top_band` | The midpoint is the unbiased guess within a band; an open band has no midpoint. |
| D11 | 2026-09-27 | Harry | Entry/exit price: adjusted close on the first trading day AFTER the disclosure (date received). Variant: same-day close | `trades.price_timing` | A copier can only act once the filing is public; filings often arrive after the close. |
| D12 | 2026-09-27 | Harry | Matching: a sale is matched FIFO to that senator's open copied positions in the same ticker, regardless of owner. Sale (Full) closes the whole position; Sale (Partial) sells the midpoint amount, capped at what we hold. Sales with no copied position are ignored (no shorting). Exchanges are ignored and logged | `trades.matching` and neighbours | A mechanical rule a reader can reproduce; FIFO is the standard default. **Confirmed by A03.** |
| D13 | 2026-09-27 | Harry | Positions still open at the end of the window are valued at the last available price | `trades.open_at_window_end` | Every position needs a return without extending the window. |
| D14 | 2026-09-27 | Harry | Every trade's return is also measured from the TRANSACTION date, alongside the disclosure date | `trades.also_compute_transaction_date_returns` | The gap between what the senator earned and what a copier earns is a core result. |
| D15 | 2026-09-27 | Harry | Calendar-time portfolio: daily return = dollar-weighted average return of open positions; idle days earn the risk-free rate. Equal weight (rebalanced at each filing date) is a switch | `portfolio.weighting`, `portfolio.idle_days_earn` | This is a return on capital actually deployed, which avoids inventing a notional capital base. |
| D16 | 2026-09-27 | Harry | Trade-level event study at 5, 21, 63, 126 and 252 trading days | `portfolio.event_study_horizons` | Shows how quickly any information edge decays, from one week to one year. |
| D17 | 2026-09-27 | Harry | USD total returns (dividend-adjusted); risk-free rate is Ken French US RF; engine runs daily; Sharpe ratios and factor regressions use monthly returns | `portfolio.returns`, `factors.risk_free`, `portfolio.stats_frequency` | One named rf series throughout; monthly statistics as the guidance asks for holdings longer than a month. |
| D18 | 2026-09-27 | Harry | Benchmarks: SPY; SPY scaled to strategy volatility; equal-weighted universe; FF3 plus momentum (US); NANC and KRUZ from their February 2023 launch | `benchmarks` | Naive, risk-matched and style-matched alternatives, as the guidance requires, plus the two products that sell this exact idea. |
| D19 | 2026-09-27 | Harry | Out-of-sample firewall: the window splits at its midpoint; OOS results are refused unless `oos_unlocked: true`, which requires a DECISIONS.md entry recording the commit hash at which the rules were frozen | `oos.*`, `project.frozen_rules_commit` | Out of sample means data that influenced no choice; the code enforces it rather than trusting memory. |
| D20 | 2026-09-27 | Harry | Scraping etiquette: at most 1 request per second, descriptive User-Agent; SEC contact email kept in config as a placeholder | `scrape.*` | Courtesy to public servers; SEC requires a contact email. |

## Amendments

| # | Date | Who | Decision | Config key | Reason |
|---|---|---|---|---|---|
| A01 | 2026-09-27 | Harry | **Owners: only Self and Joint** trades enter the analysis. Spouse and Child trades are kept in the raw cache and counted by owner type in the exclusions log. Supersedes D09 | `universe.owners: [Self, Joint]` | Trades the senator controls directly are the cleanest test of the senator's own information; the family-included variant is a one-line change. |
| A02 | 2026-09-27 | Harry | **ETFs included** for now; every trade carries an `is_etf` flag so the ETF-excluded variant is a one-line change. Mutual funds stay excluded. Supersedes the ETF part of D08 | `universe.include_etfs: true` | ETFs are liquid, US-listed and tradeable by a copier; the flag keeps the stock-only result one switch away. |
| A03 | 2026-09-27 | Harry | **Matching confirmed, no change**: FIFO within senator and ticker; a sale of anything we do not hold (for example, bought before the analysis window) is ignored and logged. No shorting | `trades.matching`, `trades.unmatched_sales` | Confirms D12 and makes the pre-window case explicit. |
| A04 | 2026-09-27 | Harry | **CRSP as a robustness price source.** WRDS access requested 27 Sep 2026, awaiting approval. When approved, a teammate downloads CRSP daily stock data as a CSV from the WRDS website into data/raw/crsp/. The Phase 3 prices stage must accept either source via config | `prices.price_source: yahoo \| crsp`, `prices.crsp_dir` | CRSP includes delisted stocks and is the academic standard, so it tests the survivorship bias in Yahoo without rewriting code. |
| A05 | 2026-09-27 | Harry | **Scope by Senate service dates, not the eFD filer-type label (E01 refined).** eFD's filer-type label reflects the filer's CURRENT status in both directions, so it cannot be trusted either way: a sitting senator's pre-election candidate PTRs are probably labelled "Senator" today (which explains why "Candidate" shows 5 filings in 2016 and 0 in every later year). New rule: a transaction is in scope if and only if its **transaction date** falls within that person's Senate service. Service dates come from the unitedstates/congress-legislators dataset (legislators-current.yaml and legislators-historical.yaml, cached in data/raw/legislators/). Phase 1 scrapes ALL PTR filer types (1 Senator, 4 Candidate, 5 Former Senator); the in-scope filter is applied in Phase 2. Supersedes E01 and D02's use of filer types | `data.scrape_filer_types: [1, 4, 5]`, `data.scope_rule`, `data.service_dates` | The label is today's status, not the status at filing; the service dates are the only record of who was a senator on the day of the trade. |
| A06 | 2026-09-27 | Harry | **Analysis end date = 2026-08-31.** Default 5-year window: disclosures 2021-09-01 to 2026-08-31 (60 months). 3-year: from 2023-09-01. 10-year: from 2016-09-01. In-sample/out-of-sample split at the midpoint in whole months: in-sample 2021-09-01 to 2024-02-29, out-of-sample 2024-03-01 to 2026-08-31. The scrape range is unchanged (received 2016-01-01 to 2026-09-30). Supersedes D04's end date and resolves HANDOVER open question 5 | `analysis.window_end: 2026-08-31`, `oos.split: midpoint_months` | Ken French data ends on 2026-08-31, and every benchmark must cover identical dates. Splitting in whole months keeps each half a whole number of months for the monthly statistics. |
| A07 | 2026-09-27 | Harry | **Record the date AND time received for every PTR.** The headline entry rule is unchanged (close of the first trading day after the date received); the timestamp will power the same-day variant later | `data.record_time_received: true` | Filings made during market hours could be copied the same day; filings after the close could not. The timestamp lets the same-day variant tell them apart. |

## Engineering interpretations (need Harry's confirmation)

| # | Date | Who | Decision | Config key | Reason |
|---|---|---|---|---|---|
| E01 | 2026-09-27 | Claude (engineer) | **Superseded by A05.** **Filer types: "sitting Senators" means senators at the time they filed**, so we include eFD filer types 1 (Senator) and 5 (Former Senator) and exclude 4 (Candidate). | `data.include_filer_types: [1, 5]` | Verified on the live site: eFD labels filers by their CURRENT status. For example, Markwayne Mullin's 17 Sep 2025 PTR sits under "Former Senator" even though its office column reads "(Senator)". Former Senators make up 82 of 200 PTRs in 2016. Using type 1 alone would keep only senators still in office today, which is survivorship bias. Candidate filings (5 in 2016, 0 since) are logged and excluded. |
| E02 | 2026-09-27 | Claude (engineer) | Phase 0 used Yahoo's chart API directly (the endpoint yfinance calls) because PyPI was blocked and yfinance could not be installed. Phase 3 uses yfinance once installable | `prices.price_source` | Environment constraint, not a methodology choice. |

## Variants run
Every run with any non-default config value is logged here: date, who, what changed, commit, where the output is.
The professor asks how many variants were tried.

| # | Date | Who | Variant (config changes from default) | Commit | Output |
|---|---|---|---|---|---|
| (none yet) | | | | | |
