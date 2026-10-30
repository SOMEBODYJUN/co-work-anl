#!/usr/bin/env python3
"""Replay unchanged decision-core audits in their required repository layout."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
METHODS = Path("tests/audits/weighted_congestion/decision_methods")
FIXTURES = Path("examples/weighted_congestion/decision_methods")
SPECS = (("runner", "decision_runner_audit.py", "decision_runner_audit.json"),
         ("quality", "decision_quality_audit.py", "decision_quality_audit.json"),
         ("independent", "independent_attack_check.py", "independent_attack.json"))


def differences(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(a.keys() | b.keys()):
            if k not in a or k not in b:
                out.append({"path": f"{path}/{k}", "frozen": a.get(k), "replay": b.get(k)})
            else:
                out.extend(differences(a[k], b[k], f"{path}/{k}"))
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [r for i, (x, y) in enumerate(zip(a, b)) for r in differences(x, y, f"{path}/{i}")]
    return [] if a == b else [{"path": path, "frozen": a, "replay": b}]


def main():
    if not __debug__:
        raise RuntimeError("Do not use -O; original audit assertions must remain enabled")
    for entry in json.loads((ROOT / "provenance.json").read_text())["sources"]:
        assert hashlib.sha256((ROOT / "original" / entry["path"]).read_bytes()).hexdigest() == entry["sha256"]
    destination = ROOT / "replay"
    destination.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="decision-core-run-", dir=ROOT) as directory:
        layout = Path(directory)
        for base in ("original", "related"):
            for path in (ROOT / base / METHODS).glob("*.py"):
                target = layout / METHODS / path.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
            for path in (ROOT / base / FIXTURES).glob("*.json"):
                target = layout / FIXTURES / path.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
        assert len(list((layout / FIXTURES).glob("*.json"))) == 5

        def run(spec):
            name, script, report = spec
            target = layout / f"new-{name}.json"
            command = [sys.executable, str(layout / METHODS / script), "--output", str(target)]
            result = subprocess.run(command, cwd=layout, text=True, capture_output=True)
            (destination / f"{name}-stdout.txt").write_text(result.stdout)
            (destination / f"{name}-stderr.txt").write_text(result.stderr)
            if result.returncode:
                raise RuntimeError(f"{name} failed; see saved stderr")
            new = json.loads(target.read_text())
            old = json.loads((ROOT / "original/evidence/runs/weighted_congestion/decision_methods" / report).read_text())
            diff = differences(old, new)
            shutil.copy2(target, destination / report)
            return {"name": name, "command": command, "exit_code": result.returncode,
                    "source_sha256": hashlib.sha256((layout / METHODS / script).read_bytes()).hexdigest(),
                    "differences": diff, "all_fields_equal": not diff}

        with ThreadPoolExecutor(max_workers=3) as executor:
            reports = list(executor.map(run, SPECS))
    output = {"status": "passed", "python": sys.version.split()[0],
              "scope": "Three unchanged exact audits, with calibration helper and five literal fixtures. Static baseline/review records are preserved, not falsely described as regenerated.",
              "runs": reports}
    (ROOT / "replay-comparison.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
