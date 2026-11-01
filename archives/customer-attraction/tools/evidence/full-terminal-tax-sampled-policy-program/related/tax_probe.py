from fractions import Fraction as F
from itertools import product, combinations
from functools import lru_cache
import json, math, sys
import numpy as np
from scipy.optimize import linprog
n=4;k=6
masks=list(range(1,1<<k))
seed={1:12,2:8,4:4,8:8,17:6,33:6,20:3,36:3,49:6,50:2,52:1,56:2}
def coef(a,z,M):
    return F(1,sum((M>>b)&1 for b in z)) if (M>>a)&1 else F(0)
def cvec(a,z):return [coef(a,z,M) for M in masks]
def terminal(z,weights):
    vals=[sum(weights.get(M,0)*coef(a,z+(a,),M) for M in masks) for a in range(k)]
    return max(range(k),key=lambda a:(vals[a],a))
sigma={h:(0 if len(h)<n-1 else terminal(h,seed)) for d in range(n) for h in product(range(k),repeat=d)}
def optimize(sigma):
    @lru_cache(None)
    def end(h):return h if len(h)==n else end(h+(sigma[h],))
    root=end(())
    gam=[]
    for h,a0 in sigma.items():
      z0=end(h)
      for a in range(k):
        z=end(h+(a,))
        gam.append([coef(a0,z0,M)-coef(a,z,M) for M in masks])
    act=[sum((M>>a)&1 for a in root) for M in masks]
    # optimum comparator arbitrary <=n actions; try all n-subsets
    opts=[]
    for cc in combinations(range(k),min(n,k)):
      cost=[-(int(any((M>>a)&1 for a in cc))-int(c>0)-F(c,c+1)) for M,c in zip(masks,act)]
      res=linprog(np.array(cost,float),A_ub=-np.array(gam,float),b_ub=np.zeros(len(gam)),A_eq=np.ones((1,len(masks))),b_eq=[1],bounds=(0,None),method='highs')
      if res.success:opts.append((res.fun,cc,res.x))
    return min(opts,key=lambda x:x[0]),root,gam
if __name__=='__main__':
  (f,cc,w),z,g=optimize(sigma)
  print('value',-f,'comparator',cc,'root',z)
  ws={M:F(float(x)).limit_denominator(1000000) for M,x in zip(masks,w) if x>1e-8}
  den=math.lcm(*(x.denominator for x in ws.values()));wi={M:int(x*den) for M,x in ws.items()}
  vals=[sum(row[masks.index(M)]*v for M,v in wi.items()) for row in g]
  print('weights',wi,'minGamma',min(vals))
