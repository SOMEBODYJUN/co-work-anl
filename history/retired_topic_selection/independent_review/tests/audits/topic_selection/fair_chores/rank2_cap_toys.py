from rank_toys import rank_tables,allocations,check
from pathlib import Path
import numpy as np,json
P=Path(__file__).resolve().parent
out=[]
for n,m,k,trials,seed,loops in [(3,9,3,1000,20261027,False),(3,9,3,1000,20261028,True),(4,8,3,250,20261029,True)]:
 rng=np.random.default_rng(seed);ms=allocations(n,m);bad=None
 for t in range(trials):
  L=rng.integers(-1 if loops else 0,k,size=(n,m),dtype=np.int8)
  D=np.minimum(rank_tables(L,k),2)
  if not check(D,ms,m):bad={'labels':L.tolist(),'trial':t};break
 out.append({'n':n,'m':m,'parallel_classes':k,'rank_cap':2,'loops':loops,'requested_trials':trials,'completed_trials':t+1,'seed':seed,'allocations_per_profile':ms.shape[1],'counterexample':bad})
(P/'rank2_cap_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
