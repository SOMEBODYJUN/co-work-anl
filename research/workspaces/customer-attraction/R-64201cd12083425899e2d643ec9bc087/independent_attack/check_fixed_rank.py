"""Independent exact state-machine audit for the arbitrary fixed-rank cutoff.

No import from the author, repository model, or equilibrium solver.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import lcm,comb
import json

def audit(m,cutoff):
    grouping=2**cutoff
    largest=(m+grouping-1)//grouping
    L=lcm(*range(1,largest+1))
    sizes=tuple(L//((m-i+grouping-1)//grouping) for i in range(m))+(L,)*m
    @lru_cache(None)
    def parse(history):
        rank=0; schedule=tuple(range(m)); previous=None
        for pos,action in enumerate(history):
            expected=schedule[pos] if rank<=cutoff else previous
            if action!=expected:
                rank+=1
                if rank<=cutoff:
                    scale=2**(cutoff-rank)
                    remaining=m-pos; prior=history[:pos].count(action)
                    denominator=L//sizes[action]
                    finalcount=max(prior+1,(remaining+prior+1)//(scale*denominator+1))
                    schedule=history[:pos]+(action,)*(finalcount-prior)
                    fresh=tuple(b for b in range(m,2*m) if b not in schedule)
                    schedule=(schedule+fresh)[:m]
                    assert len(schedule)==m
            previous=action
        return rank,(schedule[len(history)] if rank<=cutoff else previous)
    @lru_cache(None)
    def finish(history):
        if len(history)==m:return history
        return finish(history+(parse(history)[1],))
    def payoff(history,pos):
        outcome=finish(history); action=outcome[pos]
        return F(sizes[action],outcome.count(action))
    layer=[()]; histories=0; rows=0; minimum=None; byrank=[0]*(cutoff+1)
    for depth in range(m):
        following=[]
        for history in layer:
            rank,action=parse(history)
            assert rank<=cutoff
            byrank[rank]+=1; histories+=1
            value=payoff(history,depth)
            for alternative in range(2*m):
                changed=history+(alternative,)
                slack=value-payoff(changed,depth)
                assert slack>=0,(m,cutoff,history,alternative,value,slack)
                rows+=1
                minimum=slack if minimum is None else min(minimum,slack)
                if depth+1<m and rank+(alternative!=action)<=cutoff:following.append(changed)
        layer=following
    expected=sum((2*m-1)**j*comb(m,j+1) for j in range(min(cutoff,m-1)+1))
    assert histories==expected
    root=finish(()); assert root==tuple(range(m))
    W=sum(sizes[:m]); O=m*L
    assert F(O,W)==F(m)/sum((F(1,(r+grouping-1)//grouping) for r in range(1,m+1)),F())
    parse.cache_clear();finish.cache_clear()
    return {'m':m,'cutoff':cutoff,'histories':histories,'rows':rows,'by_rank':byrank,'minimum_slack':str(minimum),'W':W,'OPT':O,'ratio':str(F(O,W))}

lemma_cases=0
for r in range(1,101):
    for a in (1,2,4,8,16,32):
        for d in range(1,51):
            for p in (0,1,2,3,10,101):
                q=max(p+1,(r+p+1)//(a*d+1))
                assert d*q >= (r+2*a-1)//(2*a)
                assert 0<=q-p-1<=r-1
                if q>p+1:
                    s=r-q+p+1
                    assert a*d*q<=s
                lemma_cases+=1

cases=[audit(9,1),audit(9,2),audit(5,3),audit(5,0)]
print(json.dumps({'status':'passed; restricted formal policies only, not SPE','integer_lemma_cases':lemma_cases,'audits':cases},indent=2))
