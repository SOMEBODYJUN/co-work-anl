"""Exploratory exact boundary checks, never a universal proof."""
import random, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver

rng = random.Random(1739499)
worst = (0, None)
for k in range(1000):
    p, m = 5, 3
    customers = tuple(CustomerType(frozenset(j for j in range(p) if mask >> j & 1), rng.randrange(1,8))
                      for mask in range(1,1<<p) if rng.random()<.4)
    I = Instance(tuple(map(str,range(p))), customers, m)
    solver = ExactSPESolver(I)
    terminals = list(solver.outcomes())
    for q in terminals:
        residual = Instance(I.topics, tuple(c for c in customers if not any(q[j] for j in c.topics)), m)
        R, W = residual.optimal_welfare(), I.welfare(q)
        if W and R/W > worst[0]:
            worst=(R/W, (k, q, W, R, [(sum(1<<j for j in c.topics),c.multiplicity) for c in customers]))
        if R>W:
            print('FATAL', worst, flush=True)
            raise SystemExit
print('worst', worst)
