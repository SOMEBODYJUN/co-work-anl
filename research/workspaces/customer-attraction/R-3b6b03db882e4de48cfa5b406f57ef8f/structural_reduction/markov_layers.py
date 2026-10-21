"""Finite exact count-policy outcome enumeration, retaining shared DAG layers.

Unlike ExactSPESolver, fixes one joint count-dependent policy per layer;
independent choices are allowed only after a common deeper policy is fixed.
"""
from itertools import product
from collections import defaultdict
import json,sys,time,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import CustomerType,Instance,ExactSPESolver

def states(k,t):return tuple(q for q in product(range(t+1),repeat=k) if sum(q)==t)
def inc(q,a):return tuple(v+int(i==a) for i,v in enumerate(q))
def markov_outcomes(inst,cap=100000):
 k=inst.topic_count;n=inst.players
 levels=[states(k,t) for t in range(n+1)]
 maps={levels[n]}
 sizes=[1]
 pay={q:inst.topic_payoffs(q) for q in levels[n]}
 for depth in range(n-1,-1,-1):
  child_index={q:i for i,q in enumerate(levels[depth+1])}
  child_slots=[tuple(child_index[inc(q,a)] for a in range(k)) for q in levels[depth]]
  nextmaps=set()
  for childmap in maps:
   menus=[]
   for slots in child_slots:
    choices=[childmap[slot] for slot in slots]
    values=[pay[q][a] for a,q in enumerate(choices)]
    top=max(values)
    menus.append(tuple(sorted(set(q for q,u in zip(choices,values) if u==top))))
   size=1
   for menu in menus:size*=len(menu)
   if size>cap:return None,sizes+[f'product>{cap}']
   for parentmap in product(*menus):
    nextmaps.add(parentmap)
    if len(nextmaps)>cap:return None,sizes+[f'maps>{cap}']
  maps=nextmaps;sizes.append(len(maps))
 return {q[0] for q in maps},sizes

if __name__=='__main__':
 rng=random.Random(27991);start=time.time();skips=0
 for j in range(3000):
  k=3;n=4
  mult=[rng.randrange(4) if rng.random()<.7 else 0 for _ in range(2**k-1)]
  inst=Instance(tuple('ABC'),tuple(CustomerType(frozenset(i for i in range(k) if mask>>i&1),w) for mask,w in enumerate(mult,1) if w),n)
  allout=ExactSPESolver(inst).outcomes();mout,sizes=markov_outcomes(inst)
  if mout is None:skips+=1;continue
  if set(allout)!=mout:
   d={'scope':'failure of count-dependent outcome reduction only','instance':inst.to_dict(),'all':sorted(allout),'markov':sorted(mout),'gap':sorted(set(allout)-mout),'layer_sizes':sizes,'tested':j+1}
   Path(__file__).with_name('markov_gap.json').write_text(json.dumps(d,indent=2));print(json.dumps(d,indent=2));break
 else:print(json.dumps({'scope':'finite computation only','tested':j+1,'seconds':time.time()-start,'skips':skips,'no_gap':True}))
