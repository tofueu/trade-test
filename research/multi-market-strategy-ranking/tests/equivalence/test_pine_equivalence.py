import pytest
import os
import glob
import re
import pandas as pd

def get_pine_scripts():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    pine_dir = os.path.join(base_dir, "pine")
    return glob.glob(os.path.join(pine_dir, "*.pine"))

def extract_pine_metadata(filepath):
    """Parses Pine Script headers for metadata."""
    metadata = {
        "filename": os.path.basename(filepath),
        "version": None,
        "strategy_name": None,
        "tv_status": "UNVERIFIED"
    }
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    version_match = re.search(r"//@version=(\d+)", content)
    if version_match:
        metadata["version"] = int(version_match.group(1))

    strat_match = re.search(r"strategy\(\"([^\"]+)\"", content)
    if strat_match:
        metadata["strategy_name"] = strat_match.group(1)

    status_match = re.search(r"// TV Status:\s*(.*)", content)
    if status_match:
        metadata["tv_status"] = status_match.group(1).strip()

    return metadata

def compare_logs(python_log_path, tv_log_path, price_tolerance=0.001):
    """Fail-closed Python/TradingView trade parity, never count-only equality.

    Both files must provide canonical entry_time, exit_time, entry_price,
    exit_price and side columns. Other TradingView export schemas require an
    explicit, separately tested adapter; do not silently infer field meanings.
    """
    if not os.path.exists(python_log_path) or not os.path.exists(tv_log_path):
        return {"status": "UNVERIFIED", "reason": "Missing real trade log files"}
    if not isinstance(price_tolerance, (float, int)) or not 0 <= price_tolerance < 1:
        return {"status": "UNVERIFIED", "reason": "Invalid price tolerance"}

    required = ("entry_time", "exit_time", "entry_price", "exit_price", "side")
    try:
        py_df = pd.read_csv(python_log_path)
        tv_df = pd.read_csv(tv_log_path)
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        return {"status": "UNVERIFIED", "reason": "Unreadable trade logs"}

    if any(col not in py_df.columns or col not in tv_df.columns for col in required):
        return {"status": "UNVERIFIED", "reason": "Missing canonical trade columns; validated TV adapter required"}
    if py_df.empty or tv_df.empty:
        return {"status": "UNVERIFIED", "reason": "Empty trade log is not parity evidence"}
    if len(py_df) != len(tv_df):
        return {"status": "FAIL", "reason": f"Trade count mismatch: Py({len(py_df)}) vs TV({len(tv_df)})"}

    normalized = []
    for label, frame in (("Python", py_df), ("TradingView", tv_df)):
        data = frame.loc[:, required].copy()
        for col in ("entry_time", "exit_time"):
            data[col] = pd.to_datetime(data[col], utc=True, errors="coerce")
        for col in ("entry_price", "exit_price"):
            data[col] = pd.to_numeric(data[col], errors="coerce")
        data["side"] = data["side"].astype(str).str.strip().str.lower()
        data["side"] = data["side"].replace({"buy": "long", "sell": "short"})
        if (data.isna().any().any()
                or not data["side"].isin(("long", "short")).all()
                or not (data[["entry_price", "exit_price"]] > 0).all().all()
                or not (data["exit_time"] >= data["entry_time"]).all()):
            return {"status": "UNVERIFIED", "reason": f"Invalid {label} trade data"}
        normalized.append(data.sort_values(
            ["entry_time", "exit_time", "side"], kind="stable").reset_index(drop=True))

    py, tv = normalized
    for col in ("entry_time", "exit_time", "side"):
        if not py[col].equals(tv[col]):
            return {"status": "FAIL", "reason": f"Trade {col} mismatch"}
    for col in ("entry_price", "exit_price"):
        diff = (py[col] - tv[col]).abs()
        rel = diff / py[col].abs().clip(lower=1e-12)
        if (rel > price_tolerance).any():
            return {"status": "FAIL", "reason": f"Trade {col} mismatch beyond tolerance"}
    return {"status": "PASS", "reason": "Canonical trade timestamps, sides and prices match"}

def test_status_matrix_fail_closed():
    """
    Ensures that without explicit real TV evidence, the matrix strictly
    reports TV_COMPILE_UNVERIFIED and TV_RUN_UNVERIFIED.
    """
    scripts = get_pine_scripts()
    assert len(scripts) > 0, "No pine scripts found"

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    evidence_dir = os.path.join(base_dir, "tests", "tv_evidence")

    matrix = []

    for script in scripts:
        meta = extract_pine_metadata(script)
        script_name = meta["filename"]

        # Check for compile proof
        compile_proof_path = os.path.join(evidence_dir, script_name.replace(".pine", "_compile.json"))
        run_proof_path = os.path.join(evidence_dir, script_name.replace(".pine", "_run.csv"))

        compile_status = "PASS" if os.path.exists(compile_proof_path) else "TV_COMPILE_UNVERIFIED"
        run_status = "PASS" if os.path.exists(run_proof_path) else "TV_RUN_UNVERIFIED"

        matrix.append({
            "script": script_name,
            "compile": compile_status,
            "run": run_status,
            "overall": "UNVERIFIED" if compile_status == "TV_COMPILE_UNVERIFIED" or run_status == "TV_RUN_UNVERIFIED" else "VERIFIED"
        })

        if not os.path.exists(compile_proof_path):
            assert compile_status == "TV_COMPILE_UNVERIFIED", f"{script_name} claimed compile pass without evidence"
        if not os.path.exists(run_proof_path):
            assert run_status == "TV_RUN_UNVERIFIED", f"{script_name} claimed run pass without evidence"

    df = pd.DataFrame(matrix)

    for index, row in df.iterrows():
        script_name = row['script']
        compile_proof_path = os.path.join(evidence_dir, script_name.replace(".pine", "_compile.json"))
        run_proof_path = os.path.join(evidence_dir, script_name.replace(".pine", "_run.csv"))
        if not os.path.exists(compile_proof_path) or not os.path.exists(run_proof_path):
            assert row['overall'] == 'UNVERIFIED', f"{script_name} permitted verified status without evidence"

@pytest.mark.parametrize("pine_script", get_pine_scripts())
def test_pine_script_v6_syntax(pine_script):
    """
    Statically checks that the Pine Script file claims version 6 and has no
    obvious syntax errors.
    """
    meta = extract_pine_metadata(pine_script)
    assert meta["version"] == 6, f"{pine_script} does not claim //@version=6"
    assert meta["strategy_name"] is not None, f"{pine_script} does not have a valid strategy() call"

def test_spec_pending_strategies_have_no_executable_logic():
    """
    Ensures that scripts marked as SPEC_PENDING do not contain active,
    invented trading logic (strategy.entry, strategy.close, etc.).
    """
    scripts = get_pine_scripts()
    for script in scripts:
        with open(script, "r", encoding="utf-8") as f:
            lines = f.readlines()

        is_spec_pending = any("SPEC_PENDING" in line for line in lines)
        if is_spec_pending:
            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("//"):
                    continue
                # Reject uncommented strategy.entry, strategy.close, strategy.exit, strategy.order
                match = re.search(r'\bstrategy\.(entry|close|exit|order)\b', stripped)
                assert not match, (
                    f"Executable logic found in SPEC_PENDING file {os.path.basename(script)} "
                    f"at line {line_num}: {stripped}"
                )

def test_compare_logs_rejects_equal_count_different_prices(tmp_path):
    rows = [{"entry_time": "2025-01-01T00:00:00Z", "exit_time": "2025-01-02T00:00:00Z",
             "entry_price": 100.0, "exit_price": 105.0, "side": "long"}]
    py_path, tv_path = tmp_path / "python.csv", tmp_path / "tv.csv"
    pd.DataFrame(rows).to_csv(py_path, index=False)
    pd.DataFrame([{**rows[0], "exit_price": 120.0}]).to_csv(tv_path, index=False)
    assert compare_logs(py_path, tv_path)["status"] == "FAIL"


def test_compare_logs_rejects_equal_count_different_timestamps(tmp_path):
    rows = [{"entry_time": "2025-01-01T00:00:00Z", "exit_time": "2025-01-02T00:00:00Z",
             "entry_price": 100.0, "exit_price": 105.0, "side": "long"}]
    py_path, tv_path = tmp_path / "python.csv", tmp_path / "tv.csv"
    pd.DataFrame(rows).to_csv(py_path, index=False)
    pd.DataFrame([{**rows[0], "entry_time": "2025-01-01T01:00:00Z"}]).to_csv(tv_path, index=False)
    assert compare_logs(py_path, tv_path)["status"] == "FAIL"


def test_compare_logs_fails_closed_on_missing_fields(tmp_path):
    py_path, tv_path = tmp_path / "python.csv", tmp_path / "tv.csv"
    pd.DataFrame({"pnl": [1.0]}).to_csv(py_path, index=False)
    pd.DataFrame({"pnl": [1.0]}).to_csv(tv_path, index=False)
    assert compare_logs(py_path, tv_path)["status"] == "UNVERIFIED"


def test_compare_logs_accepts_identical_canonical_trades(tmp_path):
    row = {"entry_time": "2025-01-01T00:00:00Z", "exit_time": "2025-01-02T00:00:00Z",
           "entry_price": 100.0, "exit_price": 105.0, "side": "long"}
    py_path, tv_path = tmp_path / "python.csv", tmp_path / "tv.csv"
    pd.DataFrame([row]).to_csv(py_path, index=False)
    pd.DataFrame([row]).to_csv(tv_path, index=False)
    assert compare_logs(py_path, tv_path)["status"] == "PASS"
