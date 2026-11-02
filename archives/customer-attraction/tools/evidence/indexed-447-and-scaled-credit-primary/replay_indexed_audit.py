#!/usr/bin/env python3
"""Run only the unchanged original 447-row fixed-input audit in a fresh tree.

No LP, recovery, random search, full-type pricing or canonical SPE solver runs.
The historical 437-row formulas are reused by the original audit; its ten new
rows use its own literal ordered-index construction. This is not an independent
second implementation of all 447 rows.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
AUTHOR = "research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466"
INPUTS = [
    AUTHOR + "/audit_indexed_closure.py",
    AUTHOR + "/credible_counterexample/frozen_support_closure.json",
    "evidence/certificates/customer_attraction/five_player_indexed_bound.json",
    "tests/audits/customer_attraction_five_indexed.py",
]


def fingerprint(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    tree = out / "runtime"
    before = {}
    for rel in INPUTS:
        source = HERE / "source-root" / rel
        target = tree / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        before[rel] = fingerprint(target)
    argv = [sys.executable, str(tree / INPUTS[0])]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tic = time.monotonic()
    call = subprocess.run(argv, cwd=tree, capture_output=True)
    elapsed = time.monotonic() - tic
    ended = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (out / "stdout.txt").write_bytes(call.stdout)
    (out / "stderr.txt").write_bytes(call.stderr)
    generated = tree / AUTHOR / "audit_indexed_closure.json"
    frozen = HERE / "source-root" / AUTHOR / "audit_indexed_closure.json"
    identical = generated.exists() and generated.read_bytes() == frozen.read_bytes()
    after = {rel: fingerprint(tree / rel) for rel in INPUTS}
    event = {
        "identity": "Boss3",
        "operation": "unchanged original fixed-input audit CLI exactly once",
        "argv": argv, "cwd": str(tree), "python": sys.version,
        "started_utc": started, "ended_utc": ended,
        "wall_seconds": elapsed, "exit_code": call.returncode,
        "stdout": fingerprint(out / "stdout.txt"),
        "stderr": fingerprint(out / "stderr.txt"),
        "inputs_before": before, "inputs_after": after,
        "inputs_unchanged": before == after,
        "original_report_byte_identical": identical,
        "original_audit_main_calls": 1,
        "original_LP_main_calls": 0,
        "scaled_credit_discovery_calls": 0,
        "full_type_pricing_calls": 0,
        "independent_447_row_matrix_claimed": False,
    }
    if generated.exists():
        event["generated_report"] = fingerprint(generated)
    (out / "execution-record.json").write_text(json.dumps(event, indent=2) + "\n")
    print(json.dumps({key: event[key] for key in (
        "exit_code", "wall_seconds", "inputs_unchanged",
        "original_report_byte_identical", "original_audit_main_calls"
    )}, indent=2))
    assert call.returncode == 0 and identical and before == after, "Actual failure evidence retained"


if __name__ == "__main__":
    main()
