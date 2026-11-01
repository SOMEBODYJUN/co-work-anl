from fractions import Fraction as F
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import ExactSPESolver
from cascade_attack import Engine,seeds

triples=0
for m in range(1,61):
 for g in range(1,m+1):
  d=m-g
  for k in range(1,g+1):
   h=m-k;triples+=1
   endpoint=F(g)+F((h+2)*g*d,m*(h+1))
   assert (endpoint>=m-1)==(m*(h+d+1)>=d*d*(h+2))
   assert endpoint-(m-1)==F(m*(h+d+1)-d*d*(h+2),m*(h+1))
   if d*d<=m:assert endpoint>=m-1
paths=0;improved=0
for p,a in ((7,2),(8,3)):
 eng=Engine(p,5)
 for r in list(seeds(p,5,a))[:3]:
  inst=eng.instance(r);solver=ExactSPESolver(inst)
  cover=[frozenset(j for j,c in enumerate(inst.customers) if b in c.topics) for b in range(p)]
  for path in solver.ordered_outcomes():
   paths+=1;B=cover[path[-1]];u=inst.player_payoffs(path)[-1]
   q=inst.counts(path,terminal=True);W=inst.welfare(q)
   S=sum(c.multiplicity for j,c in enumerate(inst.customers) if j in B);V=W-S
   g=sum(B<=cover[b] for b in path);k=sum(B==cover[b] for b in path);d=5-g;h=5-k
   R=sum((F(c.multiplicity,sum(q[b] for b in c.topics)+1) for j,c in enumerate(inst.customers) if j not in B and sum(q[b] for b in c.topics)),F(0))
   assert R>=F(V,h+1)
   assert S>=g*u and S<=5*u and V>=g*(u-F(S,5))
   if 5*(h+d+1)>=d*d*(h+2):
    improved+=1;assert W+R>=4*u and inst.optimal_welfare()<=2*W
print(json.dumps({'exact_count_triples':triples,'ordered_spe_paths':paths,'paths_satisfying_refined_condition':improved,'status':'all exact checks passed'},indent=2))
