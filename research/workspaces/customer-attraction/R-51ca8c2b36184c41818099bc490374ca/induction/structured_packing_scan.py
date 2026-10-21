import numpy as np,itertools,json
from functools import lru_cache
from scipy.optimize import linprog

def comp(n,k):
 if k==1:yield (n,);return
 for a in range(n+1):
  for q in comp(n-a,k-1):yield(a,)+q

def scan(n):
 k=n+2;K=(1<<k)-1
 masks=np.array([[int(mask>>a&1) for a in range(k)] for mask in range(1,1<<k)],dtype=float)
 w=np.zeros(K);x=n-2
 for j in range(n):
  L=1<<(j+2);w[L-1]=x;w[L+2-1]=x
  if j<n-1:w[L+1-1]=1
  else:w[L+3-1]=n-1
 @lru_cache(None)
 def payoff(c):return (masks/np.maximum(1,masks@np.array(c))[:,None]).T
 moves={};rows=[];rowids=[]
 @lru_cache(None)
 def solve(q):
  if sum(q)==n:return q
  children=[]
  for a in range(k):
   v=list(q);v[a]+=1;children.append(solve(tuple(v)))
  if sum(q)==n-1:
   vals=[payoff(children[a])[a]@w for a in range(k)]
   a=max([1,0]+list(range(2,k)),key=lambda a:vals[a])
  else:a=0 if q[1]==sum(q) else 1
  c=children[a];moves[q]=a
  for a2 in range(k):
   row=payoff(c)[a]-payoff(children[a2])[a2]
   if row@w < -1e-7:raise RuntimeError((q,a,a2,row@w))
   rows.append(row);rowids.append((q,a2))
  return c
 c=solve((0,)*k);u=payoff(c)[0]
 T=tuple(range(2,k));es=np.array([((masks[:,0]==0)&(masks[:,j]==1)&(np.sum(masks[:,T],axis=1)==1)).astype(float) for j in T])
 A=np.vstack([np.column_stack([-np.array(rows),np.zeros(len(rows))]),np.column_stack([-es,np.ones(len(es))])])
 lp=linprog(np.r_[np.zeros(K),-1],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[u,0]],b_eq=[1],bounds=[(0,None)]*(K+1),method='highs')
 print('n',n,'success',lp.success,'ratio',-lp.fun if lp.success else lp.message,flush=True)
 if lp.success:
  out={'n':n,'ratio':-lp.fun,'w':[(i+1,v) for i,v in enumerate(lp.x[:K]) if v>1e-8],'dual':[(rowids[i],v) if i<len(rowids) else (('pack',i-len(rowids)),v) for i,v in enumerate(lp.ineqlin.marginals) if v < -1e-8]}
  with open('research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/induction/structured_packing_'+str(n)+'.json','w') as f:json.dump(out,f)
if __name__=='__main__':
 for n in (4,5,6):scan(n)
