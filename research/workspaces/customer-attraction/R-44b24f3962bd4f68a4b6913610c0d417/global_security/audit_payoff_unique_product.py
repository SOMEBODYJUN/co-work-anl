"""Finite independent regression for the stated payoff-unique product lemma."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json

def singleton_game(weights,tag):return [frozenset((tag,i,x)for x in range(w))for i,w in enumerate(weights)]
def pay(ss,z):
 return tuple(sum((F(1,sum(x in ss[a]for a in z))for x in ss[z[i]]),F())for i in range(len(z)))
def tree(ss,m):
 @lru_cache(None)
 def walk(h):
  if len(h)==m:return frozenset([h])
  ch=[walk(h+(a,))for a in range(len(ss))]
  floor=max(min(pay(ss,z)[len(h)]for z in c)for c in ch)
  return frozenset(z for c in ch for z in c if pay(ss,z)[len(h)]>=floor)
 root=walk(())
 unique=all(len({pay(ss,z)for z in walk(h)})==1 for l in range(m)for h in product(range(len(ss)),repeat=l))
 return root,unique

cases=[]
for m in range(1,6):
 for w1,w2 in product([(1,2),(1,3),(2,5),(1,1,1)],repeat=2):
  s1=singleton_game(w1,'I');s2=singleton_game(w2,'II')
  o1,u1=tree(s1,m);o2,u2=tree(s2,m)
  if not(u1 and u2):continue
  ss=[a|b for a,b in product(s1,s2)];oo,_=tree(ss,m);k2=len(s2)
  projected={(tuple(x//k2 for x in z),tuple(x%k2 for x in z))for z in oo}
  assert projected==set(product(o1,o2))
  cases.append(dict(m=m,weights=[w1,w2],joint_outcomes=len(oo)))
# The failure factor is rejected exactly by all-player payoff uniqueness.
_,u=tree(singleton_game((1,1),'F'),3);assert not u
print(json.dumps({'status':'finite_exact_regression_passed','passing_hypothesis_cases':len(cases),'cases':cases,'excluded_equal_two_colour_m3':True},indent=2))
