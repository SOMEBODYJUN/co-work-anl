#!/usr/bin/env python3
"""Finite audit of the dynamic-Theta candidate.

This is evidence only.  It exhausts all 3-theme customer multiplicity vectors
with each of the seven nonempty signatures having multiplicity 0, 1, or 2,
for m=6.  For every realized ordered pure-SPE path it computes
W + sum_i Theta_i - OPT, where Theta_i is the exact threshold returned by
ExactSPESolver at the path's prefix count.  A negative value would refute the
candidate in this finite class; no negative value is interpreted as a theorem.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
from customer_attraction import CustomerType, ExactSPESolver, Instance


def run() -> dict:
    p, m = 3, 6
    signatures = [frozenset(i for i in range(p) if mask >> i & 1)
                  for mask in range(1, 1 << p)]
    instances = paths = 0
    min_slack: Fraction | None = None
    witness = None
    for mults in product(range(3), repeat=len(signatures)):
        customers = tuple(CustomerType(sig, mult)
                          for sig, mult in zip(signatures, mults) if mult)
        if not customers:
            continue
        instance = Instance(tuple(f"T{i}" for i in range(p)), customers, m)
        solver = ExactSPESolver(instance)
        optimum = instance.optimal_welfare()
        for path in solver.ordered_outcomes():
            counts = (0,) * p
            theta_sum = Fraction(0)
            for action in path:
                theta_sum += solver.threshold(counts)
                nxt = list(counts)
                nxt[action] += 1
                counts = tuple(nxt)
            slack = Fraction(instance.welfare(counts)) + theta_sum - optimum
            paths += 1
            if min_slack is None or slack < min_slack:
                min_slack = slack
                witness = {
                    "multiplicities": list(mults),
                    "path": list(path),
                    "terminal_counts": list(counts),
                    "welfare": instance.welfare(counts),
                    "optimum": optimum,
                    "theta_sum": str(theta_sum),
                }
            if slack < 0:
                raise AssertionError({"slack": str(slack), "witness": witness,
                                      "instance": instance.to_dict()})
        instances += 1
    return {
        "topics": p,
        "players": m,
        "signature_multiplicity_range": [0, 2],
        "instances": instances,
        "ordered_spe_paths": paths,
        "minimum_slack": str(min_slack),
        "witness": witness,
        "status": "finite_audit_only",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
