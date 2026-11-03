"""Run one unchanged discovery source in a temporary frozen-layout tree.

Usage: python3 run_original.py old36|insurance
Generated files are collected in runs/<name>; frozen originals never change.
"""
from pathlib import Path
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
name = sys.argv[1]
assert name in ("old36", "insurance")
script = "check_shared_load_old36.py" if name == "old36" else "insurance_shared_covariance_probe.py"
outdir = HERE / "runs" / name
outdir.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="boss5-shared-covariance-") as temporary:
    root = Path(temporary)
    folder = root / "research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round11/aggregate"
    folder.mkdir(parents=True)
    destination = folder / script
    shutil.copyfile(HERE / "original" / script, destination)
    if name == "old36":
        for source, target in [("old36-input.json", "examples/customer_attraction/aggregate_theta_failure.json"),
                               ("old36-strategy.json", "evidence/certificates/customer_attraction/aggregate_theta_failure.json")]:
            path = root / target
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HERE / "related" / source, path)
    command = [sys.executable, str(destination)] + (["6"] if name == "insurance" else [])
    start = time.monotonic()
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=60)
    elapsed = time.monotonic() - start
    (outdir / "stdout.txt").write_text(result.stdout)
    (outdir / "stderr.txt").write_text(result.stderr)
    generated = []
    for path in folder.glob("*.json"):
        shutil.copyfile(path, outdir / path.name)
        generated.append(path.name)
    report = {"unchanged_source_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
              "python": platform.python_version(), "exit_code": result.returncode,
              "elapsed_seconds": elapsed, "argv_suffix": ["6"] if name == "insurance" else [],
              "temporary_layout_deleted": True, "generated_files": sorted(generated),
              "stdout_file": "stdout.txt", "stderr_file": "stderr.txt"}
    for module in ("numpy", "scipy"):
        try:
            report[module + "_version"] = __import__(module).__version__
        except ImportError:
            report[module + "_version"] = None
    (outdir / "event.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
