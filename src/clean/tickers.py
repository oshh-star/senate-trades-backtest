"""Ticker normalisation and recovery of missing tickers from the asset name.

normalise_ticker: upper-case, strip whitespace and footnote marks, share classes in Yahoo format
(BRK.B and BRK/B become BRK-B). "--" and blanks become "". The raw ticker is kept elsewhere.

Recovery, for rows with no ticker (never guessed; everything not accepted is listed):
  1. embedded: the filer wrote the ticker inside the asset name, e.g. "Wise plc Sponsored ADR
     (WIZEY)", "GOOGL - Alphabet Inc. A", "JPM-JPMorgan Chase & Co." or just "NVDA". The candidate
     is accepted only if Yahoo recognises the symbol AND (the name is the bare ticker, or a
     distinctive word of the rest of the name appears in Yahoo's or SEC's name for that symbol,
     ignoring accents, apostrophes and spaces inside words: see names_agree).
  2. sec_name (also tried when an embedded candidate is rejected): the asset name, cleaned of legal-form and share-type words, equals exactly one
     company title in SEC's company_tickers.json, and that company has exactly one plain ticker
     (or the name states a share class that picks exactly one of its class tickers).
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import requests

SEC_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_CACHE = Path("data/raw/sec/company_tickers.json")
MISSING = {"", "--", "N/A", "NA", "NONE"}
_FOOTNOTE = re.compile(r"[*†‡§¹²³⁴⁵⁶⁷⁸⁹⁰]")
_CLASS = re.compile(r"^([A-Z]{1,5})[./]([A-E])$")
_BARE = re.compile(r"^[A-Z]{1,5}(?:[.-][A-Z])?$")
_TAIL = re.compile(r"\(([A-Z]{1,5}(?:[.-][A-Z])?)\)\s*$")
_HEAD = re.compile(r"^([A-Z]{1,5}(?:[.-][A-Z])?)\s*-\s*(.+)$")
OPTION_WORDS = re.compile(r"\b(call|calls|put|puts|option|options)\b", re.I)
# Words that say nothing about which company it is.
STOP = {"inc", "incorporated", "corp", "corporation", "co", "company", "ltd", "limited", "plc", "llc",
        "lp", "l", "p", "sa", "nv", "n", "v", "ag", "se", "spa", "as", "a", "b", "c", "the", "and", "of",
        "adr", "ads", "sponsored", "unsponsored", "common", "stock", "shares", "share", "ordinary", "class",
        "cl", "com", "new", "group", "holdings", "holding", "trust", "fund", "etf", "japan", "reit",
        "international", "intl", "de", "del", "americas", "america", "usd", "par", "value"}


def normalise_ticker(raw: str) -> str:
    t = _FOOTNOTE.sub("", (raw or "")).strip().upper()
    t = re.sub(r"\s+", " ", t)
    if t in MISSING:
        return ""
    m = _CLASS.match(t)
    if m:
        t = f"{m.group(1)}-{m.group(2)}"
    return t


def fold(text: str) -> str:
    """Lower-case ASCII without accents or apostrophes: "L'Oréal" -> "loreal"."""
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"['’]", "", text)


def words(text: str, min_len: int = 3) -> set[str]:
    return {w for w in re.sub(r"[^a-z0-9]+", " ", fold(text)).split() if w not in STOP and len(w) >= min_len}


def names_agree(a: str, b: str) -> set[str]:
    """Distinctive words the two names share. Also counts a word of 4+ letters of one name found
    inside the other name written without spaces ("Fuji Film" / "FUJIFILM", "Heidelbergcement" /
    "Heidelberg Materials")."""
    wa, wb = words(a, 2), words(b, 2)
    common = wa & wb
    sa, sb = re.sub(r"[^a-z0-9]", "", fold(a)), re.sub(r"[^a-z0-9]", "", fold(b))
    common |= {w for w in wa if len(w) >= 4 and w in sb} | {w for w in wb if len(w) >= 4 and w in sa}
    return common


def clean_company(text: str) -> str:
    """Name used for exact SEC matching: lower-case, punctuation removed, STOP words removed."""
    text = re.sub(r"\([^)]*\)", " ", text)
    return " ".join(w for w in re.sub(r"[^a-z0-9]+", " ", text.lower()).split() if w not in STOP)


def embedded_candidate(asset_name: str) -> tuple[str, str] | None:
    """(ticker, rest of the name) if the asset name carries a ticker, else None."""
    name = asset_name.strip()
    if _BARE.match(name):
        return normalise_ticker(name), ""
    m = _TAIL.search(name)
    if m:
        return normalise_ticker(m.group(1)), name[:m.start()].strip()
    m = _HEAD.match(name)
    if m:
        return normalise_ticker(m.group(1)), m.group(2).strip()
    return None


def load_sec(user_agent: str) -> list[dict]:
    if not SEC_CACHE.exists():
        if "PLACEHOLDER" in user_agent:
            raise RuntimeError("scrape.contact_email is a placeholder; SEC requires a real contact email.")
        r = requests.get(SEC_URL, headers={"User-Agent": user_agent}, timeout=120)
        r.raise_for_status()
        SEC_CACHE.parent.mkdir(parents=True, exist_ok=True)
        SEC_CACHE.write_bytes(r.content)
        print(f"  [clean] downloaded SEC company_tickers.json ({len(r.content):,} bytes)")
    data = json.loads(SEC_CACHE.read_text())
    return [{"ticker": normalise_ticker(v["ticker"]), "title": v["title"], "cik": str(v["cik_str"])}
            for v in data.values()]


class SecIndex:
    def __init__(self, sec: list[dict]):
        self.by_ticker = {r["ticker"]: r for r in sec}
        self.by_name: dict[str, dict[str, set[str]]] = {}
        for r in sec:
            self.by_name.setdefault(clean_company(r["title"]), {}).setdefault(r["cik"], set()).add(r["ticker"])

    def match_name(self, asset_name: str) -> tuple[str, str]:
        """(ticker, note). ticker is "" when there is no single exact answer."""
        key = clean_company(asset_name)
        if not key:
            return "", "name empty after cleaning"
        hits = self.by_name.get(key)
        if not hits:
            return "", "no exact SEC name match"
        if len(hits) > 1:
            return "", "several SEC companies share this name: CIK " + ", ".join(sorted(hits))
        (cik, tickers), = hits.items()
        plain = sorted(t for t in tickers if re.fullmatch(r"[A-Z]{1,5}", t))
        if len(plain) != 1:
            # A share class named in the asset name picks exactly one class ticker (BF-A / BF-B).
            m = re.search(r"\bclass\s+([a-c])\b", asset_name, re.I)
            cls = [t for t in tickers if m and t.endswith("-" + m.group(1).upper())]
            if len(cls) == 1:
                return cls[0], f"SEC exact name match with share class {m.group(1).upper()}: " \
                                f"{self.by_ticker[cls[0]]['title']} (CIK {cik})"
            return "", f"SEC company CIK {cik} has several tickers: {', '.join(sorted(tickers))}"
        return plain[0], f"SEC exact name match: {self.by_ticker[plain[0]]['title']} (CIK {cik})"


def verify_embedded(ticker: str, rest: str, yahoo_rec: dict | None, sec: SecIndex | None) -> tuple[bool, str]:
    if not yahoo_rec or not yahoo_rec.get("recognised"):
        return False, f"embedded ticker {ticker} not recognised by Yahoo"
    if not rest:
        return True, f"asset name is the bare ticker {ticker}; Yahoo: {yahoo_rec.get('name', '')}"
    names = [yahoo_rec.get("name", ""), yahoo_rec.get("short_name", "")]
    if sec and ticker in sec.by_ticker:
        names.append(sec.by_ticker[ticker]["title"])
    common = set().union(*(names_agree(rest, n) for n in names if n))
    if common:
        return True, f"embedded ticker {ticker}; name words shared with {'/'.join(n for n in names if n)}: {', '.join(sorted(common))}"
    return False, f"embedded ticker {ticker} but its name ({'/'.join(n for n in names if n)}) shares no word with '{rest}'"
