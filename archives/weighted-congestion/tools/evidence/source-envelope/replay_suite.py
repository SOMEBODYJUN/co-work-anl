#!/usr/bin/env python3
"""Replay the three unchanged frozen audit programs in isolated directories.

Fraction tests are finite exact checks. Decimal outputs remain diagnostics.
This driver compares data; it does not certify the analytic asymptotic proof.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SPECS = (
    ("ceiling", "source_ceiling/verify.py", "source_ceiling/verification.json", []),
    ("sharp", "source_envelope/verify_logs.py", "source_envelope/verification.json",
     ["--output", "verification.json"]),
    ("candidate", "source_envelope_candidate/verify.py", "source_envelope_candidate/verification.json", []),
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
    name, program, frozen_report, args = spec
    source = ROOT / "original/tests/audits/weighted_congestion" / program
    target = ROOT / "replay" / name
    target.mkdir(parents=True, exist_ok=True)
    executable = target / source.name
    shutil.copy2(source, executable)
    command = [sys.executable, executable.name, *args]
    completed = subprocess.run(command, cwd=target, text=True, capture_output=True)
    (target / "stdout.txt").write_text(completed.stdout)
    (target / "stderr.txt").write_text(completed.stderr)
    if completed.returncode:
        raise RuntimeError(f"{name} failed; see {target / 'stderr.txt'}")
    old = json.loads((ROOT / "original/evidence/runs/weighted_congestion" / frozen_report).read_text())
    new = json.loads((target / "verification.json").read_text())
    diff = differences(old, new)
    return {"name": name, "command": command, "exit_code": completed.returncode,
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "differences": diff, "mathematical_fields_equal": all(d["path"] == "/python" for d in diff)}


def main():
    if not __debug__:
        raise RuntimeError("Audits require enabled assertions; do not use -O")
    manifest = json.loads((ROOT / "provenance.json").read_text())
    for source in manifest["sources"]:
        path = ROOT / "original" / source["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"], source["path"]
    with ThreadPoolExecutor(max_workers=3) as executor:
        reports = list(executor.map(run, SPECS))
    output = {"status": "passed", "python": sys.version.split()[0],
              "scope": "Unchanged finite Fraction checks and non-interval Decimal diagnostics; written proofs carry general claims.",
              "runs": reports}
    (ROOT / "replay-comparison.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
