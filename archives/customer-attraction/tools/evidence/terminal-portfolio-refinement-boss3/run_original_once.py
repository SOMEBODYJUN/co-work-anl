"""One unchanged default --verify event in a fresh external original layout.

Usage: python3 run_original_once.py REPO /absolute/new-empty-runtime
The shared manifest is a materialization inventory, not an import access log.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    repo, runtime = map(lambda x: Path(x).resolve(), sys.argv[1:3])
    runtime.mkdir(parents=True, exist_ok=False)
    shared = repo / "archives/customer-attraction/tools/evidence/combined-branch-master-program/source-manifest.json"
    manifest = json.loads(shared.read_text())
    inputs = []
    for rec in manifest["frozen_sources"]:
        src = repo / rec["stored_path"]
        assert src.stat().st_size == rec["size"] and sha(src) == rec["sha256"]
        target = runtime / rec["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, target)
        inputs.append(dict(id=rec["id"], path=rec["path"], stored_path=rec["stored_path"],
                           size=rec["size"], sha256=rec["sha256"], role="shared available dependency"))
    own = json.loads((HERE / "source-manifest.json").read_text())
    for rec in own["sources"]:
        src = HERE / "original" / rec["id"] / Path(rec["path"]).name
        target = runtime / rec["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, target)
        assert sha(target) == rec["sha256"]
        inputs.append(dict(id=rec["id"], path=rec["path"], retained_path=rec["retained_path"],
                           size=rec["size"], sha256=rec["sha256"], role="four-source batch input"))
    (runtime / "work.py").write_text("# Root-location marker only; never imported or executed.\n")
    before = {r["path"]: sha(runtime / r["path"]) for r in inputs}
    script = next(runtime / r["path"] for r in inputs if r["id"] == "b4dd5c92d5e5f049779e")
    argv = [sys.executable, "-B", str(script), "--verify"]
    start_utc = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    result = subprocess.run(argv, cwd=runtime, input=b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elapsed = time.monotonic()-start
    runs = HERE / "runs"
    runs.mkdir(exist_ok=True)
    (runs / "original.stdout").write_bytes(result.stdout)
    (runs / "original.stderr").write_bytes(result.stderr)
    after = {r["path"]: sha(runtime / r["path"]) for r in inputs}
    record = dict(start_utc=start_utc, argv=argv, cwd=str(runtime), elapsed_seconds=elapsed,
        exit_code=result.returncode, stdout_bytes=len(result.stdout), stderr_bytes=len(result.stderr),
        available_materialized_inputs=len(inputs), materialized_inputs_unchanged=before==after,
        original_default_verifier_executions=1, capacity_verifier_executions=0,
        discovery_or_LP_executions=0, inputs=inputs,
        scope="One default 5083-row finite necessary-system verification, not full SPE or independent full graph implementation")
    (runs / "original-execution.json").write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
    assert result.returncode == 0 and not result.stderr and before == after
    print(json.dumps({k:v for k,v in record.items() if k!="inputs"},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
