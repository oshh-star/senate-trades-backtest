"""Committee test (Phase 6 prep, E54): do trades in industries that the senator's committee oversees do better?

An event (a record of data/processed/event_panel.csv) is OVERSEEN when, on its TRANSACTION date, the senator sat on one
of the committees in config/committee_industries.yaml (membership: the latest version of committee-membership-current.yaml
committed on or before that date, data/raw/legislators/committee_membership_history.csv.gz) whose SIC ranges contain the
company's SIC code (data/interim/sic_codes.csv). ETFs and companies with no SIC code are left out and counted. The split
is reported exactly like the mechanism splits (src/metrics/mechanism.py): copier and senator SPY-adjusted returns at 21,
63 and 126 trading days, the pre-disclosure drift, N and t clustered by entry month, and the difference row.
"""
from __future__ import annotations

import bisect
from pathlib import Path

import pandas as pd
import yaml

from . import mechanism as mc

MAPPING = Path("config/committee_industries.yaml")
MEMBERSHIP = Path("data/raw/legislators/committee_membership_history.csv.gz")
SIC = Path("data/interim/sic_codes.csv")
OVERSEEN, NOT = "overseen by the senator's committee", "not overseen"


def available() -> bool:
    return MAPPING.exists() and MEMBERSHIP.exists() and SIC.exists()


def classify(panel: pd.DataFrame) -> pd.DataFrame:
    comm = yaml.safe_load(MAPPING.read_text())["committees"]
    mem = pd.read_csv(MEMBERSHIP, dtype=str)
    last_per_date = mem.drop_duplicates(["commit_date", "commit"])[["commit_date", "commit"]] \
        .drop_duplicates("commit_date", keep="last")                # every version, before keeping mapped committees
    mem = mem[mem["committee_id"].isin(comm)]
    versions = dict(zip(last_per_date["commit_date"], last_per_date["commit"]))
    dates = sorted(versions)
    seats = mem.groupby(["commit", "bioguide"])["committee_id"].apply(set).to_dict()
    sic = pd.read_csv(SIC, dtype=str, keep_default_na=False).set_index("symbol")["sic"].to_dict()
    p = mc.attach(panel)
    rows = []
    for e in p.itertuples():
        i = bisect.bisect_right(dates, str(e.transaction_date)) - 1
        v = versions[dates[i]] if i >= 0 else None
        cs = seats.get((v, e.bioguide_id), set()) if v else set()
        code = sic.get(e.price_ticker, "")
        hit = sorted(c for c in cs if code and any(lo <= int(code) <= hi for lo, hi in comm[c]["sic"]))
        if str(e.is_etf) == "True":
            group = "left out: ETF"
        elif not code:
            group = "left out: no SIC code"
        elif v is None:
            group = "left out: no membership version before the trade"
        else:
            group = OVERSEEN if hit else NOT
        rows.append({"committee_group": group, "mapped_seats": " ".join(sorted(cs)), "overseeing": " ".join(hit),
                     "sic": code, "membership_version_date": dates[i] if i >= 0 else ""})
    return pd.concat([p.reset_index(drop=True), pd.DataFrame(rows)], axis=1)


def write(panel: pd.DataFrame, label: str, first: str, last: str, tag: str, out_dir,
          key: str | None = None, exploratory: bool = False) -> pd.DataFrame | None:
    if not available():
        return None
    p = classify(panel)
    t = mc.split_table(p, "committee_group", [OVERSEEN, NOT])
    stem = Path(out_dir) / f"committee_{key or ('insample' if label == 'in-sample' else 'full')}_{tag}"
    t.to_csv(stem.with_suffix(".csv"), index=False, float_format="%.6g")
    p[["record_id", "senator", "price_ticker", "side", "transaction_date", "committee_group", "mapped_seats", "overseeing",
       "sic", "membership_version_date"]].to_csv(stem.parent / f"{stem.name}_events.csv", index=False)
    counts = p.groupby(["side", "committee_group"]).size().unstack(fill_value=0)
    by_comm = (p[p["committee_group"] == OVERSEEN].assign(c=lambda d: d["overseeing"].str.split()).explode("c")
               .groupby(["c", "side"]).size().unstack(fill_value=0))
    names = {k: v["name"] for k, v in yaml.safe_load(MAPPING.read_text())["committees"].items()}
    by_comm.index = [f"{c} {names.get(c, '')}" for c in by_comm.index]
    by_sen = (p[p["committee_group"] == OVERSEEN].groupby(["senator", "side"]).size().unstack(fill_value=0)
              .sort_values(by=list(p["side"].unique())[:1], ascending=False).head(10))
    L = [f"# Committee test, {label} ({first} to {last}), {tag.upper()}", ""]
    if exploratory:
        from .confirmatory import EXPLORATORY_NOTE
        L += [EXPLORATORY_NOTE, ""]
    from src.variants import price_note
    L += [price_note(tag), ""]
    L += ["_src/metrics/committee.py. An event is **overseen** when, on its transaction date, the senator sat on a committee "
          "in config/committee_industries.yaml (committed at a124f03 before this split was computed, E54) whose SIC ranges "
          "contain the company's SIC code. Membership: the latest version of congress-legislators' "
          "committee-membership-current.yaml committed on or before the trade date. Cells: mean SPY-adjusted return "
          "(t clustered by entry month); copier from the entry date, senator from the transaction date; \"t n/a\" = "
          f"fewer than {mc.MIN_CLUSTERS} entry months. After a SALE a NEGATIVE number is informative._", "",
          "## The split", "", mc.to_md(t), "",
          "## Events by group", "", counts.to_markdown(), "",
          "## Overseen events by committee (an event can count under two committees)", "",
          by_comm.to_markdown() if len(by_comm) else "_None._", "",
          "## Overseen events by senator (top 10)", "", by_sen.to_markdown() if len(by_sen) else "_None._", ""]
    stem.with_suffix(".md").write_text("\n".join(L))
    return t
