# Copying the US Senate: what we have done so far (plain English)

_Written 2026-10-07 for the group, as the project passes from Harry to the next person. No finance or coding
background needed. The technical detail is in docs/HANDOVER.md and docs/DECISIONS.md._

## The question
US senators must publicly report their share trades, usually a few weeks after they make them. Some people believe
senators trade on inside knowledge. So we asked: **if you had simply copied every senator's trade the moment it became
public, would you have beaten the stock market?** The course marks the quality of the argument, not whether the answer
is "yes".

## What we built
1. **We collected every trade report ourselves** from the Senate's official disclosure website: about 1,900 reports
   filed between January 2016 and September 2026, and about 14,600 individual trades. We kept only trades in ordinary
   US shares and share funds, made by the senator personally or jointly, while they were actually a senator. Every
   trade we dropped is counted, with the reason, in outputs/data_quality.md.
2. **We wrote down exact copying rules before looking at any results.** We buy on the first trading day after a
   purchase is published, at a size equal to the middle of the dollar range the senator reported. We sell when the
   same senator reports a sale. Corrections a senator files later are handled the way a real copier would have seen
   them, never with hindsight.
3. **We priced everything** with daily share prices (Yahoo Finance, dividends included) and compared the result with
   simple alternatives over exactly the same dates. The alternatives: just buying the US market (SPY); the market
   scaled to the same riskiness; an equal mix of all the stocks senators bought; standard academic risk models; and
   two real funds that sell this exact idea (NANC and KRUZ).
4. **We guarded against fooling ourselves.** We designed everything using only the first half of the five years
   (September 2021 to February 2024) and locked the second half away. Before unlocking it, we wrote down exactly which
   five tests would count and what we predicted for each. We then froze the rules at a recorded point in the project's
   history, and only then looked at the second half. We also defined 20 alternative versions of the rules in advance (for
   example, leaving out the busiest senator, or including spouses' trades), ran 19 of them (the 20th needs data we
   do not have) and recorded every run.
5. **One command rebuilds every number.** A fresh copy on a clean computer, with no internet, reproduced every result
   exactly.

## What we found
- **Over the full five years (September 2021 to August 2026), copying the Senate made 10.8% a year. Simply holding
  the US market made 12.7%.** Allowing for how risky the copied portfolio was (it swung more than the market), there
  is no sign of skill: the "extra return" is about zero and could easily be chance.
- **In the second half on its own**, the copied portfolio made 23.0% a year against the market's 19.3%. But it was
  also riskier, and the market scaled up to the same riskiness made 26.0%, so again no real edge.
- **Our five pre-registered tests, judged on the second half:**
  - No extra return after allowing for risk, as we predicted.
  - Stocks senators bought had actually done slightly worse than the market in the weeks before the trade became
    public (the opposite of what inside knowledge would produce), and they then rose about 1.75% more than the market in
    the following month. **Both effects come almost entirely from one unusual report**: Senator Alan Armstrong's July
    2026 filing of 654 purchases made in a single week. Leave out such bulk reports and both effects disappear.
  - A first-half hint that senators' sales in industries their own committees oversee were followed by gains did not
    repeat: it looks like a fluke, as we predicted.
  - Small trades did not behave differently from large ones.
- **Bottom line so far: copying the Senate did not beat the market once risk is taken into account.** The few
  striking patterns trace back to a single report.

## Known weaknesses (we say these openly in the report)
- Yahoo no longer has prices for some companies that were taken over or went bust, so trades in those companies are
  left out. A standard research database (CRSP) would fill the gap, but our access request was not approved in time.
  Variant V15, which fills the gap with market returns, shows how much this could matter.
- Five years is short, so the tests can only rule out large effects.
- One filing dominates the second half's purchases.

## What is left before the deadline (Monday 19 October 2026, 23:59)
1. **Write the report**: the five-year result first, the second half as the check, the five tests (with the
   Armstrong caveat), and the weaknesses above. README.md lists which file holds each table and chart.
2. **Package the submission** as two zip files: the code and small data, and the price data.
3. If database (CRSP) access arrives in time, run the one extra pre-registered check (V20). It cannot change the main
   result.
