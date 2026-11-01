from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from functools import lru_cache
import random,json,argparse

# Tests this exact all-input sufficient candidate only:
# OPT_m <= 2 sum_i quantile_r {F_j^{b_i,r}(k)}, independently of path SPE.
# Maximal-only inputs give their unique containment routing.
def evaluate(themes,m):
    themes=tuple(frozenset(t) for t in themes); s=len(themes)
    clients=sorted(set().union(*themes)); pos={x:i for i,x in enumerate(clients)}
    themes=tuple(tuple(pos[x] for x in t) for t in themes); n=len(clients)
    masks=[sum(1<<x for x in t) for t in themes]
    profiles={r:list(combinations_with_replacement(range(s),r)) for r in range(m)}
    opt=max((len(set().union(*(set(themes[j]) for j in p))) for p in combinations_with_replacement(range(s),m)),default=0)
    @lru_cache(None)
    def floor(counts):
        t=sum(counts); r=m-t
        b=[sum(counts[j] for j in range(s) if x in themes[j]) for x in range(n)]
        vals=[[None]*r for j in range(s)]
        for y in profiles[r-1]:
            q=[y.count(j) for j in range(s)]
            loads=[b[x]+1+sum(q[j] for j in range(s) if x in themes[j]) for x in range(n)]
            for j,T in enumerate(themes):
                pay=sum((F(1,loads[x]) for x in T),F())
                for k in range(q[j]+1,r+1):
                    if vals[j][k-1] is None or pay<vals[j][k-1]:vals[j][k-1]=pay
        flat=[v for row in vals for v in row]
        inf=sum(v is None for v in flat)
        finite=sorted((v for v in flat if v is not None),reverse=True)
        assert inf<r,(themes,m,counts,vals)
        return finite[r-inf-1]
    @lru_cache(None)
    def walk(counts):
        if sum(counts)==m:return F(),()
        mu=floor(counts)
        best=None
        for j in range(s):
            nxt=tuple(c+(i==j) for i,c in enumerate(counts))
            val,p=walk(nxt); z=(mu+val,(j,)+p)
            if best is None or z<best:best=z
        return best
    total,path=walk((0,)*s)
    if 2*total<opt:
        b=(0,)*s; floors=[]
        for j in path:
            floors.append(str(floor(b)));b=tuple(c+(i==j) for i,c in enumerate(b))
        return {'m':m,'themes':[[clients[x] for x in T] for T in themes],'opt':opt,'path':path,'floors':floors,'floor_sum':str(total)}

if __name__=='__main__':
    rng=random.Random(20261024)
    for trial in range(300):
        s=rng.choice([3,4,5,6]);m=rng.choice([3,4,5]);n=rng.choice([8,10,15,20])
        raw=[{x for x in range(n) if rng.random()<rng.uniform(.2,.8)} for j in range(s)]
        T=[a for j,a in enumerate(raw) if not any(a<b or (a==b and k<j) for k,b in enumerate(raw))]
        if len(T)<2:continue
        out=evaluate(T,m)
        if out:
            out['trial']=trial
            print(json.dumps(out,indent=2));break
    else: print('No counterexample to the explicitly stated path-only sufficient candidate in 300 diagnostic inputs; no theorem inferred.')
