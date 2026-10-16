#!/usr/bin/env python3
"""Independent audit: simultaneous true rows plus one exact configuration.

Uses the earlier independent sparse family definition, not the main algorithm.
No project file is written. Integer load units are 1/k, with exact validation.
"""
import sys
sys.dont_write_bytecode = True
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib, importlib.util, json, platform
SOURCE=Path(__file__).resolve().with_name('independent_row_count_escape.py')
spec=importlib.util.spec_from_file_location('independent_family_source',SOURCE)
independent=importlib.util.module_from_spec(spec);spec.loader.exec_module(independent)


def extension(f,u,v,c):
    k,N=f['k'],f['N'];kind,a=f['kinds'][v];c=set(c)
    outside=[b for b in range(N) if b not in u]
    if not u <= set(range(N)) or len(outside)<2*k:
        raise ValueError('protected centers must be valid and at most N-2k')
    if kind=='V' and a not in u:
        raise ValueError('specified center must be protected')
    if any(j<0 or j>=len(f['edges']) or v not in f['edges'][j] for j in c):
        raise ValueError('configuration contains unavailable job')
    if sum((f['edges'][j][v] for j in c),F(0))>1:
        raise ValueError('configuration exceeds true target 1')
    inactive=set();must_active=set();need=2*k
    if kind=='V':
        if f['blocks'][a]['x'] in c:must_active.add(a)
        else:inactive.add(a)
    elif kind=='G':
        if c:
            assert len(c)==1
            xa=next(b for b in range(N) if f['blocks'][b]['x'] in c)
            inactive.add(xa)
        else:need+=1
    elif kind=='R':inactive.add(a)
    active=set(must_active)
    for b in outside+sorted(u):
        if len(active)==need:break
        if b not in inactive:active.add(b)
    assert len(active)==need and not active&inactive
    # At the boundary a helper inside U is needed only for a non-V query.
    inside_active=active&u
    assert len(inside_active)<=1
    if inside_active and kind in ('G','R'):
        helper=next(iter(inside_active));assert helper not in inactive
    sigma={};freeg=iter(g for g in f['g'] if g!=v)
    forcedx=next(iter(c)) if kind=='G' and c else None
    for b,block in enumerate(f['blocks']):
        x=block['x']
        sigma[x]=v if x==forcedx else block['v'] if b in active else next(freeg)
        zs,ys,rs=block['z'],block['y'],list(block['r'])
        if kind=='V' and b==a and block['x'] not in c:
            kept=set(zs)&c
            external=[j for j in zs if j not in kept]
            for j in kept:sigma[j]=block['v']
            for j,r in zip(external,rs):sigma[j]=r
            remain=rs[len(external):]
            excess=max(0,len(ys)-len(remain))
            for j in ys[:excess]:sigma[j]=f['z']
            for j,r in zip(ys[excess:],remain):sigma[j]=r
        elif kind=='R' and b==a:
            remaining=[r for r in rs if r!=v]
            for j in zs:sigma[j]=block['v']
            if not c:
                for j,r in zip(ys,remaining):sigma[j]=r
            else:
                forced=next(iter(c));sigma[forced]=v
                for j,r in zip([j for j in ys if j!=forced],remaining):sigma[j]=r
        elif b in inside_active:
            for j,r in zip(zs,rs):sigma[j]=r
            for j in ys[:-1]:sigma[j]=f['z']
            sigma[ys[-1]]=rs[k]
        elif b in active:
            sigma[zs[0]]=rs[0]
            for j in zs[1:]:sigma[j]=block['v']
            for j,r in zip(ys,rs[1:]):sigma[j]=r
        else:
            for j in zs:sigma[j]=block['v']
            for j,r in zip(ys,rs):sigma[j]=r
    if kind=='z':
        for j in c:sigma[j]=v
    return sigma


def configurations_at(f,v):
    kind,a=f['kinds'][v]
    yield frozenset()
    if kind=='V':
        block=f['blocks'][a];yield frozenset([block['x']])
        for size in range(1,f['k']+1):
            for c in combinations(block['z'],size):yield frozenset(c)
    elif kind=='G':
        for b in f['blocks']:yield frozenset([b['x']])
    elif kind=='R':
        for j in f['blocks'][a]['y']+f['blocks'][a]['z']:yield frozenset([j])
    else:
        ys=[j for b in f['blocks'] for j in b['y']]
        for size in range(1,f['k']+1):
            for c in combinations(ys,size):yield frozenset(c)


def check(f,u,v,c,sigma):
    assert len(sigma)==len(f['edges'])
    counts=Counter();units=Counter()
    for j,i in sigma.items():
        assert i in f['edges'][j]
        value=f['edges'][j][i]*f['k'];assert value.denominator==1
        counts[i]+=1;units[i]+=value.numerator
    assert {j for j,i in sigma.items() if i==v}==set(c)
    for i,(kind,a) in enumerate(f['kinds']):
        cap=f['k'] if kind in ('V','z') else 1
        assert counts[i]<=cap
        if kind!='V' or a in u:assert units[i]<=f['k']
    assert units[v]<=f['k']
    return len(sigma)


def audit_all_k2():
    f=independent.build_family(2);N=f['N'];bound=N-4
    queries=assignments=subsets=0
    allcfg={v:list(configurations_at(f,v)) for v in range(len(f['kinds']))}
    for size in range(bound+1):
        for tup in combinations(range(N),size):
            subsets+=1;u=set(tup)
            for v,(kind,a) in enumerate(f['kinds']):
                if kind=='V' and a not in u:continue
                for c in allcfg[v]:
                    assignments+=check(f,u,v,c,extension(f,u,v,c));queries+=1
    return {'k':2,'maximum_U_centers':bound,'all_center_subsets_checked':subsets,
            'all_eligible_v_and_all_configurations_checked':queries,'job_assignments_checked':assignments,
            'z_configurations_per_U':len(allcfg[f['z']]),
            'scope':'All U intersections with V up to bound; all other rows are true by their count caps, so every choice of non-V membership is covered.'}


def sharp_hall_certificate(f):
    k,N=f['k'],f['N'];u=set(range(N-2*k+1))
    adj={b['x']:set(f['g'])|({b['v']} if a not in u else set())
         for a,b in enumerate(f['blocks'])}
    # Exact unit-capacity matching. A center has only its own X neighbor, so
    # giving it its original count capacity k cannot improve this rank.
    matching={}
    def augment(j,seen):
        for i in sorted(adj[j]):
            if i in seen:continue
            seen.add(i)
            if i not in matching or augment(matching[i],seen):
                matching[i]=j;return True
        return False
    for j in sorted(adj):augment(j,set())
    neighborhood=set().union(*adj.values())
    assert len(adj)==N and len(neighborhood)==N-1 and len(matching)==N-1
    return {'protected_centers':len(u),'forced_configuration':'z empty',
            'Hall_task_count':len(adj),'Hall_neighbor_count':len(neighborhood),
            'exact_necessary_matching_rank':len(matching),
            'edge_pruning_reason':'When z is empty, a protected true-load-1 center cannot take its X: its k Z and k Y would need 2k>k+1 local unit R slots.',
            'scope':'Exact derived necessary matching/Hall certificate, not general scheduling enumeration.'}


def audit_boundary(k):
    f=independent.build_family(k);N=f['N'];u=set(range(N-2*k));a=0;b=N-1
    cases=[]
    # All V configurations on one representative protected center.
    v=f['blocks'][a]['v']
    cases.extend((v,c) for c in configurations_at(f,v))
    # Force a protected or unprotected block's X on G; also G empty.
    g=f['g'][0];cases.extend([(g,frozenset()),(g,frozenset([f['blocks'][a]['x']])),(g,frozenset([f['blocks'][b]['x']]))])
    # All R configurations from each side of the protected-center boundary.
    for blockid in (a,b):
        r=f['blocks'][blockid]['r'][0]
        cases.extend((r,c) for c in configurations_at(f,r))
    # z empty/full in one block on each side, and distinct-block Y identities.
    z=f['z'];cases.extend([(z,frozenset()),(z,frozenset(f['blocks'][a]['y'])),(z,frozenset(f['blocks'][b]['y'])),
                          (z,frozenset(f['blocks'][t]['y'][0] for t in range(k)))])
    assignments=0
    for v,c in cases:assignments+=check(f,u,v,c,extension(f,u,v,c))
    # Sharp failure: protected centers N-2k+1, z forced empty. G count caps
    # force 2k X on centers; no protected center can accept X with z empty,
    # since its k Z and k Y cannot fit k+1 unit R slots.
    r=N-2*k+1;outside=N-r
    assert outside==2*k-1 and outside<2*k and 2*k>k+1
    return {'k':k,'boundary_U_centers':len(u),'structured_configuration_queries':len(cases),
            'job_assignments_checked':assignments,'sharp_failure_U_centers':r,
            'sharp_failure_forced_configuration':'z empty',
            'sharp_failure_outside_X_capacity':outside,'X_center_deficit':2*k,
            'input_sha256':f['input_sha256'],'sharp_Hall_certificate':sharp_hall_certificate(f)}


if __name__=='__main__':
    print(json.dumps({'title':'多行真实负载及单配置延伸的独立边界攻击','python':platform.python_version(),
                      'arithmetic':'exact integer load units 1/k; family times Fraction; no tolerance',
                      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'independent_family_source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                      'exhaustive_k2':audit_all_k2(),
                      'structured_boundary':[audit_boundary(3)],
                      'sharp_necessary_certificates':[sharp_hall_certificate(independent.build_family(k)) for k in (2,3)],
                      'limits':['Default only writes JSON to stdout; no frozen evidence overwritten.','General proof is separate from finite checks.',
                                'No claim about conditional LST/configuration LP.',
                                'Endpoint failure is proved by capacity counting, not full schedule enumeration.']},ensure_ascii=False,indent=2))
