"""Focused falsification of aggregate complete-terminal push, one formal policy.

This is not a target counterexample search and negative LP values prove nothing.
The candidate is sum_i E_{A,T iid p} K_i(T,A) <= actual W for all p.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math
import numpy as np
from scipy.optimize import linprog

M, K = 3, 6
TYPES = list(range(1, 1 << K))
MEM = np.array([[(b >> a) & 1 for a in range(K)] for b in TYPES])
L = math.lcm(*range(1, M + 2))

def action(h):
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(0, 3) if h[1] < 3 else range(3, 6)
    return next(a for a in group if a not in h)

def finish(h):
    h = tuple(h)
    while len(h) < M:
        h += (action(h),)
    return h

def payoff(a, z):
    load = MEM @ np.bincount(z, minlength=K)
    v = np.zeros(len(TYPES), dtype=int)
    hit = MEM[:, a] > 0
    v[hit] = L // load[hit]
    return v

IC = []
for i in range(M):
    for h in product(range(K), repeat=i):
        u = payoff(action(h), finish(h))
        for a in range(K):
            IC.append(u - payoff(a, finish(h + (a,))))
IC = np.array(IC, dtype=float) / L
Z = finish(())
covered = (MEM @ np.bincount(Z, minlength=K) > 0).astype(float)

def kernels(p):
    q = MEM @ np.array(p, dtype=float)
    return np.array([[q / (1 + MEM @ np.bincount(finish(Z[:i]+(a,)), minlength=K))
                      for a in range(K)] for i in range(M)])

def test(p):
    prices = kernels(p)
    push = np.einsum('a,iab->b', np.array(p,dtype=float), prices)
    delta = push - covered
    res = linprog(-delta, A_ub=-IC, b_ub=np.zeros(len(IC)),
                  A_eq=[np.ones(len(TYPES))], b_eq=[1], bounds=(0,None))
    assert res.success
    return dict(p=list(map(str,p)), gap=float(-res.fun),
                weights={str(TYPES[j]):str(F(float(x)).limit_denominator(10**7))
                         for j,x in enumerate(res.x) if x>1e-8})

def uniform_budget(p):
    prices = kernels(p)
    # Variables customer weights and one freely chosen minimum for each role.
    rows=[]
    for i in range(M):
        for a in range(K):
            r=np.zeros(len(TYPES)+M)
            r[:len(TYPES)]=-prices[i,a]
            r[len(TYPES)+i]=1
            rows.append(r)
    c=np.r_[covered,-np.ones(M)]
    res=linprog(c,A_ub=np.vstack([np.c_[-IC,np.zeros((len(IC),M))],rows]),
                b_ub=np.zeros(len(IC)+M*K),
                A_eq=[np.r_[np.ones(len(TYPES)),np.zeros(M)]],b_eq=[1],
                bounds=[(0,None)]*len(TYPES)+[(None,None)]*M)
    assert res.success
    return dict(p=list(map(str,p)),gap=float(-res.fun),
                weights={str(TYPES[j]):str(F(float(x)).limit_denominator(10**7))
                         for j,x in enumerate(res.x[:len(TYPES)]) if x>1e-8})

P=[[F(0),F(0),F(1,2),F(0),F(0),F(1,2)], [F(1,6)]*6]
out=dict(candidate='aggregate complete-terminal push <= W', policy='fixed 3-player two-group formal policy',
         all_history_IC=len(IC), types=len(TYPES),
         push=[test(p) for p in P], uniform=[uniform_budget(p) for p in P],
         warning='Floating proposals only; negative results are not certificates.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
