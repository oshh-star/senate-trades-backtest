# Committee test, out-of-sample half (2024-03-01 to 2026-08-31), YAHOO

**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, "Out-of-sample test plan"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few cells in a table like this one will reach |t| = 2 by chance.**

**Prices: Yahoo, the final headline source (R3, S2).** Stocks in the survivorship ledger (mostly delisted names Yahoo no longer serves) have no prices: their events drop out here and their purchases are skipped in the book; V15 (SPY fill) bounds the effect.

_src/metrics/committee.py. An event is **overseen** when, on its transaction date, the senator sat on a committee in config/committee_industries.yaml (committed at a124f03 before this split was computed, E54) whose SIC ranges contain the company's SIC code. Membership: the latest version of congress-legislators' committee-membership-current.yaml committed on or before the trade date. Cells: mean SPY-adjusted return (t clustered by entry month); copier from the entry date, senator from the transaction date; "t n/a" = fewer than 5 entry months. After a SALE a NEGATIVE number is informative._

## The split

| side     | group                                                               |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:--------------------------------------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | overseen by the senator's committee                                 |       27 | +12.14% (1.05) | +21.89% (1.16) | +9.42% (0.77)  | +1.32% (0.60)  | +6.07% (1.19)  | +4.52% (0.53)  | 27 / 24                 | -2.02% (-0.87)         |
| purchase | not overseen                                                        |      614 | +1.05% (1.80)  | +1.88% (1.27)  | +1.07% (0.48)  | -2.75% (-2.57) | +0.17% (0.20)  | +2.41% (1.12)  | 599 / 207               | -1.19% (-1.97)         |
| purchase | difference (overseen by the senator's committee minus not overseen) |      641 | +11.09% (0.98) | +20.02% (1.08) | +8.34% (0.72)  | +4.07% (1.67)  | +5.90% (1.16)  | +2.11% (0.26)  | 626 / 231               | -0.83% (-0.38)         |
| sale     | overseen by the senator's committee                                 |       48 | +3.18% (2.09)  | +2.27% (0.88)  | -1.72% (-0.44) | +2.56% (0.71)  | +4.85% (0.93)  | -0.35% (-0.06) | 46 / 42                 | -0.79% (-0.37)         |
| sale     | not overseen                                                        |      383 | +0.88% (1.10)  | +1.38% (0.76)  | +2.43% (0.72)  | -0.88% (-0.76) | -1.16% (-0.63) | +3.40% (0.88)  | 355 / 269               | -1.18% (-0.86)         |
| sale     | difference (overseen by the senator's committee minus not overseen) |      431 | +2.30% (1.70)  | +0.89% (0.27)  | -4.15% (-0.91) | +3.43% (0.86)  | +6.01% (0.92)  | -3.75% (-0.50) | 401 / 311               | +0.39% (0.13)          |

## Events by group

| side     |   left out: ETF |   left out: no SIC code |   not overseen |   overseen by the senator's committee |
|:---------|----------------:|------------------------:|---------------:|--------------------------------------:|
| purchase |              36 |                     296 |            614 |                                    27 |
| sale     |              70 |                       7 |            383 |                                    48 |

## Overseen events by committee (an event can count under two committees)

|                                             |   purchase |   sale |
|:--------------------------------------------|-----------:|-------:|
| SSAF Agriculture, Nutrition, and Forestry   |          0 |      9 |
| SSAS Armed Services                         |          3 |      5 |
| SSBK Banking, Housing, and Urban Affairs    |          1 |      3 |
| SSCM Commerce, Science, and Transportation  |          7 |      4 |
| SSHR Health, Education, Labor, and Pensions |         16 |     27 |

## Overseen events by senator (top 10)

| senator              |   purchase |   sale |
|:---------------------|-----------:|-------:|
| Markwayne Mullin     |         11 |      9 |
| Tommy Tuberville     |          7 |     28 |
| Jerry Moran          |          3 |      2 |
| Gary C. Peters       |          2 |      2 |
| John W. Hickenlooper |          2 |      0 |
| Ashley Moody         |          1 |      2 |
| John Kennedy         |          1 |      0 |
| Bernie Moreno        |          0 |      2 |
| John Boozman         |          0 |      2 |
| Bill Hagerty         |          0 |      1 |
