"""Exact finite audit of the disjoint-singleton product equality classification.
The arbitrary K,r proof is in product_correlation_boundary.md; this is not a SPE search.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
import json

def counts(k,r):
    if k==1:
        yield (r,);return
    for i in range(r+1):
        for rest in counts(k-1,r-i):yield (i,)+rest

def g(h):return F(1,h+1)

def value(k,r):
    q,s=divmod(r,k)
    return F(k-s,k*(q+1))+F(s,k*(q+2))

def background_value(c):return [g(x) for x in c]

def product_cap(marginals,k):
    result=[F(0)]*k
    for z in product(range(k),repeat=len(marginals)):
        probability=prod((marginals[i][a] for i,a in enumerate(z)),start=F(1))
        if not probability:continue
        c=[z.count(j) for j in range(k)]
        result=[x+probability*y for x,y in zip(result,background_value(c))]
    return result

def add(x,y):return(x[0]+y[0],x[1]+y[1])
def mul(x,y):return(x[0]*y[0]+57*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(x,c):return(x[0]*c,x[1]*c)

def main():
    cases=0;vectors=0;product_cases=0
    for k in range(1,7):
      for r in range(0,10):
        cases+=1;q,s=divmod(r,k);v=value(k,r)
        for c in counts(k,r):
            vectors+=1
            assert sum(background_value(c),F(0))/k>=v
            assert (sum(background_value(c),F(0))/k==v)==all(x in(q,q+1) for x in c)
            for h in c:
                slack=g(h)-g(q)-(h-q)*(g(q+1)-g(q))
                assert slack>=0
                assert (slack==0)==(h in(q,q+1))
        base=[q+1]*s+[q]*(k-s)
        caps=[sum((g(base[(j-shift)%k]) for shift in range(k)),F(0))/k for j in range(k)]
        assert caps==[v]*k
        if s==0 or k%s==0:
            # Deterministic seats do not need enumeration, only add q per customer.
            marginals=[]
            if s:
                block=k//s
                for i in range(s):marginals.append([F(1,block) if i*block<=j<(i+1)*block else F(0) for j in range(k)])
            cap=[F(0)]*k
            for z in product(range(k),repeat=s):
                probability=prod((marginals[i][a] for i,a in enumerate(z)),start=F(1))
                if probability:
                    cap=[cap[j]+probability*g(q+z.count(j)) for j in range(k)]
            assert cap==[v]*k
            product_cases+=1
    # Q(sqrt(57)) feasible product candidate for K3,r2.
    one=(F(1),F(0));t=(F(-5,4),F(1,4));b=add(one,scale(t,-1))
    candidate=add(one,scale(t,F(-1,2)))
    middle=add(t,scale(mul(b,b),F(1,3)))
    assert candidate==middle==(F(13,8),F(-1,8))
    assert add(add(scale(mul(t,t),2),scale(t,5)),(F(-4),F(0)))==(F(0),F(0))
    # 7<sqrt(57)<8 certifies 0<t<1; 23^2>9*57 certifies T>2/3.
    assert 7**2<57<8**2 and 23**2>9*57
    result={'status':'exact finite audit passes; general classification proof separate','parameter_cases':cases,'integer_count_vectors':vectors,'product_constructed_cases':product_cases,'smallest_gap_example':{'K':3,'r':2,'true_v':'2/3','product_cap':'strictly >2/3','feasible_upper':'(13-sqrt(57))/8','upper_claimed_sharp':False}}
    print(json.dumps(result,indent=2))
    Path(__file__).with_name('product_boundary_audit.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
