import sys,random,json,itertools
from fractions import Fraction
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
rng=random.Random(9216)
record=(Fraction(0),None)
for z in range(1500):
 m=rng.choice([2,3,4,5]); k=rng.choice([3,4,5,6])
 types=[]
 for s in range(1,1<<k):
  if rng.random()<.27:
   types.append(CustomerType(frozenset(i for i in range(k) if s>>i&1),rng.randrange(1,16)))
 inst=Instance(tuple(map(str,range(k))),tuple(types),m)
 sol=ExactSPESolver(inst); opt=inst.optimal_welfare()
 for c in sol.outcomes():
  w=inst.welfare(c); ps=inst.topic_payoffs(c); low=min(ps[i] for i,v in enumerate(c) if v)
  if low and opt>w:
   ratio=Fraction(opt-w,m)/low
   if ratio>record[0]: record=(ratio,dict(z=z,m=m,k=k,types=[(sorted(t.topics),t.multiplicity)for t in types],counts=c,payoffs=list(map(str,ps)),opt=opt,w=w))
   if ratio>1:
    print(json.dumps({'failure':str(ratio),'instance':record[1]}));sys.exit()
 if z%100==0: print(z,str(record[0]),flush=True)
print('NOFAIL',str(record[0]),json.dumps(record[1]))
