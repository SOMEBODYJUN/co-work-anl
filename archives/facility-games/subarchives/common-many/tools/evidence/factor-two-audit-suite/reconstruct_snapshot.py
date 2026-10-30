"""Materialize the declared frozen core audit fixture via the root source reader.

Only exports source files and verifies hashes. It neither runs the audits nor
performs Git claims, commits, pushes, or completion records.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-py", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--manifest", type=Path,
                        default=Path(__file__).with_name("snapshot_manifest.json"))
    args = parser.parse_args()
    work = args.work_py.resolve()
    if not work.is_file():
        parser.error("--work-py must identify the result repository's root source reader")
    manifest = json.loads(args.manifest.read_text())
    commit = manifest["frozen_commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        parser.error("Invalid pinned commit")
    destination = args.destination.resolve()
    entries = manifest["files"]
    seen = set()
    for entry in entries:
        relative = PurePosixPath(entry["path"])
        if relative.is_absolute() or ".." in relative.parts or str(relative) in seen:
            parser.error("Invalid or duplicate manifest path")
        seen.add(str(relative))
        if not re.fullmatch(r"[0-9a-f]{20}", entry["id"]):
            parser.error("Invalid source ID")
        if not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
            parser.error("Invalid source digest")
        target = destination.joinpath(*relative.parts)
        if target.exists():
            if not target.is_file() or digest(target) != entry["sha256"]:
                parser.error("Refusing to overwrite a nonmatching destination: " + str(relative))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(
                [sys.executable, str(work), "clean", "show", entry["id"],
                 "--out", str(target)],
                cwd=work.parent, capture_output=True, text=True,
            )
            if result.returncode:
                # Do not echo source-reader diagnostics that might contain local
                # connection details. Its normal read command can be inspected
                # separately when resolving a failed source fetch.
                raise SystemExit("Source reader failed for " + entry["id"]
                                 + "; no audit was executed.")
        if target.stat().st_size != entry["size_bytes"] or digest(target) != entry["sha256"]:
            raise SystemExit("Pinned-byte verification failed for " + str(relative))
    print(json.dumps({
        "frozen_commit": commit,
        "files_verified": len(entries),
        "destination": str(destination),
        "scope": manifest["purpose"],
        "audits_executed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
