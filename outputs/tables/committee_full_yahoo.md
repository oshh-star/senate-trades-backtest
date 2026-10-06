# Committee test, full window (2021-09-01 to 2026-08-31), YAHOO

**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, "Out-of-sample test plan"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few cells in a table like this one will reach |t| = 2 by chance.**

**Prices: Yahoo, the final headline source (R3, S2).** Stocks in the survivorship ledger (mostly delisted names Yahoo no longer serves) have no prices: their events drop out here and their purchases are skipped in the book; V15 (SPY fill) bounds the effect.

_src/metrics/committee.py. An event is **overseen** when, on its transaction date, the senator sat on a committee in config/committee_industries.yaml (committed at a124f03 before this split was computed, E54) whose SIC ranges contain the company's SIC code. Membership: the latest version of congress-legislators' committee-membership-current.yaml committed on or before the trade date. Cells: mean SPY-adjusted return (t clustered by entry month); copier from the entry date, senator from the transaction date; "t n/a" = fewer than 5 entry months. After a SALE a NEGATIVE number is informative._

## The split

| side     | group                                                               |   events | copier 21d    | copier 63d    | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:--------------------------------------------------------------------|---------:|:--------------|:--------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | overseen by the senator's committee                                 |       90 | +3.04% (0.80) | +4.94% (0.80) | +2.47% (0.64)  | +2.01% (1.24)  | +0.79% (0.36)  | +1.52% (0.51)  | 89 / 86                 | +1.16% (0.55)          |
| purchase | not overseen                                                        |      977 | +1.25% (2.98) | +1.65% (1.89) | +1.34% (1.24)  | -1.60% (-1.42) | +0.58% (0.81)  | +1.95% (1.66)  | 941 / 549               | -0.67% (-1.12)         |
| purchase | difference (overseen by the senator's committee minus not overseen) |     1067 | +1.79% (0.47) | +3.29% (0.53) | +1.13% (0.29)  | +3.61% (1.77)  | +0.21% (0.09)  | -0.44% (-0.14) | 1030 / 635              | +1.83% (0.85)          |
| sale     | overseen by the senator's committee                                 |      153 | +0.63% (0.74) | +2.32% (1.41) | +0.43% (0.19)  | +1.68% (1.32)  | +2.80% (1.48)  | +2.71% (1.16)  | 149 / 145               | +0.77% (0.93)          |
| sale     | not overseen                                                        |      713 | +0.41% (0.75) | +0.63% (0.66) | -0.07% (-0.04) | -0.69% (-1.00) | -0.89% (-0.79) | +0.47% (0.22)  | 643 / 557               | -0.73% (-0.84)         |
| sale     | difference (overseen by the senator's committee minus not overseen) |      866 | +0.22% (0.24) | +1.69% (0.85) | +0.51% (0.19)  | +2.38% (1.53)  | +3.69% (1.39)  | +2.24% (0.68)  | 792 / 702               | +1.49% (1.18)          |

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
