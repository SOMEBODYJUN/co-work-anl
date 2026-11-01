from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, hashlib
B=Path(__file__).resolve().parent
c=json.loads((B/'research_2/tail3_B_projection_certificate.json').read_text())
lookup={(x['actual_bits'],x['d']):F(x['psi']) for x in c['table']}
count=0
for es in product((0,1),repeat=6):
 total=sum(es); u=[F(e,total) if e else F() for e in es]; p=sum(es[:3])+es[5]
 for d in range(7):
  values=[]
  for q,r,ell in product((0,1),(0,1),range(7)):
   den=p+q+r; uq=F(q,den) if q else F(); ur=F(r,den) if r else F()
   for h in range(max(0,d+ell-6),min(d,ell)+1):
    D=(p+1)*(p+2); S=6*uq-F(d,p+1)+F(h,D); Z=6*ur-F(ell,p+q+1); V=F(d*ell-6*h,D)
    forced=u[3]-(F(es[5],den) if es[5] else F())
    v=3360*forced+96*(S+Z/12+V/6)
    v+=660*(u[1]-F(q,es[0]+5))+595*(u[1]-F(r,es[0]+5))+220*(u[2]-F(r,es[0]+es[1]+4))
    v+=522*(2*u[5]-F(q+r,1+sum(es[:5])))+108*(6*ur-F(d,p+q+1))
    values.append(v); count+=1
  assert max(values)==lookup[''.join(map(str,es)),d]
repo=next(x for x in B.parents if (x/'work.py').exists()); old=repo/c['old_point_path']; point=json.loads(old.read_text())
v=sum(lookup[z['actual_bits'],z['d']]*F(z['weight']) for z in point['columns'] if z['kind']=='hist')
assert v==F(c['old_point_value'])<0
print(json.dumps({'states':count,'visible_types':len(lookup),'point_value':str(v),'old_sha256':hashlib.sha256(old.read_bytes()).hexdigest()},indent=2))
