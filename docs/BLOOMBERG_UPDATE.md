# Bloomberg price fill (2026-10-07)

_Written by Claude for the teammate who pulled the prices. The headline is NOT changed: `config/config.yaml` still has
`prices.sources: [yahoo]` (S2, S3). Using these prices in the report needs a group decision, logged in DECISIONS.md._

## What was done
1. **Pulled daily Bloomberg prices for all 8 MUST-HAVE stocks** in docs/PRICE_REQUEST.md (95% of the missing headline
   dollars) at the LBS library terminal, with Excel BDH: `PX_LAST` and `TOT_RETURN_INDEX_GROSS_DVDS`, trading days.
   The workbook is `docs/bloomberg_price_pull.xlsx` (Setup sheet: identifier, dates, checks).
2. **Fixed two identifiers.** The tickers GOGL and PARA now belong to other securities:
   - GOGL: Golden Ocean Group Ltd = `2663476D US Equity` (acquired by CMB Tech, completed 2025-08-21).
   - PARA: Paramount Global Class B = `2677689D US Equity` (acquired 2025-08-08). The first pull (`PARA US Equity`)
     returned a different security (prices 105,927 falling to 61, no dividends) and was discarded.
3. **Checked every series**: each acquired stock ends 1 day before its SEC delisting date (manual_prices_report.csv); the last
   prices match the deal terms (X 54.84 vs $55 cash, ECOM 23.09 vs $23.10, ATVI 94.42 vs $95); the large one-day
   moves are the real takeover announcements; dividends are in the total return index.
4. **Saved the files** in `data/raw/manual_prices/` (X, ECOM, ATVI, SSBK, PARA, WBA, GOGL, TOELY .csv) and recorded
   each in `data/raw/manual_prices/SOURCES.md`.
5. **Rebuilt the headline unchanged** on a Mac (Python 3.12, the pinned packages): every table matched the committed
   one (only the "files present" note and the order of two tied committee rows differ).
6. **Ran a Bloomberg-filled copy** with one change, `prices.sources: [yahoo, manual]` (Yahoo first; Bloomberg only
   where Yahoo has no price). Results in `outputs/tables/bloomberg_fill/`.

## Results: Bloomberg-filled against the headline
| Full window 2021-09 to 2026-08 | Headline (Yahoo only) | Bloomberg-filled (8 stocks) |
|---|---|---|
| Series A, a year | 10.81% | 13.41% |
| SPY | 12.69% | 12.69% |
| SPY risk-matched to A | 15.83% | 16.30% |
| CAPM alpha (OLS t) | -1.48% (-0.29) | +1.07% (0.18) |
| Carhart alpha (OLS t) | -0.74% (-0.14) | +2.26% (0.36) |
| Excess over risk-matched SPY | -4.48% | -2.58% |
| First half (2021-09 to 2024-02), series A | -0.14% | about 4.6% (from daily returns) |
| Second half (2024-03 to 2026-08), series A | 22.95% | 22.94% |

- **The conclusion does not change**: the strategy now beats plain SPY but not SPY at the same risk; no alpha is
  significant; every confirmatory verdict (H0-H4) is unchanged.
- **The gain is in the first half**: large positions in U.S. Steel, ChannelAdvisor and Activision rose on takeover bids.
- **V15 is not a bound.** V15 (ledger purchases earn SPY) gave 11.63%, below the 13.41% with real prices. The missing
  stocks were mostly takeover targets, so leaving them out UNDERSTATED the return. The limitations section should
  say so, not call V15 a bound.

## The Armstrong filing (already covered by the pre-registered checks)
Armstrong's PTR of 2026-07-21 (654 purchases, two-thirds of the second half's purchases) drives both significant
second-half tests, not the strategy:
- Ex-bulk (R2): H1 purchases -3.20% (t -2.94) -> -0.05% (t -0.08); H2 +1.75% (t 3.57) -> +1.09% (t 0.80). Same with
  Bloomberg prices (H1 -0.09%, H2 +1.07%).
- V2.2 (leave Armstrong out): series A 10.81% -> 10.55% (full), 22.95% -> 22.38% (second half).
- V4 (no bulk filings): 8.47% (full), 19.96% (second half); no significant alpha.
- Why: the portfolio is dollar-weighted and his trades sit in the smallest bands; the tests weight every trade equally.

## Next steps
1. **Decide with Harry how the Bloomberg prices enter the report**: (a) a robustness check beside the Yahoo headline
   (fits the freeze), or (b) a post-unlock correction to the headline, logged in DECISIONS.md "Post-unlock
   corrections" with the before and after values above. Then log the decision.
2. **Re-run the variants with Bloomberg prices** (`python run_variants.py`, about 8 minutes), above all V2.2
   (no Armstrong), V4 (no bulk filings) and V15, so the Armstrong and survivorship checks use the same prices.
3. **Fix the survivorship wording in the report**: the missing stocks biased the return DOWN; V15 is not a bound.
4. **Report (Phase 7)**: the full window as the main result, the second half as the check, H0-H4 with the Armstrong
   caveat (ex-bulk and V2.2 beside them), the Bloomberg fill as decided in step 1.
5. **Submission (S4)**: two zips from the final commit, then the clean-room rebuild and `sha256sum -c`.
6. **Housekeeping**: put the puller's name in SOURCES.md ("name TBC"); the remaining 177 ledger stocks are about 5%
   of the missing dollars and stay unpriced.
