"""Finite falsification of precise general netROW, not HALF enumeration.

Every generated policy is obtained by exact full ordered-history backward
induction; count tables cache only terminal utility, never policy decisions.
"""
import json, math, random, sys
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement
from pathlib import Path

def run(m,k,weights,seed):
    rng=random.Random(seed)
    L=math.lcm(*range(1,m+1))
    policy={}
    @lru_cache(None)
    def values(counts):
        ans=[0]*k
        for mask,w in weights.items():
            n=sum(counts[a] for a in range(k) if mask>>a&1)
            if n:
                for a in range(k):
                    if counts[a] and mask>>a&1: ans[a]+=w*(L//n)
        return tuple(ans)
    def bi(h,counts):
        if len(h)==m: return h,values(counts)
        children=[]
        for a in range(k):
            c=list(counts);c[a]+=1
            z,p=bi(h+(a,),tuple(c))
            children.append((p[a],a,z,p))
        mx=max(q[0] for q in children)
        q=rng.choice([q for q in children if q[0]==mx])
        policy[h]=q[1]
        return q[2],q[3]
    z,p=bi((),(0,)*k)
    def finish(h):
        while len(h)<m: h=h+(policy[h],)
        c=tuple(h.count(a) for a in range(k))
        return h,values(c)
    supports=[]
    for ts in combinations_with_replacement(range(k),m):
        mask=sum(1<<a for a in set(ts))
        cover=sum(w for typ,w in weights.items() if typ&mask)
        supports.append((ts,cover))
    B=sum(1<<a for a in set(z));W=sum(w for typ,w in weights.items() if typ&B)
    results=[]
    for i in range(m):
        row=[finish(z[:i]+(a,))[1][a] for a in range(k)]
        best=max((cover*L-sum(row[a] for a in ts),ts,cover) for ts,cover in supports)
        results.append((best[0]-W*L,i,best,row))
    worst=max(results)
    return worst,dict(m=m,k=k,scale=L,weights=weights,seed=seed,actual=z,
                      actual_utility=[p[a] for a in z],W=W,
                      rows=results,policy={','.join(map(str,h)):a for h,a in policy.items()})

if __name__=='__main__':
    trials=int(sys.argv[1]) if len(sys.argv)>1 else 1000
    rng=random.Random(11011); best=None
    for t in range(trials):
        m,k=rng.choice([(3,5),(4,5),(4,6),(5,4),(5,5)])
        # Sparse mixtures deliberately retain private and overlapping clients.
        weights={mask:rng.randrange(1,20) for mask in range(1,1<<k) if rng.random()<0.25}
        if not weights: continue
        worst,data=run(m,k,weights,rng.randrange(1<<30))
        if best is None or worst[0]/data['scale']>best[0]:
            best=(worst[0]/data['scale'],t,data['W'],data['actual'],data['actual_utility'])
        if worst[0]>0:
            out=Path(__file__).with_name('netrow_counterexample_candidate.json')
            out.write_text(json.dumps(data,indent=2))
            print('COUNTEREXAMPLE',t,worst[:3],str(out),flush=True)
            break
        if (t+1)%100==0: print('tested',t+1,'best_gap',best,flush=True)
    else: print('NO_COUNTEREXAMPLE',trials,'best',best)
