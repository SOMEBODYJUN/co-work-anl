from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
from itertools import combinations_with_replacement
from fractions import Fraction
import random,json,time
rng=random.Random(19024)
for z in range(3000):
 k,m=6,3
 w={a:(rng.randrange(0,12) if a.bit_count()<=2 and rng.random()<0.55 else 0) for a in range(1,1<<k)}
 ins=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(i for i in range(k) if a>>i&1),b) for a,b in w.items() if b),m)
 solver=ExactSPESolver(ins)
 opt=ins.optimal_welfare()
 opts=[t for t in combinations_with_replacement(range(k),m) if ins.welfare(ins.counts(t))==opt]
 for c in solver.outcomes():
  pay=ins.topic_payoffs(c)
  u=min(pay[i] for i in range(k) if c[i])
  D=max(sum(cu.multiplicity for cu in ins.customers if not any(c[i] for i in cu.topics) and any(i in cu.topics for i in t)) for t in opts)
  if m*u<D:
   print('FAIL',z,'m',m,'k',k,'opt',opt,'W',ins.welfare(c),'D',D,'u',str(u),'counts',c,'weights',w,flush=True)
   raise SystemExit
 if z%50==0: print(z,flush=True)
print('none')
