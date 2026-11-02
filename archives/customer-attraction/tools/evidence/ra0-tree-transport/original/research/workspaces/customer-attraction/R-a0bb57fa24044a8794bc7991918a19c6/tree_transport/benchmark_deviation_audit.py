"""Exact finite audit for a benchmark-action-only row subsystem.
The policy is not SPE; complete deviations to the union theme are profitable.
"""
from fractions import Fraction as F
from itertools import product
from math import lcm
from pathlib import Path
import json

class Family:
 def __init__(self,m):
  self.m=m;self.L=lcm(*range(1,m+1))
  self.blocks=[frozenset(range(j*self.L,(j+1)*self.L)) for j in range(m)]
  self.rewards=[frozenset(sorted(self.blocks[i])[:self.L//(m-i)]) for i in range(m)]
  self.universe=frozenset(range(m*self.L))
  self.topics=list(dict.fromkeys(self.blocks+self.rewards+[self.universe]))
  self.J=tuple(self.topics.index(x) for x in self.blocks)
  self.A=tuple(self.topics.index(x) for x in self.rewards)
  self.R=self.topics.index(self.universe);self.p=len(self.topics)
 def policy(self,h):
  return self.A[len(h)] if h==self.A[:len(h)] else self.R
 def terminal(self,h):
  while len(h)<self.m:h=h+(self.policy(h),)
  return h
 def utility(self,z,i):
  c={x:sum(x in self.topics[a] for a in z) for x in self.universe}
  return sum((F(1,c[x]) for x in self.topics[z[i]]),F())
 def full_audit(self):
  nodes=kept=omitted_negative=0;minimum=F()
  for d in range(self.m):
   for h in product(range(self.p),repeat=d):
    nodes+=1;actual=self.utility(self.terminal(h),d)
    for a in range(self.p):
     gap=actual-self.utility(self.terminal(h+(a,)),d)
     if a != self.R or self.m==1:assert gap>=0,(h,a,gap);kept+=1;minimum=min(minimum,gap)
     elif gap<0:omitted_negative+=1
  return dict(m=self.m,topics=self.p,L=self.L,ordered_nodes=nodes,kept_comparisons=kept,minimum_kept_slack=str(minimum),omitted_profitable_comparisons=omitted_negative,scope='all_ordered_histories_all_catalog_queries_except_union_theme')
 def summary(self):
  W=sum(map(len,self.rewards));opt=len(self.universe)
  assert W==self.L*sum((F(1,r) for r in range(1,self.m+1)),F())
  return dict(m=self.m,L=self.L,reward_sizes=list(map(len,self.rewards)),unit_customers=opt,W=W,OPT=opt,OPT_over_W=str(F(opt,W)),OPT_minus_2W=opt-2*W,root_union_deviation_profit=str(F(opt,self.m)-F(self.L,self.m)))

def arbitrary_background_checks():
 checks=0
 # An offpath row has actual union payoff sum_x 1/(b_x+r),
 # a benchmark query's payoff is the same sum restricted to its block.
 for blocks in range(1,7):
  for r in range(1,7):
   for b in product(range(3),repeat=blocks):
    vals=[F(1,bj+r) for bj in b]
    total=sum(vals,F())
    for v in vals:assert total>=v;checks+=1
 return checks

def analytic_summary(m):
 L=lcm(*range(1,m+1));sizes=[L//r for r in range(m,0,-1)];W=sum(sizes);opt=m*L
 return dict(m=m,L=L,reward_sizes=sizes,unit_customers=opt,W=W,OPT=opt,OPT_over_W=str(F(opt,W)),OPT_minus_2W=opt-2*W,root_union_deviation_profit=str(F((m-1)*L,m)))

if __name__=='__main__':
 result=dict(status='AUXILIARY_TEMPLATE_OBSTRUCTION_NOT_SPE',full_tree_audits=[Family(m).full_audit() for m in range(1,5)],arbitrary_background_scalar_checks=arbitrary_background_checks(),family_summaries=[analytic_summary(m) for m in (4,5,8,12,20)])
 out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
