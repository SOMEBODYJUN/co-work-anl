"""Simplify the one discovered assignment witness, keeping its full policy."""
import json
from itertools import combinations, permutations
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

ROOT = Path(__file__).parent
source = json.loads((ROOT / 'probe_disjoint_assignment.json').read_text())
second = {int(a): b for a, b in source['second'].items()}
last = {tuple(map(int, h.split(','))): a for h, a in source['last'].items()}
P = tuple(range(6))
subsets = tuple(s for k in (2, 3) for s in combinations(P, k))
index = {s: i for i, s in enumerate(subsets)}
n = len(subsets)
rows, lows, highs = [], [], []


def expr(items):
    out = {}
    for c, s in items:
        idx = index[tuple(sorted(s))]
        out[idx] = out.get(idx, 0) + c
    return out


def add(items, lo=-np.inf, hi=np.inf):
    rows.append(expr(items))
    lows.append(lo)
    highs.append(hi)


def pay(a, b, c, who):
    return [(1, (a, b, c)), (-1, tuple(x for x in (a, b, c) if x != who))]


def neg(items):
    return [(-c, s) for c, s in items]


for a, b in last:
    c = last[a, b]
    for d in P:
        if d not in (a, b):
            add([(1, (a, b, c)), (-1, (a, b, d))], lo=0)
for a in P:
    b = second[a]
    c = last[a, b]
    for d in P:
        if d != a:
            e = last[a, d]
            add(pay(a, b, c, b) + neg(pay(a, d, e, d)), lo=0)
    add(pay(0, second[0], last[0, second[0]], 0)
        + neg(pay(a, b, c, a)), lo=0)
for s, v in (((0, 3, 4), 0), ((0, 4), 0), ((0, 3), 0), ((3, 4), 1)):
    add([(1, s)], lo=v, hi=v)


def welfare(s):
    return [(3, s)] + [(-1, t) for t in combinations(s, 2)]


target = (1, 2, 5)
actual = (0, 3, 4)
for s in combinations(P, 3):
    if s != target:
        add(welfare(target) + neg(welfare(s)), lo=1)
for perm in permutations(target):
    terms = []
    for i, a in enumerate(perm):
        bg = tuple(x for j, x in enumerate(actual) if j != i)
        terms += [(1, bg + (a,)), (-1, bg)]
    add(terms, lo=0)

for i in range(n):
    rows += [{i: 1, n+i: -1}, {i: -1, n+i: -1}]
    lows += [-np.inf, -np.inf]
    highs += [0, 0]
A = lil_matrix((len(rows), 2*n))
for i, row in enumerate(rows):
    for j, value in row.items():
        A[i, j] = value
result = milp(np.array([0]*n + [1]*n), integrality=np.ones(2*n),
              bounds=Bounds([-10]*n+[0]*n, [10]*n+[10]*n),
              constraints=LinearConstraint(A.tocsr(), lows, highs),
              options={'time_limit': 55})
assert result.status == 0, result.message
values = np.rint(result.x[:n]).astype(int)
out = {'status': 'integer discovery witness; requires exact replay',
       'actual': list(actual), 'target': list(target),
       'F': {','.join(map(str, s)): int(values[i]) for s, i in index.items()
             if values[i]},
       'second': source['second'], 'last': source['last']}
(ROOT/'assignment_witness.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({'l1': int(sum(abs(values))), 'nonzero_F': len(out['F'])}))
