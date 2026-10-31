from itertools import product,combinations_with_replacement
from fractions import Fraction as F
import json,random

P=3

def solve(w,details=False):
 def payoff(z,a):
  return sum((F(n,sum(bool((1<<x)&mask) for x in z)) for mask,n in enumerate(w,1) if n and ((1<<a)&mask)),F(0))
 def counts(z): return tuple(z.count(a) for a in range(P))
 leaves={ab:tuple(c for c in range(P) if payoff(ab+(c,),c)==max(payoff(ab+(d,),d) for d in range(P))) for ab in combinations_with_replacement(range(P),2)}
 def terminal(a,b,mp): return (a,b,mp[tuple(sorted((a,b)))])
 markov=set(); maps=0
 for cs in product(*leaves.values()):
  maps+=1; mp=dict(zip(leaves,cs)); seconds={}
  for a in range(P):
   vals=[payoff(terminal(a,b,mp),b) for b in range(P)]
   seconds[a]=tuple(b for b in range(P) if vals[b]==max(vals))
  floor=max(min(payoff(terminal(a,b,mp),a) for b in seconds[a]) for a in range(P))
  for a in range(P):
   for b in seconds[a]:
    z=terminal(a,b,mp)
    if payoff(z,a)>=floor: markov.add(counts(z))
 # full histories, local last maps for each first action independent
 child={}
 for a in range(P):
  poss=[]
  for cs in product(*(leaves[tuple(sorted((a,b)))] for b in range(P))):
   vals=[payoff((a,b,cs[b]),b) for b in range(P)]
   for b in range(P):
    if vals[b]==max(vals): poss.append((a,b,cs[b]))
  child[a]=set(poss)
 floor=max(min(payoff(z,a) for z in child[a]) for a in range(P))
 full={counts(z) for a in range(P) for z in child[a] if payoff(z,a)>=floor}
 return full,markov,maps

if __name__=='__main__':
 rng=random.Random(1001); best=None; totalmaps=0
 for idx,w in enumerate(product(range(2),repeat=7)):
  full,markov,maps=solve(w);totalmaps+=maps
  if full!=markov: print(json.dumps({'weights':w,'only_full':list(full-markov),'full':list(full),'markov':list(markov),'maps':maps}));break
 else:
  print('all 128 binary equal',totalmaps)
 for i in range(10000):
  w=tuple(rng.randrange(8) for _ in range(7));full,markov,maps=solve(w);totalmaps+=maps
  if full!=markov: print(json.dumps({'weights':w,'only_full':list(full-markov),'full':list(full),'markov':list(markov),'maps':maps}));break
 else: print('all 10000 random equal',totalmaps)
