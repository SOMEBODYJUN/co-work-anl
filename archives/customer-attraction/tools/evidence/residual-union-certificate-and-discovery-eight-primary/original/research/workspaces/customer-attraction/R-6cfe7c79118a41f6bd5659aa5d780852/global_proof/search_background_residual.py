from customer_attraction import Instance, CustomerType, ExactSPESolver, verify_certificate
from random import Random
from itertools import combinations
from fractions import Fraction
import json,time,sys
rng=Random(91221);best=Fraction(0);start=time.time()
for z in range(3000):
 m=3+z%3;k=4+z%2
 weights={mask:rng.randint(1,20) for mask in range(1,1<<k) if rng.random()<.12}
 if not weights:continue
 inst=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(i for i in range(k) if mask>>i&1),v) for mask,v in weights.items()),m)
 solver=ExactSPESolver(inst);solver.outcomes()
 for pre,outs in solver._outcomes.items():
  r=m-sum(pre)
  if r<2 or r==m:continue
  for out in outs:
   support=sum((1<<i) for i,q in enumerate(out) if q)
   V=sum((out[i]-pre[i])*inst.topic_payoff(i,out) for i in range(k))
   R=max(sum(v for mask,v in weights.items() if mask&cmp and not mask&support) for rr in range(min(r,k)+1) for tup in combinations(range(k),rr) for cmp in [sum(1<<j for j in tup)])
   if V and Fraction(R,V)>best:
    best=Fraction(R,V);print(z,m,k,pre,str(best),R,str(V),round(time.time()-start,2),flush=True)
   if R>V:
    obj={'instance':inst.to_dict(),'prefix':pre,'outcome':out,'residual':R,'remaining_profit':str(V)}
    open(sys.argv[1],'w').write(json.dumps(obj,indent=2));print('FOUND');quit()
print('NONE',best)
