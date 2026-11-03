from itertools import product
from scipy.optimize import linprog
import numpy as np,json,random
rng=random.Random(31)
def worst(K,r,C,d):
 def costs(z):return tuple(d[a]+sum(C[a,b] for j,b in enumerate(z) if j!=i) for i,a in enumerate(z))
 def rec(h):
  if len(h)==r:return [h]
  pools=[rec(h+(a,)) for a in range(K)];floors=[min(costs(z)[len(h)] for z in zs) for zs in pools]
  # minimization SPE: chosen branch value <= max outcome cost in each deviation branch;
  cap=min(max(costs(z)[len(h)] for z in zs) for zs in pools)
  return [z for zs in pools for z in zs if costs(z)[len(h)]<=cap+1e-8]
 zs=rec(());return max(costs(z)[0] for z in zs),zs
for r in [3,4,5]:
 for K in [3,4]:
  for it in range(2000):
   C=rng.uniform(0,1)*np.ones((K,K))
   C=np.array([[rng.randrange(8) for b in range(K)] for a in range(K)],float);C=(C+C.T)/2
   d=np.array([rng.randrange(5) for a in range(K)],float)
   A=d[:,None]+(r-1)*C
   ans=linprog(np.r_[np.zeros(K),1],A_ub=np.c_[A.T,-np.ones(K)],b_ub=np.zeros(K),A_eq=[np.r_[np.ones(K),0]],b_eq=[1],bounds=[(0,None)]*K+[(None,None)],method='highs')
   val,zs=worst(K,r,C,d)
   if val>ans.fun+1e-8:
    print(json.dumps({'r':r,'K':K,'it':it,'cost':val,'tax':ans.fun,'C':C.tolist(),'d':d.tolist()}),flush=True);raise SystemExit
print('no general symmetric-matrix witness')
