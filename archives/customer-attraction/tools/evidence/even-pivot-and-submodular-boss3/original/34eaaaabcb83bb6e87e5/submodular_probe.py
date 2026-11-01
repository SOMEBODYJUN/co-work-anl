"""Discovery only: full set-submodular Shapley lift at 3 players, fixed complete policy.
This is an enlarged model, not the actual CAG cone. No floating bound is a proof.
"""
from itertools import product,combinations_with_replacement
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
import json,argparse,math
from pathlib import Path

def solve(k,p,star=False):
 n=(1<<k)-1
 @lru_cache(None)
 def phi(h):
  d=len(h);r=np.zeros(n)
  for sm in range(1,1<<d):
   mask=0
   for i,a in enumerate(h):
    if sm>>i&1:mask|=1<<a
   j=sm.bit_count();r[mask-1]+=math.factorial(j-1)*math.factorial(d-j)/math.factorial(d)
  return r
 def u(h,a):return phi(tuple(sorted(h+(a,))))-phi(tuple(sorted(h)))
 def act(h):
  if not h:return 0
  if len(h)==1:return k//2 if h[0]<k//2 else 0
  group=range(k//2) if h[1]<k//2 else range(k//2,k)
  return next(a for a in group if a not in h)
 def term(h):
  while len(h)<3:h=h+(act(h),)
  return h
 def payoff(z,a):
  zz=list(z);zz.remove(a);return u(tuple(sorted(zz)),a)
 def vec(mask):
  z=np.zeros(n)
  if mask:z[mask-1]=1
  return z
 constraints=[]
 for s in range(1<<k):
  for a in range(k):
   if s>>a&1:continue
   constraints.append(vec(s)-vec(s|1<<a))
   for b in range(a+1,k):
    if s>>b&1:continue
    constraints.append(vec(s)+vec(s|1<<a|1<<b)-vec(s|1<<a)-vec(s|1<<b))
 for d in range(3):
  for h in product(range(k),repeat=d):
   z=term(h);a=act(h)
   for b in range(k):
    if b!=a:constraints.append(payoff(term(h+(b,)),b)-payoff(z,a))
 if star:
  for d in range(2):
   for h in combinations_with_replacement(range(k),d):
    for a,b,c in product(range(k),repeat=3):
     constraints.append(phi(tuple(sorted(h+(a,a))))+phi(tuple(sorted(h+(b,c))))-phi(tuple(sorted(h+(a,b))))-phi(tuple(sorted(h+(a,c)))))
 for h in combinations_with_replacement(range(k),2):
  constraints.append(-sum(p[a]*u(h,a) for a in range(k)))
 A=np.zeros((len(constraints),n+1));A[:,:n]=constraints;A[-math.comb(k+1,2):,-1]=1
 z=term(());pay=sum(payoff(z,a) for a in z);pair=payoff(z,z[0])+payoff(z,z[1])
 c=np.zeros(n+1);c[-1]=-1
 r=linprog(c,A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[pay,0]],b_eq=[1],bounds=[(0,None)]*(n+1),method='highs')
 out={'k':k,'query':list(p),'star_tax':star,'status':r.message,'P':1,'t':r.x[-1] if r.success else None,'triple_ratio':3*r.x[-1] if r.success else None,'enlarged_model':True,'floating_only':True}
 if r.success:out['F']=r.x[:-1].tolist();out['pair']=float(pair@r.x[:-1]);out['actual']=list(z)
 return out

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--trials',type=int,default=10);a.add_argument('--star',action='store_true');a.add_argument('--output',required=True);args=a.parse_args();rng=np.random.default_rng(22107);best=None
 for j in range(args.trials):
  p=np.ones(6)/6 if j==0 else rng.dirichlet(np.ones(6))
  out=solve(6,p,args.star)
  if out['t'] is not None and (best is None or out['t']>best['t']):best=out;Path(args.output).write_text(json.dumps(best,indent=2)+'\n');print({k:v for k,v in out.items() if k!='F'},flush=True)
