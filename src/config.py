"""Load config/config.yaml and derive the analysis window and the in/out-of-sample split."""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import yaml

CONFIG_PATH = Path("config/config.yaml")


def load_config(path: str | Path = CONFIG_PATH) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def analysis_window(cfg: dict) -> tuple[dt.date, dt.date]:
    """(start, end) of the disclosure-date window, both inclusive."""
    end = cfg["analysis"]["window_end"]
    years = int(cfg["analysis"]["window_years"])
    start = end.replace(year=end.year - years) + dt.timedelta(days=1)
    scrape_start = cfg["data"]["scrape_start"]
    if start < scrape_start:
        raise ValueError(f"Window start {start} is before the scrape start {scrape_start}")
    return start, end


def sample_split(cfg: dict) -> dict:
    """In-sample = first half of the window, out-of-sample = second half."""
    start, end = analysis_window(cfg)
    mid = start + (end - start) / 2
    return {"in_sample": (start, mid), "out_of_sample": (mid + dt.timedelta(days=1), end)}


class OutOfSampleLocked(RuntimeError):
    pass


def require_oos_unlocked(cfg: dict) -> None:
    """Call before computing ANY out-of-sample number."""
    if not cfg["oos"].get("oos_unlocked", False):
        raise OutOfSampleLocked(
            "Out-of-sample results are locked. Set oos.oos_unlocked: true only after adding a "
            "docs/DECISIONS.md entry recording the commit hash at which the rules were frozen.")
    if not cfg["project"].get("frozen_rules_commit"):
        raise OutOfSampleLocked("oos_unlocked is true but project.frozen_rules_commit is empty.")


def user_agent(cfg: dict) -> str:
    return cfg["scrape"]["user_agent"].format(contact_email=cfg["scrape"]["contact_email"])
