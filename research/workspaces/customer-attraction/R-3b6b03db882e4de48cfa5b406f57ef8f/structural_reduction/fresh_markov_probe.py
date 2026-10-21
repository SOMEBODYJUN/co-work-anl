"""Exact fresh-subset marginal-potential game: compatible count selectors."""
from itertools import combinations,product
from functools import lru_cache
from random import Random
import json
from pathlib import Path

def outcomes(p,n,F):
 @lru_cache(None)
 def solve(S):
  if len(S)==n:return frozenset({S})
  children={a:solve(tuple(sorted((*S,a)))) for a in range(p) if a not in S}
  floor=max(min(F[T]-F[tuple(b for b in T if b!=a)] for T in child) for a,child in children.items())
  return frozenset(T for a,child in children.items() for T in child if F[T]-F[tuple(b for b in T if b!=a)]>=floor)
 return solve(())

def markov3(p,F):
 pairs=list(combinations(range(p),2));menus=[]
 for S in pairs:
  v={a:F[tuple(sorted((*S,a)))] for a in range(p) if a not in S}
  menus.append(tuple(a for a in v if v[a]==max(v.values())))
 ret=set()
 for last in product(*menus):
  qmap={S:tuple(sorted((*S,a))) for S,a in zip(pairs,last)}
  children=[]
  for first in range(p):
   v={a:F[qmap[tuple(sorted((first,a)))]]-F[tuple(b for b in qmap[tuple(sorted((first,a)))] if b!=a)] for a in range(p) if a!=first}
   children.append({qmap[tuple(sorted((first,a)))] for a in v if v[a]==max(v.values())})
  floor=max(min(F[T]-F[tuple(b for b in T if b!=a)] for T in child) for a,child in enumerate(children))
  ret.update(T for a,child in enumerate(children) for T in child if F[T]-F[tuple(b for b in T if b!=a)]>=floor)
 return ret

if __name__=='__main__':
 rng=Random(1317)
 for p in [4,5]:
  for j in range(10000):
   F={S:(rng.randrange(5) if len(S)==2 else (3 if len(S)==3 else 0)) for t in range(4) for S in combinations(range(p),t)}
   ao=outcomes(p,3,F);mo=markov3(p,F)
   if set(ao)!=mo:
    d={'p':p,'tested':j+1,'F':{','.join(map(str,k)):v for k,v in F.items()},'all':sorted(ao),'markov':sorted(mo),'gap':sorted(set(ao)-mo)}
    Path(__file__).with_name('fresh_markov_gap.json').write_text(json.dumps(d,indent=2));print(json.dumps(d,indent=2));break
  else:print('no gap',p);continue
  break
