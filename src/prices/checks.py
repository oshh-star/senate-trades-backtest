"""Phase 3 sanity checks and the Phase 3 section of outputs/data_quality.md.

Per-ticker daily returns are computed HERE ONLY, to find bad prices (large moves, stale series).
No trade-level or portfolio-level return is computed anywhere in Phase 3.

Entry date (D11): the first NYSE trading day strictly after the disclosure date. "Usable price" =
the record's price_ticker has a positive adjusted close on that exact date.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from src.quality import write_section

INTERIM = Path("data/interim")
MISSING_ENTRY = INTERIM / "price_missing_entry.csv"
EARLY_END = INTERIM / "price_series_ending_early.csv"
LARGE_MOVES = INTERIM / "price_large_moves.csv"
STALE = INTERIM / "price_staleness.csv"
GAPS = INTERIM / "price_gaps.csv"
MOVE_LIMIT = 0.50
STALE_LIMIT = 0.20
GAP_DAYS = 5


def md(df: pd.DataFrame, index: bool = False) -> str:
    return df.to_markdown(index=index, floatfmt=",.0f") if len(df) else "_None._"


def pct(x) -> str:
    return "" if pd.isna(x) else f"{x:.1%}"


def next_trading_day(cal: pd.Series, dates: pd.Series) -> pd.Series:
    """First calendar date strictly after each date (NaN when beyond the calendar)."""
    c = cal.sort_values().to_numpy()
    idx = np.searchsorted(c, dates.to_numpy(dtype=str), side="right")
    return pd.Series([c[i] if i < len(c) else np.nan for i in idx], index=dates.index)


def load_records() -> pd.DataFrame:
    r = pd.read_csv("data/processed/trade_records.csv", keep_default_na=False, dtype={"ticker": str, "price_ticker": str})
    for c in ("in_scope", "is_otc", "is_etf"):
        r[c] = r[c].astype(str) == "True"
    r["amount_mid"] = pd.to_numeric(r["amount_mid"], errors="coerce")
    return r


def coverage(recs: pd.DataFrame, prices: pd.DataFrame, cal: pd.Series, spans: pd.DataFrame) -> pd.DataFrame:
    s = recs[recs["in_scope"]].copy()
    s["entry_date"] = next_trading_day(cal, s["disclosure_date"])
    ok = prices[(prices["adj_close"] > 0)][["ticker", "date"]].assign(has=True)
    s = s.merge(ok, left_on=["price_ticker", "entry_date"], right_on=["ticker", "date"], how="left",
                suffixes=("", "_px")).drop(columns=["ticker_px", "date"])
    s["has_entry_price"] = s["has"].eq(True)
    s = s.drop(columns=["has"]).merge(spans, left_on="price_ticker", right_index=True, how="left")
    s["why_missing"] = np.select(
        [s["has_entry_price"], s["first_date"].isna(), s["entry_date"] < s["first_date"], s["entry_date"] > s["last_date"]],
        ["", "no usable Yahoo history (survivorship ledger)", "series starts after the entry date",
         "series ends before the entry date"],
        "no price on that date (gap)")
    return s


def by_senator(s: pd.DataFrame) -> pd.DataFrame:
    def row(name, d):
        dol = d["amount_mid"].sum()
        return {"Senator": name, "Trades": len(d), "With entry price": int(d["has_entry_price"].sum()),
                "Share (count)": pct(d["has_entry_price"].mean()) if len(d) else "",
                "Midpoint $": dol, "Share ($)": pct(d.loc[d["has_entry_price"], "amount_mid"].sum() / dol) if dol else ""}
    out = [row("ALL IN-SCOPE", s)]
    for name, d in sorted(s.groupby("senator"), key=lambda x: -len(x[1])):
        out.append(row(name, d))
    return pd.DataFrame(out)


def early_endings(s: pd.DataFrame, spans: pd.DataFrame, end: str) -> pd.DataFrame:
    """Tickers whose series ends before `end` while an in-scope copied purchase may still be open."""
    buys = s[s["transaction_type"] == "Purchase"]
    out = []
    for (sen, px), b in buys.groupby(["senator", "price_ticker"]):
        last = spans["last_date"].get(px, np.nan)
        if isinstance(last, str) and last >= end:
            continue
        full = s[(s["senator"] == sen) & (s["price_ticker"] == px) & (s["transaction_type"] == "Sale (Full)")]
        first_buy = b["disclosure_date"].min()
        closed = bool(len(full)) and isinstance(last, str) and (
            (full["disclosure_date"] > first_buy) & (full["disclosure_date"] <= last)).any()
        out.append({"senator": sen, "price_ticker": px, "ticker": " ".join(sorted(set(b["ticker"]))),
                    "asset_name": b["asset_name"].iloc[0][:45], "purchases": len(b), "midpoint_$": b["amount_mid"].sum(),
                    "first_purchase_disclosed": first_buy, "last_price_date": last if isinstance(last, str) else "(no data)",
                    "full_sale_disclosed_before_last_price": closed})
    return pd.DataFrame(out).sort_values(["full_sale_disclosed_before_last_price", "midpoint_$"], ascending=[True, False]) \
        if out else pd.DataFrame(columns=["senator", "price_ticker"])


def daily_checks(prices: pd.DataFrame, splits: pd.DataFrame, cal: pd.Series) -> dict:
    p = prices.sort_values(["ticker", "date"]).copy()
    g = p.groupby("ticker")
    p["ret_close"] = g["close"].pct_change()
    p["ret_adj"] = g["adj_close"].pct_change()
    p["next_ret_close"] = g["ret_close"].shift(-1)
    p["prev_date"] = g["date"].shift(1)
    # large moves
    big = p[p["ret_close"].abs() > MOVE_LIMIT].copy()
    spl = splits.assign(d=pd.to_datetime(splits["date"]))
    near = []
    for r in big.itertuples():
        d = pd.Timestamp(r.date)
        sp = spl[(spl["ticker"] == r.ticker) & ((spl["d"] - d).abs() <= pd.Timedelta(days=5))]
        near.append(" ".join(sp["ratio"].astype(str)) if len(sp) else "")
    big["split_nearby"] = near
    reverts = (np.sign(big["ret_close"]) != np.sign(big["next_ret_close"])) & (big["next_ret_close"].abs() > MOVE_LIMIT / (1 + MOVE_LIMIT))
    distribution = big["ret_adj"].abs() <= MOVE_LIMIT
    big["explanation"] = np.select(
        [big["split_nearby"] != "", distribution, reverts],
        ["split " + big["split_nearby"] + " within 5 days, yet the split-adjusted close jumps: Yahoo did NOT adjust (data error)",
         "adjusted close moves less than 50%: a special dividend or distribution",
         "reverses the next day (likely a bad print)"], "unexplained (no split on record)")
    # staleness
    st = g.apply(lambda d: pd.Series({"days": len(d), "zero_return_days": int((d["close"].diff() == 0).sum()),
                                      "first_date": d["date"].min(), "last_date": d["date"].max()}),
                 include_groups=False).reset_index()
    st["zero_share"] = st["zero_return_days"] / (st["days"] - 1).clip(lower=1)
    # gaps against the NYSE calendar
    pos = pd.Series(np.arange(len(cal)), index=cal.values)
    p["cal_pos"] = p["date"].map(pos)
    p["prev_pos"] = p.groupby("ticker")["cal_pos"].shift(1)
    p["missing"] = p["cal_pos"] - p["prev_pos"] - 1
    gaps = p[p["missing"] > GAP_DAYS][["ticker", "prev_date", "date", "missing"]].rename(
        columns={"prev_date": "last_date_before_gap", "date": "first_date_after_gap", "missing": "missing_trading_days"})
    bad = p[(p["close"] <= 0) | (p["adj_close"] <= 0) | p["adj_close"].isna()]
    return {"large": big, "stale": st, "gaps": gaps, "bad": bad}


def run(cfg: dict, built: dict, daily: pd.DataFrame, monthly: pd.DataFrame) -> None:
    prices, cal, cov = built["prices"], built["calendar"]["date"], built["coverage"]
    end = cfg["prices"]["end"].isoformat()
    recs = load_records()
    tickers = pd.read_csv("data/processed/tickers.csv", keep_default_na=False)
    otc = dict(zip(tickers["price_ticker"], tickers["is_otc"].astype(str) == "True"))
    spans = cov.set_index("ticker")[["first_date", "last_date"]].replace("", np.nan)
    splits = pd.read_csv("data/processed/splits.csv", keep_default_na=False)
    from .resolve import LEDGER, ledger
    res = pd.read_csv("data/interim/ticker_resolution.csv", keep_default_na=False)
    tr_all = pd.read_csv("data/processed/trades_clean.csv", keep_default_na=False, low_memory=False, dtype={"ticker": str})
    tr_all["in_scope"] = tr_all["in_scope"].astype(str) == "True"
    tr_all["amount_mid"] = pd.to_numeric(tr_all["amount_mid"], errors="coerce")
    led = ledger(cov, tr_all, res)
    led.to_csv(LEDGER, index=False)
    ren = yaml.safe_load(Path(cfg["prices"]["ticker_renames"]).read_text()) or {}

    s = coverage(recs, prices, cal, spans)
    miss = s[~s["has_entry_price"]]
    miss[["record_id", "senator", "ticker", "price_ticker", "asset_name", "transaction_type", "disclosure_date",
          "entry_date", "amount_mid", "why_missing", "first_date", "last_date"]].to_csv(MISSING_ENTRY, index=False)
    early = early_endings(s[s["price_ticker"].isin(spans.index[spans["last_date"].notna()])], spans, end)
    early.to_csv(EARLY_END, index=False)
    # the sanity checks look at every symbol a trade (any variant) or benchmark uses
    dc = daily_checks(prices, splits, cal)
    big, st, gaps, bad = dc["large"], dc["stale"], dc["gaps"], dc["bad"]
    big.to_csv(LARGE_MOVES, index=False)
    st["is_otc"] = st["ticker"].map(lambda t: otc.get(t, False))
    st.to_csv(STALE, index=False)
    gaps.to_csv(GAPS, index=False)
    in_scope_px = set(s["price_ticker"])

    n_all, n_ok = len(s), int(s["has_entry_price"].sum())
    dol_all = s["amount_mid"].sum()
    dol_ok = s.loc[s["has_entry_price"], "amount_mid"].sum()
    ren_t = pd.DataFrame(ren.get("renames") or [])
    same_t = pd.DataFrame(ren.get("same_symbol") or [])
    rej_t = pd.DataFrame(ren.get("rejected") or [])
    s_tr = pd.read_csv("data/processed/trades_clean.csv", keep_default_na=False, low_memory=False,
                       usecols=["ticker", "in_scope"])
    n_ren = s_tr[(s_tr["in_scope"].astype(str) == "True") & s_tr["ticker"].isin(set(ren_t.get("old", [])))].shape[0]
    led_s = led[led["in_scope_trades"] > 0]

    L = ["## Phase 3: prices", "",
         f"_Stage `prices` of `python run_all.py`. Yahoo daily history {cfg['prices']['start']} to {end} for every "
         f"symbol in trades_clean.csv (all variants) plus {', '.join(cfg['prices']['extra_symbols'])}; raw responses "
         "with their download date in `data/raw/prices/yahoo/`. No trade or portfolio returns are computed; per-ticker "
         "daily returns appear only in the checks below. Coverage uses the headline records (J3: as first published)._", "",
         "### 1. Ticker resolution (renames and the survivorship ledger)", "",
         f"{len(res)} eFD tickers had no usable Yahoo record, or a Yahoo name matching no eFD name. Outcomes: "
         + ", ".join(f"{k} {v}" for k, v in res["outcome"].value_counts().items())
         + ". Renames and same-symbol name changes are confirmed through SEC EDGAR company histories (same CIK, "
         "a current or former SEC name equal to the eFD name) and Yahoo's name for the new symbol "
         "(`config/ticker_renames.yaml`, rules in `src/prices/resolve.py`).", "",
         f"Renames ({len(ren_t)}; {n_ren} in-scope trades use one):", "",
         md(ren_t[["old", "new", "effective_date", "date_basis"]]) if len(ren_t) else "_None._", "",
         f"Same symbol, company renamed ({len(same_t)}): " + (", ".join(same_t["ticker"]) if len(same_t) else "none") + ".", "",
         "Rejected by hand (same SEC company, not the same security):", "",
         md(rej_t) if len(rej_t) else "_None._", "",
         f"**Survivorship ledger** (`data/interim/survivorship_ledger.csv`): {len(led)} price symbols needed by some trade "
         f"(any variant) have no usable Yahoo history (delisted or acquired names Yahoo no longer serves, and recycled "
         f"symbols whose history now belongs to another company); {len(led_s)} of them have in-scope trades "
         f"({int(led_s['in_scope_trades'].sum())} trades, ${led_s['in_scope_midpoint_dollars'].sum():,.0f} at midpoints). "
         "CRSP (A04) is the fix.", "",
         md(led_s[["price_ticker", "efd_asset_names", "in_scope_trades", "in_scope_midpoint_dollars", "first_trade",
                   "last_trade", "why"]].assign(efd_asset_names=led_s["efd_asset_names"].str[:40], why=led_s["why"].str[:75])), "",
         "### 2. Price download", "",
         f"- Symbols requested: **{len(cov)}**; with data: **{int(cov['has_data'].sum())}**; without: "
         f"{int((~cov['has_data']).sum())}. Per-symbol first/last date and download time: `data/processed/price_coverage.csv`.",
         f"- NYSE trading calendar (SPY's dates): {cal.min()} to {cal.max()}, {len(cal):,} days "
         "(`data/processed/trading_calendar.csv`).",
         f"- `data/processed/prices.csv.gz`: {len(prices):,} rows (date, ticker, close, adj_close, volume). Yahoo's `close` is "
         "adjusted for splits only; `adj_close` for splits and dividends. Dividends and splits: "
         "`data/processed/dividends.csv`, `splits.csv`.", "",
         "### 3. Coverage: in-scope trades with a usable price on the entry date", "",
         f"Entry date = first NYSE trading day after the disclosure date (D11). **{n_ok:,} of {n_all:,} in-scope records "
         f"({pct(n_ok / n_all)}) have a price; by midpoint dollars {pct(dol_ok / dol_all)}** "
         f"(${dol_ok:,.0f} of ${dol_all:,.0f}).", "",
         md(by_senator(s)), "",
         "Why prices are missing:", "",
         md(miss.groupby("why_missing").agg(trades=("record_id", "size"), midpoint_dollars=("amount_mid", "sum")).reset_index()), "",
         f"Every in-scope record without an entry price ({len(miss)}; also `{MISSING_ENTRY}`):", "",
         md(miss[["senator", "ticker", "price_ticker", "transaction_type", "disclosure_date", "entry_date", "amount_mid",
                  "why_missing"]].sort_values(["why_missing", "senator", "disclosure_date"])), "",
         "### 4. Price series that end before the window end while a copied position may be open", "",
         f"In-scope purchases whose symbol HAS a Yahoo series that ends before {end} ({len(early)} senator-ticker pairs; "
         "symbols with no usable history at all are in the survivorship ledger, section 1; "
         f"`{EARLY_END}`). `full_sale_disclosed_before_last_price` = the same senator disclosed a Sale (Full) of it before "
         "the series ends (a rough check; FIFO matching is Phase 4). **Proposed engine rule (E20, for Harry): close the "
         "position at the last available price and hold the proceeds at the risk-free rate until the window ends.**", "",
         md(early), "",
         "### 5. Daily moves beyond +/-50% (split-adjusted close)", "",
         f"{len(big)} moves in {big['ticker'].nunique() if len(big) else 0} symbols; "
         f"{int((big['explanation'].str.startswith('unexplained')).sum()) if len(big) else 0} unexplained; "
         f"{int(big['ticker'].isin(in_scope_px).sum()) if len(big) else 0} in symbols with in-scope trades, listed below "
         f"(all of them: `{LARGE_MOVES}`). Genuine news moves (earnings, March 2020, meme stocks) also appear as "
         "'unexplained': the check only rules out splits and one-day bad prints.", "",
         md(big[big["ticker"].isin(in_scope_px)].assign(ret_close=big["ret_close"].map(pct), ret_adj=big["ret_adj"].map(pct),
                       next_ret_close=big["next_ret_close"].map(pct),
                       )[["ticker", "prev_date", "date", "close", "ret_close", "ret_adj", "next_ret_close", "explanation"]]
            .sort_values(["explanation", "ticker"], ascending=[False, True])), "",
         f"### 6. Staleness: share of days with an unchanged close (tickers above {STALE_LIMIT:.0%})", "",
         md(st[st["zero_share"] > STALE_LIMIT].assign(zero_share=lambda d: d["zero_share"].map(pct),
                                                       in_scope_symbol=lambda d: d["ticker"].isin(in_scope_px))
            .sort_values("zero_return_days", ascending=False)[
             ["ticker", "is_otc", "in_scope_symbol", "days", "zero_return_days", "zero_share", "first_date", "last_date"]]), "",
         "### 7. Zero or negative prices, and gaps longer than 5 trading days", "",
         f"- Rows with a zero, negative or missing adjusted close: **{len(bad)}**"
         + (f" ({', '.join(sorted(bad['ticker'].unique())[:20])})" if len(bad) else "") + ".",
         f"- Gaps of more than {GAP_DAYS} NYSE trading days inside a symbol's series: **{len(gaps)}** in "
         f"{gaps['ticker'].nunique() if len(gaps) else 0} symbols (`{GAPS}`).", "",
         md(gaps.assign(in_scope_symbol=gaps["ticker"].isin(in_scope_px)).sort_values("missing_trading_days", ascending=False).head(60)), "",
         "### 8. Factors (Ken French, US)", "",
         f"- Daily: {daily['date'].min()} to {daily['date'].max()} ({len(daily):,} days), `data/processed/factors_daily.csv`.",
         f"- Monthly: {monthly['month'].min()} to {monthly['month'].max()} ({len(monthly)} months), `data/processed/factors_monthly.csv`.",
         "- Columns mkt_rf_pct, smb_pct, hml_pct, rf_pct, mom_pct. **Units: percent** (1.00 = 1%), also stated in each "
         "file's `units` column; divide by 100 before use. Raw zips and download dates: `data/raw/french/`.",
         f"- NYSE calendar days without a daily factor row: {len(set(cal) - set(daily['date']))}; factor days not in the "
         f"calendar (from {cal.min()}): {len(set(daily.loc[daily['date'] >= cal.min(), 'date']) - set(cal))}.", ""]
    write_section(3, L)
    print(f"  [checks] entry-price coverage {n_ok}/{n_all} records ({pct(n_ok / n_all)}), dollars {pct(dol_ok / dol_all)}; "
          f"{len(early)} early-ending positions; {len(big)} large moves; {int((st['zero_share'] > STALE_LIMIT).sum())} stale; "
          f"{len(gaps)} gaps; {len(bad)} bad prices")
