from customer_attraction import Instance, CustomerType, ExactSPESolver
from fractions import Fraction
import random,sys

def check(inst):
 s=ExactSPESolver(inst); opt=inst.optimal_welfare(); bad=[]; minsl=None; arg=None
 for path in s.ordered_outcomes():
  counts=[0]*inst.topic_count; ts=[]
  for i,a in enumerate(path):
   ts.append(s.threshold(tuple(counts))); counts[a]+=1
  W=inst.welfare(tuple(counts)); slack=Fraction(W)+sum(ts)-opt
  if minsl is None or slack<minsl: minsl,arg=slack,(path,tuple(ts),W,opt,tuple(counts))
  if slack<0: return False,bad,minsl,arg
 return True,bad,minsl,arg

def randinst(k,m):
 c=[]
 for mask in range(1,1<<k):
  mult=random.choice([0,0,0,1,1,2])
  if mult:c.append(CustomerType(frozenset(i for i in range(k) if mask>>i&1),mult))
 return Instance(tuple(f'T{i}' for i in range(k)),tuple(c),m)
for k,m,it in [(3,3,1000),(4,4,1000),(4,5,1000),(5,4,1000),(5,5,1000)]:
 for j in range(it):
  inst=randinst(k,m)
  if not inst.customers: continue
  ok,b,minsl,arg=check(inst)
  if minsl<0:
   print('FOUND',k,m,'iter',j,'min',minsl,'arg',arg,inst.to_dict());sys.exit()
 print('done',k,m)
