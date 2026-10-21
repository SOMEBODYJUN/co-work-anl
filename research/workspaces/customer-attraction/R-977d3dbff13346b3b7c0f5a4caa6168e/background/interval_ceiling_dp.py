"""Safe min/max interval pruning of full-depth common-catalog SPE outcomes.
Not exact SPE BI: qualifying an action retains its entire child outcome set.
"""
from functools import lru_cache
from fractions import Fraction as F

class IntervalCeilingFloor:
 def __init__(self,instance):
  self.ins=instance;self.k=instance.topic_count;self.m=instance.players
  self.level={};self.allowed={}
  self.bounds=lru_cache(None)(self._bounds)
  self.pay=lru_cache(None)(instance.topic_payoffs)
  self.cost=lru_cache(None)(self._cost)
 def add(self,b,a):return b[:a]+(b[a]+1,)+b[a+1:]
 def _bounds(self,b):
  if sum(b)==self.m:
   u=self.pay(b);return u,u
  children=tuple(self.bounds(self.add(b,a)) for a in range(self.k))
  floor=max(children[a][0][a] for a in range(self.k))
  allowed=tuple(a for a in range(self.k) if children[a][1][a]>=floor)
  assert allowed
  self.level[b]=floor;self.allowed[b]=allowed
  lower=tuple(min(children[a][0][j] for a in allowed) for j in range(self.k))
  upper=tuple(max(children[a][1][j] for a in allowed) for j in range(self.k))
  return lower,upper
 def floor(self,b):self.bounds(b);return self.level[b]
 def _cost(self,b):
  if sum(b)==self.m:return F()
  self.bounds(b)
  return self.level[b]+min(self.cost(self.add(b,a)) for a in self.allowed[b])
 def root(self):return self.cost((0,)*self.k)

class MaterializedInterval:
 def __init__(self,instance):
  self.ins=instance;self.k=instance.topic_count;self.m=instance.players
  self.level={};self.allowed={}
  self.terminals=lru_cache(None)(self._terminals)
 def add(self,b,a):return b[:a]+(b[a]+1,)+b[a+1:]
 def _terminals(self,b):
  if sum(b)==self.m:return frozenset({b})
  children=tuple(self.terminals(self.add(b,a)) for a in range(self.k))
  floor=max(min(self.ins.topic_payoffs(q)[a] for q in children[a]) for a in range(self.k))
  allowed=tuple(a for a in range(self.k) if max(self.ins.topic_payoffs(q)[a] for q in children[a])>=floor)
  self.level[b]=floor;self.allowed[b]=allowed
  return frozenset(q for a in allowed for q in children[a])

def regression():
 import itertools,sys
 from pathlib import Path
 oldpath=Path(__file__).resolve().parents[2]/'R-d321c149379b425493c5e8a5e03c6f39'/'independent'
 sys.path.insert(0,str(oldpath))
 from myopic_ceiling_dp import MyopicCeilingFloor
 from copy_protection_dp import CustomerType,Instance,compositions,ExactSPESolver
 stats={'instances':0,'states':0,'nonterminal_states':0,'strict_interval_vs_myopic':0,
        'strict_interval_vs_exact':0,'strict_cost_improvements':0}
 first_gap=None
 for k in range(1,4):
  sigs=[frozenset(a for a in range(k) if mask>>a&1) for mask in range(1,1<<k)]
  for bits in itertools.product([0,1],repeat=len(sigs)):
   cs=tuple(CustomerType(s) for s,v in zip(sigs,bits) if v)
   for m in range(1,5):
    ins=Instance(tuple(map(str,range(k))),cs,m)
    old=MyopicCeilingFloor(ins);compressed=IntervalCeilingFloor(ins)
    mat=MaterializedInterval(ins);exact=ExactSPESolver(ins)
    for n in range(m+1):
     for b in compositions(n,k):
      H=mat.terminals(b);lo,hi=compressed.bounds(b)
      assert lo==tuple(min(ins.topic_payoffs(q)[a] for q in H) for a in range(k))
      assert hi==tuple(max(ins.topic_payoffs(q)[a] for q in H) for a in range(k))
      assert exact.outcomes(b)<=H<=old.terminals(b)
      stats['states']+=1
      if H<old.terminals(b):stats['strict_interval_vs_myopic']+=1
      if exact.outcomes(b)<H:
       stats['strict_interval_vs_exact']+=1
       if first_gap is None:first_gap={'instance':ins.to_dict(),'prefix':b,'exact_outcomes':sorted(exact.outcomes(b)),'interval_outcomes':sorted(H)}
      if n==m:continue
      assert mat.level[b]==compressed.level[b]
      assert mat.allowed[b]==compressed.allowed[b]
      assert compressed.level[b]>=old.level[b]
      assert compressed.cost(b)>=old.cost(b)
      if compressed.cost(b)>old.cost(b):stats['strict_cost_improvements']+=1
      stats['nonterminal_states']+=1
    stats['instances']+=1
 stats['first_strict_exact_gap']=first_gap
 return stats

if __name__=='__main__':
 import json
 from pathlib import Path
 ans=regression();print(json.dumps(ans,indent=2))
 Path(__file__).with_name('interval_regression.json').write_text(json.dumps(ans,indent=2)+'\n')
