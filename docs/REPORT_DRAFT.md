# Copying the US Senate: does it pay to trade on senators' disclosed stock trades?

_LBS CA01 Investment Fundamentals, Autumn 2026. Group [GROUP NUMBER AND NAMES]._

> **DRAFT (2026-10-09), written by Claude for the group to edit.** Every number comes from a committed file and is
> rebuilt by `python run_all.py --skip-scrape`; the source file is named in brackets after each table or claim, so it
> can be checked. Wording marked **[GROUP]** needs a decision or a check. The limit is 10 pages at 11pt including
> tables and figures (the appendix and references are extra), so this draft is longer than the final report and is
> meant to be cut.

---

## 1. The recommendation

**Do not invest.** We copied every stock trade a US senator disclosed, buying on the first trading day after a purchase
became public and selling when the same senator disclosed a sale. Over five years, September 2021 to August 2026, the
strategy returned **13.41% a year at 23.41% volatility** (Sharpe ratio 0.50). Buying SPY returned **12.69% at 15.87%**
(Sharpe 0.61). At the same volatility as the strategy, SPY would have returned **16.30%**. The strategy's CAPM alpha is
**+1.07% a year (t = 0.18)** and its Carhart four-factor alpha is **+2.26% (t = 0.37)**: both are statistically zero. Its
extra return came from a market beta of 1.21 and a small-cap tilt, which an investor can buy for a few basis points.
The second half of the window, which we did not look at while designing the rules, tells the same story: 22.94% a year
against 19.32% for SPY and 26.02% for SPY at the same risk, with an alpha of +1.69% (t = 0.29). Two senators supplied
most of the profit. The evidence also points away from informed trading: on average, the stocks senators bought had
done 2% *worse* than SPY between the trade and its disclosure.

## 2. The strategy, precisely stated

Every rule below was fixed before the second half of the data was opened. The rules were frozen at git commit
`3483184` on 6 October 2026 (`docs/DECISIONS.md`, entries F1 and U1). One rule about prices was corrected later
(Section 6.4).

| Rule | What we did |
|---|---|
| **Signal** | Every Periodic Transaction Report (PTR) filed electronically on the Senate's eFD site (efdsearch.senate.gov), keyed to the date and time it was **received**, which is when it became public. |
| **Who** | Anyone serving as a senator on the transaction date, using official service dates (congress-legislators). eFD's filer label shows the filer's status today, not on the trade date, so it is not used. |
| **What** | US common stocks and US-listed **equity** ETFs, including ADRs and OTC names. Out: options, bonds, listed notes, preferred shares, mutual funds, crypto, and bond, commodity or T-bill ETFs. |
| **Whose** | Trades owned by the senator ("Self") or held jointly. Spouse and child trades are out (variant V6 adds them). |
| **Buy** | At the adjusted close of the **first NYSE trading day after** the disclosure date. Filings often arrive after the close, so this is the first price a copier could certainly get. |
| **Size** | The midpoint of the disclosed dollar band ($1,001-$15,000 becomes $8,000.50); the open top band uses its lower bound. |
| **Sell** | When the same senator discloses a sale of the same stock: "Sale (Full)" closes every lot; "Sale (Partial)" sells the band midpoint, capped at what we hold, oldest lot first (FIFO). |
| **Never** | No shorting. A sale of something we never copied is ignored. Exchanges are ignored. |
| **Amendments** | Each record acts as first published, at its own time. A later correction reverses the original action and then acts on the corrected record at the amendment's time (no look-ahead). |
| **End** | Open positions are marked at the last close. A stock that stops trading closes at its last price. |
| **Start** | The book is built from disclosures in the 12 months before the window, so it is already full on day one. Returns are measured from 1 September 2021 only. |
| **Return** | Series A (the headline): the daily dollar-weighted return of the open positions, i.e. a return on the capital actually deployed. A day with nothing held earns the risk-free rate. Series B: one fixed pot (peak capital needed plus the opening book), with idle cash earning the risk-free rate. |

Series A answers "what did the money in senators' stocks earn?". Series B answers "what did a fixed pot earn, cash
included?". Series B's pot is sized on the whole window's peak need, so it held a lot of cash in 2022. That makes it a
partly market-timed series, so we use series A as the headline. [`config/config.yaml`; `docs/DECISIONS.md` D10-D15, J3,
L2, E31]

## 3. Why it might work, and who is on the other side

**The mechanism we test is information.** Senators sit on committees that hear about regulation, contracts and
investigations before the market does. If they trade on that, the stocks they buy should rise and the stocks they sell
should fall. The STOCK Act forces disclosure within 45 days of the trade (the median purchase in our sample was
disclosed after 40 calendar days), and a copier hopes some of the information is still unpriced on disclosure day.
The people on the other side of the copier's trade are investors who have not read the filing, or have not acted on it.

**What would make this a story that fits any result, and how we guard against it.** "Senators know things" would
explain a positive return, and "the market prices disclosures instantly" would explain a zero. So before opening the
second half, we registered four checkable implications of the information story (`docs/DECISIONS.md`, "Out-of-sample
test plan", registered 30 September 2026):

- **H1, information before disclosure.** If senators trade on information, their purchases should beat SPY *between
  the trade and the disclosure*, and their sales should lag it.
- **H2, drift after disclosure.** If copiers move prices, a short-term gain after disclosure should *reverse* later; if
  it is information, it should not.
- **H3, committees.** Sales of stocks overseen by the senator's own committee should do worse than other sales. In the
  first half they did the opposite (+3.95%); we predicted this would disappear.
- **H4, size.** If information drives the trade, senators should bet more on it, so large purchases should beat small
  ones (small minus large should be negative).

**And a second mechanism the data suggest: there is no edge, only exposure.** Senators' portfolios lean towards the
market and small caps, so a copier collects beta and size, not information. This predicts a zero alpha (H0) with
large, significant factor loadings. Section 5 tests both.

## 4. Data and sample

| Item | Choice |
|---|---|
| Trades | Senate eFD PTRs received 2016-01-01 to 2026-09-30, scraped directly at one request per second, and every page cached and submitted. Paper (scanned) filings cannot be parsed reliably; they are counted and excluded. |
| Window | Disclosures from 2021-09-01 to 2026-08-31 (60 months), plus the 12-month warm-up. The end date is the last month in the Ken French data. The 3-year and 10-year windows are variants. |
| Split | First half 2021-09 to 2024-02 (used to design the rules); second half 2024-03 to 2026-08 (opened once, after the freeze). |
| Prices | Yahoo Finance adjusted close (total return, dividends reinvested), plus Bloomberg terminal prices for 8 delisted stocks Yahoo no longer serves. |
| Currency | US dollars. For a UK investor the strategy returned 13.78% a year in sterling (SPY 13.06%). |
| Risk-free rate | Ken French US RF, one series throughout. |
| Factors | Ken French US market, SMB, HML and momentum (the same region as the strategy). |
| Frequency | The engine runs daily; every statistic and regression uses monthly returns. Drawdowns use the daily value index. |
| As first published | Trades enter as first published (amendments act at their own date); prices are a September 2026 vintage. |

**What the copier traded.** Over the window there were 2,363 in-scope trade records from 31 senators (1,408 purchases,
955 sales). The copier opened 1,475 lots in 827 symbols; the median lot was held 91 days. Four senators placed 92% of the
dollars copied (warm-up included): Tuberville 42%, Mullin 23%, Armstrong 22% and Moody 5%. Every exclusion is counted with its reason in
`outputs/data_quality.md`. [`data/processed/event_panel.csv`, `lots.csv`]

**Survivorship.** Yahoo drops delisted companies, and senators bought several stocks that were later taken over. We
listed every symbol with no usable price and the reason for it (`data/interim/survivorship_ledger.csv`). With Yahoo
alone, those skipped purchases would have been up to **67% of the capital deployed** (October 2022). We pulled the 8
largest (95% of the missing dollars) from a Bloomberg terminal. The remaining 178 symbols are now at most **2.2%** of
capital (median 0.3%). [`outputs/data_quality.md`, Phase 4 section 10]

**The missing stocks pushed the return down, not up.** The usual worry about survivorship is that the dead stocks were
losers, so leaving them out flatters the result. Here it ran the other way. Seven of the 8 we priced were taken over at
a premium (U.S. Steel, ChannelAdvisor, Activision and others), so pricing them raised series A from 10.81% (Yahoo only,
variant V18) to 13.41% a year. For the same reason, filling the gaps with SPY's return (variant V15) is not a bound:
with Yahoo only it gave 11.63%, below the 13.41% the real prices give. Every copied position in these stocks was
closed by the senator's own disclosed sale before the takeover, so the takeover dates themselves do not enter the
portfolio; in 8 of the 2,363 event-study trades the horizon runs past a cash takeover and the deal price is held flat.

## 5. Results

**Table 1. Copying the Senate against the alternatives, 1 September 2021 to 31 August 2026 (60 months, identical
dates).** [`outputs/tables/phase5_full_results.md`]

| | Series A (headline) | SPY | SPY at series A's risk (k = 1.48) | Senate universe, equal weight |
|---|---|---|---|---|
| Return, a year (geometric) | 13.41% | 12.69% | 16.30% | 13.56% |
| Volatility, a year | 23.41% | 15.87% | 23.47% | 17.14% |
| Sharpe ratio | 0.50 | 0.61 | 0.61 | 0.62 |
| CAPM alpha, a year (Newey-West t) | +1.07% (0.18) | | | +1.72% (0.74) |
| CAPM beta | 1.21 | 0.98 | | 1.01 |
| Carhart alpha, a year (Newey-West t) | +2.26% (0.37) | | | +1.68% (0.77) |
| Loadings: market, SMB, HML, MOM | 1.18, 0.33, 0.07, 0.07 | | | 1.01, 0.13, 0.14, -0.06 |
| Smallest alpha detectable at t = 2 | 11.9% (CAPM), 12.4% (Carhart) | | | |
| Maximum drawdown | -32.16% | -24.50% | -35.31% | -24.58% |
| Peak, trough, recovery | 2022-03-25, 2022-07-14, 2024-03-01 | 2022-01-03, 2022-10-12, 2023-12-13 | 2022-01-03, 2022-10-12, 2024-01-19 | 2021-11-16, 2022-10-14, 2023-12-14 |
| Correlation with SPY (all months; SPY's worst 12) | 0.81; 0.68 | 1 | 1 | 0.94; 0.87 |
| One-way turnover, a year | 102% | | | |
| Return over risk-matched SPY, a year | -2.58% | | | |

The **benchmarks** answer three questions. *SPY*: could a passive investor have done as well? *SPY at the same risk*
(the risk-free rate plus 1.48 times SPY's excess return, so its volatility matches series A's): is the extra return
just leverage? *The Senate universe* (every stock a senator bought in the previous 12 months, equal weight, rebalanced
monthly): does it matter WHEN we trade, or only WHICH stocks senators like? The Carhart model is the style benchmark.

**What Table 1 says.** The strategy beat SPY by 0.7 points a year, but it took 1.5 times SPY's volatility to do it. At
the same risk, SPY would have earned 2.9 points more. Nothing is left once beta and size are accounted for: both
alphas are under one standard error from zero. The equal-weighted universe of senators' stocks did as well as the
strategy (13.56%) with less risk, so the timing of the copied trades added nothing beyond the stock list. **But the test
cannot rule much out:** with 60 months and this much residual volatility, only an alpha of about 12% a year would have
reached t = 2.

**Figure 1** (`outputs/figures/phase5_cumulative_value.png`) shows the value of $1 in series A, SPY and risk-matched
SPY, with the design/test boundary marked. **Figure 2** (`outputs/figures/phase5_drawdowns.png`) shows the drawdowns.
The strategy fell 32% between March and July 2022, more than SPY's 24.5%, and took until March 2024 to recover.

**Table 2. Year by year.** [`outputs/tables/phase5_full_results.md`, calendar-year returns]

| | 2021 (Sep-Dec) | 2022 | 2023 | 2024 | 2025 | 2026 (Jan-Aug) |
|---|---|---|---|---|---|---|
| Series A | -2.25% | -6.01% | +19.94% | +5.02% | +27.88% | +26.76% |
| SPY | +5.89% | -18.18% | +26.18% | +24.89% | +17.72% | +13.08% |
| SPY at series A's risk | +8.51% | -27.63% | +36.85% | +35.02% | +24.29% | +17.99% |
| Senate universe | +1.94% | -15.39% | +22.18% | +17.06% | +29.79% | +17.97% |

The strategy beat SPY in three of six (part-)years: it lost less in 2022 and won in 2025 and 2026. It badly trailed
SPY in 2023 and 2024. Its worst 12 months (November 2021 to October 2022) lost 13.7%, against 14.6% for SPY over the same
months.

**The copier against the senator (Table 3).** For every trade we also measured what the senator earned from the
*transaction* date. [`outputs/tables/phase5_event_study_full.md`, `phase5_predisclosure_drift_full.md`; EXPLORATORY]

| Purchases, return minus SPY | 5 days | 21 days | 63 days | 126 days | 252 days |
|---|---|---|---|---|---|
| Senator (from the trade) | -0.08% | -2.44% | -1.28% | +2.06% | +2.55% |
| Copier (from the disclosure) | +1.91% | +1.56% | +1.91% | +1.66% | +1.77% |
| Events (5 days / 252 days) | 1,392 / 603 | | | | |

Between the trade and its disclosure (a median of 29 trading days), the stocks senators bought lagged SPY by **2.06%**
(t = -1.6, clustered by entry month). The senators did not buy ahead of good news. The copier's small gains after
disclosure are statistically fragile (5-day t = 2.09, 21-day t = 3.69; none from 63 days on reaches t = 2), and they are the kind of
cell Section 6 warns about.

**The registered tests (Table 4)**, judged on the second half only, at Holm-adjusted 5%.
[`outputs/tables/confirmatory_oos.md`]

| Test | Prediction | Second-half estimate (t) | Holm p | Smallest effect detectable (Bonferroni level) | Verdict | Without bulk filings |
|---|---|---|---|---|---|---|
| H0 CAPM alpha | zero | +1.69% a year (0.29) | 1 | ±15.8% | not distinguishable from zero | |
| H0 Carhart alpha | zero | +0.40% a year (0.06) | 1 | ±19.2% | not distinguishable from zero | |
| H1 purchases' pre-disclosure drift | close to zero | -3.22% (-2.98) | 0.017 | ±2.9% | **significantly negative** | -0.11% (-0.18) |
| H1 sales' pre-disclosure drift | close to zero | -0.99% (-0.96) | 1 | ±2.8% | not distinguishable from zero | +0.68% (1.22) |
| H2 copier purchases, 21 days (one-sided) | is it positive? | +1.74% (3.54) | 0.001 | | **positive** | +1.12% (0.81) |
| H3 committee sales, overseen minus not | disappears | +6.16% (0.94) | 1 | | not distinguishable from zero | |
| H4 small minus large purchases, 126 days | negative if informed | +4.82% (0.96) | 1 | ±13.5% | not distinguishable from zero | +1.72% (0.41) |

H0, H3 and H4 came out as predicted. H1 broke our "close to zero" prediction, but in the direction *against*
information: the stocks senators bought lagged the market before disclosure. H2 is positive, and its reversal check is
mixed: at 126 days the gain is +1.73% (t 0.77), a hair below the 21-day mean (which our rule calls "partly reversed"),
and at 252 days it is +12.03% (t 2.01).

**[GROUP] Both significant results rest on one filing.** Alan Armstrong's report disclosed on 21 July 2026 listed 654
purchases of 621 stocks, all bought on 27-31 March 2026: 67% of the second half's purchases, all in one entry month.
A standard error clustered by month, with one cluster holding two-thirds of the events, overstates precision. We
registered the check before opening the data (R2): without filings of 50 or more trades, H1 for purchases is -0.11%
(t -0.18) and H2 is +1.12% (t 0.81). Both are noise. The portfolio result does not depend on him (Section 6). The
registered verdicts stand as computed; the reader should weigh them with this caveat.

## 6. Robustness

**6.1 The half we did not use.** Opening the second half did not change the verdict. Second half: series A 22.94% a
year (volatility 17.47%, Sharpe 1.03) against SPY 19.32% (Sharpe 1.17), risk-matched SPY 26.02% and the Senate universe
23.12%. CAPM alpha +1.69% (t 0.29); Carhart +0.40% (t 0.06). [`outputs/tables/phase5_oos_results.md`] First half:
series A 4.61% a year against SPY's 6.43% (from `data/processed/monthly_returns.csv`).

**6.2 Every variant we tried.** We registered 20 robustness variants before computing any return. V2 is five runs, so
there are 24 runs; V20 needed CRSP data that never arrived, so 23 have results. Each changes one rule and keeps
everything else as in the headline. [`outputs/tables/variants_full_bloomberg.md`, EXPLORATORY]

| Variant | Return, a year | CAPM alpha (t) |
|---|---|---|
| Headline | 13.41% | +1.07% (0.18) |
| V1 / V2.1 without Tuberville | 13.31% | +1.92% (0.51) |
| V2.2 without Armstrong | 13.15% | +0.84% (0.14) |
| V2.3 without Mullin | 18.64% | +5.79% (0.74) |
| V3 without senators' first 180 days | 9.43% | -2.28% (-0.42) |
| V4 without bulk filings (50+ trades) | 11.38% | -0.98% (-0.14) |
| V5 without ETFs | 13.41% | +1.11% (0.18) |
| V6 with spouse and child trades | 14.12% | +1.60% (0.49) |
| V7 / V8 sizing at the lower bound / equal dollars | 13.41% / 12.42% | +1.08% / +0.88% |
| V9 same-day close for filings before 15:30 ET | 13.89% | +1.48% (0.25) |
| V10 equal-weight portfolio | 12.50% | +0.77% (0.30) |
| V11 3-year window (2023-09 to 2026-08) | 25.50% | +2.36% (0.39) |
| V12 10-year window (2016-09 to 2026-08) | 15.57% | -1.23% (-0.27) |
| V13 without OTC names | 13.30% | +0.97% (0.16) |
| V14 amendments "as revised" | 13.20% | +0.84% (0.14) |
| V15 skipped purchases earn SPY | 13.42% | +1.07% (0.18) |
| V16 all ETFs (bond, commodity) | 11.97% | -0.13% (-0.02) |
| V17 empty start (no warm-up) | 15.43% | +2.99% (0.49) |
| V18 Yahoo prices only | 10.81% | -1.48% (-0.29) |
| V19 with preferred shares | 13.41% | +1.07% (0.18) |

The returns span 9.4% to 25.5% (the 3-year window covers different dates), and **no variant's alpha reaches |t| = 2**
in either the full window or its own second half. The spread itself is informative: leaving out a single senator moves
the return by up to 5 points (V2.3: Mullin's large positions earned less than the rest of the book, so without him
series A rises to 18.64%). Leaving out the first 180 days of each senator's
service, when new senators restructure their portfolios, takes 4 points off. A strategy whose result depends this
much on who happens to be in the Senate is not an edge an investor can rely on.

**6.3 How many things we looked at.** Besides the 24 variant runs, the first half produced about 150 table cells
(horizons, sides, splits by size, party, filing lag, senator and committee). That is why only the seven registered
statistics in Table 4 count as tests. Across the full-window and second-half tables, 78 exploratory cells reach |t| = 2,
and most of them in the second half are the same Armstrong filing. **[GROUP]** this count is from the Yahoo-only run
(6 October); recount on the corrected tables before quoting it. [`outputs/tables/mechanism_*_bloomberg.md`, `committee_*_bloomberg.md`]

**6.4 Decisions made after seeing results (logged).** Three choices were made with some results in view, and we report
the alternative beside each:
(a) the 12-month warm-up replaced an empty start after the first-half results were seen (the empty start is V17,
15.43%);
(b) preferred shares were taken out as not being common equity (V19 puts them back; no change);
(c) **after the second half was opened**, we priced 8 delisted stocks from a Bloomberg terminal, instead of skipping
them as the frozen rule did. This is logged as post-unlock correction C1 with every before and after value. The
Yahoo-only result is V18: 10.81% a year, alpha -1.48% (t -0.29). The correction raised the return by 2.6 points,
almost all of it in the first half (U.S. Steel, ChannelAdvisor and Activision rose on takeover bids). It did not
change any verdict. **[GROUP] We chose the corrected number as the headline because it uses real prices for stocks
the senators really bought; the reader can see both.**

## 7. Costs

Series A turns over about 102% of its capital a year one-way. Its return is already 2.6 points a year *below* SPY at the
same risk before any costs, so there is no break-even cost: any cost only widens the gap. Most positions are large,
liquid US stocks and ETFs, 92% of the copied purchases are in the two smallest bands (up to $50,000), which is small for
those stocks, but Armstrong's 654-stock basket would have to be bought in one day. Costs can only make the verdict stronger.

## 8. What would change our mind

**The strongest case for the strategy.** It beat SPY over the five years (13.41% against 12.69%) and in the
second half (22.94% against 19.32%). It lost less in the 2022 bear market. Its full-window Carhart alpha is positive.
An investor who cannot borrow cannot buy "SPY at 1.48 times leverage", so for them the plain SPY comparison is the one
that matters. And our test could not have detected an alpha below about 12% a year.

**Why we still say no.** (1) The extra return is beta (1.21) and size (SMB 0.33), not skill: the risk-matched
comparison is the fair one even for an investor who cannot borrow, because the same risk is available through a
small-cap or high-beta fund. (2) The pre-disclosure evidence runs against information: senators' purchases lagged the
market before disclosure. (3) Profits are concentrated: two senators (Mullin and Moody) account for about three-quarters
of the dollar profit, and dropping a single senator moves the return by up to 5 points. (4) The two ETFs that sell this idea did
not beat the market either: over their 42 months NANC returned 24.75% a year and KRUZ 19.31%, against SPY's 22.32% and our
strategy's 19.34% over the same months; neither has a CAPM alpha distinguishable from zero (t 0.44 and -0.39).
**[GROUP]** check NANC's and KRUZ's methodology before describing them further. [`outputs/tables/phase5_full_results.md`, panel 2]

**What would change it.** A longer sample with prices for every delisted stock (CRSP) and a positive alpha of, say,
5% a year that survives without the top two senators. Or evidence that senators' purchases beat the market *before*
disclosure, which is what information would look like.

## 9. Weaknesses we know about

- **Short sample.** 60 months, 30 per half; only very large alphas would be detectable (Table 1).
- **Survivorship.** 178 delisted symbols are still unpriced (at most 2.2% of capital). Filling them with SPY (V15)
  gives 13.42%, almost the headline, so the gap is now small. It is not a bound: the 8 stocks we did price were
  takeover targets that *raised* the return (10.81% to 13.41%), so if the remaining gap biases anything, it most likely
  biases the return down.
- **Spin-offs.** Two renamed tickers (UTX and DWDP) included spin-offs that Yahoo's history may not credit; both are
  before the 5-year window and affect only the 10-year variant.
- **Disclosed bands, not amounts.** We size at band midpoints. V7 and V8 change the sizing.
- **Armstrong's filing** dominates the second half's trade-level tests (Section 5).
- **One price vintage.** Yahoo revises its history; the cached September 2026 files are what we used and submit.

## Appendix (not counted)

- A. Reproducing every number: `README.md` (one command, about 2.5 minutes, offline) and the two submission zips.
- B. Every rule, change and variant, with dates: `docs/DECISIONS.md`.
- C. Data quality and every exclusion: `outputs/data_quality.md`.
- D. Three copied trades traced step by step: `outputs/phase4_worked_examples.md`.
- E. Full tables: `outputs/tables/` (map in `README.md`, "Which file feeds each table and figure").
