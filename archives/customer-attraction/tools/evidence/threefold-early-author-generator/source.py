"""Exact complete local-type check for the ordered-floor certificate.

This script does not search finite games or infer an SPE from a relaxation.
The accompanying proof derives every summed row from one fixed full SPE.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
LAM=(F(1,3),F(1,2),F(1,2),F(2,3))
MU=F(3,2)

def share(v,c):return F(v,c) if v else F(0)
def coefficients(es,a,b,d,ell):
    p=sum(es);c=p+a+b
    alpha=share(a,c);beta=share(b,c)
    G=6*alpha+beta/2-F(d,p+1)-F(ell,12*(p+a+1))+F(d*ell,6*(p+1)*(p+2))
    H=[share(es[i],c)-F(a,sum(es[:i])+6-i) for i in range(4)]
    L=beta-F(a,p+a+1)
    Q=2*int(c>0)-int(d>0)-G-sum(v*h for v,h in zip(LAM,H))-MU*L
    return Q

def main():
    full=[];restricted=[];rho={}
    for es,a,b in product(product((0,1),repeat=4),(0,1),(0,1)):
        vals=[coefficients(es,a,b,d,ell) for d,ell in product(range(7),repeat=2)]
        r=min(vals);rho[''.join(map(str,es))+str(a)+str(b)]=str(r)
        full.extend(vals)
        if not a or sum(es)>=3:restricted.extend(vals)
    report={'status':'exact local coefficient verification only',
        'lambda':[str(v) for v in LAM],'mu':str(MU),
        'complete_restricted_state_count':len(restricted),
        'restricted_minimum':str(min(restricted)),
        'restricted_negative_count':sum(v<0 for v in restricted),
        'unrestricted_state_count':len(full),
        'unrestricted_minimum':str(min(full)),
        'unrestricted_negative_count':sum(v<0 for v in full),
        'rho_actual_membership':rho}
    assert len(restricted)==2058 and min(restricted)==0
    assert report['restricted_negative_count']==0
    (HERE/'threefold_penultimate_exact.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='rho_actual_membership'},indent=2))
if __name__=='__main__':main()
