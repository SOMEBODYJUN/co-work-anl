#!/usr/bin/env python3
"""Independent finite recomputation; candidate generators only, no check_* calls."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse, importlib.util, hashlib, json, platform, random
parser=argparse.ArgumentParser()
parser.add_argument("--repo",type=Path,default=Path.cwd())
args=parser.parse_args()
ROOT=args.repo.resolve()
SOURCE=ROOT/'tests/audits/unrelated_machines/diluted_sink_probe_gap.py'
spec=importlib.util.spec_from_file_location('submitted_generator',SOURCE)
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

def verify_x(d,x,jfix,ifix):
    job_ids=set(range(len(d['edges'])))
    assert set(x)==job_ids
    loads={i:Q(0) for i in range(len(d['configs']))}
    for j in job_ids:
        assert sum(x[j].values(),Q(0))==1
        for i,v in x[j].items():
            assert isinstance(v,Q) and v>=0
            assert i in d['edges'][j]
            assert d['edges'][j][i]<=d['T']
            loads[i]+=v*d['edges'][j][i]
    assert x[jfix].get(ifix,Q(0))==1
    assert max(loads.values())<=d['T']
    return max(loads.values())

def verify_configs(d):
    coverage={j:Q(0) for j in range(len(d['edges']))}
    total_columns=0
    for i,choices in enumerate(d['configs']):
        mass=Q(0)
        for w,jobs in choices:
            assert isinstance(w,Q) and w>=0
            assert len(jobs)==len(set(jobs))
            assert all(i in d['edges'][j] for j in jobs)
            assert sum((d['edges'][j][i] for j in jobs),Q(0))<=d['T']
            mass+=w
            for j in jobs: coverage[j]+=w
            total_columns+=1
        assert mass==1
    assert set(coverage.values())=={Q(1)}
    return total_columns

def verify_stars(d):
    count,maxF=0,0
    for j,e in enumerate(d['edges']):
        for i in e:
            Fj=[]
            for ell,domains in enumerate(d['edges']):
                if ell==j or i not in domains: continue
                if any(2*p<=d['T'] for r,p in domains.items() if r!=i): continue
                Fj.append(ell)
            # Build an explicit matching, independently of submitted augment code.
            # A successful witness suffices to show W equals total nonnegative weight.
            used=set()
            mapping={}
            for ell in sorted(Fj,key=lambda ell:len(d['edges'][ell])):
                options=set(d['edges'][ell])-{i}-used
                assert options
                r=min(options)
                used.add(r);mapping[ell]=r
            assert len(used)==len(Fj)
            assert all(r!=i and r in d['edges'][ell] for ell,r in mapping.items())
            total=sum((d['edges'][ell][i] for ell in Fj),Q(0))
            W=sum((d['edges'][ell][i] for ell in mapping),Q(0))
            assert total==W
            assert e[i]+total-W<=d['T']
            count+=1;maxF=max(maxF,len(Fj))
    return count,maxF

def independent_opt(d):
    values=[]
    best=None
    count=0
    for assignment in product(*(tuple(e.keys()) for e in d['edges'])):
        loads=[Q(0)]*len(d['configs'])
        for j,i in enumerate(assignment): loads[i]+=d['edges'][j][i]
        objective=max(loads)
        best=objective if best is None else min(best,objective)
        count+=1
    return best,count

def independently_build_schedule(d):
    assign={}
    # Choose small endpoint for all nonblockers except the bridge, then propagate
    # a single incoming unit starting at root 0 to its smallest available child.
    assign[d['bridge']]=d['roots'][0]
    for j,e in enumerate(d['edges']):
        small=[i for i,p in e.items() if p==Q(1,d['k'])]
        if small: assign[j]=small[0]
    cursor=d['roots'][0]
    while True:
        out=[j for j,e in enumerate(d['edges']) if e.get(cursor)==Q(1,d['k'])]
        if not out: break
        chosen=min(out)
        cursor=next(i for i in d['edges'][chosen] if i!=cursor)
        assign[chosen]=cursor
    for g in d['gadgets']:
        occupied=set(assign[j] for j in g['ordinary'])&set(g['terminals'])
        free=sorted(set(g['terminals'])-occupied)
        for j,i in zip(g['blockers'],free): assign[j]=i
    assert set(assign)==set(range(len(d['edges'])))
    loads=[Q(0)]*len(d['configs'])
    for j,i in assign.items():
        assert i in d['edges'][j]
        loads[i]+=d['edges'][j][i]
    assert max(loads)==2-Q(1,d['k'])
    return str(max(loads))

def generic_star_safety():
    vals=(Q(0),Q(1,2),Q(1),None)
    matrices=feasible_schedules=0
    for flat in product(vals,repeat=6):
        E=[{i:flat[2*j+i] for i in range(2) if flat[2*j+i] is not None} for j in range(3)]
        if any(not e for e in E): continue
        matrices+=1
        B={}
        for j,e in enumerate(E):
            for i,p in e.items():
                F=[ell for ell,ed in enumerate(E) if ell!=j and i in ed
                   and all(v>Q(1,2) for r,v in ed.items() if r!=i)]
                # One other machine: at most one off-source F task can match.
                W=max([Q(0)]+[E[ell][i] for ell in F if 1-i in E[ell]])
                B[i,j]=p+sum((E[ell][i] for ell in F),Q(0))-W
        for sigma in product(*(tuple(e) for e in E)):
            load=[Q(0),Q(0)]
            for j,i in enumerate(sigma): load[i]+=E[j][i]
            if max(load)>1: continue
            feasible_schedules+=1
            assert all(B[i,j]<=1 for j,i in enumerate(sigma))
    return matrices,feasible_schedules

rows=[]
rng=random.Random(20261016)
for k in (2,3,4):
    d=a.instance(k)
    allpairs=[(j,i) for j,e in enumerate(d['edges']) for i in e]
    if k<4:
        probes=allpairs
    else:
        # Independent selection: every bridge edge, every edge of one bottom
        # group, one edge for each depth/endpoint type, plus reproducible sample.
        probes={(d['bridge'],i) for i in d['roots']}
        g=d['gadgets'][0]
        for j in g['ordinary']: probes.update((j,i) for i in d['edges'][j])
        b=g['blockers'][0]
        probes.update((b,i) for i in g['terminals'])
        seen=set()
        for j,e in enumerate(d['edges']):
            for i,p in e.items():
                key=tuple(d['roles'][j])+(p,)
                if key not in seen: probes.add((j,i));seen.add(key)
        probes.update(rng.sample(allpairs,32))
        probes=sorted(probes)
    columns=verify_configs(d)
    maxima=[verify_x(d,a.probe_certificate(d,j,i),j,i) for j,i in probes]
    stars,maxF=verify_stars(d)
    row={'k':k,'h':d['h'],'machines':len(d['configs']),'jobs':len(d['edges']),
         'all_edges':len(allpairs),'config_columns':columns,'actual_probe_vectors_checked':len(probes),
         'probe_selection':'all edges' if k<4 else 'typed coverage, one full bottom blocker row, seed-20261016 sample',
         'all_star_edges_checked':stars,'largest_F':maxF,
         'largest_checked_fractional_load':str(max(maxima)),
         'independently_constructed_integer_value':independently_build_schedule(d)}
    if k==2:
        v,c=independent_opt(d);assert v==2-Q(1,k)
        row.update(independent_brute_optimum=str(v),full_assignments=c)
    rows.append(row)
print(json.dumps({'title':'独立重算稀释终端实际证书','submitted_code_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 'audit_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'python':platform.python_version(),'arithmetic':'Fraction exact','seed':20261016,
 'results':rows,'generic_star_safety_2machine_3job':generic_star_safety(),
 'limitations':['The candidate instance/probe generators are imported; all numerical assertions are independently recomputed.',
 'No submitted check_* or star_matching_certificate routine is called.',
 'Finite arithmetic audits do not prove the universal family theorem or solve UM-TARGET-v1.',
 'Section 9 general rejection proof reviewed symbolically; no generic LP solver implementation tested.']},ensure_ascii=False,indent=2))
