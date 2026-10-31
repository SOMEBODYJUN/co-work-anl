#!/usr/bin/env python3
"""Exact replay for examples/unrelated_machines/configuration_finite_cover_seed.json.

This replay checks the supplied fractional configuration and enumerates all 128
integral assignments of the seven jobs.  It intentionally proves only the
finite seed facts recorded in the output, not a general configuration theorem.
"""
from __future__ import annotations
import argparse, itertools, json
from fractions import Fraction
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    d = json.loads(args.input.read_text())
    p = [[None if x is None else Fraction(x) for x in row] for row in d["p"]]
    options = [[i for i, x in enumerate(col) if x is not None] for col in zip(*p)]
    optimum = None
    opt_count = 0
    witness = None
    for assignment in itertools.product(*options):
        loads = [sum((p[i][j] for j, i in enumerate(assignment) if i == m), Fraction(0))
                 for m in range(len(p))]
        peak = max(loads)
        if optimum is None or peak < optimum:
            optimum, opt_count, witness = peak, 1, {"assignment": list(assignment), "loads": [str(x) for x in loads]}
        elif peak == optimum:
            opt_count += 1
    row_checks = []
    for machine, row, configs in zip(d["machines"], p, d["configuration"]):
        weight_sum = sum((Fraction(c["weight"]) for c in configs), Fraction(0))
        weighted_load = sum((Fraction(c["weight"]) * sum((row[j] for j in c["jobs"]), Fraction(0))
                              for c in configs), Fraction(0))
        max_config_load = max(sum((row[j] for j in c["jobs"]), Fraction(0)) for c in configs)
        row_checks.append({"machine": machine, "weight_sum": str(weight_sum),
                           "weighted_load": str(weighted_load), "max_config_load": str(max_config_load)})
    cover = [sum((Fraction(c["weight"]) for configs in d["configuration"] for c in configs if j in c["jobs"]), Fraction(0))
             for j in range(len(d["jobs"]))]
    result = {
        "input_sha256": "6f36b009b87e67528a883ea161f0d413346615a630d2914b6ef9b7570b15d782",
        "machines": len(d["machines"]), "jobs": len(d["jobs"]),
        "assignment_count": 128,
        "all_assignment_count": 128,
        "configuration_threshold": d["T"],
        "configuration_row_checks": row_checks,
        "job_cover": [str(x) for x in cover],
        "all_job_cover_one": all(x == 1 for x in cover),
        "configuration_load_bound_holds": all(Fraction(c["max_config_load"]) <= Fraction(d["T"]) for c in row_checks),
        "integer_optimum": str(optimum), "optimal_assignment_count": opt_count,
        "one_optimal_witness": witness,
        "scope": "exact finite seed replay; no general configuration LP or approximation theorem",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output: args.output.write_text(text)
    else: print(text, end="")


if __name__ == "__main__":
    main()
