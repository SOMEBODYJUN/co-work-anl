"""Read-only integrity review of frozen saved data; no row engine, LP or SPE check.
Checks every stored coefficient string and atom field, but never reconstructs
7497-row coefficients or certifies historical floating primal/dual optimality.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
from itertools import product
import ast, hashlib, json, math
HERE=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(name): return json.loads((HERE/'original'/name).read_text())
def key(a,hidden=False):
    fields=('bits','AB_hist','AE_hist','second_hist','menus_lh','max_bits')+ (('actual_HQR_bits',) if hidden else ())
    return json.dumps({k:a[k] for k in fields},sort_keys=True,separators=(',',':'))
def atom(a,hidden=False,mass=False):
    expected={'bits','AB_hist','AE_hist','second_hist','menus_lh','max_bits'}
    if hidden: expected.add('actual_HQR_bits')
    if mass: expected.add('exact_mass')
    assert set(a)==expected
    for field,width in [('bits',10),('max_bits',5)]+([('actual_HQR_bits',3)] if hidden else []):
        assert len(a[field])==width and set(a[field])<={'0','1'}
    for field,width in [('AB_hist',8),('AE_hist',8),('second_hist',16)]:
        assert len(a[field])==width and all(type(v) is int and v>=0 for v in a[field]) and sum(a[field])==5
    d=sum(a['AB_hist'][4:]); assert sum(a['AE_hist'][4:])==sum(a['second_hist'][8:])==d
    assert len(a['menus_lh'])==3
    for menu in a['menus_lh']:
        assert len(menu)==2 and all(type(v) is int for v in menu)
        l,h=menu; assert 0<=h<=d and 0<=l-h<=5-d
    if mass: assert F(a['exact_mass'])>0
    return d

def leaves(d):
    if isinstance(d,dict): return sum(leaves(v) for v in d.values())
    if isinstance(d,list): return sum(leaves(v) for v in d)
    if isinstance(d,float): assert math.isfinite(d)
    return 1

def main():
    manifest=json.loads((HERE/'source-manifest.json').read_text()); fingerprints=[]
    for m in manifest:
        raw=(HERE/'original'/m['id']).read_bytes(); canonical=HERE/'original'/('/'.join(m['path'].split('/')[-2:]))
        assert len(raw)==m['size'] and hashlib.sha256(raw).hexdigest()==m['sha256'] and raw==canonical.read_bytes()
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==m['blob']
        if m['path'].endswith('.py'): ast.parse(raw)
        fingerprints.append({'id':m['id'],'bytes':len(raw),'sha256':m['sha256'],'blob_sha1':m['blob'],'canonical_equal':True})
    seed=load('certificate/full_actual_extension_discovery.json'); priced=load('maxroot/known_actual_extension_pricing.json')
    new=load('certificate/full_actual_extension_known_v1_discovery.json'); exact=load('certificate/exact_full_actual_extension_known_v1.json')
    assert seed['code_sha256']==sha(HERE/'original/certificate/full_actual_extension.py')
    assert new['code_sha256']==exact['code_sha256']==sha(HERE/'original/certificate/reopt_full_actual_extension.py')
    assert priced['source_sha256']==new['seed_sha256']==sha(HERE/'original/certificate/full_actual_extension_discovery.json')
    assert new['negative_columns_sha256']==sha(HERE/'original/maxroot/known_actual_extension_pricing.json')
    assert exact['discovery_sha256']==sha(HERE/'original/certificate/full_actual_extension_known_v1_discovery.json')
    names=seed['row_names']; assert names==new['row_names']==list(exact['row_slacks']) and len(names)==len(set(names))==7497
    assert sum(n.startswith('actual-extension:') for n in names)==747 and 'Actual13TrueHQRProjection' not in names
    assert len(seed['atoms'])==len(seed['primal_float'])==504
    seedstates=defaultdict(set)
    for a in seed['atoms']:
        atom(a,True); seedstates[key(a)].add(a['actual_HQR_bits'])
    assert len(seedstates)==63 and all(v=={''.join(map(str,s)) for s in product((0,1),repeat=3)} for v in seedstates.values())
    assert priced['known_old_types']==849 and priced['priced_columns']==6792 and priced['negative_columns']==len(priced['new_columns'])==119
    assert priced['active_old_rows']==45 and priced['active_extension_rows']==24 and priced['sparse_full_coefficient_checks']==12*69==828
    incoming=[c['atom'] for c in priced['new_columns']]
    for c in priced['new_columns']:
        atom(c['atom'],True,'exact_mass' in c['atom']); assert c['residual_float'] < -1e-7
    assert [c['residual_float'] for c in priced['new_columns']]==sorted(c['residual_float'] for c in priced['new_columns'])
    dedup={}
    for a in seed['atoms']+incoming:
        cleaned={k:v for k,v in a.items() if k!='exact_mass'}
        dedup.setdefault(key(a,True),cleaned)
    assert list(dedup.values())==new['atoms'] and len(new['atoms'])==len(new['primal_float'])==623
    for a in new['atoms']: atom(a,True)
    assert set(new['dual_multipliers_float'])<=set(names)
    assert set(seed['dual_multipliers_float'])<=set(names)
    assert all(v>0 for d in (seed,new) for v in d['dual_multipliers_float'].values())
    projected={}; agg=defaultdict(F); split=Counter()
    for a in exact['atoms']:
        atom(a,mass=True); assert key(a) not in projected; projected[key(a)]=F(a['exact_mass'])
    for a in exact['actual_HQR_lift']:
        atom(a,True,True); assert key(a,True) in dedup
        agg[key(a)]+=F(a['exact_mass']);split[key(a)]+=1
    assert projected==dict(agg) and len(projected)==exact['positive_projected_atoms']==64
    assert len(exact['actual_HQR_lift'])==exact['positive_extended_atoms']==85
    totals={}
    for field in ('atoms','actual_HQR_lift'):
        aa=exact[field]
        w=sum((F(a['exact_mass'])*int('1' in a['bits'][:5]) for a in aa),F())
        o=sum((F(a['exact_mass'])*int(any(a['AB_hist'][4:])) for a in aa),F())
        assert w==F(exact['welfare'])==1 and o==F(exact['comparison_cover']) and o-2==F(exact['gap_above_two'])>0
        totals[field]={'W':str(w),'O':str(o),'gap':str(o-2),'d_counts':dict(Counter(atom(a,field=='actual_HQR_lift',True) for a in aa))}
    slacks={n:F(v) for n,v in exact['row_slacks'].items()};assert min(slacks.values())==F(exact['minimum_exact_slack'])==0
    stats={'stored_slacks':len(slacks),'negative_stored_slacks':sum(v<0 for v in slacks.values()),'zero_stored_slacks':sum(v==0 for v in slacks.values()),'positive_stored_slacks':sum(v>0 for v in slacks.values()),'zero_extension_stored_slacks':sum(v==0 for n,v in slacks.items() if n.startswith('actual-extension:')),'distinct_stored_slack_values':len(set(slacks.values()))}
    reports={}
    for p in sorted((HERE/'original').glob('*/*.json')):
        d=json.loads(p.read_text()); reports[p.name]={'top_level_fields':list(d),'all_scalar_leaves_consumed':leaves(d)}
    diag=load('certificate/full_actual_extension_diagnostic.json');diag2=load('certificate/full_actual_extension_diagnostic_v2.json')
    assert diag['old_rows']==6751 and diag2['old_rows']==seed['old_rows']==6750
    assert diag['source_exact_point_sha256']==diag2['source_exact_point_sha256']==seed['source_exact_point_sha256']=='5930c355483c801f535ef2385e1907fc27d0cae25f10c4d74d83d973ebe96f98'
    result={'status':'passed','scope':'Frozen data identities/domain/aggregation/stored signs only; no 7497-row coefficient reconstruction, LP, dual pricing, full-policy or independent exact primal certification.', 'fingerprints':fingerprints,'all_report_fields':reports,'row_families':dict(Counter(n.split(':')[0] for n in names)),'columns':{'seed_extended':504,'seed_projected':63,'priced_new':119,'priced_columns_with_inert_old_exact_mass':sum('exact_mass' in a for a in incoming),'reoptimized_extended':623,'reoptimized_projected':len({key(a) for a in new['atoms']}),'positive_extended':85,'positive_projected':64,'projected_split_counts':dict(Counter(split.values()))},'totals':totals,'saved_slack_review':stats,'historical_seconds':{'pricing':priced['seconds'],'exact_recovery':exact['seconds']},'execution_account':{'original_math_entrypoints':0,'LP':0,'row_engines':0,'full_SPE_checks':0,'new_saved_data_integrity_checker_successful_runs':1,'earlier_failed_saved_data_checker_runs':1,'total_saved_data_checker_invocations_this_delivery':2}}
    (HERE/'saved-data-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','columns','saved_slack_review','execution_account')},ensure_ascii=False))
if __name__=='__main__':main()
