# Where each manual price file came from (M2)

One line per CSV in this folder. The prices stage warns about any file this table does not name.
See docs/PRICE_REQUEST.md for what to pull and how.

| file | pulled by | terminal (Bloomberg / FactSet) | date pulled | security identifier used | notes |
|---|---|---|---|---|---|
| (example) ECOM.csv | Harry | Bloomberg | 2026-10-01 | ECOM US Equity (delisted) | history ends 2022-11-15 |
| X.csv | (name TBC) | Bloomberg | 2026-10-07 | X US Equity | Excel BDH, PX_LAST and TOT_RETURN_INDEX_GROSS_DVDS, Days=T; 984 rows, 2021-07-19 to 2025-06-17; converted from docs/bloomberg_price_pull.xlsx by Claude |
| ECOM.csv | (name TBC) | Bloomberg | 2026-10-07 | ECOM US Equity | Excel BDH, PX_LAST and TOT_RETURN_INDEX_GROSS_DVDS, Days=T; 336 rows, 2021-07-19 to 2022-11-14; converted from docs/bloomberg_price_pull.xlsx by Claude |
| ATVI.csv | (name TBC) | Bloomberg | 2026-10-07 | ATVI US Equity | Excel BDH, PX_LAST and TOT_RETURN_INDEX_GROSS_DVDS, Days=T; 1135 rows, 2019-04-11 to 2023-10-12; converted from docs/bloomberg_price_pull.xlsx by Claude |
| SSBK.csv | (name TBC) | Bloomberg | 2026-10-07 | SSBK US Equity | Excel BDH, PX_LAST and TOT_RETURN_INDEX_GROSS_DVDS, Days=T; 952 rows, 2021-09-01 to 2025-06-30; converted from docs/bloomberg_price_pull.xlsx by Claude |
| WBA.csv | (name TBC) | Bloomberg | 2026-10-07 | WBA US Equity | Excel BDH, PX_LAST and TOT_RETURN_INDEX_GROSS_DVDS, Days=T; 2334 rows, 2016-05-17 to 2025-08-27; converted from docs/bloomberg_price_pull.xlsx by Claude |
| GOGL.csv | (name TBC) | Bloomberg | 2026-10-07 | 2663476D US Equity (delisted; Golden Ocean Group Ltd, US line, USD) | Excel BDH, PX_LAST and TOT_RETURN_INDEX_GROSS_DVDS, Days=T; 362 rows, 2024-03-11 to 2025-08-19; converted from docs/bloomberg_price_pull.xlsx by Claude |
| TOELY.csv | (name TBC) | Bloomberg | 2026-10-07 | TOELY US Equity | Excel BDH, PX_LAST and TOT_RETURN_INDEX_GROSS_DVDS, Days=T; 34 rows, 2026-07-15 to 2026-08-31; converted from docs/bloomberg_price_pull.xlsx by Claude |
| PARA.csv | (name TBC) | Bloomberg | 2026-10-07 | 2677689D US Equity (delisted; Paramount Global Class B, acquired 2025-08-08) | Excel BDH, PX_LAST and TOT_RETURN_INDEX_GROSS_DVDS, Days=T; 458 rows, 2023-10-09 to 2025-08-06; first pull with PARA US Equity was a different security and was discarded |
