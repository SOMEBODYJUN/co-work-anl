"""Auxiliary arbitrary subset potential, then (if found) must compile and audit.
A floating candidate is not a legal customer instance or a SPE certificate.
"""
from __future__ import annotations
import itertools as it,json,argparse
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def run(k,n,trials,seed,out):
 rng=np.random.default_rng(seed);normal=[i for i in range(k) if i not in(2,5)];queries=[2,5];p={2:.5,5:.5}
 subsets=[s for d in range(1,n+1) for s in it.combinations(range(k),d)];sid={s:i for i,s in enumerate(subsets)};d=len(subsets)
 def pay(a,z):
  v=np.zeros(d);v[sid[tuple(sorted(z))]]+=1;v[sid[tuple(sorted(x for x in z if x!=a))]]-=1;return v
 summary={'kind':'floating signed potential exploration only','trials':trials,'best_gap':0,'completed':0}
 for trial in range(trials):
  policy={():0};ends={}
  for a in range(k):
   policy[a,]=int(rng.choice([b for b in normal if b!=a]))
   for b in range(k):
    if b==a:continue
    policy[a,b]=int(rng.choice([c for c in normal if c not in(a,b)]))
  for h in sorted(policy,key=len,reverse=True):
   children=[h+(a,) if len(h)==n-1 else ends[h+(a,)] for a in range(k) if a not in h]
   actions=[a for a in range(k) if a not in h]
   ends[h]=children[actions.index(policy[h])]
  gam=[]
  for h,a0 in policy.items():
   actual=pay(a0,ends[h])
   for a in range(k):
    if a in h or a==a0:continue
    z=h+(a,) if len(h)==n-1 else ends[h+(a,)]
    gam.append(actual-pay(a,z))
  z=ends[()];c=sum((pay(a,z) for a in z),start=np.zeros(d));bgs=set()
  for i in range(n):
   h=z[:i]
   for a in range(k):
    if a in h:continue
    zz=h+(a,) if i==n-1 else ends[h+(a,)]
    bgs.add(tuple(sorted(zz[:i]+zz[i+1:])))
  assert not any(set(b)&set(queries) for b in bgs)
  beta=[sum((p[a]*pay(a,b+(a,)) for a in queries),start=np.zeros(d)) for b in bgs]
  ub=np.vstack((np.c_[-np.array(gam),np.zeros(len(gam))],np.c_[-np.array(beta),np.ones(len(beta))]))
  obj=np.r_[c,-n]
  ans=linprog(obj,A_ub=ub,b_ub=np.zeros(len(ub)),bounds=[(-1,1)]*d+[(None,None)],method='highs')
  if not ans.success:raise RuntimeError(ans.message)
  gap=-ans.fun;summary['completed']=trial+1
  if gap>summary['best_gap']+1e-8:
   summary['best_gap']=float(gap);summary['witness']={'policy':{','.join(map(str,h)):a for h,a in policy.items()},'root':z,'backgrounds':sorted(bgs),'F':{','.join(map(str,s)):float(v) for s,v in zip(subsets,ans.x[:-1])},'beta':float(ans.x[-1])}
   out.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'trial':trial,'gap':gap}),flush=True)
  if gap>1e-7:break
 out.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'completed':summary['completed'],'gap':summary['best_gap']}))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=1000);ap.add_argument('--seed',type=int,default=205301);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();run(6,3,a.trials,a.seed,a.output)
