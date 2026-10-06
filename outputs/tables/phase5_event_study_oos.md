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
|                        0 | pre-disclosure move (transaction close to entry close) | -3.20% | -3.69%   | 959 |                  30 |                          -2.94 |     -4.16 |
|                        5 | senator (from transaction date)                        | -0.11% | -0.07%   | 959 |                  30 |                          -0.91 |     -0.78 |
|                        5 | copier (from entry date)                               | 2.66%  | 2.27%    | 959 |                  30 |                           3.11 |     10.38 |
|                        5 | gap (senator minus copier)                             | -2.77% | -2.93%   | 959 |                  30 |                          -3.25 |     -8.44 |
|                       21 | senator (from transaction date)                        | -3.81% | -4.06%   | 959 |                  30 |                          -2.97 |     -9.61 |
|                       21 | copier (from entry date)                               | 1.75%  | 0.13%    | 951 |                  29 |                           3.57 |      4.64 |
|                       21 | gap (senator minus copier)                             | -5.56% | -4.34%   | 951 |                  29 |                          -3.57 |     -9.45 |
|                       63 | senator (from transaction date)                        | -2.11% | -4.54%   | 944 |                  30 |                          -1.5  |     -2.11 |
|                       63 | copier (from entry date)                               | 3.52%  | 0.36%    | 294 |                  27 |                           1.65 |      2.6  |
|                       63 | gap (senator minus copier)                             | -1.56% | -0.19%   | 294 |                  27 |                          -0.86 |     -1.47 |
|                      126 | senator (from transaction date)                        | 2.59%  | 0.03%    | 286 |                  27 |                           1.31 |      1.59 |
|                      126 | copier (from entry date)                               | 1.99%  | 0.32%    | 269 |                  24 |                           0.84 |      1.32 |
|                      126 | gap (senator minus copier)                             | 0.35%  | 0.01%    | 269 |                  24 |                           0.29 |      0.32 |
|                      252 | senator (from transaction date)                        | 10.23% | -0.07%   | 170 |                  20 |                           2.66 |      2.58 |
|                      252 | copier (from entry date)                               | 12.70% | -0.46%   | 162 |                  18 |                           2.14 |      2.63 |
|                      252 | gap (senator minus copier)                             | -3.75% | -0.78%   | 162 |                  18 |                          -1.06 |     -1.8  |

## Sales

|   horizon (trading days) | version                                                | mean   | median   |   N |   months (clusters) |   t (clustered by entry month) |   t (iid) |
|-------------------------:|:-------------------------------------------------------|:-------|:---------|----:|--------------------:|-------------------------------:|----------:|
|                        0 | pre-disclosure move (transaction close to entry close) | -0.95% | -0.68%   | 500 |                  29 |                          -0.94 |     -1.62 |
|                        5 | senator (from transaction date)                        | -0.02% | -0.09%   | 500 |                  29 |                          -0.08 |     -0.1  |
|                        5 | copier (from entry date)                               | 0.38%  | 0.09%    | 500 |                  29 |                           0.63 |      1.57 |
|                        5 | gap (senator minus copier)                             | -0.40% | -0.22%   | 500 |                  29 |                          -0.54 |     -1.31 |
|                       21 | senator (from transaction date)                        | -0.47% | -0.80%   | 500 |                  29 |                          -0.53 |     -0.91 |
|                       21 | copier (from entry date)                               | 0.94%  | 0.13%    | 478 |                  28 |                           1.38 |      2.1  |
|                       21 | gap (senator minus copier)                             | -1.42% | -0.94%   | 478 |                  28 |                          -1.03 |     -2.19 |
|                       63 | senator (from transaction date)                        | -0.19% | -1.51%   | 476 |                  29 |                          -0.16 |     -0.19 |
|                       63 | copier (from entry date)                               | 1.80%  | 0.00%    | 398 |                  26 |                           1.36 |      1.72 |
|                       63 | gap (senator minus copier)                             | -0.92% | -1.28%   | 398 |                  26 |                          -1.44 |     -1    |
|                      126 | senator (from transaction date)                        | 3.26%  | -0.16%   | 408 |                  26 |                           1.18 |      1.84 |
|                      126 | copier (from entry date)                               | 2.41%  | 0.64%    | 375 |                  23 |                           0.91 |      1.41 |
|                      126 | gap (senator minus copier)                             | 0.18%  | 0.19%    | 375 |                  23 |                           0.21 |      0.21 |
|                      252 | senator (from transaction date)                        | 3.32%  | -5.25%   | 309 |                  22 |                           0.54 |      0.7  |
|                      252 | copier (from entry date)                               | 0.21%  | -6.67%   | 283 |                  17 |                           0.04 |      0.05 |
|                      252 | gap (senator minus copier)                             | 0.84%  | -0.33%   | 283 |                  17 |                           0.78 |      0.85 |
