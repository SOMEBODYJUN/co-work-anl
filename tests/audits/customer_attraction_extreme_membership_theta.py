"""Scoped exact regression; the all-instance theorem is in the written proof.

Default output is stdout. --output saves a new report and refuses overwrite.
Seeded finite cases use a strict set-valued catalog, including empty actions.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
import argparse
import json
import random
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, ExactSPESolver


def delta(n,b,I,K):
    return F(n*I-K,n*(b+I+K)) if I or K else F(0)


def run():
    scalar_checks=0
    for n in range(1,11):
        for b in range(7):
            for transfer in range(n+1):
                for K in range(transfer+1):
                    assert delta(n,b,0,K)>=-F(transfer,n*(b+1))
                    scalar_checks+=1
                for K in range(n-transfer+1):
                    assert delta(n,b,1,K)>=F(transfer,n*(b+n))
                    h=n-transfer-K
                    assert (n-K)*(b+n)-transfer*(b+1+K)==transfer*(transfer-1)+h*(b+n+transfer)
                    scalar_checks+=2
            for K in range(n+1):
                assert delta(n,b,1,K)>=0
                assert delta(n,b,0,K)>=-F(1,b+n)
                scalar_checks+=2
    profit_checks=0
    for b in range(7):
        for c in range(1,11):
            for d in range(11):
                gap=F(c+d,b+d+1)-F(c,b+c)
                assert gap==F(c*(c-1)+b*d,(b+d+1)*(b+c))>=0
                profit_checks+=1
    rng=random.Random(80915)
    specs=[([set()],[],1),([set(),{0}],[],1),([set(),{0}], [0],2)]
    for case in range(10):
        k=3 if case<4 else 4
        maxima=[{j} for j in range(k)]
        for x in range(k,k+7):
            typ=rng.randrange(3)
            J=({rng.randrange(k)} if typ==0 else set(range(k))-{rng.randrange(k)} if typ==1 else set(range(k)))
            for j in J:maxima[j].add(x)
        subsets=[{x for x in maxima[rng.randrange(k)] if rng.randrange(2)} for _ in range(2)]
        topics=list(dict.fromkeys(map(frozenset,maxima+subsets)))
        prefix=[rng.randrange(len(topics)) for _ in range(case%3)]
        specs.append((topics,prefix,3+case%2))
    cases=[]
    for case,(topics,prefix,r) in enumerate(specs):
        topics=list(dict.fromkeys(map(frozenset,topics)))
        maxima=[A for A in topics if not any(A<B for B in topics)]
        k=len(maxima)
        assert k>=1
        for x in set().union(*maxima):
            assert sum(x in A for A in maxima) in {1,k-1,k}
        inst=Instance.from_topic_sets(topics,len(prefix)+r)
        solver=ExactSPESolver(inst)
        counts=inst.counts(prefix)
        floor=solver.threshold(counts)
        def query(a,B):
            return sum((F(c.multiplicity,1+sum(counts[j] for j in c.topics)+sum(t in c.topics for t in B)) for c in inst.customers if a in c.topics),F(0))
        theta=min(max(query(a,B) for a in range(inst.topic_count)) for B in combinations_with_replacement(range(inst.topic_count),r-1))
        assert floor>=theta
        def profit(terminal):
            result=F(0)
            for c in inst.customers:
                old=sum(counts[j] for j in c.topics)
                new=sum(terminal[j]-counts[j] for j in c.topics)
                if new:result+=F(c.multiplicity*new,old+new)
            return result
        outcomes=solver.outcomes(counts)
        minimum_profit=min(map(profit,outcomes))
        assert minimum_profit>=r*theta
        possible=[]
        for B in combinations_with_replacement(range(inst.topic_count),r):
            t=list(counts)
            for a in B:t[a]+=1
            possible.append(tuple(t))
        F_opt=max(map(profit,possible))
        assert F_opt<=(2*r-1)*theta
        cases.append({'case':case,'instance':inst.to_dict(),'prefix':prefix,'remaining':r,'maximal_topics':k,
                      'first_floor':str(floor),'theta':str(theta),'SPE_outcomes':len(outcomes),
                      'minimum_SPE_profit':str(minimum_profit),'optimal_profit':str(F_opt),
                      'count_states':solver.stats.count_states})
    # A non-laminar, non-sunflower allowed class with arbitrarily many maxima.
    k=7
    maxima=[frozenset({j}|{k+h for h in range(k) if h!=j}) for j in range(k)]
    assert all(not A<B for A in maxima for B in maxima)
    memberships=[sum(x in A for A in maxima) for x in range(2*k)]
    assert memberships==[1]*k+[k-1]*k
    partial=[delta(2,0,int(i<2),1) for i in range(4)]
    assert sum(partial,F(0))/4==-F(1,8)
    return {'scope':'Exact scalar identities and finite all-SPE regressions only; general proof is analytical.',
            'seed':80915,'strict_set_catalog':True,'scalar_checks':scalar_checks,'profit_checks':profit_checks,
            'cases':cases,'seven_maxima_range_witness':{'membership_sizes':memberships,'maxima':[sorted(A) for A in maxima]},
            'middle_incidence_menu_only':{'delta':list(map(str,partial)),'uniform_average':'-1/8','SPE_certified':False}}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    report=run()
    encoded=json.dumps(report,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x') as stream:stream.write(encoded)
        print(json.dumps({'output':str(args.output),'scalar_checks':report['scalar_checks'],
                          'profit_checks':report['profit_checks'],'cases':len(report['cases'])}))
    else:print(encoded,end='')
