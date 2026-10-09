# Confirmatory tests H0-H4, out-of-sample (2024-03-01 to 2026-08-31)

**Price sources in use** (`prices.sources`, M2): symbols priced by manual 8, yahoo 1,298; 178 symbols have no prices (the survivorship ledger; their purchases are skipped, K3). CRSP or terminal price files present: 8 (ATVI.csv, ECOM.csv, GOGL.csv, PARA.csv, SSBK.csv, TOELY.csv, WBA.csv, X.csv). Price tag: **bloomberg**. Since C1 (2026-10-09) the headline is Yahoo with the Bloomberg terminal files where Yahoo has no price; a CRSP file could only ever feed variant V20, never the headline (S3). The remaining survivorship gap is a stated limitation; V15 (SPY fill) shows its size but is not a bound (the priced ledger stocks beat SPY).

_Built by `src/metrics/confirmatory.py` (`half_report`), from the engine's event panel and data/processed/monthly_returns.csv. The tests are the ones registered in docs/DECISIONS.md, "Out-of-sample test plan" (Q2, E55, R1, R2, R4). Event returns are the stock's minus SPY's over the same trading days; events count once each, keyed to their entry date (first trading day after disclosure), with horizons past the half's last trading day censored. t: Newey-West (3 lags) for the alphas, clustered by calendar month of entry for H1-H4 (blank below 5 entry months). p: normal; two-sided except H2 (one-sided, positive). Holm across the 7 statistics (a test that cannot be computed counts as p = 1); **verdicts use the Holm p at 5%**. Minimum detectable effect (MDE) = z x SE: nominal z 1.960 (H2 1.645), Bonferroni z 2.690 (H2 2.450) for 0.05 / 7, Holm's strictest step._

## The seven confirmatory statistics

| test   | statistic                                                                        | estimate   | SE    |     t | N (clusters)   | p      |   p Holm | MDE nominal   | MDE Bonferroni   | prediction                                                | verdict (Holm, 5%)            |
|:-------|:---------------------------------------------------------------------------------|:-----------|:------|------:|:---------------|:-------|---------:|:--------------|:-----------------|:----------------------------------------------------------|:------------------------------|
| H0a    | Series A, CAPM alpha, annualised                                                 | +1.69%     | 5.87% |  0.29 | 30 months      | 0.774  |    1     | 11.51%        | 15.79%           | Not distinguishable from zero                             | not distinguishable from zero |
| H0b    | Series A, Carhart 4-factor alpha, annualised                                     | +0.40%     | 7.12% |  0.06 | 30 months      | 0.955  |    1     | 13.96%        | 19.16%           | Not distinguishable from zero                             | not distinguishable from zero |
| H1p    | Purchases: pre-disclosure drift (transaction close to entry close, SPY-adjusted) | -3.22%     | 1.08% | -2.98 | 962 (30)       | 0.003  |    0.017 | 2.12%         | 2.90%            | Close to zero (positive if senators trade on information) | significantly negative        |
| H1s    | Sales: pre-disclosure drift                                                      | -0.99%     | 1.03% | -0.96 | 504 (29)       | 0.336  |    1     | 2.01%         | 2.76%            | Close to zero (negative if senators trade on information) | not distinguishable from zero |
| H2     | Copier purchases, 21-day SPY-adjusted return                                     | +1.74%     | 0.49% |  3.54 | 956 (29)       | <0.001 |    0.001 | 0.81%         | 1.20%            | One-sided test: is it positive?                           | positive (significant)        |
| H3     | Sales, senator measure, 63 days: overseen minus not overseen                     | +6.16%     | 6.55% |  0.94 | 404 (29)       | 0.347  |    1     | 12.83%        | 17.61%           | It disappears (it was noise)                              | not distinguishable from zero |
| H4     | Purchases, copier measure, 126 days: up to $50,000 minus larger                  | +4.82%     | 5.01% |  0.96 | 273 (24)       | 0.335  |    1     | 9.81%         | 13.47%           | Negative if senators trade on information                 | not distinguishable from zero |

**Reading the nulls (R4: Bonferroni-level MDE).** H0a: no effect larger than ±15.79%. H0b: no effect larger than ±19.16%. H1s: no effect larger than ±2.76%. H3: no effect larger than ±17.61%. H4: no effect larger than ±13.47%.

## Sensitivity: without bulk filings (R2; V4 flag `bulk_ptr`, a PTR with 50 or more in-scope trades)

_Shown beside the confirmatory test, not instead of it, and not part of the Holm family (unadjusted p)._

| test   | statistic                                                                        | all events   |   t (all) |   N (all) | without bulk filings   |   t (ex-bulk) |   N (ex-bulk) |   p (ex-bulk, unadjusted) |
|:-------|:---------------------------------------------------------------------------------|:-------------|----------:|----------:|:-----------------------|--------------:|--------------:|--------------------------:|
| H1p    | Purchases: pre-disclosure drift (transaction close to entry close, SPY-adjusted) | -3.22%       |     -2.98 |       962 | -0.11%                 |         -0.18 |           314 |                     0.855 |
| H1s    | Sales: pre-disclosure drift                                                      | -0.99%       |     -0.96 |       504 | +0.68%                 |          1.22 |           389 |                     0.222 |
| H2     | Copier purchases, 21-day SPY-adjusted return                                     | +1.74%       |      3.54 |       956 | +1.12%                 |          0.81 |           307 |                     0.208 |
| H4     | Purchases, copier measure, 126 days: up to $50,000 minus larger                  | +4.82%       |      0.96 |       273 | +1.72%                 |          0.41 |           269 |                     0.685 |

## H2 reversal check (E55 d; reported whatever H2 shows)

_Copier purchases, mean SPY-adjusted return from the entry date. "Partly reversed" = below the 21-day mean; "fully reversed" = at or below zero. Descriptive: no threshold._

|   horizon (trading days) | mean    |   t (clustered) |   N | reading                                 |
|-------------------------:|:--------|----------------:|----:|:----------------------------------------|
|                       21 | +1.74%  |            3.54 | 956 | H2 itself                               |
|                      126 | +1.73%  |            0.77 | 273 | partly reversed (below the 21-day mean) |
|                      252 | +12.03% |            2.01 | 166 | not reversed                            |

## Calendar-year returns (each calendar year or part-year of the half)

_Monthly returns from data/processed/monthly_returns.csv compounded within each calendar year; total returns in USD. Risk-matched SPY is RF + k x (SPY - RF) with the k of the metrics run (outputs/tables/phase5_insample_results.md). NANC and KRUZ count only whole months whose previous month-end close exists for both (from March 2023, E41); where a series covers fewer months than the row, `coverage` names them._

|   year | months              | Series A (headline)   | Series B (fixed pot)   | SPY     | SPY risk-matched to A   | SPY risk-matched to B   | Senate universe, equal weight   | Market (Ken French Mkt-RF + RF)   | NANC    | KRUZ (as GOP)   | Risk-free (Ken French RF)   | coverage   |
|-------:|:--------------------|:----------------------|:-----------------------|:--------|:------------------------|:------------------------|:--------------------------------|:----------------------------------|:--------|:----------------|:----------------------------|:-----------|
|   2024 | Mar-Dec (10 months) | +3.39%                | +3.54%                 | +16.83% | +22.46%                 | +13.44%                 | +9.85%                          | +17.11%                           | +16.61% | +8.64%          | +4.32%                      |            |
|   2025 | full year           | +27.88%               | +13.65%                | +17.72% | +23.77%                 | +14.07%                 | +29.79%                         | +17.54%                           | +18.54% | +17.11%         | +4.25%                      |            |
|   2026 | Jan-Aug (8 months)  | +26.76%               | +16.13%                | +13.08% | +17.61%                 | +10.27%                 | +17.97%                         | +12.75%                           | +13.31% | +21.70%         | +2.40%                      |            |

## Worst rolling 12 months (compounded monthly returns)

_The worst 12 consecutive calendar months of each series, with the other's return over the same months._

| series              | from    | to      | return   | series A, same months   | SPY, same months   |   12-month windows in the half |
|:--------------------|:--------|:--------|:---------|:------------------------|:-------------------|-------------------------------:|
| Series A (headline) | 2024-04 | 2025-03 | -3.27%   | -3.27%                  | +8.30%             |                             19 |
| SPY                 | 2024-04 | 2025-03 | +8.30%   | -3.27%                  | +8.30%             |                             19 |
