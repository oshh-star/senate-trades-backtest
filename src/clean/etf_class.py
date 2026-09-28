"""K5: asset class of every ETF (equity, fixed_income, commodity, other), from Yahoo's fund category.

The project scope is US equities, so the headline keeps EQUITY ETFs only (`universe.etf_classes`);
V16 keeps every class. Yahoo's fund category (Morningstar's category name, e.g. "Large Blend",
"Ultrashort Bond", "Commodities Focused") comes from the quoteSummary endpoint (module
fundProfile), which needs Yahoo's session cookie and "crumb". One request per symbol, cached in
data/raw/yahoo_fund/<symbol>.json with the query date; delete a file to ask again. A symbol with no
category (Yahoo has no fund profile, or no longer knows the symbol) is classified from its fund name
(`method` says which rule was used).

Rules (first match wins; case-insensitive, on the category, else on the fund name):
  commodity     "commodit" (Commodities Focused / Broad Basket / Leveraged Commodities)
  fixed_income  bond, treasury, government, muni, corporate, high yield, bank loan, ultrashort,
                money market, inflation-protected, securitized, mortgage, target maturity, debt
                (Trading--Inverse / Leveraged Debt), T-bill, iBonds / BulletShares term funds
  other         digital assets, volatility, allocation, multialternative, long-short, currency,
                preferred stock, "trading--miscellaneous", systematic trend, event driven
  equity        everything else with a category (Large Blend, Technology, Real Estate, Foreign Large
                Value, Equity Precious Metals, Derivative Income, Trading--Leveraged / Inverse Equity)
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import requests

CACHE = Path("data/raw/yahoo_fund")
SUMMARY = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{sym}?modules=fundProfile,quoteType&crumb={crumb}"
CLASSES = ["equity", "fixed_income", "commodity", "other"]
OVERRIDES = Path("config/etf_class_overrides.yaml")


def load_overrides(path: Path = OVERRIDES) -> dict[str, dict]:
    """Hand classifications (symbol -> {class, note}) that win over the rules below."""
    import yaml
    if not path.exists():
        return {}
    out = (yaml.safe_load(path.read_text()) or {}).get("overrides") or {}
    bad = {k: v.get("class") for k, v in out.items() if v.get("class") not in CLASSES}
    if bad:
        raise ValueError(f"unknown ETF class in {path}: {bad}")
    return out

_COMMODITY = re.compile(r"commodit", re.I)
_FIXED = re.compile(r"\bbond|treasur|government|\bmuni|corporate|high yield|bank loan|ultrashort|money market|"
                    r"inflation-protected|securitized|leveraged debt|t-bill|\bibonds\b|bulletshares|\bcredit\b|"
                    r"fixed income|nontraditional bond|mortgage|target maturity|\bdebt\b", re.I)
_OTHER = re.compile(r"digital asset|bitcoin|\bether|crypto|volatility|allocation|multialternative|long-short|currency|"
                    r"preferred stock|trading--miscellaneous|systematic trend|event driven|macro trading|"
                    r"multistrategy|equity market neutral", re.I)
# fund names only (no category): names that say what the fund holds
_NAME_COMMODITY = re.compile(r"commodit|\bgold\b(?!.*miners)|\bsilver\b(?!.*miners)|\boil fund\b|\bnatural gas fund\b|"
                             r"precious metals? (trust|shares)|\bplatinum\b|\buranium trust\b", re.I)


def cache_path(sym: str) -> Path:
    return CACHE / (re.sub(r"[^A-Za-z0-9.\-]", lambda m: f"_{ord(m.group()):x}_", sym) + ".json")


def classify_text(category: str, name: str) -> tuple[str, str]:
    """(etf_class, method) from Yahoo's category, else from the fund name."""
    c = (category or "").strip()
    if c:
        if _COMMODITY.search(c):
            return "commodity", "category"
        if _FIXED.search(c):
            return "fixed_income", "category"
        if _OTHER.search(c):
            return "other", "category"
        return "equity", "category"
    n = (name or "").strip()
    if not n:
        return "equity", "default: no category and no name (kept as equity; listed for review)"
    if _NAME_COMMODITY.search(n):
        return "commodity", "fund name"
    if _FIXED.search(n):
        return "fixed_income", "fund name"
    if _OTHER.search(n):
        return "other", "fund name"
    return "equity", "fund name: no bond, commodity or other keyword (equity)"


class Session:
    """Yahoo session with the cookie and crumb quoteSummary needs; throttled with retries."""

    def __init__(self, user_agent: str, min_interval: float):
        from .yahoo import Throttle
        self.s = requests.Session()
        # Yahoo's crumb endpoint answers 429 to a bare tool User-Agent; the "Mozilla/5.0 (compatible; ...)"
        # form, still naming the project and its contact, is accepted (tested 2026-09-28)
        self.s.headers["User-Agent"] = f"Mozilla/5.0 (compatible; {user_agent})"
        self.throttle = Throttle(max(min_interval, 1.5))
        self.crumb = None

    def _crumb(self) -> str:
        from .yahoo import _get
        if self.crumb is None:
            _get(self.s, "https://fc.yahoo.com", self.throttle)            # sets the session cookie (answers 404)
            r = _get(self.s, "https://query2.finance.yahoo.com/v1/test/getcrumb", self.throttle)
            self.crumb = r.text.strip()
        return self.crumb

    def profile(self, sym: str) -> dict:
        from .yahoo import _get
        for attempt in range(2):
            url = SUMMARY.format(sym=requests.utils.quote(sym, safe=""), crumb=requests.utils.quote(self._crumb(), safe=""))
            r = _get(self.s, url, self.throttle)
            try:
                body = r.json()
            except ValueError:
                body = {}
            err = ((body.get("quoteSummary") or body.get("finance") or {}).get("error") or {})
            if r.status_code == 401 or "Crumb" in str(err):
                self.crumb = None                                              # expired: fetch a new one
                continue
            break
        res = ((body.get("quoteSummary") or {}).get("result") or [None])[0] or {}
        fp, qt = res.get("fundProfile") or {}, res.get("quoteType") or {}
        return {"symbol": sym, "queried_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "status": r.status_code,
                "category": fp.get("categoryName") or "", "family": fp.get("family") or "",
                "legal_type": fp.get("legalType") or "", "quote_type": qt.get("quoteType") or "",
                "long_name": qt.get("longName") or "", "error": str(err)[:200] if err else ""}


def lookup(symbols: list[str], user_agent: str | None = None, min_interval: float = 1.0) -> dict[str, dict]:
    """{symbol: cached fund profile}. Fetches symbols not cached yet when user_agent is given."""
    CACHE.mkdir(parents=True, exist_ok=True)
    out, sess, n_new = {}, None, 0
    for sym in sorted({s for s in symbols if s}):
        p = cache_path(sym)
        if p.exists():
            out[sym] = json.loads(p.read_text())
            continue
        if user_agent is None:
            continue
        sess = sess or Session(user_agent, min_interval)
        rec = sess.profile(sym)
        p.write_text(json.dumps(rec, indent=1, sort_keys=True))
        out[sym] = rec
        n_new += 1
    if user_agent is not None:
        print(f"  [etf_class] {len(out)} ETF fund profiles ({n_new} fetched this run)")
    return out
