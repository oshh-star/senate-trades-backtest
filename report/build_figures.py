"""Figures for Report V3, in London Business School navy and red, with annotations.

Reads only committed pipeline outputs (data/processed, outputs/tables) and report/diagnostics.py's files, so every
figure can be rebuilt. Run from the repo root, after python run_all.py --skip-scrape and python report/diagnostics.py:

    python report/build_figures.py

Writes report/figures/*.png.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"
OUT = ROOT / "report" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# LBS palette: navy and red, plus a mid blue and a gold for secondary series
NAVY = "#001E62"     # series A, the headline
RED = "#C8102E"      # SPY
SKY = "#4A7EBB"      # series B
GOLD = "#A87A0F"     # Senate universe
INK = "#1F2A37"
MUTED = "#6B7480"
GRID = "#E3E7EC"
PALE = "#D6E2F0"     # light blue, for bands
FREEZE = pd.Timestamp("2024-03-01")
ARMSTRONG = pd.Timestamp("2026-07-21")

plt.rcParams.update({
    "font.family": "Carlito", "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "axes.titlecolor": INK, "axes.labelcolor": INK, "axes.edgecolor": "#A9B2BC",
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.6, "xtick.color": MUTED, "ytick.color": MUTED, "legend.frameon": False,
    "lines.linewidth": 1.6, "savefig.dpi": 240, "savefig.bbox": "tight", "figure.facecolor": "white",
})


def save(fig, name, title=None, subtitle=None, source=None):
    """Market-insights style: a takeaway headline, a units-and-dates subtitle, a source line."""
    if title:
        fig.text(0.0, 1.0 + 0.30 / fig.get_figheight(), title, ha="left", va="bottom", fontsize=12, fontweight="bold",
                 color=NAVY, transform=fig.transFigure)
    if subtitle:
        fig.text(0.0, 1.0 + 0.06 / fig.get_figheight(), subtitle, ha="left", va="bottom", fontsize=8.6, color=MUTED,
                 transform=fig.transFigure)
    if source:
        fig.text(0.0, -0.02 - 0.05 / fig.get_figheight(), source, ha="left", va="top", fontsize=6.8, color=MUTED, transform=fig.transFigure)
    fig.savefig(OUT / name)
    plt.close(fig)


def daily():
    d = pd.read_csv(PROC / "daily_returns.csv", parse_dates=["date"])
    return d[(d.date >= "2021-09-01") & (d.date <= "2026-08-31")].reset_index(drop=True)


def monthly():
    m = pd.read_csv(PROC / "monthly_returns.csv", parse_dates=["month"])
    return m[(m.month >= "2021-09-01") & (m.month <= "2026-08-31")].reset_index(drop=True)


def mark_halves(ax, ytext):
    ax.axvline(FREEZE, color=MUTED, lw=0.9, ls=(0, (4, 3)))
    ax.text(FREEZE - pd.Timedelta(days=20), ytext, "design half", ha="right", va="top", fontsize=7.5, color=MUTED)
    ax.text(FREEZE + pd.Timedelta(days=20), ytext, "test half (rules frozen)", ha="left", va="top", fontsize=7.5, color=MUTED)


def fig_flow():
    fig, ax = plt.subplots(figsize=(7.2, 2.1))
    ax.set_xlim(0, 100); ax.set_ylim(0, 34); ax.axis("off")
    boxes = [
        (10, "1  Senator trades", "transaction date\nsenator's clock starts", INK, "#EEF2F6"),
        (30, "2  PTR received", "filed on Senate eFD\npublic from this time", INK, "#EEF2F6"),
        (50, "3  Copier buys", "close, first trading day\nafter receipt; size =\nband midpoint", "white", NAVY),
        (70, "4  Sale disclosed", "same senator and ticker\nmatched first in,\nfirst out; no shorting", INK, "#EEF2F6"),
        (90, "5  Copier sells", "close, first trading day\nafter receipt; open lots\nmarked 31 Aug 2026", "white", NAVY),
    ]
    w, h, yb = 17.6, 17, 4
    for x, title, body, colour, fc in boxes:
        ax.add_patch(FancyBboxPatch((x - w / 2, yb), w, h, boxstyle="round,pad=0.3,rounding_size=1.2", fc=fc, ec="none"))
        ax.text(x, yb + h - 2.0, title, ha="center", va="top", fontsize=8.4, color=colour, fontweight="bold")
        ax.text(x, yb + h - 6.4, body, ha="center", va="top", fontsize=7.2, color=colour if fc == NAVY else "#3B4652",
                linespacing=1.25)
    for x in [10, 30, 50, 70]:
        ax.annotate("", xy=(x + 20 - w / 2 - 0.5, yb + h / 2), xytext=(x + w / 2 + 0.5, yb + h / 2),
                    arrowprops=dict(arrowstyle="-|>", color="#A9B2BC", lw=1))
    ax.annotate("", xy=(30, 26.5), xytext=(10, 26.5), arrowprops=dict(arrowstyle="<->", color=RED, lw=1))
    ax.text(20, 27.6, "disclosure lag: median 33 days", ha="center", va="bottom", fontsize=8, color=RED)
    ax.annotate("", xy=(90, 26.5), xytext=(50, 26.5), arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1))
    ax.text(70, 27.6, "copied lot held until the senator sells", ha="center", va="bottom", fontsize=8, color=NAVY)
    save(fig, "fig1_flow.png", "How a copied trade works", "Each disclosed purchase opens a lot; the same senator's disclosed sale closes it")


def fig_cumulative():
    d = daily()
    series = [("r_A", "Series A, copying the Senate", NAVY, "-", 2.0), ("r_SPY", "SPY", RED, "-", 1.5),
              ("r_RM_A", "SPY at series A's volatility", RED, (0, (4, 2)), 1.3),
              ("r_EW", "Senate universe, equal weight", GOLD, "-", 1.2)]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ends = []
    for col, lab, c, ls, lw in series:
        v = np.concatenate([[1.0], (1 + d[col]).cumprod().to_numpy()])
        dates = pd.concat([pd.Series([pd.Timestamp("2021-08-31")]), d.date])
        ax.plot(dates, v, color=c, ls=ls, lw=lw, label=lab, zorder=3 if col == "r_A" else 2)
        ends.append((v[-1], c, lab))
    # end labels, nudged apart
    ends.sort()
    last = -1
    for v, c, lab in ends:
        y = max(v, last + 0.07)
        ax.text(pd.Timestamp("2026-09-10"), y, f"{v:.2f}", color=c, fontsize=8, va="center", fontweight="bold")
        last = y
    ax.axhline(1, color="#A9B2BC", lw=0.7)
    mark_halves(ax, 2.18)
    _v = (1 + d.set_index("date")["r_A"]).cumprod()
    ax.annotate("2022 bear market: series A\n−32% peak to trough, 14 Jul 2022", xy=(pd.Timestamp("2022-07-14"), float(_v.loc["2022-07-14"])),
                xytext=(pd.Timestamp("2022-10-20"), 0.63), fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    ax.annotate("Armstrong filing\n(654 purchases, 21 Jul 2026)", xy=(ARMSTRONG, 1.95), xytext=(pd.Timestamp("2025-03-01"), 2.10),
                fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    ax.set_ylim(0.55, 2.25)
    ax.set_ylabel("Value of $1 invested 31 Aug 2021 (USD, total return)")
    ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlim(pd.Timestamp("2021-08-15"), pd.Timestamp("2026-11-15"))
    ax.legend(loc="upper left", fontsize=7.8, ncol=1)
    save(fig, "fig2_cumulative.png", "Copying the Senate beat SPY, but not SPY at the same risk", "Growth of $1, USD total return, 31 August 2021 to 31 August 2026, daily", "Source: Senate eFD, Yahoo Finance, Bloomberg, Kenneth French Data Library; group calculations. Series A uses Bloomberg prices for 8 stocks Yahoo lacks (correction C1).")


def drawdown(r):
    v = np.concatenate([[1.0], (1 + r).cumprod().to_numpy()])
    return v / np.maximum.accumulate(v) - 1


def fig_drawdown():
    d = daily()
    dates = pd.concat([pd.Series([pd.Timestamp("2021-08-31")]), d.date]).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(7.2, 2.6))
    for col, lab, c, lw in [("r_SPY", "SPY", RED, 1.2), ("r_A", "Series A", NAVY, 1.6)]:
        dd = drawdown(d[col]) * 100
        ax.fill_between(dates, dd, 0, color=c, alpha=0.10 if col == "r_A" else 0.07, lw=0)
        ax.plot(dates, dd, color=c, lw=lw, label=lab)
        i = int(np.argmin(dd))
        ax.plot(dates[i], dd[i], "o", color=c, ms=4.5, zorder=4)
    ax.annotate("Series A −32.2%\ntrough 14 Jul 2022, recovered 1 Mar 2024", xy=(pd.Timestamp("2022-07-14"), -32.2),
                xytext=(pd.Timestamp("2024-08-01"), -33.5), fontsize=7.5, color=NAVY,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.7))
    ax.annotate("SPY −24.5%\ntrough 12 Oct 2022, recovered 13 Dec 2023", xy=(pd.Timestamp("2022-10-12"), -24.5),
                xytext=(pd.Timestamp("2024-08-01"), -26.5), fontsize=7.5, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.7))
    mark_halves(ax, 3.5)
    ax.set_ylim(-38, 5)
    ax.set_ylabel("Fall from previous peak (%)")
    ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="lower left", fontsize=7.8)
    save(fig, "fig3_drawdown.png", "The copied book fell further and stayed under water longer", "Fall from previous peak, %, daily value index", "Source: Senate eFD, Yahoo Finance, Bloomberg, Kenneth French Data Library; group calculations.")


def fig_calendar():
    m = monthly()
    m["year"] = m.month.dt.year
    cols = [("r_A", "Series A", NAVY), ("r_SPY", "SPY", RED), ("r_RM_A", "SPY at series A's volatility", "#E4A1AB")]
    yr = m.groupby("year")[[c for c, _, _ in cols]].apply(lambda g: (1 + g).prod() - 1) * 100
    labels = ["2021\nSep–Dec", "2022", "2023", "2024", "2025", "2026\nJan–Aug"]
    x = np.arange(len(yr)); w = 0.26
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    for k, (c, lab, colour) in enumerate(cols):
        ax.bar(x + (k - 1) * w, yr[c], w - 0.03, color=colour, label=lab, zorder=3)
    for i, v in enumerate(yr["r_A"]):
        ax.text(x[i] - w, v + (1.2 if v >= 0 else -1.2), f"{v:+.1f}", ha="center", va="bottom" if v >= 0 else "top",
                fontsize=7.2, color=NAVY, fontweight="bold")
    ax.axhline(0, color="#A9B2BC", lw=0.8)
    ax.axvspan(2.5, 5.5, color=PALE, alpha=0.45, zorder=0, lw=0)
    ax.text(5.45, 38, "test half from Mar 2024", ha="right", fontsize=7.5, color=MUTED)
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel("Calendar-year return (%)")
    ax.set_ylim(-32, 42)
    ax.legend(loc="upper left", fontsize=7.8, ncol=3)
    ax.grid(axis="x", visible=False)
    save(fig, "fig4_calendar.png", "Two strong years carry the five-year result", "Calendar-year total return, %, USD; risk-matched SPY uses k = 1.48", "Source: Senate eFD, Yahoo Finance, Bloomberg, Kenneth French Data Library; group calculations.")
    return yr


def fig_event_study():
    es = pd.read_csv(TABLES / "phase5_event_study_full.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), sharey=True)
    for ax, side, title in zip(axes, ["purchase", "sale"], ["Purchases (1,392 trades)", "Sales (971 trades)"]):
        d = es[es.side == side]
        n = d[d.version.str.startswith("senator") & (d.horizon_days == 5)].n.iloc[0]
        ax.set_title(title.split(" (")[0] + f" ({n:,} trades)")
        for version, colour, label in [("senator (from transaction date)", RED, "Senator, from the trade"),
                                       ("copier (from entry date)", NAVY, "Copier, from disclosure")]:
            g = d[d.version == version].sort_values("horizon_days")
            h, mu = g.horizon_days.to_numpy(), g["mean"].to_numpy() * 100
            se = np.abs(mu / g.t_cluster.to_numpy())
            ax.fill_between(h, mu - 1.96 * se, mu + 1.96 * se, color=colour, alpha=0.11, lw=0)
            ax.plot(h, mu, "-o", color=colour, ms=3.8, label=label)
        ax.axhline(0, color="#A9B2BC", lw=0.8)
        ax.set_xscale("log"); ax.set_xticks([5, 21, 63, 126, 252]); ax.set_xticklabels(["5", "21", "63", "126", "252"])
        ax.minorticks_off(); ax.set_xlabel("Trading days after the start date")
    pre = es[(es.side == "purchase") & (es.horizon_days == 0)]["mean"].iloc[0] * 100
    axes[0].annotate("senator's purchases trail SPY\nby 2.4% after 21 days", xy=(21, -2.44), xytext=(28, -6.4),
                     fontsize=7.5, color=RED, arrowprops=dict(arrowstyle="-", color=RED, lw=0.7))
    axes[0].set_ylabel("Mean return minus SPY (%)")
    axes[0].legend(loc="upper left", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig5_event_study.png", "Senators' purchases lag the market before anyone can copy them", "Mean return minus SPY after the trade (senator) and after disclosure (copier), %, 95% bands clustered by month", "Source: Senate eFD, Yahoo Finance, Bloomberg, Kenneth French Data Library; group calculations. Exploratory: not a registered test.")


def fig_registered():
    c = pd.read_csv(TABLES / "confirmatory_oos.csv").set_index("id")
    # ex-bulk values from outputs/tables/confirmatory_oos.md, "Sensitivity: without bulk filings" (estimate, t)
    exbulk = {"H1p": (-0.0011, -0.18), "H1s": (0.0068, 1.22), "H2": (0.0112, 0.81), "H4": (0.0172, 0.41)}
    rows = [("H1p", "H1 purchases, trade to disclosure"), ("H1s", "H1 sales, trade to disclosure"),
            ("H2", "H2 copier purchases, 21 days"), ("H3", "H3 committee sales minus other, 63 days"),
            ("H4", "H4 small minus large purchases, 126 days")]
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    for i, (k, lab) in enumerate(rows):
        y = len(rows) - 1 - i
        est, se = c.loc[k, "estimate"] * 100, c.loc[k, "se"] * 100
        sig = c.loc[k, "p_holm"] < 0.05
        ax.plot([est - 1.96 * se, est + 1.96 * se], [y + 0.12] * 2, color=NAVY, lw=2.2, alpha=0.35, solid_capstyle="round")
        ax.plot(est, y + 0.12, "o", color=NAVY, ms=6, mfc=NAVY if sig else "white", mew=1.4)
        if k in exbulk:
            e, t = exbulk[k]; e *= 100; s = abs(e / t)
            ax.plot([e - 1.96 * s, e + 1.96 * s], [y - 0.14] * 2, color=GOLD, lw=2.2, alpha=0.45, solid_capstyle="round")
            ax.plot(e, y - 0.14, "D", color=GOLD, ms=5)
        ax.text(1.01, (y + 0.5) / len(rows), f"Holm p {c.loc[k, 'p_holm']:.3f}".replace("p 1.000", "p 1"), fontsize=7.4, va="center",
                transform=ax.transAxes,
                color=INK if sig else MUTED, fontweight="bold" if sig else "normal")
    ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[1] for r in rows][::-1], fontsize=7.8)
    ax.set_xlim(-8, 20); ax.set_ylim(-0.5, len(rows) - 0.5); ax.grid(axis="y", visible=False)
    ax.set_xlabel("Estimate, % (bar = 95% interval; filled circle = significant after Holm adjustment)")
    ax.plot([], [], "o", color=NAVY, label="All trades (registered test)")
    ax.plot([], [], "D", color=GOLD, label="Without bulk filings (pre-registered check)")
    ax.legend(loc="upper right", fontsize=7.4)
    fig.subplots_adjust(left=0.36, right=0.88)
    save(fig, "fig6_registered_tests.png", "Both significant results disappear without bulk filings", "Pre-registered tests on the test half (Mar 2024 to Aug 2026), estimate and 95% interval, %", "Source: Senate eFD, Yahoo Finance, Bloomberg, Kenneth French Data Library; group calculations. Bulk filings are reports with 50 or more trades.")


def fig_variants():
    v = pd.read_csv(TABLES / "variants_full_bloomberg.csv")
    v = v[(v.status == "run") & (v.id != "V2.1")].copy()
    short = {"H": "Headline", "V1": "No Tuberville", "V2.2": "No Armstrong", "V2.3": "No Mullin",
             "V2.4": "No Boozman", "V2.5": "No Whitehouse", "V3": "No first 180 days in office", "V4": "No bulk filings",
             "V5": "No ETFs", "V6": "Add spouse and child trades", "V7": "Size at band lower bound",
             "V8": "Equal dollars per trade", "V9": "Same-day entry before 15:30", "V10": "Equal-weight lots",
             "V11": "3-year window*", "V12": "10-year window*", "V13": "No OTC names", "V14": "Amendments as revised",
             "V15": "Unpriced names earn SPY", "V16": "All ETFs incl. bond, T-bill", "V17": "Empty start, no warm-up",
             "V18": "Yahoo prices only (old headline)", "V19": "Add preferred shares",
             "V21": "Sell when senator leaves office‡"}
    v["label"] = v.id.map(short)
    v["alpha"] = v.A_capm_alpha * 100
    v["se"] = np.abs(v.alpha / v.A_capm_t_nw)
    v = v.iloc[::-1].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    yy = np.arange(len(v))
    for y, (_, r) in zip(yy, v.iterrows()):
        head = r.id == "H"
        ax.plot([r.alpha - 1.96 * r.se, r.alpha + 1.96 * r.se], [y, y], color=NAVY if head else "#A7BCD9",
                lw=3, alpha=0.9 if head else 0.55, solid_capstyle="round")
        ax.plot(r.alpha, y, "o", color=NAVY if head else INK, ms=5 if head else 4)
        ax.text(1.01, (y + 0.5) / len(v), f"{r.A_ann_return * 100:.1f}%", fontsize=7.2, va="center", transform=ax.transAxes,
                color=NAVY if head else MUTED,
                fontweight="bold" if head else "normal")
    ax.text(1.01, 1.0, "return\na year", fontsize=7, va="bottom", color=MUTED, transform=ax.transAxes)
    ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_yticks(yy); ax.set_yticklabels(v.label, fontsize=7.6)
    for t, lab in zip(ax.get_yticklabels(), v.id):
        if lab == "H":
            t.set_color(NAVY); t.set_fontweight("bold")
    ax.set_xlim(-16, 20); ax.set_ylim(-0.5, len(v) - 0.5); ax.grid(axis="y", visible=False)
    ax.set_xlabel("Series A CAPM alpha, % a year (bar = 95% interval, Newey-West). No interval excludes zero.")
    fig.subplots_adjust(left=0.27, right=0.92)
    save(fig, "fig7_variants.png", "No specification produces a reliable alpha", "Series A CAPM alpha by variant, % a year, 95% interval (Newey-West); one rule changed at a time", "Source: Senate eFD, Yahoo Finance, Bloomberg, Kenneth French Data Library; group calculations. *V11 and V12 cover 3 and 10 years. ‡Exploratory, added after the test half was opened.")


def fig_rolling():
    r = pd.read_csv(ROOT / "report" / "rolling_alpha_24m.csv", parse_dates=["month"])
    a, se = r.alpha * 100, r.se * 100
    fig, ax = plt.subplots(figsize=(7.2, 2.5))
    ax.fill_between(r.month, a - 1.96 * se, a + 1.96 * se, color=NAVY, alpha=0.12, lw=0, label="95% interval")
    ax.plot(r.month, a, color=NAVY, lw=1.8, label="CAPM alpha, trailing 24 months")
    ax.axhline(0, color=MUTED, lw=0.8)
    neg = (a + 1.96 * se) < 0
    lo = a.idxmin()
    ax.annotate("windows ending Dec 2024 to Feb 2025:\nalpha about −16% a year, interval below zero", xy=(r.month[lo], a[lo]),
                xytext=(pd.Timestamp("2025-04-01"), -27), fontsize=7.5, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.7))
    ax.plot(r.month[neg], a[neg], "o", color=RED, ms=4, zorder=4)
    ax.annotate(f"latest {a.iloc[-1]:+.1f}%", xy=(r.month.iloc[-1], a.iloc[-1]), xytext=(-4, 10), textcoords="offset points",
                ha="right", fontsize=7.5, color=NAVY)
    ax.set_ylabel("% a year")
    ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="upper left", fontsize=7.5, ncol=2)
    save(fig, "fig8_rolling_alpha.png", "Alpha swings with the sample and is never reliably positive", "CAPM alpha of Series A over the trailing 24 months, % a year, with 95% interval", "Source: Senate eFD, Yahoo Finance, Bloomberg, Kenneth French Data Library; group calculations. Overlapping windows: neighbouring points share 23 of 24 months.")


def fig_concentration():
    l = pd.read_csv(PROC / "lots.csv")
    g = l.groupby("senator").agg(d=("entry_dollars", "sum"), p=("pnl", "sum"))
    g = g.sort_values("d", ascending=False)
    top = g.head(5).copy()
    other = g.iloc[5:].sum()
    top.loc[f"{len(g) - 5} others"] = other
    top["d%"] = top.d / g.d.sum() * 100; top["p%"] = top.p / g.p.sum() * 100
    top = top.iloc[::-1]
    yy = np.arange(len(top))
    fig, ax = plt.subplots(figsize=(7.2, 2.5))
    ax.barh(yy + 0.19, top["d%"], 0.36, color=NAVY, label="Share of dollars copied", zorder=3)
    ax.barh(yy - 0.19, top["p%"], 0.36, color=GOLD, label="Share of profit", zorder=3)
    for y, (dv, pv) in zip(yy, zip(top["d%"], top["p%"])):
        ax.text(dv + 0.6, y + 0.19, f"{dv:.0f}%", va="center", fontsize=7.2, color=NAVY)
        ax.text(max(pv, 0) + 0.6, y - 0.19, f"{pv:.0f}%", va="center", fontsize=7.2, color=GOLD)
    ax.set_yticks(yy); ax.set_yticklabels(top.index)
    ax.set_xlabel("% of total, every copied lot including the warm-up (data/processed/lots.csv)")
    ax.legend(loc="lower right", fontsize=7.6); ax.grid(axis="y", visible=False)
    save(fig, "figA1_concentration.png", "Two senators made three-quarters of the profit", "Share of dollars copied and of lot profit by senator, %, every copied lot including the warm-up", "Source: data/processed/lots.csv; group calculations.")
    return top


def fig_book():
    b = pd.read_csv(PROC / "daily_book.csv", parse_dates=["date"])
    b = b[(b.date >= "2021-09-01") & (b.date <= "2026-08-31")]
    fig, ax = plt.subplots(figsize=(7.2, 2.4))
    ax.fill_between(b.date, b.capital_deployed / 1e6, color=NAVY, alpha=0.18, lw=0)
    ax.plot(b.date, b.capital_deployed / 1e6, color=NAVY, lw=1.5)
    ax.set_ylabel("Capital deployed ($m)")
    mx = b.capital_deployed.max() / 1e6
    ax.annotate(f"Armstrong filing adds his 654-stock basket;\npeak ${mx:.1f}m", xy=(ARMSTRONG, mx * 0.95),
                xytext=(pd.Timestamp("2024-06-01"), mx * 0.85), fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    mark_halves(ax, mx * 1.05)
    ax.set_ylim(0, mx * 1.12)
    ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    save(fig, "figA2_capital.png", "One filing raised the capital deployed by half in a day", "Capital in copied positions at each close, $ million", "Source: data/processed/daily_book.csv.")


def fig_sources():
    # before and after values from docs/DECISIONS.md, post-unlock correction C1 (Yahoo only = V18)
    rows = [("Return a year", 10.81, 13.41), ("Return over SPY at same risk", -4.48, -2.58),
            ("CAPM alpha", -1.48, 1.07), ("Carhart alpha", -0.74, 2.26)]
    yy = np.arange(len(rows))[::-1]
    fig, ax = plt.subplots(figsize=(7.2, 2.0))
    for y, (lab, a, b) in zip(yy, rows):
        ax.plot([a, b], [y, y], color="#A9B2BC", lw=1.4, zorder=1)
        ax.plot(a, y, "o", color=MUTED, ms=6, zorder=2); ax.plot(b, y, "o", color=NAVY, ms=6, zorder=2)
        ax.text(a, y + 0.25, f"{a:+.2f}", ha="center", fontsize=7.3, color=MUTED)
        ax.text(b, y + 0.25, f"{b:+.2f}", ha="center", fontsize=7.3, color=NAVY, fontweight="bold")
    ax.set_yticks(yy); ax.set_yticklabels([r[0] for r in rows]); ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_xlabel("% a year, full window")
    ax.plot([], [], "o", color=MUTED, label="Yahoo prices only (8 stocks skipped)")
    ax.plot([], [], "o", color=NAVY, label="With Bloomberg prices for them (headline)")
    ax.legend(loc="lower right", fontsize=7.4); ax.grid(axis="y", visible=False); ax.set_ylim(-0.6, 3.7)
    save(fig, "figA3_price_sources.png", "Real prices for eight missing stocks raise the return, not the verdict", "Full-window results with Yahoo prices only and with Bloomberg prices for the missing stocks, % a year", "Source: docs/DECISIONS.md, correction C1; Yahoo-only is variant V18.")


if __name__ == "__main__":
    fig_flow(); fig_cumulative(); fig_drawdown(); yr = fig_calendar(); fig_event_study(); fig_registered()
    fig_variants(); fig_rolling(); top = fig_concentration(); fig_book(); fig_sources()
    print(yr.round(2)); print(top.round(1))
    print("figures ->", OUT)
