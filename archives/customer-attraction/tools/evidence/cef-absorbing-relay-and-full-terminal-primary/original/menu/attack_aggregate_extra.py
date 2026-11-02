"""One fixed-strategy cone attack on AP-extra, not an instance survey.

Claim: for every complete SPE and every query p, sum_i E_{A,B~p}
g_A(Z_i(B)) <= W, with g extra-slot insertion against all m slots.
We use the published six-topic, three-player group strategy and p=(X2+Y2)/2.
The LP ranges over customer multiplicities and serves only to find a refutation.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

k,m=6,3
masks=list(range(1,1<<k))
def action(h):
    if not h: return 0
    if len(h)==1: return 3 if h[0]<3 else 0
    return min(set(range((h[-1]//3)*3,(h[-1]//3+1)*3))-set(h))
def end(h):
    while len(h)<m: h=h+(action(h),)
    return h
def coeff(h,a):
    return [F(1,sum((B>>v)&1 for v in h)) if (B>>a)&1 else F(0) for B in masks]
def insertion(h,a):
    return [F(1,1+sum((B>>v)&1 for v in h)) if (B>>a)&1 else F(0) for B in masks]
rows=[]
for n in range(m):
    for h in product(range(k),repeat=n):
        chosen=coeff(end(h),action(h))
        for a in range(k):
            other=coeff(end(h+(a,)),a)
            rows.append([x-y for x,y in zip(chosen,other)])
z=end(())
W=[F(any((B>>a)&1 for a in z)) for B in masks]
C=[F(0) for B in masks]
for i in range(m):
    for a,b in product((2,5),repeat=2):
        v=insertion(end(z[:i]+(b,)),a)
        C=[x+y/4 for x,y in zip(C,v)]
objective=np.array([float(w-c) for w,c in zip(W,C)])
result=linprog(objective,A_ub=-np.array(rows,dtype=float),b_ub=np.zeros(len(rows)),
               A_eq=np.array([W],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
out={'claim':'AP-extra','query':{'2':'1/2','5':'1/2'},
     'strategy':'published opposite-group/third-same-group complete strategy',
     'status':result.message,'lp_min_W_minus_C':result.fun}
if result.success and result.fun < -1e-8:
    weights=[F(float(x)).limit_denominator(10**8) for x in result.x]
    row_values=[sum(a*b for a,b in zip(row,weights)) for row in rows]
    gap=sum((w-c)*v for w,c,v in zip(W,C,weights))
    out.update(weights={str(B):str(v) for B,v in zip(masks,weights) if v},
               exact_min_IC=str(min(row_values)),exact_gap=str(gap),
               exact_refutation=min(row_values)>=0 and gap<0)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
