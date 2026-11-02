#!/usr/bin/env python3
"""Exact full-history audit of potential-optimal supported-branch obstruction.
The 3-player obstruction is embedded on the actual path of an exactly 6-player
complete pure SPE using a fourth disjoint topic of three unit clients.
"""
from functools import lru_cache
from itertools import product
from fractions import Fraction as F
from pathlib import Path
import json
BASE=Path(__file__).resolve().parent
small={():2,(0,):1,(1,):0,(2,):0,(0,0):1,(0,1):0,(0,2):0,(1,0):1,(1,1):0,(1,2):0,(2,0):0,(2,1):0,(2,2):0}
clients=[{0},{0,1},{1,2}]
def finish(policy,h,m):
 while len(h)<m:h=h+(policy[h],)
 return h
def payoff(terminal,i,cs):
 return sum((F(1,sum(a in c for a in terminal)) for c in cs if terminal[i] in c),F())
def tax(terminal,start,cs):
 m=len(terminal)
 return sum((F(1,1+sum(a in c for a in terminal[:i]))-F(1,m-i+sum(a in c for a in terminal[:i])) for i in range(start,m) for c in cs if terminal[i] in c),F())
def potential(terminal,start,cs):
 b=[sum(a in c for a in terminal[:start]) for c in cs]
 return sum((sum((F(1,bx+j) for j in range(1,sum(a in c for a in terminal[start:])+1)),F()) for c,bx in zip(cs,b)),F())
def budget(terminal,start,cs):return sum((payoff(terminal,i,cs) for i in range(start,len(terminal))),F())+tax(terminal,start,cs)
def audit(policy,m,p,cs):
 minimum=None;comparisons=0
 for h,a in policy.items():
  actual=finish(policy,h,m);u=payoff(actual,len(h),cs)
  for t in range(p):
   off=finish(policy,h+(t,),m);slack=u-payoff(off,len(h),cs)
   assert slack>=0,(h,a,t,actual,off,slack)
   minimum=slack if minimum is None else min(minimum,slack);comparisons+=1
 return {'histories':len(policy),'action_comparisons':comparisons,'minimum_IC_slack':str(minimum),'actual':finish(policy,(),m)}

small_audit=audit(small,3,3,clients)
A=finish(small,(),3);B=budget(A,0,clients)
allphi={t:potential(t,0,clients) for t in product(range(3),repeat=3)};P=max(allphi.values());support=sorted({a for t,v in allphi.items() if v==P for a in t})
off=[]
for t in support:
 terminal=finish(small,(t,),3);demand=sum(t in c for c in clients)+budget(terminal,1,clients)
 assert demand>B
 off.append({'topic':t,'terminal':terminal,'root_payoff':str(payoff(terminal,0,clients)),'arrival_plus_child_budget':str(demand),'excess':str(demand-B)})
assert B==F(14,3) and P==F(13,3) and support==[0,1]

# Force the previous strategy after the actual prefix (3,3,3). All histories,
# including those with fourth-topic moves after that prefix, remain present.
m=6;p=4;bigclients=clients+[{3},{3},{3}]
forced={():3,(3,):3,(3,3):3}
forced.update({(3,3,3)+h:a for h,a in small.items()})
def counts(h):return tuple(h.count(a) for a in range(p))
@lru_cache(None)
def U(q,a):
 return sum((F(1,sum(q[t] for t in c)) for c in bigclients if a in c),F())
@lru_cache(None)
def E(h):
 if len(h)==m:return frozenset([counts(h)])
 children=[E(h+(a,)) for a in range(p)]
 assert all(children),(h,'empty forced child')
 threshold=max(min(U(q,a) for q in child) for a,child in enumerate(children))
 choices=[forced[h]] if h in forced else range(p)
 out=set()
 for a in choices:
  out.update(q for q in children[a] if U(q,a)>=threshold)
 assert out,(h,'forced choices violate SPE')
 return frozenset(out)
E(())
policy={}
def realize(h,desired):
 if len(h)==m:return
 children=[E(h+(a,)) for a in range(p)]
 threshold=max(min(U(q,a) for q in child) for a,child in enumerate(children))
 choices=[forced[h]] if h in forced else range(p)
 a=next(a for a in choices if desired in children[a] and U(desired,a)>=threshold)
 policy[h]=a
 for t,child in enumerate(children):
  q=desired if t==a else min(child,key=lambda q:(U(q,t),q))
  realize(h+(t,),q)
rootterminal=(2,0,1,3) # counts for path 3,3,3,2,0,0
assert rootterminal in E(())
realize((),rootterminal)
big_audit=audit(policy,6,4,bigclients)
assert big_audit['actual']==(3,3,3,2,0,0)
for h,a in small.items():assert policy[(3,3,3)+h]==a
# The exact induction interface at the actual depth-three subgame retains the
# same local B,P and the same failure on every optimal comparison support topic.
h=(3,3,3);actual=finish(policy,h,6);localB=budget(actual,3,bigclients)
localphis={t:potential(h+t,3,bigclients) for t in product(range(4),repeat=3)};localP=max(localphis.values());localsupport=sorted({a for t,v in localphis.items() if v==localP for a in t})
assert localB==B and localP==P and localsupport==[0,1]
bigoff=[]
for t in localsupport:
 terminal=finish(policy,h+(t,),6)
 arrival=sum((F(1,1+sum(a in c for a in h)) for c in bigclients if t in c),F())
 demand=arrival+budget(terminal,4,bigclients)
 childP=max(potential(h+(t,)+tail,4,bigclients) for tail in product(range(4),repeat=2))
 assert childP==F(7,3) and budget(terminal,4,bigclients)-childP==F(1,2)
 assert demand>localB
 bigoff.append({'topic':t,'terminal':terminal,'root_payoff':str(payoff(terminal,3,bigclients)),'arrival_plus_child_budget':str(demand),'excess':str(demand-localB),'child_maximum_relative_potential':str(childP),'child_budget_slack':str(budget(terminal,4,bigclients)-childP)})
globalB=budget(actual,0,bigclients)
globalP=max(potential(t,0,bigclients) for t in product(range(4),repeat=6))
assert globalB==F(35,3) and globalP==F(59,6)
report={'status':'EXACT_FULL_SPE_INTERFACE_COUNTEREXAMPLE_ONLY','scope':'refutes existence of a BRANCH-MONO child among all maximum-potential support topics; does not refute potential candidate or half','three_player':{**small_audit,'actual_budget':str(B),'maximum_potential':str(P),'optimal_support':support,'offbranches':off},'six_player':{**big_audit,'unit_clients':len(bigclients),'catalog':[[i for i,c in enumerate(bigclients) if a in c] for a in range(4)],'actual_subgame_history':h,'local_budget':str(localB),'maximum_local_potential':str(localP),'local_optimal_support':localsupport,'offbranches':bigoff,'all_count_outcomes_at_root':len(E(())),'global_W_plus_C':str(globalB),'global_P6':str(globalP),'global_candidate_slack':str(globalB-globalP)},'forced_policy_nodes':len(forced)}
(BASE/'supported_branch_audit.json').write_text(json.dumps(report,indent=2)+'\n')
(BASE/'supported_branch_six_full_policy.json').write_text(json.dumps({'m':m,'p':p,'clients':[sorted(c) for c in bigclients],'policy':[{'history':h,'action':a} for h,a in sorted(policy.items())]},indent=2)+'\n')
print(json.dumps(report,indent=2))
