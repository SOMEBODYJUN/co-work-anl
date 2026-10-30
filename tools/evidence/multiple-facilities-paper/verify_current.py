#!/usr/bin/env python3
"""New exact curation reconstruction; does not import historical author audits.

Checks current assets and independently implements finite lexicographic choice,
four budgets, literal atomic packing, full-game strict pure repair and every
labeled continuation. Finite cases do not prove the arbitrary-input theorem.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'archives/facility-games/subarchives/common-many/papers/factor-two-current'
manifest = json.loads((HERE / 'source-manifest.json').read_text())
for item in manifest['sources']:
    b = (ROOT / item['preserved_path']).read_bytes()
    assert len(b) == item['size'] and sha256(b).hexdigest() == item['sha256']
tex = (PAPER / 'main.tex').read_text()
active = re.sub(r'(?<!\\)%[^\n]*', '', tex)
bib = (PAPER / 'references.bib').read_text()
labels = re.findall(r'\\label\{([^}]+)\}', active)
refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', active)
cites = [x for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', active) for x in group.split(',')]
bibkeys = re.findall(r'@\w+\{([^,]+),', bib)
begins = Counter(re.findall(r'\\begin\{([^}]+)\}', active))
assert begins == Counter(re.findall(r'\\end\{([^}]+)\}', active))
assert not [x for x, n in Counter(labels).items() if n > 1]
assert not (set(refs)-set(labels)) and not (set(cites)-set(bibkeys))
formal = []
for m in re.finditer(r'\\begin\{(definition|construction|lemma|theorem|proposition|corollary)\}(.*?)\\end\{\1\}', active, re.S):
    formal.append({'environment':m[1], 'labels':re.findall(r'\\label\{([^}]+)\}',m[2]),
                   'line':active[:m.start()].count('\n')+1,'sha256':sha256(m[0].encode()).hexdigest()})
assert len(formal)==9 and begins['proof']==7 and all(x['labels'] for x in formal)
pdf = PAPER/'main.pdf'
info = subprocess.run(['/usr/bin/pdfinfo',str(pdf)],capture_output=True,text=True,check=True).stdout
(HERE/'pdfinfo.txt').write_text(info)
pdftext = subprocess.run(['/usr/bin/pdftotext','-layout',str(pdf),'-'],capture_output=True,text=True,check=True).stdout
assert pdftext == (HERE/'pdf-text-layout.txt').read_text()
pages = pdftext.split('\f')
if not pages[-1].strip(): pages.pop()
assert len(pages)==8 and all(x.strip() for x in pages)


def loads(weights, assignment, k):
    return [sum((weights[i] for i,g in enumerate(assignment) if g==f),Q(0)) for f in range(k)]


def accessible(coverage, placement, i):
    return [f for f,t in enumerate(placement) if i in coverage[t]]


def feasible(weights, coverage, placement, assignment):
    for i,g in enumerate(assignment):
        options = accessible(coverage,placement,i)
        assert (g in options) if options else g==-1


def pure_ne(weights, coverage, placement, assignment):
    feasible(weights,coverage,placement,assignment)
    L=loads(weights,assignment,len(placement))
    return all(g==-1 or all(h==g or L[g]<=L[h]+weights[i] for h in accessible(coverage,placement,i)) for i,g in enumerate(assignment))


def repair(weights, coverage, placement, assignment, cap=None):
    assignment=list(assignment); seen=set(); steps=0; k=len(placement)
    heavy_positions={i:g for i,g in enumerate(assignment) if g>=0 and cap is not None and weights[i]>cap}
    while True:
        feasible(weights,coverage,placement,assignment)
        state=tuple(assignment); assert state not in seen; seen.add(state)
        L=loads(weights,assignment,k)
        if cap is not None:
            for i,g in heavy_positions.items(): assert assignment[i]==g and [j for j,h in enumerate(assignment) if h==g]==[i]
            for f,x in enumerate(L):
                occupants=[i for i,g in enumerate(assignment) if g==f]
                assert x<=cap or len(occupants)==1 and weights[occupants[0]]>cap
        move=None
        for i,g in enumerate(assignment):
            if g<0: continue
            cost,h=min((L[h]+(Q(0) if h==g else weights[i]),h) for h in accessible(coverage,placement,i))
            if cost<L[g]: move=(i,g,h,cost); break
        if move is None:
            assert pure_ne(weights,coverage,placement,assignment)
            return tuple(assignment),steps
        i,g,h,cost=move;old=sum(x*x for x in L)/2;assignment[i]=h
        new=sum(x*x for x in loads(weights,assignment,k))/2
        assert new-old==weights[i]*(cost-L[g])<0
        steps+=1


def packing(weights, clients, h, a):
    parts=[[i] for i in clients]
    while True:
        pair=next(((i,j) for i in range(len(parts)) for j in range(i+1,len(parts))
                   if sum((weights[x] for x in parts[i]+parts[j]),Q(0))<=2*a),None)
        if pair is None: break
        i,j=pair;parts[i]+=parts[j];del parts[j]
    assert sum((weights[i] for i in clients),Q(0))<=(h+1)*a
    assert len(parts)<=h
    assert all(sum((weights[i] for i in p),Q(0))<=2*a or len(p)==1 and weights[p[0]]>2*a for p in parts)
    return parts


stats=Counter(); witnesses={};ratios=[];game_records=[]


def audit_game(weights, coverage, k, tag):
    weights=tuple(map(Q,weights));coverage=tuple(map(frozenset,coverage));n=len(weights);m=len(coverage)
    best=None;chosen=None;candidate_count=0
    for s in product(range(m),repeat=k):
        O=sorted(set(s));q=Counter(s)
        choices=[[t for t in O if i in coverage[t]] for i in range(n)]
        choices=[x or [-1] for x in choices]
        for site_assignment in product(*choices):
            W={t:sum((weights[i] for i,x in enumerate(site_assignment) if x==t),Q(0)) for t in O}
            L=tuple(W[t]/q[t] for t in s);key=tuple(sorted(L));candidate_count+=1
            if best is None or key>best: best=key;chosen=(s,site_assignment,W,L)
    s,site_assignment,W,L=chosen;O=sorted(set(s));q=Counter(s)
    R=max(sum((weights[i] for i in c),Q(0)) for c in coverage)
    p=[[Q(1,q[s[f]]) if site_assignment[i]==s[f] else Q(0) for f in range(k)] for i in range(n)]
    for i in range(n):
        options=accessible(coverage,s,i)
        assert sum(p[i])==(1 if options else 0)
        costs={f:weights[i]+sum((weights[j]*p[j][f] for j in range(n) if j!=i),Q(0)) for f in options}
        assert all(not p[i][f] or costs[f]==min(costs.values()) for f in options)
    if R: assert min(L)>=R/k>0
    sigma={s:None};old_covered=set().union(*(coverage[t] for t in O));max_steps=0
    for f,u in enumerate(s):
        if not R: break
        a=L[f];J=[i for i,x in enumerate(site_assignment) if x==u]
        for r in range(m):
            if r==u:continue
            N=sum((weights[i] for i in coverage[r]-old_covered),Q(0))
            if r in O:
                rhs=W[r]+(sum((weights[i] for i in J if i in coverage[r]),Q(0)) if q[u]==1 else 0)
                assert rhs<=(q[r]+1)*a
            else:
                rhs=N+(sum((weights[i] for i in J if i in coverage[r]),Q(0)) if q[u]==1 else 0)
                assert rhs<=a
            category=('disappear' if q[u]==1 else 'survive')+('_occupied' if r in O else '_new')
            stats[category]+=1
            new=list(s);new[f]=r;new=tuple(new);assert new not in sigma
            stationary=[g for g in range(k) if g!=f];route={t:[] for t in set(s[g] for g in stationary)};onto_f=[]
            for i,t in enumerate(site_assignment):
                if t>=0 and not(q[u]==1 and t==u):route[t].append(i)
                elif t>=0:
                    options=sorted({s[g] for g in stationary if i in coverage[s[g]]})
                    if options:route[options[0]].append(i)
                    elif i in coverage[r]:onto_f.append(i)
                elif i in coverage[r]:onto_f.append(i)
            assignment=[-1]*n
            for t,clients in route.items():
                bins=[g for g in stationary if s[g]==t]
                for g,part in zip(bins,packing(weights,clients,len(bins),a)):
                    for i in part:assignment[i]=g
            for i in onto_f:assignment[i]=f
            assert loads(weights,assignment,k)[f]<=a
            result,steps=repair(weights,coverage,new,assignment,2*a)
            finalL=loads(weights,result,k);assert finalL[f]<=2*a
            sigma[new]=result;max_steps=max(max_steps,steps);stats['actual_deviations']+=1;stats['strict_repair_steps']+=steps
            ratios.append(finalL[f]/a)
            if category not in witnesses:
                witnesses[category]={'weights':list(map(str,weights)),'coverage':[sorted(x) for x in coverage],
                                     'placement':list(s),'mover':f,'target':r,'a':str(a),'seed':assignment,
                                     'terminal':list(result),'terminal_mover_load':str(finalL[f]),'steps':steps}
    for other in product(range(m),repeat=k):
        if other in sigma:continue
        assignment=[next(iter(accessible(coverage,other,i)),-1) for i in range(n)]
        terminal,steps=repair(weights,coverage,other,assignment)
        sigma[other]=terminal;stats['default_layouts']+=1;stats['default_strict_steps']+=steps
    assert len(sigma)==m**k
    stats['games']+=1;stats['candidate_site_profiles']+=candidate_count;stats['zero_reach_games']+=not bool(R)
    rec={'tag':tag,'weights':list(map(str,weights)),'coverage':[sorted(x) for x in coverage],
         'k':k,'selected_placement':list(s),'site_assignment':list(site_assignment),'onpath_loads':list(map(str,L)),
         'continuation_layouts':len(sigma),'max_capped_steps':max_steps}
    game_records.append(rec)
    return rec


# Exhaustive finite domains, not sampled games.
for weights in product((1,2,5),repeat=2):
    for memberships in product(range(4),repeat=2):
        cov=[{i for i,b in enumerate(memberships) if b&(1<<t)} for t in range(2)]
        for k in (2,3):audit_game(weights,cov,k,'two_clients_two_sites_all_memberships')
for memberships in product(range(4),repeat=3):
    cov=[{i for i,b in enumerate(memberships) if b&(1<<t)} for t in range(2)]
    for k in (2,3):audit_game((1,2,5),cov,k,'three_clients_two_sites_all_memberships')
scope_example=audit_game((1,100),({0},{0}),2,'globally_unreachable_heavy_client')
assert scope_example['onpath_loads']==['1/2','1/2']
scope_example['literal_all_I_heavy_isolation_premise_applicable']=False
scope_example['per_facility_or_served_client_premise_applicable']=True
scope_example['reason']='Client 1 has weight 100 but no accessible facility at any layout; its zero strategy is feasible, and all relevant loads ignore it.'
audit_game((3,3,2),({0},{1},{2}),2,'disappearing_source_new_coverage')
audit_game((2,2,4,1),({0,1},{2},{0,3}),2,'disappearing_source_orphans_and_new_coverage')
assert set(witnesses)=={'survive_occupied','survive_new','disappear_occupied','disappear_new'}

packing_cases=0
for length in range(6):
    for ws in combinations_with_replacement((Q(1,2),Q(1),Q(3,2),Q(2),Q(5,2),Q(3)),length):
        for h in range(1,5):
            if sum(ws)<=(h+1):packing(ws,list(range(length)),h,Q(1));packing_cases+=1
cap_seed=(0,1,1)
terminal,steps=repair(tuple(map(Q,(5,1,1))),({0,1,2},),(0,0,0),cap_seed,Q(2))
assert steps==1 and terminal[0]==0 and pure_ne(tuple(map(Q,(5,1,1))),({0,1,2},),(0,0,0),terminal)
result={'scope':'New finite exact reconstruction from current manuscript, with every labeled layout completed. No historical audit imported; no general theorem proved by enumeration.',
        'source_hashes_checked':10,'tex':{'lines':len(tex.splitlines()),'formal_count':len(formal),'proof_count':begins['proof'],
        'labels':len(labels),'ref_calls':len(refs),'cite_calls':len(cites),'bibliography_keys':bibkeys,
        'display_counts':{'equation':begins['equation'],'align':begins['align'],'bracket':len(re.findall(r'(?<!\\)\\\[',active))},'formal_blocks':formal},
        'pdf':{'pages':8,'extraction_matches':True,'page_text_sha256':[sha256(p.encode()).hexdigest() for p in pages],
        'visual':'All eight pages rendered at 100dpi and actually inspected in two four-page contact sheets; no clipping, formula spill or orphan reference page observed.'},
        'finite_construction':{'summary':dict(stats),'max_actual_deviation_ratio':str(max(ratios)),'four_case_witnesses':witnesses,
        'game_records':game_records,'independent_scalar_packing_cases':packing_cases,
        'cap_heavy_singleton_example':{'weights':['5','1','1'],'cap':'2','seed':list(cap_seed),'terminal':list(terminal),'strict_steps':steps},
        'unreachable_heavy_wording_example':scope_example},
        'not_claimed':['TeX/PDF recompiled','Historical proof-sanity/linter rerun','External source or current SIAM policy verified',
                       'Finite audit implies all positive real weights or arbitrary facility counts','Any polynomial search bound']}
(HERE/'current-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'tex':{k:v for k,v in result['tex'].items() if k!='formal_blocks'},
                  'finite_summary':result['finite_construction']['summary'],'packing_cases':packing_cases,
                  'max_finite_ratio':str(max(ratios)),'unreachable_example':scope_example},ensure_ascii=False,indent=2))
