"""Construct and exactly audit selected members of the padded kernel boundary.

BI supplies unspecified off-path subgames. The subsequent definition-level
audit checks every ordered history and never calls the outcome solver.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product,combinations
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[6]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver


def construct(m):
    base=Instance.from_dict(json.loads((ROOT/'examples/customer_attraction/portfolio_matching_failure.json').read_text()))
    aux=tuple(range(5,m+3));p=m+3
    ins=Instance(base.topics+tuple(f'Z{i+1}' for i in range(m-2)),
                 base.customers+tuple(CustomerType(frozenset({a}),22) for a in aux),m)
    solver=ExactSPESolver(ins);actions={};actual=aux+(4,0)
    def increment(q,a):return tuple(v+int(i==a) for i,v in enumerate(q))
    def default(h,desired=None):
        if len(h)==m:return
        q=ins.counts(h)
        if desired is None:desired=min(solver.outcomes(q))
        floor=solver.threshold(q)
        a=min(a for a in range(p) if desired in solver.outcomes(increment(q,a))
              and ins.topic_payoff(a,desired)>=floor)
        actions[h]=a
        for b in range(p):
            child=increment(q,b)
            target=desired if b==a else min(solver.outcomes(child),key=lambda z:(ins.topic_payoff(b,z),z))
            default(h+(b,),target)
    def punishment(h,S):
        unused=tuple(a for a in aux if a not in h)
        response={0:1,1:2,2:1,3:2,4:0}[S]
        return ((response,)+unused) if S in (0,3) else (unused+(response,))
    def forced(h,remaining,kind):
        if len(h)==m:
            assert not remaining;return
        assert remaining
        a=remaining[0];actions[h]=a
        for b in range(p):
            child=h+(b,)
            if b==a:forced(child,remaining[1:],kind)
            elif kind=='actual' and all(t in aux for t in h) and b<5:
                plan=punishment(h,b)
                assert len(plan)==m-len(child)
                forced(child,plan,'myopic')
            else:default(child)
    forced((),actual,'actual')
    return ins,actions,actual


def audit(ins,actions,actual):
    p,m=ins.topic_count,ins.players
    assert set(actions)=={h for d in range(m) for h in product(range(p),repeat=d)}
    customers=[(t.topics,t.multiplicity) for t in ins.customers]
    @lru_cache(None)
    def terminal(h):
        return h if len(h)==m else terminal(h+(actions[h],))
    @lru_cache(None)
    def counts(z):return tuple(z.count(a) for a in range(p))
    @lru_cache(None)
    def utility(a,q):
        return sum((F(n,sum(q[t] for t in interest)) for interest,n in customers if a in interest),F(0))
    checked=0
    for h,a in actions.items():
        u=utility(a,counts(terminal(h)))
        for b in range(p):
            assert u>=utility(b,counts(terminal(h+(b,)))),(h,a,b)
            checked+=1
    assert terminal(())==actual
    q=counts(actual);payoffs=[utility(a,q) for a in actual]
    assert payoffs==[F(22)]*m
    def coverage(support):return sum(n for t,n in customers if any(a in t for a in support))
    W=coverage(actual);assert W==22*m
    target=tuple(range(5,m+3))+(1,3)
    opt=max(coverage(s) for size in range(1,m+1) for s in combinations(range(p),size))
    supports=[s for size in range(1,m+1) for s in combinations(range(p),size) if coverage(s)==opt]
    assert opt==22*m+1 and supports==[tuple(sorted(target))]
    load_witnesses=[]
    for i in range(m):
        for S,interest in ((1,frozenset({1,2})),(3,frozenset({2,3}))):
            b=terminal(actual[:i]+(S,))
            load=sum(a in interest for a in b)
            assert load==(1 if i==m-1 else 2)
            load_witnesses.append({'actual_node':list(actual[:i]),'query':S,'witness_interest':sorted(interest),
                                   'terminal':b,'load':load})
    # Upper witness: match each auxiliary to itself, then B to E and D to A.
    assignment=target;diagonal=[F(0)]*(m-2)+[F(1),F(0)];weights=[1]*(m-2)+[2,1]
    branches=[terminal(actual[:i]+(a,)) for i,a in enumerate(assignment)]
    for interest,n in customers:
        J=[j for j,a in enumerate(assignment) if a in interest]
        if not J:continue
        assert len(J)==1 # the chosen optimum topics are disjoint
        j=J[0];c=sum(a in interest for a in actual)
        d=sum(a in interest for a in branches[j])
        assert d<=c-int(actual[j] in interest)+1+diagonal[j]
        assert F(weights[j],1+diagonal[j])>=1
    assert sum(F(w)*u for w,u in zip(weights,payoffs))==22*(m+1)
    return {'players':m,'topics':p,'W':W,'OPT':opt,'actual':actual,
            'histories':len(actions),'comparisons_including_self':checked,
            'all_actual_payoffs':'22','unique_optimal_support':supports[0],
            'kernel_budget_lower_bound':22*(m+1),'attained_kernel_budget':22*(m+1),
            'on_path_old_query_load_witnesses':load_witnesses,
            'upper_witness_assignment':assignment,'upper_witness_weights':weights,
            'instance':ins.to_dict(),'certificate':{'terminal_counts':q,'actions':[
                {'history':h,'action':a} for h,a in sorted(actions.items(),key=lambda z:(len(z[0]),z[0]))]}}


def main():
    results=[]
    for m in range(2,6):
        ins,actions,actual=construct(m);record=audit(ins,actions,actual);results.append(record)
        print(json.dumps({k:v for k,v in record.items() if k not in {'instance','certificate','on_path_old_query_load_witnesses'}}),flush=True)
    out={'status':'finite_complete_strategy_members_verified_exactly',
         'general_claim':'analytic all-m construction is proved separately in padding_kernel_boundary.md',
         'members':results}
    (HERE/'padding_kernel_boundary.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
