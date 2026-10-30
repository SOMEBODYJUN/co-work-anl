"""Replay one frozen finite regression; never run the default discovery search."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time


BASE = Path(__file__).resolve().parent
AUDIT = (
    "research/workspaces/customer-attraction/"
    "R-ab183d14fb74403091d09db766b05f73/credible2/"
    "audit_full_tree_milp.py"
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compare(expected, actual, path=""):
    """Retain every numerical difference; reject a changed regression case."""
    differences = []
    if isinstance(expected, dict):
        assert isinstance(actual, dict) and expected.keys() == actual.keys(), path
        for key in expected:
            differences += compare(expected[key], actual[key], f"{path}/{key}")
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(expected) == len(actual), path
        for i, (left, right) in enumerate(zip(expected, actual)):
            differences += compare(left, right, f"{path}/{i}")
    elif path.endswith(("/brute_float", "/MIP_float")):
        assert abs(expected - actual) <= 2e-6, (path, expected, actual)
        if expected != actual or str(expected) != str(actual):
            differences.append(
                {"path": path, "frozen": expected, "replay": actual,
                 "absolute_difference": abs(expected - actual)}
            )
    else:
        assert expected == actual, (path, expected, actual)
    return differences


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    provenance = json.loads((BASE / "PROVENANCE.json").read_text())
    for entry in provenance["sources"]:
        data = (BASE / entry["retained_path"]).read_bytes()
        assert len(data) == entry["bytes"], entry["source_id"]
        assert sha(data) == entry["sha256"], entry["source_id"]
    frozen = BASE / "original/credible2/full_tree_milp_audit.json"
    expected = json.loads(frozen.read_text())
    with tempfile.TemporaryDirectory(prefix="full-history-audit-", dir=output.parent) as td:
        staged = Path(td)
        for entry in provenance["sources"]:
            if "stage_path" not in entry:
                continue
            target = staged / entry["stage_path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((BASE / entry["retained_path"]).read_bytes())
        start = time.monotonic()
        command = [sys.executable, "-E", "-B", AUDIT]
        process = subprocess.run(
            command, cwd=staged, capture_output=True, timeout=180
        )
        elapsed = time.monotonic() - start
        (output / "audit-stdout.json").write_bytes(process.stdout)
        (output / "audit-stderr.txt").write_bytes(process.stderr)
        assert process.returncode == 0, process.stderr.decode(errors="replace")
        actual_bytes = (staged / Path(AUDIT).with_name("full_tree_milp_audit.json")).read_bytes()
        (output / "full_tree_milp_audit.json").write_bytes(actual_bytes)
        actual = json.loads(actual_bytes)
        assert json.loads(process.stdout) == actual
    differences = compare(expected, actual)
    assert actual["passed"] is True
    groups = actual["results"]
    records = [record for group in groups for record in group["records"]]
    assert len(groups) == 8 and len(records) == 20
    assert sum(r["independent_LPs"] for r in records) == 680
    assert all(r["agreement"] for r in records)
    import numpy
    import scipy
    report = {
        "python": platform.python_version(),
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
        "reproducer_sha256": sha(Path(__file__).read_bytes()),
        "command": ["python3", "-E", "-B", AUDIT],
        "original_audit_executions": 1,
        "original_source_modified": False,
        "exit_code": process.returncode,
        "wall_seconds": elapsed,
        "source_hashes_checked": len(provenance["sources"]),
        "group_count": len(groups),
        "root_objective_records": len(records),
        "unique_ordered_policies_by_players": {"2": 4, "3": 64},
        "fixed_cone_query_LP_calls": 680,
        "joint_MIP_solve_calls": 20,
        "selected_cone_LP_calls": 20,
        "comparison_tolerance": 2e-6,
        "all_case_definitions_and_nonnumerical_fields_equal": True,
        "saved_report_bytes_equal": actual_bytes == frozen.read_bytes(),
        "frozen_report_sha256": sha(frozen.read_bytes()),
        "replay_report_sha256": sha(actual_bytes),
        "stdout_sha256": sha(process.stdout),
        "numerical_differences": differences,
        "maximum_replay_MIP_vs_fixed_cone_difference": max(
            abs(r["MIP_float"] - r["brute_float"]) for r in records
        ),
        "scope": (
            "Finite floating implementation regression sharing StrategyCone, "
            "payoff rows and solver. No exact union optimum certificate, "
            "independent author review, default discovery run or new search."
        ),
    }
    (output / "replay-manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
