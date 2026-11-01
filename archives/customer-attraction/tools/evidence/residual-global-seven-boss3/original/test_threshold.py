"""Explore adaptive first-payoff floors; finite checks only."""
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver
rng = random.Random(582821)
worst=(10,None)
for k in range(5000):
    p, m = 5, 3
    customers=tuple(CustomerType(frozenset(j for j in range(p) if mask>>j&1),rng.randrange(1,11))
                    for mask in range(1,1<<p) if rng.random()<.15)
    I=Instance(tuple(map(str,range(p))),customers,m)
    sol=ExactSPESolver(I); root=(0,)*p
    v=sol.threshold(root); O=I.optimal_welfare()
    if O and float(v)*(2*m-1)/O<worst[0]:
        worst=(float(v)*(2*m-1)/O,(k,v,O,[(sum(1<<j for j in c.topics),c.multiplicity) for c in customers]))
    if (2*m-1)*v<O:
        print('FIRST_FLOOR_FALSE',worst,flush=True);break
else:print('NO FAILURE',worst)
