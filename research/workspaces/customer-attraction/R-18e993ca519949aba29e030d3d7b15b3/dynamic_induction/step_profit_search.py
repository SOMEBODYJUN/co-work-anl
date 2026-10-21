from fractions import Fraction
from itertools import product
from functools import lru_cache
from random import Random
from customer_attraction import Instance, CustomerType, ExactSPESolver
import json

def compositions(n,k):
 if k==1:
  yield (n,);return
 for a in range(n+1):
  for rest in compositions(n-a,k-1):yield (a,)+rest

def scan(I):
 S=ExactSPESolver(I);S.outcomes()
 @lru_cache(None)
 def F(b):
  r=I.players-sum(b)
  out=Fraction(0)
  for d in compositions(r,I.topic_count):
   cur=Fraction(0)
   for C in I.customers:
    B=sum(b[a] for a in C.topics);D=sum(d[a] for a in C.topics)
    if D:cur+=C.multiplicity*Fraction(D,B+D)
   out=max(out,cur)
  return out
 best=None
 for b,ends in S._outcomes.items():
  r=I.players-sum(b)
  if r<2:continue
  floor=S.threshold(b)
  for a in range(I.topic_count):
   child=b[:a]+(b[a]+1,)+b[a+1:]
   gap=F(b)-F(child)
   u=min((S._utility(z,a) for z in S.outcomes(child) if S._utility(z,a)>=floor),default=None)
   if u is None or u==0:continue
   ratio=gap/u
   if best is None or ratio>best[0]:best=(ratio,b,a,u,gap)
 return best,S

if __name__=='__main__':
 rng=Random(20261021);best=(Fraction(0),None)
 for z in range(1000):
  k=rng.choice([3,4,5]);n=rng.choice([3,4,5])
  C=[]
  for mask in range(1,1<<k):
   w=rng.randrange(0,8)
   if w:C.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),w))
  I=Instance(tuple(map(str,range(k))),tuple(C),n)
  B,S=scan(I)
  if B and B[0]>best[0]:
   best=(B[0],I)
   print(z,'best',tuple(map(str,B)),flush=True)
   if B[0]>2:
    print(json.dumps(I.to_dict()),flush=True);break
 print('DONE',best[0])
