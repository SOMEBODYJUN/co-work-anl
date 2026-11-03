"""Independent parent reconstruction from the thirteen disclosed raw rows.

Imports only point data and the reported final fraction for comparison;
no author's coefficient, lifting, game, or pricing implementation is used.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json

BASE=Path(__file__).resolve().parent.parent
path=BASE/'certificate/exact_current_source_own_index_v1.json'
raw=path.read_bytes();point=json.loads(raw)
states=list(product((0,1),repeat=3))
def ratio(a,b):return F(a,b) if a else F(0)
def menu(a,field,k,pos):
    return sum(n*t[pos] for n,t in zip(a[field],product((0,1),repeat=k)))
def evaluate(a,state):
    b=dict(zip('ABCDEUVWXY',map(int,a['bits'])))
    p=b['A']+b['B'];h,q,r=state;load=p+h+q+r
    u=ratio(b['C'],sum(b[t] for t in 'ABCDE'))
    vh,vq,vr=(ratio(v,load) for v in state)
    M=int(a['max_bits'][0]);z=int(a['max_bits'][4]);x=b['X'];y=b['Y']
    d=sum(a['AB_hist'][4:])
    AB=menu(a,'AB_hist',3,2);AE=menu(a,'AE_hist',3,2)
    U,V,W=(menu(a,'second_hist',4,i) for i in (1,2,3))
    H2=vq+vr+F(q,(p+h+1)*(p+h+2))
    def pair(v,w,nv,nw):
        return nv*nw*H2-F(nw*v+nv*w-2*v*w,p+h+1)-F(2*v*w,p+h+2)
    rows=[u-vh,F(h-q,p+3),F(h-r,p+3),5*vr-F(d,p+h+q+1),
          F(M-h),pair(x,y,1,1),pair(y,z,1,1),pair(AB,d,5,5),
          F(5*h-AE,p+3),pair(U,x,5,1),pair(U,V,5,5),
          pair(U,W,5,5),pair(V,d,5,5)]
    weights=[8251,4703,5446,165,307,92,66,2,925,15,7,17,4]
    return sum((v*w for v,w in zip(rows,weights)),F(0))

coefficients=[]
for a in point['atoms']:
    values=[evaluate(a,s) for s in states]
    coefficients.append(max(values))
slack=sum((F(a['exact_mass'])*v for a,v in zip(point['atoms'],coefficients)),F(0))
reported=json.loads((BASE/'certificate/actual13_projection.json').read_text())
assert slack==F(reported['exact_projection_slack'])<0
report={'status':'PASS independent exact thirteen-row reconstruction',
        'source_sha256':hashlib.sha256(raw).hexdigest(),
        'positive_atoms':len(point['atoms']),'hidden_states_per_atom':8,
        'raw_terms_checked':len(point['atoms'])*8*13,
        'exact_slack':str(slack),'slack_float':float(slack),
        'review':'Known integer weights, independently transcribed original IC/cap/tax formulas; not blind discovery.',
        'limitation':'Valid auxiliary necessary projection; strict separation is not HALF5 or a game counterexample.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
