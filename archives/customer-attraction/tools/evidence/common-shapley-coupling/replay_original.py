"""Restore the original relative paths and run the unmodified exact verifier.

Default mode verifies the preserved seven-layer certificate.  --discover
also runs the original floating candidate generator inside the temporary
tree, then verifies its newly generated certificate.  The cleanup replay
uses only the default mode.
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
ORIGINAL_RELATIVE = Path(
    "research/workspaces/customer-attraction/"
    "R-27557809587746c59216a46867c9eb07/tree_coupling"
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discover", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((BASE / "source-manifest.json").read_text())
    checked = {}
    for entry in manifest["sources"] + manifest["reproduction_dependencies"]:
        source = (BASE / entry["preserved_file"]).resolve()
        data = source.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if len(data) != entry["size"] or digest != entry["sha256"]:
            raise ValueError(f"Frozen source mismatch: {entry['id']}")
        checked[entry["id"]] = digest

    replay = BASE / "replay"
    replay.mkdir(exist_ok=True)
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="original-layout-", dir=replay) as temp:
        root = Path(temp)
        original_dir = root / ORIGINAL_RELATIVE
        original_dir.mkdir(parents=True)
        for name in ("coupling_probe.py", "verify_coupling.py", "coupling_layers.json"):
            shutil.copyfile(BASE / "original" / name, original_dir / name)
        for entry in manifest["reproduction_dependencies"]:
            destination = root / entry["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(BASE / entry["preserved_file"], destination)

        if args.discover:
            found = subprocess.run(
                [sys.executable, str(original_dir / "coupling_probe.py")],
                cwd=root, capture_output=True, text=True,
            )
            (replay / "discovery.stdout.txt").write_text(found.stdout)
            (replay / "discovery.stderr.txt").write_text(found.stderr)
            if found.returncode:
                raise SystemExit(found.returncode)
            shutil.copyfile(
                original_dir / "coupling_layers.json",
                replay / "generated-coupling-layers.json",
            )

        result = subprocess.run(
            [sys.executable, str(original_dir / "verify_coupling.py")],
            cwd=root, capture_output=True, text=True,
        )
        label = "generated-verification" if args.discover else "verification"
        (replay / f"{label}.stdout.txt").write_text(result.stdout)
        (replay / f"{label}.stderr.txt").write_text(result.stderr)
        if result.returncode:
            raise SystemExit(result.returncode)
        report = json.loads(result.stdout)
        (replay / f"{label}.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        )
        metadata = {
            "exit_code": result.returncode,
            "original_verifier_unmodified": True,
            "original_relative_layout_restored": True,
            "optimizer_executed": args.discover,
            "python": sys.version.split()[0],
            "elapsed_seconds": time.monotonic() - started,
            "frozen_source_hashes_checked": checked,
            "stderr_empty": not result.stderr,
            "scope": "Seven fixed-strategy/fixed-comparison primal-dual certificates; not a general SPE welfare theorem.",
        }
        (replay / f"{label}-metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n"
        )
        print(json.dumps({"metadata": metadata, "report": report}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
