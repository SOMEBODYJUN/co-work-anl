#!/usr/bin/env python3
"""Copy the exact original and its real adjacent input, then run the entry point.

No mathematical code is injected, imported, patched, or replaced.  This wrapper
captures stdout and binds it to the frozen report and both exact source hashes.
"""
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
FILES = {
    "audit_threefold.py": "0b336908e52a26d5785ef048a9d80c6f79e0bad59f9c4bbf40d4f8c681da8b7e",
    "research_1/threefold_penultimate_exact.json": "7adcce9a18beb2654c5fe1a4ef5dc45d8d130e8426f81928243cedd6ea75d35a",
}
REPORT_SHA = "6b3ff9871170e1179e8d3df35c5e042788d33791541f82e803804faa88889783"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    if sys.flags.optimize:
        raise RuntimeError("Certification requires Python assertions enabled.")
    output = HERE / "rerun"
    execution_root = output / "isolated"
    for rel, expected in FILES.items():
        source, target = HERE / "original" / rel, execution_root / rel
        if digest(source) != expected:
            raise RuntimeError("Frozen input hash mismatch: " + rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if digest(target) != expected:
            raise RuntimeError("Execution copy mismatch: " + rel)
    frozen_report = HERE / "related/audit_threefold.json"
    if digest(frozen_report) != REPORT_SHA:
        raise RuntimeError("Frozen reference report hash mismatch")
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    result = subprocess.run(
        [sys.executable, "-B", str(execution_root / "audit_threefold.py")],
        cwd=execution_root, env=env, capture_output=True, check=False,
    )
    (output / "audit_threefold.json").write_bytes(result.stdout)
    (output / "stderr.txt").write_bytes(result.stderr)
    if result.returncode:
        raise RuntimeError("Original entry point failed; see captured stderr")
    observed = json.loads(result.stdout)
    reference = json.loads(frozen_report.read_bytes())
    exact_input = json.loads((HERE / "original/research_1/threefold_penultimate_exact.json").read_bytes())
    checks = {
        "unmodified_source_and_dependency_before_and_after": all(
            digest(HERE / "original" / rel) == expected
            and digest(execution_root / rel) == expected
            for rel, expected in FILES.items()
        ),
        "full_report_byte_equal_to_frozen": result.stdout == frozen_report.read_bytes(),
        "full_report_json_equal_to_frozen": observed == reference,
        "rho_all_64_entries_equal_to_author": observed["rho_actual_membership"] == exact_input["rho_actual_membership"],
        "actual_membership_domain_complete": set(observed["rho_actual_membership"]) == {format(i, "06b") for i in range(64)},
        "conditional_counts_2058_3528": (observed["reduced_state_count"], observed["state_count_with_overlap"]) == (2058, 3528),
        "restricted_minimum_zero": observed["minimum_residual"] == "0",
    }
    if not all(checks.values()):
        raise RuntimeError("Replay/reference validation failed: " + str(checks))
    run_report = {
        "status": "actual_unmodified_original_entry_point_passed",
        "python_version": platform.python_version(),
        "execution": "separate unoptimized Python process, -B; isolated cwd; exact adjacent research_1 input; stdout captured",
        "return_code": result.returncode,
        "source_sha256": FILES["audit_threefold.py"],
        "dependency_sha256": FILES["research_1/threefold_penultimate_exact.json"],
        "frozen_report_sha256": REPORT_SHA,
        "stdout_sha256": sha256(result.stdout).hexdigest(),
        "stdout_size": len(result.stdout),
        "stderr_size": len(result.stderr),
        "checks": checks,
        "reported_scope": observed["scope"],
        "source_input_fields_actually_compared": ["rho_actual_membership", "complete_restricted_state_count"],
        "not_certified": "arbitrary six-player half, P2, external review, historical run environment, author JSON fields not read by original code",
    }
    (output / "run_report.json").write_text(json.dumps(run_report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(run_report, ensure_ascii=False))


if __name__ == "__main__":
    main()
