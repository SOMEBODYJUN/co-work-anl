"""One unit-customer full-product regression for the general compiler.
Suggested by parent: original A=1,B=4,z=AAB,j=2, common scale2.
No repository model/solver imported. All 43 histories and 258 actions checked.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product,combinations
from pathlib import Path
import json

m,j=3,2
oldsize=(Q(2),Q(8)); banksize=(Q(6),Q(6),Q(3)); s=Q(3); d=1

def inc(c,a): return c[:a]+(c[a]+1,)+c[a+1:]
def counts(h,p): return tuple(h.count(a) for a in range(p))
def pay(size,c,a): return size[a]/c[a] if c[a] else Q(0)

@lru_cache(None)
def oldout(c):
 if sum(c)==m: return frozenset((c,))
 children=[oldout(inc(c,a)) for a in range(2)]
 floor=max(min(pay(oldsize,t,a) for t in child) for a,child in enumerate(children))
 return frozenset(t for a,child in enumerate(children) for t in child if pay(oldsize,t,a)>=floor)

def oldrho(i,A):
 h=(0,)*(i-1)+(A,); c=counts(h,2)
 target=min(oldout(c),key=lambda t:(pay(oldsize,t,A),t)); acts={}
 def expand(h,t):
  if len(h)==m: return
  c=counts(h,2); children=[oldout(inc(c,a)) for a in range(2)]
  floor=max(min(pay(oldsize,z,a) for z in ch) for a,ch in enumerate(children))
  a=next(a for a,ch in enumerate(children) if t in ch and pay(oldsize,t,a)>=floor)
  acts[h]=a
  for b,ch in enumerate(children):
   tt=t if b==a else min(ch,key=lambda z:(pay(oldsize,z,b),z))
   expand(h+(b,),tt)
 expand(h,target)
 return acts,pay(oldsize,target,A)

@lru_cache(None)
def bankbi(c):
 if sum(c)==m:return c
 ends=[bankbi(inc(c,a)) for a in range(3)]
 return ends[max(range(3),key=lambda a:(pay(banksize,ends[a],a),-a))]

def bankrho(i,T):
 h=tuple(range(i-1))+(T,); acts={}
 mode='BI' if T<i-1 else 'Y' if T==j else 'F'; F=T
 def expand(h):
  if len(h)==m:return
  c=counts(h,3)
  clean=all(x<=1 for x in c[:j]) and c[j]<=(d if mode=='Y' else d-1)
  if mode=='BI' or not clean:
   end=bankbi(c)
   a=max(range(3),key=lambda a:(pay(banksize,bankbi(inc(c,a)),a),-a))
  else:
   empty=[a for a in range(j) if c[a]==0]
   a=empty[0] if empty else j if mode=='Y' or c[j]<d-1 else F
  acts[h]=a
  for a in range(3):expand(h+(a,))
 expand(h)
 return acts

oldr={}; bankr={}; floors={}
for i in (1,2):
 for A in range(2):
  oldr[i,A],floors[i,A]=oldrho(i,A)
 for T in range(3):bankr[i,T]=bankrho(i,T)
normal=((0,0),(0,1)); joint=list(product(range(2),range(3))); actions={}
for k in range(m):
 for h in product(joint,repeat=k):
  first=next((i for i in range(min(j,k)) if h[i]!=normal[i]),None)
  if first is not None:
   i=first+1; A,T=h[first]
   actions[h]=(oldr[i,A][tuple(a for a,t in h)],bankr[i,T][tuple(t for a,t in h)])
  elif k<j:actions[h]=normal[k]
  else:actions[h]=(1,2)

# Expand the 25 distinct unit customers and the six actual set-valued topics.
oldsets=(set(range(2)),set(range(2,10)))
banksets=(set(range(10,16)),set(range(16,22)),set(range(22,25)))
cover={a:oldsets[a[0]]|banksets[a[1]] for a in joint}
def terminal(h):
 while len(h)<m:h=h+(actions[h],)
 return h
def utilities(z):
 load={x:sum(x in cover[a] for a in z) for x in range(25)}
 return tuple(sum((Q(1,load[x]) for x in cover[a]),Q(0)) for a in z)
checks=0; minmargin=None
for h,a in actions.items():
 base=utilities(terminal(h))[len(h)]
 for b in joint:
  margin=base-utilities(terminal(h+(b,)))[len(h)]
  assert margin>=0,(h,a,b,margin)
  checks+=1;minmargin=margin if minmargin is None else min(minmargin,margin)
z=terminal(()); u=utilities(z); W=len(set().union(*(cover[a] for a in z)))
O=max(len(set().union(*(cover[a] for a in z))) for z in product(joint,repeat=m))
assert u==(Q(7),Q(7),Q(11)) and W==O==25
old_u=(Q(1),Q(1),Q(8)); Delta=max(Q(0),*(floors[i,A]-old_u[i-1] for i,A in floors))
assert Delta==s
result={'source_original':'A size1,B size4, target AAB; all customers scaled2','m':m,'j':j,'bank_d':d,'customers':25,'topics':6,'full_ordered_decision_histories':len(actions),'all_action_IC_checks':checks,'minimum_IC_margin':str(minmargin),'old_min_child_floor':{f'{i}:{A}':str(v) for (i,A),v in floors.items()},'Delta_after_scale':str(Delta),'s':str(s),'actual_joint_path':z,'actual_player_payoffs':[str(x) for x in u],'actual_W':W,'OPT_m':O,'actions':[{ 'history':h,'action':a} for h,a in actions.items()]}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='actions'}))
