"""Target the general local-common-reset candidate Lambda<=1 from ell>=0.

Random exact finite counterexample search. No positive claim is inferred from
failure to find one. Integer utilities use lcm(1,...,m), hence comparisons exact.
Positive fresh edges are only necessary seeds for a common-reset density
counterexample, not the research target or a new positive fixed-size result.
"""
from fractions import Fraction as F
from itertools import product
from math import lcm
from pathlib import Path
import json, random

rng=random.Random(240244)
m,k=4,5
den=lcm(*range(1,m+1))
def game(weights):
    strategy={}
    utilities={}
    def utility(z,i):
        key=(tuple(sorted(z)),z[i])
        if key not in utilities:
            utilities[key]=sum(w*den//sum(bool(mask&(1<<a)) for a in z)
                               for mask,w in enumerate(weights)
                               if w and mask&(1<<z[i]))
        return utilities[key]
    def solve(h):
        i=len(h)
        if i==m:return h
        leaves=[solve(h+(a,)) for a in range(k)]
        vals=[utility(z,i) for z in leaves]
        choices=[a for a,v in enumerate(vals) if v==max(vals)]
        a=rng.choice(choices);strategy[h]=a
        return leaves[a]
    Z=solve(())
    def finish(h):
        while len(h)<m:h+=(strategy[h],)
        return h
    fresh=[mask for mask,w in enumerate(weights)
           if w and all(not mask&(1<<a) for a in Z)]
    if not fresh:return None
    for i in range(m):
        for g in product(range(k),repeat=i):
            B=finish(g);A=finish(Z[:i]+(B[i],))
            for j in range(i+1,m):
                q=sum((F(weights[mask],sum(bool(mask&(1<<a)) for a in A)*
                         sum(bool(mask&(1<<a)) for a in B))
                       for mask in fresh if mask&(1<<B[i]) and mask&(1<<A[j])
                       and not mask&(1<<B[j])),F())
                if q:
                    return {'players':m,'topics':k,'weights':weights,
                            'strategy':[{'history':list(h),'action':a}
                                        for h,a in sorted(strategy.items())],
                            'actual':Z,'context':g,'i':i,'j':j,'B':B,'A':A,
                            'q':str(q)}
    return None

for trial in range(20000):
    weights=[0]+[rng.randrange(0,31) for _ in range((1<<k)-1)]
    result=game(weights)
    if result:
        result['trial']=trial
        out=Path(__file__).with_name('positive_fresh_candidate.json')
        out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result));break
else:print('No counterexample found; no general conclusion.')
