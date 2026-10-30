"""Fraction audit: common power-mixture minimizer obstruction.
The real-exponent/measure theorem is proved in the accompanying draft.
Here we check exact proof side conditions and finite integer-power/tie mixtures.
"""
from fractions import Fraction as F
import json

def integer_power(q,n):
    return F(q)**n

def params(d):
    R=F(d,16); A=d*d+1; K=d*(d+1); W=K**(4*d)
    kappa=1/(4*R*K**(4*d-2))
    assert d>=32 and R>1 and 0<kappa<=1
    assert A<=4**d
    assert F(A-1,A)**(A-1)>F(1,4)
    assert 1-F(A-1,A)**A>F(1,2)
    assert kappa*W>=16*R
    assert A**(A-d)>=4*R/kappa
    assert 2*d*d-2*d+2>=12*d-4
    return R,A,K,W,kappa

def differences(d,p,pr):
    R,A,K,W,kappa=pr
    r=p-d
    wh=F(W)**r
    dh=wh*(R-F(A)**r*(1-F(A-1,A)**p))
    dl=R*wh*(1-F(W-1,W)**p)-1
    assert kappa*dh+dl<0
    return dh,dl

def finite_audit(d):
    pr=params(d); R,A,K,W,kappa=pr
    powers=sorted(set([1,2,d-1,d,d+1,d+2,2*d]))
    ds={p:differences(d,p,pr) for p in powers}
    pl=d; ph=d+1
    hl,ll=ds[pl]; hh,lh=ds[ph]
    assert hl>0 and ll<0 and hh<0 and lh>0
    # Heavy is exactly indifferent, so every minimum must use light's bad option.
    mu_h=[-hh,hl]
    th=mu_h[0]*hl+mu_h[1]*hh
    tl=mu_h[0]*ll+mu_h[1]*lh
    assert th==0 and tl<0
    # Light is exactly indifferent, so every minimum must use heavy's bad option.
    mu_l=[lh,-ll]
    th=mu_l[0]*hl+mu_l[1]*hh
    tl=mu_l[0]*ll+mu_l[1]*lh
    assert th<0 and tl==0
    return {'d':d,'ratio':str(R),'proof_conditions':True,
            'integer_powers':powers,'strict_pointwise_witness':True,
            'heavy_tie_light_strict':True,'light_tie_heavy_strict':True}

if __name__=='__main__':
    result=[finite_audit(d) for d in [32,33]]
    for d in [64,128]:
        params(d)
    print(json.dumps({'arithmetic':'Fraction','finite_diagnostics':result,
                      'extra_exact_parameter_d':[64,128]},indent=2))
