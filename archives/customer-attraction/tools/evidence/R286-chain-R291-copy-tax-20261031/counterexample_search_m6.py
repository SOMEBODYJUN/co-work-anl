"""Exact finite attack on six-player Q-CAG-HALF.

This is deliberately a search certificate, not a proof of the general claim.
It uses the repository's exact pure-SPE outcome recurrence and then cross-checks
the extremal records with the independent Fraction solver.
"""
from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tests" / "audits"))
from customer_attraction_search import (  # noqa: E402
    canonical_confirm,
    exact_outcomes,
    instance_record,
)


def run_p3():
    """All 4^7-1 nonzero type multiplicity vectors, k=3,m=6."""
    best = Fraction(1)
    best_record = None
    violations = []
    count = 0
    for weights in itertools.product(range(4), repeat=7):
        if not any(weights):
            continue
        data = exact_outcomes(3, 6, weights)
        count += 1
        ratio = Fraction(data["worst"], data["optimum"]) if data["optimum"] else Fraction(1)
        if ratio < best:
            best = ratio
            best_record = instance_record(3, 6, weights, data)
        if 2 * data["worst"] < data["optimum"]:
            violations.append(instance_record(3, 6, weights, data))
    assert best_record is not None
    assert canonical_confirm(best_record)
    return {
        "domain": "all nonzero vectors in {0,1,2,3}^7",
        "catalog_size": 3,
        "players": 6,
        "instances": count,
        "half_violations": len(violations),
        "minimum_ratio": str(best),
        "minimum_record": best_record,
    }


def run_p4_single_pair():
    """All 3^10-1 vectors on singleton and pair customer types, k=4,m=6."""
    masks = [1, 2, 4, 8, 3, 5, 9, 6, 10, 12]
    best = Fraction(1)
    best_record = None
    violations = []
    count = 0
    for values in itertools.product(range(3), repeat=len(masks)):
        weights = [0] * 15
        for mask, value in zip(masks, values):
            weights[mask - 1] = value
        if not any(weights):
            continue
        weights = tuple(weights)
        data = exact_outcomes(4, 6, weights)
        count += 1
        ratio = Fraction(data["worst"], data["optimum"]) if data["optimum"] else Fraction(1)
        if ratio < best:
            best = ratio
            best_record = instance_record(4, 6, weights, data)
        if 2 * data["worst"] < data["optimum"]:
            violations.append(instance_record(4, 6, weights, data))
    assert best_record is not None
    assert canonical_confirm(best_record)
    return {
        "domain": "singleton and pair types only, multiplicities in {0,1,2}",
        "catalog_size": 4,
        "players": 6,
        "instances": count,
        "half_violations": len(violations),
        "minimum_ratio": str(best),
        "minimum_record": best_record,
    }


if __name__ == "__main__":
    result = {"p3": run_p3(), "p4_single_pair": run_p4_single_pair()}
    print(json.dumps(result, ensure_ascii=False, indent=2))
