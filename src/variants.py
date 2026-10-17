"""Run every pre-registered variant (docs/DECISIONS.md, V1-V20) through the engine and the metrics, each ALONE against
the headline (one config switch at a time, never combined), and write one summary table.

    python run_variants.py                 # every variant, in-sample (the firewall decides the sample)
    python run_variants.py --only V1 V17   # some of them

Each variant's engine files go to data/interim/variants/<sample>_<tag>/<id>/ (not committed); the headline is run the
same way first, so every difference is measured against a run of the same code. Outputs:
  outputs/tables/variants_<sample>_<tag>.csv, .md and .json    (<tag> = yahoo: the headline's price source, S2)
FIREWALL: the sample is the one src.engine.sample_bounds gives for the BASE config (in-sample while the firewall is
shut). A variant whose own sample would end after the headline's sample end (V11: the 3-year window's in-sample half
runs to 2025-02-28) is NOT run, and the table says why; with the firewall open (engine.sample: full) it runs.
"""
from __future__ import annotations

import copy
import json
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import load_config

TABLES = Path("outputs/tables")
WORK = Path("data/interim/variants")
ALL_ETF_CLASSES = ["equity", "fixed_income", "commodity", "other"]

# (id, short name, [(config path, value)], what it tests). V2 is expanded into one run per senator rank.
VARIANTS = [
    ("V1", "Exclude Tuberville", [("engine.drop_flags", ["v1_tuberville"])]),
    ("V2", "Leave one senator out", [("engine.drop_senator_ranks", "RANK")]),
    ("V3", "Exclude a senator's first 180 days", [("engine.drop_flags", ["v3_first_180d"])]),
    ("V4", "Exclude bulk PTRs (50+ in-scope trades)", [("engine.drop_flags", ["bulk_ptr"])]),
    ("V5", "Exclude ETFs", [("universe.include_etfs", False)]),
    ("V6", "Include spouse and child trades", [("universe.owners", ["Self", "Joint", "Spouse", "Child"])]),
    ("V7", "Size at the lower bound of the range", [("trades.sizing", "lower_bound")]),
    ("V8", "Equal dollars per trade", [("trades.sizing", "equal_dollar")]),
    ("V9", "Same-day close for filings before 15:30 ET", [("trades.price_timing", "same_day_close")]),
    ("V10", "Equal-weight portfolio (series A)", [("portfolio.weighting", "equal")]),
    ("V11", "3-year window", [("analysis.window_years", 3)]),
    ("V12", "10-year window", [("analysis.window_years", 10)]),
    ("V13", "Exclude OTC names", [("engine.drop_flags", ["v13_otc"])]),
    ("V14", "As revised (corrected values at the original datetime)", [("data.amendment_values", "as_revised")]),
    ("V15", "Neutral fill: ledger purchases earn SPY", [("engine.ledger_trades", "spy_fill")]),
    ("V16", "All ETFs, including bond and T-bill funds", [("universe.etf_classes", ALL_ETF_CLASSES)]),
    ("V17", "Empty start (no warm-up)", [("engine.warmup_months", 0)]),
    ("V18", "Yahoo only, ledger skipped", [("prices.sources", ["yahoo"])]),
    ("V19", "Include preferred shares", [("universe.include_preferred", True)]),
    ("V20", "CRSP-filled prices (the headline's sources, then CRSP where they have no price)",
     [("prices.sources", ["yahoo", "manual", "crsp"])]),          # C1: was [yahoo, crsp] on top of the Yahoo-only headline
    ("V21", "Sale on departure from office (D1, defined after the unlock)",
     [("engine.sell_on_departure", True)]),
]


def price_tag(cfg: dict | None = None) -> str:
    """The headline's price source, used in output file names: "yahoo" for `prices.sources: [yahoo]` (S2, S3), and
    "bloomberg" since C1 (2026-10-09: `[yahoo, manual]`, the Bloomberg terminal files fill symbols Yahoo has no price
    for)."""
    sources = list((cfg or load_config())["prices"].get("sources", ["yahoo"]))
    return "yahoo" if sources == ["yahoo"] else "bloomberg" if sources == ["yahoo", "manual"] else "_".join(sources)


def price_note(tag: str) -> str:
    """The one-paragraph price note at the top of every table whose file name carries the tag."""
    if tag == "yahoo":
        return ("**Prices: Yahoo only** (`prices.sources: [yahoo]`; R3, S2). Stocks in the survivorship ledger (mostly "
                "delisted names Yahoo no longer serves) have no prices: their events drop out here and their purchases "
                "are skipped in the book. Superseded as the headline by C1 (2026-10-09): see docs/DECISIONS.md.")
    if tag == "bloomberg":
        return ("**Prices: Yahoo, with Bloomberg terminal prices where Yahoo has none** (`prices.sources: [yahoo, "
                "manual]`, post-unlock correction C1, 2026-10-09): 8 delisted stocks (X, ECOM, ATVI, SSBK, PARA, WBA, "
                "GOGL, TOELY; 95% of the missing headline dollars) are priced from data/raw/manual_prices/. The other "
                "survivorship-ledger stocks still have no prices: their events drop out here and their purchases are "
                "skipped in the book. V18 is the Yahoo-only run (the headline before C1).")
    return f"**Prices: `prices.sources` = {tag}.**"


def crsp_files() -> list[Path]:
    return sorted(Path("data/raw/crsp").glob("*.csv*"))


def set_path(cfg: dict, path: str, value) -> None:
    d = cfg
    keys = path.split(".")
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = value


def expand(base: dict, only: list[str] | None) -> list[dict]:
    """One run per variant (V2: one per senator rank 1-5), each with its config."""
    tc = pd.read_csv("data/processed/trades_clean.csv", keep_default_na=False, low_memory=False,
                     usecols=["senator", "senator_rank"])
    rank_name = tc[tc["senator_rank"] != ""].drop_duplicates("senator_rank").set_index("senator_rank")["senator"]
    runs = []
    for vid, name, changes in VARIANTS:
        if only and vid not in only:
            continue
        ranks = [1, 2, 3, 4, 5] if any(v == "RANK" for _, v in changes) else [None]
        for k in ranks:
            cfg = copy.deepcopy(base)
            desc = []
            for path, v in changes:
                val = [k] if v == "RANK" else v
                set_path(cfg, path, val)
                desc.append(f"{path}: {val}")
            rid = f"{vid}.{k}" if k else vid
            label = f"{name}: {rank_name.get(str(k), rank_name.get(k, '?'))} (rank {k})" if k else name
            runs.append({"id": rid, "variant": vid, "name": label, "config": "; ".join(desc), "cfg": cfg})
    return runs


def summarise(rid: str, out: dict, eng: dict) -> dict:
    a = out["results"]["Series A (headline)"]
    b = out["results"]["Series B (fixed pot)"]
    log = eng["log"]
    first = eng["first"]
    lw = log[log["entry_date"] >= first]
    row = {"months": a["months"], "n_months": a["n_months"],
           "purchases_copied": int(lw["action"].str.startswith("bought").sum()),
           "sales_executed": int(lw["action"].str.startswith("sold").sum()),
           "lots": int(eng["pieces"]["lot_id"].nunique()), **period_cols(out["results"])}
    oos = (out.get("periods") or {}).get("oos")                # full window: the variant's own out-of-sample half
    if oos:
        row.update({f"oos_{k}": v for k, v in period_cols(oos).items()})
    return row


def period_cols(res: dict) -> dict:
    a, b = res["Series A (headline)"], res["Series B (fixed pot)"]
    return {"months": a["months"], "n_months": a["n_months"],
            "A_ann_return": a["ann_return"], "A_ann_vol": a["ann_vol"], "A_sharpe": a["sharpe"],
            "A_capm_alpha": a["capm_alpha_ann"], "A_capm_t": a["capm_t_alpha_ols"], "A_capm_t_nw": a["capm_t_alpha_nw"],
            "A_c4_alpha": a["c4_alpha_ann"], "A_c4_t": a["c4_t_alpha_ols"], "A_c4_t_nw": a["c4_t_alpha_nw"],
            "A_max_dd": a["dd_depth"], "B_ann_return": b["ann_return"], "B_sharpe": b["sharpe"],
            "SPY_ann_return": res["SPY"]["ann_return"]}


def run_one(run: dict, sample_dir: Path, limit_last: str, unlocked: bool) -> dict:
    from src import engine, metrics
    from src.engine import sample_bounds
    cfg = run["cfg"]
    first, last, label = sample_bounds(cfg)
    row = {k: run[k] for k in ("id", "variant", "name", "config")}
    row.update({"sample": f"{first}..{last}"})
    if run["variant"] == "V20":                            # S3: needs a CRSP file and its own price build
        row["status"] = ("not run: no CRSP data" if not crsp_files() else
                         "not run: CRSP data present, but the V20 price build is not implemented yet")
        return row
    if last > limit_last and not unlocked:
        row.update({"status": f"not run: its {label} sample ends {last}, after the headline's {limit_last} "
                              "(out-of-sample firewall)"})
        return row
    try:
        d = sample_dir / run["id"]
        eng = engine.run(cfg, out_dir=d, write_diagnostics=False)
        out = metrics.run(cfg, engine_dir=d, write=False)
        row.update(summarise(run["id"], out, eng))
        row["status"] = "run"                                 # no run time here: the tables must rebuild byte-for-byte
    except Exception as e:                                    # a failure is a result: log it, keep going
        row["status"] = f"failed: {type(e).__name__}: {e}"
        (sample_dir / f"{run['id']}_error.txt").write_text(traceback.format_exc())
    return row


def fmt_table(df: pd.DataFrame, p: str = "") -> pd.DataFrame:
    """p = "" for the run's whole sample, "oos_" for the out-of-sample half read off the same run."""
    c = lambda name: f"{p}{name}"
    months = df[c("months")].fillna(df["sample"]) if c("months") in df else df["sample"]
    v = pd.DataFrame({"id": df["id"], "variant": df["name"], "sample": months, "status": df["status"]})
    pct = lambda x: "" if pd.isna(x) else f"{x:.2%}"
    num = lambda x, f="{:.2f}": "" if pd.isna(x) else f.format(x)
    if c("A_ann_return") in df:
        v["A return"] = df[c("A_ann_return")].map(pct)
        v["A vol"] = df[c("A_ann_vol")].map(pct)
        v["A Sharpe"] = df[c("A_sharpe")].map(num)
        v["CAPM alpha (t)"] = [("" if pd.isna(a) else f"{a:.2%} ({t:.2f})") for a, t in zip(df[c("A_capm_alpha")], df[c("A_capm_t")])]
        v["Carhart alpha (t)"] = [("" if pd.isna(a) else f"{a:.2%} ({t:.2f})") for a, t in zip(df[c("A_c4_alpha")], df[c("A_c4_t")])]
        v["A max drawdown"] = df[c("A_max_dd")].map(pct)
        if not p:
            v["purchases copied"] = df["purchases_copied"].map(lambda x: "" if pd.isna(x) else f"{int(x)}")
            v["sales executed"] = df["sales_executed"].map(lambda x: "" if pd.isna(x) else f"{int(x)}")
        v["B return"] = df[c("B_ann_return")].map(pct)
        v["B Sharpe"] = df[c("B_sharpe")].map(num)
        v["Δ A return"] = df[f"d_{p}A_ann_return"].map(lambda x: "" if pd.isna(x) else f"{x:+.2%}")
        v["Δ A Sharpe"] = df[f"d_{p}A_sharpe"].map(lambda x: "" if pd.isna(x) else f"{x:+.2f}")
        v["Δ CAPM alpha"] = df[f"d_{p}A_capm_alpha"].map(lambda x: "" if pd.isna(x) else f"{x:+.2%}")
    return v


def main(only: list[str] | None = None, config_path: str | None = None) -> pd.DataFrame:
    from src.engine import sample_bounds
    base = load_config(config_path) if config_path else load_config()
    first, last, label = sample_bounds(base)
    unlocked = bool(base["oos"].get("oos_unlocked")) and base.get("engine", {}).get("sample") == "full"
    tag = price_tag(base)
    skey = "insample" if label == "in-sample" else "full"
    sample_dir = WORK / f"{skey}_{tag}"
    sample_dir.mkdir(parents=True, exist_ok=True)
    runs = [{"id": "H", "variant": "headline", "name": "Headline (no variant)", "config": "(default config)",
             "cfg": copy.deepcopy(base)}] + expand(base, only)
    rows = []
    for r in runs:
        print(f"[variants] {r['id']}: {r['name']} ...", flush=True)
        t0 = time.time()
        rows.append(run_one(r, sample_dir, last, unlocked))
        print(f"           {rows[-1]['status']} ({time.time() - t0:.0f}s)", flush=True)
    df = pd.DataFrame(rows)
    stem = TABLES / f"variants_{skey}_{tag}"
    if only and stem.with_suffix(".csv").exists():          # --only: replace those rows, keep the others
        old = pd.read_csv(stem.with_suffix(".csv"), keep_default_na=False, na_values=[""])
        old = old[~old["id"].isin(df["id"])][[c for c in old.columns if not c.startswith("d_")]]
        df = pd.concat([df, old], ignore_index=True)
        order = {r["id"]: i for i, r in enumerate([{"id": "H"}] + expand(base, None))}
        df = df.sort_values("id", key=lambda s: s.map(order)).reset_index(drop=True)
        rows = df.to_dict("records")
    h = df[df["id"] == "H"].iloc[0]
    sig6 = lambda v: float(f"{v:.6g}") if pd.notna(v) else np.nan    # the CSV's precision, so that a full run and an
    for c in ("A_ann_return", "A_sharpe", "A_capm_alpha", "A_c4_alpha", "B_ann_return", "B_sharpe"):  # --only run agree
        for pc in (c, f"oos_{c}"):
            if pc in df:
                df[f"d_{pc}"] = df[pc].map(sig6) - sig6(h[pc])
    TABLES.mkdir(parents=True, exist_ok=True)
    df.to_csv(stem.with_suffix(".csv"), index=False, float_format="%.6g")
    stem.with_suffix(".json").write_text(json.dumps({"sample": f"{first}..{last}", "tag": tag, "rows": rows},
                                                    indent=1, default=str))
    v = fmt_table(df)
    head = (f"# Variants, {label} ({first} to {last}), {tag.upper()}\n\n"
            + price_note(tag) + "\n\n"
            + "_Built by `python run_variants.py` (src/variants.py). Each pre-registered variant is run ALONE against the "
              "headline: one config switch, everything else as the headline (docs/DECISIONS.md, \"Pre-registered variants\"). "
              "Series A = return on capital deployed (headline); B = fixed pot. Monthly statistics as in "
              "outputs/tables/phase5_insample_results.md: annualised geometric return, volatility, Sharpe on excess returns, "
              "CAPM and Carhart alphas (annualised, OLS t), maximum drawdown of the daily index. \"Purchases copied\" = "
              "purchases the book bought inside the window. Δ = variant minus headline. "
              + ("V12 covers different dates (2016-09 to 2021-08), so its Δ compares different periods. " if skey != "full" else
                 "V11 (2023-09 to 2026-08) and V12 (2016-09 to 2026-08) cover different dates, so their Δ compare different "
                 "periods. ")
              + "Unrounded numbers: the .csv._\n\n")
    body = v.to_markdown(index=False) + "\n"
    if skey == "full":
        from src.metrics.confirmatory import EXPLORATORY_NOTE
        body = (EXPLORATORY_NOTE + "\n\n## Full window (each variant's whole window, one continuous run)\n\n" + body
                + "\n## Second half: each variant's own out-of-sample half, read off the same run\n\n"
                + "_The headline and every 5-year variant: 2024-03 to 2026-08. V11 (3-year window): 2025-03 to 2026-08. "
                  "V12 (10-year window): 2021-09 to 2026-08._\n\n"
                + (fmt_table(df, "oos_").to_markdown(index=False) + "\n" if "oos_A_ann_return" in df else "_None._\n"))
    stem.with_suffix(".md").write_text(head + body)
    print(f"[variants] {len(df)} rows -> {stem}.md")
    return df


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="+")
    ap.add_argument("--config")
    a = ap.parse_args()
    main(a.only, a.config)
