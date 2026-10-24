from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement
import random,json
random.seed(120624)

def run(weights,q,m):
 @lru_cache(None)
 def u(a,c):return sum((F(w,sum(c[b] for b in range(q) if mask>>b&1)) for mask,w in weights if mask>>a&1),F())
 @lru_cache(None)
 def eq(c):
  if sum(c)==m:return frozenset([c])
  kids=[]
  for a in range(q):
   d=tuple(c[b]+(a==b) for b in range(q));kids.append(eq(d))
  floor=max(min(u(a,z) for z in zs) for a,zs in enumerate(kids))
  return frozenset(z for a,zs in enumerate(kids) for z in zs if u(a,z)>=floor)
 def phi(c):return sum((w*sum((F(1,k) for k in range(1,sum(c[b] for b in range(q) if mask>>b&1)+1)),F()) for mask,w in weights),F())
 poss={tuple(seq.count(a) for a in range(q)) for seq in combinations_with_replacement(range(q),m)}
 p=max(map(phi,poss));top={c for c in poss if phi(c)==p}
 bad=[]
 for c in top:
  allowed=[a for a in range(q) if c[a] and c in eq(tuple(int(a==b) for b in range(q)))]
  low=min(u(a,c) for a in range(q) if c[a])
  if not allowed or all(u(a,c)>low for a in allowed):bad.append((c,allowed,[(a,str(u(a,c))) for a in range(q) if c[a]]))
 if bad:return dict(weights=weights,q=q,m=m,phi=str(p),bad=bad)
 return None
for t in range(4000):
 q=random.choice([3,4]);m=random.choice([3,4,5,6]);weights=tuple((mask,w) for mask in range(1,2**q) if (w:=random.randrange(7)))
 r=run(weights,q,m)
 if r:
  print(json.dumps(dict(iteration=t,obstruction=r)));break
else:print('no obstruction in 4000 probes')
