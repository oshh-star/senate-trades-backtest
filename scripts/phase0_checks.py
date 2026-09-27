"""Phase 0 environment checks. Run from the repo root:

    python scripts/phase0_checks.py all
    python scripts/phase0_checks.py connectivity | efd | counts | prices | factors

Small outputs are saved to data/raw/_dryrun/. Nothing here is used by the pipeline.
Uses only the standard library, requests and pyyaml, so it runs before requirements.txt
is installed.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import sys
import time
import zipfile
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import load_config, user_agent  # noqa: E402
from src.scrape.efd import FILER_TYPES, EfdClient, parse_ptr, parse_search_row  # noqa: E402

OUT = Path("data/raw/_dryrun")
CFG = load_config()
UA = user_agent(CFG)

# One representative URL per allowed domain (wildcards tested on a real subdomain).
DOMAINS = [
    ("efdsearch.senate.gov", "https://efdsearch.senate.gov/search/home/"),
    ("*.yahoo.com", "https://query1.finance.yahoo.com/v8/finance/chart/SPY?range=5d&interval=1d"),
    ("stooq.com", "https://stooq.com/q/d/l/?s=spy.us&i=d"),
    ("*.stooq.com", "https://www.stooq.com/"),
    ("mba.tuck.dartmouth.edu", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html"),
    ("www.sec.gov", "https://www.sec.gov/files/company_tickers.json"),
    ("data.sec.gov", "https://data.sec.gov/submissions/CIK0000320193.json"),
    ("fred.stlouisfed.org", "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS3MO"),
    ("theunitedstates.io", "https://theunitedstates.io/congress-legislators/legislators-current.json"),
    ("pypi.org (package manager)", "https://pypi.org/simple/pandas/"),
    ("files.pythonhosted.org (package manager)", "https://files.pythonhosted.org/"),
]


def save(name: str, text: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(text)


def connectivity() -> None:
    lines = ["| Domain | HTTP status | Note |", "|---|---|---|"]
    for domain, url in DOMAINS:
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
            status = str(r.status_code)
            if r.headers.get("x-deny-reason") or "not in allowlist" in r.text[:200]:
                note = "blocked by cloud network allowlist"
            elif r.status_code == 403 and "sec.gov" in url:
                note = "SEC refuses requests without a contact email in the User-Agent"
            else:
                note = "ok" if r.ok else "reachable, site returned an error"
        except requests.RequestException as e:
            status, note = "no response", type(e).__name__ + ": " + str(e)[:80].replace("|", "/")
            if "403" in str(e) and "Tunnel" in str(e):
                note = "blocked by cloud network allowlist"
        lines.append(f"| {domain} | {status} | {note} |")
        time.sleep(1)
    table = "\n".join(lines)
    print(table)
    save("connectivity.md", f"Checked {dt.datetime.now():%Y-%m-%d %H:%M} UTC\n\n{table}\n")


def efd() -> None:
    c = EfdClient(UA, CFG["scrape"]["min_seconds_between_requests"])
    c.agree()
    print("Terms agreement accepted; session cookie set.")
    result = {}
    for label in ("senator", "former_senator", "candidate"):
        rows, total = c.search_all([FILER_TYPES[label]], "09/01/2025", "09/30/2025")
        result[label] = [parse_search_row(r) | {"filer_type": label} for r in rows]
        assert len(rows) == total, (label, len(rows), total)
    save("efd_search_2025-09.json", json.dumps(result, indent=1))
    included = result["senator"] + result["former_senator"]
    elec = [r for r in included if r["kind"] == "electronic"]
    paper = [r for r in included if r["kind"] == "paper"]
    print(f"\nPTRs received September 2025 (filer types Senator + Former Senator): {len(included)}")
    print(f"  Senator (type 1): {len(result['senator'])}  Former Senator (type 5): "
          f"{len(result['former_senator'])}  [Candidate (type 4, excluded): {len(result['candidate'])}]")
    print(f"  Electronic: {len(elec)}  Paper: {len(paper)}  "
          f"Amendments: {sum(r['is_amendment'] for r in included)}")
    for r in included:
        print(f"   {r['date_received']}  {r['kind']:<10} {r['filer_type']:<15} {r['office']:<35} {r['title']}")

    # Parse one electronic PTR: the first with at least one ticker, else the first.
    for r in elec:
        html = c.fetch_report(r["link"])
        ptr = parse_ptr(html)
        if any(t.get("Ticker", "--") != "--" for t in ptr["transactions"]) or r is elec[-1]:
            break
    save(f"ptr_{r['report_id']}.html", html)
    save(f"ptr_{r['report_id']}.json", json.dumps(ptr, indent=1))
    print(f"\nSample PTR: {ptr['filer']} | {ptr['title']} | filed {ptr['filed_date']} {ptr['filed_time']}")
    print(f"Link: https://efdsearch.senate.gov{r['link']}")
    print(markdown_table(ptr["columns"], [[t.get(k, "") for k in ptr["columns"]] for t in ptr["transactions"]]))
    print(f"\n({c.n_requests} requests to eFD)")


def counts() -> None:
    c = EfdClient(UA, CFG["scrape"]["min_seconds_between_requests"])
    today = dt.date.today()
    rows = []
    for year in range(2016, 2027):
        end = min(dt.date(year, 12, 31), today)
        n = {k: c.count([v], f"01/01/{year}", end.strftime("%m/%d/%Y")) for k, v in FILER_TYPES.items()}
        rows.append([year, n["senator"], n["former_senator"], n["candidate"],
                     n["senator"] + n["former_senator"]])
        print(rows[-1])
    total = sum(r[4] for r in rows)
    table = markdown_table(["Year", "Senator (1)", "Former Senator (5)", "Candidate (4, excluded)",
                            "Included PTRs"], rows + [["Total", "", "", "", total]])
    print(table)
    save("ptr_counts_by_year.md", f"Search counts, date received, checked {today}\n\n{table}\n")


def prices() -> None:
    start, end = dt.date(2025, 9, 1), dt.date(2025, 9, 30)
    try:
        import yfinance as yf
        df = yf.download("SPY", start=start, end=end + dt.timedelta(days=1), auto_adjust=False, progress=False)
        print("yfinance OK")
        print(df[["Adj Close"]].to_string())
        df.to_csv(OUT / "spy_2025-09_yfinance.csv")
        return
    except ImportError:
        print("yfinance is not installed (PyPI blocked); calling Yahoo's chart API directly, "
              "which is the same endpoint yfinance uses.")
    except Exception as e:  # rate limit or block
        print(f"yfinance failed: {e}")
    p1 = int(dt.datetime(2025, 9, 1, tzinfo=dt.timezone.utc).timestamp())
    p2 = int(dt.datetime(2025, 10, 1, tzinfo=dt.timezone.utc).timestamp())
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/SPY?period1={p1}&period2={p2}"
           "&interval=1d&events=div,splits")
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
        r.raise_for_status()
        res = r.json()["chart"]["result"][0]
        adj = res["indicators"]["adjclose"][0]["adjclose"]
        close = res["indicators"]["quote"][0]["close"]
        rows = [[dt.datetime.fromtimestamp(t, dt.timezone.utc).date(), f"{c:.4f}", f"{a:.4f}"]
                for t, c, a in zip(res["timestamp"], close, adj)]
        print(f"Yahoo chart API OK: {len(rows)} trading days")
        print(markdown_table(["Date", "Close", "Adj Close"], rows))
        save("spy_2025-09_yahoo.csv", "date,close,adj_close\n" + "\n".join(",".join(map(str, x)) for x in rows) + "\n")
    except Exception as e:
        print(f"Yahoo failed: {e}")
    try:
        r = requests.get("https://stooq.com/q/d/l/?s=spy.us&d1=20250901&d2=20250930&i=d",
                         headers={"User-Agent": UA}, timeout=30)
        print(f"Stooq: HTTP {r.status_code}\n{r.text[:500]}")
        save("spy_2025-09_stooq.csv", r.text)
    except Exception as e:
        print(f"Stooq failed: {type(e).__name__}: {e}")


def _french_csv(url: str) -> tuple[list[str], list[list[str]]]:
    r = requests.get(url, headers={"User-Agent": UA}, timeout=60)
    r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    text = z.read(z.namelist()[0]).decode("latin-1")
    save(Path(url).name.replace(".zip", ".csv"), text)
    header, data = None, []
    for row in csv.reader(io.StringIO(text)):
        cells = [x.strip() for x in row]
        if header is None and len(cells) > 1 and cells[0] == "" and cells[1]:
            header = ["Date"] + cells[1:]
        elif header and cells and cells[0].isdigit() and len(cells[0]) == 8:
            data.append(cells)
        elif header and data and not (cells and cells[0].isdigit()):
            break  # end of the daily block
    return header, data


def factors() -> None:
    for key in ("daily_3factor_url", "daily_momentum_url"):
        header, data = _french_csv(CFG["factors"][key])
        print(f"\n{Path(CFG['factors'][key]).name}: {len(data)} daily rows, "
              f"{data[0][0]} to {data[-1][0]} (values in percent)")
        print(markdown_table(header, data[-5:]))
        time.sleep(1)


def markdown_table(header, rows) -> str:
    out = ["| " + " | ".join(map(str, header)) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(x) for x in r) + " |" for r in rows]
    return "\n".join(out)


CHECKS = {"connectivity": connectivity, "efd": efd, "counts": counts, "prices": prices, "factors": factors}

if __name__ == "__main__":
    names = sys.argv[1:] or ["all"]
    for name in (CHECKS if names == ["all"] else names):
        print(f"\n===== {name} =====")
        CHECKS[name]()
