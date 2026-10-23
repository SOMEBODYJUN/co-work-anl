"""Exact finite checks for the background-uncovered credit obstruction.

The arbitrary-r proof is in uncovered_background_credit_obstruction.md.
This file uses the repository solver only to reconstruct and independently
verify complete SPE certificates in the stated finite range.
"""

import json
from fractions import Fraction as Q
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from customer_attraction import (CustomerType, ExactSPESolver, Instance,
                                 verify_certificate)


def compositions(total, width):
    if width == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, width - 1):
                yield (first,) + rest


def audit(r):
    inst = Instance(("A", "B") + tuple(f"L{j}" for j in range(r - 1)),
                    (CustomerType(frozenset({0}), 2),
                     CustomerType(frozenset({1}), r)) + tuple(
                        CustomerType(frozenset({j + 2})) for j in range(r - 1)),
                    r + 1)
    path = (0,) + (1,) * r
    solver = ExactSPESolver(inst)
    cert = solver.certificate(on_path=path)
    report = verify_certificate(inst, cert)
    report.assert_valid()
    assert inst.player_payoffs(path) == (Q(2),) + (Q(1),) * r
    best = Q(0)
    scanned = 0
    for c in compositions(r, r + 1):
        scanned += 1
        value = Q(0)
        for customer in inst.customers:
            tail_load = sum(c[a] for a in customer.topics)
            bg_load = int(0 in customer.topics)
            if tail_load:
                value += Q(customer.multiplicity * tail_load, bg_load + tail_load)
        best = max(best, value)
    assert best == 2 * r - 1
    return {"r": r, "histories": len(cert.actions), "tail_combinations": scanned,
            "actual_tail_profit": r, "exact_Ftail": str(best)}


def main():
    rows = [audit(r) for r in range(1, 6)]
    # n=64 is one exact common arity at which all three forced bounds conflict.
    n = 64
    h = min(Q(j) + Q(n, j) for j in range(1, n + 1))
    shared_lower = Q(2 - h, n)
    uncovered_lower = Q(-1, 2)
    joint_upper = (Q(23 - 5 * n, 6) - Q(2, n)) / (n - 1)
    assert shared_lower + uncovered_lower > joint_upper
    print(json.dumps({"finite_SPE_and_profit_checks": rows,
                      "common_r": n - 1,
                      "h_n": str(h),
                      "shared_credit_lower": str(shared_lower),
                      "uncovered_credit_lower": str(uncovered_lower),
                      "joint_lower": str(shared_lower + uncovered_lower),
                      "joint_upper": str(joint_upper),
                      "contradiction_gap": str(shared_lower + uncovered_lower - joint_upper)},
                     indent=2))


if __name__ == "__main__":
    main()
