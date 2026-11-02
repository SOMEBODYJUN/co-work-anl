#!/usr/bin/env python3
"""Exact checks of static credit and a complete SPE defeating universal cover cost.

No canonical solver imports. Nonuniform menu algebra is not labelled a SPE.
"""
from fractions import Fraction as F
from itertools import combinations,product
import json
from pathlib import Path


def count_vectors(n,k):
    if k==1:
        yield (n,)
    else:
        for c in range(n+1):
            for z in count_vectors(n-c,k-1):yield (c,)+z


def nonuniform_static_case():
    q=3;k=2*q
    types=[]
    for i,j in combinations(range(k),2):
        w=(20 if (i<q)!=(j<q) else 10)+int((i,j)==(0,1))+int((i,j)==(0,3))
        types.append((frozenset((i,j)),w))
    types += [(frozenset((i,)),i+1) for i in range(k)]
    background=(0,1,1)
    bg=[sum(v in e for v in background) for e,w in types]
    def Fquery(i,p):
        return sum((F(w,old+1+sum(p[j] for j in e)) for (e,w),old in zip(types,bg) if i in e),F())
    D=[];slack=[]
    for i in range(k):
        side=int(i>=q)
        tail=tuple(int(int(j>=q)!=side) for j in range(k))
        D.append(Fquery(i,tail))
        value=F()
        for (e,w),old in zip(types,bg):
            if i not in e: continue
            if len(e)==1:
                value+=w*(F(1,old+1)-F(1,old+2))
            elif all(int(j>=q)==side for j in e):
                value+=w*(F(1,old+1)-F(1,old+3))
        slack.append(value)
    pX=(1,)*q+(0,)*q;pY=(0,)*q+(1,)*q
    FX=[Fquery(i,pX) for i in range(k)];FY=[Fquery(i,pY) for i in range(k)]
    assert FX==[D[i]-slack[i] if i<q else D[i] for i in range(k)]
    assert FY==[D[i] if i<q else D[i]-slack[i] for i in range(k)]
    theta=min(max(Fquery(i,p) for i in range(k)) for p in count_vectors(q,k))
    upper=min(max(FX),max(FY))
    assert theta<=upper<=max(D)
    # Every root's customer tail load is dominated by pX, in this menu shape.
    for i in range(k):
        tail=tuple(int(int(j>=q)!=int(i>=q)) for j in range(k))
        for e,w in types:
            if i in e:assert sum(pX[j] for j in e)>=sum(tail[j] for j in e)
    return dict(kind="nonuniform exact menu algebra only; no SPE asserted",q=q,
                legal_background=list(background),D=list(map(str,D)),
                static_X_queries=list(map(str,FX)),static_Y_queries=list(map(str,FY)),
                theta=str(theta),static_upper=str(upper),max_D=str(max(D)))


def credible_K5_cover_obstruction():
    k=5;m=3;edges=list(combinations(range(k),2))
    def pay(z,v):
        return sum((F(1,sum(t in e for t in z)) for e in edges if v in e),F())
    def chosen(h):
        if not h:return 0
        if len(h)==1:return (h[0]+1)%k
        a,b=h
        if a!=b and b==(a+1)%k:return (a-1)%k
        return min(set(range(k))-set(h))
    def complete(h):
        while len(h)<m:h=h+(chosen(h),)
        return h
    comparisons=0;nodes=0
    for t in range(m):
        for h in product(range(k),repeat=t):
            a=chosen(h);v=pay(complete(h),a);nodes+=1
            for j in range(k):
                assert v>=pay(complete(h+(j,)),j)
                comparisons+=1
    root_paths=[complete((i,)) for i in range(k)]
    assert all(z==(i,(i+1)%k,(i-1)%k) for i,z in enumerate(root_paths))
    assert all(all(pay(z,j)==3 for j in z) for z in root_paths)
    theta=min(max(pay(h+(j,),j) for j in range(k)) for h in product(range(k),repeat=2))
    assert theta==3
    demand={}
    for i,j in edges:
        Ki=sum(t==j for t in root_paths[i][1:])
        Kj=sum(t==i for t in root_paths[j][1:])
        demand[(i,j)]=max(Ki,Kj)
    cost=next(n for n in range(k+1) if any(all(p[i]+p[j]>=h for (i,j),h in demand.items()) for p in count_vectors(n,k)))
    assert cost==3>m-1
    return dict(kind="complete ordered-history pure SPE",topics=k,players=m,
                decision_histories=nodes,action_comparisons=comparisons,
                root_paths=root_paths,root_payoff="3",theta=str(theta),
                integer_crowding_cover_cost=cost,available_static_actions=m-1,
                positive_demand_edges=[list(e) for e,h in demand.items() if h])


def main():
    report=dict(nonuniform_static_credit=nonuniform_static_case(),
                credible_integer_cover_obstruction=credible_K5_cover_obstruction())
    print(json.dumps(report,indent=2))
    import sys
    if len(sys.argv)>1:
        p=Path(sys.argv[1]);assert not p.exists();p.write_text(json.dumps(report,indent=2)+"\n")

if __name__=="__main__":main()
