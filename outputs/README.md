# Outputs: what each file is

Every file here is rebuilt by `python run_all.py --skip-scrape` (and `python run_variants.py` for the variants).
Most tables come as a readable `.md` and an unrounded `.csv` twin with the same name.

## The files the report uses

| Report | What it shows | File |
|---|---|---|
| Table 2, Figure 2 | **Main result**: Series A and B against SPY, risk-matched SPY, the Senate universe and the factor models, full window 2021-09 to 2026-08; calendar years; worst 12 months; NANC and KRUZ | `tables/phase5_full_results.md` |
| Table 3 | **Test half** (2024-03 to 2026-08), the same statistics read off the same run | `tables/phase5_oos_results.md` |
| Tables 4 and 5, Figure 3 | **The registered tests H0 to H4**, with Holm p-values, detectable effects, the without-bulk-filings check and the H2 reversal check | `tables/confirmatory_oos.md` |
| Figure 4 | **Senator against copier**: returns after the trade and after disclosure, at 5 to 252 trading days | `tables/phase5_event_study_full.md`, `tables/phase5_predisclosure_drift_full.md` |
| Table 6, Appendix E | **Every variant**, full window and its own test half | `tables/variants_full_bloomberg.md` |
| Appendix F | Exploratory splits by filing lag, size, party, senator and committee | `tables/mechanism_full_bloomberg.md`, `tables/committee_full_bloomberg.md` |
| Appendices A and B | Every exclusion counted, concentration by senator, filing lags, survivorship ledger | `data_quality.md` |
| Appendix G | Three copied trades traced by hand | `phase4_worked_examples.md` |

The report's own charts and extra diagnostics are in `../report/` (`build_figures.py`, `diagnostics.py`).

## Supporting files

| Group | Files | Why they are kept |
|---|---|---|
| **Design-half record, frozen** | `tables/phase5_insample_results.md`, `confirmatory_insample.md`, `phase5_event_study.md`, `phase5_predisclosure_drift.md`, `*_insample_yahoo.*` | The results that existed when the rules were frozen (commit 348318447daa), on Yahoo prices. They prove what was known before the test half was opened, so they are never overwritten (DECISIONS.md E58 d, C2). |
| **Test-half exploratory tables** | `tables/*_oos*` other than `phase5_oos_results.md` and `confirmatory_oos.md` | The event study, drift, mechanism and committee tables for the test half alone. Exploratory, not tests. |
| **Event lists** | `tables/committee_*_events.csv` | One row per trade behind each committee split, so any cell can be re-derived. |
| **Warm-up check** | `tables/phase5_warmup_before_after.csv` | The book with and without the 12-month warm-up (decision L2, variant V17). |
| **Pipeline figures** | `figures/` | Charts drawn by the pipeline itself; the report uses its own versions from `../report/figures/`. |
| **First look** | `phase1_summary.md` | Filing counts by year and owner, before any filtering. |

Names: `full` = 2021-09 to 2026-08, `oos` = test half 2024-03 to 2026-08, `insample` = design half 2021-09 to 2024-02;
`bloomberg` = headline prices after correction C1 (Yahoo plus Bloomberg files for 8 stocks), `yahoo` = Yahoo only.
