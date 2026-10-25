"""Exact full client-type audit of the two-order, three-tail swap payment."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def one(bits, old, own, other):
    b=bits[0]+bits[1]
    total=b+sum(bits[q] for q in own)
    utility=lambda q: F(bits[q],total) if bits[q] else F(0)
    p=b+bits[own[0]]
    h=utility(own[1])+utility(own[2])+F(bits[own[1]],(p+1)*(p+2))
    def tax(a,d):
        k=bits[a]+bits[d]
        return h-(F(k,p+k) if k else F(0))
    k0a=utility(own[0])-F(bits[old],b+3)
    k0l=utility(own[0])-F(bits[own[2]],b+3)
    k2a=utility(own[2])-F(bits[old],b+bits[own[0]]+bits[own[1]]+1)
    k2other=utility(own[2])-F(bits[other],b+bits[own[0]]+bits[own[1]]+1)
    return (F(1,9)*k0a+F(1,6)*k0l+F(23,36)*k2a
            +F(1,3)*k2other+F(5,18)*tax(old,own[2])
            +F(0)*tax(own[2],other))

out={'status':'exact_client_coefficient_identity_not_HALF5','types':256,'coefficient':'7/12','minimum':None,'zeros':0,'residuals':[]}
for bits in product((0,1),repeat=8):
    b=bits[0]+bits[1]
    loads=[b+sum(bits[q] for q in ix) for ix in ((2,3,4),(5,6,7))]
    u=lambda q,j:F(bits[q],loads[j]) if bits[q] else F(0)
    vy=sum(u(q,0) for q in (2,3,4)); vz=sum(u(q,1) for q in (5,6,7))
    j=u(0,0)+u(1,1)-u(1,0)-u(0,1)
    paid=one(bits,0,(2,3,4),7)+one(bits,1,(5,6,7),4)
    rho=F(7,12)*(vy+vz)-j-paid
    assert rho>=0,(bits,rho)
    if out['minimum'] is None or rho<F(out['minimum']):out['minimum']=str(rho)
    if not rho: out['zeros']+=1
    out['residuals'].append(str(rho))
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='residuals'},indent=2))
