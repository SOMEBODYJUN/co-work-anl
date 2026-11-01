import random,itertools,json,time
import numpy as np
from scipy.optimize import linprog
from functools import lru_cache
rng=random.Random(228419)

def comp(n,k):
 if k==1:yield (n,);return
 for a in range(n+1):
  for q in comp(n-a,k-1):yield (a,)+q

def scan(k,r,t,reps):
 masks=np.array([[int(mask>>a&1) for a in range(k)] for mask in range(1,1<<k)],dtype=float)
 K=len(masks);backgrounds=list(comp(t,k));qs=list(comp(r,k));qs_prev=list(comp(r-1,k));best=0.
 for rep in range(reps):
  b=backgrounds[rng.randrange(len(backgrounds))]
  w=np.array([rng.randrange(0,50) if rng.random()<.6 else 0 for _ in range(K)],dtype=float)
  @lru_cache(None)
  def payoff(c):
   d=masks@np.array(c);return (masks/np.maximum(1,d)[:,None]).T
  moves={};rows=[]
  @lru_cache(None)
  def solve(q):
   if sum(q)==r:return tuple(b[a]+q[a] for a in range(k))
   children=[];values=[]
   for a in range(k):
    v=list(q);v[a]+=1;c=solve(tuple(v));children.append(c);values.append(payoff(c)[a]@w)
   a=max(range(k),key=lambda a:values[a]+rng.random()*1e-8)
   c=children[a];moves[q]=a
   for a2 in range(k):rows.append(payoff(c)[a]-payoff(children[a2])[a2])
   return c
  c=solve((0,)*k);a=moves[(0,)*k];u=payoff(c)[a]
  ba=np.array(b,dtype=float);ba[a]+=1
  completions=np.array([(masks@(ba+np.array(v))>0).astype(float) for v in qs_prev])
  comps=[(masks@(np.array(b)+np.array(v))>0).astype(float) for v in qs]
  candidates=[max(comps,key=lambda f:f@w)] if rep%3 else rng.sample(comps,min(4,len(comps)))
  for F in candidates:
   # max F.w-z subject z>=each completion.w, SPE rows, u.w=1.
   A=np.vstack([np.column_stack([-np.array(rows),np.zeros(len(rows))]),np.column_stack([completions,-np.ones(len(completions))])])
   obj=np.r_[-F,1.]
   lp=linprog(obj,A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[u,0]],b_eq=[1],bounds=[(0,None)]*(K+1),method='highs')
   if not lp.success:continue
   ratio=-lp.fun
   if ratio>best+1e-7:
    best=ratio; print('BEST',k,r,t,rep,b,c,a,ratio,'support',np.sum(lp.x[:K]>1e-8),flush=True)
   if ratio>2+1e-7:
    data={'k':k,'r':r,'t':t,'b':b,'terminal':c,'a':a,'w':lp.x[:K].tolist(),'F':F.tolist(),'moves':[(q,a) for q,a in moves.items()],'ratio':ratio}
    path='research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/induction/coverage_loss_failure_float.json'
    with open(path,'w') as f:json.dump(data,f)
    return False
 print('DONE',k,r,t,reps,best,flush=True);return True
if __name__=='__main__':
 for args in [(5,3,0,200),(6,3,1,200),(6,4,0,200),(6,4,1,200),(7,5,0,100),(7,5,1,100)]:
  if not scan(*args):break
