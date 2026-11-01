"""Definition-level finite replay of the Q/B recursive construction.
All unstructured children receive one independently computed Markov SPE.
The finite runs audit the construction; the general theorem uses its proof.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
ROOT=Path(__file__).parent

def audit(k):
 p=3*k+1;m=k+1;D=3*k
 topics=[]
 for i in range(k):
  X={3*i,3*i+1};topics.extend((X|{3*i+2},X|{3*k},X))
 topics.append({3*k,3*k+1});N=3*k+2
 def util(c,a):return sum((Fraction(1,sum(c[b]for b in range(p)if x in topics[b]))for x in topics[a]),Fraction(0))
 def add(c,a):return tuple(v+int(b==a)for b,v in enumerate(c))
 @lru_cache(None)
 def fallback(c):
  if sum(c)==m:return c
  children=[fallback(add(c,a))for a in range(p)];vals=[util(children[a],a)for a in range(p)];a=max(range(p),key=lambda a:(vals[a],-a));fallback_actions[c]=a;return children[a]
 fallback_actions={};fallback((0,)*p)
 actions={};modes={};counts={'Q':0,'B':0,'fallback':0}
 def expand(h,c,mode,U,pending):
  if len(h)==m:return
  counts[mode]+=1;modes[h]=mode
  if mode=='fallback':chosen=fallback_actions[c]
  elif mode=='B':chosen=3*min(U)if U else 3*pending
  else:chosen=3*min(U)+2 if U else D if pending is None else 3*pending+1
  actions[h]=chosen
  for a in range(p):
   childmode='fallback';childU=U;childpending=pending
   if mode=='Q'and U:
    if a==chosen:childmode='Q';childU=U-{a//3}
    elif a<D and a//3 in U and a%3==0:childmode='Q';childU=U-{a//3};childpending=a//3
    elif a<D and a//3 in U and a%3==1:childmode='B';childU=U-{a//3};childpending=a//3
   elif mode=='B'and U and a==chosen:childmode='B';childU=U-{a//3}
   expand(h+(a,),add(c,a),childmode,childU,childpending)
 expand((),(0,)*p,'Q',frozenset(range(k)),None)
 def finish(h):
  while len(h)<m:h=h+(actions[h],)
  return h
 def hc(h):return tuple(h.count(a)for a in range(p))
 minimum=None;strict=0;compares=0
 for h,a in actions.items():
  on=util(hc(finish(h)),a)
  for b in range(p):
   off=util(hc(finish(h+(b,))),b);slack=on-off;assert slack>=0,(k,h,modes[h],a,b,slack)
   minimum=slack if minimum is None else min(minimum,slack);strict+=int(slack>0);compares+=1
 actual=finish(());covered=set().union(*(topics[a]for a in actual));loads=[sum(x in topics[a]for a in actual)for x in range(N)];assert all(c<=1 for c in loads);assert len(covered)==2*k+2
 optimal_topics=tuple([3*i for i in range(k)]+[D]);assert set().union(*(topics[a]for a in optimal_topics))==set(range(N))
 return {'k':k,'players':m,'topics':p,'clients':N,'actual':actual,'payoffs':[str(util(hc(actual),a))for a in actual],'W':len(covered),'OPT':N,'ratio':str(Fraction(N,len(covered))),'histories':len(actions),'comparisons':compares,'strict_comparisons':strict,'minimum_slack':str(minimum),'mode_history_counts':counts,'max_actual_client_load':max(loads)}
report=[audit(k)for k in (1,2,3)]
print(json.dumps(report,indent=2));(ROOT/'collision_free_family_audit.json').write_text(json.dumps(report,indent=2)+'\n')
