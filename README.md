# Trade Test｜多市場交易策略研究

本倉庫收錄策略規則、回測程式與五年收益排名。完整的策略條件、資料假設和欄位解讀請看[研究說明](research/multi-market-strategy-ranking/README.md)。

## 主要結果

- [五年綜合排名前 50 名](research/multi-market-strategy-ranking/results/overall_top50.csv)
- [五年且 OOS 為正、交易數超過 50 的策略](research/multi-market-strategy-ranking/results/positive_oos_over50.csv.gz)
- [完整 9,556 組排名（Gzip CSV）](research/multi-market-strategy-ranking/results/complete_ranking_9556.csv.gz)
- [新增策略前 50 名](research/multi-market-strategy-ranking/results/additional_strategy_top50.csv)
- [新增策略 728 組完整結果（Gzip CSV）](research/multi-market-strategy-ranking/results/additional_strategy_results_728.csv.gz)

## 回測程式

- [新增策略回測入口](research/multi-market-strategy-ranking/src/run_strategies.py)
- [五年多市場與 Kelly 共用程式](research/multi-market-strategy-ranking/src/five_year_multi_market_kelly.py)
- [策略條件、停損停利、成本假設、使用方式與限制](research/multi-market-strategy-ranking/README.md)

回測資料涵蓋 2021-10-10 至 2026-10-10（日線；最後一年為 OOS），包含加密貨幣、外匯及傳統期貨商品。這些是歷史模擬結果，不代表實盤收益或未來表現；完整假設和限制請閱讀研究說明。
