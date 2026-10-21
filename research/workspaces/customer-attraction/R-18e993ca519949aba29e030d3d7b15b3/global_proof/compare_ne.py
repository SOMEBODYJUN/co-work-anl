from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
from itertools import product
from fractions import Fraction as F
import random,json,sys

def comps(n,p):
 if p==1: yield (n,);return
 for x in range(n+1):
  for z in comps(n-x,p-1): yield (x,)+z

def run(w,p,n):
 ins=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),r) for mask,r in enumerate(w,1) if r),n)
 sol=ExactSPESolver(ins);sw=sol.minimum_welfare()
 ne=[]
 for c in comps(n,p):
  u=ins.topic_payoffs(c)
  ok=True
  for a in range(p):
   if not c[a]:continue
   for b in range(p):
    if a==b:continue
    q=list(c);q[a]-=1;q[b]+=1
    if ins.topic_payoff(b,q)>u[a]:ok=False;break
   if not ok:break
  if ok:ne.append(c)
 nw=min(map(ins.welfare,ne))
 if sw<nw:
  print(json.dumps({'n':n,'p':p,'weights':w,'spe':sw,'ne':nw,'s_out':sorted(sol.worst_outcomes()),'n_out':ne}),flush=True);return False
 return True
if __name__=='__main__':
 p=int(sys.argv[1]) if len(sys.argv)>1 else 3;n=int(sys.argv[2]) if len(sys.argv)>2 else 3
 rng=random.Random(27616)
 for i in range(100000):
  w=[rng.randrange(6) if rng.random()<0.5 else 0 for _ in range(2**p-1)]
  if not run(w,p,n):break
  if i%100==0:print('checked',i,flush=True)
