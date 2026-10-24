from fractions import Fraction
from itertools import product
from scipy.optimize import linprog
from customer_attraction import CustomerType,Instance,ExactSPESolver
import random,math,sys

def calc_v(inst,b,r):
 k=inst.topic_count
 opps=[]
 for q in product(range(k), repeat=r):
  cnt=[0]*k
  for a in q:cnt[a]+=1
  opps.append(tuple(cnt))
 A=[]
 for cnt in opps:
  row=[]
  for a in range(k):
   val=0.0
   for c in inst.customers:
    if a in c.topics:
     bg=sum(b[t] for t in c.topics)
     load=sum(cnt[t] for t in c.topics)
     val += float(c.multiplicity)/ (bg+1+load)
   row.append(val)
  A.append(row)
 # max t; -A p + t <=0; sum p=1 p>=0,t free but >=0
 import numpy as np
 A_ub=[];B_ub=[]
 for row in A:
  A_ub.append([-x for x in row]+[1]);B_ub.append(0)
 c=[0]*k+[-1]
 res=linprog(c,A_ub=np.array(A_ub),b_ub=np.array(B_ub),A_eq=[[1]*k+[0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
 return -res.fun if res.success else None

def first_min(inst,bprefix=()):
 m=inst.players;k=inst.topic_count
 sol=ExactSPESolver(inst)
 minp=1e99;arg=None
 children=[]
 for a in range(k):
  cc=[0]*k;cc[a]=1
  children.append(sol.outcomes(cc))
 floors=[min(inst.topic_payoff(a,q) for q in children[a]) for a in range(k)]
 floor=max(floors)
 for a in range(k):
  for q in children[a]:
   u=inst.topic_payoff(a,q)
   if u>=floor and float(u)<minp:minp=float(u);arg=(a,u,q)
 # v_(m+1)(b) where background prefix bprefix counts
 b=[0]*k
 for a in bprefix:b[a]+=1
 v=calc_v(inst,b,m)
 return v,minp,arg,sol

rng=random.Random(20261024)
for trial in range(2000):
 k=rng.choice([3,4]);m=rng.choice([3,4])
 weights=[]
 for mask in range(1,1<<k):
  w=rng.choice([0,0,0,1,2,3,5,8,13,21])
  weights.append(w)
 cust=tuple(CustomerType(frozenset(t for t in range(k) if mask&(1<<t)),w) for mask,w in enumerate(weights,1) if w)
 if not cust:continue
 inst=Instance(tuple(str(i) for i in range(k)),cust,m)
 try:v,minp,arg,sol=first_min(inst)
 except Exception as e:continue
 if v is not None and minp+1e-8 < v:
  print('FOUND',trial,k,m,'v',v,'minp',minp,'arg',arg,'weights',weights,flush=True);break
 if trial%100==0: print('trial',trial,'ratio',minp/v if v else None,flush=True)
else: print('none')
