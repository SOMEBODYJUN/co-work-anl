import random,itertools,json
import numpy as np
from scipy.optimize import linprog
from functools import lru_cache
rng=random.Random(72218)
def comp(n,k):
 if k==1:yield (n,);return
 for a in range(n+1):
  for q in comp(n-a,k-1):yield (a,)+q

def scan(k,r,t,reps):
 masks=np.array([[int(mask>>a&1) for a in range(k)] for mask in range(1,1<<k)],dtype=float)
 K=len(masks);backgrounds=list(comp(t,k));best=0.
 for rep in range(reps):
  b=backgrounds[rng.randrange(len(backgrounds))];w=np.array([rng.randrange(0,50) if rng.random()<.6 else 0 for _ in range(K)],dtype=float)
  @lru_cache(None)
  def payoff(c):return (masks/np.maximum(1,masks@np.array(c))[:,None]).T
  moves={};rows=[]
  @lru_cache(None)
  def solve(q):
   if sum(q)==r:return tuple(b[a]+q[a] for a in range(k))
   children=[];values=[]
   for a in range(k):
    v=list(q);v[a]+=1;c=solve(tuple(v));children.append(c);values.append(payoff(c)[a]@w)
   a=max(range(k),key=lambda a:values[a]+rng.random()*1e-8);c=children[a];moves[q]=a
   for a2 in range(k):rows.append(payoff(c)[a]-payoff(children[a2])[a2])
   return c
  c=solve((0,)*k);a=moves[(0,)*k];u=payoff(c)[a]
  tuples=list(itertools.combinations([v for v in range(k) if v!=a],r))
  for T in rng.sample(tuples,min(3,len(tuples))):
   es=np.array([((masks@np.array(b)==0)&(masks[:,a]==0)&(masks[:,j]==1)&(np.sum(masks[:,T],axis=1)==1)).astype(float) for j in T])
   A=np.vstack([np.column_stack([-np.array(rows),np.zeros(len(rows))]),np.column_stack([-es,np.ones(len(es))])])
   lp=linprog(np.r_[np.zeros(K),-1],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[u,0]],b_eq=[1],bounds=[(0,None)]*(K+1),method='highs')
   if not lp.success:continue
   ratio=-lp.fun
   if ratio>best+1e-7:best=ratio;print('BEST',k,r,t,rep,b,c,a,T,ratio,'support',np.sum(lp.x[:K]>1e-8),flush=True)
   if ratio>2+1e-7:
    data={'k':k,'r':r,'t':t,'b':b,'terminal':c,'a':a,'w':lp.x[:K].tolist(),'T':T,'moves':[(q,a) for q,a in moves.items()],'ratio':ratio}
    with open('research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/induction/private_block_failure_float.json','w') as f:json.dump(data,f)
    return False
 print('DONE',k,r,t,reps,best,flush=True);return True
if __name__=='__main__':
 for args in [(6,3,0,250),(6,4,0,250),(6,4,1,200),(7,5,0,150),(7,5,1,150)]:
  if not scan(*args):break
