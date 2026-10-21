"""Exact finite comparison: all-history SPE and count-dependent SPE, m=3.

A negative witness concerns only the reduction, not half coverage.
"""
from itertools import product
from fractions import Fraction
import json, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import CustomerType, Instance, ExactSPESolver

def inc(q,a):return tuple(x+int(i==a) for i,x in enumerate(q))
def count_states(k,t):
 return [q for q in product(range(t+1),repeat=k) if sum(q)==t]

def markov_outcomes_3(inst, cap=100000):
 assert inst.players==3
 k=inst.topic_count
 depth2=count_states(k,2)
 menus=[]
 for q in depth2:
  us=[inst.topic_payoff(a,inc(q,a)) for a in range(k)]
  menus.append(tuple(a for a in range(k) if us[a]==max(us)))
 number=1
 for menu in menus:number*=len(menu)
 if number>cap:return None,number
 results=set()
 for last in product(*menus):
  qmap={q:inc(q,a) for q,a in zip(depth2,last)}
  children=[]
  for first in range(k):
   p=tuple(int(i==first) for i in range(k))
   cs=[qmap[inc(p,a)] for a in range(k)]
   us=[inst.topic_payoff(a,q) for a,q in enumerate(cs)]
   children.append(set(cs[a] for a in range(k) if us[a]==max(us)))
  floor=max(min(inst.topic_payoff(a,q) for q in child) for a,child in enumerate(children))
  results.update(q for a,child in enumerate(children) for q in child if inst.topic_payoff(a,q)>=floor)
 return results,number

def main():
 start=time.time(); tested=0
 k=3
 for mult in product(range(3),repeat=7):
  inst=Instance(tuple('ABC'),tuple(CustomerType(frozenset(i for i in range(k) if mask>>i&1),w) for mask,w in enumerate(mult,1) if w),3)
  allout=ExactSPESolver(inst).outcomes()
  mout,n=markov_outcomes_3(inst)
  tested+=1
  if mout is not None and set(allout)!=mout:
   result={'scope':'failure of count-dependent outcome reduction only','instance':inst.to_dict(),'all':sorted(allout),'markov':sorted(mout),'gap':sorted(set(allout)-mout),'last_policies':n,'tested':tested}
   print(json.dumps(result,indent=2));return
 print(json.dumps({'scope':'finite computation only','tested':tested,'seconds':time.time()-start,'no_gap':True}))
if __name__=='__main__':main()
