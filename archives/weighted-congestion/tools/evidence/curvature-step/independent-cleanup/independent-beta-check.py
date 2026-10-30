#!/usr/bin/env python3
"""Independent finite reduced-table beta check, not a literal-resource audit.

No repository modules are imported. This tests the already proved step-cost
reduction on small DAGs, and does not verify polynomial equilibrium claims.
It writes only JSON to stdout; use shell redirection to retain a fresh run.
"""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import platform
from pathlib import Path


def run():
    parameters = [F(1), F(3, 2), F(2), F(7, 2), F(10)]
    graphs = cases = profiles = ratio_comparisons = attaining_states = 0
    for n in range(1, 5):
        possible = [(u, v) for u in range(n) for v in range(u + 1, n)]
        for bits in product((0, 1), repeat=len(possible)):
            edges = [edge for edge, bit in zip(possible, bits) if bit]
            graphs += 1
            for r in parameters:
                h = []
                for v in range(n):
                    h.append((1 + sum(h[u] for u, j in edges if j == v)) / r)
                expected = min(r, 1 + sum(h))
                factors = {}
                for mask in product((0, 1), repeat=n):
                    selected = {v for v, bit in enumerate(mask) if bit}
                    # Root is fixed to column a. The other root action is
                    # covered by the symmetric exchange of the two columns.
                    ratios = [(1 + sum(h[v] for v in selected)) /
                              (1 + sum(h[v] for v in range(n)
                                       if v not in selected))]
                    for v in range(n):
                        alternative = 1 + sum(h[u] for u, j in edges
                                              if j == v and u in selected)
                        ratios.append(h[v] / alternative if v in selected
                                      else alternative / h[v])
                    factors[mask] = max(F(1), *ratios)
                    profiles += 1
                    ratio_comparisons += len(ratios)
                assert min(factors.values()) == expected
                assert factors[(0,) * n] == r
                assert factors[(1,) * n] == 1 + sum(h)
                attaining_states += 2
                cases += 1
    return {
        "status": "passed",
        "arithmetic": "fractions.Fraction",
        "python": platform.python_version(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "seed": None,
        "inputs": {
            "graphs": "all forward-labelled simple DAGs on 1..4 vertices",
            "r_values": [str(r) for r in parameters],
            "amplitudes": "A0=1; Av=(1+sum incoming h)/r",
            "states": "all light-bit states with root fixed to column a",
        },
        "counts": {
            "graphs": graphs,
            "graph_r_cases": cases,
            "reduced_profiles": profiles,
            "positive_denominator_ratio_comparisons": ratio_comparisons,
            "explicit_all_out_and_all_in_factor_checks": attaining_states,
        },
        "claim_checked": "min_state max(1, player deviation ratios) = min(r,1+sum h)",
        "scope": "finite reduced-table arithmetic check; no literal loads, polynomial costs, or universal inference",
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
