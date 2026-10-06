# Mechanism splits, in-sample (2021-09-01 to 2024-02-29), YAHOO

**Prices: Yahoo, the final headline source (R3, S2).** Stocks in the survivorship ledger (mostly delisted names Yahoo no longer serves) have no prices: their events drop out here and their purchases are skipped in the book; V15 (SPY fill) bounds the effect.

_From `data/processed/event_panel.csv` (src/metrics/mechanism.py). Each cell: mean SPY-adjusted return (t-statistic, standard errors clustered by calendar month of entry). **copier** = from the close on the entry date (first trading day after the disclosure); **senator** = from the close on the transaction date; horizons in trading days. **Pre-disclosure drift** = transaction-date close to entry-date close. A "difference" row is group 1 minus group 2 (OLS on a group dummy, same clustering). "t n/a" = fewer than 5 entry months, too few for a clustered standard error. Sign convention: the stock's return minus SPY's whatever the side; after a PURCHASE positive = informative, after a SALE NEGATIVE = informative. Horizons past the last in-sample day are censored, so N falls with the horizon._

## Trade size: the two smallest disclosed bands against every larger band

| side     | group                                                                       |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:----------------------------------------------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | two smallest bands (<= $50,000)                                             |      368 | +1.17% (1.88)  | +0.47% (0.39)  | +0.31% (0.18)  | +0.73% (1.24)  | +0.65% (0.94)  | +0.07% (0.05)  | 357 / 194               | +0.75% (1.17)          |
| purchase | larger bands (> $50,000)                                                    |       67 | +1.09% (0.67)  | -0.71% (-0.29) | -3.66% (-1.53) | +0.37% (0.32)  | -0.91% (-0.46) | -4.71% (-1.70) | 56 / 37                 | -0.32% (-0.35)         |
| purchase | difference (two smallest bands (<= $50,000) minus larger bands (> $50,000)) |      435 | +0.08% (0.05)  | +1.18% (0.49)  | +3.98% (1.52)  | +0.35% (0.27)  | +1.55% (0.81)  | +4.79% (1.63)  | 413 / 231               | +1.08% (0.98)          |
| sale     | two smallest bands (<= $50,000)                                             |      375 | -0.13% (-0.21) | +1.18% (1.39)  | -0.70% (-0.32) | +0.07% (0.15)  | +0.47% (0.33)  | +0.43% (0.19)  | 301 / 182               | +0.31% (0.50)          |
| sale     | larger bands (> $50,000)                                                    |       72 | -1.01% (-1.28) | -0.47% (-0.25) | +3.18% (0.88)  | -0.00% (-0.00) | -1.50% (-0.78) | +3.23% (0.95)  | 58 / 45                 | +0.42% (0.32)          |
| sale     | difference (two smallest bands (<= $50,000) minus larger bands (> $50,000)) |      447 | +0.87% (0.96)  | +1.64% (0.85)  | -3.87% (-1.10) | +0.08% (0.05)  | +1.97% (0.78)  | -2.80% (-0.73) | 359 / 227               | -0.11% (-0.08)         |

## Party of the senator's term on the trade date

| side     | group                                  |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:---------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | Democrat                               |       18 | +1.55% (0.59)  | -3.99% (-1.09) | +1.56% (0.26)  | -0.90% (-0.46) | -1.92% (-0.51) | +0.67% (0.10)  | 18 / 11                 | -0.60% (-0.33)         |
| purchase | Republican                             |      417 | +1.14% (1.88)  | +0.50% (0.42)  | -0.42% (-0.26) | +0.75% (1.44)  | +0.55% (0.76)  | -0.76% (-0.51) | 395 / 220               | +0.66% (1.13)          |
| purchase | difference (Democrat minus Republican) |      435 | +0.41% (0.16)  | -4.49% (-1.31) | +1.98% (0.34)  | -1.66% (-0.90) | -2.46% (-0.67) | +1.43% (0.22)  | 413 / 231               | -1.26% (-0.71)         |
| sale     | Democrat                               |       34 | -1.58% (-0.88) | -2.40% (-0.56) | -6.30% (-0.99) | +0.16% (0.10)  | +0.68% (0.23)  | -3.68% (-0.70) | 33 / 20                 | -0.38% (-0.30)         |
| sale     | Republican                             |      413 | -0.14% (-0.23) | +1.19% (1.21)  | +0.68% (0.30)  | +0.05% (0.10)  | +0.05% (0.04)  | +1.35% (0.60)  | 326 / 207               | +0.39% (0.62)          |
| sale     | difference (Democrat minus Republican) |      447 | -1.44% (-0.74) | -3.59% (-0.78) | -6.99% (-1.01) | +0.11% (0.07)  | +0.64% (0.20)  | -5.03% (-0.82) | 359 / 227               | -0.77% (-0.58)         |

## Filing lag (disclosure date minus transaction date): 30 days or less against longer

| side     | group                                                       |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:------------------------------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | filed within 30 days                                        |      293 | +1.33% (1.81)  | -0.03% (-0.02) | -1.89% (-0.66) | +0.61% (1.04)  | +0.06% (0.07)  | -2.66% (-1.09) | 279 / 106               | +0.60% (0.84)          |
| purchase | filed after 30 days                                         |      142 | +0.79% (0.69)  | +0.99% (0.58)  | +1.00% (0.77)  | +0.82% (0.83)  | +1.19% (0.86)  | +1.00% (0.76)  | 134 / 125               | +0.61% (0.69)          |
| purchase | difference (filed within 30 days minus filed after 30 days) |      435 | +0.54% (0.39)  | -1.02% (-0.49) | -2.89% (-0.95) | -0.21% (-0.19) | -1.14% (-0.78) | -3.66% (-1.42) | 413 / 231               | -0.01% (-0.01)         |
| sale     | filed within 30 days                                        |      240 | -0.62% (-0.68) | +2.30% (1.47)  | +3.44% (1.24)  | +0.34% (0.41)  | +0.01% (0.00)  | +3.17% (1.38)  | 177 / 110               | +0.37% (0.52)          |
| sale     | filed after 30 days                                         |      207 | +0.07% (0.10)  | -0.70% (-0.52) | -3.10% (-1.03) | -0.25% (-0.40) | +0.22% (0.15)  | -1.73% (-0.47) | 182 / 117               | +0.28% (0.30)          |
| sale     | difference (filed within 30 days minus filed after 30 days) |      447 | -0.69% (-0.58) | +3.00% (1.28)  | +6.55% (1.59)  | +0.59% (0.55)  | -0.21% (-0.11) | +4.90% (1.14)  | 359 / 227               | +0.08% (0.07)          |

## Senator: the top 4 by number of in-sample events, one by one, and everyone else pooled

| side     | group            |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d     | senator 126d    | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:-----------------|---------:|:---------------|:---------------|:---------------|:---------------|:----------------|:----------------|:------------------------|:-----------------------|
| purchase | Tommy Tuberville |      266 | +0.91% (0.95)  | -0.62% (-0.40) | -0.99% (-0.57) | +0.65% (0.86)  | -0.16% (-0.15)  | -1.84% (-1.11)  | 245 / 199               | +0.34% (0.40)          |
| purchase | Markwayne Mullin |      127 | +1.71% (t n/a) | +2.91% (t n/a) |                | +0.23% (t n/a) | +1.19% (t n/a)  |                 | 126 / 0                 | +0.38% (t n/a)         |
| purchase | Dan Sullivan     |       11 | +1.99% (t n/a) | +4.20% (t n/a) | +8.11% (t n/a) | +5.09% (t n/a) | +10.10% (t n/a) | +12.91% (t n/a) | 11 / 11                 | +6.47% (t n/a)         |
| purchase | Jerry Moran      |        9 | +0.73% (t n/a) | -2.86% (t n/a) | +3.27% (t n/a) | +4.50% (t n/a) | -1.36% (t n/a)  | +8.97% (t n/a)  | 9 / 8                   | +4.66% (t n/a)         |
| purchase | everyone else    |       22 | +0.52% (0.24)  | -3.95% (-1.31) | +0.55% (0.10)  | -0.17% (-0.10) | -1.15% (-0.36)  | -0.55% (-0.10)  | 22 / 13                 | +0.29% (0.19)          |
| sale     | Tommy Tuberville |      275 | -0.30% (-0.34) | +1.55% (1.27)  | +0.43% (0.16)  | -0.21% (-0.31) | +0.47% (0.29)   | +1.27% (0.40)   | 199 / 152               | +0.42% (0.55)          |
| sale     | Markwayne Mullin |       11 | -2.07% (t n/a) |                |                | -1.07% (t n/a) |                 |                 | 10 / 0                  | -0.00% (t n/a)         |
| sale     | Dan Sullivan     |       57 | -0.54% (-0.49) | +1.06% (1.03)  | +4.59% (1.04)  | -0.28% (-0.39) | -2.61% (-1.44)  | +0.35% (0.13)   | 54 / 22                 | -0.83% (-1.18)         |
| sale     | Jerry Moran      |       35 | -0.66% (t n/a) | -0.83% (t n/a) | -2.05% (t n/a) | +1.89% (t n/a) | +6.00% (t n/a)  | +4.43% (t n/a)  | 35 / 12                 | +1.62% (t n/a)         |
| sale     | everyone else    |       69 | +0.55% (0.41)  | -1.51% (-0.61) | -3.06% (-0.76) | +0.56% (0.48)  | +0.18% (0.10)   | -0.45% (-0.13)  | 61 / 41                 | +0.31% (0.27)          |
