# Data quality log

Every exclusion and every data problem, counted and explained. Phase 1 sections below; later phases add theirs.

## Phase 1: scrape

- Filings in the eFD listing (received 2016-01-01 to 2026-09-30, all filer types): **379**; electronic **323**, paper **56**, other **0**.
- Electronic PTRs downloaded: **291**; failed: **0**; pending: **32**.
- Listing fetched on or before the scrape end date is refreshed automatically on the next run (the 2026 listing is incomplete until after 2026-09-30).

### Download failures

None.

### Paper filings (excluded, D05)

**56** paper filings are scanned images and cannot be parsed; they are excluded. The full list (senator, date, link) is in `data/interim/paper_filings.csv`. By filer:

| filer_name         |   Paper filings |
|:-------------------|----------------:|
| JOHN BOOZMAN       |              27 |
| RICHARD BLUMENTHAL |              26 |
| DIANNE FEINSTEIN   |               2 |
| RICHARD M BURR     |               1 |

### Parse validation

Each of the 291 downloaded PTRs was checked three ways: rows parsed, `<tbody>` rows counted by a separate parser, and the page's own "(N transactions total)" line.

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

46 distinct filer names: override 0, exact 45, fuzzy 1, ambiguous 0, unmatched 0. Unmatched or low-confidence: **0** (listed in outputs/phase1_summary.md section 8; their transactions are left out of the key number).

- Matched filers none of whose transactions fall inside that senator's service (would suggest the wrong person): **0**
- Transactions by high-confidence matched filers dated OUTSIDE Senate service (excluded by A05 in Phase 2): **1** of 2,793.

| matched_name   |   Rows outside service |
|:---------------|-----------------------:|
| Pete Ricketts  |                      1 |

