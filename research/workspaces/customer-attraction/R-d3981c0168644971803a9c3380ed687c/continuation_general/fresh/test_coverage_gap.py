"""Directed attack of a single general static coverage-gap candidate.
Candidate: for every common catalog and tuple B of r-1 topics,
OPT_r - OPT_{r-1} <= max_A sum_{x in A} 1/(1+c_x(B)).
LP uses all nonempty interest types for selected labels and a fixed r-topic
comparison tuple O. It enforces every (r-1)-topic union <= O - gap.
No finite negative result would prove the candidate.
"""
from itertools import combinations, combinations_with_replacement
import json
import numpy as np
from scipy.optimize import linprog

def check(r):
    k=2*r-1
    masks=range(1,1<<k)
    benchmark=(1<<r)-1
    bmask=((1<<k)-1)^benchmark
    # weights plus gap variable
    costs=[-float(bool(s&benchmark)) for s in masks]+[0.]
    constraints=[]; rhs=[]
    for a in range(k):
        constraints.append([float(bool(s&(1<<a)))/(1+(s&bmask).bit_count()) for s in masks]+[0.])
        rhs.append(1.)
    for tup in combinations(range(k),r-1):
        union=sum(1<<a for a in tup)
        constraints.append([float(bool(s&union))-float(bool(s&benchmark)) for s in masks]+[1.])
        rhs.append(0.)
    # optimize gap (not total benchmark)
    costs=[0.]*(len(list(masks)))+[-1.]
    result=linprog(costs,A_ub=constraints,b_ub=rhs,bounds=[(0,None)]*len(costs),method='highs')
    out={'r':r,'success':result.success,'gap':(-result.fun if result.success else None)}
    if result.success:
        out['weights']={str(s):float(w) for s,w in zip(masks,result.x) if w>1e-8}
    return out

if __name__=='__main__':
    print(json.dumps([check(r) for r in [2,3,4]],indent=2))
