"""Fixed Markov SPE cones for background new-coverage regret candidate.
Finite floating LP discovery only; a counterexample must be exactly audited.
"""
from fractions import Fraction
from itertools import combinations
from functools import lru_cache
from pathlib import Path
import argparse,json,random,time
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).parent

def comps(n,p):
 if p==1:yield(n,);return
 for v in range(n+1):
  for tail in comps(n-v,p-1):yield(v,)+tail

def probe(q,r,trials,seed):
 rng=random.Random(seed);masks=np.arange(1,1<<q);member=np.array([[(mask>>a)&1 for a in range(q)]for mask in masks]);allstates=[c for n in range(r)for c in comps(n,q)];terminals=list(comps(r,q));ti={t:i for i,t in enumerate(terminals)}
 best=0.;start=time.time()
 for trial in range(trials):
  prefix=[0]*q
  for _ in range(rng.randrange(0,9)):prefix[rng.randrange(q)]+=1
  bg=member@np.array(prefix);fresh=(bg==0).astype(float)
  if not any(fresh):continue
  loads=np.array([member@np.array(t)for t in terminals]);tot=loads+bg
  coeff=np.divide(member[None,:,:],tot[:,:,None],out=np.zeros((len(terminals),len(masks),q)),where=tot[:,:,None]!=0)
  w=np.array([rng.randrange(0,50)if rng.random()<.4 else 0 for _ in masks]);pay=np.einsum('tka,k->ta',coeff,w)
  policy={};out={t:t for t in terminals}
  for c in reversed(allstates):
   child=[]
   for a in range(q):
    d=list(c);d[a]+=1;child.append(out[tuple(d)])
   vals=[pay[ti[child[a]],a]for a in range(q)];v=max(vals);a=rng.choice([a for a in range(q)if abs(vals[a]-v)<1e-8]);policy[c]=a;out[c]=child[a]
  actual=out[(0,)*q];at=ti[actual];objectivebase=np.divide(loads[at],tot[at],out=np.zeros(len(masks)),where=tot[at]!=0)+fresh*(loads[at]>0)
  rows=[]
  for c in allstates:
   a=policy[c];on=coeff[ti[out[c]],:,a]
   for b in range(q):
    if b==a:continue
    d=list(c);d[b]+=1;off=coeff[ti[out[tuple(d)]],:,b];rows.append(on-off)
  rows=np.array(rows)
  comparisons=list(combinations(range(q),min(r,q)));rng.shuffle(comparisons)
  for comp in comparisons[:min(12,len(comparisons))]:
   cmpfresh=fresh*(member[:,comp].sum(axis=1)>0);obj=objectivebase-cmpfresh
   if min(obj)>=0:continue
   res=linprog(obj,A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=[np.ones(len(masks))],b_eq=[1.],bounds=(0,None),method='highs')
   if res.success and res.fun<best-1e-8:
    best=float(res.fun);data={'q':q,'r':r,'trial':trial,'prefix':prefix,'actual':actual,'comparison':comp,'policy':[[c,a]for c,a in policy.items()],'weights':{int(mask):float(v)for mask,v in zip(masks,res.x)if v>1e-9},'objective':best,'seed':seed};(ROOT/'background_regret_candidate.json').write_text(json.dumps(data,indent=2));print('FOUND',trial,best,flush=True);return
  if trial%25==0:print('trial',trial,'seconds',round(time.time()-start,1),'best',best,flush=True)
 print('completed',trials,'q',q,'r',r,'best',best,'seconds',round(time.time()-start,1),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--q',type=int,default=6);p.add_argument('--r',type=int,default=3);p.add_argument('--trials',type=int,default=200);p.add_argument('--seed',type=int,default=29393);a=p.parse_args();probe(a.q,a.r,a.trials,a.seed)
