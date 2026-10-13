"""Figures for the written report (Phase 7).

Reads only files that `python run_all.py --skip-scrape` and `python run_variants.py` write, so every
figure can be rebuilt from the repository. Run from the repo root:

    python report/build_figures.py

Writes report/figures/fig*.png.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
OUT = ROOT / "report" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "#2671d9"
ORANGE = "#ee6a2f"
GREY = "#6b6b6b"
LIGHT = "#d9d9d9"
INK = "#222222"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#9a9a9a",
    "axes.labelcolor": INK,
    "xtick.color": "#555555",
    "ytick.color": "#555555",
    "axes.grid": True,
    "grid.color": "#e6e6e6",
    "grid.linewidth": 0.6,
    "savefig.dpi": 220,
    "savefig.bbox": "tight",
})


def fig_timeline():
    """How one copied trade works: transaction, disclosure, entry, exit."""
    fig, ax = plt.subplots(figsize=(7.2, 2.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 34)
    ax.axis("off")

    boxes = [
        (10, "1. Senator trades", "transaction date\n(senator measure\nstarts here)", INK, "#f2f2f2"),
        (30, "2. PTR received", "filed on Senate eFD;\npublic from this date", INK, "#f2f2f2"),
        (50, "3. Copier buys", "close of first trading\nday after receipt;\nsize = range midpoint", BLUE, "#e8f0fc"),
        (70, "4. Sale disclosed", "same senator, same\nticker, matched FIFO;\nno shorting", INK, "#f2f2f2"),
        (90, "5. Copier sells", "close of first trading\nday after receipt;\nrest marked 2026-08-31", BLUE, "#e8f0fc"),
    ]
    w, h, yb = 17.5, 17, 4
    for x, title, body, colour, fc in boxes:
        ax.add_patch(FancyBboxPatch((x - w / 2, yb), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                                    fc=fc, ec="none"))
        ax.text(x, yb + h - 2.2, title, ha="center", va="top", fontsize=7.4, color=colour, fontweight="bold")
        ax.text(x, yb + h - 6.6, body, ha="center", va="top", fontsize=6.3, color="#444444", linespacing=1.25)
    for x in [10, 30, 50, 70]:
        ax.annotate("", xy=(x + 20 - w / 2 - 0.6, yb + h / 2), xytext=(x + w / 2 + 0.6, yb + h / 2),
                    arrowprops=dict(arrowstyle="-|>", color="#9a9a9a", lw=1))
    ax.annotate("", xy=(30, 26.5), xytext=(10, 26.5), arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1))
    ax.text(20, 27.6, "disclosure lag, median 33 days", ha="center", va="bottom", fontsize=7.2, color=ORANGE)
    ax.annotate("", xy=(90, 26.5), xytext=(50, 26.5), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1))
    ax.text(70, 27.6, "copied lot held (series A weights lots by dollars; idle cash earns RF)",
            ha="center", va="bottom", fontsize=7.2, color=BLUE)
    fig.savefig(OUT / "fig1_timeline.png")
    plt.close(fig)


def fig_event_study():
    """Senator against copier, SPY-adjusted, by horizon, with 95% bands (clustered by entry month)."""
    es = pd.read_csv(TABLES / "phase5_event_study_full.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), sharey=True)
    for ax, side, title in zip(axes, ["purchase", "sale"], ["Purchases (N = 1,372 at 5 days)", "Sales (N = 901 at 5 days)"]):
        d = es[es.side == side]
        for version, colour, label in [
            ("senator (from transaction date)", ORANGE, "Senator, from transaction date"),
            ("copier (from entry date)", BLUE, "Copier, from first day after disclosure"),
        ]:
            g = d[d.version == version].sort_values("horizon_days")
            h = g.horizon_days.to_numpy()
            m = g["mean"].to_numpy() * 100
            se = np.abs(m / g.t_cluster.to_numpy())
            ax.fill_between(h, m - 1.96 * se, m + 1.96 * se, color=colour, alpha=0.13, lw=0)
            ax.plot(h, m, "-o", color=colour, ms=3.5, lw=1.6, label=label)
        ax.axhline(0, color="#9a9a9a", lw=0.8)
        ax.set_xscale("log")
        ax.set_xticks([5, 21, 63, 126, 252])
        ax.set_xticklabels(["5", "21", "63", "126", "252"])
        ax.minorticks_off()
        ax.set_title(title, fontsize=8.8, loc="left", color=INK)
        ax.set_xlabel("Trading days after the start date")
    axes[0].set_ylabel("Mean return minus SPY (%)")
    axes[0].legend(frameon=False, fontsize=7.4, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "fig3_event_study.png")
    plt.close(fig)


def fig_variants():
    """CAPM alpha of series A for every pre-registered variant, full window, 95% band (Newey-West)."""
    v = pd.read_csv(TABLES / "variants_full_yahoo.csv")
    v = v[(v.status == "run") & (v.id != "V2.1")].copy()  # V2.1 is V1 (Tuberville) by construction
    short = {
        "H": "Headline", "V1": "V1 no Tuberville", "V2.2": "V2.2 no Armstrong", "V2.3": "V2.3 no Mullin",
        "V2.4": "V2.4 no Boozman", "V2.5": "V2.5 no Whitehouse", "V3": "V3 no first 180 days",
        "V4": "V4 no bulk filings", "V5": "V5 no ETFs", "V6": "V6 add spouse/child", "V7": "V7 lower-bound size",
        "V8": "V8 equal dollars", "V9": "V9 same-day entry", "V10": "V10 equal weight", "V11": "V11 3-year window*",
        "V12": "V12 10-year window*", "V13": "V13 no OTC", "V14": "V14 as revised", "V15": "V15 SPY fill (ledger)",
        "V16": "V16 all ETFs", "V17": "V17 empty start", "V18": "V18 Yahoo only (= headline)",
        "V19": "V19 add preferreds (= headline)",
    }
    v["label"] = v.id.map(short)
    v["alpha"] = v.A_capm_alpha * 100
    v["se"] = np.abs(v.alpha / v.A_capm_t_nw)
    v = v.iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    yy = np.arange(len(v))
    colours = [BLUE if i == "H" else INK for i in v.id]
    ax.errorbar(v.alpha, yy, xerr=1.96 * v.se, fmt="none", ecolor=LIGHT, elinewidth=3, capsize=0)
    ax.scatter(v.alpha, yy, color=colours, s=18, zorder=3)
    ax.axvline(0, color=GREY, lw=0.8)
    ax.set_yticks(yy)
    ax.set_yticklabels(v.label, fontsize=7.6)
    for t, lab in zip(ax.get_yticklabels(), v.id):
        if lab == "H":
            t.set_color(BLUE)
            t.set_fontweight("bold")
    ax.set_xlabel("Series A CAPM alpha, % a year (bar = 95% interval, Newey-West)")
    ax.grid(axis="y", visible=False)
    fig.savefig(OUT / "fig4_variants.png")
    plt.close(fig)


def fig_concentration():
    """Share of in-scope trades and dollars by senator (appendix)."""
    rows = [
        ("Tuberville (R)", 31.3, 32.4), ("Armstrong (R)", 30.0, 28.1), ("Mullin (R)", 13.8, 14.0),
        ("Boozman (R)", 10.7, 2.6), ("Whitehouse (D)", 3.5, 1.9), ("26 others", 10.8, 21.0),
    ]
    labels = [r[0] for r in rows][::-1]
    trades = [r[1] for r in rows][::-1]
    dollars = [r[2] for r in rows][::-1]
    yy = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(7.2, 2.4))
    ax.barh(yy + 0.19, trades, 0.36, color=BLUE, label="Share of trades")
    ax.barh(yy - 0.19, dollars, 0.36, color=ORANGE, label="Share of dollars (range midpoints)")
    ax.set_yticks(yy)
    ax.set_yticklabels(labels)
    ax.set_xlabel("% of 2,340 in-scope trades ($87.7m at midpoints), 2021-09 to 2026-08")
    ax.legend(frameon=False, fontsize=7.6, loc="lower right")
    ax.grid(axis="y", visible=False)
    fig.savefig(OUT / "figA1_concentration.png")
    plt.close(fig)


if __name__ == "__main__":
    fig_timeline()
    fig_event_study()
    fig_variants()
    fig_concentration()
    print("figures ->", OUT)
