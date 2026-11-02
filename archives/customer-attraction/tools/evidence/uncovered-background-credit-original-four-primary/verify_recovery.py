"""Verify the preserved four-source package and replay its unchanged entry.

Run from any directory with assertions enabled. This is a recovery check, not
an independent SPE implementation or an arbitrary-player experiment.
"""

from datetime import datetime, timezone
from hashlib import sha1, sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


PACKAGE = Path(__file__).resolve().parent
REPO = next(p for p in PACKAGE.parents if (p / "cleanup/inventory.jsonl").is_file())


def main():
    if not __debug__:
        raise RuntimeError("run without -O: the original audit uses assertions")
    inventory = {row["id"]: row for row in (
        json.loads(line) for line in (REPO / "cleanup/inventory.jsonl").read_text().splitlines()
    )}
    checked = []
    for manifest in ("source-manifest.json", "related-source-manifest.json"):
        for row in json.loads((PACKAGE / manifest).read_text()):
            content = (REPO / row["preserved_path"]).read_bytes()
            blob = sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
            frozen = inventory[row["id"]]
            assert (len(content), sha256(content).hexdigest(), blob) == (
                frozen["size"], frozen["sha256"], frozen["blob"]
            )
            assert (row["size"], row["sha256"], row["blob"]) == (
                frozen["size"], frozen["sha256"], frozen["blob"]
            )
            checked.append({"id": row["id"], "path": row["preserved_path"],
                            "size": len(content), "sha256": sha256(content).hexdigest(),
                            "git_blob": blob})
    dependencies = json.loads((PACKAGE / "dependency-manifest.json").read_text())
    for row in dependencies:
        content = (REPO / row["reused_from"]).read_bytes()
        assert (len(content), sha256(content).hexdigest()) == (row["size"], row["sha256"])

    source_rows = json.loads((PACKAGE / "source-manifest.json").read_text())
    entry = next(row for row in source_rows if row["path"].endswith(".py"))
    frozen_report = next(row for row in source_rows if row["path"].endswith(".json"))
    destination = PACKAGE / "recovery-replay"
    destination.mkdir(exist_ok=True)
    scratch = REPO / "cleanup/workspaces/Boss6/recovery"
    scratch.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    with tempfile.TemporaryDirectory(prefix="deletion-source-root-", dir=scratch) as temporary:
        root = Path(temporary)
        script = root / entry["path"]
        script.parent.mkdir(parents=True)
        shutil.copyfile(REPO / entry["preserved_path"], script)
        for row in dependencies:
            target = root / row["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / row["reused_from"], target)
        argv = [sys.executable, "-I", "-B", str(script)]
        start_clock = time.perf_counter()
        completed = subprocess.run(argv, cwd=root, capture_output=True, timeout=60)
        elapsed = time.perf_counter() - start_clock
        event = {"started_utc": started, "argv": argv, "cwd": str(root),
                 "python_version": sys.version, "script_sha256": entry["sha256"],
                 "exit_code": completed.returncode, "elapsed_seconds": elapsed,
                 "stdout_bytes": len(completed.stdout),
                 "stdout_sha256": sha256(completed.stdout).hexdigest(),
                 "stderr_bytes": len(completed.stderr),
                 "byte_identical_frozen_report": completed.stdout == (
                     REPO / frozen_report["preserved_path"]).read_bytes(),
                 "assertions_enabled": True, "primary_and_related_fingerprints": checked,
                 "dependencies": dependencies,
                 "scope": "AB r1..5 full ordered histories; n64 rational formulas only"}
        (destination / "stdout.json").write_bytes(completed.stdout)
        (destination / "stderr.txt").write_bytes(completed.stderr)
        (destination / "execution.json").write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n")
    assert completed.returncode == 0 and not completed.stderr
    assert event["byte_identical_frozen_report"]
    print(json.dumps({"fingerprints_verified": len(checked),
                      "dependencies_verified": len(dependencies),
                      "exit_code": event["exit_code"],
                      "byte_identical_frozen_report": True,
                      "stdout_sha256": event["stdout_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
