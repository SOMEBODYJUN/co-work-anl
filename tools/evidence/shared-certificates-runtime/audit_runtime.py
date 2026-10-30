"""New targeted exact audit; does not replace or alter any original test."""
from fractions import Fraction as Q
from pathlib import Path
from copy import deepcopy
import json,random,sys
from facility_spe.exact import single_overlap as single
from facility_spe.exact import bounded_overlap as full
from facility_spe.exact import shared_offdiag as shared
from facility_spe.shared_phi import solve as menu_solve,serial
from facility_spe.cli.verify_phi import verify as independent_verify

ROOT=Path.cwd();OUT=Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=True)

def profile(instance,rec,key='shared'):
    weights=list(map(Q,instance['weights']));sites=list(map(set,instance['locations']));s,t=rec['layout']
    common=sorted(sites[s]&sites[t]);assert rec[key]==common
    ps=list(map(Q,rec['prob_first']));assert len(ps)==len(common)
    assert all(0<=p<=1 for p in ps)
    x=sum((weights[i] for i in sites[s]-sites[t]),Q(0))+sum((weights[i]*p for i,p in zip(common,ps)),Q(0))
    y=sum((weights[i] for i in sites[t]-sites[s]),Q(0))+sum((weights[i]*(1-p) for i,p in zip(common,ps)),Q(0))
    assert [x,y]==list(map(Q,rec['loads']))
    for i,p in zip(common,ps):
        c1=weights[i]+sum((weights[j]*z for j,z in zip(common,ps) if j!=i),Q(0))+sum((weights[j] for j in sites[s]-sites[t]),Q(0))
        c2=weights[i]+sum((weights[j]*(1-z) for j,z in zip(common,ps) if j!=i),Q(0))+sum((weights[j] for j in sites[t]-sites[s]),Q(0))
        assert p==0 or c1<=c2
        assert p==1 or c2<=c1
    return x,y

fixtures=[];complete_profiles=0
for stem in ['tiny','on_path_chord','sharp_lower_rational','sparse_four_rational','two_reach_multi_no']:
    case=json.loads((ROOT/'examples/shared'/f'{stem}.json').read_text())
    result=shared.solve(case);produced=menu_solve(case)
    independent_verify(case,produced)
    catalog=case.get('U1',list(range(len(case['locations']))))
    for s in catalog:
        for t in catalog:
            profile(case,shared.continuation(case,result,s,t));complete_profiles+=1
    (OUT/(stem+'-exact.json')).write_text(json.dumps(serial(result),indent=2)+'\n')
    (OUT/(stem+'-menu.json')).write_text(json.dumps(serial(produced),indent=2)+'\n')
    weights=list(map(Q,case['weights']));sites=list(map(set,case['locations']))
    fixtures.append({'name':stem,'reach':[sum((weights[i] for i in site),Q(0)) for site in sites],
                     'exact_alpha':result['alpha'],'exact_layout':result['on_path']['layout'],'exact_loads':result['on_path']['loads'],
                     'distinct_overlap':result['distinct_overlap'],'menu_factor':produced['factor'],'menu_family':produced['on_path']['family'],
                     'menu_layout':produced['on_path']['layout'],'menu_loads':produced['on_path']['loads'],
                     'ordered_menu_entries':produced['ordered_menu_entry_count']})

# Compare the original one-shared-customer solver to the full 3^k support solver.
rng=random.Random(2026103054);cases=[]
cases += [{'weights':[],'locations':[[],[]],'U1':[0],'U2':[1]},
          {'weights':[7],'locations':[[0],[0]],'U1':[0],'U2':[1]},
          {'weights':[1],'locations':[[0]],'U1':[0,0],'U2':[0]},
          {'weights':[2,3,5],'locations':[[0,1],[2],[0],[1]],'U1':[0,1],'U2':[2,3]}]
for _ in range(100):
    a,b=rng.randrange(1,5),rng.randrange(1,5);sites=[[] for _ in range(a+b)];weights=[]
    for s in range(a):
        for t in range(a,a+b):
            if rng.randrange(2):
                i=len(weights);weights.append(str(Q(rng.randrange(1,20),rng.randrange(1,8))));sites[s].append(i);sites[t].append(i)
    for s in range(a+b):
        for _ in range(rng.randrange(3)):
            i=len(weights);weights.append(str(Q(rng.randrange(1,20),rng.randrange(1,8))));sites[s].append(i)
    cases.append({'weights':weights,'locations':sites,'U1':list(range(a)),'U2':list(range(a,a+b))})
certificate_profiles=0;pair_checks=0
for case in cases:
    result=single.solve(case);reference=full.solve(case);assert result['finite_factor_exists']==reference['finite_factor_exists']
    if result['finite_factor_exists']:
        assert result['alpha']==reference['alpha'];single.verify(case,json.loads(json.dumps(single.serial(result))))
        profile(case,result['on_path'],'common');certificate_profiles+=1
        for rec in result['deviations']:
            profile(case,rec['witness'],'common');certificate_profiles+=1
    ws,ss,u1,u2=single.parse(case)
    for s in u1:
        for t in u2:
            one=single.local(ws,ss,s,t);all_=full.local(ws,ss,s,t)
            assert one['lo']==all_['min_piece']['lo'] and one['hi']==all_['max_piece']['hi'];pair_checks+=1

# Verify the exact original checker without its producer functions.
case=cases[3];cert=single.solve(case);interval=cases[1];icert=single.solve(interval);accepted=[];rejected=[]
old_local,old_solve=single.local,single.solve
single.local=lambda *a:(_ for _ in ()).throw(RuntimeError('local called by verifier'))
single.solve=lambda *a:(_ for _ in ()).throw(RuntimeError('solve called by verifier'))
single.verify(case,cert);accepted.append('producer-functions-disabled')
mut=deepcopy(cert);mut['alpha']=max(Q(2),cert['alpha']);single.verify(case,mut);accepted.append('valid-looser-alpha')
mut=deepcopy(cert);mut['default_continuation']='unvalidated descriptive text';single.verify(case,mut);accepted.append('arbitrary-default-description')
mutants=[]
mut=deepcopy(cert);mut['finite_factor_exists']=False;mutants.append(('negative-report',case,mut))
mut=deepcopy(cert);mut['deviations'].pop();mutants.append(('missing-deviation',case,mut))
mut=deepcopy(cert);mut['on_path']['loads'][0]+=1;mutants.append(('forged-load',case,mut))
mut=deepcopy(cert);mut['deviations'][0]['deviator']=True;mutants.append(('boolean-label',case,mut))
mut=deepcopy(icert);mut['on_path']['prob_first']=[Q(-1)];mutants.append(('negative-probability',interval,mut))
invalid=deepcopy(case);invalid['locations'][3]=[0,1];mutants.append(('unrecorded-invalid-cross-pair',invalid,cert))
for name,instance,mutant in mutants:
    try:single.verify(instance,mutant)
    except ValueError:rejected.append(name)
    else:raise RuntimeError('mutant unexpectedly accepted: '+name)
single.local,single.solve=old_local,old_solve
interval_data=single.local(*single.parse(interval)[:2],0,1)
assert (interval_data['lo'],interval_data['hi'])==(0,7)
summary={'fixtures':fixtures,'shared_complete_profiles_directly_checked':complete_profiles,
         'single_overlap':{'seed':2026103054,'directed_cases':4,'random_cases':100,'full_support_pair_comparisons':pair_checks,
                           'attainment_profiles_directly_checked':certificate_profiles,'accepted_contract_variants':accepted,'rejected_mutants':rejected,
                           'one_customer_interval':[interval_data['lo'],interval_data['hi']]},'optimization_flag':sys.flags.optimize}
(OUT/'runtime-audit-results.json').write_text(json.dumps(serial(summary),indent=2)+'\n')
print(json.dumps(serial(summary),indent=2))
