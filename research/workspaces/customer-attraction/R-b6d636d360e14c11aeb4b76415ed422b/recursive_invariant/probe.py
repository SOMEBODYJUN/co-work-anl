from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations_with_replacement, product
from random import Random
import json


def solve(types, topics, b, r):
    @lru_cache(None)
    def util(q):
        out=[Q(0)]*topics
        for mask,n,p in types:
            d=p+sum(q[a] for a in range(topics) if mask>>a&1)
            if d:
                for a in range(topics):
                    if mask>>a&1 and q[a]: out[a]+=Q(n,d)
        return tuple(out)
    @lru_cache(None)
    def go(q):
        if sum(q)==r: return frozenset([q])
        children=[]
        for a in range(topics):
            z=list(q);z[a]+=1
            children.append(go(tuple(z)))
        floor=max(min(util(z)[a] for z in child) for a,child in enumerate(children))
        return frozenset(z for a,child in enumerate(children) for z in child if util(z)[a]>=floor)
    def profit(q):
        return sum((Q(n*sum(q[a] for a in range(topics) if mask>>a&1),p+sum(q[a] for a in range(topics) if mask>>a&1)) for mask,n,p in types if sum(q[a] for a in range(topics) if mask>>a&1)),Q(0))
    def f(k):
        return max(profit(tuple(c.count(a) for a in range(topics))) for c in combinations_with_replacement(range(topics),k))
    outcomes=go((0,)*topics)
    worst=min(outcomes,key=lambda q:profit(q))
    return f(r+1),profit(worst),worst,util(worst),len(outcomes)


def main():
    rng=Random(731)
    cases=0
    for topics,r,reps in [(4,2,500),(5,2,500),(4,3,400),(5,3,200),(4,4,100),(5,4,50)]:
        for it in range(reps):
            prefix=tuple(rng.randrange(topics) for _ in range(rng.randrange(4)))
            raw=[(mask,rng.randrange(9)) for mask in range(1,1<<topics)]
            types=[(mask,n,sum(mask>>a&1 for a in prefix)) for mask,n in raw if n]
            f,profit,worst,u,count=solve(types,topics,prefix,r)
            cases+=1
            if f>2*profit:
                print(json.dumps({'status':'counterexample','candidate':'F_(r+1)(b)<=2R_r(b)','topics':topics,'r':r,'iteration':it,'prefix':prefix,'types':types,'F_extra':str(f),'R':str(profit),'outcome':worst,'utilities':[str(x) for x in u],'outcomes':count,'cases':cases},indent=2))
                return
        print(json.dumps({'completed': [topics,r,reps], 'cases':cases}),flush=True)
    print(json.dumps({'status':'no counterexample in finite probes','cases':cases,'seed':731}))
if __name__=='__main__':main()
