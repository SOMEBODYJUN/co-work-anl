"""Exploratory fixed-strategy LP attack on virtual AB tax. Not a proof."""
from functools import lru_cache
import random, json
import numpy as np
from scipy.optimize import linprog


def probe(weights,k,m,path):
 masks=list(range(1,1<<k)); w=np.array([weights.get(t,0) for t in masks],float)
 @lru_cache(None)
 def uv(a,z):return np.array([1/sum(z[b] for b in range(k) if t>>b&1) if t>>a&1 else 0 for t in masks])
 def u(a,z):return uv(a,z)@w
 @lru_cache(None)
 def ss(h):
  if sum(h)==m:return frozenset([h]),0
  cs=[]
  for a in range(k):
   z=list(h);z[a]+=1;cs.append(ss(tuple(z))[0])
  threshold=max(min(u(a,z) for z in cs[a]) for a in range(k))
  return frozenset(z for a in range(k) for z in cs[a] if u(a,z)>=threshold-1e-8),threshold
 z=tuple(path.count(a) for a in range(k)); h=[0]*k
 for a in path:
  os,t=ss(tuple(h))
  if u(a,z)<t-1e-8:return
  h[a]+=1
  if z not in ss(tuple(h))[0]:return
 sigma={}; term={}
 def recover(h,z):
  if len(h)==m:
   term[h]=z;return
  counts=tuple(h.count(a) for a in range(k));t=ss(counts)[1]
  opts=[]
  for a in range(k):
   hh=list(counts);hh[a]+=1;ocs=ss(tuple(hh))[0]
   if z in ocs and u(a,z)>=t-1e-8:opts.append(a)
  a=path[len(h)] if h==tuple(path[:len(h)]) else opts[0]
  assert a in opts
  sigma[h]=a
  for b in range(k):
   hh=list(counts);hh[b]+=1;ocs=ss(tuple(hh))[0]
   zz=z if b==a else min(ocs,key=lambda zz:u(b,zz))
   recover(h+(b,),zz)
  term[h]=term[h+(a,)]
 recover((),z)
 rows=[]
 for h,a in sigma.items():
  for b in range(k):
   if a!=b:rows.append(uv(a,term[h])-uv(b,term[h+(b,)]))
 G=np.array(rows)
 U=np.array([float(any(t>>a&1 for a in path)) for t in masks])
 ka,lb=path.count(0),path.count(1)
 result=[]
 for T in range(2,k):
  # Virtual AB cap for final two-support profiles.
  obj=[]
  for t in masks:
   ia,ib,it=(t>>0&1),(t>>1&1),(t>>T&1)
   lhs=it*(1 if not(ia or ib) else 1/ka if ia and not ib else 1/(lb+1) if ib and not ia else 1/m)
   rhs=(ka+2)/(ka*(ka+1))*ia*(1-ib)+ia*ib/m
   obj.append(lhs-rhs)
  lp=linprog(-np.array(obj),A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[U],b_eq=[1],bounds=(0,None),method='highs')
  if lp.status==3:return {'unbounded':True,'T':T,'sigma':{','.join(map(str,h)):a for h,a in sigma.items()},'path':path}
  if lp.success and -lp.fun>1e-7:
   return {'violation':-lp.fun,'T':T,'weights':{str(t):float(x) for t,x in zip(masks,lp.x) if x>1e-8},'sigma':{','.join(map(str,h)):a for h,a in sigma.items()},'path':path}
 return False

if __name__=='__main__':
 random.seed(87233);checked=0
 for rep in range(500):
  k=5;m=random.choice([4,5]);lb=random.choice([2,3]);path=[0]*(m-lb)+[1]*lb
  weights={}
  # Large disjoint A/B blocks with random overlapping auxiliary themes.
  p=random.uniform(.1,.45)
  for t in range(1,1<<k):
   ab=t&3; j=(t>>2).bit_count(); mass=(p**j)*((1-p)**(k-2-j))
   total=(m-lb)*100*1.05 if ab==1 else (lb+1)*100 if ab==2 else random.uniform(0,150) if ab==0 else random.uniform(0,100)
   weights[t]=int(total*mass*random.uniform(.5,1.5))
  got=probe(weights,k,m,path)
  if got is None:continue
  checked+=1
  if checked%10==0:print('checked',checked,'rep',rep,flush=True)
  if got:
   print(json.dumps(got,ensure_ascii=False),flush=True)
   with open(__file__.replace('.py','.json'),'w') as f:json.dump(got,f,indent=2)
   break
 else:print('completed',checked,flush=True)
