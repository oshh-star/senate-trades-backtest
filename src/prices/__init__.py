"""Stage 'prices' (Phase 3): ticker resolution, Yahoo daily prices, the NYSE calendar, Ken French
factors and the price sanity checks. No trade-level or portfolio-level returns are computed here:
per-ticker daily returns exist only inside the sanity checks (src/prices/checks.py).

Steps (python run_all.py --only prices; each is resumable from the caches in data/raw/):
  1. resolve   renames / same-symbol name changes from SEC company histories -> config/ticker_renames.yaml;
               if that file changes, the clean stage is rerun so price_ticker and instrument types follow;
  2. download  Yahoo daily history, prices.start..prices.end, for every price_ticker in trades_clean.csv
               (all variants) plus prices.extra_symbols -> data/raw/prices/yahoo/
  3. build     data/processed/prices.csv.gz (date, ticker, close, adj_close, volume), dividends.csv,
               splits.csv, trading_calendar.csv (SPY's dates), price_coverage.csv (one row per symbol)
  4. factors   data/processed/factors_daily.csv and factors_monthly.csv (percent)
  5. checks    survivorship ledger (every symbol without usable prices) -> data/interim/survivorship_ledger.csv;
               Phase 3 section of outputs/data_quality.md
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import user_agent

PROCESSED = Path("data/processed")
PRICES = PROCESSED / "prices.csv.gz"
DIVIDENDS = PROCESSED / "dividends.csv"
SPLITS = PROCESSED / "splits.csv"
CALENDAR = PROCESSED / "trading_calendar.csv"
COVERAGE = PROCESSED / "price_coverage.csv"
TRADES_CLEAN = PROCESSED / "trades_clean.csv"
RECORDS = PROCESSED / "trade_records.csv"


def symbols_needed(cfg: dict) -> list[str]:
    """Every price_ticker in trades_clean.csv AND in trade_records.csv (a first-published record can name
    a symbol the corrected trade no longer uses, e.g. HIYS -> PDBC), plus prices.extra_symbols."""
    tr = pd.read_csv(TRADES_CLEAN, dtype=str, keep_default_na=False)
    rc = pd.read_csv(RECORDS, dtype=str, keep_default_na=False)
    return sorted({t for t in tr["price_ticker"] if t} | {t for t in rc["price_ticker"] if t}
                  | set(cfg["prices"]["extra_symbols"]))


def ledger_only_symbols() -> dict[str, str]:
    """K2: symbols whose ticker is right but whose Yahoo prices must never be used."""
    from src.clean.build import load_asset_overrides
    from src.clean.tickers import normalise_ticker
    return {normalise_ticker(o["ticker"]): o.get("note", "") for o in load_asset_overrides() if o.get("ledger_only")}


def resolve_step(cfg: dict) -> pd.DataFrame:
    from src import clean
    from src.clean import tickers as tk
    from src.clean import yahoo as yh
    from . import resolve as rv
    ua = user_agent(cfg)
    interval = float(cfg["scrape"]["min_seconds_between_requests"])
    sec_index = tk.SecIndex(tk.load_sec(ua))
    lookup = lambda syms: yh.lookup(syms, ua, interval)
    trades = pd.read_csv(TRADES_CLEAN, dtype=str, keep_default_na=False)
    log = pd.read_csv("data/interim/asset_name_overrides_log.csv", dtype=str, keep_default_na=False)
    extra = {r.ticker: [n for n in r.matched_asset_names.split(" | ") if n]
             for r in log.itertuples() if not r.confirmed_by and r.matched_asset_names}
    res = rv.resolve(trades, sec_index, lookup, rv.Sec(ua, interval), extra)
    rv.RESOLUTION.parent.mkdir(parents=True, exist_ok=True)
    res.to_csv(rv.RESOLUTION, index=False)
    before = rv.RENAMES.read_text() if rv.RENAMES.exists() else ""
    rv.write_renames(res)
    if rv.RENAMES.read_text() != before:
        print("  [resolve] config/ticker_renames.yaml changed: rerunning the clean stage")
        clean.run(cfg)
    print(f"  [resolve] {len(res)} tickers checked: " + ", ".join(f"{k} {v}" for k, v in res["outcome"].value_counts().items()))
    return res


def download_step(cfg: dict, commit_every: int = 0, on_batch=None) -> dict:
    from . import yahoo_prices as yp
    p = cfg["prices"]
    return yp.download(symbols_needed(cfg), Path(p["raw_dir"]), p["start"], p["end"], user_agent(cfg),
                       float(cfg["scrape"]["min_seconds_between_requests"]), commit_every, on_batch)


def recycled_symbols() -> dict[str, str]:
    """Symbols whose Yahoo history belongs to ANOTHER company than the one the senators traded
    (Yahoo knows the symbol, but its name matches no eFD name and no rename was confirmed)."""
    from .resolve import RESOLUTION
    if not RESOLUTION.exists():
        return {}
    r = pd.read_csv(RESOLUTION, keep_default_na=False)
    r = r[(r["outcome"] == "delisted_or_unknown") & (r["yahoo_recognised"].astype(str) == "True")]
    from src.clean.build import load_recycled
    return {**dict(zip(r["ticker"], r["yahoo_name"])), **{t: f"hand: {why}" for t, why in load_recycled().items()}}


ACQUIRED = ("acquired for cash", "acquired for stock", "bankrupt", "matured or liquidated fund")
SOURCE_VALIDATION = Path("data/interim/price_source_validation.csv")
CRSP_MAP = Path("data/interim/crsp_permno_map.csv")
MANUAL_REPORT = Path("data/interim/manual_prices_report.csv")


def delisting_dates_for_request() -> dict[str, str]:
    """Last SEC Form 25 date, only for ledger symbols whose company really left the market (acquired, bankrupt,
    liquidated); a renamed company ("ticker issue") keeps trading, so its Form 25 is not the end of its history."""
    from src.engine.warmup import delisting_dates
    from .resolve import load_ledger_reasons
    reasons = load_ledger_reasons()
    return {t: d for t, d in delisting_dates().items() if (reasons.get(t) or {}).get("reason") in ACQUIRED}


def external_sources(cfg: dict, order: list[str], end: str) -> dict:
    """M2: CRSP and terminal-export (manual) series by symbol, with their reports."""
    from . import crsp, manual
    from . import yahoo_prices as yp
    from .sources import needed
    out = {"crsp": {}, "manual": {}, "crsp_map": pd.DataFrame(), "manual_report": pd.DataFrame()}
    delisted = delisting_dates_for_request()
    if "manual" in order:
        out["manual"], out["manual_report"] = manual.load(Path(cfg["prices"].get("manual_dir", manual.MANUAL_DIR)),
                                                          delisted, end)
    cdir = Path(cfg["prices"].get("crsp_dir", crsp.CRSP_DIR))
    if "crsp" in order and cdir.exists() and (list(cdir.glob("*.csv")) or list(cdir.glob("*.csv.gz"))):
        spy = yp.parse(yp.read_cached(yp.cache_path(Path(cfg["prices"]["raw_dir"]), cfg["prices"]["calendar_symbol"])))
        cal = sorted(spy["prices"]["date"])
        nd = needed(cfg, cal, end, delisted)
        wanted = {r.symbol: {"tickers": set(r.efd_tickers.split()), "first": r.first_needed, "last": r.last_needed}
                  for r in nd.itertuples()}
        out["crsp"], out["crsp_map"] = crsp.load(wanted, cdir, end)
    return out


def build_step(cfg: dict) -> dict:
    from . import yahoo_prices as yp
    from . import repairs as rp
    from . import sources as sc
    p = cfg["prices"]
    end = p["end"].isoformat()
    order = list(p.get("sources", ["yahoo"]))
    ext = external_sources(cfg, order, end)
    validation, frames_y, cov_y = [], [], []
    recycled = recycled_symbols()
    ledger_only = ledger_only_symbols()
    fixes = rp.load(Path(p.get("repairs", rp.REPAIRS)))
    frames, divs, spls, cov, fix_log = [], [], [], [], []
    for sym in symbols_needed(cfg):
        rec = yp.read_cached(yp.cache_path(Path(p["raw_dir"]), sym))
        d = yp.parse(rec) if rec else yp.parse({})
        px = d["prices"][d["prices"]["date"] <= end]
        meta = (((rec or {}).get("body") or {}).get("chart") or {}).get("result") or [{}]
        rmt = (meta[0] or {}).get("meta", {}).get("regularMarketTime") if meta and meta[0] else None
        note = ""
        px, lg = rp.apply(px, sym, fixes)
        fix_log += lg
        if sym in ledger_only:
            note = f"K2: ticker confirmed by hand but Yahoo's prices are not used ({ledger_only[sym]})"
            px = px.iloc[0:0]
            d["dividends"], d["splits"] = d["dividends"].iloc[0:0], d["splits"].iloc[0:0]
        elif sym in recycled:
            note = f"recycled symbol: Yahoo's history is {recycled[sym]!r}, another company; not used"
            px = px.iloc[0:0]
            d["dividends"], d["splits"] = d["dividends"].iloc[0:0], d["splits"].iloc[0:0]
        elif not len(px):
            note = "no Yahoo price history" + (f"; Yahoo's last market time {pd.Timestamp(rmt, unit='s'):%Y-%m-%d}" if rmt else "")
        # M2: the source hierarchy (CRSP, terminal export, Yahoo), day by day
        series = {"yahoo": px[["date", "close", "adj_close", "volume"]]} if "yahoo" in order else {}
        for s in ("crsp", "manual"):
            if s in order and sym in ext[s]:
                series[s] = ext[s][sym]
        validation += sc.validate(sym, series)
        if "yahoo" in series and len(series["yahoo"]):                         # kept for V18 (Yahoo only)
            frames_y.append(series["yahoo"].assign(ticker=sym, source="yahoo"))
        cov_y.append({"ticker": sym, "has_data": bool("yahoo" in series and len(series["yahoo"])),
                      "first_date": series["yahoo"]["date"].min() if "yahoo" in series and len(series["yahoo"]) else "",
                      "last_date": series["yahoo"]["date"].max() if "yahoo" in series and len(series["yahoo"]) else ""})
        px, info = sc.merge(series, order)
        if info["sources"] and info["sources"] != ["yahoo"]:
            note = (note + "; " if note else "") + "priced from " + " + ".join(
                f"{k} ({v} days)" for k, v in info["days_by_source"].items())
        cov.append({"ticker": sym, "note": note, "has_data": len(px) > 0, "source": "+".join(info["sources"]),
                    "unbridged_days": info["unbridged_days"], "first_date": px["date"].min() if len(px) else "",
                    "last_date": px["date"].max() if len(px) else "", "n_days": len(px),
                    "downloaded_at": (rec or {}).get("downloaded_at", ""), "http_status": (rec or {}).get("status", ""),
                    "yahoo_type": d["meta"].get("instrumentType", ""), "exchange": d["meta"].get("exchangeName", ""),
                    "currency": d["meta"].get("currency", ""), "yahoo_name": d["meta"].get("longName") or d["meta"].get("shortName") or ""})
        if len(px):
            frames.append(px.assign(ticker=sym))
        if len(d["dividends"]):
            divs.append(d["dividends"][d["dividends"]["date"] <= end].assign(ticker=sym))
        if len(d["splits"]):
            spls.append(d["splits"][d["splits"]["date"] <= end].assign(ticker=sym))
    prices = pd.concat(frames, ignore_index=True)[["date", "ticker", "close", "adj_close", "volume", "source"]]
    prices = prices.sort_values(["ticker", "date"]).reset_index(drop=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    prices.to_csv(PRICES, index=False, float_format="%.6f", compression={"method": "gzip", "mtime": 0})
    pd.concat(divs, ignore_index=True)[["date", "ticker", "dividend"]].to_csv(DIVIDENDS, index=False)
    (pd.concat(spls, ignore_index=True)[["date", "ticker", "numerator", "denominator", "ratio"]]
     if spls else pd.DataFrame(columns=["date", "ticker", "numerator", "denominator", "ratio"])).to_csv(SPLITS, index=False)
    cal = prices.loc[prices["ticker"] == p["calendar_symbol"], ["date"]].reset_index(drop=True)
    cal.to_csv(CALENDAR, index=False)
    cov = pd.DataFrame(cov)
    cov.to_csv(COVERAGE, index=False)
    # V18 (prices.sources: [yahoo]): when another source replaced some Yahoo rows, keep the Yahoo-only prices too
    y_only, y_cov = PROCESSED / "prices_yahoo_only.csv.gz", PROCESSED / "price_coverage_yahoo_only.csv"
    if set(cov.loc[cov["has_data"], "source"]) - {"yahoo"}:
        pd.concat(frames_y, ignore_index=True)[["date", "ticker", "close", "adj_close", "volume", "source"]].to_csv(
            y_only, index=False, float_format="%.6f", compression={"method": "gzip", "mtime": 0})
        pd.DataFrame(cov_y).to_csv(y_cov, index=False)
    else:
        for f in (y_only, y_cov):
            f.unlink(missing_ok=True)
    val = pd.DataFrame(validation, columns=["symbol", "source_a", "source_b", "days", "first_date", "last_date",
                                            "correlation", "mean_abs_gap", "max_abs_gap", "max_gap_date"])
    SOURCE_VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    val.to_csv(SOURCE_VALIDATION, index=False)
    ext["crsp_map"].to_csv(CRSP_MAP, index=False)
    ext["manual_report"].to_csv(MANUAL_REPORT, index=False)
    unused = sorted((set(ext["crsp"]) | set(ext["manual"])) - set(cov["ticker"]))
    print(f"  [prices] sources {order}: " + ", ".join(f"{k} {v}" for k, v in cov["source"].replace("", "no data").value_counts().items())
          + (f"; files for symbols no trade uses: {unused}" if unused else ""))
    rp.LOG.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(fix_log, columns=rp.LOG_COLUMNS).to_csv(rp.LOG, index=False)
    print(f"  [prices] K6 repairs: {len(fix_log)} price rows changed in {len({r['ticker'] for r in fix_log})} symbols -> {rp.LOG}")
    print(f"  [prices] {cov['has_data'].sum()}/{len(cov)} symbols with data; {len(prices):,} price rows -> {PRICES}; "
          f"calendar {cal['date'].min()}..{cal['date'].max()} ({len(cal)} days)")
    return {"prices": prices, "calendar": cal, "coverage": cov, "validation": val, "crsp_map": ext["crsp_map"],
            "manual_report": ext["manual_report"], "order": order}


def run(cfg: dict) -> None:
    from . import checks, french
    resolve_step(cfg)
    download_step(cfg)
    built = build_step(cfg)
    daily, monthly = french.run(cfg, user_agent(cfg))
    checks.run(cfg, built, daily, monthly)
