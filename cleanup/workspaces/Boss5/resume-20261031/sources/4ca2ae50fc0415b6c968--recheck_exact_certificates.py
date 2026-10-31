#!/usr/bin/env python3
"""Rerun four exact certificates in isolation without modifying frozen evidence.

This checks reproducibility, not novelty or the infinite-domain theorems.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile


CASES = [
    ("finite_weight/verify_universal.py", "verify_universal.json"),
    ("budget_nash/cloning_certificate.py", "cloning_certificate.json"),
    ("budget_nash/verify_cloning_conp_certificate.py", "verify_cloning_conp_certificate.json"),
    ("gap_tools/exact_uniformization_counterexample.py", "exact_uniformization_counterexample.json"),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error("output already exists; preserve frozen evidence")
    base = Path(__file__).resolve().parent
    checks = []
    with tempfile.TemporaryDirectory(prefix="boss37-exact-") as directory:
        temporary = Path(directory)
        for index, (source_name, result_name) in enumerate(CASES):
            source = base / source_name
            target = temporary / str(index)
            target.mkdir()
            shutil.copy2(source, target / source.name)
            run = subprocess.run([sys.executable, str(target / source.name)],
                                 cwd=target, capture_output=True, text=True, check=True)
            fresh = json.loads((target / result_name).read_text())
            expected = json.loads((source.parent / result_name).read_text())
            if fresh != expected:
                raise AssertionError("frozen certificate differs: " + source_name)
            checks.append({"source": source_name,
                           "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                           "result": result_name, "matches_frozen_json": True,
                           "exit_code": run.returncode})
    result = {"status": "all exact certificates reproduced", "python": platform.python_version(),
              "arithmetic": "Python integers/Fraction in the certificate programs",
              "random_seed": None, "checks": checks,
              "command": "python3 research/topic_selection/probes/recheck_exact_certificates.py --output <new-path.json>",
              "limits": "No new random cases; floating LPs and the 4200/1200 fairness sweeps are not rerun here. Reproduction does not certify a general theorem or novelty."}
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(encoded)


if __name__ == "__main__":
    main()
