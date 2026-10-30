"""Exact definition-level audit of the cyclic weighted-budget illustration."""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[6]
HERE=Path(__file__).resolve().parent


def kernel(P,weights,J):
    return sum((weights[j]/(1+sum(P[j][l] for l in J)) for j in J),F(0))


def subsets(m):
    return [tuple(j for j in range(m) if mask>>j&1) for mask in range(1,1<<m)]


def main():
    instance=json.loads((ROOT/'examples/customer_attraction/portfolio_matching_failure.json').read_text())
    certificate=json.loads((ROOT/'evidence/certificates/customer_attraction/portfolio_matching_failure.json').read_text())
    p=len(instance['topics']);m=instance['players'];assert m==2
    actions={tuple(v['history']):v['action'] for v in certificate['actions']}
    assert set(actions)=={h for depth in range(m) for h in product(range(p),repeat=depth)}
    customers=[(frozenset(t['topics']),t['multiplicity']) for t in instance['customers']]
    assert all(isinstance(n,int) and n>=0 for t,n in customers)
    def terminal(h):
        while len(h)<m:h=h+(actions[h],)
        return h
    def share(a,z,t):
        return F(1,sum(v in t for v in z)) if a in t else F(0)
    def utility(a,z):
        return sum((n*share(a,z,t) for t,n in customers),F(0))
    def welfare(z):
        return sum(n for t,n in customers if any(a in t for a in z))
    comparisons=0
    for h,a in actions.items():
        for b in range(p):
            assert utility(a,terminal(h))>=utility(b,terminal(h+(b,)))
            comparisons+=1
    z=terminal(());assert z==(4,0)
    W=welfare(z);payoffs=[utility(a,z) for a in z]
    optimum=max(welfare(pair) for pair in product(range(p),repeat=m))
    optimal_supports=[pair for pair in combinations_with_replacement(range(p),m) if welfare(pair)==optimum]
    assert W==44 and payoffs==[F(22),F(22)] and optimal_supports==[(1,3)]
    def partitioned(pi,t):
        eligible=[i for i,a in enumerate(pi) if a in t]
        if not eligible:return F(0)
        c=sum(a in t for a in z)
        return min(F(1,c+1-int(z[i] in t)) for i in eligible)
    matchings=[]
    for pi in ((1,3),(3,1)):
        branches=[terminal(z[:i]+(a,)) for i,a in enumerate(pi)]
        true_queries=[utility(a,b) for a,b in zip(pi,branches)]
        frozen=sum((n*partitioned(pi,t) for t,n in customers),F(0))
        matchings.append({'assignment':pi,'branches':branches,
                          'real_query_payoffs':[str(v) for v in true_queries],
                          'real_query_sum':str(sum(true_queries)),
                          'partitioned_frozen_R':str(frozen)})
    assert F(matchings[0]['partitioned_frozen_R'])==F(89,2)>W
    assert F(matchings[1]['partitioned_frozen_R'])==W
    P=((F(1),F(0)),(F(0),F(0)));weights=(F(2),F(1));pi=(1,3)
    branches=[terminal(z[:i]+(a,)) for i,a in enumerate(pi)]
    source_type_checks=[]
    for t,n in customers:
        J=tuple(j for j,a in enumerate(pi) if a in t)
        if not J:continue
        c=sum(a in t for a in z)
        for j in J:
            load=sum(a in t for a in branches[j])
            upper=c-int(z[j] in t)+1+sum(P[j][l] for l in J)
            assert load<=upper
        query=sum((weights[j]*share(pi[j],branches[j],t) for j in J),F(0))
        r=partitioned(pi,t)
        assert query>=r*kernel(P,weights,J)>=r
        source_type_checks.append({'topics':sorted(t),'multiplicity':n,
                                   'J':J,'R_coefficient':str(r),
                                   'weighted_real_query_coefficient':str(query)})
    kernels={str(J):str(kernel(P,weights,J)) for J in subsets(2)}
    assert min(F(v) for v in kernels.values())==1
    weighted_queries=sum(weights[j]*utility(pi[j],branches[j]) for j in range(2))
    weighted_budget=sum(weights[j]*payoffs[j] for j in range(2))
    assert weighted_queries==60 and weighted_budget==66 and weighted_budget==F(3,2)*W
    cyclic=((F(0),F(3)),(F(1,10),F(0)))
    cyclic_kernels={str(J):str(kernel(cyclic,(F(1),F(1)),J)) for J in subsets(2)}
    assert cyclic_kernels=={'(0,)':'1','(1,)':'1','(0, 1)':'51/44'}
    report={'status':'exact_definition_level_checks_passed','source_unit_customers':sum(n for t,n in customers),
            'source_complete_histories':len(actions),'source_comparisons_including_self':comparisons,
            'actual':z,'payoffs':[str(v) for v in payoffs],'W':W,'OPT':optimum,
            'unique_optimal_supports':optimal_supports,'matchings':matchings,
            'matrix':[[str(v) for v in row] for row in P],'weights':[str(v) for v in weights],
            'kernels':kernels,'weighted_real_queries':str(weighted_queries),'weighted_actual_budget':str(weighted_budget),
            'source_type_checks':source_type_checks,'cyclic_matrix_kernels':cyclic_kernels}
    (HERE/'audit_cyclic_budget.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='source_type_checks'},indent=2))

if __name__=='__main__':main()
