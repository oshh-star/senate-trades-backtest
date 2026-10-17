# Outputs: what each file is

Every file here is rebuilt by `python run_all.py --skip-scrape` (and `python run_variants.py` for the variants).
Most tables come as a readable `.md` and an unrounded `.csv` twin with the same name.

## The files the final report uses

Numbering follows `report/Copying_the_US_Senate_Study_Group_B12_final.pdf`.

| In the report | What it shows | File |
|---|---|---|
| Table 1, Table 3, Figure 1 | **Main result**: Series A and B against SPY, risk-matched SPY, the Senate universe and the factor models, full Window | `tables/phase5_full_results.md` |
| Table 4 | **Test Period** and calendar years; the Design Period under the headline prices | `tables/phase5_oos_results.md`, `tables/phase5_full_results.md` (calendar years, worst 12 months), `../report/diagnostics.json` (Design Period) |
| Table 5, Figure H1 | **The registered tests H0 to H4**, with Holm p-values and the without-bulk-filings check | `tables/confirmatory_oos.md` |
| Figure 2 | **Senator against copier**: returns after the trade and after disclosure | `tables/phase5_event_study_full.md`, `tables/phase5_predisclosure_drift_full.md` |
| Section 5.3 | NANC and KRUZ | `tables/phase5_full_results.md` (panel 2); correlations with Series A in `../report/supplementary.json` |
| Section 6.4, Table E2, Figure E1 | Profit by senator, Moody's positions, Mullin's book, the departure check | `../report/supplementary.json`; the departure check is variant V21 in `tables/variants_full_bloomberg.md` |
| Table 6, Table I1, Figure I1 | **Every alternative specification**, full Window and its own Test Period | `tables/variants_full_bloomberg.md` |
| Section 6.5, Table G1, Figure G2 | Power, bootstrap, Sharpe-difference test, rolling alpha | `../report/diagnostics.json`, `../report/rolling_alpha_24m.csv` |
| Sections 2 and 4, Appendix D, Table E1 | Counts, exclusions, filing lags, survivorship | `data_quality.md`; the smaller counts (70 opening positions, transactions after 15:30, senators with no position, Series B split) in `../report/supplementary.json` |
| Appendix B | One copied trade traced by hand | `phase4_worked_examples.md` |
| Appendix F | Effect of the Bloomberg prices | `../docs/DECISIONS.md`, corrections C1 and C2 |

The report's charts are restyled versions of those drawn by `../report/build_figures.py` from the same files.

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
