# Phase 4 worked examples (in-sample, real data)

Three copied lots traced step by step from `data/processed/lots.csv` and `engine_events.csv`, so one can be checked by hand on Yahoo Finance. Prices are Yahoo's adjusted close (splits and dividends) as downloaded on 2026-09-28.

### A Tuberville purchase later sold in full: Tommy Tuberville, Johnson & Johnson Common Stock (JNJ)

1. **Senator's trade**: Purchase dated 2021-09-30, owner Joint, disclosed range $1,001 - $15,000 (record T07112.1, trade T07112).
2. **Disclosure**: PTR received 2021-10-15 13:32:00 (US Eastern).
3. **Entry date** = first NYSE trading day after the disclosure date = **2021-10-18**.
4. **Entry price**: adjusted close 139.2527 (Yahoo 'Close' that day: 160.12). Size = midpoint $8,000.50; units = 8,000.50 / 139.2527 = 57.4531.
5. **Exit (senator sale)**: Sale (Full) dated 2023-10-16, disclosed 2023-11-16 15:10:00 ($1,001 - $15,000); executed at the close of **2023-11-17**, adjusted close 137.5493 (Yahoo 'Close' 149.79). Sells all 57.4531 units. Return 137.5493 / 139.2527 - 1 = **-1.22%**; P&L $-97.87 over 525 trading days (760 calendar days).

_To check on Yahoo Finance: open finance.yahoo.com/quote/JNJ/history, set the dates, and compare the 'Close' column (adjusted for splits only) with the Close shown here; the return uses 'Adj Close', which also reinvests dividends. Yahoo re-adjusts 'Adj Close' after every new dividend, so its level today can differ slightly from ours; the ratio between two dates should match._

### A partial sale: Tommy Tuberville, Microsoft Corporation - Common Stock (MSFT)

1. **Senator's trade**: Purchase dated 2022-09-19, owner Joint, disclosed range $250,001 - $500,000 (record T07887.1, trade T07887).
2. **Disclosure**: PTR received 2022-10-12 10:09:00 (US Eastern).
3. **Entry date** = first NYSE trading day after the disclosure date = **2022-10-13**.
4. **Entry price**: adjusted close 226.6893 (Yahoo 'Close' that day: 234.24). Size = midpoint $375,000.50; units = 375,000.50 / 226.6893 = 1,654.2490.
5. **Exit (senator sale)**: Sale (Partial) dated 2022-10-05, disclosed 2022-11-10 14:56:00 ($100,001 - $250,000); executed at the close of **2022-11-11**, adjusted close 239.1444 (Yahoo 'Close' 247.11). The partial sale sells $175,000.50 / 239.1444 = 731.7775 units of this lot (entry cost 165,886.11). Return 239.1444 / 226.6893 - 1 = **5.49%**; P&L $9,114.39 over 21 trading days (29 calendar days).
6. **Exit (senator sale)**: Sale (Partial) dated 2022-11-22, disclosed 2022-12-14 14:51:00 ($100,001 - $250,000); executed at the close of **2022-12-15**, adjusted close 241.6623 (Yahoo 'Close' 249.01). The partial sale sells $175,000.50 / 241.6623 = 724.1531 units of this lot (entry cost 164,157.74). Return 241.6623 / 226.6893 - 1 = **6.61%**; P&L $10,842.76 over 44 trading days (63 calendar days).
7. **Exit (senator sale)**: Sale (Full) dated 2023-06-20, disclosed 2023-07-14 12:55:00 ($250,001 - $500,000); executed at the close of **2023-07-17**, adjusted close 337.1040 (Yahoo 'Close' 345.73). Sells all 198.3184 units. Return 337.1040 / 226.6893 - 1 = **48.71%**; P&L $21,897.28 over 188 trading days (277 calendar days).

_To check on Yahoo Finance: open finance.yahoo.com/quote/MSFT/history, set the dates, and compare the 'Close' column (adjusted for splits only) with the Close shown here; the return uses 'Adj Close', which also reinvests dividends. Yahoo re-adjusts 'Adj Close' after every new dividend, so its level today can differ slightly from ours; the ratio between two dates should match._

### A lot held to the end of the in-sample window: Tommy Tuberville, Intel Corporation - Common Stock (INTC)

1. **Senator's trade**: Purchase dated 2021-10-15, owner Joint, disclosed range $15,001 - $50,000 (record T07164.1, trade T07164).
2. **Disclosure**: PTR received 2021-11-10 14:26:00 (US Eastern).
3. **Entry date** = first NYSE trading day after the disclosure date = **2021-11-11**.
4. **Entry price**: adjusted close 46.8649 (Yahoo 'Close' that day: 50.53). Size = midpoint $32,500.50; units = 32,500.50 / 46.8649 = 693.4937.
5. **End of window**: 693.4937 units marked at the adjusted close of **2024-02-29**, 42.6056 (Yahoo 'Close' 43.05). Return 42.6056 / 46.8649 - 1 = **-9.09%**; P&L $-2,953.80 over 576 trading days (840 calendar days).

_To check on Yahoo Finance: open finance.yahoo.com/quote/INTC/history, set the dates, and compare the 'Close' column (adjusted for splits only) with the Close shown here; the return uses 'Adj Close', which also reinvests dividends. Yahoo re-adjusts 'Adj Close' after every new dividend, so its level today can differ slightly from ours; the ratio between two dates should match._
