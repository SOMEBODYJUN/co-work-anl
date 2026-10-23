"""One fixed full-SPE policy diagnoses the all-input direct coverage floor.

Candidate: each player's realized payoff is at least OPT_m/(2m).
This is not a search for the original half-welfare conjecture.
The 6-action policy is the existing X/Y credible-response policy; only this
single policy and comparison tuple (0,1,2) are used.  Floating LP proposes a
point; Fraction independently checks every full-history SPE row before output.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import lcm
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

M = 3
K = 6
MASKS = range(1, 1 << K)


def action(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return next(a for a in group if a not in h)


def follow(h):
    h = tuple(h)
    while len(h) < M:
        h += (action(h),)
    return h


def utility(mask, z, who):
    if not (mask >> z[who]) & 1:
        return F(0)
    return F(1, sum((mask >> a) & 1 for a in z))


HISTORIES = [h for d in range(M) for h in product(range(K), repeat=d)]
ROWS = []
for h in HISTORIES:
    z = follow(h)
    i = len(h)
    for a in range(K):
        za = follow(h + (a,))
        ROWS.append([utility(mask, z, i) - utility(mask, za, i) for mask in MASKS])

Z = follow(())
comparison = (0, 1, 2)
OBJ = [F(any((mask >> a) & 1 for a in comparison)) - 2*M*utility(mask, Z, 0)
       for mask in MASKS]
res = linprog(-np.array(OBJ, dtype=float), A_ub=-np.array(ROWS, dtype=float),
              b_ub=np.zeros(len(ROWS)), A_eq=np.ones((1, len(MASKS))), b_eq=[1],
              bounds=(0, None), method='highs')
assert res.success, res.message
point = [F(float(x)).limit_denominator(10**6) for x in res.x]
den = lcm(*(v.denominator for v in point))
counts = [int(v*den) for v in point]
slacks = [sum(v*n for v,n in zip(row,counts)) for row in ROWS]
assert min(slacks) >= 0, "Floating proposal failed exact full-tree IC"
customers = [(mask,n) for mask,n in zip(MASKS,counts) if n]
root = sum(utility(mask,Z,0)*n for mask,n in customers)
payoffs = [sum(utility(mask,Z,i)*n for mask,n in customers) for i in range(M)]
cov = lambda z: sum(n for mask,n in customers if any((mask>>a)&1 for a in z))
opt = max(cov(z) for z in product(range(K),repeat=M))
out = dict(candidate='all-player direct coverage floor u_i >= OPT_m/(2m)',
           status='counterexample' if opt>2*M*root else 'not separated in this one fixed cone',
           players=M, topics=K, customers=customers, path=Z,
           payoffs=list(map(str,payoffs)), welfare=cov(Z), opt=opt,
           direct_floor_gap=str(F(opt)-2*M*root),
           comparison_gap=str(sum(v*n for v,n in zip(OBJ,counts))),
           complete_histories=len(HISTORIES), compared_actions=len(ROWS),
           smallest_exact_ic=str(min(slacks)),
           root_action_rule='0',
           second_action_rule='other group minimum',
           last_action_rule='minimum unused in second action group')
print(json.dumps(out,ensure_ascii=False,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
