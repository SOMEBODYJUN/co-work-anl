"""Independent Fraction all-outcome audit of 2 W_H-OPT >= |K|+3 delta.

Small finite examples only. No canonical model or SPE solver is imported.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import json,random


def solve(topics,m):
 n=len(topics);customers=set().union(*topics)
 @lru_cache(None)
 def pay(q,a):
  return sum((F(1,sum(q[j] for j,T in enumerate(topics) if x in T)) for x in topics[a]),F(0))
 def inc(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
 @lru_cache(None)
 def outcomes(q):
  if sum(q)==m:return frozenset([q])
  children=[outcomes(inc(q,a)) for a in range(n)]
  threshold=max(min(pay(z,a) for z in child) for a,child in enumerate(children))
  return frozenset(z for a,child in enumerate(children) for z in child if pay(z,a)>=threshold)
 def welfare(q):return len(set().union(*(T for a,T in enumerate(topics) if q[a])))
 O=max(welfare(tuple(int(a in I) for a in range(n))) for h in range(min(m,n)+1) for I in combinations(range(n),h))
 K=set.intersection(*(set(T) for T in topics))
 comparisons=0;positive=0;maxdef=F(0)
 for a in range(n):
  prefix=inc((0,)*n,a);zs=outcomes(prefix)
  for hi in zs:
   for lo in zs:
    delta=pay(hi,a)-pay(lo,a)
    if delta<=0:continue
    positive+=1
    margin=F(2*welfare(hi)-O-len(K))-3*delta
    assert margin>=0,(topics,m,a,hi,lo,delta,margin)
    maxdef=max(maxdef,delta)
   comparisons+=len(zs)
 return {'m':m,'themes':n,'customers':len(customers),'core':len(K),'outcome_pairs':comparisons,'positive_pairs':positive,'max_delta':str(maxdef)}


def main():
 rng=random.Random(7362129);reports=[]
 # Explicit sharp cases, with and without global core.
 for m in range(2,7):
  start=0;topics=[]
  for w in [2,m-1]+[1]*(m-2):
   topics.append(frozenset(range(start,start+w)));start+=w
  reports.append(solve(topics,m))
  reports.append(solve([T|{1000} for T in topics],m))
 # Arbitrary within-petal subthemes, a root may be proper or empty residual.
 for it in range(24):
  k=rng.randrange(2,5);m=rng.randrange(2,6);core={1000} if it%2 else set()
  topics=[];start=0
  for j in range(k):
   w=rng.randrange(1,5);B=set(range(start,start+w));start+=w
   topics.append(frozenset(B|core))
   for z in range(rng.randrange(0,3)):
    T={x for x in B if rng.randrange(2)}
    topics.append(frozenset(T|core))
  topics=list(dict.fromkeys(topics))
  reports.append(solve(topics,m))
 out={'scope':'finite exact audit; analytic proof carries universal statement','cases':reports,'case_count':len(reports),'positive_pairs':sum(r['positive_pairs'] for r in reports),'outcome_pairs':sum(r['outcome_pairs'] for r in reports)}
 Path(__file__).with_name('insurer_three_sharp_audit.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
