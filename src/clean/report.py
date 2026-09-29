"""Phase 2 outputs: data/processed/*.csv, data/interim audit files and the Phase 2 section of
outputs/data_quality.md. Counts and disclosed dollar ranges only: no prices, no returns."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.quality import write_section
from .build import CLEAN_COLUMNS, EXCLUSION_COLUMNS, REASONS, RECORD_COLUMNS, parse_amount

PROCESSED = Path("data/processed")
INTERIM = Path("data/interim")
TRADES_CLEAN = PROCESSED / "trades_clean.csv"
TRADE_RECORDS = PROCESSED / "trade_records.csv"
OVERRIDES_LOG = INTERIM / "asset_name_overrides_log.csv"
TICKERS = PROCESSED / "tickers.csv"
EXCLUSIONS = PROCESSED / "exclusions.csv"
AMENDMENTS = INTERIM / "amendments.csv"
CORRECTIONS = INTERIM / "amendment_corrections.csv"
RECOVERY = INTERIM / "ticker_recovery.csv"
AMOUNTS = INTERIM / "amount_strings.csv"
SUBSTANTIVE = ["owner", "transaction_date_iso", "ticker", "transaction_type", "amount"]


def md(df: pd.DataFrame, index: bool = False) -> str:
    return df.to_markdown(index=index, floatfmt=",.0f") if len(df) else "_None._"


def pct(x: float) -> str:
    return f"{x:.1%}"


def ticker_table(tr: pd.DataFrame) -> pd.DataFrame:
    """Every ticker that reached the instrument check (3/5/10-year windows, any owner)."""
    g = tr[tr["reached_instrument_step"]].groupby("ticker")
    t = pd.DataFrame({
        "n_trades": g.size(), "n_in_trades_clean": g["in_trades_clean"].sum(), "n_in_scope": g["in_scope"].sum(),
        "first_trade_date": g["transaction_date"].min(), "last_trade_date": g["transaction_date"].max(),
        "first_disclosure_date": g["disclosure_date"].min(), "last_disclosure_date": g["disclosure_date"].max(),
        "efd_asset_names": g["asset_name"].agg(lambda s: " | ".join(s.value_counts().index[:3])),
        "ticker_sources": g["ticker_source"].agg(lambda s: " ".join(sorted(set(s)))),
    })
    first = g[["price_ticker", "renamed", "instrument_status", "instrument_type", "yahoo_type", "exchange", "exchange_name", "listing", "is_etf", "is_otc",
               "instrument_unresolved", "yahoo_name_mismatch", "yahoo_name"]].first()
    return t.join(first).reset_index().sort_values("ticker")


def waterfall(rows: pd.DataFrame, trades: pd.DataFrame) -> pd.DataFrame:
    counts = rows["reason_code"].value_counts()
    label = dict(REASONS)
    out, left = [], len(rows)
    out.append({"Step": 0, "Reason code": "", "What happens": "All parsed transaction rows (Phase 1)",
                "Removed": "", "Left": left})
    step = 0
    for code, _ in REASONS:
        n = int(counts.get(code, 0))
        if code != "ETF_EXCLUDED" or n:
            step += 1
            left -= n
            out.append({"Step": step, "Reason code": code, "What happens": label[code], "Removed": n, "Left": left})
        if code == "DUPLICATE_REFILED":
            out.append({"Step": "", "Reason code": "", "What happens": "= unique trades", "Removed": "",
                        "Left": len(trades)})
    out.append({"Step": "", "Reason code": "", "What happens": "= IN-SCOPE TRADES (headline sample)",
                "Removed": "", "Left": int(trades["in_scope"].sum())})
    return pd.DataFrame(out)


def lag_table(s: pd.DataFrame, top5: list[tuple[str, str]]) -> pd.DataFrame:
    def row(name, d):
        lag = d["filing_lag_days"]
        return {"Group": name, "Trades": len(d), "Median lag (days)": lag.median(),
                "75th pct": lag.quantile(0.75), "95th pct": lag.quantile(0.95),
                "Share over 45 days": pct((lag > 45).mean()) if len(d) else ""}
    out = [row("All in-scope trades", s)]
    for bid, name in top5:
        out.append(row(name, s[s["bioguide_id"] == bid]))
    out.append(row("All other senators", s[~s["bioguide_id"].isin([b for b, _ in top5])]))
    return pd.DataFrame(out)


def run_report(cfg: dict, R: dict) -> None:
    tr, rows, amend, corr, rec = R["trades"], R["rows"], R["amendments"], R["corrections"], R["recovery"]
    start, end = R["window"]
    PROCESSED.mkdir(parents=True, exist_ok=True)
    clean = tr[tr["in_trades_clean"]].sort_values(["disclosure_datetime", "trade_id"])
    clean[CLEAN_COLUMNS].to_csv(TRADES_CLEAN, index=False)
    recs = R["records"]
    # every record of a trade in trades_clean, plus (5A.2) every record in scope but for the window and the owner from
    # the scrape start, so the 10-year window's warm-up (from 2016-01-01) has its records
    recs[recs["in_trades_clean"] | recs["in_scope_ex_window_owner"]].sort_values(["disclosure_datetime", "record_id"])[RECORD_COLUMNS].to_csv(
        TRADE_RECORDS, index=False)
    R["overrides"].to_csv(OVERRIDES_LOG, index=False)
    tickers = ticker_table(tr)
    tickers.to_csv(TICKERS, index=False)
    excl = rows[~((rows["role"] == "first_report") & rows["trade_id"].map(tr.set_index("trade_id")["in_scope"]).fillna(False).astype(bool))]
    excl = excl.rename(columns={"senator": "senator"})
    excl[EXCLUSION_COLUMNS].to_csv(EXCLUSIONS, index=False)
    amend.to_csv(AMENDMENTS, index=False)
    corr.to_csv(CORRECTIONS, index=False)
    rec.to_csv(RECOVERY, index=False)
    amounts = rows.groupby("amount").size().rename("rows").reset_index()
    amounts = pd.concat([amounts, pd.DataFrame([parse_amount(a) for a in amounts["amount"]])], axis=1)
    amounts = amounts.sort_values("amount_lower")
    amounts.to_csv(AMOUNTS, index=False)
    amounts_md = amounts.assign(**{c: amounts[c].map(lambda v: "" if pd.isna(v) else f"{v:,.1f}".replace(".0", ""))
                                   for c in ["amount_lower", "amount_upper", "amount_mid"]})

    s = tr[tr["in_scope"]].copy()
    s["year"] = s["disclosure_date"].str[:4]
    L = ["## Phase 2: clean", "",
         f"_Stage `clean` of `python run_all.py`. Default window: disclosures {start} to {end} "
         f"({cfg['analysis']['window_years']} years). Owners: {', '.join(cfg['universe']['owners'])}. "
         f"ETFs included: {cfg['universe']['include_etfs']}. Counts and disclosed dollar ranges only; no prices "
         "or returns. Files: `data/processed/trades_clean.csv` (every unique trade in the 3/5/10-year windows "
         "that passes every filter except owner, `in_scope` = headline sample), `data/processed/exclusions.csv` "
         "(every raw row that is not an in-scope trade, with its reason), `data/processed/tickers.csv`._", ""]

    # 1. waterfall
    wf = waterfall(rows, tr)
    L += ["### 1. Waterfall: raw rows to in-scope trades", "",
          "Each row is removed at the FIRST step it fails, in this order. Steps 1-2 count raw rows; from step 3 on, "
          "each row is one unique trade (a trade reported in several filings counts once).", "", md(wf), ""]
    by_owner = pd.crosstab(rows["reason_code"].replace("", "(in scope)"), rows["owner"])
    by_owner = by_owner.reindex([c for c, _ in REASONS if c in by_owner.index] + ["(in scope)"]).fillna(0).astype(int)
    by_owner.loc["Total"] = by_owner.sum()
    L += ["Owner type by reason (A01: Spouse and Child trades are counted, not silently dropped):", "",
          md(by_owner, index=True), ""]
    asset = rows[rows["reason_code"] == "ASSET_TYPE"]["reason_detail"].value_counts().rename("Trades").reset_index()
    asset.columns = ["eFD asset type", "Trades"]
    L += ["ASSET_TYPE detail (in-window trades only; earlier steps took the rest):", "", md(asset), ""]
    oth = rows[rows["reason_code"].isin(["OTHER_INSTRUMENT", "NON_US_LISTING"])].groupby(
        ["reason_code", "reason_detail"]).size().rename("Trades").reset_index()
    if len(oth):
        L += ["OTHER_INSTRUMENT / NON_US_LISTING detail (Yahoo type or exchange):", "", md(oth), ""]
    kept = rows[rows["kept_in_trades_clean"] & (rows["reason_code"] != "")]["reason_code"].value_counts()
    L += [f"Rows excluded from the headline sample but kept in trades_clean.csv for pre-registered variants: "
          + ", ".join(f"{k} {v:,}" for k, v in kept.items()) + " (OUTSIDE_WINDOW rows there fall inside the 3- or "
          "10-year window; OWNER rows are the V6 family trades).", ""]

    # 2. amendments
    cls = amend["class"].value_counts().reindex(["FULL_RESTATEMENT", "ADDITIVE", "AMBIGUOUS", "UNLINKED"]).fillna(0).astype(int)
    in_win = amend["date_received"].between(start.isoformat(), end.isoformat())
    cls_t = pd.DataFrame({"All amendments": cls,
                          "Received in default window": amend[in_win]["class"].value_counts().reindex(cls.index).fillna(0).astype(int)})
    n_dup_a = int((rows["reason_code"] == "DUPLICATE_AMENDMENT").sum())
    n_dup_r = int((rows["reason_code"] == "DUPLICATE_REFILED").sum())
    only_amend = tr[tr["first_is_amendment"]]
    corr_tr = tr[tr["corrected_fields"] != ""]
    subst = tr["corrected_fields"].str.split().map(lambda f: bool(set(f or []) & set(SUBSTANTIVE)))
    fields = corr.merge(tr[["trade_id", "in_scope"]], on="trade_id").groupby("field").agg(
        trades=("trade_id", "nunique"), in_scope_trades=("in_scope", "sum")).reset_index()
    L += ["### 2. Amendments", "",
          f"{len(amend)} electronic amendments. Each is linked to the earlier filing(s) it amends (same senator, "
          "filed earlier, same report title date and/or overlapping transactions) and classified (rules in "
          "`src/clean/amendments.py`; per-amendment detail in `data/interim/amendments.csv`).", "",
          md(cls_t, index=True), "",
          f"- Duplicate rows removed: **{n_dup_a + n_dup_r:,}** ({n_dup_a:,} restated in an amendment, "
          f"{n_dup_r:,} repeated from an unrelated earlier filing). Several identical lines inside one filing are "
          "separate trades and are kept.",
          f"- Trades that exist ONLY in an amendment (dated by the amendment, no look-ahead): **{len(only_amend):,}** "
          f"(in scope: **{int(only_amend['in_scope'].sum()):,}**).",
          f"- Trades whose fields an amendment corrected (corrected value used, original datetime kept): "
          f"**{len(corr_tr):,}** (in scope: **{int(corr_tr['in_scope'].sum()):,}**); with a substantive change "
          f"(owner, date, ticker, type or amount): **{int(subst.sum()):,}** (in scope: "
          f"**{int((subst & tr['in_scope']).sum()):,}**). By field (`data/interim/amendment_corrections.csv`):", "",
          md(fields), "",
          f"- UNLINKED amendments ({int(cls['UNLINKED'])}): no earlier electronic filing found. Reason: "
          + (", ".join(f"{v} {k}" for k, v in amend.loc[amend['class'] == 'UNLINKED', 'note'].str.replace(
              r"\(\d{4}-\d{2}-\d{2}\) ", "", regex=True).value_counts().items()) or "none")
          + ". Their rows count as first disclosed by the amendment.",
          f"- Trades touched by an AMBIGUOUS amendment: {int(tr['amendment_ambiguous'].sum()):,} "
          f"(in scope: **{int((tr['amendment_ambiguous'] & tr['in_scope']).sum()):,}**). Rule applied: keep every "
          "version's trades once (a trade missing from the amendment is NOT deleted). Flag: `amendment_ambiguous`.", ""]
    corr_t = tr[tr["corrected"] & tr["in_trades_clean"]]
    both = tr["in_scope"] & tr["in_scope_as_revised"]
    j3_only = tr["in_scope"] & ~tr["in_scope_as_revised"]
    v14_only = ~tr["in_scope"] & tr["in_scope_as_revised"]
    multi = recs[recs["in_trades_clean"] & (recs["n_records"] > 1)]
    pattern = corr_t.assign(orig=corr_t["orig_record_in_scope"].map({True: "original in scope", False: "original out"}),
                            late=corr_t["latest_record_in_scope"].map({True: "correction in scope", False: "correction out"}))
    pattern = pd.crosstab(pattern["orig"], pattern["late"]) if len(pattern) else pd.DataFrame()
    L += ["**As first published (J3, headline) vs as revised (V14).** A trade corrected by an amendment has two or "
          "more records: the original, effective at the first disclosure, and each corrected version, effective at "
          "its amendment's datetime (only changes of owner, date, asset, asset type, type or amount make a new record; "
          "a reworded asset name does not). Each record passes the filters on its own values and date. "
          "`data/processed/trade_records.csv` lists every record for the engine.", "",
          f"- Trades in trades_clean.csv with more than one record: **{len(corr_t):,}**, "
          f"{len(multi):,} records; {int((corr_t['n_records'] > 2).sum())} trades have three or more records.",
          f"- In scope under both rules: {int(both.sum()):,}; only as first published (J3): {int(j3_only.sum()):,}; "
          f"only as revised (V14): {int(v14_only.sum()):,}. Headline (J3) in-scope trades: **{int(tr['in_scope'].sum()):,}**; "
          f"as revised: **{int(tr['in_scope_as_revised'].sum()):,}**.", "",
          "Corrected trades by which of their records is in scope:", "",
          md(pattern, index=True) if len(pattern) else "_None._", ""]
    amb = amend[amend["class"] == "AMBIGUOUS"].copy()
    amb["in_window"] = amb["date_received"].between(start.isoformat(), end.isoformat())
    L += ["AMBIGUOUS amendments (for Harry):", "",
          md(amb[["senator", "date_received", "title_date", "in_window", "n_rows", "n_amended_report_trades",
                  "n_repeated_exact", "n_repeated_corrected", "n_new", "n_amended_report_not_repeated", "ptr_id"]]), ""]

    # 3. amounts
    L += ["### 3. Amount strings", "", "Every distinct amount string in the raw rows and how it was parsed "
          "(open top band = lower bound, D10):", "",
          md(amounts_md[["amount", "rows", "amount_lower", "amount_upper", "amount_mid", "amount_rule"]]), ""]

    # 4. tickers
    acc = rec[rec["accepted"]]
    rej = rec[~rec["accepted"]].sort_values(["n_trades_self_joint_in_window", "n_trades"], ascending=False)
    L += ["### 4. Tickers", "",
          f"- Unique tickers checked with Yahoo (3/5/10-year windows, any owner): **{len(tickers):,}**; kept "
          f"{int((tickers['instrument_status'] == 'kept').sum()):,}; with at least one in-scope trade "
          f"{int((tickers['n_in_scope'] > 0).sum()):,}. Status by ticker: "
          + ", ".join(f"{k} {v}" for k, v in tickers['instrument_status'].value_counts().items()) + ".",
          f"- Rows with a raw ticker changed by normalisation (case, spaces, share class BRK.B -> BRK-B): "
          f"{int((rows['ticker_raw'].str.strip().str.upper().replace('--', '') != rows['ticker']).sum())}.",
          f"- Missing-ticker asset names recovered: **{len(acc)}** names, {int(acc['n_trades'].sum())} trades "
          f"({int(acc['n_trades_self_joint_in_window'].sum())} Self/Joint in the default window). Not recovered: "
          f"**{len(rej)}** names, {int(rej['n_trades'].sum())} trades ({int(rej['n_trades_self_joint_in_window'].sum())} "
          "Self/Joint in window); these are NO_TICKER exclusions. Full list: `data/interim/ticker_recovery.csv`.", "",
          "Hand-written overrides (J5, `config/asset_name_overrides.yaml`; applied only when Yahoo's, or failing "
          "that SEC's, company name for the ticker confirms it):", "",
          md(R["overrides"][["contains", "ticker", "confirmed_by", "note", "matched_asset_names"]]), "",
          "Recovered:", "", md(acc[["asset_name", "candidate", "method", "n_trades", "n_trades_self_joint_in_window", "note"]]), "",
          "Not recovered, Self/Joint in the default window (for Harry):", "",
          md(rej[rej["n_trades_self_joint_in_window"] > 0][["asset_name", "asset_type", "candidate", "n_trades_self_joint_in_window", "note"]]), ""]
    mf = tr[tr["reason_code"].isin(["MUTUAL_FUND", "NON_US_LISTING", "OTHER_INSTRUMENT"])].groupby(
        ["reason_code", "ticker"]).agg(trades=("trade_id", "size"), yahoo_name=("yahoo_name", "first"),
                                       exchange=("exchange_name", "first"), efd_name=("asset_name", "first")).reset_index()
    unres = tickers[tickers["instrument_unresolved"]]
    L += ["Excluded by Yahoo classification (in-window trades):", "", md(mf), "",
          f"Tickers Yahoo does not resolve, or whose Yahoo name matches no eFD name for the ticker (recycled or "
          f"renamed symbol): **{len(unres)}** tickers, {int(unres['n_in_scope'].sum())} in-scope trades. Kept and "
          "flagged `instrument_unresolved`; Phase 3 resolves renames and delistings.", "",
          md(unres[["ticker", "n_in_scope", "first_trade_date", "last_trade_date", "yahoo_name_mismatch",
                    "yahoo_name", "efd_asset_names"]]), "",
          f"OTC-traded tickers (kept, `is_otc`): {int(tickers['is_otc'].sum())} tickers, "
          f"{int(s['is_otc'].sum())} in-scope trades.", ""]

    # 5. concentration
    s["dollars"] = s["amount_mid"]
    conc = s.groupby(["senator", "party"]).agg(trades=("trade_id", "size"), dollars=("dollars", "sum")).reset_index()
    conc["share_trades"] = conc["trades"] / conc["trades"].sum()
    conc["share_dollars"] = conc["dollars"] / conc["dollars"].sum()
    by_n = conc.sort_values(["trades", "senator"], ascending=[False, True]).reset_index(drop=True)
    by_n.index += 1
    by_n["cum_share_trades"] = by_n["share_trades"].cumsum()
    by_d = conc.sort_values(["dollars", "senator"], ascending=[False, True]).reset_index(drop=True)
    by_d.index += 1
    by_d["cum_share_dollars"] = by_d["share_dollars"].cumsum()
    fmt = lambda d, cols: d.assign(**{c: d[c].map(pct) for c in cols})
    L += ["### 5. Concentration by senator (in-scope trades)", "",
          f"{len(conc)} senators, {len(s):,} trades, ${s['dollars'].sum():,.0f} at range midpoints.", "",
          "By trade count:", "", md(fmt(by_n, ["share_trades", "share_dollars", "cum_share_trades"]).rename_axis("rank"), index=True), "",
          "By midpoint dollars:", "", md(fmt(by_d, ["share_trades", "share_dollars", "cum_share_dollars"]).rename_axis("rank"), index=True), ""]

    # 6. filing lag
    top5 = list(s.groupby(["bioguide_id", "senator"]).size().sort_values(ascending=False).head(5).index)
    L += ["### 6. Filing lag (disclosure date minus transaction date, in-scope trades)", "",
          md(lag_table(s, top5).round(1)), ""]

    # 7. paper filings in window
    paper = R["paper"]
    pw = paper[paper["date_received"].between(start.isoformat(), end.isoformat())]
    pw_by = pw.groupby("filer_name").agg(filings=("url", "size"), first=("date_received", "min"),
                                         last=("date_received", "max")).reset_index().sort_values("filings", ascending=False)
    L += ["### 7. Paper filings inside the default window (trades we cannot see)", "",
          f"**{len(pw)}** paper PTRs received {start} to {end}; list with links in `data/interim/paper_filings.csv`.", "",
          md(pw_by), ""]

    # 8. per year
    s["side"] = s["transaction_type"].map(lambda t: "Purchases" if t == "Purchase" else "Sales")
    all_ = pd.crosstab(s["year"], s["side"])
    no_etf = pd.crosstab(s.loc[~s["is_etf"], "year"], s.loc[~s["is_etf"], "side"])
    yt = all_.join(no_etf, rsuffix=" (no ETFs)").fillna(0).astype(int)
    yt["Total"] = yt["Purchases"] + yt["Sales"]
    yt["Total (no ETFs)"] = yt["Purchases (no ETFs)"] + yt["Sales (no ETFs)"]
    yt.loc["Total"] = yt.sum()
    L += ["### 8. In-scope purchases and sales by year of disclosure", "",
          f"{start.year} starts {start:%d %b}; {end.year} ends {end:%d %b}. Sales = Sale (Full) + Sale (Partial).", "",
          md(yt, index=True), ""]

    # 9. variant flags
    clean_rows = tr[tr["in_trades_clean"]]
    fam = clean_rows[clean_rows["in_window"] & clean_rows["v6_family_owner"]]
    vrows = [("V1", "Exclude Tuberville", int(s["v1_tuberville"].sum()), "removed")]
    for k, (bid, name) in enumerate(top5, 1):
        vrows.append((f"V2.{k}", f"Leave out #{k} {name}", int((s["bioguide_id"] == bid).sum()), "removed"))
    vrows += [("V3", "Exclude first 180 days of service", int(s["v3_first_180d"].sum()), "removed"),
              ("V4", "Exclude PTRs with 50+ in-scope trades", int(s["bulk_ptr"].sum()),
               f"removed ({s.loc[s['bulk_ptr'], 'first_ptr_id'].nunique()} PTRs)"),
              ("V5", "Exclude ETFs", int(s["is_etf"].sum()), "removed"),
              ("V6", "Add Spouse and Child trades", len(fam), "added (Spouse "
               f"{int((fam['owner'] == 'Spouse').sum())}, Child {int((fam['owner'] == 'Child').sum())})"),
              ("V9", "Same-day entry (filed before 15:30 ET)", int(s["filed_before_1530_et"].sum()), "enter same day")]
    v16 = clean_rows[clean_rows["in_window"] & clean_rows["owner"].isin(cfg["universe"]["owners"])
                     & (clean_rows["reason_code"] == "NON_EQUITY_ETF")]
    vrows.append(("V16", "Add non-equity ETFs (bond, T-bill, commodity, other)", len(v16), "added"))
    for y in (3, 10):
        c = f"in_window_{y}y"
        n = int((clean_rows[c] & clean_rows["owner"].isin(cfg["universe"]["owners"])).sum())
        vrows.append((f"V{11 if y == 3 else 12}", f"{y}-year window", n, "trades in that window (Self/Joint)"))
    L += ["### 9. Rows each pre-registered variant flag touches", "",
          f"Relative to the {len(s):,} in-scope trades. V7, V8 and V10 change sizing or weighting only.", "",
          md(pd.DataFrame(vrows, columns=["Variant", "Change", "Trades", "Effect"])), ""]
    # 10. K5: ETF classes
    e = tr[tr["in_trades_clean"] & tr["is_etf"]]
    ew = e[e["in_window"] & e["owner"].isin(cfg["universe"]["owners"])]
    by_cls = pd.DataFrame({"ETF symbols (all variants)": e.groupby("etf_class")["price_ticker"].nunique(),
                           "Trades, Self/Joint in window": ew.groupby("etf_class").size(),
                           "Midpoint $": ew.groupby("etf_class")["amount_mid"].sum()}).fillna(0).reset_index()
    syms = (e.groupby(["etf_class", "price_ticker"]).agg(category=("etf_category", "first"), method=("etf_class_method", "first"),
                                                         trades=("trade_id", "size"), name=("asset_name", "first"))
            .reset_index())
    syms = syms[syms["etf_class"] != "equity"].assign(name=lambda d: d["name"].str[:45])
    L += ["### 10. ETF asset classes (K5: the headline keeps equity ETFs only)", "",
          f"Every ETF (Yahoo instrument type ETF, or an eFD name that says ETF when Yahoo cannot describe the symbol) "
          f"is classified from Yahoo's fund category (cached in `data/raw/yahoo_fund/`), else from its fund name "
          f"(rules in `src/clean/etf_class.py`). Classes kept in the headline: {cfg['universe'].get('etf_classes')}. "
          f"Non-equity ETF trades carry reason NON_EQUITY_ETF and stay in trades_clean.csv for V16.", "",
          md(by_cls), "", "Non-equity ETF symbols:", "", md(syms), ""]
    unsure = e[e["etf_class_method"].str.startswith("default") | e["etf_class_method"].str.startswith("fund name: no")]
    if len(unsure):
        L += ["ETFs classified as equity only because no category was found and the name has no bond, commodity or "
              "other keyword: " + ", ".join(sorted(unsure["price_ticker"].unique())) + ".", ""]
    write_section(2, L)
    print(f"  [clean] {len(rows):,} raw rows -> {len(tr):,} unique trades -> {len(s):,} in scope; "
          f"{len(clean):,} rows in {TRADES_CLEAN}; {len(excl):,} in {EXCLUSIONS}; {len(tickers):,} tickers")
