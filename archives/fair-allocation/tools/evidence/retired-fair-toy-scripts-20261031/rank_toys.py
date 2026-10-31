"""Exact EFX checks for partition-rank costs. Integer lookup, fixed seeds."""
from itertools import product
from pathlib import Path
import numpy as np,json
P=Path(__file__).resolve().parent

def rank_tables(labels,k):
 n,m=labels.shape;D=np.zeros((n,1<<m),dtype=np.int8)
 for i in range(n):
  for s in range(1,1<<m):
   D[i,s]=len({int(labels[i,e]) for e in range(m) if s>>e&1 and labels[i,e]>=0})
 return D

def allocations(n,m):
 A=np.array(list(product(range(n),repeat=m)),dtype=np.int8)
 masks=np.zeros((n,len(A)),dtype=np.int32)
 for e in range(m):
  for i in range(n):masks[i]|=(A[:,e]==i).astype(np.int32)<<e
 return masks

def check(D,masks,m):
 n=D.shape[0];ok=np.ones(masks.shape[1],dtype=bool)
 for i in range(n):
  own=masks[i]
  residual=np.zeros(len(own),dtype=np.int8)
  for e in range(m):
   has=(own>>e)&1
   residual=np.maximum(residual,np.where(has,D[i,own^(1<<e)],0))
  for j in range(n):ok&=residual<=D[i,masks[j]]
 return bool(ok.any())

def trial(n,m,k,trials,seed,loops=False):
 rng=np.random.default_rng(seed);ms=allocations(n,m);bad=None
 for t in range(trials):
  L=rng.integers(-1 if loops else 0,k,size=(n,m),dtype=np.int8)
  if not check(rank_tables(L,k),ms,m):bad={'labels':L.tolist(),'trial':t};break
 return {'n':n,'m':m,'number_of_classes':k,'loops':loops,'requested_trials':trials,'completed_trials':t+1,'seed':seed,'allocations_per_profile':ms.shape[1],'counterexample':bad}
if __name__=='__main__':
 out=[]
 for args in [(3,8,2,1000,20261020,False),(3,9,2,500,20261021,True),(3,8,3,1000,20261022,False),(3,8,3,1000,20261023,True),(4,7,2,500,20261024,True)]:
  out.append(trial(*args))
 (P/'rank_toy_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
