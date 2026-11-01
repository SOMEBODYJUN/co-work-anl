#!/usr/bin/env python3
"""Exact finite profiles for the q-job compression obstruction, not its proof."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform


def feasible(matrix, capacities):
    options = [[i for i, row in enumerate(matrix)
                if row[j] is not None and row[j] <= capacities[i]]
               for j in range(len(matrix[0]))]
    count, found = 0, False
    for assignment in product(*options):
        count += 1
        loads = [F(0) for _ in matrix]
        for j, i in enumerate(assignment):
            loads[i] += matrix[i][j]
        if all(x <= c for x, c in zip(loads, capacities)):
            found = True
    return found, count


def audit():
    profiles = []
    for q in range(2, 9):
        n = q+1
        matrix = [[F(1) for _ in range(n)]]
        matrix += [[F(1, q) if i == j else F(2) for j in range(n)]
                   for i in range(n)]
        good = bad = assignments = 0
        for active in combinations(range(n), q):
            capacities = [F(1)] + [F(1, q) if i in active else F(0)
                                    for i in range(n)]
            ok, count = feasible(matrix, capacities)
            assert ok
            good += 1
            assignments += count
        for size in range(q):
            for active in combinations(range(n), size):
                capacities = [F(1)] + [F(1) if i in active else F(0)
                                        for i in range(n)]
                ok, count = feasible(matrix, capacities)
                assert not ok
                bad += 1
                assignments += count
        assert q+1 < 2*q
        profiles.append({'q': q, 'feasible_A_profiles': good,
                         'infeasible_B_profiles': bad,
                         'all_pruned_assignments_checked': assignments})
    # Two precise failures discussed by boss4: duplicate minima lose identity;
    # rank envelopes keep reverse lift but can lose forward feasibility.
    original = [[F(1)]*3, [F(0), F(2), F(2)]]
    assert not feasible(original, [F(1), F(1)])[0]
    assert feasible([[F(0), F(0)]], [F(1)])[0]
    original = [[F(1)]*3, [F(0), F(2), F(2)], [F(2), F(0), F(2)]]
    assert feasible(original, [F(1)]*3)[0]
    assert not feasible([[F(0), F(2)], [F(0), F(2)]], [F(1)]*2)[0]
    return {'python_version': platform.python_version(),
            'arithmetic': 'fractions.Fraction, exact; deterministic',
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'source_of_mathematical_obstruction': 'boss4 public message 5f557aa15a544f7aa7d02e24549b6ca1',
            'profiles': profiles, 'specific_envelope_counterexamples': 2,
            'limits': 'Finite original-star profiles only; arbitrary replacement matrices are excluded by the separate universal proof, not enumerated here.'}


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
