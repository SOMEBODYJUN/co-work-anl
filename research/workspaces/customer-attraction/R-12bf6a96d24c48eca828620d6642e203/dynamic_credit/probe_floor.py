from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
m=3;k=6; types=list(range(1,1<<k))
def sigma(h):
 if not h:return 0
 if len(h)==1:return 3 if h[0]<3 else 0
 b=h[1];return next(a for a in range(0 if b<3 else 3,3 if b<3 else 6) if a not in h)
def end(h):
 while len(h)<m:h=h+(sigma(h),)
 return h
def pay(a,z,t):return F(int(t>>a&1),sum(t>>b&1 for b in z)) if t>>a&1 else F(0)
rows=[]
for depth in range(m):
 for h in product(range(k),repeat=depth):
  z=end(h);a=sigma(h)
  for q in range(k):
   if q==a:continue
   zd=end(h+(q,));rows.append([pay(a,z,t)-pay(q,zd,t) for t in types])
z=end(());u=np.array([float(pay(z[0],z,t)) for t in types]);cov=np.array([int(any(t>>a&1 for a in z)) for t in types]);A=-np.array(rows,dtype=float)
best=(-1,None)
for comp in combinations_with_replacement(range(k),m):
 opt=np.array([int(any(t>>a&1 for a in comp)) for t in types]);obj=opt-5*u
 res=linprog(-obj,A_ub=A,b_ub=np.zeros(len(rows)),A_eq=cov.reshape(1,-1),b_eq=[1],bounds=(0,None),method='highs')
 if res.success and -res.fun>best[0]+1e-9:best=(-res.fun,(comp,res))
print('best floor violation',best[0],best[1][0]);r=best[1][1];ww=[F(float(x)).limit_denominator(100000) for x in r.x];print({t:str(w) for t,w in zip(types,ww) if w});print('minrow',min(sum(a*w for a,w in zip(row,ww)) for row in rows));print('first',sum(pay(z[0],z,t)*w for t,w in zip(types,ww)))
