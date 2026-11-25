# User scope correction — 2026-11-25

Ranks 3, 4, 6 and 7 are protected by the user's latest instruction: retain their just-updated active Pine versions and do not modify them further. The rank 3/6/7 files under drafts/ are withdrawn proposals for historical reference only; do not apply them. No active Pine file was replaced by the draft verification commit.

Remaining Pine repair/verification scope: ranks 1, 2, 5, and 8 through 31 (27 strategies). First verify Pine against the original Python; only after verification proceed with Binance USD-M API work. No five-year expiry is to be imposed on a future live execution entrypoint. Existing historical ranking results remain preserved.

---

# Pine verification before Binance USD-M API

31 strategy-branch Pine files were inspected against saved original Python rules and ranking configurations. audit.json records exact reviewed blobs and pending findings. Ranks 3, 6 and 7 have staged draft fixes removing end-date inputs; ranks 3 and 7 also fix direct reversal entry conditions, and rank 3 removes an extra signal/ATR delay relative to original Python next-open execution.

Draft source/transition checks passed via check_drafts.py. The deterministic fixture in that check is not real price data and supplies no performance evidence. The original Python backtest function is used unchanged. This is not a Pine compiler.

TradingView compilation/execution remains NOT RUN: pressing Add to chart in the GPT in-app TradingView browser presented Log in. No strategy is declared validated; these drafts have not replaced the active strategy files. 27 built-in indicator ports still need initialization/custom-Supertrend parity review. Some Pine risk/TP defaults differ from saved rankings; ranks 7 and 22 still lack matching raw ranking rows.

API development for Binance USDT perpetual futures is deferred until Pine verification passes, as requested. No live order is enabled. Historical Python source/results are preserved. The live entrypoint will not inherit a five-year expiry.
