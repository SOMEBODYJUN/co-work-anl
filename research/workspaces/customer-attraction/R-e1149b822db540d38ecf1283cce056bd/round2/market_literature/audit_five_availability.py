"""Standalone exact full ordered-history audit of the five-player example.

No imports from discovery, repository verifiers, LP solvers, or old certificates.
Integer utility is scaled by lcm(1,...,5)=60. Multiplicities are numbers of
different unit customers; all providers have unit weight.
"""
from collections import Counter
from functools import lru_cache
from itertools import product
from fractions import Fraction
from math import comb
from pathlib import Path
import json

TYPE={(0,2):37,(1,2):24,(1,3):3,(2,0):37,(2,1):24,
      (2,4):5,(2,5):24,(3,1):3,(4,2):5,(4,4):61,(5,2):24}
WEIGHT={b:TYPE.get(((b&31).bit_count(),(b>>5).bit_count()),0)
        for b in range(1,1024)}
WEIGHT={b:w for b,w in WEIGHT.items() if w}
L=60

def choose(h):
    if not h:return 0
    group=1-h[0]//5 if len(h)==1 else h[1]//5
    return next(a for a in range(5*group,5*group+5) if a not in h)

def finish(h):
    h=tuple(h)
    while len(h)<5:h+=choose(h),
    return h

@lru_cache(None)
def utility(q,a):
    ans=0
    for mask,w in WEIGHT.items():
        if mask>>a&1:
            load=sum(q[b] for b in range(10) if mask>>b&1)
            assert load>0 and L%load==0
            ans+=w*(L//load)
    return ans

def util_path(path,a):
    return utility(tuple(path.count(b) for b in range(10)),a)

def welfare(path):
    mask=sum(1<<a for a in set(path))
    return sum(w for b,w in WEIGHT.items() if b&mask)

def frac(x):return str(Fraction(x,L))

def compositions(total,width):
    if width==1:
        yield (total,)
    else:
        for v in range(total+1):
            for tail in compositions(total-v,width-1):yield (v,)+tail

def misery_defects():
    out={}
    for j in range(2,6):
        best=0;witness=None
        for q in compositions(j-1,10):
            for b in range(10):
                qq=list(q);qq[b]+=1;qq=tuple(qq)
                entrant=utility(qq,b)
                for a in range(10):
                    if not q[a]:continue
                    before=utility(q,a);after=utility(qq,a)
                    if before>after and entrant-after>best:
                        best=entrant-after;witness={'prefix_counts':q,'earlier_topic':a,'entrant_topic':b,'earlier_before':frac(before),'earlier_after':frac(after),'entrant':frac(entrant)}
        out[str(j)]={'epsilon':frac(best),'witness':witness}
    return out

def main():
    comparisons=0;histories=0;minslack=None;ties=0
    by_depth={}
    for depth in range(5):
        dmin=None
        for h in product(range(10),repeat=depth):
            a=choose(h);path=finish(h);actual=util_path(path,a)
            histories+=1
            for b in range(10):
                other=util_path(finish(h+(b,)),b)
                slack=actual-other
                assert slack>=0,(h,a,b,actual,other)
                comparisons+=1;ties+=slack==0
                minslack=slack if minslack is None else min(minslack,slack)
                dmin=slack if dmin is None else min(dmin,slack)
        by_depth[str(depth)]=frac(dmin)
    # Direct last-node definition over all 10^4 *ordered* prefixes.
    terminal_values=[max(util_path(h+(a,),a) for a in range(10))
                     for h in product(range(10),repeat=4)]
    theta=min(terminal_values)
    actual=finish(());payoffs=[util_path(actual,a) for a in actual]
    W=welfare(actual)
    assert sum(payoffs)==L*W
    assert theta==1115*L and payoffs==[1107*L]+[1115*L]*4
    assert W==5567<5*theta//L
    # Enumerate every possible ordered five-topic tuple for optimum coverage.
    optimal=max(welfare(t) for t in product(range(10),repeat=5))
    best=next(t for t in product(range(10),repeat=5) if welfare(t)==optimal)
    n=sum(WEIGHT.values())
    topicsizes=[sum(w for b,w in WEIGHT.items() if b>>a&1) for a in range(10)]
    assert len(set(topicsizes))==1
    defects=misery_defects()
    out={'status':'exact_complete_history_SPE; not a half-coverage counterexample',
         'providers':5,'topic_count':10,'unit_customer_count':n,
         'positive_customer_type_count':len(WEIGHT),'topic_sizes':topicsizes,
         'actual_path':actual,'payoffs':list(map(frac,payoffs)),'W':W,
         'theta5':frac(theta),'W_minus_5theta':str(Fraction(L*W-5*theta,L)),
         'OPT5':optimal,'optimal_path':best,'two_W_minus_OPT5':2*W-optimal,
         'ordered_decision_histories':histories,'IC_comparisons':comparisons,
         'IC_ties_including_self':ties,'min_scaled_IC_slack':minslack,
         'last_node_histories':len(terminal_values),'per_depth_min_slack':by_depth,
         'shared_misery_defects':defects,
         'type_orbits':{f'{i},{j}':w for (i,j),w in TYPE.items()},
         'utility_cache_entries':utility.cache_info().currsize}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
