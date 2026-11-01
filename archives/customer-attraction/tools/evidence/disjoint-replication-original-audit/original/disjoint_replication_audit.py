"""Definition-level Fraction audit of the explicit replicated-gadget dual.
No SPE solver, cone optimizer, floating arithmetic, or generator is imported.
"""
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement,product
import json

def customers(K):
    clients=[]
    for j in range(K):
        X=range(6*j,6*j+3);Y=range(6*j+3,6*j+6)
        clients.extend(frozenset((x,y)) for x in X for y in Y)
        for xx in combinations(X,2):
            for yy in combinations(Y,2):clients.extend([frozenset(xx+yy)]*3)
    assert len(clients)==36*K
    return clients

def payoff(clients,a,B):
    return sum((F(1,1+sum(b in C for b in B)) for C in clients if a in C),F(0))

reports=[]
for K in range(1,6):
    clients=customers(K);Q={}
    for special in range(K):
        options=[]
        for j in range(K):
            G=[tuple(range(6*j,6*j+3)),tuple(range(6*j+3,6*j+6))]
            options.append([p for g in G for p in combinations(g,2)] if j==special else G)
        for pieces in product(*options):
            B=tuple(sorted(x for piece in pieces for x in piece));assert len(B)==3*K-1
            Q[B]=Q.get(B,F(0))+F(1,K*6*2**(K-1))
    assert sum(Q.values())==1
    values=[sum(prob*payoff(clients,a,B) for B,prob in Q.items()) for a in range(6*K)]
    bound=F(15,2)+F(5,2*K);assert values==[bound]*(6*K)
    report=dict(copies=K,unit_customers=len(clients),background_support=len(Q),actions_per_background=3*K-1,pure_query_cap=str(bound),serial_34_coverage_slack=str(34*K-3*K*bound))
    if K==2:
        backgrounds=list(combinations_with_replacement(range(12),5));assert len(backgrounds)==4368
        uniform_min=min(sum((payoff(clients,a,B) for a in range(12)),F(0))/12 for B in backgrounds)
        assert uniform_min==bound==F(35,4)
        report['all_static_backgrounds']=len(backgrounds);report['uniform_query_exact_lower']=str(uniform_min)
    reports.append(report)
print(json.dumps(dict(status='exact definition-level audit passed',reports=reports),indent=2))
