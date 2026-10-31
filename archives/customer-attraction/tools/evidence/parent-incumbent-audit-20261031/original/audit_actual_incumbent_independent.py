#!/usr/bin/env python3
"""Independent full-history audit of actual-prefix incumbent bridge failure."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json, hashlib
ROOT=Path(__file__).resolve().parents[5]
S=ROOT/'research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/actual_root_B_certificate.json'
d=json.loads(S.read_text()); IP=ROOT/d['instance_source'];inst=json.loads(IP.read_text())
customers=[frozenset(c['topics']) for c in inst['customers'] for _ in range(c['multiplicity'])]
sigma={tuple(a['history']):a['action'] for a in d['certificate']['actions']};k=len(inst['topics']);m=inst['players']

def end(h):
 h=tuple(h)
 while len(h)<m:h=h+(sigma[h],)
 return h

def u(z,i):return sum((F(1,sum(a in x for a in z)) for x in customers if z[i] in x),F(0))

def BR(h):
 vals=[u(h+(a,),m-1) for a in range(k)];v=max(vals)
 return [a for a in range(k) if vals[a]==v]
count=0
for n in range(m):
 for h in product(range(k),repeat=n):
  value=u(end(h),n)
  for a in range(k):
   assert value>=u(end(h+(a,)),n),(h,a)
   if a!=sigma[h]:count+=1
actual=end(());assert actual==(1,0,0,5)
V=[[u(end(actual[:i]+(t,)),i) for t in range(k)] for i in range(m)]
assert V[0][0]==9 and V[1][0]==13 and 4*V[0][0]<3*V[1][0]
# Any complete SPE must have a last BR. Even all such endpoints give incumbent A>=9.
root_min=min(u((0,)+h+(r,),0) for h in product(range(k),repeat=2) for r in BR((0,)+h))
# At prefix BA, choosing A guarantees the third mover >=13 for every last BR;
# every other third action pays <=11 for every last BR.
rows=[]
for t in range(k):
 vals=[u((1,0,t,r),2) for r in BR((1,0,t))]
 rows.append({'action':t,'last_BR':BR((1,0,t)),'min':min(vals),'max':max(vals)})
assert root_min==9 and rows[0]['min']==13 and max(x['max'] for x in rows[1:])==11
child_min=min(u((1,0,0,r),1) for r in BR((1,0,0)))
assert child_min==13
W=sum((u(actual,i) for i in range(m)),F(0));OPT=max(sum(any(a in x for a in z) for x in customers) for z in product(range(k),repeat=m))
r={'status':'PASS','certificate_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'instance_sha256':hashlib.sha256(IP.read_bytes()).hexdigest(),'unit_customers':len(customers),'histories':len(sigma),'nonself_deviations':count,'actual':actual,'payoffs':[u(actual,i) for i in range(m)],'W':W,'OPT':OPT,'actual_V':V,'root_incumbent_min':root_min,'child_third_mover_options':rows,'child_incumbent_min':child_min,'factor':F(3,4),'gap':root_min-F(3,4)*child_min,'method':'unit-customer full histories and all last-BR endpoints, no CAG solver imported'}
print(json.dumps(r,ensure_ascii=False,indent=2,default=str))
