# Phase 5: event study (in-sample, entry dates 2021-09-01 to 2024-02-29)

_From `data/processed/event_panel.csv`. Returns are SPY-adjusted (stock minus SPY over exactly the same trading days, total returns). t-statistics use standard errors clustered by calendar month of entry; the iid t is shown for comparison. Horizons past the last in-sample day are censored, so N falls with the horizon._

**Sign convention: every number is the STOCK's return minus SPY's, whatever the side. After a PURCHASE a positive mean means the stock beat SPY (an informative purchase). After a SALE a NEGATIVE mean means the stock trailed SPY (an informative sale).**

- *senator*: from the close on the transaction date (the first trading day on or after it).
- *copier*: from the close on the entry date (the first trading day after the disclosure).
- *gap*: senator minus copier, event by event, on events with both; what the disclosure delay costs (for sales, a negative gap means the senator sold before a fall the copier partly missed).
- *pre-disclosure move*: SPY-adjusted return from the transaction-date close to the entry-date close.

## Purchases

|   horizon (trading days) | version                                                | mean   | median   |   N |   months (clusters) |   t (clustered by entry month) |   t (iid) |
|-------------------------:|:-------------------------------------------------------|:-------|:---------|----:|--------------------:|-------------------------------:|----------:|
|                        0 | pre-disclosure move (transaction close to entry close) | 0.61%  | -0.25%   | 413 |                  29 |                           1.06 |      1.3  |
|                        5 | senator (from transaction date)                        | 0.01%  | -0.03%   | 413 |                  29 |                           0.03 |      0.03 |
|                        5 | copier (from entry date)                               | 0.28%  | -0.18%   | 413 |                  29 |                           0.87 |      1.28 |
|                        5 | gap (senator minus copier)                             | -0.27% | -0.18%   | 413 |                  29 |                          -0.72 |     -0.93 |
|                       21 | senator (from transaction date)                        | 0.68%  | 0.08%    | 413 |                  29 |                           1.3  |      1.56 |
|                       21 | copier (from entry date)                               | 1.16%  | 0.24%    | 413 |                  29 |                           1.91 |      2.35 |
|                       21 | gap (senator minus copier)                             | -0.48% | -0.28%   | 413 |                  29 |                          -0.59 |     -0.74 |
|                       63 | senator (from transaction date)                        | 0.44%  | 0.14%    | 388 |                  28 |                           0.62 |      0.58 |
|                       63 | copier (from entry date)                               | 0.32%  | -0.86%   | 386 |                  27 |                           0.27 |      0.43 |
|                       63 | gap (senator minus copier)                             | 0.15%  | 0.22%    | 386 |                  27 |                           0.18 |      0.22 |
|                      126 | senator (from transaction date)                        | -0.69% | -1.56%   | 232 |                  25 |                          -0.45 |     -0.54 |
|                      126 | copier (from entry date)                               | -0.33% | -2.61%   | 231 |                  24 |                          -0.2  |     -0.25 |
|                      126 | gap (senator minus copier)                             | -0.34% | 0.21%    | 231 |                  24 |                          -0.3  |     -0.36 |
|                      252 | senator (from transaction date)                        | -2.64% | -5.30%   | 161 |                  20 |                          -1.11 |     -1.2  |
|                      252 | copier (from entry date)                               | -2.48% | -6.66%   | 157 |                  18 |                          -0.98 |     -0.98 |
|                      252 | gap (senator minus copier)                             | -0.43% | 0.27%    | 157 |                  18 |                          -0.3  |     -0.39 |

## Sales

|   horizon (trading days) | version                                                | mean   | median   |   N |   months (clusters) |   t (clustered by entry month) |   t (iid) |
|-------------------------:|:-------------------------------------------------------|:-------|:---------|----:|--------------------:|-------------------------------:|----------:|
|                        0 | pre-disclosure move (transaction close to entry close) | 0.33%  | -0.26%   | 401 |                  26 |                           0.54 |      0.75 |
|                        5 | senator (from transaction date)                        | -0.01% | -0.20%   | 401 |                  26 |                          -0.02 |     -0.03 |
|                        5 | copier (from entry date)                               | -0.08% | 0.12%    | 401 |                  26 |                          -0.4  |     -0.45 |
|                        5 | gap (senator minus copier)                             | 0.08%  | -0.00%   | 401 |                  26 |                           0.28 |      0.31 |
|                       21 | senator (from transaction date)                        | 0.06%  | -0.15%   | 401 |                  26 |                           0.12 |      0.13 |
|                       21 | copier (from entry date)                               | -0.27% | -0.57%   | 359 |                  25 |                          -0.48 |     -0.58 |
|                       21 | gap (senator minus copier)                             | 0.18%  | 0.52%    | 359 |                  25 |                           0.3  |      0.28 |
|                       63 | senator (from transaction date)                        | 0.11%  | -0.40%   | 314 |                  24 |                           0.09 |      0.13 |
|                       63 | copier (from entry date)                               | 0.88%  | -0.13%   | 312 |                  23 |                           1.05 |      1    |
|                       63 | gap (senator minus copier)                             | -0.75% | 0.09%    | 312 |                  23 |                          -0.67 |     -1    |
|                      126 | senator (from transaction date)                        | 0.95%  | -1.01%   | 262 |                  21 |                           0.47 |      0.63 |
|                      126 | copier (from entry date)                               | 0.07%  | -0.92%   | 227 |                  20 |                           0.03 |      0.04 |
|                      126 | gap (senator minus copier)                             | 1.13%  | 0.06%    | 227 |                  20 |                           1.01 |      1.3  |
|                      252 | senator (from transaction date)                        | 0.22%  | -2.75%   | 191 |                  17 |                           0.09 |      0.09 |
|                      252 | copier (from entry date)                               | -1.52% | -2.38%   | 189 |                  15 |                          -0.63 |     -0.62 |
|                      252 | gap (senator minus copier)                             | 1.74%  | 0.89%    | 189 |                  15 |                           1.43 |      2.19 |
