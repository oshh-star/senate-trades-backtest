// Builds Report V3: report/Copying_the_Senate_Report_V3.docx
// Text below; figures from report/figures (python report/build_figures.py); extra statistics from
// report/diagnostics.json (python report/diagnostics.py). Every number is read off a committed file named
// in the table notes, figure source lines or appendix. Run from the repo root:  node report/build_report.js
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType,
  ShadingType, BorderStyle, ImageRun, Footer, Header, PageNumber, PageBreak, LevelFormat, TableLayoutType,
  VerticalAlign,
} = require("docx");

const ROOT = path.resolve(__dirname, "..");
const FONT = "Calibri";
const BODY = 22;           // 11pt, as the brief requires
const SMALL = 17;          // 8.5pt for table cells, notes and captions
const W_PAGE = 9638;       // A4 minus 2 x 2 cm margins, DXA
// London Business School navy and red
const NAVY = "001E62", RED = "C8102E", PALE = "D6E2F0", MID = "6A86B5", INK = "1A1F2B", GREY = "5B6573";
const TINT = "EEF2F8", ROWTINT = "F4F7FB";

// ---------- inline markup: **bold**, *italic* ----------
function runs(text, size = BODY, extra = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  const mk = (t, more = {}) => new TextRun({ text: t, font: FONT, size, color: INK, ...extra, ...more });
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(mk(text.slice(last, m.index)));
    const t = m[0];
    out.push(t.startsWith("**") ? mk(t.slice(2, -2), { bold: true }) : mk(t.slice(1, -1), { italics: true }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(mk(text.slice(last)));
  return out;
}
const P = (text, o = {}) => new Paragraph({
  children: runs(text, o.size || BODY, o.extra || {}), alignment: o.align || AlignmentType.JUSTIFIED,
  spacing: { after: o.after ?? 110, before: o.before ?? 0, line: 252 }, keepNext: o.keepNext,
});
// First-order lead: the section's core point in navy, then the argument
const LEAD = (text) => new Paragraph({
  children: runs(text, BODY, { color: NAVY, bold: true }), alignment: AlignmentType.LEFT,
  spacing: { after: 90, line: 252 }, keepNext: true,
});
const H1 = (num, text, brk = false) => new Paragraph({
  heading: HeadingLevel.HEADING_1, pageBreakBefore: brk, spacing: { before: 260, after: 90 }, keepNext: true,
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: PALE, space: 3 } },
  children: [new TextRun({ text: num ? `${num}  ` : "", font: FONT, size: 28, bold: true, color: RED }),
             new TextRun({ text, font: FONT, size: 28, bold: true, color: NAVY })],
});
const H2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2, spacing: { before: 150, after: 60 }, keepNext: true,
  children: [new TextRun({ text, font: FONT, size: 23, bold: true, color: NAVY })],
});
const BULLET = (text) => new Paragraph({
  numbering: { reference: "bullets", level: 0 }, children: runs(text), alignment: AlignmentType.JUSTIFIED,
  spacing: { after: 60, line: 252 },
});
const NOTE = (text) => new Paragraph({
  children: runs(text, SMALL, { color: GREY }), alignment: AlignmentType.LEFT, spacing: { before: 50, after: 160, line: 240 },
});
const TTITLE = (num, text) => new Paragraph({
  keepNext: true, spacing: { before: 120, after: 60 },
  children: [new TextRun({ text: `Table ${num}  `, font: FONT, size: 19, bold: true, color: RED }),
             new TextRun({ text, font: FONT, size: 19, bold: true, color: NAVY })],
});

function figure(file, widthCm, num, note) {
  const buf = fs.readFileSync(path.join(ROOT, file));
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
  const px = Math.round(widthCm / 2.54 * 96);
  return [
    new Paragraph({ keepNext: true, spacing: { before: 140, after: 30 },
      children: [new TextRun({ text: `Figure ${num}`, font: FONT, size: 19, bold: true, color: RED })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { after: 0 },
      children: [new ImageRun({ type: "png", data: buf, transformation: { width: px, height: Math.round(px * h / w) } })] }),
    NOTE(note),
  ];
}

const thin = { style: BorderStyle.SINGLE, size: 4, color: "CDD6E3" };
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
function table(header, rows, widths, o = {}) {
  const scale = W_PAGE / widths.reduce((a, b) => a + b, 0);
  const W = widths.map((x) => Math.round(x * scale));
  W[W.length - 1] += W_PAGE - W.reduce((a, b) => a + b, 0);
  const nRows = rows.length + 1;
  let ri = 0;
  const cell = (text, i, head, fill, bold) => new TableCell({
    width: { size: W[i], type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
    shading: fill ? { type: ShadingType.CLEAR, color: "auto", fill } : undefined,
    margins: { top: 35, bottom: 35, left: 80, right: 80 },
    borders: { top: none, left: none, right: none, bottom: head ? { style: BorderStyle.SINGLE, size: 10, color: NAVY } : thin },
    children: [new Paragraph({
      alignment: (i < (o.leftCols || 1) || o.left) ? AlignmentType.LEFT : AlignmentType.RIGHT, spacing: { after: 0, line: 240 },
      keepNext: o.split ? false : ri < nRows - 1,
      children: runs(text, o.size || SMALL, head ? { bold: true, color: NAVY } : (bold ? { bold: true } : {})),
    })],
  });
  const trs = [new TableRow({ tableHeader: true, cantSplit: true, children: header.map((t, i) => cell(t, i, true, TINT)) })];
  rows.forEach((r) => {
    ri += 1;
    if (r.length === 1) {
      trs.push(new TableRow({ cantSplit: true, children: [new TableCell({
        columnSpan: W.length, width: { size: W_PAGE, type: WidthType.DXA },
        margins: { top: 40, bottom: 20, left: 80, right: 80 }, borders: { top: none, left: none, right: none, bottom: thin },
        children: [new Paragraph({ spacing: { after: 0 }, keepNext: true, children: runs(r[0], o.size || SMALL, { bold: true, color: RED }) })],
      })] }));
    } else {
      const hl = o.highlight && o.highlight(r);
      trs.push(new TableRow({ cantSplit: true, children: r.map((t, i) => cell(t, i, false, hl ? ROWTINT : undefined, hl && i === 0)) }));
    }
  });
  return new Table({ width: { size: W_PAGE, type: WidthType.DXA }, columnWidths: W, layout: TableLayoutType.FIXED, rows: trs });
}

// Key-figure tiles (market-insights style)
function tiles(items) {
  const w = Math.floor(W_PAGE / items.length);
  const c = (big, small) => new TableCell({
    width: { size: w, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: TINT },
    margins: { top: 110, bottom: 110, left: 140, right: 140 },
    borders: { top: { style: BorderStyle.SINGLE, size: 18, color: NAVY }, bottom: none, left: { style: BorderStyle.SINGLE, size: 12, color: "FFFFFF" }, right: { style: BorderStyle.SINGLE, size: 12, color: "FFFFFF" } },
    children: [new Paragraph({ spacing: { after: 30 }, children: [new TextRun({ text: big, font: FONT, size: 34, bold: true, color: NAVY })] }),
               new Paragraph({ spacing: { after: 0, line: 230 }, children: runs(small, SMALL, { color: GREY }) })],
  });
  return new Table({ width: { size: w * items.length, type: WidthType.DXA }, columnWidths: items.map(() => w),
    layout: TableLayoutType.FIXED, rows: [new TableRow({ children: items.map(([b, s]) => c(b, s)) })] });
}


// =====================================================================================
const D = JSON.parse(fs.readFileSync(path.join(ROOT, "report", "diagnostics.json")));
const C = D.concentration, V21 = D.v21_departure_exit;
const pct = (x, d = 1) => `${(x * 100).toFixed(d)}%`;
const sgn = (x, d = 1) => `${x < 0 ? "−" : "+"}${Math.abs(x * 100).toFixed(d)}`;
const body = [];
const add = (...xs) => xs.flat().forEach((x) => body.push(x));
const SPACER = (after = 100) => new Paragraph({ spacing: { after }, children: [] });

// ---------- Title block ----------
add(
  new Table({ width: { size: W_PAGE, type: WidthType.DXA }, columnWidths: [W_PAGE], layout: TableLayoutType.FIXED,
    rows: [new TableRow({ children: [new TableCell({
      width: { size: W_PAGE, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: NAVY },
      margins: { top: 260, bottom: 240, left: 320, right: 320 }, borders: { top: none, bottom: { style: BorderStyle.SINGLE, size: 30, color: RED }, left: none, right: none },
      children: [
        new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "LONDON BUSINESS SCHOOL  |  CA01 INVESTMENT FUNDAMENTALS  |  AUTUMN 2026", font: FONT, size: 16, bold: true, color: PALE, characterSpacing: 10 })] }),
        new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Copying the US Senate", font: FONT, size: 46, bold: true, color: "FFFFFF" })] }),
        new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "A five-year backtest of trading on senators' disclosed stock trades, and the case against investing in it", font: FONT, size: 23, color: "FFFFFF" })] }),
        new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: "Study group [number]  ·  [Member names]  ·  October 2026  ·  Code and data: github.com/oshh-star/senate-trades-backtest", font: FONT, size: 16, color: PALE })] }),
      ],
    })] })] }),
  SPACER(120),
);

// ---------- 1 Executive Summary ----------
add(H1("1", "Executive Summary"));
add(LEAD("Recommendation: do not invest. Copying senators' disclosed trades earned roughly the market's return with 1.5 times its volatility, and we find no evidence of skill."));
add(tiles([
  ["13.4%", "a year for the copy portfolio, Sep 2021 to Aug 2026 (SPY, the S&P 500 ETF: 12.7%)"],
  ["−2.9 pts", "a year against SPY held at the same volatility (16.3% a year)"],
  ["+1.1%", "a year of alpha after market risk, indistinguishable from zero (t = 0.18)"],
  [`${Math.round(C.pnl_share_mullin_plus_moody * 100)}%`, "of the profit made by two of the 31 senators in the sample"],
]));
add(SPACER(80));
add(P("The strategy buys every stock that a serving US senator discloses buying for their own or a joint account, at the first close after the filing becomes public, and sells when the same senator discloses the sale. We measure the resulting copy portfolio by its return on the capital it actually employs (Series A, Section 2.1). From September 2021 to August 2026 it returned **13.4% a year at 23.4% volatility**, against **12.7% at 15.9%** for SPY. An investor could have reached the same volatility by holding 1.48 times SPY's excess return over Treasury bills, which earned **16.3% a year**. The copy portfolio has a market beta of 1.21 and a tilt towards small companies, and once these exposures are priced its alpha is +1.1% a year in the CAPM (t = 0.18) and +2.3% in the Carhart four-factor model (t = 0.37), neither distinguishable from zero."));
add(P("Three further results support the recommendation. The second half of the sample, which played no part in setting the rules, gives the same verdict (22.9% a year against 26.0% for SPY at equal risk). Senators' purchases did not outperform the market between the trade and the filing, which is where informed trading would appear first. And the profit is concentrated: two senators account for three-quarters of it, a quarter comes from four semiconductor positions bought in 2025, and none of the 23 alternative specifications we ran produces a statistically reliable alpha."));

// ---------- 2 Strategy Design ----------
add(H1("2", "Strategy Design"));
add(LEAD("The strategy is a mechanical copy of public filings. Each rule can be applied without judgement, and each has a stated reason."));
add(P("Under the STOCK Act of 2012, a senator must report any securities transaction above $1,000 no later than 45 days after it takes place, in a Periodic Transaction Report (PTR) filed on the Senate's electronic disclosure site, eFD. The report gives the security, the transaction date, the direction and the value as a range ($1,001 to $15,000, $15,001 to $50,000, and so on). It is public from the moment eFD receives it, and eFD records that time to the minute. Table 1 sets out each rule and the reason for it; Figure 1 shows how one filing becomes a position."));
add(TTITLE(1, "Trading rules and the reason for each"));
add(table(["Rule", "Specification", "Reason"], [
  ["Signal", "Every electronic PTR, dated by the time eFD received it. The 308 scanned paper filings are excluded and listed.", "Receipt is when the information becomes public, the earliest moment a copier can act. Paper filings cannot be read by any automated copier."],
  ["Who counts", "A trade is copied if the filer was a serving senator on the transaction date, using official service dates.", "eFD labels filers by their current status; relying on it would drop senators who have since left office (survivorship bias)."],
  ["Accounts", "The senator's own and joint accounts.", "These are the trades the senator decides directly. Spouse and dependent-child trades are tested as variant V6."],
  ["Instruments", "US-listed common stocks, ADRs and equity ETFs. No options, bonds, preferred shares, mutual funds, crypto, or bond and commodity ETFs.", "The strategy is an equity strategy. Options and bonds cannot be sized or priced reliably from a dollar range."],
  ["Entry", "Adjusted close on the first NYSE trading day after the day of receipt.", "53% of filings arrive after 15:30 New York time, when that day's close can no longer be traded; the next close removes any look-ahead. Same-day entry for earlier filings is variant V9."],
  ["Size", "Midpoint of the disclosed range ($8,000.50 for the smallest band); the open top band uses its lower bound.", "Only the band is known, and its midpoint is the natural estimate. The lower bound (V7) and equal dollars per trade (V8) are tested."],
  ["Exit", "Sold when the same senator discloses a sale of the same stock, first in, first out. A full sale closes the position; a partial sale sells the band midpoint, capped at the holding.", "The copier mirrors the senator's own holding period, the only exit signal the filings provide."],
  ["No shorting", "A disclosed sale of a stock the copier does not hold is ignored.", "A sale is usually an exit for tax, liquidity or diversification reasons rather than a negative view. After disclosure, sold stocks moved in line with SPY (+0.15% over 21 trading days, t = 0.27), so a short position would have earned nothing and paid borrowing costs."],
  ["Senator leaves office", "Positions stay open until the senator discloses a sale or the window ends.", "Former senators stop filing PTRs, so no sale signal arrives. The frozen rules have no separate exit for this case; selling at departure is tested as V21 (Section 6.4)."],
  ["Amendments", "Each record takes effect as first published. A later correction reverses the original action at its own date and then acts on the corrected record.", "A copier only knows what has been published. Applying corrections at the original date (V14) would use information not yet available."],
  ["Window", "Disclosures from 1 September 2021 to 31 August 2026 (60 months). The portfolio is built from the 12 months of filings before the window, which are not scored.", "Five years balances relevance against sample size; the window ends with the latest Fama-French data. Without the 12-month build-up the portfolio would start empty; the empty start is variant V17."],
  ["Design and test halves", "Rules were set on September 2021 to February 2024. March 2024 to August 2026 stayed locked in the code until the rules were frozen on 6 October 2026.", "Data that influenced a choice cannot test it. The second half is a genuine out-of-sample check (Appendix I)."],
], [13, 40, 47], { left: true, split: true }));
add(NOTE("Every rule is a parameter in config/config.yaml; its date and reason are recorded in docs/DECISIONS.md. Filing times from data/processed/trade_records.csv; sale returns from outputs/tables/phase5_event_study_full.md."));
add(figure("report/figures/fig1_flow.png", 14.5, 1, "The median disclosure lag across in-scope trades is 33 calendar days. From outputs/data_quality.md."));

add(H2("2.1 How the Return Is Measured: Series A and Series B"));
add(LEAD("Series A and Series B are two measures of the same trades, not two portfolios. Series A is the headline."));
add(P("Copying senators does not use a fixed amount of money. On 1 September 2021 the copied positions are worth **$1.5m**: the market value of the 70 positions opened from filings in the preceding 12 months. Capital in positions then rises to $24.9m by August 2026 as senators buy more than they sell (Appendix C). Turning daily profit into a return therefore requires a choice of denominator, and we report two."));
add(P("**Series A, return on capital deployed (headline).** Each day, Series A is the dollar-weighted return of the positions held from the previous close. With a $10,000 position up 2% and a $30,000 position down 1%, the day's return is (200 − 300) / 40,000 = −0.25%. This is the time-weighted return of a fund that is always fully invested in whatever senators currently hold, receiving new money when purchases are disclosed and returning it when sales are. It measures the signal per dollar invested and is directly comparable with fully invested benchmarks such as SPY, which is why the verdict rests on it. A day with no position would earn the risk-free rate, the return on cash; because the portfolio starts with 70 positions, this never happens in the window."));
add(P("**Series B, a fixed account.** Series B starts with **$17.1m**: the $1.5m of initial positions plus $15.6m, the largest cumulative net cash the strategy ever required. Purchases are paid from cash, sales return cash, and cash earns the risk-free rate. Its return is the change in the account's total value, as a brokerage statement would show it. Series B is more realistic about funding but less informative about the signal, for two reasons: its size could only be known with hindsight, and because 91% of it was in cash at the start, it avoided most of the 2022 fall by construction rather than by any decision in the rules. We therefore report it beside Series A as a check."));

add(H2("2.2 Benchmarks"));
add(P("Every benchmark covers identical dates, and each answers a different question. **SPY**, the S&P 500 ETF, asks whether a passive investor would have done as well. **SPY at Series A's volatility**, the risk-free rate plus 1.48 times SPY's excess return, asks whether any extra return is simply extra market risk; it is the comparison the verdict rests on. The **Senate universe**, every stock any senator bought in the previous 12 months, equally weighted and rebalanced monthly from filings already public, asks whether the timing of the trades adds anything beyond the list of stocks. **Factor models** regress Series A's monthly excess return on the market factor (CAPM) and on the market, size (SMB), value (HML) and momentum (MOM) factors (Fama and French, 1993; Carhart, 1997); the alpha is the return left after paying for those exposures. The factor returns and the risk-free rate (one-month Treasury bills) come from the US files of Kenneth French's data library, the source used in the course. Finally, **NANC and KRUZ**, two ETFs launched in February 2023 to track Democratic and Republican congressional trades, show what a professional implementation of the idea achieved."));

// ---------- 3 Rationale ----------
add(H1("3", "Economic Rationale and Testable Predictions"));
add(LEAD("The strategy can only work if senators trade on information that is still unpriced when their filing appears. That condition can be tested."));
add(P("Senators sit on committees that draft regulation, award contracts and question executives. Ziobrowski et al. (2004) estimated that senators' purchases beat the market by about 12% a year in 1993 to 1998. Studies of the period after the STOCK Act find little or no outperformance (Eggers and Hainmueller, 2013; Belmont et al., 2022)."));
add(P("**Who is on the other side.** A copier buys about a month after the senator, from whoever sells that day. For that counterparty to lose systematically, two conditions must hold: the senator's information must still be unpriced when the filing appears, and the market must ignore a public filing that is tracked by retail apps, newsletters and two listed ETFs. The first is plausible; the second is hard to sustain. Where many copiers buy the same stock on the same day, they also pay a price that already reflects their own demand."));
add(P("On 30 September 2026, before opening the second half, we registered what each explanation implies in our data. If senators are informed and the copier acts in time, the stocks keep outperforming after disclosure (H2), sales of stocks in industries overseen by the senator's committees underperform other sales (H3), larger purchases outperform smaller ones (H4), and the copy portfolio earns an alpha (H0). If senators are informed but the market prices the news before the filing, purchases outperform between the trade and the disclosure (H1), and only the senator profits. If the return reflects nothing but market and size exposure, the alpha is zero and the factor loadings are large. Section 6.2 sets each prediction against the result."));

// ---------- 4 Data ----------
add(H1("4", "Data and Sample Construction"));
add(LEAD("The dataset is built from the primary source, and every exclusion is counted."));
add(P("We downloaded all 1,876 PTRs received on eFD from January 2016 to September 2026 (1,568 electronic, 308 scanned) and cached every page, so the results do not depend on a website that can change. After removing duplicated amendments and applying the rules in Table 1, the window contains **2,340 trades by 31 senators** (Appendix A counts every exclusion). Fifteen of the 31 disclosed only sales of stock the copier did not hold, so they generate no positions. Eighty-five paper PTRs inside the window, 64 of them Richard Blumenthal's, are invisible to any electronic copier."));
add(P("**The sample is concentrated.** Tommy Tuberville, Markwayne Mullin and Alan Armstrong account for 87% of the dollars copied (Appendix B). Armstrong was appointed on 24 March 2026 to the seat Mullin vacated, and a single report he filed on 21 July 2026 lists 654 purchases of 621 stocks made in late March. That filing is 67% of the second half's purchases, so every trade-level test is also reported without it."));
add(P("**Conventions.** Returns are total returns in US dollars, from adjusted closes with dividends reinvested; for a sterling investor the ranking is unchanged (Series A 13.8% a year, SPY 13.1%). One risk-free series is used throughout. The portfolio is valued daily, while Sharpe ratios and regressions use monthly returns, because positions are held for months; volatility is annualised by √12 and t-statistics are corrected for autocorrelation (Newey and West, 1987, three lags). Prices are a September 2026 download, and filings enter as first published."));
add(P("**Delisted stocks.** Yahoo Finance holds no history for delisted companies, so purchases of stocks that later disappeared could not be priced; at their peak, in October 2022, they would have been 67% of capital deployed. A group member retrieved daily total-return data from a Bloomberg terminal for the eight largest gaps, which cover 95% of the missing dollars; the 178 symbols still unpriced never exceed 2.2% of capital. Seven of the eight were acquired, and the large positions in U.S. Steel, ChannelAdvisor and Activision Blizzard rose on the bids, so including them raised Series A from 10.8% to 13.4% a year. The missing stocks therefore biased the return downwards, not upwards. This correction was made after the second half was opened, so it is logged with every before-and-after value (Appendix D), and the Yahoo-only result is kept as variant V18. No conclusion changes."));

// ---------- 5 Results ----------
add(H1("5", "Empirical Results"));
add(H2("5.1 Performance Against Benchmarks"));
add(LEAD("The copy portfolio beat SPY by 0.7 points a year with 1.5 times its volatility. At equal risk SPY was 2.9 points a year better, and no alpha remains once market and size exposure are priced (Figure 2, Table 2)."));
add(P("**The excess return is market and size exposure.** Series A's beta of 1.21 and size loading of 0.33 can both be bought for a few basis points through an index fund and a small-cap fund, and both alphas are less than one standard error from zero. The equal-weighted Senate universe earned as much (13.6%) with less volatility, so the timing of senators' trades added nothing beyond the list of stocks they hold. These tests have limited power: with 60 months and Series A's residual volatility of 13.1% a year, only an alpha of about 12% a year would have reached t = 2. The result rules out a large edge, not every edge (Section 6.5)."));
add(P("**Series B.** The fixed account shows a higher Sharpe ratio than SPY (0.69 against 0.61; Table 2) because most of it was in cash while the market fell in 2022: its volatility is 8.0% and its largest fall, 7.1%, came only in 2026. Its beta is 0.37 and its alpha, +2.3% a year, is not significant (t = 1.08). Its small lead over SPY at the same risk (+0.6 points a year) reflects that timing and a pot size known only with hindsight, and it turns negative in the second half (−1.8 points). The rules did not choose to hold cash in 2022; the portfolio was simply still small."));

add(figure("report/figures/fig2_cumulative.png", 14, 2, "End values per $1 in bold. Risk-matched SPY is rf + 1.48 × (SPY − rf). The chart compounds daily returns and ends at 2.10; the monthly series behind Table 2 ends at 2.13. The dashed line marks the end of the design half."));
add(TTITLE(2, "The copy portfolio against the alternatives, September 2021 to August 2026 (60 months)"));
add(table(["", "Series A (headline)", "Series B (fixed account)", "SPY", "SPY at A's risk (k = 1.48)", "Senate universe"], [
  ["Return and risk"],
  ["Return, % a year (geometric)", "13.41", "9.16", "12.69", "16.30", "13.56"],
  ["Volatility, % a year", "23.41", "8.03", "15.87", "23.47", "17.14"],
  ["Sharpe ratio", "0.50", "0.69", "0.61", "0.61", "0.62"],
  ["Factor models (monthly regressions, Newey-West t)"],
  ["CAPM alpha, % a year (t)", "+1.07 (0.18)", "+2.28 (1.08)", "+1.02 (1.62)", "+1.52 (1.62)", "+1.72 (0.74)"],
  ["CAPM beta", "1.21", "0.37", "0.98", "1.45", "1.01"],
  ["Carhart alpha, % a year (t)", "+2.26 (0.37)", "+2.62 (1.25)", "+0.09 (0.21)", "+0.14 (0.21)", "+1.68 (0.77)"],
  ["Size (SMB) loading (t)", "0.33 (1.87)", "0.18 (2.33)", "−0.13 (−8.29)", "−0.19 (−8.29)", "0.13 (1.87)"],
  ["Smallest Carhart alpha detectable at t = 2", "12.39", "4.85", "1.01", "1.49", ""],
  ["Losses and diversification"],
  ["Maximum drawdown, %", "−32.16", "−7.13", "−24.50", "−35.31", "−24.58"],
  ["Peak, trough, recovery", "Mar 22, Jul 22, Mar 24", "Jun 26, Jul 26, Aug 26", "Jan 22, Oct 22, Dec 23", "Jan 22, Oct 22, Jan 24", "Nov 21, Oct 22, Dec 23"],
  ["Correlation with SPY: all months / SPY's worst 12", "0.81 / 0.68", "0.73 / 0.36", "1 / 1", "1 / 1", "0.94 / 0.87"],
  ["Trading"],
  ["One-way turnover, % of capital a year", "102", "39", "", "", ""],
  ["Return over SPY at the same risk, % a year", "−2.58", "+0.64", "", "", ""],
  ["Break-even one-way trading cost", "none", "82 bp", "", "", ""],
], [30, 14, 14, 12, 15, 15], { highlight: (r) => r[0].startsWith("Return, %") || r[0].startsWith("Sharpe") || r[0].startsWith("Return over") }));
add(NOTE("From outputs/tables/phase5_full_results.md. Alphas are monthly estimates × 12; Newey-West t with three lags. Return over SPY at the same risk is the mean monthly difference × 12 (arithmetic, because trading costs subtract arithmetically); the geometric gap used elsewhere is 2.9 points. Break-even cost is that excess return divided by twice the annual turnover; \"none\" means the excess return is already negative before costs."));
add(H2("5.2 Risk, Drawdowns and Diversification"));
add(P("Series A's largest fall, 32.2% from March to July 2022, was deeper than SPY's 24.5%, and it regained its peak in March 2024, three months after SPY (Figure K1). A small allocation to an asset improves an existing portfolio only if the asset's Sharpe ratio exceeds its correlation with that portfolio times the portfolio's Sharpe ratio. For Series A against SPY the two sides are 0.503 and 0.81 × 0.61 = 0.499, a margin far inside sampling error: a 10% allocation to Series A raises the Sharpe ratio of an SPY holding in only 49% of 10,000 bootstrap resamples of the 60 months, and the difference between the two Sharpe ratios is not significant (p = 0.69; Appendix H). Its correlation with SPY falls only to 0.68 in SPY's twelve worst months, so it does not act as a hedge."));

add(H2("5.3 Listed Congressional-Trading ETFs"));
add(P("Over the 42 months both ETFs have traded, NANC returned 24.75% a year (Sharpe ratio 1.28) and KRUZ 19.31% (1.05), against 22.32% (1.33) for SPY and 19.34% (0.79) for Series A. Neither ETF has an alpha distinguishable from zero (CAPM +0.84%, t = 0.44; −1.33%, t = −0.39). The professional versions of the idea also track the market, which is what one would expect if the filings carry no usable information."));

add(H2("5.4 Implementation Costs"));
add(P("Series A turns over about 102% of its capital a year, one way. We do not report a net-of-cost return, because any precise cost assumption would be invented; nor is one needed, since the portfolio already trails SPY at the same risk before costs and so has no positive break-even cost. Most trades are small (92% of copied purchases are in the two lowest bands, up to $50,000); the exception is Armstrong's 654-stock basket, which a copier would have had to buy in a single day. Series B's break-even of 82 basis points disappears in the second half. Costs can only strengthen the conclusion."));

// ---------- 6 Robustness ----------
add(H1("6", "Robustness and Out-of-Sample Evidence"));
add(H2("6.1 Design Half Versus Test Half"));
add(LEAD("The half of the data that played no part in designing the rules reaches the same verdict."));
add(TTITLE(3, "The two halves of one continuous backtest (30 months each)"));
add(table(["", "Series A return", "Series A Sharpe", "SPY return", "SPY Sharpe", "Series A CAPM alpha (t)"], [
  ["Design half, Sep 2021 to Feb 2024", "4.61%", "0.20", "6.43%", "0.27", "+1.14% (0.12)"],
  ["Test half, Mar 2024 to Aug 2026", "22.94%", "1.03", "19.32%", "1.17", "+1.69% (0.29)"],
], [34, 13, 13, 13, 12, 15]));
add(NOTE("Annualised geometric returns; Newey-West t. Test half from outputs/tables/phase5_oos_results.md (SPY at Series A's volatility over the test half: 26.02%). Design half from data/processed/monthly_returns.csv under the headline prices (report/diagnostics.json); the design-half record frozen before the unlock, outputs/tables/phase5_insample_results.md, uses Yahoo prices only."));
add(P("The test half beat SPY by 3.6 points a year in raw terms, but SPY at the same volatility earned more (26.0%), the Sharpe ratio is below the index's in both halves, and the Carhart model attributes the test-half return to market exposure and a momentum loading of 0.38 (t = 3.47). The result is not stable from year to year (Figure K2): Series A trailed SPY in 2021, 2023 and 2024 (by 19.9 points in 2024), lost less in 2022, and led in 2025 and 2026, the two years that carry the test half."));

add(H2("6.2 Pre-Registered Hypothesis Tests"));
add(LEAD("Five of the seven registered statistics came out as predicted. The two significant results both rest on one bulk filing and disappear without it."));
add(TTITLE(4, "Registered predictions against test-half results (March 2024 to August 2026)"));
add(table(["Test", "If senators were informed", "Registered prediction", "Result (t)", "Without bulk filings", "Holm p", "Held?"], [
  ["H0 CAPM alpha", "positive", "zero", "+1.69% a year (0.29)", "", "1", "**Yes**"],
  ["H0 Carhart alpha", "positive", "zero", "+0.40% a year (0.06)", "", "1", "**Yes**"],
  ["H1 purchases, trade to disclosure", "positive", "near zero", "−3.22% (−2.98)", "−0.11% (−0.18)", "0.017", "**No**, wrong sign"],
  ["H1 sales, trade to disclosure", "negative", "near zero", "−0.99% (−0.96)", "+0.68% (1.22)", "1", "**Yes**"],
  ["H2 copier purchases, 21 days", "positive", "test the sign", "+1.74% (3.54)", "+1.12% (0.81)", "0.001", "**Partly**"],
  ["H3 committee sales, overseen minus other", "negative", "no difference", "+6.16% (0.94)", "", "1", "**Yes**"],
  ["H4 small minus large purchases, 126 days", "negative", "negative only if informed", "+4.82% (0.96)", "+1.72% (0.41)", "1", "**Yes**"],
], [24, 12, 13, 15, 14, 8, 14], { left: true, split: true }));
add(NOTE("From outputs/tables/confirmatory_oos.md. Event returns are the stock's return minus SPY's over the same days, with t clustered by month of entry (H1 to H4) or Newey-West (H0); H2 is one-sided. Holm p adjusts for testing seven statistics at once (Holm, 1979). Bulk filings are reports with 50 or more in-scope trades, a check registered before the data were opened. Figure K4 plots each estimate with its interval."));
add(P("If senators traded on information a copier could still use, several of these would line up: purchases would run up before disclosure, sales would run down, overseen industries and larger trades would be more informative, and the portfolio would earn an alpha. None does. The only significant departure, H1 for purchases, has the **opposite** sign: the stocks senators bought lagged the market before disclosure. H2 is positive, but its registered reversal check is mixed (+1.73% after 126 days, +12.03% after 252), and both significant results trace to Armstrong's July 2026 report, whose 621 stocks fell against SPY between the March trades and the July disclosure and then recovered. With two-thirds of the events in one month, a standard error clustered by month overstates precision. Without bulk filings, H1 is −0.11% and H2 +1.12%, neither distinguishable from zero. The pattern fits the exposure-only explanation better than any other."));

add(H2("6.3 What the Disclosure Delay Costs a Copier"));
add(LEAD("If senators were informed, their own return from the trade date would lie above the copier's from the start. For the first three months it lies below."));
add(figure("report/figures/fig5_event_study.png", 15, 3, "Full window, every in-scope trade, equal-weighted; 95% bands with standard errors clustered by month of entry. From outputs/tables/phase5_event_study_full.md and phase5_predisclosure_drift_full.md."));
add(P("Measured from the trade date, senators' purchases trailed SPY by 2.44% after one month, while the copier's purchases, measured from disclosure, beat it by 1.56%. The difference, −4.01% (t = −2.25), means the delay helped the copier: the stocks fell 2.06% against SPY (t = −1.60) over the median 29 trading days before the filing appeared. By six and twelve months the two lines meet. The copier's early gains are equal-weighted, dominated by the same Armstrong basket and statistically fragile (no horizon from three months on reaches t = 2), and they do not appear in the dollar-weighted portfolio. The sales panel shows no sign that senators sell ahead of falls."));

add(H2("6.4 Who Drives the Result"));
add(LEAD("Most of the profit comes from a few positions held by two senators, so the return depends on who happens to serve."));
const sl = C.sleeves, yrs = ["2023", "2024", "2025", "2026"];
const capShare = (y) => sl.mullin.avg_capital_by_year[y] / (sl.mullin.avg_capital_by_year[y] + sl.rest.avg_capital_by_year[y]);
add(P(`Mullin and Ashley Moody produced ${Math.round(C.pnl_share_mullin_plus_moody * 100)}% of the profit on copied positions (Appendix B). Four of Moody's 16 positions, in Micron, AMD and Applied Materials, bought within four months of her appointment in January 2025, produced $${(C.moody_top4.reduce((a, b) => a + b.pnl, 0) / 1e6).toFixed(1)}m, ${Math.round(C.moody_top4_share_of_all_pnl * 100)}% of all the profit the strategy made. Excluding every trade made in a senator's first 180 days in office (V3) lowers the return from 13.4% to 9.4% a year.`));
add(TTITLE(5, "Mullin's positions against the rest of the portfolio, Series A return by calendar year"));
add(table(["", ...yrs.map((y) => y === "2026" ? "2026 (Jan to Aug)" : y)], [
  ["Mullin's positions, return", ...yrs.map((y) => pct(sl.mullin.return_by_year[y]))],
  ["All other positions, return", ...yrs.map((y) => pct(sl.rest.return_by_year[y]))],
  ["Mullin's share of capital deployed", ...yrs.map((y) => pct(capShare(y), 0))],
], [34, 16, 16, 16, 18]));
add(NOTE("Series A rebuilt from data/processed/lots.csv for each group of positions (report/diagnostics.py; the full rebuild matches the engine's daily return to 1e-8). Mullin's first copied purchase was disclosed in 2023."));
add(P(`Table 5 explains an apparent contradiction. Mullin's positions made 39% of the dollar profit, yet removing them raises the return to 18.6% (V2.3). Series A is a time-weighted return: Mullin's positions earned 13% to 21% a year, but they were about half the capital in 2024 to 2026, when the rest of the portfolio, led by Moody's semiconductor holdings, gained ${pct(sl.rest.return_by_year["2025"], 0)} in 2025 and ${pct(sl.rest.return_by_year["2026"], 0)} in the first eight months of 2026. Large, steady positions earned many dollars and diluted the return per dollar. The exit rule adds to this. Mullin left the Senate on 23 March 2026, filed nothing afterwards, and his 150 positions ($6.0m at cost) stayed in the portfolio until the end of the window. Selling them at the first close after his departure (V21, an exploratory check added after the second half was opened) raises Series A to ${pct(V21.return)} a year, with an alpha of +3.3% (t = 0.46), still ${Math.abs(V21.gap_geometric * 100).toFixed(1)} points a year below SPY at the same volatility (${pct(V21.risk_matched_spy)}).`));

add(H2("6.5 Alternative Specifications, Power and Multiple Testing"));
add(LEAD("Changing one rule at a time moves the return a great deal, but no version produces a reliable alpha."));
add(P("We registered 16 variants (V1 to V16) before computing any return, and four more (V17 to V20) after seeing the design-half results; V21 was added after the second half was opened. V2 is five runs, one per senator; V20 could not run without access to CRSP, and V1 duplicates V2.1. That leaves 23 distinct specifications with results, grouped in Table 6 and listed in Appendix E."));
add(TTITLE(6, "What we varied, and its effect on Series A (full window)"));
add(table(["Family", "What changes", "Runs", "Return, % a year", "CAPM alpha, % a year", "Largest |t|"], [
  ["Whose trades", "Drop each of the top five senators; drop senators' first 180 days; drop bulk filings; add spouse and child trades", "8", "9.4 to 18.6", "−2.3 to +5.8", "0.74"],
  ["What we buy", "No ETFs; no OTC names; all ETFs including bond and T-bill funds; add preferred shares", "4", "12.0 to 13.4", "−0.1 to +1.1", "0.18"],
  ["How we size", "Band lower bound; equal dollars per trade; equal weight per position", "3", "12.4 to 13.4", "+0.8 to +1.1", "0.35"],
  ["When we trade", "Same-day close for filings received before 15:30; sell when the senator leaves office (V21)", "2", "13.9 to 16.0", "+1.5 to +3.3", "0.46"],
  ["Data and window", "3-year and 10-year windows; amendments as revised; unpriced stocks earn SPY; no warm-up; Yahoo prices only", "6", "10.8 to 25.5", "−1.5 to +3.0", "0.49"],
  ["Headline", "", "", "13.41", "+1.07", "0.18"],
], [14, 42, 6, 13, 14, 11], { highlight: (r) => r[0] === "Headline", leftCols: 2 }));
add(NOTE("t is the OLS t of the CAPM alpha. From outputs/tables/variants_full_bloomberg.md; every run is logged in docs/DECISIONS.md. Figure E1 shows each alpha with its 95% interval."));
add(P("No variant's CAPM alpha reaches |t| = 2, in the full window or in its own test half; the closest is the 10-year window's Carhart alpha over its test half, which is negative (−5.75% a year, OLS t = −2.00). A result that moves by four points when one group of trades is dropped is not an edge an investor can rely on."));
add(P("Two further disciplines protect the conclusion. Only the seven registered statistics are treated as tests: of the 516 exploratory cells with a clustered t-statistic, 81 reach |t| = 2, but they overlap heavily and many fall in groups dominated by Armstrong's filing. And the sample is short: at Series A's residual volatility, an alpha of 3% a year would need about 77 years of monthly data to reach t = 2, and 5% would need 28 (t ≈ information ratio × √years). The trailing 24-month alpha ranges from +10% to −16% a year and is significant only in early 2025, when it is negative (Figure K3). Five years cannot show that senators have no edge, but they rule out one large enough to justify investing."));

// ---------- 7 Counter-arguments ----------
add(H1("7", "The Case Against Our Recommendation"));
add(LEAD("The strongest case for the strategy is that it beat SPY. We take it seriously and still recommend against investing."));
add(P("**The case for.** Series A beat SPY over five years (13.4% against 12.7%) and in the test half (22.9% against 19.3%), lost less in 2022, and has positive point estimates of alpha, which rise to 3.3% a year if positions are sold when a senator leaves office. Series B has a higher Sharpe ratio than SPY. An investor who cannot borrow cannot hold 1.48 times SPY, so the unadjusted comparison may seem the relevant one. And our tests could not detect an alpha below about 12% a year."));
add(P("**Why we still decline.** First, the same risk is available without borrowing, through a high-beta or small-cap fund, so the risk-matched comparison applies to an unlevered investor too. Second, Series B's Sharpe ratio comes from holding cash in 2022, not from the trades. Third, senators' purchases did not outperform before anyone could copy them, which is where informed trading should appear first. Fourth, the profit rests on a handful of positions and on who sits in the Senate: one senator's exit moves the return by 2.6 points and dropping a single senator by up to 5. Fifth, the two ETFs that implement the idea professionally show no alpha either."));
add(P("**What would change our view.** Three pieces of evidence would: a positive return before disclosure on purchases by senators who file quickly, the cleanest sign of information a copier could still capture (in our data +0.28%, t = 0.57, for trades filed within 30 days); CRSP prices for the remaining delisted stocks (V20); and a longer, broader sample, for example including the House, with the power to detect an alpha of 3% to 5% that survives without the two largest contributors. Until then, an investor who wants this level of risk can hold about 1.5 times the index, which delivered the same volatility with 2.9 points a year more return."));

// ---------- 8 Limitations ----------
add(H1("8", "Limitations"));
add(BULLET("**Short sample.** Sixty months, thirty per half, so only very large alphas are detectable (Section 6.5)."));
add(BULLET("**Departing senators.** The frozen rules have no exit when a senator leaves office. V21 shows the effect: +2.6 points of return, with the verdict unchanged."));
add(BULLET("**Survivorship.** 178 symbols remain unpriced, at most 2.2% of capital. Since pricing the largest gaps raised the return, any remaining bias most likely runs downwards."));
add(BULLET("**One dominant filing.** Armstrong's July 2026 report dominates the test half's trade-level statistics, though not the portfolio result (13.15% a year without him, V2.2)."));
add(BULLET("**Price vintage.** Yahoo revises its history, so we use and submit the cached September 2026 files. Two renamed tickers (UTX and DWDP) include spin-offs before the window that affect only the 10-year variant."));

// ---------- 9 Conclusion ----------
add(H1("9", "Conclusion"));
add(P("Copying senators' disclosed trades from September 2021 to August 2026 earned the market's return through a beta of 1.2 and a tilt towards small companies, with higher volatility, a deeper drawdown and no reliably positive alpha in either half, in any sub-period or under any of 23 specifications. Senators' purchases did not run ahead of the market before disclosure, so there was nothing left for a copier to collect, and the filings are read by everyone else too. **We would not invest.** The question deserves another look with complete delisting data and a sample long enough to detect a modest edge; on the evidence available, the strategy is a more volatile and more expensive way to own the index."));

// ---------- References ----------
add(H1("", "References", true));
[
  "Anthropic (2026). *Claude Opus 5.5* [Large language model]. Accessed through claude.ai and Claude Code, September to October 2026. https://www.anthropic.com/claude",
  "Belmont, W., Sacerdote, B., Sehgal, R. and Van Inwegen, I. (2022). Relief rally: Senators as feckless as the rest of us at stock picking. *Journal of Public Economics*, 207, 104602.",
  "Bloomberg L.P. (2026). Daily prices and gross total-return indices for eight stocks absent from Yahoo Finance. LBS library terminal, retrieved 7 October 2026.",
  "Carhart, M. M. (1997). On persistence in mutual fund performance. *Journal of Finance*, 52(1), 57–82.",
  "Eggers, A. C. and Hainmueller, J. (2013). Capitol losses: The mediocre performance of congressional stock portfolios. *Journal of Politics*, 75(2), 535–551.",
  "Fama, E. F. and French, K. R. (1993). Common risk factors in the returns on stocks and bonds. *Journal of Financial Economics*, 33(1), 3–56.",
  "French, K. R. (2026). *Data Library*, US research factors and risk-free rate, monthly and daily. Retrieved September 2026. https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
  "Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65–70.",
  "Jobson, J. D. and Korkie, B. M. (1981). Performance hypothesis testing with the Sharpe and Treynor measures. *Journal of Finance*, 36(4), 889–908.",
  "Memmel, C. (2003). Performance hypothesis testing with the Sharpe ratio. *Finance Letters*, 1(1), 21–23.",
  "Newey, W. K. and West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.",
  "Politis, D. N. and Romano, J. P. (1994). The stationary bootstrap. *Journal of the American Statistical Association*, 89(428), 1303–1313.",
  "STOCK Act (2012). Stop Trading on Congressional Knowledge Act of 2012, Pub. L. 112-105.",
  "United States Senate (2026). *Electronic Financial Disclosures (eFD), Periodic Transaction Reports*, received January 2016 to September 2026. https://efdsearch.senate.gov",
  "@unitedstates project (2026). *congress-legislators* (GitHub repository): Senate service dates and committee membership history. https://github.com/unitedstates/congress-legislators",
  "Yahoo Finance (2026). Daily adjusted closing prices, September 2026 vintage. https://finance.yahoo.com",
  "Ziobrowski, A. J., Cheng, P., Boyd, J. W. and Ziobrowski, B. J. (2004). Abnormal returns from the common stock investments of the U.S. Senate. *Journal of Financial and Quantitative Analysis*, 39(4), 661–676.",
].forEach((r) => add(new Paragraph({ children: runs(r, 20), spacing: { after: 90 }, indent: { left: 400, hanging: 400 } })));

// ---------- Appendix ----------
add(H1("", "Appendix", true));
add(P("The appendix supports the report and is not needed to follow it. Each item names the file it comes from; every number can be rebuilt with the commands in Appendix J."));

add(H2("Statement on the Use of AI Tools"));
add(P("This project used Claude (Anthropic, 2026), a large language model, as an engineering and drafting assistant in several working sessions in September and October 2026. Claude wrote most of the pipeline code (scraping, cleaning, the backtest engine and the statistics), ran it, and drafted the decision log and the report under the group's direction. Every methodological decision, including the scope, the rules, the variants, the registered tests, the freeze and the Bloomberg correction, was made by the group and is dated in docs/DECISIONS.md, where Claude's engineering interpretations are marked and confirmed by the group in later entries. Every number is generated by code in the repository and can be re-derived with one command.", { size: 21 }));

add(H2("A. From Raw Filings to the In-Scope Sample"));
add(table(["Step", "Removed", "Left"], [
  ["All parsed transaction rows, electronic PTRs received 2016-01 to 2026-09", "", "14,592"],
  ["Duplicates restated in amendments or refiled", "2,182", "12,410"],
  ["Transaction date outside the filer's Senate service", "5", "12,405"],
  ["First disclosed outside 2021-09-01 to 2026-08-31", "7,125", "5,280"],
  ["Asset type not stock (municipal bonds 693, options 326, corporate bonds 162, futures 141, other 34)", "1,356", "3,924"],
  ["Options filed as stock, exchanges, no ticker recoverable", "292", "3,632"],
  ["Mutual funds, non-US listings, other instruments, preferred shares", "71", "3,561"],
  ["ETFs that are not equity funds (bond, T-bill, commodity, other)", "187", "3,374"],
  ["Owner spouse or child (kept for variant V6)", "1,034", "**2,340**"],
], [72, 12, 12]));
add(NOTE("From outputs/data_quality.md, Phase 2, section 1. The 85 paper PTRs inside the window are listed with links in data/interim/paper_filings.csv. Of 2,363 in-scope trade records, 31 have no price on the entry date."));

add(H2("B. Who the Strategy Is Really Copying"));
add(figure("report/figures/figA1_concentration.png", 15.5, "B1", "Profit is each copied position's full-life profit, so positions opened before the window include gains made before it."));
add(table(["", "Trades", "Median lag (days)", "Share filed after 45 days"], [
  ["All in-scope trades", "2,340", "33", "30.6%"],
  ["Tommy Tuberville", "732", "31", "0.0%"],
  ["Alan Armstrong", "702", "113", "99.9%"],
  ["Markwayne Mullin", "322", "29", "0.6%"],
  ["John Boozman", "251", "25", "1.6%"],
  ["Sheldon Whitehouse", "81", "27", "4.9%"],
  ["All other senators", "252", "27", "2.0%"],
], [40, 15, 20, 25]));
add(NOTE("Lag is the disclosure date minus the transaction date, in calendar days. From outputs/data_quality.md, Phase 2, sections 5 and 6."));

add(H2("C. The Size of the Portfolio"));
add(figure("report/figures/figA2_capital.png", 15.5, "C1", "Series A weights positions by dollars, so the July 2026 jump changes the portfolio's composition, not the scale of its return."));

add(H2("D. The Bloomberg Correction (C1)"));
add(figure("report/figures/figA3_price_sources.png", 15.5, "D1", "The test half barely moves (22.95% to 22.94%) and every registered verdict is unchanged; only the H2 reversal reading moved, from \"not reversed\" to \"partly reversed\". The design-half statistics move more (Series A from −0.14% to 4.61% a year; H4 from +3.98% to −2.85%), but the predictions were registered on the Yahoo values before the correction and stand unchanged. Every before and after value is in docs/DECISIONS.md, corrections C1 and C2."));

add(H2("E. Every Variant, Full Window and Its Own Test Half"));
add(figure("report/figures/fig7_variants.png", 15.5, "E1", "Return a year on the right. *V11 and V12 use 3- and 10-year windows, so their dates differ."));
const VROWS = JSON.parse(fs.readFileSync(path.join(ROOT, "report", "variants_rows.json")));
const VNAMES = {"H":"Headline","V1":"V1 / V2.1 exclude Tuberville","V2.2":"V2.2 exclude Armstrong","V2.3":"V2.3 exclude Mullin","V2.4":"V2.4 exclude Boozman","V2.5":"V2.5 exclude Whitehouse","V3":"V3 drop first 180 days in office","V4":"V4 drop bulk filings (50+ trades)","V5":"V5 exclude ETFs","V6":"V6 add spouse and child trades","V7":"V7 size at band lower bound","V8":"V8 equal dollars per trade","V9":"V9 same-day entry before 15:30 ET","V10":"V10 equal weight per position","V11":"V11 3-year window (2023-09 on)","V12":"V12 10-year window (2016-09 on)","V13":"V13 exclude OTC names","V14":"V14 amendments as revised","V15":"V15 unpriced stocks earn SPY","V16":"V16 all ETFs incl. bond and T-bill","V17":"V17 empty start (no warm-up)†","V18":"V18 Yahoo prices only†","V19":"V19 include preferred shares†","V20":"V20 CRSP-filled prices†","V21":"V21 sell when senator leaves office‡"};
add(table(["Variant (one rule changed)", "Return", "Sharpe", "CAPM alpha (t)", "Carhart alpha (t)", "Max DD", "Test-half return", "Test-half CAPM alpha (t)"],
  VROWS.filter((r) => r.id !== "V2.1").map((r) => r.status === "run" ? [VNAMES[r.id], r.ret, r.sharpe, r.capm, r.c4, r.mdd, r.oos_ret, r.oos_capm] : [VNAMES[r.id], "not run", "", "", "", "", "", ""]),
  [28, 9, 7, 13, 13, 8, 10, 14], { highlight: (r) => r[0] === "Headline" }));
add(NOTE("Alphas in % a year with OLS t (Figure E1 and Table 2 use Newey-West). V11's test half is 2025-03 to 2026-08 and V12's is 2021-09 to 2026-08. †Registered after the design-half results were seen. ‡Exploratory, added after the test half was opened. V20 needs CRSP data, which requires WRDS access. From outputs/tables/variants_full_bloomberg.md."));

add(H2("F. Exploratory Splits"));
add(P("These splits were examined but are not tests; with hundreds of cells, a few reach |t| = 2 by chance. Full tables are in outputs/tables/mechanism_full_bloomberg.md and committee_full_bloomberg.md."));
add(table(["Purchases, full window", "Events", "Copier, 21 days", "Senator, 63 days"], [
  ["Filed within 30 days", "532", "+1.30% (1.48)", "+1.30% (1.79)"],
  ["Filed after 30 days", "876", "+1.71% (5.13)", "−2.83% (−2.89)"],
  ["Bands up to $50,000", "1,291", "+1.54% (3.47)", "−1.35% (−0.92)"],
  ["Bands above $50,000", "117", "+1.68% (1.36)", "−0.54% (−0.33)"],
  ["Overseen by the senator's committee", "90", "+3.04% (0.80)", "+0.79% (0.36)"],
  ["Not overseen", "977", "+1.25% (2.99)", "+0.50% (0.72)"],
  ["Republican senators", "1,365", "+1.57% (3.65)", "−1.31% (−0.95)"],
  ["Democratic senators", "43", "+1.21% (0.85)", "−0.11% (−0.06)"],
], [40, 12, 24, 24]));
add(NOTE("Mean return minus SPY, with t clustered by month of entry. The committee split excludes ETFs and companies without an SEC industry code. About three-quarters of late purchases come from Armstrong's single report."));

add(H2("G. One Copied Trade, Traced by Hand"));
add(P("Tommy Tuberville bought Johnson & Johnson (joint account, band $1,001 to $15,000) on 30 September 2021. The PTR was received at 13:32 on 15 October 2021, so the copier bought at the close of Monday 18 October at an adjusted price of 139.2527, putting the $8,000.50 midpoint into 57.4531 shares. His full sale of 16 October 2023 was disclosed on 16 November 2023, and the copier sold at the close of 17 November at 137.5493, a return of −1.22% over 525 trading days. Two more traced trades, including a partial sale, are in outputs/phase4_worked_examples.md."));

add(H2("H. Additional Diagnostics"));
add(table(["Statistic", "Value"], [
  ["Sharpe ratio, Series A against SPY (monthly excess returns)", `${D.sharpe_A.toFixed(2)} against ${D.sharpe_SPY.toFixed(2)}`],
  ["Difference, Jobson-Korkie test with the Memmel correction", `${D.sharpe_diff_annual.toFixed(2)} (z = ${D.sharpe_diff_z_memmel.toFixed(2)}, p = ${D.sharpe_diff_p_memmel.toFixed(2)})`],
  ["Difference, 95% stationary block-bootstrap interval", `${D.sharpe_diff_boot_ci95[0].toFixed(2)} to ${D.sharpe_diff_boot_ci95[1].toFixed(2)}`],
  ["CAPM alpha, 95% bootstrap interval, % a year", `${(D.capm_alpha_boot_ci95[0] * 100).toFixed(1)} to ${(D.capm_alpha_boot_ci95[1] * 100).toFixed(1)}`],
  ["Diversification condition, S(A) against ρ × S(SPY)", `${D.sharpe_A.toFixed(3)} against ${D.condition_rhs_rho_x_S_SPY.toFixed(3)}`],
  ["Sharpe change from a 10% allocation to A in SPY", `${D.sharpe_gain_10pct_A_in_SPY.toFixed(4)}; positive in ${(D.share_boot_gain_positive * 100).toFixed(0)}% of resamples`],
  ["Residual volatility of the CAPM regression, % a year", (D.capm_resid_vol_annual * 100).toFixed(1)],
  ["Years of data for t = 2 at an alpha of 2%, 3%, 5%, 10%", ["2%", "3%", "5%", "10%"].map((k) => Math.round(D.years_needed_for_t2[k])).join(", ")],
  ["V21 (sell on departure): return against SPY at its own volatility (k)", `${pct(V21.return, 2)} against ${pct(V21.risk_matched_spy, 2)} (k = ${V21.k.toFixed(2)})`],
], [62, 38]));
add(NOTE(`Computed after the unlock from data/processed/monthly_returns.csv by report/diagnostics.py; not registered tests. Bootstrap ${D.bootstrap.draws.toLocaleString("en-GB")} draws (Politis and Romano, 1994), mean block ${D.bootstrap.mean_block_months} months, fixed seed.`));

add(H2("I. What Was Fixed When"));
add(BULLET("**27 September 2026.** Data source, scope, sizing, entry and exit rules, benchmarks and the design/test split fixed (docs/DECISIONS.md D01 to D20, A01 to A07). Variants V1 to V12 registered before any price, return or performance number had been computed."));
add(BULLET("**28 to 30 September 2026.** V13 to V16 registered before any portfolio return existed. The 12-month warm-up (old rule kept as V17) and the exclusion of preferred shares (V19) were decided after seeing design-half results and are labelled as such, as are V18 and V20."));
add(BULLET("**30 September to 2 October 2026.** Tests H0 to H4 and their predictions registered, then the Holm adjustment, detectable effects and the bulk-filing check added, all before any test-half number existed."));
add(BULLET("**6 October 2026.** Rules frozen at git commit 348318447daa, a fingerprint of the exact code and settings at that moment that cannot be altered later; the test half was then unlocked in a separate commit."));
add(BULLET("**9 October 2026.** Correction C1, Bloomberg prices for eight stocks Yahoo lacks, logged with every before and after value; the Yahoo-only result is kept as V18."));
add(BULLET("**13 October 2026.** Exploratory check V21 (selling when a senator leaves office) added and logged; the headline rules are unchanged."));

add(H2("J. Reproducing Every Number"));
add(P("With Python 3.11, from the repository folder, run pip install -r requirements.txt, then python run_all.py --skip-scrape (about three minutes, offline) and python run_variants.py (about eight minutes). The diagnostics, figures and this document are rebuilt with python report/diagnostics.py, python report/build_figures.py and node report/build_report.js. No file path needs editing."));

add(H2("K. Risk, Stability and Test Charts"));
add(figure("report/figures/fig3_drawdown.png", 15.5, "K1", "Daily value index. Series A's peak-to-trough fall ran from 25 March to 14 July 2022."));
add(figure("report/figures/fig4_calendar.png", 15.5, "K2", "Monthly returns compounded within each calendar year. From outputs/tables/phase5_full_results.md."));
add(figure("report/figures/fig8_rolling_alpha.png", 15.5, "K3", "Each point is a CAPM regression on the previous 24 months of Series A. From report/rolling_alpha_24m.csv (report/diagnostics.py)."));
add(figure("report/figures/fig6_registered_tests.png", 15, "K4", "Navy circles are the registered tests (filled when significant after the Holm adjustment); gold diamonds drop bulk filings. From outputs/tables/confirmatory_oos.md."));

add(H2("L. Threats to Validity"));
add(TTITLE("L1", "Common ways a backtest misleads, and the safeguard used for each"));
add(table(["Threat", "Safeguard", "Effect on Series A"], [
  ["Look-ahead", "Every input dated to when it became public; entry the day after receipt; amendments as first published; universe formed from filings public at formation; committee seats as of the trade date", "Same-day entry +0.5 pts (V9); amendments as revised −0.2 pts (V14)"],
  ["Survivorship", "Scope by official service dates, so departed senators are included; Bloomberg prices for 95% of the missing dollars", "Real prices +2.6 pts (C1); 178 names left are at most 2.2% of capital"],
  ["Cherry-picked window", "Five years fixed in advance, ending where the factor data end; results shown year by year", "3 years 25.5% (V11); 10 years 15.6%, alpha −1.2% (V12)"],
  ["Overfitting", "Variants and tests registered before results; every run reported; Holm adjustment across seven tests", "Range 9.4% to 25.5%; no CAPM alpha with |t| ≥ 2"],
  ["Leverage mistaken for skill", "SPY at the same volatility beside every return", "−2.9 pts a year against it"],
  ["A t-statistic with no economic story", "Counterparty named and its implications tested before the data were opened", "No sign of informed buying (H1)"],
], [17, 52, 31], { left: true }));
add(NOTE("Effects are changes in Series A's annualised return against the headline unless a level is stated. From outputs/tables/variants_full_bloomberg.md and docs/DECISIONS.md."));

// =====================================================================================
const doc = new Document({
  creator: "CA01 study group", title: "Copying the US Senate",
  styles: { default: { document: { run: { font: FONT, size: BODY, color: INK } } } },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "▪", alignment: AlignmentType.LEFT,
      style: { run: { color: RED }, paragraph: { indent: { left: 360, hanging: 260 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134, header: 500, footer: 500 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      new TextRun({ text: "Copying the US Senate  |  CA01 Investment Fundamentals", font: FONT, size: 15, color: MID })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      new TextRun({ text: "London Business School   ", font: FONT, size: 15, color: MID }),
      new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 15, bold: true, color: NAVY })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then((buf) => {
  const out = path.join(ROOT, "report", "Copying_the_Senate_Report_V3.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", out);
});
