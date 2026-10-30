"""Regenerate combined rankings from historical and checksum-verified Python reruns.
Only complete SHA256-verified batches participate. Unfinished batches remain visible
in the coverage matrix, without being represented as completed test results.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "combined_top100"
BATCH_ROOT = RESULTS / "all_timeframes"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rank_kelly_bernoulli as previous

FRAMES = previous.TIMEFRAMES
FAMILIES = ("original", "compound", "fixed")


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def number(x, default=math.nan):
    try:
        n = float(x)
        return n if math.isfinite(n) else default
    except (ValueError, TypeError):
        return default


def truth(x):
    return str(x).lower() in ("true", "yes", "1")


def view(df, cols):
    lines = ["| " + " | ".join(cols) + " |",
             "|" + "|".join("---" for _ in cols) + "|"]
    for _, row in df.iterrows():
        def display(c):
            x = row[c]
            if pd.isna(x):
                return "—"
            if c.endswith("_pct"):
                return f"{float(x):.2f}%"
            return str(x).replace("|", "/").replace("\n", " ")
        lines.append("| " + " | ".join(display(c) for c in cols) + " |")
    return "\n".join(lines) + "\n"


def rerun_row(r, d):
    return {
        "來源": "舊（Python多週期重測）", "原始策略族群": "舊",
        "策略分類": str(r["策略分類"]), "策略": str(r["策略"]),
        "商品": str(r["商品"]), "商品名稱": str(r["商品"]),
        "市場": str(r["市場"]), "週期": str(r["時區"]),
        "出場方式": str(r["出場方式"]), "倉位法": str(r["倉位法"]),
        "五年收益_pct": number(r["五年收益_pct"]),
        "五年交易數": int(number(r["五年交易數"], 0)),
        "最大回撤_pct": number(r["五年最大回撤_pct"]),
        "OOS收益_pct": number(r["OOS收益_pct"]),
        "OOS交易數": int(number(r["OOS交易數"], 0)),
        "IS交易數": int(number(r["IS交易數"], 0)),
        "IS_Kelly_pct": number(r["IS_Kelly_pct"]),
        "實際風險_pct": number(r["實際風險_pct"]),
        "勝率_pct": number(r["五年勝率_pct"]),
        "止盈數": int(number(r["止盈出場數"], 0)),
        "止損數": int(number(r["止損出場數"], 0)),
        "資料完整標記": truth(r["資料完整"]),
        "資金停止": truth(r["資金停止"]),
        "策略規則": str(r["策略規則"]),
        "原始證據": f"results/all_timeframes/{d.name}/ranking.csv",
        "逐筆證據": f"results/all_timeframes/{d.name}/trades.csv",
        "原始狀態": "complete_sha256_verified",
        "IS勝率_p": number(r["IS勝率_p"]),
        "IS平均贏虧比_b": number(r["IS平均贏虧比_b"]),
    }


def main():
    old = pd.read_csv(RESULTS / "complete_ranking_9556.csv.gz",
                      compression="gzip", encoding="utf-8-sig")
    if len(old) != 9556:
        raise ValueError("Unexpected number of old rows")
    rows = []
    for _, source in old.iterrows():
        row = previous.normalize_old(source)
        row.update({"原始策略族群": "舊",
                    "原始狀態": "legacy_daily_snapshot_unreproduced",
                    "逐筆證據": "",
                    "IS勝率_p": math.nan, "IS平均贏虧比_b": math.nan})
        rows.append(row)
    new_provenance = {}
    for tf in FRAMES:
        stem = f"new_BTCUSDT_{tf}_five_year"
        source = RESULTS / "intraday" / f"{stem}_ranking.csv"
        manifest = json.loads((RESULTS / "intraday" / f"{stem}_provenance.json")
                              .read_text(encoding="utf-8"))
        frame = pd.read_csv(source, encoding="utf-8-sig")
        if (len(frame) != 28 or manifest["timeframe"] != tf
                or manifest["missing_or_irregular_intervals"] != 0
                or not manifest["historical_data"]
                or len(manifest["completed_strategy_names"]) != 7):
            raise ValueError(f"Invalid new snapshot {tf}")
        signed = manifest.get("ranking_csv_sha256")
        if signed is not None and digest(source) != signed:
            raise ValueError(f"New snapshot checksum mismatch {tf}")
        status = ("ohlcv_plus_ranking_sha256_verified" if signed
                  else "ohlcv_provenance_csv_unhashed")
        new_provenance[tf] = status
        for _, r in frame.iterrows():
            row = previous.normalize_new(r, tf)
            row.update({"原始策略族群": "新", "原始狀態": status,
                        "逐筆證據": "", "IS勝率_p": math.nan,
                        "IS平均贏虧比_b": math.nan})
            rows.append(row)

    coverage = []
    reruns = []
    audited = {}
    for tf in FRAMES:
        for family in FAMILIES:
            name = f"legacy_BTCUSDT_{tf}_{family}"
            d = BATCH_ROOT / name
            mf = d / "manifest.json"
            state = "not_started"
            configs = 0
            tests = 0
            if mf.exists():
                meta = json.loads(mf.read_text(encoding="utf-8"))
                ranking = d / "ranking.csv"
                trade = d / "trades.csv"
                if (meta.get("status") != "complete"
                        or meta.get("timeframe") != tf
                        or meta.get("family") != family
                        or not ranking.is_file() or not trade.is_file()
                        or meta.get("ranking_sha256") != digest(ranking)
                        or meta.get("trades_sha256") != digest(trade)):
                    raise ValueError(f"Invalid completed manifest {name}")
                frame = pd.read_csv(ranking, encoding="utf-8-sig")
                expected = {"original": 8, "compound": 8, "fixed": 9}[family]
                if (len(frame) != meta.get("ranking_rows")
                        or frame["策略"].nunique() != expected
                        or len(meta.get("completed", [])) != expected
                        or not frame["資料完整"].map(truth).all()):
                    raise ValueError(f"Incomplete batch result {name}")
                reruns.extend(rerun_row(r, d) for _, r in frame.iterrows())
                configs = len(frame)
                tests = expected
                state = "complete_sha256_verified"
                audited[name] = {
                    "OHLCV_SHA256": meta.get("ohlcv_sha256"),
                    "ranking_SHA256": meta["ranking_sha256"],
                    "trades_SHA256": meta["trades_sha256"],
                    "strategies": tests, "configurations": configs}
            elif (d / "checkpoint.json").exists():
                cp = json.loads((d / "checkpoint.json").read_text(encoding="utf-8"))
                state = "partial_unverified_not_ranked"
                tests = len(cp.get("strategies", []))
                configs = cp.get("ranked_configs", 0)
            coverage.append({"週期": tf, "策略類型": family,
                             "狀態": state, "完成策略數": tests,
                             "配置數": configs})
    # Once verified fresh daily tests exist, do not prefer old historical rows
    # for those same symbol / timeframe / strategy names.
    replaced = {(r["商品"], r["週期"], r["策略"]) for r in reruns}
    rows = [r for r in rows if not (r["原始策略族群"] == "舊" and
        (r["商品"], r["週期"], r["策略"]) in replaced)]
    rows.extend(reruns)
    df = pd.DataFrame(rows)
    df["實際風險_pct"] = df["實際風險_pct"].where(
        df["實際風險_pct"].notna(),
        df.apply(previous.percent_risk, axis=1))
    df["Kelly倉位數值合格"] = (
        df["IS_Kelly_pct"].gt(0) & df["實際風險_pct"].gt(0)
        & df["實際風險_pct"].le(df["IS_Kelly_pct"] + 1e-7))
    df["數值收益門檻"] = (
        df["五年交易數"].ge(70) & df["五年收益_pct"].gt(100)
        & df["最大回撤_pct"].between(0, 100)
        & df["資料完整標記"]
        & ~df["資金停止"].fillna(False).astype(bool))
    df["伯努利iid驗證"] = "未驗證：Kelly從IS勝敗樣本估算，但不代表獨立同分布"
    good = df[df["數值收益門檻"] & df["Kelly倉位數值合格"]]
    good = good.sort_values(["五年收益_pct", "最大回撤_pct"],
                            ascending=[False, True])
    keys = ["商品", "週期", "策略", "出場方式"]
    good = good.drop_duplicates(keys, keep="first")
    top = good.head(100).copy().reset_index(drop=True)
    top.insert(0, "收益名次", range(1, len(top) + 1))
    families = (df.sort_values(["五年收益_pct", "最大回撤_pct"],
                  ascending=[False, True])
                  .drop_duplicates(["原始策略族群", "策略"])
                  .reset_index(drop=True))
    families.insert(0, "策略家族名次", range(1, len(families) + 1))
    eligible_names = set(map(tuple, good[["原始策略族群", "策略"]].to_numpy()))
    families["家族存在收益合格變體"] = [
        (r["原始策略族群"], r["策略"]) in eligible_names
        for _, r in families.iterrows()]
    if len(families) != 38:
        raise ValueError(f"Missing old/new families: {len(families)}")
    if top.duplicated(keys).any() or not top["Kelly倉位數值合格"].all():
        raise ValueError("Ranking duplicates or Kelly violations")
    OUT.mkdir(parents=True, exist_ok=True)
    common = ["來源", "原始狀態", "策略", "商品", "週期", "出場方式", "倉位法",
              "五年交易數", "五年收益_pct", "最大回撤_pct", "OOS收益_pct",
              "IS交易數", "IS_Kelly_pct", "實際風險_pct",
              "Kelly倉位數值合格", "伯努利iid驗證", "原始證據", "逐筆證據"]
    top[["收益名次", *common]].to_csv(OUT / "top100_by_return.csv",
                      index=False, encoding="utf-8-sig")
    fam_cols = ["原始策略族群", "來源", "原始狀態", "策略", "商品",
                "週期", "出場方式", "倉位法", "五年交易數", "五年收益_pct",
                "最大回撤_pct", "OOS收益_pct", "IS_Kelly_pct",
                "實際風險_pct", "Kelly倉位數值合格", "數值收益門檻",
                "家族存在收益合格變體"]
    f = families[["策略家族名次", *fam_cols]]
    f.to_csv(OUT / "top100_by_strategy.csv", index=False, encoding="utf-8-sig")
    f.to_csv(OUT / "all_strategy_families_ranked.csv",
             index=False, encoding="utf-8-sig")
    matrix = pd.DataFrame(coverage)
    matrix.to_csv(OUT / "old_strategy_coverage_matrix.csv",
                  index=False, encoding="utf-8-sig")
    (OUT / "old_strategy_coverage_matrix.md").write_text(
        "# 舊策略五年多週期覆蓋矩陣\n\n" +
        view(matrix, ["週期", "策略類型", "狀態", "完成策略數", "配置數"]),
        encoding="utf-8")
    (OUT / "top100_by_return.md").write_text(
        "# 舊＋新 Python 五年收益 Top100\n\n"
        "僅已有五年交易數>=70、收益>100%、風險<=前四年IS Kelly且"
        "最大回撤合理的去重配置；不可將未跑的舊週期視為完成。"
        "伯努利獨立同分布與TradingView一致性尚未驗證。\n\n"+
        view(top, ["收益名次", "來源", "策略", "商品", "週期", "倉位法",
                   "五年收益_pct", "五年交易數", "最大回撤_pct",
                   "OOS收益_pct", "IS_Kelly_pct", "實際風險_pct", "原始狀態"]),
        encoding="utf-8")
    family_text = ("# 全部舊＋新策略家族排名\n\n"
        "舊31種與新7種；保留未達70筆及低收益者。每個策略"
        "取已存在回測的最高五年收益配置，跨週期尚未重跑則不會冒充。\n\n"
        + view(families, ["策略家族名次", "原始策略族群", "策略",
            "商品", "週期", "五年收益_pct", "五年交易數",
            "家族存在收益合格變體", "原始狀態"]))
    (OUT / "all_strategy_families_ranked.md").write_text(
        family_text, encoding="utf-8")
    (OUT / "top100_by_strategy.md").write_text(
        family_text, encoding="utf-8")
    completed = len(audited)
    report = {
        "status": "complete" if completed == len(FRAMES)*len(FAMILIES) else "partial",
        "legacy_daily_archive_rows": len(old),
        "new_strategy_timeframes": len(FRAMES),
        "new_strategy_configurations": 336,
        "completed_legacy_timeframe_family_batches": completed,
        "required_legacy_timeframe_family_batches": len(FRAMES)*len(FAMILIES),
        "verified_new_legacy_configuration_rows": len(reruns),
        "all_strategy_families": len(families),
        "qualifying_unique_return_candidates": len(good),
        "published_top_return_rows": len(top),
        "top100_legacy": int(top["原始策略族群"].eq("舊").sum()),
        "top100_new": int(top["原始策略族群"].eq("新").sum()),
        "new_provenance": new_provenance,
        "legacy_batch_checksums": audited,
        "bernoulli_iid_verified": False, "tradingview_parity_verified": False,
        "all_TV_timeframes_and_markets_complete": False}
    (OUT / "latest_verification_manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Trade Test：Python 舊＋新多週期完整回測排名\n\n"
        f"執行狀態：{report['status']}，舊策略已完成並通過 SHA256 "
        f"驗證批次 {completed}/{len(FRAMES)*len(FAMILIES)}；"
        f"新策略既有 {len(FRAMES)} 個週期的 BTC 五年回測資料。\n\n"
        f"最新完整策略家族榜 {len(families)} 列，"
        f"收益前 {len(top)} 列（舊{report['top100_legacy']}／"
        f"新{report['top100_new']}）。\n\n"
        "每個已完成舊策略批次保留交易與排名 CSV、checkpoint 和 SHA256 manifest，"
        "批次狀態請見 old_strategy_coverage_matrix.csv。"
        "舊日線歷史快照未逐列獨立驗證，未完成週期不可假裝完成。"
        "勝敗的伯努利 iid 假設以及 TradingView 逐筆比對尚未驗證。\n",
        encoding="utf-8")
    print("AGGREGATION", json.dumps({
        "completed_old_batches": completed,
        "out_of": len(FRAMES)*len(FAMILIES),
        "verified_retested_rows": len(reruns),
        "families": len(families), "top": len(top),
        "old": report["top100_legacy"], "new": report["top100_new"],
    }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
