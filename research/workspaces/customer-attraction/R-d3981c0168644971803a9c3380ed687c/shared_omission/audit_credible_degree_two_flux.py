#!/usr/bin/env python3
"""Definition-level full ordered-tree audit; no canonical solver imports.

This is a genuine SPE stress family, never a counterexample to half or theta.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import json
from pathlib import Path


def audit(q, a, b):
    assert q >= 2 and 0 <= a <= b and b > 0
    k, m = 2*q, q+1
    edges = [(i,j, b if (i<q)!=(j<q) else a)
             for i,j in combinations(range(k),2)
             if (b if (i<q)!=(j<q) else a)]
    groups = [tuple(range(q)),tuple(range(q,2*q))]
    def side(v): return int(v>=q)
    def pay(path, v):
        return sum((F(w, sum(x==i or x==j for x in path))
                    for i,j,w in edges if v==i or v==j), F())
    def welfare(path):
        return sum(w for i,j,w in edges if any(x==i or x==j for x in path))
    def prescribed(h):
        if not h: return 0
        if len(h)==1: return groups[1-side(h[0])][0]
        counts = [sum(side(x)==g for x in h) for g in range(2)]
        g = side(h[-1]) if counts[0]==counts[1] else int(counts[1]>counts[0])
        if counts[g]==q: g=1-g
        return min(set(groups[g])-set(h))
    policy, leaf = {}, {}
    comparisons = 0
    worst_slack = None
    def build(h):
        nonlocal comparisons,worst_slack
        if len(h)==m:
            return h
        results = [build(h+(v,)) for v in range(k)]
        values = [pay(results[v],v) for v in range(k)]
        action = prescribed(h) if len(set(h))==len(h) else max(range(k),key=values.__getitem__)
        for value in values:
            slack=values[action]-value
            assert slack >= 0, (q,a,b,h,action,values)
            comparisons += 1
            worst_slack=slack if worst_slack is None else min(worst_slack,slack)
        policy[h]=action
        leaf[h]=results[action]
        return results[action]
    actual=build(())
    L=F(q*b,2)+(q-1)*a
    H=F((2*q-1)*b,2)+F((q-1)*a,2)
    assert actual == (0,)+tuple(range(q,2*q))
    assert tuple(pay(actual,v) for v in actual)==(L,)+(H,)*q
    # Every forced root action really leads to the opposite group's full support.
    root_paths=[]
    for v in range(k):
        z=leaf[(v,)]
        assert z[0]==v and set(z[1:])==set(groups[1-side(v)]) and len(set(z[1:]))==q
        assert pay(z,v)==L and all(pay(z,t)==H for t in z[1:])
        root_paths.append(z)
    W=welfare(actual)
    OPT=max(welfare(z) for s in range(m+1) for z in combinations(range(k),s))
    expected=q*q*b+F((q-1)*(q+2)*a,2)
    assert W==OPT==expected
    # theta is the min of the last player's max over every ordered static prefix.
    theta=min(max(pay(h+(v,),v) for v in range(k)) for h in product(range(k),repeat=q))
    assert theta==L
    stationary_flux=sum((pay(z,z[0])-sum(pay(z,v) for v in z[1:])/q for z in root_paths),F())/k
    assert stationary_flux == -F((q-1)*(b-a),2)
    # Same flux computed by independently summing each degree-two customer's coefficient.
    edge_flux=[]
    for i,j,w in edges:
        coefficient=F()
        for v,z in enumerate(root_paths):
            I=int(v==i or v==j)
            K=sum(t==i or t==j for t in z[1:])
            if I+K: coefficient += F(q*I-K,q*(I+K)*k)
        predicted=-F(q-1,2*q*q) if side(i)!=side(j) else F(1,2*q)
        assert coefficient==predicted
        edge_flux.append(w*coefficient)
    assert sum(edge_flux,F())==stationary_flux
    C={e for e,(i,j,w) in enumerate(edges) if any(t in (i,j) for t in actual)}
    comparison=tuple(range(q))+(q,)
    O={e for e,(i,j,w) in enumerate(edges) if any(t in (i,j) for t in comparison)}
    D=sum(edges[e][2] for e in O-C)
    G=sum(edges[e][2] for e in C-O)
    assert D==G==a*comb(q-1,2)
    # Every customer belongs to precisely its two endpoint topics; themes are maximal.
    coverage=[{e for e,(i,j,w) in enumerate(edges) if t in (i,j)} for t in range(k)]
    assert all(not (coverage[i] <= coverage[j]) for i in range(k) for j in range(k) if i!=j)
    return dict(q=q,a=a,b=b,m=m,topics=k,customers=sum(w for _,_,w in edges),
                decision_histories=len(policy),action_comparisons=comparisons,
                actual=list(actual),root_payoff=str(L),tail_payoff=str(H),
                theta=str(theta),welfare=W,optimum=OPT,
                stationary_flux=str(stationary_flux),shared_optimal_omission=D,
                actual_only_waste=G,minimum_spe_slack=str(worst_slack),
                degree_two_only=True,all_topics_distinct_maximal=True)


def main():
    rows=[audit(q,a,b) for q,a,b in [(2,0,1),(3,0,1),(4,0,1),(2,1,2),(3,1,2),(4,1,2),(3,1,1)]]
    report={"status":"full ordered-history pure SPE; negative stationary flux, not a half/theta counterexample", "cases":rows,
            "total_decision_histories":sum(x["decision_histories"] for x in rows),
            "total_action_comparisons":sum(x["action_comparisons"] for x in rows)}
    print(json.dumps(report,indent=2))
    import sys
    if len(sys.argv)>1:
        p=Path(sys.argv[1]); assert not p.exists(); p.write_text(json.dumps(report,indent=2)+"\n")

if __name__ == "__main__": main()
