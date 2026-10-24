from customer_attraction import Instance, CustomerType, ExactSPESolver
from fractions import Fraction
import sys,time

def check(inst):
 s=ExactSPESolver(inst); opt=inst.optimal_welfare(); minsl=None; arg=None
 for path in s.ordered_outcomes():
  counts=[0]*inst.topic_count; ts=[]
  for a in path:
   ts.append(s.threshold(tuple(counts))); counts[a]+=1
  W=inst.welfare(tuple(counts)); slack=Fraction(W)+sum(ts)-opt
  if minsl is None or slack<minsl: minsl,arg=slack,(path,tuple(ts),W,opt,tuple(counts))
  if slack<0:return slack,arg
 return minsl,arg
for k,m in [(3,3),(3,4),(3,5),(4,3)]:
 masks=list(range(1,1<<k)); cnt=0;t=time.time()
 for keep in range(1,1<<len(masks)):
  cust=[]
  for j,mask in enumerate(masks):
   if keep>>j&1:cust.append(CustomerType(frozenset(i for i in range(k) if mask>>i&1),1))
  inst=Instance(tuple(f'T{i}' for i in range(k)),tuple(cust),m)
  res,arg=check(inst);cnt+=1
  if res<0:
   print('FOUND',k,m,res,arg,inst.to_dict());sys.exit()
 print('done',k,m,'count',cnt,'sec',time.time()-t)
