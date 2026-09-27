import datetime as dt

import pytest

from src.config import (OutOfSampleLocked, analysis_window, load_config, require_oos_unlocked,
                        sample_split)


def test_default_window_is_five_years():
    assert analysis_window(load_config()) == (dt.date(2021, 10, 1), dt.date(2026, 9, 30))


@pytest.mark.parametrize("years,start", [(3, dt.date(2023, 10, 1)), (10, dt.date(2016, 10, 1))])
def test_window_variants(years, start):
    cfg = load_config()
    cfg["analysis"]["window_years"] = years
    assert analysis_window(cfg)[0] == start


def test_split_halves_are_contiguous():
    s = sample_split(load_config())
    assert s["in_sample"][1] + dt.timedelta(days=1) == s["out_of_sample"][0]


def test_oos_firewall_is_locked_by_default():
    with pytest.raises(OutOfSampleLocked):
        require_oos_unlocked(load_config())


def test_oos_unlock_needs_frozen_commit():
    cfg = load_config()
    cfg["oos"]["oos_unlocked"] = True
    with pytest.raises(OutOfSampleLocked):
        require_oos_unlocked(cfg)
    cfg["project"]["frozen_rules_commit"] = "abc1234"
    require_oos_unlocked(cfg)


def test_amended_spec_values():
    cfg = load_config()
    assert cfg["universe"]["owners"] == ["Self", "Joint"]
    assert cfg["universe"]["include_etfs"] is True
    assert cfg["prices"]["price_source"] in ("yahoo", "crsp")
    assert cfg["data"]["include_filer_types"] == [1, 5]
