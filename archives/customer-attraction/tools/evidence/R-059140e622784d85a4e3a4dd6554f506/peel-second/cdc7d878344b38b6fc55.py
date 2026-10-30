"""Test exact general Bellman-share candidate, not a new fixed-size theorem.
CANDIDATE: in any legal background b, every admitted first move A and leaf z obey
2*u_A(z)+max_{r-1 themes} P_{b+A}(themes) >= max_{r themes}P_b(themes),
where P_b(c)=sum_x c_x/(b_x+c_x). This would inductively imply half coverage.
"""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from random import Random
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver

def comps(n,q):
 if q==1:yield (n,);return
 for a in range(n+1):
  for tail in comps(n-a,q-1):yield (a,)+tail

def probe(seed=592731, trials=2000):
 rng=Random(seed)
 for trial in range(trials):
  q=rng.randrange(3,7); r=rng.randrange(2,5); old=rng.randrange(0,3)
  types=[]
  for mask in range(1,1<<q):
   if rng.random()<.35:
    types.append(CustomerType(frozenset(j for j in range(q) if mask>>j&1),rng.randrange(1,8)))
  ins=Instance(tuple(map(str,range(q))),tuple(types),r+old)
  b=tuple(rng.choice(tuple(comps(old,q))))
  solver=ExactSPESolver(ins)
  @lru_cache(None)
  def value(c,bb):
   s=F(0)
   for t in types:
    a=sum(c[j] for j in t.topics); z=sum(bb[j] for j in t.topics)
    if a:s+=F(t.multiplicity*a,z+a)
   return s
  def optimum(n,bb):return max(value(c,bb) for c in comps(n,q))
  opt=optimum(r,b)
  threshold=solver.threshold(b)
  for a in range(q):
   ba=tuple(b[j]+(j==a) for j in range(q))
   childopt=optimum(r-1,ba)
   for z in solver.outcomes(ba):
    u=ins.topic_payoff(a,z)
    if u<threshold:continue
    slack=2*u+childopt-opt
    if slack<0:
     return {'candidate':'BELLMAN-SHARE','seed':seed,'trial':trial,'instance':ins.to_dict(),'b':b,'r':r,'a':a,'terminal':z,'u':str(u),'opt':str(opt),'childopt':str(childopt),'slack':str(slack)}
 return {'candidate':'BELLMAN-SHARE','seed':seed,'trials':trials,'found':False}
if __name__=='__main__':
 result=probe(trials=int(sys.argv[1]) if len(sys.argv)>1 else 2000)
 print(json.dumps(result,indent=2))
