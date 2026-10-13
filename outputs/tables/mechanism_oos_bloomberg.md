# Mechanism splits, out-of-sample half (2024-03-01 to 2026-08-31), BLOOMBERG

**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, "Out-of-sample test plan"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few cells in a table like this one will reach |t| = 2 by chance.**

**Prices: Yahoo, with Bloomberg terminal prices where Yahoo has none** (`prices.sources: [yahoo, manual]`, post-unlock correction C1, 2026-10-09): 8 delisted stocks (X, ECOM, ATVI, SSBK, PARA, WBA, GOGL, TOELY; 95% of the missing headline dollars) are priced from data/raw/manual_prices/. The other survivorship-ledger stocks still have no prices: their events drop out here and their purchases are skipped in the book. V18 is the Yahoo-only run (the headline before C1).

_From `data/processed/event_panel.csv` (src/metrics/mechanism.py). Each cell: mean SPY-adjusted return (t-statistic, standard errors clustered by calendar month of entry). **copier** = from the close on the entry date (first trading day after the disclosure); **senator** = from the close on the transaction date; horizons in trading days. **Pre-disclosure drift** = transaction-date close to entry-date close. A "difference" row is group 1 minus group 2 (OLS on a group dummy, same clustering). "t n/a" = fewer than 5 entry months, too few for a clustered standard error. Sign convention: the stock's return minus SPY's whatever the side; after a PURCHASE positive = informative, after a SALE NEGATIVE = informative. Horizons past the last in-sample day are censored, so N falls with the horizon._

## Trade size: the two smallest disclosed bands against every larger band

| side     | group                                                                       |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:----------------------------------------------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | two smallest bands (<= $50,000)                                             |      923 | +1.76% (3.56)  | +3.55% (1.60)  | +2.51% (1.04)  | -4.00% (-3.24) | -2.17% (-1.47) | +3.22% (1.52)  | 906 / 229               | -3.32% (-2.97)         |
| purchase | larger bands (> $50,000)                                                    |       50 | +1.27% (0.75)  | +2.04% (0.55)  | -2.32% (-0.49) | +0.14% (0.12)  | -1.76% (-0.62) | -2.64% (-0.83) | 50 / 44                 | -1.21% (-0.87)         |
| purchase | difference (two smallest bands (<= $50,000) minus larger bands (> $50,000)) |      973 | +0.49% (0.29)  | +1.51% (0.35)  | +4.82% (0.96)  | -4.14% (-2.17) | -0.41% (-0.12) | +5.86% (1.57)  | 956 / 273               | -2.11% (-0.93)         |
| sale     | two smallest bands (<= $50,000)                                             |      448 | +0.99% (1.65)  | +2.63% (2.01)  | +3.48% (1.53)  | -0.31% (-0.37) | +0.39% (0.28)  | +4.32% (1.61)  | 423 / 339               | -0.58% (-0.65)         |
| sale     | larger bands (> $50,000)                                                    |       60 | -0.00% (-0.00) | -6.82% (-2.18) | -8.64% (-1.11) | -2.10% (-0.74) | -5.25% (-1.07) | -9.12% (-1.19) | 59 / 40                 | -3.97% (-1.34)         |
| sale     | difference (two smallest bands (<= $50,000) minus larger bands (> $50,000)) |      508 | +1.00% (0.52)  | +9.45% (3.01)  | +12.13% (1.74) | +1.79% (0.62)  | +5.63% (1.01)  | +13.44% (1.78) | 482 / 379               | +3.38% (1.23)          |

## Party of the senator's term on the trade date

| side     | group                                  |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:---------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | Democrat                               |       25 | +0.96% (0.58)  | +2.17% (1.12)  | -5.10% (-1.23) | -3.09% (-1.36) | +1.80% (0.88)  | -4.21% (-0.98) | 24 / 18                 | -3.26% (-1.51)         |
| purchase | Republican                             |      948 | +1.76% (3.49)  | +3.40% (1.58)  | +2.21% (0.96)  | -3.81% (-3.01) | -2.24% (-1.66) | +2.76% (1.44)  | 932 / 255               | -3.21% (-3.02)         |
| purchase | difference (Democrat minus Republican) |      973 | -0.80% (-0.45) | -1.23% (-0.38) | -7.31% (-1.60) | +0.72% (0.49)  | +4.04% (1.70)  | -6.97% (-1.59) | 956 / 273               | -0.05% (-0.03)         |
| sale     | Democrat                               |       61 | -0.45% (-0.29) | -2.83% (-1.76) | +2.19% (0.94)  | +0.02% (0.01)  | -1.17% (-0.45) | -1.52% (-0.77) | 59 / 50                 | -0.02% (-0.01)         |
| sale     | Republican                             |      447 | +1.06% (1.31)  | +2.34% (1.38)  | +2.21% (0.73)  | -0.60% (-0.62) | -0.19% (-0.14) | +3.60% (1.09)  | 423 / 329               | -1.12% (-0.99)         |
| sale     | difference (Democrat minus Republican) |      508 | -1.50% (-0.86) | -5.17% (-1.84) | -0.01% (-0.00) | +0.61% (0.28)  | -0.97% (-0.32) | -5.12% (-1.30) | 482 / 379               | +1.10% (0.70)          |

## Filing lag (disclosure date minus transaction date): 30 days or less against longer

| side     | group                                                       |   events | copier 21d     | copier 63d    | copier 126d   | senator 21d     | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:------------------------------------------------------------|---------:|:---------------|:--------------|:--------------|:----------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | filed within 30 days                                        |      239 | +1.33% (0.78)  | +3.32% (1.39) | +1.76% (0.74) | +0.06% (0.09)   | +2.15% (1.57)  | +2.34% (1.40)  | 236 / 206               | -0.15% (-0.20)         |
| purchase | filed after 30 days                                         |      734 | +1.87% (7.71)  | +3.30% (0.87) | +1.63% (0.35) | -5.05% (-10.63) | -3.52% (-6.34) | +2.29% (0.41)  | 720 / 67                | -4.22% (-9.56)         |
| purchase | difference (filed within 30 days minus filed after 30 days) |      973 | -0.54% (-0.31) | +0.02% (0.01) | +0.12% (0.03) | +5.11% (7.85)   | +5.67% (3.95)  | +0.05% (0.01)  | 956 / 273               | +4.07% (5.43)          |
| sale     | filed within 30 days                                        |      270 | -0.22% (-0.28) | +2.32% (1.36) | +3.42% (1.44) | +1.48% (2.02)   | +2.02% (1.53)  | +5.65% (1.79)  | 264 / 224               | +0.93% (1.64)          |
| sale     | filed after 30 days                                         |      238 | +2.20% (2.76)  | +0.57% (0.36) | +0.45% (0.10) | -2.78% (-2.72)  | -3.01% (-2.34) | -0.78% (-0.25) | 218 / 155               | -3.15% (-2.10)         |
| sale     | difference (filed within 30 days minus filed after 30 days) |      508 | -2.42% (-2.86) | +1.75% (0.78) | +2.97% (0.65) | +4.26% (3.38)   | +5.03% (2.76)  | +6.43% (1.58)  | 482 / 379               | +4.08% (2.51)          |

## Senator: the top 4 by number of events in this sample (Q1: the rule is applied to each sample), one by one, and everyone else pooled

| side     | group            |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:-----------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | Alan Armstrong   |      654 | +1.99% (t n/a) |                |                | -5.58% (t n/a) | -3.98% (t n/a) |                | 645 / 0                 | -4.70% (t n/a)         |
| purchase | John Boozman     |      120 | +0.91% (1.09)  | +3.36% (2.15)  | +2.98% (1.57)  | +0.03% (0.04)  | +3.78% (2.25)  | +5.11% (2.02)  | 113 / 96                | +0.46% (0.65)          |
| purchase | Tommy Tuberville |       37 | +7.32% (0.65)  | +8.38% (0.59)  | +0.38% (0.05)  | -2.03% (-1.49) | -4.79% (-0.73) | -5.02% (-0.89) | 37 / 37                 | -4.60% (-3.67)         |
| purchase | Markwayne Mullin |      111 | -0.81% (-0.80) | +0.38% (0.19)  | -0.27% (-0.08) | +0.74% (0.84)  | +1.54% (0.74)  | +1.36% (0.67)  | 111 / 100               | +1.08% (1.03)          |
| purchase | everyone else    |       51 | +1.85% (1.03)  | +6.51% (1.60)  | +4.97% (0.83)  | -1.28% (-0.74) | +2.42% (1.18)  | +4.51% (1.04)  | 50 / 40                 | -1.54% (-0.84)         |
| sale     | Alan Armstrong   |       48 | +3.68% (t n/a) |                |                | -7.40% (t n/a) | -7.47% (t n/a) |                | 48 / 0                  | -9.31% (t n/a)         |
| sale     | John Boozman     |      129 | +0.25% (0.31)  | +3.31% (2.23)  | +9.87% (2.37)  | +0.70% (0.94)  | +1.73% (1.23)  | +9.51% (2.20)  | 124 / 102               | +0.52% (0.68)          |
| sale     | Tommy Tuberville |      172 | +0.19% (0.11)  | -2.23% (-3.39) | -5.04% (-2.83) | -1.20% (-1.36) | -3.45% (-8.13) | -5.14% (-3.59) | 155 / 144               | -1.67% (-1.11)         |
| sale     | Markwayne Mullin |       73 | +2.55% (2.24)  | +9.30% (1.90)  | +6.48% (0.95)  | +3.57% (1.96)  | +9.18% (2.05)  | +16.75% (1.78) | 72 / 63                 | +3.12% (1.86)          |
| sale     | everyone else    |       86 | -0.00% (-0.00) | -0.69% (-0.43) | +2.10% (0.86)  | -0.58% (-0.39) | -1.43% (-0.72) | -2.50% (-1.26) | 83 / 70                 | -0.65% (-0.67)         |
