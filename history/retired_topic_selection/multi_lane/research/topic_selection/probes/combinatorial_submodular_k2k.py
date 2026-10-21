"""Finite numerical probe, not a global optimization proof.
Python 3 + numpy/scipy. Seed 20261020. Checks explicit rank enumeration too.
"""
import json, math
from itertools import product
from fractions import Fraction
import numpy as np
from scipy.optimize import minimize
rng=np.random.default_rng(20261020)

def nullity(a):
 p=np.array(a)**2/4
 return p.sum()-1+np.prod(1-p)
def ratio(a):
 return 1-nullity(a)/(len(a)+1)
def enum_rank(x):
 k=len(x)//2; ans=0
 for bits in product((0,1),repeat=2*k):
  c=sum(bits[2*i]*bits[2*i+1] for i in range(k))
  rank=sum(bits)-max(0,c-1)
  prob=math.prod(x[i] if b else 1-x[i] for i,b in enumerate(bits))
  ans+=prob*rank
 return ans
out={"seed":20261020,"status":"finite numerical evidence, not proof","base_optimizations":[],"rank_checks":[]}
for k in range(2,17):
 cand=[]
 starts=[np.full(k,1+1/k)]
 for i in range(k):
  a=np.ones(k);a[i]=2;starts.append(a)
 for _ in range(120):
  a=1+rng.dirichlet(np.ones(k));starts.append(a)
 for a in starts:
  res=minimize(ratio,a,method='SLSQP',bounds=[(1,2)]*k,constraints=[{'type':'eq','fun':lambda a:sum(a)-(len(a)+1)}],options={'ftol':1e-13,'maxiter':1000})
  if res.success and abs(sum(res.x)-(k+1))<1e-8:
   cand.append((res.fun,res.x.tolist()))
 best=min(cand)
 out['base_optimizations'].append(dict(k=k,best=best[0],a=best[1],symmetric=ratio(np.full(k,1+1/k)),one_full=ratio([2]+[1]*(k-1)),successful_starts=len(cand)))
for k in range(1,5):
 for tag,x in [('zero',[0.]*(2*k)),('all',[1.]*(2*k)),('balanced',[.5]*(2*k)),('random',rng.uniform(size=2*k).tolist())]:
  p=[x[2*i]*x[2*i+1] for i in range(k)]
  formula=sum(x)-sum(p)+1-math.prod(1-z for z in p)
  direct=enum_rank(x)
  assert abs(formula-direct)<1e-10
  out['rank_checks'].append(dict(k=k,tag=tag,formula=formula,enumerated=direct,error=abs(formula-direct)))
print(json.dumps(out,indent=2))
