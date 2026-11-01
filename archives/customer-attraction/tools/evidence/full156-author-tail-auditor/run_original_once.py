"""Run the original author audit exactly once in a disposable source layout."""
from pathlib import Path
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = HERE / "original/audit_full156_tail2.py"
KERNEL = HERE.parent / "full156-tail-parent-report/original/research_5/full156_tail2_kernel_10344.json"
SOURCE_SHA = "502ef5a8b2d9cff8b716dde6a8390e9c20c34838445f60ede7605cd1a2ae7fef"
KERNEL_SHA = "876f063e9e88679c8803011775b04a4b707b8b586dfd3a840fd056f9ddcef3d4"
REPORT_SHA = "a672c54c26423614174be07846777db983e2e5f7c9dcc853a26b12d776ec253d"

def fingerprint(path):
    raw = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def main():
    before = [fingerprint(SOURCE), fingerprint(KERNEL)]
    assert [d["sha256"] for d in before] == [SOURCE_SHA, KERNEL_SHA]
    out = HERE / "rerun"
    # Never overwrite the original report or an earlier execution record.
    out.mkdir(exist_ok=False)
    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="isolated-author-", dir=HERE) as scratch:
        base = Path(scratch)
        r1, r5 = base / "research_1", base / "research_5"
        r1.mkdir(); r5.mkdir()
        script = r1 / SOURCE.name
        shutil.copyfile(SOURCE, script)
        shutil.copyfile(KERNEL, r5 / KERNEL.name)
        argv = [sys.executable, "-I", "-B", str(script)]
        execution = subprocess.run(argv, cwd=base, capture_output=True, check=False)
        (out / "stdout.txt").write_bytes(execution.stdout)
        (out / "stderr.txt").write_bytes(execution.stderr)
        produced = r1 / "full156_tail2_exact_audit.json"
        report_bytes = produced.read_bytes() if produced.exists() else b""
        if produced.exists():
            (out / produced.name).write_bytes(report_bytes)
        temporary_layout = str(base)
    after = [fingerprint(SOURCE), fingerprint(KERNEL)]
    record = {"status": "local-prepared", "python": platform.python_version(), "argv": argv,
              "cwd": temporary_layout, "temporary_layout_removed": not Path(temporary_layout).exists(),
              "elapsed_seconds": time.perf_counter() - start, "returncode": execution.returncode,
              "original_entry_invocations": 1, "source_and_dependency_before": before,
              "source_and_dependency_after": after, "inputs_unchanged": before == after,
              "stdout_bytes": len(execution.stdout), "stdout_sha256": hashlib.sha256(execution.stdout).hexdigest(),
              "stderr_bytes": len(execution.stderr), "report_bytes": len(report_bytes),
              "report_sha256": hashlib.sha256(report_bytes).hexdigest(), "expected_report_sha256": REPORT_SHA,
              "byte_equal_to_frozen_report": hashlib.sha256(report_bytes).hexdigest() == REPORT_SHA,
              "scope": "One unchanged original author audit, reading only the frozen author kernel. No kernel/customer generation, parent audit, welfare generation or six-player tree execution."}
    (out / "execution.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    assert execution.returncode == 0 and not execution.stderr
    assert before == after and record["temporary_layout_removed"]
    assert execution.stdout == report_bytes and record["byte_equal_to_frozen_report"]
    json.loads(report_bytes)
    print(json.dumps({k: record[k] for k in ("status", "returncode", "report_bytes", "report_sha256", "byte_equal_to_frozen_report", "inputs_unchanged")}, ensure_ascii=False))

if __name__ == "__main__":
    main()
