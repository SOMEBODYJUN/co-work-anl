import sys,random,json
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
rng=random.Random(6135)
worst=None
for it in range(1000):
 p=4 if it<500 else 5
 m=rng.randrange(2,6)
 types=tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),r) for mask in range(1,1<<p) if (r:=rng.randrange(0,7)))
 inst=Instance(tuple(map(str,range(p))),types,m)
 sol=ExactSPESolver(inst); O=inst.optimal_welfare()
 for q in sol.outcomes():
  H=lambda c:sum((F(1,k) for k in range(1,c+1)),F(0))
  phi=sum((t.multiplicity*min(F(2),H(sum(q[a] for a in t.topics))) for t in types),F(0))
  rat=phi/O if O else F(1)
  if worst is None or rat<worst[0]: worst=(rat,it,m,p,q,phi,O,inst.to_dict())
  if phi<O:
   print(json.dumps({'status':'counterexample','worst':[str(x) for x in worst[:-1]],'instance':worst[-1]}));sys.exit()
print(json.dumps({'status':'no_counterexample','worst':[str(x) for x in worst[:-1]],'instance':worst[-1]}))
