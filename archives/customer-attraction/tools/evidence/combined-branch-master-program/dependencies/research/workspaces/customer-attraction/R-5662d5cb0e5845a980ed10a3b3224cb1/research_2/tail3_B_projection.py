"""Exact actual-fourth -> actual-last B projected necessary row.

Only standard library; discovery LP is not imported. The same original SPE
fixes the forced-B followers Q,R and all six optimal-query last replies.
The table maximizes over the enlarged hidden domain Q,R in {0,1}, ell=0..6.
The resulting customer sum is at least the nonnegative true weighted row.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import defaultdict
import hashlib
import json

WEIGHTS={'F':3360,'G':96,'H2Q':660,'H2R':595,'H3R':220,'LQ':522,'LR':522,'E':108}
POINT_REL='research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/full_new_reply_closure_exact.json'
ROOT=Path(__file__).resolve().parents[5]

def safe(num,den):return F(num,den) if num else F(0)
def raw(bits,d,q,r,ell):
    k=sum(bits[:3]);b=bits[5];p=k+b;den=p+q+r;c=sum(bits)
    u=[safe(t,c) for t in bits]
    Frow=u[3]-safe(b,den)
    G=6*safe(q,den)+safe(r,2*den)-F(d,p+1)-F(ell,12*(p+q+1))+F(d*ell,6*(p+1)*(p+2))
    return {'F':Frow,'G':G,'H2Q':u[1]-F(q,5+bits[0]),'H2R':u[1]-F(r,5+bits[0]),'H3R':u[2]-F(r,4+bits[0]+bits[1]),'LQ':u[5]-F(q,1+sum(bits[:5])),'LR':u[5]-F(r,1+sum(bits[:5])),'E':6*safe(r,den)-F(d,p+q+1)}
def coeff(bits,d,q,r,ell):
    rows=raw(bits,d,q,r,ell)
    return sum(WEIGHTS[name]*value for name,value in rows.items())
def table():
    out={}
    for bits in product(range(2),repeat=6):
        for d in range(7):
            endpoint=max(coeff(bits,d,q,r,ell) for q,r,ell in product(range(2),range(2),(0,6)))
            full=max(coeff(bits,d,q,r,ell) for q,r,ell in product(range(2),range(2),range(7)))
            assert full==endpoint
            out[(''.join(map(str,bits)),d)]=full
    return out
def verify_and_export(write=False):
    tt=table();point_path=ROOT/POINT_REL;point=json.loads(point_path.read_text());masses=defaultdict(F)
    for col in point['columns']:
        if col['kind']=='hist':masses[(col['actual_bits'],col['d'])]+=F(col['weight'])
    value=sum(tt[key]*mass for key,mass in masses.items());assert value<0
    cert={'status':'EXACT_VALID_NECESSARY_PROJECTION_AND_OLD_POINT_SEPARATION_ONLY','weights':WEIGHTS,'coefficient_domain':{'actual_bit_patterns':64,'d_values':list(range(7)),'hidden_QR_patterns':4,'ell_values':list(range(7)),'endpoint_replay_matches_full':True},'old_point_path':POINT_REL,'old_point_sha256':hashlib.sha256(point_path.read_bytes()).hexdigest(),'old_point_value':str(value),'old_point_value_decimal':float(value),'table':[{'actual_bits':bits,'d':d,'psi':str(v)} for (bits,d),v in tt.items()]}
    if write:
        target=Path(__file__).with_name('tail3_B_projection_certificate.json')
        if target.exists():raise FileExistsError(target)
        target.write_text(json.dumps(cert,indent=2)+'\n')
    return {k:v for k,v in cert.items() if k!='table'}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--export',action='store_true');a=p.parse_args()
    print(json.dumps(verify_and_export(a.export),indent=2))
