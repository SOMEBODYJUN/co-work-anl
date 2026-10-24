from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import random,json
random.seed(10624)

def run(weights,q,m):
    @lru_cache(None)
    def u(a,counts):
        return sum((F(w,sum(counts[b] for b in range(q) if mask>>b&1)) for mask,w in weights if mask>>a&1),F())
    @lru_cache(None)
    def eq(counts):
        if sum(counts)==m:return frozenset([counts])
        children=[];mins=[]
        for a in range(q):
            new=list(counts);new[a]+=1
            ends=eq(tuple(new));children.append(ends);mins.append(min(u(a,c) for c in ends))
        floor=max(mins)
        return frozenset(c for a,ends in enumerate(children) for c in ends if u(a,c)>=floor)
    def phi(c):
        return sum((w*sum((F(1,k) for k in range(1,sum(c[b] for b in range(q) if mask>>b&1)+1)),F()) for mask,w in weights),F())
    poss=[]
    for seq in product(range(q),repeat=m):
        c=tuple(seq.count(a) for a in range(q))
        if c not in poss:poss.append(c)
    p=max(map(phi,poss));top={c for c in poss if phi(c)==p};e=eq((0,)*q)
    if not top.intersection(e):return dict(weights=weights,q=q,m=m,phi=str(p),potential_max=sorted(top),SPE=sorted(e),spe_max_phi=str(max(map(phi,e))))
    return None

for t in range(2000):
    q=random.choice([3,4]);m=random.choice([3,4,5]);weights=[(mask,random.randrange(6)) for mask in range(1,2**q)]
    weights=[(mask,w) for mask,w in weights if w]
    r=run(tuple(weights),q,m)
    if r:
        print(json.dumps(dict(iteration=t,obstruction=r)));break
else:print('no obstruction in 2000 probes')
