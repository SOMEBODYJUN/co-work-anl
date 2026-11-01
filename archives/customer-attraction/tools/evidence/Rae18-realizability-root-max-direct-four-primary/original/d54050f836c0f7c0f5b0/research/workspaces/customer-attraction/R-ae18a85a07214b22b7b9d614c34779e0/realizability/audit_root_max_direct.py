"""Exact all-customer-state audit of five root-maximum inequalities.

No imports from any discovery LP or existing certificate evaluator.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

BASE=Path(__file__).resolve().parent
certs=json.loads((BASE/'root_max_direct_certificates.json').read_text())

def div(a,b):
    return F(a,b) if a else F(0)

def customer(bits,j):
    t,a,b,c,d=bits
    load=sum(bits)
    r,v2,v3,v4,v5=[div(q,load) for q in bits]
    p=t+a+b
    H=v4+v5+F(c,(p+1)*(p+2))
    return {
        'root':-r,
        'cap1':-F(a),'cap2':-F(b),'cap3':-F(c),'cap4':-F(d),
        'OPT2':5*v3-F(j,t+a+3),
        'OPT4':5*v5-F(j,t+a+b+c+1),
        'K2_4':v3-F(d,t+a+3),
        'K3_4':v4-F(d,t+a+b+2),
        'PAIRopt':10*H-F(j*(5-j),p+1)-F(j*(j-1),p+2),
    }

out=[]
for cert in certs:
    alpha,beta,lam=[F(cert[k]) for k in ('alpha','beta','lambda')]
    weights={k:F(v) for k,v in cert['weights'].items()}
    assert all(v>=0 for v in weights.values())
    assert weights['root']==alpha
    cap=sum(weights.get('cap'+str(h),0) for h in range(1,5))
    assert cap-lam==beta
    residuals=[]
    for bits in product(range(2),repeat=5):
        for j in range(6):
            ss=customer(bits,j)
            rho=-F(j>0)-lam*bits[0]-sum(w*ss[k] for k,w in weights.items())
            assert rho>=0,(cert,bits,j,rho)
            residuals.append(rho)
    out.append({
        'alpha':str(alpha),'beta':str(beta),'lambda':str(lam),
        'states':len(residuals),'minimum':str(min(residuals)),
        'zeros':sum(q==0 for q in residuals),
    })
print(json.dumps(out,indent=2))
(BASE/'root_max_direct_audit.json').write_text(json.dumps(out,indent=2)+'\n')
