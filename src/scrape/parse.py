"""Parse every downloaded PTR into data/interim/transactions_raw.csv (one row per table row).

No filtering and no cleaning: spouse trades, options, bonds and missing tickers ("--") are all
kept exactly as shown. Phase 2 decides what is in scope.

Validation, per PTR (data/interim/parse_validation.csv):
  parsed_rows   rows produced by the stdlib table parser (what goes into the CSV)
  tbody_rows    <tr> elements in the table body, counted separately with BeautifulSoup/lxml
  stated_total  the page's own "(N transactions total)" line
A PTR passes when all three agree. The page's per-owner counts ("0 Self, 1 Spouse, ...") are also
compared with the parsed Owner column. Every mismatch is listed in outputs/data_quality.md.
"""
from __future__ import annotations

import collections
import csv
import datetime as dt
import json
from pathlib import Path

from .download import MANIFEST, read_ptr
from .efd import count_table_rows, parse_ptr

TRANSACTIONS = Path("data/interim/transactions_raw.csv")
VALIDATION = Path("data/interim/parse_validation.csv")
KNOWN = {"#": "row_number", "Transaction Date": "transaction_date", "Owner": "owner",
         "Ticker": "ticker", "Asset Name": "asset_name", "Asset Type": "asset_type",
         "Type": "transaction_type", "Amount": "amount", "Comment": "comment"}
COLUMNS = ["ptr_id", "filer_name", "first_name", "last_name", "office_text", "filer_type_code",
           "filer_type_label", "date_received", "time_received", "datetime_received",
           "is_amendment", "amendment_number", "row_index", "row_number", "transaction_date",
           "transaction_date_iso", "owner", "ticker", "asset_name", "asset_type", "transaction_type",
           "amount", "comment", "extra_fields", "url"]
VALIDATION_COLUMNS = ["ptr_id", "filer_name", "date_received", "has_table", "parsed_rows",
                      "tbody_rows", "stated_total", "row_count_ok", "owner_counts_ok",
                      "owner_detail", "columns"]
OWNER_LABELS = {"Dependent Child": "Child"}


def iso_date(text: str) -> str:
    try:
        return dt.datetime.strptime(text.strip(), "%m/%d/%Y").date().isoformat()
    except ValueError:
        return ""


def parse_filing(meta: dict, html: str) -> tuple[list[dict], dict]:
    p = parse_ptr(html)
    rows = []
    for i, t in enumerate(p["transactions"], 1):
        row = {k: meta[k] for k in ("ptr_id", "filer_name", "first_name", "last_name", "office_text",
                                    "filer_type_code", "filer_type_label", "date_received",
                                    "time_received", "datetime_received", "is_amendment",
                                    "amendment_number", "url")}
        extra = {}
        for col, val in t.items():
            if col in KNOWN:
                row[KNOWN[col]] = val
            else:
                extra[col] = val
        row["row_index"] = i
        row["transaction_date_iso"] = iso_date(row.get("transaction_date", ""))
        row["extra_fields"] = json.dumps(extra) if extra else ""
        rows.append(row)
    tbody = count_table_rows(html)
    stated = p["stated_total"]
    parsed_owners = collections.Counter(r.get("owner", "") for r in rows)
    owner_detail = []
    for label, n in p["stated_owner_counts"].items():
        names = {label, OWNER_LABELS.get(label, label)}      # the page says "Dependent Child"
        got = sum(parsed_owners.get(x, 0) for x in names)
        if got != n:
            owner_detail.append(f"{label}: page {n}, parsed {got}")
    unknown = set(parsed_owners) - set(p["stated_owner_counts"]) - set(OWNER_LABELS.values())
    if p["stated_owner_counts"] and unknown:
        owner_detail.append("owners not in the page's counts: " + ", ".join(sorted(unknown)))
    n = len(rows)
    val = {"ptr_id": meta["ptr_id"], "filer_name": meta["filer_name"],
           "date_received": meta["date_received"], "has_table": p["has_table"], "parsed_rows": n,
           "tbody_rows": tbody if tbody is not None else "", "stated_total": stated if stated is not None else "",
           "owner_counts_ok": not owner_detail, "owner_detail": "; ".join(owner_detail),
           "columns": "|".join(p["columns"])}
    # A page with no transactions table fails: nothing on it shows the filing is empty on purpose.
    val["row_count_ok"] = bool(p["has_table"]) and n == tbody and (stated is None or stated == n)
    return rows, val


def run(cfg: dict) -> tuple[list[dict], list[dict]]:
    with open(MANIFEST) as f:
        manifest = [r for r in csv.DictReader(f) if r["download_status"] == "downloaded"]
    all_rows, vals = [], []
    for meta in manifest:
        rows, val = parse_filing(meta, read_ptr(Path(meta["local_path"])))
        all_rows.extend(rows)
        vals.append(val)
    TRANSACTIONS.parent.mkdir(parents=True, exist_ok=True)
    with open(TRANSACTIONS, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="raise")
        w.writeheader()
        w.writerows(all_rows)
    with open(VALIDATION, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=VALIDATION_COLUMNS)
        w.writeheader()
        w.writerows(vals)
    bad = [v for v in vals if not v["row_count_ok"]]
    bad_owner = [v for v in vals if not v["owner_counts_ok"]]
    print(f"  [parse] {len(vals)} PTRs -> {len(all_rows)} transaction rows -> {TRANSACTIONS}; "
          f"row-count mismatches: {len(bad)}; owner-count mismatches: {len(bad_owner)}")
    return all_rows, vals
