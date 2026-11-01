#!/usr/bin/env python3
"""Finite exact arithmetic only; the general bounds are proved in the review."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
primary = HERE / 'capture_occupation_and_source_margin.md'
assert len(primary.read_bytes()) == 4134
assert hashlib.sha256(primary.read_bytes()).hexdigest() == (
    '645591887ff6f022c31ea113d85c220ba57bb2e063aee64d439abf16064b455f'
)

v = [F(0)]
maximizers = {}
for k in range(1, 5):
    options = {
        d: sum((1 + v[l] for l in range(k - d, k)), F(0)) / (d + 1)
        for d in range(1, k + 1)
    }
    v.append(max(options.values()))
    maximizers[str(k)] = [d for d, value in options.items() if value == v[k]]
assert v[1:] == [F(1, 2), F(5, 6), F(10, 9), F(49, 36)]

edges = {1: [2, 3], 2: [3, 4], 3: [4], 4: []}
targets = {2, 3, 4}
visits, hit = {}, {}
for role in reversed(range(1, 5)):
    children = edges[role]
    visits[role] = F(role in targets) + sum(
        (visits[j] for j in children), F(0)
    ) / (len(children) + 1)
    hit[role] = F(1) if role in targets else sum(
        (hit[j] for j in children), F(0)
    ) / (len(children) + 1)
harmonic_comparator = sum((F(1, j) for j in range(2, 5)), F(0))
assert visits[1] == F(10, 9)
assert [visits[j] for j in [2, 3, 4]] == [F(11, 6), F(3, 2), F(1)]
assert harmonic_comparator == F(13, 12)
assert visits[1] - harmonic_comparator == F(1, 36)
assert hit[1] == F(2, 3) <= F(3, 4)

result = {
    'scope': 'finite Fraction arithmetic; no CAG instance or SPE realization claimed',
    'primary_sha256_verified': True,
    'recurrence_values': {str(k): str(value) for k, value in enumerate(v)},
    'maximizing_d': maximizers,
    'example_edges': edges,
    'target_state_total_visits': {str(j): str(visits[j]) for j in [2, 3, 4]},
    'initial_total_visits': str(visits[1]),
    'harmonic_comparator': str(harmonic_comparator),
    'excess': str(visits[1] - harmonic_comparator),
    'probability_of_any_target_hit': str(hit[1]),
    'hit_upper_bound': '3/4',
}
out = HERE / 'arithmetic-check.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
