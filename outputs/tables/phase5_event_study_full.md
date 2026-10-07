# Phase 5B: event study (full window, entry dates 2021-09-01 to 2026-08-31)

**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, "Out-of-sample test plan"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few cells in a table like this one will reach |t| = 2 by chance.**

_From `data/processed/event_panel.csv`. Returns are SPY-adjusted (stock minus SPY over exactly the same trading days, total returns). t-statistics use standard errors clustered by calendar month of entry; the iid t is shown for comparison. Horizons past the last day of the sample are censored, so N falls with the horizon._

**Sign convention: every number is the STOCK's return minus SPY's, whatever the side. After a PURCHASE a positive mean means the stock beat SPY (an informative purchase). After a SALE a NEGATIVE mean means the stock trailed SPY (an informative sale).**

- *senator*: from the close on the transaction date (the first trading day on or after it).
- *copier*: from the close on the entry date (the first trading day after the disclosure).
- *gap*: senator minus copier, event by event, on events with both; what the disclosure delay costs (for sales, a negative gap means the senator sold before a fall the copier partly missed).
- *pre-disclosure move*: SPY-adjusted return from the transaction-date close to the entry-date close.

## Purchases

|   horizon (trading days) | version                                                | mean   | median   |    N |   months (clusters) |   t (clustered by entry month) |   t (iid) |
|-------------------------:|:-------------------------------------------------------|:-------|:---------|-----:|--------------------:|-------------------------------:|----------:|
|                        0 | pre-disclosure move (transaction close to entry close) | -2.06% | -2.05%   | 1372 |                  59 |                          -1.57 |     -3.68 |
|                        5 | senator (from transaction date)                        | -0.08% | -0.05%   | 1372 |                  59 |                          -0.72 |     -0.66 |
|                        5 | copier (from entry date)                               | 1.94%  | 1.19%    | 1372 |                  59 |                           2.07 |     10.07 |
|                        5 | gap (senator minus copier)                             | -2.02% | -1.63%   | 1372 |                  59 |                          -2.13 |     -8.15 |
|                       21 | senator (from transaction date)                        | -2.46% | -2.62%   | 1372 |                  59 |                          -1.6  |     -7.89 |
|                       21 | copier (from entry date)                               | 1.57%  | 0.19%    | 1364 |                  58 |                           3.74 |      5.19 |
|                       21 | gap (senator minus copier)                             | -4.02% | -3.17%   | 1364 |                  58 |                          -2.23 |     -8.77 |
|                       63 | senator (from transaction date)                        | -1.25% | -3.01%   | 1357 |                  59 |                          -0.9  |     -1.7  |
|                       63 | copier (from entry date)                               | 1.98%  | -0.05%   |  707 |                  56 |                           1.9  |      2.77 |
|                       63 | gap (senator minus copier)                             | -0.74% | -0.13%   |  707 |                  56 |                          -0.88 |     -1.24 |
|                      126 | senator (from transaction date)                        | 1.88%  | 0.11%    |  699 |                  56 |                           1.82 |      2.08 |
|                      126 | copier (from entry date)                               | 1.47%  | -0.31%   |  682 |                  53 |                           1.33 |      1.73 |
|                      126 | gap (senator minus copier)                             | 0.30%  | 0.00%    |  682 |                  53 |                           0.45 |      0.5  |
|                      252 | senator (from transaction date)                        | 2.80%  | -4.51%   |  583 |                  49 |                           1.43 |      1.62 |
|                      252 | copier (from entry date)                               | 2.06%  | -4.77%   |  575 |                  47 |                           0.77 |      1.11 |
|                      252 | gap (senator minus copier)                             | 0.27%  | -0.11%   |  575 |                  47 |                           0.17 |      0.29 |

## Sales

|   horizon (trading days) | version                                                | mean   | median   |   N |   months (clusters) |   t (clustered by entry month) |   t (iid) |
|-------------------------:|:-------------------------------------------------------|:-------|:---------|----:|--------------------:|-------------------------------:|----------:|
|                        0 | pre-disclosure move (transaction close to entry close) | -0.38% | -0.41%   | 901 |                  55 |                          -0.58 |     -1    |
|                        5 | senator (from transaction date)                        | -0.01% | -0.11%   | 901 |                  55 |                          -0.08 |     -0.1  |
|                        5 | copier (from entry date)                               | 0.18%  | 0.09%    | 901 |                  55 |                           0.5  |      1.12 |
|                        5 | gap (senator minus copier)                             | -0.19% | -0.14%   | 901 |                  55 |                          -0.43 |     -0.93 |
|                       21 | senator (from transaction date)                        | -0.23% | -0.48%   | 901 |                  55 |                          -0.43 |     -0.65 |
|                       21 | copier (from entry date)                               | 0.37%  | -0.02%   | 879 |                  54 |                           0.82 |      1.19 |
|                       21 | gap (senator minus copier)                             | -0.61% | -0.20%   | 879 |                  54 |                          -0.73 |     -1.35 |
|                       63 | senator (from transaction date)                        | -0.05% | -0.97%   | 877 |                  55 |                          -0.06 |     -0.08 |
|                       63 | copier (from entry date)                               | 1.14%  | -0.11%   | 799 |                  52 |                           1.58 |      1.76 |
|                       63 | gap (senator minus copier)                             | -0.64% | -0.86%   | 799 |                  52 |                          -1.16 |     -1.14 |
|                      126 | senator (from transaction date)                        | 1.24%  | -1.12%   | 809 |                  52 |                           0.78 |      1.15 |
|                      126 | copier (from entry date)                               | 0.43%  | -0.48%   | 776 |                  49 |                           0.31 |      0.43 |
|                      126 | gap (senator minus copier)                             | 0.40%  | 0.01%    | 776 |                  49 |                           0.6  |      0.69 |
|                      252 | senator (from transaction date)                        | -1.09% | -5.50%   | 710 |                  48 |                          -0.38 |     -0.48 |
|                      252 | copier (from entry date)                               | -2.62% | -5.45%   | 684 |                  43 |                          -1.11 |     -1.35 |
|                      252 | gap (senator minus copier)                             | 0.43%  | -0.13%   | 684 |                  43 |                           0.64 |      0.75 |
