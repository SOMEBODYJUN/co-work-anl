import random,json,sys
import numpy as np
from scipy.optimize import linprog
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
rng=random.Random(192918)
record=(-1e100,None)
for z in range(1600):
 m=rng.choice([2,3,4,5]); k=rng.choice([3,4,5,6])
 types=[]
 for s in range(1,1<<k):
  if rng.random()<.25:types.append(CustomerType(frozenset(i for i in range(k) if s>>i&1),rng.randrange(1,21)))
 inst=Instance(tuple(map(str,range(k))),tuple(types),m); sol=ExactSPESolver(inst)
 n=len(types); A=np.zeros((n,k+n))
 for j,t in enumerate(types):
  for i in t.topics:A[j,i]=-1
  A[j,k+j]=1
 for q in sol.outcomes():
  w=inst.welfare(q);us=inst.topic_payoffs(q);v=min(us[i]for i,num in enumerate(q)if num)
  if not v:continue
  ob=np.array([float(v)]*k+[-t.multiplicity for t in types])
  lp=linprog(ob,A_ub=A,b_ub=np.zeros(n),bounds=[(0,None)]*k+[(0,1)]*n,method='highs')
  value=-lp.fun;gap=value-w
  if gap>record[0]:record=(gap,dict(z=z,m=m,k=k,types=[(sorted(t.topics),t.multiplicity)for t in types],q=q,us=list(map(str,us)),w=w,value=value,topicweights=list(lp.x[:k])))
  if gap>1e-7:
   print('FAIL',json.dumps(record[1]),flush=True);sys.exit()
 if z%100==0:print(z,record[0],flush=True)
print('NOFAIL',json.dumps(record[1]))
