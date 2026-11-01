"""Run the four frozen entry points in a separate copy, recording actual results.

The NumPy/SciPy programs are discovery computations, except for the original
prefix program's explicit Fraction residual checks. No solver status here is
an exact infeasibility certificate or a full-history game certificate.
"""
from pathlib import Path
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
PROGRAM_DIR = Path("research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2")


def main():
    import numpy
    import scipy
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    for item in manifest:
        path = HERE / item["evidence_path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    assert not (out / "execution.json").exists(), "Use a new recorded run directory, do not overwrite an execution."
    runs = []
    with tempfile.TemporaryDirectory(prefix="boss3-prefix-tail-nested-") as temp:
        runtime = Path(temp) / "runtime"
        shutil.copytree(HERE / "original", runtime)
        env = dict(os.environ)
        env.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
        for name in ("prefix_floor_lp.py", "last_three_lp.py", "nested_branch_lp.py", "lift_old_point.py"):
            program = runtime / PROGRAM_DIR / name
            argv = [sys.executable, "-B", str(program)]
            start = time.time()
            completed = subprocess.run(argv, cwd=program.parent, capture_output=True, env=env)
            stem = Path(name).stem
            (out / (stem + ".stdout.json")).write_bytes(completed.stdout)
            (out / (stem + ".stderr.txt")).write_bytes(completed.stderr)
            run = {"program": name, "argv": argv, "cwd": str(program.parent),
                   "exit_code": completed.returncode, "seconds": time.time() - start,
                   "stdout_bytes": len(completed.stdout), "stderr_bytes": len(completed.stderr),
                   "source_sha256": hashlib.sha256(program.read_bytes()).hexdigest()}
            runs.append(run)
            (out / "execution.partial.json").write_text(json.dumps(runs, indent=2) + "\n")
            print(json.dumps(run), flush=True)
            if completed.returncode:
                break
        for item in manifest:
            assert hashlib.sha256((runtime / item["path"]).read_bytes()).hexdigest() == item["sha256"]
    result = {"python": platform.python_version(), "numpy": numpy.__version__,
              "scipy": scipy.__version__, "assertions_enabled": __debug__,
              "thread_environment": {"OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1"},
              "original_files_unchanged": True, "runs": runs}
    (out / "execution.json").write_text(json.dumps(result, indent=2) + "\n")
    if any(run["exit_code"] for run in runs):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
