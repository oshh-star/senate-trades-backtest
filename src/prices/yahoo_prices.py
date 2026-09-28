"""Daily Yahoo price history: download, cache and parse.

One request per symbol to Yahoo's chart endpoint (the one yfinance uses) for prices.start ..
prices.end, with dividends and splits. The raw response is cached as gzipped JSON in
data/raw/prices/yahoo/<symbol>.json.gz, wrapped with the URL and the DOWNLOAD DATE: Yahoo
back-adjusts its history (adjusted close changes after every dividend and split), so the vintage
of each file matters. Resumable: a symbol with a cached answer is never asked again (delete the
file to refresh it); a symbol Yahoo did not know is asked once more on a later run (`retried`).

Fields kept when parsing: close (Yahoo's close is adjusted for splits, not for dividends),
adj_close (adjusted for splits and dividends), volume, dividends and splits.
"""
from __future__ import annotations

import datetime as dt
import gzip
import json
import re
import time
from pathlib import Path

import pandas as pd
import requests

CHART = ("https://query2.finance.yahoo.com/v8/finance/chart/{sym}?period1={p1}&period2={p2}"
         "&interval=1d&events=div%7Csplit&includeAdjustedClose=true")


def cache_path(raw_dir: Path, sym: str) -> Path:
    return Path(raw_dir) / (re.sub(r"[^A-Za-z0-9.\-]", lambda m: f"_{ord(m.group()):x}_", sym) + ".json.gz")


def epoch(d: dt.date) -> int:
    return int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp())


def read_cached(path: Path) -> dict | None:
    if not path.exists():
        return None
    with gzip.open(path, "rt") as f:
        return json.load(f)


def has_data(rec: dict | None) -> bool:
    if not rec or rec.get("status") != 200:
        return False
    res = ((rec.get("body") or {}).get("chart") or {}).get("result") or []
    return bool(res) and bool(res[0].get("timestamp"))


def fetch(session, sym: str, start: dt.date, end: dt.date, throttle) -> dict:
    url = CHART.format(sym=requests.utils.quote(sym, safe=""), p1=epoch(start),
                       p2=epoch(end + dt.timedelta(days=1)))
    from src.clean.yahoo import _get
    r = _get(session, url, throttle, timeout=60)
    try:
        body = r.json()
    except ValueError:
        body = {"text": r.text[:500]}
    return {"symbol": sym, "url": url, "status": r.status_code,
            "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "requested_start": start.isoformat(), "requested_end": end.isoformat(), "body": body}


def download(symbols: list[str], raw_dir: Path, start: dt.date, end: dt.date, user_agent: str,
             min_interval: float, commit_every: int = 0, on_batch=None) -> dict[str, str]:
    """Fetch every symbol not cached yet. Returns {symbol: 'cached' | 'fetched' | 'no data'}."""
    from src.clean.yahoo import Throttle
    raw_dir = Path(raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = user_agent
    throttle = Throttle(min_interval)
    out, n_new = {}, 0
    todo = sorted({s for s in symbols if s})
    for i, sym in enumerate(todo, 1):
        p = cache_path(raw_dir, sym)
        rec = read_cached(p)
        if rec is not None and (has_data(rec) or rec.get("retried")):
            out[sym] = "cached" if has_data(rec) else "no data"
            continue
        new = fetch(session, sym, start, end, throttle)
        if rec is not None:                      # second attempt for a symbol Yahoo did not know
            new["retried"] = True
            new["first_attempt"] = {"downloaded_at": rec.get("downloaded_at"), "status": rec.get("status")}
        with gzip.open(p, "wt") as f:
            json.dump(new, f)
        out[sym] = "fetched" if has_data(new) else "no data"
        n_new += 1
        if n_new % 100 == 0:
            print(f"  [prices] {i}/{len(todo)} symbols ({n_new} fetched this run)", flush=True)
        if commit_every and on_batch and n_new % commit_every == 0:
            on_batch(n_new)
    print(f"  [prices] {len(todo)} symbols: {sum(v == 'cached' for v in out.values())} cached, {n_new} fetched, "
          f"{sum(v == 'no data' for v in out.values())} without data")
    return out


def parse(rec: dict) -> dict:
    """{'prices': DataFrame(date, close, adj_close, volume), 'dividends': ..., 'splits': ..., 'meta': {...}}"""
    empty = pd.DataFrame(columns=["date", "close", "adj_close", "volume"])
    if not has_data(rec):
        return {"prices": empty, "dividends": pd.DataFrame(columns=["date", "dividend"]),
                "splits": pd.DataFrame(columns=["date", "numerator", "denominator", "ratio"]), "meta": {}}
    res = rec["body"]["chart"]["result"][0]
    meta = res.get("meta", {})
    tz = meta.get("exchangeTimezoneName") or "America/New_York"

    def dates(ts):
        return pd.to_datetime(pd.Series(ts, dtype="int64"), unit="s", utc=True).dt.tz_convert(tz).dt.strftime("%Y-%m-%d")

    q = (res.get("indicators", {}).get("quote") or [{}])[0]
    adj = (res.get("indicators", {}).get("adjclose") or [{}])[0].get("adjclose")
    ts = res["timestamp"]
    px = pd.DataFrame({"date": dates(ts), "close": q.get("close") or [None] * len(ts),
                       "adj_close": adj or [None] * len(ts), "volume": q.get("volume") or [None] * len(ts)})
    px = px.dropna(subset=["close"]).drop_duplicates("date", keep="last").sort_values("date").reset_index(drop=True)
    ev = res.get("events", {}) or {}
    div = pd.DataFrame([{"date": v["date"], "dividend": v.get("amount")} for v in (ev.get("dividends") or {}).values()])
    if len(div):
        div["date"] = dates(div["date"]).values
    else:
        div = pd.DataFrame(columns=["date", "dividend"])
    spl = pd.DataFrame([{"date": v["date"], "numerator": v.get("numerator"), "denominator": v.get("denominator"),
                         "ratio": v.get("splitRatio")} for v in (ev.get("splits") or {}).values()])
    if len(spl):
        spl["date"] = dates(spl["date"]).values
    else:
        spl = pd.DataFrame(columns=["date", "numerator", "denominator", "ratio"])
    keep = {k: meta.get(k) for k in ("symbol", "currency", "exchangeName", "fullExchangeName", "instrumentType",
                                      "firstTradeDate", "longName", "shortName", "exchangeTimezoneName")}
    return {"prices": px, "dividends": div.sort_values("date"), "splits": spl.sort_values("date"), "meta": keep}
