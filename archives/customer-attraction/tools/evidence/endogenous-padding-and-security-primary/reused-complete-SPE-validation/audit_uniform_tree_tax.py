#!/usr/bin/env python3
"""Exact definition-level audit of the uniform full-tree tax budget.

Checks all seven fixed first-action subgames of an existing complete unit SPE.
No solver or shared verifier is imported. Path sums follow sigma from each fixed
history; no sum is asserted across an arbitrary sequence of deviating branches.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
ins=json.loads((HERE/"endogenous_53_instance.json").read_text())
cert=json.loads((HERE/"endogenous_53_strategy.json").read_text())
base=tuple(frozenset(row["topics"]) for row in ins["customers"] for _ in range(row["multiplicity"]))
actions={tuple(row["history"]):row["action"] for row in cert["actions"]}
p=7;m=4
assert set(actions)=={h for d in range(m) for h in product(range(p),repeat=d)}

@lru_cache(None)
def finish(h):
    return h if len(h)==m else finish(h+(actions[h],))

rows=[]
for core in (0,7):
 customers=base+(frozenset(range(p)),)*core
 for lam in (F(1,2),F(3,4),F(84796,85443)):
  node_regret={};checks=0;positive=0;max_regret=F();max_path_slack=None
  for root in range(p):
   def old(z,i):
    return sum((F(1,sum(t in s for t in z)) for s in customers if z[i] in s),F())
   def new(z,i):
    return sum((lam/(int(root in s)+lam*sum(t in s for t in z[1:])) for s in customers if z[i] in s),F())
   def refund(z):
    return sum((1/(F(1)+lam*sum(t in s for t in z[1:]))-F(1,1+sum(t in s for t in z[1:])) for s in customers if root in s),F())
   for depth in range(1,m):
    for tail_prefix in product(range(p),repeat=depth-1):
     h=(root,)+tail_prefix;z=finish(h);i=len(h)
     tax=old(z,i)-new(z,i)
     assert tax>=0
     regrets=[]
     for a in range(p):
      dz=finish(h+(a,))
      assert old(z,i)>=old(dz,i)
      dtax=old(dz,i)-new(dz,i)
      assert new(z,i)+tax>=new(dz,i)+dtax
      assert new(dz,i)-new(z,i)<=tax
      regrets.append(max(F(),new(dz,i)-new(z,i)));checks+=1
     r=max(regrets);node_regret[h]=r
     positive+=int(r>0);max_regret=max(max_regret,r)
   for depth in range(1,m):
    for tail_prefix in product(range(p),repeat=depth-1):
     h=(root,)+tail_prefix;z=finish(h)
     path_nodes=[z[:i] for i in range(len(h),m)]
     path_regret=sum((node_regret[v] for v in path_nodes),F())
     future_tax=sum((old(z,i)-new(z,i) for i in range(len(h),m)),F())
     full_tax=sum((old(z,i)-new(z,i) for i in range(1,m)),F())
     assert path_regret<=future_tax<=full_tax==refund(z)
     core_tax=F(core)*(1-lam)/(4*(1+3*lam))
     assert path_regret<=future_tax-(m-len(h))*core_tax
     # A single pool also controls every full-slot insertion query.
     H=F();HJ=F()
     for s in customers:
      c=sum(t in s for t in z[1:])
      H+=1/(1+lam*c)-F(1,1+c)
      HJ+=1/(1+int(root in s)+lam*c)-F(1,1+int(root in s)+c)
     assert 0<=HJ<=H and refund(z)<=H
     slack=refund(z)-path_regret
     max_path_slack=slack if max_path_slack is None else max(max_path_slack,slack)
  rows.append({"core":core,"lambda":str(lam),"fixed_first_action_subgames":p,
               "tail_decision_histories":len(node_regret),"deviations_including_self":checks,
               "strict_regret_nodes":positive,"maximum_local_regret":str(max_regret),
               "maximum_refund_minus_prescribed_path_regret":str(max_path_slack)})

out={"scope":"uniform tail mass; corrected complete IC and sigma-continuation tax sums only; no arbitrary-deviation-path telescoping", "rows":rows}
(HERE/"uniform_tree_tax_exact.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
