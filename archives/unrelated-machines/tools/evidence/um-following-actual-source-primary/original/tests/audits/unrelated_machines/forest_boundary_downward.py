from fractions import Fraction as F
from itertools import product
from random import Random
from collections import defaultdict
import json

# Independent contract reconstruction. Node 0 is unconstrained boundary.
# jobs are dictionaries {available machine: exact nonnegative processing time}.
def compress(parent, jobs, T, eta):
    verts=set(parent)|{0}
    unary=defaultdict(list)
    bundles=defaultdict(list)
    for j,e in enumerate(jobs):
        if len(e)==1:
            unary[next(iter(e))].append(j)
        else:
            u,v=e
            if parent.get(u)==v: child=u
            elif parent.get(v)==u: child=v
            else: raise ValueError('not forest edge')
            bundles[child].append(j)
    children=defaultdict(list)
    for v,p in parent.items(): children[p].append(v)
    order=[]; stack=[0]
    while stack:
        v=stack.pop(); order.append(v); stack.extend(children[v])
    msg={}; assignment={}
    for v in order[::-1]:
        if v==0: continue
        fixed=sum((jobs[j][v] for j in unary[v]),F(0))+sum((msg[c] for c in children[v]),F(0))
        if fixed>T: return None
        p=parent[v]; ids=bundles[v]
        if not ids:
            here=[]; there=[]
        elif T==0:
            # At zero, assignments to an internal endpoint require p_vj=0.
            here=[j for j in ids if jobs[j][v]==0]
            there=[j for j in ids if jobs[j][v]!=0]
        else:
            q=len(ids)
            assert q>0
            delta=eta*T/q
            cap=(T-fixed)//delta
            dp={0:(F(0),())}
            # Objective is exact parent load. Every job is placed at exactly one endpoint.
            for j in ids:
                w=jobs[j][v]//delta
                nd={}
                for a,(cost,decisions) in dp.items():
                    c=(cost+jobs[j][p],decisions+(p,))
                    if a not in nd or c[0]<nd[a][0]: nd[a]=c
                    if a+w<=cap:
                        c=(cost,decisions+(v,))
                        if a+w not in nd or c[0]<nd[a+w][0]: nd[a+w]=c
                dp=nd
            _,(_,dest)=min(dp.items(),key=lambda kv:(kv[1][0],kv[0]))
            here=[j for j,d in zip(ids,dest) if d==v]
            there=[j for j,d in zip(ids,dest) if d==p]
        msg[v]=sum((jobs[j][p] for j in there),F(0))
        assignment.update({j:v for j in unary[v]+here})
        assignment.update({j:p for j in there})
    assignment.update({j:0 for j in unary[0]})
    loads={v:sum((jobs[j][v] for j,d in assignment.items() if d==v),F(0)) for v in verts}
    return loads[0],assignment,loads

def exact(parent,jobs,T):
    feasible=[]
    for dest in product(*(tuple(e) for e in jobs)):
        loads={v:sum((e[v] for e,d in zip(jobs,dest) if d==v),F(0)) for v in set(parent)|{0}}
        if all(loads[v]<=T for v in parent): feasible.append((loads[0],dest))
    return min(feasible,default=None)

def check(parent,jobs,T,eta):
    truth=exact(parent,jobs,T)
    got=compress(parent,jobs,T,eta)
    if truth is not None:
        assert got is not None,(parent,jobs,T,eta,truth)
        assert got[0]<=truth[0],(parent,jobs,T,eta,truth,got)
    if got is not None:
        b,a,loads=got
        assert len(a)==len(jobs)
        assert all(v in jobs[j] for j,v in a.items())
        assert all(loads[v]<=(1+eta)*T for v in parent),(parent,jobs,T,eta,got)
    return truth is not None,got is not None

rng=Random(723091)
counts=defaultdict(int)
for trial in range(2500):
    nv=rng.randrange(1,5)
    parent={v:rng.randrange(v) for v in range(1,nv+1)}
    jobs=[]
    for v,p in parent.items():
        for _ in range(rng.randrange(1,3)):
            jobs.append({v:F(rng.randrange(8),rng.randrange(1,8)),p:F(rng.randrange(8),rng.randrange(1,8))})
    for v in range(nv+1):
        if rng.randrange(3)==0: jobs.append({v:F(rng.randrange(5),rng.randrange(1,6))})
    T=F(rng.randrange(8),rng.randrange(1,7))
    eta=F(1,rng.randrange(1,6))
    a,b=check(parent,jobs,T,eta)
    counts[f'exact_{a}_returned_{b}']+=1
# Degenerate q=0 components, no tasks, and root-only tasks.
for parent,jobs,T in [({},[],F(0)),({},{0:F(9)},F(1)),({1:0},[{1:F(0)}],F(0)),({1:0},[{1:F(7,5)}],F(2))]:
    if isinstance(jobs,dict): jobs=[jobs]
    check(parent,jobs,T,F(1,3))
# Huge unrelated denominators and near-zero weights; exact arithmetic throughout.
parent={1:0,2:1,3:2}
jobs=[{1:F(1,10**101+1),0:F(10**99,7)},{2:F(0),1:F(1,10**97+3)},{3:F(1,10**103+7),2:F(2,10**103+7)},{3:F(0)}]
for T in [F(0),F(1,10**103+7),F(1)]:
    for eta in [F(1),F(1,7)]: check(parent,jobs,T,eta)
# A deep chain avoids recursion and tests no accumulated cap error.
parent={v:v-1 for v in range(1,301)}
jobs=[{v:F(101,100),v-1:F(1)} for v in parent]
r=compress(parent,jobs,F(1),F(1,10))
assert r is not None and max(r[2][v] for v in parent)<=F(11,10)
# Nested singleton-leaf elimination, with recursive original-task recovery.
def eliminate_all(parent,jobs,T,eta):
    parent=dict(parent)
    # Each current job stores the original assignments it represents when placed
    # at an available endpoint. Ordinary jobs are trivial endpoint-dependent maps.
    current=[(dict(e),{v:{j:v} for v in e}) for j,e in enumerate(jobs)]
    while parent:
        parents=set(parent.values())
        v=next(v for v in parent if v not in parents)
        p=parent[v]
        ids=[k for k,(e,_) in enumerate(current) if v in e]
        local=[{(0 if u==p else u):t for u,t in current[k][0].items()} for k in ids]
        got=compress({v:0},local,T,eta)
        if got is None: return None
        b,a,_=got
        expansion={}
        for j,d in a.items():
            old_endpoint=p if d==0 else d
            expansion.update(current[ids[j]][1][old_endpoint])
        current=[e for k,e in enumerate(current) if k not in ids]
        current.append(({p:b},{p:expansion}))
        del parent[v]
    expansion={}
    b=F(0)
    for e,exp in current:
        b+=e[0]
        expansion.update(exp[0])
    loads={v:sum((e[v] for j,e in enumerate(jobs) if expansion[j]==v),F(0)) for v in set(expansion.values())|{0}}
    assert loads[0]==b
    return b,expansion,loads
for trial in range(100):
    nv=rng.randrange(1,6)
    parent={v:rng.randrange(v) for v in range(1,nv+1)}
    jobs=[]
    for v,p in parent.items():
        for _ in range(rng.randrange(1,3)):
            jobs.append({v:F(rng.randrange(6),rng.randrange(1,6)),p:F(rng.randrange(6),rng.randrange(1,6))})
    truth=exact(parent,jobs,F(1))
    got=eliminate_all(parent,jobs,F(1),F(1,4))
    if truth is not None:
        assert got is not None
        assert got[0]<=truth[0]
    if got is not None:
        assert all(t<=F(5,4) for v,t in got[2].items() if v!=0)
print(json.dumps({'random_trials':2500,'outcomes':dict(counts),'large_denominator_cases':6,'degenerate_cases':4,'nested_composition_trials':100,'deep_chain_vertices':300,'deep_chain_max_internal_load':str(max(r[2][v] for v in parent)),'seed':723091,'fraction_exact':True},sort_keys=True,indent=2))
