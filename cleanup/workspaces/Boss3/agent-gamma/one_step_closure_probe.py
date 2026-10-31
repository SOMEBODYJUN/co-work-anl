from fractions import Fraction as F
from itertools import combinations_with_replacement
import random,json
import numpy as np
from scipy.optimize import linprog
r=3;k=4;types=list(range(1,1<<k));tails=list(combinations_with_replacement(range(k),r-1));comps=list(combinations_with_replacement(range(k),r));random.seed(942)
def load(z,t):return sum(t>>a&1 for a in z)
def util(a,z,t):return F(int(t>>a&1),load(z,t)) if t>>a&1 else F(0)
def profit(z,b,t):
 c=load(z,t);return F(c,load(b,t)+c) if c else F(0)
def covered(z,t):return int(load(z,t)>0)
for trial in range(3000):
 response={a:random.choice(tails) for a in range(k)}
 actual=(0,)+response[0];cov=np.array([covered(actual,t) for t in types]);rows=[]
 for a in range(k):
  z=(a,)+response[a]
  if a:rows.append([util(0,actual,t)-util(a,z,t) for t in types])
  for q in tails:rows.append([2*profit(response[a],(a,),t)-profit(q,(a,),t) for t in types])
 obj=np.array([covered((1,2,3),t)-2*covered(actual,t) for t in types])
 res=linprog(-obj,A_ub=-np.array(rows,dtype=float),b_ub=np.zeros(len(rows)),A_eq=cov.reshape(1,-1),b_eq=[1],bounds=(0,None),method='highs')
 if res.success and res.fun<-1e-8:
  w=[F(float(x)).limit_denominator(100000) for x in res.x]
  print('FOUND',trial,response,'gap',sum(F(int(x))*v for x,v in zip(obj,w)))
  print({t:str(v) for t,v in zip(types,w) if v});print('minrow',min(sum(a*v for a,v in zip(row,w)) for row in rows))
  break
else:print('no witness',trial+1)
