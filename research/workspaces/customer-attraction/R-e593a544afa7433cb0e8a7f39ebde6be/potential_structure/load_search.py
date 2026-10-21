"""Finite attacks on a proposed refined load bound; not a general theorem."""
import argparse, functools, itertools, json, math, random, time
from fractions import Fraction


def solve(types, p, m):
    scale=math.lcm(*range(1,m+1))
    @functools.lru_cache(None)
    def util(c):
        z=[0]*p
        for B,n in types:
            d=sum(c[a] for a in B)
            if d:
                for a in B:
                    if c[a]: z[a]+=n*(scale//d)
        return tuple(z)
    @functools.lru_cache(None)
    def E(c):
        if sum(c)==m:return frozenset([c])
        children=[E(c[:a]+(c[a]+1,)+c[a+1:]) for a in range(p)]
        threshold=max(min(util(t)[a] for t in child) for a,child in enumerate(children))
        return frozenset(t for a,child in enumerate(children) for t in child if util(t)[a]>=threshold)
    def coverage(c):
        return sum(n for B,n in types if sum(c[a] for a in B))
    opt=max(coverage(tuple(int(a in S) for a in range(p))) for k in range(min(p,m)+1) for S in itertools.combinations(range(p),k))
    outcomes=E((0,)*p)
    best=None
    for c in outcomes:
        load={}
        for B,n in types:
            d=sum(c[a] for a in B)
            if d: load[d]=load.get(d,0)+n
        proxy=sum(n*max(Fraction(3,2),2-Fraction(1,d)) for d,n in load.items())
        gap=proxy-opt
        if best is None or gap<best[0]:best=(gap,c,load,coverage(c),proxy,opt)
    return best


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=500);ap.add_argument('--seed',type=int,default=8901);ap.add_argument('--p',type=int,default=5);ap.add_argument('--m',type=int,default=5);ap.add_argument('--json',default=None);args=ap.parse_args()
    rng=random.Random(args.seed);start=time.time();record=None
    for trial in range(args.trials):
        p=args.p;m=args.m
        types=[]
        for mask in range(1,1<<p):
            if rng.random()<rng.choice([.1,.2,.4,.7]):
                types.append((tuple(a for a in range(p) if mask>>a&1),rng.randint(1,5)))
        if not types:continue
        result=solve(types,p,m)
        gap,c,load,w,proxy,opt=result
        if record is None or float(gap)/max(1,opt)<record['normalized_gap']:
            record=dict(trial=trial,types=types,p=p,m=m,gap=str(gap),normalized_gap=float(gap)/max(1,opt),counts=c,load=load,W=w,proxy=str(proxy),OPT=opt)
            print(json.dumps(record),flush=True)
        if gap<0:break
    report=dict(seed=args.seed,trials_attempted=trial+1,elapsed=time.time()-start,best=record)
    if args.json:
        with open(args.json,'x') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True)
if __name__=='__main__':main()
