#!/usr/bin/env python3
"""Independent perfect3DM reduction, every job exactly one small end and N empty."""
from fractions import Fraction as F
from itertools import product
import json,random,hashlib,platform
from itertools import combinations
from pathlib import Path
from joint_matching_completion import perfect_3dm,certificate_from_schedule,round_interface

def reduction(q,triples):
    s=len(triples);m=s+3*q+1;n=q+3+3*s;source=m-1
    p=[[None]*n for _ in range(m)]
    for j in range(q+3):
        p[source][j]=F(1,3)
        for a in range(s):p[a][j]=F(1)
    for a,t in enumerate(triples):
        for d,e in enumerate(t):
            j=q+3+3*a+d;p[a][j]=F(1,3);p[s+d*q+e][j]=F(1)
    assert all(sum(v is not None and v<=F(1,2) for v in (p[i][j] for i in range(m)))==1 for j in range(n))
    return p

def scheduling_oracle(p,first_jobs,T=F(1)):
    """Full backtracking; first_jobs only changes search order, never prunes a legal option."""
    from math import lcm
    scale=T.denominator
    for row in p:
        for value in row:
            if value is not None:scale=lcm(scale,F(value).denominator)
    p=[[None if value is None else int(F(value)*scale) for value in row] for row in p]
    T=int(T*scale)
    m=len(p);n=len(p[0]);loads=[0]*m;assignment=[None]*n;nodes=0
    choices=[[i for i in range(m) if p[i][j] is not None and p[i][j]<=T] for j in range(n)]
    def dfs(todo):
        nonlocal nodes
        nodes+=1
        if not todo:return tuple(assignment)
        pool=todo&first_jobs or todo
        available={j:[i for i in choices[j] if loads[i]+p[i][j]<=T] for j in pool}
        j=min(pool,key=lambda j:(len(available[j]),j))
        for i in sorted(available[j],key=lambda i:(p[i][j],i)):
            assignment[j]=i;loads[i]+=p[i][j]
            result=dfs(todo-{j})
            if result is not None:return result
            loads[i]-=p[i][j];assignment[j]=None
        return None
    ans=dfs(set(range(n)))
    return ans,nodes

def audit():
    rng=random.Random(20261016);cases=0;yes=0;nodes=0
    enumerated=[]
    for q in (0,1,2):
        universe=list(product(range(q),repeat=3))
        for mask in range(1<<len(universe)):
            triples=[t for j,t in enumerate(universe) if mask>>j&1]
            expected=perfect_3dm(q,triples);p=reduction(q,triples)
            a,nn=scheduling_oracle(p,set(range(q+3)))
            assert (a is not None)==(expected is not None),(q,triples,expected,a)
            if a is not None:
                H,x=certificate_from_schedule(p,a);round_interface(p,F(1),H,x);yes+=1
            cases+=1;nodes+=nn
        enumerated.append({'q':q,'all_hypergraphs':1<<len(universe)})
    for _ in range(50):
        q=3;triples=rng.sample(list(product(range(q),repeat=3)),rng.randint(1,12))
        expected=perfect_3dm(q,triples);p=reduction(q,triples)
        a,nn=scheduling_oracle(p,set(range(q+3)))
        assert (a is not None)==(expected is not None),(q,triples,expected,a)
        if a is not None:
            H,x=certificate_from_schedule(p,a);round_interface(p,F(1),H,x);yes+=1
        cases+=1;nodes+=nn
    return {'schema_version':1,'python_version':platform.python_version(),'arithmetic':'fractions.Fraction; exact backtracking; no tolerance','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(Path(__file__).with_name('joint_matching_completion.py').read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256(Path(__file__).with_name('rounding_and_gap.py').read_bytes()).hexdigest(),'seed':20261016,'warning':'Finite audits; universal reduction proof and classical perfect3DM NP-completeness remain theorem dependencies.','instances':cases,'yes_instances':yes,'exhaustive_3dm_ranges':enumerated,'sampled_q3_instances':50,'scheduling_backtracking_nodes':nodes,'every_job_exactly_one_small':True,'N_empty':True,'block_cuts':audit_block_cuts()}
def audit_block_cuts():
    from heavy_matching_residual import height
    configurations=0
    # Fully enumerate all star/reserve choices of a single k=4 bottom block.
    k=4
    for incoming in (0,1):
        for star in product((0,1),repeat=k):
            for reserve in product((0,1,2),repeat=k-1):
                terminals=list(star)
                z=0
                for ell,choice in enumerate(reserve):
                    if choice==2:z+=1
                    else:terminals[ell+choice]+=1
                for target in (F(1),F(5,4),F(3,2),F(7,4)):
                    parent=F(incoming)+F(k-sum(star),k)
                    if parent>target or max(terminals)>target or F(z,2)>target:continue
                    r=k-(k*(target-1)).numerator//(k*(target-1)).denominator
                    assert z >= (r-1)*incoming
                    configurations+=1
    rows=[]
    for k in range(4,65):
        h,_=height(k)
        for numerator in range(2*k,4*k-1):
            target=F(numerator,2*k)
            theta=F(2*k-1,k)
            r=k-(k*(target-1)).numerator//(k*(target-1)).denominator
            if target<theta:
                assert r>=2 and F(r-1,2)*r**(h-1)>=2>target
            else:
                assert target==theta and r==1
        rows.append({'k':k,'h':h,'threshold':str(F(2*k-1,k)),
                     'grid_step':str(F(1,2*k)),'threshold_cut_coefficient':0})
    # Sharp excluded boundary delta=1/3: q=1 with no triples is NO 3DM,
    # but four selectors on the common source have load4/3.
    p=reduction(1,[])
    source=len(p)-1
    assert perfect_3dm(1,[]) is None
    assert sum(p[source])==F(4,3)
    H={};x=[[F(int(i==source)) for _ in p[0]] for i in range(len(p))]
    round_interface(p,F(1),H,x,F(1,3))
    assert F(3,2)+F(1,3)==F(11,6) and F(3,2)+F(1,2)==2
    return {'single_block_k4_feasible_assignments_counted_per_threshold':configurations,
            'family_parameter_checks':rows,'delta_one_third_counterexample':True,
            'limits':'Finite block enumeration and grid/parameter checks only; no full-tree schedule enumeration.'}

if __name__=='__main__':print(json.dumps(audit(),indent=2))
