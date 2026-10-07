# Committee test, in-sample (2021-09-01 to 2024-02-29), YAHOO

**Prices: Yahoo, the final headline source (R3, S2).** Stocks in the survivorship ledger (mostly delisted names Yahoo no longer serves) have no prices: their events drop out here and their purchases are skipped in the book; V15 (SPY fill) bounds the effect.

_src/metrics/committee.py. An event is **overseen** when, on its transaction date, the senator sat on a committee in config/committee_industries.yaml (committed at a124f03 before this split was computed, E54) whose SIC ranges contain the company's SIC code. Membership: the latest version of congress-legislators' committee-membership-current.yaml committed on or before the trade date. Cells: mean SPY-adjusted return (t clustered by entry month); copier from the entry date, senator from the transaction date; "t n/a" = fewer than 5 entry months. After a SALE a NEGATIVE number is informative._

## The split

| side     | group                                                               |   events | copier 21d     | copier 63d     | copier 126d    | senator 21d    | senator 63d    | senator 126d   | N (copier 21d / 126d)   | pre-disclosure drift   |
|:---------|:--------------------------------------------------------------------|---------:|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:------------------------|:-----------------------|
| purchase | overseen by the senator's committee                                 |       63 | -0.92% (-0.61) | -1.92% (-0.57) | -0.80% (-0.20) | +2.30% (1.07)  | -1.21% (-0.56) | +0.60% (0.15)  | 62 / 40                 | +2.55% (0.88)          |
| purchase | not overseen                                                        |      363 | +1.59% (2.20)  | +0.84% (0.74)  | -0.07% (-0.04) | +0.42% (0.81)  | +0.94% (1.18)  | -0.95% (-0.52) | 342 / 183               | +0.26% (0.61)          |
| purchase | difference (overseen by the senator's committee minus not overseen) |      426 | -2.51% (-1.43) | -2.76% (-0.85) | -0.73% (-0.17) | +1.89% (0.85)  | -2.15% (-0.89) | +1.56% (0.35)  | 404 / 223               | +2.29% (0.79)          |
| sale     | overseen by the senator's committee                                 |      105 | -0.25% (-0.28) | +3.45% (1.41)  | +3.01% (0.74)  | +1.29% (1.52)  | +2.92% (2.16)  | +5.15% (1.76)  | 93 / 68                 | +1.48% (2.08)          |
| sale     | not overseen                                                        |      330 | -0.24% (-0.33) | -0.01% (-0.01) | -1.23% (-0.49) | -0.45% (-0.94) | -1.02% (-0.75) | -0.84% (-0.32) | 256 / 151               | -0.14% (-0.20)         |
| sale     | difference (overseen by the senator's committee minus not overseen) |      435 | -0.02% (-0.01) | +3.45% (1.27)  | +4.24% (0.87)  | +1.74% (2.14)  | +3.95% (2.25)  | +5.99% (1.40)  | 349 / 219               | +1.62% (1.80)          |

## Events by group

| side     |   left out: ETF |   left out: no SIC code |   not overseen |   overseen by the senator's committee |
|:---------|----------------:|------------------------:|---------------:|--------------------------------------:|
| purchase |               7 |                       2 |            363 |                                    63 |
| sale     |               7 |                       5 |            330 |                                   105 |

## Overseen events by committee (an event can count under two committees)

|                                             |   purchase |   sale |
|:--------------------------------------------|-----------:|-------:|
| SSAF Agriculture, Nutrition, and Forestry   |          7 |     13 |
| SSAS Armed Services                         |          8 |      8 |
| SSBK Banking, Housing, and Urban Affairs    |          3 |     11 |
| SSCM Commerce, Science, and Transportation  |          7 |     36 |
| SSEG Energy and Natural Resources           |          0 |      1 |
| SSHR Health, Education, Labor, and Pensions |         38 |     36 |

## Overseen events by senator (top 10)

| senator              |   purchase |   sale |
|:---------------------|-----------:|-------:|
| Tommy Tuberville     |         36 |     51 |
| Markwayne Mullin     |         16 |      1 |
| Jerry Moran          |          6 |     17 |
| Dan Sullivan         |          2 |     13 |
| Gary C. Peters       |          2 |      1 |
| Patrick J. Toomey    |          1 |      0 |
| Bill Hagerty         |          0 |      8 |
| Deb Fischer          |          0 |      3 |
| John W. Hickenlooper |          0 |      8 |
| Maria Cantwell       |          0 |      1 |
