# Mechanism splits, full window (2021-09-01 to 2026-08-31), YAHOO

**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, "Out-of-sample test plan"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few cells in a table like this one will reach |t| = 2 by chance.**

**Prices: Yahoo, the final headline source (R3, S2).** Stocks in the survivorship ledger (mostly delisted names Yahoo no longer serves) have no prices: their events drop out here and their purchases are skipped in the book; V15 (SPY fill) bounds the effect.

_From `data/processed/event_panel.csv` (src/metrics/mechanism.py). Each cell: mean SPY-adjusted return (t-statistic, standard errors clustered by calendar month of entry). **copier** = from the close on the entry date (first trading day after the disclosure); **senator** = from the close on the transaction date; horizons in trading days. **Pre-disclosure drift** = transaction-date close to entry-date close. A "difference" row is group 1 minus group 2 (OLS on a group dummy, same clustering). "t n/a" = fewer than 5 entry months, too few for a clustered standard error. Sign convention: the stock's return minus SPY's whatever the side; after a PURCHASE positive = informative, after a SALE NEGATIVE = informative. Horizons past the last in-sample day are censored, so N falls with the horizon._

## Trade size: the two smallest disclosed bands against every larger band

| side     | group                                                                       |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:----------------------------------------------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | two smallest bands (<= $50,000)                                             |     1291 | +1.61% (3.70)  | +2.17% (1.91)  | +1.87% (1.60)  | -2.68% (-1.71) | -1.22% (-0.79) | +2.53% (2.19)  | 1260 / 584              | -2.17% (-1.55)         |
| purchase | larger bands (> $50,000)                                                    |      117 | +1.18% (1.00)  | +0.81% (0.40)  | -0.90% (-0.33) | +0.24% (0.28)  | -1.65% (-0.98) | -2.01% (-0.95) | 104 / 98                | -0.74% (-0.91)         |
| purchase | difference (two smallest bands (<= $50,000) minus larger bands (> $50,000)) |     1408 | +0.42% (0.34)  | +1.36% (0.60)  | +2.78% (0.97)  | -2.91% (-1.56) | +0.43% (0.17)  | +4.54% (1.85)  | 1364 / 682              | -1.43% (-0.74)         |
| sale     | two smallest bands (<= $50,000)                                             |      823 | +0.49% (1.13)  | +1.72% (2.36)  | +0.64% (0.48)  | -0.14% (-0.28) | +0.38% (0.43)  | +1.57% (0.94)  | 763 / 679               | -0.20% (-0.33)         |
| sale     | larger bands (> $50,000)                                                    |      132 | -0.37% (-0.39) | -3.01% (-1.53) | -1.00% (-0.23) | -0.82% (-0.50) | -2.85% (-1.05) | -1.18% (-0.29) | 116 / 97                | -1.62% (-0.97)         |
| sale     | difference (two smallest bands (<= $50,000) minus larger bands (> $50,000)) |      955 | +0.86% (1.13)  | +4.73% (2.38)  | +1.63% (0.39)  | +0.68% (0.42)  | +3.23% (1.05)  | +2.75% (0.65)  | 879 / 776               | +1.42% (0.97)          |

## Party of the senator's term on the trade date

| side     | group                                  |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:---------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | Democrat                               |       43 | +1.21% (0.85)  | +1.17% (0.44)  | -3.65% (-1.16) | -2.17% (-1.40) | -0.11% (-0.06) | -3.71% (-1.06) | 42 / 36                 | -2.15% (-1.45)         |
| purchase | Republican                             |     1365 | +1.59% (3.70)  | +2.02% (1.85)  | +1.76% (1.54)  | -2.46% (-1.59) | -1.28% (-0.91) | +2.19% (2.08)  | 1322 / 646              | -2.05% (-1.56)         |
| purchase | difference (Democrat minus Republican) |     1408 | -0.37% (-0.25) | -0.86% (-0.30) | -5.40% (-1.64) | +0.29% (0.23)  | +1.17% (0.48)  | -5.90% (-1.67) | 1364 / 682              | -0.09% (-0.08)         |
| sale     | Democrat                               |       95 | -0.85% (-0.71) | -2.26% (-1.37) | +0.99% (0.40)  | +0.07% (0.05)  | -0.47% (-0.26) | -1.73% (-0.90) | 92 / 83                 | -0.14% (-0.17)         |
| sale     | Republican                             |      860 | +0.52% (1.06)  | +1.55% (1.77)  | +0.36% (0.23)  | -0.27% (-0.45) | +0.00% (0.00)  | +1.59% (0.88)  | 787 / 693               | -0.41% (-0.57)         |
| sale     | difference (Democrat minus Republican) |      955 | -1.37% (-1.05) | -3.82% (-1.79) | +0.63% (0.21)  | +0.33% (0.23)  | -0.47% (-0.23) | -3.31% (-1.23) | 879 / 776               | +0.26% (0.24)          |

## Filing lag (disclosure date minus transaction date): 30 days or less against longer

| side     | group                                                       |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:------------------------------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | filed within 30 days                                        |      532 | +1.32% (1.52)  | +1.95% (1.52)  | +1.43% (1.10)  | +0.35% (0.84)  | +1.40% (1.79)  | +1.96% (1.69)  | 511 / 481               | +0.30% (0.61)          |
| purchase | filed after 30 days                                         |      876 | +1.73% (5.03)  | +2.04% (1.25)  | +1.58% (0.91)  | -4.14% (-3.73) | -2.82% (-2.86) | +1.70% (0.85)  | 853 / 201               | -3.47% (-3.64)         |
| purchase | difference (filed within 30 days minus filed after 30 days) |     1408 | -0.41% (-0.44) | -0.08% (-0.04) | -0.15% (-0.07) | +4.49% (4.15)  | +4.22% (3.40)  | +0.26% (0.11)  | 1364 / 682              | +3.76% (3.82)          |
| sale     | filed within 30 days                                        |      510 | -0.31% (-0.58) | +2.05% (1.92)  | +1.69% (1.00)  | +1.01% (1.76)  | +1.24% (1.29)  | +3.93% (2.07)  | 471 / 431               | +0.67% (1.50)          |
| sale     | filed after 30 days                                         |      445 | +1.16% (1.87)  | -0.06% (-0.07) | -1.14% (-0.55) | -1.61% (-2.07) | -1.50% (-1.41) | -2.07% (-1.11) | 408 / 345               | -1.55% (-1.37)         |
| sale     | difference (filed within 30 days minus filed after 30 days) |      955 | -1.47% (-1.86) | +2.12% (1.51)  | +2.83% (1.05)  | +2.62% (2.71)  | +2.75% (1.95)  | +6.00% (2.43)  | 879 / 776               | +2.23% (1.84)          |

## Senator: the top 4 by number of events in this sample (Q1: the rule is applied to each sample), one by one, and everyone else pooled

| side     | group            |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:-----------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | Tommy Tuberville |      303 | +1.73% (1.13)  | +1.03% (0.46)  | +0.02% (0.01)  | +0.29% (0.41)  | -0.75% (-0.54) | -1.31% (-0.84) | 278 / 278               | -0.22% (-0.28)         |
| purchase | Alan Armstrong   |      654 | +2.03% (t n/a) |                |                | -5.58% (t n/a) | -3.98% (t n/a) |                | 644 / 0                 | -4.70% (t n/a)         |
| purchase | Markwayne Mullin |      238 | +0.53% (0.60)  | +2.00% (1.70)  | +2.05% (1.17)  | +0.47% (0.84)  | +2.05% (1.67)  | +3.60% (2.06)  | 237 / 226               | +0.71% (1.15)          |
| purchase | John Boozman     |      122 | +0.80% (0.97)  | +3.14% (2.04)  | +2.72% (1.45)  | +0.01% (0.02)  | +3.61% (2.18)  | +4.85% (1.96)  | 115 / 98                | +0.48% (0.68)          |
| purchase | everyone else    |       91 | +1.58% (1.39)  | +3.54% (1.40)  | +3.36% (1.04)  | +0.32% (0.25)  | +2.15% (1.39)  | +4.05% (1.43)  | 90 / 80                 | +0.42% (0.30)          |
| sale     | Tommy Tuberville |      447 | -0.07% (-0.10) | -0.19% (-0.22) | -2.61% (-1.64) | -0.56% (-0.99) | -1.05% (-1.09) | -2.06% (-1.25) | 390 / 379               | -0.40% (-0.47)         |
| sale     | Alan Armstrong   |       48 | +3.68% (t n/a) |                |                | -7.40% (t n/a) | -7.47% (t n/a) |                | 48 / 0                  | -9.31% (t n/a)         |
| sale     | Markwayne Mullin |       84 | +1.99% (1.81)  | +8.09% (1.82)  | +4.19% (0.66)  | +3.01% (1.80)  | +8.56% (2.16)  | +13.62% (1.53) | 82 / 73                 | +2.74% (1.80)          |
| sale     | John Boozman     |      132 | +0.37% (0.48)  | +3.30% (2.26)  | +9.81% (2.43)  | +0.97% (1.28)  | +2.15% (1.54)  | +9.57% (2.28)  | 127 / 105               | +0.69% (0.88)          |
| sale     | everyone else    |      244 | -0.12% (-0.19) | -0.25% (-0.29) | -0.05% (-0.04) | -0.01% (-0.01) | -1.07% (-1.13) | -1.59% (-1.01) | 232 / 219               | -0.21% (-0.32)         |
