"""Exact two-copy Cartesian SPE from the aggregate three-actor menu formula.
All 273 ordered-history nodes and 4368 deviations are checked separately.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import json

def main():
    root=Path(__file__).parent;src=json.loads((root/'cartesian_convexification_k4.json').read_text())['analysis'];w=src['weights'];k=src['k'];K=2
    clients=[frozenset(a for a in range(k) if mask>>a&1) for mask,weight in enumerate(w,1) for _ in range(weight)]
    def pu(a,z):return sum((F(1,sum(b in C for b in z)) for C in clients if a in C),F(0))
    pay={z:tuple(pu(a,z) for a in z) for z in product(range(k),repeat=3)}
    br={};phi=[];menus=[]
    for a in range(k):
        rows=[];floors=[]
        for b in range(k):
            value=max(pay[a,b,c][2] for c in range(k));B=[c for c in range(k) if pay[a,b,c][2]==value];br[a,b]=B;floors.append(min(pay[a,b,c][1] for c in B));rows.extend((a,b,c) for c in B)
        phi.append(max(floors));menus.append(rows)
    def util(z):return tuple(sum(pay[t][i] for t in z) for i in range(3))
    M={};pess={}
    for A in product(range(k),repeat=K):
        M[A]=[z for z in product(*(menus[a] for a in A)) if util(z)[1]>=sum(phi[a] for a in A)]
        pess[A]=min(M[A],key=lambda z:(util(z)[0],sum(util(z)),z))
    G=max(util(z)[0] for z in pess.values());G1=max(min(pay[z][0] for z in menus[a] if pay[z][1]>=phi[a]) for a in range(k))
    selected=min((z for menu in M.values() for z in menu if util(z)[0]>=G),key=lambda z:(sum(util(z)),util(z)[0],z))
    Astar=tuple(z[0] for z in selected);pess[Astar]=selected
    topics=list(product(range(k),repeat=K));index={A:i for i,A in enumerate(topics)};actions={():index[Astar]}
    for A in topics:
        chosen=pess[A];Bchosen=tuple(z[1] for z in chosen);Cchosen=tuple(z[2] for z in chosen);actions[(index[A],)]=index[Bchosen]
        for B in topics:
            C=Cchosen if B==Bchosen else tuple(min(br[a,b],key=lambda c:(pay[a,b,c][1],pay[a,b,c][0],c)) for a,b in zip(A,B))
            actions[(index[A],index[B])]=index[C]
    actual=[]
    while len(actual)<3:actual.append(actions[tuple(actual)])
    joint_clients=[frozenset(i for i,A in enumerate(topics) if A[j] in C) for j in range(K) for C in clients]
    @lru_cache(None)
    def terminal(h):
        return h if len(h)==3 else terminal(h+(actions[h],))
    @lru_cache(None)
    def up(z,a):return sum((F(1,sum(b in C for b in z)) for C in joint_clients if a in C),F(0))
    comparisons=0;minslack=None
    for h,chosen in actions.items():
        own=up(terminal(h),chosen)
        for a in range(len(topics)):
            gap=own-up(terminal(h+(a,)),a);assert gap>=0,(h,a,gap)
            minslack=gap if minslack is None else min(minslack,gap);comparisons+=1
    assert len(actions)==273 and comparisons==4368
    actual_topics=[topics[a] for a in actual];actual_u=[up(tuple(actual),a) for a in actual]
    assert actual_u==list(util(selected))
    assert G<2*G1
    game=dict(players=3,topics=[str(A) for A in topics],customers=[dict(topics=sorted(C),multiplicity=1) for C in joint_clients])
    packet=dict(status='exact full ordered-history SPE verified; no safety or half counterexample asserted',base_weights=w,base_clients=len(clients),copies=K,phi=list(map(str,phi)),base_root_minimum_guarantee=str(G1),joint_root_minimum_guarantee=str(G),root_floor_drop=str(2*G1-G),actual_labels=actual,actual_components=actual_topics,payoffs=list(map(str,actual_u)),W=str(sum(actual_u)),ordered_histories=len(actions),all_comparisons=comparisons,min_slack=str(minslack),root_deviation_values=[str(up(terminal((i,)),i)) for i in range(len(topics))],game=game,policy=[dict(history=h,action=a) for h,a in actions.items()])
    (root/'cartesian_two_copy_exact.json').write_text(json.dumps(packet,indent=2)+'\n')
    print(json.dumps({k:v for k,v in packet.items() if k not in ('game','policy','base_weights')}))

if __name__=='__main__':main()
