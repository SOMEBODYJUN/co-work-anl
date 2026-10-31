"""Independent raw-input/certificate arithmetic; no original module imports."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter
import ast, hashlib, json, math

HERE=Path(__file__).resolve().parent
STAGE=HERE.parents[4]
def read(p): return json.loads((HERE/p).read_text())
def save(p,d):
    q=HERE/p;q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(d,ensure_ascii=False,indent=2,default=str)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rank(rows):
    a=[list(map(F,row)) for row in rows]
    if not a:return 0
    k=0
    for j in range(len(a[0])):
        p=next((i for i in range(k,len(a)) if a[i][j]),None)
        if p is None:continue
        a[k],a[p]=a[p],a[k];v=a[k][j];a[k]=[x/v for x in a[k]]
        for i in range(k+1,len(a)):
            v=a[i][j]
            if v:a[i]=[x-v*y for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k

def ghmr():
    d=read('comparison/evidence/runs/unrelated_machines/heavy_matching_escape_independent.json')
    assert d['exhaustive_weighted_matching_cases']==4**3*4**3*7==28672
    assert d['edge_preservation']['matrices']==24**3==13824
    f=[1,3,6,10]
    assert 5**3*sum(math.comb(3,k)*f[k]*f[3-k] for k in range(4))==16000
    for row in d['family']['expanded']:
        k,h=row['k'],row['height']
        internal=2*sum(k**j for j in range(h));bottom=2*k**(h-1)
        assert row['machines']==internal+2*k**h+1
        assert row['jobs']==1+k*internal+(k-1)*bottom
        assert row['all_optional_matching_witnesses']==2+k*internal+2*(k-1)*bottom
    for row in d['family']['compressed']:
        k,h=row['k'],row['height'];alpha=F(1,k-1);height=1
        while alpha<F(1,2):alpha*=F(k,k-1);height+=1
        assert height==h
        assert F(row['optimum'])==2-F(1,k)
        assert F(row['ratio'])==2-F(3,k+1)
        assert F(row['immediately_lower_grid'])==2-F(3,2*k)
        assert int(row['lower_grid_min_reserves'])==2**(h-1)
    main=read('comparison/evidence/runs/unrelated_machines/heavy_matching_residual_audit.json')
    assert len(main['compressed_parameters'])==61
    for row in main['compressed_parameters']:
        k=row['k'];a=F(1,k-1);h=1
        while a<F(1,2):a*=F(k,k-1);h+=1
        assert row['h']==h and F(row['optimum'])==2-F(1,k)
        assert F(row['configuration_target'])==1+F(1,k)
        assert F(row['ratio_lower_bound'])==2-F(3,k+1)
    return {'weighted_queries':28672,'small_matrices':13824,'T1_feasible_schedule_occurrences':16000,
            'expanded_family_points':3,'compressed_family_points':6}

def source(q,triples):
    calls=0
    for S in combinations(range(len(triples)),q):
        calls+=1
        if all(len({triples[a][d] for a in S})==q for d in range(3)):return list(S),calls
    return None,calls
def half_matrix(q,triples):
    s=len(triples);m=s+3*q+1
    rows=[]
    for x in range(q):
        for _ in range(3):
            row=[None]*m;row[x]=F(1,2)
            for a,t in enumerate(triples):
                if t[0]==x:row[q+a]=F(1)
            rows.append(row)
    for a,(_,y,z) in enumerate(triples):
        for dest in (q+s+y,q+s+q+z):
            row=[None]*m;row[q+a]=F(1,2);row[dest]=F(1);rows.append(row)
    return rows,m
def half():
    old=read('comparison/evidence/runs/unrelated_machines/half_unit_joint_choice_audit.json')
    p=old['primary'];tot=Counter();selected=[]
    for row in p['instances']:
        q,triples=row['q'],row['triples'];S,calls=source(q,triples)
        assert S==row['perfect_triple_indices'] and (S is not None)==row['perfect_3dm']
        assert row['machines']==len(triples)+3*q+1 and row['jobs']==3*q+2*len(triples)
        tot['source_states']+=calls;tot['instances']+=1;tot['yes_3dm']+=S is not None;tot[row['category']]+=1
        for query in row['queries']:
            expected=True if F(query['delta'])==F(1,2) else S is not None
            assert query['A_delta']==query['full_schedule']==expected
            tot['delta_queries']+=1
            tot['big_selection_states']+=query['big_selection_states']
            tot['scheduling_states']+=query['scheduling_states']
        if row['name'] in ['exhaustive_q0_mask0','exhaustive_q1_mask0','exhaustive_q1_mask1',
                           'duplicate_yes','duplicate_no_isolated','q3_cover_all_vertices_but_no_perfect']:
            P,m=half_matrix(q,triples)
            assert sum(x is not None for r in P for x in r)==3*q+7*len(triples)
            sigma=[x for x in range(q) for _ in range(3)]+[q+a for a in range(len(triples)) for _ in range(2)]
            kind='all-small endpoint witness'
            if S is not None:
                chosen=set(S);byx={triples[a][0]:a for a in S}
                for x in range(q):sigma[3*x]=q+byx[x]
                for a,(_x,y,z) in enumerate(triples):
                    if a in chosen:sigma[3*q+2*a]=q+len(triples)+y;sigma[3*q+2*a+1]=2*q+len(triples)+z
                kind='perfect-source actualT1 witness'
            loads=[F(0)]*m
            for j,i in enumerate(sigma):assert P[j][i] is not None;loads[i]+=P[j][i]
            assert max(loads,default=0)<=(1 if S is not None else F(3,2))
            permutation=list(range(1,m))+[0]
            independentP=[[None]*m for _ in P]
            for j,r in enumerate(P):
                for i,v in enumerate(r):independentP[j][permutation[i]]=None if v is None else 2*v
            selected.append({'name':row['name'],'q':q,'triples':triples,'matrix_job_major':P,
              'sigma':sigma,'loads':loads,'witness_kind':kind,'primary_to_independent_machine_permutation':permutation,
              'independent_integer_half_unit_matrix_job_major':independentP})
    assert dict(tot)==p['totals']
    ind=old['independent'];base=[]
    for q in range(3):
        universe=list(product(range(q),repeat=3))
        for mask in range(1<<len(universe)):base.append((q,[t for i,t in enumerate(universe) if mask>>i&1]))
    extras=[(1,[(0,0,0),(0,0,0)]),(2,[(0,0,0),(0,0,0),(1,1,1)]),
      (2,[(0,0,0),(1,0,1)]),(3,[(0,0,0),(1,1,1),(2,2,2)]),
      (3,[(0,0,0),(1,0,1),(2,2,2)]),(3,[(0,0,0),(0,1,1),(1,2,2)])]
    assert len(base+extras)==ind['checks']['cases']==265
    assert sum(source(q,t)[0] is not None for q,t in base+extras)==ind['checks']['yes']==180
    assert all(math.floor(2*(1+F(d)))==2 for d in ind['rational_deltas'])
    text=(HERE/'comparison/research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md').read_text()
    section=text[text.index('## 3a.'):text.index('\n## 4.')]
    assert hashlib.sha256(section.encode()).hexdigest()==old['section_3a_sha256']
    assert hashlib.sha256(text.encode()).hexdigest()==old['source_sha256']['research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md']
    save('inputs/half-unit-six-full-matrices-and-witnesses.json',selected)
    return {'primary_rows':362,'all_primary_totals_reconstructed':dict(tot),
            'independent_source_truth_cases':265,'independent_yes':180,'explicit_full_matrix_witnesses':len(selected)}

def hall():
    inputs=read('comparison/examples/unrelated_machines/hall_group_joint_flow_cases.json')['cases']
    outputs=read('comparison/evidence/certificates/unrelated_machines/hall_group_joint_flow_witness.json')['cases']
    assert set(inputs)==set(outputs) and len(inputs)==9
    total_assignments=jobs_checked=successful=0;counts={}
    for name,case in inputs.items():
        a=case['input'];H=len(a['groups']);m=H+a['k'];P=[]
        for r in a['macros']:P.append([None if v is None else F(v) for v in r]+[None]*a['k'])
        for h,G in enumerate(a['groups']):
            for w in G:
                r=[None]*m;r[h]=F(w)
                for z in a['eligibility'][h]:r[H+z]=F(w)
                P.append(r)
        assert P==[[None if v is None else F(v) for v in r] for r in case['original_matrix_job_major']]
        best=None;nassign=0
        for sigma in product(*[[i for i,v in enumerate(r) if v is not None] for r in P]):
            loads=[F(0)]*m
            for j,i in enumerate(sigma):loads[i]+=P[j][i]
            peak=max(loads,default=F(0));best=peak if best is None else min(best,peak);nassign+=1
        cert=outputs[name];assert best==F(cert['exact_optimum'])
        total_assignments+=nassign;counts[name]=nassign
        out=cert['output']
        if out is None:
            assert cert['sigma_machine_indices'] is None
            assert best>F(a['T'])
            continue
        successful+=1
        sigma=cert['sigma_machine_indices'];assert len(sigma)==len(P)
        loads=[F(0)]*m
        for j,i in enumerate(sigma):assert P[j][i] is not None;loads[i]+=P[j][i];jobs_checked+=1
        assert loads==list(map(F,out['loads']))
        flat=list(out['macro_assignment'])+[x for G in out['assignment'] for x in G]
        assert sigma==[i if k=='h' else H+i for k,i in flat]
        q,de=a['q'],F(a['delta']);rho=F(q)*(2+de)/(q+1)
        assert F(out['rho'])==rho
        T=F(out.get('threshold',a.get('T','0')))
        assert max(loads,default=F(0))<=rho*T
        if 'threshold' in out:assert T<=best
    old=read('comparison/evidence/runs/unrelated_machines/hall_group_joint_flow_audit.json')
    base=sum((2**k)**h*sum((2**h-1)**b for b in range(min(2,h)+1)) for h in range(1,4) for k in range(3))
    assert base==old['all_instances']==4448
    assert sum(h*4**h for h in range(1,4))==old['nonuniform_zero_job_cases']==228
    assert 2*sum(4**k for k in range(3))*sum(15**b for b in range(3))==old['varying_macro_times']['instances']==10122
    assert old['successful_outputs']-old['T_feasible']==495
    save('saved-hall-nine-oracle-counts.json',counts)
    return {'fixtures':9,'successful_actual_outputs':successful,'all_original_output_jobs_checked':jobs_checked,
            'original_assignments_enumerated':total_assignments,'base_cases':4448,
            'base_success_above_true_T_feasibility_count':495}

def flat():
    report=read('runs/global-flat-original/full-report.json');event=read('runs/global-flat-original/execution.json')
    assert event['exit_code']==0 and event['output_sha256']==sha(HERE/'runs/global-flat-original/full-report.json')
    points=read('inputs/global-flat-built-in-inputs.json')['cases'];stats={};atom_job_checks=0
    names={'flat_macro_micro':'flat_macro_micro','nonflat_independent':'nonflat_valid_global_distribution',
           'same_first_moments_compressed':None,'balanced_optimal':'balanced_optimal_uniform_distribution'}
    for name,outname in names.items():
        p=points[name];jobs=[{int(i):F(v) for i,v in j.items()} for j in p['jobs']]
        atoms=[(F(a['weight']),a['assignment']) for a in p['atoms']]
        variables=[(i,j) for j,job in enumerate(jobs) for i in sorted(job)]
        assert sum(w for w,a in atoms)==1
        for w,a in atoms:
            loads=Counter()
            for j,i in enumerate(a):assert i in jobs[j];loads[i]+=jobs[j][i];atom_job_checks+=1
            assert max(loads.values(),default=0)<=F(p['T'])
        def features(degree):
            mon=[S for k in range(degree+1) for S in combinations(variables,k) if len({j for i,j in S})==k]
            return [[int(all(a[j]==i for i,j in S)) for S in mon] for _w,a in atoms]
        pair=(rank(features(1)),rank(features(2)));stats[name]=pair
        if outname:
            assert pair==(report[outname]['checks']['low_rank'],report[outname]['checks']['high_rank'])
        else:assert pair==(2,2)
    data=report['flat_macro_micro'];P=points['flat_macro_micro'];atoms=P['atoms']
    assert len(data['moments'])==data['moment_entries']==211
    for rec in data['moments']:
        assert F(rec['value'])==sum((F(a['weight']) for a in atoms if all(a['assignment'][j]==i for i,j in rec['edges'])),F(0))
    assert Counter((F(a['weight']),tuple(a['assignment'])) for a in data['extracted_distribution'])==Counter(
        (F(a['weight']),tuple(a['assignment'])) for a in atoms)
    assert report['nonflat_valid_global_distribution']['compressed_operator_checks']['trace_defect_Delta']=='6'
    assert report['balanced_optimal_uniform_distribution']['compressed_operator_checks']['trace_defect_Delta']=='4'
    triples=points['cyclic_latin4']['triples']
    # Exact characters of Z4^2 diagonalize the integral16*covariance circulant.
    kernel={(x,z):(3 if x==z==0 else 1 if x and z and (x+z)%4 else -1)
            for x in range(4) for z in range(4)}
    values=[]
    for u,v in product(range(4),repeat=2):
        real=imag=0
        for (x,z),c in kernel.items():
            rr,ii=[(1,0),(0,1),(-1,0),(0,-1)][(u*x+v*z)%4];real+=c*rr;imag+=c*ii
        assert imag==0 and real>=0;values.append({'character':[u,v],'eigenvalue':real})
    assert sum(x['eigenvalue']>0 for x in values)==6
    assert not any(all(len({triples[a][d] for a in S})==4 for d in range(3))
                   for S in combinations(range(16),4))
    save('inputs/latin4-exact-character-PSD-check.json',values)
    # Independently check the recorded whitespace-only current/old document relation.
    doc=HERE/'comparison/research/current/unrelated_machines/global_assignment_moment_rounding.md'
    lines=doc.read_text().splitlines(keepends=True)
    for k in (12,15,17):assert lines[k]=='\n';lines[k]='  \n'
    assert hashlib.sha256(''.join(lines).encode()).hexdigest()=='5ec060ea153b2044de1c45395e7eec9db8dbc59a0769f38a86d5ff70dbd538b3'
    return {'built_in_point_feature_ranks':stats,'explicit_atom_job_checks':atom_job_checks,
            'all_flat_moments_reconstructed':211,'latin4_exact_nonnegative_character_values':16,
            'latin4_covariance_rank':6,'latin4_four_subsets_checked':1820,'old_whitespace_hash_recovered':True}

def main():
    manifest=read('primary-inventory.json')+read('comparison-inventory.json')
    by={d['path']:d['sha256'] for d in manifest}
    for d in manifest:
        p=STAGE/d['preserved_repo_path'];assert p.stat().st_size==d['size'] and sha(p)==d['sha256']
        if p.suffix=='.py':ast.parse(p.read_text())
    g=read('comparison/evidence/runs/unrelated_machines/heavy_matching_escape_independent.json')
    assert g['independent_sha256']==by['tests/audits/unrelated_machines/ghmr_independent.py']
    assert g['production_sha256']==by['tests/audits/unrelated_machines/heavy_matching_residual.py']
    hu=read('comparison/evidence/runs/unrelated_machines/half_unit_joint_choice_audit.json')
    for n in ['half_unit_joint_choice.py','half_unit_schedule_independent.py']:
        assert hu['source_sha256']['tests/audits/unrelated_machines/'+n]==by['tests/audits/unrelated_machines/'+n]
    h=read('comparison/evidence/runs/unrelated_machines/hall_group_joint_flow_audit.json')
    assert h['metadata']['source_sha256']==by['tests/audits/unrelated_machines/hall_group_joint_flow.py']
    flat_report=read('runs/global-flat-original/full-report.json')
    flat_event=read('runs/global-flat-original/execution.json')
    assert flat_report['source_sha256']==flat_event['source_sha256']==by['tests/audits/unrelated_machines/global_assignment_flat_moment_audit.py']
    result={'status':'passed','verification':'independent raw-data arithmetic and explicitly bounded new certificate checks; no original imports',
            'inventory_files':len(manifest),'new_original_program_runs':1,'original_program':'global_assignment_flat_moment_audit main only',
            'ghmr':ghmr(),'half_unit':half(),'hall':hall(),'flat_moment':flat()}
    save('data-selfcheck.json',result);print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
