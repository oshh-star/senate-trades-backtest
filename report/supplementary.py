"""Supplementary figures quoted in the final report that no pipeline table holds (added 2026-10-17).

Every number here is computed from committed pipeline outputs, so the report's text can be re-derived on request.
None is a registered test. Run from the repo root, after `python run_all.py --skip-scrape` and
`python run_variants.py` (V21, the departure check, is read from the variant runner's own engine files):

    python report/supplementary.py

Writes report/supplementary.json and report/supplementary.md.

Covers:
  - Section 2.2: positions open at the start of the window
  - Section 2.3, Table 2: share of in-scope transactions received after 15:30 ET; sold stocks after disclosure
  - Section 2.4: Series B pot split (warm-up book, cash) and its cash share on day one
  - Section 4: senators who generate no position
  - Section 5.3: NANC and KRUZ correlations with SPY and with Series A
  - Section 6.4: profit shares (window only), Moody's four semiconductor positions, Mullin's book at departure,
    the departure check (V21) against its own risk-matched SPY
  - Appendix E, Table E2: Series A of Mullin's positions and of all other positions, by calendar year
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.engine import load_market  # noqa: E402
from src.engine.book import Prices  # noqa: E402
from src.engine.portfolio import _matrix  # noqa: E402

PROC = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"
V21_DIR = ROOT / "data" / "interim" / "variants" / "full_bloomberg" / "V21"
W0, W1 = "2021-09-01", "2026-08-31"
MULLIN, MOODY = "M001190", "M001244"
out = {}

lots = pd.read_csv(PROC / "lots.csv", dtype={"entry_date": str, "exit_date": str})
meta = json.loads((PROC / "engine_metadata.json").read_text())
rec = meta["reconciliation"]

# Section 2.2: positions (lots) open at the close before the window
open0 = lots[(lots.entry_date < W0) & (lots.exit_date >= W0)]
out["positions_open_at_window_start"] = int(open0.lot_id.nunique())

# Section 2.3: timing of in-scope records received in the window
tr = pd.read_csv(PROC / "trade_records.csv", low_memory=False, parse_dates=["disclosure_datetime"])
w = tr[(tr.in_scope.astype(str) == "True") & (tr.disclosure_datetime >= W0) & (tr.disclosure_datetime < "2026-09-01")]
mins = w.disclosure_datetime.dt.hour * 60 + w.disclosure_datetime.dt.minute
ptr = w.drop_duplicates("record_ptr_id")
pmins = ptr.disclosure_datetime.dt.hour * 60 + ptr.disclosure_datetime.dt.minute
out["share_transactions_received_after_1530_ET"] = float((mins >= 15 * 60 + 30).mean())
out["share_PTRs_received_after_1530_ET"] = float((pmins >= 15 * 60 + 30).mean())
es = pd.read_csv(TABLES / "phase5_event_study_full.csv")
s21 = es[(es.side == "sale") & (es.horizon_days == 21) & es.version.str.startswith("copier")].iloc[0]
out["sales_copier_21d_vs_SPY"] = {"mean": float(s21["mean"]), "t_clustered": float(s21.t_cluster)}

# Section 2.4: Series B pot
out["series_b_pot"] = {"K": rec["K"], "warmup_book": rec["K_warmup_book"], "cash": rec["K_cash"],
                       "cash_share_day_one": rec["K_cash"] / rec["K"]}

# Section 4: senators in the window who generate no copied position at all
out["senators_in_window"] = int(w.senator.nunique())
out["senators_with_no_position"] = sorted(set(w.senator) - set(lots.senator))

# Section 5.3: ETF correlations over the months both ETFs exist
m = pd.read_csv(PROC / "monthly_returns.csv")
m = m[(m.month >= W0[:7]) & (m.month <= W1[:7])]
e = m.dropna(subset=["r_NANC", "r_KRUZ"])
out["etf_correlations"] = {"months": int(len(e)),
                           "NANC_SPY": float(e.r_NANC.corr(e.r_SPY)), "KRUZ_SPY": float(e.r_KRUZ.corr(e.r_SPY)),
                           "NANC_seriesA": float(e.r_NANC.corr(e.r_A)), "KRUZ_seriesA": float(e.r_KRUZ.corr(e.r_A))}

# Prices and days exactly as the engine uses them
mk = load_market(W1, json.loads(json.dumps(meta["config"], default=str)) | {"prices": {"sources": ["yahoo", "manual"]}})
prices = Prices(mk["prices"], mk["calendar"], mk["last_dates"])
book_days = [d for d in mk["calendar"] if d >= min(lots.entry_date.min(), W0)]
m0 = book_days.index(W0)


def window_pnl(pc: pd.DataFrame) -> float:
    """Each piece's P&L from max(entry, the close before the window): the engine's reconciliation rule."""
    return float(_matrix(pc, prices.ffill, book_days)["pnl"][m0:].sum())


def series_a(pc: pd.DataFrame) -> pd.Series:
    """Series A of a subset of lots: dollar-weighted daily return of the subset's positions held into each day."""
    mx = _matrix(pc, prices.ffill, book_days)
    held = mx["vprev"] > 0
    r = np.where(held, np.divide(mx["pnl"], mx["vprev"], out=np.zeros_like(mx["pnl"]), where=held), np.nan)
    return pd.Series(r, index=pd.to_datetime(book_days))[W0:], pd.Series(mx["capital"], index=pd.to_datetime(book_days))[W0:]


# Check: the subset routine on all lots reproduces the headline Series A
a_all, cap_all = series_a(lots)
book = pd.read_csv(PROC / "daily_book.csv", parse_dates=["date"]).set_index("date")
out["check_series_a_reproduced_max_abs_diff"] = float(np.nanmax(np.abs(a_all.values - book.series_a_return.values)))

# Section 6.4: profit shares over the window (gains and losses from 1 Sep 2021 only)
total = window_pnl(lots)
by_sen = {s: window_pnl(g) for s, g in lots.groupby("bioguide_id")}
out["window_profit_total"] = total
out["window_profit_check_vs_engine"] = total - rec["lot_pnl"]
out["share_profit_mullin_plus_moody"] = (by_sen[MULLIN] + by_sen[MOODY]) / total
out["share_profit_by_senator"] = {lots[lots.bioguide_id == b].senator.iloc[0]: v / total
                                  for b, v in sorted(by_sen.items(), key=lambda x: -x[1])[:6]}
mo = lots[lots.bioguide_id == MOODY]
top4 = mo.groupby("lot_id").apply(window_pnl, include_groups=False).sort_values(ascending=False).head(4)
out["moody"] = {"positions": int(mo.lot_id.nunique()),
                "top4_lots": {k: {"symbol": mo[mo.lot_id == k].val_symbol.iloc[0], "pnl": float(v)} for k, v in top4.items()},
                "top4_pnl": float(top4.sum()), "top4_share_of_window_profit": float(top4.sum() / total)}
mu_open = lots[(lots.bioguide_id == MULLIN) & (lots.exit_reason == "end of window")]
out["mullin_open_at_window_end"] = {"positions": int(mu_open.lot_id.nunique()),
                                    "cost": float(mu_open.entry_dollars.sum())}

# Appendix E, Table E2: Series A of Mullin's positions and of the rest, by calendar year; Mullin's share of capital
a_mu, cap_mu = series_a(lots[lots.bioguide_id == MULLIN])
a_rest, cap_rest = series_a(lots[lots.bioguide_id != MULLIN])
e2 = {}
for y in range(2023, 2027):
    ys = str(y)
    e2[ys] = {"mullin_return": float((1 + a_mu[ys].dropna()).prod() - 1),
              "others_return": float((1 + a_rest[ys].dropna()).prod() - 1),
              "mullin_share_of_capital": float(cap_mu[ys].sum() / (cap_mu[ys].sum() + cap_rest[ys].sum()))}
out["table_E2"] = e2

# Section 6.4: the departure check, V21, against SPY at its own volatility (monthly, as every statistic)
if (V21_DIR / "daily_book.csv").exists():
    d21 = pd.read_csv(V21_DIR / "daily_book.csv", parse_dates=["date"]).set_index("date")
    r21 = (1 + d21.series_a_return).groupby(d21.index.to_period("M")).prod() - 1
    mm = m.set_index(pd.PeriodIndex(m.month, freq="M"))
    ex21, exs = r21.values - mm.rf.values, mm.r_SPY.values - mm.rf.values
    k = ex21.std(ddof=1) / exs.std(ddof=1)
    rm = mm.rf.values + k * exs
    ann = lambda r: float(np.prod(1 + r) ** (12 / len(r)) - 1)
    out["departure_check_V21"] = {"departure_days": "first trading day after the end of continuous Senate service",
                                  "series_a": ann(r21.values), "k": float(k), "risk_matched_spy": ann(rm),
                                  "gap_vs_risk_matched": ann(r21.values) - ann(rm),
                                  "change_vs_headline": ann(r21.values) - ann(mm.r_A.values)}
else:
    out["departure_check_V21"] = "run `python run_variants.py --only V21` first"

(ROOT / "report" / "supplementary.json").write_text(json.dumps(out, indent=1, default=str))
md = ["# Supplementary figures for the final report (not registered tests)", "",
      "_Built by report/supplementary.py from committed pipeline outputs._", "",
      "```json", json.dumps(out, indent=1, default=str), "```"]
(ROOT / "report" / "supplementary.md").write_text("\n".join(md) + "\n")
print(json.dumps(out, indent=1, default=str))
