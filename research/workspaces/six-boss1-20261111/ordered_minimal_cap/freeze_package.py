#!/usr/bin/env python3
"""Bind the finished local proof package; no model inputs or optimizer touched."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
BASE=HERE.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((HERE/name).read_text())


def save(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


pins=load('source_pins.json')['pins']
for name,expected in pins.items():
    path=Path(name) if name.startswith('/') else BASE/name
    assert digest(path)==expected,('source changed',name)
assert pins['source2_minimal_cap_safe/freeze_manifest.json']=='d63c117b0adf2353f70ffaf7d959dd91e8c4ee378838f7e5f4af6e99c86861ec'
literal=load('literal_checker_output.json')
geometry=load('geometry_counts.json')
family=load('exact_family.json')
review=load('proof_review.json')
assert literal['status']=='PASS'
assert literal['rows']==family['raw_row_count']==geometry['total_vertices']==137
assert literal['full_row_coefficients']==137*513
assert review['review_status']=='PASS'
assert family['source_vertex_counts']=={'1':90,'2':28,'3':12,'4':5,'5':2}
assert family['no_C_size_equality'] and not family['row_pruning']
assert literal['input_files_all_local_JSON'] and not literal['generator_imported_or_executed']
files=sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in ['freeze_manifest.json','SHA256SUMS'])
hashes={p.name:digest(p) for p in files}
manifest={
    'schema':'ordered_minimal_cap_frozen_v1',
    'status':'FROZEN_FOR_MAIN_REVIEW_NOT_IMPORTED_TO_LP',
    'run':'six-boss1-20261111',
    'package':'ordered_minimal_cap',
    'scope':'Exact complete vertex generator for the specified q0=1/5 minimal-cap outer-six inner-other-five ordered-menu affine family, sources 1 through 5.',
    'sources':[1,2,3,4,5],
    'source_vertex_counts':family['source_vertex_counts'],
    'raw_rows':137,
    'variables':513,
    'K_column':512,
    'K_coefficient':'S=1+sum(beta_j)',
    'true_source_IC_weight':'25+sum(tau_j)-s',
    'numeric_positive_divisor':'25',
    'outer_menu_indices':6,
    'inner_query_indices':5,
    'inner_excludes_only_same_index':True,
    'uses_C_size_equality':False,
    'all_root_vertices_retained':True,
    'all_zero_and_duplicate_types_retained':True,
    'all_weak_ties_retained':True,
    'all_64_menus_verified':True,
    'independent_geometry':'true-state-derived facets, exact edge clipping',
    'independent_literal_checker':'local JSON inputs only, no generator import or execution',
    'bearing_steps_review':'PASS',
    'full_rho_affine_forms':114,
    'full_rho_vertex_checks':4164,
    'hidden_states':literal['hidden_states'],
    'physical_condition_minima':literal['physical_condition_minima'],
    'all_tied_tail_occurrences':literal['all_tied_tail_occurrences'],
    'full_row_coefficients':literal['full_row_coefficients'],
    'source_bindings':pins,
    'files':hashes,
    'optimizer_calls':0,
    'LP_points_read':0,
    'unified_inputs_modified':False,
    'Git_or_RUN_modified':False,
    'active_all_source_minimal_cap_safe_read':False,
    'all_possible_wallet_optimality_claimed':False,
    'SPE_realizability_claimed':False,
    'half_status':'OPEN',
    'manifest_hash_is_in_SHA256SUMS':True,
}
save('freeze_manifest.json',manifest)
all_hashes=dict(hashes);all_hashes['freeze_manifest.json']=digest(HERE/'freeze_manifest.json')
(HERE/'SHA256SUMS').write_text(''.join(f'{all_hashes[name]}  {name}\n' for name in sorted(all_hashes)))
print(json.dumps({'status':manifest['status'],'manifest_sha256':all_hashes['freeze_manifest.json'],'exact_family_sha256':hashes['exact_family.json'],'proof_sha256':hashes['proof.md'],'literal_checker_output_sha256':hashes['literal_checker_output.json'],'files_bound':len(hashes),'raw_rows':137,'variables':513},ensure_ascii=False))
