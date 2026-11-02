"""Run the frozen author entry point and compare its complete original output.

This wrapper contains no mathematical coefficient implementation. It executes
source.py in an unoptimized child and checks all output fields and bytes.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source.py"
ROOT = next(p for p in HERE.parents
            if (p / "AGENTS.md").is_file() and (p / "archives/customer-attraction").is_dir())
EXPECTED = ROOT / "archives/customer-attraction/tools/evidence/threefold-early-auditor/original/research_1/threefold_penultimate_exact.json"
OUTPUT = HERE / "threefold_penultimate_exact.json"
SOURCE_SHA = "7cb092bb5ffbdb20c8a3398b436d6ca19ce788f74c3ad2e5f06730052d81b285"
EXPECTED_SHA = "7adcce9a18beb2654c5fe1a4ef5dc45d8d130e8426f81928243cedd6ea75d35a"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if sys.flags.optimize:
        raise RuntimeError("Run without -O/-OO: source assertions must be enabled.")
    if sha(SOURCE) != SOURCE_SHA or sha(EXPECTED) != EXPECTED_SHA:
        raise RuntimeError("Frozen source/input hash mismatch.")
    source_before = SOURCE.read_bytes()
    expected_before = EXPECTED.read_bytes()
    env = dict(os.environ)
    env.pop("PYTHONOPTIMIZE", None)
    completed = subprocess.run(
        [sys.executable, str(SOURCE)], cwd=HERE, env=env,
        capture_output=True, timeout=30, check=True,
    )
    (HERE / "original_stdout.json").write_bytes(completed.stdout)
    (HERE / "original_stderr.txt").write_bytes(completed.stderr)
    generated = json.loads(OUTPUT.read_bytes())
    expected = json.loads(expected_before)
    stdout = json.loads(completed.stdout)
    expected_stdout = {key: value for key, value in generated.items()
                       if key != "rho_actual_membership"}
    if OUTPUT.read_bytes() != expected_before:
        raise RuntimeError("Original author output is not byte-identical to frozen JSON.")
    if generated != expected or stdout != expected_stdout or completed.stderr:
        raise RuntimeError("Complete output, stdout projection, or stderr check failed.")
    if SOURCE.read_bytes() != source_before or EXPECTED.read_bytes() != expected_before:
        raise RuntimeError("Source or frozen comparator changed during replay.")
    record = {
        "status": "PASS_ORIGINAL_AUTHOR_ENTRY_POINT_REPLAY",
        "scope": "All ten frozen report fields and exact output bytes; no new coefficient implementation, game enumeration, SPE inference, or external review.",
        "python_version": sys.version,
        "command": [sys.executable, "source.py"],
        "child_pythonoptimize_environment_removed": True,
        "exit_code": completed.returncode,
        "source_sha256": sha(SOURCE),
        "source_size": len(source_before),
        "comparator_repository_path": str(EXPECTED.relative_to(ROOT)),
        "comparator_sha256": sha(EXPECTED),
        "generated_json_sha256": sha(OUTPUT),
        "generated_json_size": OUTPUT.stat().st_size,
        "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        "stdout_size": len(completed.stdout),
        "stderr_size": len(completed.stderr),
        "byte_identical_to_frozen_author_json": True,
        "all_ten_report_fields_equal": True,
        "report_fields_compared": list(expected),
        "stdout_fields": list(stdout),
        "rho_table_keys": len(generated["rho_actual_membership"]),
        "source_and_comparator_unchanged": True,
        "report_without_rho": stdout,
        "wrapper_sha256": sha(Path(__file__)),
    }
    (HERE / "run_report.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({key: value for key, value in record.items()
                      if key in ("status", "exit_code", "generated_json_size", "stdout_size", "stderr_size",
                                 "byte_identical_to_frozen_author_json", "all_ten_report_fields_equal")}, indent=2))


if __name__ == "__main__":
    main()
