# Removed Pine historical end date

2026-11-25: Removed the endTime input, the upper date bound on entries, and forced end-of-test closure. No optional end-date toggle was added. This existing Pine continues to evaluate confirmed signals after 2026-10-10. All indicators, normal exits, initial stop, sizing (11.7685413% half Kelly), commission and other parameters remain unchanged relative to the saved conversation version. The original start-time/warm-up settings remain.

Python historical dates are unchanged. This Pine is the prior daily half-Kelly configuration, not a verified reproduction of the homepage SOLUSDT 2h fixed-10% result. Source-diff checks passed; TradingView compilation and execution have not been run. Backup is in backups/before_remove_end_20261125/.
