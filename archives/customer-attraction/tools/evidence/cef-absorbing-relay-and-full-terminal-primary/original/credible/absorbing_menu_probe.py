"""Test one explicit all-history candidate, not unrestricted instance search.

Candidate: after first topic t, every remaining player always chooses f(t).
f is a fixed paired involution. The full suffix SPE criterion is exact.
The LP searches client multiplicities for violation of half by this candidate.
Floating output is discovery only; no candidate gets claimed without exact IC.
"""
from itertools import combinations
import json
import numpy as np
from scipy.optimize import linprog


def test(m, q, comp):
    masks=list(range(1,1<<q))
    inc=np.array([[(b>>a)&1 for b in masks] for a in range(q)], dtype=float)
    f=[a^1 for a in range(q)]
    root=0
    rows=[]
    # All positive-depth IC follow the exact constant-suffix criterion,
    # frozen after first topic t, with background 1_t and r=m-1.
    for t in range(q):
        a=f[t]
        for s in range(q):
            # Required difference >= 0.
            row=inc[a]*(1-inc[s])/(inc[t]+m-1)
            row-=inc[s]*(1-inc[a])/(inc[t]+1)
            rows.append(-row)
    def root_pay(t):
        return inc[t]*(1-inc[f[t]])+inc[t]*inc[f[t]]/m
    actual=root_pay(root)
    for t in range(q):
        rows.append(root_pay(t)-actual)
    welfare=np.maximum(inc[root],inc[f[root]])
    covered=np.maximum.reduce([inc[a] for a in comp])
    res=linprog(-covered, A_ub=rows, b_ub=np.zeros(len(rows)),
                A_eq=[welfare],b_eq=[1],bounds=(0,None),method='highs')
    out={'m':m,'q':q,'comparison':comp,'status':res.message}
    if res.success:
        out['comparison_over_W']=-res.fun
        out['positive_types']=[(b,float(x)) for b,x in zip(masks,res.x) if x>1e-8]
    return out


if __name__=='__main__':
    # One paired-absorber family; representatives distinguish whether the
    # comparison uses no bank, one bank, or both banks, and complete pairs.
    cases=[(5,8,[0,2,3,4,6]),(5,8,[0,1,2,4,6]),
           (5,10,[0,2,4,6,8]),(8,12,[0,1,2,3,4,6,8,10])]
    print(json.dumps([test(*args) for args in cases],indent=2))
