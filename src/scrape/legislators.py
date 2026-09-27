"""Senate service dates from the unitedstates/congress-legislators dataset (decision A05).

Downloads legislators-current.yaml and legislators-historical.yaml into data/raw/legislators/
(cached; delete a file to refresh it) and writes data/interim/senate_terms.csv with one row per
Senate term that ends on or after data.service_dates.terms_from.

Early departures: the dataset records the actual last day when a senator left before the
scheduled end (resignation, death, appointment elsewhere). A term is flagged ended_early when its
end is not the scheduled 3 January for its Senate class. check_departures() lists seats where a
successor started before the predecessor's recorded end, i.e. a departure the dataset may not
record, and current senators whose term end has already passed.
"""
from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path

import requests
import yaml

RAW_DIR = Path("data/raw/legislators")
TERMS_CSV = Path("data/interim/senate_terms.csv")
COLUMNS = ["bioguide_id", "full_name", "first", "middle", "last", "suffix", "nickname", "party",
           "state", "senate_class", "term_start", "term_end", "start_how", "end_type",
           "scheduled_end", "ended_early", "source_file"]
# The class of seats up in the election of November (Y - 1) and ending 3 January Y:
# class 1 ends in 2019, 2025, 2031...; class 2 in 2015, 2021, 2027...; class 3 in 2017, 2023, 2029...
_CLASS_END_YEAR_MOD6 = {1: 2019 % 6, 2: 2021 % 6, 3: 2023 % 6}


def download(cfg: dict, user_agent: str) -> list[Path]:
    sd = cfg["data"]["service_dates"]
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    for name in sd["files"]:
        path = RAW_DIR / name
        if not path.exists():
            r = requests.get(sd["base_url"] + name, headers={"User-Agent": user_agent}, timeout=120)
            r.raise_for_status()
            path.write_bytes(r.content)
            print(f"  [legislators] downloaded {name} ({len(r.content):,} bytes)")
        paths.append(path)
    return paths


def scheduled_end(senate_class: int, start: dt.date) -> dt.date:
    """The regular 3 January end of the seat's six-year cycle that contains `start`."""
    y = start.year + 1
    while y % 6 != _CLASS_END_YEAR_MOD6[senate_class] or dt.date(y, 1, 3) <= start:
        y += 1
    return dt.date(y, 1, 3)


def _date(x) -> dt.date:
    return x if isinstance(x, dt.date) else dt.date.fromisoformat(str(x))


def build_terms(cfg: dict) -> list[dict]:
    terms_from = _date(cfg["data"]["service_dates"]["terms_from"])
    rows = []
    for name in cfg["data"]["service_dates"]["files"]:
        people = yaml.safe_load(open(RAW_DIR / name))
        for p in people:
            n = p["name"]
            full = n.get("official_full") or " ".join(x for x in (n.get("first"), n.get("last")) if x)
            for t in p.get("terms", []):
                if t["type"] != "sen":
                    continue
                start, end = _date(t["start"]), _date(t["end"])
                if end < terms_from:
                    continue
                sched = scheduled_end(int(t["class"]), start)
                rows.append({
                    "bioguide_id": p["id"]["bioguide"], "full_name": full,
                    "first": n.get("first", ""), "middle": n.get("middle", ""), "last": n.get("last", ""),
                    "suffix": n.get("suffix", ""), "nickname": n.get("nickname", ""),
                    "party": t.get("party", ""), "state": t["state"], "senate_class": t["class"],
                    "term_start": start.isoformat(), "term_end": end.isoformat(),
                    "start_how": t.get("how", ""), "end_type": t.get("end-type", ""),
                    "scheduled_end": sched.isoformat(), "ended_early": end < sched,
                    "source_file": name,
                })
    rows.sort(key=lambda r: (r["state"], r["senate_class"], r["term_start"]))
    return rows


def check_departures(rows: list[dict], today: dt.date) -> list[str]:
    """Plain-English list of cases where a departure date may be missing or inconsistent."""
    issues = []
    by_seat: dict[tuple, list[dict]] = {}
    for r in rows:
        by_seat.setdefault((r["state"], r["senate_class"]), []).append(r)
    for (state, cls), terms in sorted(by_seat.items()):
        terms = sorted(terms, key=lambda r: r["term_start"])
        for a, b in zip(terms, terms[1:]):
            if a["bioguide_id"] != b["bioguide_id"] and b["term_start"] < a["term_end"]:
                issues.append(f"{state} class {cls}: {b['full_name']} started {b['term_start']} before "
                              f"{a['full_name']}'s recorded end {a['term_end']} (departure may be missing)")
    for r in rows:
        if r["source_file"] == "legislators-historical.yaml" and _date(r["term_end"]) > today:
            issues.append(f"{r['full_name']} ({r['bioguide_id']}) is in the historical file but the "
                          f"term end {r['term_end']} is in the future (departure date not recorded)")
        if r["source_file"] == "legislators-current.yaml" and _date(r["term_end"]) < today \
                and r is max((x for x in rows if x["bioguide_id"] == r["bioguide_id"]),
                             key=lambda x: x["term_end"]):
            issues.append(f"{r['full_name']} ({r['bioguide_id']}) is in the current file but the last "
                          f"term ended {r['term_end']}")
    return issues


def write_terms(rows: list[dict]) -> None:
    TERMS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(TERMS_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)


def run(cfg: dict, user_agent: str, today: dt.date | None = None) -> tuple[list[dict], list[str]]:
    download(cfg, user_agent)
    rows = build_terms(cfg)
    write_terms(rows)
    issues = check_departures(rows, today or dt.date.today())
    n_people = len({r["bioguide_id"] for r in rows})
    print(f"  [legislators] {len(rows)} Senate terms for {n_people} senators -> {TERMS_CSV}; "
          f"{sum(r['ended_early'] for r in rows)} ended early; {len(issues)} departure issues")
    return rows, issues
