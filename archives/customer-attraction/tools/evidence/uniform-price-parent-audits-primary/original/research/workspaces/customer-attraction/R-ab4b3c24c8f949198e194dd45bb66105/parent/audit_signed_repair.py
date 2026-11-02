#!/usr/bin/env python3
"""Exact donor coefficients and compact-domain support-function audit."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def levels(v,kind):
    last=F(0);out=[]
    for h in sorted(set(x for x in v if x>0)):
        I=tuple(i for i,x in enumerate(v) if x>=h)
        out.append((h-last,I,kind));last=h
    return out

def run():
    cases=0;negative=0
    vals=[F(-2),F(-1,2),F(0),F(1,3),F(2)]
    for d in range(1,5):
        prices=[x for x in product(map(F,range(4)),repeat=d)
                if sum(max(F(0),1-t) for t in x)<=1 and sum(max(F(0),t-2) for t in x)<=1]
        for g in product(vals,repeat=d):
            gp=tuple(max(F(0),t) for t in g);gn=tuple(max(F(0),-t) for t in g)
            C=2*sum(gp)-sum(gn)+max(gp,default=F(0))+max(gn,default=F(0))
            atoms=levels(gp,'bank')+levels(gn,'low')
            balances=list(g);cost=F(0)
            for q,I,kind in atoms:
                if kind=='bank':
                    cost+=q*(2*len(I)+1)
                    for i in I:balances[i]-=q
                else:
                    cost+=q*(1-len(I))
                    for i in I:balances[i]+=q
            assert balances==[0]*d and cost==C
            sup=max(sum(x*y for x,y in zip(lam,g)) for lam in prices)
            assert sup==C
            if C<0:negative+=1
            cases+=1
    # Finite exact arithmetic for the strong-security compiler; D is an assumed seed margin.
    compiled=0
    for d in range(1,5):
        m=d+1
        for g in product(vals,repeat=d):
            for D in [F(1,3),F(2)]:
                B=-D-sum(g);t=max([F(0)]+[-x for x in g]);a=[x+t for x in g]
                assert min(a)>=0
                if t:
                    threshold=t*m*(m-1)/(2*D)
                    k=max(m,threshold.numerator//threshold.denominator+1)
                    eps=F(m*(m-1),2*k)
                    total=B+t*(-d+eps)+sum(a)
                    assert total==-D+t*eps<0
                else:
                    total=B+sum(a)
                    assert total==-D<0
                assert all(x+t-y==0 for x,y in zip(g,a))
                compiled+=1
    return {"all_checks_passed":True,"scope":"exact coefficient/algebra audit, not existence of any bad seed",
            "signed_vectors_checked":cases,"negative_cost_vectors_checked":negative,
            "strong_compiler_coefficient_cases":compiled}
if __name__=='__main__':
    out=run();Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
