#!/usr/bin/env python3
"""Independent exhaustive legal-assignment audit; no shared research imports.
All processing times use integer units 1/k. Every original job-incidence
assignment is visited for the stated finite cases; arbitrary k is not proved
by this computation. Row data x are reconstructed from explicit OPT witnesses.
"""
from fractions import Fraction
from itertools import product
from math import ceil, floor
import json, platform, hashlib


def instance(r,k):
    # machine indices [0,r) homes, [r,2r) private sinks. Job 0 is large.
    p=[[None]*(1+r*k) for _ in range(2*r)]
    for i in range(r):
        p[i][0]=Fraction(1)
        for t in range(k):
            j=1+i*k+t
            p[i][j]=p[r+i][j]=Fraction(1,k)
    witnesses=[]
    for h in range(r):
        sigma=[h]+[(r+i if i==h else i) for i in range(r) for _ in range(k)]
        witnesses.append(sigma)
    x=[[sum(s[j]==i for s in witnesses)*Fraction(1,r) for j in range(1+r*k)] for i in range(2*r)]
    ell=[sum((p[i][j]*x[i][j] for j in range(1+r*k) if x[i][j]),Fraction()) for i in range(2*r)]
    M=[max((p[i][j] for j in range(1+r*k) if x[i][j]), default=Fraction()) for i in range(2*r)]
    cnt=[sum(xi,Fraction()) for xi in x]
    assert ell==[Fraction(1)]*r+[Fraction(1,r)]*r
    assert M==[Fraction(1)]*r+[Fraction(1,k)]*r
    assert cnt==[k-Fraction(k-1,r)]*r+[Fraction(k,r)]*r
    for sigma in witnesses:
        assert max(sum((p[i][j] for j in range(1+r*k) if sigma[j]==i),Fraction()) for i in range(2*r))==1
    return ell,M,cnt


def audit(r,k):
    ell,M,cnt=instance(r,k)
    pairs=[(Fraction(1),Fraction(1)),(Fraction(2),Fraction(1)),(Fraction(1),Fraction(3,2)),(Fraction(3),Fraction(2))]
    row_caps=[[floor(k*(a*e+b*s)) for e,s in zip(ell,M)] for a,b in pairs]
    b0s=range(3)
    count_caps=[[ceil(t)+b0 for t in cnt] for b0 in b0s]
    row_best=[None]*len(pairs); count_best=[None]*len(count_caps)
    opt=None; assignments=0; amp_checks=0
    group_mask=(1<<k)-1
    for mask in range(1<<(r*k)):
        # Each mask is a distinct assignment of individually labelled small jobs.
        z=[((mask>>(i*k))&group_mask).bit_count() for i in range(r)]
        for h in range(r):
            home_load=[k-v+(k if i==h else 0) for i,v in enumerate(z)]
            home_count=[k-v+(1 if i==h else 0) for i,v in enumerate(z)]
            loads=home_load+z; counts=home_count+z
            c=max(loads); assignments+=1
            opt=c if opt is None else min(opt,c)
            for t,cap in enumerate(row_caps):
                if all(l<=v for l,v in zip(loads,cap)):
                    row_best[t]=c if row_best[t] is None else min(row_best[t],c)
            for t,cap in enumerate(count_caps):
                if all(l<=v for l,v in zip(counts,cap)):
                    count_best[t]=c if count_best[t] is None else min(count_best[t],c)
            for eps in [Fraction(1,2),Fraction(1,3)]:
                if Fraction(c,k)<=2-eps:
                    assert Fraction(z[h],k)>=eps
                    amp_checks+=1
    assert opt==k
    row_results=[]
    for (a,b),got in zip(pairs,row_best):
        q=min(k,floor(a*Fraction(k,r)+b))
        want=2*k-q
        assert got==want, (r,k,a,b,got,want)
        assert Fraction(got,k)==2-Fraction(q,k)
        row_results.append({'a':str(a),'b':str(b),'best':str(Fraction(got,k)),'q':q})
    count_results=[]
    for b0,got in zip(b0s,count_best):
        q=min(k,ceil(Fraction(k,r))+b0)
        want=2*k-q
        assert got==want,(r,k,b0,got,want)
        count_results.append({'b0':b0,'best':str(Fraction(got,k)),'q':q})
    return {'r':r,'k':k,'legal_assignments':assignments,'opt':str(Fraction(opt,k)),'row_results':row_results,'count_results':count_results,'amplification_checked_assignments':amp_checks}


def main():
    cases=[(1,1),(4,2),(3,3),(4,3),(4,4)]
    results=[audit(r,k) for r,k in cases]
    # Exact large-parameter identities only: not exhaustive schedule checks.
    asymptotic=[]
    for k in [8,16,64,256]:
        for a,b in [(Fraction(1),Fraction(1)),(Fraction(7,2),Fraction(9,2))]:
            r=k*k; q=min(k,floor(a*Fraction(k,r)+b)); ratio=2-Fraction(q,k)
            assert 2-ratio==Fraction(q,k)
            assert ratio>=2-Fraction(b,k)-Fraction(a,k*k)
            asymptotic.append({'k':k,'r':r,'a':str(a),'b':str(b),'q':q,'ratio':str(ratio)})
    print(json.dumps({'python':platform.python_version(),'seed':None,'arithmetic':'integer/Fraction; no numerical tolerance','coverage':'all individual legal assignments only for listed finite cases; asymptotic lines check formulas only','cases':results,'formula_checks':asymptotic},indent=2))

if __name__=='__main__': main()
