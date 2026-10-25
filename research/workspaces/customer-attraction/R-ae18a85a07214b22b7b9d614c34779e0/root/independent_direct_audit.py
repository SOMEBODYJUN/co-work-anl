"""Independent exact arithmetic check of realizability's five scalar cuts.

Reads certificate weights only; does not import its evaluator or discovery.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

BASE=Path(__file__).resolve().parent
certs=json.loads((BASE.parent/'realizability/root_max_direct_certificates.json').read_text())
def sh(n,d):return F(n,d)if n else F()
results=[]
for c in certs:
    w={k:F(v)for k,v in c['weights'].items()}
    alpha,beta,la=map(F,(c['alpha'],c['beta'],c['lambda']))
    assert alpha==w['root']
    assert beta==sum(w.get('cap'+str(i),F())for i in range(1,5))-la
    assert all(v>=0 for v in w.values())
    minimum=None;zero=0
    for t,a,b,cc,d in product((0,1),repeat=5):
        p=t+a+b;ell=p+cc+d
        rr=sh(t,ell);v3=sh(b,ell);v4=sh(cc,ell);v5=sh(d,ell)
        for j in range(6):
            z={'root':-rr,'cap1':-F(a),'cap2':-F(b),'cap3':-F(cc),'cap4':-F(d),
               'OPT2':5*v3-F(j,t+a+3),'OPT4':5*v5-F(j,p+cc+1),
               'K2_4':v3-F(d,t+a+3),'K3_4':v4-F(d,p+2),
               'PAIRopt':10*(v4+v5+F(cc,(p+1)*(p+2)))-F(j*(5-j),p+1)-F(j*(j-1),p+2)}
            rho=-F(j>0)-la*t-sum(v*z[k]for k,v in w.items())
            assert rho>=0,(c,t,a,b,cc,d,j,rho)
            minimum=rho if minimum is None else min(minimum,rho);zero+=rho==0
    results.append({'alpha':str(alpha),'beta':str(beta),'min_residual':str(minimum),'zero_count':zero,'states':192})
print(json.dumps(results,indent=2))
(BASE/'independent_direct_audit.json').write_text(json.dumps(results,indent=2)+'\n')
