// Builds Report V2: report/Copying_the_Senate_Report_V2.docx
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
// London Business School logo palette
const NAVY = "1D5A99", RED = "C23349", PALE = "D8E3EE", MID = "799DC3", INK = "1F2A37", GREY = "5B6573";

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

const thin = { style: BorderStyle.SINGLE, size: 4, color: "C9D3DE" };
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
      alignment: (i === 0 || o.left) ? AlignmentType.LEFT : AlignmentType.RIGHT, spacing: { after: 0, line: 240 },
      keepNext: o.split ? false : ri < nRows - 1,
      children: runs(text, o.size || SMALL, head ? { bold: true, color: NAVY } : (bold ? { bold: true } : {})),
    })],
  });
  const trs = [new TableRow({ tableHeader: true, cantSplit: true, children: header.map((t, i) => cell(t, i, true, "EEF3F8")) })];
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
      trs.push(new TableRow({ cantSplit: true, children: r.map((t, i) => cell(t, i, false, hl ? "F3F6FA" : undefined, hl && i === 0)) }));
    }
  });
  return new Table({ width: { size: W_PAGE, type: WidthType.DXA }, columnWidths: W, layout: TableLayoutType.FIXED, rows: trs });
}

// Key-figure tiles (market-insights style)
function tiles(items) {
  const w = Math.floor(W_PAGE / items.length);
  const c = (big, small) => new TableCell({
    width: { size: w, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: "EEF3F8" },
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
const pct = (x, d = 1) => `${(x * 100).toFixed(d)}%`;
const body = [];
const add = (...xs) => xs.flat().forEach((x) => body.push(x));

// ---------- Title block ----------
add(
  new Table({ width: { size: W_PAGE, type: WidthType.DXA }, columnWidths: [W_PAGE], layout: TableLayoutType.FIXED,
    rows: [new TableRow({ children: [new TableCell({
      width: { size: W_PAGE, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: NAVY },
      margins: { top: 240, bottom: 220, left: 300, right: 300 }, borders: { top: none, bottom: { style: BorderStyle.SINGLE, size: 24, color: RED }, left: none, right: none },
      children: [
        new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "LONDON BUSINESS SCHOOL  |  CA01 INVESTMENT FUNDAMENTALS  |  AUTUMN 2026", font: FONT, size: 16, bold: true, color: PALE })] }),
        new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Copying the US Senate", font: FONT, size: 44, bold: true, color: "FFFFFF" })] }),
        new Paragraph({ spacing: { after: 100 }, children: [new TextRun({ text: "A five-year test of trading on senators' disclosed stock trades, and why an investor should not put money behind it", font: FONT, size: 23, color: "FFFFFF" })] }),
        new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: "Study group [number]  ·  [Member names]  ·  Report V2, October 2026  ·  Code and data: github.com/oshh-star/senate-trades-backtest", font: FONT, size: 16, color: PALE })] }),
      ],
    })] })] }),
  new Paragraph({ spacing: { after: 120 }, children: [] }),
);

// ---------- 1 Executive Summary ----------
add(H1("1", "Executive Summary"));
add(LEAD("Recommendation: do not invest. Copying senators' disclosed trades delivered the market's return with 1.5 times its risk, and no evidence of skill."));
add(tiles([
  ["13.4%", "a year, Series A, Sep 2021 to Aug 2026 (SPY 12.7%)"],
  ["−2.6 pts", "a year against SPY at the same volatility"],
  ["t = 0.18", "CAPM alpha of +1.1% a year; Carhart +2.3%, t = 0.37"],
  ["−2.1%", "senators' purchases against SPY before disclosure"],
]));
add(new Paragraph({ spacing: { after: 80 }, children: [] }));
add(P("We copied every stock trade a sitting US senator disclosed for their own or a joint account, buying at the first close after a purchase became public and selling when the same senator disclosed a sale. Over five years the copied book (Series A) returned **13.41% a year at 23.41% volatility**, against **12.69% at 15.87%** for SPY. The comparison that matters is SPY scaled to the same volatility, which earned **16.30%**. The book's market beta is 1.21 and it tilts towards small caps, and once those exposures are priced the alpha is statistically zero in both the CAPM and the Carhart (1997) four-factor model."));
add(P("Three further findings point the same way. First, the half of the sample we never looked at while designing the rules confirms the verdict, at 22.94% a year against 26.02% for risk-matched SPY. Second, the stocks senators buy do not run ahead of the market between the trade and the disclosure. If anything they lag it, by 2.1% (t = −1.6), so there is no head start for a copier to inherit. Third, the profit is concentrated, with two senators producing three-quarters of it and no specification yielding a reliable alpha. The idea is plausible, but on this evidence it is a costlier and more volatile way to own the market."));

// ---------- 2 Strategy Design ----------
add(H1("2", "Strategy Design"));
add(LEAD("The strategy is a mechanical copy of public filings. Every rule was fixed before the test half of the data was opened."));
add(P("Under the STOCK Act of 2012, a senator must report each trade within 45 days in a Periodic Transaction Report (PTR) on the Senate's electronic disclosure site (eFD). A report states the stock, the date, the direction and the amount as a dollar band ($1,001 to $15,000, $15,001 to $50,000 and so on). It becomes public the moment it is received. Table 1 states every rule, and Figure 1 shows how one disclosure becomes a position. The rules were frozen at commit 348318447daa on 6 October 2026, before the test half was unlocked (Appendix I)."));
add(TTITLE(1, "Trading rules"));
add(table(["Rule", "Specification"], [
  ["Signal", "Every electronic PTR on eFD, keyed to the date and time received. Scanned paper filings cannot be parsed and are counted and excluded."],
  ["Universe", "Anyone serving as a senator on the transaction date (official service dates, not eFD's current label). US common stocks and US-listed equity ETFs, including ADRs and OTC names; no options, bonds, preferred shares, mutual funds, crypto, or bond and commodity ETFs."],
  ["Owner", "The senator's own or joint accounts. Spouse and dependent-child trades are a variant (V6)."],
  ["Entry", "Adjusted close of the first NYSE trading day after the receipt date, the first price a copier could certainly obtain."],
  ["Size", "Midpoint of the disclosed band ($8,000.50 for the smallest); the open-ended top band uses its lower bound."],
  ["Exit", "The same senator's disclosed sale of the same stock, matched first in, first out. A full sale closes every lot; a partial sale sells the band midpoint, capped at the holding. No shorting; sales of stock never copied are ignored."],
  ["Amendments", "Each record acts as first published. A later correction reverses the original action and acts on the corrected record at its own date, so no later information leaks in."],
  ["Window", "Disclosures from 1 September 2021 to 31 August 2026 (60 months), after a 12-month warm-up so the book is not empty on day one."],
], [16, 84], { left: true, split: true }));
add(NOTE("From config/config.yaml and docs/DECISIONS.md (D01 to D20, J3, L2)."));
add(figure("report/figures/fig1_flow.png", 14.5, 1, "The median disclosure lag is across in-scope trades, in calendar days. From outputs/data_quality.md."));

add(H2("2.1 Measuring Returns: Series A and Series B"));
add(LEAD("Copying senators needs a varying amount of money, so the return depends on what it is measured against. We report it two ways and lead with Series A."));
add(P("The book is a collection of lots that appear when senators buy and vanish when they sell. The capital it ties up rose from $1.5m to $24.9m over the window (Appendix C), so there is no fixed fund size to divide profits by. There are two honest ways to turn the book's daily profit into a return, and they answer different questions."));
add(P("**Series A, the headline, is the return on capital deployed.** Each day it takes the dollar-weighted average return of the lots held from the previous close. Suppose the book holds a $10,000 lot that rises 2% and a $30,000 lot that falls 1%. Series A's return that day is (10,000 × 2% − 30,000 × 1%) / 40,000 = −0.25%. On a day with nothing held it earns the risk-free rate. This is the time-weighted return of a fund that is always fully invested in whatever senators currently own, taking in money as new purchases are disclosed and paying it out on sales. It measures the quality of the signal per dollar invested, and it is directly comparable with fully invested benchmarks such as SPY. That is why the verdict rests on it."));
add(P("**Series B is a fixed pot.** It starts with $17.1m, the warm-up book at market value plus the largest net cash the strategy ever required. Purchases draw on the cash, sales refill it, and idle cash earns the risk-free rate. Its return is the change in the pot's total value, like an investor's brokerage account. In the example above, the same $100 loss is spread over $17.1m. Series B is more realistic about funding but less informative about the signal, for two reasons. Its size is only known with hindsight, since nobody in 2021 knew the peak need would be reached in 2026. And because the book was small in 2022, the pot was mostly cash during the bear market, which gives it an accidental market-timing benefit. We therefore report it beside Series A as a check, never as the headline."));

add(H2("2.2 Benchmarks"));
add(P("Each benchmark answers a different question, and all cover identical dates. **SPY** asks whether a passive investor would have done as well. **SPY at Series A's volatility**, the risk-free rate plus 1.48 times SPY's excess return, asks whether the extra return is just leverage, and it is the comparison the verdict rests on. The **Senate universe**, every stock any senator bought in the previous 12 months held in equal weights and rebalanced monthly from public filings only, asks whether timing adds anything beyond the stock list. The **Fama-French (1993) three factors plus Carhart (1997) momentum**, from the US files of the French (2026) data library, are the style benchmark. **NANC and KRUZ**, two listed ETFs launched in February 2023 to track Democratic and Republican congressional trades, show what professional versions of the idea achieved."));

// ---------- 3 Rationale ----------
add(H1("3", "Economic Rationale and Testable Predictions"));
add(LEAD("The case for copying rests on senators knowing things the market does not. For a copier, that knowledge must still be unpriced a month later, so we tested that claim directly."));
add(P("Senators sit on committees that write regulation, award contracts and question executives. Early evidence was striking, with Ziobrowski et al. (2004) estimating that senators' purchases beat the market by about 12% a year in 1993 to 1998. Studies of the period after the STOCK Act find little or nothing (Eggers and Hainmueller, 2013; Belmont et al., 2022)."));
add(P("**Who is on the other side?** A copier buys about a month after the senator, from whoever is selling that day. For that counterparty to keep losing, two things must both be true. The senator's information must still be unpriced when the filing appears, and the market must overlook a public filing that apps, newsletters and two listed ETFs now track. The first is plausible and the second is not. A crowd of copiers buying the same names at once also makes the copier a price-taker rather than a beneficiary."));
add(P("A story that fits any result proves nothing, so before opening the test half we wrote down what each explanation implies in our own data and registered five tests on 30 September 2026. Each explanation leaves a different fingerprint. If senators are informed and the copier is in time, the stocks keep beating the market after disclosure (H2), senators' sales of stocks their committees oversee do worse than their other sales (H3), larger purchases beat smaller ones (H4), and the copied book earns an alpha (H0). If senators are informed but the market prices the news before the filing, the stocks run up between the trade and the disclosure (H1) and only the senator profits. If copiers merely crowd into the same names, prices rise after disclosure and then reverse. A fourth explanation emerged from the design half, that there is no edge at all, only exposure to the market and small caps, which predicts a zero alpha with large factor loadings. Section 6.3 scores every prediction against the result (Table 5)."));
add(NOTE("Tests and predictions registered in docs/DECISIONS.md, \"Out-of-sample test plan\", with Holm (1979) adjusted p-values across seven statistics and the smallest detectable effect for each."));
add(H1("4", "Data and Sample Construction"));
add(LEAD("We built the dataset from the primary source, and every exclusion is counted. Real prices for delisted stocks raised the return, which is the opposite of the usual survivorship worry."));
add(P("We scraped all 1,876 PTRs received on eFD from January 2016 to September 2026, of which 1,568 are electronic and 308 are scanned paper filings that cannot be parsed. Every raw page is cached, so the result does not depend on a website that can change. After removing duplicated amendments and applying the scope rules, the window holds **2,340 in-scope trades by 31 senators**. Corrected amendments add records, making 2,363 trade records in all. Including the warm-up, the copier opened 1,475 lots in 827 symbols, of which 1,398 in 802 symbols were opened inside the window (Appendix A has the full exclusion waterfall). Eighty-five paper PTRs inside the window, 64 of them Richard Blumenthal's, are invisible to any electronic copier."));
add(P("**The sample is concentrated.** Tommy Tuberville, Markwayne Mullin and Alan Armstrong placed 87% of the dollars copied (Appendix B). One Armstrong report received on 21 July 2026 listed 654 purchases of 621 stocks bought in late March 2026. That single filing is 67% of the test half's purchases, and we report every trade-level result with and without it."));
add(P("**Conventions.** Returns are total returns in US dollars, from adjusted closes with dividends reinvested. For a sterling investor the ranking is unchanged, at 13.78% a year for Series A against 13.06% for SPY. The risk-free rate and factors are the Kenneth French US files, one series throughout. The engine runs daily, while every Sharpe ratio and regression uses monthly returns, annualised by √12 for volatility. Trades enter as first published, and prices are a September 2026 vintage."));
add(H2("4.1 Survivorship and the Bloomberg Correction"));
add(P("Yahoo Finance drops delisted companies entirely. With Yahoo alone, purchases of stocks that later vanished would have been skipped, and at their peak in October 2022 they would have been 67% of capital deployed. A group member pulled daily prices and total-return indices from a Bloomberg terminal for the eight largest gaps, which cover 95% of the missing dollars. Seven are delisted (U.S. Steel, ChannelAdvisor, Activision Blizzard, Southern States Bancshares, Paramount Class B, Walgreens and Golden Ocean); the eighth, the Tokyo Electron ADR, still trades but Yahoo serves no history for it. The remaining 178 unpriced symbols are at most 2.2% of capital."));
add(P("**Leaving these stocks out understated the return.** All seven delisted names were taken over, and the large positions in U.S. Steel, ChannelAdvisor and Activision rose on the bids (docs/archive/BLOOMBERG_UPDATE.md), so pricing them raised Series A from 10.81% to 13.41% a year (Appendix D). Filling the gaps with SPY's return (variant V15) is therefore not a conservative bound. Because this change was made after the test half was opened, it is logged as post-unlock correction C1 with every before and after value. The Yahoo-only result is kept as variant V18. No verdict changed."));

// ---------- 5 Results ----------
add(H1("5", "Empirical Results"));
add(H2("5.1 Performance Against Benchmarks"));
add(LEAD("The copied book beat SPY by 0.7 points a year, but it took 1.5 times SPY's volatility to do it. At equal risk SPY wins by 2.6 points, and nothing remains once the market and size exposures are priced."));
add(figure("report/figures/fig2_cumulative.png", 14.5, 2, "End values per $1 in bold. Risk-matched SPY is rf + 1.48 (SPY − rf). The chart compounds daily returns, so it ends at 2.10; the monthly series behind Table 2 ends at 2.13. The dashed line marks the end of the design half."));
add(TTITLE(2, "Copying the Senate against the alternatives, September 2021 to August 2026 (60 months)"));
add(table(["", "Series A (headline)", "Series B (fixed pot)", "SPY", "SPY at A's risk (k = 1.48)", "Senate universe"], [
  ["Return and risk"],
  ["Return, % a year (geometric)", "13.41", "9.16", "12.69", "16.30", "13.56"],
  ["Volatility, % a year", "23.41", "8.03", "15.87", "23.47", "17.14"],
  ["Sharpe ratio", "0.50", "0.69", "0.61", "0.61", "0.62"],
  ["Factor models (monthly, Newey and West (1987) t, 3 lags)"],
  ["CAPM alpha, % a year (t)", "+1.07 (0.18)", "+2.28 (1.08)", "+1.02 (1.62)", "+1.52 (1.62)", "+1.72 (0.74)"],
  ["CAPM beta", "1.21", "0.37", "0.98", "1.45", "1.01"],
  ["Carhart alpha, % a year (t)", "+2.26 (0.37)", "+2.62 (1.25)", "+0.09 (0.21)", "+0.14 (0.21)", "+1.68 (0.77)"],
  ["SMB loading (t)", "0.33 (1.87)", "0.18 (2.33)", "−0.13 (−8.29)", "−0.19 (−8.29)", "0.13 (1.87)"],
  ["Smallest Carhart alpha detectable at t = 2", "12.39", "4.85", "1.01", "1.49", ""],
  ["Loss and diversification"],
  ["Maximum drawdown, %", "−32.16", "−7.13", "−24.50", "−35.31", "−24.58"],
  ["Peak, trough, recovery", "Mar 22, Jul 22, Mar 24", "Jun 26, Jul 26, Aug 26", "Jan 22, Oct 22, Dec 23", "Jan 22, Oct 22, Jan 24", "Nov 21, Oct 22, Dec 23"],
  ["Correlation with SPY, all months / SPY's worst 12", "0.81 / 0.68", "0.73 / 0.36", "1 / 1", "1 / 1", "0.94 / 0.87"],
  ["Trading"],
  ["One-way turnover, % of capital a year", "102", "39", "", "", ""],
  ["Return over risk-matched SPY, % a year", "−2.58", "+0.64", "", "", ""],
  ["Break-even one-way cost", "none", "82 bp", "", "", ""],
], [30, 14, 14, 12, 15, 15], { highlight: (r) => r[0].startsWith("Return, %") || r[0].startsWith("Sharpe") || r[0].startsWith("Return over") }));
add(NOTE("From outputs/tables/phase5_full_results.md. Alphas are monthly estimates × 12. Return over risk-matched SPY is the mean monthly difference × 12 (arithmetic); the geometric gap is 2.9 points. Break-even cost is that return divided by twice the annual turnover; \"none\" means it is already negative before costs."));
add(P("**The extra return is exposure, not skill.** Series A has a beta of 1.21 and a small-cap loading of 0.33, and both can be bought for a few basis points through an index fund and a small-cap fund. Both alphas sit well under one standard error from zero. The equal-weighted Senate universe matched the copied book's return (13.56%) with less risk, so copying the *timing* of trades added nothing beyond the *list* of stocks senators like. The tests are weak, however. With 60 months and this much residual volatility, only an alpha of about 12% a year would have reached t = 2, so a null here means \"no large effect\" rather than \"no effect\" (Section 6.7)."));

add(H2("5.2 Risk, Drawdowns and Diversification"));
add(LEAD("Series A fell further than SPY from its peak and stayed under water longer. Whether it improves a portfolio is a coin flip."));

add(P("Series A's worst fall, 32.2%, was deeper than SPY's 24.5%, and it regained its peak in March 2024, three months after SPY (Figure K1). The textbook test for whether a small allocation improves an existing portfolio is whether the asset's Sharpe ratio exceeds its correlation with the portfolio times the portfolio's Sharpe ratio. For Series A against SPY that is 0.50 against 0.81 × 0.61 = 0.50, a pass by 0.004. Read literally, a marginal allocation helps. In practice it does not survive any reasonable allocation. A 10% slice of Series A in an SPY portfolio *lowers* the Sharpe ratio by 0.002, and across 10,000 stationary block-bootstrap resamples (Politis and Romano, 1994) of the 60 months the slice helps in 49% of them. The difference between the two Sharpe ratios, −0.11, has a p-value of 0.69 in the Jobson and Korkie (1981) test with the Memmel (2003) correction and a bootstrap 95% interval of −0.70 to +0.37 (Appendix H). Its correlation with SPY falls to 0.68 in SPY's worst months, but not far enough to make it a hedge."));

add(H2("5.3 Comparison With Listed Congressional-Trading ETFs"));
add(P("Over the 42 months both ETFs have traded, NANC returned 24.75% a year with a Sharpe ratio of 1.28 and KRUZ 19.31% with 1.05, against 22.32% and 1.33 for SPY. Neither has an alpha distinguishable from zero (CAPM +0.84%, t = 0.44, and −1.33%, t = −0.39). Over the same months Series A returned 19.34% (Sharpe ratio 0.79). Professional versions of the idea also track the market, as they should if the filings carry no information."));

add(H2("5.4 Implementation Costs"));
add(P("Series A turns over about 102% of its capital a year one way. We do not report a net-of-cost return, because a confident cost estimate would be made up. It is also unnecessary, since the book already trails risk-matched SPY before costs and so has no positive break-even cost. 92% of copied purchases are in the two smallest bands (up to $50,000), so most trades are small. The exception is Armstrong's 654-stock basket, which a copier would have to buy in a single day. Series B's break-even of 82 bp one way looks comfortable, but it falls to none in the test half and rests on the hindsight pot size. Costs can only strengthen the verdict."));

// ---------- 6 Robustness ----------
add(H1("6", "Robustness and Out-of-Sample Evidence"));
add(H2("6.1 Design Half Versus Test Half"));
add(LEAD("The half of the data that played no part in designing the rules reaches the same verdict."));
add(TTITLE(3, "The two halves of one continuous backtest (30 months each)"));
add(table(["", "Series A return", "Series A Sharpe", "SPY return", "SPY Sharpe", "Series A CAPM alpha (t)"], [
  ["Design half, Sep 2021 to Feb 2024", "4.61%", "0.20", "6.43%", "0.27", "+1.14% (0.12)"],
  ["Test half, Mar 2024 to Aug 2026", "22.94%", "1.03", "19.32%", "1.17", "+1.69% (0.29)"],
], [34, 13, 13, 13, 12, 15]));
add(NOTE("Annualised geometric returns; Newey-West t. Test half from outputs/tables/phase5_oos_results.md (risk-matched SPY 26.02%). Design half from data/processed/monthly_returns.csv under the headline prices (report/diagnostics.json); the frozen design-half record in outputs/tables/phase5_insample_results.md uses Yahoo prices only."));
add(P("The test half beat SPY by 3.6 points a year in raw terms, but SPY at the same volatility did better still (26.02%), the Sharpe ratio is below the index's in both halves, and the Carhart model attributes the test-half return to market exposure and a momentum loading of 0.38 (t = 3.47). Figure K2 shows the result is not stable from year to year. Series A trailed SPY in 2021, 2023 and 2024 (by 19.9 points in 2024), lost less in 2022, and led in 2025 and 2026, the two years that carry the test-half result."));


add(H2("6.2 Pre-Registered Hypothesis Tests"));
add(LEAD("The predicted nulls held. The two significant results both rest on bulk filings, chiefly one Armstrong report, and both disappear without them."));
add(TTITLE(4, "Confirmatory tests on the test half (March 2024 to August 2026)"));
add(table(["Test", "Prediction", "Estimate (t)", "Holm p", "None larger than", "Verdict", "Without bulk filings"], [
  ["H0 CAPM alpha", "zero", "+1.69% a year (0.29)", "1", "±15.8%", "zero", ""],
  ["H0 Carhart alpha", "zero", "+0.40% a year (0.06)", "1", "±19.2%", "zero", ""],
  ["H1 purchases, trade to disclosure", "near zero", "−3.22% (−2.98)", "0.017", "", "**negative**", "−0.11% (−0.18)"],
  ["H1 sales, trade to disclosure", "near zero", "−0.99% (−0.96)", "1", "±2.8%", "zero", "+0.68% (1.22)"],
  ["H2 copier purchases, 21 days", "positive?", "+1.74% (3.54)", "0.001", "", "**positive**", "+1.12% (0.81)"],
  ["H3 committee sales, overseen minus not", "disappears", "+6.16% (0.94)", "1", "±17.6%", "zero", ""],
  ["H4 small minus large purchases, 126 days", "negative if informed", "+4.82% (0.96)", "1", "±13.5%", "zero", "+1.72% (0.41)"],
], [25, 12, 16, 7, 11, 11, 18], { left: false }));
add(NOTE("From outputs/tables/confirmatory_oos.md. Event returns are the stock's minus SPY's over the same days; t clustered by month of entry for H1 to H4, Newey-West for H0; H2 is one-sided. \"None larger than\" is the Bonferroni-level detectable effect. Bulk filings are reports with 50 or more in-scope trades; the check was registered before the data were opened."));
add(P("H0, H3 and H4 came out as predicted. H1 broke the \"near zero\" prediction, but *against* information, since the stocks senators bought lagged the market before disclosure. H2 is positive. Its registered reversal check is mixed, at +1.73% after 126 days (a hair below the 21-day mean, which the rule calls \"partly reversed\") and +12.03% after 252 days. Both significant results trace to bulk filings, chiefly Armstrong's July 2026 report, whose 621 stocks fell against SPY between the March trades and the July disclosure and then rebounded. A standard error clustered by month, with two-thirds of the events in one month, overstates precision. Without bulk filings, H1 is −0.11% and H2 is +1.12%, neither distinguishable from zero (Figure 3). We read them as one portfolio's reaction to the spring 2026 market, not as evidence about senators."));
add(figure("report/figures/fig6_registered_tests.png", 14, 3, "Navy circles are the registered tests (filled when significant after Holm adjustment); gold diamonds drop bulk filings. From outputs/tables/confirmatory_oos.md."));


add(H2("6.3 Predictions Against Results"));
add(LEAD("Five of the seven registered statistics came out as predicted. One broke its prediction in the direction against information, and the only result favourable to a copier rests on the same bulk filings."));
add(P("Table 5 sets each registered prediction beside the result, and beside what we would have seen if senators really were trading on information a copier could still use. The scorecard matters more than any single number, because the information story makes a joint prediction. Purchases should run up before disclosure, sales should run down, overseen industries and larger trades should be more informative, and the copied book should earn an alpha. If senators were informed, several of these would line up. Only one does, H2, and it rests on bulk filings."));
add(TTITLE(5, "Scorecard: registered predictions against test-half results"));
add(table(["Test", "If senators were informed", "We predicted", "We found", "Held?", "What it tells us"], [
  ["H0 alpha (CAPM, Carhart)", "positive alpha", "zero", "+1.69% (t 0.29); +0.40% (t 0.06)", "**Yes**", "No skill once market and size are priced"],
  ["H1 purchases, trade to disclosure", "run up before the filing", "near zero", "−3.22% (t −2.98); −0.11% without bulk filings", "**No**", "Wrong sign for information, and driven by bulk filings"],
  ["H1 sales, trade to disclosure", "fall before the filing", "near zero", "−0.99% (t −0.96)", "**Yes**", "Senators do not sell ahead of falls"],
  ["H2 copier purchases, 21 days", "positive and persistent", "test the sign", "+1.74% (t 3.54); +1.12% (t 0.81) without bulk filings", "**Partly**", "Positive, but rests on bulk filings; reversal check mixed"],
  ["H3 committee sales", "overseen sales do worse", "the design-half anomaly disappears", "+6.16% (t 0.94)", "**Yes**", "Committee seats carry no visible edge"],
  ["H4 small minus large purchases", "negative (bigger bets on better information)", "negative only if informed", "+4.82% (t 0.96)", "**Yes**", "Size of the bet says nothing"],
  ["Exposure story (not a registered test)", "", "zero alpha, large loadings", "beta 1.21; SMB 0.33 (t 1.87); test-half momentum 0.38 (t 3.47)", "**Yes**", "The return is beta and style"],
], [17, 15, 13, 24, 7, 24], { left: true }));
add(NOTE("Test-half estimates from outputs/tables/confirmatory_oos.md; the exposure row from outputs/tables/phase5_full_results.md and phase5_oos_results.md. \"Held\" judges the result against our registered prediction at Holm-adjusted 5%."));
add(P("**Reading the scorecard.** If the information story were true, H1 would be positive for purchases, H3 and H4 would show the signs in the second column, and H0 would show an alpha. Instead the only significant departure, H1 for purchases, has the opposite sign and disappears once bulk filings, chiefly Armstrong's report, are removed. H2 is the one result a believer could point to, a positive month after disclosure, but without bulk filings it is +1.12% with t = 0.81, and it does not survive in the dollar-weighted portfolio. The pattern fits the fourth explanation in Section 3, no information and only exposure, better than any other."));

add(H2("6.4 What the Disclosure Delay Costs a Copier"));
add(LEAD("If senators were informed, the senator line in Figure 4 would sit above the copier's from the start. For the first three months it sits below it, which is what uninformed trades look like."));
add(figure("report/figures/fig5_event_study.png", 15, 4, "Full window, every in-scope trade, equal-weighted. From outputs/tables/phase5_event_study_full.md and phase5_predisclosure_drift_full.md."));
add(P("Measured from the trade date, the senators' own purchases trailed SPY by 2.44% after a month, while the copier's purchases measured from disclosure beat it by 1.56%. The gap, −4.01% (t = −2.25), means the delay *helped* the copier, because the stocks fell 2.06% against SPY (t = −1.60) in the median 29 trading days before the filing appeared. By six and twelve months the two lines meet. The copier's early gains are equal-weighted, dominated by the same Armstrong basket and statistically fragile (no horizon from 63 days on reaches t = 2), and they do not show up in the dollar-weighted book. Nothing in the sales panel suggests senators sell ahead of falls."));

add(H2("6.5 Stability of Alpha Over Time"));
add(P("A genuine edge should show up across sub-periods. Figure K3 tracks the CAPM alpha over a trailing 24-month window. It swings from about +10% to −16% a year, its 95% interval excludes zero only in three overlapping windows ending December 2024 to February 2025, and there it is *negative*. The full-window alpha of +1.1% is an average of very different periods, not a steady return."));


add(H2("6.6 Alternative Specifications"));
add(LEAD("We changed one rule at a time across five families of choices. The return moves a great deal, but no version produces a reliable alpha."));
add(P("We registered 16 variants (V1 to V16) before computing any return and four more (V17 to V20) after seeing the design-half results, labelled as such. V2 is five runs, one per senator, so there are 24 runs. V20 could not run and V1 duplicates V2.1, leaving 22 distinct specifications with results. Table 6 groups them by the question they ask, and Appendix E lists every run."));
add(TTITLE(6, "What we varied, and what it did to Series A (full window)"));
add(table(["Family", "What changes", "Runs", "Return, % a year", "CAPM alpha, % a year", "Largest |t|"], [
  ["Whose trades", "Drop each of the top five senators; drop senators' first 180 days; drop bulk filings; add spouse and child trades", "8", "9.4 to 18.6", "−2.3 to +5.8", "0.74"],
  ["What we buy", "No ETFs; no OTC names; all ETFs including bond and T-bill funds; add preferred shares", "4", "12.0 to 13.4", "−0.1 to +1.1", "0.18"],
  ["How we size", "Band lower bound; equal dollars per trade; equal-weight lots", "3", "12.4 to 13.4", "+0.8 to +1.1", "0.35"],
  ["When we trade", "Same-day close for filings received before 15:30 ET", "1", "13.9", "+1.5", "0.25"],
  ["Data and window", "3-year and 10-year windows; amendments as revised; unpriced names earn SPY; no warm-up; Yahoo prices only", "6", "10.8 to 25.5", "−1.5 to +3.0", "0.49"],
  ["Headline", "", "", "13.41", "+1.07", "0.18"],
], [14, 44, 6, 13, 14, 9], { highlight: (r) => r[0] === "Headline" }));
add(NOTE("t is the OLS t of the CAPM alpha. CRSP-filled prices (V20) could not run without WRDS access. From outputs/tables/variants_full_bloomberg.md; every run is logged in docs/DECISIONS.md. Figure E1 in Appendix E shows each alpha with its interval."));
add(P("The spread is informative in itself. Dropping Mullin lifts the return to 18.6%, and dropping senators' first 180 days in office, when new members restructure their portfolios, takes four points off. A result that depends this much on who happens to sit in the Senate is not an edge an investor can rely on. Nothing about sizing, timing or the instrument list rescues it, and no variant's CAPM alpha reaches |t| = 2 in the full window or in its own test half. The closest is the 10-year window's Carhart alpha over its own test half (2021 to 2026), which is negative, at −5.75% a year (OLS t = −2.00, Newey-West t = −1.75)."));

add(H2("6.7 Statistical Power and Multiple Testing"));
add(P("Two disciplines protect the conclusion. First, only the seven registered statistics count as tests. Across the 516 exploratory cells with a clustered t-statistic (event study, drift, mechanism splits and committee test), 81 reach |t| = 2. The cells overlap heavily, since the same trades appear at several horizons and splits, and many hits sit in groups that Armstrong's filing dominates. Second, the sample is short. At Series A's residual volatility of 13.1% a year, a genuine alpha of 3% would need about 77 years of monthly data to reach t = 2, and even 5% would need 28 (t ≈ IR × √years). A block bootstrap puts the 95% interval for the CAPM alpha at −9.7% to +12.0% a year. Five years cannot prove that senators have no edge, but they rule out an edge large enough to be worth copying with confidence. Appendix L lists the standard ways a backtest misleads and the safeguard we used for each."));

// ---------- 7 Counter-arguments ----------
add(H1("7", "Counter-Arguments and Conditions for Revisiting"));
add(LEAD("The strongest case for the strategy is that it beat SPY. We take it seriously and still decline."));
add(P("**The case for.** Series A beat SPY over five years (13.41% against 12.69%) and in the test half (22.94% against 19.32%), lost less in the 2022 bear market, and has a positive Carhart alpha. An investor who cannot borrow cannot buy 1.48 times SPY, so for them the plain comparison may seem the relevant one. And our tests could not have detected an alpha below about 12% a year."));
add(P("**Why we still say no.** First, the same risk is available without borrowing, through a high-beta or small-cap fund, so the risk-matched comparison is the fair one even for an unlevered investor. Second, the pre-disclosure evidence shows no sign of information, since senators' purchases did not run ahead of the market before anyone could copy them. Third, the profit is concentrated. Mullin and Ashley Moody produced about three-quarters of the lot profit, Moody with under 5% of the dollars, and dropping a single senator moves the return by up to five points. Fourth, the professional versions of the idea did not deliver skill either. NANC beat SPY on raw return but not on a risk-adjusted basis, KRUZ trailed it, and neither has an alpha distinguishable from zero."));
add(P("**What would change our view.** Three pieces of evidence would. The first is a positive pre-disclosure drift in the purchases of senators who file quickly, which is the cleanest sign of information a copier could still capture. In our data it is +0.28% (t = 0.57) for trades filed within 30 days. The second is CRSP prices for the remaining delisted names (variant V20). The third is a longer and broader sample, for example adding House members, with enough power to detect an alpha of 3% to 5% that survives without the top two senators. Until then, an investor who wants this much risk should hold about 1.5 times the index, which delivered the same volatility with 2.9 points a year more return and no filings to read."));

// ---------- 8 Limitations ----------
add(H1("8", "Limitations"));
add(BULLET("**Short sample.** Sixty months, thirty per half, so only very large alphas are detectable (Section 6.7)."));
add(BULLET("**Survivorship.** 178 symbols remain unpriced, at most 2.2% of capital. Because the priced ones raised the return, any remaining bias most likely runs downwards."));
add(BULLET("**One dominant filing.** Armstrong's July 2026 report dominates the test half's trade-level statistics, though not the portfolio result (V2.2 returns 13.15%)."));
add(BULLET("**One price vintage, two spin-offs.** Yahoo revises its history, so the cached September 2026 files are what we used and submit. Two renamed tickers (UTX and DWDP) include spin-offs before the window that affect only the 10-year variant."));

// ---------- 9 Conclusion ----------
add(H1("9", "Conclusion"));
add(P("Copying senators' disclosed trades from September 2021 to August 2026 earned the market's return through a beta of 1.2 and a small-cap tilt, at higher volatility, with deeper drawdowns and no reliable alpha in any half, period or specification. Senators' purchases did not run ahead of the market before disclosure, so there was nothing left for a copier to collect, and the filings are read by everyone else too. **We would not invest.** The question deserves another look with complete delisting data and a sample long enough to detect a modest edge, but on the evidence available the strategy is a more volatile and more expensive way to own the index."));

// ---------- AI statement ----------
add(H1("", "Statement on the Use of AI Tools"));
add(P("This project used Claude (Anthropic, 2026), a large language model, as an engineering and drafting assistant across several working sessions in September and October 2026. Claude wrote most of the pipeline code (scraping, cleaning, the backtest engine and the statistics), ran it, and drafted the decision log and both report drafts under the group's direction. Every methodological decision, including the scope, the rules, the variants, the registered tests, the freeze and the Bloomberg correction, was made by the group and is dated in docs/DECISIONS.md, with Claude's engineering interpretations marked for the group's confirmation. Every number is generated by code in the repository, re-derivable with one command, and was checked against its source file by an independent model review. [GROUP: confirm this wording against the CA01 AI-use policy before submission.]", { size: 21 }));

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
add(P("The appendix supports the report and is not needed to follow it. Each item names the file it comes from."));

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
  ["Owner Spouse or Child (kept for variant V6)", "1,034", "**2,340**"],
], [72, 12, 12]));
add(NOTE("From outputs/data_quality.md, Phase 2, section 1. 85 paper PTRs inside the window are listed with links in data/interim/paper_filings.csv. Of 2,363 in-scope trade records, 31 have no price on the entry date."));

add(H2("B. Who the Strategy Is Really Copying"));
add(figure("report/figures/figA1_concentration.png", 15.5, "B1", "Lot profit is each copied lot's full-life profit, so warm-up lots include gains before the window."));
add(table(["", "Trades", "Median lag (days)", "Share filed after 45 days"], [
  ["All in-scope trades", "2,340", "33", "30.6%"],
  ["Tommy Tuberville", "732", "31", "0.0%"],
  ["Alan Armstrong", "702", "113", "99.9%"],
  ["Markwayne Mullin", "322", "29", "0.6%"],
  ["John Boozman", "251", "25", "1.6%"],
  ["Sheldon Whitehouse", "81", "27", "4.9%"],
  ["All other senators", "252", "27", "2.0%"],
], [40, 15, 20, 25]));
add(NOTE("Lag is the disclosure date minus the transaction date, calendar days. From outputs/data_quality.md, Phase 2, sections 5 and 6."));

add(H2("C. The Size of the Book"));
add(figure("report/figures/figA2_capital.png", 15.5, "C1", "Series A weights lots by dollars, so the July 2026 jump changes the book's composition, not the scale of its return."));

add(H2("D. The Bloomberg Correction (C1)"));
add(figure("report/figures/figA3_price_sources.png", 15.5, "D1", "The second half barely moves (22.95% to 22.94%) and every registered verdict is unchanged; only the H2 reversal reading moved, from \"not reversed\" to \"partly reversed\". The design-half statistics move more (Series A from −0.14% to 4.61% a year; H4 from +3.98% to −2.85%), but the predictions were registered on the Yahoo values before the correction and stand unchanged. Every before and after value is in docs/DECISIONS.md, corrections C1 and C2."));

add(H2("E. Every Variant, Full Window and Its Own Test Half"));
add(figure("report/figures/fig7_variants.png", 15.5, "E1", "Return a year on the right. *V11 and V12 use 3- and 10-year windows, so their dates differ."));
const VROWS = JSON.parse(fs.readFileSync(path.join(ROOT, "report", "variants_rows.json")));
const VNAMES = {"H":"Headline","V1":"V1 / V2.1 exclude Tuberville","V2.2":"V2.2 exclude Armstrong","V2.3":"V2.3 exclude Mullin","V2.4":"V2.4 exclude Boozman","V2.5":"V2.5 exclude Whitehouse","V3":"V3 drop first 180 days in office","V4":"V4 drop bulk filings (50+ trades)","V5":"V5 exclude ETFs","V6":"V6 add spouse and child trades","V7":"V7 size at band lower bound","V8":"V8 equal dollars per trade","V9":"V9 same-day entry before 15:30 ET","V10":"V10 equal-weight lots","V11":"V11 3-year window (2023-09 on)","V12":"V12 10-year window (2016-09 on)","V13":"V13 exclude OTC names","V14":"V14 amendments as revised","V15":"V15 unpriced names earn SPY","V16":"V16 all ETFs incl. bond and T-bill","V17":"V17 empty start (no warm-up)†","V18":"V18 Yahoo prices only†","V19":"V19 include preferred shares†","V20":"V20 CRSP-filled prices†"};
add(table(["Variant (one rule changed)", "Return", "Sharpe", "CAPM alpha (t)", "Carhart alpha (t)", "Max DD", "Test-half return", "Test-half CAPM alpha (t)"],
  VROWS.filter((r) => r.id !== "V2.1").map((r) => r.status === "run" ? [VNAMES[r.id], r.ret, r.sharpe, r.capm, r.c4, r.mdd, r.oos_ret, r.oos_capm] : [VNAMES[r.id], "not run", "", "", "", "", "", ""]),
  [28, 9, 7, 13, 13, 8, 10, 14], { highlight: (r) => r[0] === "Headline" }));
add(NOTE("Alphas in % a year with OLS t (Figure E1 and Table 2 use Newey-West). V11's test half is 2025-03 to 2026-08 and V12's is 2021-09 to 2026-08. †Registered after the design-half results were seen. From outputs/tables/variants_full_bloomberg.md."));

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
add(NOTE("Mean return minus SPY with t clustered by entry month. The committee split excludes ETFs and companies without an SEC industry code. About three-quarters of late purchases come from Armstrong's single report."));

add(H2("G. One Copied Trade, Traced by Hand"));
add(P("Tommy Tuberville bought Johnson & Johnson (joint account, band $1,001 to $15,000) on 30 September 2021. The PTR was received at 13:32 on 15 October 2021, so the copier bought at the close of Monday 18 October at an adjusted price of 139.2527, putting the $8,000.50 midpoint into 57.4531 units. His full sale of 16 October 2023 was disclosed on 16 November 2023, and the copier sold at the close of 17 November at 137.5493, a return of −1.22% over 525 trading days. Two more traced trades, including a partial sale, are in outputs/phase4_worked_examples.md."));

add(H2("H. Additional Diagnostics"));
add(table(["Statistic", "Value"], [
  ["Sharpe ratio, Series A against SPY (excess returns, monthly)", `${D.sharpe_A.toFixed(2)} against ${D.sharpe_SPY.toFixed(2)}`],
  ["Difference, Memmel-corrected Jobson-Korkie test", `${D.sharpe_diff_annual.toFixed(2)} (z = ${D.sharpe_diff_z_memmel.toFixed(2)}, p = ${D.sharpe_diff_p_memmel.toFixed(2)})`],
  ["Difference, 95% stationary block bootstrap interval", `${D.sharpe_diff_boot_ci95[0].toFixed(2)} to ${D.sharpe_diff_boot_ci95[1].toFixed(2)}`],
  ["CAPM alpha, 95% bootstrap interval, % a year", `${(D.capm_alpha_boot_ci95[0] * 100).toFixed(1)} to ${(D.capm_alpha_boot_ci95[1] * 100).toFixed(1)}`],
  ["Diversification condition, S(A) against ρ × S(SPY)", `${D.sharpe_A.toFixed(3)} against ${D.condition_rhs_rho_x_S_SPY.toFixed(3)}`],
  ["Sharpe change from a 10% slice of A in SPY", `${D.sharpe_gain_10pct_A_in_SPY.toFixed(4)}; positive in ${(D.share_boot_gain_positive * 100).toFixed(0)}% of resamples`],
  ["Residual volatility of the CAPM regression, % a year", (D.capm_resid_vol_annual * 100).toFixed(1)],
  ["Years of data for t = 2 at an alpha of 2%, 3%, 5%, 10%", ["2%", "3%", "5%", "10%"].map((k) => Math.round(D.years_needed_for_t2[k])).join(", ")],
], [62, 38]));
add(NOTE(`Computed after the unlock from data/processed/monthly_returns.csv by report/diagnostics.py; not registered tests. Bootstrap ${D.bootstrap.draws.toLocaleString("en-GB")} draws, mean block ${D.bootstrap.mean_block_months} months, fixed seed.`));

add(H2("I. What Was Fixed When"));
add(BULLET("**27 September 2026.** Data source, scope, sizing, entry and exit rules, benchmarks and the design/test split locked (docs/DECISIONS.md D01 to D20, A01 to A07). Variants V1 to V12 registered at commit 622a455, before any price, return or performance number had been computed."));
add(BULLET("**28 to 30 September 2026.** V13 to V16 registered before any portfolio return existed. The 12-month warm-up (L2, old rule kept as V17) and the exclusion of preferred shares (N2, V19) were decided after seeing design-half results and are labelled as such, as are V18 and V20."));
add(BULLET("**30 September to 2 October 2026.** Tests H0 to H4 and their predictions registered (commit eac5bf6), then Holm adjustment, detectable effects and the bulk-filing check added, all before any test-half number existed."));
add(BULLET("**6 October 2026.** Rules frozen at commit 348318447daa, then the test half unlocked in a separate commit."));
add(BULLET("**9 October 2026.** Post-unlock correction C1, Bloomberg prices for eight stocks Yahoo lacks, logged with every before and after value; the Yahoo-only result is kept as V18."));

add(H2("J. Reproducing Every Number"));
add(P("With Python 3.11, from the repository folder, run pip install -r requirements.txt, then python run_all.py --skip-scrape (about three minutes, offline) and python run_variants.py (about eight minutes). The report's diagnostics, figures and this document are rebuilt with python report/diagnostics.py, python report/build_figures.py and node report/build_report.js. No file path needs editing."));


add(H2("K. Risk and Stability Charts"));
add(figure("report/figures/fig3_drawdown.png", 15.5, "K1", "Daily value index. Series A's peak-to-trough fall ran from 25 March to 14 July 2022."));
add(figure("report/figures/fig4_calendar.png", 15.5, "K2", "Monthly returns compounded within each calendar year. From outputs/tables/phase5_full_results.md, calendar-year returns."));
add(figure("report/figures/fig8_rolling_alpha.png", 15.5, "K3", "Each point is a CAPM regression on the previous 24 months of Series A. From report/rolling_alpha_24m.csv (report/diagnostics.py)."));
add(H2("L. Threats to Validity"));
add(TTITLE("L1", "Common ways a backtest misleads, and what we did about each"));
add(table(["Threat", "Safeguard", "Effect on Series A"], [
  ["Look-ahead", "Every input dated to when it became public; entry the day after receipt; amendments as first published; universe formed from filings public at formation; committee seats as of the trade date", "Same-day entry +0.5 pts (V9); amendments as revised −0.2 pts (V14)"],
  ["Survivorship", "Scope by official service dates, so departed senators are in; Bloomberg prices for 95% of the missing dollars", "Real prices +2.6 pts (C1); 178 names left are ≤ 2.2% of capital"],
  ["Cherry-picked window", "Five years fixed in advance, ending where the factor data end; results shown year by year", "3 years 25.5% (V11); 10 years 15.6%, alpha −1.2% (V12)"],
  ["Overfitting", "Variants and tests registered before results; every run reported; Holm adjustment across seven tests", "Range 9.4% to 25.5%; no CAPM alpha with |t| ≥ 2"],
  ["Leverage mistaken for skill", "SPY at the same volatility beside every return", "−2.6 pts a year against it"],
  ["A t-statistic with no story", "Counterparty named and implied signs tested before the data were opened", "No sign of informed buying (H1)"],
], [17, 52, 31], { left: true }));
add(NOTE("Effects are changes in Series A's annualised return against the headline unless a level is stated. From outputs/tables/variants_full_bloomberg.md and docs/DECISIONS.md."));


// =====================================================================================
const doc = new Document({
  creator: "CA01 study group", title: "Copying the US Senate, Report V2",
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
  const out = path.join(ROOT, "report", "Copying_the_Senate_Report_V2.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", out);
});
