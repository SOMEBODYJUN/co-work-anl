"""Targeted falsification of pooled-mean all-p background payment.
Exactly one pre-existing six-action strategy and its known bad p. The convex
saddle constraints are intentionally absent; this tests the all-p candidate.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from math import lcm,gcd
from functools import reduce
import json
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
RAW=HERE.parents[1]/'round3_general/equilibrium/fractional_global_raw.json'
d=json.loads(RAW.read_text());m=d['players'];k=len(d['topics'])
pol={tuple(r['history']):r['action'] for r in d['policy']}
types=list(range(1,1<<k));p=[Q(int(a in (2,5)),2) for a in range(k)]
def leaf(h):
 h=list(h)
 while len(h)<m:h.append(pol[tuple(h)])
 return tuple(h)
def load(t,z):return sum((t>>a)&1 for a in z)
def u(t,z,i):
 c=load(t,z)
 return Q((t>>z[i])&1,c) if c else Q(0)
z=leaf(())
IC=[]
for i in range(m):
 for h in product(range(k),repeat=i):
  y=leaf(h)
  for a in range(k):
   v=leaf(h+(a,));IC.append([u(t,y,i)-u(t,v,i) for t in types])
pooled=[];welfare=[]
for t in types:
 px=sum(p[a] for a in range(k) if (t>>a)&1)
 mu=sum(p[a]*load(t,leaf(z[:i]+(a,))[:i]+leaf(z[:i]+(a,))[i+1:]) for i in range(m) for a in range(k))/m
 pooled.append(m*px/(1+mu));welfare.append(Q(bool(load(t,z))))
gap=[a-b for a,b in zip(pooled,welfare)]
res=linprog(-np.array(gap,dtype=float),A_ub=-np.array(IC,dtype=float),b_ub=np.zeros(len(IC)),A_eq=np.ones((1,len(types))),b_eq=[1.],bounds=(0,None),method='highs')
report={'candidate':'m*f(p,mean_i mean_query competitors)<=W for all p','fixed_query':'p=(e2+e5)/2','fixed_strategy':'old six-action complete strategy','status':res.message}
if res.success:
 report['numerical_max_gap_per_customer']=-res.fun
 v=[Q(float(x)).limit_denominator(10**7) if x>1e-9 else Q(0) for x in res.x]
 den=lcm(*(x.denominator for x in v));counts=[int(x*den) for x in v];gg=reduce(gcd,counts);counts=[x//gg for x in counts]
 report['proposed_counts']={str(t):w for t,w in zip(types,counts) if w}
 report['exact_minimum_IC']=str(min(sum(x*w for x,w in zip(row,counts)) for row in IC))
 report['exact_pooled_gap']=str(sum(x*w for x,w in zip(gap,counts)))
 report['exact_welfare']=sum(x*w for x,w in zip(welfare,counts)).numerator
 report['unit_customers']=sum(counts)
(HERE/'pooled_mean_background_probe.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
