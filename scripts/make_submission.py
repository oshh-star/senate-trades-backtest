"""Build the two submission zips (S4): everything the professor needs to rebuild every number offline.

    python scripts/make_submission.py

  dist/submission.zip         the code, the small data and the results (everything below except the Yahoo price cache)
  dist/submission_prices.zip  the Yahoo price cache, data/raw/prices/yahoo/ (S4: kept apart so each zip stays small)
Both unzip into the same folder (each holds the top folder senate-trades-backtest/), and both must be unzipped before
`python run_all.py --skip-scrape`.

Contents = the files committed to git (so the zip holds exactly what the clean-room test ran), minus what a reader does
not need: data/raw/_dryrun/ (Phase 0 test output) and .claude/ (assistant settings). That is:
  run_all.py, run_variants.py, requirements.txt, README.md, CLAUDE.md
  config/ src/ scripts/ tests/ docs/        code, locked parameters, decisions log, handover, course guidance
  data/raw/                                  every raw download (eFD pages and listings, Yahoo, SEC, Ken French,
                                             congress-legislators): what `python run_all.py --skip-scrape` reads offline
  data/interim/                              derived files, including the scrape stage's parsed output and the by-hand
                                             scripts' output (SIC codes, SEC delisting evidence), inputs to --skip-scrape
  data/processed/, outputs/                  the committed results, to compare a rebuild against
  CHECKSUMS.sha256                           SHA-256 of every file in both zips, in `sha256sum` format (in submission.zip)
After unzipping and running `python run_all.py --skip-scrape`, `sha256sum -c CHECKSUMS.sha256` (on a Mac:
`shasum -a 256 -c CHECKSUMS.sha256`) checks that the rebuilt files are identical to the submitted ones.

Must be run from a clean git checkout (it refuses to package uncommitted changes). The zip is deterministic: files in
sorted order, fixed timestamps, so the same commit always gives the same zips.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

OUT = Path("dist/submission.zip")
OUT_PRICES = Path("dist/submission_prices.zip")
PRICES_PREFIX = "data/raw/prices/yahoo/"         # S4: the Yahoo price cache goes in the second zip
TOP = "senate-trades-backtest"                   # folder name inside the zip
EXCLUDE_PREFIXES = ("data/raw/_dryrun/", ".claude/")
FIXED_TIME = (2026, 10, 19, 0, 0, 0)             # the submission date, so the zip does not depend on when it is built


def tracked_files() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], check=True, capture_output=True).stdout.decode()
    return sorted(f for f in out.split("\0") if f and not f.startswith(EXCLUDE_PREFIXES))


def add(z: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(f"{TOP}/{name}", FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    z.writestr(info, data)


def main() -> int:
    if not Path("run_all.py").exists():
        sys.exit("Run this from the repository root.")
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], check=True,
                           capture_output=True).stdout.decode().strip()
    if dirty:
        sys.exit("Uncommitted changes to tracked files: commit them first, so the zip matches a commit.\n" + dirty)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True).stdout.decode().strip()
    files = tracked_files()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sums, total = [], 0
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z, \
            zipfile.ZipFile(OUT_PRICES, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zp:
        for f in files:
            data = Path(f).read_bytes()
            total += len(data)
            sums.append(f"{hashlib.sha256(data).hexdigest()}  {f}")
            add(zp if f.startswith(PRICES_PREFIX) else z, f, data)
        add(z, "CHECKSUMS.sha256", ("\n".join(sums) + "\n").encode())
        add(z, "COMMIT.txt", (commit + "\n").encode())
        add(zp, "COMMIT.txt", (commit + "\n").encode())
    n_prices = sum(f.startswith(PRICES_PREFIX) for f in files)
    for out, n in ((OUT, len(files) - n_prices), (OUT_PRICES, n_prices)):
        print(f"{out}: {out.stat().st_size / 1e6:.1f} MB compressed, {n} files, commit {commit[:7]}")
    print(f"  together {total / 1e6:.1f} MB unzipped, {len(files)} files")
    by_top: dict[str, list[int]] = {}
    for f in files:
        key = "/".join(f.split("/")[:2]) if f.startswith("data/") else f.split("/")[0]
        by_top.setdefault(key, [0, 0])
        by_top[key][0] += 1
        by_top[key][1] += Path(f).stat().st_size
    for k, (n, b) in sorted(by_top.items(), key=lambda kv: -kv[1][1]):
        print(f"  {k:<28} {n:>6} files {b / 1e6:>8.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
