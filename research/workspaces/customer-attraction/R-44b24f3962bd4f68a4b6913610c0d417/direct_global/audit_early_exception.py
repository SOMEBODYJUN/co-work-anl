"""Exact algebra regression for the early singleton-exception proof candidate.

Standard-library Fraction only. Finite audit checks implementation and identities;
the arbitrary-m argument is the explicit bilinear-corner proof in the note.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

def qvalue(m,a,b,ell,d):
    p=(m-3)*a+b;den=(m-1)*a+b
    ua=F(a,den) if den else F(0);ub=F(b,den) if den else F(0)
    mu=F(m*(m-4),2*(m-2)*(m-1))
    g=(m+F(1,2))*ua-F(ell,p+1)-F(d,2*m*(p+a+1))+F(ell*d,m*(p+1)*(p+2))
    return 2*int(bool(a+b))-int(ell>0)-g-mu*(ub-F(a,m))

def direct(m,a,b,tvec,rvec):
    p=(m-3)*a+b;den=(m-1)*a+b
    ua=F(a,den) if den else F(0);ub=F(b,den) if den else F(0)
    def share(c,e):return F(c,p+c+e) if c else F(0)
    S=sum((ua-share(t,r) for t,r in zip(tvec,rvec)),F(0))
    Z=sum((ua-share(r,a) for r in rvec),F(0))
    V=sum((share(rvec[i],tvec[i])-share(rvec[j],tvec[i])
           for i in range(m) for j in range(m) if i!=j),F(0))
    mu=F(m*(m-4),2*(m-2)*(m-1))
    return 2*int(bool(a+b))-int(any(tvec))-S-Z/(2*m)-V/m-mu*(ub-F(a,m))

def run():
    membership=0;corners=0
    for m in (4,5,6):
        for a,b in product(range(2),repeat=2):
            for tv in product(range(2),repeat=m):
                for rv in product(range(2),repeat=m):
                    q=qvalue(m,a,b,sum(tv),sum(rv))
                    assert q==direct(m,a,b,tv,rv)
                    assert q>=0
                    membership+=1
    for m in list(range(4,101))+[127,1000,1000000]:
        mu=F(m*(m-4),2*(m-2)*(m-1));assert 0<=mu<F(1,2)
        formulas={
          (0,0):[0,0,m-1,F(m-1,2)],
          (0,1):[F(3,2)-mu,F(19,12)-mu,1+F(m,2)-mu,F(5,4)+F(m,3)-mu],
          (1,0):[0,F(m-4,2*(m-2)*(m-1)),F(m-1,m-2),F(m*(2*m-5),2*(m-2)*(m-1))],
          (1,1):[F(m+1,2*m*(m-1)),F(1,m),F(2*m*m-m+1,2*m*(m-1)),1]}
        for a,b in product(range(2),repeat=2):
            vals=[qvalue(m,a,b,L,d) for L,d in ((1,0),(1,m),(m,0),(m,m))]
            assert vals==formulas[a,b],(m,a,b,vals,formulas[a,b])
            for L,d in ((0,0),(0,m),(1,0),(1,m),(m,0),(m,m)):
                assert qvalue(m,a,b,L,d)>=0;corners+=1
    out={'status':'exact regression passed; arbitrary-m proof is analytic',
         'binary_membership_cases':membership,'corner_checks':corners,
         'scope':'early singleton exception with last two actions equal, m>=4',
         'general_half_coverage':'OPEN'}
    Path(__file__).with_name('early_exception_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))

if __name__=='__main__':run()
