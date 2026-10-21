from customer_attraction import Instance, CustomerType, ExactSPESolver
from itertools import combinations
import random,json,time
rng=random.Random(88131)
for trial in range(30000):
 p=5; m=2
 cs=tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1), w) for mask in range(1,1<<p) if (w:=rng.randrange(0,8) if rng.random()<.42 else 0))
 I=Instance(tuple(map(str,range(p))),cs,m); solver=ExactSPESolver(I); worst=solver.minimum_welfare(); opt=I.optimal_welfare()
 if opt<=worst: continue
 os=[frozenset(T) for T in combinations(range(p),2) if I.welfare(tuple(int(a in T) for a in range(p)))==opt]
 for q in solver.worst_outcomes():
  supp={a for a in range(p) if q[a]}
  for O in os:
   keep=supp|O
   newcs=tuple(c for c in cs if c.topics&keep)
   if len(cs)==len(newcs): continue
   J=Instance(I.topics,newcs,m); news=ExactSPESolver(J); nw=news.minimum_welfare()
   if nw>worst:
    result={'trial':trial,'instance':I.to_dict(),'q':q,'opt_support':sorted(O),'original_min':worst,'opt':opt,'deleted':sum(c.multiplicity for c in cs if not c.topics&keep),'new_min':nw,'new_worst':sorted(news.worst_outcomes())}
    print(json.dumps(result,ensure_ascii=False));raise SystemExit
 if trial%1000==0: print('progress',trial,flush=True)
print('none')
