#!/usr/bin/env python3
"""Run one unchanged frozen entry point once, in a newly created empty cwd."""
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
parser.add_argument("program", choices=["main", "independent"])
args = parser.parse_args()
ROOT = Path(__file__).resolve().parent
filename = {"main": "uniform_random_moment_reset.py",
            "independent": "uniform_random_reset_independent.py"}[args.program]
source = ROOT / "original" / filename
run_dir = ROOT / "runs" / (args.program + "-001")
run_dir.mkdir(parents=True, exist_ok=False)
started = datetime.now(timezone.utc).isoformat()
clock = time.monotonic()
command = [sys.executable, str(source)]
with (run_dir / "stdout.json").open("xb") as stdout, (run_dir / "stderr.txt").open("xb") as stderr:
    result = subprocess.run(command, cwd=run_dir, stdout=stdout, stderr=stderr)
metadata = {"command": command, "cwd": str(run_dir), "started_utc": started,
            "duration_seconds": time.monotonic() - clock,
            "exit_code": result.returncode, "python": platform.python_version(),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "input_contract": "No external files or CLI arguments; unchanged default deterministic parameter loops.",
            "runs_of_this_entry_point_in_this_batch": 1,
            "stdout_sha256": hashlib.sha256((run_dir / "stdout.json").read_bytes()).hexdigest(),
            "stderr_bytes": (run_dir / "stderr.txt").stat().st_size}
if result.returncode == 0:
    output = json.loads((run_dir / "stdout.json").read_text())
    metadata["output_source_hash_matches"] = output["source_sha256"] == metadata["source_sha256"]
(run_dir / "run.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(metadata, ensure_ascii=False))
raise SystemExit(result.returncode)
