"""Replay the recovered 51-weight dual audit and the 67-atom primal audit.

This launcher only restores the original relative paths in a new output folder.
It never edits source bytes, reruns the mature 60-atom point, invokes discovery
LPs, or accesses the network.  The original parent audit deliberately executes
only the definition prefix of the mature 437-row evaluator.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "work.py").is_file())
EVIDENCE = REPO / "archives/customer-attraction/tools/evidence"
ACTOR = "research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    runtime = output / "runtime"
    runtime.mkdir()
    routes = [
        (HERE / "original/round4_independent/full_pricing_audit.py",
         f"{ACTOR}/round4_independent/full_pricing_audit.py"),
        (HERE / "original/round4_parent/audit_full_primal.py",
         f"{ACTOR}/round4_parent/audit_full_primal.py"),
        (EVIDENCE / "round4-pricing-resumed-boss2/original/exact_dual_overlap1.json",
         f"{ACTOR}/round4_pricing/exact_dual_overlap1.json"),
        (EVIDENCE / "round4-pricing-resumed-boss2/original/exact_optimum_primal_overlap1.json",
         f"{ACTOR}/round4_pricing/exact_optimum_primal_overlap1.json"),
        (EVIDENCE / "five-player-indexed/tests/audits/customer_attraction_five_indexed.py",
         "tests/audits/customer_attraction_five_indexed.py"),
        (EVIDENCE / "catalog-boundaries-original-boss3/dependencies/customer_attraction/__init__.py",
         "customer_attraction/__init__.py"),
    ]
    bindings = []
    for source, relative in routes:
        target = runtime / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        bindings.append({"source": source.relative_to(REPO).as_posix(),
                         "runtime_path": relative, "size": source.stat().st_size,
                         "sha256": sha(source)})
    (output / "input-bindings.json").write_text(
        json.dumps(bindings, ensure_ascii=False, indent=2) + "\n")
    cases = [
        ("dual-full-universe", [sys.executable,
          str(runtime / ACTOR / "round4_independent/full_pricing_audit.py")],
         runtime / ACTOR / "round4_independent/full_pricing_audit.json",
         HERE / "original/round4_independent/full_pricing_audit.json", {"seconds"}),
        ("primal-67", [sys.executable,
          str(runtime / ACTOR / "round4_parent/audit_full_primal.py"),
          "--source", str(runtime / ACTOR / "round4_pricing/exact_optimum_primal_overlap1.json"),
          "--output", str(output / "primal-67.json")],
         output / "primal-67.json",
         HERE / "original/round4_parent/audit_optimum557_primal.json", set()),
    ]
    observations = []
    for name, argv, report_path, frozen_report, timing_keys in cases:
        began = time.perf_counter()
        run = subprocess.run(argv, cwd=runtime, capture_output=True, text=True, timeout=300)
        elapsed = time.perf_counter() - began
        (output / f"{name}.stdout.txt").write_text(run.stdout)
        (output / f"{name}.stderr.txt").write_text(run.stderr)
        observation = {"case": name, "invocations": 1, "returncode": run.returncode,
                       "elapsed_seconds": elapsed, "argv": argv}
        observations.append(observation)
        (output / "execution.json").write_text(json.dumps(
            {"recorded_at_utc": datetime.now(timezone.utc).isoformat(),
             "python": platform.python_version(), "runs": observations},
            ensure_ascii=False, indent=2) + "\n")
        if run.returncode:
            raise RuntimeError(f"{name} failed; inspect preserved stdout and stderr")
        current = json.loads(report_path.read_text())
        prior = json.loads(frozen_report.read_text())
        differences = {key: {"frozen": prior.get(key), "current": current.get(key)}
                       for key in sorted(set(current) | set(prior))
                       if current.get(key) != prior.get(key)}
        assert set(differences) <= timing_keys, differences
        observation.update(
            output_sha256=sha(report_path), frozen_report_sha256=sha(frozen_report),
            semantic_report_equal=True, differences=differences,
            byte_equal=(report_path.read_bytes() == frozen_report.read_bytes()))
        if report_path != output / f"{name}.json":
            shutil.copyfile(report_path, output / f"{name}.json")
        (output / "execution.json").write_text(json.dumps(
            {"recorded_at_utc": datetime.now(timezone.utc).isoformat(),
             "python": platform.python_version(), "runs": observations},
            ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(observation, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
