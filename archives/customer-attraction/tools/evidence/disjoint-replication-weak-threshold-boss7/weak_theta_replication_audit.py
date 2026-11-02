"""Exact local arithmetic for the disjoint-block weak-theta obstruction.

No canonical solver, compressed payoff implementation, or stored certificate
is imported. Each of the 36 unit clients is expanded explicitly. The universal
strategy claim is a separate nice-state induction in the adjacent Markdown.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json

X=tuple(range(3));Y=tuple(range(3,6));A=X+Y
clients=[frozenset((x,y)) for x in X for y in Y]
for i in combinations(X,2):
    for j in combinations(Y,2):
        clients.extend([frozenset(i+j)]*3)
assert len(clients)==36

def group(a):return X if a in X else Y
def utility(history,position):
    a=history[position]
    return sum((F(1,sum(b in s for b in history)) for s in clients if a in s),F(0))
def join(history,a):return utility(tuple(history)+(a,),len(history))
def cover(history):return sum(any(a in s for a in history) for s in clients)
def reply(a,b):
    return min(t for t in group(b) if t not in (a,b))

checks=0
for a in A:
    assert join((a,),a)==F(21,2);checks+=1
    for b in A:
        if b==a:continue
        c=reply(a,b)
        assert utility((a,b,c),1)==12;checks+=1
        expected=([9,12,10] if group(a)==group(b) else [F(25,3),12])
        for t in A:
            if group(a)==group(b):
                v=9 if t in (a,b) else 12 if t in group(a) else 10
            else:v=F(25,3) if t in (a,b) else 12
            assert join((a,b),t)==v;checks+=1

for h in permutations(A,3):
    same=len({a//3 for a in h})==1
    u=tuple(utility(h,i) for i in range(3))
    if same:
        assert u==(12,12,12) and cover(h)==36
        assert {join(h,t) for t in A}=={F(15,2)}
    else:
        assert sorted(u)==[10,12,12] and cover(h)==34
        majority=next(g for g in (X,Y) if sum(a in g for a in h)==2)
        for t in A:
            expected=(F(22,3) if t in h else F(19,2)) if t in majority else (F(20,3) if t in h else F(35,4))
            assert join(h,t)==expected;checks+=1
    assert max(join(h,t) for t in A)<=F(19,2);checks+=1

theta_by_local_length={}
for n in range(3):
    values=[max(join(h,a) for a in A) for h in product(A,repeat=n)]
    theta_by_local_length[n]=min(values)
assert theta_by_local_length=={0:F(21),1:F(33,2),2:F(12)}
assert max(join((0,0),a) for a in A)==15
assert max(join((0,3),a) for a in A)==12
assert max(join((0,3,4),a) for a in A)==F(19,2)
assert tuple(utility((0,3,4),i) for i in range(3))==(10,12,12)
assert cover((0,3,4))==34 and cover((0,1,2))==36

def counts(p,n):
    if p==1:
        yield (n,)
    else:
        for v in range(n+1):
            for q in counts(p-1,n-v):yield (v,)+q
def uniform_local_query(q):
    return sum((F(len(s),6*(1+sum(q[a] for a in s))) for s in clients),F(0))
g_expected=(F(21),F(29,2),F(10),F(15,2),F(19,3),F(161,30))
g_results={};opponent_count_checks=0
for t,expected in enumerate(g_expected):
    rows=[(uniform_local_query(q),q) for q in counts(6,t)]
    opponent_count_checks+=len(rows)
    value,argmin=min(rows)
    assert value==expected and value>=15-F(5,2)*t
    g_results[t]={'value':str(value),'minimizer':argmin}
assert opponent_count_checks==462
for k in range(1,101):
    assert 34*k-(3*k-F(1,2))*12==6-2*k
    assert (34*k<(3*k-F(1,2))*12)==(k>=4)
    security=F(15,2)+F(5,2*k)
    assert 34*k-3*k*security==F(23*k-15,2)>0

print(json.dumps({'status':'exact_local_arithmetic_passed','expanded_unit_clients':len(clients),'local_class_checks':checks,
                  'theta_local_minima':{k:str(v) for k,v in theta_by_local_length.items()},
                  'uniform_query_local_count_checks':opponent_count_checks,'uniform_query_minima':g_results,
                  'all_k_claim':'separate_nice_state_induction','smallest_weak_bridge_failure':{'k':4,'m':12,'W':136,'theta':12,'proposed_rhs':138},
                  'main_half_coverage':'not_refuted'}))
