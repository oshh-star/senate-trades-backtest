# Phase 5B: pre-disclosure drift (full window, entry dates 2021-09-01 to 2026-08-31)

**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, "Out-of-sample test plan"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few cells in a table like this one will reach |t| = 2 by chance.**

_What the disclosure lag costs a copier: the stock's return minus SPY's from the close on the TRANSACTION date (the senator's trade; the first trading day on or after it) to the close on the ENTRY date (the first trading day after the disclosure, when the copier acts). Every in-scope purchase and sale record with an entry date in the sample and prices on both dates counts once. t-statistics cluster by calendar month of entry. From `data/processed/event_panel.csv` (column gap_x)._

**Sign convention.** The drift is the stock's move, whatever the side. For a PURCHASE a positive drift means the price ran up before the copier could buy (a cost). For a SALE a negative drift means the price fell before the copier could sell (a cost). "Mean cost to the copier" flips the sign for sales so that positive always means the lag hurt the copier.

| side     |    N |   months (clusters) | mean SPY-adjusted drift   | median SPY-adjusted drift   |   t (clustered by entry month) |   t (iid) | mean stock return   | mean SPY return   |   median lag (trading days) | mean cost to the copier   | share of events against the copier   |
|:---------|-----:|--------------------:|:--------------------------|:----------------------------|-------------------------------:|----------:|:--------------------|:------------------|----------------------------:|:--------------------------|:-------------------------------------|
| purchase | 1372 |                  59 | -2.06%                    | -2.05%                      |                          -1.57 |     -3.68 | 7.01%               | 9.07%             |                          29 | -2.06%                    | 41.47%                               |
| sale     |  901 |                  55 | -0.38%                    | -0.41%                      |                          -0.58 |     -1    | 3.27%               | 3.65%             |                          22 | 0.38%                     | 52.72%                               |
