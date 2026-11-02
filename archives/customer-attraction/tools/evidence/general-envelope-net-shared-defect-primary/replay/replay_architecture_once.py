"""Run exactly the preserved architecture entry once and bind its report.

No added mathematical search.  The frozen report has provenance fields that
are not printed by main; compare its mathematical output as a strict subset.
"""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys
import time


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    base = Path(__file__).resolve().parents[1]
    originals = base / "original"
    code = originals / "58e03e79ee88a9622740" / "audit_architecture.py"
    report = originals / "6f390bdf3e3c31d1bc62" / "audit_architecture_result.json"
    output = base / "replay" / "original-main-001"
    output.mkdir(parents=True, exist_ok=True)
    before = sha(code)
    assert before == "1b18bc2209ada987e1509cec159a1ede92a7b82f4a401f5bc03e628e70e07e55"
    argv = [sys.executable, str(code)]
    start_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    start = time.perf_counter()
    run = subprocess.run(argv, cwd=base, capture_output=True, check=False)
    seconds = time.perf_counter() - start
    (output / "stdout.txt").write_bytes(run.stdout)
    (output / "stderr.txt").write_bytes(run.stderr)
    after = sha(code)
    assert run.returncode == 0 and before == after
    actual = json.loads(run.stdout)
    frozen = json.loads(report.read_bytes())
    assert all(frozen[k] == value for k, value in actual.items())
    bindings = {}
    for filename, digest in frozen["source_sha256"].items():
        matches = list(originals.glob("*/" + filename))
        assert len(matches) == 1
        bindings[filename] = {"actual_sha256": sha(matches[0]), "frozen_sha256": digest}
        assert sha(matches[0]) == digest
    event = {
        "status": "passed", "run_count": 1, "start_utc": start_utc,
        "argv": argv, "cwd": str(base), "elapsed_seconds": seconds,
        "exit_code": run.returncode, "python_version": platform.python_version(),
        "source_pre_sha256": before, "source_post_sha256": after,
        "stdout_sha256": hashlib.sha256(run.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(run.stderr).hexdigest(),
        "stdout_size": len(run.stdout), "stderr_size": len(run.stderr),
        "frozen_report_sha256": sha(report),
        "printed_fields": list(actual),
        "all_printed_fields_equal_frozen_report": True,
        "frozen_only_fields": sorted(set(frozen) - set(actual)),
        "source_bindings": bindings,
        "actual_execution_scope": {
            "farkas_check_calls": 116,
            "recurrence_identity_calls": 114,
            "all_big_n_3_to_40_count_cases": actual["all_big_history_count_cases"],
            "additional_n2_count_cases_not_in_printed_total": 3,
            "projection_corner_cases": actual["projection_corner_cases"],
            "shared_defect_algebra_cases": actual["shared_defect_algebra_cases"],
            "LP_calls": 0, "general_SPE_enumeration_calls": 0,
            "new_instance_or_parameter_scan_outside_original_main": 0
        },
        "limits": [
            "count cases are sufficient compressed parameters, not 123405 ordered histories",
            "projection corners and scalar data need not be SPE realizable",
            "frozen metadata python_version/command are historical fields, not native stdout",
            "universal results rely on analytic proofs, not these finite regressions"
        ]
    }
    (output / "execution.json").write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": event["status"], "seconds": seconds,
                      "stdout_size": len(run.stdout), "matched_fields": len(actual)}, indent=2))


if __name__ == "__main__":
    main()
