"""Independent exact audit of stationary successor-source restriction.
Reads only old raw unit-client instance and strategy DAG. Does not import CAG
model, solver, certificate verifier, menu probe, or old numeric audit outputs.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json'
OUT = Path(__file__).with_name('stationary_source_independent_audit.json')
rawbytes=SOURCE.read_bytes(); doc=json.loads(rawbytes)
I=doc['instance']; topics=I['topics']; m=I['players']; n=len(topics); nodes=doc['nodes']; root=doc['root']
assert isinstance(m,int) and m>=1 and n>=1
clients=[]
for typ in I['customers']:
    inds=typ['topics']; mult=typ['multiplicity']
    assert isinstance(mult,int) and mult>=0 and len(inds)==len(set(inds))
    assert all(isinstance(a,int) and 0<=a<n for a in inds)
    clients += [frozenset(inds) for _ in range(mult)]

# Reachability and history-complete edges, independent of claimed targets.
seen={root}; todo=[root]; depthnodes=defaultdict(list)
while todo:
    v=todo.pop(); d=nodes[v]; q=tuple(d['counts']); dep=sum(q)
    assert len(q)==n and all(isinstance(c,int) and c>=0 for c in q) and dep<=m
    depthnodes[dep].append(v)
    if dep==m:
        assert d['action'] is None and d['children']==[]
    else:
        assert isinstance(d['action'],int) and 0<=d['action']<n and len(d['children'])==n
        for a,w in enumerate(d['children']):
            assert isinstance(w,int) and 0<=w<len(nodes)
            expected=list(q); expected[a]+=1
            assert nodes[w]['counts']==expected
            if w not in seen: seen.add(w); todo.append(w)
assert len(seen)==len(nodes)
assert nodes[root]['counts']==[0]*n

# Recover actual leaves through prescribed edges, not stored target fields.
leaf={}
for dep in range(m,-1,-1):
    for v in depthnodes[dep]:
        d=nodes[v]
        leaf[v]=tuple(d['counts']) if dep==m else leaf[d['children'][d['action']]]
        assert leaf[v]==tuple(d['target'])

@lru_cache(None)
def pay(q):
    res=[F(0) for _ in range(n)]
    for c in clients:
        load=sum(q[a] for a in c)
        if load:
            for a in c: res[a]+=F(1,load)
    return tuple(res)

slack=None; comparisons=0; strict=0
for v in sorted(seen):
    d=nodes[v]
    if d['action'] is None: continue
    a=d['action']; actual=pay(leaf[v])[a]
    for b,w in enumerate(d['children']):
        gap=actual-pay(leaf[w])[b]
        assert gap>=0,(v,a,b,gap)
        comparisons+=1; strict+=gap>0
        slack=gap if slack is None else min(slack,gap)

# Counting all expanded ordered histories proves coverage beyond just DAG nodes.
ways=Counter({root:1}); expanded_decisions=0; expanded_leaves=0
for dep in range(m+1):
    assert sum(ways[v] for v in depthnodes[dep])==n**dep
    for v in depthnodes[dep]:
        if dep==m: expanded_leaves+=ways[v]
        else:
            expanded_decisions+=ways[v]
            for w in nodes[v]['children']: ways[w]+=ways[v]

def path_after_forcing(a):
    seq=[a]; v=nodes[root]['children'][a]
    while nodes[v]['action'] is not None:
        b=nodes[v]['action']; seq.append(b); v=nodes[v]['children'][b]
    assert len(seq)==m
    assert tuple(Counter(seq)[b] for b in range(n))==leaf[v]
    return tuple(seq)
cols=[path_after_forcing(a) for a in range(n)]
colcounts=[tuple(Counter(z)[a] for a in range(n)) for z in cols]
assert colcounts==[tuple(x) for x in doc['root_columns']]
root_action=nodes[root]['action']; actual=cols[root_action]; qactual=colcounts[root_action]
u=pay(qactual)[root_action]
W=sum(any(qactual[a] for a in c) for c in clients)
# Explicit feasible optimum covering every unit client, padded to m actions.
opt_witness=(0,3,4,7)+(0,)*(m-4)
assert len(opt_witness)==m and all(any(a in c for a in opt_witness) for c in clients)
OPT=len(clients)
K=[[sum((F(1,1+sum(a in c for a in z)) for c in clients if t in c),F(0)) for z in cols] for t in range(n)]
P=[[F(z[1:].count(t),m-1) for z in cols] for t in range(n)]
assert all(sum(P[t][a] for t in range(n))==1 for a in range(n))

# Rational RREF. Rows augmented by right-hand side.
def rref(rows,variables):
    A=[list(map(F,row)) for row in rows]; piv=[]; pr=0
    for c in range(variables):
        ii=next((i for i in range(pr,len(A)) if A[i][c]),None)
        if ii is None: continue
        A[pr],A[ii]=A[ii],A[pr]
        scale=A[pr][c]; A[pr]=[v/scale for v in A[pr]]
        for i in range(len(A)):
            if i!=pr and A[i][c]:
                scale=A[i][c]; A[i]=[x-scale*y for x,y in zip(A[i],A[pr])]
        piv.append(c); pr+=1
    assert all(any(row[:variables]) or row[variables]==0 for row in A)
    return A,piv
statrows=[[P[t][a]-F(t==a) for a in range(n)]+[F(0)] for t in range(n)]
_, statpiv=rref(statrows,n)
rr,piv=rref(statrows+[[F(1)]*n+[F(1)]],n)
assert len(piv)==n
Q=[F(0)]*n
for row,c in zip(rr,piv): Q[c]=row[-1]
assert all(q>=0 for q in Q) and sum(Q)==1
assert all(sum(P[t][a]*Q[a] for a in range(n))==Q[t] for t in range(n))
stationary_queries=[sum(K[t][a]*Q[a] for a in range(n)) for t in range(n)]
cap=max(stationary_queries)
assert cap>u

# A separately supplied free-Q candidate is checked from the reconstructed K.
freeQ=[F(0)]*n; dualp=[F(0)]*n
for j in [0,1]:
    freeQ[4*j+2]=F(1,14); freeQ[4*j+3]=F(3,7)
    dualp[4*j+2]=F(2,7); dualp[4*j+3]=F(3,14)
assert sum(freeQ)==sum(dualp)==1
free_queries=[sum(K[t][a]*freeQ[a] for a in range(n)) for t in range(n)]
dual_columns=[sum(dualp[t]*K[t][a] for t in range(n)) for a in range(n)]
assert max(free_queries)==min(dual_columns)<u
free_stat_error=[sum(P[t][a]*freeQ[a] for a in range(n))-freeQ[t] for t in range(n)]
assert any(free_stat_error)
branch=[]
for a,z in enumerate(cols):
    ps=pay(colcounts[a]); rpay=ps[a]; fs=[ps[b] for b in z[1:]]
    branch.append(dict(root=topics[a],path=[topics[b] for b in z],root_payoff=str(rpay),follower_payoffs=list(map(str,fs)),minimum_follower=str(min(fs)),follower_copies_of_root=z[1:].count(a)))
result=dict(status='PASS',scope='Stationary successor-source restriction only; free Mfull and Q-CAG-HALF are not refuted',source=str(SOURCE.relative_to(ROOT)),source_sha256=hashlib.sha256(rawbytes).hexdigest(),unit_clients=len(clients),players=m,topics=topics,reachable_DAG_nodes=len(seen),DAG_terminal_nodes=len(depthnodes[m]),comparisons_including_self=comparisons,strict_comparisons=strict,minimum_SPE_slack=str(slack),expanded_ordered_decision_histories=expanded_decisions,expanded_terminal_histories=expanded_leaves,root_action=topics[root_action],actual_path=[topics[a] for a in actual],actual_payoffs=[str(pay(qactual)[a]) for a in actual],W=W,OPT=OPT,root_utility=str(u),root_branches=branch,K=[[str(x) for x in row] for row in K],P=[[str(x) for x in row] for row in P],rank_P_minus_I=len(statpiv),rank_with_normalization=len(piv),unique_stationary_Q=list(map(str,Q)),stationary_queries=list(map(str,stationary_queries)),stationary_cap=str(cap),stationary_gap=str(cap-u),free_Q=list(map(str,freeQ)),free_queries=list(map(str,free_queries)),free_Q_stationarity_error=list(map(str,free_stat_error)),free_dual_p=list(map(str,dualp)),free_dual_columns=list(map(str,dual_columns)),free_menu_value=str(max(free_queries)),free_menu_slack=str(u-max(free_queries)))
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','unit_clients','players','reachable_DAG_nodes','comparisons_including_self','expanded_ordered_decision_histories','root_utility','W','OPT','rank_P_minus_I','unique_stationary_Q','stationary_cap','stationary_gap','free_menu_value']},indent=2))
