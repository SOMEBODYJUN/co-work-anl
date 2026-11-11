"""Run one declared step and retain actual argv, source, and raw process output."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
STEPS = {"dual_repair": "recover_dual_repair.py"}


def main():
    step = sys.argv[1]
    script = STEPS[step]
    manifest_path = HERE/"execution_manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {
        "scope":"actual frozen-input finite LP executions; raw stdout/stderr retained verbatim",
        "executions": []}
    attempt = 1 + sum(record["step"] == step for record in manifest["executions"])
    suffix = "" if attempt == 1 else "_attempt" + str(attempt)
    stdout_path, stderr_path = HERE/(step+suffix+"_stdout.txt"), HERE/(step+suffix+"_stderr.txt")
    assert not stdout_path.exists() and not stderr_path.exists()
    digest = sha256((HERE/script).read_bytes()).hexdigest()
    snapshot = HERE/"executed_sources"/(Path(script).stem+"_"+digest+".py")
    assert snapshot.read_bytes() == (HERE/script).read_bytes()
    command = [sys.executable, "-u", script]
    start = time.time()
    record = {"step":step, "attempt":attempt, "command":command,
              "driver_command":[sys.executable,"-u","run_repair.py",step],
              "working_directory":str(HERE), "started_utc":datetime.now(timezone.utc).isoformat(),
              "executed_source":script, "source_sha256":digest,
              "source_snapshot":str(snapshot.relative_to(HERE)),
              "driver_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
              "stdout":stdout_path.name, "stderr":stderr_path.name, "status":"running"}
    manifest["executions"].append(record)
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        process = subprocess.run(command,cwd=HERE,stdout=stdout,stderr=stderr,check=False)
    record.update({"exit_code":process.returncode,"status":"finished","seconds":time.time()-start,
                   "finished_utc":datetime.now(timezone.utc).isoformat(),
                   "stdout_sha256":sha256(stdout_path.read_bytes()).hexdigest(),
                   "stderr_sha256":sha256(stderr_path.read_bytes()).hexdigest()})
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(record,ensure_ascii=False),flush=True)
    raise SystemExit(process.returncode)


if __name__ == "__main__":
    main()
