"""First-look counts (outputs/phase1_summary.md) and the Phase 1 data-quality log
(outputs/data_quality.md). Counts only: no prices and no returns of any kind.

"Year" means the year the PTR was RECEIVED (the disclosure date), unless a table says otherwise.

The key number is a rough preview of the Phase 2 sample. A transaction counts when:
  - its PTR was received inside the default analysis window (A06: 2021-09-01 to 2026-08-31);
  - the filer is matched to a senator with high confidence (low-confidence and unmatched names
    are left out rather than guessed);
  - its transaction date falls within that senator's Senate service (A05);
  - the owner is Self or Joint (A01);
  - a ticker is present (not "--" or blank);
  - the asset type is "Stock", or "Other Securities"/"Other" with a ticker (a rough ETF proxy until
    ETFs are classified properly in Phase 2). eFD's form labels this type "Other" in the filings
    seen so far; "Other" with a ticker is mostly ETFs plus some mutual funds, so the table also
    counts tickers that look like mutual funds (five letters ending in X).
Amendments are NOT de-duplicated yet (Phase 2 keeps the latest version), so an amended filing's
transactions can appear twice; the table shows how many rows come from amendment filings.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pandas as pd

from src.config import analysis_window
from src.quality import write_section
from .download import FAILURES, MANIFEST
from .legislators import TERMS_CSV, check_departures
from .names import MATCHES, filer_key
from .parse import TRANSACTIONS, VALIDATION

SUMMARY = Path("outputs/phase1_summary.md")
QUALITY = Path("outputs/data_quality.md")
PAPER_LOG = Path("data/interim/paper_filings.csv")
MISSING_TICKERS = {"--", "", "N/A", "n/a"}
ETF_PROXY_TYPES = ["Other Securities", "Other"]
MUTUAL_FUND_LIKE = r"^[A-Z]{4}X$"
OWNERS = ["Self", "Joint", "Spouse", "Child"]


def md(df: pd.DataFrame, index: bool = True) -> str:
    return df.to_markdown(index=index)


def load() -> dict:
    man = pd.read_csv(MANIFEST, dtype=str, keep_default_na=False)
    tx = pd.read_csv(TRANSACTIONS, dtype=str, keep_default_na=False)
    matches = pd.read_csv(MATCHES, dtype=str, keep_default_na=False)
    terms = pd.read_csv(TERMS_CSV, dtype=str, keep_default_na=False)
    val = pd.read_csv(VALIDATION, dtype=str, keep_default_na=False)
    for df in (man, tx):
        df["year"] = df["date_received"].str[:4]
    tx["filer_key"] = [filer_key(f, l) for f, l in zip(tx["first_name"], tx["last_name"])]
    tx = tx.merge(matches[["filer_key", "bioguide_id", "matched_name", "confidence"]], on="filer_key", how="left")
    return {"man": man, "tx": tx, "matches": matches, "terms": terms, "val": val}


def in_service(tx: pd.DataFrame, terms: pd.DataFrame) -> pd.Series:
    """True where the transaction date falls inside one of the matched senator's terms."""
    spans: dict[str, list[tuple[str, str]]] = {}
    for b, s, e in zip(terms["bioguide_id"], terms["term_start"], terms["term_end"]):
        spans.setdefault(b, []).append((s, e))
    return pd.Series([bool(d) and any(s <= d <= e for s, e in spans.get(b, []))
                      for b, d in zip(tx["bioguide_id"], tx["transaction_date_iso"])], index=tx.index)


def key_filter(tx: pd.DataFrame, cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(rows passing every key-number condition, step-by-step waterfall of row counts)."""
    start, end = analysis_window(cfg)
    steps = []
    d = tx
    steps.append(("All parsed transaction rows (all years)", len(d)))
    d = d[(d["date_received"] >= start.isoformat()) & (d["date_received"] <= end.isoformat())]
    steps.append((f"PTR received {start} to {end} (default window)", len(d)))
    d = d[d["confidence"] == "high"]
    steps.append(("Filer matched to a senator with high confidence", len(d)))
    d = d[d["in_service"]]
    steps.append(("Transaction date inside the filer's Senate service", len(d)))
    d = d[d["owner"].isin(cfg["universe"]["owners"])]
    steps.append(("Owner is " + " or ".join(cfg["universe"]["owners"]), len(d)))
    d = d[~d["ticker"].isin(MISSING_TICKERS)]
    steps.append(("Ticker present", len(d)))
    d = d[d["asset_type"].isin(["Stock"] + ETF_PROXY_TYPES)]
    steps.append(('Asset type "Stock", or "Other Securities"/"Other" with a ticker (ETF proxy)', len(d)))
    return d, pd.DataFrame(steps, columns=["Condition (cumulative)", "Rows left"])


def type_group(t: str) -> str:
    if t == "Purchase":
        return "Purchase"
    if t.startswith("Sale"):
        return t if t in ("Sale (Full)", "Sale (Partial)") else "Sale (other)"
    return "Exchange" if t == "Exchange" else "Other"


def filings_by_year(man: pd.DataFrame) -> pd.DataFrame:
    g = man.groupby("year")
    out = pd.DataFrame({
        "Filings": g.size(),
        "Electronic": g.apply(lambda x: (x["kind"] == "electronic").sum()),
        "Paper": g.apply(lambda x: (x["kind"] == "paper").sum()),
        "Amendments": g.apply(lambda x: (x["is_amendment"] == "True").sum()),
        "Amendments (paper)": g.apply(lambda x: ((x["is_amendment"] == "True") & (x["kind"] == "paper")).sum()),
        "Downloaded": g.apply(lambda x: (x["download_status"] == "downloaded").sum()),
        "Failed/pending": g.apply(lambda x: x["download_status"].str.match(r"failed|pending").sum()),
        'Label "Senator"': g.apply(lambda x: (x["filer_type_label"] == "Senator").sum()),
        'Label "Former Senator"': g.apply(lambda x: (x["filer_type_label"] == "Former Senator").sum()),
        'Label "Candidate"': g.apply(lambda x: (x["filer_type_label"] == "Candidate").sum()),
    })
    out.loc["Total"] = out.sum()
    return out


def with_total(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Total"] = df.sum(axis=1)
    df.loc["Total"] = df.sum()
    return df


def run(cfg: dict) -> None:
    D = load()
    man, tx, matches, terms, val = D["man"], D["tx"], D["matches"], D["terms"], D["val"]
    tx["in_service"] = in_service(tx, terms)
    start, end = analysis_window(cfg)
    in_window = (tx["date_received"] >= start.isoformat()) & (tx["date_received"] <= end.isoformat())
    key, waterfall = key_filter(tx, cfg)

    # ---- tables
    fby = filings_by_year(man)
    owner = tx["owner"].where(tx["owner"].isin(OWNERS), tx["owner"].replace("", "(blank)"))
    t_owner = with_total(pd.crosstab(tx["year"], owner))
    t_asset = pd.DataFrame({"All years": tx["asset_type"].replace("", "(blank)").value_counts(),
                            "Default window": tx.loc[in_window, "asset_type"].replace("", "(blank)").value_counts()}
                           ).fillna(0).astype(int).sort_values("All years", ascending=False)
    t_asset.loc["Total"] = t_asset.sum()
    t_type = pd.DataFrame({"All years": tx["transaction_type"].replace("", "(blank)").value_counts(),
                           "Default window": tx.loc[in_window, "transaction_type"].replace("", "(blank)").value_counts()}
                          ).fillna(0).astype(int).sort_values("All years", ascending=False)
    t_type.loc["Total"] = t_type.sum()

    missing = tx["ticker"].isin(MISSING_TICKERS)
    t_missing = pd.DataFrame({"All years": tx.loc[missing, "asset_type"].replace("", "(blank)").value_counts(),
                              "Default window": tx.loc[missing & in_window, "asset_type"].replace("", "(blank)").value_counts()}
                             ).fillna(0).astype(int).sort_values("All years", ascending=False)
    t_missing.loc["Total"] = t_missing.sum()

    k = key.assign(group=key["transaction_type"].map(type_group),
                   period=key["year"].map(lambda y: {str(start.year): f"{y} (from {start:%d %b})",
                                                     str(end.year): f"{y} (to {end:%d %b})"}.get(y, y)))
    t_key = pd.crosstab(k["period"], k["group"])
    for c in ["Purchase", "Sale (Full)", "Sale (Partial)", "Sale (other)", "Exchange", "Other"]:
        if c not in t_key:
            t_key[c] = 0
    t_key["Sales (all)"] = t_key[["Sale (Full)", "Sale (Partial)", "Sale (other)"]].sum(axis=1)
    t_key["Total"] = t_key[["Purchase", "Sales (all)", "Exchange", "Other"]].sum(axis=1)
    t_key["of which in amendment filings"] = k.groupby("period")["is_amendment"].apply(lambda s: (s == "True").sum())
    proxy = k["asset_type"].isin(ETF_PROXY_TYPES)
    t_key["of which ETF proxy (Other with ticker)"] = proxy.groupby(k["period"]).sum()
    t_key["of which ETF proxy with mutual-fund-like ticker"] = \
        (proxy & k["ticker"].str.match(MUTUAL_FUND_LIKE)).groupby(k["period"]).sum()
    t_key = t_key[["Purchase", "Sale (Full)", "Sale (Partial)", "Sale (other)", "Sales (all)", "Exchange",
                   "Other", "Total", "of which in amendment filings", "of which ETF proxy (Other with ticker)",
                   "of which ETF proxy with mutual-fund-like ticker"]]
    t_key = t_key.fillna(0).astype(int)
    t_key.loc["Total"] = t_key.sum()

    # senators
    tx_matched = tx[tx["confidence"] == "high"]
    n_filer_names = matches.shape[0]
    n_senators_filing = man.assign(k=[filer_key(f, l) for f, l in zip(man["first_name"], man["last_name"])]) \
        .merge(matches[["filer_key", "bioguide_id"]], left_on="k", right_on="filer_key")["bioguide_id"]
    n_senators_filing = n_senators_filing[n_senators_filing != ""].nunique()
    n_senators_tx = tx_matched["bioguide_id"].nunique()
    n_senators_key = key["bioguide_id"].nunique()
    top = key.groupby(["bioguide_id", "matched_name"]).size().sort_values(ascending=False)
    top5 = top.head(5).reset_index(name="Transactions")
    top5["Share of key-number transactions"] = (top5["Transactions"] / len(key)).map("{:.1%}".format)
    top5 = top5.rename(columns={"matched_name": "Senator", "bioguide_id": "bioguide_id"})
    party_state = terms.sort_values("term_start").groupby("bioguide_id").last()[["party", "state"]]
    top5 = top5.join(party_state, on="bioguide_id")[["Senator", "party", "state", "bioguide_id",
                                                     "Transactions", "Share of key-number transactions"]]
    top5_share = top.head(5).sum() / len(key) if len(key) else 0

    review = matches[(matches["confidence"] != "high")]
    bad_dates = tx[tx["transaction_date_iso"] == ""]
    bad_rows = val[val["row_count_ok"] != "True"]
    bad_owner = val[val["owner_counts_ok"] != "True"]

    # sanity check: matched filers none of whose transactions fall inside service
    per = tx_matched.groupby(["filer_key", "matched_name"])["in_service"].agg(["size", "sum"]).reset_index()
    suspicious = per[per["sum"] == 0]
    outside = tx_matched[~tx_matched["in_service"]]
    outside_by = outside.groupby("matched_name").size().sort_values(ascending=False)

    # ---- phase1_summary.md
    L = [f"# Phase 1 summary: first-look counts",
         "",
         f"_Generated by `python run_all.py` (stage scrape) on {dt.date.today()}. Counts only: no prices "
         f"or returns. \"Year\" is the year the PTR was received (the disclosure date). Paper filings are "
         f"scanned images and have no parsed transactions._",
         "",
         "## 1. Filings by year received",
         "",
         "All filer types (A05). The eFD filer-type label is today's status, shown for reference only.",
         "",
         md(fby),
         "",
         "## 2. Transactions by year received and owner",
         "",
         "Every row of every downloaded electronic PTR, before any filtering.",
         "",
         md(t_owner),
         "",
         "## 3. Transactions by asset type",
         "",
         f"\"Default window\" = PTR received {start} to {end}.",
         "",
         md(t_asset),
         "",
         "## 4. Transactions by transaction type",
         "",
         md(t_type),
         "",
         "## 5. Senators",
         "",
         f"- Distinct filer names in the listing: **{n_filer_names}** "
         f"({(matches['confidence'] == 'high').sum()} matched to a senator with high confidence, "
         f"{len(review)} unmatched or low confidence; see section 8).",
         f"- Distinct senators (bioguide ids) with at least one filing: **{n_senators_filing}**; "
         f"with at least one parsed transaction: **{n_senators_tx}**; "
         f"with at least one key-number transaction: **{n_senators_key}**.",
         f"- The top 5 senators account for **{top5_share:.1%}** of the {len(key):,} key-number transactions:",
         "",
         md(top5, index=False),
         "",
         "## 6. Missing tickers",
         "",
         f"**{missing.sum():,}** of {len(tx):,} rows ({missing.mean():.1%}) have no ticker "
         f"(shown as \"--\" or blank); {(missing & in_window).sum():,} of them are in the default window. "
         "By asset type:",
         "",
         md(t_missing),
         "",
         "## 7. THE KEY NUMBER: copyable purchases and sales in the default window",
         "",
         f"PTR received {start} to {end}; filer matched to a senator with high confidence; transaction "
         "date inside that senator's Senate service; owner Self or Joint; ticker present; asset type "
         "\"Stock\", or \"Other Securities\"/\"Other\" with a ticker (rough ETF proxy until Phase 2 "
         "classifies ETFs). eFD labels this type \"Other\" in these filings; with a ticker it is mostly "
         "ETFs plus some mutual funds, counted separately below (five-letter tickers ending in X).",
         "",
         "**Caveat:** amendments are not de-duplicated yet (Phase 2 keeps the latest version only), so "
         "rows from an amended filing can appear twice. The \"of which in amendment filings\" column shows "
         "the most this can inflate each count.",
         "",
         md(t_key),
         "",
         "How each condition narrows the sample:",
         "",
         md(waterfall, index=False),
         "",
         "## 8. Filer names to review",
         "",
    ]
    if len(review):
        L += ["These were not matched with high confidence and are left OUT of the key number. Settle each "
              "one in `config/name_overrides.yaml` (a bioguide_id, or null for \"not a senator\").", "",
              md(review[["first_name", "last_name", "office_texts", "filer_type_labels", "n_filings",
                         "first_received", "last_received", "method", "confidence", "matched_name",
                         "bioguide_id", "score", "runner_up", "note"]], index=False)]
    else:
        L += ["None: every filer name matched a senator with high confidence."]
    L += ["", "Full match table: `data/interim/filer_matches.csv`. Data-quality log: `outputs/data_quality.md`.", ""]
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text("\n".join(L))

    # ---- data_quality.md (Phase 1 sections)
    failures = json.loads(FAILURES.read_text()) if FAILURES.exists() else {}
    paper = man[man["kind"] == "paper"][["filer_name", "office_text", "filer_type_label", "date_received",
                                         "report_title", "url"]]
    paper.to_csv(PAPER_LOG, index=False)
    paper_by = paper.groupby("filer_name").size().sort_values(ascending=False).rename("Paper filings").to_frame()
    page_diff = man[man["page_date_differs"] == "True"]
    no_time = man[(man["download_status"] == "downloaded") & (man["time_received"] == "")]
    dep_issues = check_departures(terms.assign(senate_class=terms["senate_class"]).to_dict("records"),
                                  dt.date.today())
    early = terms[terms["ended_early"] == "True"][["full_name", "state", "party", "term_start", "term_end",
                                                    "scheduled_end", "start_how", "end_type"]]
    Q = ["## Phase 1: scrape", "",
         f"- Filings in the eFD listing (received {cfg['data']['scrape_start']} to {cfg['data']['scrape_end']}, "
         f"all filer types): **{len(man):,}**; electronic **{(man['kind'] == 'electronic').sum():,}**, "
         f"paper **{(man['kind'] == 'paper').sum():,}**, other **{(~man['kind'].isin(['electronic', 'paper'])).sum()}**.",
         f"- Electronic PTRs downloaded: **{(man['download_status'] == 'downloaded').sum():,}**; failed: "
         f"**{man['download_status'].str.startswith('failed').sum()}**; pending: "
         f"**{(man['download_status'] == 'pending').sum()}**.",
         f"- Listing fetched on or before the scrape end date is refreshed automatically on the next run "
         f"(the 2026 listing is incomplete until after {cfg['data']['scrape_end']}).",
         "", "### Download failures", ""]
    Q += [md(pd.DataFrame(failures).T)] if failures else ["None."]
    Q += ["", "### Paper filings (excluded, D05)", "",
          f"**{len(paper)}** paper filings are scanned images and cannot be parsed; they are excluded. "
          f"The full list (senator, date, link) is in `{PAPER_LOG}`. By filer:", "", md(paper_by), "",
          "### Parse validation", "",
          f"Each of the {len(val):,} downloaded PTRs was checked three ways: rows parsed, `<tbody>` rows "
          "counted by a separate parser, and the page's own \"(N transactions total)\" line.", "",
          f"- Row-count mismatches: **{len(bad_rows)}**"]
    if len(bad_rows):
        Q += ["", md(bad_rows[["ptr_id", "filer_name", "date_received", "has_table", "parsed_rows",
                               "tbody_rows", "stated_total"]], index=False), ""]
    Q += [f"- Owner-count mismatches (page's \"N Self / N Spouse ...\" line vs parsed Owner column): "
          f"**{len(bad_owner)}**"]
    if len(bad_owner):
        Q += ["", md(bad_owner[["ptr_id", "filer_name", "date_received", "owner_detail"]], index=False), ""]
    Q += [f"- Transaction rows whose date could not be read as MM/DD/YYYY: **{len(bad_dates)}**"]
    if len(bad_dates):
        Q += ["", md(bad_dates[["ptr_id", "filer_name", "row_number", "transaction_date"]].head(50), index=False), ""]
    Q += [f"- Downloaded PTRs with no \"Filed ... @ time\" timestamp: **{len(no_time)}**",
          f"- PTRs whose page \"Filed\" date differs from the listing's date received: **{len(page_diff)}**"]
    if len(page_diff):
        Q += ["", md(page_diff[["ptr_id", "filer_name", "date_received", "filed_date_on_page",
                                "time_received"]], index=False), ""]
    Q += ["", "### Senate service dates (A05)", "",
          f"`{TERMS_CSV}`: {len(terms)} Senate terms ending on or after "
          f"{cfg['data']['service_dates']['terms_from']}, {terms['bioguide_id'].nunique()} senators. "
          f"{len(early)} terms ended before their scheduled 3 January end; the dataset records the actual "
          "last day for each, listed below. An appointee's term that ends at a special election is "
          "listed too.", "", md(early, index=False), "",
          "Checks for departures the dataset may NOT record (a successor in the same seat starting before "
          "the predecessor's recorded end; a historical senator with a future end date; a current "
          f"senator whose last term has ended): **{len(dep_issues)}** found.", ""]
    Q += [f"- {x}" for x in dep_issues] or []
    Q += ["", "### Filer name matching", "",
          f"{len(matches)} distinct filer names: " +
          ", ".join(f"{m} {(matches['method'] == m).sum()}" for m in ["override", "exact", "fuzzy", "ambiguous", "unmatched"]) +
          f". Unmatched or low-confidence: **{len(review)}** (listed in outputs/phase1_summary.md section 8; "
          "their transactions are left out of the key number).", "",
          f"- Matched filers none of whose transactions fall inside that senator's service (would suggest "
          f"the wrong person): **{len(suspicious)}**"]
    if len(suspicious):
        Q += ["", md(suspicious.rename(columns={"size": "rows", "sum": "in service"}), index=False), ""]
    Q += [f"- Transactions by high-confidence matched filers dated OUTSIDE Senate service (excluded by A05 "
          f"in Phase 2): **{len(outside):,}** of {len(tx_matched):,}."]
    if len(outside_by):
        Q += ["", md(outside_by.rename("Rows outside service").to_frame()), ""]
    write_section(1, Q, QUALITY)
    print(f"  [summary] key number: {len(key):,} transactions -> {SUMMARY}; quality log -> {QUALITY}")
