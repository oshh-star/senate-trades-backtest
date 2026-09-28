"""Link amendments to their original PTRs, classify them, and de-duplicate to one row per trade.

Linking. An amendment A is linked to every EARLIER electronic PTR E of the same senator (earlier =
E's date-and-time received is before A's) where either
  - title: E's report title date equals A's title date (an amendment's title repeats the date of
    the report it amends, e.g. "Periodic Transaction Report for 12/24/2015 (Amendment 1)"), or E was
    received on A's title date; or
  - overlap: at least one of A's transactions exactly matches one of E's (same match key).
The linked filings, and every trade they carry, form A's "family".

Match key (one unique trade): senator, owner, transaction date, asset (normalised ticker, or the
normalised asset name when there is no ticker), transaction type, amount band.

Pairing. Filings are processed in the order they became public. For an amendment, each of its
rows is paired with a family trade:
  pass "exact"        all six key fields equal (multiset: n identical lines pair with n trades);
  pass "amount"       everything equal except the amount band;
  pass "owner"        everything equal except the owner;
  pass "date"         everything equal except the transaction date;
  pass "sale_type"    Sale (Full) vs Sale (Partial), everything else equal;
  pass "type"         any other change of transaction type (e.g. Purchase corrected to Sale);
  pass "asset"        same asset NAME, ticker added or changed, everything else equal;
  pass "asset_replaced" a different asset, everything else equal (e.g. SPY corrected to the
                      SPDR S&P Bank ETF), only as a unique leftover pair.
The "type" and "asset_replaced" passes apply only when the amendment repeats at least one trade
exactly; when they would have paired a line in an amendment that repeats nothing, the line is kept
as a new trade and the amendment is classified AMBIGUOUS (new trade, or a replacement?).
A correction pass pairs only when exactly one unpaired row and one unpaired trade share the loose
key, so nothing is guessed. A paired row updates the trade to the amendment's (corrected) values
and the trade KEEPS its first disclosure datetime (no look-ahead: it was already public). An
unpaired row is a new trade dated by the amendment. Every row, from any filing, is finally checked
against all of the senator's earlier trades from OTHER filings by exact key: a match is the same
trade reported again (a re-filed original) and is merged the same way.

Several identical lines inside ONE filing are separate trades (for example two lots bought the same
day) and are kept: de-duplication is only ever across filings.

Classification of each amendment (against its family trades before it was applied):
  FULL_RESTATEMENT  every trade of the amended report is repeated (exactly or with a correction);
                    it may add rows;
  ADDITIVE          no earlier trade is repeated: only new transactions;
  AMBIGUOUS         some but not all trades of the amended report are repeated (was the rest
                    withdrawn, or does the amendment list only the lines it changes?);
  UNLINKED          no earlier electronic filing found (the original is a paper filing, predates
                    the scrape, or is missing). Its rows are all new trades dated by the amendment.
"The amended report" = the linked filings with the amendment's title date that share at least one
trade with it (all title-linked filings if none shares one; the overlap-linked filings if no title
matches). Other linked filings (usually a later original that re-reported some of the same trades)
are used for pairing but not for the classification.
The mechanical rule is the same for every class (union of the versions, de-duplicated, latest
values, first datetime); AMBIGUOUS families are flagged on every trade so they can be reviewed.
"""
from __future__ import annotations

import collections
import datetime as dt
import re

import pandas as pd

KEY = ["bioguide_id", "owner", "transaction_date_iso", "asset_id", "transaction_type", "amount"]
SALES = {"Sale (Full)", "Sale (Partial)"}
CORRECTION_PASSES = [
    ("amount", ["bioguide_id", "owner", "transaction_date_iso", "asset_id", "transaction_type"]),
    ("owner", ["bioguide_id", "transaction_date_iso", "asset_id", "transaction_type", "amount"]),
    ("date", ["bioguide_id", "owner", "asset_id", "transaction_type", "amount"]),
    ("sale_type", ["bioguide_id", "owner", "transaction_date_iso", "asset_id", "amount", "is_sale"]),
    ("type", ["bioguide_id", "owner", "transaction_date_iso", "asset_id", "amount"]),
    ("asset", ["bioguide_id", "owner", "transaction_date_iso", "asset_name_norm", "transaction_type", "amount"]),
    ("asset_replaced", ["bioguide_id", "owner", "transaction_date_iso", "transaction_type", "amount"]),
]
# The weakest passes pair only inside an amendment that also repeats at least one trade exactly
# (a restatement). Otherwise a lone new line could be mistaken for a correction.
NEEDS_RESTATEMENT = {"type", "asset_replaced"}
# Fields compared to decide whether a pairing corrected anything.
COMPARED = ["owner", "transaction_date_iso", "ticker", "asset_name", "asset_type", "transaction_type", "amount"]


def norm_name(text: str) -> str:
    """Lower-case, punctuation removed, dates written MM/DD/YYYY turned into YYYY-MM-DD first
    (eFD changed the format of bond maturity dates inside asset names over time)."""
    text = re.sub(r"\b(\d{2})/(\d{2})/(\d{4})\b", r"\3-\1-\2", text)
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def asset_id(ticker: str, asset_name: str, embedded: str = "") -> str:
    """Asset identity for matching versions of a trade: the ticker, else a ticker written inside the
    asset name ("AAPL-Apple Inc." -> AAPL; used for matching only, not accepted as the ticker until
    verified), else the normalised asset name."""
    return ticker or embedded or "name:" + norm_name(asset_name)


def _key(row: dict, fields: list[str]) -> tuple:
    return tuple(row[f] for f in fields)


def link_amendments(filings: pd.DataFrame, rows_by_ptr: dict[str, list[dict]],
                    paper: pd.DataFrame, scrape_start: dt.date) -> dict[str, dict]:
    """For each amendment ptr_id: linked earlier ptr_ids, how they were found, and notes."""
    out = {}
    by_senator = {b: g.sort_values(["datetime_received", "ptr_id"]) for b, g in filings.groupby("bioguide_id")}
    paper_by = paper.groupby("bioguide_id")["date_received"].apply(set).to_dict() if len(paper) else {}
    for _, a in filings[filings["is_amendment"]].iterrows():
        g = by_senator[a["bioguide_id"]]
        earlier = g[(g["datetime_received"] < a["datetime_received"])
                    | ((g["datetime_received"] == a["datetime_received"]) & (g["ptr_id"] < a["ptr_id"])
                       & ~g["is_amendment"])]
        a_keys = collections.Counter(_key(r, KEY) for r in rows_by_ptr.get(a["ptr_id"], []))
        linked, basis = [], {}
        for _, e in earlier.iterrows():
            by_title = e["title_date"] == a["title_date"] or e["date_received"] == a["title_date"]
            e_keys = {_key(r, KEY) for r in rows_by_ptr.get(e["ptr_id"], [])}
            by_overlap = bool(e_keys & set(a_keys))
            if by_title or by_overlap:
                linked.append(e["ptr_id"])
                basis[e["ptr_id"]] = "+".join(x for x, ok in (("title", by_title), ("overlap", by_overlap)) if ok)
        notes = []
        if not linked:
            t = a["title_date"]
            near = {t, (dt.date.fromisoformat(t) - dt.timedelta(days=1)).isoformat()} if t else set()
            if near & paper_by.get(a["bioguide_id"], set()):
                notes.append("original is a paper filing")
            if t and t < scrape_start.isoformat():
                notes.append(f"original ({t}) predates the scrape start")
            if not notes:
                notes.append("no earlier filing found")
        out[a["ptr_id"]] = {"linked": linked, "basis": basis, "notes": "; ".join(notes)}
    return out


class TradeBook:
    """Unique trades per senator, built filing by filing in the order they became public."""

    def __init__(self):
        self.trades: list[dict] = []
        self.by_senator: dict[str, list[int]] = collections.defaultdict(list)
        self.row_map: list[dict] = []          # one entry per raw row: which trade it became/joined
        self.corrections: list[dict] = []

    def new_trade(self, row: dict, filing: pd.Series) -> int:
        i = len(self.trades)
        t = {**row, "trade_id": f"T{i + 1:05d}", "first_ptr_id": filing["ptr_id"],
             "first_datetime": filing["datetime_received"], "first_date_received": filing["date_received"],
             "first_is_amendment": bool(filing["is_amendment"]), "ptr_ids": [filing["ptr_id"]],
             "row_ids": [row["row_id"]], "latest_ptr_id": filing["ptr_id"], "corrected_fields": set(),
             "amendment_classes": set()}
        self.trades.append(t)
        self.by_senator[row["bioguide_id"]].append(i)
        self.row_map.append({"row_id": row["row_id"], "trade_id": t["trade_id"], "role": "first_report",
                             "match_pass": ""})
        return i

    def merge(self, i: int, row: dict, filing: pd.Series, how: str, role: str) -> None:
        t = self.trades[i]
        changed = [f for f in COMPARED if t[f] != row[f]]
        if changed and filing["is_amendment"]:
            for f in changed:
                self.corrections.append({"trade_id": t["trade_id"], "field": f, "old": t[f], "new": row[f],
                                         "amendment_ptr_id": filing["ptr_id"], "match_pass": how})
                t["corrected_fields"].add(f)
            for f in COMPARED + ["asset_id", "asset_name_norm", "is_sale", "ticker_raw", "comment"]:
                t[f] = row[f]
        if filing["ptr_id"] not in t["ptr_ids"]:
            t["ptr_ids"].append(filing["ptr_id"])
        t["row_ids"].append(row["row_id"])
        t["latest_ptr_id"] = filing["ptr_id"]
        self.row_map.append({"row_id": row["row_id"], "trade_id": t["trade_id"], "role": role, "match_pass": how})


def pair(rows: list[dict], trades: list[int], book: TradeBook, fields: list[str], unique_only: bool) -> list[tuple]:
    """Pair rows with trade indices on `fields`. Returns [(row, trade_index)]; mutates neither list."""
    r_groups, t_groups = collections.defaultdict(list), collections.defaultdict(list)
    for r in rows:
        r_groups[_key(r, fields)].append(r)
    for i in trades:
        t_groups[_key(book.trades[i], fields)].append(i)
    out = []
    for k, rs in r_groups.items():
        ts = t_groups.get(k, [])
        if not ts:
            continue
        if unique_only and (len(rs) != 1 or len(ts) != 1):
            continue
        out.extend(zip(rs, ts))
    return out


def build_trades(rows: pd.DataFrame, filings: pd.DataFrame, links: dict[str, dict]) -> tuple[TradeBook, pd.DataFrame]:
    """Process every filing in public order. Returns the book and the amendment classification table."""
    rows_by_ptr: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows.to_dict("records"):
        rows_by_ptr[r["ptr_id"]].append(r)
    book = TradeBook()
    trades_of_ptr: dict[str, set[int]] = collections.defaultdict(set)
    classes = []
    for _, f in filings.sort_values(["datetime_received", "ptr_id"]).iterrows():
        frows = rows_by_ptr.get(f["ptr_id"], [])
        remaining = list(frows)
        counts = collections.Counter()
        family: list[int] = []
        if f["is_amendment"]:
            link = links[f["ptr_id"]]
            trades_of_ptr_before = {p: set(trades_of_ptr[p]) for p in link["linked"]}
            family = sorted(set().union(*[trades_of_ptr[p] for p in link["linked"]])) if link["linked"] else []
            free = list(family)
            paired_trades: set[int] = set()
            maybe_replacement = False
            for how, fields in [("exact", KEY)] + CORRECTION_PASSES:
                pairs = pair(remaining, free, book, fields, unique_only=how != "exact")
                if how in NEEDS_RESTATEMENT and not counts["exact"]:
                    maybe_replacement |= bool(pairs)
                    continue
                for r, i in pairs:
                    book.merge(i, r, f, how, "restated_in_amendment")
                    trades_of_ptr[f["ptr_id"]].add(i)
                    counts[how] += 1
                used_r = {id(r) for r, _ in pairs}
                used_t = {i for _, i in pairs}
                paired_trades |= used_t
                remaining = [r for r in remaining if id(r) not in used_r]
                free = [i for i in free if i not in used_t]
        # Any filing: exact repeats of the senator's trades from OTHER filings (re-filed trades).
        if remaining and frows:
            senator = frows[0]["bioguide_id"]
            others = [i for i in book.by_senator[senator]
                      if f["ptr_id"] not in book.trades[i]["ptr_ids"] and i not in trades_of_ptr[f["ptr_id"]]]
            pairs = pair(remaining, others, book, KEY, unique_only=False)
            for r, i in pairs:
                book.merge(i, r, f, "exact_other_filing", "repeated_from_other_filing")
                trades_of_ptr[f["ptr_id"]].add(i)
                counts["exact_other_filing"] += 1
            used_r = {id(r) for r, _ in pairs}
            remaining = [r for r in remaining if id(r) not in used_r]
        for r in remaining:
            trades_of_ptr[f["ptr_id"]].add(book.new_trade(r, f))
        if f["is_amendment"]:
            link = links[f["ptr_id"]]
            n_paired = len(paired_trades)
            n_family = len(family)
            titled = [p for p in link["linked"] if "title" in link["basis"][p]]
            overlapping = [p for p in titled if trades_of_ptr_before[p] & paired_trades]
            primary = overlapping or titled or link["linked"]
            target = set().union(*[trades_of_ptr_before[p] for p in primary]) if primary else set()
            n_target_repeated = len(target & paired_trades)
            if not link["linked"]:
                cls = "UNLINKED"
            elif n_paired == 0:
                cls = "ADDITIVE" if frows and not maybe_replacement else "AMBIGUOUS"
            elif n_target_repeated == len(target):
                cls = "FULL_RESTATEMENT"
            else:
                cls = "AMBIGUOUS"
            for i in set(family) | trades_of_ptr[f["ptr_id"]]:
                book.trades[i]["amendment_classes"].add(cls)
            n_corr = sum(v for k, v in counts.items() if k not in ("exact", "exact_other_filing"))
            classes.append({
                "ptr_id": f["ptr_id"], "bioguide_id": f["bioguide_id"], "senator": f["senator"],
                "date_received": f["date_received"], "datetime_received": f["datetime_received"],
                "title_date": f["title_date"], "amendment_number": f["amendment_number"],
                "linked_ptr_ids": " ".join(link["linked"]), "amended_ptr_ids": " ".join(primary),
                "link_basis": " ".join(f"{p[:8]}:{b}" for p, b in link["basis"].items()),
                "n_rows": len(frows), "n_family_trades": n_family, "n_repeated_exact": counts["exact"],
                "n_repeated_corrected": n_corr, "n_repeated_other_filing": counts["exact_other_filing"],
                "n_new": len(remaining), "n_family_not_repeated": n_family - n_paired,
                "n_amended_report_trades": len(target), "n_amended_report_not_repeated": len(target) - n_target_repeated,
                "correction_passes": " ".join(f"{k}:{v}" for k, v in counts.items()
                                              if k not in ("exact", "exact_other_filing")),
                "class": cls, "note": "; ".join(x for x in [link["notes"], "a new line could instead replace an "
                                                            "earlier one (type or asset changed)" if maybe_replacement else ""] if x),
            })
    return book, pd.DataFrame(classes)
