"""Fixed automaton, arbitrary r: discovery of a two-background pair certificate.
All Gamma rows kept individually; optional symbolic-background coefficient test.
"""
from pathlib import Path
from itertools import product
import argparse,json,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

def run(n,symbolic):
 k=2*n;d=(1<<k)-1
 masks=np.arange(1,1<<k);M=((masks[None,:]>>np.arange(k)[:,None])&1).astype(float)
 def action(h):
  if not h:return 0
  if len(h)==1:return n if h[0]<n else 0
  return next(a for a in (range(n) if h[1]<n else range(n,k)) if a not in h)
 def terminal(h):
  while len(h)<n:h=h+(action(h),)
  return h
 if symbolic:
  nums=[np.zeros(n)]
  for j in range(1,n+1):
   pol=np.array([1.])
   for l in range(1,n+1):
    if l!=j:pol=np.polynomial.polynomial.polymul(pol,[l,1])
   nums.append(pol)
  nums=np.array(nums)
 def row(a,h):
  load=M[list(h)].sum(axis=0).astype(int)
  if symbolic:return (M[a,:,None]*nums[load]).flatten()
  return M[a]/np.maximum(load,1)
 G=[];labels=[]
 for depth in [0,1,n-1]:
  hs=[()] if depth==0 else [(0,)] if depth==1 else product(range(k),repeat=depth)
  for h in hs:
   chosen=action(h);old=row(chosen,terminal(h))
   for a in range(k):
    if a!=chosen:G.append(old-row(a,terminal(h+(a,))));labels.append((h,a))
 G=np.array(G);root=terminal(());B=tuple(range(n-1));C=(0,)+tuple(range(2,n));budget=row(root[0],root)+row(root[1],root)
 out={'kind':'floating discovery only','players':n,'labels':k,'symbolic_background':symbolic,'root':root,'B':B,'C':C,'queries':[],'general_half_proof':False}
 start=time.time()
 for a in range(k):
  target=budget-row(a,B+(a,))-row(a,C+(a,))
  res=linprog(np.ones(len(G)),A_ub=csr_matrix(G.T),b_ub=target,bounds=(0,None),method='highs')
  q={'a':a,'status':res.status,'message':res.message}
  if res.success:q.update(lambdas=[{'h':list(h),'a':aa,'value':float(v)} for (h,aa),v in zip(labels,res.x) if v>1e-8],min_remainder=float(np.min(target-G.T@res.x)))
  out['queries'].append(q);print(json.dumps({'query':a,'status':res.status,'rows_used':len(q.get('lambdas',[])),'seconds':time.time()-start}),flush=True)
 out['seconds']=time.time()-start
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=4);ap.add_argument('--symbolic',action='store_true');ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();o=run(a.players,a.symbolic);a.output.write_text(json.dumps(o,indent=2)+'\n')
