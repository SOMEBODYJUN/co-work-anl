"""Run the frozen coefficient audit once in a new, isolated directory.

The original has no main guard and overwrites its sibling report. This wrapper
copies its unchanged source into a new directory before execution; it adds no
second coefficient, game or equilibrium implementation.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    source = here / "original/max_topic_saturation_audit.py"
    frozen = here / "original/max_topic_saturation_audit.json"
    hashes = {
        source.name: "f4e2b3ea422a125cfc131b8870c0781d186d18c54b0a9034d3f670185c7ff85f",
        frozen.name: "6dbd6a1b822cd33773c7b291b13f4567360f492405aacf874af200b3b7d6ccf8",
    }
    for path in (source, frozen):
        if hashlib.sha256(path.read_bytes()).hexdigest() != hashes[path.name]:
            raise SystemExit(f"Frozen source hash differs: {path.name}")
    if not __debug__:
        raise SystemExit("Assertions must be enabled")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(source, out / source.name)
    environment = dict(os.environ)
    environment.pop("PYTHONOPTIMIZE", None)
    run = subprocess.run([sys.executable, str(out / source.name)], cwd=out,
                         capture_output=True, timeout=60, env=environment)
    (out / "stdout.txt").write_bytes(run.stdout)
    (out / "stderr.txt").write_bytes(run.stderr)
    generated = out / frozen.name
    event = {
        "implementation": "unchanged original coefficient audit; no game solver or independent implementation",
        "python": sys.version,
        "platform": platform.platform(),
        "assertions_enabled": __debug__,
        "PYTHONOPTIMIZE_removed_for_child": True,
        "original_entry_runs": 1,
        "source_sha256": hashes,
        "exit_code": run.returncode,
        "report_bytes_equal": generated.exists() and generated.read_bytes() == frozen.read_bytes(),
        "stderr_empty": not run.stderr,
    }
    if run.returncode == 0:
        report = json.loads(generated.read_text())
        summary = json.loads(run.stdout)
        event["stdout_matches_full_report_projection"] = summary == {
            "m_values": len(report["players_checked"]),
            "customer_masks": sum(row["customer_masks"] for row in report["players_checked"]),
            "floor_only_obstruction": report["floor_only_obstruction"],
        }
    (out / "execution.json").write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(event, ensure_ascii=False, indent=2))
    if run.returncode or not event["report_bytes_equal"] or not event.get("stdout_matches_full_report_projection"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
