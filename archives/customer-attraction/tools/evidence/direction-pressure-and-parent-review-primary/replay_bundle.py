"""Check preserved bytes; optionally replay the old audit in an isolated temporary tree.

Default only checks file identities. --run performs the old mathematical audit once
and saves its generated report at a new, explicit output path. Frozen files stay intact.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "cleanup/inventory.jsonl").is_file() and (p / "work.py").is_file())
AUDIT = "research/workspaces/customer-attraction/R-b6d636d360e14c11aeb4b76415ed422b/direction_review/audit_followup.py"


def checked_inputs():
    primary = json.loads((HERE / "source-manifest.json").read_text())
    dependencies = json.loads((HERE / "dependency-manifest.json").read_text())
    rows = [(HERE / "original-root" / row["path"], row["path"], row["sha256"]) for row in primary]
    rows += [(REPO / row["repository_path"], row["runtime_path"], row["sha256"]) for row in dependencies]
    for source, runtime, expected in rows:
        actual = hashlib.sha256(source.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Preserved file identity mismatch: {source}")
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", action="store_true", help="execute original audit once in a disposable tree")
    ap.add_argument("--output", type=Path, help="new output directory, required with --run")
    args = ap.parse_args()
    rows = checked_inputs()
    if not args.run:
        print(json.dumps({"byte_identity_checks": len(rows), "mathematical_execution": False}))
        return
    if args.output is None:
        ap.error("--run requires --output")
    # Exclusive creation prevents overwriting an earlier reproduction event.
    args.output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="direction-original-audit-") as temp:
        work = Path(temp)
        for source, runtime, expected in rows:
            target = work / runtime
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        (work / "work.py").write_text("# Reproduction root marker; no repository or Git operation.\n")
        (work / ".git").mkdir()  # The original audit chooses this name for its temporary files.
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        run = subprocess.run([sys.executable, str(work / AUDIT)], cwd=work, env=env,
                             capture_output=True, text=True, timeout=240)
        (args.output / "stdout.txt").write_text(run.stdout)
        (args.output / "stderr.txt").write_text(run.stderr)
        execution = {"returncode": run.returncode, "original_entry_executions": 1,
                     "entry_sha256": hashlib.sha256((work / AUDIT).read_bytes()).hexdigest(),
                     "preserved_input_files": len(rows), "scope": "old finite audit; not a new general theorem"}
        generated = (work / AUDIT).with_name("followup_verification.json")
        # Only a successful entry may count the copied file as freshly generated.
        if run.returncode == 0:
            frozen = json.loads((HERE / "original-root" / str(Path(AUDIT).with_name("followup_verification.json"))).read_text())
            new = json.loads(generated.read_text())
            execution["matches_frozen_semantically"] = new == frozen
            shutil.copy2(generated, args.output / "followup_verification.json")
        (args.output / "execution.json").write_text(json.dumps(execution, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(execution, ensure_ascii=False))
        if run.returncode:
            raise SystemExit(run.returncode)


if __name__ == "__main__":
    main()
