#!/usr/bin/env python3
"""Exact small checks for the equal-quantum arbitrary-eligibility candidate."""
from fractions import Fraction
from itertools import product

def feasible_assignments(nh, E, p, u, T, H, Z):
    # Each home has one macro and n_h private jobs. Enumerate all private choices.
    q = int(T // u)
    r = int((T-p)//u)
    k = [max(0,n-r) for n in nh]
    jobs=[(h,j) for h,n in enumerate(nh) for j in range(n)]
    out=[]
    for dests in product(*[(['h']+list(E[h][j])) for h,j in jobs]):
        hc=[0]*H; zc=[0]*Z; ok=True
        for (h,j),d in zip(jobs,dests):
            if d=='h': hc[h]+=1
            else: zc[d]+=1
        if any(p+u*hc[h]>T for h in range(H)) or any(u*zc[z]>T for z in range(Z)): continue
        if any(sum(d!='h' for (hh,jj),d in zip(jobs,dests) if hh==h)<k[h] for h in range(H)): continue
        out.append((hc,zc))
    return out

# Boundary: different private qualifications can split to sinks with empty group intersection.
T,p,u=Fraction(1),Fraction(3,5),Fraction(2,5)
nh=[2]; E=[[(0,),(1,)]]
assert feasible_assignments(nh,E,p,u,T,1,2)
# Exhaustive tiny random instances: flow lower bounds are equivalent to direct assignments.
import random
random.seed(20261017)
for _ in range(3000):
    H=random.randint(1,3); Z=random.randint(0,3)
    u=Fraction(random.randint(1,5),10); p=Fraction(random.randint(6,10),10); T=Fraction(1)
    nh=[random.randint(0,3) for _ in range(H)]
    E=[[(z,) for z in range(Z)] for _ in range(H)]
    E=[ [tuple(z for z in range(Z) if random.randrange(2)) for j in range(n)] for h,n in enumerate(nh)]
    # replace empty eligibility with no sink as permitted
    sols=feasible_assignments(nh,E,p,u,T,H,Z)
    q=int(T//u); r=int((T-p)//u)
    # brute force lower-bound feasibility by checking every assignment's counts
    jobs=[(h,j) for h,n in enumerate(nh) for j in range(n)]
    brute=False
    for ds in product(*[(['h']+list(E[h][j])) for h,j in jobs]):
        hc=[0]*H; zc=[0]*Z
        for (h,j),d in zip(jobs,ds):
            if d=='h': hc[h]+=1
            else: zc[d]+=1
        if any(p+u*hc[h]>T for h in range(H)) or any(u*zc[z]>T for z in range(Z)): continue
        if any(sum(d!='h' for (hh,jj),d in zip(jobs,ds) if hh==h)<max(0,nh[h]-r) for h in range(H)): continue
        brute=True; break
    assert bool(sols)==brute
print('equal-quantum arbitrary-eligibility exhaustive checks passed')
