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
|                        0 | pre-disclosure move (transaction close to entry close) | -2.06% | -2.07%   | 1392 |                  59 |                          -1.6  |     -3.73 |
|                        5 | senator (from transaction date)                        | -0.08% | -0.05%   | 1392 |                  59 |                          -0.71 |     -0.64 |
|                        5 | copier (from entry date)                               | 1.91%  | 1.18%    | 1396 |                  59 |                           2.09 |      9.98 |
|                        5 | gap (senator minus copier)                             | -2.02% | -1.63%   | 1392 |                  59 |                          -2.15 |     -8.21 |
|                       21 | senator (from transaction date)                        | -2.44% | -2.62%   | 1392 |                  59 |                          -1.61 |     -7.89 |
|                       21 | copier (from entry date)                               | 1.56%  | 0.13%    | 1388 |                  58 |                           3.69 |      5.13 |
|                       21 | gap (senator minus copier)                             | -4.01% | -3.25%   | 1384 |                  58 |                          -2.25 |     -8.78 |
|                       63 | senator (from transaction date)                        | -1.28% | -3.00%   | 1377 |                  59 |                          -0.94 |     -1.76 |
|                       63 | copier (from entry date)                               | 1.91%  | -0.07%   |  730 |                  56 |                           1.93 |      2.69 |
|                       63 | gap (senator minus copier)                             | -0.82% | -0.17%   |  727 |                  56 |                          -0.98 |     -1.38 |
|                      126 | senator (from transaction date)                        | 2.06%  | 0.13%    |  719 |                  56 |                           2.11 |      2.24 |
|                      126 | copier (from entry date)                               | 1.66%  | -0.32%   |  705 |                  53 |                           1.59 |      1.92 |
|                      126 | gap (senator minus copier)                             | 0.25%  | -0.01%   |  702 |                  53 |                           0.37 |      0.41 |
|                      252 | senator (from transaction date)                        | 2.55%  | -4.46%   |  603 |                  49 |                           1.39 |      1.49 |
|                      252 | copier (from entry date)                               | 1.77%  | -4.77%   |  598 |                  47 |                           0.67 |      0.97 |
|                      252 | gap (senator minus copier)                             | 0.24%  | -0.12%   |  595 |                  47 |                           0.16 |      0.26 |

## Sales

|   horizon (trading days) | version                                                | mean   | median   |   N |   months (clusters) |   t (clustered by entry month) |   t (iid) |
|-------------------------:|:-------------------------------------------------------|:-------|:---------|----:|--------------------:|-------------------------------:|----------:|
|                        0 | pre-disclosure move (transaction close to entry close) | -0.54% | -0.58%   | 936 |                  56 |                          -0.85 |     -1.46 |
|                        5 | senator (from transaction date)                        | 0.00%  | -0.12%   | 936 |                  56 |                           0.01 |      0.02 |
|                        5 | copier (from entry date)                               | 0.09%  | 0.04%    | 936 |                  56 |                           0.26 |      0.6  |
|                        5 | gap (senator minus copier)                             | -0.09% | -0.02%   | 936 |                  56 |                          -0.21 |     -0.45 |
|                       21 | senator (from transaction date)                        | -0.36% | -0.64%   | 936 |                  56 |                          -0.69 |     -1.04 |
|                       21 | copier (from entry date)                               | 0.15%  | -0.32%   | 914 |                  55 |                           0.27 |      0.46 |
|                       21 | gap (senator minus copier)                             | -0.51% | -0.21%   | 914 |                  55 |                          -0.59 |     -1.14 |
|                       63 | senator (from transaction date)                        | -0.41% | -1.31%   | 912 |                  56 |                          -0.52 |     -0.68 |
|                       63 | copier (from entry date)                               | 0.95%  | -0.11%   | 834 |                  53 |                           1.27 |      1.49 |
|                       63 | gap (senator minus copier)                             | -0.87% | -0.98%   | 834 |                  53 |                          -1.56 |     -1.58 |
|                      126 | senator (from transaction date)                        | 1.16%  | -1.19%   | 844 |                  53 |                           0.74 |      1.11 |
|                      126 | copier (from entry date)                               | 0.86%  | 0.00%    | 811 |                  50 |                           0.63 |      0.89 |
|                      126 | gap (senator minus copier)                             | -0.09% | -0.08%   | 811 |                  50 |                          -0.16 |     -0.17 |
|                      252 | senator (from transaction date)                        | -0.54% | -4.06%   | 745 |                  49 |                          -0.19 |     -0.25 |
|                      252 | copier (from entry date)                               | -1.78% | -4.22%   | 719 |                  44 |                          -0.77 |     -0.96 |
|                      252 | gap (senator minus copier)                             | 0.20%  | -0.29%   | 719 |                  44 |                           0.27 |      0.36 |
