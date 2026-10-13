# Mechanism splits, full window (2021-09-01 to 2026-08-31), BLOOMBERG

**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, "Out-of-sample test plan"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few cells in a table like this one will reach |t| = 2 by chance.**

**Prices: Yahoo, with Bloomberg terminal prices where Yahoo has none** (`prices.sources: [yahoo, manual]`, post-unlock correction C1, 2026-10-09): 8 delisted stocks (X, ECOM, ATVI, SSBK, PARA, WBA, GOGL, TOELY; 95% of the missing headline dollars) are priced from data/raw/manual_prices/. The other survivorship-ledger stocks still have no prices: their events drop out here and their purchases are skipped in the book. V18 is the Yahoo-only run (the headline before C1).

_From `data/processed/event_panel.csv` (src/metrics/mechanism.py). Each cell: mean SPY-adjusted return (t-statistic, standard errors clustered by calendar month of entry). **copier** = from the close on the entry date (first trading day after the disclosure); **senator** = from the close on the transaction date; horizons in trading days. **Pre-disclosure drift** = transaction-date close to entry-date close. A "difference" row is group 1 minus group 2 (OLS on a group dummy, same clustering). "t n/a" = fewer than 5 entry months, too few for a clustered standard error. Sign convention: the stock's return minus SPY's whatever the side; after a PURCHASE positive = informative, after a SALE NEGATIVE = informative. Horizons past the last in-sample day are censored, so N falls with the horizon._

## Trade size: the two smallest disclosed bands against every larger band

| side     | group                                                                       |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:----------------------------------------------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | two smallest bands (<= $50,000)                                             |     1291 | +1.54% (3.47)  | +2.00% (1.85)  | +1.68% (1.52)  | -2.69% (-1.74) | -1.35% (-0.92) | +2.22% (2.05)  | 1271 / 594              | -2.20% (-1.61)         |
| purchase | larger bands (> $50,000)                                                    |      117 | +1.68% (1.36)  | +1.40% (0.75)  | +1.57% (0.63)  | +0.37% (0.45)  | -0.54% (-0.33) | +1.15% (0.53)  | 117 / 111               | -0.48% (-0.59)         |
| purchase | difference (two smallest bands (<= $50,000) minus larger bands (> $50,000)) |     1408 | -0.14% (-0.11) | +0.60% (0.29)  | +0.12% (0.04)  | -3.06% (-1.66) | -0.81% (-0.34) | +1.07% (0.44)  | 1388 / 705              | -1.72% (-0.92)         |
| sale     | two smallest bands (<= $50,000)                                             |      823 | +0.31% (0.65)  | +1.53% (2.08)  | +0.86% (0.67)  | -0.24% (-0.46) | +0.07% (0.08)  | +1.40% (0.86)  | 785 / 701               | -0.34% (-0.60)         |
| sale     | larger bands (> $50,000)                                                    |      132 | -0.88% (-0.69) | -2.80% (-1.34) | +0.91% (0.21)  | -1.14% (-0.75) | -3.34% (-1.32) | -0.37% (-0.09) | 129 / 110               | -1.77% (-1.05)         |
| sale     | difference (two smallest bands (<= $50,000) minus larger bands (> $50,000)) |      955 | +1.19% (1.16)  | +4.33% (2.07)  | -0.05% (-0.01) | +0.91% (0.59)  | +3.41% (1.18)  | +1.77% (0.41)  | 914 / 811               | +1.43% (0.94)          |

## Party of the senator's term on the trade date

| side     | group                                  |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:---------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | Democrat                               |       43 | +1.21% (0.85)  | +1.17% (0.44)  | -3.65% (-1.16) | -2.17% (-1.40) | -0.11% (-0.06) | -3.71% (-1.06) | 42 / 36                 | -2.15% (-1.45)         |
| purchase | Republican                             |     1365 | +1.57% (3.65)  | +1.95% (1.89)  | +1.95% (1.81)  | -2.45% (-1.60) | -1.31% (-0.95) | +2.36% (2.41)  | 1346 / 669              | -2.06% (-1.59)         |
| purchase | difference (Democrat minus Republican) |     1408 | -0.35% (-0.24) | -0.79% (-0.28) | -5.59% (-1.72) | +0.28% (0.22)  | +1.20% (0.49)  | -6.07% (-1.74) | 1388 / 705              | -0.09% (-0.08)         |
| sale     | Democrat                               |       95 | -0.85% (-0.71) | -2.26% (-1.37) | +0.99% (0.40)  | +0.07% (0.05)  | -0.47% (-0.26) | -1.73% (-0.90) | 92 / 83                 | -0.14% (-0.17)         |
| sale     | Republican                             |      860 | +0.26% (0.44)  | +1.32% (1.49)  | +0.85% (0.56)  | -0.41% (-0.73) | -0.41% (-0.46) | +1.49% (0.84)  | 822 / 728               | -0.59% (-0.84)         |
| sale     | difference (Democrat minus Republican) |      955 | -1.11% (-0.83) | -3.59% (-1.69) | +0.14% (0.05)  | +0.48% (0.32)  | -0.06% (-0.03) | -3.21% (-1.20) | 914 / 811               | +0.44% (0.41)          |

## Filing lag (disclosure date minus transaction date): 30 days or less against longer

| side     | group                                                       |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:------------------------------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | filed within 30 days                                        |      532 | +1.30% (1.48)  | +1.76% (1.46)  | +1.57% (1.27)  | +0.36% (0.89)  | +1.30% (1.79)  | +2.14% (1.99)  | 526 / 496               | +0.28% (0.57)          |
| purchase | filed after 30 days                                         |      876 | +1.71% (5.13)  | +2.28% (1.38)  | +1.89% (1.12)  | -4.14% (-3.77) | -2.83% (-2.89) | +1.86% (0.93)  | 862 / 209               | -3.48% (-3.71)         |
| purchase | difference (filed within 30 days minus filed after 30 days) |     1408 | -0.42% (-0.44) | -0.52% (-0.26) | -0.33% (-0.17) | +4.49% (4.21)  | +4.13% (3.45)  | +0.28% (0.12)  | 1388 / 705              | +3.75% (3.86)          |
| sale     | filed within 30 days                                        |      510 | -0.70% (-1.16) | +1.89% (1.73)  | +2.51% (1.53)  | +0.62% (1.13)  | +0.51% (0.51)  | +3.93% (2.06)  | 497 / 457               | +0.27% (0.60)          |
| sale     | filed after 30 days                                         |      445 | +1.15% (1.62)  | -0.32% (-0.34) | -1.26% (-0.63) | -1.48% (-1.88) | -1.49% (-1.38) | -2.35% (-1.26) | 417 / 354               | -1.48% (-1.29)         |
| sale     | difference (filed within 30 days minus filed after 30 days) |      955 | -1.85% (-2.11) | +2.21% (1.48)  | +3.77% (1.44)  | +2.10% (2.20)  | +2.01% (1.43)  | +6.28% (2.50)  | 914 / 811               | +1.75% (1.43)          |

## Senator: the top 4 by number of events in this sample (Q1: the rule is applied to each sample), one by one, and everyone else pooled

| side     | group            |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:-----------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | Tommy Tuberville |      303 | +1.70% (1.15)  | +0.94% (0.47)  | +0.58% (0.37)  | +0.19% (0.27)  | -0.92% (-0.69) | -0.68% (-0.47) | 301 / 301               | -0.36% (-0.46)         |
| purchase | Alan Armstrong   |      654 | +1.99% (t n/a) |                |                | -5.58% (t n/a) | -3.98% (t n/a) |                | 645 / 0                 | -4.70% (t n/a)         |
| purchase | Markwayne Mullin |      238 | +0.53% (0.60)  | +2.00% (1.70)  | +2.05% (1.17)  | +0.47% (0.84)  | +2.05% (1.67)  | +3.60% (2.06)  | 237 / 226               | +0.71% (1.15)          |
| purchase | John Boozman     |      122 | +0.80% (0.97)  | +3.14% (2.04)  | +2.72% (1.45)  | +0.01% (0.02)  | +3.61% (2.18)  | +4.85% (1.96)  | 115 / 98                | +0.48% (0.68)          |
| purchase | everyone else    |       91 | +1.58% (1.39)  | +3.54% (1.40)  | +3.36% (1.04)  | +0.32% (0.25)  | +2.15% (1.39)  | +4.05% (1.43)  | 90 / 80                 | +0.42% (0.30)          |
| sale     | Tommy Tuberville |      447 | -0.53% (-0.56) | -0.46% (-0.49) | -1.51% (-0.97) | -0.80% (-1.63) | -1.74% (-1.75) | -1.94% (-1.21) | 425 / 414               | -0.74% (-0.92)         |
| sale     | Alan Armstrong   |       48 | +3.68% (t n/a) |                |                | -7.40% (t n/a) | -7.47% (t n/a) |                | 48 / 0                  | -9.31% (t n/a)         |
| sale     | Markwayne Mullin |       84 | +1.99% (1.81)  | +8.09% (1.82)  | +4.19% (0.66)  | +3.01% (1.80)  | +8.56% (2.16)  | +13.62% (1.53) | 82 / 73                 | +2.74% (1.80)          |
| sale     | John Boozman     |      132 | +0.37% (0.48)  | +3.30% (2.26)  | +9.81% (2.43)  | +0.97% (1.28)  | +2.15% (1.54)  | +9.57% (2.28)  | 127 / 105               | +0.69% (0.88)          |
| sale     | everyone else    |      244 | -0.12% (-0.19) | -0.25% (-0.29) | -0.05% (-0.04) | -0.01% (-0.01) | -1.07% (-1.13) | -1.59% (-1.01) | 232 / 219               | -0.21% (-0.32)         |
