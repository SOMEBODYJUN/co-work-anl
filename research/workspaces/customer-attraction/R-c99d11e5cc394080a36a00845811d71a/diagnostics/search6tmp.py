import random,itertools,sys
sys.path.insert(0,'.')
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

def randinst(T=6,C=10):
    sets=[]
    for t in range(T):
      s={x for x in range(C) if random.random()<random.uniform(.1,.7)}
      sets.append(s)
    if all(not s for s in sets): sets[0]={0}
    sig={}
    for x in range(C):
      ss=frozenset(t for t,s in enumerate(sets) if x in s)
      if ss: sig[ss]=sig.get(ss,0)+1
    cust=tuple(CustomerType(k,v) for k,v in sig.items())
    return Instance(tuple(f't{t}' for t in range(T)),cust,6)

best=(0,None)
for it in range(10000):
  T=random.randint(2,8); C=random.randint(3,12)
  ins=randinst(T,C)
  try: sol=ExactSPESolver(ins); r=sol.inefficiency_ratio();
  except Exception as e: continue
  if r>best[0]:
    best=(r,ins)
    print('it',it,'ratio',r,float(r),'T,C',T,C,'stats',sol.stats)
    print(ins.to_dict(),'opt',ins.optimal_welfare(),'min',sol.minimum_welfare(),'worst',sol.worst_outcomes(),flush=True)
  if r>2:
    print('FOUND',r,ins.to_dict());break
print('BEST',best[0])
