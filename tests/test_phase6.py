"""Phase 6 prep: variant runner (config switches, firewall), scope recomputation, mechanism splits."""
import copy
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.config import load_config
from src.engine import events as evm
from src import variants as vr


def test_rescope_equals_the_clean_stage_for_the_default_config():
    cfg = load_config()
    raw = pd.read_csv("data/processed/trade_records.csv", keep_default_na=False, dtype={"ticker": str, "price_ticker": str})
    u = evm.load_units(cfg)
    assert (u["in_scope"].to_numpy() == (raw["in_scope"].astype(str) == "True").to_numpy()).all()
    assert (u["in_scope_ex_window"].to_numpy() == (raw["in_scope_ex_window"].astype(str) == "True").to_numpy()).all()


def test_rescope_switches_owners_etfs_and_preferred():
    cfg = load_config()
    u = pd.DataFrame({"scope_base": [True] * 5, "owner": ["Self", "Spouse", "Self", "Self", "Self"],
                      "is_etf": [False, False, True, True, False], "etf_class": ["", "", "equity", "fixed_income", ""],
                      "is_preferred": [False, False, False, False, True],
                      "disclosure_date": ["2022-01-03"] * 5})
    assert evm.rescope(u, cfg)["in_scope"].tolist() == [True, False, True, False, False]           # headline
    c = copy.deepcopy(cfg)
    c["universe"]["owners"] = ["Self", "Joint", "Spouse", "Child"]                                   # V6
    assert evm.rescope(u, c)["in_scope"].tolist()[1]
    c = copy.deepcopy(cfg)
    c["universe"]["etf_classes"] = vr.ALL_ETF_CLASSES                                                # V16
    assert evm.rescope(u, c)["in_scope"].tolist()[3]
    c = copy.deepcopy(cfg)
    c["universe"]["include_etfs"] = False                                                           # V5
    assert not evm.rescope(u, c)["in_scope"].tolist()[2]
    c = copy.deepcopy(cfg)
    c["universe"]["include_preferred"] = True                                                       # V19
    assert evm.rescope(u, c)["in_scope"].tolist()[4]


def test_every_preregistered_variant_is_expanded_with_its_switch():
    runs = vr.expand(load_config(), None)
    ids = [r["id"] for r in runs]
    assert ids[:1] == ["V1"] and "V2.1" in ids and "V2.5" in ids and "V19" in ids and "V21" in ids and len(ids) == 25
    v20 = next(r for r in runs if r["id"] == "V20")                       # S3, C1: CRSP after the headline sources
    assert v20["cfg"]["prices"]["sources"] == ["yahoo", "manual", "crsp"]
    v17 = next(r for r in runs if r["id"] == "V17")
    assert v17["cfg"]["engine"]["warmup_months"] == 0
    v2 = next(r for r in runs if r["id"] == "V2.3")
    assert v2["cfg"]["engine"]["drop_senator_ranks"] == [3]


def test_the_runner_refuses_a_variant_past_the_firewall(tmp_path):
    base = load_config()
    run = next(r for r in vr.expand(base, ["V11"]))
    row = vr.run_one(run, tmp_path, "2024-02-29", unlocked=False)
    assert row["status"].startswith("not run") and "firewall" in row["status"]


def test_mechanism_groups_and_difference_row():
    from src.metrics import mechanism as mc
    rng = np.random.default_rng(0)
    n = 60
    months = [f"2022-{m:02d}-03" for m in range(1, 13)] * 5
    p = pd.DataFrame({"side": "purchase", "entry_date": months, "size_group": np.where(np.arange(n) < 30, "small", "large"),
                      **{f"x_entry_{h}": rng.normal(0, 0.01, n) for h in mc.HORIZONS},
                      **{f"x_txn_{h}": rng.normal(0, 0.01, n) for h in mc.HORIZONS}, "gap_x": rng.normal(0, 0.01, n)})
    p.loc[p["size_group"] == "small", "x_entry_21"] += 0.05
    p["entry_month"] = p["entry_date"].str[:7]
    t = mc.split_table(p, "size_group", ["small", "large"]).set_index("group")
    d = t.loc["difference (small minus large)"]
    assert d["copier_21_mean"] == pytest.approx(0.05, abs=0.01) and d["copier_21_t"] > 5
    assert t.loc["small", "events"] == 30


def test_committee_classification_uses_the_membership_on_the_trade_date(tmp_path, monkeypatch):
    from src.metrics import committee as cm
    from src.metrics import mechanism as mc
    (tmp_path / "map.yaml").write_text("committees:\n  SSAS: {name: Armed Services, oversees: defence, sic: [[3760, 3769]]}\n")
    pd.DataFrame({"commit": ["c1", "c2"], "commit_date": ["2022-01-01", "2022-06-01"], "committee_id": ["SSAS", "SSFI"],
                  "bioguide": ["B1", "B1"], "name": "x", "party": "R", "rank": 1, "title": ""}).to_csv(tmp_path / "m.csv", index=False)
    pd.DataFrame({"symbol": ["LMT", "AAPL"], "sic": ["3760", "3571"]}).to_csv(tmp_path / "sic.csv", index=False)
    monkeypatch.setattr(cm, "MAPPING", tmp_path / "map.yaml")
    monkeypatch.setattr(cm, "MEMBERSHIP", tmp_path / "m.csv")
    monkeypatch.setattr(cm, "SIC", tmp_path / "sic.csv")
    monkeypatch.setattr(mc, "attach", lambda p: p)
    panel = pd.DataFrame({"bioguide_id": "B1", "price_ticker": ["LMT", "LMT", "AAPL", "LMT"], "is_etf": [False, False, False, True],
                          "transaction_date": ["2022-03-01", "2022-07-01", "2022-03-01", "2022-03-01"]})
    g = cm.classify(panel)["committee_group"].tolist()
    # on SSAS in March (version c1), moved to SSFI by July (version c2); AAPL is not defence; the ETF is left out
    assert g == [cm.OVERSEEN, cm.NOT, cm.NOT, "left out: ETF"]


def test_departure_rule_is_off_in_the_headline_and_sells_on_departure_in_v21():
    """D1 (2026-10-17): the headline has no departure exits; V21 closes a departed senator's lots at the first close
    after their service ends and copies none of their later purchases."""
    import yaml
    from src.engine import departure_days
    cfg = yaml.safe_load(open("config/config.yaml"))
    assert not cfg.get("engine", {}).get("sell_on_departure", False)
    lots = pd.read_csv("data/processed/lots.csv")
    assert "senator left office" not in set(lots["exit_reason"])
    cal = pd.read_csv("data/processed/trading_calendar.csv", dtype=str)["date"].tolist()
    dep = departure_days([d for d in cal if "2020-09-09" <= d <= "2026-08-31"], "2026-08-31")
    assert dep["M001190"] == "2026-03-24"          # Mullin's service ended 2026-03-23
    assert "A000383" not in dep                     # Armstrong is still serving at the window end
