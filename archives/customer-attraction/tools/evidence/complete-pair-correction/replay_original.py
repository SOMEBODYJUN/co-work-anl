"""Replay the unchanged complete-pair verifier in its original sibling layout.

Default mode checks only the preserved v2 certificate. Optional --discover
reruns the old floating generator and then verifies its new v2 output; that
optional mode was not executed for this cleanup.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
RELATIVE_PARENT = Path(
    "research/workspaces/customer-attraction/"
    "R-27557809587746c59216a46867c9eb07/tree_coupling"
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discover", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((BASE / "source-manifest.json").read_text())
    entries = manifest["sources"] + manifest["reused_dependencies"]
    checked = {}
    for entry in entries:
        data = (BASE / entry["preserved_file"]).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert len(data) == entry["size"] and digest == entry["sha256"], entry["id"]
        checked[entry["id"]] = digest
    replay = BASE / "replay"
    replay.mkdir(exist_ok=True)
    started = time.monotonic()
    # Outside the clone so a concurrent Git preserve-work snapshot cannot
    # restore an already-deleted temporary copy after the process finishes.
    with tempfile.TemporaryDirectory(prefix="boss2-pair-runtime-", dir=REPO.parent) as td:
        root = Path(td)
        parent = root / RELATIVE_PARENT
        round2 = parent / "round2"
        round2.mkdir(parents=True)
        for entry in entries:
            target = root / entry["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(BASE / entry["preserved_file"], target)
        if args.discover:
            result = subprocess.run(
                [sys.executable, str(round2 / "complete_pair_v2.py")],
                cwd=root, text=True, capture_output=True,
            )
            (replay / "discovery.stdout.txt").write_text(result.stdout)
            (replay / "discovery.stderr.txt").write_text(result.stderr)
            if result.returncode:
                raise SystemExit(result.returncode)
            shutil.copyfile(round2 / "complete_pair_v2.json", replay / "generated-complete-pair-v2.json")
        result = subprocess.run(
            [sys.executable, str(round2 / "verify_complete_pair_v2.py")],
            cwd=root, text=True, capture_output=True,
        )
        name = "generated-verification" if args.discover else "verification"
        (replay / (name + ".stdout.txt")).write_text(result.stdout)
        (replay / (name + ".stderr.txt")).write_text(result.stderr)
        if result.returncode:
            raise SystemExit(result.returncode)
        report = json.loads(result.stdout)
        (replay / (name + ".json")).write_text(json.dumps(report, indent=2) + "\n")
        metadata = {
            "exit_code": result.returncode,
            "original_v2_verifier_unmodified": True,
            "old_verifier_helpers_imported_without_main": True,
            "optimizer_executed": args.discover,
            "python": sys.version.split()[0],
            "elapsed_seconds": time.monotonic() - started,
            "frozen_hashes_checked": checked,
            "stderr_empty": not result.stderr,
            "scope": "One fixed complete three-provider/six-label strategy and fixed comparison; full pair coupling, not global common-customer realizability.",
        }
        (replay / (name + "-metadata.json")).write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps({"metadata": metadata, "report": report}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
