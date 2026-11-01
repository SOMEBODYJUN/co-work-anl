#!/usr/bin/env python3
"""Definition-level check: extra-slot aggregate counterexample without empty themes."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[5]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json'
d=json.loads(SOURCE.read_text()); sigma={tuple(a['history']):a['action'] for a in d['certificate']['actions']}
k=7;m=3;query=2;proxy=6;K=67;J=1;eps=F(1,24)
customers=[frozenset(c['topics']) for c in d['instance']['customers'] for _ in range(K*c['multiplicity'])]+[frozenset({proxy}) for _ in range(J)]

def endpoint(h):
 h=tuple(h)
 while len(h)<m:h=h+(sigma[h],)
 return h

def payoff(z,i):
 return sum((F(1,sum(a in x for a in z)) for x in customers if z[i] in x),F(0))

def insert(z,a):
 return sum((F(1,1+sum(t in x for t in z)) for x in customers if a in x),F(0))

sets=[frozenset(i for i,x in enumerate(customers) if a in x) for a in range(k)]
assert all(sets) and len(set(sets))==k
comparisons=0; slack_min=None
for n in range(m):
 for h in product(range(k),repeat=n):
  z=endpoint(h);u=payoff(z,n)
  assert sigma[h]!=proxy
  for a in range(k):
   slack=u-payoff(endpoint(h+(a,)),n)
   assert slack>=0,(h,a,slack)
   if a!=sigma[h]:
    comparisons+=1; slack_min=slack if slack_min is None else min(slack_min,slack)
actual=endpoint(())

def sums(e):
 ps={query:e,proxy:1-e};D=F(0);G=F(0)
 for i in range(m):
  for a,pa in ps.items():
   z=endpoint(actual[:i]+(a,));D+=pa*payoff(z,i)
   G+=sum((pa*pt*insert(z,t) for t,pt in ps.items()),F(0))
 return D,G

for e in [F(0),F(1,100),F(1,24),F(70,1611),F(1,12),F(1,2),F(1)]:
 D,G=sums(e)
 assert D-G==K*(12*e*e-e)+F(3*J,2)*(1-e)**2
D,G=sums(eps);assert D-G==-F(7,384)
W=sum((payoff(actual,i) for i in range(m)),F(0))
OPT=max(sum(any(a in x for a in z) for x in customers) for z in product(range(k),repeat=m))
assert W==32*K and OPT==34*K and 2*W>=OPT
report={'source':str(SOURCE.relative_to(ROOT)),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'K':K,'private_proxy_customers':J,'customers':len(customers),'all_topics_nonempty_distinct':True,'histories':len(sigma),'nonself_deviations':comparisons,'actual':actual,'W':W,'OPT':OPT,'epsilon':eps,'D':D,'G':G,'gap':D-G,'quadratic_coefficients':[F(3*J,2),-K-3*J,12*K+F(3*J,2)],'discriminant':K*(K-66*J),'method':'expanded unit customers, full ordered history comparison; no CAG solver imported'}
print(json.dumps(report,ensure_ascii=False,indent=2,default=str))
