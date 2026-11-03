"""Independent all-history audit of the proposed larger-class counterexample.
This game is not CAG; its payoffs fail diminishing returns.
"""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from pathlib import Path
import json
K=22; M=3

def adjacent(a,b):return (a-b)%K in (1,K-1)
@lru_cache(None)
def phi3(z):
 return F(0) if any(adjacent(a,b) for a in z for b in z) else F(11)
@lru_cache(None)
def phi2(z):
 a,b=z
 if a==b:return F(10)
 if adjacent(a,b):return F(-1)
 return sum((phi3(tuple(sorted((a,b,t)))) for t in range(K)),F())/K

def utility(z,i,shift=11):return phi3(tuple(sorted(z)))-phi2(tuple(sorted(z[:i]+z[i+1:])))+shift

def action(h):
 if not h:return 0
 if len(h)==1:return (h[0]+1)%K
 return h[1] if adjacent(*h) else h[0]

def finish(h):
 while len(h)<M:h=h+(action(h),)
 return h
checks=0
for d in range(M):
 for h in product(range(K),repeat=d):
  current=utility(finish(h),d)
  for a in range(K):
   assert current>=utility(finish(h+(a,)),d)
   checks+=1
actual=finish(()); pay=[utility(actual,i) for i in range(M)]
assert pay==[F(1),F(12),F(12)] and sum(pay)==25
values={}
for v in product(range(K),repeat=2):
 g=sum((utility((t,)+v,0) for t in range(K)),F())/K
 expected=F(12) if adjacent(*v) else F(11)
 assert g==expected
 values[v]=g
menus=[]
for i in range(M):
 cols=[]
 for a in range(K):
  w=finish(actual[:i]+(a,)); v=w[:i]+w[i+1:]
  cols.append(values[v])
 menus.append(min(cols))
assert menus==[F(11),F(11),F(12)] and sum(menus)-sum(pay)==9
# Nonnegative monotone extension: phi0=phi1=0, phi2hat=phi2+11,
# phi3hat=phi3+22. Utilities are their marginal differences.
minimum=F(100)
for z in product(range(K),repeat=3):
 for i in range(3):
  value=utility(z,i); minimum=min(minimum,value)
  assert value>=0
for v in product(range(K),repeat=2):assert phi2(tuple(sorted(v)))+11>=0
before=phi2((0,1))+11
after=phi3((0,1,1))+22-(phi2((0,1))+11)
assert after==12>before==10
out={'scope':'Anonymous exact marginal-potential game; explicitly NOT a CAG or HALF counterexample.',
 'K':K,'players':M,'actual':actual,'payoffs':list(map(str,pay)),'total_utility':str(sum(pay)),
 'complete_ordered_histories':sum(K**d for d in range(M)),
 'all_history_action_comparisons':checks,'position_menu_minima':list(map(str,menus)),
 'AFC_violation':str(sum(menus)-sum(pay)),
 'uniform_static_security_lower_bound':'11','aggregate_security_violation_at_least':str(M*11-sum(pay)),
 'nonnegative_marginals':True,'all_level_monotone_extension':True,
 'DR_witness':{'add_second':'10','add_third_same':'12'},'minimum_terminal_payoff':str(minimum)}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
