"""Phase 2 core: from data/interim/transactions_raw.csv to one row per unique, in-scope trade.

Waterfall (every raw row ends in exactly one place; the first failing step is its reason):
  1  FILER_UNMATCHED       filer not matched to a senator with high confidence
  2  DUPLICATE_AMENDMENT   the row repeats a trade already public (restated in an amendment)
     DUPLICATE_REFILED     the row repeats a trade from an unrelated earlier filing
     -> unique trades (amendments.py; the trade keeps its FIRST disclosure datetime)
  3  OUTSIDE_SERVICE       transaction date outside the senator's Senate service (A05)
  4  OUTSIDE_WINDOW        first disclosure outside the analysis window (A06, window_years)
  5  ASSET_TYPE            eFD asset type not Stock/Other (bonds, options, crypto, futures, ...)
  6  OPTION_IN_NAME        a "Stock"/"Other" row whose asset name says call/put option
  7  EXCHANGE              transaction type Exchange (D12)
  8  NO_TICKER             no ticker, and none recovered from the asset name
  9  MUTUAL_FUND / OTHER_INSTRUMENT / NON_US_LISTING   Yahoo instrument classification
 10  ETF_EXCLUDED          only when universe.include_etfs is false (V5)
 11  AMOUNT_UNPARSED       amount string not understood
 12  OWNER                 owner not in universe.owners (Spouse and Child; V6 adds them back)
     -> in-scope trades (the headline sample)

data/processed/trades_clean.csv holds every unique trade that passes steps 1-3 and 5-11 and was
disclosed inside the 3-, 5- or 10-year window, whatever the owner, so every pre-registered variant
(V1-V14) is a filter on this file. `in_scope` marks the headline sample for the current config.

Two views of every trade go through exactly the same filters (J3):
  records     ("as first published", the headline): each published version of a trade with the
              values published at that moment, effective at its own datetime. A trade is in scope
              when at least one of its records is; its reason code otherwise is its first record's.
              data/processed/trade_records.csv lists every record, for the engine.
  as revised  (variant V14): the latest values at the first disclosure datetime (the Phase 2 rule),
              in columns `in_scope_as_revised` / `reason_code_as_revised`.
Hand-written asset-name overrides (J5, config/asset_name_overrides.yaml) and ticker renames
(config/ticker_renames.yaml; a trade under an old symbol is priced with the new symbol,
`price_ticker`) are applied to both views.
"""
from __future__ import annotations

import copy
import datetime as dt
import re
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from src.config import analysis_window
from src.scrape.names import filer_key
from . import amendments as am
from . import tickers as tk

TUBERVILLE = "T000278"
STOCK_TYPES = {"Stock", "Other"}
LATE_DAYS = 45
BULK_PTR = 50
FIRST_DAYS = 180
SAME_DAY_CUTOFF = "15:30"
WINDOW_VARIANTS = [3, 5, 10]
ASSET_OVERRIDES = Path("config/asset_name_overrides.yaml")
TICKER_RENAMES = Path("config/ticker_renames.yaml")
# Yahoo's suffixes for non-US exchanges (e.g. LM09.SG = Stuttgart). A ticker carrying one is a
# non-US listing even when Yahoo no longer knows the symbol. Share classes use "-" (BRK-B).
FOREIGN_SUFFIXES = {"L", "IL", "PA", "AS", "SW", "SG", "TI", "BE", "MU", "F", "DE", "DU", "HM", "HA", "MX",
                    "TO", "V", "CN", "NE", "HK", "T", "AX", "MI", "MC", "ST", "CO", "OL", "HE", "BR", "LS",
                    "VI", "NZ", "SA", "KS", "KQ", "TW", "SS", "SZ", "NS", "BO", "JK", "SI", "BK", "IR", "PR",
                    "WA", "IS", "TA", "JO", "SN", "BA", "KL", "AT", "ME", "IC", "RG", "VS", "TL"}
REASONS = [
    ("FILER_UNMATCHED", "Filer not matched to a senator with high confidence"),
    ("DUPLICATE_AMENDMENT", "Duplicate: trade restated in an amendment (kept once, first disclosure datetime)"),
    ("DUPLICATE_REFILED", "Duplicate: trade repeated from another, unrelated filing"),
    ("OUTSIDE_SERVICE", "Transaction date outside the senator's Senate service (A05)"),
    ("OUTSIDE_WINDOW", "First disclosure outside the analysis window"),
    ("ASSET_TYPE", "eFD asset type is not Stock or Other"),
    ("OPTION_IN_NAME", "Asset name shows a call/put option"),
    ("EXCHANGE", "Exchange transaction (not a purchase or sale)"),
    ("NO_TICKER", "No ticker, and none recovered from the asset name"),
    ("MUTUAL_FUND", "Yahoo: mutual fund"),
    ("OTHER_INSTRUMENT", "Yahoo: neither equity, ETF nor mutual fund"),
    ("NON_US_LISTING", "Yahoo: not listed in the US"),
    ("LISTED_NOTE", "Exchange-listed note (a bond) filed as Stock (E50; bonds are excluded, D08)"),
    ("PREFERRED_SHARE", "Preferred share, not common equity (N2); universe.include_preferred puts it back (V19)"),
    ("ETF_EXCLUDED", "ETF, and universe.include_etfs is false"),
    ("NON_EQUITY_ETF", "ETF that is not an equity fund (K5: bond, T-bill, commodity or other)"),
    ("AMOUNT_UNPARSED", "Amount string not understood"),
    ("OWNER", "Owner not in universe.owners"),
]
_RANGE = re.compile(r"^\$([\d,]+)\s*-\s*\$([\d,]+)$")
_OVER = re.compile(r"^(?:over|more than)\s*\$([\d,]+)\+?$|^\$([\d,]+)\s*\+$", re.I)
_OPTION = re.compile(r"\b(call|calls|put|puts)\b|\boptions?\b.*\b(strike|expir\w*|exp)\b|\$\d+(\.\d+)?\s*(c|p)\b", re.I)
# The fields each view carries into the filters.
UNIT_FIELDS = ["owner", "transaction_date_iso", "ticker", "ticker_raw", "asset_name", "asset_type",
               "transaction_type", "amount", "comment"]


def parse_amount(text: str) -> dict:
    t = (text or "").strip()
    m = _RANGE.match(t)
    if m:
        lo, hi = (float(x.replace(",", "")) for x in m.groups())
        return {"amount_lower": lo, "amount_upper": hi, "amount_mid": (lo + hi) / 2, "amount_open_top": False,
                "amount_parsed": True, "amount_rule": "range: midpoint of lower and upper"}
    m = _OVER.match(t)
    if m:
        lo = float((m.group(1) or m.group(2)).replace(",", ""))
        return {"amount_lower": lo, "amount_upper": np.nan, "amount_mid": lo, "amount_open_top": True,
                "amount_parsed": True, "amount_rule": "open top band: lower bound (D10)"}
    return {"amount_lower": np.nan, "amount_upper": np.nan, "amount_mid": np.nan, "amount_open_top": False,
            "amount_parsed": False, "amount_rule": "not understood"}


def is_option_name(asset_name: str) -> bool:
    return bool(_OPTION.search(asset_name or ""))


def windows(cfg: dict) -> dict[str, tuple[dt.date, dt.date]]:
    out = {}
    for y in sorted(set(WINDOW_VARIANTS) | {int(cfg["analysis"]["window_years"])}):
        c = copy.deepcopy(cfg)
        c["analysis"]["window_years"] = y
        out[f"in_window_{y}y"] = analysis_window(c)
    return out


# ------------------------------------------------------------------ hand-written config files
def load_asset_overrides(path: Path = ASSET_OVERRIDES) -> list[dict]:
    """J5: [{contains, ticker, expect, note}]. `contains` is matched case-insensitively inside the
    eFD asset name; `expect` must appear in Yahoo's (or, failing that, SEC's) name for the ticker."""
    if not path.exists():
        return []
    return (yaml.safe_load(path.read_text()) or {}).get("overrides") or []


def load_renames(path: Path = TICKER_RENAMES) -> dict[str, dict]:
    """old ticker -> {new, effective_date, source, ...} from config/ticker_renames.yaml."""
    if not path.exists():
        return {}
    items = (yaml.safe_load(path.read_text()) or {}).get("renames") or []
    return {tk.normalise_ticker(r["old"]): {**r, "new": tk.normalise_ticker(r["new"])} for r in items}


def load_same_symbol(path: Path = TICKER_RENAMES) -> set[str]:
    """Tickers whose company changed its name but kept the symbol (confirmed via SEC history)."""
    if not path.exists():
        return set()
    return {tk.normalise_ticker(r["ticker"]) for r in (yaml.safe_load(path.read_text()) or {}).get("same_symbol") or []}


def load_non_us(path: Path = TICKER_RENAMES) -> dict[str, str]:
    """Hand-classified non-US listings (e.g. a Canadian depositary receipt): ticker -> reason."""
    if not path.exists():
        return {}
    return {tk.normalise_ticker(r["ticker"]): r.get("reason", "") for r in (yaml.safe_load(path.read_text()) or {}).get("non_us") or []}


PREFERRED = Path("config/preferred_shares.yaml")


def load_preferred(path: Path = PREFERRED) -> tuple[dict[str, str], dict[str, str]]:
    """N2 / E50: hand-reviewed preferred shares and exchange-listed notes, ticker -> name."""
    d = yaml.safe_load(path.read_text()) if path.exists() else {}
    get = lambda k: {tk.normalise_ticker(r["ticker"]): r.get("name", "") for r in (d or {}).get(k) or []}
    return get("preferred"), get("notes")


def load_recycled(path: Path = TICKER_RENAMES) -> dict[str, str]:
    """Hand-listed recycled symbols: Yahoo describes another security (ticker -> reason)."""
    if not path.exists():
        return {}
    return {tk.normalise_ticker(r["ticker"]): r.get("reason", "") for r in (yaml.safe_load(path.read_text()) or {}).get("recycled") or []}


def price_symbol(ticker: str, renames: dict[str, dict]) -> str:
    """Follow renames (FB -> META) to the symbol whose price history Yahoo keeps."""
    seen = set()
    while ticker in renames and ticker not in seen:
        seen.add(ticker)
        ticker = renames[ticker]["new"]
    return ticker


def override_label(o: dict) -> str:
    return o.get("contains") or f"= {o.get('equals')}"


def override_matches(o: dict, asset_name: str) -> bool:
    if "equals" in o:
        return asset_name.strip().lower() == str(o["equals"]).strip().lower()
    return str(o["contains"]).lower() in asset_name.lower()


def confirm_override(o: dict, meta: dict, sec_index, renames: dict) -> tuple[str, str]:
    """('yahoo' | 'sec' | '', note): is `expect` in the company name Yahoo (or SEC) gives the ticker?"""
    t = tk.normalise_ticker(o["ticker"])
    p = price_symbol(t, renames)
    if o.get("ledger_only"):
        return "hand", f"K2: ticker {t} confirmed by hand; its Yahoo prices are never used (survivorship ledger)"
    wants = [tk.fold(w) for w in ([o["expect"]] if isinstance(o["expect"], str) else o["expect"])]
    m = meta.get(p) or {}
    for n in (m.get("name", ""), m.get("short_name", "")):
        if n and any(w in tk.fold(n) for w in wants):
            return "yahoo", f"Yahoo name for {p}: {n}"
    if sec_index is not None:
        for s in (t, p):
            r = sec_index.by_ticker.get(s)
            if r and any(w in tk.fold(r["title"]) for w in wants):
                return "sec", f"Yahoo has no matching name for {p}; SEC title for {s}: {r['title']}"
    got = m.get("name") or m.get("short_name") or "(Yahoo does not know the symbol)"
    return "", f"not confirmed: expected '{o['expect']}', Yahoo name for {p}: {got}"


# ------------------------------------------------------------------ loading
def load_inputs() -> dict:
    rd = lambda p: pd.read_csv(p, dtype=str, keep_default_na=False)
    return {"tx": rd("data/interim/transactions_raw.csv"), "man": rd("data/interim/filings_manifest.csv"),
            "matches": rd("data/interim/filer_matches.csv"), "terms": rd("data/interim/senate_terms.csv"),
            "paper": rd("data/interim/paper_filings.csv")}


def prepare(D: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """(rows, filings, paper) with senator ids and normalised tickers."""
    m = D["matches"][["filer_key", "bioguide_id", "matched_name", "confidence"]]
    tx = D["tx"].copy()
    tx["filer_key"] = [filer_key(f, l) for f, l in zip(tx["first_name"], tx["last_name"])]
    tx = tx.merge(m, on="filer_key", how="left").fillna({"bioguide_id": "", "confidence": "", "matched_name": ""})
    tx.loc[tx["confidence"] != "high", "bioguide_id"] = ""
    tx["row_id"] = tx["ptr_id"] + ":" + tx["row_index"]
    tx["senator"] = tx["matched_name"]
    tx["ticker_raw"] = tx["ticker"]
    tx["ticker"] = tx["ticker_raw"].map(tk.normalise_ticker)
    tx["asset_name_norm"] = tx["asset_name"].map(am.norm_name)
    emb = {n: tk.embedded_candidate(n) for n in tx["asset_name"].unique()}
    tx["asset_id"] = [am.asset_id(t, n, (emb[n] or ("",))[0]) for t, n in zip(tx["ticker"], tx["asset_name"])]
    tx["is_sale"] = tx["transaction_type"].isin(am.SALES)
    man = D["man"].copy()
    man["filer_key"] = [filer_key(f, l) for f, l in zip(man["first_name"], man["last_name"])]
    man = man.merge(m, on="filer_key", how="left").fillna({"bioguide_id": "", "confidence": ""})
    man.loc[man["confidence"] != "high", "bioguide_id"] = ""
    man["senator"] = man["matched_name"]
    man["is_amendment"] = man["is_amendment"] == "True"
    filings = man[(man["kind"] == "electronic") & (man["download_status"] == "downloaded") & (man["bioguide_id"] != "")]
    paper = man[man["kind"] == "paper"]
    return tx, filings.reset_index(drop=True), paper.reset_index(drop=True)


def service_lookup(terms: pd.DataFrame):
    spans: dict[str, list[tuple]] = {}
    for r in terms.itertuples():
        spans.setdefault(r.bioguide_id, []).append((r.term_start, r.term_end, r.party, r.state, r.service_start))
    for v in spans.values():
        v.sort()

    def find(bid: str, date: str) -> dict:
        ts = spans.get(bid, [])
        for s, e, party, state, ss in ts:
            if date and s <= date <= e:
                return {"in_service": True, "party": party, "state": state, "service_start": ss}
        last = ts[-1] if ts else ("", "", "", "", "")
        return {"in_service": False, "party": last[2], "state": last[3], "service_start": ""}
    return find


# ------------------------------------------------------------------ the filters, for either view
def annotate(u: pd.DataFrame, cfg: dict, terms: pd.DataFrame, yahoo_lookup, sec_index,
             overrides: list[dict], renames: dict,
             same_symbol: set[str] | None = None, fund_lookup=None,
             non_us_hand: dict[str, str] | None = None) -> tuple[pd.DataFrame, pd.DataFrame, dict, pd.DataFrame]:
    """Every scope attribute and reason code for the units in `u` (records or as-revised trades).

    `u` needs trade_id, bioguide_id, senator, UNIT_FIELDS, disclosure_datetime, disclosure_date.
    Returns (u annotated, ticker recovery table, Yahoo classification per symbol, J5 override log).
    """
    from . import yahoo as yh
    u = u.reset_index(drop=True).copy()
    start, end = analysis_window(cfg)
    wins = windows(cfg)
    union_start = min(s for s, _ in wins.values())

    find = service_lookup(terms)
    sv = pd.DataFrame([find(b, d) for b, d in zip(u["bioguide_id"], u["transaction_date_iso"])])
    u = pd.concat([u, sv], axis=1)
    u["transaction_date"] = u["transaction_date_iso"]
    u["disclosure_time"] = u["disclosure_datetime"].str[11:16]
    u["filed_before_1530_et"] = (u["disclosure_time"] != "") & (u["disclosure_time"] < SAME_DAY_CUTOFF)
    tdate = pd.to_datetime(u["transaction_date"], errors="coerce")
    u["filing_lag_days"] = (pd.to_datetime(u["disclosure_date"]) - tdate).dt.days
    u["late_filing"] = u["filing_lag_days"] > LATE_DAYS
    u["days_since_service_start"] = (tdate - pd.to_datetime(u["service_start"], errors="coerce")).dt.days
    for col, (ws, we) in wins.items():
        u[col] = (u["disclosure_date"] >= ws.isoformat()) & (u["disclosure_date"] <= we.isoformat())
    u["in_window"] = (u["disclosure_date"] >= start.isoformat()) & (u["disclosure_date"] <= end.isoformat())
    u["in_any_window"] = (u["disclosure_date"] >= union_start.isoformat()) & (u["disclosure_date"] <= end.isoformat())
    # Phase 5A.2: instruments are classified for every disclosure from the scrape start, so the warm-up (L2) of any
    # window, including the 10-year window's (from 2016-01-01), has fully classified records
    u["in_class_range"] = (u["disclosure_date"] >= cfg["data"]["scrape_start"].isoformat()) & (u["disclosure_date"] <= end.isoformat())
    u = pd.concat([u, pd.DataFrame([parse_amount(a) for a in u["amount"]])], axis=1)
    u["option_in_name"] = u["asset_type"].isin(STOCK_TYPES) & u["asset_name"].map(is_option_name)

    # ---- tickers: recovery from the asset name for units that could still be in scope
    candidate = (u["in_service"] & u["in_class_range"] & u["asset_type"].isin(STOCK_TYPES)
                 & ~u["option_in_name"] & (u["transaction_type"] != "Exchange"))
    u["ticker_source"] = np.where(u["ticker"] != "", "efd", "")
    u["ticker_recovery_note"] = ""
    need = u[candidate & (u["ticker"] == "")]
    names = list(need["asset_name"].unique())
    ovr = {n: next((o for o in overrides if override_matches(o, n)), None) for n in names}
    emb = {n: tk.embedded_candidate(n) for n in names}
    sec_hits = {n: sec_index.match_name(n) for n in names} if sec_index is not None else {}
    symbols = set(u.loc[candidate & (u["ticker"] != ""), "ticker"]) | {c[0] for c in emb.values() if c}
    symbols |= {t for t, _ in sec_hits.values() if t}
    symbols |= {tk.normalise_ticker(o["ticker"]) for o in overrides}
    symbols |= {price_symbol(s, renames) for s in list(symbols)}
    meta_raw = yahoo_lookup(sorted(symbols)) if yahoo_lookup else {}
    meta = {s: yh.classify(meta_raw.get(s)) for s in symbols}

    override_log = []
    for o in overrides:
        conf, note = confirm_override(o, meta, sec_index, renames)
        hits = [n for n in names if ovr.get(n) is o]
        override_log.append({"contains": override_label(o), "ticker": tk.normalise_ticker(o["ticker"]),
                             "expect": o["expect"], "confirmed_by": conf, "note": note,
                             "matched_asset_names": " | ".join(hits), "source_note": o.get("note", "")})
    ovr_conf = {r["contains"]: r["confirmed_by"] for r in override_log}   # keyed by label

    recovery = []
    for n in names:
        sel = need["asset_name"] == n
        ids = need.loc[sel, "trade_id"]
        info = {"asset_name": n, "asset_type": " | ".join(sorted(need.loc[sel, "asset_type"].unique())),
                "n_trades": int(ids.nunique()), "n_trades_self_joint_in_window": int(need.loc[
                    sel & need["owner"].isin(cfg["universe"]["owners"]) & need["in_window"], "trade_id"].nunique()),
                "candidate": "", "method": "none", "accepted": False, "note": "no SEC list loaded"}
        if ovr.get(n):
            o = ovr[n]
            lab = override_label(o)
            ok = bool(ovr_conf[lab])
            info.update(candidate=tk.normalise_ticker(o["ticker"]), method="override", accepted=ok,
                        note=f"J5 override '{lab}' ({ovr_conf[lab] or 'NOT confirmed'})")
        if not info["accepted"] and emb.get(n):
            t, rest = emb[n]
            ok, note = tk.verify_embedded(t, rest, meta.get(t), sec_index)
            info.update(candidate=t, method="embedded", accepted=ok,
                        note=note if info["method"] == "none" else f"{info['note']}; then {note}")
        if not info["accepted"] and n in sec_hits:
            t, note = sec_hits[n]
            if t or info["method"] == "none":
                info.update(candidate=t, method="sec_name", accepted=bool(t),
                            note=note if info["method"] == "none" else f"{info['note']}; then {note}")
            else:
                info["note"] += f"; then {note}"
        recovery.append(info)
        if info["accepted"]:
            idx = need.index[sel]
            u.loc[idx, "ticker"] = info["candidate"]
            u.loc[idx, "ticker_source"] = info["method"]
            u.loc[idx, "ticker_recovery_note"] = info["note"]
    recovery = pd.DataFrame(recovery, columns=["asset_name", "asset_type", "n_trades", "n_trades_self_joint_in_window",
                                               "candidate", "method", "accepted", "note"])
    u["reached_instrument_step"] = candidate & (u["ticker"] != "")

    # ---- instrument classification, from the symbol whose prices we use (after renames)
    u["price_ticker"] = [price_symbol(t, renames) if t else "" for t in u["ticker"]]
    u["renamed"] = (u["price_ticker"] != u["ticker"]) & (u["ticker"] != "")
    none = yh.classify(None)
    cls = pd.DataFrame([meta.get(p, none) if p else none for p in u["price_ticker"]], index=u.index)
    for c_out, c_in in [("instrument_type", "instrument_type"), ("yahoo_type", "yahoo_type"), ("exchange", "exchange"),
                        ("exchange_name", "exchange_name"), ("listing", "listing"), ("is_otc", "is_otc"),
                        ("yahoo_name", "name")]:
        u[c_out] = cls[c_in]
    # Yahoo describes today's owner of a symbol. When its name shares no word with any eFD asset
    # name for that ticker (recycled symbol, e.g. FB is now a ProShares ETF, or a renamed company),
    # its classification is not trusted: "unresolved". A confirmed rename (ticker_renames.yaml,
    # checked by name history) or a confirmed J5 override is trusted instead.
    names_by_ticker = u[u["ticker"] != ""].groupby("ticker")["asset_name"].apply(lambda s: sorted(set(s)))
    mismatch = {t: bool(names_by_ticker.get(t)) and not any(
        tk.names_agree(n, m["name"]) or tk.names_agree(n, m["short_name"]) or tk.ticker_in_name(t, n)
        for n in names_by_ticker[t]) for t, m in meta.items() if m["recognised"] and t in names_by_ticker}
    trusted = u["renamed"] | (u["ticker_source"] == "override") | u["ticker"].isin(same_symbol or set())
    u["yahoo_name_mismatch"] = pd.Series([mismatch.get(t, False) for t in u["ticker"]], index=u.index) & ~trusted
    u["yahoo_name_mismatch"] |= u["ticker"].isin(set(load_recycled()))
    mm = u["yahoo_name_mismatch"]
    u.loc[mm, "instrument_type"] = "unresolved"
    u.loc[mm, "listing"] = "unknown"
    u.loc[mm, "is_otc"] = False
    u["is_otc"] = u["is_otc"].astype(bool)
    # K5: an instrument Yahoo cannot describe is an ETF when its eFD name says so ("... ETF",
    # "Exchange-Traded Fund"), e.g. matured iBonds / BulletShares term funds
    etf_name = u["asset_name"].str.contains(r"\bETF\b|exchange[- ]traded fund", case=False, regex=True)
    u["etf_by_name"] = (u["instrument_type"] == "unresolved") & etf_name & (u["price_ticker"] != "")
    u.loc[u["etf_by_name"], "instrument_type"] = "etf"
    u["is_etf"] = u["instrument_type"] == "etf"
    from . import etf_class as ec
    etf_syms = sorted(set(u.loc[u["is_etf"] & (u["price_ticker"] != ""), "price_ticker"]))
    prof = fund_lookup(etf_syms) if fund_lookup else ec.lookup(etf_syms)
    cls_of, hand = {}, ec.load_overrides()
    for sym in etf_syms:
        if sym in hand:
            cls_of[sym] = (hand[sym]["class"], "by hand (config/etf_class_overrides.yaml)", (prof.get(sym) or {}).get("category", ""))
            continue
        pr = prof.get(sym) or {}
        cat = pr.get("category", "")
        nm = pr.get("long_name") or (meta.get(sym) or {}).get("name", "")
        if not cat and not nm:
            nm = u.loc[u["price_ticker"] == sym, "asset_name"].iloc[0]
        cls_of[sym] = (*ec.classify_text(cat, nm), cat)
    u["etf_class"] = [cls_of.get(p, ("", "", ""))[0] if e else "" for p, e in zip(u["price_ticker"], u["is_etf"])]
    u["etf_class_method"] = [cls_of.get(p, ("", "", ""))[1] if e else "" for p, e in zip(u["price_ticker"], u["is_etf"])]
    u["etf_category"] = [cls_of.get(p, ("", "", ""))[2] if e else "" for p, e in zip(u["price_ticker"], u["is_etf"])]
    u["instrument_unresolved"] = u["instrument_type"] == "unresolved"
    suffix = u["ticker"].str.extract(r"\.([A-Z]{1,2})$")[0]
    u["foreign_suffix"] = suffix.isin(FOREIGN_SUFFIXES)
    u["non_us_hand"] = u["ticker"].isin(set(non_us_hand or {}))
    u["non_us"] = ((u["listing"] == "non_us") & ~u["instrument_unresolved"]) | u["foreign_suffix"] | u["non_us_hand"]
    u["instrument_status"] = np.select(
        [u["instrument_type"] == "mutual_fund", u["instrument_type"] == "other", u["non_us"]],
        ["excluded: mutual fund", "excluded: other instrument type", "excluded: non-US listing"], "kept")

    # ---- reasons (first failing step)
    owners = cfg["universe"]["owners"]
    include_etfs = bool(cfg["universe"]["include_etfs"])
    include_preferred = bool(cfg["universe"].get("include_preferred", False))
    pref, notes = load_preferred()
    u["is_preferred"] = u["ticker"].isin(set(pref)) | u["price_ticker"].isin(set(pref))
    u["is_listed_note"] = u["ticker"].isin(set(notes)) | u["price_ticker"].isin(set(notes))
    etf_classes = set(cfg["universe"].get("etf_classes") or ec.CLASSES)
    conds = [
        ("OUTSIDE_SERVICE", ~u["in_service"]),
        ("OUTSIDE_WINDOW", ~u["in_window"]),
        ("ASSET_TYPE", ~u["asset_type"].isin(STOCK_TYPES)),
        ("OPTION_IN_NAME", u["option_in_name"]),
        ("EXCHANGE", u["transaction_type"] == "Exchange"),
        ("NO_TICKER", u["ticker"] == ""),
        ("MUTUAL_FUND", u["instrument_type"] == "mutual_fund"),
        ("OTHER_INSTRUMENT", u["instrument_type"] == "other"),
        ("NON_US_LISTING", u["non_us"]),
        ("LISTED_NOTE", u["is_listed_note"]),
        ("PREFERRED_SHARE", u["is_preferred"] & (not include_preferred)),
        ("ETF_EXCLUDED", u["is_etf"] & (not include_etfs)),
        ("NON_EQUITY_ETF", u["is_etf"] & ~u["etf_class"].isin(etf_classes)),
        ("AMOUNT_UNPARSED", ~u["amount_parsed"]),
        ("OWNER", ~u["owner"].isin(owners)),
    ]
    u["reason_code"] = ""
    for code, c in conds:
        u.loc[(u["reason_code"] == "") & c, "reason_code"] = code
    u["reason_detail"] = ""
    u.loc[u["reason_code"] == "ASSET_TYPE", "reason_detail"] = u["asset_type"]
    u.loc[u["reason_code"] == "OWNER", "reason_detail"] = u["owner"]
    u.loc[u["reason_code"] == "OTHER_INSTRUMENT", "reason_detail"] = u["yahoo_type"]
    nu = u["reason_code"] == "NON_US_LISTING"
    u.loc[nu, "reason_detail"] = pd.Series(np.where(
        u["foreign_suffix"], "ticker suffix ." + u["ticker"].str.split(".").str[-1], u["exchange"] + " " + u["exchange_name"]),
        index=u.index)[nu]
    hand = (u["reason_code"] == "NON_US_LISTING") & u["non_us_hand"]
    u.loc[hand, "reason_detail"] = "by hand: " + u.loc[hand, "ticker"].map(non_us_hand or {})
    u.loc[u["reason_code"] == "NON_EQUITY_ETF", "reason_detail"] = u["etf_class"] + ": " + u["etf_category"]
    u["in_scope"] = u["reason_code"] == ""
    # L2 warm-up: every filter except the window; and (price request, V6) every filter except the window and the owner
    ex = pd.Series(True, index=u.index)
    for code, c in conds:
        if code not in ("OUTSIDE_WINDOW", "OWNER"):
            ex &= ~c
    owner_ok = dict(conds)["OWNER"]
    u["in_scope_ex_window_owner"] = ex & u["in_class_range"]
    # Phase 6: every filter except the ones a variant switches (window, owners, ETFs, ETF class, preferred), so the
    # engine can recompute scope for any single-variant config without rerunning this stage (events.load_units)
    base = pd.Series(True, index=u.index)
    for code, c in conds:
        if code not in ("OUTSIDE_WINDOW", "ETF_EXCLUDED", "NON_EQUITY_ETF", "PREFERRED_SHARE", "OWNER"):
            base &= ~c
    u["scope_base"] = base & u["in_class_range"]
    u["in_scope_ex_window"] = ex & ~owner_ok & u["in_class_range"]
    keep = u["in_any_window"].copy()
    for code, c in conds:
        if code not in ("OUTSIDE_WINDOW", "ETF_EXCLUDED", "NON_EQUITY_ETF", "PREFERRED_SHARE", "OWNER"):
            keep &= ~c
    u["in_trades_clean"] = keep
    return u, recovery, meta, pd.DataFrame(override_log)


# ------------------------------------------------------------------ main
def build(cfg: dict, D: dict | None = None, yahoo_lookup=None, sec_index=None,
          overrides: list[dict] | None = None, renames: dict | None = None,
          same_symbol: set[str] | None = None, fund_lookup=None, non_us_hand: dict[str, str] | None = None) -> dict:
    """Everything Phase 2 produces, as DataFrames. yahoo_lookup(symbols) -> {symbol: cached record}."""
    D = D or load_inputs()
    overrides = load_asset_overrides() if overrides is None else overrides
    renames = load_renames() if renames is None else renames
    same_symbol = load_same_symbol() if same_symbol is None else same_symbol
    non_us_hand = load_non_us() if non_us_hand is None else non_us_hand
    rows, filings, paper = prepare(D)
    start, end = analysis_window(cfg)
    wins = windows(cfg)

    # ---- 1-2: unmatched rows, then amendments and de-duplication
    matched = rows[rows["bioguide_id"] != ""]
    rows_by_ptr = {p: g.to_dict("records") for p, g in matched.groupby("ptr_id")}
    links = am.link_amendments(filings, rows_by_ptr, paper, cfg["data"]["scrape_start"])
    book, amend = am.build_trades(matched, filings, links)
    rowmap = pd.DataFrame(book.row_map)
    corrections = pd.DataFrame(book.corrections, columns=["trade_id", "field", "old", "new", "amendment_ptr_id", "match_pass"])
    tr = pd.DataFrame(book.trades)
    tr["n_versions"] = tr["ptr_ids"].map(len)
    tr["ptr_ids"] = tr["ptr_ids"].map(" ".join)
    tr["row_ids"] = tr["row_ids"].map(" ".join)
    tr["corrected_fields"] = tr["corrected_fields"].map(lambda s: " ".join(sorted(s)))
    order = ["AMBIGUOUS", "UNLINKED", "FULL_RESTATEMENT", "ADDITIVE"]
    tr["amendment_class"] = tr["amendment_classes"].map(lambda s: next((c for c in order if c in s), ""))
    tr["amendment_ambiguous"] = tr["amendment_classes"].map(lambda s: "AMBIGUOUS" in s)
    url_of = dict(zip(filings["ptr_id"], filings["url"]))
    tr["url"] = tr["first_ptr_id"].map(url_of)

    # ---- the two views
    recs = []
    for t in book.trades:
        n = len(t["records"])
        for k, r in enumerate(t["records"], 1):
            recs.append({**{f: r[f] for f in UNIT_FIELDS}, "trade_id": t["trade_id"], "bioguide_id": t["bioguide_id"],
                         "senator": t["senator"], "record_id": f"{t['trade_id']}.{k}", "record_no": k, "n_records": n,
                         "disclosure_datetime": r["effective_datetime"], "disclosure_date": r["effective_date"],
                         "record_ptr_id": r["record_ptr_id"], "changed_fields": r["changed_fields"],
                         "superseded_datetime": t["records"][k]["effective_datetime"] if k < n else ""})
    recs = pd.DataFrame(recs).assign(view="record")
    rev = tr[["trade_id", "bioguide_id", "senator"] + UNIT_FIELDS].assign(
        view="as_revised", record_id="", disclosure_datetime=tr["first_datetime"], disclosure_date=tr["first_date_received"])
    both, recovery, meta, override_log = annotate(pd.concat([recs, rev], ignore_index=True), cfg, D["terms"],
                                                  yahoo_lookup, sec_index, overrides, renames, same_symbol,
                                                  fund_lookup, non_us_hand)
    recs = both[both["view"] == "record"].reset_index(drop=True)
    rev = both[both["view"] == "as_revised"].set_index("trade_id")

    # ---- trade table: as-revised attributes, J3 scope from the records
    record_only = ["view", "record_id", "record_no", "n_records", "record_ptr_id", "changed_fields", "superseded_datetime"]
    rev = rev.drop(columns=[c for c in record_only if c in rev.columns])
    tr = tr.drop(columns=[c for c in rev.columns if c in tr.columns]).join(rev, on="trade_id")
    tr = tr.rename(columns={"in_scope": "in_scope_as_revised", "in_scope_ex_window": "in_scope_ex_window_as_revised",
                            "reason_code": "reason_code_as_revised",
                            "reason_detail": "reason_detail_as_revised"})
    g = recs.groupby("trade_id")
    first = recs[recs["record_no"] == 1].set_index("trade_id")
    last = recs.sort_values("record_no").groupby("trade_id").last()
    tr["n_records"] = tr["trade_id"].map(g.size())
    tr["corrected"] = tr["n_records"] > 1
    tr["correction_datetime"] = np.where(tr["corrected"], tr["trade_id"].map(last["disclosure_datetime"]), "")
    tr["correction_ptr_id"] = np.where(tr["corrected"], tr["trade_id"].map(last["record_ptr_id"]), "")
    for f in ["owner", "transaction_date", "ticker", "asset_name", "asset_type", "transaction_type", "amount"]:
        tr[f"orig_{f}"] = tr["trade_id"].map(first[f])
    tr["orig_record_in_scope"] = tr["trade_id"].map(first["in_scope"])
    tr["latest_record_in_scope"] = tr["trade_id"].map(last["in_scope"])
    tr["in_scope"] = tr["trade_id"].map(g["in_scope"].any())
    tr["reason_code"] = np.where(tr["in_scope"], "", tr["trade_id"].map(first["reason_code"]))
    tr["reason_detail"] = np.where(tr["in_scope"], "", tr["trade_id"].map(first["reason_detail"]))
    tr["in_trades_clean"] = tr["in_trades_clean"] | tr["trade_id"].map(g["in_trades_clean"].any())
    tr["disclosure_datetime"] = tr["first_datetime"]
    tr["disclosure_date"] = tr["first_date_received"]
    tr = add_scope_flags(tr)
    recs["in_trades_clean"] = recs["trade_id"].map(tr.set_index("trade_id")["in_trades_clean"])

    # ---- row-level exclusions (J3 reasons)
    rows_x = rows.merge(rowmap, on="row_id", how="left")
    rows_x["reason_code"] = np.select(
        [rows_x["bioguide_id"] == "", rows_x["role"] == "restated_in_amendment", rows_x["role"] == "repeated_from_other_filing"],
        ["FILER_UNMATCHED", "DUPLICATE_AMENDMENT", "DUPLICATE_REFILED"], "")
    first_row = rows_x["role"] == "first_report"
    tmap = tr.set_index("trade_id")
    rows_x.loc[first_row, "reason_code"] = rows_x.loc[first_row, "trade_id"].map(tmap["reason_code"])
    rows_x["reason_detail"] = ""
    rows_x.loc[first_row, "reason_detail"] = rows_x.loc[first_row, "trade_id"].map(tmap["reason_detail"])
    rows_x.loc[rows_x["role"].isin(["restated_in_amendment", "repeated_from_other_filing"]), "reason_detail"] = \
        "same trade as " + rows_x["trade_id"].fillna("") + " (" + rows_x["match_pass"].fillna("") + ")"
    rows_x["kept_in_trades_clean"] = first_row & rows_x["trade_id"].map(tmap["in_trades_clean"]).fillna(False).astype(bool)
    return {"rows": rows_x, "trades": tr, "records": recs, "amendments": amend, "corrections": corrections,
            "recovery": recovery, "overrides": override_log, "meta": meta, "links": links, "filings": filings,
            "paper": paper, "window": (start, end), "windows": wins, "renames": renames}


def add_scope_flags(tr: pd.DataFrame) -> pd.DataFrame:
    """Flags for the pre-registered variants, relative to the rows with in_scope == True."""
    tr = tr.copy()
    s = tr[tr["in_scope"]]
    ptr_n = s.groupby("first_ptr_id").size()
    tr["ptr_n_in_scope"] = tr["first_ptr_id"].map(ptr_n).fillna(0).astype(int)
    tr["bulk_ptr"] = tr["ptr_n_in_scope"] >= BULK_PTR
    sen = s.groupby(["bioguide_id", "senator"]).size().reset_index(name="n").sort_values(["n", "senator"], ascending=[False, True])
    sen["rank"] = range(1, len(sen) + 1)
    tr["senator_n_in_scope"] = tr["bioguide_id"].map(dict(zip(sen["bioguide_id"], sen["n"]))).fillna(0).astype(int)
    tr["senator_rank"] = tr["bioguide_id"].map(dict(zip(sen["bioguide_id"], sen["rank"]))).astype("Int64")
    tr["v1_tuberville"] = tr["bioguide_id"] == TUBERVILLE
    tr["v2_top5_senator"] = tr["senator_rank"].le(5).fillna(False).astype(bool)
    tr["v3_first_180d"] = tr["days_since_service_start"].between(0, FIRST_DAYS - 1)
    tr["v4_bulk_ptr"] = tr["bulk_ptr"]
    tr["v5_etf"] = tr["is_etf"]
    tr["v6_family_owner"] = tr["owner"].isin(["Spouse", "Child"])
    tr["v13_otc"] = tr["is_otc"]
    tr["v16_non_equity_etf"] = tr["is_etf"] & (tr.get("etf_class", pd.Series("equity", index=tr.index)) != "equity")
    tr["v19_preferred"] = tr.get("is_preferred", pd.Series(False, index=tr.index)).astype(bool)
    return tr


CLEAN_COLUMNS = [
    "trade_id", "in_scope", "reason_code", "in_scope_as_revised", "reason_code_as_revised",
    "in_scope_ex_window_as_revised", "bioguide_id", "senator", "party", "state", "owner",
    "transaction_date", "disclosure_datetime", "disclosure_date", "disclosure_time", "filed_before_1530_et",
    "transaction_type", "ticker", "price_ticker", "renamed", "ticker_raw", "ticker_source", "asset_name", "asset_type",
    "instrument_type", "is_etf", "etf_class", "etf_category", "etf_class_method", "exchange", "exchange_name", "listing", "is_otc", "instrument_unresolved",
    "yahoo_name", "yahoo_name_mismatch", "amount", "amount_lower", "amount_upper", "amount_mid", "amount_open_top",
    "filing_lag_days", "late_filing", "service_start", "days_since_service_start",
    "first_ptr_id", "first_is_amendment", "latest_ptr_id", "ptr_ids", "n_versions", "corrected_fields",
    "amendment_class", "amendment_ambiguous",
    "corrected", "n_records", "correction_datetime", "correction_ptr_id", "orig_owner", "orig_transaction_date",
    "orig_ticker", "orig_asset_name", "orig_asset_type", "orig_transaction_type", "orig_amount",
    "orig_record_in_scope", "latest_record_in_scope",
    "ptr_n_in_scope", "bulk_ptr", "senator_n_in_scope", "senator_rank",
    "in_window", "in_window_3y", "in_window_5y", "in_window_10y",
    "v1_tuberville", "v2_top5_senator", "v3_first_180d", "v4_bulk_ptr", "v5_etf", "v6_family_owner", "v13_otc",
    "v16_non_equity_etf", "is_preferred", "v19_preferred", "comment", "url",
]
RECORD_COLUMNS = [
    "record_id", "trade_id", "record_no", "n_records", "disclosure_datetime", "disclosure_date", "superseded_datetime",
    "record_ptr_id", "changed_fields", "in_scope", "in_scope_ex_window", "in_scope_ex_window_owner", "scope_base", "reason_code", "reason_detail", "bioguide_id",
    "senator", "owner", "transaction_date", "transaction_type", "ticker", "price_ticker", "asset_name", "asset_type", "instrument_type",
    "is_etf", "etf_class", "is_otc", "is_preferred", "instrument_unresolved", "amount", "amount_lower", "amount_upper", "amount_mid",
    "filed_before_1530_et", "in_window", "in_window_3y", "in_window_5y", "in_window_10y",
]
EXCLUSION_COLUMNS = [
    "row_id", "ptr_id", "senator", "bioguide_id", "filer_name", "date_received", "is_amendment", "transaction_date_iso",
    "owner", "ticker_raw", "asset_name", "asset_type", "transaction_type", "amount", "reason_code", "reason_detail",
    "trade_id", "kept_in_trades_clean", "url",
]
