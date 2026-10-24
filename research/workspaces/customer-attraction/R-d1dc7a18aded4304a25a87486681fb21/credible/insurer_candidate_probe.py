"""Finite attack on the universal effective insurer inequality, never a proof.
Candidate: 2W_H-OPT >= 3(u_root(H)-minimum full-SPE root payoff).
The exact outcome-set recurrence is used numerically for discovery only.
"""
import argparse, itertools as it, json, time
from functools import lru_cache
from pathlib import Path
import numpy as np

def setup(k,m):
 paths=list(it.combinations_with_replacement(range(k),m))
 counts=np.array([[p.count(a)for a in range(k)]for p in paths],dtype=int)
 ix={tuple(q):j for j,q in enumerate(counts)}
 C=np.array([[(b>>a)&1 for b in range(1,1<<k)]for a in range(k)],dtype=int)
 load=counts@C
 us=C[None,:,:]/np.maximum(load[:,None,:],1)
 ws=load>0
 return counts,ix,us,ws

def evaluate(w,k,m,qs,ix,us,ws):
 u=us@w;W=ws@w
 @lru_cache(None)
 def calc(q):
  if sum(q)==m:return np.array([ix[q]],dtype=int)
  child=[calc(tuple(q[b]+(a==b)for b in range(k)))for a in range(k)]
  floor=max(np.min(u[ch,a])for a,ch in enumerate(child))
  return np.unique(np.concatenate([ch[u[ch,a]>=floor-1e-9]for a,ch in enumerate(child)]))
 child=[calc(tuple(int(a==b)for b in range(k)))for a in range(k)]
 M=max(min(u[ch,a])for a,ch in enumerate(child))
 O=max(W)
 best=(-float('inf'),None)
 for a,ch in enumerate(child):
  scores=O-2*W[ch]+3*(u[ch,a]-M)
  z=int(np.argmax(scores));j=int(ch[z]);sc=float(scores[z])
  if sc>best[0]:best=(sc,dict(a=a,q=qs[j].tolist(),h=float(u[j,a]),M=float(M),W=float(W[j]),O=float(O),status='numerical_only'))
 return best

def main():
 p=argparse.ArgumentParser();p.add_argument('--k',type=int,default=4);p.add_argument('--m',type=int,default=5);p.add_argument('--trials',type=int,default=1000);p.add_argument('--seed',type=int,default=13721);p.add_argument('--out',required=True,type=Path);a=p.parse_args()
 qs,ix,us,ws=setup(a.k,a.m);rng=np.random.default_rng(a.seed);start=time.time();best=-float('inf');rec={}
 for t in range(a.trials):
  w=rng.integers(1,15,2**a.k-1);w*=rng.random(len(w))<rng.choice([.25,.5,.75,1.]);
  if not any(w):continue
  sc,r=evaluate(w,a.k,a.m,qs,ix,us,ws)
  if sc>best+1e-8:
   best=sc;rec=dict(k=a.k,m=a.m,trial=t,seed=a.seed,weights=w.tolist(),score=sc,**r);print(json.dumps(rec),flush=True)
  if sc>1e-7:
   a.out.write_text(json.dumps(rec,indent=2)+'\n');return
 rec.update(completed_trials=a.trials,seconds=time.time()-start,status='finite_no_strict_candidate_counterexample')
 a.out.write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec),flush=True)
if __name__=='__main__':main()
