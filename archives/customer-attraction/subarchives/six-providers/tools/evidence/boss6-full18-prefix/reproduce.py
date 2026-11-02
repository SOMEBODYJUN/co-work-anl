"""Replay the two frozen exact entries in an isolated writable tree; no LP."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def strip_seconds(value):
    if isinstance(value, dict):
        return {k: strip_seconds(v) for k, v in value.items() if k != "seconds"}
    if isinstance(value, list):
        return [strip_seconds(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    run = out / "run-tree"
    shutil.copytree(HERE / "original", run)
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    for rec in manifest:
        data = (HERE / rec["saved_path"]).read_bytes()
        assert len(data) == rec["size"]
        assert hashlib.sha256(data).hexdigest() == rec["sha256"]
    records = []
    jobs = [
        ("full18", ["full18_exact_bi.py"], "full18_exact_bi.json", "full18_exact_bi.json"),
        ("Rdiag-prefix", ["audit_seed_actual_prefix.py", "../research_5/seed18_Rdiag.json", "prefix-replay"],
         "prefix-replay_actual_prefix_audit.json", "seed18_Rdiag_actual_prefix_audit.json"),
    ]
    for name, argv, product, reference in jobs:
        command = [sys.executable] + argv
        start = time.monotonic()
        result = subprocess.run(command, cwd=run / "research_1", text=True, capture_output=True)
        (out / (name + ".stdout.txt")).write_text(result.stdout)
        (out / (name + ".stderr.txt")).write_text(result.stderr)
        rec = {"name": name, "argv": ["python3"] + argv, "cwd": "run-tree/research_1",
               "returncode": result.returncode, "elapsed_seconds": time.monotonic() - start}
        records.append(rec)
        assert result.returncode == 0, rec
        actual = json.loads((run / "research_1" / product).read_text())
        expected = json.loads((HERE / "original/research_1" / reference).read_text())
        same = strip_seconds(actual) == strip_seconds(expected)
        rec["all_non_time_fields_equal"] = same
        dump(out / (name + ".json"), actual)
        assert same, name
    import numpy
    import scipy
    dump(out / "execution.json", {"python": platform.python_version(), "numpy": numpy.__version__,
         "scipy": scipy.__version__, "source_sha256_verified": True,
         "method": "original implementation replay; not an independent SPE solver", "jobs": records})
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
