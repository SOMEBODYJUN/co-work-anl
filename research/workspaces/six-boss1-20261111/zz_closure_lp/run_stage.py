"""Run one reproducible stage, preserving complete stdout/stderr and exit data."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("solve", "recover", "verify", "separate"))
    args = parser.parse_args()
    entry = {"solve": HERE / "solve_full.py", "recover": HERE / "recover_full.py", "verify": HERE / "verify_certificates.py",
             "separate": HERE.parent / "common_coupling_math" / "audit_boolean.py"}[args.stage]
    command = [sys.executable, "-B", str(entry)]
    if args.stage == "separate":
        command.extend([str(HERE / "augmented_lp_exact.json"), "--matrix", str(HERE / "exact_matrix.json.gz"),
                        "--output", str(HERE / "zz-at-certified-point.json")])
    start = datetime.now(timezone.utc).isoformat()
    tick = time.monotonic()
    stdout_path, stderr_path = HERE / (args.stage + "_stdout.txt"), HERE / (args.stage + "_stderr.txt")
    assert not stdout_path.exists() and not stderr_path.exists(), "Preserve existing evidence; choose a fresh stage directory for reruns"
    with stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
        process = subprocess.run(command, cwd=HERE, stdout=stdout, stderr=stderr)
    record = {"stage": args.stage, "command": command, "cwd": str(HERE),
              "start_utc": start, "end_utc": datetime.now(timezone.utc).isoformat(),
              "seconds": time.monotonic()-tick, "exit_code": process.returncode,
              "entry_sha256": sha256(entry.read_bytes()).hexdigest(),
              "stdout": stdout_path.name, "stderr": stderr_path.name,
              "stdout_sha256": sha256(stdout_path.read_bytes()).hexdigest(),
              "stderr_sha256": sha256(stderr_path.read_bytes()).hexdigest()}
    records_path = HERE / "execution_records.json"
    records = json.loads(records_path.read_text()) if records_path.exists() else []
    records.append(record)
    records_path.write_text(json.dumps(records, indent=2)+"\n")
    print(json.dumps(record, indent=2), flush=True)
    print(stdout_path.read_text(), end="", flush=True)
    if stderr_path.stat().st_size:
        print(stderr_path.read_text(), end="", file=sys.stderr, flush=True)
    raise SystemExit(process.returncode)


if __name__ == "__main__":
    main()
