#!/usr/bin/env python3
"""Independent Fraction checks of product marginals, envelopes, and full policies."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

# First component: disjoint covers of sizes 2 and 1.
# Second: two covers of size 2 with intersection 1. Six separate unit clients.
C1=(frozenset({0}),frozenset({0}),frozenset({1}))
C2=(frozenset({0}),frozenset({0,1}),frozenset({1}))
A=tuple(product(range(2),repeat=2))
CLIENTS=tuple(frozenset(a for a in range(4) if A[a][0] in c) for c in C1)+tuple(
    frozenset(a for a in range(4) if A[a][1] in c) for c in C2)

def cover(clients,z):
    return sum((min(Q(1),sum((z[a] for a in c),Q())) for c in clients),Q())
def curve(t):
    if t<=1:return 2*t
    if t<=2:return t+1
    return Q(3)
def B(v):return max(Q(),2-v,3-2*v)
def Bprod(v):return max(Q(),4-v,6-2*v)

marginal_checks=0
for z in product((Q(),Q(1,2),Q(1)),repeat=4):
    marg=tuple(tuple(sum((z[a] for a in range(4) if A[a][j]==b),Q())
                     for b in range(2)) for j in range(2))
    t=sum(z,Q())
    assert all(sum(v,Q())==t for v in marg)
    assert cover(CLIENTS,z)==cover(C1,marg[0])+cover(C2,marg[1])
    assert cover(CLIENTS,z)<=2*curve(t)
    marginal_checks+=1

coupling_checks=0
for t in (Q(),Q(1,3),Q(1),Q(3,2),Q(2),Q(5)):
    if t==0:z1=z2=(Q(),Q())
    elif t<=1:z1=z2=(t,Q())
    elif t<=2:z1=z2=(Q(1),t-1)
    else:z1=z2=(t-1,Q(1))
    z=tuple(z1[a]*z2[b]/t if t else Q() for a,b in A)
    assert sum(z,Q())==t
    assert cover(CLIENTS,z)==2*curve(t)
    coupling_checks+=1

price_checks=0
for h in range(33):
    v=Q(h,4)
    splitmin=min(B(Q(r,8))+B(v-Q(r,8)) for r in range(2*h+1))
    assert splitmin==Bprod(v)==2*B(v/2)
    price_checks+=1

# m=2 component policy 1: root 0; reply 0 after either first action.
# Component policy 2: root 0; reply the opposite of first action.
def select(h):
    if not h:return A.index((0,0))
    first=A[h[0]]
    return A.index((0,1-first[1]))
def terminal(h):
    while len(h)<2:h=h+(select(h),)
    return h
def payoff(path,pos):
    return sum((Q(1,sum(a in c for a in path)) for c in CLIENTS if path[pos] in c),Q())
comparisons=0
for h in ((),)+tuple((a,) for a in range(4)):
    actual=terminal(h); pos=len(h)
    for a in range(4):
        deviated=terminal(h+(a,))
        assert payoff(actual,pos)>=payoff(deviated,pos)
        comparisons+=1
path=terminal(())
assert tuple(payoff(path,i) for i in range(2))==(Q(5,2),Q(5,2))
assert sum(any(a in c for a in path) for c in CLIENTS)==5
opt=max(sum(any(a in c for a in z) for c in CLIENTS) for z in product(range(4),repeat=2))
assert opt==6
report={'marginal_arrays':marginal_checks,'optimal_couplings':coupling_checks,
        'price_splittings':price_checks,'complete_policy_nodes':5,
        'complete_policy_comparisons':comparisons,'product_path':path,
        'payoffs':['5/2','5/2'],'welfare':5,'optimum':opt}
if __name__=='__main__':
    Path(__file__).with_name('audit_product_representation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
