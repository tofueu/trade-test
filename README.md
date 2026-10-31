# Trade Test｜多市場交易策略研究

本倉庫收錄五年多市場研究的策略條件、Python 回測程式與收益排名。總榜共有 9,556 列，涵蓋 32 種訊號規則，並展開不同出場法、商品及倉位法。

## 查看排名

- [綜合收益前 50 名](research/multi-market-strategy-ranking/results/overall_top50.csv)
- [五年及 OOS 都正收益、交易超過 50 筆](research/multi-market-strategy-ranking/results/positive_oos_over50.csv.gz)
- [完整 9,556 列排名（Gzip CSV）](research/multi-market-strategy-ranking/results/complete_ranking_9556.csv.gz)
- [新增策略 728 組結果（Gzip CSV）](research/multi-market-strategy-ranking/results/additional_strategy_results_728.csv.gz)

## 研究與程式

- [完整策略規則、停損停利、成本假設、排名欄位與重建命令](research/multi-market-strategy-ranking/README.md)
- [8 種基礎訊號與共用回測程式](research/multi-market-strategy-ranking/src/five_year_multi_market_kelly.py)
- [出場變體、複合策略、固定盈虧及新增策略程式](research/multi-market-strategy-ranking/src/)

回測為歷史模擬，不代表實盤收益或未來表現。總榜期間為 2021-10-10 至 2026-10-10；最後一年作為 OOS。詳細資料、限制及可重現命令請見研究說明。
