"""Exact Fraction checks for WC-R1-HET-ENDPOINT-REDUCTION v1.
This is regression evidence; the adjacent proof supplies the general theorem.
"""
from fractions import Fraction as F
from itertools import product
import json


def poly(c,x):
    return sum((a*x**j for j,a in enumerate(c) if a),F(0))

def monomial(k,a=F(1)):
    return [F(0)]*k+[a]

def endpoints(p,weights,fs,alpha):
    W=sum(weights,F(0))
    heavy=poly(p,F(1))+sum((poly(f,1+w) for w,f in zip(weights,fs)),F(0))
    switch=poly(p,1+W)+sum((poly(f,F(1)) for f in fs),F(0))
    assert heavy>alpha*switch
    for w,f in zip(weights,fs):
        assert poly(p,1+w)+poly(f,w)>alpha*(poly(p,W)+poly(f,1+w))
    return heavy/switch

def full_states(p,weights,fs,alpha):
    # Column symmetry makes heavy=A sufficient, but every subset is checked.
    W=sum(weights,F(0));minimum=None;argmin=None
    table=[]
    for S in product((False,True),repeat=len(weights)):
        T=sum((w for w,s in zip(weights,S) if s),F(0));U=W-T
        hc=poly(p,1+T)+sum((poly(f,1 if s else 1+w) for w,f,s in zip(weights,fs,S)),F(0))
        hd=poly(p,1+U)+sum((poly(f,1+w if s else 1) for w,f,s in zip(weights,fs,S)),F(0))
        ratios=[hc/hd]
        for w,f,s in zip(weights,fs,S):
            if s: c=poly(p,1+T)+poly(f,w);z=poly(p,U+w)+poly(f,1+w)
            else: c=poly(p,U)+poly(f,1+w);z=poly(p,1+T+w)+poly(f,w)
            assert z>0
            ratios.append(c/z)
        best=max(ratios);assert best>alpha
        if minimum is None or best<minimum:minimum,argmin=best,S
    return {'states_checked':2**len(weights),'min_best_ratio_float':float(minimum),'argmin':list(argmin)}

def reduce(p,weights,fs,alpha):
    W=sum(weights,F(0));R=alpha*poly(p,1+W)-poly(p,F(1))
    indexes=[i for i,(w,f) in enumerate(zip(weights,fs)) if (poly(f,1+w)-alpha*poly(f,F(1)))*W>R*w]
    assert indexes
    # Pick nonintegral effective multiplicity to exercise genuine rounding.
    i=next((i for i in indexes if (W/weights[i]).denominator!=1),indexes[0])
    w,f=weights[i],fs[i];n=W/w;m=n.numerator//n.denominator;rho=F(m)/n
    gamma=1+rho*(alpha-1)
    assert n>(alpha-1)**2
    assert gamma>1 and gamma>alpha-1/(alpha-1)
    endpoints(p,[w]*m,[f]*m,gamma)
    return i,n,m,gamma,full_states(p,[w]*m,[f]*m,gamma)


def main():
    d=100;p=monomial(2);alpha=F(12,5)
    weights=[F(23,1000)]*5+[F(24,1000)]*5
    W=sum(weights,F(0));fs=[]
    for w in weights:
        bound=(poly(p,1+w)-alpha*poly(p,W))/(alpha*(1+w)**d-w**d)
        assert bound>0
        fs.append(monomial(d,F(99,100)*bound))
    h=endpoints(p,weights,fs,alpha)
    a=full_states(p,weights,fs,alpha)
    i,n,m,gamma,b=reduce(p,weights,fs,alpha)
    # A homogeneous input has an integer witness and rho=1.
    sameweights=[weights[i]]*m;samefs=[fs[i]]*m
    _,n2,m2,gamma2,_=reduce(p,sameweights,samefs,gamma)
    assert n2==m2 and gamma2==gamma
    # Identically zero core cannot satisfy strict L_i when alpha>1.
    for f in [monomial(0,F(0)),monomial(0),monomial(3)]:
        w=F(1,3)
        assert not poly(f,w)>F(3,2)*poly(f,1+w)
    result={'claim':'WC-R1-HET-ENDPOINT-REDUCTION v1','arithmetic':'exact fractions','d':d,'alpha':str(alpha),'weights':list(map(str,weights)),'beta_formula':'(99/100)*[(1+w)^2-alpha*W^2]/[alpha*(1+w)^100-w^100]','input_heavy_endpoint_ratio_float':float(h),'density_witness_index':i,'real_multiplicity':str(n),'integer_multiplicity':m,'gamma':str(gamma),'input':a,'output':b,'integer_branch_checked':True,'zero_core_examples_checked':True}
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
