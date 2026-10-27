import random,sys,time
sys.path.insert(0,'.')
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

def randinst(T,C,p=None):
 sets=[]
 for t in range(T):
  q=random.uniform(.05,.8) if p is None else p
  sets.append({x for x in range(C) if random.random()<q})
 if all(not s for s in sets):sets[0]={0}
 sig={}
 for x in range(C):
  ss=frozenset(t for t,s in enumerate(sets) if x in s)
  if ss:sig[ss]=sig.get(ss,0)+1
 return Instance(tuple(map(str,range(T))),tuple(CustomerType(k,v) for k,v in sig.items()),6)
best=(0,None); st=time.time()
for it in range(3000):
 T=random.randint(3,10);C=random.randint(4,20)
 ins=randinst(T,C)
 try:
  sol=ExactSPESolver(ins); rr=sol.inefficiency_ratio()
 except Exception:continue
 if rr>best[0]:
  best=(rr,ins);print(it,float(rr),rr,'T',T,'C',C,'opt',ins.optimal_welfare(),'min',sol.minimum_welfare(),'stats',sol.stats,ins.to_dict(),flush=True)
 if rr>2:break
 if time.time()-st>110:break
print('DONE',best[0])
