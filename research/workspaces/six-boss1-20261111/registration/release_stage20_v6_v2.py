"""Main issues a fresh one-call release after reviewing the strict schema fix."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import os

R = Path(__file__).resolve().parents[4]
W = R / 'research/workspaces/six-boss1-20261111'
OLD = W / 'visible_maximum_joint_v6_solve'
NEW = W / 'visible_maximum_joint_v6_solve_v2'

def read(p): return json.loads(p.read_text())
def digest(p): return sha256(p.read_bytes()).hexdigest()
def relative(p): return str(p.relative_to(R))

assert not (OLD / 'single_lp_consumed.json').exists()
assert not (NEW / 'single_lp_consumed.json').exists()
assert not (NEW / 'main_release.json').exists()
revocation = W / 'registration/v6_first_release_revoked.json'
revoked = read(revocation)
assert revoked['status'] == 'MAIN_RELEASE_REVOKED_BEFORE_ANY_OPTIMIZER_CALL'
assert revoked['optimizer_calls_consumed'] == 0
assert revoked['release_sha256'] == digest(OLD / 'main_release.json') == 'eef504e3ad50d3e2f901e12a8689a95415986be2552c73cd885041e4d8dbdbaf'
review = W / 'main_v6_solver_v2_review.json'
rv = read(review)
assert rv['status'] == 'PASS_MAIN_V2_STRICT_SOURCE_INTERFACE_REVIEW'
assert rv['validate_model_AST_exactly_unchanged'] and rv['strict_44_source_entries_and_order_exact']
assert digest(NEW / 'scaffold_manifest.json') == rv['scaffold_manifest_sha256'] == '3f16193e13ac0cb04c4f3272fc068e4922adf661a3b41d627ad64b87db244ec8'
repair = NEW / 'repair_preflight_result.json'
assert digest(repair) == '19f34854460bad3cc94f0a20059f0a85323e135156567e2ef14c450105bf7543'
rp = read(repair)
assert rp['status'] == 'PASS_ZERO_OPTIMIZER_REPAIR_FULL4177_SOURCE_PIN_INTERFACE'
assert rp['exact_source_pin_file_contents_SHA_checked'] == rp['exact_source_pin_file_byte_counts_checked'] == 44
assert rp['total_optimizer_calls'] == 0

# Prior file supplies immutable, already audited input references only. Main
# creates the authority below, for this new reviewed package and this call.
prior = read(OLD / 'main_release.json')
d = read(NEW / 'main_release.template.json')
fields = ['input_path','input_sha256','preparation_manifest_sha256','scaling_sha256',
          'row_catalog_sha256','source_review_sha256','source_pins_sha256','raw_row_order_sha256',
          'expected_dimensions','expected_row_blocks','expected_appended_scaling','source_validity_scope',
          'literal_parent','preparation_manifest_count_pointers','required_evidence',
          'mandatory_model_erratum','semantic_release','solver','solver_options']
for field in fields: d[field] = prior[field]
assert d['input_sha256'] == '8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769'
assert d['schema'] == 'visible_maximum_joint_v6_solve_v2_main_release_v1'
assert d['solver_package'] == 'visible_maximum_joint_v6_solve_v2'
d.update(status='MAIN_EXPLICIT_FULL4177_RAW_V6_SOLVE_V2_SINGLE_LP_RELEASE',
         authorized_by='/root', optimizer_calls_authorized=1, input_read_authorized=True,
         source_closure_read_authorized=True, planning_contract_confirmed=True,
         scaffold_manifest_sha256=digest(NEW/'scaffold_manifest.json'))
d['explicit_main_instruction'] = (
    'Main has personally read the exact interface patch and verified all20 scaffold artifacts, '
    'the unchanged full mathematical validator and six unchanged optimizer/recovery/checker programs. '
    'The old release is revoked and never consumed. Main now explicitly authorizes exactly one '
    'full4177/513/2 highs-ds call in this new package, with all published source pins checked. '
    'First perform the actual released preflight; any mismatch stops before consumption. '
    'Keep the true actual-prefix-maximal X condition, maximum-bare C and O=OPT6 semantics. '
    'Use only solve_once.py, preserve the durable exclusive marker, never rerun or remove raw constraints. '
    'On successful discovery recover and independently verify every exact row/column, the complete '
    'optimal face and its own fresh true-payment branches. New cap3/rootCAP4 rows are not part of '
    'this frozen input. A necessary LP point is not a complete SPE counterexample.'
)
d['required_evidence'].extend([
    {'role':'main_solver_interface_review','path':relative(review),'sha256':digest(review),
     'expected_status':rv['status'],'status_pointer':'/status',
     'expected_json_values':{'/original_and_v2_optimization_consumption':0,
                             '/validate_model_AST_exactly_unchanged':True}},
    {'role':'strict_interface_full_zero_optimizer_load','path':relative(repair),'sha256':digest(repair),
     'expected_status':rp['status'],'status_pointer':'/status',
     'expected_json_values':{'/exact_source_pin_file_contents_SHA_checked':44,
                             '/all_raw_rows_checked':4177,'/all_nonnegative_columns_checked':513,
                             '/free_equalities_checked':2,'/total_optimizer_calls':0}}
])
d['replaces_revoked_zero_consumption_release'] = {'path':relative(revocation),'sha256':digest(revocation)}
d['released_at_utc'] = datetime.now(timezone.utc).isoformat()
d['notice'] = 'Actual Main release for the reviewed solver-v2 package. The one original-system discovery budget has not yet been consumed. Only this package may now consume it.'
with (NEW/'main_release.json').open('x') as f:
    f.write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    f.flush();os.fsync(f.fileno())
print(json.dumps({'status':d['status'],'release_sha256':digest(NEW/'main_release.json'),
                  'input_sha256':d['input_sha256'],'optimizer_calls_consumed':0}))
