#!/usr/bin/env python3
"""Independent unit-customer audit of the aggregate extra-slot bridge boundary."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[5]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json'
data=json.loads(SOURCE.read_text())
inst=data['instance']; m=inst['players']; k=len(inst['topics'])
customers=[frozenset(c['topics']) for c in inst['customers'] for _ in range(c['multiplicity'])]
sigma={tuple(r['history']):r['action'] for r in data['certificate']['actions']}
expected={h for n in range(m) for h in product(range(k),repeat=n)}
assert set(sigma)==expected
assert len({frozenset(j for j,x in enumerate(customers) if a in x) for a in range(k)})==k

def endpoint(h):
 h=tuple(h)
 while len(h)<m: h=h+(sigma[h],)
 return h

def payoff(z,i):
 a=z[i]
 return sum((F(1,sum(b in x for b in z)) for x in customers if a in x),F(0))

def insert(z,a):
 return sum((F(1,1+sum(b in x for b in z)) for x in customers if a in x),F(0))

comparisons=0; slacks=[]
for h in sorted(expected,key=lambda h:(len(h),h)):
 i=len(h); z=endpoint(h); u=payoff(z,i)
 for a in range(k):
  w=endpoint(h+(a,))
  slack=u-payoff(w,i)
  assert slack>=0,(h,a,slack)
  if a!=sigma[h]: comparisons+=1; slacks.append(slack)
actual=endpoint(()); query=2; empty=6
assert not any(empty in x for x in customers)
rows=[]
for i in range(m):
 za=endpoint(actual[:i]+(query,)); ze=endpoint(actual[:i]+(empty,))
 rows.append({'position':i+1,'forced_query':za,'forced_empty':ze,'D':payoff(za,i),'vacancy':insert(ze,query),'pure_extra':insert(za,query)})
D=sum((r['D'] for r in rows),F(0)); H=sum((r['vacancy'] for r in rows),F(0)); G=sum((r['pure_extra'] for r in rows),F(0))
a=D-H; b=H-G
assert (a,b)==(F(-1),F(12))
eps=F(1,24)

def direct(e):
 ps={query:e,empty:1-e}; ds=F(0); gs=F(0)
 for i in range(m):
  for a,pa in ps.items():
   z=endpoint(actual[:i]+(a,)); ds+=pa*payoff(z,i)
   for t,pt in ps.items(): gs+=pa*pt*insert(z,t)
 return ds,gs
for e in [F(0),F(1,100),F(1,24),F(1,12),F(1,10),F(1,2),F(1)]:
 d,g=direct(e); assert d-g==a*e+b*e*e
assert direct(eps)[0]-direct(eps)[1]==-F(1,48)
W=sum((payoff(actual,i) for i in range(m)),F(0))
covered=len([x for x in customers if any(a in x for a in actual)])
assert W==covered
opt=max(sum(any(a in x for a in z) for x in customers) for z in product(range(k),repeat=m))
assert 2*W>=opt
report={'source':str(SOURCE.relative_to(ROOT)),'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'method':'independent expanded unit customers; no solver or discovery code imported','customers':len(customers),'topics':k,'players':m,'histories':len(expected),'nonself_deviations':comparisons,'actual':actual,'payoffs':[payoff(actual,i) for i in range(m)],'W':W,'OPT':opt,'rows':rows,'D':D,'vacancy':H,'pure_extra':G,'linear_coefficient':a,'quadratic_coefficient':b,'epsilon':eps,'direct_D_G':direct(eps),'gap':direct(eps)[0]-direct(eps)[1]}
print(json.dumps(report,ensure_ascii=False,indent=2,default=str))
