import random,itertools,json,time
import numpy as np
from scipy.optimize import linprog
from functools import lru_cache
from fractions import Fraction
rng=random.Random(948153)

def comp(n,k):
 if k==1: yield (n,); return
 for a in range(n+1):
  for q in comp(n-a,k-1):yield (a,)+q

def scan(k,r,t,reps):
 masks=np.array([[int(mask>>a&1) for a in range(k)] for mask in range(1,1<<k)],dtype=float)
 K=len(masks)
 backgrounds=list(comp(t,k));qs=list(comp(r,k));best=0.
 for rep in range(reps):
  b=backgrounds[rng.randrange(len(backgrounds))]
  w=np.array([rng.randrange(0,50) if rng.random()<.6 else 0 for _ in range(K)],dtype=float)
  @lru_cache(None)
  def payoff(c):
   d=masks@np.array(c);return (masks/np.maximum(1,d)[:,None]).T
  moves={};out={};rows=[]
  @lru_cache(None)
  def solve(q):
   if sum(q)==r:
    c=tuple(b[a]+q[a] for a in range(k));return c
   children=[];values=[]
   for a in range(k):
    v=list(q);v[a]+=1;c=solve(tuple(v));children.append(c);values.append(payoff(c)[a]@w)
   a=max(range(k),key=lambda a:values[a]+rng.random()*1e-8)
   c=children[a];moves[q]=a;out[q]=c
   for a2 in range(k):rows.append(payoff(c)[a]-payoff(children[a2])[a2])
   return c
  c=solve((0,)*k);q=tuple(c[a]-b[a] for a in range(k))
  den=masks@np.array(c);R=(masks@np.array(q))/np.maximum(1,den)
  comps=[]
  for v in qs:
   v=np.array(v);d=masks@v;f=d/np.maximum(1,masks@np.array(b)+d);comps.append(f)
  if rep%4: candidates=[max(comps,key=lambda f:f@w)]
  else:candidates=rng.sample(comps,min(5,len(comps)))
  for F in candidates:
   lp=linprog(-F,A_ub=-np.array(rows),b_ub=np.zeros(len(rows)),A_eq=[R],b_eq=[1],bounds=[(0,None)]*K,method='highs')
   if not lp.success:continue
   ratio=-lp.fun
   if ratio>best+1e-7:
    best=ratio
    print('BEST',k,r,t,rep,b,c,ratio,'support',np.sum(lp.x>1e-8),flush=True)
   if ratio>2+1e-7:
    data={'k':k,'r':r,'t':t,'b':b,'terminal':c,'w':lp.x.tolist(),'F':F.tolist(),'moves':[(q,a) for q,a in moves.items()],'ratio':ratio}
    path='research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/induction/background_failure_float.json'
    with open(path,'w') as f:json.dump(data,f)
    return False
 print('DONE',k,r,t,reps,best,flush=True);return True
if __name__=='__main__':
 for args in [(6,3,1,200),(6,3,3,200),(6,4,1,200),(7,4,2,100),(6,5,1,100),(7,5,2,50)]:
  if not scan(*args):break
