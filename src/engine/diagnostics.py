"""Phase 4 diagnostics: the Phase 4 section of outputs/data_quality.md, the open-lots / capital chart,
the three worked examples (outputs/phase4_worked_examples.md) and the in-sample return and volatility
of series A, series B and SPY over identical dates. No Sharpe ratios, alphas or variants (Phases 5-6)."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.quality import write_section

FIG = Path("outputs/figures/phase4_open_lots_capital.png")
EXAMPLES = Path("outputs/phase4_worked_examples.md")
REPAIR_LOG = Path("data/interim/price_repairs_log.csv")
# chart tokens (dataviz reference palette: series slot 1, light surface, ink, hairline grid)
SERIES, SURFACE, INK, INK2, MUTED, GRID = "#2a78d6", "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"


def md(df: pd.DataFrame, floatfmt=",.2f") -> str:
    return df.to_markdown(index=False, floatfmt=floatfmt) if len(df) else "_None._"


def ann(r: np.ndarray) -> tuple[float, float]:
    r = np.asarray(r, dtype=float)
    return float(np.prod(1 + r) ** (252 / len(r)) - 1), float(np.std(r, ddof=1) * np.sqrt(252))


def chart(daily: pd.DataFrame, label: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    d = pd.to_datetime(daily["date"])
    fig, axes = plt.subplots(2, 1, figsize=(9, 5.6), sharex=True, facecolor=SURFACE)
    for ax, col, title, scale in ((axes[0], "open_lots", "Open copied lots at each close", 1),
                                  (axes[1], "capital_deployed", "Capital deployed at each close ($ millions)", 1e6)):
        ax.set_facecolor(SURFACE)
        ax.plot(d, daily[col] / scale, color=SERIES, linewidth=2)
        ax.set_title(title, loc="left", color=INK, fontsize=11)
        ax.grid(axis="y", color=GRID, linewidth=0.6)
        ax.tick_params(colors=MUTED, labelsize=9)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.set_ylim(bottom=0)
        i = int(daily[col].idxmax())
        ax.annotate(f"max {daily[col].iat[i] / scale:,.{0 if scale == 1 else 1}f}", (d.iat[i], daily[col].iat[i] / scale),
                    textcoords="offset points", xytext=(4, 4), fontsize=8, color=INK2)
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    fig.suptitle(f"Copy-the-Senate book, {label} ({daily['date'].iat[0]} to {daily['date'].iat[-1]})",
                 x=0.01, ha="left", color=INK, fontsize=12)
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def pick_examples(pieces: pd.DataFrame, events: pd.DataFrame) -> list[tuple[str, pd.DataFrame]]:
    """(title, pieces of one lot): a Tuberville purchase later sold in full, a partial sale, a lot held to the end.
    Deterministic: large, liquid, non-ETF names first, then the earliest lot."""
    ev = events.set_index("record_id")
    p = pieces.copy()
    p["exit_type"] = p["exit_record_id"].map(ev["transaction_type"]).fillna("")
    lots = p.groupby("lot_id")
    liquid = {"AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "NVDA", "JPM", "XOM", "CVX", "PFE", "JNJ", "WMT", "DIS",
              "HD", "KO", "PEP", "INTC", "CSCO", "BAC", "WFC", "T", "VZ", "ABBV", "MRK", "UNH", "V", "MA", "NKE", "COST"}

    def best(cands: list[str]) -> str | None:
        if not cands:
            return None
        c = sorted(cands, key=lambda l: (p.loc[p["lot_id"] == l, "price_ticker"].iat[0] not in liquid, l))
        return c[0]
    out = []
    tub = [l for l, g in lots if g["senator"].iat[0] == "Tommy Tuberville" and len(g) == 1
           and g["exit_type"].iat[0] == "Sale (Full)" and g["origin"].iat[0] == "purchase"]
    l = best(tub)
    if l:
        out.append(("A Tuberville purchase later sold in full", p[p["lot_id"] == l]))
    part = [l for l, g in lots if (g["exit_type"] == "Sale (Partial)").any() and g["origin"].iat[0] == "purchase"]
    split = [l for l in part if (p["lot_id"] == l).sum() > 1]          # prefer a lot the partial sale splits
    l = best(split) or best(part)
    if l:
        out.append(("A partial sale", p[p["lot_id"] == l]))
    held = [l for l, g in lots if len(g) == 1 and g["exit_reason"].iat[0] == "end of window" and g["origin"].iat[0] == "purchase"]
    l = best(held)
    if l:
        out.append(("A lot held to the end of the in-sample window", p[p["lot_id"] == l]))
    return out


def example_text(title: str, lot: pd.DataFrame, events: pd.DataFrame, px: pd.DataFrame) -> list[str]:
    ev = events.set_index("record_id")
    lot = lot.rename(columns={"return": "ret"})
    first = lot.iloc[0]
    buy = ev.loc[first["record_id"]]
    sym = first["price_ticker"]
    close = px[px["ticker"] == sym].set_index("date")["close"]
    L = [f"### {title}: {buy['senator']}, {buy['asset_name'][:60]} ({sym})", "",
         f"1. **Senator's trade**: {buy['transaction_type']} dated {buy['transaction_date']}, owner {buy['owner']}, "
         f"disclosed range {buy['amount']} (record {first['record_id']}, trade {first['trade_id']}).",
         f"2. **Disclosure**: PTR received {buy['disclosure_datetime'].replace('T', ' ')} (US Eastern).",
         f"3. **Entry date** = first NYSE trading day after the disclosure date = **{first['entry_date']}**.",
         f"4. **Entry price**: adjusted close {first['entry_price']:.4f} (Yahoo 'Close' that day: "
         f"{close.get(first['entry_date'], np.nan):.2f}). Size = midpoint ${buy['size']:,.2f}; "
         f"units = {buy['size']:,.2f} / {first['entry_price']:.4f} = {lot['units'].sum():,.4f}."]
    k = 5
    for r in lot.itertuples():
        if r.exit_reason in ("senator sale", "reversal"):
            s = ev.loc[r.exit_record_id]
            L.append(f"{k}. **Exit ({r.exit_reason})**: {s['transaction_type']} dated {s['transaction_date']}, disclosed "
                     f"{s['disclosure_datetime'].replace('T', ' ')} ({s['amount']}); executed at the close of **{r.exit_date}**, "
                     f"adjusted close {r.exit_price:.4f} (Yahoo 'Close' {close.get(r.exit_date, np.nan):.2f}). "
                     + (f"The partial sale sells ${s['size']:,.2f} / {r.exit_price:.4f} = {r.units:,.4f} units of this lot "
                        f"(entry cost {r.entry_dollars:,.2f}). " if s["transaction_type"] == "Sale (Partial)" else
                        f"Sells all {r.units:,.4f} units. ")
                     + f"Return {r.exit_price:.4f} / {r.entry_price:.4f} - 1 = **{r.ret:.2%}**; P&L ${r.pnl:,.2f} "
                     f"over {r.holding_trading_days} trading days ({r.holding_calendar_days} calendar days).")
        else:
            L.append(f"{k}. **{r.exit_reason.capitalize()}**: {r.units:,.4f} units marked at the adjusted close of "
                     f"**{r.exit_date}**, {r.exit_price:.4f} (Yahoo 'Close' {close.get(r.exit_date, np.nan):.2f}). "
                     f"Return {r.exit_price:.4f} / {r.entry_price:.4f} - 1 = **{r.ret:.2%}**; P&L ${r.pnl:,.2f} over "
                     f"{r.holding_trading_days} trading days ({r.holding_calendar_days} calendar days).")
        k += 1
    L += ["", "_To check on Yahoo Finance: open finance.yahoo.com/quote/" + sym + "/history, set the dates, and compare "
          "the 'Close' column (adjusted for splits only) with the Close shown here; the return uses 'Adj Close', which also "
          "reinvests dividends. Yahoo re-adjusts 'Adj Close' after every new dividend, so its level today can differ "
          "slightly from ours; the ratio between two dates should match._", ""]
    return L


def run(cfg: dict, o: dict) -> None:
    pieces, log, daily, rec, panel, ev = o["pieces"], o["log"], o["daily"], o["rec"], o["panel"], o["events"]
    label, days = o["label"], o["days"]
    last = days[-1]
    chart(daily, label)
    # actions
    acts = log.assign(kind=log["action"].str.split(":").str[0].str.replace(r" \(.*", "", regex=True))
    act_t = acts.groupby("action").agg(events=("record_id", "size"), dollars=("dollars", "sum")).reset_index() \
        .sort_values("events", ascending=False)
    ign = log[log["action"].str.startswith("ignored: nothing held")]
    ign_t = ign.groupby("senator").agg(sales_ignored=("record_id", "size"), dollars=("dollars", "sum")).reset_index() \
        .sort_values("sales_ignored", ascending=False)
    sales = log[log["transaction_type"].isin(["Sale (Full)", "Sale (Partial)"]) & ~log["action"].str.startswith("reversal")]
    skipped = log[log["action"].str.startswith("skipped")]
    sk_t = skipped.groupby(["action", "price_ticker"]).agg(purchases=("record_id", "size"), dollars=("dollars", "sum")) \
        .reset_index().sort_values("dollars", ascending=False)
    # open lots and capital
    st = pd.DataFrame([{"measure": "Open lots at the close", "min": daily["open_lots"].min(),
                        "median": daily["open_lots"].median(), "max": daily["open_lots"].max()},
                       {"measure": "Capital deployed at the close ($)", "min": daily["capital_deployed"].min(),
                        "median": daily["capital_deployed"].median(), "max": daily["capital_deployed"].max()}])
    idle = int(daily["idle_day"].sum())
    # holding periods (closed pieces: every exit except the end-of-window mark)
    closed = pieces[pieces["exit_reason"] != "end of window"]
    hp = pd.DataFrame([{"lot pieces": len(closed), "p25 trading days": closed["holding_trading_days"].quantile(.25),
                        "median trading days": closed["holding_trading_days"].median(),
                        "p75 trading days": closed["holding_trading_days"].quantile(.75),
                        "p25 calendar days": closed["holding_calendar_days"].quantile(.25),
                        "median calendar days": closed["holding_calendar_days"].median(),
                        "p75 calendar days": closed["holding_calendar_days"].quantile(.75)}])
    ex_t = pieces.groupby("exit_reason").agg(pieces=("lot_id", "size"), lots=("lot_id", "nunique"),
                                             entry_dollars=("entry_dollars", "sum"), pnl=("pnl", "sum")).reset_index()
    eow = pieces[pieces["exit_reason"] == "end of window"]
    share_cost = eow["entry_dollars"].sum() / pieces["entry_dollars"].sum()
    # repairs inside holding periods
    rep = pd.read_csv(REPAIR_LOG) if REPAIR_LOG.exists() else pd.DataFrame(columns=["ticker", "date"])
    if len(rep):
        rep["inside_copied_holding"] = [bool(((pieces["val_symbol"] == t) & (pieces["entry_date"] < d) & (pieces["exit_date"] >= d)).any())
                                        for t, d in zip(rep["ticker"], rep["date"])]
        rep["inside_sample"] = rep["date"].between(days[0], last)
    rep_t = rep.groupby("ticker").agg(rows=("date", "size"), first=("date", "min"), last=("date", "max"),
                                      in_sample=("inside_sample", "any"), inside_holding=("inside_copied_holding", "any")) \
        .reset_index() if len(rep) else pd.DataFrame()
    # returns over identical dates
    a_r, a_v = ann(daily["series_a_return"])
    b_r, b_v = ann(daily["series_b_return"])
    s_r, s_v = ann(daily["spy_return"])
    rv = pd.DataFrame([{"series": "A: return on capital deployed (headline)", "annualised return": a_r, "annualised volatility": a_v},
                       {"series": f"B: fixed pot (K = ${rec['K']:,.0f})", "annualised return": b_r, "annualised volatility": b_v},
                       {"series": "SPY (total return)", "annualised return": s_r, "annualised volatility": s_v}])
    rv_fmt = rv.assign(**{c: rv[c].map(lambda x: f"{x:.2%}") for c in ("annualised return", "annualised volatility")})
    from .panel import n_by_horizon
    nh = n_by_horizon(panel, o["horizons"])
    # worked examples
    px = o["prices_raw"] if "prices_raw" in o else pd.read_csv("data/processed/prices.csv.gz", dtype={"date": str, "ticker": str})
    px = px[px["date"] <= last]
    evx = ev
    ex = pick_examples(pieces, evx)
    EX = ["# Phase 4 worked examples (in-sample, real data)", "",
          "Three copied lots traced step by step from `data/processed/lots.csv` and `engine_events.csv`, so one can be "
          "checked by hand on Yahoo Finance. Prices are Yahoo's adjusted close (splits and dividends) as downloaded on "
          "2026-09-28.", ""]
    for t, lot in ex:
        EX += example_text(t, lot, evx, px)
    EXAMPLES.parent.mkdir(parents=True, exist_ok=True)
    EXAMPLES.write_text("\n".join(EX))

    n_ev = len(ev)
    L = ["## Phase 4: engine (in-sample only)", "",
         f"_Stage `engine` of `python run_all.py`. Sample: **{label}, {days[0]} to {last}** ({len(days)} NYSE trading days). "
         "The out-of-sample firewall is shut: prices, RF and the calendar are cut at the last in-sample day before anything "
         "is computed. Outputs: `data/processed/lots.csv`, `daily_book.csv`, `event_panel.csv`, `engine_events.csv`, "
         "`engine_metadata.json` (definitions, K, reconciliation, config)._", "",
         "### 1. Events and what the book did with them", "",
         f"{n_ev} events: in-scope records (J3, as first published) whose entry date (first NYSE trading day after the "
         "disclosure date) falls in the sample, plus out-of-scope corrections that reverse an in-scope record. Same-day "
         "order: entry date, disclosure datetime, transaction date, row number (E29).", "",
         md(act_t, ",.0f"), "",
         "### 2. Records not copied", "",
         f"- **Survivorship ledger** (K3, logged and skipped until CRSP): {int(skipped['action'].str.contains('ledger').sum())} "
         f"purchases, ${skipped.loc[skipped['action'].str.contains('ledger'), 'dollars'].sum():,.0f} at midpoints. "
         "V15 (pre-registered, not run) fills them with SPY.",
         f"- **No price on the entry date** (series exists): {int(skipped['action'].str.contains('no price').sum())}.", "",
         md(sk_t, ",.0f"), "",
         f"**Sales ignored because nothing was held** (no shorting; includes anything bought before the window): "
         f"{len(ign)} of {len(sales)} sale records ({len(ign) / max(len(sales), 1):.0%}), by senator:", "",
         md(ign_t, ",.0f"), "",
         "### 3. Open lots and capital deployed", "",
         f"![open lots and capital](figures/{FIG.name})", "",
         md(st, ",.0f"), "",
         f"Days with no open lot (series A earns RF): {idle} of {len(days)}. Days without a Ken French RF value: "
         f"{o['missing_rf']}.", "",
         "### 4. Holding periods and exits", "",
         "Closed lot pieces (every exit except the end-of-window mark; a partial sale closes a piece of a lot):", "",
         md(hp, ",.0f"), "", md(ex_t, ",.0f"), "",
         f"**Still held on the last in-sample day ({last})**: {eow['lot_id'].nunique()} lots, "
         f"{share_cost:.1%} of all dollars ever invested (at cost; ${eow['entry_dollars'].sum():,.0f} of "
         f"${pieces['entry_dollars'].sum():,.0f}), marked at ${eow['exit_value'].sum():,.0f}.", "",
         "### 5. Reconciliation (lot P&L against the daily book)", "",
         f"- Sum of lot P&L: **${rec['lot_pnl']:,.2f}**.",
         f"- Sum of daily book P&L (units x daily change in adjusted close): ${rec['book_pnl']:,.2f}; "
         f"difference **${rec['diff_book_minus_lots']:.6f}**.",
         f"- Series A return x capital at the prior close, summed: ${rec['series_a_implied_pnl']:,.2f}; difference "
         f"${rec['diff_series_a_minus_lots']:.6f}.",
         f"- Series B: final NAV - K - interest earned on cash = ${rec['pot_pnl_ex_interest']:,.2f}; difference "
         f"${rec['diff_pot_minus_lots']:.6f}. K = **${rec['K']:,.2f}**; interest on idle cash ${rec['pot_interest']:,.2f}; "
         f"lowest cash balance ${rec['min_pot_cash']:,.2f} (never negative by construction).", "",
         "### 6. K6 price repairs and copied holding periods", "",
         (md(rep_t, ",.0f") if len(rep_t) else "_No repairs._"), "",
         f"Repairs inside the sample: {int(rep['inside_sample'].sum()) if len(rep) else 0} rows; inside a copied holding "
         f"period: **{int(rep['inside_copied_holding'].sum()) if len(rep) else 0}**.", "",
         "### 7. Trade-level panel: N per horizon", "",
         f"`data/processed/event_panel.csv`: {len(panel)} in-scope purchase and sale records; {int(panel['no_price'].sum())} "
         "without a price on the entry date. Horizons that run past the last in-sample day are censored.", "",
         md(nh, ",.0f"), "",
         "### 8. In-sample annualised return and volatility, identical dates", "",
         f"Daily returns {days[0]} to {last} ({len(days)} days); annualised return = (product of 1 + r)^(252/N) - 1, "
         "volatility = daily standard deviation x sqrt(252). Nothing else yet: no Sharpe ratios, alphas or variants "
         "(Phases 5 and 6).", "",
         md(rv_fmt), "",
         "### 9. Worked examples", "",
         f"Three lots traced step by step in `{EXAMPLES}`.", ""]
    write_section(4, L)
