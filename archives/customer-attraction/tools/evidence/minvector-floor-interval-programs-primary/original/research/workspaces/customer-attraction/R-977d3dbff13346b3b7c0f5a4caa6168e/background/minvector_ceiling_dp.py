"""Exact coordinate-minimum compression of the myopic-ceiling H relaxation.

This is not exact SPE BI: it computes the same L,E,G as the H-superset DP.
Terminal utility on an absent topic is set to zero, consistent with the model.
Every queried child for action a already contains a, so that convention is inert.
"""
from functools import lru_cache
from fractions import Fraction as F

class MinVectorCeilingFloor:
 def __init__(self,instance):
  self.ins=instance;self.k=instance.topic_count;self.m=instance.players
  self.level={};self.allowed={};self.minimum=lru_cache(None)(self._minimum)
  self.pay=lru_cache(None)(instance.topic_payoffs)
  self.cost=lru_cache(None)(self._cost)
 def add(self,b,a):return b[:a]+(b[a]+1,)+b[a+1:]
 def myopic(self,b,a):
  return sum((F(c.multiplicity,1+sum(b[t] for t in c.topics))
              for c in self.ins.customers if a in c.topics),F())
 def _minimum(self,b):
  if sum(b)==self.m:return self.pay(b)
  children=tuple(self.minimum(self.add(b,a)) for a in range(self.k))
  floor=max(children[a][a] for a in range(self.k))
  allowed=tuple(a for a in range(self.k) if self.myopic(b,a)>=floor)
  assert allowed
  self.level[b]=floor;self.allowed[b]=allowed
  return tuple(min(children[a][j] for a in allowed) for j in range(self.k))
 def floor(self,b):self.minimum(b);return self.level[b]
 def _cost(self,b):
  if sum(b)==self.m:return F()
  self.minimum(b)
  return self.level[b]+min(self.cost(self.add(b,a)) for a in self.allowed[b])
 def root(self):return self.cost((0,)*self.k)

def regression():
 import importlib.util,itertools,json,sys
 from pathlib import Path
 oldpath=Path(__file__).resolve().parents[2]/'R-d321c149379b425493c5e8a5e03c6f39'/'independent'
 sys.path.insert(0,str(oldpath))
 from myopic_ceiling_dp import MyopicCeilingFloor
 from copy_protection_dp import CustomerType,Instance,compositions
 stats={'instances':0,'all_states':0,'nonterminal_states':0,'minimum_coordinates':0,
        'matching_floors':0,'matching_allowed_sets':0,'matching_costs':0}
 for k in range(1,4):
  sigs=[frozenset(a for a in range(k) if mask>>a&1) for mask in range(1,1<<k)]
  for bits in itertools.product([0,1],repeat=len(sigs)):
   cs=tuple(CustomerType(s) for s,v in zip(sigs,bits) if v)
   for m in range(1,5):
    ins=Instance(tuple(map(str,range(k))),cs,m)
    old=MyopicCeilingFloor(ins);new=MinVectorCeilingFloor(ins)
    for n in range(m+1):
     for b in compositions(n,k):
      H=old.terminals(b);V=new.minimum(b)
      expected=tuple(min(ins.topic_payoffs(q)[a] for q in H) for a in range(k))
      assert V==expected,(ins,b,V,expected)
      stats['all_states']+=1;stats['minimum_coordinates']+=k
      if n==m:continue
      assert old.level[b]==new.level[b]
      assert old.allowed[b]==new.allowed[b]
      assert old.cost(b)==new.cost(b)
      stats['nonterminal_states']+=1
      for s in ['matching_floors','matching_allowed_sets','matching_costs']:stats[s]+=1
    assert old.root()==new.root();stats['instances']+=1
 return stats

if __name__=='__main__':
 import json
 from pathlib import Path
 ans=regression();print(json.dumps(ans,indent=2))
 Path(__file__).with_name('minvector_regression.json').write_text(json.dumps(ans,indent=2)+'\n')
