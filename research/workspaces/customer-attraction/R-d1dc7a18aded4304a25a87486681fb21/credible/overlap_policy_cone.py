"""Attack universal D >= 3(high-root - low-root) using a fixed real policy pair.
All nonempty customer incidences, including arbitrary overlaps, are variables.
A positive LP result is discovery only until Fraction reconstruction.
"""
from pathlib import Path
from functools import lru_cache
from itertools import product
from fractions import Fraction as F
import argparse,json
import numpy as np
from scipy.optimize import linprog


def run(m):
 masses=(2,m-1)+(1,)*(m-2)
 @lru_cache(None)
 def bi(k):
  if sum(k)==m:return k
  return max((F(masses[a],z[a]),-a,z)for a in range(m)for z in [bi(tuple(x+(j==a)for j,x in enumerate(k)))])[-1]
 def biact(h):
  k=tuple(h.count(a)for a in range(m))
  return -max((F(masses[a],z[a]),-a)for a in range(m)for z in [bi(tuple(x+(j==a)for j,x in enumerate(k)))])[-1]
 def act(h,high):
  if not h:return 0
  if h[0]==0:return 1 if high or len(h)>1 else 0
  if h[0]>1:return biact(h)
  first=next((a for a in h if a!=1),None)
  if first is None:return 0
  return 1 if first==0 else biact(h)
 def tree(high):
  @lru_cache(None)
  def end(h):return h if len(h)==m else end(h+(act(h,high),))
  rows=[]
  for d in range(m):
   for h in product(range(m),repeat=d):
    ac=act(h,high);z=end(h);cz=np.array([z.count(a)for a in range(m)])
    for b in range(m):
     zz=end(h+(b,));cc=np.array([zz.count(a)for a in range(m)])
     rows.append(pay(cz,ac)-pay(cc,b))
  return np.array(rows),end(())
 C=np.array([[(b>>a)&1 for b in range(1,1<<m)]for a in range(m)],dtype=int)
 def pay(q,a):return C[a]/np.maximum(q@C,1)
 GH,H=tree(True);GL,L=tree(False)
 qh=np.array([H.count(a)for a in range(m)]);ql=np.array([L.count(a)for a in range(m)])
 ch=(qh@C)>0;score=np.ones(2**m-1)-2*ch+3*(pay(qh,0)-pay(ql,0))
 G=np.concatenate([GH,GL]);r=linprog(-score,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=np.ones((1,2**m-1)),b_eq=[1],bounds=(0,None),method='highs')
 assert r.success
 w=[str(F(float(x)).limit_denominator(1000000))for x in r.x]
 return dict(m=m,score=float(-r.fun),weights=w,H=H,L=L,rows=len(G),types=2**m-1,status='numerical_fixed_policy_pair_only')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--m',type=int,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rec=run(a.m);a.out.write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec),flush=True)
