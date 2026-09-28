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
(V1-V12) is a filter on this file. `in_scope` marks the headline sample for the current config.
"""
from __future__ import annotations

import copy
import datetime as dt
import re

import numpy as np
import pandas as pd

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
    ("ETF_EXCLUDED", "ETF, and universe.include_etfs is false"),
    ("AMOUNT_UNPARSED", "Amount string not understood"),
    ("OWNER", "Owner not in universe.owners"),
]
_RANGE = re.compile(r"^\$([\d,]+)\s*-\s*\$([\d,]+)$")
_OVER = re.compile(r"^(?:over|more than)\s*\$([\d,]+)\+?$|^\$([\d,]+)\s*\+$", re.I)
_OPTION = re.compile(r"\b(call|calls|put|puts)\b|\boptions?\b.*\b(strike|expir\w*|exp)\b|\$\d+(\.\d+)?\s*(c|p)\b", re.I)


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


# ------------------------------------------------------------------ main
def build(cfg: dict, D: dict | None = None, yahoo_lookup=None, sec_index=None) -> dict:
    """Everything Phase 2 produces, as DataFrames. yahoo_lookup(symbols) -> {symbol: cached record}."""
    from . import yahoo as yh
    D = D or load_inputs()
    rows, filings, paper = prepare(D)
    start, end = analysis_window(cfg)
    wins = windows(cfg)
    union_start = min(s for s, _ in wins.values())

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
    tr = tr.drop(columns=["amendment_classes"])
    url_of = dict(zip(filings["ptr_id"], filings["url"]))
    tr["url"] = tr["first_ptr_id"].map(url_of)

    # ---- trade-level attributes
    find = service_lookup(D["terms"])
    sv = pd.DataFrame([find(b, d) for b, d in zip(tr["bioguide_id"], tr["transaction_date_iso"])])
    tr = pd.concat([tr, sv], axis=1)
    tr["transaction_date"] = tr["transaction_date_iso"]
    tr["disclosure_datetime"] = tr["first_datetime"]
    tr["disclosure_date"] = tr["first_date_received"]
    tr["disclosure_time"] = tr["disclosure_datetime"].str[11:16]
    tr["filed_before_1530_et"] = (tr["disclosure_time"] != "") & (tr["disclosure_time"] < SAME_DAY_CUTOFF)
    tdate = pd.to_datetime(tr["transaction_date"], errors="coerce")
    tr["filing_lag_days"] = (pd.to_datetime(tr["disclosure_date"]) - tdate).dt.days
    tr["late_filing"] = tr["filing_lag_days"] > LATE_DAYS
    tr["days_since_service_start"] = (tdate - pd.to_datetime(tr["service_start"], errors="coerce")).dt.days
    for col, (ws, we) in wins.items():
        tr[col] = (tr["disclosure_date"] >= ws.isoformat()) & (tr["disclosure_date"] <= we.isoformat())
    tr["in_window"] = (tr["disclosure_date"] >= start.isoformat()) & (tr["disclosure_date"] <= end.isoformat())
    tr["in_any_window"] = (tr["disclosure_date"] >= union_start.isoformat()) & (tr["disclosure_date"] <= end.isoformat())
    amt = pd.DataFrame([parse_amount(a) for a in tr["amount"]])
    tr = pd.concat([tr, amt], axis=1)
    tr["option_in_name"] = tr["asset_type"].isin(STOCK_TYPES) & tr["asset_name"].map(is_option_name)

    # ---- tickers: recovery from the asset name for rows that could still be in scope
    candidate = (tr["in_service"] & tr["in_any_window"] & tr["asset_type"].isin(STOCK_TYPES)
                 & ~tr["option_in_name"] & (tr["transaction_type"] != "Exchange"))
    tr["ticker_source"] = np.where(tr["ticker"] != "", "efd", "")
    tr["ticker_recovery_note"] = ""
    need = tr[candidate & (tr["ticker"] == "")]
    emb = {n: tk.embedded_candidate(n) for n in need["asset_name"].unique()}
    symbols = set(tr.loc[candidate & (tr["ticker"] != ""), "ticker"]) | {c[0] for c in emb.values() if c}
    sec_hits = {}
    if sec_index is not None:
        for n in need["asset_name"].unique():
            sec_hits[n] = sec_index.match_name(n)
        symbols |= {t for t, _ in sec_hits.values() if t}
    meta_raw = yahoo_lookup(sorted(symbols)) if yahoo_lookup else {}
    meta = {s: yh.classify(meta_raw.get(s)) for s in symbols}
    recovery = []
    for n in need["asset_name"].unique():
        sel = need["asset_name"] == n
        info = {"asset_name": n, "asset_type": " | ".join(sorted(need.loc[sel, "asset_type"].unique())),
                "n_trades": int(sel.sum()), "n_trades_self_joint_in_window": int(
                    (sel & need["owner"].isin(cfg["universe"]["owners"]) & need["in_window"]).sum())}
        info.update(candidate="", method="none", accepted=False, note="no SEC list loaded")
        if emb.get(n):
            t, rest = emb[n]
            ok, note = tk.verify_embedded(t, rest, meta.get(t), sec_index)
            info.update(candidate=t, method="embedded", accepted=ok, note=note)
        if not info["accepted"] and n in sec_hits:
            t, note = sec_hits[n]
            if t or not emb.get(n):
                info.update(candidate=t, method="sec_name", accepted=bool(t),
                            note=note if not emb.get(n) else f"{info['note']}; then {note}")
            else:
                info["note"] += f"; then {note}"
        recovery.append(info)
        if info["accepted"]:
            idx = need.index[sel]
            tr.loc[idx, "ticker"] = info["candidate"]
            tr.loc[idx, "ticker_source"] = info["method"]
            tr.loc[idx, "ticker_recovery_note"] = info["note"]
    recovery = pd.DataFrame(recovery, columns=["asset_name", "asset_type", "n_trades", "n_trades_self_joint_in_window",
                                               "candidate", "method", "accepted", "note"])

    tr["reached_instrument_step"] = candidate & (tr["ticker"] != "")

    # ---- instrument classification
    cls = pd.DataFrame([meta.get(t, yh.classify(None)) if t else yh.classify(None) for t in tr["ticker"]], index=tr.index)
    tr["instrument_type"] = cls["instrument_type"]
    tr["yahoo_type"] = cls["yahoo_type"]
    tr["exchange"] = cls["exchange"]
    tr["exchange_name"] = cls["exchange_name"]
    tr["listing"] = cls["listing"]
    tr["is_otc"] = cls["is_otc"]
    # Yahoo describes today's owner of the symbol. When its name shares no word with any eFD asset
    # name for that ticker (recycled symbol, e.g. FB is now a ProShares ETF, or a renamed company),
    # its classification is not trusted: the instrument is "unresolved" and Phase 3 resolves it.
    names_by_ticker = tr[tr["ticker"] != ""].groupby("ticker")["asset_name"].apply(lambda s: sorted(set(s)))
    tr["yahoo_name"] = cls["name"]
    mismatch = {t: bool(names_by_ticker.get(t)) and not any(
        tk.names_agree(n, m["name"]) or tk.names_agree(n, m["short_name"]) or t.lower() in tk.words(n, 1)
        for n in names_by_ticker[t]) for t, m in meta.items() if m["recognised"] and t in names_by_ticker}
    tr["yahoo_name_mismatch"] = [mismatch.get(t, False) for t in tr["ticker"]]
    mm = tr["yahoo_name_mismatch"]
    tr.loc[mm, "instrument_type"] = "unresolved"
    tr.loc[mm, "listing"] = "unknown"
    tr.loc[mm, "is_otc"] = False
    tr["is_etf"] = tr["instrument_type"] == "etf"
    tr["instrument_unresolved"] = tr["instrument_type"] == "unresolved"
    suffix = tr["ticker"].str.extract(r"\.([A-Z]{1,2})$")[0]
    tr["foreign_suffix"] = suffix.isin(FOREIGN_SUFFIXES)
    tr["non_us"] = ((tr["listing"] == "non_us") & ~tr["instrument_unresolved"]) | tr["foreign_suffix"]
    tr["instrument_status"] = np.select(
        [tr["instrument_type"] == "mutual_fund", tr["instrument_type"] == "other", tr["non_us"]],
        ["excluded: mutual fund", "excluded: other instrument type", "excluded: non-US listing"], "kept")

    # ---- reasons (first failing step)
    owners = cfg["universe"]["owners"]
    include_etfs = bool(cfg["universe"]["include_etfs"])
    conds = [
        ("OUTSIDE_SERVICE", ~tr["in_service"]),
        ("OUTSIDE_WINDOW", ~tr["in_window"]),
        ("ASSET_TYPE", ~tr["asset_type"].isin(STOCK_TYPES)),
        ("OPTION_IN_NAME", tr["option_in_name"]),
        ("EXCHANGE", tr["transaction_type"] == "Exchange"),
        ("NO_TICKER", tr["ticker"] == ""),
        ("MUTUAL_FUND", tr["instrument_type"] == "mutual_fund"),
        ("OTHER_INSTRUMENT", tr["instrument_type"] == "other"),
        ("NON_US_LISTING", tr["non_us"]),
        ("ETF_EXCLUDED", tr["is_etf"] & (not include_etfs)),
        ("AMOUNT_UNPARSED", ~tr["amount_parsed"]),
        ("OWNER", ~tr["owner"].isin(owners)),
    ]
    tr["reason_code"] = ""
    for code, c in conds:
        tr.loc[(tr["reason_code"] == "") & c, "reason_code"] = code
    tr["reason_detail"] = ""
    tr.loc[tr["reason_code"] == "ASSET_TYPE", "reason_detail"] = tr["asset_type"]
    tr.loc[tr["reason_code"] == "OWNER", "reason_detail"] = tr["owner"]
    tr.loc[tr["reason_code"] == "OTHER_INSTRUMENT", "reason_detail"] = tr["yahoo_type"]
    tr.loc[tr["reason_code"] == "NON_US_LISTING", "reason_detail"] = np.where(
        tr["foreign_suffix"], "ticker suffix ." + tr["ticker"].str.split(".").str[-1], tr["exchange"] + " " + tr["exchange_name"])
    tr["in_scope"] = tr["reason_code"] == ""
    keep = tr["in_any_window"].copy()
    for code, c in conds:
        if code not in ("OUTSIDE_WINDOW", "ETF_EXCLUDED", "OWNER"):
            keep &= ~c
    tr["in_trades_clean"] = keep

    # ---- flags that depend on the in-scope sample (recomputed by add_scope_flags for any config)
    tr = add_scope_flags(tr)

    # ---- row-level exclusions
    rows_x = rows.merge(rowmap, on="row_id", how="left")
    rows_x["reason_code"] = np.select(
        [rows_x["bioguide_id"] == "", rows_x["role"] == "restated_in_amendment", rows_x["role"] == "repeated_from_other_filing"],
        ["FILER_UNMATCHED", "DUPLICATE_AMENDMENT", "DUPLICATE_REFILED"], "")
    first = rows_x["role"] == "first_report"
    tmap = tr.set_index("trade_id")
    rows_x.loc[first, "reason_code"] = rows_x.loc[first, "trade_id"].map(tmap["reason_code"])
    rows_x["reason_detail"] = ""
    rows_x.loc[first, "reason_detail"] = rows_x.loc[first, "trade_id"].map(tmap["reason_detail"])
    rows_x.loc[rows_x["role"].isin(["restated_in_amendment", "repeated_from_other_filing"]), "reason_detail"] = \
        "same trade as " + rows_x["trade_id"].fillna("") + " (" + rows_x["match_pass"].fillna("") + ")"
    rows_x["kept_in_trades_clean"] = first & rows_x["trade_id"].map(tmap["in_trades_clean"]).fillna(False).astype(bool)
    return {"rows": rows_x, "trades": tr, "amendments": amend, "corrections": corrections, "recovery": recovery,
            "meta": meta, "links": links, "filings": filings, "paper": paper, "window": (start, end), "windows": wins}


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
    return tr


CLEAN_COLUMNS = [
    "trade_id", "in_scope", "reason_code", "bioguide_id", "senator", "party", "state", "owner",
    "transaction_date", "disclosure_datetime", "disclosure_date", "disclosure_time", "filed_before_1530_et",
    "transaction_type", "ticker", "ticker_raw", "ticker_source", "asset_name", "asset_type",
    "instrument_type", "is_etf", "exchange", "exchange_name", "listing", "is_otc", "instrument_unresolved",
    "yahoo_name", "yahoo_name_mismatch", "amount", "amount_lower", "amount_upper", "amount_mid", "amount_open_top",
    "filing_lag_days", "late_filing", "service_start", "days_since_service_start",
    "first_ptr_id", "first_is_amendment", "latest_ptr_id", "ptr_ids", "n_versions", "corrected_fields",
    "amendment_class", "amendment_ambiguous", "ptr_n_in_scope", "bulk_ptr", "senator_n_in_scope", "senator_rank",
    "in_window", "in_window_3y", "in_window_5y", "in_window_10y",
    "v1_tuberville", "v2_top5_senator", "v3_first_180d", "v4_bulk_ptr", "v5_etf", "v6_family_owner",
    "comment", "url",
]
EXCLUSION_COLUMNS = [
    "row_id", "ptr_id", "senator", "bioguide_id", "filer_name", "date_received", "is_amendment", "transaction_date_iso",
    "owner", "ticker_raw", "asset_name", "asset_type", "transaction_type", "amount", "reason_code", "reason_detail",
    "trade_id", "kept_in_trades_clean", "url",
]
