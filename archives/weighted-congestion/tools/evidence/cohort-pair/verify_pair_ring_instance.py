#!/usr/bin/env python3
"""New exact literal check of the frozen pure-pair quadratic example."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
weights = (Q(1), Q(3), Q(2))
coefficients = (Q(1), Q(11,25), Q(93,50))
def costs(bits):
    result = [Q(0)] * 3
    for edge, coefficient in enumerate(coefficients):
        users = (edge, (edge+1)%3)
        for player in users:
            load = sum(weights[j] for j in users if bits[j] == bits[player])
            result[player] += coefficient * load**2
    return result
rows = []
for state in product((0,1), repeat=3):
    current = costs(state)
    after = [costs(tuple(1-b if i == j else b for j,b in enumerate(state)))[i]
             for i in range(3)]
    ratios = [a/b for a,b in zip(current,after)]
    rows.append(dict(state=state, current=current, deviations=after,
                     ratios=ratios, factor=max(Q(1),*ratios)))
assert min(row['factor'] for row in rows) == Q(500,499)
assert all(row['factor'] > 1 for row in rows)
report = dict(scope='one fixed quadratic pure pair ring; all eight states and all true unilateral flips',
              weights=weights, coefficients=coefficients, degree=2, best_factor=Q(500,499),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), rows=rows)
print(json.dumps(report, default=str, indent=2))
