from customer_attraction import Instance,CustomerType,ExactSPESolver
from itertools import product
from fractions import Fraction
import random,sys

def F(inst,counts):
 rem=inst.players-sum(counts); k=inst.topic_count; best=0
 for acts in product(range(k),repeat=rem):
  q=list(counts)
  for a in acts:q[a]+=1
  best=max(best,inst.welfare(q))
 return best

def randinst(k,m):
 c=[]
 for mask in range(1,1<<k):
  mult=random.choice([0,0,1,1,2])
  if mult:c.append(CustomerType(frozenset(i for i in range(k) if mask>>i&1),mult))
 return Instance(tuple(f'T{i}' for i in range(k)),tuple(c),m)
for k,m in [(3,3),(4,4)]:
 for jj in range(30):
  inst=randinst(k,m); s=ExactSPESolver(inst)
  for path in s.ordered_outcomes():
   counts=[0]*k
   for i,a in enumerate(path):
    st=tuple(counts); theta=s.threshold(st); f=F(inst,st); counts[a]+=1; fc=F(inst,tuple(counts))
    if f-fc>theta:
      print('LOCAL BAD',k,m,'path',path,'at',i,'st',st,'act',a,'theta',theta,'F',f,'Fc',fc,'gap',f-fc,inst.to_dict());sys.exit()
 print('done',k,m)
