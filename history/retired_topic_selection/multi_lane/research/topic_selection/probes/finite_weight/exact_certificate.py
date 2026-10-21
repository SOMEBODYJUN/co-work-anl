"""Exact rational check of a two-type, 4-player local potential certificate."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

states=list(product(range(3),range(3))); idx={s:i for i,s in enumerate(states)}
alpha=Q(37,33); A=[]; b=[]
for k,l in states:
 for dk,dl,w in [(1,0,1),(0,1,2)]:
  if k+dk>2 or l+dl>2:continue
  v=idx[(k+dk,l+dl)];u=idx[(k,l)];cost=w*(k+2*l+w)**2
  row=np.zeros(9);row[u]=1;row[v]=-1;A.append(row);b.append(-cost)
  row=np.zeros(9);row[v]=1;row[u]=-1;A.append(row);b.append(float(alpha*cost))
r=linprog(np.zeros(9),A_ub=A,b_ub=b,bounds=[(0,0)]+[(None,None)]*8,method='highs')
assert r.success
F={s:Q(float(r.x[i])).limit_denominator(100000) for s,i in idx.items()}
checks=[]
for k,l in states:
 for dk,dl,w in [(1,0,1),(0,1,2)]:
  if k+dk>2 or l+dl>2:continue
  cost=Q(w*(k+2*l+w)**2); diff=F[k+dk,l+dl]-F[k,l]
  assert cost<=diff<=alpha*cost,(k,l,w,cost,diff)
  checks.append(dict(start=[k,l],weight=w,cost=str(cost),marginal=str(diff),ratio=str(diff/cost)))
print('CERTIFIED',str(alpha),'12 marginal inequalities; all arithmetic rational')
for k in range(3):print(k,[str(F[k,l]) for l in range(3)])
# A necessary lower bound for this certificate template follows by two paths
# from (0,0) to (2,1): light/light/heavy costs 1+4+32=37;
# heavy/light/light costs 8+9+16=33, so alpha >=37/33.
assert Q(1+4+32,8+9+16)==alpha
out=dict(alpha=str(alpha),states={f'{k},{l}':str(v) for (k,l),v in F.items()},checks=checks,
 template_lower_bound={'long_path_cost':37,'short_path_cost':33})
Path(__file__).with_name('exact_certificate.json').write_text(json.dumps(out,indent=2))
