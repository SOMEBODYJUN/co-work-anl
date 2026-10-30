#!/usr/bin/env python3
"""Replay four unchanged Fraction audits without overwriting frozen evidence."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SPECS = (
    ("padding-author", "density_padding/verify.py", "density_padding/verification.json", True),
    ("padding-independent", "density_padding/independent_check.py", "density_padding/independent_verification.json", False),
    ("share-author", "high_degree_share/verify.py", "high_degree_share/verification.json", True),
    ("share-independent", "high_degree_share/check_independent.py", "high_degree_share/independent_verification.json", True),
)


def differences(old, new, prefix=""):
    if isinstance(old, dict) and isinstance(new, dict):
        result = []
        for key in sorted(old.keys() | new.keys()):
            path = f"{prefix}/{key}"
            if key not in old or key not in new:
                result.append({"path": path, "frozen": old.get(key), "replay": new.get(key)})
            else:
                result.extend(differences(old[key], new[key], path))
        return result
    if isinstance(old, list) and isinstance(new, list) and len(old) == len(new):
        return [d for i, (a, b) in enumerate(zip(old, new))
                for d in differences(a, b, f"{prefix}/{i}")]
    return [] if old == new else [{"path": prefix, "frozen": old, "replay": new}]


def run(spec):
    name, program, report, generate = spec
    source = ROOT / "original/tests/audits/weighted_congestion" / program
    frozen = ROOT / "original/evidence/runs/weighted_congestion" / report
    target = ROOT / "replay" / name
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="run-", dir=ROOT) as folder:
        workspace = Path(folder)
        shutil.copy2(source, workspace / source.name)
        command = [sys.executable, source.name]
        if generate:
            command += ["--generate", "verification.json"]
        completed = subprocess.run(command, cwd=workspace, text=True, capture_output=True)
        (target / "stdout.txt").write_text(completed.stdout)
        (target / "stderr.txt").write_text(completed.stderr)
        shutil.copy2(source, target / source.name)
        if completed.returncode:
            raise RuntimeError(f"{name} failed; inspect its stderr.txt")
        new = json.loads((workspace / "verification.json").read_text() if generate else completed.stdout)
        (target / "verification.json").write_text(json.dumps(new, ensure_ascii=False, indent=2) + "\n")
    diff = differences(json.loads(frozen.read_text()), new)
    return {"name": name, "command": command, "exit_code": completed.returncode,
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "differences": diff, "mathematical_fields_equal": all(d["path"] == "/python_version" for d in diff)}


def main():
    if not __debug__:
        raise RuntimeError("Do not run with -O; all source assertions must be enabled")
    manifest = json.loads((ROOT / "provenance.json").read_text())
    for entry in manifest["sources"]:
        source = ROOT / "original" / entry["path"]
        assert hashlib.sha256(source.read_bytes()).hexdigest() == entry["sha256"], entry["path"]
    with ThreadPoolExecutor(max_workers=4) as executor:
        runs = list(executor.map(run, SPECS))
    output = {"status": "passed", "python": sys.version.split()[0], "arithmetic": "Fraction only",
              "scope": "Exact finite regression and frozen-output comparison; general theorems use analytic proofs.",
              "runs": runs}
    (ROOT / "replay-comparison.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
