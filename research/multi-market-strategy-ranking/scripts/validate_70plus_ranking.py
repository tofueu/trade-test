import pandas as pd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "results" / "strategy_70plus_ranking.csv"

def is_full_five_years(row):
    try:
        start = pd.to_datetime(row['Start Date'])
        end = pd.to_datetime(row['End Date'])
        delta = end - start
        return delta.days >= 1800
    except:
        return False

def validate_ranking():
    if not CSV_PATH.exists():
        print(f"Error: {CSV_PATH} not found.")
        sys.exit(1)

    df = pd.read_csv(CSV_PATH)

    required_cols = [
        "Start Date", "End Date", "Data Source", "Costs", "Trades", "TP/SL",
        "CAGR %", "Max DD %", "Win Rate %", "PF", "IS Kelly %", "OOS Return %",
        "OOS Trades", "Pine Path", "Pine Status"
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"Error: Missing columns {missing}")
        sys.exit(1)

    valid_rows = []

    for idx, row in df.iterrows():
        if not is_full_five_years(row):
            continue
        if int(row['Trades']) < 70:
            continue
        if str(row['Pine Status']) != 'TV_UNVERIFIED':
            continue

        has_all_data = True
        for c in required_cols:
            if pd.isna(row[c]) or str(row[c]).strip() == "":
                has_all_data = False
                break

        if has_all_data:
            valid_rows.append(row)

    valid_df = pd.DataFrame(valid_rows)

    if not valid_df.empty:
        # Sort properly again just in case
        valid_df['5y Net Return %'] = pd.to_numeric(valid_df['5y Net Return %'])
        valid_df = valid_df.sort_values("5y Net Return %", ascending=False).reset_index(drop=True)
        valid_df["Rank"] = range(1, len(valid_df) + 1)

        valid_df.to_csv(CSV_PATH, index=False)
        md_path = ROOT / "results" / "strategy_70plus_ranking.md"
        valid_df.to_markdown(md_path, index=False)

        summary = f"Validation successful. Retained {len(valid_df)} valid strategies. Files overwritten."
        print(summary)

        summary_path = ROOT / "results" / "strategy_70plus_ranking_summary.md"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(f"# 70+ Ranking Validation Summary\n\n{summary}\n")
    else:
        print("Error: No valid strategies remained after filtering.")
        sys.exit(1)

if __name__ == "__main__":
    validate_ranking()
