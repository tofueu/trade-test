import os
import glob
import pandas as pd
from test_pine_equivalence import extract_pine_metadata, compare_logs

def get_pine_scripts():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    pine_dir = os.path.join(base_dir, "pine")
    return sorted(glob.glob(os.path.join(pine_dir, "*.pine")))

def build_matrix():
    scripts = get_pine_scripts()
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    evidence_dir = os.path.join(base_dir, "tests", "tv_evidence")

    matrix = []

    for script in scripts:
        meta = extract_pine_metadata(script)
        script_name = meta["filename"]

        compile_proof_path = os.path.join(evidence_dir, script_name.replace(".pine", "_compile.json"))
        run_proof_path = os.path.join(evidence_dir, script_name.replace(".pine", "_run.csv"))
        python_log_path = os.path.join(base_dir, "src", script_name.replace(".pine", "_python_run.csv"))

        # Determine compile status
        compile_status = "PASS" if os.path.exists(compile_proof_path) else "TV_COMPILE_UNVERIFIED"

        # Determine run status
        run_status = "TV_RUN_UNVERIFIED"
        parity_status = "N/A"
        match_reason = "No evidence"

        if os.path.exists(run_proof_path):
            run_status = "PASS"
            # Try to compare logs if both exist
            if os.path.exists(python_log_path):
                parity_result = compare_logs(python_log_path, run_proof_path)
                parity_status = parity_result["status"]
                match_reason = parity_result["reason"]
            else:
                parity_status = "UNVERIFIED"
                match_reason = "Missing python log"

        overall = "UNVERIFIED" if compile_status == "TV_COMPILE_UNVERIFIED" or run_status == "TV_RUN_UNVERIFIED" or parity_status != "PASS" else "VERIFIED"

        matrix.append({
            "Script Name": f"`{script_name}`",
            "Compilation": compile_status,
            "Run Status": run_status,
            "Parity (Strict)": parity_status,
            "Overall Status": overall,
            "Notes": match_reason
        })

    df = pd.DataFrame(matrix)

    # Generate markdown
    md = "# Pine Script Validation Matrix\n\n"
    md += "This matrix validates the equivalence of Python backtests and TradingView Pine scripts.\n"
    md += "It strictly requires offline parity vs real TradingView run evidence (`tv_evidence`).\n"
    md += "If real TradingView credentials/interactions are needed but absent, scripts remain UNVERIFIED.\n\n"
    md += df.to_markdown(index=False)

    output_path = os.path.join(base_dir, "VALIDATION_MATRIX.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Validation matrix written to {output_path}")

if __name__ == "__main__":
    build_matrix()
