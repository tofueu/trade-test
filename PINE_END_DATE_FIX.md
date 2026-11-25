# Pine optional test end — 2026-11-25

The user-nominated prior conversation Pine is restored as strategy.pine. Added limitTestEnd (default false). When disabled, the existing start-time condition remains and there is no end-time block or forced end close. Enable it to restore the original fixed-period comparison and final close. Indicators, signals, sizing, costs and normal exits are unchanged relative to the nominated conversation source.

Python historical START/END/OOS remain unchanged for reproducible rankings. This is not a live execution API. This commit has source-diff and date-gate checks only; TradingView compile and current-chart execution are untested. Prior conversation script defaults are preserved and may differ from the homepage best configuration.

Backups are stored under backups/before_optional_end_20261125/.
