from customer_attraction import Instance,CustomerType,ExactSPESolver
from itertools import product
import random,sys,time

def F(inst,counts):
 rem=inst.players-sum(counts); k=inst.topic_count;best=0
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
for k,m,it in [(3,4,300),(4,4,100),(4,5,50),(5,4,50)]:
 t=time.time()
 for jj in range(it):
  inst=randinst(k,m); s=ExactSPESolver(inst)
  # enumerate all prefix states total < m
  for remn in range(m):
   for st in product(range(m+1),repeat=k):
    if sum(st)!=remn:continue
    f=F(inst,st)
    for a in range(k):
     child=st[:a]+(st[a]+1,)+st[a+1:]
     gap=f-F(inst,child)
     for z in s._solve(child):
      u=s._utility(z,a)
      if gap>u:
       print('LOCAL ALL BAD',k,m,'st',st,'a',a,'gap',gap,'u',u,'z',z,inst.to_dict());sys.exit()
 print('done',k,m,'sec',time.time()-t)
