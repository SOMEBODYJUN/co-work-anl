"""Run the unmodified frozen parent enumerator once in a disposable copy.

The persistent output directory is created exclusively before execution, so
an accidental second invocation does not overwrite this execution record.
The large author inputs remain preserved only in the sibling report package.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time


BASE = Path(__file__).resolve().parent
REPORT_BASE = BASE.parent / "full156-tail-parent-report"
SOURCE = BASE / "original/audit_full156_reply_set.py"
ORIGINAL_REPORT = REPORT_BASE / "original/audit_full156_reply_set.json"
INPUTS = {
    "combined_branch_master_exact.json": (816453, "d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8"),
    "full156_tail2_kernel_10344.json": (3395493, "876f063e9e88679c8803011775b04a4b707b8b586dfd3a840fd056f9ddcef3d4"),
    "full156_tail2_welfare_10344.json": (1685067, "fe8fb09f7527f8f4cd26ad67f6e43be5bc84cb5d9c47fea39fd0661bab0e5256"),
}


def fingerprint(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data).hexdigest()}


def main():
    assert fingerprint(SOURCE) == {"bytes": 3920, "sha256": "6818a46135139c032f7a399ac9a75be908e0f921728f89a5887777375efd575d"}
    original_report_fingerprint = fingerprint(ORIGINAL_REPORT)
    assert original_report_fingerprint == {"bytes": 1349, "sha256": "99d94577b978d76a618781ba5274fee0297ccdeef087e90fba5d6ef52f827415"}
    dependencies = []
    for filename, (size, digest) in INPUTS.items():
        path = REPORT_BASE / "original/research_5" / filename
        assert fingerprint(path) == {"bytes": size, "sha256": digest}
        dependencies.append({"path": str(path), **fingerprint(path)})
    output = BASE / "rerun"
    output.mkdir(exist_ok=False)
    start_utc = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="full156-execution-", dir=BASE) as temporary:
        temp_root = Path(temporary)
        temp_source = temp_root / SOURCE.name
        shutil.copyfile(SOURCE, temp_source)
        (temp_root / "research_5").mkdir()
        for filename in INPUTS:
            shutil.copyfile(REPORT_BASE / "original/research_5" / filename, temp_root / "research_5" / filename)
        assert fingerprint(temp_source) == fingerprint(SOURCE)
        command = [sys.executable, "-B", str(temp_source)]
        env = os.environ.copy()
        env.pop("PYTHONOPTIMIZE", None)
        completed = subprocess.run(command, cwd=temp_root, env=env, capture_output=True, timeout=60)
        elapsed = time.perf_counter() - start
        (output / "stdout.txt").write_bytes(completed.stdout)
        (output / "stderr.txt").write_bytes(completed.stderr)
        generated = temp_root / "audit_full156_reply_set.json"
        if generated.exists():
            shutil.copyfile(generated, output / generated.name)
        record = {
            "kind": "one new run of unmodified frozen entrypoint",
            "source_execution_count_this_invocation": 1,
            "source": {"path": str(SOURCE), **fingerprint(SOURCE)},
            "dependency_files": dependencies,
            "python": platform.python_version(), "python_executable": sys.executable,
            "python_bytecode_disabled": True, "assertions_enabled": True,
            "third_party_dependencies": [], "local_program_imports": [],
            "argv": command, "cwd": str(temp_root),
            "start_utc": start_utc, "end_utc": datetime.now(timezone.utc).isoformat(),
            "wall_seconds": elapsed, "exit_code": completed.returncode,
            "stdout": fingerprint(output / "stdout.txt"), "stderr": fingerprint(output / "stderr.txt"),
            "source_original_unchanged": fingerprint(SOURCE)["sha256"] == "6818a46135139c032f7a399ac9a75be908e0f921728f89a5887777375efd575d",
            "frozen_original_report_unchanged": fingerprint(ORIGINAL_REPORT) == original_report_fingerprint,
            "original_optimizers_or_kernel_generator_executed": False,
            "large_dependencies_persisted_in_this_package": False,
        }
        if generated.exists():
            record["generated_report"] = fingerprint(generated)
            record["generated_report_byte_equal_frozen"] = generated.read_bytes() == ORIGINAL_REPORT.read_bytes()
            record["stdout_byte_equal_generated_report"] = completed.stdout == generated.read_bytes()
            record["generated_report_field_equal_frozen"] = json.loads(generated.read_text()) == json.loads(ORIGINAL_REPORT.read_text())
        for dep in dependencies:
            assert fingerprint(Path(dep["path"])) == {"bytes": dep["bytes"], "sha256": dep["sha256"]}
    record["temporary_execution_directory_removed"] = not temp_root.exists()
    (output / "execution.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    assert completed.returncode == 0
    assert record["generated_report_byte_equal_frozen"]
    assert not completed.stderr
    print(json.dumps({key: record[key] for key in (
        "exit_code", "wall_seconds", "generated_report", "generated_report_byte_equal_frozen",
        "stdout_byte_equal_generated_report", "temporary_execution_directory_removed")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
