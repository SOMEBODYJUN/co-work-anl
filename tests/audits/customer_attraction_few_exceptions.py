"""Independent exact review audit for the few-exceptions half certificate.

No canonical solver or discovery audit import. Raw per-client real comparisons
are reconstructed before the aggregate formula. Sparse polynomial arithmetic
checks the all-parameter square-threshold identity exactly, not by sampling.
"""
from fractions import Fraction as F
from itertools import product
from random import Random
from pathlib import Path
import argparse
import json


def add(*polys):
    out={}
    for poly in polys:
        for power,c in poly.items():out[power]=out.get(power,0)+c
    return {p:c for p,c in out.items() if c}


def scale(poly,c):return {p:c*v for p,v in poly.items() if c*v}


def mul(a,b):
    out={}
    for (i,j),c in a.items():
        for (k,l),d in b.items():out[i+k,j+l]=out.get((i+k,j+l),0)+c*d
    return {p:c for p,c in out.items() if c}


def power(poly,n):
    result={(0,0):1}
    for _ in range(n):result=mul(result,poly)
    return result


def polynomial_check():
    # Variables q,s; substitute r=q-1 and m=q^2+1+s exactly.
    one={(0,0):1};q={(1,0):1};s={(0,1):1}
    r=add(q,scale(one,-1));m=add(power(q,2),one,s)
    P=add(power(m,3),scale(mul(add(power(r,2),scale(r,2),scale(one,4)),power(m,2)),-1),
          mul(add(scale(power(r,2),2),scale(r,5),scale(one,5)),m),
          scale(power(r,2),-2),scale(r,-4))
    expected=add(power(s,3),scale(mul(power(q,2),power(s,2)),2),
                 mul(add(power(q,4),q,scale(one,-1)),s),
                 mul(q,power(add(q,scale(one,-1)),2)),scale(one,2))
    assert P==expected
    return P


def parameters(m,r):
    den=m*(m*m-3*m+3)-r*(m*m-2*m+2)
    return F(m*(m-1)**2,den),F((m-1)*(r+2),(m-2)*r+m-1)


def formula(m,r,a,b,e,p,d,ell):
    c=p+a+b
    alpha=F(a,c) if a else F(0)
    beta=F(b,c) if b else F(0)
    actual_e=F(e,c) if e else F(0)
    g=m*alpha+beta/2-F(d,p+1)-F(ell,2*m*(p+a+1))+F(d*ell,m*(p+1)*(p+2))
    k=actual_e-F(r*a,m)+(r*beta-F(e,p+a+1))/(m-1)
    mu,_=parameters(m,r)
    return 2*int(c>0)-int(d>0)-g-mu*k,k,g


def raw_case(m,r,a,b,exception_bits,other_bits,t,replies):
    p=sum(exception_bits)+sum(other_bits)
    c=p+a+b
    ua=F(a,c) if a else F(0)
    ub=F(b,c) if b else F(0)
    S=sum((ua-F(ti,p+1+ri) for ti,ri in zip(t,replies)),F(0))
    Z=sum((ub-F(ri,p+1+a) for ri in replies),F(0))
    V=sum((F(replies[i],p+1+t[i])-F(replies[j],p+1+t[i])
           for i in range(m) for j in range(m) if i!=j),F(0))
    G=S+Z/(2*m)+V/m
    K=F(0)
    for x in exception_bits:
        actual=F(x,c) if x else F(0)
        K+=actual-F(a,m)+(ub-F(x,p+1+a))/(m-1)
    Q,k,g=formula(m,r,a,b,sum(exception_bits),p,sum(t),sum(replies))
    mu,_=parameters(m,r)
    assert k==K and g==G
    assert Q==2*int(c>0)-int(any(t))-G-mu*K
    assert Q>=0


def run():
    shifted=polynomial_check()
    rng=Random(540013)
    raw=0
    for m,r in ((5,1),(10,2),(17,3)):
        for a,b in product((0,1),repeat=2):
            for e in range(r+1):
                exception_bits=(1,)*e+(0,)*(r-e)
                for other_load in ({m-2-r} if a else range(m-1-r)):
                    other=(1,)*other_load+(0,)*(m-2-r-other_load)
                    patterns=[((0,)*m,(0,)*m),((0,)*m,(1,)*m),
                              ((1,)+(0,)*(m-1),(0,)*m),
                              ((1,)+(0,)*(m-1),(1,)*m),
                              ((1,)*m,(0,)*m),((1,)*m,(1,)*m)]
                    patterns += [(tuple(rng.randrange(2) for _ in range(m)),
                                  tuple(rng.randrange(2) for _ in range(m)))
                                 for _ in range(2)]
                    for t,replies in patterns:
                        raw_case(m,r,a,b,exception_bits,other,t,replies)
                        raw+=1
    corners=0;params=0;minimum=None
    for r in range(1,21):
        threshold=(r+1)**2+1
        for m in sorted({threshold,threshold+1,2*threshold,threshold+123}):
            mu,cap=parameters(m,r)
            assert mu<=cap and mu>=F(m,m-1-r)>1
            for a,b,e in product((0,1),(0,1),range(r+1)):
                loads=({m-2-r+e} if a else {e,max(e,r),max(e,r+1),m-2})
                for p in loads:
                    for d,ell in product((0,1,m),(0,m)):
                        Q,_,_=formula(m,r,a,b,e,p,d,ell)
                        assert Q>=0,(m,r,a,b,e,p,d,ell,Q)
                        minimum=Q if minimum is None else min(minimum,Q)
                        corners+=1
            A=m*(m-1)**2-r*(m*m-m+1)
            B=m*(m-2)-r*(m-1)
            assert m*B-A==r-m<0
            for t in range(r+1):
                p=m-2-t;e=r-t
                _,K0,_=formula(m,r,1,0,e,p,1,0)
                c=m-1-t
                assert K0==-F(t*(A-t*B),m*(m-1)*c*(c+1))
                _,K1,_=formula(m,r,1,1,e,p,1,0)
                assert K1==-F(t*B,m*(m-1)*(m-t))
            params+=1
    return {'status':'independent exact audit passed; no fatal objection',
            'raw_comparison_formula_cases':raw,'parameter_cases':params,
            'aggregate_corner_cases':corners,'minimum_Q':str(minimum),
            'polynomial_identity':'exact sparse coefficient identity in q,s',
            'shifted_polynomial_coefficients':[[list(p),c] for p,c in sorted(shifted.items())],
            'scope':'m >= (r+1)^2+1, r>=1; arbitrary directory/full-history pure SPE',
            'general_Q_CAG_HALF':'OPEN'}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    result=run()
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result,stream,ensure_ascii=False,indent=2)
            stream.write('\n')
    print(json.dumps(result,ensure_ascii=False))
