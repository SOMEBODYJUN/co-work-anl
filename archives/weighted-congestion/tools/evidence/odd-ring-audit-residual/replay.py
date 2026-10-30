#!/usr/bin/env python3
"""Portable equivalent of the recorded four-source isolated replay.

This entry point is saved for reuse; the actual recorded run was performed by
recorded-execution.py. Do not rerun merely to duplicate already passed evidence.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROWS = [
    ("literal", "tests/audits/weighted_congestion/odd_ring/verify.py", [], "verification.json"),
    ("ring", "tests/audits/weighted_congestion/odd_ring_linear/verify_ring.py", ["--enumerate", "--output", "new-ring.json"], "new-ring.json"),
    ("attack", "tests/audits/weighted_congestion/odd_ring_linear/attack.py", ["--enumerate"], None),
    ("asymptotic", "tests/audits/weighted_congestion/odd_ring_linear_audit/audit_checks.py", [], "audit_checks.json"),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="new directory, must not exist")
    args = parser.parse_args()
    if sys.flags.optimize:
        parser.error("source assertions must be enabled")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)

    def run(row):
        name, relative, extra, report = row
        directory = output / name
        directory.mkdir()
        raw = (HERE / "original" / relative).read_bytes()
        code = directory / Path(relative).name
        code.write_bytes(raw)
        command = [sys.executable, str(code), *extra]
        completed = subprocess.run(command, cwd=directory, capture_output=True, text=True)
        (output / (name + "-stdout.txt")).write_text(completed.stdout)
        (output / (name + "-stderr.txt")).write_text(completed.stderr)
        record = {"name": name, "command": command, "exit_code": completed.returncode,
                  "source_sha256": hashlib.sha256(raw).hexdigest()}
        if completed.returncode == 0:
            payload = (directory / report).read_bytes() if report else completed.stdout.encode()
            json.loads(payload)
            (output / (name + ".json")).write_bytes(payload)
        return record

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        records = list(executor.map(run, ROWS))
    (output / "runs.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(records, ensure_ascii=False, indent=2))
    if any(record["exit_code"] for record in records):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
