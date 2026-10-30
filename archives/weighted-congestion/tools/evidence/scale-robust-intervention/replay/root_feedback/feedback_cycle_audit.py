#!/usr/bin/env python3
"""Exact finite check of cycle certificates, not of equilibrium nonexistence."""
from fractions import Fraction as F
from itertools import combinations, permutations
import json

def cycles(n, edges):
    eset={tuple(sorted(e)) for e in edges}
    out=[]
    for k in range(3,n+1):
        for vertices in combinations(range(n),k):
            first=min(vertices)
            for tail in permutations(v for v in vertices if v!=first):
                if tail[0]>tail[-1]: continue
                c=(first,)+tail
                if all(tuple(sorted((c[j],c[(j+1)%k]))) in eset for j in range(k)):
                    p=sum(c[j]<c[(j+1)%k] for j in range(k))
                    out.append((p,k-p,k))
    return out

def feasible(n,edges,beta,L):
    dist=[F(1)]*n
    for iteration in range(n):
        new=dist[:]
        for a,b in edges:
            new[b]=min(new[b],dist[a]*beta)
            new[a]=min(new[a],dist[b]/L)
        if new==dist:return True
        dist=new
    return False

def main():
    count=0; infeasible=0; equality_cases=0
    for n in range(1,6):
        all_edges=list(combinations(range(n),2))
        for mask in range(1<<len(all_edges)):
            edges=[e for j,e in enumerate(all_edges) if mask>>j&1]
            cs=cycles(n,edges)
            for d,beta in [(5,F(3)),(9,F(4)),(9,F(5)),(7,F(3))]:
                L=F(d-1,beta-1)
                assert 1<L<=beta
                bad=[(p,q,k) for p,q,k in cs if L**p>beta**q or L**q>beta**p]
                ok=feasible(n,edges,beta,L)
                assert ok==(not bad),(n,edges,d,beta,bad)
                for p,q,k in bad:
                    if L**q>beta**p:p,q=q,p
                    assert p>=1 and q>=1 and L**p>beta**q
                    # Exact integer floor of log(beta)/log(L), avoiding floats.
                    floorR=0
                    while L**(floorR+1)<=beta:floorR+=1
                    assert k>=floorR+2
                count+=1; infeasible+=not ok
                equality_cases+=sum(L**p==beta**q or L**q==beta**p for p,q,k in cs)
    return {'scope':'all simple strictly weight-ordered graphs on at most five types; four rational parameter pairs','graph_parameter_checks':count,'contract_infeasible':infeasible,'equalities_seen':equality_cases,'status':'PASS','does_not_prove':'universal theorem or original-game nonexistence'}
if __name__=='__main__': print(json.dumps(main(),indent=2))
