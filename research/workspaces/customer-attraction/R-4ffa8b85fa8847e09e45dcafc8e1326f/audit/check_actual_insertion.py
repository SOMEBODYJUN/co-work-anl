"""Attack only: max_T extra-query(T,z) <= W(z)/m for arbitrary SPE.

Uses the existing six-label, three-position full policy as a probe. A positive
LP candidate is rechecked with Fractions on every ordered history.
"""
from fractions import Fraction as F
from itertools import product
from math import lcm, gcd
import json
import numpy as np
from scipy.optimize import linprog

m, k = 3, 6
masks = tuple(range(1, 1 << k))

def policy(h):
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return next(t for t in group if t not in h)

def terminal(h):
    h = tuple(h)
    while len(h) < m:
        h += (policy(h),)
    return h

def payoff(z, i, mask):
    return F(bool(mask >> z[i] & 1), sum(mask >> t & 1 for t in z) or 1)

rows = []
for depth in range(m):
    for h in product(range(k), repeat=depth):
        z = terminal(h)
        for a in range(k):
            za = terminal(h + (a,))
            rows.append(tuple(payoff(z, depth, b) - payoff(za, depth, b) for b in masks))
z = terminal(())
welfare = tuple(F(any(b >> t & 1 for t in z)) for b in masks)
out = []
for t in range(k):
    delta = tuple(m * F(bool(b >> t & 1), 1 + sum(b >> a & 1 for a in z)) - w
                  for b, w in zip(masks, welfare))
    res = linprog(-np.array(delta, dtype=float), A_ub=-np.array(rows, dtype=float),
                  b_ub=np.zeros(len(rows)), A_eq=[welfare], b_eq=[1],
                  bounds=(0, None), method="highs")
    if not res.success:
        out.append({"query": t, "status": res.message})
        continue
    point = [F(float(x)).limit_denominator(10**7) for x in res.x]
    den = lcm(*(x.denominator for x in point))
    ints = [int(x * den) for x in point]
    common = gcd(*ints)
    ints = [x // common for x in ints]
    exact_delta = sum(c * x for c, x in zip(delta, ints))
    exact_min_ic = min(sum(c * x for c, x in zip(row, ints)) for row in rows)
    W = sum(c * x for c, x in zip(welfare, ints))
    out.append({"query": t, "float_delta_per_W": -res.fun,
                "exact_delta": str(exact_delta), "min_ic": str(exact_min_ic),
                "W": str(W), "path": z,
                "positive_types": {str(b): x for b, x in zip(masks, ints) if x}})
print(json.dumps(out, ensure_ascii=False, indent=2))
