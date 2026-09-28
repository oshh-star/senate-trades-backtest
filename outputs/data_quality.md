# Data quality log

Every exclusion and every data problem, counted and explained. One section per phase.

## Phase 1: scrape

- Filings in the eFD listing (received 2016-01-01 to 2026-09-30, all filer types): **1,874**; electronic **1,566**, paper **308**, other **0**.
- Electronic PTRs downloaded: **1,566**; failed: **0**; pending: **0**.
- Listing fetched on or before the scrape end date is refreshed automatically on the next run (the 2026 listing is incomplete until after 2026-09-30).

### Download failures

None.

### Paper filings (excluded, D05)

**308** paper filings are scanned images and cannot be parsed; they are excluded. The full list (senator, date, link) is in `data/interim/paper_filings.csv`. By filer:

| filer_name         |   Paper filings |
|:-------------------|----------------:|
| RICHARD BLUMENTHAL |             118 |
| JOHN BOOZMAN       |              74 |
| RICHARD M BURR     |              63 |
| DIANNE FEINSTEIN   |              37 |
| MARK R WARNER      |              14 |
| JAMES M INHOFE     |               1 |
| JOHN FETTERMAN     |               1 |

### Parse validation

Each of the 1,566 downloaded PTRs was checked three ways: rows parsed, `<tbody>` rows counted by a separate parser, and the page's own "(N transactions total)" line.

- Row-count mismatches: **0**
- Owner-count mismatches (page's "N Self / N Spouse ..." line vs parsed Owner column): **0**
- Transaction rows whose date could not be read as MM/DD/YYYY: **0**
- Downloaded PTRs with no "Filed ... @ time" timestamp: **0**
- PTRs whose page "Filed" date differs from the listing's date received: **0**

### Senate service dates (A05)

`data/interim/senate_terms.csv`: 407 Senate terms ending on or after 2010-01-01, 208 senators. 42 terms ended before their scheduled 3 January end; the dataset records the actual last day for each, listed below. An appointee's term that ends at a special election is listed too.

| full_name           | state   | party      | term_start   | term_end   | scheduled_end   | start_how   | end_type         |
|:--------------------|:--------|:-----------|:-------------|:-----------|:----------------|:------------|:-----------------|
| Jeff Sessions       | AL      | Republican | 2015-01-06   | 2017-02-08 | 2021-01-03      |             |                  |
| Luther Strange      | AL      | Republican | 2017-02-09   | 2018-01-03 | 2021-01-03      | appointment |                  |
| John McCain         | AZ      | Republican | 2017-01-03   | 2018-08-25 | 2023-01-03      |             |                  |
| Jon Kyl             | AZ      | Republican | 2018-09-05   | 2018-12-31 | 2023-01-03      | appointment |                  |
| Martha McSally      | AZ      | Republican | 2019-01-03   | 2020-12-02 | 2023-01-03      | appointment | special-election |
| Dianne Feinstein    | CA      | Democrat   | 2019-01-03   | 2023-09-28 | 2025-01-03      |             |                  |
| Laphonza R. Butler  | CA      | Democrat   | 2023-10-03   | 2024-12-08 | 2025-01-03      | appointment | special-election |
| Kamala D. Harris    | CA      | Democrat   | 2017-01-03   | 2021-01-18 | 2023-01-03      |             |                  |
| Alex Padilla        | CA      | Democrat   | 2021-01-20   | 2022-12-21 | 2023-01-03      | appointment |                  |
| Edward Kaufman      | DE      | Democrat   | 2009-01-16   | 2010-11-15 | 2015-01-03      | appointment |                  |
| Marco Rubio         | FL      | Republican | 2023-01-03   | 2025-01-20 | 2029-01-03      |             |                  |
| Ashley Moody        | FL      | Republican | 2025-01-21   | 2026-11-03 | 2029-01-03      | appointment | special-election |
| Johnny Isakson      | GA      | Republican | 2017-01-03   | 2019-12-31 | 2023-01-03      |             |                  |
| Kelly Loeffler      | GA      | Republican | 2020-01-06   | 2021-01-20 | 2023-01-03      | appointment | special-election |
| Daniel K. Inouye    | HI      | Democrat   | 2011-01-05   | 2012-12-17 | 2017-01-03      |             |                  |
| Brian Schatz        | HI      | Democrat   | 2012-12-27   | 2015-01-03 | 2017-01-03      | appointment |                  |
| Roland Burris       | IL      | Democrat   | 2009-01-15   | 2010-11-29 | 2011-01-03      | appointment |                  |
| Paul Kirk           | MA      | Democrat   | 2009-09-25   | 2010-02-04 | 2013-01-03      | appointment |                  |
| John F. Kerry       | MA      | Democrat   | 2009-01-06   | 2013-02-01 | 2015-01-03      |             |                  |
| William M. Cowan    | MA      | Democrat   | 2013-02-06   | 2013-07-16 | 2015-01-03      | appointment |                  |
| Al Franken          | MN      | Democrat   | 2015-01-06   | 2018-01-02 | 2021-01-03      |             |                  |
| Tina Smith          | MN      | Democrat   | 2018-01-03   | 2018-11-06 | 2021-01-03      | appointment | special-election |
| Thad Cochran        | MS      | Republican | 2015-01-06   | 2018-04-01 | 2021-01-03      |             |                  |
| Cindy Hyde-Smith    | MS      | Republican | 2018-04-09   | 2018-11-27 | 2021-01-03      | appointment | special-election |
| Max Baucus          | MT      | Democrat   | 2009-01-06   | 2014-02-06 | 2015-01-03      |             |                  |
| Ben Sasse           | NE      | Republican | 2021-01-03   | 2023-01-08 | 2027-01-03      |             |                  |
| Pete Ricketts       | NE      | Republican | 2023-01-23   | 2024-11-05 | 2027-01-03      | appointment | special-election |
| Robert Menendez     | NJ      | Democrat   | 2019-01-03   | 2024-08-20 | 2025-01-03      |             |                  |
| George S. Helmy     | NJ      | Democrat   | 2024-09-09   | 2024-12-08 | 2025-01-03      | appointment |                  |
| Frank R. Lautenberg | NJ      | Democrat   | 2009-01-06   | 2013-06-03 | 2015-01-03      |             |                  |
| Jeff Chiesa         | NJ      | Republican | 2013-06-10   | 2013-10-31 | 2015-01-03      | appointment |                  |
| John Ensign         | NV      | Republican | 2007-01-04   | 2011-05-03 | 2013-01-03      |             |                  |
| J.D. Vance          | OH      | Republican | 2023-01-03   | 2025-01-09 | 2029-01-03      |             |                  |
| Jon Husted          | OH      | Republican | 2025-01-21   | 2026-11-03 | 2029-01-03      | appointment | special-election |
| James M. Inhofe     | OK      | Republican | 2021-01-03   | 2023-01-03 | 2027-01-03      |             |                  |
| Markwayne Mullin    | OK      | Republican | 2023-01-03   | 2026-03-23 | 2027-01-03      |             |                  |
| Tom Coburn          | OK      | Republican | 2011-01-05   | 2015-01-03 | 2017-01-03      |             |                  |
| Lindsey Graham      | SC      | Republican | 2021-01-03   | 2026-07-11 | 2027-01-03      |             |                  |
| Jim DeMint          | SC      | Republican | 2011-01-05   | 2013-01-01 | 2017-01-03      |             |                  |
| Tim Scott           | SC      | Republican | 2013-01-03   | 2015-01-03 | 2017-01-03      | appointment |                  |
| Robert Byrd         | WV      | Democrat   | 2007-01-04   | 2010-06-28 | 2013-01-03      |             |                  |
| Carte Goodwin       | WV      | Democrat   | 2010-07-20   | 2010-11-14 | 2013-01-03      | appointment |                  |

Checks for departures the dataset may NOT record (a successor in the same seat starting before the predecessor's recorded end; a historical senator with a future end date; a current senator whose last term has ended): **0** found.


### Filer name matching

82 distinct filer names: override 1, exact 80, fuzzy 1, ambiguous 0, unmatched 0. Unmatched or low-confidence: **0** (listed in outputs/phase1_summary.md section 8; their transactions are left out of the key number).

- Matched filers none of whose transactions fall inside that senator's service (would suggest the wrong person): **0**
- Transactions by high-confidence matched filers dated OUTSIDE Senate service (excluded by A05 in Phase 2): **5** of 14,558.

| matched_name    |   Rows outside service |
|:----------------|-----------------------:|
| John R. Curtis  |                      3 |
| David McCormick |                      1 |
| Pete Ricketts   |                      1 |

## Phase 2: clean

_Stage `clean` of `python run_all.py`. Default window: disclosures 2021-09-01 to 2026-08-31 (5 years). Owners: Self, Joint. ETFs included: True. Counts and disclosed dollar ranges only; no prices or returns. Files: `data/processed/trades_clean.csv` (every unique trade in the 3/5/10-year windows that passes every filter except owner, `in_scope` = headline sample), `data/processed/exclusions.csv` (every raw row that is not an in-scope trade, with its reason), `data/processed/tickers.csv`._

### 1. Waterfall: raw rows to in-scope trades

Each row is removed at the FIRST step it fails, in this order. Steps 1-2 count raw rows; from step 3 on, each row is one unique trade (a trade reported in several filings counts once).

| Step   | Reason code         | What happens                                                                     | Removed   |   Left |
|:-------|:--------------------|:---------------------------------------------------------------------------------|:----------|-------:|
| 0      |                     | All parsed transaction rows (Phase 1)                                            |           |  14558 |
| 1      | FILER_UNMATCHED     | Filer not matched to a senator with high confidence                              | 0         |  14558 |
| 2      | DUPLICATE_AMENDMENT | Duplicate: trade restated in an amendment (kept once, first disclosure datetime) | 2158      |  12400 |
| 3      | DUPLICATE_REFILED   | Duplicate: trade repeated from another, unrelated filing                         | 24        |  12376 |
|        |                     | = unique trades                                                                  |           |  12376 |
| 4      | OUTSIDE_SERVICE     | Transaction date outside the senator's Senate service (A05)                      | 5         |  12371 |
| 5      | OUTSIDE_WINDOW      | First disclosure outside the analysis window                                     | 7091      |   5280 |
| 6      | ASSET_TYPE          | eFD asset type is not Stock or Other                                             | 1356      |   3924 |
| 7      | OPTION_IN_NAME      | Asset name shows a call/put option                                               | 33        |   3891 |
| 8      | EXCHANGE            | Exchange transaction (not a purchase or sale)                                    | 24        |   3867 |
| 9      | NO_TICKER           | No ticker, and none recovered from the asset name                                | 236       |   3631 |
| 10     | MUTUAL_FUND         | Yahoo: mutual fund                                                               | 65        |   3566 |
| 11     | OTHER_INSTRUMENT    | Yahoo: neither equity, ETF nor mutual fund                                       | 1         |   3565 |
| 12     | NON_US_LISTING      | Yahoo: not listed in the US                                                      | 0         |   3565 |
| 13     | AMOUNT_UNPARSED     | Amount string not understood                                                     | 0         |   3565 |
| 14     | OWNER               | Owner not in universe.owners                                                     | 1052      |   2513 |
|        |                     | = IN-SCOPE TRADES (headline sample)                                              |           |   2513 |

Owner type by reason (A01: Spouse and Child trades are counted, not silently dropped):

| reason_code         |   Child |   Joint |   Self |   Spouse |
|:--------------------|--------:|--------:|-------:|---------:|
| DUPLICATE_AMENDMENT |      17 |   1,176 |    168 |      797 |
| DUPLICATE_REFILED   |       1 |       2 |      6 |       15 |
| OUTSIDE_SERVICE     |       0 |       3 |      0 |        2 |
| OUTSIDE_WINDOW      |     127 |   3,172 |  1,037 |    2,755 |
| ASSET_TYPE          |      88 |     434 |    382 |      452 |
| OPTION_IN_NAME      |       0 |       0 |     33 |        0 |
| EXCHANGE            |       0 |       7 |      8 |        9 |
| NO_TICKER           |      17 |       6 |     32 |      181 |
| MUTUAL_FUND         |       0 |      24 |      7 |       34 |
| OTHER_INSTRUMENT    |       0 |       0 |      0 |        1 |
| OWNER               |      39 |       0 |      0 |    1,013 |
| (in scope)          |       0 |   1,423 |  1,090 |        0 |
| Total               |     289 |   6,247 |  2,763 |    5,259 |

ASSET_TYPE detail (in-window trades only; earlier steps took the rest):

| eFD asset type               |   Trades |
|:-----------------------------|---------:|
| Municipal Security           |      693 |
| Stock Option                 |      326 |
| Corporate Bond               |      162 |
| Commodities/Futures Contract |      141 |
| Non-Public Stock             |       31 |
| Cryptocurrency               |        3 |

OTHER_INSTRUMENT / NON_US_LISTING detail (Yahoo type or exchange):

| reason_code      | reason_detail   |   Trades |
|:-----------------|:----------------|---------:|
| OTHER_INSTRUMENT | ECNQUOTE        |        1 |

Rows excluded from the headline sample but kept in trades_clean.csv for pre-registered variants: OUTSIDE_WINDOW 4,844, OWNER 1,052 (OUTSIDE_WINDOW rows there fall inside the 3- or 10-year window; OWNER rows are the V6 family trades).

### 2. Amendments

155 electronic amendments. Each is linked to the earlier filing(s) it amends (same senator, filed earlier, same report title date and/or overlapping transactions) and classified (rules in `src/clean/amendments.py`; per-amendment detail in `data/interim/amendments.csv`).

| class            |   All amendments |   Received in default window |
|:-----------------|-----------------:|-----------------------------:|
| FULL_RESTATEMENT |               97 |                           35 |
| ADDITIVE         |                4 |                            1 |
| AMBIGUOUS        |               40 |                            2 |
| UNLINKED         |               14 |                            0 |

- Duplicate rows removed: **2,182** (2,158 restated in an amendment, 24 repeated from an unrelated earlier filing). Several identical lines inside one filing are separate trades and are kept.
- Trades that exist ONLY in an amendment (dated by the amendment, no look-ahead): **438** (in scope: **0**).
- Trades whose fields an amendment corrected (corrected value used, original datetime kept): **179** (in scope: **34**); with a substantive change (owner, date, ticker, type or amount): **170** (in scope: **34**). By field (`data/interim/amendment_corrections.csv`):

| field                |   trades |   in_scope_trades |
|:---------------------|---------:|------------------:|
| amount               |        6 |                 1 |
| asset_name           |       46 |                 8 |
| asset_type           |        8 |                 0 |
| owner                |       38 |                 2 |
| ticker               |       34 |                 9 |
| transaction_date_iso |       28 |                 3 |
| transaction_type     |       79 |                19 |

- UNLINKED amendments (14): no earlier electronic filing found. Reason: 14 original predates the scrape start. Their rows count as first disclosed by the amendment.
- Trades touched by an AMBIGUOUS amendment: 583 (in scope: **18**). Rule applied: keep every version's trades once (a trade missing from the amendment is NOT deleted). Flag: `amendment_ambiguous`.

**As first published (J3, headline) vs as revised (V14).** A trade corrected by an amendment has two or more records: the original, effective at the first disclosure, and each corrected version, effective at its amendment's datetime (only changes of owner, date, asset, asset type, type or amount make a new record; a reworded asset name does not). Each record passes the filters on its own values and date. `data/processed/trade_records.csv` lists every record for the engine.

- Trades in trades_clean.csv with more than one record: **131**, 267 records; 5 trades have three or more records.
- In scope under both rules: 2,511; only as first published (J3): 2; only as revised (V14): 0. Headline (J3) in-scope trades: **2,513**; as revised: **2,511**.

Corrected trades by which of their records is in scope:

| orig              |   correction in scope |   correction out |
|:------------------|----------------------:|-----------------:|
| original in scope |                    27 |                2 |
| original out      |                     1 |              101 |

AMBIGUOUS amendments (for Harry):

| senator              | date_received   | title_date   | in_window   |   n_rows |   n_amended_report_trades |   n_repeated_exact |   n_repeated_corrected |   n_new |   n_amended_report_not_repeated | ptr_id                               |
|:---------------------|:----------------|:-------------|:------------|---------:|--------------------------:|-------------------:|-----------------------:|--------:|--------------------------------:|:-------------------------------------|
| Susan M. Collins     | 2016-05-03      | 2016-03-04   | False       |        5 |                         5 |                  1 |                      1 |       3 |                               3 | 58a3b1ce-d1c2-4ad6-9458-be9a7fbe6c6d |
| Bill Cassidy         | 2016-10-07      | 2016-01-12   | False       |        3 |                         3 |                  0 |                      2 |       1 |                               1 | 19885715-1a99-459e-bfce-8f5f57ca5e94 |
| Thomas R. Carper     | 2017-03-14      | 2016-12-01   | False       |       21 |                        22 |                 21 |                      0 |       0 |                               1 | 9f6408dd-ef9e-4be8-b763-73fa074c4a0a |
| Susan M. Collins     | 2017-05-10      | 2016-07-08   | False       |        3 |                         5 |                  3 |                      0 |       0 |                               2 | 8ce46f93-dceb-4c05-9cf3-c463ebce7867 |
| Patrick J. Toomey    | 2017-11-30      | 2016-06-16   | False       |        1 |                         3 |                  1 |                      0 |       0 |                               2 | 3073357f-338e-4f4f-b3eb-5c0feabcfa74 |
| David Perdue         | 2017-12-06      | 2017-10-02   | False       |       38 |                        39 |                 38 |                      0 |       0 |                               1 | e0d89ca5-da6d-49f5-b191-07000462306e |
| Patrick J. Toomey    | 2017-12-12      | 2016-01-12   | False       |        2 |                         4 |                  2 |                      0 |       0 |                               2 | fba0b99c-4ab5-4493-aaaa-69268002dca6 |
| Patrick J. Toomey    | 2017-12-19      | 2016-01-12   | False       |        1 |                         4 |                  1 |                      0 |       0 |                               3 | 1179b764-b4af-4732-9948-81a32fbf2a54 |
| Patrick J. Toomey    | 2017-12-21      | 2016-02-11   | False       |        6 |                         7 |                  3 |                      1 |       2 |                               3 | 72854f36-aae4-445b-b63a-4fba86861178 |
| Pat Roberts          | 2018-06-28      | 2017-09-29   | False       |       15 |                        16 |                 15 |                      0 |       0 |                               1 | a329be05-5227-49ed-a7db-605f7939adfb |
| Pat Roberts          | 2018-06-28      | 2017-12-01   | False       |       12 |                        27 |                 12 |                      0 |       0 |                              15 | 5ba30cf2-0019-4c66-9318-23c1283367f3 |
| Tammy Duckworth      | 2018-08-07      | 2018-01-05   | False       |        1 |                         1 |                  0 |                      0 |       1 |                               1 | 9c8e433f-aa03-4595-b25c-3d3305a4f40f |
| Patrick J. Toomey    | 2018-08-13      | 2017-02-09   | False       |        4 |                         5 |                  2 |                      2 |       0 |                               1 | bd44b543-c8e5-4d3b-9638-9a8e0c9c35e1 |
| Patrick J. Toomey    | 2018-08-13      | 2017-03-03   | False       |        4 |                         5 |                  3 |                      1 |       0 |                               1 | c88f4a1d-16de-4362-955d-ab5402b6653e |
| Patrick J. Toomey    | 2018-08-13      | 2017-09-06   | False       |        1 |                         2 |                  0 |                      1 |       0 |                               1 | 9ff9c3ee-4a28-46e5-a818-f02bbb6ebe47 |
| Patrick J. Toomey    | 2018-08-13      | 2018-01-10   | False       |        5 |                         5 |                  0 |                      3 |       2 |                               2 | b133682c-13d9-4484-b7f5-847c1ee7f768 |
| James M. Inhofe      | 2018-12-12      | 2018-12-12   | False       |        2 |                         3 |                  2 |                      0 |       0 |                               1 | ddf06dcd-abf8-4537-a9c6-96e1fc3f2408 |
| Thomas R. Carper     | 2019-05-15      | 2019-01-03   | False       |        5 |                         5 |                  3 |                      0 |       2 |                               2 | acf289a7-36c4-40fb-a491-8f31e24cdb32 |
| Thom Tillis          | 2019-06-15      | 2019-02-27   | False       |        1 |                         2 |                  1 |                      0 |       0 |                               1 | 2c7b33c4-c85b-44a8-b8f7-cfe2f15961f5 |
| Thom Tillis          | 2019-07-30      | 2019-02-27   | False       |        1 |                         2 |                  0 |                      1 |       0 |                               1 | eaa9e663-e475-41a5-ac0d-3e107ed67481 |
| Patrick J. Toomey    | 2019-08-12      | 2018-08-03   | False       |        1 |                         3 |                  1 |                      0 |       0 |                               2 | 6f737b9c-6983-43ae-854d-8e03a702c3b7 |
| Patrick J. Toomey    | 2019-08-12      | 2018-08-03   | False       |        1 |                         3 |                  0 |                      1 |       0 |                               2 | f3401d4b-32f3-4ae3-8fad-d76d5154f170 |
| Patrick J. Toomey    | 2019-08-12      | 2018-02-07   | False       |        6 |                         6 |                  3 |                      1 |       2 |                               4 | 482ea72a-ca70-4fd9-922a-68cd723b0ee7 |
| Patrick J. Toomey    | 2019-08-12      | 2018-03-07   | False       |        2 |                         2 |                  1 |                      0 |       1 |                               1 | fbe05b6b-08c1-4c10-8115-2e453d6f8a06 |
| Patrick J. Toomey    | 2019-08-12      | 2018-04-10   | False       |        2 |                         2 |                  1 |                      0 |       1 |                               1 | adfa0396-aa71-4fe6-8033-600e6e70e669 |
| Patrick J. Toomey    | 2019-08-12      | 2018-06-07   | False       |        3 |                         3 |                  1 |                      0 |       2 |                               2 | a2e8208b-16b3-4e97-ad54-fa8b2e6e443a |
| Patrick J. Toomey    | 2019-08-12      | 2018-10-05   | False       |        1 |                         3 |                  1 |                      0 |       0 |                               2 | d70bb093-22e4-48a6-a682-2aa1f569d32c |
| Patrick J. Toomey    | 2019-08-12      | 2018-09-07   | False       |        3 |                         3 |                  0 |                      2 |       1 |                               1 | 42013227-54d2-4641-ba01-d21a7d77cee7 |
| Patrick J. Toomey    | 2019-11-15      | 2019-08-13   | False       |        2 |                         3 |                  2 |                      0 |       0 |                               1 | 3dd9dbd6-91d8-4e1e-ad52-9193a3ae0d30 |
| Kelly Loeffler       | 2020-05-01      | 2020-02-07   | False       |       20 |                        22 |                 12 |                      8 |       0 |                               2 | 07b4e543-0978-4d51-87d4-bc4bbe63a1fc |
| Kelly Loeffler       | 2020-05-01      | 2020-03-12   | False       |       25 |                        25 |                  4 |                     16 |       5 |                               5 | 8d87d0d9-8094-4891-a29c-c0e0435acb1a |
| Kelly Loeffler       | 2020-05-01      | 2020-04-01   | False       |       42 |                        42 |                 33 |                      8 |       1 |                               1 | b56659bd-564b-46ee-9c6f-4520348904fd |
| Thomas R. Carper     | 2020-05-25      | 2019-07-03   | False       |        6 |                         7 |                  6 |                      0 |       0 |                               1 | 389ee4d6-3c3f-4383-9311-315a74454c90 |
| Jerry Moran          | 2020-08-05      | 2019-10-21   | False       |       40 |                        40 |                 36 |                      0 |       4 |                               4 | c5faa8f8-b17f-478f-9457-794d602266c3 |
| Patrick J. Toomey    | 2020-08-11      | 2019-02-21   | False       |        1 |                         2 |                  1 |                      0 |       0 |                               1 | acdea934-650d-4726-8f8a-af34f2e36706 |
| David Perdue         | 2021-05-02      | 2020-05-08   | False       |      189 |                       189 |                186 |                      1 |       2 |                               2 | b907f852-1e91-473b-ab7b-3b33cf57b58f |
| Thomas R. Carper     | 2021-05-17      | 2020-11-02   | False       |        3 |                         3 |                  1 |                      0 |       2 |                               2 | 14af60f9-7849-45a0-8f42-c7742edfe403 |
| Patrick J. Toomey    | 2021-08-05      | 2021-01-09   | False       |        3 |                         4 |                  3 |                      0 |       0 |                               1 | 355e54ff-08df-4323-b019-5c88cf24aa6f |
| Shelley Moore Capito | 2022-01-21      | 2022-01-15   | True        |        4 |                         5 |                  4 |                      0 |       0 |                               1 | cbca251b-4a4d-40cb-95c9-7ac3fc6b8d7c |
| Dan Sullivan         | 2023-07-26      | 2022-12-21   | True        |       17 |                        41 |                 17 |                      0 |       0 |                              24 | 016757b7-4990-4541-a2e6-3058ea8b0bfe |

### 3. Amount strings

Every distinct amount string in the raw rows and how it was parsed (open top band = lower bound, D10):

| amount                   |   rows | amount_lower   | amount_upper   | amount_mid   | amount_rule                        |
|:-------------------------|-------:|:---------------|:---------------|:-------------|:-----------------------------------|
| $1,001 - $15,000         |   9527 | 1,001          | 15,000         | 8,000.5      | range: midpoint of lower and upper |
| $15,001 - $50,000        |   2712 | 15,001         | 50,000         | 32,500.5     | range: midpoint of lower and upper |
| $50,001 - $100,000       |    911 | 50,001         | 100,000        | 75,000.5     | range: midpoint of lower and upper |
| $100,001 - $250,000      |    751 | 100,001        | 250,000        | 175,000.5    | range: midpoint of lower and upper |
| $250,001 - $500,000      |    337 | 250,001        | 500,000        | 375,000.5    | range: midpoint of lower and upper |
| $500,001 - $1,000,000    |    257 | 500,001        | 1,000,000      | 750,000.5    | range: midpoint of lower and upper |
| $1,000,001 - $5,000,000  |     50 | 1,000,001      | 5,000,000      | 3,000,000.5  | range: midpoint of lower and upper |
| $5,000,001 - $25,000,000 |     13 | 5,000,001      | 25,000,000     | 15,000,000.5 | range: midpoint of lower and upper |

### 4. Tickers

- Unique tickers checked with Yahoo (3/5/10-year windows, any owner): **1,522**; kept 1,464; with at least one in-scope trade 982. Status by ticker: kept 1464, excluded: mutual fund 51, excluded: non-US listing 6, excluded: other instrument type 1.
- Rows with a raw ticker changed by normalisation (case, spaces, share class BRK.B -> BRK-B): 23.
- Missing-ticker asset names recovered: **490** names, 544 trades (381 Self/Joint in the default window). Not recovered: **304** names, 544 trades (39 Self/Joint in window); these are NO_TICKER exclusions. Full list: `data/interim/ticker_recovery.csv`.

Hand-written overrides (J5, `config/asset_name_overrides.yaml`; applied only when Yahoo's, or failing that SEC's, company name for the ticker confirms it):

| contains                    | ticker   | confirmed_by   | note                                                                                         | matched_asset_names                                                   |
|:----------------------------|:---------|:---------------|:---------------------------------------------------------------------------------------------|:----------------------------------------------------------------------|
| glaxo wellcome              | GSK      | yahoo          | Yahoo name for GSK: GSK plc                                                                  | Glaxo Wellcome plc ADR (GSK)                                          |
| rolls-royce                 | RYCEY    | yahoo          | Yahoo name for RYCEY: Rolls-Royce Holdings plc                                               | ROLLS-ROYCE HOLDINGS PLC SPONSORED ADR | ROLLS-ROYCE HOLDINGS PLC ADR |
| rolls royce                 | RYCEY    | yahoo          | Yahoo name for RYCEY: Rolls-Royce Holdings plc                                               | Rolls Royce Holdings plc Sponsored ADR (RYCEY)                        |
| ishares tr russell 1000 etf | IWB      | yahoo          | Yahoo name for IWB: iShares Russell 1000 ETF                                                 | Ishares TR Russell 1000 ETF                                           |
| = starbuck                  | SBUX     | yahoo          | Yahoo name for SBUX: Starbucks Corporation                                                   | starbuck                                                              |
| (wizey)                     | WIZEY    |                | not confirmed: expected 'Wise', Yahoo name for WIZEY: (Yahoo does not know the symbol)       | Wise plc Sponsored ADR (WIZEY)                                        |
| (murgy)                     | MURGY    | yahoo          | Yahoo name for MURGY: Münchener Rückversicherungs-Gesellschaft Aktiengesellschaft in München | Munich Re Group ADR (MURGY)                                           |
| (holx)                      | HOLX     |                | not confirmed: expected 'Hologic', Yahoo name for HOLX: (Yahoo does not know the symbol)     | Hologic, Inc. (HOLX)                                                  |
| (bk)                        | BK       | yahoo          | Yahoo name for BNY: The Bank of New York Mellon Corporation                                  | Bank of New York Mellon Corp (BK)                                     |
| (pstg)                      | PSTG     | yahoo          | Yahoo name for P: Everpure, Inc.                                                             | Everpure, Inc. Class A (PSTG)                                         |
| (kyocy)                     | KYOCY    |                | not confirmed: expected 'Kyocera', Yahoo name for KYOCY: (Yahoo does not know the symbol)    | Kyocera Corporation ADR Japan (KYOCY)                                 |

Recovered:

| asset_name                                                                       | candidate   | method   |   n_trades |   n_trades_self_joint_in_window | note                                                                                                                                                                                                            |
|:---------------------------------------------------------------------------------|:------------|:---------|-----------:|--------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| INTC-Intel Corporation (NASDAQ)                                                  | INTC        | embedded |          1 |                               0 | embedded ticker INTC; name words shared with Intel Corporation/Intel Corporation/INTEL CORP: intel                                                                                                              |
| AAPL-Apple Inc. (NASDAQ)                                                         | AAPL        | embedded |          1 |                               0 | embedded ticker AAPL; name words shared with Apple Inc./Apple Inc./Apple Inc.: apple                                                                                                                            |
| PFE-Pfizer Inc.                                                                  | PFE         | embedded |          2 |                               0 | embedded ticker PFE; name words shared with Pfizer Inc./Pfizer, Inc./PFIZER INC: pfizer                                                                                                                         |
| GS-The Goldman Sachs Group, Inc.                                                 | GS          | embedded |          1 |                               0 | embedded ticker GS; name words shared with The Goldman Sachs Group, Inc./Goldman Sachs Group, Inc. (The)/GOLDMAN SACHS GROUP INC: goldman, sachs                                                                |
| OKE-ONEOK Inc.                                                                   | OKE         | embedded |          1 |                               0 | embedded ticker OKE; name words shared with ONEOK, Inc./ONEOK, Inc./ONEOK INC /NEW/: oneok                                                                                                                      |
| STT-State Street Corporation                                                     | STT         | embedded |          1 |                               0 | embedded ticker STT; name words shared with State Street Corporation/State Street Corporation/STATE STREET CORP: state, street                                                                                  |
| Philip Morris Intl                                                               | PM          | sec_name |          1 |                               0 | SEC exact name match: Philip Morris International Inc. (CIK 1413329)                                                                                                                                            |
| HD-The Home Depot, Inc.                                                          | HD          | embedded |          1 |                               0 | embedded ticker HD; name words shared with The Home Depot, Inc./Home Depot, Inc. (The)/HOME DEPOT, INC.: depot, home                                                                                            |
| Lincoln National Corporation                                                     | LNC         | sec_name |          1 |                               0 | SEC exact name match: LINCOLN NATIONAL CORP (CIK 59558)                                                                                                                                                         |
| MetLife Inc                                                                      | MET         | sec_name |          2 |                               0 | SEC exact name match: METLIFE INC (CIK 1099219)                                                                                                                                                                 |
| PFS-Provident Financial Services, Inc.                                           | PFS         | embedded |          1 |                               0 | embedded ticker PFS; name words shared with Provident Financial Services, Inc./Provident Financial Services, I/PROVIDENT FINANCIAL SERVICES INC: financial, provident, services                                 |
| PRGO-Perrigo Company plc                                                         | PRGO        | embedded |          1 |                               0 | embedded ticker PRGO; name words shared with Perrigo Company plc/Perrigo Company plc/PERRIGO Co plc: perrigo                                                                                                    |
| Pfizer Inc                                                                       | PFE         | sec_name |          3 |                               0 | SEC exact name match: PFIZER INC (CIK 78003)                                                                                                                                                                    |
| TMO - Thermo Fisher Scientific Inc.                                              | TMO         | embedded |          1 |                               0 | embedded ticker TMO; name words shared with Thermo Fisher Scientific Inc./Thermo Fisher Scientific Inc/THERMO FISHER SCIENTIFIC INC.: fisher, scientific, thermo                                                |
| IR-Ingersoll-Rand Plc                                                            | IR          | embedded |          2 |                               0 | embedded ticker IR; name words shared with Ingersoll Rand Inc./Ingersoll Rand Inc./Ingersoll Rand Inc.: ingersoll, rand                                                                                         |
| NFLX-Netflix, Inc.                                                               | NFLX        | embedded |          1 |                               0 | embedded ticker NFLX; name words shared with Netflix, Inc./Netflix, Inc./NETFLIX INC: netflix                                                                                                                   |
| KBA - KraneShares Bosera MSCI China A ETF                                        | KBA         | embedded |          1 |                               0 | embedded ticker KBA; name words shared with KraneShares Bosera MSCI China A 50 Connect Index ETF/KraneShares Bosera MSCI China A: bosera, china, kraneshares, msci                                              |
| AAPL-Apple Inc.                                                                  | AAPL        | embedded |          4 |                               0 | embedded ticker AAPL; name words shared with Apple Inc./Apple Inc./Apple Inc.: apple                                                                                                                            |
| DIS-The Walt Disney Company                                                      | DIS         | embedded |          1 |                               0 | embedded ticker DIS; name words shared with The Walt Disney Company/Walt Disney Company (The)/Walt Disney Co: disney, walt                                                                                      |
| JPM-JPMorgan Chase & Co.                                                         | JPM         | embedded |          2 |                               0 | embedded ticker JPM; name words shared with JPMorgan Chase & Co./JP Morgan Chase & Co./JPMORGAN CHASE & CO: chase, jpmorgan, morgan                                                                             |
| C-Citigroup Inc.                                                                 | C           | embedded |          1 |                               0 | embedded ticker C; name words shared with Citigroup Inc./Citigroup, Inc./CITIGROUP INC: citigroup                                                                                                               |
| COP-ConocoPhillips                                                               | COP         | embedded |          1 |                               0 | embedded ticker COP; name words shared with ConocoPhillips/ConocoPhillips/CONOCOPHILLIPS: conocophillips                                                                                                        |
| NKE-NIKE, Inc.                                                                   | NKE         | embedded |          1 |                               0 | embedded ticker NKE; name words shared with NIKE, Inc./Nike, Inc./NIKE, Inc.: nike                                                                                                                              |
| BP-BP p.l.c.                                                                     | BP          | embedded |          1 |                               0 | embedded ticker BP; name words shared with BP p.l.c./BP p.l.c./BP PLC: bp                                                                                                                                       |
| PG-The Procter & Gamble Company                                                  | PG          | embedded |          3 |                               0 | embedded ticker PG; name words shared with The Procter & Gamble Company/Procter & Gamble Company (The)/PROCTER & GAMBLE Co: gamble, procter                                                                     |
| AFL-Aflac Incorporated                                                           | AFL         | embedded |          1 |                               0 | embedded ticker AFL; name words shared with Aflac Incorporated/AFLAC Incorporated/AFLAC INC: aflac                                                                                                              |
| SO-The Southern Company                                                          | SO          | embedded |          1 |                               0 | embedded ticker SO; name words shared with The Southern Company/Southern Company (The)/SOUTHERN CO: southern                                                                                                    |
| MRK-Merck & Co., Inc.                                                            | MRK         | embedded |          1 |                               0 | embedded ticker MRK; name words shared with Merck & Co., Inc./Merck & Company, Inc./Merck & Co., Inc.: merck                                                                                                    |
| VNQ-Vanguard REIT ETF                                                            | VNQ         | embedded |          1 |                               0 | embedded ticker VNQ; name words shared with Vanguard Real Estate Index Fund ETF Shares/Vanguard Real Estate ETF: vanguard                                                                                       |
| SBUX-Starbucks Corporation                                                       | SBUX        | embedded |          2 |                               0 | embedded ticker SBUX; name words shared with Starbucks Corporation/Starbucks Corporation/STARBUCKS CORP: starbucks                                                                                              |
| BA-The Boeing Company                                                            | BA          | embedded |          1 |                               0 | embedded ticker BA; name words shared with The Boeing Company/Boeing Company (The)/BOEING CO: boeing                                                                                                            |
| Visa Inc                                                                         | V           | sec_name |          1 |                               0 | SEC exact name match: VISA INC. (CIK 1403161)                                                                                                                                                                   |
| Nvidia Corp                                                                      | NVDA        | sec_name |          1 |                               0 | SEC exact name match: NVIDIA CORP (CIK 1045810)                                                                                                                                                                 |
| Honeywell Intl Inc                                                               | HON         | sec_name |          1 |                               0 | SEC exact name match: HONEYWELL INTERNATIONAL INC (CIK 773840)                                                                                                                                                  |
| Packaging Corp of America                                                        | PKG         | sec_name |          1 |                               0 | SEC exact name match: PACKAGING CORP OF AMERICA (CIK 75677)                                                                                                                                                     |
| Altria Corp                                                                      | MO          | sec_name |          1 |                               0 | SEC exact name match: ALTRIA GROUP, INC. (CIK 764180)                                                                                                                                                           |
| Axis Capital Holdings Ltd                                                        | AXS         | sec_name |          1 |                               0 | SEC exact name match: AXIS CAPITAL HOLDINGS LTD (CIK 1214816)                                                                                                                                                   |
| Medical Properties Trust Inc                                                     | MPT         | sec_name |          1 |                               0 | SEC exact name match: MEDICAL PROPERTIES TRUST INC (CIK 1287865)                                                                                                                                                |
| ETN - Eaton Corporation plc                                                      | ETN         | embedded |          1 |                               0 | embedded ticker ETN; name words shared with Eaton Corporation plc/Eaton Corporation, PLC/Eaton Corp plc: eaton                                                                                                  |
| Zoetis Corp                                                                      | ZTS         | sec_name |          1 |                               0 | SEC exact name match: Zoetis Inc. (CIK 1555280)                                                                                                                                                                 |
| PNR - Pentair plc                                                                | PNR         | embedded |          1 |                               0 | embedded ticker PNR; name words shared with Pentair plc/Pentair plc./PENTAIR plc: pentair                                                                                                                       |
| Chubb Corp                                                                       | CB          | sec_name |          1 |                               0 | SEC exact name match: Chubb Ltd (CIK 896159)                                                                                                                                                                    |
| Analog Devices Inc                                                               | ADI         | sec_name |          1 |                               0 | SEC exact name match: ANALOG DEVICES INC (CIK 6281)                                                                                                                                                             |
| Bristol Myers Squibb                                                             | BMY         | sec_name |          1 |                               0 | SEC exact name match: BRISTOL MYERS SQUIBB CO (CIK 14272)                                                                                                                                                       |
| CSCO-Cisco Systems, Inc.                                                         | CSCO        | embedded |          1 |                               0 | embedded ticker CSCO; name words shared with Cisco Systems, Inc./Cisco Systems, Inc./CISCO SYSTEMS, INC.: cisco, systems                                                                                        |
| Walt Disney Corp                                                                 | DIS         | sec_name |          2 |                               0 | SEC exact name match: Walt Disney Co (CIK 1744489)                                                                                                                                                              |
| FMC Corp New                                                                     | FMC         | sec_name |          1 |                               0 | SEC exact name match: FMC CORP (CIK 37785)                                                                                                                                                                      |
| GE-General Electric Company                                                      | GE          | embedded |          1 |                               0 | embedded ticker GE; name words shared with GE Aerospace/GE Aerospace/GENERAL ELECTRIC CO: electric, general                                                                                                     |
| INTC-Intel Corporation                                                           | INTC        | embedded |          1 |                               0 | embedded ticker INTC; name words shared with Intel Corporation/Intel Corporation/INTEL CORP: intel                                                                                                              |
| Johnson and Johnson                                                              | JNJ         | sec_name |          1 |                               0 | SEC exact name match: JOHNSON & JOHNSON (CIK 200406)                                                                                                                                                            |
| MSFT-Microsoft Corporation                                                       | MSFT        | embedded |          1 |                               0 | embedded ticker MSFT; name words shared with Microsoft Corporation/Microsoft Corporation/MICROSOFT CORP: microsoft                                                                                              |
| NVDA-NVIDIA Corporation                                                          | NVDA        | embedded |          1 |                               0 | embedded ticker NVDA; name words shared with NVIDIA Corporation/NVIDIA Corporation/NVIDIA CORP: nvidia                                                                                                          |
| Compass Minerals                                                                 | CMP         | sec_name |          1 |                               0 | SEC exact name match: COMPASS MINERALS INTERNATIONAL INC (CIK 1227654)                                                                                                                                          |
| Hexcel Corp New                                                                  | HXL         | sec_name |          1 |                               0 | SEC exact name match: HEXCEL CORP /DE/ (CIK 717605)                                                                                                                                                             |
| SAFRY - Safran SA                                                                | SAFRY       | embedded |          1 |                               0 | embedded ticker SAFRY; name words shared with Safran SA/Safran SA: safran                                                                                                                                       |
| EADSY - Airbus SE                                                                | EADSY       | embedded |          1 |                               0 | embedded ticker EADSY; name words shared with Airbus SE/Airbus SE: airbus                                                                                                                                       |
| AAGIY - AIA Group Limited                                                        | AAGIY       | embedded |          1 |                               0 | embedded ticker AAGIY; name words shared with AIA Group Limited/AIA Group, Ltd.: aia                                                                                                                            |
| HLT-Hilton Worldwide Holdings Inc.                                               | HLT         | embedded |          1 |                               0 | embedded ticker HLT; name words shared with Hilton Worldwide Holdings Inc./Hilton Worldwide Holdings Inc./Hilton Worldwide Holdings Inc.: hilton, worldwide                                                     |
| WEC-WEC Energy Group, Inc.                                                       | WEC         | embedded |          1 |                               0 | embedded ticker WEC; name words shared with WEC Energy Group, Inc./WEC Energy Group, Inc./WEC ENERGY GROUP, INC.: energy, wec                                                                                   |
| AMZN-Amazon.com, Inc.                                                            | AMZN        | embedded |          1 |                               0 | embedded ticker AMZN; name words shared with Amazon.com, Inc./Amazon.com, Inc./AMAZON COM INC: amazon                                                                                                           |
| ETN-Eaton Corporation plc                                                        | ETN         | embedded |          1 |                               0 | embedded ticker ETN; name words shared with Eaton Corporation plc/Eaton Corporation, PLC/Eaton Corp plc: eaton                                                                                                  |
| XOM-Exxon Mobil Corporation                                                      | XOM         | embedded |          1 |                               0 | embedded ticker XOM; name words shared with ExxonMobil Holdings Corporation/ExxonMobil Holdings Corporation/ExxonMobil Holdings Corp: exxon, exxonmobil, mobil                                                  |
| PFS                                                                              | PFS         | embedded |          1 |                               0 | asset name is the bare ticker PFS; Yahoo: Provident Financial Services, Inc.                                                                                                                                    |
| Seagate Technology                                                               | STX         | sec_name |          2 |                               0 | SEC exact name match: Seagate Technology Holdings plc (CIK 1137789)                                                                                                                                             |
| Iron Mountain                                                                    | IRM         | sec_name |          3 |                               0 | SEC exact name match: IRON MOUNTAIN INC (CIK 1020569)                                                                                                                                                           |
| Ares Capital                                                                     | ARCC        | sec_name |          1 |                               0 | SEC exact name match: ARES CAPITAL CORP (CIK 1287750)                                                                                                                                                           |
| Newell Brands                                                                    | NWL         | sec_name |          1 |                               0 | SEC exact name match: NEWELL BRANDS INC. (CIK 814453)                                                                                                                                                           |
| Axis Capital Holdings                                                            | AXS         | sec_name |          1 |                               0 | SEC exact name match: AXIS CAPITAL HOLDINGS LTD (CIK 1214816)                                                                                                                                                   |
| FMC Corp                                                                         | FMC         | sec_name |          1 |                               0 | SEC exact name match: FMC CORP (CIK 37785)                                                                                                                                                                      |
| General Electric                                                                 | GE          | sec_name |          2 |                               0 | SEC exact name match: GENERAL ELECTRIC CO (CIK 40545)                                                                                                                                                           |
| Intel Corp                                                                       | INTC        | sec_name |          2 |                               0 | SEC exact name match: INTEL CORP (CIK 50863)                                                                                                                                                                    |
| Robert Half Intl                                                                 | RHI         | sec_name |          1 |                               0 | SEC exact name match: ROBERT HALF INC. (CIK 315213)                                                                                                                                                             |
| Nvent Electric                                                                   | NVT         | sec_name |          1 |                               0 | SEC exact name match: nVent Electric plc (CIK 1720635)                                                                                                                                                          |
| The Scotts Miracle-Gro Group                                                     | SMG         | sec_name |          1 |                               0 | SEC exact name match: SCOTTS MIRACLE-GRO CO (CIK 825542)                                                                                                                                                        |
| CVS Health                                                                       | CVS         | sec_name |          1 |                               0 | SEC exact name match: CVS HEALTH Corp (CIK 64803)                                                                                                                                                               |
| Amazon.com, Inc.                                                                 | AMZN        | sec_name |          1 |                               0 | SEC exact name match: AMAZON COM INC (CIK 1018724)                                                                                                                                                              |
| GILD                                                                             | GILD        | embedded |          2 |                               0 | asset name is the bare ticker GILD; Yahoo: Gilead Sciences, Inc.                                                                                                                                                |
| Knight-Swift Transportation Holdings                                             | KNX         | sec_name |          1 |                               0 | SEC exact name match: Knight-Swift Transportation Holdings Inc. (CIK 1492691)                                                                                                                                   |
| Danaher Corp                                                                     | DHR         | sec_name |          1 |                               0 | SEC exact name match: DANAHER CORP /DE/ (CIK 313616)                                                                                                                                                            |
| Sprott Physical Gold and Silver                                                  | CEF         | sec_name |          1 |                               0 | SEC exact name match: Sprott Physical Gold & Silver Trust (CIK 1726122)                                                                                                                                         |
| Abbvie                                                                           | ABBV        | sec_name |          2 |                               0 | SEC exact name match: AbbVie Inc. (CIK 1551152)                                                                                                                                                                 |
| Analog Devices                                                                   | ADI         | sec_name |          2 |                               0 | SEC exact name match: ANALOG DEVICES INC (CIK 6281)                                                                                                                                                             |
| Hexcel Corp                                                                      | HXL         | sec_name |          1 |                               0 | SEC exact name match: HEXCEL CORP /DE/ (CIK 717605)                                                                                                                                                             |
| Qualcomm Inc                                                                     | QCOM        | sec_name |          2 |                               1 | SEC exact name match: QUALCOMM INC/DE (CIK 804328)                                                                                                                                                              |
| Agilent Technologies                                                             | A           | sec_name |          1 |                               0 | SEC exact name match: AGILENT TECHNOLOGIES, INC. (CIK 1090872)                                                                                                                                                  |
| Lazard Global Total Return & Income                                              | LGI         | sec_name |          1 |                               0 | SEC exact name match: LAZARD GLOBAL TOTAL RETURN & INCOME FUND INC (CIK 1278211)                                                                                                                                |
| Packaging Corp                                                                   | PKG         | sec_name |          1 |                               0 | SEC exact name match: PACKAGING CORP OF AMERICA (CIK 75677)                                                                                                                                                     |
| Fedex Corp                                                                       | FDX         | sec_name |          2 |                               0 | SEC exact name match: FEDEX CORP (CIK 1048911)                                                                                                                                                                  |
| Altria Group                                                                     | MO          | sec_name |          1 |                               0 | SEC exact name match: ALTRIA GROUP, INC. (CIK 764180)                                                                                                                                                           |
| Metlife                                                                          | MET         | sec_name |          1 |                               0 | SEC exact name match: METLIFE INC (CIK 1099219)                                                                                                                                                                 |
| Zoetis Inc Class A                                                               | ZTS         | sec_name |          1 |                               0 | SEC exact name match: Zoetis Inc. (CIK 1555280)                                                                                                                                                                 |
| Pentair PLC                                                                      | PNR         | sec_name |          1 |                               0 | SEC exact name match: PENTAIR plc (CIK 77360)                                                                                                                                                                   |
| Fifth Third Bancorp                                                              | FITB        | sec_name |          1 |                               0 | SEC exact name match: FIFTH THIRD BANCORP (CIK 35527)                                                                                                                                                           |
| Tyson Foods                                                                      | TSN         | sec_name |          1 |                               0 | SEC exact name match: TYSON FOODS, INC. (CIK 100493)                                                                                                                                                            |
| Amazon                                                                           | AMZN        | sec_name |          5 |                               0 | SEC exact name match: AMAZON COM INC (CIK 1018724)                                                                                                                                                              |
| Marathon Petroleum Corp                                                          | MPC         | sec_name |          2 |                               0 | SEC exact name match: Marathon Petroleum Corp (CIK 1510295)                                                                                                                                                     |
| Pfizer                                                                           | PFE         | sec_name |          1 |                               0 | SEC exact name match: PFIZER INC (CIK 78003)                                                                                                                                                                    |
| Apple Inc.                                                                       | AAPL        | sec_name |          2 |                               0 | SEC exact name match: Apple Inc. (CIK 320193)                                                                                                                                                                   |
| General Electric Company                                                         | GE          | sec_name |          1 |                               0 | SEC exact name match: GENERAL ELECTRIC CO (CIK 40545)                                                                                                                                                           |
| Apple Inc                                                                        | AAPL        | sec_name |          1 |                               0 | SEC exact name match: Apple Inc. (CIK 320193)                                                                                                                                                                   |
| Cameco Corp                                                                      | CCJ         | sec_name |          1 |                               0 | SEC exact name match: CAMECO CORP (CIK 1009001)                                                                                                                                                                 |
| Newell Brands Inc                                                                | NWL         | sec_name |          1 |                               0 | SEC exact name match: NEWELL BRANDS INC. (CIK 814453)                                                                                                                                                           |
| Altria Group Inc                                                                 | MO          | sec_name |          1 |                               0 | SEC exact name match: ALTRIA GROUP, INC. (CIK 764180)                                                                                                                                                           |
| Quest Diagnostics                                                                | DGX         | sec_name |          1 |                               0 | SEC exact name match: QUEST DIAGNOSTICS INC (CIK 1022079)                                                                                                                                                       |
| Hormel Foods                                                                     | HRL         | sec_name |          1 |                               0 | SEC exact name match: HORMEL FOODS CORP /DE/ (CIK 48465)                                                                                                                                                        |
| GOOG - Alphabet Inc. C                                                           | GOOG        | embedded |          1 |                               0 | embedded ticker GOOG; name words shared with Alphabet Inc./Alphabet Inc./Alphabet Inc.: alphabet                                                                                                                |
| GOOGL - Alphabet Inc. A                                                          | GOOGL       | embedded |          1 |                               0 | embedded ticker GOOGL; name words shared with Alphabet Inc./Alphabet Inc./Alphabet Inc.: alphabet                                                                                                               |
| The Allstate Corporation                                                         | ALL         | sec_name |          1 |                               0 | SEC exact name match: ALLSTATE CORP (CIK 899051)                                                                                                                                                                |
| Verizon Communications Inc.                                                      | VZ          | sec_name |          1 |                               0 | SEC exact name match: VERIZON COMMUNICATIONS INC (CIK 732712)                                                                                                                                                   |
| PPL                                                                              | PPL         | embedded |          1 |                               0 | asset name is the bare ticker PPL; Yahoo: PPL Corporation                                                                                                                                                       |
| Costco Wholesale Corporation                                                     | COST        | sec_name |          1 |                               0 | SEC exact name match: COSTCO WHOLESALE CORP /NEW (CIK 909832)                                                                                                                                                   |
| The Boeing Company                                                               | BA          | sec_name |          1 |                               0 | SEC exact name match: BOEING CO (CIK 12927)                                                                                                                                                                     |
| Walmart Inc.                                                                     | WMT         | sec_name |          1 |                               0 | SEC exact name match: Walmart Inc. (CIK 104169)                                                                                                                                                                 |
| Spotify Technology S.A.                                                          | SPOT        | sec_name |          1 |                               0 | SEC exact name match: Spotify Technology S.A. (CIK 1639920)                                                                                                                                                     |
| Editas Medicine, Inc.                                                            | EDIT        | sec_name |          1 |                               0 | SEC exact name match: Editas Medicine, Inc. (CIK 1650664)                                                                                                                                                       |
| GSMYX - GOLDMAN SACHS SM MD CAP GROWTH I                                         | GSMYX       | embedded |          2 |                               0 | embedded ticker GSMYX; name words shared with Goldman Sachs Small/Mid Cap Growth Instl/Goldman Sachs Small/Mid Cap Gro: cap, goldman, growth, sachs                                                             |
| Bristol-Myers Squibb Company Common Stock                                        | BMY         | sec_name |          1 |                               0 | SEC exact name match: BRISTOL MYERS SQUIBB CO (CIK 14272)                                                                                                                                                       |
| WFC - Wells Fargo & Company                                                      | WFC         | embedded |          1 |                               0 | embedded ticker WFC; name words shared with Wells Fargo & Company/Wells Fargo & Company/WELLS FARGO & COMPANY/MN: fargo, wells                                                                                  |
| Quest Diagnostics Incorporated Common Stock                                      | DGX         | sec_name |          1 |                               1 | SEC exact name match: QUEST DIAGNOSTICS INC (CIK 1022079)                                                                                                                                                       |
| PM                                                                               | PM          | embedded |          1 |                               0 | asset name is the bare ticker PM; Yahoo: Philip Morris International Inc.                                                                                                                                       |
| VZ                                                                               | VZ          | embedded |          1 |                               1 | asset name is the bare ticker VZ; Yahoo: Verizon Communications Inc.                                                                                                                                            |
| UnitedHealth Group Incorporated Common Stock (DE)                                | UNH         | sec_name |          1 |                               0 | embedded ticker DE but its name (Deere & Company/Deere & Company/DEERE & CO) shares no word with 'UnitedHealth Group Incorporated Common Stock'; then SEC exact name match: UNITEDHEALTH GROUP INC (CIK 731766) |
| FIMKX - Fidelity Advisor Focused Emerging Markets I                              | FIMKX       | embedded |          3 |                               0 | embedded ticker FIMKX; name words shared with Fidelity Advisor Focused Em Mkts I/Fidelity Advisor Emerging Marke: advisor, emerging, fidelity, focused, marke                                                   |
| KH                                                                               | KH          | embedded |          1 |                               0 | asset name is the bare ticker KH; Yahoo:                                                                                                                                                                        |
| PayPal Holdings, Inc. - Common Stock                                             | PYPL        | sec_name |          1 |                               1 | SEC exact name match: PayPal Holdings, Inc. (CIK 1633917)                                                                                                                                                       |
| PMI                                                                              | PMI         | embedded |          1 |                               0 | asset name is the bare ticker PMI; Yahoo: Picard Medical, Inc.                                                                                                                                                  |
| Brown-Forman Corp Class B                                                        | BF-B        | sec_name |          1 |                               1 | SEC exact name match with share class B: BROWN FORMAN CORP (CIK 14693)                                                                                                                                          |
| Verizon Communications Inc. Common Stock                                         | VZ          | sec_name |          1 |                               1 | SEC exact name match: VERIZON COMMUNICATIONS INC (CIK 732712)                                                                                                                                                   |
| SIEGY                                                                            | SIEGY       | embedded |          1 |                               1 | asset name is the bare ticker SIEGY; Yahoo: Siemens Aktiengesellschaft                                                                                                                                          |
| JTKWY - Just Eat Takeaway.com NV - ADR                                           | JTKWY       | embedded |          1 |                               0 | embedded ticker JTKWY; name words shared with Just Eat Takeaway.com N.V./Just Eat Takeaway.com N.V.: eat, just, takeaway                                                                                        |
| AXAHY                                                                            | AXAHY       | embedded |          1 |                               1 | asset name is the bare ticker AXAHY; Yahoo: AXA SA                                                                                                                                                              |
| WFC                                                                              | WFC         | embedded |          1 |                               0 | asset name is the bare ticker WFC; Yahoo: Wells Fargo & Company                                                                                                                                                 |
| chevron                                                                          | CVX         | sec_name |          1 |                               0 | SEC exact name match: CHEVRON CORP (CIK 93410)                                                                                                                                                                  |
| FWONK - Formula One Group                                                        | FWONK       | embedded |          1 |                               0 | embedded ticker FWONK; name words shared with Formula One Group/Liberty Media Corporation - Ser/Liberty Media Corp: formula, one                                                                                |
| ROLLS-ROYCE HOLDINGS PLC SPONSORED ADR                                           | RYCEY       | override |          2 |                               2 | J5 override 'rolls-royce' (yahoo)                                                                                                                                                                               |
| Ishares TR Russell 1000 ETF                                                      | IWB         | override |          1 |                               1 | J5 override 'ishares tr russell 1000 etf' (yahoo)                                                                                                                                                               |
| ROLLS-ROYCE HOLDINGS PLC ADR                                                     | RYCEY       | override |          3 |                               3 | J5 override 'rolls-royce' (yahoo)                                                                                                                                                                               |
| CARR - Carrier Global Corp                                                       | CARR        | embedded |          1 |                               1 | embedded ticker CARR; name words shared with Carrier Global Corporation/Carrier Global Corporation/CARRIER GLOBAL Corp: carrier, global                                                                         |
| Otis Worldwide Corporation Common Stock                                          | OTIS        | sec_name |          1 |                               1 | SEC exact name match: Otis Worldwide Corp (CIK 1781335)                                                                                                                                                         |
| AMAT                                                                             | AMAT        | embedded |          2 |                               2 | asset name is the bare ticker AMAT; Yahoo: Applied Materials, Inc.                                                                                                                                              |
| Meta Platforms Inc                                                               | META        | sec_name |          1 |                               0 | SEC exact name match: Meta Platforms, Inc. (CIK 1326801)                                                                                                                                                        |
| LLY                                                                              | LLY         | embedded |          1 |                               1 | asset name is the bare ticker LLY; Yahoo: Eli Lilly and Company                                                                                                                                                 |
| AMD                                                                              | AMD         | embedded |          1 |                               1 | asset name is the bare ticker AMD; Yahoo: Advanced Micro Devices, Inc.                                                                                                                                          |
| SMCI                                                                             | SMCI        | embedded |          4 |                               4 | asset name is the bare ticker SMCI; Yahoo: Super Micro Computer, Inc.                                                                                                                                           |
| HWM                                                                              | HWM         | embedded |          2 |                               2 | asset name is the bare ticker HWM; Yahoo: Howmet Aerospace Inc.                                                                                                                                                 |
| GENI                                                                             | GENI        | embedded |          1 |                               1 | asset name is the bare ticker GENI; Yahoo: Genius Sports Limited                                                                                                                                                |
| ASML                                                                             | ASML        | embedded |          1 |                               1 | asset name is the bare ticker ASML; Yahoo: ASML Holding N.V.                                                                                                                                                    |
| KPTI                                                                             | KPTI        | embedded |          1 |                               1 | asset name is the bare ticker KPTI; Yahoo: Karyopharm Therapeutics Inc.                                                                                                                                         |
| ADCT                                                                             | ADCT        | embedded |          1 |                               1 | asset name is the bare ticker ADCT; Yahoo: ADC Therapeutics SA                                                                                                                                                  |
| NVDA                                                                             | NVDA        | embedded |          2 |                               2 | asset name is the bare ticker NVDA; Yahoo: NVIDIA Corporation                                                                                                                                                   |
| ET                                                                               | ET          | embedded |          1 |                               1 | asset name is the bare ticker ET; Yahoo: Energy Transfer LP                                                                                                                                                     |
| JPM                                                                              | JPM         | embedded |          1 |                               1 | asset name is the bare ticker JPM; Yahoo: JPMorgan Chase & Co.                                                                                                                                                  |
| ARCC                                                                             | ARCC        | embedded |          1 |                               1 | asset name is the bare ticker ARCC; Yahoo: Ares Capital Corporation                                                                                                                                             |
| SDZNY - Sandoz Group AG                                                          | SDZNY       | embedded |          1 |                               1 | embedded ticker SDZNY; name words shared with Sandoz Group AG/Sandoz Group AG: sandoz                                                                                                                           |
| Broadcom Inc. - Common Stock                                                     | AVGO        | sec_name |          1 |                               1 | SEC exact name match: Broadcom Inc. (CIK 1730168)                                                                                                                                                               |
| RBLX                                                                             | RBLX        | embedded |          1 |                               1 | asset name is the bare ticker RBLX; Yahoo: Roblox Corporation                                                                                                                                                   |
| BRK-B - Berkshire Hathaway Inc Class B                                           | BRK-B       | embedded |          1 |                               1 | embedded ticker BRK-B; name words shared with Berkshire Hathaway Inc./Berkshire Hathaway Inc. New/BERKSHIRE HATHAWAY INC: berkshire, hathaway                                                                   |
| starbuck                                                                         | SBUX        | override |          1 |                               1 | J5 override '= starbuck' (yahoo)                                                                                                                                                                                |
| Citigroup Inc New (C)                                                            | C           | embedded |          1 |                               0 | embedded ticker C; name words shared with Citigroup Inc./Citigroup, Inc./CITIGROUP INC: citigroup                                                                                                               |
| META                                                                             | META        | embedded |          1 |                               1 | asset name is the bare ticker META; Yahoo: Meta Platforms, Inc.                                                                                                                                                 |
| MRSH - Marsh & McLennan Companies, Inc. Common Stock                             | MRSH        | embedded |          1 |                               0 | embedded ticker MRSH; name words shared with Marsh & McLennan Companies, Inc./Marsh/MARSH & MCLENNAN COMPANIES, INC.: companies, marsh, mclennan                                                                |
| SPYM                                                                             | SPYM        | embedded |          1 |                               1 | asset name is the bare ticker SPYM; Yahoo: State Street SPDR Portfolio S&P 500 ETF                                                                                                                              |
| GOOGL - Alphabet Inc. - Class C Capital Stock                                    | GOOGL       | embedded |          1 |                               0 | embedded ticker GOOGL; name words shared with Alphabet Inc./Alphabet Inc./Alphabet Inc.: alphabet                                                                                                               |
| SJM - The J.M. Smucker Company Common Stock                                      | SJM         | embedded |          1 |                               1 | embedded ticker SJM; name words shared with The J. M. Smucker Company/The J.M. Smucker Company/J M SMUCKER Co: smucker                                                                                          |
| PEP - PepsiCo, Inc. - Common Stock                                               | PEP         | embedded |          1 |                               1 | embedded ticker PEP; name words shared with PepsiCo, Inc./Pepsico, Inc./PEPSICO INC: pepsico                                                                                                                    |
| Citigroup New Inc (C)                                                            | C           | embedded |          1 |                               0 | embedded ticker C; name words shared with Citigroup Inc./Citigroup, Inc./CITIGROUP INC: citigroup                                                                                                               |
| SCHP - Schwab U.S. TIPS ETF                                                      | SCHP        | embedded |          1 |                               1 | embedded ticker SCHP; name words shared with Schwab U.S. TIPS ETF/Schwab U.S. TIPs ETF: schwab, tips                                                                                                            |
| CEG - Constellation Energy Corporation - Common Stock When-Issued                | CEG         | embedded |          1 |                               1 | embedded ticker CEG; name words shared with Constellation Energy Corporation/Constellation Energy Corporatio/Constellation Energy Corp: constellation, corporatio, energy                                       |
| ACN - Accenture plc Class A Ordinary Shares (Ireland)                            | ACN         | embedded |          1 |                               1 | embedded ticker ACN; name words shared with Accenture plc/Accenture plc/Accenture plc: accenture                                                                                                                |
| Recruit Holdings Co Ltd Unsponsored ADR (RCRUY)                                  | RCRUY       | embedded |          1 |                               1 | embedded ticker RCRUY; name words shared with Recruit Holdings Co., Ltd./Recruit Holdings Co., Ltd.: recruit                                                                                                    |
| AIA Group Limited (AAGIY)                                                        | AAGIY       | embedded |          1 |                               1 | embedded ticker AAGIY; name words shared with AIA Group Limited/AIA Group, Ltd.: aia                                                                                                                            |
| Hensoldt AG ADR (HAGHY)                                                          | HAGHY       | embedded |          1 |                               1 | embedded ticker HAGHY; name words shared with Hensoldt AG/HENSOLDT AG: hensoldt                                                                                                                                 |
| Tokyo Electron Ltd ADR (TOELY)                                                   | TOELY       | embedded |          1 |                               1 | embedded ticker TOELY; name words shared with Tokyo Electron Ltd/Tokyo Electron Ltd.: electron, tokyo                                                                                                           |
| Pan Pacific International Holdings Corporation ADR (DQJCY)                       | DQJCY       | embedded |          1 |                               1 | embedded ticker DQJCY; name words shared with Pan Pacific International Holdings Corporation/Pan Pac Intl Hldgs Corp.: pacific, pan                                                                             |
| East Japan Railway Co ADR (EJPRY)                                                | EJPRY       | embedded |          1 |                               1 | embedded ticker EJPRY; name words shared with East Japan Railway Company/East Japan Railway Co.: east, railway                                                                                                  |
| Zurich Insurance Group Ltd Sponsored ADR (ZURVY)                                 | ZURVY       | embedded |          2 |                               2 | embedded ticker ZURVY; name words shared with Zurich Insurance Group AG/Zurich Insurance Group Ltd: insurance, zurich                                                                                           |
| Wise plc Sponsored ADR (WIZEY)                                                   | WSE         | sec_name |          2 |                               2 | J5 override '(wizey)' (NOT confirmed); then embedded ticker WIZEY not recognised by Yahoo; then SEC exact name match: Wise Group plc (CIK 2099039)                                                              |
| Unicredit SPA Unsponsored ADR (UNCRY)                                            | UNCRY       | embedded |          2 |                               2 | embedded ticker UNCRY; name words shared with UniCredit S.p.A./UniCredito Spa: unicredit                                                                                                                        |
| Swisscom AG Sponsored ADR (SCMWY)                                                | SCMWY       | embedded |          2 |                               2 | embedded ticker SCMWY; name words shared with Swisscom AG/Swisscom AG/SWISSCOM AG: swisscom                                                                                                                     |
| Schneider Electric SE Unsponsored ADR (SBGSY)                                    | SBGSY       | embedded |          2 |                               2 | embedded ticker SBGSY; name words shared with Schneider Electric S.E./Schneider Electric SE: electric, schneider                                                                                                |
| SAP SE Sponsored ADR (SAP)                                                       | SAP         | embedded |          1 |                               1 | embedded ticker SAP; name words shared with SAP SE/SAP  SE/SAP SE: sap                                                                                                                                          |
| Royal KPN N.V. Sponsored ADR (KKPNY)                                             | KKPNY       | embedded |          2 |                               2 | embedded ticker KKPNY; name words shared with Koninklijke KPN N.V./Royal KPN NV: kpn, royal                                                                                                                     |
| Rolls Royce Holdings plc Sponsored ADR (RYCEY)                                   | RYCEY       | override |          2 |                               2 | J5 override 'rolls royce' (yahoo)                                                                                                                                                                               |
| Henkel AG & Co KGAA Sponsored ADR (HENKY)                                        | HENKY       | embedded |          1 |                               1 | embedded ticker HENKY; name words shared with Henkel AG & Co. KGaA/Henkel AG & Co. KGAA: henkel, kgaa                                                                                                           |
| Heineken NV Sponsored ADR (HEINY)                                                | HEINY       | embedded |          2 |                               2 | embedded ticker HEINY; name words shared with Heineken N.V./Heineken N.V.: heineken                                                                                                                             |
| Glencore plc Unsponsored ADR (GLNCY)                                             | GLNCY       | embedded |          2 |                               2 | embedded ticker GLNCY; name words shared with Glencore plc/Glencore Plc: glencore                                                                                                                               |
| DSV A/S ADR (DSDVY)                                                              | DSDVY       | embedded |          2 |                               2 | embedded ticker DSDVY; name words shared with DSV A/S/DSV A S: dsv                                                                                                                                              |
| Compagnie Financiere Richemont AG ADR (CFRUY)                                    | CFRUY       | embedded |          2 |                               2 | embedded ticker CFRUY; name words shared with Compagnie Financière Richemont SA/Compagnie Financiere Richemont : compagnie, financiere, richemont                                                               |
| Carrefour SA Sponsored ADR (CRRFY)                                               | CRRFY       | embedded |          2 |                               2 | embedded ticker CRRFY; name words shared with Carrefour SA/Carrefour S.A.: carrefour                                                                                                                            |
| BHP Group Limited (BHP)                                                          | BHP         | embedded |          2 |                               2 | embedded ticker BHP; name words shared with BHP Group Limited/BHP Group Limited/BHP Group Ltd: bhp                                                                                                              |
| Air Liquide ADR France (AIQUY)                                                   | AIQUY       | embedded |          1 |                               1 | embedded ticker AIQUY; name words shared with L'Air Liquide S.A./L'Air Liquide SA: liquide                                                                                                                      |
| Yara International ASA Sponsored ADR (YARIY)                                     | YARIY       | embedded |          1 |                               1 | embedded ticker YARIY; name words shared with Yara International ASA/Yara International ASA/YARA INTERNATIONAL ASA: asa, yara                                                                                   |
| Wolters Kluwer NV Sponsored ADR (WTKWY)                                          | WTKWY       | embedded |          1 |                               1 | embedded ticker WTKWY; name words shared with Wolters Kluwer N.V./Wolters Kluwer N.V./WOLTERS KLUWER N V /FI: kluwer, wolters                                                                                   |
| Wilmar International Ltd AADR (WLMIY)                                            | WLMIY       | embedded |          1 |                               1 | embedded ticker WLMIY; name words shared with Wilmar International Limited/Wilmar International, Ltd.: wilmar                                                                                                   |
| Wesfarmers Ltd Unsponsored ADR (WFAFY)                                           | WFAFY       | embedded |          1 |                               1 | embedded ticker WFAFY; name words shared with Wesfarmers Limited/Wesfarmers Ltd.: wesfarmers                                                                                                                    |
| Vonovia SE ADR (VONOY)                                                           | VONOY       | embedded |          1 |                               1 | embedded ticker VONOY; name words shared with Vonovia SE/VONOVIA SE: vonovia                                                                                                                                    |
| Volvo AB-A Unsponsored ADR (VLVLY)                                               | VLVLY       | embedded |          1 |                               1 | embedded ticker VLVLY; name words shared with AB Volvo (publ)/Volvo AB: ab, volvo                                                                                                                               |
| Volkswagen AG Unsponsored ADR (VWAPY)                                            | VWAPY       | embedded |          1 |                               1 | embedded ticker VWAPY; name words shared with Volkswagen AG/Volkswagen AG: volkswagen                                                                                                                           |
| Vodafone Group Plc (VOD)                                                         | VOD         | embedded |          1 |                               1 | embedded ticker VOD; name words shared with Vodafone Group Public Limited Company/Vodafone Group Plc/VODAFONE GROUP PUBLIC LTD CO: vodafone                                                                     |
| Vinci S.A. ADR (VCISY)                                                           | VCISY       | embedded |          1 |                               1 | embedded ticker VCISY; name words shared with Vinci SA/Vinci SA: vinci                                                                                                                                          |
| Vestas Wind Systems A/S ADR (VWDRY)                                              | VWDRY       | embedded |          1 |                               1 | embedded ticker VWDRY; name words shared with Vestas Wind Systems A/S/Vestas Wind Systems A/S: systems, vestas, wind                                                                                            |
| VAT Group AG Unsponsored ADR (VACNY)                                             | VACNY       | embedded |          1 |                               1 | embedded ticker VACNY; name words shared with VAT Group AG/VAT Group AG: vat                                                                                                                                    |
| UPM Kymmene Corporation ADR (UPMMY)                                              | UPMMY       | embedded |          1 |                               1 | embedded ticker UPMMY; name words shared with UPM-Kymmene Oyj/UPM-Kymmene Corp.: kymmene, upm                                                                                                                   |
| United Overseas Bank Ltd Sponsored ADR Singapore (UOVEY)                         | UOVEY       | embedded |          1 |                               1 | embedded ticker UOVEY; name words shared with United Overseas Bank Limited/United Overseas Bank Ltd.: bank, overseas, united                                                                                    |
| Universal Music Group ADR (UNVGY)                                                | UNVGY       | embedded |          1 |                               1 | embedded ticker UNVGY; name words shared with Universal Music Group N.V./UNIVERSAL MUSIC GROUP/Universal Music Group N.V./ADR: music, universal                                                                 |
| Unilever PLC (UL)                                                                | UL          | embedded |          1 |                               1 | embedded ticker UL; name words shared with Unilever PLC/Unilever PLC/UNILEVER PLC: unilever                                                                                                                     |
| Unicharm Corporation Sponsored ADR (UNICY)                                       | UNICY       | embedded |          1 |                               1 | embedded ticker UNICY; name words shared with Unicharm Corporation/Unicharm Corp.: unicharm                                                                                                                     |
| UCB SA ADR (UCBJY)                                                               | UCBJY       | embedded |          1 |                               1 | embedded ticker UCBJY; name words shared with UCB SA/UCB S.A.: ucb                                                                                                                                              |
| Tokio Marine Holdings Inc Sponsored (TKOMY)                                      | TKOMY       | embedded |          1 |                               1 | embedded ticker TKOMY; name words shared with Tokio Marine Holdings, Inc./Tokio Marine Holdings, Inc./TOKIO MARINE HOLDINGS, INC.: marine, tokio                                                                |
| Toray Industries ADR Japan (TRYIY)                                               | TRYIY       | embedded |          1 |                               1 | embedded ticker TRYIY; name words shared with Toray Industries, Inc./Toray Industries Inc.: industries, toray                                                                                                   |
| Thales Unsponsored ADR (THLLY)                                                   | THLLY       | embedded |          1 |                               1 | embedded ticker THLLY; name words shared with Thales S.A./THALES: thales                                                                                                                                        |
| Terumo Corporation ADR (TRUMY)                                                   | TRUMY       | embedded |          1 |                               1 | embedded ticker TRUMY; name words shared with Terumo Corporation/Terumo Corp.: terumo                                                                                                                           |
| Telstra Group Ltd Sponsored ADR (TLGPY)                                          | TLGPY       | embedded |          1 |                               1 | embedded ticker TLGPY; name words shared with Telstra Group Limited/Telstra Group Limited: telstra                                                                                                              |
| Telia Co AB ADR (TLSNY)                                                          | TLSNY       | embedded |          1 |                               1 | embedded ticker TLSNY; name words shared with Telia Company AB (publ)/Telia Company AB: ab, telia                                                                                                               |
| Telenor ASA ADR (TELNY)                                                          | TELNY       | embedded |          1 |                               1 | embedded ticker TELNY; name words shared with Telenor ASA/Telenor ASA/TELENOR ASA: asa, telenor                                                                                                                 |
| Telefonica SA Sponsored ADR (TELFY)                                              | TELFY       | embedded |          1 |                               1 | embedded ticker TELFY; name words shared with Telefónica, S.A./Telefonica S.A./TELEFONICA S A: telefonica                                                                                                       |
| Telecom Italia SPA Sponsored (TIIAY)                                             | TIIAY       | embedded |          1 |                               1 | embedded ticker TIIAY; name words shared with Telecom Italia S.p.A./Telecom Italia S.p.A.: italia, telecom                                                                                                      |
| Techtronic Industries Sponsored ADR Hong Kong (TTNDY)                            | TTNDY       | embedded |          1 |                               1 | embedded ticker TTNDY; name words shared with Techtronic Industries Company Limited/Techtronic Industries Ltd.: industries, techtronic                                                                          |
| TDK Corp ADR Japan (TTDKY)                                                       | TTDKY       | embedded |          1 |                               1 | embedded ticker TTDKY; name words shared with TDK Corporation/TDK Corp.: tdk                                                                                                                                    |
| Takeda Pharmaceutical Company Limited (TAK)                                      | TAK         | embedded |          1 |                               1 | embedded ticker TAK; name words shared with Takeda Pharmaceutical Company Limited/Takeda Pharmaceutical Company L/TAKEDA PHARMACEUTICAL CO LTD: pharmaceutical, takeda                                          |
| Sysmex Corporation Unsponsored ADR (SSMXY)                                       | SSMXY       | embedded |          1 |                               1 | embedded ticker SSMXY; name words shared with Sysmex Corporation/Sysmex Corp.: sysmex                                                                                                                           |
| Symrise AG ADR (SYIEY)                                                           | SYIEY       | embedded |          1 |                               1 | embedded ticker SYIEY; name words shared with Symrise AG/Symrise Ag: symrise                                                                                                                                    |
| Swiss Re Ltd Sponsored ADR (SSREY)                                               | SSREY       | embedded |          1 |                               1 | embedded ticker SSREY; name words shared with Swiss Re AG/Swiss Re Ltd: re, swiss                                                                                                                               |
| Swire Pacific Ltd Sponsored ADR (SWRAY)                                          | SWRAY       | embedded |          1 |                               1 | embedded ticker SWRAY; name words shared with Swire Pacific Limited/Swire Pacific Ltd.: pacific, swire                                                                                                          |
| Swedbank AB ADR (SWDBY)                                                          | SWDBY       | embedded |          1 |                               1 | embedded ticker SWDBY; name words shared with Swedbank AB (publ)/Swedbank AB: ab, swedbank                                                                                                                      |
| Swatch Group AG ADR (SWGAY)                                                      | SWGAY       | embedded |          1 |                               1 | embedded ticker SWGAY; name words shared with The Swatch Group AG/Swatch Group AG: swatch                                                                                                                       |
| Svenska Handelbanken AB ADR (SVNLY)                                              | SVNLY       | embedded |          1 |                               1 | embedded ticker SVNLY; name words shared with Svenska Handelsbanken AB (publ)/Svenska Handelsbanken AB PUBL: ab, svenska                                                                                        |
| Suzuki Motor Corporation Ltd ADR (SZKMY)                                         | SZKMY       | embedded |          1 |                               1 | embedded ticker SZKMY; name words shared with Suzuki Motor Corporation/Suzuki Motor Co.: motor, suzuki                                                                                                          |
| Sun Hung Kai Properties Ltd Sponsored ADR (SUHJY)                                | SUHJY       | embedded |          1 |                               1 | embedded ticker SUHJY; name words shared with Sun Hung Kai Properties Limited/Sun Hung Kai Properties Ltd.: hung, kai, properties, sun                                                                          |
| Sumitomo Mitsui Trust Group Inc Sponsored ADR (SUTNY)                            | SUTNY       | embedded |          1 |                               1 | embedded ticker SUTNY; name words shared with Sumitomo Mitsui Trust Group, Inc./Sumitomo Mitsui Trust Group, In: mitsui, sumitomo                                                                               |
| Sumitomo Metal Mining Co Ltd Unsponsored ADR (SMMYY)                             | SMMYY       | embedded |          1 |                               1 | embedded ticker SMMYY; name words shared with Sumitomo Metal Mining Co., Ltd./Sumitomo Metal Mining Co., Ltd.: metal, mining, sumitomo                                                                          |
| Sumitomo Electric Industries Ltd ADR Japan (SMTOY)                               | SMTOY       | embedded |          1 |                               1 | embedded ticker SMTOY; name words shared with Sumitomo Electric Industries, Ltd./Sumitomo Electric Industries Lt/SUMITOMO ELECTRIC INDUSTRIES LTD/ADR/: electric, industries, sumitomo                          |
| Subaru Corporation Unsponsored ADR (FUJHY)                                       | FUJHY       | embedded |          1 |                               1 | embedded ticker FUJHY; name words shared with Subaru Corporation/Subaru Corporation: subaru                                                                                                                     |
| Stora Enso Oyj ADR (SEOAY)                                                       | SEOAY       | embedded |          1 |                               1 | embedded ticker SEOAY; name words shared with Stora Enso Oyj/Stora Enso Oyj: enso, oyj, stora                                                                                                                   |
| Standard Chartered plc ADR (SCBFY)                                               | SCBFY       | embedded |          1 |                               1 | embedded ticker SCBFY; name words shared with Standard Chartered PLC/Standard Chartered PLC: chartered, standard                                                                                                |
| South32 Ltd Sponsored ADR (SOUHY)                                                | SOUHY       | embedded |          1 |                               1 | embedded ticker SOUHY; name words shared with South32 Limited/South32 Ltd.: south32                                                                                                                             |
| Sony Financial Group Inc Sponsored ADR (SFGYY)                                   | SFGYY       | embedded |          1 |                               1 | embedded ticker SFGYY; name words shared with Sony Financial Group Inc./Sony Financial Group Inc./Sony Financial Group Inc./ADR: financial, sony                                                                |
| Sonova Holding AG ADR (SONVY)                                                    | SONVY       | embedded |          1 |                               1 | embedded ticker SONVY; name words shared with Sonova Holding AG/Sonova Holding AG: sonova                                                                                                                       |
| Sonic Healthcare Ltd Sponsored ADR (SKHHY)                                       | SKHHY       | embedded |          1 |                               1 | embedded ticker SKHHY; name words shared with Sonic Healthcare Limited/Sonic Healthcare Ltd.: healthcare, sonic                                                                                                 |
| Sompo Holdings Inc Unsponsored ADR (SMPNY)                                       | SMPNY       | embedded |          1 |                               1 | embedded ticker SMPNY; name words shared with Sompo Holdings, Inc./Sompo Hldgs Inc: sompo                                                                                                                       |
| Softbank Group Corp ADR (SFTBY)                                                  | SFTBY       | embedded |          1 |                               1 | embedded ticker SFTBY; name words shared with SoftBank Group Corp./Softbank Group Corp: softbank                                                                                                                |
| Softbank Corp Unsponsored ADR (SOBKY)                                            | SOBKY       | embedded |          1 |                               1 | embedded ticker SOBKY; name words shared with SoftBank Corp./Softbank Corp.: softbank                                                                                                                           |
| Sodexo ADR (SDXAY)                                                               | SDXAY       | embedded |          1 |                               1 | embedded ticker SDXAY; name words shared with Sodexo S.A./Sodexo: sodexo                                                                                                                                        |
| Societe Generale France Sponsored ADR (SCGLY)                                    | SCGLY       | embedded |          1 |                               1 | embedded ticker SCGLY; name words shared with Société Générale Société anonyme/Societe Generale: generale, societe                                                                                              |
| Smiths Group plc Sponsored ADR (SMGZY)                                           | SMGZY       | embedded |          1 |                               1 | embedded ticker SMGZY; name words shared with Smiths Group plc/Smiths Group Plc: smiths                                                                                                                         |
| SMC Corp Sponsored ADR (SMCAY)                                                   | SMCAY       | embedded |          1 |                               1 | embedded ticker SMCAY; name words shared with SMC Corporation/SMC Corp: smc                                                                                                                                     |
| Skanska AB Sponsored ADR (SKBSY)                                                 | SKBSY       | embedded |          1 |                               1 | embedded ticker SKBSY; name words shared with Skanska AB (publ)/Skanska AB: ab, skanska                                                                                                                         |
| Singapore Telecom Ltd New Sponsored ADR (SGAPY)                                  | SGAPY       | embedded |          1 |                               1 | embedded ticker SGAPY; name words shared with Singapore Telecommunications Limited/Singapore Telecommunications Lt: singapore, telecom                                                                          |
| Singapore Exchange Ltd ADR (SPXCY)                                               | SPXCY       | embedded |          1 |                               1 | embedded ticker SPXCY; name words shared with Singapore Exchange Limited/Singapore Exchange Ltd.: exchange, singapore                                                                                           |
| Singapore Airlines Ltd ADR (SINGY)                                               | SINGY       | embedded |          1 |                               1 | embedded ticker SINGY; name words shared with Singapore Airlines Limited/Singapore Airlines Ltd.: airlines, singapore                                                                                           |
| Siemens Energy AG Sponsored ADR (SMERY)                                          | SMERY       | embedded |          1 |                               1 | embedded ticker SMERY; name words shared with Siemens Energy AG/Siemens Energy AG/Siemens Energy AG/ADR: energy, siemens                                                                                        |
| Siemens AG Sponsored ADR (SIEGY)                                                 | SIEGY       | embedded |          1 |                               1 | embedded ticker SIEGY; name words shared with Siemens Aktiengesellschaft/Siemens AG: siemens                                                                                                                    |
| Shiseido Co Ltd Sponsored ADR Japan (SSDOY)                                      | SSDOY       | embedded |          1 |                               1 | embedded ticker SSDOY; name words shared with Shiseido Company, Limited/Shiseido Company, Ltd.: shiseido                                                                                                        |
| Shionogi & Co Ltd ADR (SGIOY)                                                    | SGIOY       | embedded |          1 |                               1 | embedded ticker SGIOY; name words shared with Shionogi & Co., Ltd./Shionogi & Co. Ltd.: shionogi                                                                                                                |
| Shin Etsu Chemical Co Ltd ADR (SHECY)                                            | SHECY       | embedded |          1 |                               1 | embedded ticker SHECY; name words shared with Shin-Etsu Chemical Co., Ltd./Shin-Etsu Chemical Co., Ltd.: chemical, etsu, shin                                                                                   |
| Shimano Inc Unsponsored ADR (SMNNY)                                              | SMNNY       | embedded |          1 |                               1 | embedded ticker SMNNY; name words shared with Shimano Inc./Shimano Inc.: shimano                                                                                                                                |
| SGS SA ADR Unsponsored (SGSOY)                                                   | SGSOY       | embedded |          1 |                               1 | embedded ticker SGSOY; name words shared with SGS SA/SGS SA: sgs                                                                                                                                                |
| Seven & I Holdings Co Ltd ADR (SVNDY)                                            | SVNDY       | embedded |          1 |                               1 | embedded ticker SVNDY; name words shared with Seven & i Holdings Co., Ltd./Seven & I Holdings Co., Ltd.: seven                                                                                                  |
| Sekisui House Ltd Sponsored ADR (SKHSY)                                          | SKHSY       | embedded |          1 |                               1 | embedded ticker SKHSY; name words shared with Sekisui House, Ltd./Sekisui House Ltd.: house, sekisui                                                                                                            |
| Secom Ltd ADR Japan (SOMLY)                                                      | SOMLY       | embedded |          1 |                               1 | embedded ticker SOMLY; name words shared with SECOM CO., LTD./Secom Co., Ltd.: secom                                                                                                                            |
| Sea Limited (SE)                                                                 | SE          | embedded |          1 |                               1 | embedded ticker SE; name words shared with Sea Limited/Sea Limited/Sea Ltd: sea                                                                                                                                 |
| Sandvik AB Sponsored ADR (SDVKY)                                                 | SDVKY       | embedded |          1 |                               1 | embedded ticker SDVKY; name words shared with Sandvik AB (publ)/Sandvik AB: ab, sandvik                                                                                                                         |
| Sandoz Group AG Sponsored ADR (SDZNY)                                            | SDZNY       | embedded |          1 |                               1 | embedded ticker SDZNY; name words shared with Sandoz Group AG/Sandoz Group AG: sandoz                                                                                                                           |
| Sampo OYJ ADR (SAXPY)                                                            | SAXPY       | embedded |          1 |                               1 | embedded ticker SAXPY; name words shared with Sampo Oyj/Sampo OYJ: oyj, sampo                                                                                                                                   |
| Sage Group plc Unsponsored ADR (SGPYY)                                           | SGPYY       | embedded |          1 |                               1 | embedded ticker SGPYY; name words shared with The Sage Group plc/Sage Group plc (The): sage                                                                                                                     |
| Safran SA ADR (SAFRY)                                                            | SAFRY       | embedded |          1 |                               1 | embedded ticker SAFRY; name words shared with Safran SA/Safran SA: safran                                                                                                                                       |
| Saab AB ADR (SAABY)                                                              | SAABY       | embedded |          1 |                               1 | embedded ticker SAABY; name words shared with Saab AB (publ)/Saab AB: ab, saab                                                                                                                                  |
| Ryanair Holdings plc (RYAAY)                                                     | RYAAY       | embedded |          1 |                               1 | embedded ticker RYAAY; name words shared with Ryanair Holdings plc/Ryanair Holdings plc/RYANAIR HOLDINGS PLC: ryanair                                                                                           |
| Roche Holdings Ltd Sponsored ADR (RHHBY)                                         | RHHBY       | embedded |          1 |                               1 | embedded ticker RHHBY; name words shared with Roche Holding AG/Roche Holding Ltd: roche                                                                                                                         |
| Rheinmetall AG ADR (RNMBY)                                                       | RNMBY       | embedded |          1 |                               1 | embedded ticker RNMBY; name words shared with Rheinmetall AG/Rheinmetall AG: rheinmetall                                                                                                                        |
| Resona Holdings Inc ADR (RSHGY)                                                  | RSHGY       | embedded |          1 |                               1 | embedded ticker RSHGY; name words shared with Resona Holdings, Inc./Resona Holdings, Inc./RESONA HOLDINGS INC: resona                                                                                           |
| Rentokil Initial plc (RTO)                                                       | RTO         | embedded |          1 |                               1 | embedded ticker RTO; name words shared with Rentokil Initial plc/Rentokil Initial plc/RENTOKIL INITIAL PLC /FI: initial, rentokil                                                                               |
| Renesas Electronic Corp ADR (RNECY)                                              | RNECY       | embedded |          1 |                               1 | embedded ticker RNECY; name words shared with Renesas Electronics Corporation/Renesas Electronics Corp: electronic, renesas                                                                                     |
| Renault SA Unsponsored ADR (RNLSY)                                               | RNLSY       | embedded |          1 |                               1 | embedded ticker RNLSY; name words shared with Renault SA/Renault SA: renault                                                                                                                                    |
| RELX plc (RELX)                                                                  | RELX        | embedded |          1 |                               1 | embedded ticker RELX; name words shared with RELX PLC/RELX PLC PLC/RELX PLC: relx                                                                                                                               |
| Reckitt Benckiser Group plc Sponsored ADR (RBGLY)                                | RBGLY       | embedded |          1 |                               1 | embedded ticker RBGLY; name words shared with Reckitt Benckiser Group plc/Reckitt Benckiser Group Plc./RECKITT BENCKISER GROUP PLC: benckiser, reckitt                                                          |
| QBE Insurance Group Ltd Sponsored ADR (QBIEY)                                    | QBIEY       | embedded |          1 |                               1 | embedded ticker QBIEY; name words shared with QBE Insurance Group Limited/QBE Insurance Group Ltd.: insurance, qbe                                                                                              |
| Qantas Airways Ltd Sponsored ADR (QABSY)                                         | QABSY       | embedded |          1 |                               1 | embedded ticker QABSY; name words shared with Qantas Airways Limited/Qantas Airways Ltd.: airways, qantas                                                                                                       |
| Publicis Groupe S.A. New Sponsored ADR (PUBGY)                                   | PUBGY       | embedded |          1 |                               1 | embedded ticker PUBGY; name words shared with Publicis Groupe S.A./Publicis Groupe S.A.: groupe, publicis                                                                                                       |
| Prysmian SPA ADR (PRYMY)                                                         | PRYMY       | embedded |          1 |                               1 | embedded ticker PRYMY; name words shared with Prysmian S.p.A./Prysmian S.P.A.: prysmian                                                                                                                         |
| Prudential plc ADR United Kingdom (PUK)                                          | PUK         | embedded |          1 |                               1 | embedded ticker PUK; name words shared with Prudential plc/Prudential Public Limited Compa/PRUDENTIAL PLC: prudential                                                                                           |
| Prosus NV Sponsored ADR (PROSY)                                                  | PROSY       | embedded |          1 |                               1 | embedded ticker PROSY; name words shared with Prosus N.V./Prosus NV: prosus                                                                                                                                     |
| Pernod Ricard SA Sponsored ADR (PRNDY)                                           | PRNDY       | embedded |          1 |                               1 | embedded ticker PRNDY; name words shared with Pernod Ricard SA/Pernod Ricard S.A.: pernod, ricard                                                                                                               |
| Pandora A/S ADR (PNDRY)                                                          | PNDRY       | embedded |          1 |                               1 | embedded ticker PNDRY; name words shared with Pandora A/S/Pandora A/S/Pandora A/S / ADR: pandora                                                                                                                |
| Panasonic Corporation ADR (PCRHY)                                                | PCRHY       | embedded |          1 |                               1 | embedded ticker PCRHY; name words shared with Panasonic Holdings Corporation/Panasonic Holdings Corporation: panasonic                                                                                          |
| Overseas-Chinese Bank ADR (OVCHY)                                                | OVCHY       | embedded |          1 |                               1 | embedded ticker OVCHY; name words shared with Oversea-Chinese Banking Corporation Limited/Overseas Chinese Banking Corp.,: bank, chinese, oversea, overseas                                                     |
| Otsuka Holdings Co Ltd Unsponsored ADR (OTSKY)                                   | OTSKY       | embedded |          1 |                               1 | embedded ticker OTSKY; name words shared with Otsuka Holdings Co., Ltd./Otsuka Holdings Co. Ltd.: otsuka                                                                                                        |
| Orkla ASA Sponsored ADR (ORKLY)                                                  | ORKLY       | embedded |          1 |                               1 | embedded ticker ORKLY; name words shared with Orkla ASA/Orkla ASA: asa, orkla                                                                                                                                   |
| Oriental Land Co Ltd Unsponsored ADR (OLCLY)                                     | OLCLY       | embedded |          1 |                               1 | embedded ticker OLCLY; name words shared with Oriental Land Co., Ltd./Oriental Land Co., Ltd.: land, oriental                                                                                                   |
| Orange Sponsored ADR (ORANY)                                                     | ORANY       | embedded |          1 |                               1 | embedded ticker ORANY; name words shared with Orange S.A./Orange/ORANGE: orange                                                                                                                                 |
| Obic Co Ltd ADR (OBICY)                                                          | OBICY       | embedded |          1 |                               1 | embedded ticker OBICY; name words shared with OBIC Co.,Ltd./Obic Co. Ltd./OBIC Co., Ltd./ADR: obic                                                                                                              |
| NTT Inc Sponsored ADR (NTTYY)                                                    | NTTYY       | embedded |          1 |                               1 | embedded ticker NTTYY; name words shared with NTT, Inc./NTT Inc./NIPPON TELEGRAPH & TELEPHONE CORP: ntt                                                                                                         |
| Novonesis B ADR (NVZMY)                                                          | NVZMY       | embedded |          1 |                               1 | embedded ticker NVZMY; name words shared with Novozymes A/S/NOVONESIS A S: novonesis                                                                                                                            |
| Norsk Hydro A.S. New Norway Sponsored ADR (NHYDY)                                | NHYDY       | embedded |          1 |                               1 | embedded ticker NHYDY; name words shared with Norsk Hydro ASA/Norsk Hydro ASA: hydro, norsk                                                                                                                     |
| Nordea BK ABP Sponsored ADR (NRDBY)                                              | NRDBY       | embedded |          1 |                               1 | embedded ticker NRDBY; name words shared with Nordea Bank Abp/Nordea Bank Abp: abp, nordea                                                                                                                      |
| Nomura Research Institute Ltd ADR (NRILY)                                        | NRILY       | embedded |          1 |                               1 | embedded ticker NRILY; name words shared with Nomura Research Institute, Ltd./Nomura Research Institute Ltd.: institute, nomura, research                                                                       |
| NN Group NV Unsponsored ADR (NNGRY)                                              | NNGRY       | embedded |          1 |                               1 | embedded ticker NNGRY; name words shared with NN Group N.V./NN Group NV: nn                                                                                                                                     |
| Nippon Yusen Kabushiki Sponsored ADR (NPNYY)                                     | NPNYY       | embedded |          1 |                               1 | embedded ticker NPNYY; name words shared with Nippon Yusen Kabushiki Kaisha/Nippon Yusen Kabushiki Kaisha: kabushiki, nippon, yusen                                                                             |
| Nippon Steel Corporation Unsponsored ADR (NPSCY)                                 | NPSCY       | embedded |          1 |                               1 | embedded ticker NPSCY; name words shared with Nippon Steel Corporation/Nippon Steel Corporation: nippon, steel                                                                                                  |
| Nintendo Ltd ADR Japan (NTDOY)                                                   | NTDOY       | embedded |          1 |                               1 | embedded ticker NTDOY; name words shared with Nintendo Co., Ltd./Nintendo Co., Ltd.: nintendo                                                                                                                   |
| NICE Ltd - (NICE)                                                                | NICE        | embedded |          1 |                               1 | embedded ticker NICE; name words shared with NICE Ltd./NICE Ltd/NICE Ltd.: nice                                                                                                                                 |
| Nexon Company Ltd Unsponsored ADR (NEXOY)                                        | NEXOY       | embedded |          1 |                               1 | embedded ticker NEXOY; name words shared with NEXON Co., Ltd./Nexon Co Ltd.: nexon                                                                                                                              |
| Nestle SA Sponsored ADR (NSRGY)                                                  | NSRGY       | embedded |          1 |                               1 | embedded ticker NSRGY; name words shared with Nestlé S.A./Nestle S.A.: nestle                                                                                                                                   |
| NatWest Group plc (NWG)                                                          | NWG         | embedded |          1 |                               1 | embedded ticker NWG; name words shared with NatWest Group plc/NatWest Group plc/NatWest Group plc: natwest                                                                                                      |
| National Australia Bank Ltd Sponsored ADR (NABZY)                                | NABZY       | embedded |          1 |                               1 | embedded ticker NABZY; name words shared with National Australia Bank Limited/National Australia Bank Ltd. (V: australia, bank, national                                                                        |
| Murata MFG Co Ltd ADR (MRAAY)                                                    | MRAAY       | embedded |          1 |                               1 | embedded ticker MRAAY; name words shared with Murata Manufacturing Co., Ltd./Murata Manufacturing Inc.: murata                                                                                                  |
| Munich Re Group ADR (MURGY)                                                      | MURGY       | override |          1 |                               1 | J5 override '(murgy)' (yahoo)                                                                                                                                                                                   |
| MS&AD Insurance Group Holdings ADR (MSADY)                                       | MSADY       | embedded |          1 |                               1 | embedded ticker MSADY; name words shared with MS&AD Insurance Group Holdings, Inc./MS&AD Insurance Group Holdings,: ad, insurance, ms                                                                           |
| Moncler SPA Unsponsored ADR (MONRY)                                              | MONRY       | embedded |          1 |                               1 | embedded ticker MONRY; name words shared with Moncler S.p.A./Moncler S.P.A.: moncler                                                                                                                            |
| Mitsui Osk Lines Ltd Unsponsored ADR (MSLOY)                                     | MSLOY       | embedded |          1 |                               1 | embedded ticker MSLOY; name words shared with Mitsui O.S.K. Lines, Ltd./Mitsui O.S.K. Lines Ltd.: lines, mitsui                                                                                                 |
| Mitsui Fudosan Co Ltd ADR (MTSFY)                                                | MTSFY       | embedded |          1 |                               1 | embedded ticker MTSFY; name words shared with Mitsui Fudosan Co., Ltd./Mitsui Fudosan Co., Ltd.: fudosan, mitsui                                                                                                |
| Mitsui & Co Ltd ADR Japan (MITSY)                                                | MITSY       | embedded |          1 |                               1 | embedded ticker MITSY; name words shared with Mitsui & Co., Ltd./Mitsui & Co., Ltd.: mitsui                                                                                                                     |
| Mitsubishi Heavy Industries Ltd ADR (MHVIY)                                      | MHVIY       | embedded |          1 |                               1 | embedded ticker MHVIY; name words shared with Mitsubishi Heavy Industries, Ltd./Mitsubishi Heavy Industries Ltd: heavy, industries, mitsubishi                                                                  |
| Mitsubishi Estate Ltd ADR (MITEY)                                                | MITEY       | embedded |          1 |                               1 | embedded ticker MITEY; name words shared with Mitsubishi Estate Co., Ltd./Mitsubishi Estate Co. Ltd.: estate, mitsubishi                                                                                        |
| Mitsubishi Electric Corporation ADR Japan (MIELY)                                | MIELY       | embedded |          1 |                               1 | embedded ticker MIELY; name words shared with Mitsubishi Electric Corporation/Mitsubishi Electric Corp.: electric, mitsubishi                                                                                   |
| Mitsubishi Corporation ADR (MTSUY)                                               | MTSUY       | embedded |          1 |                               1 | embedded ticker MTSUY; name words shared with Mitsubishi Corporation/Mitsubishi Corp.: mitsubishi                                                                                                               |
| Michelin Compagnie Generale ADR (MGDDY)                                          | MGDDY       | embedded |          1 |                               1 | embedded ticker MGDDY; name words shared with Compagnie Générale des Établissements Michelin Société en commandite par actions/CIE GENERALE DES ETABLISSEMENTS: compagnie, generale, michelin                   |
| Mercedes-Benz Group AG Unsponsored ADR (MBGYY)                                   | MBGYY       | embedded |          1 |                               1 | embedded ticker MBGYY; name words shared with Mercedes-Benz Group AG/Mercedes Benz Group AG: benz, mercedes                                                                                                     |
| Marubeni Corporation ADR Japan (MARUY)                                           | MARUY       | embedded |          1 |                               1 | embedded ticker MARUY; name words shared with Marubeni Corporation/Marubeni Corp.: marubeni                                                                                                                     |
| Macquarie Group Ltd Unsponsored ADR (MQBKY)                                      | MQBKY       | embedded |          1 |                               1 | embedded ticker MQBKY; name words shared with Macquarie Group Limited/Macquarie Group, Ltd.: macquarie                                                                                                          |
| Lynas Rare Earths Ltd Sponsored ADR (LYSDY)                                      | LYSDY       | embedded |          1 |                               1 | embedded ticker LYSDY; name words shared with Lynas Rare Earths Limited/Lynas Rare Earths Limited: earths, lynas, rare                                                                                          |
| LY Corporation ADR (YAHOY)                                                       | YAHOY       | embedded |          1 |                               1 | embedded ticker YAHOY; name words shared with LY Corporation/LY Corporation: ly                                                                                                                                 |
| Loreal Company ADR France (LRLCY)                                                | LRLCY       | embedded |          1 |                               1 | embedded ticker LRLCY; name words shared with L'Oréal S.A./L'Oreal Co.: loreal                                                                                                                                  |
| Lonza Group AG ADR (LZAGY)                                                       | LZAGY       | embedded |          1 |                               1 | embedded ticker LZAGY; name words shared with Lonza Group AG/Lonza Group AG: lonza                                                                                                                              |
| London Stock Exchange Group Sponsored ADR (LSEGY)                                | LSEGY       | embedded |          1 |                               1 | embedded ticker LSEGY; name words shared with London Stock Exchange Group plc/London Stock Exchange Group plc/London Stock Exchange Group plc: exchange, london                                                 |
| Leonardo SPA ADR (FINMY)                                                         | FINMY       | embedded |          1 |                               1 | embedded ticker FINMY; name words shared with Leonardo S.p.a./Leonardo S.P.A.: leonardo                                                                                                                         |
| Legrand SA Unsponsored ADR (LGRDY)                                               | LGRDY       | embedded |          1 |                               1 | embedded ticker LGRDY; name words shared with Legrand SA/LeGrand SA: legrand                                                                                                                                    |
| Legal & General Group plc Sponsored ADR (LGGNY)                                  | LGGNY       | embedded |          1 |                               1 | embedded ticker LGGNY; name words shared with Legal & General Group Plc/Legal & General Group Plc: general, legal                                                                                               |
| Lasertec Corporation ADR (LSRCY)                                                 | LSRCY       | embedded |          1 |                               1 | embedded ticker LSRCY; name words shared with Lasertec Corporation/Lasertec Corp.: lasertec                                                                                                                     |
| Land Secs Group plc ADR (LDSCY)                                                  | LDSCY       | embedded |          1 |                               1 | embedded ticker LDSCY; name words shared with Land Securities Group Plc/Land Securities Group Plc.: land                                                                                                        |
| Lam Research Corporation (LRCX)                                                  | LRCX        | embedded |          1 |                               1 | embedded ticker LRCX; name words shared with Lam Research Corporation/Lam Research Corporation/LAM RESEARCH CORP: lam, research                                                                                 |
| Kuehne & Nagel International AG ADR (KHNGY)                                      | KHNGY       | embedded |          1 |                               1 | embedded ticker KHNGY; name words shared with Kuehne + Nagel International AG/Kuehne & Nagel International AG: kuehne, nagel                                                                                    |
| Kubota Corporation ADR Japan (KUBTY)                                             | KUBTY       | embedded |          1 |                               1 | embedded ticker KUBTY; name words shared with Kubota Corporation/Kubota Corp.: kubota                                                                                                                           |
| Koninklijke Philips NV Sponsored ADR (PHG)                                       | PHG         | embedded |          1 |                               1 | embedded ticker PHG; name words shared with Koninklijke Philips N.V./Koninklijke Philips N.V. NY Reg/KONINKLIJKE PHILIPS NV: koninklijke, philips                                                               |
| Koninklijke Ahold Delhaize NV Sponsored ADR (ADRNY)                              | ADRNY       | embedded |          1 |                               1 | embedded ticker ADRNY; name words shared with Koninklijke Ahold Delhaize N.V./Koninklijke Ahold Delhaize N.V.: ahold, delhaize, koninklijke                                                                     |
| Kongsberg Gruppen ASA ADR (KBGGY)                                                | KBGGY       | embedded |          1 |                               1 | embedded ticker KBGGY; name words shared with Kongsberg Gruppen ASA/Kongsberg Gruppen ASA/Kongsberg Gruppen ASA/ADR: asa, gruppen, kongsberg                                                                    |
| Kone Oyj ADR (KNYJY)                                                             | KNYJY       | embedded |          1 |                               1 | embedded ticker KNYJY; name words shared with KONE Oyj/Kone Oyj: kone, oyj                                                                                                                                      |
| Komatsu Ltd Sponsored ADR (KMTUY)                                                | KMTUY       | embedded |          1 |                               1 | embedded ticker KMTUY; name words shared with Komatsu Ltd./Komatsu Ltd.: komatsu                                                                                                                                |
| Knorr-Bremse Unsponsored ADR (KNRRY)                                             | KNRRY       | embedded |          1 |                               1 | embedded ticker KNRRY; name words shared with Knorr-Bremse AG/Knorr-Bremse: bremse, knorr                                                                                                                       |
| Kirin Holdings Ltd Sponsored ADR (KNBWY)                                         | KNBWY       | embedded |          1 |                               1 | embedded ticker KNBWY; name words shared with Kirin Holdings Company, Limited/Kirin Holdings Co., Ltd.: kirin                                                                                                   |
| Kioxia Holdings Corporation ADR (KXIAY)                                          | KXIAY       | embedded |          1 |                               1 | embedded ticker KXIAY; name words shared with Kioxia Holdings Corporation/KIOXIA HLDGS CORP/Kioxia Holdings Corporation/ADR: kioxia                                                                             |
| Kingfisher plc Sponsored ADR (KGFHY)                                             | KGFHY       | embedded |          1 |                               1 | embedded ticker KGFHY; name words shared with Kingfisher plc/Kingfisher plc: kingfisher                                                                                                                         |
| Kering SA Unsponosred ADR (PPRUY)                                                | PPRUY       | embedded |          1 |                               1 | embedded ticker PPRUY; name words shared with Kering SA/Kering SA: kering                                                                                                                                       |
| KDDI Corporation ADR (KDDIY)                                                     | KDDIY       | embedded |          1 |                               1 | embedded ticker KDDIY; name words shared with KDDI Corporation/KDDI Corp.: kddi                                                                                                                                 |
| KBC Group NV ADR (KBCSY)                                                         | KBCSY       | embedded |          1 |                               1 | embedded ticker KBCSY; name words shared with KBC Group NV/KBC Group SA: kbc                                                                                                                                    |
| Airbus SE (EADSY)                                                                | EADSY       | embedded |          1 |                               1 | embedded ticker EADSY; name words shared with Airbus SE/Airbus SE: airbus                                                                                                                                       |
| Kawaski Heavy Industries Sponsored ADR (KWHIY)                                   | KWHIY       | embedded |          1 |                               1 | embedded ticker KWHIY; name words shared with Kawasaki Heavy Industries, Ltd./Kawasaki Heavy Industries Ltd.: heavy, industries                                                                                 |
| Air Liquide Ord ADR (AIQUY)                                                      | AIQUY       | embedded |          1 |                               1 | embedded ticker AIQUY; name words shared with L'Air Liquide S.A./L'Air Liquide SA: liquide                                                                                                                      |
| Kao Corporation Unsponsored ADR (KAOOY)                                          | KAOOY       | embedded |          1 |                               1 | embedded ticker KAOOY; name words shared with Kao Corporation/Kao Corp.: kao                                                                                                                                    |
| Julius Baer Group Ltd ADR (JBAXY)                                                | JBAXY       | embedded |          1 |                               1 | embedded ticker JBAXY; name words shared with Julius Bär Gruppe AG/Julius Baer Group Ltd.: baer, julius                                                                                                         |
| AIB Group ADR (AIBGY)                                                            | AIBGY       | embedded |          1 |                               1 | embedded ticker AIBGY; name words shared with AIB Group plc/AIB Group PLC: aib                                                                                                                                  |
| Jeronimo Martins SGPS SA ADR (JRONY)                                             | JRONY       | embedded |          1 |                               1 | embedded ticker JRONY; name words shared with Jerónimo Martins, SGPS, S.A./Jeronimo Martins, SGPS, SA: jeronimo, martins, sgps                                                                                  |
| Ageas SA - ADR (AGESY)                                                           | AGESY       | embedded |          1 |                               1 | embedded ticker AGESY; name words shared with ageas SA/NV/ageas SA/NV: ageas                                                                                                                                    |
| Jardine Matheson Holdings Unsponsored ADR (JMHLY)                                | JMHLY       | embedded |          1 |                               1 | embedded ticker JMHLY; name words shared with Jardine Matheson Holdings Limited/Jardine Matheson Holdings Ltd.: jardine, matheson                                                                               |
| Japan Tobacco Inc Unsponsored ADR (JAPAY)                                        | JAPAY       | embedded |          1 |                               1 | embedded ticker JAPAY; name words shared with Japan Tobacco Inc./Japan Tobacco: tobacco                                                                                                                         |
| Japan Exchange Group Inc Unsponsored ADR (JPXGY)                                 | JPXGY       | embedded |          1 |                               1 | embedded ticker JPXGY; name words shared with Japan Exchange Group, Inc./Japan Exchange Group, Inc.: exchange                                                                                                   |
| J. Sainsbury plc Sponsored ADR (JSAIY)                                           | JSAIY       | embedded |          1 |                               1 | embedded ticker JSAIY; name words shared with J Sainsbury plc/J Sainsbury plc: sainsbury                                                                                                                        |
| Itochu Corporation ADR Japan (ITOCY)                                             | ITOCY       | embedded |          1 |                               1 | embedded ticker ITOCY; name words shared with ITOCHU Corporation/Itochu Corp.: itochu                                                                                                                           |
| Aeon ADR (AONNY)                                                                 | AONNY       | embedded |          1 |                               1 | embedded ticker AONNY; name words shared with Aeon Co., Ltd./Aeon Co. Ltd.: aeon                                                                                                                                |
| Isuzu Motor Company Ltd ADR (ISUZY)                                              | ISUZY       | embedded |          1 |                               1 | embedded ticker ISUZY; name words shared with Isuzu Motors Limited/Isuzu Motors, Ltd.: isuzu, motor                                                                                                             |
| Intesa Sanpaolo Sponsored ADR (ISNPY)                                            | ISNPY       | embedded |          1 |                               1 | embedded ticker ISNPY; name words shared with Intesa Sanpaolo S.p.A./Intesa Sanpaolo S.p.A.: intesa, sanpaolo                                                                                                   |
| Aena SME ADR (ANYYY)                                                             | ANYYY       | embedded |          1 |                               1 | embedded ticker ANYYY; name words shared with Aena S.M.E., S.A./Aena SME S.A.: aena, sme                                                                                                                        |
| International Consolidated Airlines Group Sponsored ADR (ICAGY)                  | ICAGY       | embedded |          1 |                               1 | embedded ticker ICAGY; name words shared with International Consolidated Airlines Group S.A./International Consolidated Airl: airl, airlines, consolidated                                                      |
| Adyen ADR (ADYEY)                                                                | ADYEY       | embedded |          1 |                               1 | embedded ticker ADYEY; name words shared with Adyen N.V./Adyen N.V.: adyen                                                                                                                                      |
| Intercontinental Hotels Group American (IHG)                                     | IHG         | embedded |          1 |                               1 | embedded ticker IHG; name words shared with InterContinental Hotels Group PLC/Intercontinental Hotels Group/INTERCONTINENTAL HOTELS GROUP PLC /NEW/: hotels, intercontinental                                   |
| Informa plc Sponsored ADR (IFJPY)                                                | IFJPY       | embedded |          1 |                               1 | embedded ticker IFJPY; name words shared with Informa plc/Informa Plc.: informa                                                                                                                                 |
| Advantest Corp (ATEYY)                                                           | ATEYY       | embedded |          1 |                               1 | embedded ticker ATEYY; name words shared with Advantest Corporation/Advantest Corp./ADVANTEST CORP: advantest                                                                                                   |
| Infineon Technologies ADR (IFNNY)                                                | IFNNY       | embedded |          1 |                               1 | embedded ticker IFNNY; name words shared with Infineon Technologies AG/Infineon Technologies AG/INFINEON TECHNOLOGIES AG: infineon, technologies                                                                |
| Admiral Group ADR (AMIGY)                                                        | AMIGY       | embedded |          1 |                               1 | embedded ticker AMIGY; name words shared with Admiral Group plc/Admiral Group Plc.: admiral                                                                                                                     |
| Industria De Diseno Textil Inditex ADR (IDEXY)                                   | IDEXY       | embedded |          1 |                               1 | embedded ticker IDEXY; name words shared with Industria de Diseño Textil, S.A./Industria de Diseno Textil Indi: diseno, indi, industria, textil                                                                 |
| Indra Sistemas ADR (ISMAY)                                                       | ISMAY       | embedded |          1 |                               1 | embedded ticker ISMAY; name words shared with Indra Sistemas, S.A./Indra Sistemas SA: indra, sistemas                                                                                                           |
| adidas AG (ADDYY)                                                                | ADDYY       | embedded |          1 |                               1 | embedded ticker ADDYY; name words shared with adidas AG/adidas AG: adidas                                                                                                                                       |
| IHI Corporation Unsponsored ADR (IHICY)                                          | IHICY       | embedded |          1 |                               1 | embedded ticker IHICY; name words shared with IHI Corporation/IHI Corp: ihi                                                                                                                                     |
| ACS Actividades De Construccion Y Servicios (ACSAY)                              | ACSAY       | embedded |          1 |                               1 | embedded ticker ACSAY; name words shared with ACS, Actividades de Construcción y Servicios, S.A./ACS Actividades De Construccion: acs, actividades, construccion, servicios                                     |
| Hoya Corporation Sponsored ADR (HOCPY)                                           | HOCPY       | embedded |          1 |                               1 | embedded ticker HOCPY; name words shared with HOYA Corporation/Hoya Corp.: hoya                                                                                                                                 |
| Hong Kong Exchanges & Clearing Ltd ADR (HKXCY)                                   | HKXCY       | embedded |          1 |                               1 | embedded ticker HKXCY; name words shared with Hong Kong Exchanges and Clearing Limited/Hong Kong Exchange & Clearing L: clearing, exchange, exchanges, hong, kong                                               |
| ABN Amro Bank (AAVMY)                                                            | AAVMY       | embedded |          1 |                               1 | embedded ticker AAVMY; name words shared with ABN AMRO Bank N.V./Abn Amro BK N V: abn, amro, bank                                                                                                               |
| Holcim Ltd Sponsored ADR (HCMLY)                                                 | HCMLY       | embedded |          1 |                               1 | embedded ticker HCMLY; name words shared with Holcim AG/HOLCIM LTD: holcim                                                                                                                                      |
| Hitachi Ltd ADR Japan (HTHIY)                                                    | HTHIY       | embedded |          1 |                               1 | embedded ticker HTHIY; name words shared with Hitachi, Ltd./Hitachi Ltd./HITACHI LTD: hitachi                                                                                                                   |
| ABB Ltd. (ABBNY)                                                                 | ABBNY       | embedded |          1 |                               1 | embedded ticker ABBNY; name words shared with ABB Ltd/ABB Ltd./ABB LTD: abb                                                                                                                                     |
| Hexagon AB Unsponsored ADR (HXGBY)                                               | HXGBY       | embedded |          1 |                               1 | embedded ticker HXGBY; name words shared with Hexagon AB (publ)/Hexagon AB: ab, hexagon                                                                                                                         |
| A P Mollar-Maersk (AMKBY)                                                        | AMKBY       | embedded |          1 |                               1 | embedded ticker AMKBY; name words shared with A.P. Møller - Mærsk A/S/A.P. Moeller-Maersk A/S: maersk                                                                                                           |
| 3I Group PLC (TGOPY)                                                             | TGOPY       | embedded |          1 |                               1 | embedded ticker TGOPY; name words shared with 3i Group plc/3i Group: 3i                                                                                                                                         |
| Hermes International SCA ADR (HESAY)                                             | HESAY       | embedded |          1 |                               1 | embedded ticker HESAY; name words shared with Hermès International Société en commandite par actions/Hermes International SA: hermes                                                                            |
| Hennes & Mauritz AB ADR (HNNMY)                                                  | HNNMY       | embedded |          1 |                               1 | embedded ticker HNNMY; name words shared with H & M Hennes & Mauritz AB (publ)/Hennes & Mauritz AB: ab, hennes, mauritz                                                                                         |
| Tesco Stores Holdings (TSCDY)                                                    | TSCDY       | embedded |          1 |                               1 | embedded ticker TSCDY; name words shared with Tesco PLC/Tesco PLC: tesco                                                                                                                                        |
| Henkel AG & Company KGAA PFD Sponsored ADR (HENOY)                               | HENOY       | embedded |          1 |                               1 | embedded ticker HENOY; name words shared with Henkel AG & Co. KGaA/Henkel AG & Co. KGAA: henkel, kgaa                                                                                                           |
| Heidelbergcement AG ADR Sponsored (HDLMY)                                        | HDLMY       | embedded |          1 |                               1 | embedded ticker HDLMY; name words shared with Heidelberg Materials AG/HEIDELBERG MATERIALS AG: heidelberg                                                                                                       |
| Hannover Rueck SE Sponsored ADR (HVRRY)                                          | HVRRY       | embedded |          1 |                               1 | embedded ticker HVRRY; name words shared with Hannover Rück SE/Hannover Re: hannover                                                                                                                            |
| Halma plc Unsponsored ADR (HALMY)                                                | HALMY       | embedded |          1 |                               1 | embedded ticker HALMY; name words shared with Halma plc/Halma PLC: halma                                                                                                                                        |
| Haleon plc Sponsored ADR (HLN)                                                   | HLN         | embedded |          1 |                               1 | embedded ticker HLN; name words shared with Haleon plc/Haleon plc/Haleon plc: haleon                                                                                                                            |
| Glaxo Wellcome plc ADR (GSK)                                                     | GSK         | override |          1 |                               1 | J5 override 'glaxo wellcome' (yahoo)                                                                                                                                                                            |
| Givaudan SA ADR (GVDNY)                                                          | GVDNY       | embedded |          1 |                               1 | embedded ticker GVDNY; name words shared with Givaudan SA/Givaudan SA: givaudan                                                                                                                                 |
| Geberit AG ADR (GBERY)                                                           | GBERY       | embedded |          1 |                               1 | embedded ticker GBERY; name words shared with Geberit AG/Geberit AG: geberit                                                                                                                                    |
| Galderma Group AG Sponsored ADR (GALDY)                                          | GALDY       | embedded |          1 |                               1 | embedded ticker GALDY; name words shared with Galderma Group AG/GALDERMA GROUP AG/Galderma Group AG/ADR: galderma                                                                                               |
| Fujitsu Ltd ADR New Japan (FJTSY)                                                | FJTSY       | embedded |          1 |                               1 | embedded ticker FJTSY; name words shared with Fujitsu Limited/Fujitsu Ltd.: fujitsu                                                                                                                             |
| Fuji Film Holding Corporation ADR (FUJIY)                                        | FUJIY       | embedded |          1 |                               1 | embedded ticker FUJIY; name words shared with FUJIFILM Holdings Corporation/FUJIFILM Holdings Corp.: film, fuji, fujifilm                                                                                       |
| Fresenius SE & Company Sponsored ADR (FSNUY)                                     | FSNUY       | embedded |          1 |                               1 | embedded ticker FSNUY; name words shared with Fresenius SE & Co. KGaA/Fresenius SE & Co. KGaA/Fresenius SE & Co. KGaA: fresenius                                                                                |
| Fresenius Medical Care AG (FMS)                                                  | FMS         | embedded |          1 |                               1 | embedded ticker FMS; name words shared with Fresenius Medical Care AG/Fresenius Medical Care AG/Fresenius Medical Care AG: care, fresenius, medical                                                             |
| Fortescue Metals Group Ltd Sponsored ADR (FSUGY)                                 | FSUGY       | embedded |          1 |                               1 | embedded ticker FSUGY; name words shared with Fortescue Ltd/FORTESCUE LTD.: fortescue                                                                                                                           |
| Fast Retailing Co Ltd ADR (FRCOY)                                                | FRCOY       | embedded |          1 |                               1 | embedded ticker FRCOY; name words shared with Fast Retailing Co., Ltd./Fast Retailing Co. Ltd.: fast, retailing                                                                                                 |
| Fanuc Corporation ADR (FANUY)                                                    | FANUY       | embedded |          1 |                               1 | embedded ticker FANUY; name words shared with Fanuc Corporation/Fanuc Corporation: fanuc                                                                                                                        |
| Experian plc Sponsored ADR (EXPGY)                                               | EXPGY       | embedded |          1 |                               1 | embedded ticker EXPGY; name words shared with Experian plc/Experian plc: experian                                                                                                                               |
| Evolution AB Unsponsored ADR (EVVTY)                                             | EVVTY       | embedded |          1 |                               1 | embedded ticker EVVTY; name words shared with Evolution AB (publ)/Evolution AB: ab, evolution                                                                                                                   |
| Essilorluxottica ADR (ESLOY)                                                     | ESLOY       | embedded |          1 |                               1 | embedded ticker ESLOY; name words shared with EssilorLuxottica Société anonyme/EssilorLuxottica: essilorluxottica                                                                                               |
| Erste Group Bank AG Sponsored ADR (EBKDY)                                        | EBKDY       | embedded |          1 |                               1 | embedded ticker EBKDY; name words shared with Erste Group Bank AG/Erste Group Bank AG: bank, erste                                                                                                              |
| Ericsson - ADR (ERIC)                                                            | ERIC        | embedded |          1 |                               1 | embedded ticker ERIC; name words shared with Telefonaktiebolaget LM Ericsson (publ)/Ericsson/ERICSSON LM TELEPHONE CO: ericsson                                                                                 |
| Epiroc Aktiebolag Class A Sponsored ADR (EPOAY)                                  | EPOAY       | embedded |          1 |                               1 | embedded ticker EPOAY; name words shared with Epiroc AB (publ)/Epiroc Aktiebolag: aktiebolag, epiroc                                                                                                            |
| Eisai Co Ltd ADR (ESAIY)                                                         | ESAIY       | embedded |          1 |                               1 | embedded ticker ESAIY; name words shared with Eisai Co., Ltd./Eisai Co., Ltd.: eisai                                                                                                                            |
| Ebara Corporation ADR (EBCOY)                                                    | EBCOY       | embedded |          1 |                               1 | embedded ticker EBCOY; name words shared with Ebara Corporation/Ebara Corp.: ebara                                                                                                                              |
| DSM Firmenich AG Sponsored ADR (DSFIY)                                           | DSFIY       | embedded |          1 |                               1 | embedded ticker DSFIY; name words shared with DSM-Firmenich AG/DSM Firmenich AG: dsm, firmenich                                                                                                                 |
| Dr. Ing. h.c. F. Porsche AG Unsponsored ADR (DRPRY)                              | DRPRY       | embedded |          1 |                               1 | embedded ticker DRPRY; name words shared with Dr. Ing. h.c. F. Porsche AG/DR ING H C F PORSCHE AG: dr, ing, porsche                                                                                             |
| DNB BK ASA Sponsored ADR (DNBBY)                                                 | DNBBY       | embedded |          1 |                               1 | embedded ticker DNBBY; name words shared with DNB Bank ASA/DNB ASA: asa, dnb                                                                                                                                    |
| Disco Corporation Unsponsored ADR (DSCSY)                                        | DSCSY       | embedded |          1 |                               1 | embedded ticker DSCSY; name words shared with Disco Corporation/Disco Corp.: disco                                                                                                                              |
| Deutsche Telekom AG DE Sponsored ADR (DTEGY)                                     | DTEGY       | embedded |          1 |                               1 | embedded ticker DTEGY; name words shared with Deutsche Telekom AG/Deutsche Telekom AG/DEUTSCHE TELEKOM AG: deutsche, telekom                                                                                    |
| Deutsche Post AG Sponsored ADR (DHLGY)                                           | DHLGY       | embedded |          1 |                               1 | embedded ticker DHLGY; name words shared with DHL AG/Deutsche Post AG: deutsche, post                                                                                                                           |
| Deutsche Lufthansa AG Sponsored ADR (DLAKY)                                      | DLAKY       | embedded |          1 |                               1 | embedded ticker DLAKY; name words shared with Deutsche Lufthansa AG/Deutsche Lufthansa AG/DEUTSCHE LUFTHANSA A G /FI: deutsche, lufthansa                                                                       |
| Deutsche Boerse ADR (DBOEY)                                                      | DBOEY       | embedded |          1 |                               1 | embedded ticker DBOEY; name words shared with Deutsche Börse AG/Deutsche Boerse AG: boerse, deutsche                                                                                                            |
| Denso Corporation ADR (DNZOY)                                                    | DNZOY       | embedded |          1 |                               1 | embedded ticker DNZOY; name words shared with DENSO Corporation/Denso Corp.: denso                                                                                                                              |
| DBS Group Holdings Ltd Sponsored ADR (DBSDY)                                     | DBSDY       | embedded |          1 |                               1 | embedded ticker DBSDY; name words shared with DBS Group Holdings Ltd/DBS Group Holdings Ltd.: dbs                                                                                                               |
| Dassault Systems SA Sponsored ADR (DASTY)                                        | DASTY       | embedded |          1 |                               1 | embedded ticker DASTY; name words shared with Dassault Systèmes SE/Dassault Systemes SA: dassault                                                                                                               |
| Danske Bank A/S Sponsored ADR (DNKEY)                                            | DNKEY       | embedded |          1 |                               1 | embedded ticker DNKEY; name words shared with Danske Bank A/S/Danske Bank A/S: bank, danske                                                                                                                     |
| Danone Sponsored ADR (DANOY)                                                     | DANOY       | embedded |          1 |                               1 | embedded ticker DANOY; name words shared with Danone S.A./Danone: danone                                                                                                                                        |
| Daiwa House Industries Ltd ADR Japan (DWAHY)                                     | DWAHY       | embedded |          1 |                               1 | embedded ticker DWAHY; name words shared with Daiwa House Industry Co., Ltd./Daiwa House Industry Co. Ltd.: daiwa, house                                                                                        |
| Daito Trust Construction Sponsored ADR (DIFTY)                                   | DIFTY       | embedded |          1 |                               1 | embedded ticker DIFTY; name words shared with Daito Trust Construction Co.,Ltd./Daito Trust Construction Co.: construction, daito                                                                               |
| Daimler Truck Holding AG Sponsored ADR (DTRUY)                                   | DTRUY       | embedded |          1 |                               1 | embedded ticker DTRUY; name words shared with Daimler Truck Holding AG/DAIMLER TRUCK HLDG AG: daimler, truck                                                                                                    |
| Daikin Industries Ltd ADR (DKILY)                                                | DKILY       | embedded |          1 |                               1 | embedded ticker DKILY; name words shared with Daikin Industries,Ltd./Daikin Industries Ltd.: daikin, industries                                                                                                 |
| Daiichi Sankyo Co Ltd Sponsored ADR (DSNKY)                                      | DSNKY       | embedded |          1 |                               1 | embedded ticker DSNKY; name words shared with Daiichi Sankyo Company, Limited/Daiichi Sankyo Co., Ltd.: daiichi, sankyo                                                                                         |
| Daifuku Co Ltd ADR (DFKCY)                                                       | DFKCY       | embedded |          1 |                               1 | embedded ticker DFKCY; name words shared with Daifuku Co Ltd/Daifuku Co., Ltd.: daifuku                                                                                                                         |
| Daiichi Life Holdings Inc Unsponsored ADR (DLICY)                                | DLICY       | embedded |          1 |                               1 | embedded ticker DLICY; name words shared with Daiichi Life Group, Inc./DAIICHI LIFE GROUP INC.: daiichi, life                                                                                                   |
| CSL Ltd Sponsored ADR (CSLLY)                                                    | CSLLY       | embedded |          1 |                               1 | embedded ticker CSLLY; name words shared with CSL Limited/CSL Ltd./CSL LTD: csl                                                                                                                                 |
| Credit Agricole SA ADR (CRARY)                                                   | CRARY       | embedded |          1 |                               1 | embedded ticker CRARY; name words shared with Crédit Agricole S.A./Credit Agricole SA: agricole, credit                                                                                                         |
| Commonwealth Bank Australia Sponsored ADR (CMWAY)                                | CMWAY       | embedded |          1 |                               1 | embedded ticker CMWAY; name words shared with Commonwealth Bank of Australia/Commonwealth Bank of Australia: australia, bank, commonwealth                                                                      |
| Computershare Ltd Sponsored ADR (CMSQY)                                          | CMSQY       | embedded |          1 |                               1 | embedded ticker CMSQY; name words shared with Computershare Limited/Computershare Ltd.: computershare                                                                                                           |
| Compass Group plc Sponsored ADR (CMPGY)                                          | CMPGY       | embedded |          1 |                               1 | embedded ticker CMPGY; name words shared with Compass Group PLC/Compass Group Plc: compass                                                                                                                      |
| Roper Technologies, Inc. - Common Stock (ROP)                                    | ROP         | embedded |          1 |                               1 | embedded ticker ROP; name words shared with Roper Technologies, Inc./Roper Technologies, Inc./ROPER TECHNOLOGIES INC: roper, technologies                                                                       |
| Compagnie de Saint-Gobain ADR (CODYY)                                            | CODYY       | embedded |          1 |                               1 | embedded ticker CODYY; name words shared with Compagnie de Saint-Gobain S.A./Compagnie de Saint-Gobain: compagnie, gobain, saint                                                                                |
| Commerzbank AG Sponsored ADR (CRZBY)                                             | CRZBY       | embedded |          1 |                               1 | embedded ticker CRZBY; name words shared with Commerzbank AG/Commerzbank AG: commerzbank                                                                                                                        |
| Coloplast AS Sponsored ADR (CLPBY)                                               | CLPBY       | embedded |          1 |                               1 | embedded ticker CLPBY; name words shared with Coloplast A/S/Coloplast AS: coloplast                                                                                                                             |
| Cochlear Ltd ADR (CHEOY)                                                         | CHEOY       | embedded |          1 |                               1 | embedded ticker CHEOY; name words shared with Cochlear Limited/CochLear Ltd.: cochlear                                                                                                                          |
| Coca-Cola HBC AG ADR (CCHGY)                                                     | CCHGY       | embedded |          1 |                               1 | embedded ticker CCHGY; name words shared with Coca-Cola HBC AG/Coca-Cola HBC AG: coca, cola, hbc                                                                                                                |
| CK Hutchison Holdings Ltd Unsponsored ADR (CKHUY)                                | CKHUY       | embedded |          1 |                               1 | embedded ticker CKHUY; name words shared with CK Hutchison Holdings Limited/CK Hutchison Holdings LTD: ck, hutchison                                                                                            |
| Chugai Pharmaceutical Ltd DDR (CHGCY)                                            | CHGCY       | embedded |          1 |                               1 | embedded ticker CHGCY; name words shared with Chugai Pharmaceutical Co., Ltd./Chugai Pharmaceutical Co., Ltd.: chugai, pharmaceutical                                                                           |
| Central Japan RAI ADR (CJPRY)                                                    | CJPRY       | embedded |          1 |                               1 | embedded ticker CJPRY; name words shared with Central Japan Railway Company/Central Japan Railway Co.: central                                                                                                  |
| Cellnex Telecom SAU Unsponsored ADR (CLLNY)                                      | CLLNY       | embedded |          1 |                               1 | embedded ticker CLLNY; name words shared with Cellnex Telecom, S.A./Cellnex Telecom SA: cellnex, telecom                                                                                                        |
| Carlsberg AS Sponsored ADR (CABGY)                                               | CABGY       | embedded |          1 |                               1 | embedded ticker CABGY; name words shared with Carlsberg A/S/Carlsberg AS: carlsberg                                                                                                                             |
| Capgemini SE Unsponsored (CGEMY)                                                 | CGEMY       | embedded |          1 |                               1 | embedded ticker CGEMY; name words shared with Capgemini SE/Capgemini SE: capgemini                                                                                                                              |
| Capcom Co Ltd Unsponsored ADR (CCOEY)                                            | CCOEY       | embedded |          1 |                               1 | embedded ticker CCOEY; name words shared with Capcom Co., Ltd./Capcom Co. Ltd: capcom                                                                                                                           |
| Canon Inc ADR Japan Sponsored (CAJPY)                                            | CAJPY       | embedded |          1 |                               1 | embedded ticker CAJPY; name words shared with Canon Inc./Canon, Inc./CANON INC: canon                                                                                                                           |
| Caixabank Unsponsored ADR (CAIXY)                                                | CAIXY       | embedded |          1 |                               1 | embedded ticker CAIXY; name words shared with CaixaBank, S.A./Caixabank SA: caixabank                                                                                                                           |
| Bureau Veritas SA Unsponsored ADR (BVVBY)                                        | BVVBY       | embedded |          1 |                               1 | embedded ticker BVVBY; name words shared with Bureau Veritas SA/Bureau Veritas SA: bureau, veritas                                                                                                              |
| Bunzl plc New Sponsored ADR (BZLFY)                                              | BZLFY       | embedded |          1 |                               1 | embedded ticker BZLFY; name words shared with Bunzl plc/Bunzl plc/BUNZL PLC: bunzl                                                                                                                              |
| Bridgestone Corporation Ltd ADR Japan (BRDCY)                                    | BRDCY       | embedded |          1 |                               1 | embedded ticker BRDCY; name words shared with Bridgestone Corporation/Bridgestone Corp.: bridgestone                                                                                                            |
| Brenntag Se Unsponsored ADR (BNTGY)                                              | BNTGY       | embedded |          1 |                               1 | embedded ticker BNTGY; name words shared with Brenntag SE/Brenntag SE: brenntag                                                                                                                                 |
| Brambles Ltd Sponsored ADR (BXBLY)                                               | BXBLY       | embedded |          1 |                               1 | embedded ticker BXBLY; name words shared with Brambles Limited/Brambles, Ltd.: brambles                                                                                                                         |
| Bouygues SA ADR (BOUYY)                                                          | BOUYY       | embedded |          1 |                               1 | embedded ticker BOUYY; name words shared with Bouygues SA/Bouygues SA: bouygues                                                                                                                                 |
| Boliden AB AR (BDNNY)                                                            | BDNNY       | embedded |          1 |                               1 | embedded ticker BDNNY; name words shared with Boliden AB (publ)/Boliden AB: ab, boliden                                                                                                                         |
| Boc Hong Kong Holdings Ltd Sponsored ADR (BHKLY)                                 | BHKLY       | embedded |          1 |                               1 | embedded ticker BHKLY; name words shared with BOC Hong Kong (Holdings) Limited/BOC Hong Kong (Holdings) Ltd.: boc, hong, kong                                                                                   |
| BNP Paribas SA ADR (BNPQY)                                                       | BNPQY       | embedded |          1 |                               1 | embedded ticker BNPQY; name words shared with BNP Paribas SA/BNP Paribas: bnp, paribas                                                                                                                          |
| Bayerische Motors Werke AG ADR (BMWKY)                                           | BMWKY       | embedded |          1 |                               1 | embedded ticker BMWKY; name words shared with Bayerische Motoren Werke Aktiengesellschaft/Bayerische Motoren Werke AG/Bayerische Motoren Werke AG/ADR: bayerische, werke                                        |
| Bayer AG Sponsored ADR (BAYRY)                                                   | BAYRY       | embedded |          1 |                               1 | embedded ticker BAYRY; name words shared with Bayer Aktiengesellschaft/Bayer A.G.: bayer                                                                                                                        |
| BASF SE Sponsored ADR (BASFY)                                                    | BASFY       | embedded |          1 |                               1 | embedded ticker BASFY; name words shared with BASF SE/BASF SE: basf                                                                                                                                             |
| Barry Callebaut AG Unsponsored ADR (BRRLY)                                       | BRRLY       | embedded |          1 |                               1 | embedded ticker BRRLY; name words shared with Barry Callebaut AG/Barry Callebaut AG: barry, callebaut                                                                                                           |
| Barratt Redrow plc ADR (BTDPY)                                                   | BTDPY       | embedded |          1 |                               1 | embedded ticker BTDPY; name words shared with Barratt Redrow plc/BARRATT REDROW PLC/Barratt Developments PLC/ADR: barratt, redrow                                                                               |
| Barclays plc ADR (BCS)                                                           | BCS         | embedded |          1 |                               1 | embedded ticker BCS; name words shared with Barclays PLC/Barclays PLC/BARCLAYS PLC: barclays                                                                                                                    |
| Bankinter SA Sponsored ADR (BKNIY)                                               | BKNIY       | embedded |          1 |                               1 | embedded ticker BKNIY; name words shared with Bankinter, S.A./Bankinter, S.A.: bankinter                                                                                                                        |
| Bandai Namco Holdings Inc ADR (NCBDY)                                            | NCBDY       | embedded |          1 |                               1 | embedded ticker NCBDY; name words shared with BANDAI NAMCO Holdings Inc./Bandai Namco Holdings, Inc.: bandai, namco                                                                                             |
| BAE Systems plc Sponsored ADR (BAESY)                                            | BAESY       | embedded |          1 |                               1 | embedded ticker BAESY; name words shared with BAE Systems plc/BAE Systems PLC/BAE SYSTEMS PLC /FI/: bae, systems                                                                                                |
| AXA ADR (AXAHY)                                                                  | AXAHY       | embedded |          1 |                               1 | embedded ticker AXAHY; name words shared with AXA SA/AXA: axa                                                                                                                                                   |
| Avolta AG ADR (DUFRY)                                                            | DUFRY       | embedded |          1 |                               1 | embedded ticker DUFRY; name words shared with Avolta AG/AVOLTA AG: avolta                                                                                                                                       |
| Aviva plc ADR (AVVIY)                                                            | AVVIY       | embedded |          1 |                               1 | embedded ticker AVVIY; name words shared with Aviva plc/Aviva Plc: aviva                                                                                                                                        |
| Atlas Copco AB New Series B Sponsored ADR (ATLCY)                                | ATLCY       | embedded |          1 |                               1 | embedded ticker ATLCY; name words shared with Atlas Copco AB (publ)/Atlas Copco AB: ab, atlas, copco                                                                                                            |
| Atlas Copco AB New Shares Representing Series A Common Stock (Sponsored) (ATLKY) | ATLKY       | embedded |          1 |                               1 | embedded ticker ATLKY; name words shared with Atlas Copco AB (publ)/Atlas Copco AB: ab, atlas, copco                                                                                                            |
| ASX Ltd ADR (ASXFY)                                                              | ASXFY       | embedded |          1 |                               1 | embedded ticker ASXFY; name words shared with ASX Limited/ASX, Ltd.: asx                                                                                                                                        |
| Astellas Pharma Inc ADR (ALPMY)                                                  | ALPMY       | embedded |          1 |                               1 | embedded ticker ALPMY; name words shared with Astellas Pharma Inc./Astellas Pharma, Inc.: astellas, pharma                                                                                                      |
| Associated British Foods plc ADR (ASBFY)                                         | ASBFY       | embedded |          1 |                               1 | embedded ticker ASBFY; name words shared with Associated British Foods plc/Associated British Foods plc: associated, british, foods                                                                             |
| Assicurazioni Generali SpA ADR (ARZGY)                                           | ARZGY       | embedded |          1 |                               1 | embedded ticker ARZGY; name words shared with Assicurazioni Generali S.p.A./Assicurazioni Generali Spa: assicurazioni, generali                                                                                 |
| Assa Abloy AB ADR (ASAZY)                                                        | ASAZY       | embedded |          1 |                               1 | embedded ticker ASAZY; name words shared with ASSA ABLOY AB (publ)/Assa Abloy AB: ab, abloy, assa                                                                                                               |
| Asics Corp Unsponsored ADR (ASCCY)                                               | ASCCY       | embedded |          1 |                               1 | embedded ticker ASCCY; name words shared with ASICS Corporation/Asics Corp.: asics                                                                                                                              |
| Asahi Kaisei Corp Unsponsored ADR (AHKSY)                                        | AHKSY       | embedded |          1 |                               1 | embedded ticker AHKSY; name words shared with Asahi Kasei Corporation/Asahi Kaisei Corp.: asahi, kaisei                                                                                                         |
| ANZ Group Holdings LTD Sponsored ADR (ANZGY)                                     | ANZGY       | embedded |          1 |                               1 | embedded ticker ANZGY; name words shared with ANZ Group Holdings Limited/ANZ GROUP HLDGS LTD: anz                                                                                                               |
| Anglo American plc Sponsored ADR (NGLOY)                                         | NGLOY       | embedded |          1 |                               1 | embedded ticker NGLOY; name words shared with Anglo American plc/Anglo American plc: american, anglo                                                                                                            |
| Amadeus IT Group Unsponsored ADR (AMADY)                                         | AMADY       | embedded |          1 |                               1 | embedded ticker AMADY; name words shared with Amadeus IT Group, S.A./Amadeus IT Group SA: amadeus, it                                                                                                           |
| Alstom ADR (ALSMY)                                                               | ALSMY       | embedded |          1 |                               1 | embedded ticker ALSMY; name words shared with Alstom SA/Alstom: alstom                                                                                                                                          |
| Allianz SE ADR (ALIZY)                                                           | ALIZY       | embedded |          1 |                               1 | embedded ticker ALIZY; name words shared with Allianz SE/Allianz SE: allianz                                                                                                                                    |
| Loews Corporation (L)                                                            | L           | embedded |          1 |                               1 | embedded ticker L; name words shared with Loews Corporation/Loews Corporation/LOEWS CORP: loews                                                                                                                 |
| Alfa Laval AB Sweden ADR (ALFVY)                                                 | ALFVY       | embedded |          1 |                               1 | embedded ticker ALFVY; name words shared with Alfa Laval AB (publ)/Alfa-Laval AB: ab, alfa, laval                                                                                                               |
| Everpure, Inc. Class A (PSTG)                                                    | PSTG        | override |          1 |                               1 | J5 override '(pstg)' (yahoo)                                                                                                                                                                                    |
| Bank of New York Mellon Corp (BK)                                                | BK          | override |          1 |                               1 | J5 override '(bk)' (yahoo)                                                                                                                                                                                      |
| LVMH Moet Hennessy Louis ADR (LVMUY)                                             | LVMUY       | embedded |          1 |                               1 | embedded ticker LVMUY; name words shared with LVMH Moët Hennessy - Louis Vuitton, Société Européenne/LVMH-Moet Hennessy Louis Vuitto: hennessy, louis, lvmh, moet                                               |

Not recovered, Self/Joint in the default window (for Harry):

| asset_name                                                                                                                                                                                                     | asset_type   | candidate   |   n_trades_self_joint_in_window | note                                                                                                                                                                                                                                                                                               |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------|:------------|--------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| More Company: More (Ebene, Muritius (India)) Description: Grocery Chain                                                                                                                                        | Other        |             |                               2 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| BetterCloud Company: BetterCloud (New York, NY) Description: Cloud Storage                                                                                                                                     | Other        |             |                               2 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| PHLD - Phillips Edison Grocery Center REIT I                                                                                                                                                                   | Stock        | PHLD        |                               2 | embedded ticker PHLD not recognised by Yahoo; then no exact SEC name match                                                                                                                                                                                                                         |
| NationsBuilders Insurance Services, Inc. Company: NationsBuilders Insurance Services, Inc. (Atlanta, GA) Description: Insurance                                                                                | Other        |             |                               2 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| Pimco Commodities Plus Strategy Fund Class                                                                                                                                                                     | Stock        |             |                               2 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| BofA Finance LLC Trigger Autocallable Contingent Yield Notes Company: Bank of America Corporation (Charlotte, NC) Description: Equity Index-Linked Note                                                        | Other        |             |                               2 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| Canadian Imperial Bank of Commerce Trigger Autocallable Contingent Yield Notes Company: Canadian Imperial Bank of Commerce (Toronto, Ontario) Description: Equity Index-Linked Note                            | Other        |             |                               2 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| Empire Petroleum Partners LLC Company: Empire Petroleum Partners LLC (Gaithersburg, MD) Description: Energy Company                                                                                            | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| MSR-EB Waterfront Venture LLC (The Pointe at Stono Shores) Company: MSR-EB Waterfront Venture LLC (Charleston, SC) Description: Real Estate                                                                    | Other        | MSR         |                               1 | embedded ticker MSR but its name (Graniteshares Autocallable Mstr ETF/GraniteShares Autocallable MSTR) shares no word with 'EB Waterfront Venture LLC (The Pointe at Stono Shores) Company: MSR-EB Waterfront Venture LLC (Charleston, SC) Description: Real Estate'; then no exact SEC name match |
| Dyson Capital Series Fund, LLC Company: Dyson Capital Series Fund, LLC (Alexandria, VA) Description: Holding Company - Private Equity                                                                          | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| MOWI                                                                                                                                                                                                           | Stock        | MOWI        |                               1 | embedded ticker MOWI not recognised by Yahoo; then no exact SEC name match                                                                                                                                                                                                                         |
| Narya Capital Fund II, L.P. Company: Narya Capital Fund II, L.P. (Cincinnati, OH) Description: Venture capital fund                                                                                            | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| 445 Park Commons Company: 445 Park Commons (Nashville, TN) Description: Underlying commercial real estate asset owned by NSHD MSE Block C Joint Venture, LLC in Nashville, TN.                                 | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| NSHD MSE Block C Joint Venture, LLC Company: NSHD MSE Block C Joint Venture, LLC (Nashville, TN) Description: LLC interest for the purpose of investing in commercial real estate.                             | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| T-Mobile US, Inc. - Common Stock                                                                                                                                                                               | Stock        | T           |                               1 | embedded ticker T but its name (AT&T Inc./AT&T Inc./AT&T INC.) shares no word with 'Mobile US, Inc. - Common Stock'; then SEC company CIK 1283699 has several tickers: TMUS, TMUSI, TMUSL, TMUSZ                                                                                                   |
| euNetworks Group Limited Company: euNetworks Group Limited (London, England) Description: Bandwidth infrastructure services                                                                                    | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| Nestle ADR                                                                                                                                                                                                     | Stock        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| Invesco Actively Managed Exchange Traded                                                                                                                                                                       | Stock        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| VANGUARD INDEX FDS VANGUARD MID-CAP ETF                                                                                                                                                                        | Stock        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| DM                                                                                                                                                                                                             | Stock        | DM          |                               1 | embedded ticker DM not recognised by Yahoo; then no exact SEC name match                                                                                                                                                                                                                           |
| JP Morgan Chase Financial Company LLC Trigger Autocallable Contingent Yield Notes Company: JP Morgan Chase Financial Company LLC (New York, NY) Description: Structured Note                                   | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| US Treasury Bill (912797NX1) MATURED                                                                                                                                                                           | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| US Treasury Bill 25U DUE 10/16/25                                                                                                                                                                              | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| US Treasury Bill26U S T Bill Due 1/1/26                                                                                                                                                                        | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| GS Finance Corp. Trigger Autocallable Contingent Yield Note Company: GS Finance Corp. (New York, NY) Description: Equity Index-Linked Note                                                                     | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| US TREASURY BILL26U T Bill due 4/2/26                                                                                                                                                                          | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| US TREASURY Bill26U Bill Due 04/02.26                                                                                                                                                                          | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| West Deptford Energy Holdings, LLC Company: West Deptford Energy Holdings, LLC (New York, NY) Description: Energy Company                                                                                      | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| Contour Venture Partners V, LP Company: Contour Venture Partners V, LP (Princeton, NJ) Description: Limited partnership for the purpose of making early stage equity investments.                              | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| Hall Ward Energy Fund II, LP Company: Hall Ward Energy Fund II, LP (Oklahoma City, OK) Description: Limited Partnership with the purpose of investing in non-operating working interests in oil and gas wells. | Other        |             |                               1 | no exact SEC name match                                                                                                                                                                                                                                                                            |
| Kyocera Corporation ADR Japan (KYOCY)                                                                                                                                                                          | Stock        | KYOCY       |                               1 | J5 override '(kyocy)' (NOT confirmed); then embedded ticker KYOCY not recognised by Yahoo; then SEC company CIK 57083 has several tickers: KYOAY, KYOCF                                                                                                                                            |
| Hologic, Inc. (HOLX)                                                                                                                                                                                           | Stock        | HOLX        |                               1 | J5 override '(holx)' (NOT confirmed); then embedded ticker HOLX not recognised by Yahoo; then no exact SEC name match                                                                                                                                                                              |

Excluded by Yahoo classification (in-window trades):

| reason_code      | ticker   |   trades | yahoo_name                                          | exchange   | efd_name                                                                              |
|:-----------------|:---------|---------:|:----------------------------------------------------|:-----------|:--------------------------------------------------------------------------------------|
| MUTUAL_FUND      | ABNFX    |        2 | American Funds Bond Fund of Amer F-2                | Nasdaq     | The Bond Fd of America Class F-2 Shares                                               |
| MUTUAL_FUND      | ABQCX    |        1 | AB Bond Fund, Inc. - AB Total Return Bond Portfolio | Nasdaq     | Ab Bond Fund Inc. - Ab Total Return Bond Portfo                                       |
| MUTUAL_FUND      | ABYIX    |        3 | Abbey Capital Futures Strategy I                    | Nasdaq     | Abbey Capital Futures Strategy Fund- Class I Sha                                      |
| MUTUAL_FUND      | CFSSX    |        1 | Column Small Cap Select                             | Nasdaq     | Column Small Cap Select Fund                                                          |
| MUTUAL_FUND      | DALCX    |        1 | Dean Mid Cap Value                                  | Nasdaq     | Dean Mid Cap Value Fund No-Load                                                       |
| MUTUAL_FUND      | DBLEX    |        1 | DoubleLine Emerging Markets Fixed Inc I             | Nasdaq     | DoubleLine Emerging Markets Fixed Income Fund - Class I                               |
| MUTUAL_FUND      | EIBLX    |        1 | Eaton Vance Floating Rate I                         | Nasdaq     | Eaton Vance Floating Rate Fund Insti Share Company: EATON VANCE FLOATING RATE CLASS I |
| MUTUAL_FUND      | EMRZX    |        3 | VanEck Emerging Markets Z                           | Nasdaq     | Emerging Markets Fund Class Z                                                         |
| MUTUAL_FUND      | FCPIX    |        6 | Fidelity Advisor Intl Cap App I                     | Nasdaq     | Fidelity Advisor International Capital Appreciat                                      |
| MUTUAL_FUND      | FGSCX    |        1 | Federated Hermes MDT Mid Cap Growth C               | Nasdaq     | Federated Mdt Mid Cap Growth Fund - C Shares                                          |
| MUTUAL_FUND      | FIASX    |        1 | Fidelity Advisor Intl Small Cap A                   | Nasdaq     | Fidelity Advisor International Small Cap Class A                                      |
| MUTUAL_FUND      | FIMKX    |        7 | Fidelity Advisor Focused Em Mkts I                  | Nasdaq     | Fidelity Advisor Emerging Markets Fund                                                |
| MUTUAL_FUND      | FTBFX    |        1 | Fidelity Total Bond Fund                            | Nasdaq     | Fidelity Total Bond                                                                   |
| MUTUAL_FUND      | GEMIX    |        2 | Goldman Sachs Emerging Markets Eq Instl             | Nasdaq     | Goldman Sachs Emerging Markets Equity Fund Insti                                      |
| MUTUAL_FUND      | GICIX    |        1 | Goldman Sachs Intl Sm Cp Insghts Instl              | Nasdaq     | Goldman Sachs Intl Small Cap Insights Fd Inst                                         |
| MUTUAL_FUND      | GSIMX    |        1 | Goldman Sachs GQG Ptnrs Intl Opps Instl             | Nasdaq     | Goldman Sachs Gqg Partners International Opportu                                      |
| MUTUAL_FUND      | GSMYX    |        4 | Goldman Sachs Small/Mid Cap Growth Instl            | Nasdaq     | Goldman Sachs Small/Mid-Cap Growth Fund Inst Cl                                       |
| MUTUAL_FUND      | JHCBX    |        1 | JHancock Bond C                                     | Nasdaq     | John Hancock Bond Fund Cl C                                                           |
| MUTUAL_FUND      | LUBFX    |        1 | Lord Abbett Ultra Short Bond F                      | Nasdaq     | Lord Abbett Ultra Short Bond Fund - Class F                                           |
| MUTUAL_FUND      | LUBYX    |        4 | Lord Abbett Ultra Short Bond I                      | Nasdaq     | Lord Abbett Ultra Short Bond Fund - Class I                                           |
| MUTUAL_FUND      | MBXIX    |        3 | Catalyst/Millburn Hedge Strategy I                  | Nasdaq     | Catalyst/Millburn Hedge Strategy Fund Class I                                         |
| MUTUAL_FUND      | NMVZX    |        2 | Nuance Mid Cap Value Z                              | Nasdaq     | Nuance Mid Cap Value Fund Z Class                                                     |
| MUTUAL_FUND      | PCLPX    |        2 | PIMCO CommoditiesPLUS and Bond Alp I-2              | Nasdaq     | Pimco Commoditiesplus Strategy Fund Class I-2                                         |
| MUTUAL_FUND      | PCNNX    |        1 | PIMCO Investment Grade Credit Bond I-3              | Nasdaq     | Pimco Investment Grade Credit Bond Fund Class I-                                      |
| MUTUAL_FUND      | PONCX    |        1 | PIMCO Income C                                      | Nasdaq     | Pimco Income Fund Class C                                                             |
| MUTUAL_FUND      | RNWGX    |        6 | American Funds New World R-6                        | Nasdaq     | New World Fund Inc. Cl R-6                                                            |
| MUTUAL_FUND      | SBPYX    |        2 | ClearBridge Small Cap Growth I                      | Nasdaq     | Clearbridge Small Cap Growth Fd Cl I                                                  |
| MUTUAL_FUND      | VWUAX    |        1 | Vanguard US Growth Admiral                          | Nasdaq     | Vanguard U.S. Growth Fund Admiral Shares                                              |
| MUTUAL_FUND      | VWUSX    |        1 | Vanguard US Growth Investor                         | Nasdaq     | Vanguard U.S. Growth Fund                                                             |
| MUTUAL_FUND      | WWSYX    |        3 | Westwood Quality SmallCap Fund Ultra                | Nasdaq     | Westwood Quality Smallcap Fund - Ultra Shares                                         |
| OTHER_INSTRUMENT | KH       |        1 |                                                     | NYSE       | KH                                                                                    |

Tickers Yahoo does not resolve, or whose Yahoo name matches no eFD name for the ticker (recycled or renamed symbol): **173** tickers, 87 in-scope trades. Kept and flagged `instrument_unresolved`; Phase 3 resolves renames and delistings.

| ticker   |   n_in_scope | first_trade_date   | last_trade_date   | yahoo_name_mismatch   | yahoo_name                                  | efd_asset_names                                                                                                                                                                 |
|:---------|-------------:|:-------------------|:------------------|:----------------------|:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0QZI.IL  |            0 | 2019-09-25         | 2019-09-25        | True                  | Meta Platforms, Inc.                        | FACEBOOK INC FACEBOOK CLASS A                                                                                                                                                   |
| 3V64.TI  |            0 | 2019-09-25         | 2019-09-25        | False                 |                                             | VISA - CLASSE A                                                                                                                                                                 |
| ABB      |            0 | 2019-07-18         | 2019-07-18        | False                 |                                             | ABB Ltd                                                                                                                                                                         |
| AGN      |            0 | 2016-09-13         | 2020-04-14        | False                 |                                             | Allergan plc                                                                                                                                                                    |
| AGU      |            0 | 2017-04-04         | 2017-04-04        | False                 |                                             | Agrium Inc.                                                                                                                                                                     |
| AHL-C    |            1 | 2025-01-02         | 2025-01-02        | False                 |                                             | Aspen Insurance Holdings Ltd [Ahl/Pc]                                                                                                                                           |
| AJRD     |            0 | 2020-11-20         | 2021-01-08        | False                 |                                             | Aerojet Rocketdyne Holdings, Inc.                                                                                                                                               |
| AL       |            0 | 2018-04-24         | 2018-04-24        | False                 |                                             | Air Lease Corporation                                                                                                                                                           |
| ALTM     |            0 | 2024-03-21         | 2024-03-21        | False                 |                                             | Arcadium Lithium Plc                                                                                                                                                            |
| AMWD     |            0 | 2020-08-24         | 2020-08-27        | False                 |                                             | American Woodmark Corporation                                                                                                                                                   |
| ANDX     |            0 | 2017-11-29         | 2018-09-14        | False                 |                                             | Andeavor Logistics LP                                                                                                                                                           |
| AQFH     |            0 | 2017-02-01         | 2017-02-03        | False                 |                                             | Aquesta Financial Holdings, Inc.                                                                                                                                                |
| ARNA     |            0 | 2020-02-05         | 2020-11-20        | False                 |                                             | Arena Pharmaceuticals, Inc.                                                                                                                                                     |
| ATVI     |            2 | 2019-03-11         | 2023-04-26        | False                 |                                             | Activision Blizzard, Inc. | Activision Blizzard, Inc - Common Stock                                                                                                             |
| AVP      |            0 | 2017-11-21         | 2019-05-23        | False                 |                                             | Avon Products, Inc.                                                                                                                                                             |
| AY       |            0 | 2020-07-09         | 2024-12-13        | False                 |                                             | Atlantica Sustainable Infrastructure plc | Atlantica Sustainable Infrastructure plc - Ordinar | Atlantica Yield Plc                                                             |
| BBL      |            0 | 2017-12-21         | 2017-12-21        | False                 |                                             | BHP Billiton plc                                                                                                                                                                |
| BCR      |            0 | 2017-04-24         | 2017-05-12        | False                 |                                             | C. R. Bard, Inc.                                                                                                                                                                |
| BERY     |            0 | 2020-05-07         | 2020-06-02        | False                 |                                             | Berry Global Group, Inc.                                                                                                                                                        |
| BIVV     |            0 | 2017-05-24         | 2017-05-24        | False                 |                                             | Bioverativ Inc.                                                                                                                                                                 |
| BKEP     |            1 | 2021-12-29         | 2021-12-29        | False                 |                                             | Blueknight Energy Partners L.P., L.L.C. - Common U                                                                                                                              |
| BKEPP    |            1 | 2022-08-19         | 2022-08-19        | False                 |                                             | Blueknight Energy Partners L.P. - Series A Preferr                                                                                                                              |
| BPL      |            0 | 2016-12-13         | 2019-09-18        | False                 |                                             | Buckeye Partners, L.P.                                                                                                                                                          |
| BRK      |            1 | 2025-02-13         | 2025-02-13        | False                 |                                             | Bershire Hathaway Cdr [Cad Hedged]                                                                                                                                              |
| BRKB     |            0 | 2017-03-02         | 2018-12-06        | False                 |                                             | Berkshire Hathaway Inc.                                                                                                                                                         |
| BSCP     |            1 | 2025-12-17         | 2025-12-17        | False                 |                                             | Invesco BulletShares 2025 Corporate Bond ETF                                                                                                                                    |
| CAB      |            0 | 2016-10-06         | 2016-11-15        | False                 |                                             | Cabela's Incorporated                                                                                                                                                           |
| CBS      |            0 | 2018-01-18         | 2019-11-12        | False                 |                                             | CBS Corporation                                                                                                                                                                 |
| CCCS     |            0 | 2023-04-28         | 2023-04-28        | False                 |                                             | CCC Intelligent Solutions Holdings Inc. Common Sto                                                                                                                              |
| CELG     |            0 | 2015-07-02         | 2019-10-01        | False                 |                                             | Celgene Corporation | Celgene Corporation (NASDAQ)                                                                                                                              |
| CEM      |            0 | 2021-12-21         | 2021-12-21        | False                 |                                             | ClearBridge MLP and Midstream Fund Inc. Common Sto                                                                                                                              |
| CEQP     |            0 | 2019-05-28         | 2020-04-07        | False                 |                                             | Crestwood Equity Partners LP                                                                                                                                                    |
| CERN     |            0 | 2016-12-01         | 2018-02-27        | False                 |                                             | Cerner Corporation                                                                                                                                                              |
| CGNT     |            0 | 2018-03-29         | 2018-04-12        | True                  | Cognyte Software Ltd.                       | Cogentix Medical, Inc.                                                                                                                                                          |
| CLR      |            0 | 2018-05-03         | 2019-04-16        | False                 |                                             | Continental Resources, Inc.                                                                                                                                                     |
| CMA      |            0 | 2017-03-16         | 2017-06-15        | False                 |                                             | Comerica Incorporated                                                                                                                                                           |
| CNR      |            0 | 2021-03-29         | 2021-03-29        | True                  | Core Natural Resources, Inc.                | Cornerstone Building Brands, Inc.                                                                                                                                               |
| COLPAL   |            2 | 2025-04-08         | 2025-10-09        | False                 |                                             | COLGATE PALMOLIVE LTD.                                                                                                                                                          |
| CONE     |            0 | 2020-08-21         | 2021-11-26        | False                 |                                             | CyrusOne Inc. | CyrusOne Inc - Common Stock                                                                                                                                     |
| COUP     |            0 | 2020-06-17         | 2022-11-11        | False                 |                                             | Coupa Software Incorporated | Coupa Software Incorporated - Common Stock                                                                                                        |
| CSII     |            0 | 2023-04-05         | 2023-04-05        | False                 |                                             | Cardiovascular Systems, Inc. - Common Stock                                                                                                                                     |
| CTAA     |            0 | 2021-02-16         | 2021-02-16        | True                  | ClearThink 1 Acquisition Corp.              | Qwest Corp. NT 7% 2056                                                                                                                                                          |
| CTECBX   |            0 | 2020-05-04         | 2020-05-04        | False                 |                                             | CTECBX Company: Guggenheim Investments (Chicago, IL) Description: Guggenheim Investments is the global asset management and investment advisory division of Guggenheim Partners |
| CTXS     |            0 | 2020-02-14         | 2020-04-07        | False                 |                                             | Citrix Systems, Inc.                                                                                                                                                            |
| CUTR     |            0 | 2018-01-16         | 2018-08-30        | False                 |                                             | Cutera, Inc.                                                                                                                                                                    |
| CVET     |            0 | 2019-08-15         | 2019-08-15        | False                 |                                             | Covetrus, Inc.                                                                                                                                                                  |
| CYBR     |            2 | 2024-01-04         | 2024-12-18        | False                 |                                             | CyberArk Software Ltd. - Ordinary Shares                                                                                                                                        |
| DCP      |            0 | 2019-09-19         | 2020-02-19        | False                 |                                             | DCP Midstream, LP                                                                                                                                                               |
| DFS      |            0 | 2018-05-03         | 2020-04-14        | False                 |                                             | Discover Financial Services                                                                                                                                                     |
| DISH     |            0 | 2017-02-10         | 2017-12-05        | False                 |                                             | DISH Network Corporation | DISH-DISH Network Corporation                                                                                                                        |
| DNKN     |            0 | 2017-03-16         | 2020-12-16        | False                 |                                             | Dunkin' Brands Group, Inc.                                                                                                                                                      |
| DPM      |            0 | 2016-11-09         | 2016-11-09        | False                 |                                             | DCP Midstream Partners LP                                                                                                                                                       |
| DVMT     |            0 | 2016-12-14         | 2017-08-23        | False                 |                                             | Dell Technologies Inc.                                                                                                                                                          |
| ECOM     |            6 | 2021-02-10         | 2022-09-07        | False                 |                                             | ChannelAdvisor Corporation Common Stock | ChannelAdvisor Corporation                                                                                                            |
| ENTL     |            0 | 2018-01-05         | 2018-01-05        | True                  | Leverage Shares 2X Long ENTG Daily ETF      | Entellus Medical, Inc.                                                                                                                                                          |
| EQC      |            1 | 2024-12-13         | 2024-12-13        | False                 |                                             | Equity Commonwealth                                                                                                                                                             |
| EQM      |            0 | 2018-03-15         | 2020-04-14        | False                 |                                             | EQT Midstream Partners, LP | EQM Midstream Partners, LP                                                                                                                         |
| ESRX     |            0 | 2016-12-16         | 2017-03-15        | False                 |                                             | Express Scripts Holding Company                                                                                                                                                 |
| ESV      |            0 | 2015-02-24         | 2015-02-24        | False                 |                                             | Ensco plc (NYSE)                                                                                                                                                                |
| ETP      |            0 | 2016-09-15         | 2016-12-12        | False                 |                                             | Energy Transfer Partners, L.P.                                                                                                                                                  |
| ETRN     |            0 | 2024-01-17         | 2024-03-11        | False                 |                                             | Equitrans Midstream Corp                                                                                                                                                        |
| EV       |            0 | 2016-10-31         | 2018-04-24        | False                 |                                             | Eaton Vance Corp.                                                                                                                                                               |
| EVOP     |            0 | 2020-11-20         | 2021-01-25        | False                 |                                             | EVO Payments, Inc.                                                                                                                                                              |
| FDC      |            0 | 2017-06-02         | 2019-04-15        | False                 |                                             | First Data Corporation                                                                                                                                                          |
| FEYE     |            0 | 2016-08-05         | 2021-01-11        | False                 |                                             | FireEye, Inc.                                                                                                                                                                   |
| FL       |            0 | 2017-03-16         | 2017-03-16        | False                 |                                             | Foot Locker, Inc.                                                                                                                                                               |
| FPL      |            0 | 2020-04-02         | 2020-04-02        | False                 |                                             | First Trust New Opportunities MLP & Energy Fund                                                                                                                                 |
| FUN      |            1 | 2022-01-13         | 2022-01-13        | True                  | Six Flags Entertainment Corporation         | Cedar Fair, L.P. Common Stock                                                                                                                                                   |
| GAN      |            0 | 2021-04-13         | 2021-04-13        | False                 |                                             | GAN Limited                                                                                                                                                                     |
| GOGL     |            2 | 2024-02-27         | 2024-04-30        | True                  | Corgi GOOGL 2x Daily ETF                    | Golden Ocean Group Limited - Common Stock                                                                                                                                       |
| GRUB     |            0 | 2020-04-06         | 2020-04-06        | False                 |                                             | Grubhub Inc.                                                                                                                                                                    |
| HBI      |            0 | 2017-04-20         | 2020-11-20        | False                 |                                             | Hanesbrands Inc.                                                                                                                                                                |
| HDS      |            0 | 2016-11-15         | 2016-11-15        | False                 |                                             | HD Supply Holdings, Inc.                                                                                                                                                        |
| HES      |            1 | 2024-03-28         | 2024-03-28        | False                 |                                             | Hess Corp                                                                                                                                                                       |
| HOLX     |            0 | 2016-12-01         | 2023-01-11        | False                 |                                             | Hologic, Inc. | Hologic, Inc. - Common Stock                                                                                                                                    |
| HYH      |            0 | 2016-08-22         | 2016-08-23        | False                 |                                             | Halyard Health, Inc.                                                                                                                                                            |
| IBDO     |            1 | 2022-06-30         | 2022-06-30        | False                 |                                             | iShares iBonds Dec 2023 Term Corporate ETF                                                                                                                                      |
| IBDQ     |            2 | 2022-06-30         | 2025-12-18        | False                 |                                             | iShares iBonds Dec 2025 Term Corporate ETF | Dec 2025 Term Corp Ishares Ibonds ETF                                                                                              |
| IBKC     |            0 | 2015-05-06         | 2015-05-07        | False                 |                                             | IberiaBank Corp. (NASDAQ)                                                                                                                                                       |
| IIN      |            0 | 2018-07-26         | 2018-07-26        | False                 |                                             | IntriCon Corporation                                                                                                                                                            |
| INST     |            1 | 2023-01-03         | 2024-01-04        | False                 |                                             | Instructure Holdings, Inc. Common Stock | Instructure Holdings Inc                                                                                                              |
| IPHI     |            0 | 2020-02-24         | 2020-04-07        | False                 |                                             | Inphi Corporation                                                                                                                                                               |
| IRBT     |            0 | 2020-04-06         | 2025-02-06        | False                 |                                             | iRobot Corporation | iRobot Corporation - Common Stock                                                                                                                          |
| JNPR     |            0 | 2021-06-07         | 2021-06-07        | False                 |                                             | Juniper Networks, Inc.                                                                                                                                                          |
| JWN      |            0 | 2016-11-14         | 2016-11-14        | False                 |                                             | Nordstrom, Inc.                                                                                                                                                                 |
| K        |            0 | 2017-09-27         | 2025-12-11        | False                 |                                             | Kellogg Company | Kellanova                                                                                                                                                     |
| KL       |            0 | 2020-02-04         | 2020-02-04        | False                 |                                             | Kirkland Lake Gold Ltd.                                                                                                                                                         |
| LAZR     |            0 | 2025-06-26         | 2025-12-24        | True                  | Tema Photonics & Optical ETF                | Luminar Technologies Inc                                                                                                                                                        |
| LGF-B    |            0 | 2018-11-09         | 2020-04-14        | False                 |                                             | Lions Gate Entertainment Corp.                                                                                                                                                  |
| LLTC     |            0 | 2017-03-14         | 2017-03-14        | False                 |                                             | Linear Technology Corporation                                                                                                                                                   |
| LM09.SG  |            0 | 2018-12-06         | 2018-12-19        | False                 |                                             | Liberty Media Corp. Reg.Sh.C FO                                                                                                                                                 |
| LMACU    |            0 | 2021-01-22         | 2021-01-22        | False                 |                                             | Liberty Media Acquisition Corporation                                                                                                                                           |
| LMRK     |            0 | 2020-07-09         | 2021-08-23        | False                 |                                             | Landmark Infrastructure Partners LP | Landmark Infrastructure Partners LP - Common Units                                                                                        |
| LMST     |            2 | 2022-03-30         | 2023-04-03        | False                 |                                             | Limestone Bancorp, Inc. - Common Stock                                                                                                                                          |
| LSXMK    |            0 | 2021-03-15         | 2024-09-06        | False                 |                                             | Liberty Media Corporation - Series C Liberty Siriu                                                                                                                              |
| LTRPA    |            0 | 2023-03-20         | 2023-03-20        | False                 |                                             | Liberty TripAdvisor Holdings, Inc. - Series A Comm                                                                                                                              |
| MANT     |            0 | 2020-07-09         | 2021-06-04        | False                 |                                             | ManTech International Corporation                                                                                                                                               |
| MASI     |            2 | 2022-03-30         | 2022-10-05        | False                 |                                             | Masimo Corporation - Common Stock                                                                                                                                               |
| MAXR     |            0 | 2020-11-20         | 2023-01-04        | False                 |                                             | Maxar Technologies Inc | Maxar Technologies Inc.                                                                                                                                |
| MCC      |            0 | 2017-06-27         | 2017-06-27        | False                 |                                             | Medley Capital Corporation                                                                                                                                                      |
| MDC      |            0 | 2017-06-15         | 2017-06-15        | False                 |                                             | M.D.C. Holdings, Inc.                                                                                                                                                           |
| MMP      |            0 | 2018-09-24         | 2020-04-15        | False                 |                                             | Magellan Midstream Partners, L.P.                                                                                                                                               |
| MRO      |            0 | 2023-01-24         | 2023-01-24        | False                 |                                             | Marathon Oil Corp                                                                                                                                                               |
| MSTY.PA  |            0 | 2018-10-29         | 2018-10-30        | True                  | Yieldmax MSTR Option Income Strategy ETC    | Mainstay Medical International plc                                                                                                                                              |
| MXIM     |            0 | 2017-03-16         | 2017-06-15        | False                 |                                             | Maxim Integrated Products, Inc.                                                                                                                                                 |
| MYL      |            0 | 2017-09-27         | 2019-07-15        | False                 |                                             | Mylan N.V.                                                                                                                                                                      |
| NFX      |            0 | 2017-06-26         | 2017-06-26        | True                  | Corgi NFLX 2x Daily ETF                     | Newfield Exploration Company                                                                                                                                                    |
| NID      |            0 | 2022-10-04         | 2022-10-04        | False                 |                                             | Nuveen Intermediate Duration Municipal Term Fund C                                                                                                                              |
| NKLA     |            0 | 2020-07-09         | 2020-07-20        | False                 |                                             | Nikola Corporation                                                                                                                                                              |
| NPSND    |            0 | 2017-09-08         | 2017-09-08        | False                 |                                             | Naspers Limited                                                                                                                                                                 |
| NS       |            1 | 2021-12-29         | 2021-12-29        | False                 |                                             | Nustar Energy L.P. Common Units                                                                                                                                                 |
| NTRP     |            0 | 2018-02-15         | 2018-02-15        | True                  | NextTrip, Inc.                              | Neurotrope, Inc.                                                                                                                                                                |
| NUAN     |            0 | 2020-11-20         | 2021-04-13        | False                 |                                             | Nuance Communications, Inc.                                                                                                                                                     |
| OKS      |            0 | 2016-12-14         | 2016-12-14        | False                 |                                             | ONEOK Partners, L.P.                                                                                                                                                            |
| PARA     |            4 | 2023-09-18         | 2024-05-10        | True                  | Banzai International, Inc.                  | Paramount Global - Class B Common Stock | Paramount Global Cl B                                                                                                                 |
| PDRDY    |            0 | 2017-09-08         | 2019-03-11        | False                 |                                             | Pernod Ricard SA                                                                                                                                                                |
| PHLD     |            0 | 2017-08-03         | 2017-08-03        | False                 |                                             | PHILLIPS EDISON GR                                                                                                                                                              |
| POT      |            0 | 2017-05-09         | 2017-05-09        | False                 |                                             | Potash Corporation of Saskatchewan Inc.                                                                                                                                         |
| PSXP     |            0 | 2020-02-21         | 2020-04-15        | False                 |                                             | Phillips 66 Partners LP                                                                                                                                                         |
| PX       |            0 | 2016-10-31         | 2018-04-24        | False                 |                                             | Praxair, Inc. | Praxair Inc.                                                                                                                                                    |
| PXD      |            2 | 2023-01-10         | 2023-08-22        | False                 |                                             | Pioneer Natural Resources Company Common Stock | Pioneer Natural Resources Company                                                                                              |
| QRTEA    |            0 | 2021-05-10         | 2021-05-10        | False                 |                                             | Qurate Retail, Inc. | Qurate Retail, Inc. - Series A Common Stock                                                                                                               |
| QRTEP    |            0 | 2021-03-26         | 2021-03-26        | False                 |                                             | Qurate Retail, Inc.                                                                                                                                                             |
| RAI      |            0 | 2016-11-17         | 2017-06-15        | False                 |                                             | Reynolds American Inc.                                                                                                                                                          |
| RDS-A    |            0 | 2018-01-04         | 2018-01-04        | False                 |                                             | Royal Dutch Shell plc                                                                                                                                                           |
| RDS-B    |            0 | 2017-09-08         | 2020-08-21        | False                 |                                             | Royal Dutch Shell plc                                                                                                                                                           |
| RDSA     |            0 | 2021-07-26         | 2021-07-26        | False                 |                                             | Royal Dutch Shell Plc                                                                                                                                                           |
| RDSA.AS  |            0 | 2019-06-10         | 2019-06-10        | False                 |                                             | Royal Dutch Shell plc                                                                                                                                                           |
| REVB     |            0 | 2017-11-15         | 2019-07-31        | True                  | Revelation Biosciences, Inc.                | Revere Bank                                                                                                                                                                     |
| RGC      |            0 | 2017-03-28         | 2017-12-08        | True                  | Regencell Bioscience Holdings Limited       | Regal Entertainment Group                                                                                                                                                       |
| RHT      |            0 | 2016-08-01         | 2019-05-17        | False                 |                                             | Red Hat, Inc.                                                                                                                                                                   |
| RNWK     |            1 | 2022-12-28         | 2022-12-28        | False                 |                                             | RealNetworks, Inc. - Common Stock                                                                                                                                               |
| RSPP     |            0 | 2017-06-26         | 2017-11-13        | False                 |                                             | RSP Permian, Inc.                                                                                                                                                               |
| RTN      |            0 | 2017-03-16         | 2020-04-02        | False                 |                                             | Raytheon Company                                                                                                                                                                |
| RVNC     |            0 | 2023-10-04         | 2023-10-04        | False                 |                                             | Revance Therapeutics, Inc. - Common Stock                                                                                                                                       |
| RYT      |            0 | 2018-03-09         | 2018-03-09        | False                 |                                             | Guggenheim S&P 500 Eq Wt Technology ETF                                                                                                                                         |
| SAND     |            0 | 2023-01-11         | 2023-01-11        | False                 |                                             | Sandstorm Gold Ltd. Ordinary Shares (Canada)                                                                                                                                    |
| SCG      |            0 | 2017-08-22         | 2017-08-22        | False                 |                                             | SCANA Corporation                                                                                                                                                               |
| SHLX     |            0 | 2018-02-05         | 2020-04-15        | False                 |                                             | Shell Midstream Partners, L.P.                                                                                                                                                  |
| SI       |            0 | 2020-11-20         | 2022-01-31        | True                  | Shoulder Innovations, Inc.                  | Silvergate Capital Corporation | Silvergate Capital Corporation Class A Common Stoc                                                                                             |
| SIVB     |            1 | 2021-03-29         | 2022-03-30        | False                 |                                             | SVB Financial Group | SVB Financial Group - Common Stock                                                                                                                        |
| SQ       |            2 | 2018-12-28         | 2023-09-20        | False                 |                                             | Square, Inc. | Block, Inc. Class A Common Stock, | Square, Inc. Class A Common Stock                                                                                            |
| SRCL     |            0 | 2016-12-01         | 2016-12-01        | False                 |                                             | Stericycle, Inc.                                                                                                                                                                |
| SSBK     |           15 | 2021-08-12         | 2024-04-30        | False                 |                                             | Southern States Bancshares, Inc. - Common Stock                                                                                                                                 |
| STI      |            0 | 2017-03-16         | 2017-06-15        | True                  | Solidion Technology, Inc.                   | SunTrust Banks, Inc.                                                                                                                                                            |
| TCP      |            0 | 2019-10-30         | 2020-04-15        | False                 |                                             | TC PipeLines, LP                                                                                                                                                                |
| TCS      |            0 | 2017-09-26         | 2017-09-26        | False                 |                                             | The Container Store Group, Inc.                                                                                                                                                 |
| TLLP     |            0 | 2017-03-24         | 2017-03-24        | False                 |                                             | Tesoro Logistics LP                                                                                                                                                             |
| TRIT     |            0 | 2021-04-13         | 2021-06-29        | False                 |                                             | Triterras, Inc.                                                                                                                                                                 |
| TUP      |            0 | 2017-03-16         | 2017-06-15        | False                 |                                             | Tupperware Brands Corporation                                                                                                                                                   |
| TWTR     |            0 | 2017-05-24         | 2017-05-24        | False                 |                                             | Twitter, Inc.                                                                                                                                                                   |
| TWX      |            0 | 2017-03-16         | 2018-05-04        | False                 |                                             | Time Warner Inc.                                                                                                                                                                |
| UN       |            0 | 2017-03-16         | 2020-04-14        | True                  | Corgi UNH 2x Daily ETF                      | Unilever N.V. | The Unilever Group                                                                                                                                              |
| VFC      |            0 | 2016-10-31         | 2022-12-15        | True                  | V.F. Corporation                            | V.F. Corporation | V.F. Corporation Common Stock                                                                                                                                |
| VGR      |            0 | 2019-05-02         | 2019-05-02        | False                 |                                             | Vector Group Ltd.                                                                                                                                                               |
| VIAB     |            0 | 2016-11-07         | 2017-02-10        | False                 |                                             | Viacom, Inc.                                                                                                                                                                    |
| VIAC     |            0 | 2020-02-21         | 2020-04-14        | False                 |                                             | ViacomCBS Inc.                                                                                                                                                                  |
| VLP      |            0 | 2018-10-23         | 2018-12-20        | False                 |                                             | Valero Energy Partners LP                                                                                                                                                       |
| VMW      |            1 | 2021-03-29         | 2022-03-30        | False                 |                                             | VMware, Inc. | Vmware, Inc. Common stock, Class A                                                                                                                               |
| VSM      |            0 | 2016-11-07         | 2017-11-16        | False                 |                                             | Versum Materials, Inc.                                                                                                                                                          |
| WBA      |            7 | 2017-03-16         | 2024-04-30        | False                 |                                             | Walgreens Boots Alliance, Inc. - Common Stock | Walgreens Boots Alliance, Inc.                                                                                                  |
| WFM      |            0 | 2016-09-07         | 2017-08-17        | False                 |                                             | Whole Foods Market, Inc.                                                                                                                                                        |
| WOOF     |            0 | 2017-02-01         | 2017-03-14        | True                  | Petco Health and Wellness Company, Inc.     | VCA Inc.                                                                                                                                                                        |
| WPX      |            0 | 2016-09-01         | 2020-04-14        | False                 |                                             | WPX Energy, Inc.                                                                                                                                                                |
| WPZ      |            0 | 2016-08-11         | 2016-09-13        | False                 |                                             | Williams Partners L.P.                                                                                                                                                          |
| WRK      |            0 | 2017-03-16         | 2017-06-15        | False                 |                                             | WestRock Company                                                                                                                                                                |
| WTT      |            1 | 2023-08-15         | 2023-08-15        | False                 |                                             | Wireless Telecom Group Inc                                                                                                                                                      |
| WTW      |            0 | 2017-01-24         | 2018-12-27        | True                  | Willis Towers Watson Public Limited Company | Weight Watchers International, Inc.                                                                                                                                             |
| X        |           22 | 2021-05-06         | 2023-10-11        | False                 |                                             | United States Steel Corporation Common Stock | United States Steel Corporation                                                                                                  |
| XLNX     |            0 | 2018-03-09         | 2019-02-28        | False                 |                                             | Xilinx, Inc.                                                                                                                                                                    |
| ZAYO     |            0 | 2019-02-19         | 2019-02-20        | False                 |                                             | Zayo Group Holdings, Inc.                                                                                                                                                       |
| ZNGA     |            0 | 2016-12-15         | 2016-12-15        | False                 |                                             | Zynga Inc.                                                                                                                                                                      |
| ZNGA.SW  |            0 | 2017-07-14         | 2017-07-14        | False                 |                                             | Zynga Inc.                                                                                                                                                                      |

OTC-traded tickers (kept, `is_otc`): 304 tickers, 315 in-scope trades.

### 5. Concentration by senator (in-scope trades)

31 senators, 2,513 trades, $91,589,756 at range midpoints.

By trade count:

|   rank | senator              | party      |   trades |    dollars | share_trades   | share_dollars   | cum_share_trades   |
|-------:|:---------------------|:-----------|---------:|-----------:|:---------------|:----------------|:-------------------|
|      1 | Tommy Tuberville     | Republican |      734 | 28,619,367 | 29.2%          | 31.2%           | 29.2%              |
|      2 | Alan Armstrong       | Republican |      700 | 24,635,350 | 27.9%          | 26.9%           | 57.1%              |
|      3 | John Boozman         | Republican |      387 |  3,695,694 | 15.4%          | 4.0%            | 72.5%              |
|      4 | Markwayne Mullin     | Republican |      326 | 13,109,663 | 13.0%          | 14.3%           | 85.4%              |
|      5 | Sheldon Whitehouse   | Democrat   |       81 |  1,666,040 | 3.2%           | 1.8%            | 88.7%              |
|      6 | Dan Sullivan         | Republican |       68 |    807,034 | 2.7%           | 0.9%            | 91.4%              |
|      7 | Jerry Moran          | Republican |       56 |    521,528 | 2.2%           | 0.6%            | 93.6%              |
|      8 | Gary C. Peters       | Democrat   |       32 |    470,016 | 1.3%           | 0.5%            | 94.9%              |
|      9 | David McCormick      | Republican |       24 |  4,148,012 | 1.0%           | 4.5%            | 95.8%              |
|     10 | Ashley Moody         | Republican |       23 |  1,926,512 | 0.9%           | 2.1%            | 96.7%              |
|     11 | Bill Hagerty         | Republican |       19 |  4,517,510 | 0.8%           | 4.9%            | 97.5%              |
|     12 | John W. Hickenlooper | Democrat   |       19 |  4,633,010 | 0.8%           | 5.1%            | 98.2%              |
|     13 | Lindsey Graham       | Republican |       10 |    300,505 | 0.4%           | 0.3%            | 98.6%              |
|     14 | Shelley Moore Capito | Republican |        6 |     72,503 | 0.2%           | 0.1%            | 98.9%              |
|     15 | Jim Banks            | Republican |        5 |     40,002 | 0.2%           | 0.0%            | 99.1%              |
|     16 | Deb Fischer          | Republican |        4 |    166,002 | 0.2%           | 0.2%            | 99.2%              |
|     17 | Mark R. Warner       | Democrat   |        3 |    625,002 | 0.1%           | 0.7%            | 99.4%              |
|     18 | Bernie Moreno        | Republican |        2 |    207,501 | 0.1%           | 0.2%            | 99.4%              |
|     19 | Marco Rubio          | Republican |        2 |     16,001 | 0.1%           | 0.0%            | 99.5%              |
|     20 | Cynthia M. Lummis    | Republican |        1 |      8,000 | 0.0%           | 0.0%            | 99.6%              |
|     21 | J.D. Vance           | Republican |        1 |     75,000 | 0.0%           | 0.1%            | 99.6%              |
|     22 | James C. Justice     | Republican |        1 |    375,000 | 0.0%           | 0.4%            | 99.6%              |
|     23 | John Kennedy         | Republican |        1 |      8,000 | 0.0%           | 0.0%            | 99.7%              |
|     24 | John Thune           | Republican |        1 |     32,500 | 0.0%           | 0.0%            | 99.7%              |
|     25 | Katie Boyd Britt     | Republican |        1 |      8,000 | 0.0%           | 0.0%            | 99.8%              |
|     26 | Maria Cantwell       | Democrat   |        1 |     32,500 | 0.0%           | 0.0%            | 99.8%              |
|     27 | Patrick J. Toomey    | Republican |        1 |      8,000 | 0.0%           | 0.0%            | 99.8%              |
|     28 | Rick Scott           | Republican |        1 |    750,000 | 0.0%           | 0.8%            | 99.9%              |
|     29 | Tammy Duckworth      | Democrat   |        1 |     32,500 | 0.0%           | 0.0%            | 99.9%              |
|     30 | Thom Tillis          | Republican |        1 |      8,000 | 0.0%           | 0.0%            | 100.0%             |
|     31 | Thomas R. Carper     | Democrat   |        1 |     75,000 | 0.0%           | 0.1%            | 100.0%             |

By midpoint dollars:

|   rank | senator              | party      |   trades |    dollars | share_trades   | share_dollars   | cum_share_dollars   |
|-------:|:---------------------|:-----------|---------:|-----------:|:---------------|:----------------|:--------------------|
|      1 | Tommy Tuberville     | Republican |      734 | 28,619,367 | 29.2%          | 31.2%           | 31.2%               |
|      2 | Alan Armstrong       | Republican |      700 | 24,635,350 | 27.9%          | 26.9%           | 58.1%               |
|      3 | Markwayne Mullin     | Republican |      326 | 13,109,663 | 13.0%          | 14.3%           | 72.5%               |
|      4 | John W. Hickenlooper | Democrat   |       19 |  4,633,010 | 0.8%           | 5.1%            | 77.5%               |
|      5 | Bill Hagerty         | Republican |       19 |  4,517,510 | 0.8%           | 4.9%            | 82.4%               |
|      6 | David McCormick      | Republican |       24 |  4,148,012 | 1.0%           | 4.5%            | 87.0%               |
|      7 | John Boozman         | Republican |      387 |  3,695,694 | 15.4%          | 4.0%            | 91.0%               |
|      8 | Ashley Moody         | Republican |       23 |  1,926,512 | 0.9%           | 2.1%            | 93.1%               |
|      9 | Sheldon Whitehouse   | Democrat   |       81 |  1,666,040 | 3.2%           | 1.8%            | 94.9%               |
|     10 | Dan Sullivan         | Republican |       68 |    807,034 | 2.7%           | 0.9%            | 95.8%               |
|     11 | Rick Scott           | Republican |        1 |    750,000 | 0.0%           | 0.8%            | 96.6%               |
|     12 | Mark R. Warner       | Democrat   |        3 |    625,002 | 0.1%           | 0.7%            | 97.3%               |
|     13 | Jerry Moran          | Republican |       56 |    521,528 | 2.2%           | 0.6%            | 97.9%               |
|     14 | Gary C. Peters       | Democrat   |       32 |    470,016 | 1.3%           | 0.5%            | 98.4%               |
|     15 | James C. Justice     | Republican |        1 |    375,000 | 0.0%           | 0.4%            | 98.8%               |
|     16 | Lindsey Graham       | Republican |       10 |    300,505 | 0.4%           | 0.3%            | 99.1%               |
|     17 | Bernie Moreno        | Republican |        2 |    207,501 | 0.1%           | 0.2%            | 99.4%               |
|     18 | Deb Fischer          | Republican |        4 |    166,002 | 0.2%           | 0.2%            | 99.5%               |
|     19 | J.D. Vance           | Republican |        1 |     75,000 | 0.0%           | 0.1%            | 99.6%               |
|     20 | Thomas R. Carper     | Democrat   |        1 |     75,000 | 0.0%           | 0.1%            | 99.7%               |
|     21 | Shelley Moore Capito | Republican |        6 |     72,503 | 0.2%           | 0.1%            | 99.8%               |
|     22 | Jim Banks            | Republican |        5 |     40,002 | 0.2%           | 0.0%            | 99.8%               |
|     23 | John Thune           | Republican |        1 |     32,500 | 0.0%           | 0.0%            | 99.9%               |
|     24 | Maria Cantwell       | Democrat   |        1 |     32,500 | 0.0%           | 0.0%            | 99.9%               |
|     25 | Tammy Duckworth      | Democrat   |        1 |     32,500 | 0.0%           | 0.0%            | 99.9%               |
|     26 | Marco Rubio          | Republican |        2 |     16,001 | 0.1%           | 0.0%            | 100.0%              |
|     27 | Cynthia M. Lummis    | Republican |        1 |      8,000 | 0.0%           | 0.0%            | 100.0%              |
|     28 | John Kennedy         | Republican |        1 |      8,000 | 0.0%           | 0.0%            | 100.0%              |
|     29 | Katie Boyd Britt     | Republican |        1 |      8,000 | 0.0%           | 0.0%            | 100.0%              |
|     30 | Patrick J. Toomey    | Republican |        1 |      8,000 | 0.0%           | 0.0%            | 100.0%              |
|     31 | Thom Tillis          | Republican |        1 |      8,000 | 0.0%           | 0.0%            | 100.0%              |

### 6. Filing lag (disclosure date minus transaction date, in-scope trades)

| Group               |   Trades |   Median lag (days) |   75th pct |   95th pct | Share over 45 days   |
|:--------------------|---------:|--------------------:|-----------:|-----------:|:---------------------|
| All in-scope trades |     2513 |                  32 |        113 |        116 | 28.6%                |
| Tommy Tuberville    |      734 |                  31 |         38 |         42 | 0.0%                 |
| Alan Armstrong      |      700 |                 113 |        116 |        116 | 99.9%                |
| John Boozman        |      387 |                  26 |         35 |         42 | 2.3%                 |
| Markwayne Mullin    |      326 |                  29 |         29 |         34 | 0.6%                 |
| Sheldon Whitehouse  |       81 |                  27 |         29 |         42 | 4.9%                 |
| All other senators  |      285 |                  27 |         32 |         39 | 1.8%                 |

### 7. Paper filings inside the default window (trades we cannot see)

**85** paper PTRs received 2021-09-01 to 2026-08-31; list with links in `data/interim/paper_filings.csv`.

| filer_name         |   filings | first      | last       |
|:-------------------|----------:|:-----------|:-----------|
| RICHARD BLUMENTHAL |        64 | 2021-09-22 | 2026-08-31 |
| JOHN BOOZMAN       |        19 | 2021-09-08 | 2023-08-21 |
| DIANNE FEINSTEIN   |         1 | 2022-02-15 | 2022-02-15 |
| JOHN FETTERMAN     |         1 | 2024-07-12 | 2024-07-12 |

### 8. In-scope purchases and sales by year of disclosure

2021 starts 01 Sep; 2026 ends 31 Aug. Sales = Sale (Full) + Sale (Partial).

| year   |   Purchases |   Sales |   Purchases (no ETFs) |   Sales (no ETFs) |   Total |   Total (no ETFs) |
|:-------|------------:|--------:|----------------------:|------------------:|--------:|------------------:|
| 2021   |          29 |      35 |                    29 |                35 |      64 |                64 |
| 2022   |         133 |     150 |                   126 |               144 |     283 |               270 |
| 2023   |         253 |     172 |                   247 |               165 |     425 |               412 |
| 2024   |         114 |     293 |                    75 |               265 |     407 |               340 |
| 2025   |         192 |     183 |                   129 |               131 |     375 |               260 |
| 2026   |         798 |     161 |                   756 |               126 |     959 |               882 |
| Total  |       1,519 |     994 |                 1,362 |               866 |   2,513 |             2,228 |

### 9. Rows each pre-registered variant flag touches

Relative to the 2,513 in-scope trades. V7, V8 and V10 change sizing or weighting only.

| Variant   | Change                                 |   Trades | Effect                             |
|:----------|:---------------------------------------|---------:|:-----------------------------------|
| V1        | Exclude Tuberville                     |      734 | removed                            |
| V2.1      | Leave out #1 Tommy Tuberville          |      734 | removed                            |
| V2.2      | Leave out #2 Alan Armstrong            |      700 | removed                            |
| V2.3      | Leave out #3 John Boozman              |      387 | removed                            |
| V2.4      | Leave out #4 Markwayne Mullin          |      326 | removed                            |
| V2.5      | Leave out #5 Sheldon Whitehouse        |       81 | removed                            |
| V3        | Exclude first 180 days of service      |      746 | removed                            |
| V4        | Exclude PTRs with 50+ in-scope trades  |     1111 | removed (8 PTRs)                   |
| V5        | Exclude ETFs                           |      285 | removed                            |
| V6        | Add Spouse and Child trades            |     1054 | added (Spouse 1015, Child 39)      |
| V9        | Same-day entry (filed before 15:30 ET) |     1241 | enter same day                     |
| V11       | 3-year window                          |     2003 | trades in that window (Self/Joint) |
| V12       | 10-year window                         |     5458 | trades in that window (Self/Joint) |
## Phase 3: prices

_Stage `prices` of `python run_all.py`. Yahoo daily history 2016-01-01 to 2026-08-31 for every symbol in trades_clean.csv (all variants) plus SPY, NANC, KRUZ, GBPUSD=X; raw responses with their download date in `data/raw/prices/yahoo/`. No trade or portfolio returns are computed; per-ticker daily returns appear only in the checks below. Coverage uses the headline records (J3: as first published)._

### 1. Ticker resolution (renames and the survivorship ledger)

204 eFD tickers had no usable Yahoo record, or a Yahoo name matching no eFD name. Outcomes: delisted_or_unknown 169, rename 32, same_symbol 3. Renames and same-symbol name changes are confirmed through SEC EDGAR company histories (same CIK, a current or former SEC name equal to the eFD name) and Yahoo's name for the new symbol (`config/ticker_renames.yaml`, rules in `src/prices/resolve.py`).

Renames (32; 17 in-scope trades use one):

| old   | new   | effective_date   | date_basis                                         |
|:------|:------|:-----------------|:---------------------------------------------------|
| ABC   | COR   | 2023-08-15       | SEC: end of former name                            |
| ANTM  | ELV   | 2004-11-30       | SEC: end of former name                            |
| BIF   | STEW  | 2022-04-26       | SEC: end of former name                            |
| BK    | BNY   |                  | name unchanged; ticker change date not in SEC data |
| BLL   | BALL  |                  | name unchanged; ticker change date not in SEC data |
| CHK   | EXE   | 2024-09-26       | SEC: end of former name                            |
| CTL   | LUMN  | 2021-01-20       | SEC: end of former name                            |
| DGNR  | CCC   | 2021-07-29       | SEC: end of former name                            |
| DISCA | WBD   | 2018-03-05       | SEC: end of former name                            |
| DLPH  | APTV  | 2017-11-29       | SEC: end of former name                            |
| DPS   | KDP   | 2018-07-02       | SEC: end of former name                            |
| DWDP  | DD    | 2019-05-31       | SEC: end of former name                            |
| ETE   | ET    | 2018-09-18       | SEC: end of former name                            |
| EXPI  | AGNT  | 2026-06-01       | SEC: end of former name                            |
| FB    | META  | 2021-10-27       | SEC: end of former name                            |
| FI    | FISV  |                  | name unchanged; ticker change date not in SEC data |
| FLT   | CPAY  | 2024-03-14       | SEC: end of former name                            |
| GMRE  | XRN   | 2026-01-26       | SEC: end of former name                            |
| HRS   | LHX   | 2019-06-25       | SEC: end of former name                            |
| KAR   | OPLN  | 2023-05-12       | SEC: end of former name                            |
| LB    | BBWI  | 2013-03-22       | SEC: end of former name                            |
| MMC   | MRSH  | 2005-01-31       | SEC: end of former name                            |
| MPW   | MPT   |                  | name unchanged; ticker change date not in SEC data |
| OFC   | CDP   | 1998-01-22       | SEC: end of former name                            |
| PCLN  | BKNG  | 2018-02-16       | SEC: end of former name                            |
| PKI   | RVTY  | 2023-04-14       | SEC: end of former name                            |
| PSTG  | P     |                  | name unchanged; ticker change date not in SEC data |
| TMK   | GL    | 2019-08-02       | SEC: end of former name                            |
| UTX   | RTX   | 2020-04-06       | SEC: end of former name                            |
| WETF  | WT    | 2022-11-04       | SEC: end of former name                            |
| XON   | PGEN  | 2020-01-22       | SEC: end of former name                            |
| ZIOP  | TCRT  | 2022-01-04       | SEC: end of former name                            |

Same symbol, company renamed (3): RUM, SLB, UHAL.

Rejected by hand (same SEC company, not the same security):

| ticker   | reason                                                                                                                           |
|:---------|:---------------------------------------------------------------------------------------------------------------------------------|
| DVMT     | Dell Class V tracking stock, exchanged in Dec 2018 for DELL Class C shares (ratio 1.8036) or cash; not the same security as DELL |
| ESV      | Ensco -> Ensco Rowan -> Valaris; the old equity was cancelled in the 2020-21 Chapter 11; VAL is new equity                       |
| WTW      | Weight Watchers -> WW International; the old equity was cancelled in the 2025 Chapter 11; WW is new equity                       |

**Survivorship ledger** (`data/interim/survivorship_ledger.csv`): 169 tickers with no usable Yahoo data and no confirmed rename; 29 of them have in-scope trades (87 trades, $5,487,544 at midpoints). CRSP (A04) is the fix.

| ticker   | efd_asset_names                               |   in_scope_trades |   in_scope_midpoint_dollars | first_trade   | last_trade   | note                                                                   |
|:---------|:----------------------------------------------|------------------:|----------------------------:|:--------------|:-------------|:-----------------------------------------------------------------------|
| X        | United States Steel Corporation | United Stat |                22 |                   1,678,011 | 2021-10-18    | 2023-10-11   | no listed SEC company with this name (delisted, acquired, or not an SE |
| ECOM     | ChannelAdvisor Corporation | ChannelAdvisor C |                 6 |                   1,215,503 | 2022-03-08    | 2022-09-07   | no listed SEC company with this name (delisted, acquired, or not an SE |
| WTT      | Wireless Telecom Group Inc                    |                 1 |                     750,000 | 2023-08-15    | 2023-08-15   | no listed SEC company with this name (delisted, acquired, or not an SE |
| ATVI     | Activision Blizzard, Inc - Common Stock | Act |                 2 |                     350,001 | 2022-11-08    | 2023-04-26   | no listed SEC company with this name (delisted, acquired, or not an SE |
| SSBK     | Southern States Bancshares, Inc. - Common Sto |                15 |                     345,508 | 2021-08-12    | 2024-04-30   | no listed SEC company with this name (delisted, acquired, or not an SE |
| PARA     | Paramount Global - Class B Common Stock | Par |                 4 |                     315,002 | 2023-09-18    | 2024-05-10   | no listed SEC company with this name (delisted, acquired, or not an SE |
| WBA      | Walgreens Boots Alliance, Inc. | Walgreens Bo |                 7 |                     172,004 | 2022-01-12    | 2024-04-30   | no listed SEC company with this name (delisted, acquired, or not an SE |
| GOGL     | Golden Ocean Group Limited - Common Stock     |                 2 |                     150,001 | 2024-02-27    | 2024-04-30   | no listed SEC company with this name (delisted, acquired, or not an SE |
| NS       | Nustar Energy L.P. Common Units               |                 1 |                      75,000 | 2021-12-29    | 2021-12-29   | no listed SEC company with this name (delisted, acquired, or not an SE |
| IBDQ     | Dec 2025 Term Corp Ishares Ibonds ETF | iShar |                 2 |                      65,001 | 2022-06-30    | 2025-12-18   | no listed SEC company with this name (delisted, acquired, or not an SE |
| AHL-C    | Aspen Insurance Holdings Ltd [Ahl/Pc]         |                 1 |                      32,500 | 2025-01-02    | 2025-01-02   | no listed SEC company with this name (delisted, acquired, or not an SE |
| BKEP     | Blueknight Energy Partners L.P., L.L.C. - Com |                 1 |                      32,500 | 2021-12-29    | 2021-12-29   | no listed SEC company with this name (delisted, acquired, or not an SE |
| BKEPP    | Blueknight Energy Partners L.P. - Series A Pr |                 1 |                      32,500 | 2022-08-19    | 2022-08-19   | no listed SEC company with this name (delisted, acquired, or not an SE |
| BRK      | Bershire Hathaway Cdr [Cad Hedged]            |                 1 |                      32,500 | 2025-02-13    | 2025-02-13   | no listed SEC company with this name (delisted, acquired, or not an SE |
| BSCP     | Invesco BulletShares 2025 Corporate Bond ETF  |                 1 |                      32,500 | 2025-12-17    | 2025-12-17   | no listed SEC company with this name (delisted, acquired, or not an SE |
| FUN      | Cedar Fair, L.P. Common Stock                 |                 1 |                      32,500 | 2022-01-13    | 2022-01-13   | no listed SEC company with this name (delisted, acquired, or not an SE |
| RNWK     | RealNetworks, Inc. - Common Stock             |                 1 |                      32,500 | 2022-12-28    | 2022-12-28   | no listed SEC company with this name (delisted, acquired, or not an SE |
| COLPAL   | COLGATE PALMOLIVE LTD.                        |                 2 |                      16,001 | 2025-04-08    | 2025-10-09   | not a US-style symbol (likely a non-US listing); no rename searched    |
| CYBR     | CyberArk Software Ltd. - Ordinary Shares      |                 2 |                      16,001 | 2024-01-04    | 2024-12-18   | no listed SEC company with this name (delisted, acquired, or not an SE |
| LMST     | Limestone Bancorp, Inc. - Common Stock        |                 2 |                      16,001 | 2022-03-30    | 2023-04-03   | no listed SEC company with this name (delisted, acquired, or not an SE |
| MASI     | Masimo Corporation - Common Stock             |                 2 |                      16,001 | 2022-03-30    | 2022-10-05   | no listed SEC company with this name (delisted, acquired, or not an SE |
| PXD      | Pioneer Natural Resources Company | Pioneer N |                 2 |                      16,001 | 2023-01-10    | 2023-08-22   | no listed SEC company with this name (delisted, acquired, or not an SE |
| SQ       | Block, Inc. Class A Common Stock, | Square, I |                 2 |                      16,001 | 2022-04-11    | 2023-09-20   | SEC CIK 1512673 matches but has no single plain ticker (BSQKZ, XYZ)    |
| EQC      | Equity Commonwealth                           |                 1 |                       8,000 | 2024-12-13    | 2024-12-13   | no listed SEC company with this name (delisted, acquired, or not an SE |
| HES      | Hess Corp                                     |                 1 |                       8,000 | 2024-03-28    | 2024-03-28   | no listed SEC company with this name (delisted, acquired, or not an SE |
| IBDO     | iShares iBonds Dec 2023 Term Corporate ETF    |                 1 |                       8,000 | 2022-06-30    | 2022-06-30   | no listed SEC company with this name (delisted, acquired, or not an SE |
| INST     | Instructure Holdings Inc | Instructure Holdin |                 1 |                       8,000 | 2023-12-22    | 2023-12-22   | no listed SEC company with this name (delisted, acquired, or not an SE |
| SIVB     | SVB Financial Group | SVB Financial Group - C |                 1 |                       8,000 | 2022-03-30    | 2022-03-30   | no listed SEC company with this name (delisted, acquired, or not an SE |
| VMW      | VMware, Inc. | Vmware, Inc. Common stock, Cla |                 1 |                       8,000 | 2022-03-30    | 2022-03-30   | no listed SEC company with this name (delisted, acquired, or not an SE |

### 2. Price download

- Symbols requested: **1453**; with data: **136**; without: 1317. Per-symbol first/last date and download time: `data/processed/price_coverage.csv`.
- NYSE trading calendar (SPY's dates): 2016-01-04 to 2026-08-31, 2,680 days (`data/processed/trading_calendar.csv`).
- `data/processed/prices.csv.gz`: 344,900 rows (date, ticker, close, adj_close, volume). Yahoo's `close` is adjusted for splits only; `adj_close` for splits and dividends. Dividends and splits: `data/processed/dividends.csv`, `splits.csv`.

### 3. Coverage: in-scope trades with a usable price on the entry date

Entry date = first NYSE trading day after the disclosure date (D11). **294 of 2,540 in-scope records (11.6%) have a price; by midpoint dollars 9.8%** ($9,070,647 of $92,656,270).

| Senator              |   Trades |   With entry price | Share (count)   |   Midpoint $ | Share ($)   |
|:---------------------|---------:|-------------------:|:----------------|-------------:|:------------|
| ALL IN-SCOPE         |     2540 |                294 | 11.6%           |   92,656,270 | 9.8%        |
| Tommy Tuberville     |      752 |                 80 | 10.6%           |   29,148,876 | 8.2%        |
| Alan Armstrong       |      700 |                 83 | 11.9%           |   24,635,350 | 6.2%        |
| John Boozman         |      392 |                 47 | 12.0%           |    3,760,196 | 11.3%       |
| Markwayne Mullin     |      327 |                 50 | 15.3%           |   13,484,664 | 19.3%       |
| Sheldon Whitehouse   |       81 |                  7 | 8.6%            |    1,666,040 | 10.7%       |
| Dan Sullivan         |       68 |                 11 | 16.2%           |      807,034 | 17.0%       |
| Jerry Moran          |       56 |                  5 | 8.9%            |      521,528 | 7.7%        |
| Gary C. Peters       |       32 |                  0 | 0.0%            |      470,016 | 0.0%        |
| David McCormick      |       24 |                  0 | 0.0%            |    4,148,012 | 0.0%        |
| Ashley Moody         |       23 |                  7 | 30.4%           |    1,926,512 | 42.3%       |
| Bill Hagerty         |       20 |                  0 | 0.0%            |    4,550,010 | 0.0%        |
| John W. Hickenlooper |       19 |                  3 | 15.8%           |    4,633,010 | 20.0%       |
| Lindsey Graham       |       12 |                  0 | 0.0%            |      365,506 | 0.0%        |
| Shelley Moore Capito |        6 |                  1 | 16.7%           |       72,503 | 11.0%       |
| Jim Banks            |        5 |                  0 | 0.0%            |       40,002 | 0.0%        |
| Deb Fischer          |        4 |                  0 | 0.0%            |      166,002 | 0.0%        |
| Mark R. Warner       |        3 |                  0 | 0.0%            |      625,002 | 0.0%        |
| Bernie Moreno        |        2 |                  0 | 0.0%            |      207,501 | 0.0%        |
| Marco Rubio          |        2 |                  0 | 0.0%            |       16,001 | 0.0%        |
| Cynthia M. Lummis    |        1 |                  0 | 0.0%            |        8,000 | 0.0%        |
| J.D. Vance           |        1 |                  0 | 0.0%            |       75,000 | 0.0%        |
| James C. Justice     |        1 |                  0 | 0.0%            |      375,000 | 0.0%        |
| John Kennedy         |        1 |                  0 | 0.0%            |        8,000 | 0.0%        |
| John Thune           |        1 |                  0 | 0.0%            |       32,500 | 0.0%        |
| Katie Boyd Britt     |        1 |                  0 | 0.0%            |        8,000 | 0.0%        |
| Maria Cantwell       |        1 |                  0 | 0.0%            |       32,500 | 0.0%        |
| Patrick J. Toomey    |        1 |                  0 | 0.0%            |        8,000 | 0.0%        |
| Rick Scott           |        1 |                  0 | 0.0%            |      750,000 | 0.0%        |
| Tammy Duckworth      |        1 |                  0 | 0.0%            |       32,500 | 0.0%        |
| Thom Tillis          |        1 |                  0 | 0.0%            |        8,000 | 0.0%        |
| Thomas R. Carper     |        1 |                  0 | 0.0%            |       75,000 | 0.0%        |

Why prices are missing:

| why_missing                  |   trades |   midpoint_dollars |
|:-----------------------------|---------:|-------------------:|
| no Yahoo data for the symbol |     2246 |         83,585,623 |

Every in-scope record without an entry price (2246; also `data/interim/price_missing_entry.csv`):

| senator              | ticker   | price_ticker   | transaction_type   | disclosure_date   | entry_date   |   amount_mid | why_missing                  |
|:---------------------|:---------|:---------------|:-------------------|:------------------|:-------------|-------------:|:-----------------------------|
| Alan Armstrong       | UHS      | UHS            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WMB      | WMB            | Sale (Partial)     | 2026-07-21        | 2026-07-22   |   15,000,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RCRUY    | RCRUY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DVA      | DVA            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DDOG     | DDOG           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CDNS     | CDNS           | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BXP      | BXP            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BG       | BG             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BRO      | BRO            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BR       | BR             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HAGHY    | HAGHY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TOELY    | TOELY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | DQJCY    | DQJCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EJPRY    | EJPRY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ZURVY    | ZURVY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WSE      | WSE            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | UNCRY    | UNCRY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SCMWY    | SCMWY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SBGSY    | SBGSY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SAP      | SAP            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KKPNY    | KKPNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RYCEY    | RYCEY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NVS      | NVS            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HENKY    | HENKY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HEINY    | HEINY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GLNCY    | GLNCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DSDVY    | DSDVY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CFRUY    | CFRUY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CRRFY    | CRRFY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BHP      | BHP            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SAN      | SAN            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ZURVY    | ZURVY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | YARIY    | YARIY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WTKWY    | WTKWY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WSE      | WSE            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WLMIY    | WLMIY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WFAFY    | WFAFY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | WELL     | WELL           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VONOY    | VONOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VLVLY    | VLVLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VWAPY    | VWAPY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VOD      | VOD            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VCISY    | VCISY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | VWDRY    | VWDRY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VRSN     | VRSN           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VACNY    | VACNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | UPMMY    | UPMMY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | UOVEY    | UOVEY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | UNVGY    | UNVGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | UL       | UL             | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | UNCRY    | UNCRY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | UNICY    | UNICY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | UCBJY    | UCBJY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | UBS      | UBS            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | UBER     | UBER           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TM       | TM             | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | TKOMY    | TKOMY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TRYIY    | TRYIY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | THLLY    | THLLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TEVA     | TEVA           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TSLA     | TSLA           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TRUMY    | TRUMY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TLGPY    | TLGPY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TLSNY    | TLSNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TELNY    | TELNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TELFY    | TELFY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TIIAY    | TIIAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TTNDY    | TTNDY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TTDKY    | TTDKY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TAK      | TAK            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SSMXY    | SSMXY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SYIEY    | SYIEY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SCMWY    | SCMWY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SSREY    | SSREY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SWRAY    | SWRAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SWDBY    | SWDBY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SWGAY    | SWGAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SVNLY    | SVNLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SZKMY    | SZKMY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SUHJY    | SUHJY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SUTNY    | SUTNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SMFG     | SMFG           | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | SMMYY    | SMMYY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SMTOY    | SMTOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FUJHY    | FUJHY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SEOAY    | SEOAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | STM      | STM            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | STLA     | STLA           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SCBFY    | SCBFY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SPOT     | SPOT           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SOUHY    | SOUHY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SONY     | SONY           | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | SFGYY    | SFGYY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SONVY    | SONVY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SKHHY    | SKHHY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SMPNY    | SMPNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SFTBY    | SFTBY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SOBKY    | SOBKY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SDXAY    | SDXAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SCGLY    | SCGLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SMGZY    | SMGZY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SNN      | SNN            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SMCAY    | SMCAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SKBSY    | SKBSY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SGAPY    | SGAPY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SPXCY    | SPXCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SINGY    | SINGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SMERY    | SMERY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | SIEGY    | SIEGY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | SSDOY    | SSDOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SGIOY    | SGIOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SHECY    | SHECY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SMNNY    | SMNNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SGSOY    | SGSOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SVNDY    | SVNDY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SKHSY    | SKHSY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SOMLY    | SOMLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SE       | SE             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SCHW     | SCHW           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SBGSY    | SBGSY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | SAP      | SAP            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | SNY      | SNY            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | SDVKY    | SDVKY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SDZNY    | SDZNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SAXPY    | SAXPY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SGPYY    | SGPYY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SAFRY    | SAFRY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | SAABY    | SAABY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RYAAY    | RYAAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KKPNY    | KKPNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RYCEY    | RYCEY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | RHHBY    | RHHBY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | RIO      | RIO            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | RNMBY    | RNMBY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RSHGY    | RSHGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RTO      | RTO            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RNECY    | RNECY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RNLSY    | RNLSY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RELX     | RELX           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RBGLY    | RBGLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DGX      | DGX            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | QBIEY    | QBIEY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | QABSY    | QABSY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PUBGY    | PUBGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PRYMY    | PRYMY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PUK      | PUK            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PROSY    | PROSY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PRNDY    | PRNDY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PSO      | PSO            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PNDRY    | PNDRY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PCRHY    | PCRHY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | OVCHY    | OVCHY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | OTSKY    | OTSKY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ORKLY    | ORKLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | IX       | IX             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | OLCLY    | OLCLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ORANY    | ORANY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | OBICY    | OBICY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ORLY     | ORLY           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NVDA     | NVDA           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NTTYY    | NTTYY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NVZMY    | NVZMY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NVO      | NVO            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | NVS      | NVS            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | NHYDY    | NHYDY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NRDBY    | NRDBY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NRILY    | NRILY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NMR      | NMR            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NOK      | NOK            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NNGRY    | NNGRY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NPNYY    | NPNYY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NPSCY    | NPSCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NTDOY    | NTDOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NICE     | NICE           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NEXOY    | NEXOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NSRGY    | NSRGY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | NBIS     | NBIS           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NWG      | NWG            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NABZY    | NABZY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | MRAAY    | MRAAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MURGY    | MURGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MSADY    | MSADY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MNDY     | MNDY           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MONRY    | MONRY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MFG      | MFG            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | MSLOY    | MSLOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MTSFY    | MTSFY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MITSY    | MITSY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | MHVIY    | MHVIY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | MITEY    | MITEY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MIELY    | MIELY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MTSUY    | MTSUY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | MSFT     | MSFT           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MGDDY    | MGDDY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MBGYY    | MBGYY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MARUY    | MARUY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MQBKY    | MQBKY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LYSDY    | LYSDY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | YAHOY    | YAHOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LRLCY    | LRLCY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | LZAGY    | LZAGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LSEGY    | LSEGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LOGI     | LOGI           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LYG      | LYG            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FINMY    | FINMY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LGRDY    | LGRDY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LGGNY    | LGGNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LSRCY    | LSRCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LDSCY    | LDSCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LRCX     | LRCX           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KHNGY    | KHNGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KUBTY    | KUBTY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PHG      | PHG            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KBGGY    | KBGGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KNYJY    | KNYJY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KMTUY    | KMTUY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KNRRY    | KNRRY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KNBWY    | KNBWY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KXIAY    | KXIAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KGFHY    | KGFHY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KMB      | KMB            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PPRUY    | PPRUY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KDDIY    | KDDIY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KBCSY    | KBCSY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EADSY    | EADSY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | KWHIY    | KWHIY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KAOOY    | KAOOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | JBAXY    | JBAXY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | JNJ      | JNJ            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | JRONY    | JRONY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | JMHLY    | JMHLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | JAPAY    | JAPAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | JPXGY    | JPXGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | JSAIY    | JSAIY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ITOCY    | ITOCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ISUZY    | ISUZY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ISNPY    | ISNPY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | ICAGY    | ICAGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | IHG      | IHG            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ING      | ING            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | IFJPY    | IFJPY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | IFNNY    | IFNNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | IDEXY    | IDEXY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ISMAY    | ISMAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | IHICY    | IHICY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ICL      | ICL            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HSBC     | HSBC           | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | HOCPY    | HOCPY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HKXCY    | HKXCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HMC      | HMC            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HCMLY    | HCMLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HTHIY    | HTHIY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | HXGBY    | HXGBY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TGOPY    | TGOPY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HESAY    | HESAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HNNMY    | HNNMY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TSCDY    | TSCDY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HENOY    | HENOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HEINY    | HEINY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HDLMY    | HDLMY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HVRRY    | HVRRY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ZBH      | ZBH            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HALMY    | HALMY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HLN      | HLN            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | YUM      | YUM            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GS       | GS             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GLNCY    | GLNCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WYNN     | WYNN           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WDC      | WDC            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GSK      | GSK            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | GVDNY    | GVDNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WDAY     | WDAY           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GMAB     | GMAB           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GBERY    | GBERY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WELL     | WELL           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GALDY    | GALDY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WFC      | WFC            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FJTSY    | FJTSY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FUJIY    | FUJIY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WBD      | WBD            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FSNUY    | FSNUY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DIS      | DIS            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FMS      | FMS            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FSUGY    | FSUGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WMT      | WMT            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | RACE     | RACE           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | WAB      | WAB            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FRCOY    | FRCOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FANUY    | FANUY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | V        | V              | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | EXPGY    | EXPGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VICI     | VICI           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EVVTY    | EVVTY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ESLOY    | ESLOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EBKDY    | EBKDY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ERIC     | ERIC           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EPOAY    | EPOAY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EA       | EA             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ESLT     | ESLT           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ESAIY    | ESAIY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EBCOY    | EBCOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DSDVY    | DSDVY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DSFIY    | DSFIY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DRPRY    | DRPRY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DNBBY    | DNBBY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DSCSY    | DSCSY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DEO      | DEO            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DTEGY    | DTEGY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | DHLGY    | DHLGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DLAKY    | DLAKY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DBOEY    | DBOEY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | DB       | DB             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DNZOY    | DNZOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DBSDY    | DBSDY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | DASTY    | DASTY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DNKEY    | DNKEY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DANOY    | DANOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DWAHY    | DWAHY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DIFTY    | DIFTY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DTRUY    | DTRUY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DKILY    | DKILY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DSNKY    | DSNKY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DFKCY    | DFKCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DLICY    | DLICY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CSLLY    | CSLLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CRARY    | CRARY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CMWAY    | CMWAY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | CMSQY    | CMSQY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CMPGY    | CMPGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CFRUY    | CFRUY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VRT      | VRT            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VRTX     | VRTX           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VZ       | VZ             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VRSK     | VRSK           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | VTR      | VTR            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | URI      | URI            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | UNH      | UNH            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | UPS      | UPS            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | UNP      | UNP            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | UDR      | UDR            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TFC      | TFC            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TRV      | TRV            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TDG      | TDG            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TT       | TT             | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | TMO      | TMO            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | COO      | COO            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CI       | CI             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CPB      | CPB            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TXT      | TXT            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TXN      | TXN            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TSLA     | TSLA           | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | TER      | TER            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TDY      | TDY            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TPR      | TPR            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TTWO     | TTWO           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TMUS     | TMUS           | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | SNPS     | SNPS           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SYF      | SYF            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SYK      | SYK            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | STLD     | STLD           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SBUX     | SBUX           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SOLV     | SOLV           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SNA      | SNA            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SJM      | SJM            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SWKS     | SWKS           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SPG      | SPG            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NOW      | NOW            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | STX      | STX            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SCHW     | SCHW           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SNDK     | SNDK           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CRM      | CRM            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SPGI     | SPGI           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RTX      | RTX            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | RCL      | RCL            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ROP      | ROP            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HOOD     | HOOD           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RMD      | RMD            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RSG      | RSG            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | REGN     | REGN           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | REG      | REG            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | O        | O              | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DGX      | DGX            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PWR      | PWR            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | QCOM     | QCOM           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | Q        | Q              | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PSA      | PSA            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PTC      | PTC            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PRU      | PRU            | Sale (Full)        | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PGR      | PGR            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | PG       | PG             | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | PFG      | PFG            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | POOL     | POOL           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PNC      | PNC            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PSX      | PSX            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PM       | PM             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PEP      | PEP            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PYPL     | PYPL           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PAYX     | PAYX           | Sale (Full)        | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CODYY    | CODYY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CRZBY    | CRZBY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CLPBY    | CLPBY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CHEOY    | CHEOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PH       | PH             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CCHGY    | CCHGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PANW     | PANW           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CCEP     | CCEP           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CKHUY    | CKHUY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PLTR     | PLTR           | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | CIEN     | CIEN           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CHGCY    | CHGCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PCAR     | PCAR           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CHKP     | CHKP           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | OTIS     | OTIS           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CJPRY    | CJPRY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ORCL     | ORCL           | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | CLLNY    | CLLNY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | OMC      | OMC            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CRRFY    | CRRFY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ORLY     | ORLY           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CABGY    | CABGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NXPI     | NXPI           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CGEMY    | CGEMY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NVDA     | NVDA           | Purchase           | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NUE      | NUE            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CCOEY    | CCOEY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CAJPY    | CAJPY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NOC      | NOC            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CAIXY    | CAIXY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NSC      | NSC            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NKE      | NKE            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BVVBY    | BVVBY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BZLFY    | BZLFY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BTI      | BTI            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | BRDCY    | BRDCY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BNTGY    | BNTGY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BXBLY    | BXBLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BOUYY    | BOUYY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BHKLY    | BHKLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BNPQY    | BNPQY          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | BHP      | BHP            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | BMWKY    | BMWKY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BRRLY    | BRRLY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BTDPY    | BTDPY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BKNIY    | BKNIY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NCBDY    | NCBDY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SAN      | SAN            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | DUFRY    | DUFRY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NEE      | NEE            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NEM      | NEM            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | NFLX     | NFLX           | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | NDAQ     | NDAQ           | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MSCI     | MSCI           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MSI      | MSI            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MOS      | MOS            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MS       | MS             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MDLZ     | MDLZ           | Sale (Full)        | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | TAP      | TAP            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MAA      | MAA            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MSFT     | MSFT           | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | MU       | MU             | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | MCHP     | MCHP           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MGM      | MGM            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MT       | MT             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MET      | MET            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | META     | META           | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | MRK      | MRK            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | MDT      | MDT            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BUD      | BUD            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MCK      | MCK            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MCD      | MCD            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MA       | MA             | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | NGLOY    | NGLOY          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MRSH     | MRSH           | Sale (Full)        | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MAR      | MAR            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LYB      | LYB            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GOOG     | GOOG           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LITE     | LITE           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LOW      | LOW            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | L        | L              | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LMT      | LMT            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LYV      | LYV            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LIN      | LIN            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | LLY      | LLY            | Sale (Full)        | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LEN      | LEN            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LDOS     | LDOS           | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | LRCX     | LRCX           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LH       | LH             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LHX      | LHX            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KHC      | KHC            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KLAC     | KLAC           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KKR      | KKR            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KMI      | KMI            | Sale (Full)        | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KIM      | KIM            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KEY      | KEY            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KDP      | KDP            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KVUE     | KVUE           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | JPM      | JPM            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | JNJ      | JNJ            | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | INVH     | INVH           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ISRG     | ISRG           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | INTU     | INTU           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | IBM      | IBM            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ICE      | ICE            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | INTC     | INTC           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HBAN     | HBAN           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HUM      | HUM            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HUBB     | HUBB           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HPQ      | HPQ            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HWM      | HWM            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HON      | HON            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HD       | HD             | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | HLT      | HLT            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HPE      | HPE            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HSY      | HSY            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DOC      | DOC            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HCA      | HCA            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HAS      | HAS            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HIG      | HIG            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GS       | GS             | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | GDDY     | GDDY           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GL       | GL             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GPN      | GPN            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GILD     | GILD           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GPC      | GPC            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GIS      | GIS            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GD       | GD             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GM       | GM             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GEN      | GEN            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GEV      | GEV            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | GEHC     | GEHC           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GE       | GE             | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | FCX      | FCX            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BEN      | BEN            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FOXA     | FOXA           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FTV      | FTV            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FTNT     | FTNT           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | F        | F              | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FISV     | FISV           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FSLR     | FSLR           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FIS      | FIS            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FDX      | FDX            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FRT      | FRT            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FICO     | FICO           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FFIV     | FFIV           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | XOM      | XOM            | Sale (Full)        | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EXPD     | EXPD           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EXPE     | EXPE           | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | PSTG     | P              | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EG       | EG             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ESS      | ESS            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EMR      | EMR            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EME      | EME            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ELV      | ELV            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EA       | EA             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EW       | EW             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | EBAY     | EBAY           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | ETN      | ETN            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DUK      | DUK            | Sale (Full)        | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DOW      | DOW            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DOV      | DOV            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DASH     | DASH           | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | DPZ      | DPZ            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DLR      | DLR            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DELL     | DELL           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DE       | DE             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DRI      | DRI            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DHR      | DHR            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CVS      | CVS            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CSX      | CSX            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CCI      | CCI            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CRWD     | CRWD           | Sale (Full)        | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | COST     | COST           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CTVA     | CTVA           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GLW      | GLW            | Sale (Full)        | 2026-07-21        | 2026-07-22   |      175,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CPRT     | CPRT           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | STZ      | STZ            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CAG      | CAG            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FIX      | FIX            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CMCSA    | CMCSA          | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | COIN     | COIN           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CTSH     | CTSH           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | KO       | KO             | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | CME      | CME            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | C        | C              | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | CSCO     | CSCO           | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | CIEN     | CIEN           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CB       | CB             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CVX      | CVX            | Sale (Full)        | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CHTR     | CHTR           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CF       | CF             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | COR      | COR            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CBOE     | CBOE           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CCL      | CCL            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CAH      | CAH            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | COF      | COF            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | CPT      | CPT            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BMY      | BMY            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BSX      | BSX            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BKNG     | BKNG           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BX       | BX             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BIIB     | BIIB           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BRK-B    | BRK-B          | Purchase           | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BDX      | BDX            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | BK       | BNY            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | AVB      | AVB            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | T        | T              | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Alan Armstrong       | MO       | MO             | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | GOOG     | GOOG           | Purchase           | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | MMM      | MMM            | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | SOLS     | SOLS           | Sale (Full)        | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Alan Armstrong       | PFE      | PFE            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | LVMUY    | LVMUY          | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HON      | HON            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | HD       | HD             | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | RACE     | RACE           | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | FDX      | FDX            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Alan Armstrong       | DVN      | DVN            | Sale (Full)        | 2026-07-21        | 2026-07-22   |       75,000 | no Yahoo data for the symbol |
| Ashley Moody         | MU       | MU             | Purchase           | 2025-02-21        | 2025-02-24   |       75,000 | no Yahoo data for the symbol |
| Ashley Moody         | HWM      | HWM            | Purchase           | 2025-02-21        | 2025-02-24   |       75,000 | no Yahoo data for the symbol |
| Ashley Moody         | OKTA     | OKTA           | Sale (Full)        | 2025-02-21        | 2025-02-24   |       75,000 | no Yahoo data for the symbol |
| Ashley Moody         | LLY      | LLY            | Purchase           | 2025-03-22        | 2025-03-24   |      175,000 | no Yahoo data for the symbol |
| Ashley Moody         | SMCI     | SMCI           | Sale (Partial)     | 2025-03-22        | 2025-03-24   |       75,000 | no Yahoo data for the symbol |
| Ashley Moody         | SMCI     | SMCI           | Sale (Partial)     | 2025-03-22        | 2025-03-24   |       32,500 | no Yahoo data for the symbol |
| Ashley Moody         | HWM      | HWM            | Sale (Full)        | 2025-03-22        | 2025-03-24   |       75,000 | no Yahoo data for the symbol |
| Ashley Moody         | GENI     | GENI           | Purchase           | 2025-03-22        | 2025-03-24   |        8,000 | no Yahoo data for the symbol |
| Ashley Moody         | KPTI     | KPTI           | Sale (Full)        | 2025-03-22        | 2025-03-24   |        8,000 | no Yahoo data for the symbol |
| Ashley Moody         | NVDA     | NVDA           | Purchase           | 2025-04-20        | 2025-04-21   |       32,500 | no Yahoo data for the symbol |
| Ashley Moody         | NVDA     | NVDA           | Purchase           | 2025-04-20        | 2025-04-21   |      175,000 | no Yahoo data for the symbol |
| Ashley Moody         | SMCI     | SMCI           | Sale (Partial)     | 2025-04-20        | 2025-04-21   |       32,500 | no Yahoo data for the symbol |
| Ashley Moody         | SMCI     | SMCI           | Purchase           | 2025-04-20        | 2025-04-21   |      175,000 | no Yahoo data for the symbol |
| Ashley Moody         | ET       | ET             | Purchase           | 2025-05-13        | 2025-05-14   |       32,500 | no Yahoo data for the symbol |
| Ashley Moody         | JPM      | JPM            | Purchase           | 2025-05-13        | 2025-05-14   |       32,500 | no Yahoo data for the symbol |
| Ashley Moody         | HWM      | HWM            | Purchase           | 2025-05-13        | 2025-05-14   |       32,500 | no Yahoo data for the symbol |
| Bernie Moreno        | BEEP     | BEEP           | Sale (Full)        | 2025-04-30        | 2025-05-01   |       32,500 | no Yahoo data for the symbol |
| Bernie Moreno        | ETOR     | ETOR           | Sale (Full)        | 2026-05-22        | 2026-05-26   |      175,000 | no Yahoo data for the symbol |
| Bill Hagerty         | DDOG     | DDOG           | Sale (Partial)     | 2021-11-23        | 2021-11-24   |    3,000,000 | no Yahoo data for the symbol |
| Bill Hagerty         | VRM      | VRM            | Sale (Full)        | 2021-12-22        | 2021-12-23   |        8,000 | no Yahoo data for the symbol |
| Bill Hagerty         | DDOG     | DDOG           | Sale (Full)        | 2022-01-10        | 2022-01-11   |       32,500 | no Yahoo data for the symbol |
| Bill Hagerty         | RHP      | RHP            | Sale (Full)        | 2022-01-10        | 2022-01-11   |      175,000 | no Yahoo data for the symbol |
| Bill Hagerty         | RNR      | RNR            | Sale (Partial)     | 2022-01-10        | 2022-01-11   |      375,000 | no Yahoo data for the symbol |
| Bill Hagerty         | RHP      | RHP            | Sale (Partial)     | 2022-01-10        | 2022-01-11   |       32,500 | no Yahoo data for the symbol |
| Bill Hagerty         | RNR      | RNR            | Sale (Partial)     | 2022-01-10        | 2022-01-11   |      375,000 | no Yahoo data for the symbol |
| Bill Hagerty         | PNFP     | PNFP           | Sale (Partial)     | 2022-01-10        | 2022-01-11   |      175,000 | no Yahoo data for the symbol |
| Bill Hagerty         | ENVA     | ENVA           | Sale (Full)        | 2022-01-10        | 2022-01-11   |       32,500 | no Yahoo data for the symbol |
| Bill Hagerty         | CCEP     | CCEP           | Sale (Full)        | 2022-01-10        | 2022-01-11   |       75,000 | no Yahoo data for the symbol |
| Bill Hagerty         | BKEP     | BKEP           | Sale (Full)        | 2022-01-10        | 2022-01-11   |       32,500 | no Yahoo data for the symbol |
| Bill Hagerty         | NS       | NS             | Sale (Full)        | 2022-01-10        | 2022-01-11   |       75,000 | no Yahoo data for the symbol |
| Bill Hagerty         | CLDT     | CLDT           | Sale (Full)        | 2022-01-10        | 2022-01-11   |        8,000 | no Yahoo data for the symbol |
| Bill Hagerty         | TACO     | TACO           | Sale (Partial)     | 2022-04-13        | 2022-04-14   |       32,500 | no Yahoo data for the symbol |
| Bill Hagerty         | LMND     | LMND           | Sale (Partial)     | 2022-05-16        | 2022-05-17   |        8,000 | no Yahoo data for the symbol |
| Bill Hagerty         | BKEPP    | BKEPP          | Sale (Full)        | 2022-09-02        | 2022-09-06   |       32,500 | no Yahoo data for the symbol |
| Bill Hagerty         | TACO     | TACO           | Sale (Full)        | 2023-08-14        | 2023-08-15   |       32,500 | no Yahoo data for the symbol |
| Bill Hagerty         | DDOG     | DDOG           | Sale (Full)        | 2024-01-10        | 2024-01-11   |        8,000 | no Yahoo data for the symbol |
| Bill Hagerty         | EQC      | EQC            | Sale (Full)        | 2024-12-30        | 2024-12-31   |        8,000 | no Yahoo data for the symbol |
| Bill Hagerty         | AHL-C    | AHL-C          | Sale (Full)        | 2025-01-22        | 2025-01-23   |       32,500 | no Yahoo data for the symbol |
| Cynthia M. Lummis    | J        | J              | Purchase           | 2021-10-07        | 2021-10-08   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | RPM      | RPM            | Sale (Partial)     | 2022-04-07        | 2022-04-08   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | RPM      | RPM            | Sale (Partial)     | 2022-07-14        | 2022-07-15   |       32,500 | no Yahoo data for the symbol |
| Dan Sullivan         | FIVE     | FIVE           | Sale (Full)        | 2022-11-03        | 2022-11-04   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | SYK      | SYK            | Sale (Full)        | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | PYPL     | PYPL           | Sale (Full)        | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | META     | META           | Sale (Full)        | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | MDT      | MDT            | Sale (Full)        | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | MLM      | MLM            | Sale (Full)        | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | FFIV     | FFIV           | Sale (Full)        | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | ELAN     | ELAN           | Sale (Full)        | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | CMCSA    | CMCSA          | Sale (Full)        | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | GOOG     | GOOG           | Sale (Partial)     | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | RPM      | RPM            | Sale (Partial)     | 2022-12-21        | 2022-12-22   |       32,500 | no Yahoo data for the symbol |
| Dan Sullivan         | ZTS      | ZTS            | Purchase           | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | TJX      | TJX            | Purchase           | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | TMO      | TMO            | Purchase           | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | MSFT     | MSFT           | Purchase           | 2022-12-21        | 2022-12-22   |       32,500 | no Yahoo data for the symbol |
| Dan Sullivan         | LRCX     | LRCX           | Purchase           | 2022-12-21        | 2022-12-22   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | ULTA     | ULTA           | Sale (Partial)     | 2023-02-13        | 2023-02-14   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | PXD      | PXD            | Sale (Partial)     | 2023-02-13        | 2023-02-14   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | JPM      | JPM            | Sale (Partial)     | 2023-02-13        | 2023-02-14   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | CVS      | CVS            | Sale (Partial)     | 2023-02-13        | 2023-02-14   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | BMY      | BMY            | Sale (Partial)     | 2023-02-13        | 2023-02-14   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | BKNG     | BKNG           | Sale (Partial)     | 2023-02-13        | 2023-02-14   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | ZTS      | ZTS            | Purchase           | 2023-02-13        | 2023-02-14   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | SCHW     | SCHW           | Sale (Partial)     | 2023-03-16        | 2023-03-17   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | CHD      | CHD            | Purchase           | 2023-03-16        | 2023-03-17   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | CHD      | CHD            | Purchase           | 2023-03-16        | 2023-03-17   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | GOOG     | GOOG           | Purchase           | 2023-03-16        | 2023-03-17   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | WFC      | WFC            | Sale (Full)        | 2023-04-26        | 2023-04-27   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | ZTS      | ZTS            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | ULTA     | ULTA           | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | TSCO     | TSCO           | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | TJX      | TJX            | Sale (Full)        | 2023-09-18        | 2023-09-19   |       32,500 | no Yahoo data for the symbol |
| Dan Sullivan         | TMO      | TMO            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | LUV      | LUV            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | PPG      | PPG            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | PNC      | PNC            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | PXD      | PXD            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | NTRS     | NTRS           | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | MSFT     | MSFT           | Sale (Full)        | 2023-09-18        | 2023-09-19   |       75,000 | no Yahoo data for the symbol |
| Dan Sullivan         | MA       | MA             | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | LRCX     | LRCX           | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | LH       | LH             | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | JPM      | JPM            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | JNJ      | JNJ            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | HON      | HON            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | CVS      | CVS            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | COST     | COST           | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | CHD      | CHD            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | CVX      | CVX            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | SCHW     | SCHW           | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | BMY      | BMY            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | BKNG     | BKNG           | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | BLK      | BLK            | Sale (Full)        | 2023-09-18        | 2023-09-19   |        8,000 | no Yahoo data for the symbol |
| Dan Sullivan         | GOOG     | GOOG           | Sale (Full)        | 2023-09-18        | 2023-09-19   |       32,500 | no Yahoo data for the symbol |
| Dan Sullivan         | RPM      | RPM            | Sale (Partial)     | 2024-02-09        | 2024-02-12   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | RUM      | RUM            | Sale (Full)        | 2025-02-09        | 2025-02-10   |    3,000,000 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-03-05        | 2025-03-06   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-03-05        | 2025-03-06   |       75,000 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-03-29        | 2025-03-31   |       75,000 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-03-29        | 2025-03-31   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-03-29        | 2025-03-31   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-03-29        | 2025-03-31   |       75,000 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-03-29        | 2025-03-31   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-03-29        | 2025-03-31   |       75,000 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-03-29        | 2025-03-31   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-03-29        | 2025-03-31   |       75,000 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-04-23        | 2025-04-24   |       75,000 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-04-23        | 2025-04-24   |       75,000 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-04-23        | 2025-04-24   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-04-30        | 2025-05-01   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-04-30        | 2025-05-01   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-04-30        | 2025-05-01   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-04-30        | 2025-05-01   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-04-30        | 2025-05-01   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | IJR      | IJR            | Sale (Partial)     | 2025-06-04        | 2025-06-05   |        8,000 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-11-27        | 2025-11-28   |       32,500 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-11-27        | 2025-11-28   |       75,000 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-12-26        | 2025-12-29   |       75,000 | no Yahoo data for the symbol |
| David McCormick      | BITB     | BITB           | Purchase           | 2025-12-26        | 2025-12-29   |       75,000 | no Yahoo data for the symbol |
| Deb Fischer          | LMT      | LMT            | Sale (Full)        | 2022-07-20        | 2022-07-21   |       75,000 | no Yahoo data for the symbol |
| Deb Fischer          | KO       | KO             | Sale (Full)        | 2022-07-20        | 2022-07-21   |        8,000 | no Yahoo data for the symbol |
| Deb Fischer          | CSCO     | CSCO           | Sale (Full)        | 2022-07-20        | 2022-07-21   |        8,000 | no Yahoo data for the symbol |
| Deb Fischer          | CAT      | CAT            | Sale (Full)        | 2022-07-20        | 2022-07-21   |       75,000 | no Yahoo data for the symbol |
| Gary C. Peters       | CAG      | CAG            | Purchase           | 2021-12-07        | 2021-12-08   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | OFC      | CDP            | Purchase           | 2021-12-07        | 2021-12-08   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | VZ       | VZ             | Purchase           | 2021-12-07        | 2021-12-08   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | IBM      | IBM            | Purchase           | 2022-01-08        | 2022-01-10   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | HBAN     | HBAN           | Purchase           | 2022-01-08        | 2022-01-10   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | FSK      | FSK            | Purchase           | 2022-05-16        | 2022-05-17   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | WBD      | WBD            | Sale (Full)        | 2023-01-10        | 2023-01-11   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | TFC      | TFC            | Purchase           | 2023-04-12        | 2023-04-13   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | O        | O              | Purchase           | 2023-04-12        | 2023-04-13   |       32,500 | no Yahoo data for the symbol |
| Gary C. Peters       | NUE      | NUE            | Sale (Full)        | 2023-04-12        | 2023-04-13   |       75,000 | no Yahoo data for the symbol |
| Gary C. Peters       | IFF      | IFF            | Purchase           | 2023-06-30        | 2023-07-03   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | D        | D              | Sale (Full)        | 2024-01-25        | 2024-01-26   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | SOLV     | SOLV           | Sale (Full)        | 2024-05-23        | 2024-05-24   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | CCL      | CCL            | Sale (Full)        | 2024-05-23        | 2024-05-24   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | SLB      | SLB            | Sale (Full)        | 2024-05-23        | 2024-05-24   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | IFF      | IFF            | Sale (Full)        | 2024-05-23        | 2024-05-24   |       32,500 | no Yahoo data for the symbol |
| Gary C. Peters       | OTIS     | OTIS           | Sale (Full)        | 2024-08-05        | 2024-08-06   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | CARR     | CARR           | Sale (Full)        | 2024-08-05        | 2024-08-06   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | LEG      | LEG            | Sale (Full)        | 2024-11-14        | 2024-11-15   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | LW       | LW             | Sale (Full)        | 2024-11-14        | 2024-11-15   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | IVZ      | IVZ            | Sale (Full)        | 2024-11-14        | 2024-11-15   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | OGN      | OGN            | Sale (Full)        | 2025-11-24        | 2025-11-25   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | CAG      | CAG            | Purchase           | 2025-12-04        | 2025-12-05   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | VZ       | VZ             | Purchase           | 2026-01-07        | 2026-01-08   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | WPC      | WPC            | Purchase           | 2026-01-20        | 2026-01-21   |       32,500 | no Yahoo data for the symbol |
| Gary C. Peters       | SWK      | SWK            | Purchase           | 2026-01-20        | 2026-01-21   |       32,500 | no Yahoo data for the symbol |
| Gary C. Peters       | CTVA     | CTVA           | Sale (Full)        | 2026-05-11        | 2026-05-12   |       32,500 | no Yahoo data for the symbol |
| Gary C. Peters       | SJM      | SJM            | Purchase           | 2026-05-11        | 2026-05-12   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | PEP      | PEP            | Purchase           | 2026-05-11        | 2026-05-12   |       32,500 | no Yahoo data for the symbol |
| Gary C. Peters       | KHC      | KHC            | Purchase           | 2026-06-11        | 2026-06-12   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | T        | T              | Purchase           | 2026-07-02        | 2026-07-06   |        8,000 | no Yahoo data for the symbol |
| Gary C. Peters       | O        | O              | Purchase           | 2026-08-07        | 2026-08-10   |        8,000 | no Yahoo data for the symbol |
| J.D. Vance           | WMT      | WMT            | Sale (Full)        | 2023-10-23        | 2023-10-24   |       75,000 | no Yahoo data for the symbol |
| James C. Justice     | PEBO     | PEBO           | Sale (Full)        | 2025-10-10        | 2025-10-13   |      375,000 | no Yahoo data for the symbol |
| Jerry Moran          | USB      | USB            | Sale (Partial)     | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | MSFT     | MSFT           | Sale (Partial)     | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | KR       | KR             | Sale (Partial)     | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | GILD     | GILD           | Sale (Full)        | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | FB       | META           | Sale (Partial)     | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | XOM      | XOM            | Sale (Partial)     | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | DVA      | DVA            | Sale (Partial)     | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | CVS      | CVS            | Sale (Partial)     | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | BRK-B    | BRK-B          | Sale (Partial)     | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | GOOG     | GOOG           | Sale (Partial)     | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | VZ       | VZ             | Purchase           | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | PII      | PII            | Purchase           | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | PFE      | PFE            | Purchase           | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | KMB      | KMB            | Purchase           | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | CMCSA    | CMCSA          | Purchase           | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | CSCO     | CSCO           | Purchase           | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | CI       | CI             | Purchase           | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | BK       | BNY            | Purchase           | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | VZ       | VZ             | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | USB      | USB            | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | CI       | CI             | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | PII      | PII            | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | PFE      | PFE            | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | MSFT     | MSFT           | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | META     | META           | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | KR       | KR             | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | KMB      | KMB            | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | JNJ      | JNJ            | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | INTC     | INTC           | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | HAL      | HAL            | Sale (Full)        | 2024-01-17        | 2024-01-18   |       32,500 | no Yahoo data for the symbol |
| Jerry Moran          | XOM      | XOM            | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | DVA      | DVA            | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | CVS      | CVS            | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | CMCSA    | CMCSA          | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | CSCO     | CSCO           | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | CVX      | CVX            | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | BRK-B    | BRK-B          | Purchase           | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | BK       | BNY            | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | GOOG     | GOOG           | Sale (Full)        | 2024-01-17        | 2024-01-18   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | BRK-B    | BRK-B          | Sale (Partial)     | 2024-08-29        | 2024-08-30   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | BRK-B    | BRK-B          | Sale (Partial)     | 2024-08-29        | 2024-08-30   |       32,500 | no Yahoo data for the symbol |
| Jerry Moran          | BRK-B    | BRK-B          | Purchase           | 2025-01-18        | 2025-01-21   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | GOOG     | GOOG           | Purchase           | 2025-06-18        | 2025-06-20   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | GOOG     | GOOG           | Purchase           | 2025-06-18        | 2025-06-20   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | BRK-B    | BRK-B          | Purchase           | 2025-10-27        | 2025-10-28   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | GOOG     | GOOG           | Sale (Partial)     | 2025-10-27        | 2025-10-28   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | BRK-B    | BRK-B          | Purchase           | 2026-06-25        | 2026-06-26   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | GOOG     | GOOG           | Sale (Partial)     | 2026-06-25        | 2026-06-26   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | BRK-B    | BRK-B          | Purchase           | 2026-06-25        | 2026-06-26   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | GOOG     | GOOG           | Purchase           | 2026-07-21        | 2026-07-22   |        8,000 | no Yahoo data for the symbol |
| Jerry Moran          | BRK-B    | BRK-B          | Purchase           | 2026-07-21        | 2026-07-22   |       32,500 | no Yahoo data for the symbol |
| Jim Banks            | YUM      | YUM            | Sale (Full)        | 2025-03-10        | 2025-03-11   |        8,000 | no Yahoo data for the symbol |
| Jim Banks            | RBLX     | RBLX           | Sale (Full)        | 2025-06-26        | 2025-06-27   |        8,000 | no Yahoo data for the symbol |
| Jim Banks            | SBUX     | SBUX           | Purchase           | 2025-08-10        | 2025-08-11   |        8,000 | no Yahoo data for the symbol |
| Jim Banks            | SBUX     | SBUX           | Sale (Full)        | 2026-04-20        | 2026-04-21   |        8,000 | no Yahoo data for the symbol |
| Jim Banks            | PTON     | PTON           | Sale (Full)        | 2026-06-07        | 2026-06-08   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FEP      | FEP            | Sale (Full)        | 2023-09-07        | 2023-09-08   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | SHY      | SHY            | Sale (Partial)     | 2023-12-12        | 2023-12-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CMBS     | CMBS           | Sale (Partial)     | 2023-12-12        | 2023-12-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLT      | TLT            | Sale (Partial)     | 2023-12-12        | 2023-12-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GBIL     | GBIL           | Sale (Partial)     | 2023-12-12        | 2023-12-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GIGB     | GIGB           | Sale (Partial)     | 2023-12-12        | 2023-12-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JMBS     | JMBS           | Purchase           | 2023-12-12        | 2023-12-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SHY      | SHY            | Purchase           | 2023-12-12        | 2023-12-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLH      | TLH            | Purchase           | 2023-12-12        | 2023-12-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLT      | TLT            | Purchase           | 2023-12-12        | 2023-12-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MBB      | MBB            | Purchase           | 2023-12-12        | 2023-12-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LRCX     | LRCX           | Sale (Partial)     | 2024-01-08        | 2024-01-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GBIL     | GBIL           | Sale (Partial)     | 2024-01-08        | 2024-01-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PFE      | PFE            | Purchase           | 2024-01-08        | 2024-01-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PALL     | PALL           | Purchase           | 2024-01-08        | 2024-01-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PALL     | PALL           | Purchase           | 2024-01-08        | 2024-01-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PPLT     | PPLT           | Purchase           | 2024-01-08        | 2024-01-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EFA      | EFA            | Sale (Partial)     | 2024-05-07        | 2024-05-08   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | CMBS     | CMBS           | Sale (Partial)     | 2024-05-07        | 2024-05-08   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JMBS     | JMBS           | Purchase           | 2024-05-07        | 2024-05-08   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SCZ      | SCZ            | Purchase           | 2024-05-07        | 2024-05-08   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | SCHP     | SCHP           | Sale (Partial)     | 2024-05-08        | 2024-05-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IEF      | IEF            | Sale (Partial)     | 2024-05-08        | 2024-05-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLH      | TLH            | Purchase           | 2024-05-08        | 2024-05-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLT      | TLT            | Purchase           | 2024-05-08        | 2024-05-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | HES      | HES            | Sale (Full)        | 2024-05-08        | 2024-05-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GIGB     | GIGB           | Purchase           | 2024-06-05        | 2024-06-06   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVW      | IVW            | Sale (Partial)     | 2024-06-05        | 2024-06-06   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EFA      | EFA            | Sale (Partial)     | 2024-06-05        | 2024-06-06   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VEA      | VEA            | Purchase           | 2024-07-11        | 2024-07-12   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | SCHP     | SCHP           | Purchase           | 2024-07-11        | 2024-07-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MSFT     | MSFT           | Purchase           | 2024-07-11        | 2024-07-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JMBS     | JMBS           | Purchase           | 2024-07-11        | 2024-07-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLH      | TLH            | Purchase           | 2024-07-11        | 2024-07-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GEM      | GEM            | Purchase           | 2024-07-11        | 2024-07-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MDY      | MDY            | Sale (Partial)     | 2024-07-11        | 2024-07-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVV      | IVV            | Sale (Partial)     | 2024-07-11        | 2024-07-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EFA      | EFA            | Sale (Partial)     | 2024-07-11        | 2024-07-12   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | IEF      | IEF            | Sale (Partial)     | 2024-07-11        | 2024-07-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SHY      | SHY            | Sale (Partial)     | 2024-07-11        | 2024-07-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CMCSA    | CMCSA          | Sale (Full)        | 2024-07-11        | 2024-07-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VEA      | VEA            | Purchase           | 2024-08-06        | 2024-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MSI      | MSI            | Purchase           | 2024-08-06        | 2024-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GOOGL    | GOOGL          | Purchase           | 2024-08-06        | 2024-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MDY      | MDY            | Sale (Partial)     | 2024-08-06        | 2024-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LRCX     | LRCX           | Sale (Partial)     | 2024-08-06        | 2024-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SCHP     | SCHP           | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JMBS     | JMBS           | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVV      | IVV            | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IEF      | IEF            | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SHY      | SHY            | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLH      | TLH            | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CMBS     | CMBS           | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IEI      | IEI            | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLT      | TLT            | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MBB      | MBB            | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Purchase           | 2024-10-18        | 2024-10-21   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | GIGB     | GIGB           | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FTGC     | FTGC           | Purchase           | 2024-10-18        | 2024-10-21   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | PPLT     | PPLT           | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PALL     | PALL           | Purchase           | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FI       | FISV           | Sale (Partial)     | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VEA      | VEA            | Sale (Partial)     | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VNQI     | VNQI           | Sale (Partial)     | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MDY      | MDY            | Sale (Partial)     | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TPYP     | TPYP           | Sale (Partial)     | 2024-10-18        | 2024-10-21   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | IVV      | IVV            | Sale (Partial)     | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IWM      | IWM            | Sale (Partial)     | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EFA      | EFA            | Sale (Partial)     | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EMLP     | EMLP           | Sale (Partial)     | 2024-10-18        | 2024-10-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VWO      | VWO            | Sale (Partial)     | 2024-12-17        | 2024-12-18   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SWKS     | SWKS           | Sale (Full)        | 2024-12-17        | 2024-12-18   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CRM      | CRM            | Purchase           | 2025-02-08        | 2025-02-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | NVDA     | NVDA           | Purchase           | 2025-02-08        | 2025-02-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | NRG      | NRG            | Purchase           | 2025-02-08        | 2025-02-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MA       | MA             | Purchase           | 2025-02-08        | 2025-02-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Purchase           | 2025-02-08        | 2025-02-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Purchase           | 2025-02-08        | 2025-02-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVW      | IVW            | Sale (Partial)     | 2025-02-08        | 2025-02-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | QQQ      | QQQ            | Sale (Full)        | 2025-02-08        | 2025-02-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | HPQ      | HPQ            | Sale (Full)        | 2025-02-08        | 2025-02-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EBAY     | EBAY           | Sale (Full)        | 2025-02-08        | 2025-02-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CSCO     | CSCO           | Sale (Full)        | 2025-02-08        | 2025-02-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | URNM     | URNM           | Purchase           | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LITP     | LITP           | Purchase           | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | NVDA     | NVDA           | Purchase           | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MSI      | MSI            | Purchase           | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MSFT     | MSFT           | Purchase           | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MSFT     | MSFT           | Purchase           | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MA       | MA             | Purchase           | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Purchase           | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | ECL      | ECL            | Purchase           | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | BSX      | BSX            | Purchase           | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GOOGL    | GOOGL          | Purchase           | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | QSR      | QSR            | Sale (Full)        | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PFE      | PFE            | Sale (Full)        | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LRCX     | LRCX           | Sale (Partial)     | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JPM      | JPM            | Sale (Partial)     | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVW      | IVW            | Sale (Partial)     | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVW      | IVW            | Sale (Partial)     | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FTGC     | FTGC           | Sale (Partial)     | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EMLP     | EMLP           | Sale (Partial)     | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | DIS      | DIS            | Sale (Full)        | 2025-03-06        | 2025-03-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Purchase           | 2025-04-20        | 2025-04-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Purchase           | 2025-04-20        | 2025-04-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVW      | IVW            | Sale (Partial)     | 2025-04-20        | 2025-04-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | DTE      | DTE            | Sale (Full)        | 2025-04-20        | 2025-04-21   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | UNH      | UNH            | Purchase           | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | ORCL     | ORCL           | Purchase           | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MSFT     | MSFT           | Purchase           | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MSFT     | MSFT           | Purchase           | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | META     | META           | Purchase           | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | HYG      | HYG            | Purchase           | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | COLPAL   | COLPAL         | Purchase           | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FTGC     | FTGC           | Purchase           | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CRM      | CRM            | Sale (Partial)     | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LRCX     | LRCX           | Sale (Partial)     | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JPM      | JPM            | Sale (Partial)     | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVW      | IVW            | Sale (Full)        | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SHY      | SHY            | Sale (Partial)     | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GILD     | GILD           | Sale (Full)        | 2025-05-14        | 2025-05-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | RTX      | RTX            | Purchase           | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | NVDA     | NVDA           | Purchase           | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | META     | META           | Purchase           | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | META     | META           | Purchase           | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | HD       | HD             | Purchase           | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | HD       | HD             | Purchase           | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GOOGL    | GOOGL          | Purchase           | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VLO      | VLO            | Sale (Full)        | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | NRG      | NRG            | Sale (Partial)     | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LOW      | LOW            | Sale (Partial)     | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Sale (Partial)     | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GD       | GD             | Sale (Partial)     | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FBIN     | FBIN           | Sale (Full)        | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | DTE      | DTE            | Sale (Full)        | 2025-06-14        | 2025-06-16   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Purchase           | 2025-07-09        | 2025-07-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | UNH      | UNH            | Sale (Full)        | 2025-07-09        | 2025-07-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MU       | MU             | Sale (Partial)     | 2025-07-09        | 2025-07-10   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | WMT      | WMT            | Purchase           | 2025-08-06        | 2025-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GIGB     | GIGB           | Purchase           | 2025-08-06        | 2025-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GE       | GE             | Purchase           | 2025-08-06        | 2025-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | BRK-B    | BRK-B          | Purchase           | 2025-08-06        | 2025-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MDLZ     | MDLZ           | Sale (Partial)     | 2025-08-06        | 2025-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MU       | MU             | Sale (Partial)     | 2025-08-06        | 2025-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JPM      | JPM            | Sale (Partial)     | 2025-08-06        | 2025-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | HYG      | HYG            | Sale (Full)        | 2025-08-06        | 2025-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GD       | GD             | Sale (Partial)     | 2025-08-06        | 2025-08-07   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VNQI     | VNQI           | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SCHP     | SCHP           | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | NVDA     | NVDA           | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LLY      | LLY            | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LLY      | LLY            | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JMBS     | JMBS           | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IWM      | IWM            | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IEF      | IEF            | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SHY      | SHY            | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLH      | TLH            | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CMBS     | CMBS           | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IEI      | IEI            | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLT      | TLT            | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MBB      | MBB            | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GEM      | GEM            | Purchase           | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VEA      | VEA            | Sale (Partial)     | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | URNM     | URNM           | Sale (Partial)     | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MU       | MU             | Sale (Partial)     | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVV      | IVV            | Sale (Partial)     | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EFA      | EFA            | Sale (Partial)     | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SLV      | SLV            | Sale (Partial)     | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Sale (Partial)     | 2025-09-12        | 2025-09-15   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | GIGB     | GIGB           | Sale (Partial)     | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GEM      | GEM            | Sale (Partial)     | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EMLP     | EMLP           | Sale (Partial)     | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PPLT     | PPLT           | Sale (Partial)     | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PALL     | PALL           | Sale (Partial)     | 2025-09-12        | 2025-09-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SCHP     | SCHP           | Purchase           | 2025-10-10        | 2025-10-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IEF      | IEF            | Purchase           | 2025-10-10        | 2025-10-13   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | SHY      | SHY            | Purchase           | 2025-10-10        | 2025-10-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IEI      | IEI            | Purchase           | 2025-10-10        | 2025-10-13   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | ETN      | ETN            | Purchase           | 2025-10-10        | 2025-10-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GOOGL    | GOOGL          | Purchase           | 2025-10-10        | 2025-10-13   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | ORCL     | ORCL           | Sale (Partial)     | 2025-10-10        | 2025-10-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MU       | MU             | Sale (Partial)     | 2025-10-10        | 2025-10-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JMBS     | JMBS           | Sale (Partial)     | 2025-10-10        | 2025-10-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CMBS     | CMBS           | Sale (Partial)     | 2025-10-10        | 2025-10-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLT      | TLT            | Sale (Partial)     | 2025-10-10        | 2025-10-13   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | MBB      | MBB            | Sale (Partial)     | 2025-10-10        | 2025-10-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GBIL     | GBIL           | Sale (Partial)     | 2025-10-10        | 2025-10-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GIGB     | GIGB           | Sale (Partial)     | 2025-10-10        | 2025-10-13   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | META     | META           | Purchase           | 2025-11-15        | 2025-11-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FTGC     | FTGC           | Purchase           | 2025-11-15        | 2025-11-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EIPI     | EIPI           | Purchase           | 2025-11-15        | 2025-11-17   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | COST     | COST           | Purchase           | 2025-11-15        | 2025-11-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TPYP     | TPYP           | Sale (Partial)     | 2025-11-15        | 2025-11-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | URNM     | URNM           | Sale (Full)        | 2025-11-15        | 2025-11-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LITP     | LITP           | Sale (Partial)     | 2025-11-15        | 2025-11-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | OMC      | OMC            | Sale (Partial)     | 2025-11-15        | 2025-11-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SLV      | SLV            | Sale (Partial)     | 2025-11-15        | 2025-11-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IQV      | IQV            | Sale (Partial)     | 2025-11-15        | 2025-11-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EMLP     | EMLP           | Sale (Full)        | 2025-11-15        | 2025-11-17   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | COLPAL   | COLPAL         | Sale (Full)        | 2025-11-15        | 2025-11-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VEA      | VEA            | Purchase           | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VWO      | VWO            | Purchase           | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MDY      | MDY            | Purchase           | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PYPL     | PYPL           | Purchase           | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | META     | META           | Purchase           | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JMBS     | JMBS           | Purchase           | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CMBS     | CMBS           | Purchase           | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MBB      | MBB            | Purchase           | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GIGB     | GIGB           | Purchase           | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VEA      | VEA            | Sale (Partial)     | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VNQI     | VNQI           | Sale (Partial)     | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TPYP     | TPYP           | Sale (Partial)     | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CRM      | CRM            | Sale (Full)        | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LLY      | LLY            | Sale (Partial)     | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVV      | IVV            | Sale (Partial)     | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IWM      | IWM            | Sale (Partial)     | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EFA      | EFA            | Sale (Partial)     | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GEM      | GEM            | Sale (Partial)     | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FISV     | FISV           | Sale (Partial)     | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FTGC     | FTGC           | Sale (Partial)     | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EIPI     | EIPI           | Sale (Partial)     | 2025-12-08        | 2025-12-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | WFC      | WFC            | Purchase           | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SMCI     | SMCI           | Purchase           | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SPYM     | SPYM           | Purchase           | 2026-01-13        | 2026-01-14   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | MSFT     | MSFT           | Purchase           | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVW      | IVW            | Purchase           | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IJR      | IJR            | Purchase           | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SMCI     | SMCI           | Sale (Full)        | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | KRE      | KRE            | Sale (Full)        | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MSI      | MSI            | Sale (Partial)     | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SLV      | SLV            | Sale (Partial)     | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Sale (Partial)     | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | BSX      | BSX            | Sale (Partial)     | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PPLT     | PPLT           | Sale (Partial)     | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PALL     | PALL           | Sale (Partial)     | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | V        | V              | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VNQI     | VNQI           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TPYP     | TPYP           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LITP     | LITP           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PYPL     | PYPL           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | NFLX     | NFLX           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JMBS     | JMBS           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVV      | IVV            | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CMBS     | CMBS           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MBB      | MBB            | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GIGB     | GIGB           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GEM      | GEM            | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FTGC     | FTGC           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EIPI     | EIPI           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | XOM      | XOM            | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | ETN      | ETN            | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | DIS      | DIS            | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | DXCM     | DXCM           | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CVS      | CVS            | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CAT      | CAT            | Purchase           | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | UNP      | UNP            | Sale (Partial)     | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SPYM     | SPYM           | Sale (Partial)     | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MDY      | MDY            | Sale (Partial)     | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | OMC      | OMC            | Sale (Full)        | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | OMC      | OMC            | Sale (Partial)     | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MU       | MU             | Sale (Partial)     | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MU       | MU             | Sale (Partial)     | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LRCX     | LRCX           | Sale (Partial)     | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVW      | IVW            | Sale (Full)        | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IWM      | IWM            | Sale (Partial)     | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SLV      | SLV            | Sale (Full)        | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FISV     | FISV           | Sale (Full)        | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PPLT     | PPLT           | Sale (Full)        | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PALL     | PALL           | Sale (Full)        | 2026-02-15        | 2026-02-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | UBER     | UBER           | Purchase           | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | NTAP     | NTAP           | Purchase           | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MSFT     | MSFT           | Purchase           | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | KR       | KR             | Purchase           | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IEF      | IEF            | Purchase           | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLH      | TLH            | Purchase           | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EMB      | EMB            | Purchase           | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CMBS     | CMBS           | Purchase           | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GIGB     | GIGB           | Purchase           | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | XTWO     | XTWO           | Purchase           | 2026-03-06        | 2026-03-09   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | UNP      | UNP            | Sale (Partial)     | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PG       | PG             | Sale (Partial)     | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JMBS     | JMBS           | Sale (Partial)     | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SHY      | SHY            | Sale (Full)        | 2026-03-06        | 2026-03-09   |       32,500 | no Yahoo data for the symbol |
| John Boozman         | MBB      | MBB            | Sale (Partial)     | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VEA      | VEA            | Purchase           | 2026-04-14        | 2026-04-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SPYM     | SPYM           | Purchase           | 2026-04-14        | 2026-04-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | NVDA     | NVDA           | Purchase           | 2026-04-14        | 2026-04-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MSFT     | MSFT           | Purchase           | 2026-04-14        | 2026-04-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FTGC     | FTGC           | Purchase           | 2026-04-14        | 2026-04-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TPYP     | TPYP           | Sale (Partial)     | 2026-04-14        | 2026-04-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JNJ      | JNJ            | Sale (Partial)     | 2026-04-14        | 2026-04-15   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | DVN      | DVN            | Purchase           | 2026-05-08        | 2026-05-11   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CEG      | CEG            | Purchase           | 2026-05-08        | 2026-05-11   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TBLL     | TBLL           | Sale (Partial)     | 2026-05-08        | 2026-05-11   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GOOGL    | GOOGL          | Purchase           | 2026-05-11        | 2026-05-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | DTE      | DTE            | Sale (Partial)     | 2026-05-11        | 2026-05-12   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SCHP     | SCHP           | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PLTR     | PLTR           | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JMBS     | JMBS           | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IEF      | IEF            | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TLH      | TLH            | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CMBS     | CMBS           | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | MBB      | MBB            | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GBIL     | GBIL           | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GIGB     | GIGB           | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GIGB     | GIGB           | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | XFIV     | XFIV           | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | XFIV     | XFIV           | Purchase           | 2026-06-16        | 2026-06-17   |       75,000 | no Yahoo data for the symbol |
| John Boozman         | XTWO     | XTWO           | Purchase           | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VEA      | VEA            | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | VNQI     | VNQI           | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | LITP     | LITP           | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IVV      | IVV            | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SCHP     | SCHP           | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JMBS     | JMBS           | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SPYM     | SPYM           | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IWM      | IWM            | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EFA      | EFA            | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CMBS     | CMBS           | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IEI      | IEI            | Sale (Full)        | 2026-06-16        | 2026-06-17   |       75,000 | no Yahoo data for the symbol |
| John Boozman         | MBB      | MBB            | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | GEM      | GEM            | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FTGC     | FTGC           | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EIPI     | EIPI           | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | ECL      | ECL            | Sale (Partial)     | 2026-06-16        | 2026-06-17   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IGV      | IGV            | Purchase           | 2026-07-13        | 2026-07-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PALL     | PALL           | Purchase           | 2026-07-13        | 2026-07-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SCHP     | SCHP           | Purchase           | 2026-07-13        | 2026-07-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CEG      | CEG            | Purchase           | 2026-07-13        | 2026-07-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | UNH      | UNH            | Purchase           | 2026-07-13        | 2026-07-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TPYP     | TPYP           | Sale (Partial)     | 2026-07-13        | 2026-07-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | FTGC     | FTGC           | Sale (Partial)     | 2026-07-13        | 2026-07-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | IEF      | IEF            | Sale (Partial)     | 2026-07-13        | 2026-07-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | BSX      | BSX            | Sale (Partial)     | 2026-07-13        | 2026-07-14   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | PYPL     | PYPL           | Purchase           | 2026-08-17        | 2026-08-18   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SPYM     | SPYM           | Purchase           | 2026-08-17        | 2026-08-18   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | EL       | EL             | Purchase           | 2026-08-17        | 2026-08-18   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CVX      | CVX            | Purchase           | 2026-08-17        | 2026-08-18   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | SPYM     | SPYM           | Purchase           | 2026-08-17        | 2026-08-18   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CBOE     | CBOE           | Sale (Full)        | 2026-08-17        | 2026-08-18   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | JPM      | JPM            | Sale (Partial)     | 2026-08-17        | 2026-08-18   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | HD       | HD             | Sale (Full)        | 2026-08-17        | 2026-08-18   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | TRV      | TRV            | Sale (Full)        | 2026-08-17        | 2026-08-18   |        8,000 | no Yahoo data for the symbol |
| John Boozman         | CBOE     | CBOE           | Purchase           | 2026-08-20        | 2026-08-21   |        8,000 | no Yahoo data for the symbol |
| John Kennedy         | NLY      | NLY            | Purchase           | 2025-05-08        | 2025-05-09   |        8,000 | no Yahoo data for the symbol |
| John Thune           | IRT      | IRT            | Sale (Full)        | 2022-05-12        | 2022-05-13   |       32,500 | no Yahoo data for the symbol |
| John W. Hickenlooper | CVX      | CVX            | Sale (Full)        | 2021-11-19        | 2021-11-22   |      175,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | PYPL     | PYPL           | Sale (Full)        | 2021-12-10        | 2021-12-13   |      375,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | NVDA     | NVDA           | Sale (Full)        | 2021-12-10        | 2021-12-13   |      750,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | MSFT     | MSFT           | Sale (Full)        | 2021-12-10        | 2021-12-13   |      375,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | FB       | META           | Sale (Full)        | 2021-12-10        | 2021-12-13   |      375,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | GOOGL    | GOOGL          | Sale (Full)        | 2021-12-10        | 2021-12-13   |      375,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | VZ       | VZ             | Sale (Full)        | 2023-06-15        | 2023-06-16   |      175,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | INTC     | INTC           | Sale (Full)        | 2023-06-15        | 2023-06-16   |      175,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | SDZNY    | SDZNY          | Sale (Full)        | 2025-05-15        | 2025-05-16   |        8,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | INTU     | INTU           | Purchase           | 2025-10-06        | 2025-10-07   |      175,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | PEP      | PEP            | Sale (Full)        | 2025-10-06        | 2025-10-07   |      175,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | PANW     | PANW           | Purchase           | 2025-10-06        | 2025-10-07   |      175,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | LOW      | LOW            | Sale (Partial)     | 2026-02-06        | 2026-02-09   |       75,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | TJX      | TJX            | Sale (Partial)     | 2026-02-06        | 2026-02-09   |       75,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | ETN      | ETN            | Purchase           | 2026-02-06        | 2026-02-09   |       75,000 | no Yahoo data for the symbol |
| John W. Hickenlooper | UBER     | UBER           | Purchase           | 2026-02-06        | 2026-02-09   |      175,000 | no Yahoo data for the symbol |
| Katie Boyd Britt     | ONEW     | ONEW           | Sale (Full)        | 2024-07-29        | 2024-07-30   |        8,000 | no Yahoo data for the symbol |
| Lindsey Graham       | VTIP     | VTIP           | Sale (Full)        | 2022-07-13        | 2022-07-14   |       32,500 | no Yahoo data for the symbol |
| Lindsey Graham       | IBDO     | IBDO           | Purchase           | 2022-07-13        | 2022-07-14   |        8,000 | no Yahoo data for the symbol |
| Lindsey Graham       | IBDQ     | IBDQ           | Purchase           | 2022-07-13        | 2022-07-14   |       32,500 | no Yahoo data for the symbol |
| Lindsey Graham       | VIG      | VIG            | Sale (Partial)     | 2024-01-26        | 2024-01-29   |       32,500 | no Yahoo data for the symbol |
| Lindsey Graham       | USFR     | USFR           | Purchase           | 2024-01-26        | 2024-01-29   |       32,500 | no Yahoo data for the symbol |
| Lindsey Graham       | VIG      | VIG            | Sale (Partial)     | 2024-05-08        | 2024-05-09   |       32,500 | no Yahoo data for the symbol |
| Lindsey Graham       | USFR     | USFR           | Purchase           | 2024-05-08        | 2024-05-09   |       32,500 | no Yahoo data for the symbol |
| Lindsey Graham       | XONE     | XONE           | Purchase           | 2025-07-14        | 2025-07-15   |       32,500 | no Yahoo data for the symbol |
| Lindsey Graham       | BSCV     | BSCV           | Purchase           | 2025-07-14        | 2025-07-15   |       32,500 | no Yahoo data for the symbol |
| Lindsey Graham       | BSCP     | BSCP           | Sale (Full)        | 2026-01-06        | 2026-01-07   |       32,500 | no Yahoo data for the symbol |
| Lindsey Graham       | BSCQ     | BSCQ           | Purchase           | 2026-01-06        | 2026-01-07   |       32,500 | no Yahoo data for the symbol |
| Lindsey Graham       | IBDQ     | IBDQ           | Sale (Full)        | 2026-01-06        | 2026-01-07   |       32,500 | no Yahoo data for the symbol |
| Marco Rubio          | CSCO     | CSCO           | Sale (Full)        | 2025-02-06        | 2025-02-07   |        8,000 | no Yahoo data for the symbol |
| Marco Rubio          | KO       | KO             | Sale (Full)        | 2025-02-06        | 2025-02-07   |        8,000 | no Yahoo data for the symbol |
| Maria Cantwell       | RNWK     | RNWK           | Sale (Full)        | 2023-01-13        | 2023-01-17   |       32,500 | no Yahoo data for the symbol |
| Mark R. Warner       | ROAD     | ROAD           | Sale (Full)        | 2021-11-17        | 2021-11-18   |       75,000 | no Yahoo data for the symbol |
| Mark R. Warner       | ROAD     | ROAD           | Sale (Full)        | 2022-02-18        | 2022-02-22   |      175,000 | no Yahoo data for the symbol |
| Mark R. Warner       | ROAD     | ROAD           | Sale (Full)        | 2023-09-12        | 2023-09-13   |      375,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | GOOGL    | GOOGL          | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | ELV      | ELV            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | BRK-B    | BRK-B          | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | BLK      | BLK            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | BSX      | BSX            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CSX      | CSX            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CAT      | CAT            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CVX      | CVX            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CMG      | CMG            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | KO       | KO             | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CMCSA    | CMCSA          | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | COP      | COP            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | STZ      | STZ            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | COST     | COST           | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | DHR      | DHR            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | DE       | DE             | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | EW       | EW             | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | EMR      | EMR            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | META     | META           | Purchase           | 2023-10-12        | 2023-10-13   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | FI       | FISV           | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | GS       | GS             | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | HLT      | HLT            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | HD       | HD             | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | HON      | HON            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | ICE      | ICE            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | JPM      | JPM            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | KLAC     | KLAC           | Purchase           | 2023-10-12        | 2023-10-13   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRCX     | LRCX           | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LLY      | LLY            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | MA       | MA             | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | MSFT     | MSFT           | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | NKE      | NKE            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | NVDA     | NVDA           | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | PANW     | PANW           | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | PEP      | PEP            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | PG       | PG             | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | RTX      | RTX            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | SPGI     | SPGI           | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CRM      | CRM            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | SHW      | SHW            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | SBUX     | SBUX           | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | TMUS     | TMUS           | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | TXN      | TXN            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | TMO      | TMO            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | UNP      | UNP            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | UNH      | UNH            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | VLO      | VLO            | Purchase           | 2023-10-12        | 2023-10-13   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | V        | V              | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | ZTS      | ZTS            | Purchase           | 2023-10-12        | 2023-10-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | GOOGL    | GOOGL          | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ELV      | ELV            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | BRK-B    | BRK-B          | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | BLK      | BLK            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | BSX      | BSX            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CSX      | CSX            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CAT      | CAT            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CVX      | CVX            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CMG      | CMG            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | KO       | KO             | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CMCSA    | CMCSA          | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | COP      | COP            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | STZ      | STZ            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | COST     | COST           | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | DE       | DE             | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | EW       | EW             | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | EMR      | EMR            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | META     | META           | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | FI       | FISV           | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | GS       | GS             | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | HLT      | HLT            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | HD       | HD             | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | HON      | HON            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ICE      | ICE            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | JPM      | JPM            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRCX     | LRCX           | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | LLY      | LLY            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | MA       | MA             | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | MSFT     | MSFT           | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | NKE      | NKE            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | NVDA     | NVDA           | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | PANW     | PANW           | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | PEP      | PEP            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | PG       | PG             | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | RTX      | RTX            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | SPGI     | SPGI           | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CRM      | CRM            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | SHW      | SHW            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | SBUX     | SBUX           | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | TXN      | TXN            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | TMO      | TMO            | Purchase           | 2023-11-01        | 2023-11-02   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | UNP      | UNP            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | UNH      | UNH            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | V        | V              | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ZTS      | ZTS            | Purchase           | 2023-11-01        | 2023-11-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | VLTO     | VLTO           | Sale (Partial)     | 2023-12-28        | 2023-12-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ZTS      | ZTS            | Purchase           | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | SFM      | SFM            | Purchase           | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | OLLI     | OLLI           | Purchase           | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | GS       | GS             | Purchase           | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | FRPT     | FRPT           | Purchase           | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ETN      | ETN            | Purchase           | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ELF      | ELF            | Purchase           | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CYBR     | CYBR           | Purchase           | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | BMI      | BMI            | Purchase           | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | META     | META           | Purchase           | 2024-01-26        | 2024-01-29   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRCX     | LRCX           | Purchase           | 2024-01-26        | 2024-01-29   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | NVDA     | NVDA           | Purchase           | 2024-01-26        | 2024-01-29   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | SHOP     | SHOP           | Sale (Partial)     | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | PYPL     | PYPL           | Sale (Partial)     | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | PODD     | PODD           | Sale (Partial)     | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | INST     | INST           | Sale (Partial)     | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | HUBB     | HUBB           | Sale (Partial)     | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | FN       | FN             | Sale (Partial)     | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | FCFS     | FCFS           | Sale (Partial)     | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | EXLS     | EXLS           | Sale (Partial)     | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CTVA     | CTVA           | Sale (Partial)     | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CELH     | CELH           | Sale (Partial)     | 2024-01-26        | 2024-01-29   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ZTS      | ZTS            | Sale (Partial)     | 2024-05-01        | 2024-05-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ZTS      | ZTS            | Sale (Partial)     | 2024-05-02        | 2024-05-03   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | IWB      | IWB            | Sale (Partial)     | 2024-06-07        | 2024-06-10   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | IWB      | IWB            | Sale (Partial)     | 2024-06-07        | 2024-06-10   |      175,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | IWB      | IWB            | Sale (Partial)     | 2024-07-12        | 2024-07-15   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CMCSA    | CMCSA          | Sale (Partial)     | 2024-07-12        | 2024-07-15   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | PH       | PH             | Purchase           | 2024-07-12        | 2024-07-15   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | NKE      | NKE            | Sale (Partial)     | 2024-07-12        | 2024-07-15   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | IWB      | IWB            | Sale (Partial)     | 2024-07-12        | 2024-07-15   |      750,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | EW       | EW             | Sale (Partial)     | 2024-09-19        | 2024-09-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | IQV      | IQV            | Purchase           | 2024-09-19        | 2024-09-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | SBUX     | SBUX           | Sale (Partial)     | 2024-09-19        | 2024-09-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | TJX      | TJX            | Purchase           | 2024-09-19        | 2024-09-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRN      | LRN            | Purchase           | 2024-11-08        | 2024-11-11   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | HIYS     | HIYS           | Purchase           | 2024-12-03        | 2024-12-04   |      375,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | IEFA     | IEFA           | Purchase           | 2024-12-19        | 2024-12-20   |      175,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | IEMG     | IEMG           | Purchase           | 2024-12-19        | 2024-12-20   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | EZU      | EZU            | Purchase           | 2024-12-19        | 2024-12-20   |      175,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ETN      | ETN            | Sale (Full)        | 2024-12-31        | 2025-01-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | SFM      | SFM            | Sale (Full)        | 2024-12-31        | 2025-01-02   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | OLLI     | OLLI           | Sale (Full)        | 2024-12-31        | 2025-01-02   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRN      | LRN            | Sale (Full)        | 2024-12-31        | 2025-01-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | GS       | GS             | Sale (Full)        | 2024-12-31        | 2025-01-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | FRPT     | FRPT           | Sale (Full)        | 2024-12-31        | 2025-01-02   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | ELF      | ELF            | Sale (Full)        | 2024-12-31        | 2025-01-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CYBR     | CYBR           | Sale (Full)        | 2024-12-31        | 2025-01-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | BMI      | BMI            | Sale (Full)        | 2024-12-31        | 2025-01-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | PEP      | PEP            | Sale (Full)        | 2024-12-31        | 2025-01-02   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | VNQ      | VNQ            | Purchase           | 2025-01-03        | 2025-01-06   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | PDBC     | PDBC           | Sale (Full)        | 2025-01-03        | 2025-01-06   |      375,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | IEMG     | IEMG           | Purchase           | 2025-01-03        | 2025-01-06   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | IEFA     | IEFA           | Sale (Partial)     | 2025-01-31        | 2025-02-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | EZU      | EZU            | Sale (Partial)     | 2025-01-31        | 2025-02-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | WAB      | WAB            | Purchase           | 2025-01-31        | 2025-02-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | PRMB     | PRMB           | Purchase           | 2025-01-31        | 2025-02-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | MTZ      | MTZ            | Purchase           | 2025-01-31        | 2025-02-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRN      | LRN            | Purchase           | 2025-01-31        | 2025-02-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | IRM      | IRM            | Purchase           | 2025-01-31        | 2025-02-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | GS       | GS             | Purchase           | 2025-01-31        | 2025-02-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | DELL     | DELL           | Purchase           | 2025-01-31        | 2025-02-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CRDO     | CRDO           | Purchase           | 2025-01-31        | 2025-02-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | COHR     | COHR           | Purchase           | 2025-01-31        | 2025-02-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | WAB      | WAB            | Purchase           | 2025-02-27        | 2025-02-28   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | PRMB     | PRMB           | Purchase           | 2025-02-27        | 2025-02-28   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | MTZ      | MTZ            | Purchase           | 2025-02-27        | 2025-02-28   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRN      | LRN            | Purchase           | 2025-02-27        | 2025-02-28   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | IRM      | IRM            | Purchase           | 2025-02-27        | 2025-02-28   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | GS       | GS             | Purchase           | 2025-02-27        | 2025-02-28   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | DELL     | DELL           | Purchase           | 2025-02-27        | 2025-02-28   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CRDO     | CRDO           | Purchase           | 2025-02-27        | 2025-02-28   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | COHR     | COHR           | Purchase           | 2025-02-27        | 2025-02-28   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | VAW      | VAW            | Sale (Full)        | 2025-02-27        | 2025-02-28   |      175,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | LHX      | LHX            | Purchase           | 2025-02-27        | 2025-02-28   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | STZ      | STZ            | Sale (Partial)     | 2025-02-27        | 2025-02-28   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LPLA     | LPLA           | Purchase           | 2025-02-27        | 2025-02-28   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | IQV      | IQV            | Purchase           | 2025-02-27        | 2025-02-28   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | TJX      | TJX            | Purchase           | 2025-02-27        | 2025-02-28   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | MSFT     | MSFT           | Purchase           | 2025-02-27        | 2025-02-28   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | DHR      | DHR            | Sale (Full)        | 2025-02-27        | 2025-02-28   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | HON      | HON            | Sale (Full)        | 2025-02-27        | 2025-02-28   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | PM       | PM             | Purchase           | 2025-02-27        | 2025-02-28   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | BRK      | BRK            | Sale (Partial)     | 2025-02-27        | 2025-02-28   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | COF      | COF            | Purchase           | 2025-04-13        | 2025-04-14   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | COP      | COP            | Sale (Full)        | 2025-05-12        | 2025-05-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | TMO      | TMO            | Sale (Full)        | 2025-05-12        | 2025-05-13   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | TXN      | TXN            | Sale (Full)        | 2025-05-12        | 2025-05-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | VLO      | VLO            | Sale (Full)        | 2025-05-12        | 2025-05-13   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ZTS      | ZTS            | Sale (Full)        | 2025-05-12        | 2025-05-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CVX      | CVX            | Sale (Full)        | 2025-05-12        | 2025-05-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRCX     | LRCX           | Sale (Partial)     | 2025-05-12        | 2025-05-13   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CSX      | CSX            | Sale (Full)        | 2025-05-12        | 2025-05-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CSX      | CSX            | Purchase           | 2025-06-11        | 2025-06-12   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CVX      | CVX            | Purchase           | 2025-06-11        | 2025-06-12   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | COP      | COP            | Purchase           | 2025-06-11        | 2025-06-12   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LPLA     | LPLA           | Purchase           | 2025-06-11        | 2025-06-12   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LHX      | LHX            | Purchase           | 2025-06-11        | 2025-06-12   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRCX     | LRCX           | Purchase           | 2025-06-11        | 2025-06-12   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | TXN      | TXN            | Purchase           | 2025-06-11        | 2025-06-12   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | TMO      | TMO            | Purchase           | 2025-06-11        | 2025-06-12   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | VLO      | VLO            | Purchase           | 2025-06-11        | 2025-06-12   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ZTS      | ZTS            | Purchase           | 2025-06-11        | 2025-06-12   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | PDBC     | PDBC           | Purchase           | 2025-08-12        | 2025-08-13   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | PDBC     | PDBC           | Purchase           | 2025-08-12        | 2025-08-13   |      375,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | LLY      | LLY            | Purchase           | 2025-08-12        | 2025-08-13   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | UNH      | UNH            | Sale (Partial)     | 2025-08-18        | 2025-08-19   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | UNH      | UNH            | Purchase           | 2025-10-01        | 2025-10-02   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | NOW      | NOW            | Purchase           | 2025-10-01        | 2025-10-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | INTU     | INTU           | Purchase           | 2025-10-01        | 2025-10-02   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | ISRG     | ISRG           | Purchase           | 2025-10-01        | 2025-10-02   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | TXN      | TXN            | Sale (Full)        | 2025-10-01        | 2025-10-02   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | IHF      | IHF            | Sale (Full)        | 2025-10-01        | 2025-10-02   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | WAB      | WAB            | Sale (Full)        | 2025-10-01        | 2025-10-02   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | WAB      | WAB            | Sale (Full)        | 2025-10-01        | 2025-10-02   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | FI       | FISV           | Sale (Full)        | 2025-11-21        | 2025-11-24   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CMG      | CMG            | Sale (Full)        | 2025-11-21        | 2025-11-24   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | MSFT     | MSFT           | Purchase           | 2025-11-21        | 2025-11-24   |      375,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | BRK-B    | BRK-B          | Sale (Full)        | 2025-11-21        | 2025-11-24   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | TMUS     | TMUS           | Sale (Full)        | 2025-11-21        | 2025-11-24   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | COF      | COF            | Purchase           | 2025-12-05        | 2025-12-08   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CSX      | CSX            | Sale (Full)        | 2025-12-05        | 2025-12-08   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | ZTS      | ZTS            | Sale (Full)        | 2025-12-05        | 2025-12-08   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | PNR      | PNR            | Purchase           | 2025-12-05        | 2025-12-08   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | PRMB     | PRMB           | Sale (Full)        | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | MTZ      | MTZ            | Sale (Full)        | 2026-01-13        | 2026-01-14   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRN      | LRN            | Sale (Full)        | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | IRM      | IRM            | Sale (Full)        | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | GS       | GS             | Sale (Full)        | 2026-01-13        | 2026-01-14   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | DELL     | DELL           | Sale (Full)        | 2026-01-13        | 2026-01-14   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CRDO     | CRDO           | Sale (Full)        | 2026-01-13        | 2026-01-14   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | COHR     | COHR           | Sale (Full)        | 2026-01-13        | 2026-01-14   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | PRMB     | PRMB           | Sale (Full)        | 2026-01-13        | 2026-01-14   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CAT      | CAT            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LLY      | LLY            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | JPM      | JPM            | Purchase           | 2026-01-16        | 2026-01-20   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | COF      | COF            | Purchase           | 2026-01-16        | 2026-01-20   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | RTX      | RTX            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | GOOGL    | GOOGL          | Purchase           | 2026-01-16        | 2026-01-20   |      175,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | ICE      | ICE            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | DE       | DE             | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | BSX      | BSX            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | MSFT     | MSFT           | Purchase           | 2026-01-16        | 2026-01-20   |      175,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | GS       | GS             | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRCX     | LRCX           | Purchase           | 2026-01-16        | 2026-01-20   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | KO       | KO             | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | NVDA     | NVDA           | Purchase           | 2026-01-16        | 2026-01-20   |      175,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | CRM      | CRM            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | IQV      | IQV            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | ELV      | ELV            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CVX      | CVX            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | META     | META           | Purchase           | 2026-01-16        | 2026-01-20   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | MA       | MA             | Purchase           | 2026-01-16        | 2026-01-20   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | HLT      | HLT            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | COST     | COST           | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | ISRG     | ISRG           | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | HD       | HD             | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | INTU     | INTU           | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | NOW      | NOW            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | COP      | COP            | Purchase           | 2026-01-16        | 2026-01-20   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | VSEC     | VSEC           | Purchase           | 2026-02-04        | 2026-02-05   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | MPWR     | MPWR           | Purchase           | 2026-02-04        | 2026-02-05   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | MCK      | MCK            | Purchase           | 2026-02-04        | 2026-02-05   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRN      | LRN            | Purchase           | 2026-02-04        | 2026-02-05   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | FCFS     | FCFS           | Purchase           | 2026-02-04        | 2026-02-05   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CRS      | CRS            | Purchase           | 2026-02-04        | 2026-02-05   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | C        | C              | Purchase           | 2026-02-04        | 2026-02-05   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | VSEC     | VSEC           | Purchase           | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | MTZ      | MTZ            | Sale (Full)        | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | MPWR     | MPWR           | Purchase           | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | MCK      | MCK            | Purchase           | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | LRN      | LRN            | Purchase           | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | IRM      | IRM            | Sale (Full)        | 2026-03-02        | 2026-03-03   |        8,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | GS       | GS             | Sale (Full)        | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | FCFS     | FCFS           | Purchase           | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | DELL     | DELL           | Sale (Full)        | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CRS      | CRS            | Purchase           | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | CRDO     | CRDO           | Sale (Full)        | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | COHR     | COHR           | Sale (Full)        | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | C        | C              | Purchase           | 2026-03-02        | 2026-03-03   |       32,500 | no Yahoo data for the symbol |
| Markwayne Mullin     | UNH      | UNH            | Purchase           | 2026-03-10        | 2026-03-11   |       75,000 | no Yahoo data for the symbol |
| Markwayne Mullin     | INTU     | INTU           | Sale (Full)        | 2026-03-10        | 2026-03-11   |       32,500 | no Yahoo data for the symbol |
| Patrick J. Toomey    | SPG      | SPG            | Purchase           | 2021-11-15        | 2021-11-16   |        8,000 | no Yahoo data for the symbol |
| Rick Scott           | WTT      | WTT            | Sale (Full)        | 2023-09-15        | 2023-09-18   |      750,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | MCHP     | MCHP           | Sale (Full)        | 2021-09-13        | 2021-09-14   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | T        | T              | Sale (Full)        | 2021-09-13        | 2021-09-14   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | TGT      | TGT            | Purchase           | 2022-03-16        | 2022-03-17   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | TSLA     | TSLA           | Purchase           | 2022-03-16        | 2022-03-17   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | C        | C              | Sale (Full)        | 2022-12-30        | 2023-01-03   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | ESS      | ESS            | Sale (Full)        | 2023-05-17        | 2023-05-18   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | MET      | MET            | Sale (Full)        | 2023-10-17        | 2023-10-18   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | IR       | IR             | Sale (Full)        | 2023-10-17        | 2023-10-18   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | KVUE     | KVUE           | Purchase           | 2023-10-17        | 2023-10-18   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | VZ       | VZ             | Purchase           | 2023-10-17        | 2023-10-18   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | NVS      | NVS            | Purchase           | 2023-10-17        | 2023-10-18   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | MMM      | MMM            | Sale (Full)        | 2023-10-17        | 2023-10-18   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | T        | T              | Sale (Full)        | 2023-10-17        | 2023-10-18   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | TSLA     | TSLA           | Purchase           | 2023-10-17        | 2023-10-18   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | SQ       | SQ             | Sale (Full)        | 2023-10-17        | 2023-10-18   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | WBD      | WBD            | Sale (Full)        | 2023-10-17        | 2023-10-18   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | LLY      | LLY            | Purchase           | 2023-10-17        | 2023-10-18   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | CELH     | CELH           | Purchase           | 2023-12-07        | 2023-12-08   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | VLTO     | VLTO           | Sale (Full)        | 2023-12-07        | 2023-12-08   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | KMB      | KMB            | Sale (Full)        | 2023-12-07        | 2023-12-08   |       75,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | VLTO     | VLTO           | Sale (Full)        | 2023-12-07        | 2023-12-08   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | TGT      | TGT            | Sale (Full)        | 2024-01-18        | 2024-01-19   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | KO       | KO             | Purchase           | 2024-01-18        | 2024-01-19   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | PFE      | PFE            | Sale (Full)        | 2024-01-18        | 2024-01-19   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | UL       | UL             | Sale (Full)        | 2024-04-24        | 2024-04-25   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | CMCSA    | CMCSA          | Sale (Full)        | 2024-04-24        | 2024-04-25   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | NVS      | NVS            | Sale (Partial)     | 2024-05-20        | 2024-05-21   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | CCI      | CCI            | Purchase           | 2024-06-06        | 2024-06-07   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | DEO      | DEO            | Sale (Full)        | 2024-06-06        | 2024-06-07   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | GS       | GS             | Purchase           | 2024-07-16        | 2024-07-17   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | HD       | HD             | Purchase           | 2024-07-16        | 2024-07-17   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | MSFT     | MSFT           | Purchase           | 2024-07-16        | 2024-07-17   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | JNJ      | JNJ            | Sale (Full)        | 2024-08-21        | 2024-08-22   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | MCD      | MCD            | Sale (Full)        | 2024-08-21        | 2024-08-22   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | DIS      | DIS            | Sale (Full)        | 2024-08-21        | 2024-08-22   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | CAG      | CAG            | Sale (Full)        | 2024-08-21        | 2024-08-22   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | KO       | KO             | Purchase           | 2024-11-07        | 2024-11-08   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | CELH     | CELH           | Sale (Full)        | 2024-11-07        | 2024-11-08   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | SBUX     | SBUX           | Sale (Partial)     | 2024-11-07        | 2024-11-08   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | VZ       | VZ             | Sale (Partial)     | 2024-11-07        | 2024-11-08   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | HON      | HON            | Sale (Partial)     | 2024-11-07        | 2024-11-08   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | MA       | MA             | Sale (Partial)     | 2024-11-07        | 2024-11-08   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | TSLA     | TSLA           | Sale (Partial)     | 2024-11-07        | 2024-11-08   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | TSLA     | TSLA           | Sale (Full)        | 2024-11-07        | 2024-11-08   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | LLY      | LLY            | Purchase           | 2024-11-07        | 2024-11-08   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | KVUE     | KVUE           | Sale (Full)        | 2024-12-05        | 2024-12-06   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | NVDA     | NVDA           | Sale (Partial)     | 2025-01-08        | 2025-01-10   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | LRCX     | LRCX           | Sale (Full)        | 2025-01-08        | 2025-01-10   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | SBUX     | SBUX           | Sale (Partial)     | 2025-05-13        | 2025-05-14   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | SBUX     | SBUX           | Sale (Partial)     | 2025-05-13        | 2025-05-14   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | EL       | EL             | Sale (Full)        | 2025-05-13        | 2025-05-14   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | DHR      | DHR            | Sale (Full)        | 2025-09-03        | 2025-09-04   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | UNH      | UNH            | Sale (Full)        | 2025-10-03        | 2025-10-06   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | VZ       | VZ             | Sale (Full)        | 2025-10-03        | 2025-10-06   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | NVDA     | NVDA           | Sale (Partial)     | 2025-10-03        | 2025-10-06   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | HON      | HON            | Sale (Full)        | 2025-10-03        | 2025-10-06   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | MSFT     | MSFT           | Sale (Partial)     | 2025-10-03        | 2025-10-06   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | NVDA     | NVDA           | Sale (Partial)     | 2025-11-03        | 2025-11-04   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | GH       | GH             | Purchase           | 2025-12-01        | 2025-12-02   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | KO       | KO             | Purchase           | 2025-12-01        | 2025-12-02   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | HSY      | HSY            | Purchase           | 2025-12-01        | 2025-12-02   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | SBUX     | SBUX           | Sale (Full)        | 2026-02-04        | 2026-02-05   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | NVDA     | NVDA           | Sale (Partial)     | 2026-02-04        | 2026-02-05   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | HD       | HD             | Sale (Partial)     | 2026-02-04        | 2026-02-05   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | HD       | HD             | Sale (Full)        | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | PEP      | PEP            | Sale (Partial)     | 2026-03-06        | 2026-03-09   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | JPM      | JPM            | Sale (Partial)     | 2026-05-04        | 2026-05-05   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | ORCL     | ORCL           | Sale (Partial)     | 2026-06-02        | 2026-06-03   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | NVDA     | NVDA           | Sale (Partial)     | 2026-06-02        | 2026-06-03   |      175,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | CCI      | CCI            | Sale (Full)        | 2026-07-08        | 2026-07-09   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | NVDA     | NVDA           | Sale (Partial)     | 2026-07-08        | 2026-07-09   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | COHR     | COHR           | Purchase           | 2026-07-08        | 2026-07-09   |       32,500 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | MU       | MU             | Purchase           | 2026-07-08        | 2026-07-09   |        8,000 | no Yahoo data for the symbol |
| Sheldon Whitehouse   | LOW      | LOW            | Sale (Partial)     | 2026-08-03        | 2026-08-04   |        8,000 | no Yahoo data for the symbol |
| Shelley Moore Capito | SMFG     | SMFG           | Sale (Partial)     | 2022-01-15        | 2022-01-18   |        8,000 | no Yahoo data for the symbol |
| Shelley Moore Capito | VZ       | VZ             | Sale (Partial)     | 2022-01-21        | 2022-01-24   |        8,000 | no Yahoo data for the symbol |
| Shelley Moore Capito | UNH      | UNH            | Sale (Partial)     | 2022-11-13        | 2022-11-14   |        8,000 | no Yahoo data for the symbol |
| Shelley Moore Capito | TFC      | TFC            | Sale (Partial)     | 2024-01-12        | 2024-01-16   |       32,500 | no Yahoo data for the symbol |
| Shelley Moore Capito | ENB      | ENB            | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tammy Duckworth      | ITW      | ITW            | Sale (Full)        | 2023-05-01        | 2023-05-02   |       32,500 | no Yahoo data for the symbol |
| Thom Tillis          | KD       | KD             | Sale (Full)        | 2023-07-15        | 2023-07-17   |        8,000 | no Yahoo data for the symbol |
| Thomas R. Carper     | ICLN     | ICLN           | Purchase           | 2024-03-29        | 2024-04-01   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSYS     | SSYS           | Purchase           | 2021-09-08        | 2021-09-09   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Purchase           | 2021-09-08        | 2021-09-09   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PG       | PG             | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NFLX     | NFLX           | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MPWR     | MPWR           | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KEYS     | KEYS           | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KLAC     | KLAC           | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | JNJ      | JNJ            | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTU     | INTU           | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GNRC     | GNRC           | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | EL       | EL             | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | EXP      | EXP            | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DEO      | DEO            | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CTAS     | CTAS           | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CABO     | CABO           | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BKE      | BKE            | Purchase           | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WAL      | WAL            | Sale (Full)        | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MMM      | MMM            | Sale (Full)        | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DGX      | DGX            | Sale (Full)        | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DECK     | DECK           | Sale (Full)        | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLX      | CLX            | Sale (Full)        | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CHE      | CHE            | Sale (Full)        | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BHP      | BHP            | Sale (Full)        | 2021-10-15        | 2021-10-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSYS     | SSYS           | Purchase           | 2021-10-15        | 2021-10-18   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RMD      | RMD            | Sale (Full)        | 2021-11-10        | 2021-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Purchase           | 2021-11-10        | 2021-11-11   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Purchase           | 2021-11-10        | 2021-11-11   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Purchase           | 2021-11-10        | 2021-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GE       | GE             | Sale (Full)        | 2021-11-10        | 2021-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | UAA      | UAA            | Sale (Full)        | 2021-11-10        | 2021-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | UA       | UA             | Sale (Full)        | 2021-11-10        | 2021-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | BDX      | BDX            | Sale (Full)        | 2021-11-10        | 2021-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | D        | D              | Sale (Full)        | 2021-11-10        | 2021-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | DOW      | DOW            | Sale (Full)        | 2021-11-10        | 2021-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GD       | GD             | Sale (Full)        | 2021-11-10        | 2021-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | OXY      | OXY            | Sale (Full)        | 2021-12-10        | 2021-12-13   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2021-12-10        | 2021-12-13   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SCCO     | SCCO           | Purchase           | 2021-12-10        | 2021-12-13   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSYS     | SSYS           | Purchase           | 2022-01-12        | 2022-01-13   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOLD     | GOLD           | Purchase           | 2022-02-14        | 2022-02-15   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WBA      | WBA            | Purchase           | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VZ       | VZ             | Purchase           | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MMM      | MMM            | Purchase           | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PFE      | PFE            | Purchase           | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | IBM      | IBM            | Purchase           | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Purchase           | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KO       | KO             | Purchase           | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CSCO     | CSCO           | Purchase           | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CVX      | CVX            | Purchase           | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DOW      | DOW            | Purchase           | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DUK      | DUK            | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MDT      | MDT            | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | ABC      | COR            | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CTAS     | CTAS           | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | LMT      | LMT            | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PEP      | PEP            | Sale (Full)        | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PM       | PM             | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PG       | PG             | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | TSN      | TSN            | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | XEL      | XEL            | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | FUN      | FUN            | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CRWD     | CRWD           | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GILD     | GILD           | Sale (Full)        | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLOU     | CLOU           | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | NWL      | NWL            | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PEGA     | PEGA           | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | VTRS     | VTRS           | Sale (Full)        | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CTAS     | CTAS           | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | LLY      | LLY            | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MA       | MA             | Sale (Full)        | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | NEE      | NEE            | Sale (Full)        | 2022-02-14        | 2022-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | RTX      | RTX            | Sale (Full)        | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WMT      | WMT            | Sale (Full)        | 2022-02-14        | 2022-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | OXY      | OXY            | Sale (Partial)     | 2022-03-11        | 2022-03-14   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Purchase           | 2022-03-11        | 2022-03-14   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2022-03-11        | 2022-03-14   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2022-03-11        | 2022-03-14   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WST      | WST            | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VEEV     | VEEV           | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VMW      | VMW            | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SNA      | SNA            | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SIVB     | SIVB           | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SPGI     | SPGI           | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ROK      | ROK            | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | REGN     | REGN           | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NFLX     | NFLX           | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | LMST     | LMST           | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KEY      | KEY            | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTU     | INTU           | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GNRC     | GNRC           | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FGBI     | FGBI           | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FITB     | FITB           | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | EXP      | EXP            | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DEO      | DEO            | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CFG      | CFG            | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CE       | CE             | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CP       | CP             | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CABO     | CABO           | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BKE      | BKE            | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BIO      | BIO            | Sale (Full)        | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BMO      | BMO            | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TMO      | TMO            | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RMD      | RMD            | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RF       | RF             | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NOC      | NOC            | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NDAQ     | NDAQ           | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MRK      | MRK            | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MASI     | MASI           | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MMC      | MRSH           | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MKSI     | MKSI           | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Purchase           | 2022-04-08        | 2022-04-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | HON      | HON            | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GFI      | GFI            | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | IT       | IT             | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DHI      | DHI            | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CDNS     | CDNS           | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOOG     | GOOG           | Purchase           | 2022-04-08        | 2022-04-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ECOM     | ECOM           | Purchase           | 2022-04-08        | 2022-04-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | NU       | NU             | Purchase           | 2022-04-08        | 2022-04-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | ECOM     | ECOM           | Purchase           | 2022-04-08        | 2022-04-11   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SQ       | SQ             | Sale (Full)        | 2022-05-13        | 2022-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2022-05-13        | 2022-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Full)        | 2022-05-13        | 2022-05-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ECOM     | ECOM           | Purchase           | 2022-05-13        | 2022-05-16   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Purchase           | 2022-06-13        | 2022-06-14   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2022-06-13        | 2022-06-14   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2022-06-13        | 2022-06-14   |      375,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BRK-B    | BRK-B          | Sale (Full)        | 2022-07-13        | 2022-07-14   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2022-07-13        | 2022-07-14   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Sale (Partial)     | 2022-07-13        | 2022-07-14   |      375,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOLD     | GOLD           | Sale (Full)        | 2022-07-13        | 2022-07-14   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Purchase           | 2022-07-13        | 2022-07-14   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSYS     | SSYS           | Purchase           | 2022-07-13        | 2022-07-14   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Purchase           | 2022-07-13        | 2022-07-14   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SCCO     | SCCO           | Sale (Full)        | 2022-07-13        | 2022-07-14   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2022-07-13        | 2022-07-14   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | EVT      | EVT            | Sale (Full)        | 2022-07-13        | 2022-07-14   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CVX      | CVX            | Sale (Full)        | 2022-07-13        | 2022-07-14   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Purchase           | 2022-07-13        | 2022-07-14   |      375,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2022-07-13        | 2022-07-14   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSYS     | SSYS           | Purchase           | 2022-07-13        | 2022-07-14   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSYS     | SSYS           | Purchase           | 2022-07-13        | 2022-07-14   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Purchase           | 2022-07-13        | 2022-07-14   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | EVT      | EVT            | Purchase           | 2022-07-13        | 2022-07-14   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | ECOM     | ECOM           | Purchase           | 2022-07-13        | 2022-07-14   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2022-08-15        | 2022-08-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ECOM     | ECOM           | Purchase           | 2022-08-15        | 2022-08-16   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | IVV      | IVV            | Sale (Full)        | 2022-09-15        | 2022-09-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | EFAV     | EFAV           | Sale (Full)        | 2022-09-15        | 2022-09-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | XLY      | XLY            | Sale (Full)        | 2022-09-15        | 2022-09-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | VTRS     | VTRS           | Sale (Full)        | 2022-09-15        | 2022-09-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RSP      | RSP            | Purchase           | 2022-09-15        | 2022-09-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | IDV      | IDV            | Purchase           | 2022-09-15        | 2022-09-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | DHS      | DHS            | Purchase           | 2022-09-15        | 2022-09-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | ORCL     | ORCL           | Sale (Full)        | 2022-09-15        | 2022-09-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | XLC      | XLC            | Sale (Full)        | 2022-09-15        | 2022-09-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | TSCO     | TSCO           | Sale (Full)        | 2022-09-15        | 2022-09-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MUB      | MUB            | Purchase           | 2022-09-15        | 2022-09-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | OC       | OC             | Purchase           | 2022-09-15        | 2022-09-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSYS     | SSYS           | Sale (Full)        | 2022-09-15        | 2022-09-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Partial)     | 2022-09-15        | 2022-09-16   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Purchase           | 2022-09-15        | 2022-09-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Purchase           | 2022-09-15        | 2022-09-16   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Purchase           | 2022-10-12        | 2022-10-13   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Purchase           | 2022-10-12        | 2022-10-13   |      375,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ECOM     | ECOM           | Sale (Full)        | 2022-10-12        | 2022-10-13   |      750,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NU       | NU             | Purchase           | 2022-10-12        | 2022-10-13   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2022-11-10        | 2022-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Purchase           | 2022-11-10        | 2022-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | NU       | NU             | Purchase           | 2022-11-10        | 2022-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Purchase           | 2022-11-10        | 2022-11-11   |      375,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NU       | NU             | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NU       | NU             | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VCTR     | VCTR           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VCTR     | VCTR           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VCTR     | VCTR           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VRTX     | VRTX           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TREX     | TREX           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SCI      | SCI            | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RELX     | RELX           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RH       | RH             | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PHM      | PHM            | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PAYC     | PAYC           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GIS      | GIS            | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GLPI     | GLPI           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RACE     | RACE           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | XOM      | XOM            | Purchase           | 2022-11-10        | 2022-11-11   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | EXR      | EXR            | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ETSY     | ETSY           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ELS      | ELS            | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DQ       | DQ             | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CROX     | CROX           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CSCO     | CSCO           | Purchase           | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ZTS      | ZTS            | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WIT      | WIT            | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SEIC     | SEIC           | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RMD      | RMD            | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TROW     | TROW           | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NOC      | NOC            | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NVDA     | NVDA           | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MNST     | MNST           | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Sale (Partial)     | 2022-11-10        | 2022-11-11   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MASI     | MASI           | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MKTX     | MKTX           | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | IDXX     | IDXX           | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HON      | HON            | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GGG      | GGG            | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | IT       | IT             | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GRMN     | GRMN           | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FAST     | FAST           | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | EL       | EL             | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DHI      | DHI            | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CHD      | CHD            | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BF-B     | BF-B           | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VZ       | VZ             | Sale (Full)        | 2022-11-10        | 2022-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | SIEGY    | SIEGY          | Sale (Full)        | 2022-11-10        | 2022-11-11   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | FDX      | FDX            | Sale (Full)        | 2022-11-10        | 2022-11-11   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Sale (Partial)     | 2022-12-14        | 2022-12-15   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | F        | F              | Sale (Full)        | 2022-12-14        | 2022-12-15   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | F        | F              | Purchase           | 2022-12-14        | 2022-12-15   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Purchase           | 2022-12-14        | 2022-12-15   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Partial)     | 2022-12-14        | 2022-12-15   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ATVI     | ATVI           | Purchase           | 2022-12-14        | 2022-12-15   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2022-12-14        | 2022-12-15   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2022-12-14        | 2022-12-15   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NU       | NU             | Purchase           | 2022-12-14        | 2022-12-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2022-12-14        | 2022-12-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOLD     | GOLD           | Purchase           | 2023-01-13        | 2023-01-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | NU       | NU             | Purchase           | 2023-01-13        | 2023-01-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DIS      | DIS            | Sale (Partial)     | 2023-01-13        | 2023-01-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Partial)     | 2023-01-13        | 2023-01-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Partial)     | 2023-01-13        | 2023-01-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Partial)     | 2023-01-13        | 2023-01-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Partial)     | 2023-01-13        | 2023-01-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Partial)     | 2023-01-13        | 2023-01-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Partial)     | 2023-01-13        | 2023-01-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2023-01-13        | 2023-01-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOLD     | GOLD           | Purchase           | 2023-01-13        | 2023-01-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2023-01-13        | 2023-01-17   |      375,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Sale (Partial)     | 2023-01-13        | 2023-01-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Purchase           | 2023-01-13        | 2023-01-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOLD     | GOLD           | Purchase           | 2023-01-13        | 2023-01-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOLD     | GOLD           | Purchase           | 2023-02-14        | 2023-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-02-14        | 2023-02-15   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | UAA      | UAA            | Purchase           | 2023-02-14        | 2023-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-02-14        | 2023-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-02-14        | 2023-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-02-14        | 2023-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-02-14        | 2023-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-02-14        | 2023-02-15   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-04-12        | 2023-04-13   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-04-12        | 2023-04-13   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-04-12        | 2023-04-13   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-04-12        | 2023-04-13   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-04-12        | 2023-04-13   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-04-12        | 2023-04-13   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-04-12        | 2023-04-13   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-04-12        | 2023-04-13   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KMB      | KMB            | Purchase           | 2023-04-12        | 2023-04-13   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | BMO      | BMO            | Sale (Full)        | 2023-04-12        | 2023-04-13   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | F        | F              | Purchase           | 2023-05-11        | 2023-05-12   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | F        | F              | Purchase           | 2023-05-11        | 2023-05-12   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | F        | F              | Purchase           | 2023-05-11        | 2023-05-12   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | ATVI     | ATVI           | Sale (Full)        | 2023-05-11        | 2023-05-12   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-05-11        | 2023-05-12   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-05-11        | 2023-05-12   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-05-11        | 2023-05-12   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MMM      | MMM            | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | XP       | XP             | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VCTR     | VCTR           | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VZ       | VZ             | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TREX     | TREX           | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MMM      | MMM            | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TMO      | TMO            | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TSLA     | TSLA           | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SKY      | SKY            | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSD      | SSD            | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SCI      | SCI            | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QSR      | QSR            | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | REGN     | REGN           | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RRC      | RRC            | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RH       | RH             | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PHM      | PHM            | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PAM      | PAM            | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NSC      | NSC            | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NDSN     | NDSN           | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NVDA     | NVDA           | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MCO      | MCO            | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MPWR     | MPWR           | Sale (Partial)     | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MPWR     | MPWR           | Sale (Partial)     | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MTD      | MTD            | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MMC      | MRSH           | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MKSI     | MKSI           | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | LMST     | LMST           | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ITW      | ITW            | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | IDXX     | IDXX           | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GFI      | GFI            | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FLT      | CPAY           | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | META     | META           | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ETSY     | ETSY           | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | EW       | EW             | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DQ       | DQ             | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CROX     | CROX           | Sale (Full)        | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CSCO     | CSCO           | Sale (Full)        | 2023-05-11        | 2023-05-12   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GSK      | GSK            | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GNTX     | GNTX           | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GRMN     | GRMN           | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DIOD     | DIOD           | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CBSH     | CBSH           | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CRUS     | CRUS           | Purchase           | 2023-05-11        | 2023-05-12   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-06-15        | 2023-06-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-06-15        | 2023-06-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Partial)     | 2023-06-15        | 2023-06-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Partial)     | 2023-06-15        | 2023-06-16   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | OXY      | OXY            | Purchase           | 2023-06-15        | 2023-06-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2023-06-15        | 2023-06-16   |      375,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Purchase           | 2023-06-15        | 2023-06-16   |      375,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WBA      | WBA            | Purchase           | 2023-06-15        | 2023-06-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RF       | RF             | Purchase           | 2023-06-15        | 2023-06-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Purchase           | 2023-06-15        | 2023-06-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NU       | NU             | Purchase           | 2023-06-15        | 2023-06-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | KEY      | KEY            | Purchase           | 2023-06-15        | 2023-06-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FGBI     | FGBI           | Purchase           | 2023-06-15        | 2023-06-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FITB     | FITB           | Purchase           | 2023-06-15        | 2023-06-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CFG      | CFG            | Purchase           | 2023-06-15        | 2023-06-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Full)        | 2023-07-14        | 2023-07-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Sale (Full)        | 2023-07-14        | 2023-07-17   |      375,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-07-14        | 2023-07-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | WBA      | WBA            | Purchase           | 2023-07-14        | 2023-07-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | UAA      | UAA            | Purchase           | 2023-07-14        | 2023-07-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WBA      | WBA            | Purchase           | 2023-07-14        | 2023-07-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PFE      | PFE            | Purchase           | 2023-07-14        | 2023-07-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KEY      | KEY            | Purchase           | 2023-07-14        | 2023-07-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FGBI     | FGBI           | Purchase           | 2023-07-14        | 2023-07-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FGBI     | FGBI           | Purchase           | 2023-07-14        | 2023-07-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FITB     | FITB           | Purchase           | 2023-07-14        | 2023-07-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CFG      | CFG            | Purchase           | 2023-07-14        | 2023-07-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Purchase           | 2023-07-14        | 2023-07-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Purchase           | 2023-07-14        | 2023-07-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Purchase           | 2023-07-14        | 2023-07-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Purchase           | 2023-07-14        | 2023-07-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-07-14        | 2023-07-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | WBA      | WBA            | Purchase           | 2023-08-14        | 2023-08-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VZ       | VZ             | Purchase           | 2023-08-14        | 2023-08-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | UAA      | UAA            | Purchase           | 2023-08-14        | 2023-08-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MMM      | MMM            | Purchase           | 2023-08-14        | 2023-08-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PFE      | PFE            | Purchase           | 2023-08-14        | 2023-08-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KEY      | KEY            | Purchase           | 2023-08-14        | 2023-08-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FGBI     | FGBI           | Purchase           | 2023-08-14        | 2023-08-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FGBI     | FGBI           | Purchase           | 2023-08-14        | 2023-08-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Purchase           | 2023-08-14        | 2023-08-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Purchase           | 2023-08-14        | 2023-08-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Purchase           | 2023-08-14        | 2023-08-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-08-14        | 2023-08-15   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Purchase           | 2023-09-15        | 2023-09-18   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | F        | F              | Sale (Full)        | 2023-09-15        | 2023-09-18   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | LLY      | LLY            | Sale (Partial)     | 2023-10-13        | 2023-10-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PRU      | PRU            | Sale (Partial)     | 2023-10-13        | 2023-10-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | TSN      | TSN            | Sale (Partial)     | 2023-10-13        | 2023-10-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KR       | KR             | Purchase           | 2023-10-13        | 2023-10-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLX      | CLX            | Purchase           | 2023-10-13        | 2023-10-16   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PARA     | PARA           | Purchase           | 2023-10-13        | 2023-10-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TXN      | TXN            | Purchase           | 2023-10-13        | 2023-10-16   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KMB      | KMB            | Purchase           | 2023-10-13        | 2023-10-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | TXN      | TXN            | Purchase           | 2023-10-13        | 2023-10-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-10-13        | 2023-10-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Sale (Full)        | 2023-10-13        | 2023-10-16   |      375,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KMB      | KMB            | Purchase           | 2023-10-13        | 2023-10-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | LPX      | LPX            | Purchase           | 2023-10-13        | 2023-10-16   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KMB      | KMB            | Purchase           | 2023-10-13        | 2023-10-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-10-13        | 2023-10-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-10-13        | 2023-10-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KMB      | KMB            | Sale (Full)        | 2023-11-16        | 2023-11-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HPQ      | HPQ            | Sale (Full)        | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLX      | CLX            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLX      | CLX            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLX      | CLX            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLX      | CLX            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLX      | CLX            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLX      | CLX            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HPQ      | HPQ            | Purchase           | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLX      | CLX            | Purchase           | 2023-11-16        | 2023-11-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HPQ      | HPQ            | Purchase           | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | HPQ      | HPQ            | Sale (Full)        | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Purchase           | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | WU       | WU             | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | UNP      | UNP            | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MMM      | MMM            | Purchase           | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | TSLA     | TSLA           | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SCCO     | SCCO           | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SWKS     | SWKS           | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ROK      | ROK            | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RMD      | RMD            | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PHM      | PHM            | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NXPI     | NXPI           | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MCO      | MCO            | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MNST     | MNST           | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MPWR     | MPWR           | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MCHP     | MCHP           | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MMC      | MRSH           | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ITW      | ITW            | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GGG      | GGG            | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FTNT     | FTNT           | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | META     | META           | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KO       | KO             | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BMY      | BMY            | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WMS      | WMS            | Purchase           | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SKY      | SKY            | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RRC      | RRC            | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ODFL     | ODFL           | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NSC      | NSC            | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MRK      | MRK            | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | JNJ      | JNJ            | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | JKHY     | JKHY           | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GSK      | GSK            | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GIS      | GIS            | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DIOD     | DIOD           | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CBSH     | CBSH           | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CRUS     | CRUS           | Sale (Full)        | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CSX      | CSX            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | X        | X              | Sale (Partial)     | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | TXN      | TXN            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TXN      | TXN            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TXN      | TXN            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | TXN      | TXN            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | TXN      | TXN            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TXN      | TXN            | Sale (Partial)     | 2023-11-16        | 2023-11-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NU       | NU             | Sale (Full)        | 2023-11-16        | 2023-11-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | LPX      | LPX            | Sale (Full)        | 2023-11-16        | 2023-11-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KR       | KR             | Sale (Full)        | 2023-11-16        | 2023-11-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KR       | KR             | Purchase           | 2023-11-16        | 2023-11-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KEY      | KEY            | Purchase           | 2023-12-15        | 2023-12-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | FGBI     | FGBI           | Sale (Full)        | 2023-12-15        | 2023-12-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PARA     | PARA           | Purchase           | 2024-01-12        | 2024-01-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | VZ       | VZ             | Sale (Partial)     | 2024-01-12        | 2024-01-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | RF       | RF             | Sale (Full)        | 2024-01-12        | 2024-01-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | KEY      | KEY            | Purchase           | 2024-01-12        | 2024-01-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | UAA      | UAA            | Sale (Full)        | 2024-01-12        | 2024-01-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOLD     | GOLD           | Purchase           | 2024-01-12        | 2024-01-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CVX      | CVX            | Purchase           | 2024-01-12        | 2024-01-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CVX      | CVX            | Purchase           | 2024-01-12        | 2024-01-16   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOLD     | GOLD           | Purchase           | 2024-01-12        | 2024-01-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOLD     | GOLD           | Purchase           | 2024-01-12        | 2024-01-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SCCO     | SCCO           | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MNST     | MNST           | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MMC      | MRSH           | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | IDXX     | IDXX           | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | META     | META           | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Sale (Partial)     | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Sale (Partial)     | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Sale (Partial)     | 2024-02-14        | 2024-02-15   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Sale (Partial)     | 2024-02-14        | 2024-02-15   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | XP       | XP             | Sale (Full)        | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PAM      | PAM            | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NVO      | NVO            | Sale (Full)        | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | LRCX     | LRCX           | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | IBM      | IBM            | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GNTX     | GNTX           | Sale (Full)        | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | RACE     | RACE           | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CFG      | CFG            | Sale (Full)        | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOOGL    | GOOGL          | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOOG     | GOOG           | Sale (Full)        | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOOGL    | GOOGL          | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BMY      | BMY            | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | LLY      | LLY            | Sale (Partial)     | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | ORCL     | ORCL           | Sale (Partial)     | 2024-02-14        | 2024-02-15   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SLF      | SLF            | Sale (Partial)     | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | DGX      | DGX            | Sale (Partial)     | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | UNP      | UNP            | Sale (Partial)     | 2024-02-14        | 2024-02-15   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | SBLK     | SBLK           | Purchase           | 2024-03-15        | 2024-03-18   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Purchase           | 2024-03-15        | 2024-03-18   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PFE      | PFE            | Purchase           | 2024-03-15        | 2024-03-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOGL     | GOGL           | Purchase           | 2024-03-15        | 2024-03-18   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Purchase           | 2024-03-15        | 2024-03-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | WBA      | WBA            | Purchase           | 2024-04-15        | 2024-04-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PARA     | PARA           | Purchase           | 2024-04-15        | 2024-04-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | RYCEY    | RYCEY          | Purchase           | 2024-04-15        | 2024-04-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RYCEY    | RYCEY          | Purchase           | 2024-04-15        | 2024-04-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Purchase           | 2024-04-15        | 2024-04-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Purchase           | 2024-04-15        | 2024-04-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Purchase           | 2024-04-15        | 2024-04-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CSX      | CSX            | Sale (Full)        | 2024-04-15        | 2024-04-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | JPM      | JPM            | Sale (Full)        | 2024-04-15        | 2024-04-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TXN      | TXN            | Sale (Full)        | 2024-04-15        | 2024-04-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WBA      | WBA            | Sale (Full)        | 2024-05-15        | 2024-05-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SBLK     | SBLK           | Sale (Full)        | 2024-05-15        | 2024-05-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSBK     | SSBK           | Sale (Full)        | 2024-05-15        | 2024-05-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | OXY      | OXY            | Sale (Full)        | 2024-05-15        | 2024-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | NVDA     | NVDA           | Sale (Full)        | 2024-05-15        | 2024-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | KEY      | KEY            | Sale (Full)        | 2024-05-15        | 2024-05-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOGL     | GOGL           | Sale (Full)        | 2024-05-15        | 2024-05-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | XOM      | XOM            | Sale (Full)        | 2024-05-15        | 2024-05-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CVX      | CVX            | Sale (Full)        | 2024-05-15        | 2024-05-16   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Sale (Partial)     | 2024-05-15        | 2024-05-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MMM      | MMM            | Sale (Full)        | 2024-05-15        | 2024-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PAC      | PAC            | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NTES     | NTES           | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TEL      | TEL            | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SNPS     | SNPS           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SWKS     | SWKS           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QLYS     | QLYS           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ODFL     | ODFL           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ODFL     | ODFL           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NFLX     | NFLX           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSI      | MSI            | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NTES     | NTES           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | LULU     | LULU           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | LSCC     | LSCC           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | JKHY     | JKHY           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PAC      | PAC            | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GILD     | GILD           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DECK     | DECK           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CBSH     | CBSH           | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BRO      | BRO            | Purchase           | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WU       | WU             | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SSD      | SSD            | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ROK      | ROK            | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QSR      | QSR            | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | REGN     | REGN           | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PHM      | PHM            | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PAYC     | PAYC           | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NDAQ     | NDAQ           | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KEYS     | KEYS           | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MCHP     | MCHP           | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | LLY      | LLY            | Sale (Full)        | 2024-05-15        | 2024-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | FTNT     | FTNT           | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | IEX      | IEX            | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | EXR      | EXR            | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BMY      | BMY            | Sale (Full)        | 2024-05-15        | 2024-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Sale (Full)        | 2024-06-14        | 2024-06-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Sale (Partial)     | 2024-06-14        | 2024-06-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Sale (Full)        | 2024-06-14        | 2024-06-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Sale (Partial)     | 2024-06-14        | 2024-06-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PARA     | PARA           | Sale (Full)        | 2024-06-14        | 2024-06-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Sale (Partial)     | 2024-06-14        | 2024-06-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Sale (Partial)     | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Sale (Partial)     | 2024-06-14        | 2024-06-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Sale (Partial)     | 2024-06-14        | 2024-06-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Sale (Partial)     | 2024-06-14        | 2024-06-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CLF      | CLF            | Sale (Partial)     | 2024-06-14        | 2024-06-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Purchase           | 2024-06-14        | 2024-06-17   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SWKS     | SWKS           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Purchase           | 2024-06-14        | 2024-06-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GILD     | GILD           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | LSCC     | LSCC           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INTC     | INTC           | Purchase           | 2024-06-14        | 2024-06-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FITB     | FITB           | Sale (Full)        | 2024-06-14        | 2024-06-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOLD     | GOLD           | Sale (Full)        | 2024-06-14        | 2024-06-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WMS      | WMS            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WAT      | WAT            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | V        | V              | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VRTX     | VRTX           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | VRSK     | VRSK           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | UI       | UI             | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TER      | TER            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TEL      | TEL            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SNPS     | SNPS           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SOLV     | SOLV           | Purchase           | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RYCEY    | RYCEY          | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RYCEY    | RYCEY          | Sale (Partial)     | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RYCEY    | RYCEY          | Sale (Partial)     | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RMD      | RMD            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | RELX     | RELX           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | QLYS     | QLYS           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PG       | PG             | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PFE      | PFE            | Sale (Full)        | 2024-06-14        | 2024-06-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PEP      | PEP            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Full)        | 2024-06-14        | 2024-06-17   |      175,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PAYX     | PAYX           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ODFL     | ODFL           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NDSN     | NDSN           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NXPI     | NXPI           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | NFLX     | NFLX           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSI      | MSI            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MCO      | MCO            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MPWR     | MPWR           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MA       | MA             | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | LULU     | LULU           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | KLAC     | KLAC           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | INFY     | INFY           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ITW      | ITW            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HUMA     | HUMA           | Sale (Partial)     | 2024-06-14        | 2024-06-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | HSY      | HSY            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | JKHY     | JKHY           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GGG      | GGG            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GRMN     | GRMN           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | GLPI     | GLPI           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | FDS      | FDS            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | ELS      | ELS            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DECK     | DECK           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CPRT     | CPRT           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CBSH     | CBSH           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CTAS     | CTAS           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CDNS     | CDNS           | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | DOW      | DOW            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | BRO      | BRO            | Sale (Full)        | 2024-06-14        | 2024-06-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MDT      | MDT            | Sale (Full)        | 2024-09-13        | 2024-09-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CVS      | CVS            | Sale (Full)        | 2024-09-13        | 2024-09-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | UPS      | UPS            | Sale (Full)        | 2024-09-13        | 2024-09-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CTVA     | CTVA           | Sale (Full)        | 2024-11-15        | 2024-11-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | HON      | HON            | Sale (Full)        | 2024-11-15        | 2024-11-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | JNJ      | JNJ            | Sale (Full)        | 2024-11-15        | 2024-11-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | KMB      | KMB            | Sale (Full)        | 2024-11-15        | 2024-11-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MCD      | MCD            | Sale (Full)        | 2024-11-15        | 2024-11-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Sale (Full)        | 2024-11-15        | 2024-11-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | OTIS     | OTIS           | Sale (Full)        | 2024-11-15        | 2024-11-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | OC       | OC             | Sale (Full)        | 2024-11-15        | 2024-11-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | TRV      | TRV            | Sale (Full)        | 2024-11-15        | 2024-11-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | TSCO     | TSCO           | Sale (Full)        | 2025-02-14        | 2025-02-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CARR     | CARR           | Sale (Full)        | 2025-02-14        | 2025-02-18   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | TXN      | TXN            | Sale (Full)        | 2025-02-14        | 2025-02-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | DEO      | DEO            | Sale (Full)        | 2025-02-14        | 2025-02-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Sale (Full)        | 2025-02-14        | 2025-02-18   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | BMY      | BMY            | Sale (Full)        | 2025-05-15        | 2025-05-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | PYPL     | PYPL           | Sale (Full)        | 2025-05-15        | 2025-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | USIG     | USIG           | Purchase           | 2025-05-15        | 2025-05-16   |       75,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | JPM      | JPM            | Sale (Full)        | 2025-05-15        | 2025-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOOGL    | GOOGL          | Sale (Full)        | 2025-05-15        | 2025-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | CSX      | CSX            | Sale (Full)        | 2025-05-15        | 2025-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | STZ      | STZ            | Sale (Full)        | 2025-05-15        | 2025-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | DUK      | DUK            | Sale (Full)        | 2025-05-15        | 2025-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GS       | GS             | Sale (Full)        | 2025-05-15        | 2025-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | LLY      | LLY            | Sale (Full)        | 2025-05-15        | 2025-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MA       | MA             | Sale (Full)        | 2025-05-15        | 2025-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Sale (Full)        | 2025-05-15        | 2025-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | QCOM     | QCOM           | Sale (Full)        | 2025-05-15        | 2025-05-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PEP      | PEP            | Sale (Full)        | 2025-11-15        | 2025-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | OC       | OC             | Sale (Full)        | 2025-11-15        | 2025-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Sale (Full)        | 2025-11-15        | 2025-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOOGL    | GOOGL          | Sale (Full)        | 2025-11-15        | 2025-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | ORCL     | ORCL           | Sale (Full)        | 2025-11-15        | 2025-11-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | XLU      | XLU            | Purchase           | 2026-01-15        | 2026-01-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | XLP      | XLP            | Purchase           | 2026-01-15        | 2026-01-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | XLV      | XLV            | Purchase           | 2026-01-15        | 2026-01-16   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOOGL    | GOOGL          | Sale (Full)        | 2026-01-15        | 2026-01-16   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | WAB      | WAB            | Sale (Full)        | 2026-07-16        | 2026-07-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CSX      | CSX            | Sale (Full)        | 2026-07-16        | 2026-07-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | DUK      | DUK            | Sale (Full)        | 2026-07-16        | 2026-07-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | LMT      | LMT            | Sale (Full)        | 2026-07-16        | 2026-07-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MA       | MA             | Sale (Full)        | 2026-07-16        | 2026-07-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | NEE      | NEE            | Sale (Full)        | 2026-07-16        | 2026-07-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PFE      | PFE            | Sale (Full)        | 2026-07-16        | 2026-07-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | PG       | PG             | Sale (Full)        | 2026-07-16        | 2026-07-17   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | TSCO     | TSCO           | Sale (Full)        | 2026-07-16        | 2026-07-17   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | CSX      | CSX            | Sale (Partial)     | 2026-08-05        | 2026-08-06   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | JPM      | JPM            | Sale (Partial)     | 2026-08-05        | 2026-08-06   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | SOLV     | SOLV           | Sale (Full)        | 2026-08-05        | 2026-08-06   |        8,000 | no Yahoo data for the symbol |
| Tommy Tuberville     | MSFT     | MSFT           | Sale (Partial)     | 2026-08-05        | 2026-08-06   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | OC       | OC             | Sale (Partial)     | 2026-08-05        | 2026-08-06   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOOGL    | GOOGL          | Sale (Partial)     | 2026-08-05        | 2026-08-06   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GS       | GS             | Sale (Partial)     | 2026-08-05        | 2026-08-06   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | MA       | MA             | Sale (Partial)     | 2026-08-05        | 2026-08-06   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOOGL    | GOOGL          | Sale (Partial)     | 2026-08-05        | 2026-08-06   |       32,500 | no Yahoo data for the symbol |
| Tommy Tuberville     | GOOGL    | GOOGL          | Sale (Partial)     | 2026-08-05        | 2026-08-06   |        8,000 | no Yahoo data for the symbol |

### 4. Price series that end before the window end while a copied position may be open

In-scope purchases whose symbol's Yahoo series ends before 2026-08-31 (923 senator-ticker pairs; `data/interim/price_series_ending_early.csv`). `full_sale_disclosed_before_last_price` = the same senator disclosed a Sale (Full) of it before the series ends (a rough check; FIFO matching is Phase 4). **Proposed engine rule (E20, for Harry): close the position at the last available price and hold the proceeds at the risk-free rate until the window ends.**

| senator              | price_ticker   | ticker   | asset_name                                    |   purchases |   midpoint_$ | first_purchase_disclosed   | last_price_date   | full_sale_disclosed_before_last_price   |
|:---------------------|:---------------|:---------|:----------------------------------------------|------------:|-------------:|:---------------------------|:------------------|:----------------------------------------|
| Tommy Tuberville     | PYPL           | PYPL     | PayPal Holdings, Inc. - Common Stock          |          13 |    2,180,506 | 2022-03-11                 | (no data)         | False                                   |
| Tommy Tuberville     | QCOM           | QCOM     | QUALCOMM Incorporated - Common Stock          |           8 |    1,166,004 | 2022-07-13                 | (no data)         | False                                   |
| David McCormick      | BITB           | BITB     | Bitwise Bitcoin ETF                           |          22 |    1,140,011 | 2025-03-05                 | (no data)         | False                                   |
| Tommy Tuberville     | CLF            | CLF      | Cleveland-Cliffs Inc. Common Stock            |          18 |    1,051,509 | 2021-12-10                 | (no data)         | False                                   |
| Tommy Tuberville     | INTC           | INTC     | Intel Corporation - Common Stock              |          11 |    1,006,006 | 2021-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | X              | X        | United States Steel Corporation Common Stock  |           5 |      875,002 | 2021-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | MSFT           | MSFT     | Microsoft Corporation - Common Stock          |           3 |      782,502 | 2022-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | MSFT           | MSFT     | Microsoft Corp                                |           5 |      665,502 | 2023-10-12                 | (no data)         | False                                   |
| Tommy Tuberville     | ECOM           | ECOM     | ChannelAdvisor Corporation Common Stock       |           5 |      465,502 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | F              | F        | Ford Motor Company Common Stock               |           4 |      415,002 | 2022-12-14                 | (no data)         | False                                   |
| Markwayne Mullin     | PDBC           | PDBC     | Invesco Optimum Yield Diversified Commodity S |           2 |      407,501 | 2025-08-12                 | (no data)         | False                                   |
| Markwayne Mullin     | HIYS           | HIYS     | Invesco Actively Managed Exchange-Traded Fund |           1 |      375,000 | 2024-12-03                 | (no data)         | False                                   |
| Tommy Tuberville     | CLX            | CLX      | Clorox Company (The) Common Stock             |           2 |      350,001 | 2023-10-13                 | (no data)         | False                                   |
| Tommy Tuberville     | GOLD           | GOLD     | Barrick Gold Corporation Common Stock (BC)    |           8 |      314,004 | 2022-02-14                 | (no data)         | False                                   |
| Tommy Tuberville     | CVX            | CVX      | Chevron Corporation Common Stock              |           3 |      258,002 | 2022-02-14                 | (no data)         | False                                   |
| Tommy Tuberville     | TXN            | TXN      | Texas Instruments Incorporated - Common Stock |           2 |      250,001 | 2023-10-13                 | (no data)         | False                                   |
| Markwayne Mullin     | NVDA           | NVDA     | NVIDIA Corporation - Common Stock             |           4 |      248,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | GOOGL          | GOOGL    | Alphabet Cl A                                 |           3 |      215,502 | 2023-10-12                 | (no data)         | False                                   |
| Ashley Moody         | NVDA           | NVDA     | NVDA                                          |           2 |      207,501 | 2025-04-20                 | (no data)         | False                                   |
| Markwayne Mullin     | META           | META     | Meta Platforms, Inc. - Class A Common Stock   |           4 |      190,502 | 2023-10-12                 | (no data)         | False                                   |
| Tommy Tuberville     | SCCO           | SCCO     | Southern Copper Corporation Common Stock      |           2 |      183,001 | 2021-12-10                 | (no data)         | False                                   |
| Markwayne Mullin     | COF            | COF      | Capital One Financial Corp                    |           3 |      182,502 | 2025-04-13                 | (no data)         | False                                   |
| Markwayne Mullin     | LRCX           | LRCX     | Lam Research Corp                             |           5 |      180,502 | 2023-10-12                 | (no data)         | False                                   |
| Ashley Moody         | LLY            | LLY      | LLY                                           |           1 |      175,000 | 2025-03-22                 | (no data)         | False                                   |
| Ashley Moody         | SMCI           | SMCI     | SMCI                                          |           1 |      175,000 | 2025-04-20                 | (no data)         | False                                   |
| John W. Hickenlooper | INTU           | INTU     | Intuit Inc. - Common Stock                    |           1 |      175,000 | 2025-10-06                 | (no data)         | False                                   |
| John W. Hickenlooper | PANW           | PANW     | Palo Alto Networks, Inc. Common Stock         |           1 |      175,000 | 2025-10-06                 | (no data)         | False                                   |
| John W. Hickenlooper | UBER           | UBER     | Uber Technologies, Inc. Common Stock          |           1 |      175,000 | 2026-02-06                 | (no data)         | False                                   |
| Markwayne Mullin     | EZU            | EZU      | iShares MSCI Eurozone ETF                     |           1 |      175,000 | 2024-12-19                 | (no data)         | False                                   |
| Markwayne Mullin     | IEFA           | IEFA     | iShares Core MSCI EAFE ETF                    |           1 |      175,000 | 2024-12-19                 | (no data)         | False                                   |
| Tommy Tuberville     | ATVI           | ATVI     | Activision Blizzard, Inc - Common Stock       |           1 |      175,000 | 2022-12-14                 | (no data)         | False                                   |
| Tommy Tuberville     | LPX            | LPX      | Louisiana-Pacific Corporation Common Stock    |           1 |      175,000 | 2023-10-13                 | (no data)         | False                                   |
| Tommy Tuberville     | KMB            | KMB      | Kimberly-Clark Corporation Common Stock       |           4 |      172,502 | 2023-04-12                 | (no data)         | False                                   |
| Tommy Tuberville     | SSYS           | SSYS     | Stratasys, Ltd. - Common Stock                |           6 |      164,003 | 2021-09-08                 | (no data)         | False                                   |
| Markwayne Mullin     | VLO            | VLO      | Valero Energy Corporation Common Stock        |           2 |      150,001 | 2023-10-12                 | (no data)         | False                                   |
| Tommy Tuberville     | SSBK           | SSBK     | Southern States Bancshares, Inc. - Common Sto |           2 |      150,001 | 2021-09-08                 | (no data)         | False                                   |
| Markwayne Mullin     | CVX            | CVX      | Chevron Corp                                  |           4 |      148,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | LLY            | LLY      | Eli Lilly and Company                         |           4 |      148,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | UNH            | UNH      | Unitedhealth Group Inc                        |           4 |      148,002 | 2023-10-12                 | (no data)         | False                                   |
| Tommy Tuberville     | PARA           | PARA     | Paramount Global - Class B Common Stock       |           3 |      140,002 | 2023-10-13                 | (no data)         | False                                   |
| Tommy Tuberville     | HUMA           | HUMA     | Humacyte, Inc. - Common Stock                 |           8 |      137,504 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | NU             | NU       | Nu Holdings Ltd. Class A Ordinary Shares      |           8 |      137,504 | 2022-04-08                 | (no data)         | False                                   |
| Markwayne Mullin     | ZTS            | ZTS      | Zoetis Inc. Class A Common Stock              |           4 |      123,502 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | GS             | GS       | Goldman Sachs Group, Inc. (The) Common Stock  |           6 |      121,503 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | JPM            | JPM      | JP Morgan Chase & Co. Common Stock            |           3 |      115,502 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | MA             | MA       | Mastercard Inc                                |           3 |      115,502 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | LRN            | LRN      | Stride Inc                                    |           5 |      113,502 | 2024-11-08                 | (no data)         | False                                   |
| Ashley Moody         | HWM            | HWM      | Howmet Aerospace Inc                          |           2 |      107,501 | 2025-02-21                 | (no data)         | False                                   |
| Markwayne Mullin     | ISRG           | ISRG     | Intuitive Surgical, Inc. - Common Stock       |           2 |      107,501 | 2025-10-01                 | (no data)         | False                                   |
| Markwayne Mullin     | LPLA           | LPLA     | Lpl Financial Holdings                        |           2 |      107,501 | 2025-02-27                 | (no data)         | False                                   |
| Tommy Tuberville     | KR             | KR       | Kroger Company (The) Common Stock             |           2 |      107,501 | 2023-10-13                 | (no data)         | False                                   |
| Markwayne Mullin     | COP            | COP      | ConocoPhillips Common Stock                   |           4 |      105,502 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | IQV            | IQV      | Iqvia Holdings Inc                            |           3 |       97,502 | 2024-09-19                 | (no data)         | False                                   |
| Markwayne Mullin     | TMO            | TMO      | Thermo Fisher Scientific Inc                  |           3 |       97,502 | 2023-10-12                 | (no data)         | False                                   |
| Tommy Tuberville     | KEY            | KEY      | KeyCorp Common Stock                          |           6 |       97,003 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | WBA            | WBA      | Walgreens Boots Alliance, Inc. - Common Stock |           6 |       97,003 | 2022-02-14                 | (no data)         | False                                   |
| John Boozman         | TBLL           | TBLL     | Invesco Short Term Treasury ETF               |           8 |       88,504 | 2024-10-18                 | (no data)         | False                                   |
| Alan Armstrong       | GOOG           | GOOG     | Alphabet Inc. - Class C Capital Stock         |           2 |       83,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NVDA           | NVDA     | NVIDIA Corporation - Common Stock             |           2 |       83,001 | 2026-07-21                 | (no data)         | False                                   |
| John Boozman         | XFIV           | XFIV     | BondBloxx Bloomberg Five Year Target Duration |           2 |       83,001 | 2026-06-16                 | (no data)         | False                                   |
| Markwayne Mullin     | IEMG           | IEMG     | iShares Core MSCI Emerging Markets ETF        |           2 |       83,001 | 2024-12-19                 | (no data)         | False                                   |
| Alan Armstrong       | BRK-B          | BRK-B    | Berkshire Hathaway Inc. New Common Stock      |           1 |       75,000 | 2026-07-21                 | (no data)         | False                                   |
| Ashley Moody         | MU             | MU       | Micron Technology                             |           1 |       75,000 | 2025-02-21                 | (no data)         | False                                   |
| John W. Hickenlooper | ETN            | ETN      | Eaton Corporation, PLC Ordinary Shares        |           1 |       75,000 | 2026-02-06                 | (no data)         | False                                   |
| Markwayne Mullin     | KLAC           | KLAC     | KLA Corporation - Common Stock                |           1 |       75,000 | 2023-10-12                 | (no data)         | False                                   |
| Thomas R. Carper     | ICLN           | ICLN     | Global Clean Energy Ishares ETF               |           1 |       75,000 | 2024-03-29                 | (no data)         | False                                   |
| Tommy Tuberville     | GOGL           | GOGL     | Golden Ocean Group Limited - Common Stock     |           1 |       75,000 | 2024-03-15                 | (no data)         | False                                   |
| Tommy Tuberville     | MUB            | MUB      | iShares National Muni Bond ETF                |           1 |       75,000 | 2022-09-15                 | (no data)         | False                                   |
| Tommy Tuberville     | SBLK           | SBLK     | Star Bulk Carriers Corp. - Common Shares      |           1 |       75,000 | 2024-03-15                 | (no data)         | False                                   |
| Tommy Tuberville     | USIG           | USIG     | iShares Broad USD Investment Grade Corporate  |           1 |       75,000 | 2025-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | XOM            | XOM      | Exxon Mobil Corporation Common Stock          |           1 |       75,000 | 2022-11-10                 | (no data)         | False                                   |
| Markwayne Mullin     | BSX            | BSX      | Boston Scientific Corp                        |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | CAT            | CAT      | Caterpillar, Inc. Common Stock                |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | COST           | COST     | Costco Wholesale Corporation - Common Stock   |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | CRM            | CRM      | Salesforce, Inc. Common Stock                 |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | CSX            | CSX      | CSX Corporation - Common Stock                |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | DE             | DE       | Deere & Company                               |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | ELV            | ELV      | Elevance Health, Inc. Common Stock            |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | HD             | HD       | Home Depot, Inc. (The) Common Stock           |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | HLT            | HLT      | Hilton Worldwide Holdings Inc. Common Stock   |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | ICE            | ICE      | Intercontinental Exchange                     |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | KO             | KO       | Coca-Cola Company                             |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | RTX            | RTX      | RTX Corporation Common Stock                  |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | TXN            | TXN      | Texas Instruments Incorporated - Common Stock |           3 |       73,002 | 2023-10-12                 | (no data)         | False                                   |
| Jerry Moran          | BRK-B          | BRK-B    | Berkshire Hathaway Cl B                       |           6 |       72,503 | 2024-01-17                 | (no data)         | False                                   |
| Lindsey Graham       | USFR           | USFR     | Wisdomtree Floating Rate Treasury Fund        |           2 |       65,001 | 2024-01-26                 | (no data)         | False                                   |
| Markwayne Mullin     | C              | C        | Citigroup Inc                                 |           2 |       65,001 | 2026-02-04                 | (no data)         | False                                   |
| Markwayne Mullin     | CRS            | CRS      | Carpenter Technology Corporation Common Stock |           2 |       65,001 | 2026-02-04                 | (no data)         | False                                   |
| Markwayne Mullin     | FCFS           | FCFS     | FirstCash Holdings, Inc. - Common Stock       |           2 |       65,001 | 2026-02-04                 | (no data)         | False                                   |
| Markwayne Mullin     | INTU           | INTU     | Intuit Inc. - Common Stock                    |           2 |       65,001 | 2025-10-01                 | (no data)         | False                                   |
| Markwayne Mullin     | LHX            | LHX      | L3Harris Technologies Inc                     |           2 |       65,001 | 2025-02-27                 | (no data)         | False                                   |
| Markwayne Mullin     | MCK            | MCK      | McKesson Corporation Common Stock             |           2 |       65,001 | 2026-02-04                 | (no data)         | False                                   |
| Markwayne Mullin     | MPWR           | MPWR     | Monolithic Power Systems, Inc. - Common Stock |           2 |       65,001 | 2026-02-04                 | (no data)         | False                                   |
| Markwayne Mullin     | TJX            | TJX      | TJX Companies, Inc. (The) Common Stock        |           2 |       65,001 | 2024-09-19                 | (no data)         | False                                   |
| Markwayne Mullin     | VSEC           | VSEC     | VSE Corporation - Common Stock                |           2 |       65,001 | 2026-02-04                 | (no data)         | False                                   |
| Sheldon Whitehouse   | LLY            | LLY      | Eli Lilly and Company                         |           2 |       65,001 | 2023-10-17                 | (no data)         | False                                   |
| Tommy Tuberville     | HPQ            | HPQ      | HP Inc. Common Stock                          |           2 |       65,001 | 2023-11-16                 | (no data)         | False                                   |
| John Boozman         | FTGC           | FTGC     | First Trust Global Tactical Commodity Strateg |           5 |       64,502 | 2024-10-18                 | (no data)         | False                                   |
| John Boozman         | GOOGL          | GOOGL    | Alphabet Inc. - Class A Common Stock          |           5 |       64,502 | 2024-08-06                 | (no data)         | False                                   |
| John Boozman         | IEF            | IEF      | iShares 7-10 Year Treasury Bond ETF           |           5 |       64,502 | 2024-10-18                 | (no data)         | False                                   |
| Tommy Tuberville     | MMM            | MMM      | 3M Company Common Stock                       |           5 |       64,502 | 2022-02-14                 | (no data)         | False                                   |
| John Boozman         | GIGB           | GIGB     | Goldman Sachs Access Investment Grade Corpora |           8 |       64,004 | 2024-06-05                 | (no data)         | False                                   |
| John Boozman         | JMBS           | JMBS     | Janus Henderson Mortgage-Backed Securities ET |           8 |       64,004 | 2023-12-12                 | (no data)         | False                                   |
| John Boozman         | MSFT           | MSFT     | Microsoft Corp                                |           8 |       64,004 | 2024-07-11                 | (no data)         | False                                   |
| John Boozman         | SPYM           | SPYM     | State Street SPDR Portfolio S&P 500 ETF       |           4 |       56,502 | 2026-01-13                 | (no data)         | False                                   |
| John Boozman         | VEA            | VEA      | Vanguard FTSE Developed Markets ETF           |           4 |       56,502 | 2024-07-11                 | (no data)         | False                                   |
| John Boozman         | TLH            | TLH      | iShares 10-20 Year Treasury Bond ETF          |           7 |       56,004 | 2023-12-12                 | (no data)         | False                                   |
| John Boozman         | IEI            | IEI      | iShares 3-7 Year Treasury Bond ETF            |           3 |       48,502 | 2024-10-18                 | (no data)         | False                                   |
| Tommy Tuberville     | UAA            | UAA      | Under Armour, Inc. Class A Common Stock       |           3 |       48,502 | 2023-02-14                 | (no data)         | False                                   |
| John Boozman         | CMBS           | CMBS     | iShares CMBS Bond ETF                         |           6 |       48,003 | 2024-10-18                 | (no data)         | False                                   |
| John Boozman         | MBB            | MBB      | iShares MBS ETF                               |           6 |       48,003 | 2023-12-12                 | (no data)         | False                                   |
| John Boozman         | SCHP           | SCHP     | Schwab U.S. TIPS ETF                          |           6 |       48,003 | 2024-07-11                 | (no data)         | False                                   |
| Tommy Tuberville     | FGBI           | FGBI     | First Guaranty Bancshares, Inc. - Common Stoc |           6 |       48,003 | 2022-04-08                 | (no data)         | False                                   |
| Alan Armstrong       | BHP            | BHP      | BHP Group Limited (BHP)                       |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GS             | GS       | Goldman Sachs Group, Inc. (The) Common Stock  |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | JNJ            | JNJ      | Johnson & Johnson Common Stock                |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MSFT           | MSFT     | Microsoft Corporation - Common Stock          |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NVS            | NVS      | Novartis AG Common Stock                      |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RYCEY          | RYCEY    | Rolls Royce Holdings plc Sponsored ADR (RYCEY |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SAN            | SAN      | Banco Santander, S.A. Sponsored ADR (Spain)   |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SAP            | SAP      | SAP SE Sponsored ADR (SAP)                    |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SBGSY          | SBGSY    | Schneider Electric SE Unsponsored ADR (SBGSY) |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TSLA           | TSLA     | Tesla, Inc. - Common Stock                    |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UNCRY          | UNCRY    | Unicredit SPA Unsponsored ADR (UNCRY)         |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ZURVY          | ZURVY    | Zurich Insurance Group Ltd Sponsored ADR (ZUR |           2 |       40,501 | 2026-07-21                 | (no data)         | False                                   |
| Gary C. Peters       | O              | O        | Realty Income Corporation Common Stock        |           2 |       40,501 | 2023-04-12                 | (no data)         | False                                   |
| John Boozman         | EIPI           | EIPI     | First Trust Exchange-Traded Fund VIII FT Ener |           2 |       40,501 | 2025-11-15                 | (no data)         | False                                   |
| John Boozman         | XTWO           | XTWO     | BondBloxx Bloomberg Two Year Target Duration  |           2 |       40,501 | 2026-03-06                 | (no data)         | False                                   |
| Markwayne Mullin     | BLK            | BLK      | BlackRock, Inc. Common Stock                  |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | BRK-B          | BRK-B    | Berkshire Hathaway Cl B                       |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | CMCSA          | CMCSA    | Comcast Corporation - Class A Common Stock    |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | CMG            | CMG      | Chipotle Mexican Grill                        |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | COHR           | COHR     | Coherent Corp                                 |           2 |       40,501 | 2025-01-31                 | (no data)         | False                                   |
| Markwayne Mullin     | CRDO           | CRDO     | Credo Technology Group Holding Ltd            |           2 |       40,501 | 2025-01-31                 | (no data)         | False                                   |
| Markwayne Mullin     | DELL           | DELL     | Dell Technologies Inc. Class C Common Stock   |           2 |       40,501 | 2025-01-31                 | (no data)         | False                                   |
| Markwayne Mullin     | EMR            | EMR      | Emerson Electric Company                      |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | EW             | EW       | Edwards Lifesciences Corporation Common Stock |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | FISV           | FI       | Fiserv, Inc. Common Stock                     |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | HON            | HON      | Honeywell International Inc                   |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | IRM            | IRM      | Iron Mountain Inc                             |           2 |       40,501 | 2025-01-31                 | (no data)         | False                                   |
| Markwayne Mullin     | MTZ            | MTZ      | Mastec Inc                                    |           2 |       40,501 | 2025-01-31                 | (no data)         | False                                   |
| Markwayne Mullin     | NKE            | NKE      | Nike Inc                                      |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | NOW            | NOW      | ServiceNow, Inc. Common Stock                 |           2 |       40,501 | 2025-10-01                 | (no data)         | False                                   |
| Markwayne Mullin     | PANW           | PANW     | Palo Alto Networks, Inc. - Common Stock       |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | PEP            | PEP      | Pepsico Inc                                   |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | PG             | PG       | Procter & Gamble Company                      |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | PRMB           | PRMB     | Primo Brands Corporation Cl A                 |           2 |       40,501 | 2025-01-31                 | (no data)         | False                                   |
| Markwayne Mullin     | SBUX           | SBUX     | Starbucks Corporation - Common Stock          |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | SHW            | SHW      | Sherwin-Williams Company                      |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | SPGI           | SPGI     | S&P Global Inc. Common Stock                  |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | STZ            | STZ      | Constellation Brands, Inc. Common Stock       |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | UNP            | UNP      | Union Pacific Corporation Common Stock        |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | V              | V        | Visa Inc                                      |           2 |       40,501 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | WAB            | WAB      | Wabtec Corp                                   |           2 |       40,501 | 2025-01-31                 | (no data)         | False                                   |
| Sheldon Whitehouse   | TSLA           | TSLA     | Tesla, Inc. - Common Stock                    |           2 |       40,501 | 2022-03-16                 | (no data)         | False                                   |
| John Boozman         | META           | META     | Meta Platforms Inc                            |           5 |       40,002 | 2025-05-14                 | (no data)         | False                                   |
| John Boozman         | NVDA           | NVDA     | Nvidia Corp                                   |           5 |       40,002 | 2025-02-08                 | (no data)         | False                                   |
| Alan Armstrong       | BNPQY          | BNPQY    | BNP Paribas SA ADR (BNPQY)                    |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BTI            | BTI      | British American Tobacco Industries, p.l.c. C |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | C              | C        | Citigroup, Inc. Common Stock                  |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CMWAY          | CMWAY    | Commonwealth Bank Australia Sponsored ADR (CM |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CSCO           | CSCO     | Cisco Systems, Inc. - Common Stock            |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DBOEY          | DBOEY    | Deutsche Boerse ADR (DBOEY)                   |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DBSDY          | DBSDY    | DBS Group Holdings Ltd Sponsored ADR (DBSDY)  |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DTEGY          | DTEGY    | Deutsche Telekom AG DE Sponsored ADR (DTEGY)  |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EADSY          | EADSY    | Airbus SE (EADSY)                             |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GE             | GE       | GE Aerospace Common Stock                     |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GSK            | GSK      | Glaxo Wellcome plc ADR (GSK)                  |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HSBC           | HSBC     | HSBC Holdings, plc. Common Stock              |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HTHIY          | HTHIY    | Hitachi Ltd ADR Japan (HTHIY)                 |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ISNPY          | ISNPY    | Intesa Sanpaolo Sponsored ADR (ISNPY)         |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KO             | KO       | Coca-Cola Company (The) Common Stock          |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LRLCY          | LRLCY    | Loreal Company ADR France (LRLCY)             |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | META           | META     | Meta Platforms, Inc. - Class A Common Stock   |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MFG            | MFG      | Mizuho Financial Group, Inc. Sponosred ADR (J |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MHVIY          | MHVIY    | Mitsubishi Heavy Industries Ltd ADR (MHVIY)   |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MITSY          | MITSY    | Mitsui & Co Ltd ADR Japan (MITSY)             |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MTSUY          | MTSUY    | Mitsubishi Corporation ADR (MTSUY)            |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MU             | MU       | Micron Technology, Inc. - Common Stock        |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NABZY          | NABZY    | National Australia Bank Ltd Sponsored ADR (NA |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NFLX           | NFLX     | Netflix, Inc. - Common Stock                  |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NSRGY          | NSRGY    | Nestle SA Sponsored ADR (NSRGY)               |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NVO            | NVO      | Novo Nordisk A/S Common Stock                 |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ORCL           | ORCL     | Oracle Corporation Common Stock               |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PLTR           | PLTR     | Palantir Technologies Inc. - Class A Common S |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RHHBY          | RHHBY    | Roche Holdings Ltd Sponsored ADR (RHHBY)      |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RIO            | RIO      | Rio Tinto Plc Common Stock                    |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RTX            | RTX      | RTX Corporation Common Stock                  |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SAFRY          | SAFRY    | Safran SA ADR (SAFRY)                         |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SIEGY          | SIEGY    | Siemens AG Sponsored ADR (SIEGY)              |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SMERY          | SMERY    | Siemens Energy AG Sponsored ADR (SMERY)       |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SMFG           | SMFG     | Sumitomo Mitsui Financial Group Inc Unsponsor |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SNY            | SNY      | Sanofi - American Depositary Shares           |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SONY           | SONY     | Sony Group Corporation American Depositary Sh |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | T              | T        | AT&T Inc.                                     |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TM             | TM       | Toyota Motor Corporation Common Stock         |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TOELY          | TOELY    | Tokyo Electron Ltd ADR (TOELY)                |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UBS            | UBS      | UBS Group AG Registered Ordinary Shares       |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UL             | UL       | Unilever PLC (UL)                             |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UNH            | UNH      | UnitedHealth Group Incorporated Common Stock  |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UNP            | UNP      | Union Pacific Corporation Common Stock        |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | V              | V        | Visa Inc.                                     |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VCISY          | VCISY    | Vinci S.A. ADR (VCISY)                        |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | WFAFY          | WFAFY    | Wesfarmers Ltd Unsponsored ADR (WFAFY)        |           1 |       32,500 | 2026-07-21                 | (no data)         | False                                   |
| Ashley Moody         | ET             | ET       | ET                                            |           1 |       32,500 | 2025-05-13                 | (no data)         | False                                   |
| Ashley Moody         | JPM            | JPM      | JPM                                           |           1 |       32,500 | 2025-05-13                 | (no data)         | False                                   |
| Dan Sullivan         | MSFT           | MSFT     | Microsoft Corporation - Common Stock          |           1 |       32,500 | 2022-12-21                 | (no data)         | False                                   |
| Gary C. Peters       | PEP            | PEP      | PEP - PepsiCo, Inc. - Common Stock            |           1 |       32,500 | 2026-05-11                 | (no data)         | False                                   |
| Gary C. Peters       | SWK            | SWK      | Stanley Black & Decker Inc                    |           1 |       32,500 | 2026-01-20                 | (no data)         | False                                   |
| Gary C. Peters       | WPC            | WPC      | W. P. Carey Inc. REIT                         |           1 |       32,500 | 2026-01-20                 | (no data)         | False                                   |
| John Boozman         | SCZ            | SCZ      | iShares MSCI EAFE Small-Cap ETF               |           1 |       32,500 | 2024-05-07                 | (no data)         | False                                   |
| Lindsey Graham       | BSCQ           | BSCQ     | Invesco BulletShares 2026 Corporate Bond ETF  |           1 |       32,500 | 2026-01-06                 | (no data)         | False                                   |
| Lindsey Graham       | BSCV           | BSCV     | Invesco BulletShares 2031 Corporate Bond ETF  |           1 |       32,500 | 2025-07-14                 | (no data)         | False                                   |
| Lindsey Graham       | IBDQ           | IBDQ     | iShares iBonds Dec 2025 Term Corporate ETF    |           1 |       32,500 | 2022-07-13                 | (no data)         | False                                   |
| Lindsey Graham       | XONE           | XONE     | Boxx One Year Target Duration ETF             |           1 |       32,500 | 2025-07-14                 | (no data)         | False                                   |
| Markwayne Mullin     | DHR            | DHR      | Danaher Corporation Common Stock              |           1 |       32,500 | 2023-10-12                 | (no data)         | False                                   |
| Markwayne Mullin     | PH             | PH       | Parker-Hannifin Corporation Common Stock      |           1 |       32,500 | 2024-07-12                 | (no data)         | False                                   |
| Markwayne Mullin     | PM             | PM       | Philip Morris International Inc               |           1 |       32,500 | 2025-02-27                 | (no data)         | False                                   |
| Markwayne Mullin     | PNR            | PNR      | Pentair plc. Ordinary Share                   |           1 |       32,500 | 2025-12-05                 | (no data)         | False                                   |
| Markwayne Mullin     | TMUS           | TMUS     | T-Mobile US                                   |           1 |       32,500 | 2023-10-12                 | (no data)         | False                                   |
| Sheldon Whitehouse   | COHR           | COHR     | Coherent Corp. Common Stock                   |           1 |       32,500 | 2026-07-08                 | (no data)         | False                                   |
| Sheldon Whitehouse   | NVS            | NVS      | Novartis Ag ADR                               |           1 |       32,500 | 2023-10-17                 | (no data)         | False                                   |
| Sheldon Whitehouse   | TGT            | TGT      | Target Corporation Common Stock               |           1 |       32,500 | 2022-03-16                 | (no data)         | False                                   |
| Tommy Tuberville     | DHS            | DHS      | Wisdomtree U.S. High Dividend Fund            |           1 |       32,500 | 2022-09-15                 | (no data)         | False                                   |
| Tommy Tuberville     | EVT            | EVT      | Eaton Vance Tax Advantaged Dividend Income Fu |           1 |       32,500 | 2022-07-13                 | (no data)         | False                                   |
| Tommy Tuberville     | IDV            | IDV      | iShares International Select Dividend ETF     |           1 |       32,500 | 2022-09-15                 | (no data)         | False                                   |
| Tommy Tuberville     | OC             | OC       | Owens Corning Inc Common Stock New            |           1 |       32,500 | 2022-09-15                 | (no data)         | False                                   |
| Tommy Tuberville     | OXY            | OXY      | Occidental Petroleum Corporation Common Stock |           1 |       32,500 | 2023-06-15                 | (no data)         | False                                   |
| Tommy Tuberville     | RSP            | RSP      | Invesco S&P 500 Equal Weight ETF              |           1 |       32,500 | 2022-09-15                 | (no data)         | False                                   |
| Tommy Tuberville     | XLP            | XLP      | SPDR Select Sector Fund - Consumer Staples    |           1 |       32,500 | 2026-01-15                 | (no data)         | False                                   |
| Tommy Tuberville     | XLU            | XLU      | SPDR Select Sector Fund - Utilities           |           1 |       32,500 | 2026-01-15                 | (no data)         | False                                   |
| Tommy Tuberville     | XLV            | XLV      | SPDR Select Sector Fund - Health Care         |           1 |       32,500 | 2026-01-15                 | (no data)         | False                                   |
| John Boozman         | PALL           | PALL     | abrdn Physical Palladium Shares ETF           |           4 |       32,002 | 2024-01-08                 | (no data)         | False                                   |
| John Boozman         | SHY            | SHY      | iShares 1-3 Year Treasury Bond ETF            |           4 |       32,002 | 2023-12-12                 | (no data)         | False                                   |
| John Boozman         | TLT            | TLT      | 20+ Year Treas Bond Ishares ETF               |           4 |       32,002 | 2023-12-12                 | (no data)         | False                                   |
| Tommy Tuberville     | PFE            | PFE      | Pfizer, Inc. Common Stock                     |           4 |       32,002 | 2022-02-14                 | (no data)         | False                                   |
| Jerry Moran          | GOOG           | GOOG     | Alphabet Cl C                                 |           3 |       24,002 | 2025-06-18                 | (no data)         | False                                   |
| John Boozman         | GEM            | GEM      | Goldman Sachs ActiveBeta Emerging Markets Equ |           3 |       24,002 | 2024-07-11                 | (no data)         | False                                   |
| John Boozman         | PYPL           | PYPL     | Paypal Holdings                               |           3 |       24,002 | 2025-12-08                 | (no data)         | False                                   |
| Sheldon Whitehouse   | KO             | KO       | Coca-Cola Company                             |           3 |       24,002 | 2024-01-18                 | (no data)         | False                                   |
| Tommy Tuberville     | CFG            | CFG      | Citizens Financial Group, Inc. Common Stock   |           3 |       24,002 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | FITB           | FITB     | Fifth Third Bancorp - Common Stock            |           3 |       24,002 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | VCTR           | VCTR     | Victory Capital Holdings, Inc. - Common Stock |           3 |       24,002 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | VZ             | VZ       | Verizon Communications Inc. Common Stock      |           3 |       24,002 | 2022-02-14                 | (no data)         | False                                   |
| Alan Armstrong       | CFRUY          | CFRUY    | Compagnie Financiere Richemont AG ADR (CFRUY) |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CIEN           | CIEN     | Ciena Corporation Common Stock                |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CRRFY          | CRRFY    | Carrefour SA Sponsored ADR (CRRFY)            |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DGX            | DGX      | Quest Diagnostics Incorporated Common Stock   |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DSDVY          | DSDVY    | DSV A/S ADR (DSDVY)                           |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EA             | EA       | Electronic Arts Inc. - Common Stock           |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GLNCY          | GLNCY    | Glencore plc Unsponsored ADR (GLNCY)          |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HEINY          | HEINY    | Heineken NV Sponsored ADR (HEINY)             |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KKPNY          | KKPNY    | Royal KPN N.V. Sponsored ADR (KKPNY)          |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LRCX           | LRCX     | Lam Research Corporation (LRCX)               |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ORLY           | ORLY     | O'Reilly Automotive, Inc. - Common Stock      |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SCHW           | SCHW     | Charles Schwab Corporation (The) Common Stock |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SCMWY          | SCMWY    | Swisscom AG Sponsored ADR (SCMWY)             |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | WELL           | WELL     | Welltower Inc. Common Stock                   |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | WSE            | WSE      | Wise plc Sponsored ADR (WIZEY)                |           2 |       16,001 | 2026-07-21                 | (no data)         | False                                   |
| Dan Sullivan         | CHD            | CHD      | Church & Dwight Company, Inc. Common Stock    |           2 |       16,001 | 2023-03-16                 | (no data)         | False                                   |
| Dan Sullivan         | ZTS            | ZTS      | Zoetis Inc. Class A Common Stock              |           2 |       16,001 | 2022-12-21                 | (no data)         | False                                   |
| Gary C. Peters       | CAG            | CAG      | ConAgra Brands, Inc. Common Stock             |           2 |       16,001 | 2021-12-07                 | (no data)         | False                                   |
| Gary C. Peters       | VZ             | VZ       | VZ                                            |           2 |       16,001 | 2021-12-07                 | (no data)         | False                                   |
| John Boozman         | CEG            | CEG      | Constellation Energy Corporation - Common Sto |           2 |       16,001 | 2026-05-08                 | (no data)         | False                                   |
| John Boozman         | ETN            | ETN      | Eaton Corp                                    |           2 |       16,001 | 2025-10-10                 | (no data)         | False                                   |
| John Boozman         | HD             | HD       | Home Depot                                    |           2 |       16,001 | 2025-06-14                 | (no data)         | False                                   |
| John Boozman         | IVV            | IVV      | iShares Core S&P 500 ETF                      |           2 |       16,001 | 2024-10-18                 | (no data)         | False                                   |
| John Boozman         | LITP           | LITP     | Sprott Lithium Miners ETF                     |           2 |       16,001 | 2025-03-06                 | (no data)         | False                                   |
| John Boozman         | LLY            | LLY      | Eli Lilly and Company                         |           2 |       16,001 | 2025-09-12                 | (no data)         | False                                   |
| John Boozman         | MA             | MA       | Mastercard Incorporated Common Stock          |           2 |       16,001 | 2025-02-08                 | (no data)         | False                                   |
| John Boozman         | MSI            | MSI      | Motorola Solutions, Inc. Common Stock         |           2 |       16,001 | 2024-08-06                 | (no data)         | False                                   |
| John Boozman         | PPLT           | PPLT     | abrdn Physical Platinum Shares ETF            |           2 |       16,001 | 2024-01-08                 | (no data)         | False                                   |
| John Boozman         | UNH            | UNH      | Unitedhealth Group Inc                        |           2 |       16,001 | 2025-05-14                 | (no data)         | False                                   |
| John Boozman         | VNQI           | VNQI     | Vanguard Global ex-U.S. Real Estate ETF       |           2 |       16,001 | 2025-09-12                 | (no data)         | False                                   |
| Tommy Tuberville     | CBSH           | CBSH     | Commerce Bancshares, Inc. - Common Stock      |           2 |       16,001 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | CSCO           | CSCO     | Cisco Systems, Inc. - Common Stock            |           2 |       16,001 | 2022-02-14                 | (no data)         | False                                   |
| Tommy Tuberville     | MPWR           | MPWR     | Monolithic Power Systems, Inc. - Common Stock |           2 |       16,001 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | MRSH           | MMC      | Marsh & McLennan Companies, Inc. Common Stock |           2 |       16,001 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | NFLX           | NFLX     | Netflix, Inc. - Common Stock                  |           2 |       16,001 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | ODFL           | ODFL     | Old Dominion Freight Line, Inc. - Common Stoc |           2 |       16,001 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | PHM            | PHM      | PulteGroup, Inc. Common Stock                 |           2 |       16,001 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | RF             | RF       | Regions Financial Corporation Common Stock    |           2 |       16,001 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | RMD            | RMD      | ResMed Inc. Common Stock                      |           2 |       16,001 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | RYCEY          | RYCEY    | ROLLS-ROYCE HOLDINGS PLC SPONSORED ADR        |           2 |       16,001 | 2024-04-15                 | (no data)         | False                                   |
| Alan Armstrong       | AVB            | AVB      | AvalonBay Communities, Inc. Common Stock      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BDX            | BDX      | Becton, Dickinson and Company Common Stock    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BEN            | BEN      | Franklin Resources, Inc. Common Stock         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BG             | BG       | Bunge Limited Common Shares                   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BHKLY          | BHKLY    | Boc Hong Kong Holdings Ltd Sponsored ADR (BHK |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BIIB           | BIIB     | Biogen Inc. - Common Stock                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BKNG           | BKNG     | Booking Holdings Inc. - Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BKNIY          | BKNIY    | Bankinter SA Sponsored ADR (BKNIY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BMWKY          | BMWKY    | Bayerische Motors Werke AG ADR (BMWKY)        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BMY            | BMY      | Bristol-Myers Squibb Company Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BNTGY          | BNTGY    | Brenntag Se Unsponsored ADR (BNTGY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BNY            | BK       | Bank of New York Mellon Corp (BK)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BOUYY          | BOUYY    | Bouygues SA ADR (BOUYY)                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BR             | BR       | Broadridge Financial Solutions, Inc. Common S |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BRDCY          | BRDCY    | Bridgestone Corporation Ltd ADR Japan (BRDCY) |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BRO            | BRO      | Brown & Brown, Inc. Common Stock              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BRRLY          | BRRLY    | Barry Callebaut AG Unsponsored ADR (BRRLY)    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BSX            | BSX      | Boston Scientific Corporation Common Stock    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BTDPY          | BTDPY    | Barratt Redrow plc ADR (BTDPY)                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BUD            | BUD      | Anheuser-Busch Inbev SA Sponsored ADR (Belgiu |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BVVBY          | BVVBY    | Bureau Veritas SA Unsponsored ADR (BVVBY)     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BX             | BX       | Blackstone Inc. Common Stock                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BXBLY          | BXBLY    | Brambles Ltd Sponsored ADR (BXBLY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BXP            | BXP      | BXP, Inc. Common Stock                        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | BZLFY          | BZLFY    | Bunzl plc New Sponsored ADR (BZLFY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CABGY          | CABGY    | Carlsberg AS Sponsored ADR (CABGY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CAG            | CAG      | ConAgra Brands, Inc. Common Stock             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CAH            | CAH      | Cardinal Health, Inc. Common Stock            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CAIXY          | CAIXY    | Caixabank Unsponsored ADR (CAIXY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CAJPY          | CAJPY    | Canon Inc ADR Japan Sponsored (CAJPY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CB             | CB       | Chubb Limited Common Stock                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CBOE           | CBOE     | Cboe Global Markets, Inc. Common Stock        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CCEP           | CCEP     | Coca-Cola Europacific Partners plc - Ordinary |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CCHGY          | CCHGY    | Coca-Cola HBC AG ADR (CCHGY)                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CCI            | CCI      | Crown Castle Inc. Common Stock                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CCL            | CCL      | Carnival Corporation Ltd. Common Shares       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CCOEY          | CCOEY    | Capcom Co Ltd Unsponsored ADR (CCOEY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CF             | CF       | CF Industries Holdings, Inc. Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CGEMY          | CGEMY    | Capgemini SE Unsponsored (CGEMY)              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CHEOY          | CHEOY    | Cochlear Ltd ADR (CHEOY)                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CHGCY          | CHGCY    | Chugai Pharmaceutical Ltd DDR (CHGCY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CHKP           | CHKP     | Check Point Software Technologies Ltd. - Ordi |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CHTR           | CHTR     | Charter Communications, Inc. - Class A Common |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CI             | CI       | The Cigna Group Common Stock                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CJPRY          | CJPRY    | Central Japan RAI ADR (CJPRY)                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CKHUY          | CKHUY    | CK Hutchison Holdings Ltd Unsponsored ADR (CK |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CLLNY          | CLLNY    | Cellnex Telecom SAU Unsponsored ADR (CLLNY)   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CLPBY          | CLPBY    | Coloplast AS Sponsored ADR (CLPBY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CMCSA          | CMCSA    | Comcast Corporation - Class A Common Stock    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CME            | CME      | CME Group Inc. - Class A Common Stock         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CMPGY          | CMPGY    | Compass Group plc Sponsored ADR (CMPGY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CMSQY          | CMSQY    | Computershare Ltd Sponsored ADR (CMSQY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CODYY          | CODYY    | Compagnie de Saint-Gobain ADR (CODYY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | COF            | COF      | Capital One Financial Corporation Common Stoc |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | COIN           | COIN     | Coinbase Global, Inc. - Class A Common Stock  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | COO            | COO      | The Cooper Companies, Inc. - Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | COR            | COR      | Cencora, Inc. Common Stock                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | COST           | COST     | Costco Wholesale Corporation - Common Stock   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CPB            | CPB      | The Campbell's Company - Common Stock         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CPRT           | CPRT     | Copart, Inc. - Common Stock                   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CPT            | CPT      | Camden Property Trust Common Stock            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CRARY          | CRARY    | Credit Agricole SA ADR (CRARY)                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CRM            | CRM      | Salesforce, Inc. Common Stock                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CRZBY          | CRZBY    | Commerzbank AG Sponsored ADR (CRZBY)          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CSLLY          | CSLLY    | CSL Ltd Sponsored ADR (CSLLY)                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CSX            | CSX      | CSX Corporation - Common Stock                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CTSH           | CTSH     | Cognizant Technology Solutions Corporation -  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CTVA           | CTVA     | Corteva, Inc. Common Stock                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | CVS            | CVS      | CVS Health Corporation Common Stock           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DANOY          | DANOY    | Danone Sponsored ADR (DANOY)                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DASTY          | DASTY    | Dassault Systems SA Sponsored ADR (DASTY)     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DB             | DB       | Deutsche Bank AG Common Stock                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DDOG           | DDOG     | Datadog, Inc. - Class A Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DE             | DE       | Deere & Company Common Stock                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DELL           | DELL     | Dell Technologies Inc. Class C Common Stock   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DEO            | DEO      | Diageo plc Common Stock                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DFKCY          | DFKCY    | Daifuku Co Ltd ADR (DFKCY)                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DHLGY          | DHLGY    | Deutsche Post AG Sponsored ADR (DHLGY)        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DHR            | DHR      | Danaher Corporation Common Stock              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DIFTY          | DIFTY    | Daito Trust Construction Sponsored ADR (DIFTY |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DIS            | DIS      | Walt Disney Company (The) Common Stock        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DKILY          | DKILY    | Daikin Industries Ltd ADR (DKILY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DLAKY          | DLAKY    | Deutsche Lufthansa AG Sponsored ADR (DLAKY)   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DLICY          | DLICY    | Daiichi Life Holdings Inc Unsponsored ADR (DL |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DLR            | DLR      | Digital Realty Trust, Inc. Common Stock       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DNBBY          | DNBBY    | DNB BK ASA Sponsored ADR (DNBBY)              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DNKEY          | DNKEY    | Danske Bank A/S Sponsored ADR (DNKEY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DNZOY          | DNZOY    | Denso Corporation ADR (DNZOY)                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DOC            | DOC      | Healthpeak Properties, Inc. Common Stock      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DOV            | DOV      | Dover Corporation Common Stock                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DOW            | DOW      | Dow Inc. Common Stock                         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DPZ            | DPZ      | Domino's Pizza Inc - Common Stock             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DQJCY          | DQJCY    | Pan Pacific International Holdings Corporatio |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DRI            | DRI      | Darden Restaurants, Inc. Common Stock         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DRPRY          | DRPRY    | Dr. Ing. h.c. F. Porsche AG Unsponsored ADR ( |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DSCSY          | DSCSY    | Disco Corporation Unsponsored ADR (DSCSY)     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DSFIY          | DSFIY    | DSM Firmenich AG Sponsored ADR (DSFIY)        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DSNKY          | DSNKY    | Daiichi Sankyo Co Ltd Sponsored ADR (DSNKY)   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DTRUY          | DTRUY    | Daimler Truck Holding AG Sponsored ADR (DTRUY |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DUFRY          | DUFRY    | Avolta AG ADR (DUFRY)                         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DVA            | DVA      | DaVita Inc. Common Stock                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | DWAHY          | DWAHY    | Daiwa House Industries Ltd ADR Japan (DWAHY)  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EBAY           | EBAY     | eBay Inc. - Common Stock                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EBCOY          | EBCOY    | Ebara Corporation ADR (EBCOY)                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EBKDY          | EBKDY    | Erste Group Bank AG Sponsored ADR (EBKDY)     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EG             | EG       | Everest Group, Ltd. Common Stock              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EJPRY          | EJPRY    | East Japan Railway Co ADR (EJPRY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ELV            | ELV      | Elevance Health, Inc. Common Stock            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EME            | EME      | EMCOR Group, Inc. Common Stock                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EMR            | EMR      | Emerson Electric Company Common Stock         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EPOAY          | EPOAY    | Epiroc Aktiebolag Class A Sponsored ADR (EPOA |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ERIC           | ERIC     | Ericsson - ADR (ERIC)                         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ESAIY          | ESAIY    | Eisai Co Ltd ADR (ESAIY)                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ESLOY          | ESLOY    | Essilorluxottica ADR (ESLOY)                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ESLT           | ESLT     | Elbit Systems Ltd. - Ordinary Shares          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ESS            | ESS      | Essex Property Trust, Inc. Common Stock       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ETN            | ETN      | Eaton Corporation, PLC Ordinary Shares        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EVVTY          | EVVTY    | Evolution AB Unsponsored ADR (EVVTY)          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EW             | EW       | Edwards Lifesciences Corporation Common Stock |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EXPD           | EXPD     | Expeditors International of Washington, Inc.  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | EXPGY          | EXPGY    | Experian plc Sponsored ADR (EXPGY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | F              | F        | Ford Motor Company Common Stock               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FANUY          | FANUY    | Fanuc Corporation ADR (FANUY)                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FCX            | FCX      | Freeport-McMoRan, Inc. Common Stock           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FDX            | FDX      | FedEx Corporation Common Stock                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FFIV           | FFIV     | F5, Inc. - Common Stock                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FICO           | FICO     | Fair Isaac Corporation Common Stock           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FINMY          | FINMY    | Leonardo SPA ADR (FINMY)                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FIS            | FIS      | Fidelity National Information Services, Inc.  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FISV           | FISV     | Fiserv, Inc. - Common Stock                   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FIX            | FIX      | Comfort Systems USA, Inc. Common Stock        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FJTSY          | FJTSY    | Fujitsu Ltd ADR New Japan (FJTSY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FMS            | FMS      | Fresenius Medical Care AG (FMS)               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FOXA           | FOXA     | Fox Corporation - Class A Common Stock        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FRCOY          | FRCOY    | Fast Retailing Co Ltd ADR (FRCOY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FRT            | FRT      | Federal Realty Investment Trust Common Stock  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FSLR           | FSLR     | First Solar, Inc. - Common Stock              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FSNUY          | FSNUY    | Fresenius SE & Company Sponsored ADR (FSNUY)  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FSUGY          | FSUGY    | Fortescue Metals Group Ltd Sponsored ADR (FSU |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FTNT           | FTNT     | Fortinet, Inc. - Common Stock                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FTV            | FTV      | Fortive Corporation Common Stock              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FUJHY          | FUJHY    | Subaru Corporation Unsponsored ADR (FUJHY)    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | FUJIY          | FUJIY    | Fuji Film Holding Corporation ADR (FUJIY)     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GALDY          | GALDY    | Galderma Group AG Sponsored ADR (GALDY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GBERY          | GBERY    | Geberit AG ADR (GBERY)                        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GD             | GD       | General Dynamics Corporation Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GDDY           | GDDY     | GoDaddy Inc. Class A Common Stock             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GEHC           | GEHC     | GE HealthCare Technologies Inc. - Common Stoc |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GEN            | GEN      | Gen Digital Inc. - Common Stock               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GILD           | GILD     | Gilead Sciences, Inc. - Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GIS            | GIS      | General Mills, Inc. Common Stock              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GL             | GL       | Globe Life Inc. Common Stock                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GM             | GM       | General Motors Company Common Stock           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GMAB           | GMAB     | Genmab A/S - American Depositary Shares       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GPC            | GPC      | Genuine Parts Company Common Stock            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GPN            | GPN      | Global Payments Inc. Common Stock             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | GVDNY          | GVDNY    | Givaudan SA ADR (GVDNY)                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HAGHY          | HAGHY    | Hensoldt AG ADR (HAGHY)                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HALMY          | HALMY    | Halma plc Unsponsored ADR (HALMY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HAS            | HAS      | Hasbro, Inc. - Common Stock                   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HBAN           | HBAN     | Huntington Bancshares Incorporated - Common S |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HCA            | HCA      | HCA Healthcare, Inc. Common Stock             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HCMLY          | HCMLY    | Holcim Ltd Sponsored ADR (HCMLY)              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HDLMY          | HDLMY    | Heidelbergcement AG ADR Sponsored (HDLMY)     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HENKY          | HENKY    | Henkel AG & Co KGAA Sponsored ADR (HENKY)     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HENOY          | HENOY    | Henkel AG & Company KGAA PFD Sponsored ADR (H |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HESAY          | HESAY    | Hermes International SCA ADR (HESAY)          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HIG            | HIG      | The Hartford Insurance Group, Inc. Common Sto |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HKXCY          | HKXCY    | Hong Kong Exchanges & Clearing Ltd ADR (HKXCY |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HLN            | HLN      | Haleon plc Sponsored ADR (HLN)                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HLT            | HLT      | Hilton Worldwide Holdings Inc. Common Stock   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HMC            | HMC      | Honda Motor Company, Ltd. Common Stock        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HNNMY          | HNNMY    | Hennes & Mauritz AB ADR (HNNMY)               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HOCPY          | HOCPY    | Hoya Corporation Sponsored ADR (HOCPY)        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HON            | HON      | Honeywell International Inc. - Common Stock   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HOOD           | HOOD     | Robinhood Markets, Inc. - Class A Common Stoc |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HPE            | HPE      | Hewlett Packard Enterprise Company Common Sto |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HPQ            | HPQ      | HP Inc. Common Stock                          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HSY            | HSY      | The Hershey Company Common Stock              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HUBB           | HUBB     | Hubbell Inc Common Stock                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HUM            | HUM      | Humana Inc. Common Stock                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HVRRY          | HVRRY    | Hannover Rueck SE Sponsored ADR (HVRRY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HWM            | HWM      | Howmet Aerospace Inc. Common Stock            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | HXGBY          | HXGBY    | Hexagon AB Unsponsored ADR (HXGBY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | IBM            | IBM      | International Business Machines Corporation C |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ICAGY          | ICAGY    | International Consolidated Airlines Group Spo |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ICE            | ICE      | Intercontinental Exchange Inc. Common Stock   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ICL            | ICL      | ICL Group Ltd. Ordinary Shares                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | IDEXY          | IDEXY    | Industria De Diseno Textil Inditex ADR (IDEXY |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | IFJPY          | IFJPY    | Informa plc Sponsored ADR (IFJPY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | IFNNY          | IFNNY    | Infineon Technologies ADR (IFNNY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | IHG            | IHG      | Intercontinental Hotels Group American (IHG)  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | IHICY          | IHICY    | IHI Corporation Unsponsored ADR (IHICY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ING            | ING      | ING Group, N.V. Common Stock                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | INTC           | INTC     | Intel Corporation - Common Stock              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | INTU           | INTU     | Intuit Inc. - Common Stock                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | INVH           | INVH     | Invitation Homes Inc. Common Stock            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ISMAY          | ISMAY    | Indra Sistemas ADR (ISMAY)                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ISRG           | ISRG     | Intuitive Surgical, Inc. - Common Stock       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ISUZY          | ISUZY    | Isuzu Motor Company Ltd ADR (ISUZY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ITOCY          | ITOCY    | Itochu Corporation ADR Japan (ITOCY)          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | IX             | IX       | ORIX Corporation American Depositary Shares   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | JAPAY          | JAPAY    | Japan Tobacco Inc Unsponsored ADR (JAPAY)     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | JBAXY          | JBAXY    | Julius Baer Group Ltd ADR (JBAXY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | JMHLY          | JMHLY    | Jardine Matheson Holdings Unsponsored ADR (JM |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | JPXGY          | JPXGY    | Japan Exchange Group Inc Unsponsored ADR (JPX |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | JRONY          | JRONY    | Jeronimo Martins SGPS SA ADR (JRONY)          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | JSAIY          | JSAIY    | J. Sainsbury plc Sponsored ADR (JSAIY)        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KAOOY          | KAOOY    | Kao Corporation Unsponsored ADR (KAOOY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KBCSY          | KBCSY    | KBC Group NV ADR (KBCSY)                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KBGGY          | KBGGY    | Kongsberg Gruppen ASA ADR (KBGGY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KDDIY          | KDDIY    | KDDI Corporation ADR (KDDIY)                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KDP            | KDP      | Keurig Dr Pepper Inc. - Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KEY            | KEY      | KeyCorp Common Stock                          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KGFHY          | KGFHY    | Kingfisher plc Sponsored ADR (KGFHY)          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KHC            | KHC      | The Kraft Heinz Company - Common Stock        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KHNGY          | KHNGY    | Kuehne & Nagel International AG ADR (KHNGY)   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KIM            | KIM      | Kimco Realty Corporation (HC) Common Stock    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KKR            | KKR      | KKR & Co. Inc. Common Stock                   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KLAC           | KLAC     | KLA Corporation - Common Stock                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KMB            | KMB      | Kimberly-Clark Corporation - Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KMTUY          | KMTUY    | Komatsu Ltd Sponsored ADR (KMTUY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KNBWY          | KNBWY    | Kirin Holdings Ltd Sponsored ADR (KNBWY)      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KNRRY          | KNRRY    | Knorr-Bremse Unsponsored ADR (KNRRY)          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KNYJY          | KNYJY    | Kone Oyj ADR (KNYJY)                          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KUBTY          | KUBTY    | Kubota Corporation ADR Japan (KUBTY)          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KVUE           | KVUE     | Kenvue Inc. Common Stock                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KWHIY          | KWHIY    | Kawaski Heavy Industries Sponsored ADR (KWHIY |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | KXIAY          | KXIAY    | Kioxia Holdings Corporation ADR (KXIAY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | L              | L        | Loews Corporation (L)                         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LDSCY          | LDSCY    | Land Secs Group plc ADR (LDSCY)               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LEN            | LEN      | Lennar Corporation Class A Common Stock       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LGGNY          | LGGNY    | Legal & General Group plc Sponsored ADR (LGGN |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LGRDY          | LGRDY    | Legrand SA Unsponsored ADR (LGRDY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LH             | LH       | Labcorp Holdings Inc. Common Stock            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LHX            | LHX      | L3Harris Technologies, Inc. Common Stock      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LITE           | LITE     | Lumentum Holdings Inc. - Common Stock         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LMT            | LMT      | Lockheed Martin Corporation Common Stock      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LOGI           | LOGI     | Logitech International S.A. - Registered Shar |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LOW            | LOW      | Lowe's Companies, Inc. Common Stock           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LSEGY          | LSEGY    | London Stock Exchange Group Sponsored ADR (LS |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LSRCY          | LSRCY    | Lasertec Corporation ADR (LSRCY)              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LYB            | LYB      | LyondellBasell Industries NV Ordinary Shares  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LYG            | LYG      | Lloyds Banking Group Plc American Depositary  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LYSDY          | LYSDY    | Lynas Rare Earths Ltd Sponsored ADR (LYSDY)   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LYV            | LYV      | Live Nation Entertainment, Inc. Common Stock  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | LZAGY          | LZAGY    | Lonza Group AG ADR (LZAGY)                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MAA            | MAA      | Mid-America Apartment Communities, Inc. Commo |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MAR            | MAR      | Marriott International - Class A Common Stock |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MARUY          | MARUY    | Marubeni Corporation ADR Japan (MARUY)        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MBGYY          | MBGYY    | Mercedes-Benz Group AG Unsponsored ADR (MBGYY |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MCD            | MCD      | McDonald's Corporation Common Stock           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MCHP           | MCHP     | Microchip Technology Incorporated - Common St |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MCK            | MCK      | McKesson Corporation Common Stock             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MDT            | MDT      | Medtronic plc. Ordinary Shares                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MET            | MET      | MetLife, Inc. Common Stock                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MGDDY          | MGDDY    | Michelin Compagnie Generale ADR (MGDDY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MGM            | MGM      | MGM Resorts International Common Stock        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MIELY          | MIELY    | Mitsubishi Electric Corporation ADR Japan (MI |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MITEY          | MITEY    | Mitsubishi Estate Ltd ADR (MITEY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MMM            | MMM      | 3M Company Common Stock                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MNDY           | MNDY     | monday.com Ltd. - Ordinary Shares             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MO             | MO       | Altria Group, Inc.                            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MONRY          | MONRY    | Moncler SPA Unsponsored ADR (MONRY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MOS            | MOS      | Mosaic Company (The) Common Stock             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MQBKY          | MQBKY    | Macquarie Group Ltd Unsponsored ADR (MQBKY)   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MRAAY          | MRAAY    | Murata MFG Co Ltd ADR (MRAAY)                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MS             | MS       | Morgan Stanley Common Stock                   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MSADY          | MSADY    | MS&AD Insurance Group Holdings ADR (MSADY)    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MSCI           | MSCI     | MSCI Inc. Common Stock                        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MSI            | MSI      | Motorola Solutions, Inc. Common Stock         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MSLOY          | MSLOY    | Mitsui Osk Lines Ltd Unsponsored ADR (MSLOY)  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MT             | MT       | Arcelor Mittal NY Registry Shares NEW         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MTSFY          | MTSFY    | Mitsui Fudosan Co Ltd ADR (MTSFY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | MURGY          | MURGY    | Munich Re Group ADR (MURGY)                   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NBIS           | NBIS     | Nebius Group N.V. - Class A Ordinary Shares   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NCBDY          | NCBDY    | Bandai Namco Holdings Inc ADR (NCBDY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NEM            | NEM      | Newmont Corporation                           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NEXOY          | NEXOY    | Nexon Company Ltd Unsponsored ADR (NEXOY)     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NGLOY          | NGLOY    | Anglo American plc Sponsored ADR (NGLOY)      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NHYDY          | NHYDY    | Norsk Hydro A.S. New Norway Sponsored ADR (NH |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NICE           | NICE     | NICE Ltd - (NICE)                             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NKE            | NKE      | Nike, Inc. Common Stock                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NMR            | NMR      | Nomura Holdings Inc ADR American Depositary S |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NNGRY          | NNGRY    | NN Group NV Unsponsored ADR (NNGRY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NOC            | NOC      | Northrop Grumman Corporation Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NOK            | NOK      | Nokia Corporation Sponsored American Deposita |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NPNYY          | NPNYY    | Nippon Yusen Kabushiki Sponsored ADR (NPNYY)  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NPSCY          | NPSCY    | Nippon Steel Corporation Unsponsored ADR (NPS |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NRDBY          | NRDBY    | Nordea BK ABP Sponsored ADR (NRDBY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NRILY          | NRILY    | Nomura Research Institute Ltd ADR (NRILY)     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NSC            | NSC      | Norfolk Southern Corporation Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NTDOY          | NTDOY    | Nintendo Ltd ADR Japan (NTDOY)                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NTTYY          | NTTYY    | NTT Inc Sponsored ADR (NTTYY)                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NUE            | NUE      | Nucor Corporation Common Stock                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NVZMY          | NVZMY    | Novonesis B ADR (NVZMY)                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NWG            | NWG      | NatWest Group plc (NWG)                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | NXPI           | NXPI     | NXP Semiconductors N.V. - Common Stock        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | O              | O        | Realty Income Corporation Common Stock        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | OBICY          | OBICY    | Obic Co Ltd ADR (OBICY)                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | OLCLY          | OLCLY    | Oriental Land Co Ltd Unsponsored ADR (OLCLY)  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | OMC            | OMC      | Omnicom Group Inc. Common Stock               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ORANY          | ORANY    | Orange Sponsored ADR (ORANY)                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ORKLY          | ORKLY    | Orkla ASA Sponsored ADR (ORKLY)               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | OTIS           | OTIS     | Otis Worldwide Corporation Common Stock       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | OTSKY          | OTSKY    | Otsuka Holdings Co Ltd Unsponsored ADR (OTSKY |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | OVCHY          | OVCHY    | Overseas-Chinese Bank ADR (OVCHY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PANW           | PANW     | Palo Alto Networks, Inc. - Common Stock       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PCAR           | PCAR     | PACCAR Inc. - Common Stock                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PCRHY          | PCRHY    | Panasonic Corporation ADR (PCRHY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PEP            | PEP      | PepsiCo, Inc. - Common Stock                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PFG            | PFG      | Principal Financial Group Inc - Common Stock  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PH             | PH       | Parker-Hannifin Corporation Common Stock      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PHG            | PHG      | Koninklijke Philips NV Sponsored ADR (PHG)    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PM             | PM       | Philip Morris International Inc Common Stock  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PNDRY          | PNDRY    | Pandora A/S ADR (PNDRY)                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | POOL           | POOL     | Pool Corporation - Common Stock               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PPRUY          | PPRUY    | Kering SA Unsponosred ADR (PPRUY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PRNDY          | PRNDY    | Pernod Ricard SA Sponsored ADR (PRNDY)        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PROSY          | PROSY    | Prosus NV Sponsored ADR (PROSY)               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PRYMY          | PRYMY    | Prysmian SPA ADR (PRYMY)                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PSA            | PSA      | Public Storage Common Stock                   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PSO            | PSO      | Pearson, Plc Common Stock                     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PTC            | PTC      | PTC Inc. - Common Stock                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PUBGY          | PUBGY    | Publicis Groupe S.A. New Sponsored ADR (PUBGY |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PUK            | PUK      | Prudential plc ADR United Kingdom (PUK)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PWR            | PWR      | Quanta Services, Inc. Common Stock            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | PYPL           | PYPL     | PayPal Holdings, Inc. - Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | Q              | Q        | Qnity Electronics, Inc. Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | QABSY          | QABSY    | Qantas Airways Ltd Sponsored ADR (QABSY)      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | QBIEY          | QBIEY    | QBE Insurance Group Ltd Sponsored ADR (QBIEY) |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | QCOM           | QCOM     | QUALCOMM Incorporated - Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RACE           | RACE     | Ferrari N.V. Common Shares                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RBGLY          | RBGLY    | Reckitt Benckiser Group plc Sponsored ADR (RB |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RCL            | RCL      | Royal Caribbean Cruises Ltd. Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RCRUY          | RCRUY    | Recruit Holdings Co Ltd Unsponsored ADR (RCRU |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | REG            | REG      | Regency Centers Corporation - Common Stock    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | REGN           | REGN     | Regeneron Pharmaceuticals, Inc. - Common Stoc |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RELX           | RELX     | RELX plc (RELX)                               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RMD            | RMD      | ResMed Inc. Common Stock                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RNECY          | RNECY    | Renesas Electronic Corp ADR (RNECY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RNLSY          | RNLSY    | Renault SA Unsponsored ADR (RNLSY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RNMBY          | RNMBY    | Rheinmetall AG ADR (RNMBY)                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ROP            | ROP      | Roper Technologies, Inc. - Common Stock (ROP) |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RSG            | RSG      | Republic Services, Inc. Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RSHGY          | RSHGY    | Resona Holdings Inc ADR (RSHGY)               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RTO            | RTO      | Rentokil Initial plc (RTO)                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | RYAAY          | RYAAY    | Ryanair Holdings plc (RYAAY)                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SAABY          | SAABY    | Saab AB ADR (SAABY)                           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SAXPY          | SAXPY    | Sampo OYJ ADR (SAXPY)                         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SBUX           | SBUX     | Starbucks Corporation - Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SCBFY          | SCBFY    | Standard Chartered plc ADR (SCBFY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SCGLY          | SCGLY    | Societe Generale France Sponsored ADR (SCGLY) |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SDVKY          | SDVKY    | Sandvik AB Sponsored ADR (SDVKY)              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SDXAY          | SDXAY    | Sodexo ADR (SDXAY)                            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SDZNY          | SDZNY    | Sandoz Group AG Sponsored ADR (SDZNY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SE             | SE       | Sea Limited (SE)                              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SEOAY          | SEOAY    | Stora Enso Oyj ADR (SEOAY)                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SFGYY          | SFGYY    | Sony Financial Group Inc Sponsored ADR (SFGYY |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SFTBY          | SFTBY    | Softbank Group Corp ADR (SFTBY)               |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SGAPY          | SGAPY    | Singapore Telecom Ltd New Sponsored ADR (SGAP |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SGIOY          | SGIOY    | Shionogi & Co Ltd ADR (SGIOY)                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SGPYY          | SGPYY    | Sage Group plc Unsponsored ADR (SGPYY)        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SGSOY          | SGSOY    | SGS SA ADR Unsponsored (SGSOY)                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SHECY          | SHECY    | Shin Etsu Chemical Co Ltd ADR (SHECY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SINGY          | SINGY    | Singapore Airlines Ltd ADR (SINGY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SJM            | SJM      | The J.M. Smucker Company Common Stock         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SKBSY          | SKBSY    | Skanska AB Sponsored ADR (SKBSY)              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SKHHY          | SKHHY    | Sonic Healthcare Ltd Sponsored ADR (SKHHY)    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SKHSY          | SKHSY    | Sekisui House Ltd Sponsored ADR (SKHSY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SMCAY          | SMCAY    | SMC Corp Sponsored ADR (SMCAY)                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SMGZY          | SMGZY    | Smiths Group plc Sponsored ADR (SMGZY)        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SMMYY          | SMMYY    | Sumitomo Metal Mining Co Ltd Unsponsored ADR  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SMNNY          | SMNNY    | Shimano Inc Unsponsored ADR (SMNNY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SMPNY          | SMPNY    | Sompo Holdings Inc Unsponsored ADR (SMPNY)    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SMTOY          | SMTOY    | Sumitomo Electric Industries Ltd ADR Japan (S |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SNA            | SNA      | Snap-On Incorporated Common Stock             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SNDK           | SNDK     | Sandisk Corporation - Common Stock When-Issue |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SNN            | SNN      | Smith & Nephew SNATS, Inc. Common Stock       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SNPS           | SNPS     | Synopsys, Inc. - Common Stock                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SOBKY          | SOBKY    | Softbank Corp Unsponsored ADR (SOBKY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SOLV           | SOLV     | Solventum Corporation Common Stock            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SOMLY          | SOMLY    | Secom Ltd ADR Japan (SOMLY)                   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SONVY          | SONVY    | Sonova Holding AG ADR (SONVY)                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SOUHY          | SOUHY    | South32 Ltd Sponsored ADR (SOUHY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SPG            | SPG      | Simon Property Group, Inc. Common Stock       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SPGI           | SPGI     | S&P Global Inc. Common Stock                  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SPOT           | SPOT     | Spotify Technology S.A. Ordinary Shares       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SPXCY          | SPXCY    | Singapore Exchange Ltd ADR (SPXCY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SSDOY          | SSDOY    | Shiseido Co Ltd Sponsored ADR Japan (SSDOY)   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SSMXY          | SSMXY    | Sysmex Corporation Unsponsored ADR (SSMXY)    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SSREY          | SSREY    | Swiss Re Ltd Sponsored ADR (SSREY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | STLA           | STLA     | Stellantis N.V. Common Shares                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | STLD           | STLD     | Steel Dynamics, Inc. - Common Stock           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | STM            | STM      | STMicroelectronics N.V. Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | STX            | STX      | Seagate Technology Holdings PLC - Ordinary Sh |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | STZ            | STZ      | Constellation Brands, Inc. Common Stock       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SUHJY          | SUHJY    | Sun Hung Kai Properties Ltd Sponsored ADR (SU |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SUTNY          | SUTNY    | Sumitomo Mitsui Trust Group Inc Sponsored ADR |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SVNDY          | SVNDY    | Seven & I Holdings Co Ltd ADR (SVNDY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SVNLY          | SVNLY    | Svenska Handelbanken AB ADR (SVNLY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SWDBY          | SWDBY    | Swedbank AB ADR (SWDBY)                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SWGAY          | SWGAY    | Swatch Group AG ADR (SWGAY)                   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SWKS           | SWKS     | Skyworks Solutions, Inc. - Common Stock       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SWRAY          | SWRAY    | Swire Pacific Ltd Sponsored ADR (SWRAY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SYF            | SYF      | Synchrony Financial Common Stock              |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SYIEY          | SYIEY    | Symrise AG ADR (SYIEY)                        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | SZKMY          | SZKMY    | Suzuki Motor Corporation Ltd ADR (SZKMY)      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TAK            | TAK      | Takeda Pharmaceutical Company Limited (TAK)   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TAP            | TAP      | Molson Coors Beverage Company Class B Common  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TDG            | TDG      | Transdigm Group Incorporated Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TELFY          | TELFY    | Telefonica SA Sponsored ADR (TELFY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TELNY          | TELNY    | Telenor ASA ADR (TELNY)                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TER            | TER      | Teradyne, Inc. - Common Stock                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TEVA           | TEVA     | Teva Pharmaceutical Industries Limited Americ |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TFC            | TFC      | Truist Financial Corporation Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TGOPY          | TGOPY    | 3I Group PLC (TGOPY)                          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | THLLY          | THLLY    | Thales Unsponsored ADR (THLLY)                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TIIAY          | TIIAY    | Telecom Italia SPA Sponsored (TIIAY)          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TKOMY          | TKOMY    | Tokio Marine Holdings Inc Sponsored (TKOMY)   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TLGPY          | TLGPY    | Telstra Group Ltd Sponsored ADR (TLGPY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TLSNY          | TLSNY    | Telia Co AB ADR (TLSNY)                       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TMO            | TMO      | Thermo Fisher Scientific Inc Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TPR            | TPR      | Tapestry, Inc. Common Stock                   |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TRUMY          | TRUMY    | Terumo Corporation ADR (TRUMY)                |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TRV            | TRV      | The Travelers Companies, Inc. Common Stock    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TRYIY          | TRYIY    | Toray Industries ADR Japan (TRYIY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TSCDY          | TSCDY    | Tesco Stores Holdings (TSCDY)                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TTDKY          | TTDKY    | TDK Corp ADR Japan (TTDKY)                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TTNDY          | TTNDY    | Techtronic Industries Sponsored ADR Hong Kong |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TTWO           | TTWO     | Take-Two Interactive Software, Inc. - Common  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TXN            | TXN      | Texas Instruments Incorporated - Common Stock |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | TXT            | TXT      | Textron Inc. Common Stock                     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UBER           | UBER     | Uber Technologies, Inc. Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UCBJY          | UCBJY    | UCB SA ADR (UCBJY)                            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UDR            | UDR      | UDR, Inc. Common Stock                        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UHS            | UHS      | Universal Health Services, Inc. Common Stock  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UNICY          | UNICY    | Unicharm Corporation Sponsored ADR (UNICY)    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UNVGY          | UNVGY    | Universal Music Group ADR (UNVGY)             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UOVEY          | UOVEY    | United Overseas Bank Ltd Sponsored ADR Singap |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UPMMY          | UPMMY    | UPM Kymmene Corporation ADR (UPMMY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | UPS            | UPS      | United Parcel Service, Inc. Common Stock      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | URI            | URI      | United Rentals, Inc. Common Stock             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VACNY          | VACNY    | VAT Group AG Unsponsored ADR (VACNY)          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VICI           | VICI     | VICI Properties Inc. Common Stock             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VLVLY          | VLVLY    | Volvo AB-A Unsponsored ADR (VLVLY)            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VOD            | VOD      | Vodafone Group Plc (VOD)                      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VONOY          | VONOY    | Vonovia SE ADR (VONOY)                        |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VRSK           | VRSK     | Verisk Analytics, Inc. - Common Stock         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VRSN           | VRSN     | VeriSign, Inc. - Common Stock                 |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VRT            | VRT      | Vertiv Holdings, LLC Class A Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VRTX           | VRTX     | Vertex Pharmaceuticals Incorporated - Common  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VTR            | VTR      | Ventas, Inc. Common Stock                     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VWAPY          | VWAPY    | Volkswagen AG Unsponsored ADR (VWAPY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VWDRY          | VWDRY    | Vestas Wind Systems A/S ADR (VWDRY)           |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | VZ             | VZ       | Verizon Communications Inc. Common Stock      |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | WAB            | WAB      | Westinghouse Air Brake Technologies Corporati |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | WBD            | WBD      | Warner Bros. Discovery, Inc. - Series A Commo |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | WDAY           | WDAY     | Workday, Inc. - Class A Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | WDC            | WDC      | Western Digital Corporation - Common Stock    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | WFC            | WFC      | Wells Fargo & Company Common Stock            |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | WLMIY          | WLMIY    | Wilmar International Ltd AADR (WLMIY)         |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | WTKWY          | WTKWY    | Wolters Kluwer NV Sponsored ADR (WTKWY)       |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | WYNN           | WYNN     | Wynn Resorts, Limited - Common Stock          |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | YAHOY          | YAHOY    | LY Corporation ADR (YAHOY)                    |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | YARIY          | YARIY    | Yara International ASA Sponsored ADR (YARIY)  |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | YUM            | YUM      | Yum! Brands, Inc.                             |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Alan Armstrong       | ZBH            | ZBH      | Zimmer Biomet Holdings, Inc. Common Stock     |           1 |        8,000 | 2026-07-21                 | (no data)         | False                                   |
| Ashley Moody         | GENI           | GENI     | GENI                                          |           1 |        8,000 | 2025-03-22                 | (no data)         | False                                   |
| Cynthia M. Lummis    | J              | J        | Jacobs Engineering Group Inc. Common Stock    |           1 |        8,000 | 2021-10-07                 | (no data)         | False                                   |
| Dan Sullivan         | GOOG           | GOOG     | Alphabet Inc. - Class C Capital Stock         |           1 |        8,000 | 2023-03-16                 | (no data)         | False                                   |
| Dan Sullivan         | LRCX           | LRCX     | Lam Research Corporation - Common Stock       |           1 |        8,000 | 2022-12-21                 | (no data)         | False                                   |
| Dan Sullivan         | TJX            | TJX      | TJX Companies, Inc. (The) Common Stock        |           1 |        8,000 | 2022-12-21                 | (no data)         | False                                   |
| Dan Sullivan         | TMO            | TMO      | Thermo Fisher Scientific Inc Common Stock     |           1 |        8,000 | 2022-12-21                 | (no data)         | False                                   |
| Gary C. Peters       | CDP            | OFC      | Corporate Office Properties Trust Common Stoc |           1 |        8,000 | 2021-12-07                 | (no data)         | False                                   |
| Gary C. Peters       | FSK            | FSK      | FS KKR Capital Corp. Common Stock             |           1 |        8,000 | 2022-05-16                 | (no data)         | False                                   |
| Gary C. Peters       | HBAN           | HBAN     | Huntington Bancshares Incorporated - Common S |           1 |        8,000 | 2022-01-08                 | (no data)         | False                                   |
| Gary C. Peters       | IBM            | IBM      | International Business Machines Corporation C |           1 |        8,000 | 2022-01-08                 | (no data)         | False                                   |
| Gary C. Peters       | IFF            | IFF      | Internationa Flavors & Fragrances, Inc. Commo |           1 |        8,000 | 2023-06-30                 | (no data)         | False                                   |
| Gary C. Peters       | KHC            | KHC      | The Kraft Heinz Company - Common Stock        |           1 |        8,000 | 2026-06-11                 | (no data)         | False                                   |
| Gary C. Peters       | SJM            | SJM      | SJM - The J.M. Smucker Company Common Stock   |           1 |        8,000 | 2026-05-11                 | (no data)         | False                                   |
| Gary C. Peters       | T              | T        | AT&T Inc.                                     |           1 |        8,000 | 2026-07-02                 | (no data)         | False                                   |
| Gary C. Peters       | TFC            | TFC      | Truist Financial Corporation Common Stock     |           1 |        8,000 | 2023-04-12                 | (no data)         | False                                   |
| Jerry Moran          | BNY            | BK       | The Bank of New York Mellon Corporation Commo |           1 |        8,000 | 2022-01-21                 | (no data)         | False                                   |
| Jerry Moran          | CI             | CI       | Cigna Corporation Common Stock                |           1 |        8,000 | 2022-01-21                 | (no data)         | False                                   |
| Jerry Moran          | CMCSA          | CMCSA    | Comcast Corporation - Class A Common Stock    |           1 |        8,000 | 2022-01-21                 | (no data)         | False                                   |
| Jerry Moran          | CSCO           | CSCO     | Cisco Systems, Inc. - Common Stock            |           1 |        8,000 | 2022-01-21                 | (no data)         | False                                   |
| Jerry Moran          | KMB            | KMB      | Kimberly-Clark Corporation Common Stock       |           1 |        8,000 | 2022-01-21                 | (no data)         | False                                   |
| Jerry Moran          | PFE            | PFE      | Pfizer, Inc. Common Stock                     |           1 |        8,000 | 2022-01-21                 | (no data)         | False                                   |
| Jerry Moran          | PII            | PII      | Polaris Inc. Common Stock                     |           1 |        8,000 | 2022-01-21                 | (no data)         | False                                   |
| Jerry Moran          | VZ             | VZ       | Verizon Communications Inc. Common Stock      |           1 |        8,000 | 2022-01-21                 | (no data)         | False                                   |
| Jim Banks            | SBUX           | SBUX     | starbuck                                      |           1 |        8,000 | 2025-08-10                 | (no data)         | False                                   |
| John Boozman         | BRK-B          | BRK-B    | BRK-B - Berkshire Hathaway Inc Class B        |           1 |        8,000 | 2025-08-06                 | (no data)         | False                                   |
| John Boozman         | BSX            | BSX      | Boston Scientific Corp                        |           1 |        8,000 | 2025-03-06                 | (no data)         | False                                   |
| John Boozman         | CAT            | CAT      | Caterpillar Inc                               |           1 |        8,000 | 2026-02-15                 | (no data)         | False                                   |
| John Boozman         | CBOE           | CBOE     | Cboe Global Markets, Inc. Common Stock        |           1 |        8,000 | 2026-08-20                 | (no data)         | False                                   |
| John Boozman         | COLPAL         | COLPAL   | COLGATE PALMOLIVE LTD.                        |           1 |        8,000 | 2025-05-14                 | (no data)         | False                                   |
| John Boozman         | COST           | COST     | Costco Wholesale                              |           1 |        8,000 | 2025-11-15                 | (no data)         | False                                   |
| John Boozman         | CRM            | CRM      | Salesforce Inc                                |           1 |        8,000 | 2025-02-08                 | (no data)         | False                                   |
| John Boozman         | CVS            | CVS      | CVS Corp                                      |           1 |        8,000 | 2026-02-15                 | (no data)         | False                                   |
| John Boozman         | CVX            | CVX      | Chevron Corporation Common Stock              |           1 |        8,000 | 2026-08-17                 | (no data)         | False                                   |
| John Boozman         | DIS            | DIS      | Walt Disney Company                           |           1 |        8,000 | 2026-02-15                 | (no data)         | False                                   |
| John Boozman         | DVN            | DVN      | Devon Energy Corporation Common Stock         |           1 |        8,000 | 2026-05-08                 | (no data)         | False                                   |
| John Boozman         | DXCM           | DXCM     | Dexcom Inc                                    |           1 |        8,000 | 2026-02-15                 | (no data)         | False                                   |
| John Boozman         | ECL            | ECL      | Ecolab Inc                                    |           1 |        8,000 | 2025-03-06                 | (no data)         | False                                   |
| John Boozman         | EL             | EL       | Estee Lauder Companies, Inc. (The) Common Sto |           1 |        8,000 | 2026-08-17                 | (no data)         | False                                   |
| John Boozman         | EMB            | EMB      | iShares J.P. Morgan USD Emerging Markets Bond |           1 |        8,000 | 2026-03-06                 | (no data)         | False                                   |
| John Boozman         | GBIL           | GBIL     | Goldman Sachs Access Treasury 0-1 Year ETF    |           1 |        8,000 | 2026-06-16                 | (no data)         | False                                   |
| John Boozman         | GE             | GE       | General Electric Company                      |           1 |        8,000 | 2025-08-06                 | (no data)         | False                                   |
| John Boozman         | HYG            | HYG      | iShares iBoxx $ High Yield Corporate Bond ETF |           1 |        8,000 | 2025-05-14                 | (no data)         | False                                   |
| John Boozman         | IGV            | IGV      | iShares Expanded Tech-Software Sector ETF     |           1 |        8,000 | 2026-07-13                 | (no data)         | False                                   |
| John Boozman         | IJR            | IJR      | iShares Core S&P Small-Cap ETF                |           1 |        8,000 | 2026-01-13                 | (no data)         | False                                   |
| John Boozman         | IVW            | IVW      | iShares S&P 500 Growth ETF                    |           1 |        8,000 | 2026-01-13                 | (no data)         | False                                   |
| John Boozman         | IWM            | IWM      | iShares Russell 2000 ETF                      |           1 |        8,000 | 2025-09-12                 | (no data)         | False                                   |
| John Boozman         | KR             | KR       | Kroger Company (The) Common Stock             |           1 |        8,000 | 2026-03-06                 | (no data)         | False                                   |
| John Boozman         | MDY            | MDY      | S&P Midcap 400 SPDR                           |           1 |        8,000 | 2025-12-08                 | (no data)         | False                                   |
| John Boozman         | NFLX           | NFLX     | Netflix Inc                                   |           1 |        8,000 | 2026-02-15                 | (no data)         | False                                   |
| John Boozman         | NRG            | NRG      | NRG Energy, Inc. Common Stock                 |           1 |        8,000 | 2025-02-08                 | (no data)         | False                                   |
| John Boozman         | NTAP           | NTAP     | NetApp, Inc. - Common Stock                   |           1 |        8,000 | 2026-03-06                 | (no data)         | False                                   |
| John Boozman         | ORCL           | ORCL     | Oracle Corp                                   |           1 |        8,000 | 2025-05-14                 | (no data)         | False                                   |
| John Boozman         | PFE            | PFE      | Pfizer Inc                                    |           1 |        8,000 | 2024-01-08                 | (no data)         | False                                   |
| John Boozman         | PLTR           | PLTR     | Palantir Technologies Inc. - Class A Common S |           1 |        8,000 | 2026-06-16                 | (no data)         | False                                   |
| John Boozman         | RTX            | RTX      | Raytheon Technologies Corp                    |           1 |        8,000 | 2025-06-14                 | (no data)         | False                                   |
| John Boozman         | SMCI           | SMCI     | Super Micro Computer                          |           1 |        8,000 | 2026-01-13                 | (no data)         | False                                   |
| John Boozman         | TPYP           | TPYP     | Tortoise Capital Series Trust Tortoise North  |           1 |        8,000 | 2026-02-15                 | (no data)         | False                                   |
| John Boozman         | UBER           | UBER     | Uber Technologies, Inc. Common Stock          |           1 |        8,000 | 2026-03-06                 | (no data)         | False                                   |
| John Boozman         | URNM           | URNM     | Sprott Uranium Miners ETF                     |           1 |        8,000 | 2025-03-06                 | (no data)         | False                                   |
| John Boozman         | V              | V        | Visa Inc                                      |           1 |        8,000 | 2026-02-15                 | (no data)         | False                                   |
| John Boozman         | VWO            | VWO      | Vanguard FTSE Emerging Markets ETF            |           1 |        8,000 | 2025-12-08                 | (no data)         | False                                   |
| John Boozman         | WFC            | WFC      | Wells Fargo & Company                         |           1 |        8,000 | 2026-01-13                 | (no data)         | False                                   |
| John Boozman         | WMT            | WMT      | Walmart Inc                                   |           1 |        8,000 | 2025-08-06                 | (no data)         | False                                   |
| John Boozman         | XOM            | XOM      | Exxon Mobil Corp                              |           1 |        8,000 | 2026-02-15                 | (no data)         | False                                   |
| John Kennedy         | NLY            | NLY      | Annaly Capital Management Inc Company: Annaly |           1 |        8,000 | 2025-05-08                 | (no data)         | False                                   |
| Lindsey Graham       | IBDO           | IBDO     | iShares iBonds Dec 2023 Term Corporate ETF    |           1 |        8,000 | 2022-07-13                 | (no data)         | False                                   |
| Markwayne Mullin     | BMI            | BMI      | Badger Meter, Inc. Common Stock               |           1 |        8,000 | 2024-01-26                 | (no data)         | False                                   |
| Markwayne Mullin     | CYBR           | CYBR     | CyberArk Software Ltd. - Ordinary Shares      |           1 |        8,000 | 2024-01-26                 | (no data)         | False                                   |
| Markwayne Mullin     | ELF            | ELF      | E.L.F. Beauty Inc                             |           1 |        8,000 | 2024-01-26                 | (no data)         | False                                   |
| Markwayne Mullin     | ETN            | ETN      | Eaton Corp                                    |           1 |        8,000 | 2024-01-26                 | (no data)         | False                                   |
| Markwayne Mullin     | FRPT           | FRPT     | Freshpet, Inc. - Common Stock                 |           1 |        8,000 | 2024-01-26                 | (no data)         | False                                   |
| Markwayne Mullin     | OLLI           | OLLI     | Ollie's Bargain Outlet Holdings, Inc. - Commo |           1 |        8,000 | 2024-01-26                 | (no data)         | False                                   |
| Markwayne Mullin     | SFM            | SFM      | Sprouts Farmers Market                        |           1 |        8,000 | 2024-01-26                 | (no data)         | False                                   |
| Markwayne Mullin     | VNQ            | VNQ      | Vanguard Real Estate ETF                      |           1 |        8,000 | 2025-01-03                 | (no data)         | False                                   |
| Patrick J. Toomey    | SPG            | SPG      | Simon Property Group, Inc. Common Stock       |           1 |        8,000 | 2021-11-15                 | (no data)         | False                                   |
| Sheldon Whitehouse   | CCI            | CCI      | Crown Castle Inc                              |           1 |        8,000 | 2024-06-06                 | (no data)         | False                                   |
| Sheldon Whitehouse   | CELH           | CELH     | Celsius Holdings Inc                          |           1 |        8,000 | 2023-12-07                 | (no data)         | False                                   |
| Sheldon Whitehouse   | GH             | GH       | Guardant Health Inc                           |           1 |        8,000 | 2025-12-01                 | (no data)         | False                                   |
| Sheldon Whitehouse   | GS             | GS       | Goldman Sachs Group, Inc. (The) Common Stock  |           1 |        8,000 | 2024-07-16                 | (no data)         | False                                   |
| Sheldon Whitehouse   | HD             | HD       | Home Depot                                    |           1 |        8,000 | 2024-07-16                 | (no data)         | False                                   |
| Sheldon Whitehouse   | HSY            | HSY      | Hershey Foods Corp                            |           1 |        8,000 | 2025-12-01                 | (no data)         | False                                   |
| Sheldon Whitehouse   | KVUE           | KVUE     | Kenvue Inc                                    |           1 |        8,000 | 2023-10-17                 | (no data)         | False                                   |
| Sheldon Whitehouse   | MSFT           | MSFT     | Microsoft Corp                                |           1 |        8,000 | 2024-07-16                 | (no data)         | False                                   |
| Sheldon Whitehouse   | MU             | MU       | Micron Technology, Inc. - Common Stock        |           1 |        8,000 | 2026-07-08                 | (no data)         | False                                   |
| Sheldon Whitehouse   | VZ             | VZ       | Verizon Communications Inc                    |           1 |        8,000 | 2023-10-17                 | (no data)         | False                                   |
| Tommy Tuberville     | BKE            | BKE      | Buckle, Inc. (The) Common Stock               |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | BMO            | BMO      | Bank of Montreal                              |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | BMY            | BMY      | Bristol-Myers Squibb Company Common Stock     |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | BRO            | BRO      | Brown & Brown, Inc. Common Stock              |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | CABO           | CABO     | Cable One, Inc. Common Stock                  |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | CDNS           | CDNS     | Cadence Design Systems, Inc. - Common Stock   |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | CROX           | CROX     | Crocs, Inc. - Common Stock                    |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | CRUS           | CRUS     | Cirrus Logic, Inc. - Common Stock             |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | CTAS           | CTAS     | Cintas Corporation - Common Stock             |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | DECK           | DECK     | Deckers Outdoor Corporation Common Stock      |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | DEO            | DEO      | Diageo plc Common Stock                       |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | DHI            | DHI      | D.R. Horton, Inc. Common Stock                |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | DIOD           | DIOD     | Diodes Incorporated - Common Stock            |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | DOW            | DOW      | Dow Inc. Common Stock                         |           1 |        8,000 | 2022-02-14                 | (no data)         | False                                   |
| Tommy Tuberville     | DQ             | DQ       | DAQO New Energy Corp. American Depositary Sha |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | EL             | EL       | Estee Lauder Companies, Inc. (The) Common Sto |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | ELS            | ELS      | Equity Lifestyle Properties, Inc. Common Stoc |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | ETSY           | ETSY     | Etsy, Inc. - Common Stock                     |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | EXP            | EXP      | Eagle Materials Inc Common Stock              |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | EXR            | EXR      | Extra Space Storage Inc Common Stock          |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | FTNT           | FTNT     | Fortinet, Inc. - Common Stock                 |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | GFI            | GFI      | Gold Fields Limited American Depositary Share |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | GGG            | GGG      | Graco Inc. Common Stock                       |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | GILD           | GILD     | Gilead Sciences, Inc. - Common Stock          |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | GIS            | GIS      | General Mills, Inc. Common Stock              |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | GLPI           | GLPI     | Gaming and Leisure Properties, Inc. - Common  |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | GNRC           | GNRC     | Generac Holdlings Inc. Common Stock           |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | GNTX           | GNTX     | Gentex Corporation - Common Stock             |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | GOOG           | GOOG     | Alphabet Inc. - Class C Capital Stock         |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | GRMN           | GRMN     | Garmin Ltd. - Common Stock                    |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | GSK            | GSK      | GSK plc American Depositary Shares (Each repr |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | HON            | HON      | Honeywell International Inc. - Common Stock   |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | IBM            | IBM      | International Business Machines Corporat      |           1 |        8,000 | 2022-02-14                 | (no data)         | False                                   |
| Tommy Tuberville     | IDXX           | IDXX     | IDEXX Laboratories, Inc. - Common Stock       |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | INTU           | INTU     | Intuit Inc. - Common Stock                    |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | IT             | IT       | Gartner, Inc. Common Stock                    |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | ITW            | ITW      | Illinois Tool Works Inc. Common Stock         |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | JKHY           | JKHY     | Jack Henry & Associates, Inc. - Common Stock  |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | JNJ            | JNJ      | Johnson & Johnson Common Stock                |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | KEYS           | KEYS     | Keysight Technologies Inc. Common Stock       |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | KLAC           | KLAC     | KLA Corporation - Common Stock                |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | KO             | KO       | Coca-Cola Company (The) Common Stock          |           1 |        8,000 | 2022-02-14                 | (no data)         | False                                   |
| Tommy Tuberville     | LMST           | LMST     | Limestone Bancorp, Inc. - Common Stock        |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | LSCC           | LSCC     | Lattice Semiconductor Corporation - Common St |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | LULU           | LULU     | lululemon athletica inc. - Common Stock       |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | MASI           | MASI     | Masimo Corporation - Common Stock             |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | MCHP           | MCHP     | Microchip Technology Incorporated - Common St |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | MCO            | MCO      | Moody's Corporation Common Stock              |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | META           | META     | Meta Platforms, Inc. - Class A Common Stock   |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | MKSI           | MKSI     | MKS Instruments, Inc. - Common Stock          |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | MNST           | MNST     | Monster Beverage Corporation - Common Stock   |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | MRK            | MRK      | Merck & Company, Inc. Common Stock (new)      |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | MSI            | MSI      | Motorola Solutions, Inc. Common Stock         |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | NDAQ           | NDAQ     | Nasdaq, Inc. - Common Stock                   |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | NDSN           | NDSN     | Nordson Corporation - Common Stock            |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | NOC            | NOC      | Northrop Grumman Corporation Common Stock     |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | NSC            | NSC      | Norfolk Southern Corporation Common Stock     |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | NTES           | NTES     | Netease Inc ADR                               |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | NVDA           | NVDA     | NVIDIA Corporation - Common Stock             |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | NXPI           | NXPI     | NXP Semiconductors N.V. - Common Stock        |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | PAC            | PAC      | Grupo Aeroportuario Del Pacifico, S.A. B. de  |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | PAM            | PAM      | Pampa Energia S.A. Pampa Energia S.A.         |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | PAYC           | PAYC     | Paycom Software, Inc. Common Stock            |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | PG             | PG       | Procter & Gamble Company (The) Common Stock   |           1 |        8,000 | 2021-10-15                 | (no data)         | False                                   |
| Tommy Tuberville     | QLYS           | QLYS     | Qualys, Inc. - Common Stock                   |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | QSR            | QSR      | Restaurant Brands International Inc           |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | RACE           | RACE     | Ferrari N.V. Common Shares                    |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | REGN           | REGN     | Regeneron Pharmaceuticals, Inc. - Common Stoc |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | RELX           | RELX     | RELX PLC PLC American Depositary Shares (Each |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | RH             | RH       | RH Common Stock                               |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | ROK            | ROK      | Rockwell Automation, Inc. Common Stock        |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | RRC            | RRC      | Range Resources Corporation Common Stock      |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | SCI            | SCI      | Service Corporation International Common Stoc |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | SKY            | SKY      | Skyline Champion Corporation Common Stock     |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | SNPS           | SNPS     | Synopsys, Inc. - Common Stock                 |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | SOLV           | SOLV     | Solventum Corporation Common Stock            |           1 |        8,000 | 2024-06-14                 | (no data)         | False                                   |
| Tommy Tuberville     | SSD            | SSD      | Simpson Manufacturing Company, Inc. Common St |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | SWKS           | SWKS     | Skyworks Solutions, Inc. - Common Stock       |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | TEL            | TEL      | Te Connectivity Ltd                           |           1 |        8,000 | 2024-05-15                 | (no data)         | False                                   |
| Tommy Tuberville     | TMO            | TMO      | Thermo Fisher Scientific Inc Common Stock     |           1 |        8,000 | 2022-04-08                 | (no data)         | False                                   |
| Tommy Tuberville     | TREX           | TREX     | Trex Company, Inc. Common Stock               |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | TSLA           | TSLA     | Tesla, Inc. - Common Stock                    |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |
| Tommy Tuberville     | VRTX           | VRTX     | Vertex Pharmaceuticals Incorporated - Common  |           1 |        8,000 | 2022-11-10                 | (no data)         | False                                   |
| Tommy Tuberville     | WMS            | WMS      | Advanced Drainage Systems, Inc. Common Stock  |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | WU             | WU       | Western Union Company (The) Common Stock      |           1 |        8,000 | 2023-11-16                 | (no data)         | False                                   |
| Tommy Tuberville     | XP             | XP       | XP Inc. - Class A Common Stock                |           1 |        8,000 | 2023-05-11                 | (no data)         | False                                   |

### 5. Daily moves beyond +/-50% (split-adjusted close)

6 moves in 4 symbols; 6 unexplained; 5 in symbols with in-scope trades (`data/interim/price_large_moves.csv`).

| ticker   | prev_date   | date       |   close | ret_close   | ret_adj   | next_ret_close   | in_scope_symbol   | explanation                      |
|:---------|:------------|:-----------|--------:|:------------|:----------|:-----------------|:------------------|:---------------------------------|
| ADCT     | 2023-12-12  | 2023-12-13 |       2 | 63.1%       | 63.1%     | 6.5%             | True              | unexplained (no split on record) |
| ADCT     | 2024-12-05  | 2024-12-06 |       3 | 63.0%       | 63.0%     | 2.6%             | True              | unexplained (no split on record) |
| ADCT     | 2026-06-03  | 2026-06-04 |       1 | -57.1%      | -57.1%    | -22.0%           | True              | unexplained (no split on record) |
| AMD      | 2016-04-21  | 2016-04-22 |       4 | 52.3%       | 52.3%     | -13.5%           | True              | unexplained (no split on record) |
| APA      | 2020-03-06  | 2020-03-09 |      10 | -53.9%      | -53.9%    | 13.0%            | False             | unexplained (no split on record) |
| ARGX     | 2017-12-08  | 2017-12-11 |      54 | 78.9%       | 78.9%     | 1.0%             | True              | unexplained (no split on record) |

### 6. Staleness: share of days with an unchanged close (tickers above 20%)

| ticker   | is_otc   | in_scope_symbol   |   days |   zero_return_days | zero_share   | first_date   | last_date   |
|:---------|:---------|:------------------|-------:|-------------------:|:-------------|:-------------|:------------|
| BDNNY    | True     | True              |   2680 |               1166 | 43.5%        | 2016-01-04   | 2026-08-31  |
| AIBGY    | True     | True              |   1951 |               1069 | 54.8%        | 2018-11-23   | 2026-08-31  |
| ASXFY    | True     | True              |   2680 |                998 | 37.3%        | 2016-01-04   | 2026-08-31  |
| AONNY    | True     | True              |   2680 |                830 | 31.0%        | 2016-01-04   | 2026-08-31  |
| AMCR     | False    | True              |   2680 |                787 | 29.4%        | 2016-01-04   | 2026-08-31  |
| ASCCY    | True     | True              |   2680 |                787 | 29.4%        | 2016-01-04   | 2026-08-31  |
| ARZGY    | True     | True              |   2680 |                743 | 27.7%        | 2016-01-04   | 2026-08-31  |

### 7. Zero or negative prices, and gaps longer than 5 trading days

- Rows with a zero, negative or missing adjusted close: **0**.
- Gaps of more than 5 NYSE trading days inside a symbol's series: **0** in 0 symbols (`data/interim/price_gaps.csv`).

_None._

### 8. Factors (Ken French, US)

- Daily: 2015-01-02 to 2026-08-31 (2,932 days), `data/processed/factors_daily.csv`.
- Monthly: 2015-01 to 2026-08 (140 months), `data/processed/factors_monthly.csv`.
- Columns mkt_rf_pct, smb_pct, hml_pct, rf_pct, mom_pct. **Units: percent** (1.00 = 1%), also stated in each file's `units` column; divide by 100 before use. Raw zips and download dates: `data/raw/french/`.
- NYSE calendar days without a daily factor row: 0; factor days not in the calendar (from 2016-01-04): 0.
