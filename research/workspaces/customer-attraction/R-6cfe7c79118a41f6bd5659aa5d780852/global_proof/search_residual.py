from customer_attraction import Instance, CustomerType, ExactSPESolver, verify_certificate
from random import Random
from itertools import combinations
from fractions import Fraction
import json,sys,time
rng=Random(17291)
best=Fraction(0)
start=time.time()
for z in range(5000):
 m=2+(z%3); k=4+(z%2)
 weights={mask:rng.randint(1,8) for mask in range(1,1<<k) if rng.random()<.24}
 if not weights:continue
 inst=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(i for i in range(k) if mask>>i&1),v) for mask,v in weights.items()),m)
 solver=ExactSPESolver(inst)
 residuals={}
 for out in solver.outcomes():
  support=sum((1<<i) for i,q in enumerate(out) if q)
  W=inst.welfare(out)
  if support not in residuals:
   residuals[support]=max(sum(v for mask,v in weights.items() if mask&cmp and not mask&support) for r in range(min(m,k)+1) for tup in combinations(range(k),r) for cmp in [sum(1<<j for j in tup)])
  R=residuals[support]
  if W and Fraction(R,W)>best:
   best=Fraction(R,W)
   print(z,m,k,str(best),R,W,round(time.time()-start,2),flush=True)
  if R>W:
   cert=solver.certificate(out)
   verify_certificate(inst,cert).assert_valid()
   obj={'instance':inst.to_dict(),'outcome':out,'residual':R,'welfare':W,'certificate':cert.to_dict()}
   open(sys.argv[1],'w').write(json.dumps(obj,indent=2))
   print('FOUND',sys.argv[1]);quit()
print('No residual counterexample',best)
