"""Audit one literal complete-assignment rounding contract, not BMKP's theorem.

No search, no seed: Fraction confirms a feasible fractional point and exhausts
all complete integer assignments. Optional discard has a feasible empty output.
"""
from fractions import Fraction as F
from itertools import product
import json


def audit():
    weights = [F(2)]
    profits = [F(1, 100)]
    capacities = [F(1), F(1)]
    fractional = [F(1, 2), F(1, 2)]
    targets = [profits[0] * x for x in fractional]
    assert sum(fractional) == 1
    assert all(weights[0] * x <= b for x, b in zip(fractional, capacities))
    full_assignments = list(product((0, 1), repeat=len(capacities)))
    valid = [a for a in full_assignments if sum(a) == 1 and
             all(weights[0] * x <= b for x, b in zip(a, capacities))]
    assert valid == []
    assert all(F(0) >= t - 2 * max(profits) for t in targets)
    return {
        "weights": list(map(str, weights)), "profits": list(map(str, profits)),
        "capacities": list(map(str, capacities)),
        "fractional": list(map(str, fractional)), "targets": list(map(str, targets)),
        "fractional_feasible": True, "complete_integer_feasible": valid,
        "discard_variant_not_refuted": True,
        "scope": "Literal all-item coverage plus exact capacity, without edge eligibility; not a refutation of BMKP's main theorem or discard rounding.",
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
