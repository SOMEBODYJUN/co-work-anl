#!/usr/bin/env python3
"""Run the preserved price corollary once in a fresh, self-contained tree.

The original script overwrites a sibling JSON. This wrapper only runs a copy
inside a temporary tree and writes the new evidence to an exclusively created
output directory. It never overwrites frozen sources or calls an optimizer.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
SOURCE = Path("research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/credible2/protected_price_boundary.py")
REPORT = SOURCE.with_suffix(".json")


def run(out):
    manifest = json.loads((HERE / "PROVENANCE.json").read_text(encoding="utf-8"))
    for entry in manifest["entries"]:
        data = (HERE / entry["saved_path"]).read_bytes()
        if sha256(data).hexdigest() != entry["sha256"] or len(data) != entry["size"]:
            raise ValueError("Frozen source mismatch: " + entry["path"])
    out.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="price-boundary-", dir=out) as name:
        stage = Path(name).resolve()
        shutil.copytree(HERE / "dependencies/customer_attraction", stage / "customer_attraction")
        script = stage / SOURCE
        script.parent.mkdir(parents=True)
        shutil.copyfile(HERE / "original" / SOURCE, script)
        command = [sys.executable, "-E", "-B", str(script)]
        start = time.monotonic()
        result = subprocess.run(command, cwd=stage, capture_output=True)
        elapsed = time.monotonic() - start
        (out / "stdout.txt").write_bytes(result.stdout)
        (out / "stderr.txt").write_bytes(result.stderr)
        if result.returncode:
            raise RuntimeError("Preserved script failed; inspect stderr.txt")
        produced = (stage / REPORT).read_bytes()
        frozen = (HERE / "original" / REPORT).read_bytes()
        (out / "protected_price_boundary.json").write_bytes(produced)
        record = {
            "python": platform.python_version(),
            "command": command,
            "cwd": str(stage),
            "temporary_execution_tree_removed_after_capture": True,
            "execution_count": 1,
            "source_code_modified": False,
            "assertions_enabled": True,
            "exit_code": result.returncode,
            "elapsed_seconds": elapsed,
            "stderr_bytes": len(result.stderr),
            "original_script_overwrite_confined_to_fresh_temporary_tree": True,
            "frozen_report_sha256": sha256(frozen).hexdigest(),
            "new_report_sha256": sha256(produced).hexdigest(),
            "whole_report_bytes_equal": produced == frozen,
            "whole_report_json_equal": json.loads(produced) == json.loads(frozen),
            "stdout_equals_new_report_bytes": result.stdout == produced,
            "excluded_report_fields": [],
            "runtime_dependency_sha256": {entry["path"]: entry["sha256"] for entry in manifest["entries"]
                                          if entry["role"].startswith("previously-read-")},
            "original_source_sha256": next(entry["sha256"] for entry in manifest["entries"]
                                           if entry["path"] == str(SOURCE)),
        }
        (out / "replay-manifest.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if result.stderr or not record["whole_report_bytes_equal"] or not record["whole_report_json_equal"]:
            raise AssertionError("Replay mismatch; frozen sources were not altered")
        return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True, help="new evidence directory")
    args = parser.parse_args()
    print(json.dumps(run(args.out.resolve()), ensure_ascii=False, indent=2))
