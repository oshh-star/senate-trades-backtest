# Mechanism splits, out-of-sample half (2024-03-01 to 2026-08-31), YAHOO

**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, "Out-of-sample test plan"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few cells in a table like this one will reach |t| = 2 by chance.**

**Prices: Yahoo, the final headline source (R3, S2).** Stocks in the survivorship ledger (mostly delisted names Yahoo no longer serves) have no prices: their events drop out here and their purchases are skipped in the book; V15 (SPY fill) bounds the effect.

_From `data/processed/event_panel.csv` (src/metrics/mechanism.py). Each cell: mean SPY-adjusted return (t-statistic, standard errors clustered by calendar month of entry). **copier** = from the close on the entry date (first trading day after the disclosure); **senator** = from the close on the transaction date; horizons in trading days. **Pre-disclosure drift** = transaction-date close to entry-date close. A "difference" row is group 1 minus group 2 (OLS on a group dummy, same clustering). "t n/a" = fewer than 5 entry months, too few for a clustered standard error. Sign convention: the stock's return minus SPY's whatever the side; after a PURCHASE positive = informative, after a SALE NEGATIVE = informative. Horizons past the last in-sample day are censored, so N falls with the horizon._

## Trade size: the two smallest disclosed bands against every larger band

| side     | group                                                                       |   events | copier 21d    | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:----------------------------------------------------------------------------|---------:|:--------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | two smallest bands (<= $50,000)                                             |      923 | +1.78% (3.59) | +3.73% (1.55)  | +2.83% (1.10)  | -4.01% (-3.26) | -2.13% (-1.41) | +3.60% (1.62)  | 903 / 227               | -3.31% (-2.93)         |
| purchase | larger bands (> $50,000)                                                    |       50 | +1.29% (0.73) | +2.28% (0.59)  | -2.55% (-0.51) | +0.08% (0.06)  | -1.86% (-0.64) | -3.15% (-0.96) | 48 / 42                 | -1.22% (-0.86)         |
| purchase | difference (two smallest bands (<= $50,000) minus larger bands (> $50,000)) |      973 | +0.49% (0.27) | +1.45% (0.32)  | +5.39% (1.01)  | -4.09% (-2.13) | -0.27% (-0.07) | +6.76% (1.71)  | 951 / 269               | -2.09% (-0.90)         |
| sale     | two smallest bands (<= $50,000)                                             |      448 | +0.99% (1.65) | +2.63% (2.01)  | +3.48% (1.53)  | -0.31% (-0.37) | +0.39% (0.28)  | +4.32% (1.61)  | 423 / 339               | -0.58% (-0.65)         |
| sale     | larger bands (> $50,000)                                                    |       60 | +0.49% (0.30) | -6.02% (-1.71) | -7.73% (-0.88) | -1.71% (-0.57) | -4.55% (-0.87) | -7.10% (-0.86) | 55 / 36                 | -3.84% (-1.43)         |
| sale     | difference (two smallest bands (<= $50,000) minus larger bands (> $50,000)) |      508 | +0.50% (0.40) | +8.65% (2.45)  | +11.21% (1.40) | +1.40% (0.47)  | +4.94% (0.84)  | +11.42% (1.40) | 478 / 375               | +3.25% (1.32)          |

## Party of the senator's term on the trade date

| side     | group                                  |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:---------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | Democrat                               |       25 | +0.96% (0.58)  | +2.17% (1.12)  | -5.10% (-1.23) | -3.09% (-1.36) | +1.80% (0.88)  | -4.21% (-0.98) | 24 / 18                 | -3.26% (-1.51)         |
| purchase | Republican                             |      948 | +1.78% (3.52)  | +3.62% (1.56)  | +2.50% (1.01)  | -3.83% (-3.05) | -2.20% (-1.60) | +3.04% (1.51)  | 927 / 251               | -3.20% (-2.98)         |
| purchase | difference (Democrat minus Republican) |      973 | -0.81% (-0.46) | -1.44% (-0.42) | -7.60% (-1.63) | +0.74% (0.50)  | +4.00% (1.68)  | -7.25% (-1.63) | 951 / 269               | -0.06% (-0.04)         |
| sale     | Democrat                               |       61 | -0.45% (-0.29) | -2.83% (-1.76) | +2.19% (0.94)  | +0.02% (0.01)  | -1.17% (-0.45) | -1.52% (-0.77) | 59 / 50                 | -0.02% (-0.01)         |
| sale     | Republican                             |      447 | +1.13% (1.57)  | +2.53% (1.51)  | +2.44% (0.81)  | -0.53% (-0.55) | -0.05% (-0.04) | +3.96% (1.22)  | 419 / 325               | -1.08% (-0.96)         |
| sale     | difference (Democrat minus Republican) |      508 | -1.58% (-0.92) | -5.37% (-1.92) | -0.25% (-0.07) | +0.55% (0.25)  | -1.11% (-0.36) | -5.48% (-1.42) | 478 / 375               | +1.06% (0.67)          |

## Filing lag (disclosure date minus transaction date): 30 days or less against longer

| side     | group                                                       |   events | copier 21d     | copier 63d    | copier 126d   | senator 21d     | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:------------------------------------------------------------|---------:|:---------------|:--------------|:--------------|:----------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | filed within 30 days                                        |      239 | +1.30% (0.76)  | +3.59% (1.37) | +2.11% (0.81) | +0.04% (0.06)   | +2.36% (1.60)  | +2.68% (1.48)  | 232 / 202               | -0.06% (-0.09)         |
| purchase | filed after 30 days                                         |      734 | +1.90% (7.76)  | +3.30% (0.87) | +1.63% (0.35) | -5.05% (-10.63) | -3.52% (-6.34) | +2.29% (0.41)  | 719 / 67                | -4.22% (-9.56)         |
| purchase | difference (filed within 30 days minus filed after 30 days) |      973 | -0.60% (-0.35) | +0.29% (0.06) | +0.47% (0.09) | +5.09% (7.75)   | +5.89% (3.82)  | +0.40% (0.07)  | 951 / 269               | +4.16% (5.72)          |
| sale     | filed within 30 days                                        |      270 | -0.05% (-0.07) | +2.60% (1.58) | +3.78% (1.66) | +1.54% (2.01)   | +2.19% (1.63)  | +6.08% (1.97)  | 261 / 221               | +0.92% (1.60)          |
| sale     | filed after 30 days                                         |      238 | +2.13% (2.69)  | +0.56% (0.34) | +0.44% (0.10) | -2.72% (-2.58)  | -2.92% (-2.23) | -0.61% (-0.20) | 217 / 154               | -3.04% (-2.02)         |
| sale     | difference (filed within 30 days minus filed after 30 days) |      508 | -2.18% (-2.47) | +2.05% (0.92) | +3.34% (0.72) | +4.26% (3.26)   | +5.11% (2.67)  | +6.68% (1.67)  | 478 / 375               | +3.96% (2.42)          |

## Senator: the top 4 by number of events in this sample (Q1: the rule is applied to each sample), one by one, and everyone else pooled

| side     | group            |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:-----------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | Alan Armstrong   |      654 | +2.03% (t n/a) |                |                | -5.58% (t n/a) | -3.98% (t n/a) |                | 644 / 0                 | -4.70% (t n/a)         |
| purchase | John Boozman     |      120 | +0.91% (1.09)  | +3.36% (2.15)  | +2.98% (1.57)  | +0.03% (0.04)  | +3.78% (2.25)  | +5.11% (2.02)  | 113 / 96                | +0.46% (0.65)          |
| purchase | Tommy Tuberville |       37 | +7.81% (0.61)  | +10.79% (0.59) | +2.34% (0.22)  | -2.34% (-1.75) | -3.94% (-0.49) | -3.42% (-0.43) | 33 / 33                 | -4.39% (-4.14)         |
| purchase | Markwayne Mullin |      111 | -0.81% (-0.80) | +0.38% (0.19)  | -0.27% (-0.08) | +0.74% (0.84)  | +1.54% (0.74)  | +1.36% (0.67)  | 111 / 100               | +1.08% (1.03)          |
| purchase | everyone else    |       51 | +1.85% (1.03)  | +6.51% (1.60)  | +4.97% (0.83)  | -1.28% (-0.74) | +2.42% (1.18)  | +4.51% (1.04)  | 50 / 40                 | -1.54% (-0.84)         |
| sale     | Alan Armstrong   |       48 | +3.68% (t n/a) |                |                | -7.40% (t n/a) | -7.47% (t n/a) |                | 48 / 0                  | -9.31% (t n/a)         |
| sale     | John Boozman     |      129 | +0.25% (0.31)  | +3.31% (2.23)  | +9.87% (2.37)  | +0.70% (0.94)  | +1.73% (1.23)  | +9.51% (2.20)  | 124 / 102               | +0.52% (0.68)          |
| sale     | Tommy Tuberville |      172 | +0.38% (0.25)  | -1.89% (-3.42) | -4.70% (-2.49) | -1.05% (-1.16) | -3.16% (-7.54) | -4.54% (-3.27) | 151 / 140               | -1.57% (-1.10)         |
| sale     | Markwayne Mullin |       73 | +2.55% (2.24)  | +9.30% (1.90)  | +6.48% (0.95)  | +3.57% (1.96)  | +9.18% (2.05)  | +16.75% (1.78) | 72 / 63                 | +3.12% (1.86)          |
| sale     | everyone else    |       86 | -0.00% (-0.00) | -0.69% (-0.43) | +2.10% (0.86)  | -0.58% (-0.39) | -1.43% (-0.72) | -2.50% (-1.26) | 83 / 70                 | -0.65% (-0.67)         |
