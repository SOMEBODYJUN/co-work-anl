"""Restore an exact, explicitly one-fixture workspace for the three old probes.

This new staging helper is not a historical search driver. It never runs the
two floating-point LAST searches. --run-extra runs the original exact query
probe on the single archived coverage_opportunity_failure input.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
EXTRA = Path(
    "research/workspaces/customer-attraction/"
    "R-d1dc7a18aded4304a25a87486681fb21/exchange/"
    "actual_extra_candidate_probe.py"
)
FAILURE = EXTRA.with_name("actual_extra_candidate_failure.json")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--run-extra", action="store_true")
    args = parser.parse_args()
    if sys.flags.optimize:
        raise SystemExit("Use ordinary Python without -O or -OO.")
    destination = args.destination.resolve()
    if destination.exists():
        raise SystemExit("Destination must not already exist.")
    manifest = json.loads((BASE / "PROVENANCE.json").read_text())
    files: list[tuple[dict, bytes]] = []
    for record in manifest["frozen_entries"]:
        path = Path(record["path"])
        # Preserve the original relative imports and both probes' parents[5].
        # Frozen reports and prose are preserved at BASE, not execution input.
        if not (
            path.suffix == ".py"
            or str(path).startswith("examples/")
            or str(path).startswith("evidence/certificates/")
        ):
            continue
        raw = (BASE / "original" / path).read_bytes()
        if sha(raw) != record["sha256"]:
            raise SystemExit("Frozen-file hash mismatch: " + str(path))
        files.append((record, raw))
    destination.mkdir(parents=True, exist_ok=False)
    for record, raw in files:
        target = destination / record["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(raw)
    staged = {
        "purpose": "One archived input, full original relative program layout",
        "files": [
            {key: record[key] for key in ("id", "path", "sha256")}
            for record, _ in files
        ],
        "examples": [
            record["path"]
            for record, _ in files
            if record["path"].startswith("examples/")
        ],
        "not_a_historical_full_directory_reconstruction": True,
        "last_probe_main_functions_executed": False,
    }
    if args.run_extra:
        env = os.environ.copy()
        env.pop("PYTHONOPTIMIZE", None)
        env["PYTHONPATH"] = str(destination)
        command = [sys.executable, "-B", str(destination / EXTRA)]
        started = time.monotonic()
        result = subprocess.run(
            command, cwd=destination, env=env, capture_output=True, text=True
        )
        elapsed = time.monotonic() - started
        (destination / "extra_stdout.txt").write_text(result.stdout)
        (destination / "extra_stderr.txt").write_text(result.stderr)
        run = {
            "command": command,
            "cwd": str(destination),
            "python": platform.python_version(),
            "parent_optimize_flag": sys.flags.optimize,
            "child_pythonoptimize_removed": True,
            "returncode": result.returncode,
            "elapsed_seconds": elapsed,
            "run_count": 1,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        if result.returncode == 0 and (destination / FAILURE).is_file():
            actual = (destination / FAILURE).read_bytes()
            frozen = (BASE / "original" / FAILURE).read_bytes()
            run.update(
                {
                    "generated_report": str(FAILURE),
                    "generated_sha256": sha(actual),
                    "frozen_sha256": sha(frozen),
                    "byte_equal": actual == frozen,
                    "all_json_equal": json.loads(actual) == json.loads(frozen),
                }
            )
        staged["actual_extra_run"] = run
        (destination / "stage_manifest.json").write_text(
            json.dumps(staged, ensure_ascii=False, indent=2) + "\n"
        )
        if result.returncode:
            raise SystemExit(result.returncode)
        if "generated_report" not in run:
            raise SystemExit("The exact probe did not produce its expected report.")
    else:
        (destination / "stage_manifest.json").write_text(
            json.dumps(staged, ensure_ascii=False, indent=2) + "\n"
        )
    print(json.dumps(staged, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
