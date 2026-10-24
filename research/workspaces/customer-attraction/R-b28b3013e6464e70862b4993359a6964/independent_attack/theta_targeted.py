from customer_attraction import Instance,ExactSPESolver
from fractions import Fraction
from itertools import product
import random,time,json

def Ls(inst,s,hist):
 vals=[]
 for i in range(inst.players):
  cnt=inst.counts(hist[:i]); row=[]
  for a in range(inst.topic_count):
   child=tuple(cnt[j]+(j==a) for j in range(inst.topic_count))
   row.append(min(inst.topic_payoff(a,t) for t in s._solve(child)))
  vals.append(row)
 return vals

def tops(inst):
 O=inst.optimal_welfare(); return [t for t in product(range(inst.topic_count),repeat=inst.players) if inst.welfare(tuple(int(j in set(t)) for j in range(inst.topic_count)))==O]
def run(inst):
 s=ExactSPESolver(inst); O=inst.optimal_welfare(); T=tops(inst)
 best=None
 for z in s.outcomes():
  W=inst.welfare(z)
  if O<=2*W: # only look candidate deficit O-W positive
   pass
  for h in s.ordered_outcomes(z):
   ls=Ls(inst,s,h)
   # optimize min sum over optimum tuples
   sm,tt=min((sum(ls[i][t[i]] for i in range(inst.players)),t) for t in T)
   if sm < O-W:
    return {'O':O,'W':W,'sm':sm,'gap':O-W,'h':h,'z':z,'T':tt,'ls':ls,'inst':inst.to_dict()}
 return None
random.seed(20261024);start=time.time()
for it in range(10000):
 p=3;m=random.randint(6,12); mult=[0]+[random.randint(0,15) for _ in range(7)]
 if sum(mult)==0: continue
 # no empty signature; build Instance directly
 from customer_attraction import CustomerType
 cs=tuple(CustomerType(frozenset(j for j in range(p) if mask>>j&1),mult[mask]) for mask in range(1,8) if mult[mask])
 inst=Instance(tuple(f'T{j}' for j in range(p)),cs,m)
 try:r=run(inst)
 except Exception as e: continue
 if r:
  print(json.dumps({k:str(v) for k,v in r.items() if k!='ls'},indent=2));break
 if it%500==0: print('it',it,'sec',time.time()-start,flush=True)
else: print('none')
