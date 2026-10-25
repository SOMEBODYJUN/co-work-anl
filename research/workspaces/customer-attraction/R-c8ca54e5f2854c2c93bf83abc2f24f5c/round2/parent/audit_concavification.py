"""Independent finite check of the general cardinality-concavification theorem.
The theorem is analytic; the concrete example is NOT a customer-attraction game.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement,product
from pathlib import Path
import json
K=22;m=3;M=F(21);L=F(43)
def adjacent(a,b):return (a-b)%K in (1,K-1)
@lru_cache(None)
def phi3(s):return F(0) if any(adjacent(a,b) for a in s for b in s) else F(11)
@lru_cache(None)
def phi2(s):
 a,b=s
 if a==b:return F(10)
 if adjacent(a,b):return F(-1)
 return sum((phi3(tuple(sorted((a,b,t)))) for t in range(K)),F())/K
@lru_cache(None)
def old(s):
 if len(s)<2:return F()
 return phi2(s)+11 if len(s)==2 else phi3(s)+22
@lru_cache(None)
def new(s):return old(s)+L*len(s)-M*len(s)*(len(s)-1)/2
def add(s,a):return tuple(sorted(s+(a,)))
max_old=F();max_new=None;dc=0
for n in range(m-1):
 for s in combinations_with_replacement(range(K),n):
  for a,b in product(range(K),repeat=2):
   oldd=old(add(add(s,a),b))-old(add(s,a))-old(add(s,b))+old(s)
   newd=new(add(add(s,a),b))-new(add(s,a))-new(add(s,b))+new(s)
   assert newd==oldd-M and newd<=0
   max_old=max(max_old,oldd);max_new=newd if max_new is None else max(max_new,newd);dc+=1
assert max_old==M
min_increment=None;mc=0
for n in range(m):
 for s in combinations_with_replacement(range(K),n):
  for a in range(K):
   inc=new(add(s,a))-new(s);assert inc>=0
   min_increment=inc if min_increment is None else min(min_increment,inc);mc+=1
D=L-M*(m-1);assert D==1
for z in combinations_with_replacement(range(K),m):
 for i in range(m):
  v=z[:i]+z[i+1:]
  assert new(z)-new(v)==old(z)-old(v)+D
actual=(0,1,1)
new_u=[new(tuple(sorted(actual)))-new(tuple(sorted(actual[:i]+actual[i+1:]))) for i in range(m)]
assert new_u==[F(2),F(13),F(13)]
# The original full-history policy remains SPE because EVERY terminal payoff
# of EVERY role is shifted by the same D, including all deviations.
query={}
for v in combinations_with_replacement(range(K),m-1):
 g=sum((new(add(v,a))-new(v) for a in range(K)),F())/K
 oldg=sum((old(add(v,a))-old(v) for a in range(K)),F())/K
 assert g==oldg+D
 query[v]=g
def finish(h):
 while len(h)<m:
  if not h:a=0
  elif len(h)==1:a=(h[0]+1)%K
  else:a=h[1] if adjacent(h[0],h[1]) else h[0]
  h=h+(a,)
 return h
menus=[]
for i in range(m):
 columns=[]
 for a in range(K):
  z=finish(actual[:i]+(a,)); v=tuple(sorted(z[:i]+z[i+1:]))
  columns.append(query[v])
 menus.append(min(columns))
assert sum(menus)-sum(new_u)==9
# Singleton layer edge cases: empty mixed-difference set, one action, m=1.
phi0=F(-7);phi1=F(-9);M1=F();L1=max(F(),phi0-phi1)
assert (phi1-phi0)+L1>=0 and L1-M1*0==2
out={'scope':'Anonymous monotone DR marginal-potential counterexample, NOT CAG.',
 'M':str(M),'L':str(L),'terminal_and_query_shift':str(D),
 'local_DR_comparisons':dc,'maximum_original_second_difference':str(max_old),
 'maximum_new_second_difference':str(max_new),'monotonicity_comparisons':mc,
 'minimum_increment':str(min_increment),'new_actual_payoffs':list(map(str,new_u)),
 'new_actual_total_utility':str(sum(new_u)),'new_menu_minima':list(map(str,menus)),
 'AFC_gap':str(sum(menus)-sum(new_u)),'empty_second_difference_m1_checked':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
