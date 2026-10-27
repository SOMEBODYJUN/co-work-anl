"""Exact author audit of the two-remaining / three-comparison interface.

The infinite integer-background claim relies on the accompanying analytic proof.
This program does not import a game solver, LP, or discovery implementation.
"""
from fractions import Fraction as F
from itertools import product
import json

def frac(n,d):
    return F(n,d) if n else F(0)

def audit(p,a,b,t,r):
    def U(x,y):return frac(x,p+x+y)
    ua=U(a,b); ub=U(b,a)
    S=sum(ua-U(ti,ri) for ti,ri in zip(t,r))
    Z=sum(ub-U(ri,a) for ri in r)
    V=sum(U(r[i],t[i])-U(r[j],t[i]) for i in range(3) for j in range(3) if i!=j)
    L=sum(ub-U(ti,a) for ti in t)
    G=(6*S+Z+2*V+5*L)/11
    d=sum(t); ell=sum(r); h=sum(ti*ri for ti,ri in zip(t,r))
    D=(p+1)*(p+2)
    direct=(18*(ua+ub)-F(6*d,p+1)-F(ell+5*d,p+a+1)+F(2*d*ell,D))/11
    assert G==direct
    w=int(p+a+b>0); o=int(d>0)
    Q=2*w-o-G
    assert Q>=0,(p,a,b,t,r,Q)
    if p==0:
        expr=4*w-11*o+6*d+F(ell+5*d,a+1)-d*ell
        assert 11*Q==expr
        if d==0: assert expr==4*w+F(ell,a+1)
        elif a==0: assert expr==4*b+(d-1)*(11-ell)
        else: assert expr>=F(11,2)*(d-1)
    else:
        assert ua+ub<=F(2,p+2)
        if d==0: assert G<=F(12,11)
        elif p>=2: assert G<=F(9,11)
        else: assert G<=F(10,11)
    return Q

stats={}
for p in range(21):
    vals=[audit(p,a,b,t,r) for a,b in product(range(2),repeat=2)
          for t in product(range(2),repeat=3) for r in product(range(2),repeat=3)]
    stats[str(p)]={"literal_columns":len(vals),"minimum_residual":str(min(vals))}
print(json.dumps({"status":"passed","zero_background_complete":True,
                  "positive_background_status":"finite implementation regression; analytic proof covers all positive integer p",
                  "backgrounds":stats},indent=2))
