"""Match every eFD filer name to a bioguide_id in data/interim/senate_terms.csv.

Order of precedence:
  1. config/name_overrides.yaml: hand-checked answers (a bioguide_id, or null = "not a senator").
  2. exact: the normalised last name matches, and a first-name token matches the senator's first
     name, nickname, middle name or official first name (eFD's office text, e.g. "Hagerty, Bill",
     supplies nicknames), and exactly one senator fits.
  3. fuzzy: best difflib similarity on the full name. Reported as "high" confidence only when the
     last names match, the score is at least 0.85 and the runner-up is at least 0.10 behind;
     everything else is "low" and goes on the review list.
Names are never guessed: low-confidence and unmatched filers are listed in outputs/data_quality.md
and outputs/phase1_summary.md for a person to settle in the override file.

A sanity check flags any match where none of the filer's transactions fall inside that senator's
service, which would suggest the wrong person.
"""
from __future__ import annotations

import csv
import difflib
import re
import unicodedata
from pathlib import Path

import yaml

from .download import MANIFEST
from .legislators import TERMS_CSV

MATCHES = Path("data/interim/filer_matches.csv")
MATCH_COLUMNS = ["filer_key", "first_name", "last_name", "office_texts", "filer_type_labels",
                 "n_filings", "first_received", "last_received", "bioguide_id", "matched_name",
                 "method", "confidence", "score", "runner_up", "note"]
_DROP = {"mr", "mrs", "ms", "miss", "dr", "the", "honorable", "hon", "jr", "sr", "ii", "iii", "iv",
         "md", "senator"}


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z ]", " ", text.lower().replace("-", " ").replace("'", ""))
    return " ".join(t for t in text.split() if t not in _DROP)


def filer_key(first: str, last: str) -> str:
    return f"{norm(first)}|{norm(last)}"


def office_names(office: str) -> tuple[str, str]:
    """'Hagerty, Bill (Senator)' -> ('bill', 'hagerty'). Paper filings just say 'Senator'."""
    body = re.sub(r"\(.*?\)", "", office)
    if "," not in body:
        return "", ""
    last, first = body.split(",", 1)
    return norm(first), norm(last)


def load_senators() -> dict[str, dict]:
    people: dict[str, dict] = {}
    with open(TERMS_CSV) as f:
        for r in csv.DictReader(f):
            p = people.setdefault(r["bioguide_id"], {**r, "terms": []})
            p["terms"].append((r["term_start"], r["term_end"]))
    for p in people.values():
        p["last_n"] = norm(p["last"]).replace(" ", "")
        p["first_tokens"] = set(norm(" ".join([p["first"], p["nickname"], p["middle"]])).split())
        p["first_tokens"] |= set(norm(p["full_name"]).split()[:1])
        p["full_n"] = norm(f"{p['nickname'] or p['first']} {p['last']}")
    return people


def load_overrides(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text()) or {}
    return {filer_key(*k.split("|", 1)) if "|" in k else k: v for k, v in (data.get("overrides") or {}).items()}


def match_one(first: str, last: str, offices: set[str], people: dict, overrides: dict) -> dict:
    key = filer_key(first, last)
    if key in overrides:
        o = overrides[key]
        bid = o.get("bioguide_id") if isinstance(o, dict) else o
        note = o.get("note", "") if isinstance(o, dict) else ""
        return {"bioguide_id": bid or "", "method": "override", "confidence": "high" if bid else "none",
                "score": "", "runner_up": "", "note": note or ("override: not a senator" if not bid else "")}
    first_tokens = set(norm(first).split())
    last_n = norm(last).replace(" ", "")
    for o in offices:
        of, ol = office_names(o)
        if ol.replace(" ", "") == last_n:
            first_tokens |= set(of.split())
    exact = [b for b, p in people.items() if p["last_n"] == last_n and first_tokens & p["first_tokens"]]
    if len(exact) == 1:
        return {"bioguide_id": exact[0], "method": "exact", "confidence": "high", "score": 1.0,
                "runner_up": "", "note": ""}
    if len(exact) > 1:
        return {"bioguide_id": "", "method": "ambiguous", "confidence": "low", "score": "",
                "runner_up": "", "note": "several senators fit: " + ", ".join(sorted(exact))}
    target = norm(f"{first} {last}")
    scored = sorted(((difflib.SequenceMatcher(None, target, p["full_n"]).ratio(), b)
                     for b, p in people.items()), reverse=True)
    (s1, b1), (s2, b2) = scored[0], scored[1]
    same_last = people[b1]["last_n"] == last_n
    high = same_last and s1 >= 0.85 and s1 - s2 >= 0.10
    if s1 < 0.6:
        return {"bioguide_id": "", "method": "unmatched", "confidence": "none", "score": round(s1, 3),
                "runner_up": f"{people[b1]['full_name']} ({b1})", "note": "no senator with a similar name"}
    return {"bioguide_id": b1, "method": "fuzzy", "confidence": "high" if high else "low",
            "score": round(s1, 3), "runner_up": f"{people[b2]['full_name']} ({b2}) {s2:.3f}",
            "note": "" if same_last else "last name differs"}


def run(cfg: dict) -> list[dict]:
    people = load_senators()
    overrides = load_overrides(cfg["data"]["name_overrides"])
    filers: dict[str, dict] = {}
    with open(MANIFEST) as f:
        for r in csv.DictReader(f):
            k = filer_key(r["first_name"], r["last_name"])
            e = filers.setdefault(k, {"first_name": r["first_name"], "last_name": r["last_name"],
                                      "offices": set(), "labels": set(), "dates": []})
            e["offices"].add(r["office_text"])
            e["labels"].add(r["filer_type_label"])
            e["dates"].append(r["date_received"])
    out = []
    for k, e in sorted(filers.items()):
        m = match_one(e["first_name"], e["last_name"], e["offices"], people, overrides)
        out.append({"filer_key": k, "first_name": e["first_name"], "last_name": e["last_name"],
                    "office_texts": " | ".join(sorted(e["offices"])),
                    "filer_type_labels": " | ".join(sorted(e["labels"])), "n_filings": len(e["dates"]),
                    "first_received": min(e["dates"]), "last_received": max(e["dates"]),
                    "matched_name": people[m["bioguide_id"]]["full_name"] if m["bioguide_id"] else "",
                    **m})
    MATCHES.parent.mkdir(parents=True, exist_ok=True)
    with open(MATCHES, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=MATCH_COLUMNS)
        w.writeheader()
        w.writerows(out)
    c = {m: sum(r["method"] == m for r in out) for m in ("override", "exact", "fuzzy", "ambiguous", "unmatched")}
    print(f"  [names] {len(out)} distinct filer names -> {MATCHES}: {c}; "
          f"low confidence: {sum(r['confidence'] == 'low' for r in out)}")
    return out
