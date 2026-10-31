#!/usr/bin/env python3
"""Capture each newly relevant finite checker once in a fresh empty directory."""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import platform
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("case", choices=["gap", "nonsymmetric_inline"])
args = parser.parse_args()
ROOT = Path(__file__).resolve().parent
source = (ROOT / "original/cotransversal_uniform_configuration_gap.py" if args.case == "gap"
          else ROOT / "derived/nonsymmetric_five_literal_check.py")
run_dir = ROOT / "runs" / (args.case + "-001")
run_dir.mkdir(parents=True, exist_ok=False)
command = [sys.executable, str(source)]
if args.case == "gap":
    command += ["--output", str(run_dir / "result.json")]
started = datetime.now(timezone.utc).isoformat()
clock = time.monotonic()
with (run_dir / "stdout.txt").open("xb") as stdout, (run_dir / "stderr.txt").open("xb") as stderr:
    result = subprocess.run(command, cwd=run_dir, stdout=stdout, stderr=stderr)
metadata = {"command": command, "cwd": str(run_dir), "started_utc": started,
            "duration_seconds": time.monotonic() - clock, "exit_code": result.returncode,
            "python": platform.python_version(), "python_optimization_level": sys.flags.optimize,
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "entry_point_runs_in_this_batch": 1,
            "stdout_bytes": (run_dir / "stdout.txt").stat().st_size,
            "stderr_bytes": (run_dir / "stderr.txt").stat().st_size,
            "input_contract": "No external input; frozen default D=3,4 with fresh output, or exact inline five-literal fixture.",
            "previous_reset_entry_points_reexecuted": False}
if args.case == "gap" and result.returncode == 0:
    raw = (run_dir / "result.json").read_bytes()
    metadata["result_sha256"] = hashlib.sha256(raw).hexdigest()
    metadata["result_source_hash_matches"] = json.loads(raw)["source_code_sha256"] == metadata["source_sha256"]
(run_dir / "run.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(metadata, ensure_ascii=False))
raise SystemExit(result.returncode)
