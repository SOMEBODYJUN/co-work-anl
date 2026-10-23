"""Attack the precise path-only certificate candidate using true count-policy SPEs.
No finite run proves the candidate. Every generated policy is backward induction.
"""
import argparse, functools, json, math
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def probe(seed, m, k):
 rng=np.random.default_rng(seed); masks=np.arange(1,2**k); incidence=((masks[:,None]>>np.arange(k))&1).astype(np.int64)
 # Keep every type positive; favor a sparse selection of the original types.
 weights=np.ones(2**k-1,dtype=np.int64)
 selected=rng.choice(len(weights),size=min(len(weights),2*k),replace=False)
 weights[selected]+=rng.integers(1,500,size=len(selected))
 action={}; scale=math.lcm(*range(1,m+1))
 assert int(weights.sum())*scale < 2**62
 @functools.lru_cache(None)
 def outcome(prefix):
  if sum(prefix)==m:return prefix
  cand=[]; vals=[]
  for t in range(k):
   p=list(prefix);p[t]+=1;q=outcome(tuple(p));cand.append(q)
   loads=incidence@q; reciprocal=np.array([scale//max(int(d),1) for d in loads],dtype=np.int64)
   vals.append(int((weights*reciprocal)@incidence[:,t]))
  vmax=max(vals);ts=[t for t,v in enumerate(vals) if v==vmax]
  chosen=int(rng.choice(ts));action[prefix]=chosen;return cand[chosen]
 c=outcome((0,)*k);actual=[];counts=[0]*k
 for i in range(m):
  t=action[tuple(counts)];actual.append(t);counts[t]+=1
 C=incidence@c; W=(C>0).astype(np.int64);G=[];prefix=[0]*k
 for i,a in enumerate(actual):
  for t in range(k):
   p=prefix.copy();p[t]+=1;d=incidence@outcome(tuple(p))
   G.append(incidence[:,a]/np.maximum(C,1)-incidence[:,t]/np.maximum(d,1))
  prefix[a]+=1
 G=np.array(G); O=np.ones(len(masks)) # m>=k permits the entire catalogue union.
 r=linprog(2*W-O,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[W],b_eq=[1],bounds=(0,None),method='highs')
 report={'seed':seed,'players':m,'topics':k,'actual':actual,'half_slack':r.fun if r.success else None}
 if r.success and r.fun < -1e-7:
  report['original_weights']={str(R):int(w)for R,w in zip(masks,weights)}
  report['bad_reweighting']={str(R):str(Fraction(float(w)).limit_denominator(1000000)) for R,w in zip(masks,r.x)if w>1e-8}
  report['count_policy']=[{'counts':list(p),'action':a}for p,a in sorted(action.items())]
 return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=20);p.add_argument('--players',type=int,default=8);p.add_argument('--topics',type=int,default=6);p.add_argument('--output');a=p.parse_args();results=[]
 assert a.players>=a.topics
 for seed in range(a.trials):
  r=probe(seed,a.players,a.topics);results.append(r);print(json.dumps({k:v for k,v in r.items()if k not in {'original_weights','bad_reweighting','count_policy'}}),flush=True)
  if r['half_slack'] is not None and r['half_slack'] < -1e-7:break
 if a.output:
  with open(a.output,'x')as f:json.dump(results,f,indent=2)
