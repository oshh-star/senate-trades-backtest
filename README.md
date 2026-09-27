# Copying the US Senate: a backtest

LBS CA01 Investment Fundamentals, Autumn 2026, group project.

## What this project is
US senators must publicly disclose their stock trades on the Senate's Electronic Financial
Disclosure site (efdsearch.senate.gov) in Periodic Transaction Reports (PTRs), usually weeks
after they trade. We test whether an investor could profit by **copying those trades once they
become public**: buy when a senator's purchase is disclosed, and sell when the same senator
discloses a sale. We compare the result with what the investor could have done instead (SPY,
SPY scaled to the same volatility, the equal-weighted universe of traded stocks, the
Fama-French-Carhart factors, and the NANC and KRUZ ETFs that sell this exact idea), always
over identical dates.

We also measure what the senators themselves earned from the **transaction** date, so the gap
between the senator's return and the copier's return shows how much of any edge is lost to the
disclosure delay.

The rules are stated precisely in `config/config.yaml`. The reason for every rule, every later
change and every variant we ran is in `docs/DECISIONS.md`.

## How to reproduce every number
With Python 3.11, from the repository root:

```bash
pip install -r requirements.txt
python run_all.py
```

That single command runs every stage in order (scrape, clean, prices, engine, metrics, report) and
rebuilds every table in `outputs/tables/`, every figure in `outputs/figures/`, and the data-quality
report `outputs/data_quality.md`. All raw eFD downloads are cached in `data/raw/` and committed,
so no re-scraping is needed. To use the cache only, run:

```bash
python run_all.py --skip-scrape
```

No file paths need editing. Run `python run_all.py --help` for the other options, and
`python -m pytest` for the test suite.

## Where the data came from
| Data | Source | Notes |
|---|---|---|
| Senate trades | Senate eFD, Periodic Transaction Reports received 2016-01-01 to 2026-09-30, scraped directly | Keyed to the date each report was **received** (made public). In scope only if the transaction date falls within the filer's Senate service (congress-legislators dates). Paper (scanned) filings, out-of-service transactions, amended originals and excluded owners are counted and listed in `outputs/data_quality.md`. |
| Stock and ETF prices | Yahoo Finance adjusted close (dividends reinvested), USD | Delisted stocks are missing from Yahoo (survivorship bias). CRSP is used as a robustness check if WRDS access is granted (`prices.price_source: crsp`). |
| Factors and risk-free rate | Kenneth French Data Library: US Fama-French 3 factors, momentum, and RF (daily and monthly) | One risk-free series throughout: Ken French US RF (one-month T-bill). |

Returns are USD total returns. The engine runs daily; Sharpe ratios and factor regressions use
monthly returns. The analysis window is split at its midpoint into an in-sample half (used to
design the rules) and an out-of-sample half. The code refuses to report the out-of-sample half
until the rules are frozen at a recorded commit.

## Repository layout
See `CLAUDE.md` for the full map and the phase plan. The course guidance is in `docs/`.
