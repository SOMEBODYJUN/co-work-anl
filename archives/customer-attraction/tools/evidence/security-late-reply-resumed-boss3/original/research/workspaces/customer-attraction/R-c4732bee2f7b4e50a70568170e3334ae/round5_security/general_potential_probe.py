"""Auxiliary symmetric exact-potential model: not a legal customer instance.
The goal is to check whether an exact-potential identity alone could prove menu safety.
"""
from __future__ import annotations
import argparse,itertools as it,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def run(k,n,trials,seed,out):
 rng=np.random.default_rng(seed)
 profiles=list(it.combinations_with_replacement(range(k),n));backgrounds=list(it.combinations_with_replacement(range(k),n-1))
 si={s:i for i,s in enumerate(profiles)};bi={b:len(profiles)+i for i,b in enumerate(backgrounds)};d=len(profiles)+len(backgrounds)
 def pay(a,z):
  v=np.zeros(d);v[si[tuple(sorted(z))]]=1
  b=list(z);b.remove(a);v[bi[tuple(sorted(b))]]-=1;return v
 nodes=[h for depth in range(n) for h in it.product(range(k),repeat=depth)]
 summary={'kind':'floating auxiliary exact-potential discovery, not legal CAG','topics':k,'players':n,'completed':0,'best_gap':0}
 for trial in range(trials):
  policy={h:int(rng.integers(k)) for h in nodes};ends={}
  for h in reversed(nodes):
   for a in range(k):
    if len(h)==n-1:ends[h+(a,)]=h+(a,)
   ends[h]=ends[h+(policy[h],)]
  gamma=[pay(policy[h],ends[h])-pay(a,ends[h+(a,)]) for h in nodes for a in range(k) if a!=policy[h]]
  z=ends[()];c=sum((pay(a,z) for a in z),start=np.zeros(d));bgs=set()
  for i in range(n):
   h=z[:i]
   for a in range(k):
    zz=ends[h+(a,)];bgs.add(tuple(sorted(zz[:i]+zz[i+1:])))
  ps=[np.ones(k)/k]+[np.array([.5 if a in pair else 0 for a in range(k)]) for pair in it.combinations(range(k),2)]
  for p in ps:
   beta=np.array([sum((p[a]*pay(a,b+(a,)) for a in range(k)),start=np.zeros(d)) for b in bgs])
   ub=np.vstack((np.c_[-np.array(gamma),np.zeros(len(gamma))],np.c_[-beta,np.ones(len(beta))]))
   ans=linprog(np.r_[c,-n],A_ub=ub,b_ub=np.zeros(len(ub)),bounds=[(-1,1)]*d+[(None,None)],method='highs')
   if not ans.success:raise RuntimeError(ans.message)
   gap=-ans.fun
   if gap>summary['best_gap']+1e-9:
    summary['best_gap']=float(gap);summary['witness']={'policy':{','.join(map(str,h)):a for h,a in policy.items()},'root':z,'backgrounds':sorted(bgs),'F':{','.join(map(str,s)):float(v) for s,v in zip(profiles,ans.x[:len(profiles)])},'G':{','.join(map(str,s)):float(v) for s,v in zip(backgrounds,ans.x[len(profiles):-1])},'beta':float(ans.x[-1]),'p':p.tolist()}
  summary['completed']=trial+1
  if summary['best_gap']>1e-7:break
 out.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'completed':summary['completed'],'gap':summary['best_gap']}))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--topics',type=int,default=3);a.add_argument('--players',type=int,default=3);a.add_argument('--trials',type=int,default=5000);a.add_argument('--seed',type=int,default=205308);a.add_argument('--output',type=Path,required=True);x=a.parse_args();run(x.topics,x.players,x.trials,x.seed,x.output)
