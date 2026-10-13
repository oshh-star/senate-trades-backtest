# Committee test, full window (2021-09-01 to 2026-08-31), BLOOMBERG

**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, "Out-of-sample test plan"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few cells in a table like this one will reach |t| = 2 by chance.**

**Prices: Yahoo, with Bloomberg terminal prices where Yahoo has none** (`prices.sources: [yahoo, manual]`, post-unlock correction C1, 2026-10-09): 8 delisted stocks (X, ECOM, ATVI, SSBK, PARA, WBA, GOGL, TOELY; 95% of the missing headline dollars) are priced from data/raw/manual_prices/. The other survivorship-ledger stocks still have no prices: their events drop out here and their purchases are skipped in the book. V18 is the Yahoo-only run (the headline before C1).

_src/metrics/committee.py. An event is **overseen** when, on its transaction date, the senator sat on a committee in config/committee_industries.yaml (committed at a124f03 before this split was computed, E54) whose SIC ranges contain the company's SIC code. Membership: the latest version of congress-legislators' committee-membership-current.yaml committed on or before the trade date. Cells: mean SPY-adjusted return (t clustered by entry month); copier from the entry date, senator from the transaction date; "t n/a" = fewer than 5 entry months. After a SALE a NEGATIVE number is informative._

## The split

| side     | group                                                               |   events | copier 21d    | copier 63d    | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:--------------------------------------------------------------------|---------:|:--------------|:--------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | overseen by the senator's committee                                 |       90 | +3.04% (0.80) | +4.94% (0.80) | +2.47% (0.64)  | +2.01% (1.24)  | +0.79% (0.36)  | +1.52% (0.51)  | 89 / 86                 | +1.16% (0.55)          |
| purchase | not overseen                                                        |      977 | +1.25% (2.99) | +1.58% (1.85) | +1.58% (1.54)  | -1.60% (-1.44) | +0.50% (0.72)  | +2.16% (1.97)  | 964 / 572               | -0.70% (-1.21)         |
| purchase | difference (overseen by the senator's committee minus not overseen) |     1067 | +1.79% (0.47) | +3.36% (0.54) | +0.89% (0.23)  | +3.60% (1.78)  | +0.29% (0.12)  | -0.65% (-0.20) | 1053 / 658              | +1.86% (0.87)          |
| sale     | overseen by the senator's committee                                 |      153 | +0.63% (0.74) | +2.32% (1.41) | +0.43% (0.19)  | +1.68% (1.32)  | +2.80% (1.48)  | +2.71% (1.16)  | 149 / 145               | +0.77% (0.93)          |
| sale     | not overseen                                                        |      713 | +0.10% (0.15) | +0.40% (0.41) | +0.55% (0.33)  | -0.84% (-1.25) | -1.34% (-1.19) | +0.41% (0.19)  | 678 / 592               | -0.92% (-1.10)         |
| sale     | difference (overseen by the senator's committee minus not overseen) |      866 | +0.53% (0.57) | +1.92% (0.95) | -0.12% (-0.04) | +2.53% (1.60)  | +4.13% (1.58)  | +2.30% (0.69)  | 827 / 737               | +1.69% (1.32)          |

## Events by group

| side     |   left out: ETF |   left out: no SIC code |   not overseen |   overseen by the senator's committee |
|:---------|----------------:|------------------------:|---------------:|--------------------------------------:|
| purchase |              43 |                     298 |            977 |                                    90 |
| sale     |              77 |                      12 |            713 |                                   153 |

## Overseen events by committee (an event can count under two committees)

|                                             |   purchase |   sale |
|:--------------------------------------------|-----------:|-------:|
| SSAF Agriculture, Nutrition, and Forestry   |          7 |     22 |
| SSAS Armed Services                         |         11 |     13 |
| SSBK Banking, Housing, and Urban Affairs    |          4 |     14 |
| SSCM Commerce, Science, and Transportation  |         14 |     40 |
| SSEG Energy and Natural Resources           |          0 |      1 |
| SSHR Health, Education, Labor, and Pensions |         54 |     63 |

## Overseen events by senator (top 10)

| senator              |   purchase |   sale |
|:---------------------|-----------:|-------:|
| Tommy Tuberville     |         43 |     79 |
| Markwayne Mullin     |         27 |     10 |
| Jerry Moran          |          9 |     19 |
| Gary C. Peters       |          4 |      3 |
| John W. Hickenlooper |          2 |      8 |
| Dan Sullivan         |          2 |     13 |
| Ashley Moody         |          1 |      2 |
| Patrick J. Toomey    |          1 |      0 |
| John Kennedy         |          1 |      0 |
| Bernie Moreno        |          0 |      2 |
