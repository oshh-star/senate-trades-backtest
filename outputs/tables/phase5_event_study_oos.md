# Phase 5B: event study (out-of-sample half, entry dates 2024-03-01 to 2026-08-31)

**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, "Out-of-sample test plan"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few cells in a table like this one will reach |t| = 2 by chance.**

_From `data/processed/event_panel.csv`. Returns are SPY-adjusted (stock minus SPY over exactly the same trading days, total returns). t-statistics use standard errors clustered by calendar month of entry; the iid t is shown for comparison. Horizons past the last day of the sample are censored, so N falls with the horizon._

**Sign convention: every number is the STOCK's return minus SPY's, whatever the side. After a PURCHASE a positive mean means the stock beat SPY (an informative purchase). After a SALE a NEGATIVE mean means the stock trailed SPY (an informative sale).**

- *senator*: from the close on the transaction date (the first trading day on or after it).
- *copier*: from the close on the entry date (the first trading day after the disclosure).
- *gap*: senator minus copier, event by event, on events with both; what the disclosure delay costs (for sales, a negative gap means the senator sold before a fall the copier partly missed).
- *pre-disclosure move*: SPY-adjusted return from the transaction-date close to the entry-date close.

## Purchases

|   horizon (trading days) | version                                                | mean   | median   |   N |   months (clusters) |   t (clustered by entry month) |   t (iid) |
|-------------------------:|:-------------------------------------------------------|:-------|:---------|----:|--------------------:|-------------------------------:|----------:|
|                        0 | pre-disclosure move (transaction close to entry close) | -3.22% | -3.70%   | 962 |                  30 |                          -2.98 |     -4.18 |
|                        5 | senator (from transaction date)                        | -0.11% | -0.07%   | 962 |                  30 |                          -0.86 |     -0.73 |
|                        5 | copier (from entry date)                               | 2.65%  | 2.27%    | 964 |                  30 |                           3.17 |     10.28 |
|                        5 | gap (senator minus copier)                             | -2.79% | -2.93%   | 962 |                  30 |                          -3.3  |     -8.49 |
|                       21 | senator (from transaction date)                        | -3.79% | -4.06%   | 962 |                  30 |                          -2.95 |     -9.59 |
|                       21 | copier (from entry date)                               | 1.74%  | 0.13%    | 956 |                  29 |                           3.54 |      4.61 |
|                       21 | gap (senator minus copier)                             | -5.55% | -4.32%   | 954 |                  29 |                          -3.55 |     -9.46 |
|                       63 | senator (from transaction date)                        | -2.15% | -4.54%   | 947 |                  30 |                          -1.56 |     -2.16 |
|                       63 | copier (from entry date)                               | 3.32%  | 0.34%    | 298 |                  27 |                           1.69 |      2.46 |
|                       63 | gap (senator minus copier)                             | -1.55% | -0.17%   | 297 |                  27 |                          -0.86 |     -1.47 |
|                      126 | senator (from transaction date)                        | 2.33%  | 0.03%    | 289 |                  27 |                           1.23 |      1.42 |
|                      126 | copier (from entry date)                               | 1.73%  | 0.29%    | 273 |                  24 |                           0.77 |      1.15 |
|                      126 | gap (senator minus copier)                             | 0.28%  | 0.00%    | 272 |                  24 |                           0.23 |      0.26 |
|                      252 | senator (from transaction date)                        | 9.77%  | -0.15%   | 173 |                  20 |                           2.54 |      2.5  |
|                      252 | copier (from entry date)                               | 12.03% | -0.46%   | 166 |                  18 |                           2.01 |      2.54 |
|                      252 | gap (senator minus copier)                             | -3.88% | -0.84%   | 165 |                  18 |                          -1.12 |     -1.89 |

## Sales

|   horizon (trading days) | version                                                | mean   | median   |   N |   months (clusters) |   t (clustered by entry month) |   t (iid) |
|-------------------------:|:-------------------------------------------------------|:-------|:---------|----:|--------------------:|-------------------------------:|----------:|
|                        0 | pre-disclosure move (transaction close to entry close) | -0.99% | -0.68%   | 504 |                  29 |                          -0.96 |     -1.69 |
|                        5 | senator (from transaction date)                        | -0.03% | -0.09%   | 504 |                  29 |                          -0.13 |     -0.16 |
|                        5 | copier (from entry date)                               | 0.34%  | 0.09%    | 504 |                  29 |                           0.56 |      1.4  |
|                        5 | gap (senator minus copier)                             | -0.37% | -0.21%   | 504 |                  29 |                          -0.5  |     -1.21 |
|                       21 | senator (from transaction date)                        | -0.52% | -0.85%   | 504 |                  29 |                          -0.6  |     -1.02 |
|                       21 | copier (from entry date)                               | 0.87%  | 0.09%    | 482 |                  28 |                           1.17 |      1.95 |
|                       21 | gap (senator minus copier)                             | -1.41% | -0.88%   | 482 |                  28 |                          -1    |     -2.18 |
|                       63 | senator (from transaction date)                        | -0.31% | -1.60%   | 480 |                  29 |                          -0.25 |     -0.32 |
|                       63 | copier (from entry date)                               | 1.64%  | 0.00%    | 402 |                  26 |                           1.22 |      1.57 |
|                       63 | gap (senator minus copier)                             | -0.91% | -1.23%   | 402 |                  26 |                          -1.46 |     -1    |
|                      126 | senator (from transaction date)                        | 2.95%  | -0.24%   | 412 |                  26 |                           1.05 |      1.67 |
|                      126 | copier (from entry date)                               | 2.20%  | 0.64%    | 379 |                  23 |                           0.83 |      1.3  |
|                      126 | gap (senator minus copier)                             | 0.06%  | 0.17%    | 379 |                  23 |                           0.07 |      0.07 |
|                      252 | senator (from transaction date)                        | 2.99%  | -5.67%   | 313 |                  22 |                           0.49 |      0.64 |
|                      252 | copier (from entry date)                               | -0.02% | -6.67%   | 287 |                  17 |                          -0    |     -0.01 |
|                      252 | gap (senator minus copier)                             | 0.74%  | -0.29%   | 287 |                  17 |                           0.68 |      0.74 |
