# Phase 4 worked examples (in-sample, real data)

Three copied lots traced step by step from `data/processed/lots.csv` and `engine_events.csv`, so one can be checked by hand on Yahoo Finance. Prices are Yahoo's adjusted close (splits and dividends) as downloaded on 2026-09-28.

### A Tuberville purchase later sold in full: Tommy Tuberville, Johnson & Johnson Common Stock (JNJ)

1. **Senator's trade**: Purchase dated 2021-09-30, owner Joint, disclosed range $1,001 - $15,000 (record T07112.1, trade T07112).
2. **Disclosure**: PTR received 2021-10-15 13:32:00 (US Eastern).
3. **Entry date** = first NYSE trading day after the disclosure date = **2021-10-18**.
4. **Entry price**: adjusted close 139.2527 (Yahoo 'Close' that day: 160.12). Size = midpoint $8,000.50; units = 8,000.50 / 139.2527 = 57.4531.
5. **Exit (senator sale)**: Sale (Full) dated 2023-10-16, disclosed 2023-11-16 15:10:00 ($1,001 - $15,000); executed at the close of **2023-11-17**, adjusted close 137.5493 (Yahoo 'Close' 149.79). Sells all 57.4531 units. Return 137.5493 / 139.2527 - 1 = **-1.22%**; P&L $-97.87 over 525 trading days (760 calendar days).

_To check on Yahoo Finance: open finance.yahoo.com/quote/JNJ/history, set the dates, and compare the 'Close' column (adjusted for splits only) with the Close shown here; the return uses 'Adj Close', which also reinvests dividends. Yahoo re-adjusts 'Adj Close' after every new dividend, so its level today can differ slightly from ours; the ratio between two dates should match._

### A partial sale: Tommy Tuberville, Intel Corporation - Common Stock (INTC)

1. **Senator's trade**: Purchase dated 2022-08-05, owner Joint, disclosed range $1,001 - $15,000 (record T07860.1, trade T07860).
2. **Disclosure**: PTR received 2022-09-15 12:53:00 (US Eastern).
3. **Entry date** = first NYSE trading day after the disclosure date = **2022-09-16**.
4. **Entry price**: adjusted close 27.8197 (Yahoo 'Close' that day: 29.24). Size = midpoint $8,000.50; units = 8,000.50 / 27.8197 = 287.5835.
5. **Exit (senator sale)**: Sale (Partial) dated 2024-05-10, disclosed 2024-06-14 14:39:00 ($100,001 - $250,000); executed at the close of **2024-06-17**, adjusted close 30.7847 (Yahoo 'Close' 30.98). The partial sale sells $175,000.50 / 30.7847 = 187.5587 units of this lot (entry cost 5,217.84). Return 30.7847 / 27.8197 - 1 = **10.66%**; P&L $556.11 over 439 trading days (640 calendar days).
6. **Exit (senator sale)**: Sale (Full) dated 2024-05-13, disclosed 2024-06-14 14:39:00 ($100,001 - $250,000); executed at the close of **2024-06-17**, adjusted close 30.7847 (Yahoo 'Close' 30.98). Sells all 100.0248 units. Return 30.7847 / 27.8197 - 1 = **10.66%**; P&L $296.57 over 439 trading days (640 calendar days).

_To check on Yahoo Finance: open finance.yahoo.com/quote/INTC/history, set the dates, and compare the 'Close' column (adjusted for splits only) with the Close shown here; the return uses 'Adj Close', which also reinvests dividends. Yahoo re-adjusts 'Adj Close' after every new dividend, so its level today can differ slightly from ours; the ratio between two dates should match._

### A lot held to the end of the in-sample window: Gary C. Peters, VZ (VZ)

1. **Senator's trade**: Purchase dated 2021-11-09, owner Self, disclosed range $1,001 - $15,000 (record T07204.1, trade T07204).
2. **Disclosure**: PTR received 2021-12-07 10:59:00 (US Eastern).
3. **Entry date** = first NYSE trading day after the disclosure date = **2021-12-08**.
4. **Entry price**: adjusted close 37.2436 (Yahoo 'Close' that day: 50.49). Size = midpoint $8,000.50; units = 8,000.50 / 37.2436 = 214.8155.
5. **End of window**: 214.8155 units marked at the adjusted close of **2026-08-31**, 50.0200 (Yahoo 'Close' 50.02). Return 50.0200 / 37.2436 - 1 = **34.31%**; P&L $2,744.57 over 1185 trading days (1727 calendar days).

_To check on Yahoo Finance: open finance.yahoo.com/quote/VZ/history, set the dates, and compare the 'Close' column (adjusted for splits only) with the Close shown here; the return uses 'Adj Close', which also reinvests dividends. Yahoo re-adjusts 'Adj Close' after every new dividend, so its level today can differ slightly from ours; the ratio between two dates should match._
