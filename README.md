# Copying the US Senate

**London Business School, CA01 Investment Fundamentals, Autumn 2026. Group project.**

US senators must disclose their stock trades within 45 days. We test whether an investor who copies each disclosed
trade, buying when a purchase becomes public and selling when the same senator discloses a sale, beats what they could
have held instead. **It does not.** Over September 2021 to August 2026 the copied book returned 13.4% a year at 23.4%
volatility, against 12.7% for SPY and 16.3% for SPY at the same volatility. Its alpha is statistically zero, and the
half of the data we never used to design the rules gives the same answer.

**The report:** [`report/Copying_the_US_Senate_Study_Group_B12_final.pdf`](report/Copying_the_US_Senate_Study_Group_B12_final.pdf). Every number in it can be re-derived from this repository; [`outputs/README.md`](outputs/README.md) says which file holds each one.

## Rebuild every number

You need Python 3.11. Everything runs offline from the cached data, and no file path needs editing.

```bash
pip install -r requirements.txt
python run_all.py --skip-scrape     # about 3 minutes: every table in outputs/
python run_variants.py              # about 8 minutes: the robustness variants
python -m pytest                    # about 8 seconds: 184 checks
```

Then the report's extra figures: `python report/diagnostics.py` (bootstrap, Sharpe test, rolling alpha),
`python report/supplementary.py` (the counts and shares quoted in Sections 2 to 6 and Table E2) and
`python report/build_figures.py` (the charts).

## What is where

| Folder | Contents |
|---|---|
| `data/` | `raw/` every download, cached exactly as received (Senate filings, prices, factors, SEC files); `interim/` and `processed/` are rebuilt from it |
| `src/` | The pipeline, one folder per stage: `scrape`, `clean`, `prices`, `engine`, `metrics` |
| `config/` | `config.yaml`, every rule of the strategy as a parameter, plus hand-checked lookup tables |
| `outputs/` | Every result table and the data-quality log. **[`outputs/README.md`](outputs/README.md) says which file feeds each table in the report** |
| `report/` | The final report, and the scripts behind its charts and extra figures |
| `docs/` | [`DECISIONS.md`](docs/DECISIONS.md), the dated record of every rule, change and variant; [`HANDOVER.md`](docs/HANDOVER.md), the current state; [`REPRODUCING.md`](docs/REPRODUCING.md), full rebuild detail; `archive/`, finished paperwork |
| `tests/`, `scripts/` | Automatic checks, and one-off helper scripts that were run by hand |

## Why the result can be trusted

- **Rules fixed before the test.** Every rule was frozen at commit `348318447daa` on 6 October 2026 before the second
  half of the data was opened. Five hypotheses and their predictions were registered on 30 September.
- **Every choice on the record.** `docs/DECISIONS.md` logs each decision with its date and reason, including every
  variant run and each change made after the unlock (C1 to C3), with before and after values.
- **Primary data.** Trades are scraped from the Senate's own disclosure site, and every exclusion is counted in
  `outputs/data_quality.md`. Bloomberg prices fill the eight largest gaps in Yahoo's history of delisted stocks.
