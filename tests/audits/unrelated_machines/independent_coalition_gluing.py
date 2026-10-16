#!/usr/bin/env python3
"""Independent baseline-lift oracle; exact finite audit, not a general solver.

Imports the old baseline, not long_path_coalition_gap.py. Writes stdout only.
"""
from fractions import Fraction as F
from itertools import combinations, product
from collections import Counter, defaultdict
import importlib.util, json, hashlib, platform
from pathlib import Path
path=Path(__file__).with_name('rounding_and_gap.py')
spec=importlib.util.spec_from_file_location('base',path);base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

def lift(k,ell):
    p,y,T=base.gap_instance(k); oldm=len(p);oldn=len(p[0])
    oe=[{i:p[i][j] for i in range(oldm) if p[i][j] is not None} for j in range(oldn)]
    counts=Counter(tuple(sorted(e)) for e in oe); edges=[];configs=[None]*oldm; repl={};newvars=[]
    for j,e in enumerate(oe):
        if counts[tuple(sorted(e))]==1:
            jj=len(edges);edges.append(e)
            for i in e:repl[i,j]=jj
        else:
            u=min(e,key=lambda i:e[i]);v=max(e,key=lambda i:e[i]);chain=[u]
            for _ in range(ell-1):chain.append(oldm+len(newvars));newvars.append(None)
            chain.append(v);ids=[]
            for a,b in zip(chain,chain[1:]):
                ids.append(len(edges));edges.append({a:F(1,k) if a==u else F(1),b:F(1)})
            repl[u,j]=ids[0];repl[v,j]=ids[-1]
            for s in range(1,ell):newvars[chain[s]-oldm]=[(F(1,k),(ids[s-1],)),(1-F(1,k),(ids[s],))]
    for i in range(oldm):configs[i]=[(w,tuple(repl[i,j] for j in S)) for w,S in y[i]]
    configs.extend(newvars)
    configs=[[(w,frozenset(S)) for w,S in c if w] for c in configs]
    for i,c in enumerate(configs):
        assert sum(w for w,S in c)==1
        assert all(sum(edges[j][i] for j in S)<=T for w,S in c)
    for j,e in enumerate(edges):
        assert sum(w for i in e for w,S in configs[i] if j in S)==1
    return edges,configs,T

def verify_coalition(edges,y,T,W):
    W=set(W); adj={i:[] for i in W}; edge_of={}
    for j,e in enumerate(edges):
        u,v=e
        if u in W and v in W:adj[u].append(v);adj[v].append(u);edge_of[u,v]=edge_of[v,u]=j
    parent={};roots=[];order=[]
    for rt in sorted(W):
        if rt in parent:continue
        roots.append(rt);parent[rt]=None;todo=[rt]
        for u in todo:
            order.append(u)
            for v in adj[u]:
                if v==parent[u]:continue
                assert v not in parent,'coalition has cycle'
                parent[v]=u;todo.append(v)
    marg=[{S:w for w,S in yi} for yi in y]
    # combine equal duplicate configs if any
    for i,yi in enumerate(y):
        d=defaultdict(F)
        for w,S in yi:d[S]+=w
        marg[i]=d
    expected={i:defaultdict(F) for i in W};total=F(0);states=0
    for Ss in product(*(list(marg[i]) for i in order)):
        pick=dict(zip(order,Ss));weight=F(1)
        for i in order:
            pi=parent[i]
            if pi is None:weight*=marg[i][pick[i]];continue
            j=edge_of[pi,i];b=j in pick[pi]
            if (j in pick[i])==b:weight=F(0);break
            denom=sum(w for S,w in marg[i].items() if (j in S)!=b)
            weight*=marg[i][pick[i]]/denom
        if not weight:continue
        total+=weight;states+=1
        for i in W:expected[i][pick[i]]+=weight
        assignment=[]
        for j,e in enumerate(edges):
            inside=[i for i in e if i in W and j in pick[i]]
            assert len(inside)<=1
            if inside:assignment.append(inside[0])
            else:
                outside=[i for i in e if i not in W]
                assert outside,'internal job uncovered'
                assignment.append(outside[0])
        loads={i:F(0) for i in W}
        for j,i in enumerate(assignment):
            if i in W:loads[i]+=edges[j][i]
        assert all(loads[i]==sum(edges[j][i] for j in pick[i])<=T for i in W)
    assert total==1
    for i in W:assert dict(expected[i])==dict(marg[i])
    return states

out=[]
for k in (2,3):
    for ell in (2,3):
        edges,y,T=lift(k,ell);r=min(3,2*ell-1);coalitions=states=0
        for size in range(r+1):
            for W in combinations(range(len(y)),size):states+=verify_coalition(edges,y,T,W);coalitions+=1
        out.append(dict(k=k,ell=ell,m=len(y),n=len(edges),T=str(T),max_coalition=r,coalitions=coalitions,joint_states=states))
# Independently enumerate path orientations and implication used by integer lower bound.
path_cases=0
for k in range(2,9):
    for ell in range(2,9):
        for bits in product((0,1),repeat=ell):
            # bit 0=left endpoint, bit 1=right endpoint
            loads=[F(0)]*(ell+1)
            for s,b in enumerate(bits):loads[s+b]+=F(1,k) if s==0 and b==0 else F(1)
            if max(loads)<2 and bits[0]==1:assert bits[-1]==1
            path_cases+=1
print(json.dumps(dict(code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     baseline_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                     python=platform.python_version(), random_seed=None,
                     coalition_exact_checks=out,path_orientation_cases=path_cases,
                     limits='Only stated finite ranges; no full-overlap hierarchy or generic optimization oracle.',
                     arithmetic='fractions.Fraction; exhaustive stated ranges'),indent=2))
