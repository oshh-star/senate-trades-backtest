"""outputs/data_quality.md is shared by every phase: each stage rewrites only its own
"## Phase N: ..." section and leaves the others untouched."""
from __future__ import annotations

import re
from pathlib import Path

QUALITY = Path("outputs/data_quality.md")
PREAMBLE = ["# Data quality log", "",
            "Every exclusion and every data problem, counted and explained. One section per phase.", ""]
_HEAD = re.compile(r"^## Phase (\d+)\b")


def write_section(phase: int, lines: list[str], path: Path = QUALITY) -> None:
    """Replace (or add) the section whose heading starts with "## Phase <phase>"."""
    sections: dict[int, list[str]] = {}
    if path.exists():
        cur = None
        for line in path.read_text().splitlines():
            m = _HEAD.match(line)
            if m:
                cur = int(m.group(1))
                sections[cur] = []
            if cur is not None:
                sections[cur].append(line)
    body = list(lines)
    if not body or not _HEAD.match(body[0]):
        raise ValueError(f"section must start with '## Phase {phase}: ...'")
    while body and body[-1] == "":
        body.pop()
    sections[phase] = body + [""]
    out = PREAMBLE + [x for k in sorted(sections) for x in sections[k]]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out).rstrip("\n") + "\n")
