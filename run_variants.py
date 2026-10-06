"""Run every pre-registered variant (V1-V19), each alone against the headline, from the repo root:

    python run_variants.py                  # all of them (about 4 minutes)
    python run_variants.py --only V1 V17    # some of them

Needs the headline stages first (python run_all.py). See src/variants.py for the rules and the firewall.
"""
import argparse
import sys
from pathlib import Path

from src.variants import main


def _ensure_utf8() -> None:
    """Every text file is UTF-8. Where the machine's default text encoding is not (Windows: cp1252), rerun this command
    in Python's UTF-8 mode, so reading and writing files never depends on the computer it runs on."""
    import locale
    import subprocess
    if not sys.flags.utf8_mode and locale.getpreferredencoding(False).lower().replace("-", "") != "utf8":
        sys.exit(subprocess.call([sys.executable, "-X", "utf8", *sys.argv]))


if __name__ == "__main__":
    _ensure_utf8()
    if not Path("config/config.yaml").exists():
        sys.exit("Run this from the repository root (config/config.yaml not found).")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="+", help="variant ids, e.g. V1 V2 V17")
    main(ap.parse_args().only)
