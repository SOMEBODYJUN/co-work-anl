"""Standalone exact audit of the maximum-root four-tail aggregate certificate.

No optimizer, SPE solver, discovery helper, or legacy coefficient evaluator is
imported. The finite domain exhausts CUSTOMER MEMBERSHIPS, not finite games.
The semantic proof giving each nonnegative SPE slack is in max_root_four_tail.md.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json

HERE = Path(__file__).resolve().parent

def frac(num, den):
    return F(num, den) if num else F()

def raw_rows(eta, e):
    t,a,b,c,d,q,r,s = eta
    actual_den=t+a+b+c+d
    off_den=t+d+q+r+s
    UB=frac(b,actual_den)
    UD=frac(d,actual_den)
    UA=frac(a,actual_den)
    YD=frac(d,off_den)
    YR=frac(r,off_den)
    YS=frac(s,off_den)
    b_act=t+a+b
    b_off=t+d+q
    H_act=frac(c,actual_den)+UD+frac(c,(b_act+1)*(b_act+2))
    H_off=YR+YS+frac(r,(b_off+1)*(b_off+2))
    rows={
        'act:K1:4': UB-frac(d,t+a+3),
        'act:K1:5': UB-frac(q,t+a+3),
        'act:K1:6': UB-frac(r,t+a+3),
        'act:K1:7': UB-frac(s,t+a+3),
        'act:K3:opt': 5*UD-frac(e,t+a+b+c+1),
        'act:P': 10*H_act-frac(e*(5-e),b_act+1)-frac(e*(e-1),b_act+2),
        'off:K3:opt': 5*YS-frac(e,t+d+q+r+1),
        'off:P': 10*H_off-frac(e*(5-e),b_off+1)-frac(e*(e-1),b_off+2),
        'F': UA-YD,
        'root': -frac(t,actual_den),
        'size:opt': -e,
    }
    rows.update({f'size:{i}':-value for i,value in enumerate(eta)})
    return rows

def audit():
    cert=json.loads((HERE/'local_max_tail_certificate.json').read_text())
    lam={n:F(v) for n,v in cert['multipliers'].items()}
    gamma=F(cert['gamma_T'])
    A=lam['root']
    B=gamma+sum((5 if n=='size:opt' else 1)*v for n,v in lam.items() if n.startswith('size:'))
    assert A==F(48741762,1000000)
    assert B==F(-7896499,1000000)
    assert all(v>=0 for v in lam.values())
    minimum=None
    zeros=0
    groups={}
    for eta in product((0,1),repeat=8):
        for e in range(6):
            row=raw_rows(eta,e)
            rho=gamma*eta[0]-int(e>0)-sum(v*row[n] for n,v in lam.items())
            assert rho>=0,(eta,e,rho)
            minimum=rho if minimum is None else min(minimum,rho)
            zeros+=rho==0
            key=''.join(map(str,eta[:5]))
            groups[key]=min(groups.get(key,rho),rho)
            # Coefficient identity; u,K are deliberately arbitrary here.
            for u,K in [(F(0),F(0)),(F(7,11),F(5,13))]:
                slacks={n:row[n]+(u if n=='root' else ((5 if n=='size:opt' else 1)*K if n.startswith('size:') else 0)) for n in lam}
                rhs=sum(lam[n]*slacks[n] for n in lam)+rho
                lhs=A*u+B*K-int(e>0)+gamma*(eta[0]-K)
                assert lhs==rhs,(eta,e,lhs-rhs)
    # In the AGGREGATE identity the correction is gamma*(sum_x t_x-K),
    # which vanishes because |T|=K. The per-type algebra test above does
    # not sum its freely chosen global u,K once per customer.
    rootfloor=F(50)-A
    Kextra=F(-8)-(B-rootfloor/5)
    assert rootfloor==F(cert['root_floor_multiplier'])>=0
    assert Kextra==F(cert['K_nonnegative_multiplier'])>=0
    assert minimum==0 and zeros==1
    result={'status':'all exact coefficient and algebra checks passed',
            'domain':'2^8 * 6 complete binary memberships / optimum multiplicities',
            'states':1536,'zero_residuals':zeros,'minimum_residual':str(minimum),
            'A':str(A),'B':str(B),
            'simple_rootfloor_multiplier':str(rootfloor),'simple_Kextra':str(Kextra),
            'minimum_residual_by_TABCD':{k:str(v) for k,v in groups.items()},
            'semantic_boundary':'The analytical SPE slack validity is stated in max_root_four_tail.md. This code does not certify a full-history game instance or prove half coverage.'}
    (HERE/'local_max_tail_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': audit()
