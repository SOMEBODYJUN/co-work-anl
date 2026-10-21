"""Discovery-only Cartesian-catalog full outcome-set probe.

No Markov restriction: count caching retains the full realizable outcome set.
Any strict finding must be rationally reconstructed and independently audited.
"""
import argparse,itertools as it,json,time
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def profiles(k,n):
 z=list(it.combinations_with_replacement(range(k),n))
 q=np.array([[x.count(a) for a in range(k)] for x in z])
 return z,q,{tuple(v):i for i,v in enumerate(q)}

def utility(q,C):
 load=q@C
 return C[None,:,:]/np.maximum(load[:,None,:],1), (load>0).astype(float)

def security(w,C,n):
 _,q,_=profiles(len(C),n-1)
 f=C[None,:,:]/(1+(q@C)[:,None,:])
 B=f@w
 lp=linprog(np.r_[np.zeros(len(C)),-1.],A_ub=np.c_[-B,np.ones(len(B))],b_ub=np.zeros(len(B)),A_eq=[np.r_[np.ones(len(C)),0]],b_eq=[1],bounds=[(0,None)]*len(C)+[(None,None)],method='highs')
 assert lp.success
 return lp.x[-1]

def outcomes(u,w,k,n,ix):
 @lru_cache(None)
 def calc(q):
  if sum(q)==n:return np.array([ix[q]],dtype=int)
  child=[calc(tuple(q[b]+(a==b) for b in range(k))) for a in range(k)]
  floor=max(np.min(u[ch,a]) for a,ch in enumerate(child))
  return np.unique(np.concatenate([ch[u[ch,a]>=floor-1e-9] for a,ch in enumerate(child)]))
 z=calc((0,)*k)
 return z,calc

def main():
 p=argparse.ArgumentParser();p.add_argument('--k',type=int,default=3);p.add_argument('--n',type=int,default=3);p.add_argument('--trials',type=int,default=1000);p.add_argument('--seed',type=int,default=5101);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 k,n=a.k,a.n;K=k*k
 C=np.array([[(mask>>b)&1 for mask in range(1,1<<k)]for b in range(k)])
 Cprod=np.array([np.r_[C[i],C[j]]for i,j in it.product(range(k),repeat=2)])
 zs,qs,ix=profiles(K,n);us,ws=utility(qs,Cprod)
 zc,qc,ic=profiles(k,n);uc,wc=utility(qc,C)
 rng=np.random.default_rng(a.seed);best=10;bestadd=1;bestpair=10
 start=time.time()
 for t in range(a.trials):
  r=rng.integers(0,10,2*((1<<k)-1));r*=rng.random(len(r))<rng.choice([.3,.5,.75,1.]);
  if sum(r)==0:continue
  u,w=us@r,ws@r
  root,calc=outcomes(u,w,K,n,ix);j=min(root,key=lambda j:w[j]);W=w[j];target_j=j
  safe=sum(security(r[x*len(C[0]):(x+1)*len(C[0])],C,n) for x in range(2))
  mins=[]
  for x in range(2):
   rr=r[x*len(C[0]):(x+1)*len(C[0])];o,_=outcomes(uc@rr,wc@rr,k,n,ic);mins.append(min((wc@rr)[o]))
  ratio=W/(n*safe) if safe>0 else 1
  add=W/sum(mins) if sum(mins)>0 else 1
  # First two actual positions may have many orderings; recover all admissible prefix pairs.
  pairs=[]
  for b in range(K):
   qb=tuple(int(c==b)for c in range(K));co=calc(qb)
   fl=max(min(u[j,c] for j in calc(tuple(int(v==c)for v in range(K))))for c in range(K))
   for d in range(K):
    qbd=tuple(int(c==b)+int(c==d)for c in range(K));ch=calc(qbd)
    floor2=max(min(u[j,c]for j in calc(tuple(qb[v]+int(v==c)for v in range(K))))for c in range(K))
    for j in ch:
     if j in co and j in root and u[j,b]>=fl-1e-9 and u[j,d]>=floor2-1e-9:pairs.append((u[j,b]+u[j,d],b,d,j))
  pair=min(pairs) if pairs else (float('inf'),0,0,0)
  pr=pair[0]/(2*safe) if safe>0 else 1
  if ratio<best-1e-9 or add<bestadd-1e-9 or pr<bestpair-1e-9:
   best=min(best,ratio);bestadd=min(bestadd,add);bestpair=min(bestpair,pr)
   rec=dict(k=k,n=n,trial=t,seed=a.seed,weights=r.tolist(),W=W,v_sum=safe,strong_ratio=ratio,component_worst=mins,add_ratio=add,pair=pair,pair_ratio=pr,target=zs[target_j],best=best,bestadd=bestadd,bestpair=bestpair,status='numerical_only')
   print(json.dumps(rec,default=lambda x:x.item()),flush=True);a.out.write_text(json.dumps(rec,indent=2,default=lambda x:x.item()))
  if ratio<1-1e-7 or pr<1-1e-7:return
 print(json.dumps(dict(status='completed_no_strict_security_failure',trials=a.trials,seed=a.seed,best=best,bestadd=bestadd,bestpair=bestpair,seconds=time.time()-start)),flush=True)
if __name__=='__main__':main()
