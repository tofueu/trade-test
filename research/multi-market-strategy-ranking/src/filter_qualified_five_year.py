"""Filter historical Trade Test rows by user-requested minimum acceptance gates.

This does not execute a backtest or establish TradingView/Python parity.
Input must be the actual five-year ranking CSV from the existing research run.
"""
import argparse
import csv
import gzip
import math
from pathlib import Path

REQUIRED = ("五年收益_pct", "五年交易數", "IS_Kelly_pct")
MIN_TRADES = 70
MIN_RETURN = 100.0

def numeric(row, key):
    try:
        value = float(row[key].strip().replace("%", "").replace(",", ""))
    except (KeyError, ValueError, TypeError, AttributeError):
        return None
    return value if math.isfinite(value) else None

def qualify(rows):
    qualified = []
    total = 0
    for row in rows:
        total += 1
        ret = numeric(row, "五年收益_pct")
        trades = numeric(row, "五年交易數")
        kelly = numeric(row, "IS_Kelly_pct")
        # Strict >100% return, >=70 closed trades and positive IS Kelly.
        # Reject fractional trade counts and malformed/non-finite metrics.
        if (ret is None or trades is None or kelly is None
                or ret <= MIN_RETURN or trades < MIN_TRADES
                or not trades.is_integer() or kelly <= 0):
            continue
        qualified.append(row)
    qualified.sort(key=lambda row: (
        -numeric(row, "五年收益_pct"),
        numeric(row, "五年最大回撤_pct") if numeric(row, "五年最大回撤_pct") is not None else float("inf")))
    return total, qualified

def open_csv(path):
    if str(path).endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8-sig", newline="")
    return open(path, "r", encoding="utf-8-sig", newline="")

def run(input_path, output_path):
    with open_csv(input_path) as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or any(k not in reader.fieldnames for k in REQUIRED):
            raise ValueError("Missing required five-year return/trade/IS Kelly columns")
        fieldnames = list(reader.fieldnames)
        total, accepted = qualify(reader)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(accepted)
    return total, len(accepted)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Refusing to overwrite original ranking input")
    total, count = run(args.input, args.output)
    print(f"Five-year ranking rows: {total}; qualified (>100% return, >=70 trades, IS Kelly >0): {count}")
    print("Historical rows only; no new backtest or TradingView parity is claimed.")

if __name__ == "__main__":
    main()
