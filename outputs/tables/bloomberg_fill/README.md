# Bloomberg-filled run (NOT the headline)

Built 2026-10-07 (PARA added the same day) by Claude, in a separate copy of the repo, with one change: `prices.sources: [yahoo, manual]`
(Yahoo first; Bloomberg terminal prices in data/raw/manual_prices/ fill symbols Yahoo has no price for).
Files filled: X, ECOM, ATVI, SSBK, PARA, WBA, GOGL, TOELY, all 8 MUST-HAVE rows (see data/raw/manual_prices/SOURCES.md).
PARA's first pull (PARA US Equity) was a different security and was discarded; the re-pull uses 2677689D US Equity. The headline (`prices.sources: [yahoo]`, decisions S2/S3) is unchanged;
using these numbers in the report needs a group decision logged in docs/DECISIONS.md.

| Full window 2021-09 to 2026-08 | Headline (Yahoo only) | Bloomberg-filled |
|---|---|---|
| Series A return, a year | 10.81% | 13.41% |
| SPY | 12.69% | 12.69% |
| SPY risk-matched to A | 15.83% | 16.30% |
| CAPM alpha (OLS t) | -1.48% (-0.29) | +1.07% (0.18) |
| Carhart alpha (OLS t) | -0.74% (-0.14) | +2.26% (0.36) |
| Max drawdown | -32.15% | -32.16% |
| Excess over risk-matched SPY | -4.48% | -2.58% |

Second half (2024-03 to 2026-08): series A 22.95% -> 22.94%. Confirmatory tests H0-H4: every verdict unchanged.
For reference, V15 (ledger purchases earn SPY) gave 11.63%: the real prices are HIGHER than that "bound", because the
missing stocks were mostly takeover targets that rose on the bid.

**Variants with Bloomberg prices** (2026-10-09, `variants_full.md` / `.csv`): every pre-registered variant rerun with the
same one change. No full-window or second-half alpha reaches |t| = 2 (with Yahoo, V12's second-half Carhart t was -2.11;
here -1.75). The gain from Bloomberg sits almost entirely in Tuberville's trades: leaving him out (V1) gives 13.32% with
Yahoo and 13.31% with Bloomberg. V2.2 (no Armstrong) 13.15%; V4 (no bulk filings) 11.38%; V15 (remaining ledger
purchases earn SPY) 13.42%.
