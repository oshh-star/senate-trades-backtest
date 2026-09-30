"""Senate committee memberships by date (Phase 6 prep, committee test), reconstructed from the git history of
committee-membership-current.yaml in unitedstates/congress-legislators. Run by hand from the repo root:

    python scripts/committee_history.py

A partial clone (no file contents until asked) goes to data/interim/_congress_legislators/ (not committed); every
version of the file is read with `git show <commit>:committee-membership-current.yaml`. Output (committed):
data/raw/legislators/committee_membership_history.csv.gz, one row per (version, Senate full committee, member):
commit, commit_date, committee_id, bioguide, name, party, rank, title. Only full Senate committees (4-letter ids
starting with S: SSAS Armed Services, SSAF Agriculture, ...) are kept; subcommittees and House committees are dropped.
The membership on a date is the latest version committed ON OR BEFORE that date (the repository is updated by
volunteers, usually within weeks of a change). Resumable: versions already in the output are not read again.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pandas as pd
import yaml

REPO = "https://github.com/unitedstates/congress-legislators"
CLONE = Path("data/interim/_congress_legislators")
FILE = "committee-membership-current.yaml"
OUT = Path("data/raw/legislators/committee_membership_history.csv.gz")


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(CLONE), *args], check=True, capture_output=True, text=True).stdout


def main() -> None:
    if not CLONE.exists():
        subprocess.run(["git", "clone", "-q", "--filter=blob:none", "--no-checkout", REPO, str(CLONE)], check=True)
    else:
        git("fetch", "-q", "origin")
    commits = [l.split() for l in git("log", "origin/HEAD", "--format=%H %cs", "--", FILE).splitlines()]
    have = pd.read_csv(OUT, dtype=str) if OUT.exists() else pd.DataFrame(columns=["commit"])
    done = set(have["commit"])
    rows = []
    for i, (h, d) in enumerate(commits):
        if h in done:
            continue
        data = yaml.safe_load(git("show", f"{h}:{FILE}")) or {}
        for cid, members in data.items():
            if not (len(cid) == 4 and cid.startswith("S")):
                continue
            for m in members or []:
                rows.append({"commit": h, "commit_date": d, "committee_id": cid, "bioguide": m.get("bioguide", ""),
                             "name": m.get("name", ""), "party": m.get("party", ""), "rank": m.get("rank", ""),
                             "title": m.get("title", "")})
        if (i + 1) % 25 == 0:
            print(f"  {i + 1}/{len(commits)} versions read", flush=True)
    out = pd.concat([have, pd.DataFrame(rows)], ignore_index=True) if rows else have
    out = out.sort_values(["commit_date", "commit", "committee_id", "rank"]).reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False, compression={"method": "gzip", "mtime": 0})
    print(f"{OUT}: {out['commit'].nunique()} versions, {out['commit_date'].min()} to {out['commit_date'].max()}, "
          f"{len(out):,} rows")


if __name__ == "__main__":
    main()
