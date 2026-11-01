#!/usr/bin/env python3
"""Independent audit of parent's actual-source uniform-optimal-menu bridge failure.
Uses no game-model/strategy/certificate modules and no discovery implementation.
All actual mathematical comparisons use integer multiples of 60 or Fraction.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement,product
from pathlib import Path
import json

BASE=((4,1),(27,4),(29,3),(30,3),(31,2),(32,1),(43,3),(45,3),(46,3),(51,3),(53,3),(54,3),(59,2))
CUSTOMERS=tuple(mask for mask,r in BASE for _ in range(r))+tuple(1<<a for a in (6,7,8) for _ in range(18))
M=6;Q=9;ANCHOR=(6,7,8)
@lru_cache(None)
def payoff60(multiset):
 loads=tuple(sum((mask>>a)&1 for a in multiset) for mask in CUSTOMERS)
 return tuple(sum(60//c for mask,c in zip(CUSTOMERS,loads) if (mask>>a)&1 and c) for a in range(Q))

def cover(seq):return sum(any((mask>>a)&1 for a in seq) for mask in CUSTOMERS)

def override(h):
 if len(h)<3 and h==ANCHOR[:len(h)]:return ANCHOR[len(h)]
 if h[:3]!=ANCHOR:return None
 r=h[3:]
 if not r:return 0
 if len(r)==1:return (3 if r[0]<3 else 0) if r[0]<6 else 3
 if max(r)<6:
  return next(a for a in (range(3) if r[1]<3 else range(3,6)) if a not in r)
 if r[0]>=6 and r[1]==3:return 4
 return None

def run():
 policy={};desc={}; histories=0
 def build(h):
  nonlocal histories
  if len(h)==M:return h
  branches=tuple(build(h+(a,)) for a in range(Q))
  vals=tuple(payoff60(tuple(sorted(z)))[a] for a,z in enumerate(branches))
  chosen=vals.index(max(vals));fixed=override(h)
  if fixed is not None:
   assert vals[fixed]==max(vals),(h,fixed,vals)
   chosen=fixed
  policy[h]=chosen;desc[h]=branches[chosen];histories+=1
  return branches[chosen]
 actual=build(())
 assert actual==(6,7,8,0,3,4)
 # Re-follow the completed map for every action, not using build's saved leaves.
 def follow(h):
  while len(h)<M:h=h+(policy[h],)
  return h
 tested=0;minimum=None
 for h,a in policy.items():
  z=follow(h); own=payoff60(tuple(sorted(z)))[a]
  for q in range(Q):
   if q==a:continue
   rival=payoff60(tuple(sorted(follow(h+(q,)))))[q]
   slack=own-rival;assert slack>=0
   minimum=slack if minimum is None else min(minimum,slack);tested+=1
 def u(a,seq):return F(payoff60(tuple(sorted(seq)))[a],60)
 def one(a,theme):
  return sum((F(1,1+sum((mask>>v)&1 for v in ANCHOR)+((mask>>a)&1)) for mask in CUSTOMERS if (mask>>theme)&1),F())
 rows=[]
 for menu in combinations_with_replacement(range(Q),M):
  if cover(menu)!=88:continue
  tails=tuple(follow(ANCHOR+(a,))[-2:] for a in menu)
  diag=sum((u(a,ANCHOR+(a,)+tail) for a,tail in zip(menu,tails)),F())/6
  indep=sum((u(a,ANCHOR+(a,)+tail) for a in menu for tail in tails),F())/36
  ic1=ic2=opt=F()
  for a,(b,c) in zip(menu,tails):
   for e,f in tails:
    g=policy[ANCHOR+(a,e)]
    ic1+=(u(b,ANCHOR+(a,b,c))-u(e,ANCHOR+(a,e,g)))/36
    ic2+=(u(g,ANCHOR+(a,e,g))-u(f,ANCHOR+(a,e,f)))/36
    opt+=(one(a,c)-one(a,g))/36
  assert diag-indep==ic1+ic2+opt and diag<indep and ic1>=0 and ic2>=0
  rows.append({'menu':menu,'diagonal':str(diag),'independent':str(indep),'delta':str(diag-indep),'first_ic':str(ic1),'last_ic':str(ic2),'option':str(opt)})
 assert histories==66430 and tested==531440 and len(rows)==4
 return {'status':'independent exact auxiliary-counterexample audit passed; no half or ROW counterexample', 'customers':len(CUSTOMERS),'histories':histories,'nonself_ics':tested,'minimum_ic_times_60':minimum,'actual':actual,'payoffs':[str(u(a,actual)) for a in actual],'W':cover(actual),'OPT6':88,'optimal_menus':rows}
if __name__=='__main__':
 report=run();target=Path(__file__).with_suffix('.json');target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
