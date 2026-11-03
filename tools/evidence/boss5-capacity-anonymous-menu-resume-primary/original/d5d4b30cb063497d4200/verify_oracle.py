"""Definition-level oracle audit. Exhaust all complete policies, not outcomes.

These are implementation checks for the AFC falsification oracle, not new
fixed-player research or positive evidence for the general conjecture.
"""
from fractions import Fraction as F
from itertools import product
import json
import numpy as np
from full_menu import Attack, FullMenu

def brute(m,k,w,p):
    histories=[h for n in range(m) for h in product(range(k),repeat=n)]
    sig=[tuple(a for a in range(k) if b>>a&1) for b in range(1,1<<k)]
    def utility(a,end):
        return sum((F(n,sum(b in s for b in end)) for s,n in zip(sig,w) if a in s),F(0))
    def query(bg):
        return sum((p[a]*sum((F(n,1+sum(b in s for b in bg)) for s,n in zip(sig,w) if a in s),F(0)) for a in range(k)),F(0))
    best=None;eqs=0
    for choices in product(range(k),repeat=len(histories)):
        pi=dict(zip(histories,choices))
        def end(h):
            while len(h)<m:h=h+(pi[h],)
            return h
        ok=True
        for h,a in pi.items():
            actual=utility(a,end(h+(a,)))
            if any(utility(b,end(h+(b,)))>actual for b in range(k)):
                ok=False;break
        if not ok:continue
        eqs+=1;B=end(())
        W=sum(n for s,n in zip(sig,w) if any(b in s for b in B))
        lhs=sum((min(query(end(B[:i]+(a,))[:i]+end(B[:i]+(a,))[i+1:]) for a in range(k)) for i in range(m)),F(0))
        gap=lhs-W
        if best is None or gap>best:best=gap
    assert best is not None
    return best,eqs,k**len(histories)

def run():
    cases=[
        ('generic',3,2,[3,4,2],[F(1,3),F(2,3)]),
        ('disjoint_ties',3,2,[3,3,0],[F(1,2),F(1,2)]),
        ('empty_theme',3,2,[4,0,0],[F(1,3),F(2,3)]),
        ('identical_coverages',3,2,[0,0,5],[F(1,3),F(2,3)]),
        ('zero_customers',3,2,[0,0,0],[F(1,3),F(2,3)]),
        ('one_empty_theme',3,1,[0],[F(1)]),
        ('one_player_zero',1,2,[0,0,0],[F(1,3),F(2,3)]),
    ]
    for name,m,k,w,p in cases:
        exact,eqs,total=brute(m,k,w,p)
        o=Attack(m,k,np.random.default_rng(0));oracle=FullMenu(o,w)
        result=oracle.best(p,exact=True)
        assert exact==result[0],(name,exact,result)
        ic,menus,cover,pi=oracle.materialize(result)
        if len(ic):assert np.max(ic@np.array(w))<1e-9
        # Check the one materialized complete policy through the original model
        # in exact rational arithmetic, independently of the envelope routine.
        from customer_attraction.model import Instance,CustomerType
        inst=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if b>>a&1),n) for b,n in enumerate(w,1) if n),m)
        def end(h):
            while len(h)<m:h=h+(pi[h],)
            return h
        for h,a in pi.items():
            actual=inst.topic_payoff(a,inst.counts(end(h),terminal=True))
            for b in range(k):assert actual>=inst.topic_payoff(b,inst.counts(end(h+(b,)),terminal=True))
        print(json.dumps({'case':name,'complete_policies':total,'SPEs':eqs,'exact_max_gap':str(exact),'oracle_gap':str(result[0]),'match':True}))

if __name__=='__main__':run()
