"""Attack only the general candidate OPT_m(N\\actual_union) <= actual W.
No finite success is treated as a proof. All SPE outcomes via canonical exact solver.
"""
import json,random,itertools,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
seed=20261024
rng=random.Random(seed)
start=time.time(); examined=0; outcome_count=0; maxratio=(0,None)
for m,p,trials in [(4,5,400),(5,6,120),(6,6,80)]:
 for trial in range(trials):
  weights={mask:rng.randrange(9) for mask in range(1,1<<p) if rng.random()<.35}
  customers=tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),w) for mask,w in weights.items() if w)
  inst=Instance(tuple(map(str,range(p))),customers,m)
  sol=ExactSPESolver(inst)
  for counts in sol.outcomes():
   outcome_count+=1
   missed=[c for c in customers if not any(counts[a] for a in c.topics)]
   W=inst.welfare(counts)
   optU=max((sum(c.multiplicity for c in missed if c.topics.intersection(s)) for k in range(min(m,p)+1) for s in itertools.combinations(range(p),k)),default=0)
   ratio=optU/W if W else 0
   if ratio>maxratio[0]:maxratio=(ratio,{'m':m,'p':p,'trial':trial,'W':W,'optU':optU,'counts':counts,'weights':weights})
   if optU>W:
    cert=sol.certificate(counts)
    print(json.dumps({'status':'COUNTEREXAMPLE_CANDIDATE','instance':inst.to_dict(),'counts':counts,'W':W,'optU':optU,'certificate':cert.to_dict(),'seed':seed,'elapsed':time.time()-start},indent=2));sys.exit()
  examined+=1
 print(json.dumps({'m':m,'p':p,'examined':examined,'outcomes':outcome_count,'maxratio':maxratio,'elapsed':time.time()-start}),flush=True)
print(json.dumps({'status':'FINITE_ATTACK_ONLY','seed':seed,'examined':examined,'outcomes':outcome_count,'maxratio':maxratio,'elapsed':time.time()-start}))
