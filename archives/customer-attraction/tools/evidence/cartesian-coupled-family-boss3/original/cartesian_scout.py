"""Exact marginal-state solver for Cartesian products of disjoint resource menus.
Finite diagnosis of a uniform composition mechanism; not a general theorem.
"""
from functools import lru_cache
from itertools import product
from math import lcm
from fractions import Fraction
import random, json, argparse

def solve(weights,m, expose=False):
    dims=tuple(map(len,weights)); actions=tuple(product(*map(range,dims)))
    scale=lcm(*range(1,m+1)); weights=tuple(tuple(w) for w in weights)
    @lru_cache(None)
    def payoff(q,a):
        return sum(weights[j][a[j]]*(scale//q[j][a[j]]) for j in range(len(dims)))
    @lru_cache(None)
    def rec(k):
        if sum(k[0])==m:return frozenset((k,))
        children=[]; threshold=0
        for a in actions:
            child=tuple(tuple(c+(r==a[j]) for r,c in enumerate(k[j])) for j in range(len(dims)))
            R=rec(child); floor=min(payoff(q,a) for q in R)
            threshold=max(threshold,floor);children.append((a,R))
        return frozenset(q for a,R in children for q in R if payoff(q,a)>=threshold)
    root=rec(tuple((0,)*d for d in dims))
    def welfare(q):return sum(v for ws,qs in zip(weights,q) for v,c in zip(ws,qs) if c)
    best=min(root,key=lambda q:(welfare(q),q));W=welfare(best)
    OPT=sum(sum(sorted(w,reverse=True)[:m]) for w in weights)
    report={'weights':weights,'m':m,'W':W,'OPT':OPT,'ratio':str(Fraction(OPT,W)),'target':best,'root_outcomes':len(root),'states':rec.cache_info().currsize}
    if expose:return report,root,rec,payoff,actions
    return report,root

def main():
    p=argparse.ArgumentParser();p.add_argument('--m',type=int,default=4);p.add_argument('--trials',type=int,default=50);p.add_argument('--seed',type=int,default=132);p.add_argument('--dims',type=int,nargs='+',default=[3,3]);args=p.parse_args()
    rng=random.Random(args.seed);best=Fraction(0)
    for i in range(args.trials):
        weights=tuple(tuple(rng.randint(1,12) for _ in range(d)) for d in args.dims)
        report,_=solve(weights,args.m)
        factor=[solve((w,),args.m)[0] for w in weights];base=sum(x['W'] for x in factor)
        report['component_minimum_sum']=base;report['amplifies']=report['W']<base
        ratio=Fraction(report['ratio'])
        if report['amplifies'] or ratio>best:
            print(json.dumps({'trial':i,**report}),flush=True);best=max(best,ratio)
        if report['amplifies']:break
if __name__=='__main__':main()
