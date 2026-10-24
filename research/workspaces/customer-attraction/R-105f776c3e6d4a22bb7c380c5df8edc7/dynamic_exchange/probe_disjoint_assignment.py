"""Targeted diagnostic for the seq242 static optimal-tuple assignment bridge.

This is one named candidate attack, not a scan of Q-CAG-HALF.  Search only a
six-label, three-player fresh-action subset-potential gadget with actual
(0,3,4), disjoint unique optimal support (1,2,5), actual signed utilities
(-1,0,0), and every static target assignment cost at least zero.
An integer solution must be replayed independently and compiled before use.
"""
import json
from itertools import combinations, permutations
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

P = tuple(range(6))
actual = (0, 3, 4)
target = (1, 2, 5)
BIG = 100
names = []
lb, ub, integral = [], [], []


def var(name, lo=-30, hi=30, integer=False):
    idx = len(names)
    names.append(name)
    lb.append(lo)
    ub.append(hi)
    integral.append(int(integer))
    return idx


F = {s: var(('F', s), -10, 10, True)
     for k in (2, 3) for s in combinations(P, k)}
y = {(a, b, c): var(('last', a, b, c), 0, 1, True)
     for a in P for b in P if b != a
     for c in P if c not in (a, b)}
z = {(a, b): var(('second', a, b), 0, 1, True)
     for a in P for b in P if a != b}
p2 = {(a, b): var(('p2', a, b)) for a, b in z}
q1 = {(a, b): var(('q1', a, b)) for a, b in z}
u1 = {a: var(('u1', a)) for a in P}
rows = []
rowlb, rowub = [], []


def row(coeff, lo=-np.inf, hi=np.inf):
    rows.append(coeff)
    rowlb.append(lo)
    rowub.append(hi)


def fs(items):
    return F[tuple(sorted(items))]


def combine(*terms):
    out = {}
    for coef, idx in terms:
        out[idx] = out.get(idx, 0) + coef
    return {k: v for k, v in out.items() if v}


for a in P:
    row({z[a, b]: 1 for b in P if b != a}, 1, 1)
    for b in P:
        if b == a:
            continue
        row({y[a, b, c]: 1 for c in P if c not in (a, b)}, 1, 1)
        for c in P:
            if c in (a, b):
                continue
            yi = y[a, b, c]
            for d in P:
                if d in (a, b):
                    continue
                # Chosen terminal has maximum subset potential.
                row(combine((1, fs((a, b, c))),
                            (-1, fs((a, b, d))), (-BIG, yi)), lo=-BIG)
            for payoff, deleted in ((p2[a, b], (a, c)),
                                    (q1[a, b], (b, c))):
                expr = combine((1, payoff), (-1, fs((a, b, c))),
                               (1, fs(deleted)))
                row({**expr, yi: BIG}, hi=BIG)
                row({**expr, yi: -BIG}, lo=-BIG)
        zi = z[a, b]
        for d in P:
            if d != a:
                row(combine((1, p2[a, b]), (-1, p2[a, d]),
                            (-BIG, zi)), lo=-BIG)
        row(combine((1, u1[a]), (-1, q1[a, b]), (BIG, zi)), hi=BIG)
        row(combine((1, u1[a]), (-1, q1[a, b]), (-BIG, zi)), lo=-BIG)
    row(combine((1, u1[0]), (-1, u1[a])), lo=0)

for s, value in (((0, 3, 4), 0), ((0, 4), 0), ((0, 3), 0), ((3, 4), 1)):
    row({fs(s): 1}, value, value)
row({z[0, 3]: 1}, 1, 1)
row({y[0, 3, 4]: 1}, 1, 1)


def welfare(s):
    return combine((3, fs(s)), *((-1, fs(t)) for t in combinations(s, 2)))


wt = welfare(target)
for s in combinations(P, 3):
    if s == target:
        continue
    coeff = dict(wt)
    for idx, coef in welfare(s).items():
        coeff[idx] = coeff.get(idx, 0) - coef
    row(coeff, lo=1)

for perm in permutations(target):
    coeff = {}
    for i, t in enumerate(perm):
        bg = tuple(a for j, a in enumerate(actual) if i != j)
        for idx, coef in ((fs(bg + (t,)), 1), (fs(bg), -1)):
            coeff[idx] = coeff.get(idx, 0) + coef
    row(coeff, lo=0)  # actual signed welfare is -1

A = lil_matrix((len(rows), len(names)))
for i, coeff in enumerate(rows):
    for j, coef in coeff.items():
        A[i, j] = coef
result = milp(np.zeros(len(names)), integrality=np.array(integral),
              bounds=Bounds(lb, ub),
              constraints=LinearConstraint(A.tocsr(), rowlb, rowub),
              options={'time_limit': 55})
out = {'status': int(result.status), 'message': result.message,
       'variables': len(names), 'constraints': len(rows)}
if result.x is not None:
    rounded = np.rint(result.x).astype(int)
    if np.max(np.abs(rounded - result.x)) > 1e-5:
        out['nonintegral_payoff_variables'] = True
    out['F'] = {','.join(map(str, s)): int(rounded[i]) for s, i in F.items()}
    out['second'] = {str(a): b for (a, b), i in z.items() if rounded[i]}
    out['last'] = {f'{a},{b}': c for (a, b, c), i in y.items() if rounded[i]}
Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items()
                  if k not in ('F', 'second', 'last')}, indent=2))
