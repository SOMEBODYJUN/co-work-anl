#!/usr/bin/env python3
"""Run the exact frozen independent audit bytes, including their original EOF."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output", type=Path)
    mode.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    manifest = json.loads((base / "source-manifest.json").read_text())
    row = next(x for x in manifest["files"] if x["id"] == "7a02bf4225ed1566ad23")
    packed = (base / row["stored_original_path"]).read_bytes()
    assert hashlib.sha256(packed).hexdigest() == row["stored_sha256"]
    raw = gzip.decompress(packed)
    assert len(raw) == row["size"]
    assert hashlib.sha256(raw).hexdigest() == row["sha256"]
    readable = (base / row["normalized_copy_path"]).read_bytes()
    assert hashlib.sha256(readable).hexdigest() == row["normalized_copy_sha256"]
    assert readable == raw.rstrip(b"\n") + b"\n"
    if args.verify_only:
        print(json.dumps({"status": "PASS", "original_sha256": row["sha256"]}))
        return
    output = args.output.resolve()
    with tempfile.TemporaryDirectory(prefix="prefix-family-frozen-") as temporary:
        script = Path(temporary) / Path(row["original_path"]).name
        script.write_bytes(raw)
        subprocess.run([sys.executable, str(script), "--output", str(output)], check=True)


if __name__ == "__main__":
    main()
