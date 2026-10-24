"""Single conjecture attack: occupancy payment; do not infer proof from finite tests.
Start with the known all-history collision-free family certificate, then allow
arbitrary customer incidence consistent with collision-free actual play and all
of that complete certificate's IC rows. This is not a new fixed-size bound task.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
import json,numpy as np
from scipy.optimize import linprog
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver
OUT=Path(__file__).parent
k=2;m=k+1
coverage=[]
for i in range(k):
 X={f'x{i}a',f'x{i}b'}
 coverage.extend([X|{f'a{i}'},X|{'b'},X])
coverage.append({'b','d'})
p=len(coverage)
inst=Instance.from_topic_sets(coverage,m)
target=tuple([2,5,6]);counts=inst.counts(target,terminal=True)
solver=ExactSPESolver(inst);cert=solver.certificate(on_path=target)
actions=cert.actions
masks=[mask for mask in range(1,1<<p) if sum(mask>>a&1 for a in target)<=1]
def leaf(h):
 while len(h)<m:h=h+(actions[h],)
 return h
def payoff(mask,h,a):
 return Fraction(1,sum(mask>>b&1 for b in h)) if mask>>a&1 else Fraction()
rows=[]
for h,chosen in actions.items():
 actual=leaf(h);us=[payoff(mask,actual,chosen) for mask in masks]
 for a in range(p):
  if a!=chosen:
   alt=leaf(h+(a,));rows.append([float(payoff(mask,alt,a)-u) for mask,u in zip(masks,us)])
c=np.array([1.5 if any(mask>>a&1 for a in target) else 0.0 for mask in masks])
maximum=0
for opt in combinations(range(p),m):
 o=np.array([float(any(mask>>a&1 for a in opt)) for mask in masks])
 res=linprog(-o,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=c[None,:],b_eq=[1],bounds=(0,None),method='highs')
 if res.success:
  maximum=max(maximum,-res.fun)
  if -res.fun>1+1e-8:
   print('CANDIDATE',opt,-res.fun)
   (OUT/'collisionfree_extension_failure.json').write_text(json.dumps({'comparison':opt,'value':-res.fun,'masks':masks,'weights':res.x.tolist(),'actions':[{'history':h,'action':a} for h,a in actions.items()]},indent=2));break
print('maximum relative conjecture RHS',maximum,'masks',len(masks),'IC rows',len(rows))
