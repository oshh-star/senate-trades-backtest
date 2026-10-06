# Confirmatory tests H0-H4, in-sample (2021-09-01 to 2024-02-29)

**Price sources in use** (`prices.sources`, M2): symbols priced by yahoo 1,298; 186 symbols have no prices (the survivorship ledger; their purchases are skipped, K3). CRSP or terminal price files present: 0. Price tag: **prefill**. With no CRSP or terminal file, every price is Yahoo's: under R3 (deadline 2026-10-04) Yahoo is the best available source, the survivorship gap is a stated limitation and V15 (SPY fill) bounds it.

_Built by `src/metrics/confirmatory.py` (`half_report`), from the engine's event panel and data/processed/monthly_returns.csv. The tests are the ones registered in docs/DECISIONS.md, "Out-of-sample test plan" (Q2, E55, R1, R2, R4). Event returns are the stock's minus SPY's over the same trading days; events count once each, keyed to their entry date (first trading day after disclosure), with horizons past the half's last trading day censored. t: Newey-West (3 lags) for the alphas, clustered by calendar month of entry for H1-H4 (blank below 5 entry months). p: normal; two-sided except H2 (one-sided, positive). Holm across the 7 statistics (a test that cannot be computed counts as p = 1); **verdicts use the Holm p at 5%**. Minimum detectable effect (MDE) = z x SE: nominal z 1.960 (H2 1.645), Bonferroni z 2.690 (H2 2.450) for 0.05 / 7, Holm's strictest step._

## The seven confirmatory statistics

| test   | statistic                                                                        | estimate   | SE    |     t | N (clusters)   |     p |   p Holm | MDE nominal   | MDE Bonferroni   | prediction                                                | verdict (Holm, 5%)            |
|:-------|:---------------------------------------------------------------------------------|:-----------|:------|------:|:---------------|------:|---------:|:--------------|:-----------------|:----------------------------------------------------------|:------------------------------|
| H0a    | Series A, CAPM alpha, annualised                                                 | -3.95%     | 6.65% | -0.59 | 30 months      | 0.553 |    1     | 13.04%        | 17.89%           | Not distinguishable from zero                             | not distinguishable from zero |
| H0b    | Series A, Carhart 4-factor alpha, annualised                                     | -1.86%     | 6.80% | -0.27 | 30 months      | 0.784 |    1     | 13.33%        | 18.30%           | Not distinguishable from zero                             | not distinguishable from zero |
| H1p    | Purchases: pre-disclosure drift (transaction close to entry close, SPY-adjusted) | +0.61%     | 0.57% |  1.06 | 413 (29)       | 0.289 |    1     | 1.12%         | 1.54%            | Close to zero (positive if senators trade on information) | not distinguishable from zero |
| H1s    | Sales: pre-disclosure drift                                                      | +0.33%     | 0.60% |  0.54 | 401 (26)       | 0.586 |    1     | 1.18%         | 1.62%            | Close to zero (negative if senators trade on information) | not distinguishable from zero |
| H2     | Copier purchases, 21-day SPY-adjusted return                                     | +1.16%     | 0.61% |  1.91 | 413 (29)       | 0.028 |    0.171 | 1.00%         | 1.49%            | One-sided test: is it positive?                           | not shown to be positive      |
| H3     | Sales, senator measure, 63 days: overseen minus not overseen                     | +3.95%     | 1.75% |  2.25 | 305 (24)       | 0.024 |    0.171 | 3.44%         | 4.72%            | It disappears (it was noise)                              | not distinguishable from zero |
| H4     | Purchases, copier measure, 126 days: up to $50,000 minus larger                  | +3.98%     | 2.61% |  1.52 | 231 (24)       | 0.128 |    0.641 | 5.12%         | 7.03%            | Negative if senators trade on information                 | not distinguishable from zero |

**Reading the nulls (R4: Bonferroni-level MDE).** H0a: no effect larger than ±17.89%. H0b: no effect larger than ±18.30%. H1p: no effect larger than ±1.54%. H1s: no effect larger than ±1.62%. H2: no positive effect larger than 1.49%. H3: no effect larger than ±4.72%. H4: no effect larger than ±7.03%.

## Sensitivity: without bulk filings (R2; V4 flag `bulk_ptr`, a PTR with 50 or more in-scope trades)

_Shown beside the confirmatory test, not instead of it, and not part of the Holm family (unadjusted p)._

| test   | statistic                                                                        | all events   |   t (all) |   N (all) | without bulk filings   |   t (ex-bulk) |   N (ex-bulk) |   p (ex-bulk, unadjusted) |
|:-------|:---------------------------------------------------------------------------------|:-------------|----------:|----------:|:-----------------------|--------------:|--------------:|--------------------------:|
| H1p    | Purchases: pre-disclosure drift (transaction close to entry close, SPY-adjusted) | +0.61%       |      1.06 |       413 | +1.25%                 |          1.34 |           218 |                     0.179 |
| H1s    | Sales: pre-disclosure drift                                                      | +0.33%       |      0.54 |       401 | +0.12%                 |          0.17 |           273 |                     0.863 |
| H2     | Copier purchases, 21-day SPY-adjusted return                                     | +1.16%       |      1.91 |       413 | +1.21%                 |          1.31 |           218 |                     0.095 |
| H4     | Purchases, copier measure, 126 days: up to $50,000 minus larger                  | +3.98%       |      1.52 |       231 | +3.96%                 |          1.26 |           173 |                     0.207 |

## H2 reversal check (E55 d; reported whatever H2 shows)

_Copier purchases, mean SPY-adjusted return from the entry date. "Partly reversed" = below the 21-day mean; "fully reversed" = at or below zero. Descriptive: no threshold._

|   horizon (trading days) | mean   |   t (clustered) |   N | reading                           |
|-------------------------:|:-------|----------------:|----:|:----------------------------------|
|                       21 | +1.16% |            1.91 | 413 | H2 itself                         |
|                      126 | -0.33% |           -0.2  | 231 | fully reversed (at or below zero) |
|                      252 | -2.48% |           -0.98 | 157 | fully reversed (at or below zero) |

## Calendar-year returns (each calendar year or part-year of the half)

_Monthly returns from data/processed/monthly_returns.csv compounded within each calendar year; total returns in USD. Risk-matched SPY is RF + k x (SPY - RF) with the k of the metrics run (outputs/tables/phase5_insample_results.md). NANC and KRUZ count only whole months whose previous month-end close exists for both (from March 2023, E41); where a series covers fewer months than the row, `coverage` names them._

|   year | months             | Series A (headline)   | Series B (fixed pot)   | SPY     | SPY risk-matched to A   | SPY risk-matched to B   | Senate universe, equal weight   | Market (Ken French Mkt-RF + RF)   | NANC    | KRUZ (as GOP)   | Risk-free (Ken French RF)   | coverage                              |
|-------:|:-------------------|:----------------------|:-----------------------|:--------|:------------------------|:------------------------|:--------------------------------|:----------------------------------|:--------|:----------------|:----------------------------|:--------------------------------------|
|   2021 | Sep-Dec (4 months) | -0.00%                | +0.08%                 | +5.89%  | +8.05%                  | +3.92%                  | +2.22%                          | +3.58%                            |         |                 | +0.01%                      |                                       |
|   2022 | full year          | -21.40%               | -5.57%                 | -18.18% | -25.95%                 | -11.34%                 | -16.89%                         | -19.92%                           |         |                 | +1.41%                      |                                       |
|   2023 | full year          | +24.00%               | +19.86%                | +26.18% | +34.92%                 | +18.68%                 | +21.49%                         | +26.69%                           | +27.30% | +13.74%         | +4.94%                      | NANC: Mar-Dec; KRUZ (as GOP): Mar-Dec |
|   2024 | Jan-Feb (2 months) | +2.26%                | +2.27%                 | +6.89%  | +9.30%                  | +4.81%                  | +7.01%                          | +6.76%                            | +8.76%  | +5.35%          | +0.89%                      |                                       |

## Worst rolling 12 months (compounded monthly returns)

_The worst 12 consecutive calendar months of each series, with the other's return over the same months._

| series              | from    | to      | return   | series A, same months   | SPY, same months   |   12-month windows in the half |
|:--------------------|:--------|:--------|:---------|:------------------------|:-------------------|-------------------------------:|
| Series A (headline) | 2021-11 | 2022-10 | -22.93%  | -22.93%                 | -14.63%            |                             19 |
| SPY                 | 2022-01 | 2022-12 | -18.18%  | -21.40%                 | -18.18%            |                             19 |
