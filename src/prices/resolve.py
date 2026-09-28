"""Step 1 of Phase 3: resolve tickers Yahoo does not describe correctly (renames, recycled symbols,
delistings), using SEC EDGAR company histories. Never guesses: every outcome needs a company name
that agrees with the eFD asset name.

For each eFD ticker T whose own Yahoo record is missing, or whose Yahoo name shares no word with any
eFD asset name for T:
  A. same symbol, company renamed: T is in SEC's company_tickers.json and one of that company's
     names (current or former, from its EDGAR submissions file) agrees with an eFD name for T.
     Recorded under `same_symbol:` in config/ticker_renames.yaml; prices come from T.
  B. new symbol: an eFD name for T equals (after cleaning) a name, current or former, of exactly one
     SEC company that is still listed (company_tickers.json) under exactly one plain ticker T2 != T,
     Yahoo knows T2, and Yahoo's name for T2 agrees with the company's current SEC name. Recorded
     under `renames:` (old T, new T2, effective date, source); a trade under T uses T2's prices.
     Only the SAME legal entity (same SEC CIK) counts: a company absorbed by another in a merger is
     not a rename (its holders got different shares) and stays in the ledger.
  C. otherwise: survivorship ledger (data/interim/survivorship_ledger.csv), with in-scope trade
     count and midpoint dollars. CRSP is the fix once WRDS access arrives (A04).

The effective date is the date SEC shows the old name ending (formerNames `to`), which can differ
from the day the ticker itself changed; `date_basis` says which date it is.

Sources, cached in data/raw/sec/: company_tickers.json; cik-lookup-data.txt.gz (every name an SEC
filer has used, with its CIK); submissions/CIK##########.json.gz (current and former names).
"""
from __future__ import annotations

import gzip
import json
import re
import time
from pathlib import Path

import pandas as pd
import requests
import yaml

from src.clean import tickers as tk
from src.clean import yahoo as yh

SEC_DIR = Path("data/raw/sec")
CIK_LOOKUP_URL = "https://www.sec.gov/Archives/edgar/cik-lookup-data.txt"
CIK_LOOKUP = SEC_DIR / "cik-lookup-data.txt.gz"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
SUBMISSIONS = SEC_DIR / "submissions"
RESOLUTION = Path("data/interim/ticker_resolution.csv")
LEDGER = Path("data/interim/survivorship_ledger.csv")
RENAMES = Path("config/ticker_renames.yaml")
HEADER = """# Ticker renames and confirmed same-symbol name changes (Phase 3, step 1).
# Written by `python run_all.py --only prices` (src/prices/resolve.py) from SEC EDGAR company histories
# and checked against Yahoo's company names; entries can also be added by hand (say so in `source`).
#   renames:     a trade under `old` uses the price history of `new` (same company, same SEC CIK).
#   same_symbol: the company changed its name but kept the symbol; Yahoo's current name is trusted.
#   rejected:    written by hand: same SEC company but NOT the same security (tracking stock exchanged,
#                equity cancelled in bankruptcy, ...); never treated as a rename.
# The clean stage reads this file (price_ticker, instrument type), so rerun `clean` after editing it.
"""


LEGAL = {"inc", "incorporated", "corp", "corporation", "co", "company", "ltd", "limited", "plc", "llc", "lp", "l", "p",
         "sa", "nv", "n", "v", "ag", "se", "the", "de", "new", "common", "stock", "shares", "share", "class", "cl",
         "ordinary", "adr", "ads", "sponsored", "unsponsored", "a", "b", "c", "nyse", "nasdaq"}
US_SYMBOL = re.compile(r"^[A-Z]{1,5}(-[A-Z])?$")


def strict_name(text: str) -> str:
    """Company name for rename matching: punctuation, legal forms and share-type words removed, but
    distinctive words such as Group, Holding, Trust or International kept ("Vector Group" is not
    "Vector Holding")."""
    text = re.sub(r"\([^)]*\)", " ", tk.fold(text).replace("&", " and "))
    text = re.sub(r"company:.*$", " ", text)            # eFD adds "Company: ... Description: ..."
    return " ".join(w for w in re.sub(r"[^a-z0-9]+", " ", text).split() if w not in LEGAL)


class Sec:
    def __init__(self, user_agent: str, min_interval: float):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = user_agent
        self.throttle = yh.Throttle(min_interval)
        self._lookup = None

    def _get(self, url: str) -> requests.Response:
        self.throttle.wait()
        r = self.session.get(url, timeout=300)
        r.raise_for_status()
        return r

    def name_index(self) -> dict[str, set[str]]:
        """strict_name(name) -> {cik} over every name any SEC filer has used."""
        if self._lookup is None:
            if not CIK_LOOKUP.exists():
                SEC_DIR.mkdir(parents=True, exist_ok=True)
                r = self._get(CIK_LOOKUP_URL)
                with gzip.open(CIK_LOOKUP, "wb") as f:
                    f.write(r.content)
                print(f"  [resolve] downloaded cik-lookup-data.txt ({len(r.content):,} bytes)")
            idx: dict[str, set[str]] = {}
            with gzip.open(CIK_LOOKUP, "rt", encoding="latin-1") as f:
                for line in f:
                    m = re.match(r"^(.*):(\d{10}):\s*$", line)
                    if m:
                        idx.setdefault(strict_name(m.group(1)), set()).add(str(int(m.group(2))))
            self._lookup = idx
        return self._lookup

    def submissions(self, cik: str) -> dict:
        p = SUBMISSIONS / f"CIK{int(cik):010d}.json.gz"
        if not p.exists():
            SUBMISSIONS.mkdir(parents=True, exist_ok=True)
            r = self._get(SUBMISSIONS_URL.format(cik=int(cik)))
            d = r.json()
            keep = {k: d.get(k) for k in ("cik", "name", "tickers", "exchanges", "formerNames", "sic", "sicDescription")}
            keep["downloaded_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            with gzip.open(p, "wt") as f:
                json.dump(keep, f)
        with gzip.open(p, "rt") as f:
            return json.load(f)


def agree(efd_names: list[str], other: str) -> bool:
    return any(tk.names_agree(n, other) for n in efd_names) if other else False


def load_rejected(path: Path = RENAMES) -> dict[str, str]:
    """Hand-written `rejected:` entries: tickers that must NOT be treated as renamed, with the reason."""
    if not path.exists():
        return {}
    return {tk.normalise_ticker(r["ticker"]): r.get("reason", "") for r in (yaml.safe_load(path.read_text()) or {}).get("rejected") or []}


def resolve(trades: pd.DataFrame, sec_index: tk.SecIndex, yahoo_lookup, sec: Sec,
            extra: dict[str, list[str]] | None = None) -> pd.DataFrame:
    """One row per unresolved eFD ticker with its outcome. `extra` adds tickers not (yet) in
    trades_clean.csv, with their eFD asset names (the J5 overrides Yahoo could not confirm)."""
    names = trades[trades["ticker"] != ""].groupby("ticker")["asset_name"].apply(lambda s: sorted(set(s))).to_dict()
    for t, ns in (extra or {}).items():
        names[t] = sorted(set(names.get(t, [])) | set(ns))
    tickers = sorted(names)
    meta = {t: yh.classify(r) for t, r in yahoo_lookup(tickers).items()}
    todo = []
    for t in tickers:
        m = meta.get(t, yh.classify(None))
        ok = m["recognised"] and (agree(names[t], m["name"]) or agree(names[t], m["short_name"])
                                  or any(t.lower() in tk.words(n, 1) for n in names[t]))
        if not ok:
            todo.append(t)
    by_cik = {}
    for r in sec_index.by_ticker.values():
        by_cik.setdefault(r["cik"], set()).add(r["ticker"])
    rejected = load_rejected()
    out = []
    for t in todo:
        efd = names[t]
        m = meta.get(t, yh.classify(None))
        row = {"ticker": t, "efd_asset_names": " | ".join(efd[:3]), "yahoo_recognised": m["recognised"],
               "yahoo_name": m["name"], "outcome": "delisted_or_unknown", "new_ticker": "", "cik": "",
               "sec_name": "", "matched_sec_name": "", "effective_date": "", "date_basis": "", "note": ""}
        # A. same symbol, company renamed
        rec = sec_index.by_ticker.get(t)
        if rec and m["recognised"]:
            sub = sec.submissions(rec["cik"])
            all_names = [sub.get("name") or rec["title"]] + [f["name"] for f in sub.get("formerNames") or []]
            wanted_a = {strict_name(n) for n in efd} - {""}
            hit = next((n for n in all_names if strict_name(n) in wanted_a), "")
            if hit and (agree([sub.get("name") or rec["title"]], m["name"]) or agree([rec["title"]], m["short_name"])):
                row.update(outcome="same_symbol", cik=rec["cik"], sec_name=sub.get("name") or rec["title"],
                           matched_sec_name=hit, note=f"SEC CIK {rec['cik']} has used the name '{hit}'; "
                           f"Yahoo's name for {t} ('{m['name']}') is the company's current name")
                fn = next((f for f in sub.get("formerNames") or [] if f["name"] == hit), None)
                if fn:
                    row.update(effective_date=(fn.get("to") or "")[:10], date_basis="SEC: end of former name")
                out.append(row)
                continue
        if t in rejected:
            row.update(outcome="delisted_or_unknown", note=f"rename rejected by hand: {rejected[t]}")
            out.append(row)
            continue
        if not US_SYMBOL.match(t):
            row["note"] = "not a US-style symbol (likely a non-US listing); no rename searched"
            out.append(row)
            continue
        # B. new symbol, same company (same CIK)
        idx = sec.name_index()
        wanted = {strict_name(n) for n in efd} - {""}
        ciks = set()
        for n in wanted:
            ciks |= idx.get(n, set())
        listed = {c: by_cik[c] for c in ciks if c in by_cik}
        if len(listed) == 1:
            (cik, tset), = listed.items()
            plain = sorted(x for x in tset if re.fullmatch(r"[A-Z]{1,5}", x))
            new = plain[0] if len(plain) == 1 else ""
            sub = sec.submissions(cik)
            cur = sub.get("name") or sec_index.by_ticker[sorted(tset)[0]]["title"]
            all_names = [cur] + [f["name"] for f in sub.get("formerNames") or []]
            hit = next((n for n in all_names if strict_name(n) in wanted), "")
            row.update(cik=cik, sec_name=cur, matched_sec_name=hit)
            if new and new != t and hit:
                m2 = yh.classify(yahoo_lookup([new]).get(new))
                if m2["recognised"] and (agree([cur], m2["name"]) or agree([cur], m2["short_name"])):
                    fns = sorted((f for f in sub.get("formerNames") or [] if strict_name(f["name"]) in wanted),
                                 key=lambda f: f.get("to") or "")
                    fn = fns[0] if fns else None
                    hit = fn["name"] if fn else hit
                    row["matched_sec_name"] = hit
                    row.update(outcome="rename", new_ticker=new,
                               effective_date=(fn.get("to") or "")[:10] if fn else "",
                               date_basis="SEC: end of former name" if fn else "name unchanged; ticker change date not in SEC data",
                               note=f"SEC CIK {cik} ('{cur}') used the name '{hit}' and trades today as {new}; "
                                    f"Yahoo's name for {new}: '{m2['name']}'")
                    out.append(row)
                    continue
                row["note"] = f"SEC CIK {cik} matches but Yahoo's name for {new} ('{m2['name']}') does not agree"
            elif not new:
                row["note"] = f"SEC CIK {cik} matches but has no single plain ticker ({', '.join(sorted(tset))})"
            elif new == t:
                row["note"] = f"SEC CIK {cik} still lists {t}; Yahoo has no usable record"
        elif len(listed) > 1:
            row["note"] = "several listed SEC companies share this name: CIK " + ", ".join(sorted(listed))
        else:
            row["note"] = ("no listed SEC company with this name (delisted, acquired, or not an SEC filer)"
                           + (f"; {len(ciks)} unlisted CIK(s) with the name" if ciks else ""))
        out.append(row)
    return pd.DataFrame(out)


def write_renames(res: pd.DataFrame, path: Path = RENAMES) -> None:
    """Rewrite the generated entries, keeping any entry marked `hand: true`."""
    old = yaml.safe_load(path.read_text()) if path.exists() else {}
    old = old or {}
    rejected = old.get("rejected") or []
    hand_r = [r for r in old.get("renames") or [] if r.get("hand")]
    hand_s = [r for r in old.get("same_symbol") or [] if r.get("hand")]
    ren = [{"old": r.ticker, "new": r.new_ticker, "effective_date": r.effective_date, "date_basis": r.date_basis,
            "source": f"SEC EDGAR CIK {r.cik}: {r.note}"} for r in res[res["outcome"] == "rename"].itertuples()]
    same = [{"ticker": r.ticker, "cik": r.cik, "source": f"SEC EDGAR CIK {r.cik}: {r.note}"}
            for r in res[res["outcome"] == "same_symbol"].itertuples()]
    hand_old = {r["old"] for r in hand_r}
    hand_t = {r["ticker"] for r in hand_s}
    data = {"renames": hand_r + [r for r in ren if r["old"] not in hand_old],
            "same_symbol": hand_s + [r for r in same if r["ticker"] not in hand_t], "rejected": rejected}
    path.write_text(HEADER + yaml.safe_dump(data, sort_keys=False, width=200, allow_unicode=True))


def ledger(res: pd.DataFrame, trades: pd.DataFrame) -> pd.DataFrame:
    gone = res[res["outcome"] == "delisted_or_unknown"]
    s = trades[trades["in_scope"]]
    g = s.groupby("ticker").agg(in_scope_trades=("trade_id", "size"), in_scope_midpoint_dollars=("amount_mid", "sum"),
                                first_trade=("transaction_date", "min"), last_trade=("transaction_date", "max"))
    a = trades.groupby("ticker").agg(all_variant_trades=("trade_id", "size"))
    out = gone.join(g, on="ticker").join(a, on="ticker")
    out[["in_scope_trades", "in_scope_midpoint_dollars"]] = out[["in_scope_trades", "in_scope_midpoint_dollars"]].fillna(0)
    return out.sort_values(["in_scope_midpoint_dollars", "ticker"], ascending=[False, True])
