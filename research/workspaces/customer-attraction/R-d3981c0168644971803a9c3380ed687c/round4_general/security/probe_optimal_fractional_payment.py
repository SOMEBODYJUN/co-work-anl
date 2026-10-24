"""One targeted test: can δ-optimality p=q=uniform repair FG in the
already fixed six-action full-SPE strategy cone? Numerical LP is discovery only.
No game/policy/parameter scan and no inference from a nonpositive optimum.
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
d=json.loads(RAW.read_text()); m=d['players']; k=len(d['topics'])
pol={tuple(r['history']):r['action'] for r in d['policy']}
types=list(range(1,1<<k)); p=[Q(1,k)]*k; q=p

def leaf(h):
 h=list(h)
 while len(h)<m:h.append(pol[tuple(h)])
 return tuple(h)
def load(mask,z):return sum((mask>>a)&1 for a in z)
def u(mask,z,i):
 c=load(mask,z)
 return Q((mask>>z[i])&1,c) if c else Q(0)
z=leaf(())
IC=[]
for i in range(m):
 for h in product(range(k),repeat=i):
  y=leaf(h)
  for a in range(k):
   v=leaf(h+(a,));IC.append([u(t,y,i)-u(t,v,i) for t in types])
fg=[]; welfare=[]
for t in types:
 px=sum(p[a] for a in range(k) if (t>>a)&1)
 val=Q(0)
 for i in range(m):
  mu=sum(p[a]*load(t,leaf(z[:i]+(a,))[:i]+leaf(z[:i]+(a,))[i+1:]) for a in range(k))
  val+=px/(1+mu)
 fg.append(val);welfare.append(Q(bool(load(t,z))))
f=[[Q((t>>a)&1,1)/(1+(m-1)*sum(q[b] for b in range(k) if (t>>b)&1)) for t in types] for a in range(k)]
g=[[Q((t>>a)&1,1)*sum(p[b] for b in range(k) if (t>>b)&1)/(1+(m-1)*sum(q[b] for b in range(k) if (t>>b)&1))**2 for t in types] for a in range(k)]
eq=[[Q(1)]*len(types)]+[[x-y for x,y in zip(f[a],f[0])] for a in range(1,k)]+[[x-y for x,y in zip(g[a],g[0])] for a in range(1,k)]
gap=[a-b for a,b in zip(fg,welfare)]
res=linprog(-np.array(gap,dtype=float),A_ub=-np.array(IC,dtype=float),b_ub=np.zeros(len(IC)),A_eq=np.array(eq,dtype=float),b_eq=[1.]+[0.]*(len(eq)-1),bounds=(0,None),method='highs')
report={'test':'FG only for a saddle optimal p; fixed p=q=uniform, fixed known full strategy cone','status':res.message}
if res.success:
 report['numerical_max_gap_per_customer']=-res.fun
 v=[Q(float(x)).limit_denominator(10**7) if x>1e-9 else Q(0) for x in res.x]
 den=lcm(*(x.denominator for x in v));counts=[int(x*den) for x in v];gg=reduce(gcd,counts);counts=[x//gg for x in counts]
 report['proposed_counts']={str(t):w for t,w in zip(types,counts) if w}
 report['exact_minimum_IC']=str(min(sum(x*w for x,w in zip(row,counts)) for row in IC))
 report['exact_equality_residuals']=list(map(str,[sum(x*w for x,w in zip(row,counts)) for row in eq[1:]]))
 report['exact_FG_gap']=str(sum(x*w for x,w in zip(gap,counts)))
 report['exact_delta']=str(sum(x*w for x,w in zip(f[0],counts)))
 report['exact_welfare']=sum(x*w for x,w in zip(welfare,counts)).numerator
(HERE/'optimal_fractional_payment_probe.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
