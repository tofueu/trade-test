"""Regenerate OLD+NEW strategy and Kelly/Bernoulli-assumption rankings.

Inputs: immutable historical CSV snapshots already in this research branch.
This program sorts existing Python backtests; it is NOT a re-backtest or
proof of independent Bernoulli win/loss observations.
"""
from __future__ import annotations

import math
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "combined_top100"
OUT.mkdir(parents=True, exist_ok=True)
TIMEFRAMES = ("1m", "3m", "5m", "15m", "30m", "1h",
              "2h", "4h", "6h", "8h", "12h", "1d")


def number(value: object, default: float = math.nan) -> float:
    try:
        x = float(value)
        return x if math.isfinite(x) else default
    except (ValueError, TypeError):
        return default


def value(row: pd.Series, key: str, default: object = "") -> object:
    return row[key] if key in row and pd.notna(row[key]) else default


def percent_risk(row: dict) -> float:
    method = row["倉位法"]
    k = row["IS_Kelly_pct"]
    if method == "固定1R":
        return 10.0  # repo base.FIXED_RISK=0.10 of initial equity
    if method == "全凱利":
        return k
    if method == "半凱利":
        return k / 2
    if method == "四分之一凱利":
        return k / 4
    return math.nan


def normalize_old(r: pd.Series) -> dict:
    return {
        "來源": "舊（日線多市場）",
        "策略分類": str(value(r, "測試類型")),
        "策略": str(value(r, "策略")),
        "商品": str(value(r, "代碼")),
        "商品名稱": str(value(r, "商品")),
        "市場": str(value(r, "市場")),
        "週期": "1d",
        "出場方式": str(value(r, "出場方式")),
        "倉位法": str(value(r, "倉位法")),
        "五年收益_pct": number(value(r, "五年收益_pct")),
        "五年交易數": int(number(value(r, "五年交易數"), 0)),
        "最大回撤_pct": number(value(r, "五年最大回撤_pct")),
        "OOS收益_pct": number(value(r, "OOS收益_pct")),
        "OOS交易數": int(number(value(r, "OOS交易數"), 0)),
        "IS交易數": int(number(value(r, "IS交易數"), 0)),
        "IS_Kelly_pct": number(value(r, "IS_Kelly_pct")),
        "勝率_pct": math.nan,
        "止盈數": int(number(value(r, "止盈出場數"), 0)),
        "止損數": int(number(value(r, "止損出場數"), 0)),
        "資料完整標記": True,
        "資金停止": None,
        "策略規則": str(value(r, "策略規則")),
        "原始證據": "results/complete_ranking_9556.csv.gz",
    }


def normalize_new(r: pd.Series, tf: str) -> dict:
    def flag(key: str) -> bool:
        return str(value(r, key)).strip().lower() in ("true", "1")
    return {
        "來源": "新（BTC多週期）",
        "策略分類": "新策略×BTC多週期",
        "策略": str(value(r, "策略")),
        "商品": str(value(r, "代碼")),
        "商品名稱": str(value(r, "商品")),
        "市場": str(value(r, "市場")),
        "週期": tf,
        "出場方式": str(value(r, "出場方式")),
        "倉位法": str(value(r, "倉位法")),
        "五年收益_pct": number(value(r, "五年收益_pct")),
        "五年交易數": int(number(value(r, "五年交易數"), 0)),
        "最大回撤_pct": number(value(r, "五年最大回撤_pct")),
        "OOS收益_pct": number(value(r, "OOS收益_pct")),
        "OOS交易數": int(number(value(r, "OOS交易數"), 0)),
        "IS交易數": int(number(value(r, "IS交易數"), 0)),
        "IS_Kelly_pct": number(value(r, "IS_Kelly_pct")),
        "勝率_pct": number(value(r, "五年勝率_pct")),
        "止盈數": int(number(value(r, "止盈出場數"), 0)),
        "止損數": int(number(value(r, "止損出場數"), 0)),
        "資料完整標記": flag("資料完整"),
        "資金停止": flag("資金停止"),
        "策略規則": str(value(r, "策略規則")),
        "原始證據": f"results/intraday/new_BTCUSDT_{tf}_five_year_ranking.csv",
    }


def md_escape(x: object) -> str:
    return str(x).replace("|", "/").replace("\n", " ")


def show_md(df: pd.DataFrame, cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |\n"
    sep = "|" + "|".join("---" for _ in cols) + "|\n"
    lines = []
    for _, row in df.iterrows():
        cells = []
        for c in cols:
            v = row[c]
            if pd.isna(v):
                cells.append("—")
            elif c.endswith("_pct"):
                cells.append(f"{float(v):.2f}%")
            else:
                cells.append(md_escape(v))
        lines.append("| " + " | ".join(cells) + " |")
    return header + sep + "\n".join(lines) + "\n"


def main() -> None:
    original = pd.read_csv(RESULTS / "complete_ranking_9556.csv.gz",
                           compression="gzip", encoding="utf-8-sig")
    rows = [normalize_old(r) for _, r in original.iterrows()]
    new_source = 0
    for tf in TIMEFRAMES:
        path = RESULTS / "intraday" / f"new_BTCUSDT_{tf}_five_year_ranking.csv"
        new = pd.read_csv(path, encoding="utf-8-sig")
        new_source += len(new)
        rows += [normalize_new(r, tf) for _, r in new.iterrows()]
    if len(original) != 9556 or new_source != 336:
        raise RuntimeError(f"Unexpected source sizes: {len(original)} + {new_source}")

    all_rows = pd.DataFrame(rows)
    all_rows["實際風險_pct"] = all_rows.apply(percent_risk, axis=1)
    all_rows["Kelly倉位數值合格"] = (
        all_rows["IS_Kelly_pct"].gt(0)
        & all_rows["實際風險_pct"].gt(0)
        & all_rows["實際風險_pct"].le(all_rows["IS_Kelly_pct"] + 1e-7)
    )
    all_rows["五年數值門檻"] = (
        all_rows["五年交易數"].ge(70)
        & all_rows["五年收益_pct"].gt(100)
        & all_rows["最大回撤_pct"].between(0, 100)
        & all_rows["資料完整標記"]
        & ~all_rows["資金停止"].fillna(False).astype(bool)
    )
    # "Bernoulli" is the modeling assumption used to estimate p from
    # binary win/loss outcomes. CSVs do NOT contain IS trade-by-trade
    # outcomes: independence/stationarity cannot be empirically certified.
    all_rows["伯努利獨立同分布驗證"] = "未驗證－須檢視逐筆IS勝敗與序列相關"
    all_rows["Kelly計算依據"] = "前4年IS勝率p及平均贏虧比b；f*=p-(1-p)/b"
    all_rows["收益榜候選"] = all_rows["五年數值門檻"] & all_rows["Kelly倉位數值合格"]
    valid = all_rows[all_rows["收益榜候選"]].sort_values(
        ["五年收益_pct", "最大回撤_pct"], ascending=[False, True]
    )
    unique_keys = ["商品", "週期", "策略", "出場方式"]
    unique = valid.drop_duplicates(unique_keys, keep="first")
    ret = unique.head(100).copy().reset_index(drop=True)
    ret.insert(0, "收益名次", range(1, len(ret) + 1))

    # All strategy families: do NOT exclude losing or <70-trade families.
    families = all_rows.sort_values(
        ["五年收益_pct", "最大回撤_pct"], ascending=[False, True]
    ).drop_duplicates(["來源", "策略"], keep="first")
    exists_good = set(map(tuple, unique[["來源", "策略"]].to_numpy()))
    families = families.copy()
    families["此家族至少有一個合格配置"] = [
        (v, s) in exists_good for v, s in families[["來源", "策略"]].to_numpy()
    ]
    families = families.reset_index(drop=True)
    families.insert(0, "策略家族名次", range(1, len(families) + 1))

    if len(families) != 38:
        raise RuntimeError(f"Expected 31 legacy + 7 new family rows, got {len(families)}")
    if len(ret) != 100:
        raise RuntimeError(f"Only {len(ret)} Kelly capped unique configurations; do not pad fake entries")
    if not ret["五年數值門檻"].all() or not ret["Kelly倉位數值合格"].all():
        raise AssertionError("One or more candidates violate numeric / sizing thresholds")
    if ret.duplicated(unique_keys).any():
        raise AssertionError("Duplicate symbol/timeframe/strategy/exit in top100")
    cols = ["來源", "策略", "商品", "週期", "出場方式", "倉位法",
            "五年交易數", "五年收益_pct", "最大回撤_pct", "OOS收益_pct",
            "IS交易數", "IS_Kelly_pct", "實際風險_pct", "Kelly倉位數值合格",
            "伯努利獨立同分布驗證", "原始證據"]
    ret[["收益名次", *cols]].to_csv(
        OUT / "top100_by_return.csv", index=False, encoding="utf-8-sig"
    )
    family_cols = ["來源", "策略", "商品", "週期", "出場方式", "倉位法",
                   "五年交易數", "五年收益_pct", "最大回撤_pct",
                   "OOS收益_pct", "IS_Kelly_pct", "實際風險_pct",
                   "Kelly倉位數值合格", "五年數值門檻",
                   "此家族至少有一個合格配置", "伯努利獨立同分布驗證"]
    families[["策略家族名次", *family_cols]].to_csv(
        OUT / "all_strategy_families_ranked.csv", index=False, encoding="utf-8-sig"
    )
    families[["策略家族名次", *family_cols]].to_csv(
        OUT / "top100_by_strategy.csv", index=False, encoding="utf-8-sig"
    )
    intro = (
        "# 舊＋新策略，全部策略家族排名\n\n"
        "這份榜單涵蓋所有研究來源策略家族：舊31種、新7種（名稱可能重疊），"
        "不因交易不足70筆或五年收益不足100%而消失。故為38列，**不得補造100種**。\n\n"
        "每一來源×策略取現有配置的最高五年收益；『此家族至少有一個合格配置』"
        "是檢查家族內其他配置是否有符合交易、收益、回撤與Kelly數值限制。\n\n"
        "Kelly倉位數值合格不代表伯努利獨立同分布已證實；原始交易序列未隨CSV提供。\n\n"
    )
    family_md = intro + show_md(families, [
        "策略家族名次", "來源", "策略", "商品", "週期", "倉位法",
        "五年收益_pct", "五年交易數", "IS_Kelly_pct",
        "實際風險_pct", "Kelly倉位數值合格", "此家族至少有一個合格配置"
    ])
    for name in ("top100_by_strategy.md", "all_strategy_families_ranked.md"):
        (OUT / name).write_text(family_md, encoding="utf-8")
    (OUT / "top100_by_return.md").write_text(
        "# 舊＋新：收益 Top100（Kelly風險上限篩選）\n\n"
        "從9556列舊日線+336列新BTC多週期現有回測數據整理，已嚴格篩選"
        "五年成交>=70、五年收益>100%、最大回撤介於0~100%、Kelly>0、"
        "實際部位風險<=前四年IS Kelly，並依商品×週期×策略×出場方式去重。\n\n"
        "注意：**這是 Kelly 參數與部位大小的數值合規榜，不代表伯努利"
        "勝敗獨立同分布已獲證實，也不是 TradingView 或實盤績效驗證**。"
        "部分舊結果沒有逐筆IS輸出、也沒有行情來源manifest，需再稽核。\n\n"
        + show_md(ret, [
            "收益名次", "來源", "策略", "商品", "週期", "倉位法",
            "五年收益_pct", "五年交易數", "最大回撤_pct",
            "OOS收益_pct", "IS_Kelly_pct", "實際風險_pct"
        ]), encoding="utf-8"
    )

    old_count = int(ret["來源"].str.startswith("舊").sum())
    new_count = len(ret) - old_count
    manual = f"""# Trade Test 舊＋新：Kelly / 伯努利模型排名說明

## 最新報表
- 全部策略家族：{len(families)} 列（舊31、新7；部分同名），包含不合格策略，見 \`all_strategy_families_ranked.md\` 或 \`top100_by_strategy.md\`。
- 合格收益 Top 100：{len(ret)} 列（舊{old_count}、新{new_count}），見 \`top100_by_return.md\`。
- 重排來源：舊五年日線9,556列，新BTC12週期336列；**此次只是對既有Python輸出重新檢驗／排序，沒有完成舊策略全時區重測。**

## 數值硬性要求
1. 五年實際成交筆數 >=70，五年累積收益率 **>100%**，最大回撤0~100%，有新資料完整記錄且未標記資金停止。
2. 部位倉位與Kelly：原程式按**前四年IS**樣本勝率p、輸家平均虧損與贏家平均獲利比b，計算 \`f*=max(0, p - (1-p)/b)\`，可用的實際部位風險百分比須 **0 < 風險 <= IS_Kelly_pct**。
3. 固定1R在原程式代表初始本金10%的風險，不能因名叫固定1R就視作1%。若10% > IS_Kelly_pct，該列不得進收益榜。
4. 不得將全凱利的舊收益直接改標成半凱利。**必須使用實際完成過的半凱利回測收益**；去重每商品×週期×策略×出場方式只取最高合規倉位結果。
5. 伯努利：勝敗為二元結果，\`p=IS贏單數/IS總單數\`，\`q=1-p\`，\`b=IS平均獲利R/平均虧損R\`。勝率估計可作Bernoulli模型輸入，但交易獨立同分布、樣本穩定性、連敗分布、置信下界及逐筆交易輸出 **尚未獨立驗證**。不得把「Kelly計算出數值」當作「伯努利假設已通過」。
6. 舊與新排行僅基於已存在的實測配置；舊 1D 以外時框、缺少的TradingView週期、HTF>LTF、部分標的仍需要跑，秒級資料不足時標 unavailable，不能捏造。

## 產生方式
\`python research/multi-market-strategy-ranking/tools/rank_kelly_bernoulli.py\`

此腳本重新從原始壓縮CSV讀取並核對每列門檻，輸出四份CSV/Markdown；不修改原CSV，不將結果寫進main，不執行TV轉換。
"""
    (OUT / "README.md").write_text(manual, encoding="utf-8")
    print("INPUT", len(original), new_source)
    print("PASS_RAW", int(all_rows["收益榜候選"].sum()),
          "PASS_DEDUP", len(unique), "TOP100", len(ret),
          "FAMILIES", len(families), "OLD_NEW_TOP100", old_count, new_count,
          flush=True)


if __name__ == "__main__":
    main()
