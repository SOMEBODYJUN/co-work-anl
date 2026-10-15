#!/usr/bin/env python3
"""Replay frozen WC audit code in a disposable source-layout mirror.

The curated repository separates proof, review, code and evidence. Older exact
checkers used relative siblings and overwrote their own output files. This
runner restores those layouts only inside a TemporaryDirectory. Frozen records
in the repository are never output destinations. --report is an explicit new
result file and refuses to overwrite an existing one.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "research/weighted_congestion_frontier/INTEGRATION.json"


def execute(script, timeout=120):
    manifest = json.loads(MANIFEST.read_text())
    files = manifest["classification"]
    aliases = {item["path"]: old for old, item in files.items() if "path" in item}
    old = aliases.get(script, script)
    if old not in files or not old.endswith(".py") or "path" not in files[old]:
        raise ValueError("Select a registered audit script with --list.")
    before = {item["path"]: hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest()
              for item in files.values() if "path" in item
              and item["path"].startswith("evidence/")}
    with tempfile.TemporaryDirectory(prefix="wc-replay-", dir=ROOT.parent) as folder:
        temp = Path(folder)
        for original, item in files.items():
            if "path" not in item:
                continue
            target = temp / original
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / item["path"]).read_bytes())
        # A few original checkers record their Git version. This local fixture
        # has no network remote or credential configuration.
        subprocess.run(["git", "init", "--quiet", "--initial-branch=main"], cwd=temp, check=True)
        subprocess.run(["git", "-c", "user.name=Audit", "-c", "user.email=audit@example.invalid",
                        "commit", "--quiet", "--allow-empty", "-m", "isolated replay"], cwd=temp, check=True)
        started = time.monotonic()
        extra = (["--output", str(temp / "linear-reset-replay.json")]
                 if old.endswith("odd_ring_audit/verify_linear_reset.py") else [])
        if old.endswith("multicolumn_frontier/verify.py"):
            # This checker correctly refuses overwriting its frozen sibling.
            # Remove only the disposable copy; the original stays immutable.
            (temp / old).with_name("evidence.json").unlink(missing_ok=True)
        result = subprocess.run([sys.executable, str(temp / old), *extra], cwd=temp,
                                capture_output=True, text=True, timeout=timeout,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        record = {"script": files[old]["path"], "source_path": old,
                  "source_sha256": hashlib.sha256((ROOT / files[old]["path"]).read_bytes()).hexdigest(),
                  "exit_code": result.returncode, "seconds": round(time.monotonic()-started, 3),
                  "stdout": result.stdout[-12000:], "stderr": result.stderr[-4000:]}
    after = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in before}
    if before != after:
        raise RuntimeError("Frozen evidence changed during replay.")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", nargs="?")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    files = json.loads(MANIFEST.read_text())["classification"]
    if args.list:
        print("\n".join(sorted(item["path"] for old,item in files.items()
                               if old.endswith(".py") and "path" in item)))
        return 0
    if not args.script:
        parser.error("Select a script, or use --list.")
    if args.report and args.report.exists():
        parser.error("--report must name a new file; frozen outputs cannot be overwritten.")
    record = execute(args.script, args.timeout)
    text = json.dumps(record, ensure_ascii=False, indent=2)+"\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open("x") as out:
            out.write(text)
    print(text, end="")
    return record["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
