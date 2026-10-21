"""Finite numeric attack on local fractional benchmark, not a proof search oracle."""
from fractional_explore import benchmark
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
from pathlib import Path
import random,json,time
rng=random.Random(6709884)
best=0
for n in [3,4,5,6]:
 for trial in range(100):
  k=7
  types=[]
  for mask in range(1,1<<k):
   if rng.random()<.22:
    types.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(1,10)))
  ins=Instance(tuple(map(str,range(k))),tuple(types),n)
  ss=ExactSPESolver(ins); root=(0,)*k
  ss.outcomes(); floor=ss.threshold(root)
  v,_=benchmark(ins,root)
  for a in range(k):
   b=tuple(int(j==a) for j in range(k)); vb,_=benchmark(ins,b)
   us=[ins.topic_payoff(a,t) for t in ss.outcomes(b) if ins.topic_payoff(a,t)>=floor]
   if not us:continue
   u=min(us); d=float(u)+(n-1)*vb-n*v
   if d<best:
    best=d
    print(n,trial,a,'D',d,'u',str(u),'M',v,'Mnext',vb,flush=True)
   if d<-.0001:
    out={'instance':ins.to_dict(),'n':n,'a':a,'u':str(u),'M':v,'Mnext':vb,'D':d}
    Path(__file__).with_name('fractional_local_obstruction.json').write_text(json.dumps(out,indent=2))
    raise SystemExit
 print('finished',n,flush=True)
