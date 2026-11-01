from pathlib import Path
import hashlib, json
base=Path(__file__).resolve().parents[1]
checks=[]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def same(g,f):
    assert g.read_bytes()==f.read_bytes(), (g,f)
    return {'generated':str(g),'frozen':str(f),'bytes':g.stat().st_size,'sha256':sha(g)}
# Byte exact generated-report preservation.
checks.append(same(base/'237a9c14a68cbe08a526/coverage_geometry_audit.json', base.parent/'clean-show/10b27e972bf58a53c84e.coverage_geometry_audit.json'))
checks.append(same(base/'3bcc00f6fc8a8ac6756c/positive_moment_locality_audit.json', base.parent/'clean-show/ae25ad82555f3e1b6d27.positive_moment_locality_audit.json'))
checks.append(same(base/'02ff2fdb8846b201e378/root_independent_audit.json', base.parent/'clean-show/b1ce857888be2dae3928.root_independent_audit.json'))
g=json.loads((base/'237a9c14a68cbe08a526/coverage_geometry_audit.json').read_text())
assert g['identity'].endswith('general half remains OPEN')
assert len(g['spaces'])==22 and all(x['ranks_coverage_payoff_potential_terminal_differences'][0:3]==[x['dimension']]*3 for x in g['spaces'])
assert len(g['full_ordered_history_strategies'])==7
assert all(x['last_all_root_ranks'][1:]==[x['last_all_root_ranks'][0],x['last_all_root_ranks'][0]+1] for x in g['full_ordered_history_strategies'])
assert len(g['exposed_rays'])==7 and g['exposed_rays'][0]['nonzero_proper_exposure'] is False
assert [x['final_positive_types'] for x in g['adaptive_sparse_reduction']]==[4,15,15,24,7]
p=json.loads((base/'3bcc00f6fc8a8ac6756c/positive_moment_locality_audit.json').read_text())
assert p['identity'].startswith('PM-1/PM-2/PM-3') and len(p['cases'])==6
assert sum(x['full_nonempty_types_checked'] for x in p['cases'])==21834
assert sum(x['local_single_pair_moments_checked'] for x in p['cases'])==502
assert all(x['all_maximal_proper_restriction_classes_realizable'] for x in p['cases'])
assert all(str(x['dual_value_at_fake_data']).startswith('-') for x in p['cases'])
r=json.loads((base/'02ff2fdb8846b201e378/root_independent_audit.json').read_text())
assert r['scope'].endswith('no welfare theorem') and len(r['rank_cases'])==20 and r['exposing_functional_pairs']==86368 and r['m1_exception_checked'] is True
print(json.dumps({'status':'pass','byte_exact_reports':len(checks),'geometry_space_cases':len(g['spaces']),'geometry_strategy_cases':len(g['full_ordered_history_strategies']),'geometry_exposure_pairs':sum(x['ordered_nonempty_type_pairs'] for x in g['exposed_rays']),'positive_full_types':sum(x['full_nonempty_types_checked'] for x in p['cases']),'positive_local_moments':sum(x['local_single_pair_moments_checked'] for x in p['cases']),'root_rank_cases':len(r['rank_cases']),'root_exposing_pairs':r['exposing_functional_pairs']},ensure_ascii=False,indent=2))
