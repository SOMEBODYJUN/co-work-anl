"""Main exact size-consistency feedback for the genuine fifth-source root row."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
def main():
    result=[];quotients=[]
    for bits in product((0,1),repeat=7):
        p,y2,y3,y4,y5,z,o=bits;n=y2+y3+y4+y5;c=p+n+z
        v=F(p,c) if c else F(0);s=F(y5,c) if c else F(0);w=F(z,c) if c else F(0);q=F(o,6)
        tau=F(n,2)+z-7*p+25*v-w-q/F(1+5*p)+q/F(1+p+n)
        delta=v-s+q/F(p+n-y5+2)-F(o,12)+F(p,18)
        rho=delta+F(12,5)*tau
        E=65*delta+72*tau-35*(p-y5)
        eta=F(65,84)*rho-tau-F(5,12)*(p-y5)
        assert E==84*eta>=0
        if rho:quotients.append(((tau+F(5,12)*(p-y5))/rho,bits))
        else:assert tau+F(5,12)*(p-y5)<=0
        result.append({'bits':list(bits),'tau':str(tau),'delta':str(delta),'rho':str(rho),'E':str(E),'eta':str(eta)})
    assert max(q for q,_ in quotients)==F(65,84)
    cp=HERE/'universal_union_wallet_v2/exact_certificate.json'
    assert sha256(cp.read_bytes()).hexdigest()=='12d4f059b7be021c8b3c89ed6adf3bde208750da6ce0eee79c383a813d50b36b'
    cert=json.loads(cp.read_text());u=F(cert['derived']['u1_u6'][0]);K=F(cert['K'])
    H=150*u-F(139,6)*K-1;L=10980*u-1658*K-87;J=67140*u-9878*K-627
    assert L==0 and H>0 and J==13*L-504*H<0
    out={'status':'PASS','type_count':128,'inequality':'67140*u1-9878*K-627*O>=0',
      'eta_zero_types':sum(F(r['eta'])==0 for r in result),'ratio_max':'65/84',
      'ratio_max_types':[list(t) for q,t in quotients if q==F(65,84)],
      'v2_certificate_sha256':sha256(cp.read_bytes()).hexdigest(),'v2_H':str(H),'v2_L':'0','v2_J':str(J),
      'v2_J_decimal':float(J),'types':result}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
