"""Finite falsification test for the all-p uniform full-menu budget.

For a fixed complete policy and fixed p, optimize all nonnegative unit-type
multiplicities subject to every true SPE row and W=1. No general conclusion
can be drawn from an absence of a positive optimum.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from itertools import product
import json
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
CASES = ['root_tax_failure', 'global_decorrelation_failure',
         'individual_security_failure', 'local_security_increment',
         'onpath_budget_failure']

def probe(name):
    cert = json.loads((ROOT / f'evidence/certificates/customer_attraction/{name}.json').read_text())
    policy = {tuple(row['history']): row['action'] for row in cert['strategy']['actions']}
    n = max(map(len,policy)) + 1
    k = max(policy.values()) + 1
    masks = range(1,1 << k)
    @lru_cache(None)
    def terminal(h):
        return h if len(h) == n else terminal(h+(policy[h],))
    def coeff(z,i):
        return [F(1,sum((mask>>a)&1 for a in z)) if (mask>>z[i])&1 else F(0)
                for mask in masks]
    query_cache={}
    def qcoeff(z,p):
        key=(z,tuple(p))
        if key not in query_cache:
            query_cache[key]=[sum((p[a] for a in range(k) if (mask>>a)&1),F(0)) /
                    (1+sum((mask>>a)&1 for a in z)) for mask in masks]
        return query_cache[key]
    z=terminal(())
    W=[int(any((mask>>a)&1 for a in z)) for mask in masks]
    gamma=[]
    for h in policy:
        own=coeff(terminal(h),len(h))
        for a in range(k):
            alt=coeff(terminal(h+(a,)),len(h))
            gamma.append([b-a for a,b in zip(own,alt)])
    # Each p gives an independent, precisely identified candidate test.
    queries = [[F(1,k)]*k]
    if 'security' in cert:
        queries.append(list(map(F,cert['security']['primary'])))
    for a in range(k):
        for b in range(a+1,k):
            p=[F(0)]*k;p[a]=p[b]=F(1,2);queries.append(p)
    best=None
    best_average=None
    for p in queries:
        rows=[list(map(float,g))+[0]*n for g in gamma]
        for i in range(n):
            for a in range(k):
                rows.append([-float(t) for t in qcoeff(terminal(z[:i]+(a,)),p)]
                            +[int(j==i) for j in range(n)])
        lp=linprog([0]*len(W)+[-1]*n,A_ub=rows,b_ub=[0]*len(rows),
                   A_eq=[W+[0]*n],b_eq=[1],bounds=[(0,None)]*(len(W)+n),method='highs')
        if lp.success and (best is None or -lp.fun>best['sum_R']):
            best={'policy':name,'p':list(map(str,p)),'sum_R':-lp.fun,
                  'gap':-lp.fun-1,'weights':{str(mask):float(v) for mask,v in zip(masks,lp.x[:len(W)]) if v>1e-8}}
        C=[sum((p[a]*qcoeff(terminal(z[:i]+(a,)),p)[j]
                for i in range(n) for a in range(k)),F(0)) for j in range(len(W))]
        avg_lp=linprog([-float(c) for c in C],A_ub=[list(map(float,g)) for g in gamma],
                       b_ub=[0]*len(gamma),A_eq=[W],b_eq=[1],bounds=[(0,None)]*len(W),method='highs')
        if avg_lp.success and (best_average is None or -avg_lp.fun>best_average['sum_C']):
            best_average={'p':list(map(str,p)),'sum_C':-avg_lp.fun,'gap':-avg_lp.fun-1,
                'weights':{str(mask):float(v) for mask,v in zip(masks,avg_lp.x) if v>1e-8}}
    cross_best=None
    for a in range(k):
        terminals=[terminal(z[:i]+(a,)) for i in range(n)]
        for t in range(k):
            p=[F(int(j==t)) for j in range(k)]
            C=[sum((qcoeff(zz,p)[j] for zz in terminals),F(0)) for j in range(len(W))]
            cross_lp=linprog([-float(c) for c in C],A_ub=[list(map(float,g)) for g in gamma],
                       b_ub=[0]*len(gamma),A_eq=[W],b_eq=[1],bounds=[(0,None)]*len(W),method='highs')
            if cross_lp.success and (cross_best is None or -cross_lp.fun>cross_best['sum_cross']):
                cross_best={'forced_action':a,'query_action':t,'sum_cross':-cross_lp.fun,'gap':-cross_lp.fun-1,
                    'weights':{str(mask):float(v) for mask,v in zip(masks,cross_lp.x) if v>1e-8}}
    return {'minimum_menu_test':best,'average_push_test':best_average,'cross_test':cross_best}

if __name__=='__main__':
    for name in CASES:
        print(json.dumps(probe(name)))
