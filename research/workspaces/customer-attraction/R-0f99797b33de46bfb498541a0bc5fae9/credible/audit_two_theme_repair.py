"""Exact, standard-library replay of a Cartesian root-only SPE repair.

All finite witnesses are complete ordered-history policies. The general
proof and scope are in two_theme_root_repair.md. No external packages.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def counts(h,p):
    return tuple(h.count(a) for a in range(p))

def two_outcomes(m,x,y):
    @lru_cache(None)
    def R(a,b):
        if a+b==m:return frozenset([a])
        child=[R(a+1,b),R(a,b+1)]
        floors=[min(F(x,k) for k in child[0]),min(F(y,m-k) for k in child[1])]
        ans=set()
        for z in child[0]:
            if F(x,z)>=floors[1]:ans.add(z)
        for z in child[1]:
            if F(y,m-z)>=floors[0]:ans.add(z)
        return frozenset(ans)
    return R

def expected_outcomes(m,x,y,a,b):
    t=F((m+1)*x,x+y)
    # ceil(t-1) = ceil(t)-1, including integral t.
    low=-((-t.numerator)//t.denominator)-1
    high=t.numerator//t.denominator
    clamp=lambda z:max(a,min(m-b,z))
    return frozenset([clamp(low),clamp(high)])

def insurance_action(h,m,mode):
    """h is the full insurance history, root already fixed.
    X=0,Y=1. The mode is selected separately at each joint root branch.
    """
    assert h
    if mode=='high':
        assert h[0]==0
        return 1
    assert mode=='low'
    if h[0]==0:
        return 0 if len(h)==1 else 1
    return 0 if 0 not in h else 1

def insurance_audit(m):
    x,y=2,m-1
    ans=[]
    for first,mode in [(0,'high'),(0,'low'),(1,'low')]:
        def action(h):return insurance_action(h,m,mode)
        def end(h):
            while len(h)<m:h=h+(action(h),)
            return h
        def u(z,a):return F(x,z.count(0)) if a==0 else F(y,z.count(1))
        slack=[]
        actions=[]
        for d in range(1,m):
            for tail in product(range(2),repeat=d-1):
                h=(first,)+tail;a=action(h);z=end(h)
                actions.append({'history':list(h),'action':a})
                for b in range(2):slack.append(u(z,a)-u(end(h+(b,)),b))
        assert min(slack,default=F(0))>=0
        z=end((first,))
        v=u(z,first)
        assert v==(2 if mode=='high' else 1)
        ans.append({'first':first,'mode':mode,'root_payoff':str(v),'path':list(z),
                    'ordered_nodes':len(actions),'comparisons':len(slack),'minimum_slack':str(min(slack,default=F(0)))})
    return ans

def product_witness(m):
    # Old topics A={one private client}, B={2m disjoint clients}.
    # All positive-depth histories follow exact deterministic BI; root forced A.
    base_mass=(1,2*m)
    def base_u(z,a):return F(base_mass[a],z.count(a))
    @lru_cache(None)
    def base_end(h):
        if len(h)==m:return h
        options=[base_end(h+(a,)) for a in range(2)]
        a=max(range(2),key=lambda a:(base_u(options[a],a),-a))
        return options[a]
    def base_action(h):return base_end(h)[len(h)]
    def base_term(h):
        if not h:h=(0,)
        return base_end(h)
    u=base_u(base_term(()),0)
    ds=[base_u(base_term((a,)),a) for a in range(2)]
    delta=max(ds)-u
    assert delta==1
    # Four joint themes (base,insurance), s=delta=1.
    labels=list(product(range(2),repeat=2))
    def act(h):
        if not h:return 0 # (A,X)
        root_base,root_ins=labels[h[0]]
        mode='high' if (root_base,root_ins)==(0,0) else 'low'
        bh=tuple(labels[a][0] for a in h)
        ih=tuple(labels[a][1] for a in h)
        return labels.index((base_action(bh),insurance_action(ih,m,mode)))
    def end(h):
        while len(h)<m:h=h+(act(h),)
        return h
    # Explicit unit-customer sets; four topics are distinct.
    customers=[{0,1}] # old A labels
    customers += [{2,3} for _ in range(2*m)] # old B
    customers += [{0,2} for _ in range(2)] # insurance X
    customers += [{1,3} for _ in range(m-1)] # insurance Y
    def welfare(z):return sum(bool(B.intersection(z)) for B in customers)
    def util(z,a):return sum((F(1,sum(b in B for b in z)) for B in customers if a in B),F(0))
    actions=[];slacks=[]
    for d in range(m):
        for h in product(range(4),repeat=d):
            a=act(h);z=end(h)
            actions.append({'history':list(h),'action':a})
            for b in range(4):slacks.append(util(z,a)-util(end(h+(b,)),b))
    assert min(slacks)>=0
    z=end(())
    opt=max(welfare(t) for t in product(range(4),repeat=m))
    assert welfare(z)==3*m+2==opt
    return {'schema':'explicit-ordered-history-pure-SPE-v1','m':m,'topics':labels,
            'unit_customer_interest':[sorted(B) for B in customers],
            'actions':actions,'root_path':list(z),'root_payoff':str(util(z,act(()))),
            'old_root_payoff':str(u),'old_root_deviation_payoffs':list(map(str,ds)),
            'delta':str(delta),'insurance_mass':m+1,'W':welfare(z),'OPT':opt,
            'comparisons':len(slacks),'minimum_slack':str(min(slacks))}

def main():
    state_tests=0;root_spread_tests=0
    # Exact set-valued BI, not a deterministic tie sample.
    for m in range(2,21):
        for x in range(1,21):
            for y in range(1,21):
                R=two_outcomes(m,x,y)
                for a in range(m+1):
                    for b in range(m+1-a):
                        assert R(a,b)==expected_outcomes(m,x,y,a,b),(m,x,y,a,b,R(a,b),expected_outcomes(m,x,y,a,b))
                        state_tests+=1
                vals=[F(x,k) for k in R(1,0)]
                spread=max(vals)-min(vals)
                assert spread<=F(x+y,m+1),(m,x,y,spread)
                root_spread_tests+=1
    witnesses=[]
    for m in range(2,6):
        z=product_witness(m);(HERE/f'two_theme_repair_m{m}_certificate.json').write_text(json.dumps(z,indent=2)+'\n')
        witnesses.append({k:v for k,v in z.items() if k not in ('actions','unit_customer_interest','topics')})
    report={'scope':'Finite exact implementation audit. General statements require the proof in two_theme_root_repair.md. No half-coverage counterexample claimed.',
            'exact_set_valued_BI_state_tests':state_tests,'root_spread_tests':root_spread_tests,
            'insurance_full_ordered_subtree_checks':{str(m):insurance_audit(m) for m in range(2,11)},
            'complete_product_SPE_witnesses':witnesses}
    (HERE/'two_theme_repair_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'state_tests':state_tests,'root_spread_tests':root_spread_tests,'product_witnesses':witnesses},indent=2))
if __name__=='__main__':main()
