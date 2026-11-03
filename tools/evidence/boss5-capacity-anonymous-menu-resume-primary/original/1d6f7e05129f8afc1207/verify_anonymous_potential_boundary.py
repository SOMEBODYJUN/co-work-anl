"""Exact definition-level audit of the anonymous-potential method boundary.

This is NOT a customer-attraction game or a counterexample to Q-CAG-HALF.
No project model or solver is imported.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json

K=22
A=range(K)

def adjacent(a,b):
    return (a-b)%K in (1,K-1)

def f3(z):
    return F(0 if any(adjacent(a,b) for a,b in combinations_with_replacement(z,2)) else 11)

def f2(v):
    a,b=v
    if a==b:return F(10)
    if adjacent(a,b):return F(-1)
    return sum((f3((a,b,t)) for t in A),F(0))/K

def phi(z):
    if len(z)<2:return F(0)
    if len(z)==2:return f2(z)+11
    if len(z)==3:return f3(z)+22
    raise ValueError(z)

def utility(z,i):
    return phi(z)-phi(z[:i]+z[i+1:])

def policy(h):
    if len(h)==0:return 0
    if len(h)==1:return (h[0]+1)%K
    a,b=h
    return b if adjacent(a,b) else a

def terminal(h):
    while len(h)<3:h=h+(policy(h),)
    return h

def query(v):
    return sum((phi(v+(t,))-phi(v) for t in A),F(0))/K

def run():
    checked_histories=checked_comparisons=0
    for depth in range(3):
        for h in product(A,repeat=depth):
            selected=utility(terminal(h),depth)
            for a in A:
                assert selected>=utility(terminal(h+(a,)),depth),(h,a)
                checked_comparisons+=1
            checked_histories+=1
    terminals=list(product(A,repeat=3))
    assert min(utility(z,i) for z in terminals for i in range(3))==1
    assert all(phi(z)>=phi(z[:i]+z[i+1:]) for z in terminals for i in range(3))
    pairs=list(combinations_with_replacement(A,2))
    assert all(phi(v)>=0 for v in pairs)
    assert {query(v) for v in pairs}=={F(11),F(12)}
    assert all(query(v)==(12 if adjacent(*v) else 11) for v in pairs)
    z=terminal(())
    menus=[]
    for i in range(3):
        columns=[]
        for a in A:
            leaf=terminal(z[:i]+(a,))
            columns.append(query(leaf[:i]+leaf[i+1:]))
        menus.append(min(columns))
    utilities=[utility(z,i) for i in range(3)]
    assert z==(0,1,1)
    assert utilities==[1,12,12]
    assert menus==[11,11,12]
    assert sum(menus)-sum(utilities)==9
    gammas=[]
    cross=[]
    for i,a in enumerate((0,0,1)):
        branch=terminal(z[:i]+(a,))
        v=branch[:i]+branch[i+1:]
        gammas.append(utilities[i]-utility(branch,i))
        cross.append(phi(branch)-sum((phi(v+(t,)) for t in A),F(0))/K)
    assert gammas==[0,0,0]
    assert cross==[-10,1,0]
    assert sum(utilities)-sum(menus)==sum(gammas)+sum(cross)
    lower_marginal=phi((0,1))-phi((0,))
    upper_marginal=phi((0,1,1))-phi((0,1))
    assert (lower_marginal,upper_marginal)==(10,12)
    print(json.dumps({
        'status':'exact_method_counterexample_verified',
        'scope':'anonymous marginal-potential games; not customer attraction',
        'histories':checked_histories,'comparisons_including_prescribed':checked_comparisons,
        'ordered_terminals':len(terminals),'unordered_competitors':len(pairs),
        'actual_path':z,'actual_utilities':list(map(str,utilities)),
        'total_utility':str(sum(utilities)),'free_column_minima':list(map(str,menus)),
        'gap':str(sum(menus)-sum(utilities)),
        'uniform_static_security_lower_bound':'11',
        'minimizing_columns':[0,0,1],
        'IC_slacks':list(map(str,gammas)),
        'cross_potential_terms':list(map(str,cross)),
        'diminishing_returns_failure':[str(lower_marginal),str(upper_marginal)],
    },ensure_ascii=False,indent=2))

if __name__=='__main__':run()
