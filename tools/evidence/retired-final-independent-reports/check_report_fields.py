"""Arithmetic consistency of recorded JSON fields, not a generator rerun.
Does not recount all perfect matchings, all graphic-rank subset LPs, or all
243-allocation Pareto landscapes. Frozen count provenance remains separate.
"""
from pathlib import Path
from fractions import Fraction as Q
import json, hashlib, sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sources=json.loads((HERE/'source-manifest.json').read_text())
data={s['id']:json.loads((ROOT/s['preserved_path']).read_text()) for s in sources}

def dot(x,y): return sum((a*b for a,b in zip(x,y)),Q(0))
def rank(rows):
    a=[list(map(Q,row)) for row in rows]
    if not a:return 0
    r=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        d=a[r][col];a[r]=[x/d for x in a[r]]
        for i in range(r+1,len(a)):
            d=a[i][col]
            a[i]=[x-d*y for x,y in zip(a[i],a[r])]
        r+=1
    return r
center=[]
for name,c in data['3a8d140b8f57b847ff1d']['examples'].items():
    n=c['n'];edges=[tuple(x) for x in c['edges']]
    assert len(edges)==len(set(edges)) and edges==sorted(edges)
    p=list(map(Q,c['projection']));assert len(p)==len(edges)
    vs=[]
    for perm in c['permutations']:
        assert sorted(perm)==list(range(n))
        assert all((i,perm[i]) in edges for i in range(n))
        vs.append([Q(int(perm[i]==j)) for i,j in edges])
    assert {e for perm in c['permutations'] for e in enumerate(perm)}==set(edges)
    dirs=[[a-b for a,b in zip(v,vs[0])] for v in vs[1:]]
    assert rank(dirs)==c['face_dimension']
    assert all(dot(p,d)==0 for d in dirs)
    assert rank(dirs+[[a-b for a,b in zip(p,vs[0])]])==c['face_dimension']
    assert all(sum(p[t] for t,(i,j) in enumerate(edges) if i==row)==1 for row in range(n))
    assert all(sum(p[t] for t,(i,j) in enumerate(edges) if j==col)==1 for col in range(n))
    assert min(p)==Q(c['minimum']) and dot(p,p)==Q(c['squared_norm'])
    assert (min(p)>=0)==c['centered']
    center.append({'name':name,'stored_vertices':len(vs),'stored_edges':len(edges),
                   'affine_dimension':c['face_dimension'],'normal_equations_exact':True,
                   'projection_in_affine_span':True,'minimum':c['minimum'],
                   'squared_norm':c['squared_norm']})
theta=[]
for c in data['9b95ac91318e47666b07']['cases']:
    k,l=c['k'],c['length'];assert c['subsets']==2**(k*l)
    best=(Q(1),1,1)
    for s in range(2,k+1):
        for q in range(1,s+1):
            a=((Q(l-1)+Q(1,q))/l)**l;b=Q(l-1,l)**l
            ratio=1-(q*a+(s-q)*b-1+(1-a)**q*(1-b)**(s-q))/Q(s*(l-1)+1)
            best=min(best,(ratio,s,q))
    assert best==(Q(c['candidate_ratio']),c['attaining_support_paths'],c['attaining_active_t'])
    assert Q(c['exact_witness_ratio'])==best[0]
    assert Q(c['exact_witness_mass'])==best[1]*(l-1)+1
    assert c['lp_samples']==28 and c['min_numeric_margin']>-1e-8
    assert c['max_lp_equality_residual']<1e-8
    theta.append({'k':k,'length':l,'finite_formula_minimum_fields_match':True,
                  'stored_subset_count':c['subsets'],'stored_lp_samples':c['lp_samples']})

def family(a,b,c): return [[Q(1),Q(1),Q(1),a,a],[Q(1),Q(1),b,Q(1),Q(1)],
                           [Q(1),Q(1),c,c,c]]
def one(values,assignment):
    n=len(values);m=len(values[0])
    assert len(assignment)==m and all(0<=i<n for i in assignment)
    bundles=[[g for g in range(m) if assignment[g]==i] for i in range(n)]
    u=[sum((values[i][g] for g in bundles[i]),Q(0)) for i in range(n)]
    bad=[]
    for i in range(n):
        for j in range(n):
            for removed in bundles[j]:
                remain=sum((values[i][g] for g in bundles[j] if g!=removed),Q(0))
                if u[i]<remain:bad.append([i,j,removed,str(remain)])
    return u,bad

fair=data['8c8ec755dcaf145e7078']
fair_checks=[]
target=[1,1,2,0,0]
full=[([Q(2),Q(3),Q(4)],fair['base'])]
full += [(list(map(Q,c['parameters'])),c['result']) for c in fair['boundary_checks']]
listed_dominators=0
for parameters,c in full:
    values=family(*parameters);u,bad=one(values,target)
    assert list(map(str,u))==c['target_utility'] and (not bad)==c['target_is_efx']
    assert c['agents']==3 and c['goods']==5 and c['all_allocations']==243
    for d in c['dominators']:
        du,dbad=one(values,d['assignment'])
        assert list(map(str,du))==d['utility']
        assert (not dbad)==d['efx'] and dbad==d['violations']
        assert all(a>=b for a,b in zip(du,u)) and any(a>b for a,b in zip(du,u))
        listed_dominators+=1
    assert c['completion_failure']==(bool(c['dominators']) and all(not d['efx'] for d in c['dominators']))
    fair_checks.append({'parameters':list(map(str,parameters)),
                        'recorded_target_and_all_listed_dominators_exact':True,
                        'listed_dominators':len(c['dominators']),
                        'exhaustive_count_fields_not_recomputed':True})
for c in fair['family_checks']:
    a,b,cpar=map(Q,[c['a'],c['b'],c['c']])
    expected=a<2 or b>2
    assert c['obstruction']==expected and c['dominators']==(2 if expected else 0)
    assert c['efx_po']==(13 if expected else 16)
for c,expected in zip(fair['degenerate'],[(1,0,1),(2,2,4),(1,2,1)]):
    n,m,total=expected
    assert c=={'agents':n,'goods':m,'all_allocations':total,
               'efx_allocations':total,'efx_po_allocations':total}
all_parameters={(Q(2),Q(3),Q(4))}
all_parameters.update(tuple(map(Q,[c['a'],c['b'],c['c']])) for c in fair['family_checks'])
all_parameters.update(tuple(map(Q,c['parameters'])) for c in fair['boundary_checks'])
assert len(all_parameters)==10
out={'status':'passed','kind':'recorded-field arithmetic consistency only',
     'fresh_original_generator_runs':0,'python':sys.version,
     'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'source_sha256':{s['id']:s['sha256'] for s in sources},
     'centered_examples':center,'theta_formula_fields':theta,
     'fair_targets_and_listed_dominators':fair_checks,
     'fair_listed_dominator_records_checked':listed_dominators,
     'fair_grid_summary_fields_match_stated_8_point_contract':True,
     'fair_degenerate_counts_consistent':True,
     'fair_audit_call_count_from_source':15,
     'fair_distinct_three_agent_parameter_points':10,
     'fair_allocation_records_across_calls_including_duplicates':2922,
     'limits':['Does not enumerate missing vertices to certify completeness anew.',
               'Does not rerun graphic subset-rank/concave-envelope LP generator.',
               'Does not recount all EFX/PO landscape totals; they remain frozen original counts.',
               'Does not certify general theorems, external independence or novelty.']}
(HERE/'report-field-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':out['status'],'centered_examples':len(center),'theta_rows':len(theta),
                  'fair_listed_dominators':listed_dominators,'fresh_original_generator_runs':0}))
