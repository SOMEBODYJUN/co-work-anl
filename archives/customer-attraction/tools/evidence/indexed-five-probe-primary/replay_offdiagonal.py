"""Replay the preserved original main in a fresh original-layout directory.

The helper itself was not executed during the single recorded original replay.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path)
    args = parser.parse_args()
    work = args.work_dir or Path(tempfile.mkdtemp(prefix="cag-offdiagonal-replay-"))
    if args.work_dir:
        work.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    source = next(x for x in manifest if x["id"] == "0fbaf567de4f29fac658")
    frozen = next(x for x in manifest if x["id"] == "559c69af59f4e0284761")
    source_file = HERE / source["preserved_path"]
    assert sha256(source_file) == source["sha256"]
    reuse = json.loads((HERE / "reused-input.json").read_text())
    certificate = REPO / reuse["path"]
    assert sha256(certificate) == reuse["sha256"]
    script = work / source["path"]
    script.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, script)
    input_file = work / "evidence/certificates/customer_attraction/five_player_indexed_bound.json"
    input_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(certificate, input_file)
    process = subprocess.run([sys.executable, str(script)], cwd=work,
                             capture_output=True, text=True)
    (work / "stdout.json").write_text(process.stdout)
    (work / "stderr.txt").write_text(process.stderr)
    assert process.returncode == 0, process.stderr
    output = script.with_suffix(".json")
    assert output.read_bytes() == (HERE / frozen["preserved_path"]).read_bytes()
    print(json.dumps({"work_dir": str(work), "output": str(output),
                      "byte_identical": True, "output_sha256": sha256(output)}))


if __name__ == "__main__":
    main()
