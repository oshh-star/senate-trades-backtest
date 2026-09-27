"""Download electronic PTR pages and build the filings manifest.

Electronic PTRs go to data/raw/efd/ptr/<year received>/<ptr_id>.html.gz (gzip with a fixed
timestamp, so re-saving the same page gives identical bytes). Paper filings are scanned images:
only their listing metadata is kept and nothing is downloaded (decision D05).

Resumable: a PTR already on disk is skipped. A PTR that still fails after the client's retries is
recorded in data/raw/efd/download_failures.json and tried again on the next run. If
`max_consecutive_failures` PTRs fail in a row the site is probably down, so the chunk stops early
and the next run carries on from where it stopped.
"""
from __future__ import annotations

import csv
import datetime as dt
import gzip
import json
import re
from pathlib import Path

from .efd import EfdClient

PTR_DIR = Path("data/raw/efd/ptr")
FAILURES = Path("data/raw/efd/download_failures.json")
MANIFEST = Path("data/interim/filings_manifest.csv")
BASE_URL = "https://efdsearch.senate.gov"
# The site prints on-the-hour times without minutes ("10 AM") and may print "noon"/"midnight".
FILED_RE = re.compile(r"Filed\s+(\d{2}/\d{2}/\d{4})\s*@\s*(\d{1,2}(?::\d{2})?\s*[AP]\.?M\.?|noon|midnight)", re.I)
MANIFEST_COLUMNS = [
    "ptr_id", "filer_name", "first_name", "last_name", "office_text", "filer_type_code",
    "filer_type_label", "date_received", "time_received", "datetime_received", "filed_date_on_page",
    "page_date_differs", "report_title", "title_date", "kind", "is_amendment", "amendment_number",
    "url", "download_status", "local_path"]


def ptr_path(rec: dict) -> Path:
    year = rec["date_received"][-4:]
    return PTR_DIR / year / f"{rec['report_id']}.html.gz"


def read_ptr(path: Path) -> str:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return f.read()


def write_ptr(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
        gz.write(html.encode("utf-8"))


def _load_failures() -> dict:
    return json.loads(FAILURES.read_text()) if FAILURES.exists() else {}


def _save_failures(f: dict) -> None:
    FAILURES.parent.mkdir(parents=True, exist_ok=True)
    FAILURES.write_text(json.dumps(f, indent=1, sort_keys=True) + "\n")


def download(client: EfdClient, records: list[dict], max_consecutive_failures: int = 5) -> dict:
    """Fetch every electronic PTR in `records` that is not on disk yet. Returns counts."""
    failures = _load_failures()
    counts = {"cached": 0, "downloaded": 0, "failed": 0, "paper": 0, "stopped_early": False}
    streak = 0
    todo = [r for r in records if r["kind"] == "electronic"]
    counts["paper"] = sum(r["kind"] == "paper" for r in records)
    for i, rec in enumerate(todo, 1):
        path = ptr_path(rec)
        if path.exists():
            counts["cached"] += 1
            failures.pop(rec["report_id"], None)
            continue
        try:
            html = client.fetch_report(rec["link"])
        except Exception as e:  # noqa: BLE001 - one failure must never stop the run
            counts["failed"] += 1
            streak += 1
            prev = failures.get(rec["report_id"], {})
            failures[rec["report_id"]] = {"url": BASE_URL + rec["link"], "error": f"{type(e).__name__}: {e}"[:300],
                                          "attempts": prev.get("attempts", 0) + 1,
                                          "last_attempt": dt.datetime.now().replace(microsecond=0).isoformat()}
            _save_failures(failures)
            print(f"    [download] FAILED {rec['report_id']}: {e}")
            if streak >= max_consecutive_failures:
                print(f"    [download] {streak} failures in a row: the site looks down; stopping this chunk")
                counts["stopped_early"] = True
                break
            continue
        streak = 0
        write_ptr(path, html)
        failures.pop(rec["report_id"], None)
        counts["downloaded"] += 1
        if counts["downloaded"] % 25 == 0:
            print(f"    [download] {i}/{len(todo)} ({counts['downloaded']} new)")
    _save_failures(failures)
    return counts


def normalise_time(t: str) -> str:
    """'10 AM' -> '10:00 AM', '9:09 p.m.' -> '9:09 PM', 'noon' -> '12:00 PM'."""
    t = " ".join(t.replace(".", "").upper().split())
    if t in ("NOON", "MIDNIGHT"):
        return "12:00 PM" if t == "NOON" else "12:00 AM"
    m = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*([AP]M)", t)
    return f"{int(m.group(1))}:{m.group(2) or '00'} {m.group(3)}" if m else ""


def filed_timestamp(html: str) -> tuple[str, str]:
    """('MM/DD/YYYY', 'H:MM AM') from the "Filed ... @ ..." line of a PTR page."""
    m = FILED_RE.search(html)
    return (m.group(1), normalise_time(m.group(2))) if m else ("", "")


def _iso(mdy: str) -> str:
    return dt.datetime.strptime(mdy, "%m/%d/%Y").date().isoformat() if mdy else ""


def build_manifest(records: list[dict]) -> list[dict]:
    failures = _load_failures()
    rows = []
    for rec in records:
        path = ptr_path(rec)
        filed_date = filed_time = ""
        if rec["kind"] != "electronic":
            status = "paper_metadata_only" if rec["kind"] == "paper" else f"not_downloaded_{rec['kind']}"
        elif path.exists():
            status = "downloaded"
            filed_date, filed_time = filed_timestamp(read_ptr(path))
        elif rec["report_id"] in failures:
            status = "failed: " + failures[rec["report_id"]]["error"]
        else:
            status = "pending"
        received = _iso(rec["date_received"])
        dtr = ""
        if filed_time:
            dtr = dt.datetime.strptime(f"{filed_date} {filed_time}", "%m/%d/%Y %I:%M %p").isoformat()
        rows.append({
            "ptr_id": rec["report_id"],
            "filer_name": f"{rec['first_name']} {rec['last_name']}".strip(),
            "first_name": rec["first_name"], "last_name": rec["last_name"],
            "office_text": rec["office"], "filer_type_code": rec["filer_type_code"],
            "filer_type_label": rec["filer_type_label"], "date_received": received,
            "time_received": filed_time, "datetime_received": dtr,
            "filed_date_on_page": _iso(filed_date),
            "page_date_differs": bool(filed_date) and _iso(filed_date) != received,
            "report_title": rec["title"], "title_date": _iso(rec["title_date"]),
            "kind": rec["kind"], "is_amendment": rec["is_amendment"],
            "amendment_number": rec["amendment_number"], "url": BASE_URL + rec["link"],
            "download_status": status, "local_path": str(path) if status == "downloaded" else "",
        })
    rows.sort(key=lambda r: (r["date_received"], r["datetime_received"], r["ptr_id"]))
    return rows


def write_manifest(rows: list[dict]) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS)
        w.writeheader()
        w.writerows(rows)
