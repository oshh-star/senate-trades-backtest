# Committee test, out-of-sample half (2024-03-01 to 2026-08-31), BLOOMBERG

**EXPLORATORY.** Not one of the registered confirmatory tests (H0-H4, docs/DECISIONS.md, "Out-of-sample test plan"; outputs/tables/confirmatory_oos.md). Roughly 150 cells were examined in-sample, so a few cells in a table like this one will reach |t| = 2 by chance.**

**Prices: Yahoo, with Bloomberg terminal prices where Yahoo has none** (`prices.sources: [yahoo, manual]`, post-unlock correction C1, 2026-10-09): 8 delisted stocks (X, ECOM, ATVI, SSBK, PARA, WBA, GOGL, TOELY; 95% of the missing headline dollars) are priced from data/raw/manual_prices/. The other survivorship-ledger stocks still have no prices: their events drop out here and their purchases are skipped in the book. V18 is the Yahoo-only run (the headline before C1).

_src/metrics/committee.py. An event is **overseen** when, on its transaction date, the senator sat on a committee in config/committee_industries.yaml (committed at a124f03 before this split was computed, E54) whose SIC ranges contain the company's SIC code. Membership: the latest version of congress-legislators' committee-membership-current.yaml committed on or before the trade date. Cells: mean SPY-adjusted return (t clustered by entry month); copier from the entry date, senator from the transaction date; "t n/a" = fewer than 5 entry months. After a SALE a NEGATIVE number is informative._

## The split

| side     | group                                                               |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:--------------------------------------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | overseen by the senator's committee                                 |       27 | +12.14% (1.05) | +21.89% (1.16) | +9.42% (0.77)  | +1.32% (0.60)  | +6.07% (1.19)  | +4.52% (0.53)  | 27 / 24                 | -2.02% (-0.87)         |
| purchase | not overseen                                                        |      614 | +1.07% (1.86)  | +1.65% (1.13)  | +0.75% (0.34)  | -2.73% (-2.54) | +0.10% (0.12)  | +2.08% (0.97)  | 603 / 211               | -1.22% (-2.07)         |
| purchase | difference (overseen by the senator's committee minus not overseen) |      641 | +11.07% (0.98) | +20.24% (1.09) | +8.67% (0.73)  | +4.05% (1.66)  | +5.97% (1.16)  | +2.44% (0.29)  | 630 / 235               | -0.80% (-0.37)         |
| sale     | overseen by the senator's committee                                 |       48 | +3.18% (2.09)  | +2.27% (0.88)  | -1.72% (-0.44) | +2.56% (0.71)  | +4.85% (0.93)  | -0.35% (-0.06) | 46 / 42                 | -0.79% (-0.37)         |
| sale     | not overseen                                                        |      383 | +0.80% (0.88)  | +1.16% (0.63)  | +2.14% (0.63)  | -0.95% (-0.82) | -1.31% (-0.70) | +2.98% (0.75)  | 359 / 273               | -1.23% (-0.88)         |
| sale     | difference (overseen by the senator's committee minus not overseen) |      431 | +2.38% (1.80)  | +1.10% (0.33)  | -3.87% (-0.84) | +3.50% (0.87)  | +6.16% (0.94)  | -3.33% (-0.44) | 405 / 315               | +0.44% (0.15)          |

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
