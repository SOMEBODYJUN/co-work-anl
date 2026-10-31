#!/usr/bin/env python3
"""Exact explicit joint distributions auditing pairwise-correlation sharpness.
No independent-random rounding assumptions; distributions list all outcomes in
both symmetric modes. No shared research implementation is imported.
"""
from fractions import Fraction
from itertools import combinations, product
from math import comb
import json, platform


def outcomes(r,k,q):
    rho=Fraction(comb(k,2),r*comb(q,2))
    assert r>=k and 0<=rho<=1 and 2<=q<=k
    if rho:
        weight=rho/(r*comb(k,q)*comb(r-1,k-q)*k**(k-q))
        for h in range(r):
            other=[i for i in range(r) if i!=h]
            for active in combinations(other,k-q):
                for chosen in combinations(range(k),q):
                    for singles in product(range(k),repeat=k-q):
                        masks=[0]*r; masks[h]=sum(1<<t for t in chosen)
                        for i,t in zip(active,singles): masks[i]=1<<t
                        yield weight,h,masks,True
    if rho<1:
        weight=(1-rho)/(comb(r,k)*k**k*k)
        for active in combinations(range(r),k):
            for singles in product(range(k),repeat=k):
                masks=[0]*r
                for i,t in zip(active,singles): masks[i]=1<<t
                for h in active: yield weight,h,masks,False


def audit(r,k,q):
    total=Fraction(); ey=[[Fraction() for _ in range(k)] for _ in range(r)]
    eb=[Fraction() for _ in range(r)]; pairs={(i,t,u):Fraction() for i in range(r) for t in range(k) for u in range(t+1,k)}
    exp_c=Fraction(); success=Fraction(); count=0
    eps=Fraction(2*q-1,2*k)
    for w,h,masks,collision in outcomes(r,k,q):
        z=[mask.bit_count() for mask in masks]
        assert sum(z)==k
        loads=[k-v+(k if i==h else 0) for i,v in enumerate(z)]+z
        c=Fraction(max(loads),k)
        assert c==2-Fraction(q if collision else 1,k)
        total+=w; eb[h]+=w; exp_c+=w*c; count+=1
        if c<=2-eps: success+=w
        for i,mask in enumerate(masks):
            for t in range(k):
                if mask>>t&1:
                    ey[i][t]+=w
                    for u in range(t+1,k):
                        if mask>>u&1: pairs[i,t,u]+=w
    assert total==1
    assert all(p==Fraction(1,r) for p in eb)
    assert all(p==Fraction(1,r) for row in ey for p in row)
    assert all(p==Fraction(1,r*r) for p in pairs.values())
    rho=Fraction(k*(k-1),r*q*(q-1))
    assert success==rho
    assert (2-exp_c)*k==1+rho*(q-1) # inverse check
    bound=2-Fraction(1,k)-Fraction(k-1,2*r)
    assert exp_c>=bound
    if q==2: assert exp_c==bound
    return {'r':r,'k':k,'q':q,'support_outcomes_counted':count,'marginals':'all B and all small sink indicators exact 1/r','same_sink_pairs':'all exact 1/r^2','expected_C':str(exp_c),'expected_lower_bound':str(bound),'epsilon':str(eps),'success_probability':str(success),'probability_bound':str(rho),'expected_bound_attained':exp_c==bound}

if __name__=='__main__':
    print(json.dumps({'python':platform.python_version(),'seed':None,'arithmetic':'Fraction, exact enumeration of symmetric finite distribution','coverage':'listed finite r,k,q only; general proof is separate','cases':[audit(*case) for case in [(4,2,2),(3,3,2),(9,3,2),(9,3,3),(6,4,2),(6,4,3)]]},indent=2))
