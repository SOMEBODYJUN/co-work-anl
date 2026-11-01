"""Materialize the unchanged early-B exporter in its original path layout.

Usage: python3 run_original_once.py /absolute/new-empty-runtime
The shared old 5108-row point is copied, not re-solved or re-verified here.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import time
import shutil

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
PREFIX = Path("research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1")
POINT_REL = PREFIX / "research_5/combined_branch_master_exact.json"
POINT_STORED = REPO / "archives/customer-attraction/tools/evidence/full156-tail-parent-report/original/research_5/combined_branch_master_exact.json"
CODE = HERE / "original/b724ae73630ef1019a70/early_B_projections.py"
CERT = HERE / "original/519adddb8a5e5058acc5/early_B_projection_certificate.json"
EXPECTED_POINT = "d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    runtime = Path(sys.argv[1]).resolve()
    runtime.mkdir(parents=True, exist_ok=False)
    assert digest(POINT_STORED) == EXPECTED_POINT
    code_path = runtime / PREFIX / "research_2/early_B_projections.py"
    point_path = runtime / POINT_REL
    code_path.parent.mkdir(parents=True)
    point_path.parent.mkdir(parents=True)
    shutil.copyfile(CODE, code_path)
    shutil.copyfile(POINT_STORED, point_path)
    before = {str(p): digest(p) for p in (CODE, CERT, POINT_STORED, code_path, point_path)}
    runs = HERE / "runs"
    runs.mkdir(exist_ok=True)
    argv = [sys.executable, "-I", "-B", str(code_path), "--export"]
    start_utc = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    result = subprocess.run(argv, cwd=runtime, input=b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elapsed = time.monotonic() - start
    (runs / "original.stdout").write_bytes(result.stdout)
    (runs / "original.stderr").write_bytes(result.stderr)
    assert result.returncode == 0 and not result.stderr
    exported = code_path.with_name("early_B_projection_certificate.json")
    shutil.copyfile(exported, runs / "generated-certificate.json")
    assert exported.read_bytes() == CERT.read_bytes()
    after = {str(p): digest(p) for p in (CODE, CERT, POINT_STORED, code_path, point_path)}
    assert before == after
    record = {
        "start_utc": start_utc, "argv": argv, "cwd": str(runtime),
        "elapsed_seconds": elapsed, "exit_code": result.returncode,
        "stdout_bytes": len(result.stdout), "stderr_bytes": len(result.stderr),
        "source_and_input_sha256_before": before,
        "source_and_input_sha256_after": after,
        "exported_bytes": exported.stat().st_size, "exported_sha256": digest(exported),
        "export_byte_equal_to_frozen_certificate": True,
        "original_math_entry_executions": 1,
        "float_lp_executions": 0,
        "scope": "original standard-library full-table export and three values on the shared selected old point",
    }
    (runs / "original-execution.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
