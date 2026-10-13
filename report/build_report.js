// Builds report/Copying_the_Senate_report.docx from the text below and the figures in
// report/figures (python report/build_figures.py) and outputs/figures (python run_all.py).
// Every number in the text is read off a file in outputs/ ; the appendix says which.
// Run from the repo root:  node report/build_report.js
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, ImageRun, Footer, PageNumber, PageBreak, LevelFormat,
  TableLayoutType,
} = require("docx");

const ROOT = path.resolve(__dirname, "..");
const FONT = "Calibri";
const BODY = 22; // 11pt
const SMALL = 18; // 9pt for tables and captions
const CONTENT_W = 9638; // A4 minus 2 x 2 cm margins, DXA
const ACCENT = "1F4E9A";

// ---------- inline markup: **bold**, *italic* ----------
function runs(text, size = BODY, extra = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, size, ...extra }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), bold: true, font: FONT, size, ...extra }));
    else out.push(new TextRun({ text: t.slice(1, -1), italics: true, font: FONT, size, ...extra }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, size, ...extra }));
  return out;
}
const P = (text, opts = {}) => new Paragraph({
  children: runs(text, opts.size || BODY), alignment: opts.align || AlignmentType.JUSTIFIED,
  spacing: { after: opts.after ?? 100, before: opts.before ?? 0, line: 240 }, keepNext: opts.keepNext,
});
const H1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1, spacing: { before: 200, after: 80 }, keepNext: true,
  children: [new TextRun({ text, font: FONT, size: 26, bold: true, color: ACCENT })],
});
const H2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2, spacing: { before: 120, after: 60 }, keepNext: true,
  children: [new TextRun({ text, font: FONT, size: BODY, bold: true, color: "333333" })],
});
const BULLET = (text) => new Paragraph({
  numbering: { reference: "bullets", level: 0 }, children: runs(text), alignment: AlignmentType.JUSTIFIED,
  spacing: { after: 50, line: 240 },
});
const NUM = (text, ref = "nums") => new Paragraph({
  numbering: { reference: ref, level: 0 }, children: runs(text), alignment: AlignmentType.JUSTIFIED,
  spacing: { after: 50, line: 240 },
});
const CAPTION = (text) => new Paragraph({
  children: runs(text, SMALL, { color: "444444" }), alignment: AlignmentType.LEFT,
  spacing: { before: 40, after: 140, line: 240 },
});
const TITLE = (text) => new Paragraph({
  children: runs(text, SMALL + 1, { bold: true }), keepNext: true, spacing: { before: 100, after: 50 },
});

function figure(file, widthCm, caption) {
  const buf = fs.readFileSync(path.join(ROOT, file));
  // PNG width/height from the IHDR chunk
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
  const px = Math.round(widthCm / 2.54 * 96);
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 60, after: 0 },
      children: [new ImageRun({ type: "png", data: buf, transformation: { width: px, height: Math.round(px * h / w) } })],
    }),
    CAPTION(caption),
  ];
}

const thin = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
function table(header, rows, widths, opts = {}) {
  const total = widths.reduce((a, b) => a + b, 0);
  const scale = CONTENT_W / total;
  const W = widths.map((x) => Math.round(x * scale));
  W[W.length - 1] += CONTENT_W - W.reduce((a, b) => a + b, 0);
  const nRows = rows.length + 1;
  let rowIdx = 0;
  const cell = (text, i, isHead, shade, boldRow) => new TableCell({
    width: { size: W[i], type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, color: "auto", fill: shade } : undefined,
    margins: { top: 30, bottom: 30, left: 70, right: 70 },
    borders: { top: none, left: none, right: none, bottom: isHead ? { style: BorderStyle.SINGLE, size: 8, color: "7F7F7F" } : thin },
    children: [new Paragraph({
      alignment: (i === 0 || opts.left) ? AlignmentType.LEFT : AlignmentType.RIGHT, spacing: { after: 0, line: 240 },
      keepNext: rowIdx < nRows - 1,
      children: runs(text, opts.size || SMALL, { bold: isHead || boldRow }),
    })],
  });
  const trs = [new TableRow({ tableHeader: true, cantSplit: true, children: header.map((t, i) => cell(t, i, true, "E8EEF7")) })];
  rows.forEach((r) => {
    rowIdx += 1;
    const sec = r.length === 1;
    if (sec) {
      trs.push(new TableRow({ cantSplit: true, children: [new TableCell({
        columnSpan: W.length, width: { size: CONTENT_W, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, color: "auto", fill: "F4F4F4" },
        margins: { top: 20, bottom: 20, left: 70, right: 70 },
        borders: { top: none, left: none, right: none, bottom: thin },
        children: [new Paragraph({ spacing: { after: 0 }, keepNext: true, children: runs(r[0], opts.size || SMALL, { italics: true }) })],
      })] }));
    } else {
      trs.push(new TableRow({ cantSplit: true, children: r.map((t, i) => cell(t, i, false, undefined, opts.boldFirst && i === 0)) }));
    }
  });
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: W, layout: TableLayoutType.FIXED, rows: trs });
}

// =====================================================================================
// CONTENT
// =====================================================================================
const body = [];
const add = (...xs) => xs.flat().forEach((x) => body.push(x));

// ---------- title block ----------
add(
  new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Copying the US Senate", font: FONT, size: 36, bold: true, color: ACCENT })] }),
  new Paragraph({ spacing: { after: 40 }, children: runs("A five-year backtest of trading on senators' disclosed stock trades, and why we would not put money behind it", 24, { color: "444444" }) }),
  new Paragraph({ spacing: { after: 160 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: ACCENT, space: 4 } },
    children: runs("CA01 Investment Fundamentals, Autumn 2026   |   Study group [number]   |   [Member names]   |   Code and data at github.com/oshh-star/senate-trades-backtest", SMALL, { color: "666666" }) }),
);

// ---------- 1. Recommendation ----------
add(H1("1. The recommendation"));
add(P("**Do not invest.** We copied every stock trade that US senators disclosed electronically for their own or joint accounts between September 2021 and August 2026, buying on the first trading day after a purchase became public and selling when the same senator disclosed a sale. The copied book earned **10.8% a year at 22.4% volatility**, against **12.7% at 15.9% for SPY** over identical months (Sharpe ratios **0.41** and **0.61**). Its market beta is 1.21, and once that leverage is priced nothing is left. The CAPM alpha is **−1.5% a year (t = −0.3)** and the Carhart four-factor alpha is **−0.7% (t = −0.2)**. SPY scaled to the same volatility returned 15.8% a year, so the investor gives up **5.0 points a year** for the same risk before paying a single trading cost."));
add(P("We fixed the rules on the first half of the sample and registered five tests before opening the second half. The second half looks better in raw terms (23.0% against 19.3% for SPY) but still trails volatility-matched SPY (26.0%), and its alpha is again indistinguishable from zero. The evidence on the mechanism points the same way. Stocks senators buy **fall** relative to the market between the trade and its disclosure, which is the opposite of what informed buying would produce. A copier is not trading behind anyone's information, and an investor who wants this much risk can buy it more cheaply as 1.4 times the index."));

// ---------- 2. Strategy ----------
add(H1("2. The strategy, precisely stated"));
add(P("Under the STOCK Act of 2012, every senator must file a Periodic Transaction Report (PTR) within 45 days of a trade, giving the asset, the date, whether it was a purchase or sale, and the amount in a dollar band ($1,001 to $15,000, $15,001 to $50,000 and so on). The reports are published on the Senate's electronic disclosure site (eFD), each stamped with the date and time it was received. Figure 1 shows how one copied trade moves through the book."));
add(figure("report/figures/fig1_timeline.png", 15, "**Figure 1.** How one copied trade works. The senator measure starts at the transaction date and the copier measure at the first close after the PTR is received. The median lag across in-scope trades is 33 calendar days."));
add(P("The rules are mechanical and each is logged with its date and reason. Two were changed after we saw design-half results, and the original versions are kept as variants (Appendix A8 lists the decisions, the dates and the commits)."));
add(BULLET("**Universe.** Every electronic PTR received on eFD from 2016 to September 2026, scraped directly from the Senate site, restricted to trades whose transaction date falls inside the filer's Senate service. We keep US common stocks and US-listed equity ETFs, and drop options, bonds, crypto, mutual funds, preferred shares and bond or commodity ETFs. Only trades the senator controls (owner Self or Joint) count; spouse and child trades are variant V6."));
add(BULLET("**Entry.** Buy at the adjusted close of the first NYSE trading day **after** the date the PTR was received, since many filings arrive after the close. The position size is the midpoint of the disclosed band (the lower bound for the open-ended top band)."));
add(BULLET("**Exit.** A disclosed sale is matched first in, first out to that senator's open copied lots in the same ticker. A full sale closes the position and a partial sale sells the band midpoint, capped at what we hold. Sales of stock we never copied are ignored, and nothing is ever shorted. Positions still open on 31 August 2026 are marked at that day's close."));
add(BULLET("**Amendments.** Every record enters the book **as first published**. If a senator later corrects a filing, the copier reverses the original action on the day of the correction and acts on the corrected record, so no later information is used."));
add(BULLET("**Window.** Disclosures from 1 September 2021 to 31 August 2026, 60 months, with a 12-month warm-up so the book does not start empty. Returns are measured only inside the window."));
add(P("**What capital the return is a return on.** The book grows from $1.2m to $24.9m deployed as senators keep buying, so there is no single natural fund size. We report two series. **Series A**, the headline, is the dollar-weighted daily return on the capital actually deployed, with idle days earning the risk-free rate. It is the return of a fund that takes in money as the signal calls for it. **Series B** is a fixed pot of $17.5m, the warm-up book plus the largest net cash the strategy ever needed, with unused cash earning the risk-free rate. Series B is the honest answer to \"what would a fixed allocation have earned\", but its pot size is only known with hindsight and it held mostly cash in 2022, so we treat it as a secondary check."));
add(P("**Benchmarks.** We compare against (i) **SPY**, the naive alternative; (ii) **SPY scaled to each series' volatility**, rf + k(SPY − rf) with k = 1.41 for series A, the risk-matched alternative and the one the verdict rests on, since series A is far more volatile than the index; (iii) an **equal-weighted portfolio of every stock senators bought in the previous 12 months**, rebalanced monthly using only filings public at formation, which separates *which* stocks senators pick from *when* the copier buys them; (iv) the **Fama-French three factors plus momentum** (US files); and (v) **NANC and KRUZ**, two ETFs launched in February 2023 that sell this exact idea."));

// ---------- 3. Mechanism ----------
add(H1("3. Why it might work, and who is on the other side"));
add(P("The case for copying senators is that they hear things the market does not. They sit on committees that write regulation, award contracts and question executives, and an older literature found striking results. Ziobrowski et al. (2004) estimated that senators' purchases beat the market by about 12% a year in 1993 to 1998. Later work on Congress after the STOCK Act finds little or nothing (Eggers and Hainmueller, 2013; Belmont et al., 2022)."));
add(P("For a copier, private information is not enough. The copier typically buys about a month late and trades with whoever is selling on that day. For that counterparty to keep losing, two things must both hold. The senator's information must still be unpriced when the filing appears, and the market must ignore a public filing that apps, newsletters and two listed ETFs now track. We see no reason to expect the second, and a crowd of copiers buying the same names at once makes the copier the price-taker rather than the beneficiary. So the mechanism is plausible for the senator and doubtful for the copier. Rather than assert either, we wrote down what each story implies in our own data and tested it. Table 1 sets out the predictions."));
add(NUM("**Information before disclosure (H1).** If senators trade on information, their purchases should beat SPY between the trade and the disclosure, and their sales should lag it."));
add(NUM("**Committee oversight (H3).** Trades in industries the senator's committee oversees should carry more information than others. We mapped six committees to SIC industry codes and committed the mapping before computing any split."));
add(NUM("**Size (H4).** A senator acting on conviction should trade more, so larger purchases should beat smaller ones."));
add(NUM("**Short-run drift and reversal (H2).** If copiers move prices, purchases should rise in the month after disclosure and then give it back by six to twelve months. If the senator was informed, the gain should not reverse."));
add(NUM("**Portfolio alpha (H0).** If none of this survives the disclosure lag, the copied book should have no alpha once its market and style exposure is priced."));
add(TITLE("Table 1. What each explanation predicts in our data"));
add(table(
  ["Measure", "Senators informed, copier still in time", "Senators informed, priced before filing", "No information, copiers crowd in", "No information at all"],
  [
    ["Purchases, trade to disclosure (H1)", "positive", "strongly positive", "zero", "zero"],
    ["Copier purchases, first month (H2)", "positive, persists", "zero", "positive, then reverses", "zero"],
    ["Committee-overseen minus other (H3)", "positive", "positive (senator only)", "zero", "zero"],
    ["Large minus small purchases (H4)", "positive", "positive (senator only)", "zero", "zero"],
    ["Copied book alpha (H0)", "positive", "zero", "zero or negative", "zero"],
  ],
  [27, 19, 19, 19, 16], { left: true },
));
add(CAPTION("Only the first column is worth paying for. Sign conventions for sales are reversed. The tests and our predictions were registered on 30 September 2026 (docs/DECISIONS.md, \"Out-of-sample test plan\")."));
add(P("Our in-sample results led us to predict nulls for H0, H1 and H3 and to test the sign of H4, and we registered those predictions, with Holm-adjusted p-values across the seven statistics and the smallest effect each test could detect, before any second-half number existed."));

// ---------- 4. Data ----------
add(H1("4. Data and sample"));
add(P("**Trades.** We scraped all 1,876 PTRs received on eFD from January 2016 to September 2026 (1,568 electronic, 308 scanned paper filings that cannot be parsed). Every raw page is cached in the repository, so the results do not depend on a website that can change. After de-duplicating amendments and applying the scope rules, the window holds **2,340 in-scope trades by 31 senators**, 1,404 purchases and 936 sales, worth $87.7m at band midpoints (Appendix A1 has the full exclusion waterfall). The sample is concentrated. Tommy Tuberville, Alan Armstrong and Markwayne Mullin account for 75% of trades, and one Armstrong filing received on 21 July 2026, listing 654 purchases of 621 stocks made in late March 2026, is 67% of second-half purchases (Appendix A2). We report results with and without it throughout. Eighty-five paper PTRs inside the window, 64 of them Richard Blumenthal's, are invisible to us."));
add(P("**Prices and conventions.** Prices are Yahoo Finance adjusted closes, so returns are **total returns in US dollars** with dividends reinvested. The risk-free rate and factors are the **US files from Kenneth French's data library**, monthly for every statistic (the daily RF only for idle days in the daily book), one series throughout. The engine runs daily; Sharpe ratios, volatilities and regressions use **monthly** returns and are annualised by √12; drawdowns use the daily value index. Trade data are **as first published** on eFD, and prices are the current Yahoo vintage. For a sterling investor the ranking is unchanged (series A 11.2% a year in pounds against 13.1% for SPY)."));
add(P("**Survivorship.** Yahoo drops delisted companies entirely. 186 symbols that senators traded have no usable prices (acquired, bankrupt or recycled tickers), so their purchases are logged and skipped. At cost, these skipped positions were a median 2.7% of capital deployed but peaked at 67% in October 2022. We requested CRSP access, which includes delisted stocks, but it did not arrive in time. We bound the effect with variant V15, which gives every skipped purchase SPY's return over its holding period. It moves series A from 10.8% to 11.6% a year and its alpha from −1.48% to −0.65%, so the gap would have to be very unusual to change the verdict."));

// ---------- 5. Results ----------
add(H1("5. Results"));
add(P("Table 2 sets the copied book beside its benchmarks over the same 60 months, and Figure 2 shows the path."));
add(figure("outputs/figures/phase5_cumulative_value.png", 14, "**Figure 2.** Value of $1 invested at the close of 31 August 2021. The dashed line marks the end of the design sample. Series A finishes at 1.67, below SPY (1.82), the senators' own stock picks held equally (1.86) and SPY at the same volatility (2.07)."));
add(TITLE("Table 2. Full window, September 2021 to August 2026 (60 months), USD total returns"));
add(table(
  ["", "Series A (headline)", "Series B (fixed pot)", "SPY", "SPY risk-matched to A (k = 1.41)", "Senate universe, equal weight"],
  [
    ["Return and risk"],
    ["Annualised return (geometric)", "10.81%", "8.78%", "12.69%", "15.83%", "13.21%"],
    ["Annualised volatility", "22.37%", "7.53%", "15.87%", "22.41%", "17.26%"],
    ["Sharpe ratio (excess over rf)", "0.41", "0.69", "0.61", "0.61", "0.60"],
    ["Factor models (monthly, Newey-West t)"],
    ["CAPM alpha, % a year (t)", "−1.48 (−0.33)", "2.26 (1.18)", "1.02 (1.62)", "1.45 (1.62)", "1.34 (0.59)"],
    ["CAPM beta", "1.21", "0.32", "0.98", "1.38", "1.02"],
    ["Carhart alpha, % a year (t)", "−0.74 (−0.16)", "2.52 (1.33)", "0.09 (0.21)", "0.13 (0.21)", "1.31 (0.62)"],
    ["Smallest alpha detectable at t = 2 (Carhart)", "10.56%", "4.81%", "1.01%", "1.42%", "4.43%"],
    ["Loss and diversification"],
    ["Maximum drawdown (daily)", "−32.2%", "−7.1%", "−24.5%", "−33.9%", "−25.6%"],
    ["Peak, trough", "Mar 22, Nov 22", "Jun 26, Jul 26", "Jan 22, Oct 22", "Jan 22, Oct 22", "Nov 21, Oct 22"],
    ["Recovered (trading days from trough)", "Jun 2025 (649)", "Aug 2026 (11)", "Dec 2023 (294)", "Jan 2024 (318)", "Jan 2024 (317)"],
    ["Correlation with SPY, all months / SPY's worst 12", "0.86 / 0.88", "0.69 / 0.27", "1 / 1", "1 / 1", "0.95 / 0.89"],
    ["Trading"],
    ["One-sided turnover, % of capital a year", "100%", "35%", "", "", ""],
    ["Return over risk-matched SPY, % a year", "−4.48%", "+0.55%", "", "", ""],
    ["Break-even one-way cost", "none", "79 bp", "", "", ""],
  ],
  [30, 14, 14, 11, 15, 14],
));
add(CAPTION("From outputs/tables/phase5_full_results.md. Risk-matched SPY is rf + k(SPY − rf) built monthly so its volatility equals the series'. Alphas are monthly estimates × 12. Break-even cost is the return over risk-matched SPY divided by twice annual turnover; \"none\" means that return is already negative."));
add(H2("Leverage, not skill"));
add(P("Series A's 10.8% looks respectable until it is set beside its risk. A beta of 1.21 and volatility 1.4 times the market's mean the fair comparison is the index at 1.41 times, which earned 15.8% a year. The copier takes the same risk and earns 5.0 points a year less (4.5 on the arithmetic measure in Table 2, which is the one trading costs are set against). Both factor alphas are negative, and the Carhart loadings show nothing to explain (SMB 0.24, HML 0.08, momentum 0.04, none significant). The book is a high-beta, noisy version of the market."));
add(H2("It does not improve a portfolio the reader already holds"));
add(P("A small allocation to an asset raises the Sharpe ratio of a portfolio B only if its own Sharpe exceeds its correlation with B times B's Sharpe. For series A against SPY that requires 0.41 > 0.86 × 0.61 = 0.52, which fails. Nor is it a hedge, since its correlation with SPY rises to 0.88 in SPY's twelve worst months. Its worst drawdown, −32.2%, was deeper than SPY's −24.5% and took 649 trading days to recover against 294 (Figure 3). Series B does pass the test (0.69 > 0.42), but only because it was mostly cash during 2022 and its pot size uses hindsight, and its alpha is not significant (t = 1.2)."));
add(figure("outputs/figures/phase5_drawdowns.png", 12.5, "**Figure 3.** Drawdown of the daily value index from its previous peak. Series A fell 32.2% from 29 March to 3 November 2022 and regained its peak only on 9 June 2025; SPY fell 24.5% and recovered in December 2023."));
add(H2("It does not beat the products that sell the idea either"));
add(P("Over the 42 months both ETFs have traded, NANC returned 24.8% a year with a Sharpe of 1.28 and KRUZ 19.3% with 1.05, against 22.3% and 1.33 for SPY. Neither has a significant alpha (0.8% and −1.3%), and series A over the same months returned 21.6% with a Sharpe of 0.90 (Appendix A3). Professionally run versions of this strategy track the market, which is what we would expect if the signal carries no information."));
add(H2("What it costs to trade"));
add(P("Series A turns over about 100% of its capital a year one way, and many copied names are small or traded over the counter. We do not estimate a net-of-cost return, because a confident cost number would be made up. It does not matter here, since the strategy already trails its risk-matched benchmark before costs, so there is no positive break-even cost. Series B's break-even of 79 bp one way is comfortably above typical one-way costs for liquid US large caps, but it falls to none in the second half, and it rests on the hindsight pot size noted above."));

// ---------- 6. Robustness ----------
add(H1("6. Robustness"));
add(H2("Out of sample"));
add(P("We designed everything on September 2021 to February 2024 and froze the rules at a recorded commit (348318447daa) on 6 October 2026. The second half, March 2024 to August 2026, had influenced no choice when we opened it. Table 3 shows both halves read off the same continuous book."));
add(P("The test half beat SPY by 3.6 points a year in raw terms, and calendar 2025 and 2026 were strong (27.9% and 26.8% against 17.7% and 13.1%). But volatility-matched SPY did better still, the Sharpe ratio is lower than the index's in both halves, and the Carhart regression attributes the test-half return to market exposure and a momentum loading of 0.38 (t = 3.5) rather than to alpha. Table 4 shows the edge is not stable from year to year. Series A trailed SPY in each of its first four calendar years, by 19 points in 2024, and led only in 2025 and 2026, the two years that carry the test-half result."));
add(TITLE("Table 3. The two halves of the same backtest (30 months each)"));
add(table(
  ["", "Design, Series A", "Design, SPY", "Design, SPY risk-matched", "Test, Series A", "Test, SPY", "Test, SPY risk-matched"],
  [
    ["Annualised return", "−0.14%", "6.43%", "6.84%", "22.95%", "19.32%", "26.03%"],
    ["Annualised volatility", "26.40%", "18.99%", "26.45%", "17.47%", "12.12%", "17.52%"],
    ["Sharpe ratio", "0.02", "0.27", "0.27", "1.03", "1.17", "1.17"],
    ["CAPM alpha, % a year (t)", "−3.95 (−0.59)", "1.65 (1.47)", "2.31 (1.47)", "1.66 (0.28)", "0.47 (0.92)", "0.68 (0.92)"],
    ["Carhart alpha, % a year (t)", "−1.86 (−0.27)", "0.45 (0.61)", "0.63 (0.61)", "0.35 (0.05)", "−0.27 (−0.72)", "−0.39 (−0.72)"],
    ["Maximum drawdown", "−32.2%", "−24.5%", "−33.4%", "−19.6%", "−18.8%", "−26.4%"],
    ["Return over risk-matched SPY", "−6.78%", "", "", "−2.51%", "", ""],
  ],
  [26, 12, 11, 13, 12, 11, 13],
));
add(CAPTION("Design half September 2021 to February 2024, test half March 2024 to August 2026. Risk-matched SPY uses each half's own k (1.40 and 1.45). Newey-West t. From outputs/tables/phase5_insample_results.md and phase5_oos_results.md; the full run reproduces the design half to the bit."));
add(TITLE("Table 4. Year by year (calendar years, USD total returns)"));
add(table(
  ["", "2021 (Sep to Dec)", "2022", "2023", "2024", "2025", "2026 (Jan to Aug)"],
  [
    ["Series A", "−0.0%", "−21.4%", "+24.0%", "+5.7%", "+27.9%", "+26.8%"],
    ["SPY", "+5.9%", "−18.2%", "+26.2%", "+24.9%", "+17.7%", "+13.1%"],
    ["SPY risk-matched to A", "+8.2%", "−26.3%", "+35.3%", "+33.6%", "+23.4%", "+17.3%"],
    ["Senate universe, equal weight", "+2.2%", "−16.9%", "+21.5%", "+18.4%", "+29.0%", "+18.0%"],
    ["Series A minus SPY", "−5.9", "−3.2", "−2.2", "−19.2", "+10.2", "+13.7"],
  ],
  [28, 13, 11, 11, 11, 11, 15],
));
add(CAPTION("Monthly returns compounded within each year; the last row is in percentage points. Risk-matched SPY uses the full-window k of 1.41. From outputs/tables/phase5_full_results.md."));
add(H2("The registered tests"));
add(P("Table 5 reports the seven confirmatory statistics, judged on Holm-adjusted p-values exactly as registered."));
add(TITLE("Table 5. Confirmatory tests on the test half (March 2024 to August 2026)"));
add(table(
  ["Test", "Estimate", "t", "Holm p", "Prediction", "Verdict", "Without bulk filings"],
  [
    ["H0a CAPM alpha, series A", "+1.66% a year", "0.28", "1.00", "zero", "zero (none above ±15.9%)", ""],
    ["H0b Carhart alpha, series A", "+0.35% a year", "0.05", "1.00", "zero", "zero (none above ±19.2%)", ""],
    ["H1 purchases, trade to disclosure", "−3.20%", "−2.94", "0.02", "near zero", "**negative**", "−0.05% (t −0.08)"],
    ["H1 sales, trade to disclosure", "−0.95%", "−0.94", "1.00", "near zero", "zero", "+0.67% (t 1.19)"],
    ["H2 copier purchases, 21 days", "+1.75%", "3.57", "0.001", "one-sided, > 0?", "**positive**, not reversed", "+1.09% (t 0.80)"],
    ["H3 sales, committee minus other, 63 days", "+6.01%", "0.92", "1.00", "disappears", "zero", ""],
    ["H4 purchases ≤ $50k minus larger, 126 days", "+5.39%", "1.01", "1.00", "negative if informed", "zero", "+2.15% (t 0.48)"],
  ],
  [27, 11, 6, 7, 12, 19, 14],
));
add(CAPTION("Event returns are the stock's minus SPY's over the same days; t clustered by month of entry for H1 to H4, Newey-West for H0. \"None above\" gives the Bonferroni-level detectable effect, the smallest effect the test could have found. Bulk filings are PTRs with 50 or more in-scope trades. From outputs/tables/confirmatory_oos.md."));
add(P("The predicted nulls held for both alphas, for sales, for the committee test and for size, and the two surprises both trace to one filing. H1 for purchases is significantly **negative**, the opposite of informed buying, and H2 is significantly positive with no reversal. Both are driven by Armstrong's July 2026 filing, whose 621 stocks fell 4.7% relative to SPY between the March trades and the July disclosure and then rebounded. Without bulk filings, H1 is −0.05% and H2 is +1.09%, neither distinguishable from zero. A clustered standard error with two-thirds of the events in one month overstates precision, so we read these as one portfolio's reaction to the spring 2026 market, not as evidence about senators."));
add(P("Figure 4 shows the same pattern over the full window. The senator's purchases are flat to negative against SPY for three months after the trade, and the copier's positive month-one return carries t = 3.7 but is equal-weighted, dominated by the same filing, and does not show up in the dollar-weighted book. Nothing in the sales panel suggests that senators sell ahead of falls."));
add(P("The gap between the two lines is what the disclosure delay costs a copier, and it has the wrong sign for the story. Over the first month the senator's own purchases trailed the copier's by 4.0 points (t = −2.2), because the stocks fell 2.1% relative to SPY in the 29 trading days between the trade and the filing. By six and twelve months the two lines meet (gaps of +0.3%, t = 0.5 and 0.2). If senators held information that the delay gave away, the senator line would sit above the copier's. It sits below it and then joins it, which is what uninformed trades look like."));
add(figure("report/figures/fig3_event_study.png", 16, "**Figure 4.** Mean return minus SPY after senators' trades, full window, with 95% bands clustered by month. Orange starts at the senator's transaction date and blue at the copier's entry. Exploratory, since about 150 cells were examined in the design half and a few will reach |t| = 2 by chance. From outputs/tables/phase5_event_study_full.md."));
add(H2("Every variant we ran"));
add(P("We registered 16 variants before computing any return and four more (V17 to V20) after seeing the design-half results, labelled as such. We report every run, 23 in all (V1 and V2.1 are the same rule, and V20 could not run without CRSP data; Appendix A5). Figure 5 shows the alpha of each. Series A's return ranges from 6.4% a year (dropping senators' first 180 days in office) to 25.8% (a three-year window starting September 2023), and **no variant's alpha reaches |t| = 2**. Leaving out Mullin adds 5.1 points and leaving out Tuberville 2.5, so the result is sensitive to which senator dominates, but none of the variants turns the book into something with a reliable alpha."));
add(figure("report/figures/fig4_variants.png", 15, "**Figure 5.** Series A CAPM alpha for the headline and each pre-registered variant, each changing one rule, full window. *V11 and V12 use 3- and 10-year windows. From outputs/tables/variants_full_yahoo.md."));

// ---------- 7. What would change our mind ----------
add(H2("Six ways to be wrong, and what we did about each"));
add(TITLE("Table 6. Threats to the result and how much each could move it"));
add(table(
  ["Threat", "What we did", "Effect on series A (full window)"],
  [
    ["Look-ahead", "Every input dated to when it became public. Entry the day after receipt; amendments as first published; benchmark universe formed only from filings public at formation; committee seats as of the trade date", "Same-day entry +0.4 pt (V9); amendments as revised −0.3 pt (V14)"],
    ["Survivorship", "Scope set by Senate service dates, so senators who later left are in. Delisted names without Yahoo prices are skipped and bounded", "Skipped names earn SPY +0.8 pt (V15)"],
    ["Cherry-picked window", "Five years fixed in advance, ending where the factor data end; year-by-year results shown", "3 years 25.8% (V11); 10 years 15.3%, alpha −1.5% (V12)"],
    ["Overfitting", "Variants registered before results; every run reported; seven confirmatory tests with Holm adjustment", "Range 6.4% to 25.8%; no alpha with |t| ≥ 2"],
    ["Leverage mistaken for skill", "SPY scaled to the same volatility beside every return", "−5.0 pt a year against it"],
    ["A t-statistic with no story", "Counterparty named and the implied signs tested before the data were opened", "The informed-buying sign is contradicted (H1)"],
  ],
  [17, 55, 28], { left: true },
));
add(CAPTION("Effects are changes in series A's annualised return relative to the headline (pt = percentage points), except the window row, which gives levels, and the leverage row, which is the gap to risk-matched SPY. From outputs/tables/variants_full_yahoo.md and docs/DECISIONS.md."));
add(H1("7. What would change our mind"));
add(P("**The strongest case against our verdict** is the recent record. Since March 2024 series A has beaten SPY by 3.6 points a year, the three-year variant returns 25.8% with a Sharpe of 1.12, and the equal-weighted basket of stocks senators bought earned a CAPM alpha of 4.4% in the test half (t = 1.45). An investor could argue that disclosure has become better, that the post-2023 cohort of senators is different, or that the edge lies in *which* stocks senators pick rather than in copying their timing."));
add(P("We take this seriously and still decline, for three reasons. First, the raw outperformance disappears against SPY at the same volatility, and the Sharpe ratio is below the index's in every half and in the full window. Second, the recent sample is concentrated in a handful of senators and one giant filing, and the momentum loading explains what remains. Third, and most important, our tests cannot detect the kind of edge an investor should care about. The smallest Carhart alpha the full window could distinguish from zero is about **10.6% a year**. At this book's residual volatility, a genuine alpha of 3% a year would need more than fifty years of data to reach t = 2 (Appendix A10). A null from five years is therefore weak evidence of absence, and a positive point estimate from two and a half years is weaker still."));
add(P("Three things would change our view. (i) **CRSP prices for the delisted names** (variant V20), if they showed the skipped purchases did far better than the market. (ii) **A positive pre-disclosure drift in the purchases of short-lag filers**, which is the cleanest sign of information a copier could still capture. In our data it is +0.3% (t = 0.6) for trades filed within 30 days. (iii) **A longer, broader sample**, such as adding House members, that gives the tests enough power to detect a 3% to 5% alpha. Until then, an investor who wants this much risk should hold 1.4 times the index, which delivered the same volatility with 5 points a year more return and no filings to read."));

// ---------- References ----------
add(H1("8. The bottom line for an investor"));
add(BULLET("**Return.** 10.8% a year over five years, 1.9 points a year below SPY and 5.0 below SPY at the same volatility."));
add(BULLET("**Risk.** Beta 1.21, volatility 22.4%, a −32% drawdown that took two and a half years to recover, and no diversification when markets fall."));
add(BULLET("**Skill.** No positive alpha distinguishable from zero in the full window, in either half or in any variant. The two significant results in the test half both belong to a single filing, and one of them has the opposite sign to informed buying."));
add(BULLET("**Mechanism.** Senators' purchases do not run up before disclosure, so there is nothing left for a copier to collect, and the disclosure is read by everyone else too."));
add(P("We would not invest. The idea is worth revisiting with CRSP prices for the delisted names and a sample long enough to detect a modest alpha, but on the evidence available the strategy is a more volatile and more expensive way to own the market.", { before: 60 }));
add(new Paragraph({ children: [new PageBreak()] }));
add(H1("References"));
[
  "Belmont, W., Sacerdote, B., Sehgal, R. and Van Inwegen, I. (2022). Relief rally: Senators as feckless as the rest of us at stock picking. *Journal of Public Economics*, 207, 104602.",
  "Carhart, M. M. (1997). On persistence in mutual fund performance. *Journal of Finance*, 52(1), 57–82.",
  "Eggers, A. C. and Hainmueller, J. (2013). Capitol losses: The mediocre performance of congressional stock portfolios. *Journal of Politics*, 75(2), 535–551.",
  "Fama, E. F. and French, K. R. (1993). Common risk factors in the returns on stocks and bonds. *Journal of Financial Economics*, 33(1), 3–56.",
  "French, K. R. Data Library, US research factors and risk-free rate, monthly and daily files (downloaded September 2026). mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
  "Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65–70.",
  "Newey, W. K. and West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.",
  "Stop Trading on Congressional Knowledge (STOCK) Act of 2012, Pub. L. 112-105.",
  "United States Senate, Electronic Financial Disclosures (eFD), Periodic Transaction Reports. efdsearch.senate.gov",
  "unitedstates/congress-legislators, Senate service dates and committee membership history. github.com/unitedstates/congress-legislators",
  "Ziobrowski, A. J., Cheng, P., Boyd, J. W. and Ziobrowski, B. J. (2004). Abnormal returns from the common stock investments of the U.S. Senate. *Journal of Financial and Quantitative Analysis*, 39(4), 661–676.",
].forEach((r) => add(new Paragraph({ children: runs(r, 20), spacing: { after: 80 }, indent: { left: 360, hanging: 360 } })));

// ---------- Appendix ----------
add(new Paragraph({ children: [new PageBreak()] }));
add(H1("Appendix"));
add(P("The appendix supports the report and is not needed to follow it. Every number in the report can be rebuilt with two commands (A9), and each table below names the file it comes from."));

add(H2("A1. From raw filings to the in-scope sample"));
add(table(
  ["Step", "Removed", "Left"],
  [
    ["All parsed transaction rows, electronic PTRs received 2016-01 to 2026-09", "", "14,592"],
    ["Duplicates restated in amendments or refiled", "2,182", "12,410"],
    ["Transaction date outside the filer's Senate service", "5", "12,405"],
    ["First disclosed outside 2021-09-01 to 2026-08-31", "7,125", "5,280"],
    ["Asset type not stock (municipal bonds 693, options 326, corporate bonds 162, futures 141, other 34)", "1,356", "3,924"],
    ["Options filed as stock, exchanges, no ticker recoverable", "292", "3,632"],
    ["Mutual funds, non-US listings, other instruments, preferred shares", "71", "3,561"],
    ["ETFs that are not equity funds (bond, T-bill, commodity, other)", "187", "3,374"],
    ["Owner Spouse or Child (kept for variant V6)", "1,034", "**2,340**"],
  ],
  [70, 12, 12],
));
add(CAPTION("From outputs/data_quality.md, Phase 2, section 1. 85 paper PTRs received inside the window cannot be parsed and are listed with links in data/interim/paper_filings.csv. Of 2,363 in-scope purchase and sale records, 2,273 (96.2%; 93.8% of dollars) have a usable price on the entry date."));

add(H2("A2. Who the strategy is really copying"));
add(figure("report/figures/figA1_concentration.png", 15.5, "**Figure A1.** Share of in-scope trades and dollars by senator. From outputs/data_quality.md, Phase 2, section 5."));
add(table(
  ["", "Trades", "Median lag (days)", "Share filed after 45 days"],
  [
    ["All in-scope trades", "2,340", "33", "30.6%"],
    ["Tommy Tuberville", "732", "31", "0.0%"],
    ["Alan Armstrong", "702", "113", "99.9%"],
    ["Markwayne Mullin", "322", "29", "0.6%"],
    ["John Boozman", "251", "25", "1.6%"],
    ["Sheldon Whitehouse", "81", "27", "4.9%"],
    ["All other senators", "252", "27", "2.0%"],
  ],
  [40, 15, 20, 25],
));
add(CAPTION("Lag is disclosure date minus transaction date, calendar days. From outputs/data_quality.md, Phase 2, section 6. Almost all late filings are Armstrong's single July 2026 report."));

add(H2("A3. Calendar years, the worst year, and the ETFs"));
add(table(
  ["Year", "Series A", "Series B", "SPY", "SPY risk-matched to A", "Senate universe", "NANC", "KRUZ", "Risk-free"],
  [
    ["2021 (Sep to Dec)", "−0.00%", "+0.04%", "+5.89%", "+8.15%", "+2.22%", "", "", "+0.01%"],
    ["2022", "−21.40%", "−2.01%", "−18.18%", "−26.32%", "−16.89%", "", "", "+1.41%"],
    ["2023", "+24.00%", "+11.96%", "+26.18%", "+35.34%", "+21.49%", "+27.30%*", "+13.74%*", "+4.94%"],
    ["2024", "+5.72%", "+5.14%", "+24.89%", "+33.58%", "+18.40%", "+26.82%", "+14.44%", "+5.25%"],
    ["2025", "+27.88%", "+13.64%", "+17.72%", "+23.37%", "+28.99%", "+18.54%", "+17.11%", "+4.25%"],
    ["2026 (Jan to Aug)", "+26.79%", "+16.13%", "+13.08%", "+17.31%", "+17.96%", "+13.31%", "+21.70%", "+2.40%"],
  ],
  [18, 10, 10, 10, 13, 11, 10, 10, 9],
));
add(CAPTION("*March to December only. Worst 12 months for series A were November 2021 to October 2022 (−22.9%, SPY −14.6% over the same months). Over the 42 months from March 2023, NANC returned 24.75% a year (volatility 14.71%, Sharpe 1.28, CAPM alpha +0.84%, t 0.44), KRUZ (now ticker GOP) 19.31% (13.37%, 1.05, −1.33%, t −0.39), series A 21.62% (18.65%, 0.90, −2.83%, t −0.52) and SPY 22.32% (12.46%, 1.33). From outputs/tables/phase5_full_results.md."));

add(H2("A4. The size of the book"));
add(figure("outputs/figures/phase4_open_lots_capital.png", 15, "**Figure A2.** Open copied lots and capital deployed at each close. The jump in July 2026 is the Armstrong filing. Series A weights lots by dollars, so this jump changes its composition but not its scale."));

add(H2("A5. Every variant, full window and its own second half"));
add(table(
  ["Variant (one rule changed)", "A return", "A Sharpe", "CAPM alpha (t)", "Carhart alpha (t)", "Max DD", "Test-half A return", "Test-half CAPM alpha (t)"],
  [
    ["Headline", "10.81%", "0.41", "−1.48 (−0.29)", "−0.74 (−0.14)", "−32.2%", "22.95%", "1.66 (0.24)"],
    ["V1 / V2.1 exclude Tuberville", "13.32%", "0.60", "1.92 (0.51)", "−0.00 (−0.00)", "−24.6%", "26.23%", "4.72 (0.71)"],
    ["V2.2 exclude Armstrong", "10.55%", "0.40", "−1.71 (−0.33)", "−0.97 (−0.18)", "−32.2%", "22.38%", "1.14 (0.16)"],
    ["V2.3 exclude Mullin", "15.94%", "0.56", "3.25 (0.45)", "4.12 (0.55)", "−32.2%", "35.63%", "9.94 (0.81)"],
    ["V2.4 exclude Boozman", "10.95%", "0.42", "−1.34 (−0.26)", "−0.60 (−0.11)", "−32.2%", "23.25%", "1.87 (0.26)"],
    ["V2.5 exclude Whitehouse", "10.92%", "0.42", "−1.40 (−0.28)", "−0.79 (−0.15)", "−32.0%", "22.95%", "1.48 (0.22)"],
    ["V3 drop first 180 days in office", "6.41%", "0.23", "−5.41 (−1.16)", "−4.55 (−0.95)", "−33.4%", "14.80%", "−3.28 (−0.90)"],
    ["V4 drop bulk filings (50+ trades)", "8.47%", "0.31", "−3.88 (−0.61)", "−2.49 (−0.39)", "−33.5%", "19.96%", "−4.19 (−0.42)"],
    ["V5 exclude ETFs", "10.62%", "0.40", "−1.63 (−0.30)", "−1.02 (−0.18)", "−33.3%", "22.96%", "1.44 (0.20)"],
    ["V6 add spouse and child trades", "12.76%", "0.54", "0.34 (0.13)", "1.51 (0.55)", "−28.0%", "23.22%", "2.59 (0.68)"],
    ["V7 size at band lower bound", "10.24%", "0.37", "−2.07 (−0.33)", "−0.97 (−0.15)", "−36.7%", "23.39%", "1.56 (0.20)"],
    ["V8 equal dollars per trade", "11.72%", "0.53", "0.11 (0.05)", "−0.42 (−0.19)", "−26.1%", "20.67%", "1.43 (0.38)"],
    ["V9 same-day entry before 15:30 ET", "11.23%", "0.43", "−1.12 (−0.22)", "−0.38 (−0.07)", "−31.6%", "23.25%", "1.88 (0.28)"],
    ["V10 equal-weight lots", "11.92%", "0.53", "0.09 (0.04)", "−0.30 (−0.14)", "−25.7%", "20.65%", "1.90 (0.62)"],
    ["V11 3-year window (2023-09 on)", "25.80%", "1.12", "2.57 (0.43)", "2.25 (0.36)", "−20.1%", "35.83%", "10.59 (1.02)"],
    ["V12 10-year window (2016-09 on)", "15.29%", "0.62", "−1.46 (−0.32)", "−0.11 (−0.02)", "−51.1%", "5.64%", "−5.51 (−1.94)"],
    ["V13 exclude OTC names", "10.70%", "0.41", "−1.58 (−0.31)", "−0.84 (−0.16)", "−32.2%", "22.71%", "1.43 (0.21)"],
    ["V14 amendments as revised", "10.55%", "0.40", "−1.78 (−0.35)", "−0.80 (−0.15)", "−32.8%", "22.64%", "1.28 (0.19)"],
    ["V15 skipped delisted names earn SPY", "11.63%", "0.46", "−0.65 (−0.15)", "−0.25 (−0.05)", "−29.2%", "23.08%", "1.78 (0.26)"],
    ["V16 all ETFs incl. bond and T-bill", "9.43%", "0.36", "−2.65 (−0.56)", "−1.86 (−0.38)", "−32.0%", "19.95%", "−0.12 (−0.02)"],
    ["V17 empty start (no warm-up)†", "15.14%", "0.52", "2.12 (0.28)", "2.02 (0.25)", "−33.7%", "23.25%", "1.68 (0.24)"],
    ["V18 Yahoo only† (= headline)", "10.81%", "0.41", "−1.48 (−0.29)", "−0.74 (−0.14)", "−32.2%", "22.95%", "1.66 (0.24)"],
    ["V19 include preferred shares†", "10.81%", "0.41", "−1.48 (−0.29)", "−0.74 (−0.14)", "−32.2%", "22.95%", "1.66 (0.24)"],
    ["V20 CRSP-filled prices†", "not run", "", "", "", "", "", ""],
  ],
  [30, 9, 8, 13, 13, 8, 10, 13],
));
add(CAPTION("Alphas in % a year with OLS t (Figure 5 and Table 2 use Newey-West). V11's test half is 2025-03 to 2026-08; V12's is 2021-09 to 2026-08. †Registered after the design-half results were seen. V20 needed CRSP access that did not arrive before submission. From outputs/tables/variants_full_yahoo.md; every run is logged in docs/DECISIONS.md."));

add(H2("A6. Exploratory splits"));
add(P("These tables were examined but are not confirmatory, and with roughly 150 cells examined in the design half a few will reach |t| = 2 by chance. Full tables are in outputs/tables/mechanism_full_yahoo.md and committee_full_yahoo.md."));
add(table(
  ["Purchases, full window", "Events", "Copier, 21 days", "Senator, 63 days", "Trade to disclosure"],
  [
    ["Filed within 30 days", "532", "+1.32% (1.52)", "+1.40% (1.79)", "+0.30% (0.61)"],
    ["Filed after 30 days", "876", "+1.73% (5.03)", "−2.82% (−2.86)", "−3.47% (−3.64)"],
    ["Bands up to $50,000", "1,291", "+1.61% (3.70)", "−1.22% (−0.79)", "−2.17% (−1.55)"],
    ["Bands above $50,000", "117", "+1.18% (1.00)", "−1.65% (−0.98)", "−0.74% (−0.91)"],
    ["Overseen by senator's committee", "90", "+3.04% (0.80)", "+0.79% (0.36)", "+1.16% (0.55)"],
    ["Not overseen", "977", "+1.25% (2.98)", "+0.58% (0.81)", "−0.67% (−1.12)"],
    ["Republican senators", "1,365", "+1.59% (3.70)", "−1.28% (−0.91)", "−2.05% (−1.56)"],
    ["Democratic senators", "43", "+1.21% (0.85)", "−0.11% (−0.06)", "−2.15% (−1.45)"],
  ],
  [34, 10, 18, 18, 20],
));
add(CAPTION("Mean return minus SPY, t clustered by entry month in brackets. The committee split excludes ETFs and companies without an SEC industry code."));

add(H2("A7. One copied trade, traced by hand"));
add(P("Tommy Tuberville bought Johnson & Johnson (Joint account, band $1,001 to $15,000) on 30 September 2021. The PTR was received at 13:32 on 15 October 2021, so the copier bought at the close of Monday 18 October at an adjusted price of 139.2527, putting the $8,000.50 midpoint into 57.4531 units. His full sale of 16 October 2023 was disclosed on 16 November 2023, and the copier sold at the close of 17 November at 137.5493, a return of −1.22% over 525 trading days. Two more traced trades, including a partial sale, are in outputs/phase4_worked_examples.md."));

add(H2("A8. What was fixed when"));
add(BULLET("**27 September 2026.** Data source, scope, sizing, entry and exit rules, benchmarks and the out-of-sample split locked (DECISIONS.md D01 to D20, A01 to A07). Variants V1 to V12 registered at commit 622a455, before any price, return or performance number had been computed."));
add(BULLET("**28 to 30 September 2026.** V13 to V16 registered before any portfolio return existed. Two scope changes were made after seeing design-half results and are disclosed as such, the 12-month warm-up (L2, with the old rule kept as V17) and excluding preferred shares (N2, V19). V18 (Yahoo-only prices, now identical to the headline) was registered on 29 September and V20 (CRSP-filled prices) on 6 October, both after design-half results existed."));
add(BULLET("**30 September to 2 October 2026.** Tests H0 to H4 and their predictions registered (commit eac5bf6), then Holm adjustment, detectable-effect reporting and the bulk-filing sensitivity added, all before any second-half number existed."));
add(BULLET("**6 October 2026.** Rules frozen at commit 348318447daa, then the second half unlocked in a separate commit. No rule has changed since, and the one post-unlock correction changed a test file only."));

add(H2("A9. Reproducing every number"));
add(P("With Python 3.11, from the repository folder, run pip install -r requirements.txt, then python run_all.py --skip-scrape (about 3 minutes, offline, rebuilds every table in outputs/ and the three pipeline figures) and python run_variants.py (about 8 minutes, the variants table). The report figures are rebuilt with python report/build_figures.py and this document with node report/build_report.js. No file path needs editing. We reran the full pipeline from a fresh environment on 13 October 2026; every committed output was reproduced and all 183 tests pass."));

add(H2("A10. How much data the tests would need"));
add(P("The Carhart alpha's standard error over 60 months is about 5.3% a year (half of the 10.56% detectable at t = 2), which implies a residual volatility of about 5.3% × √5 ≈ 11.8% a year. Using t ≈ IR × √years with IR = α / σε, an alpha of 3% a year has IR ≈ 3 / 11.8 = 0.254 and needs (2 / 0.254)² ≈ 62 years to reach t = 2, and even a 5% alpha needs about 22 years. Short samples cannot settle this question in either direction."));

// =====================================================================================
const doc = new Document({
  creator: "CA01 study group",
  title: "Copying the US Senate",
  styles: {
    default: { document: { run: { font: FONT, size: BODY } } },
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] },
      { reference: "nums", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 300 } } } }] },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134, footer: 567 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: SMALL, color: "888888" })] })] }) },
    children: body,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(ROOT, "report", "Copying_the_Senate_report.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", out);
});
