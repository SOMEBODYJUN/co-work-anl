"""Replay exactly the frozen seed-1301 source once into a new directory.

This is an execution wrapper, not a second equilibrium implementation.
It refuses to overwrite a previous run and compares every deterministic
report field. Elapsed time is deliberately preserved, not compared.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    expected = {
        "isolated_option_probe.py": "88a73c4a13abeb09059228775da2743307962e89687678ec9f24f6ecb101c772",
        "isolated_option_unit_seed1301.json": "76283ba45b75bb47a48f7d7913aba0a54613330e67d45911d0bb85dee234a49a",
    }
    for name, sha in expected.items():
        actual = hashlib.sha256((here / "original" / name).read_bytes()).hexdigest()
        if actual != sha:
            raise SystemExit(f"Frozen source hash differs: {name}")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    command = [sys.executable, str(here / "original/isolated_option_probe.py"),
               "--seed", "1301", "--cases", "10000", "--mode", "unit",
               "--output", str(out / "report.json")]
    run = subprocess.run(command, cwd=out, capture_output=True, timeout=180)
    (out / "stdout.txt").write_bytes(run.stdout)
    (out / "stderr.txt").write_bytes(run.stderr)
    event = {
        "implementation": "unchanged frozen original; no independent solver",
        "python": sys.version,
        "platform": platform.platform(),
        "source_sha256": expected,
        "arguments": ["--seed", "1301", "--cases", "10000", "--mode", "unit"],
        "exit_code": run.returncode,
        "excluded_comparison_fields": ["elapsed_seconds"],
    }
    if run.returncode == 0:
        old = json.loads((here / "original/isolated_option_unit_seed1301.json").read_text())
        new = json.loads((out / "report.json").read_text())
        old_deterministic = {k: v for k, v in old.items() if k != "elapsed_seconds"}
        new_deterministic = {k: v for k, v in new.items() if k != "elapsed_seconds"}
        event["deterministic_fields_equal"] = old_deterministic == new_deterministic
        event["compared_fields"] = sorted(old_deterministic)
        event["original_elapsed_seconds"] = old["elapsed_seconds"]
        event["new_elapsed_seconds"] = new["elapsed_seconds"]
        event["stdout_equals_written_report"] = run.stdout == (out / "report.json").read_bytes()
    (out / "execution.json").write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(event, ensure_ascii=False, indent=2))
    if run.returncode or not event.get("deterministic_fields_equal") or not event.get("stdout_equals_written_report"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
