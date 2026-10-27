"""Exact finite six-player search: all binary customer-type weights on 4 topics.

This searches all 2^15-1 nonzero vectors for the 15 nonempty customer types,
keeps every history-dependent pure-SPE terminal count vector, and independently
rechecks the extremal record with customer_attraction.ExactSPESolver.
It is finite evidence only; it is not a proof of Q-CAG-HALF-6.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tests" / "audits"))
from customer_attraction_search import canonical_confirm, exact_outcomes, instance_record  # noqa: E402


def main() -> None:
    best = Fraction(1)
    best_record = None
    violations = []
    count = 0
    for values in itertools.product(range(2), repeat=15):
        if not any(values):
            continue
        weights = tuple(values)
        data = exact_outcomes(4, 6, weights)
        count += 1
        ratio = Fraction(data["worst"], data["optimum"]) if data["optimum"] else Fraction(1)
        if best_record is None or ratio < best:
            best = ratio
            best_record = instance_record(4, 6, weights, data)
        if 2 * data["worst"] < data["optimum"]:
            violations.append(instance_record(4, 6, weights, data))
    assert best_record is not None
    assert canonical_confirm(best_record)
    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "status": "completed",
        "claim_status": "finite_evidence_only",
        "domain": "all nonzero vectors in {0,1}^15 over every nonempty customer type on 4 topics",
        "catalog_size": 4,
        "players": 6,
        "instances": count,
        "all_history_dependent_pure_spe_outcomes": True,
        "half_violations": len(violations),
        "minimum_welfare_ratio": str(best),
        "minimum_record": best_record,
        "independent_fraction_recheck": "passed for minimum_record",
        "script_sha256": script_hash,
    }
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
