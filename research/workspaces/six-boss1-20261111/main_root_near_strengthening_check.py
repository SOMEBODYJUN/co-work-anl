"""Main exact 128-type root-maximal-label strengthening, with no optimization."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
def main():
    types=[]
    ratios=[]
    for p,y2,y3,y4,y5,z,o in product((0,1),repeat=7):
        n=y2+y3+y4+y5
        c=p+n+z
        v=F(p,c) if c else F(0)
        s=F(y5,c) if c else F(0)
        w=F(z,c) if c else F(0)
        theta=F(o,6)
        tau=F(n,2)+z-7*p+25*v-w-theta/F(1+5*p)+theta/F(1+p+n)
        delta=v-s+theta/F(p+n-y5+2)-F(o,12)+F(p,18)
        rho=delta+F(12,5)*tau
        assert tau>=0 and rho>=0
        if tau:
            ratios.append((-delta/tau,(p,y2,y3,y4,y5,z,o)))
        else:
            assert delta>=0
        types.append({'bits':[p,y2,y3,y4,y5,z,o], 'tau':str(tau),'delta':str(delta),'rho':str(rho)})
    assert max(r for r,_ in ratios)==F(12,5)
    certp=HERE/'universal_union_wallet_lp/exact_certificate.json'
    assert sha256(certp.read_bytes()).hexdigest()=='ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85'
    cert=json.loads(certp.read_text());K=F(cert['K'])
    u1=F(cert['derived']['u1_u6'][0])
    H=150*u1-F(139,6)*K-1
    L=10980*u1-1658*K-87
    assert H==0 and L==F(189*K-69,5)<0
    out={
        'status':'PASS','scope':'universal genuine largest-label root branch; all128 client types',
        'inequality':'10980*u1 - 1658*K - 87*OPT6 >= 0',
        'type_count':len(types),'min_tau':str(min(F(t['tau']) for t in types)),
        'min_rho':str(min(F(t['rho']) for t in types)),
        'max_negative_delta_over_tau':'12/5',
        'sharp_ratio_types':[list(t) for r,t in ratios if r==F(12,5)],
        'fixed_point_certificate_sha256':sha256(certp.read_bytes()).hexdigest(),
        'fixed_point_H':str(H),'fixed_point_K':str(K),
        'fixed_point_L':str(L),'fixed_point_L_decimal':float(L),
        'point_excluded':True,'whole_optimal_face_excluded':False,
        'types':types,
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
