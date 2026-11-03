"""Finite attack on conjectural OPT_m <= 2W-u_last. Not a proof of universality."""
from itertools import product, combinations
from random import Random
from math import lcm
import json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def run(m,k,trials,seed):
 rng=Random(seed);L=lcm(*range(1,m+1));masks=np.arange(1,1<<k)
 mem=np.array([[(s>>a)&1 for s in masks] for a in range(k)],dtype=int)
 opts=[np.max(mem[list(s)],axis=0) for s in combinations(range(k),min(m,k))]
 best=0.;start=time.time()
 for trial in range(trials):
  weights=np.array([rng.randrange(1,51) if rng.random()<.27 else 0 for s in masks],dtype=int)
  valcache={}; coefcache={};action={};terminal={}
  def coef(a,z):
   key=(a,z)
   if key not in coefcache:
    counts=np.sum(mem[list(z)],axis=0)
    coefcache[key]=np.divide(L*mem[a],counts,out=np.zeros(len(masks),dtype=float),where=counts>0)
   return coefcache[key]
  def rec(h):
   if len(h)==m:return h
   zs=[rec(h+(a,)) for a in range(k)]
   values=[coef(a,z)@weights for a,z in enumerate(zs)]
   mx=max(values);ties=[a for a in range(k) if values[a]>=mx-.00001]
   # Deliberately permit ordered-history ties.
   a=rng.choice(ties);action[h]=a;terminal[h]=zs[a]
   return zs[a]
  actual=rec(())
  rows=[]
  for h,a in action.items():
   lhs=coef(a,terminal[h])
   for b in range(k):
    if b==a:continue
    hb=h+(b,);z=hb if len(hb)==m else terminal[hb]
    rows.append(lhs-coef(b,z))
  rows=np.array(rows)/L
  c=(np.sum(mem[list(actual)],axis=0)>0).astype(float)
  ulast=coef(actual[-1],actual)/L
  for oi,o in enumerate(opts):
   objective=o-2*c+ulast
   res=linprog(-objective,A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=[c],b_eq=[1],bounds=(0,None),method='highs')
   if res.status!=0:continue
   gap=-res.fun
   if gap>best+1e-8:
    best=gap;print('BEST',m,k,trial,gap,'actual',actual,flush=True)
   if gap>1e-7:
    obj={'m':m,'k':k,'trial':trial,'seed':seed,'actual':actual,'normalized_violation':gap,'weights':res.x.tolist(),'actions':{','.join(map(str,h)):a for h,a in action.items()},'opt_index':oi}
    p=Path(__file__).with_name(f'additive_terminal_failure_m{m}_k{k}_s{seed}.json');p.write_text(json.dumps(obj,indent=2))
    print('FAIL',p,flush=True);return obj
  if trial%50==0:print('progress',m,k,trial,'seconds',time.time()-start,'best',best,flush=True)
 print('DONE',m,k,trials,'best',best,'seconds',time.time()-start,flush=True)
if __name__=='__main__':run(*map(int,sys.argv[1:]))
