"""Independent algebra audit of the common-penultimate-theme half certificate.

Explicit bit menus are summed before deriving aggregate expressions. Standard
library exact arithmetic only; the all-m proof is in the accompanying review.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json


def fractions(m, p, a, b, t, r):
    alpha = F(a, p+a+b) if a else F(0)
    beta = F(b, p+a+b) if b else F(0)
    # Direct contribution of this client to each actual inequality.
    ss = sum((alpha-F(ti, p+1+ri) for ti, ri in zip(t, r)), F(0))
    zz = sum((beta-F(ri, p+1+a) for ri in r), F(0))
    vv = sum((F(r[i],p+1+t[i])-F(r[j],p+1+t[i])
              for i in range(m) for j in range(m) if i != j), F(0))
    d, ell, h = sum(t), sum(r), sum(ti*ri for ti,ri in zip(t,r))
    D = (p+1)*(p+2)
    assert ss == m*alpha-F(d,p+1)+F(h,D)
    assert zz == m*beta-F(ell,p+a+1)
    assert vv == F(d*ell-m*h,D)
    gg = ss+zz/(2*m)+vv/m
    rho = 2*int(p+a+b>0)-int(d>0)-gg
    expected = (2*int(p+a+b>0)-int(d>0)-m*alpha-beta/2
                +F(d,p+1)+F(ell,2*m*(p+a+1))-F(d*ell,m*D))
    assert rho == expected
    return rho


def general_rho(m,p,a,b,d,ell):
    alpha=F(a,p+a+b) if a else F(0)
    beta=F(b,p+a+b) if b else F(0)
    return (2*int(p+a+b>0)-int(d>0)-m*alpha-beta/2
            +F(d,p+1)+F(ell,2*m*(p+a+1))
            -F(d*ell,m*(p+1)*(p+2)))


def run():
    direct = 0
    for m in (2,3,4):
        for p in range(m-1):
            for a,b in product((0,1),repeat=2):
                for bits in product((0,1),repeat=2*m):
                    rho=fractions(m,p,a,b,bits[:m],bits[m:])
                    if m>=3 and (not a or p==m-2):
                        assert rho>=0
                    direct+=1
    aggregate=0
    minima={}
    for m in range(3,31):
        minimum=None
        for p in range(m-1):
            for a,b in product((0,1),repeat=2):
                if a and p!=m-2:continue
                # Bilinear cells permit corner checking separately on d=0
                # and d in [1,m]. The exhaustive small direct menu test above
                # independently checks the aggregate reduction itself.
                for d,ell in product((0,1,m),(0,m)):
                    rho=general_rho(m,p,a,b,d,ell)
                    assert rho>=0
                    minimum=rho if minimum is None else min(minimum,rho)
                    aggregate+=1
        minima[m]=str(minimum)
    # Eight claimed corners, each verified directly as a rational identity.
    for m in range(3,101):
        claims={
            (0,1,0):F(0),
            (0,1,m):F(m-3,2*m*(m-1)),
            (0,m,0):F(1),
            (0,m,m):1-F(m+1,2*m*(m-1)),
            (1,1,0):F(m+1,2*m*(m-1)),
            (1,1,m):F(1,m),
            (1,m,0):F(m,m-1)-F(1,2*m),
            (1,m,m):F(1),
        }
        for (b,d,ell),claimed in claims.items():
            assert general_rho(m,m-2,1,b,d,ell)==claimed
            assert claimed>=0
    assert general_rho(4,0,1,0,1,0)==-2
    assert general_rho(3,0,1,0,1,0)==-1
    generalized=0
    for k in range(3,25):
        for p in range(k-2,120):
            for b,d,ell in product((0,1),(0,1,k),(0,k)):
                assert general_rho(k,p,1,b,d,ell)>=0
                generalized+=1
    return {'status':'independent algebra checks passed',
            'direct_raw_bit_menu_cases':direct,
            'aggregate_corner_cases':aggregate,
            'small_m_minimum_residuals':minima,
            'empty_and_zero_contributions':'included by exact zero conventions',
            'all_m_proof':'analytic case split; finite checks audit formulas only',
            'general_target':'OPEN',
            'generalized_k_p_corner_cases':generalized,
            'generalized_scope':'k comparison topics, arbitrary total players, A-client background p>=k-2',
            'boundary_correction':'a1 p0 b0 d1 ell0 gives rho=2-m'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report=run()
    if args.output:
        with args.output.open('x') as stream:
            json.dump(report,stream,ensure_ascii=False,indent=2)
            stream.write('\n')
    print(json.dumps(report,ensure_ascii=False))
