"""Main's explicit, exclusive release of the already audited full v6 system."""
from pathlib import Path
from hashlib import sha256
import json
import os
from datetime import datetime, timezone

R = Path(__file__).resolve().parents[4]
W = R / 'research/workspaces/six-boss1-20261111'
P = W / 'visible_maximum_joint_v6'
S = W / 'visible_maximum_joint_v6_solve'

def read(p):
    return json.loads(p.read_text())

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

def relative(p):
    return str(p.relative_to(R))

def write_new(p, value):
    with p.open('x') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
        f.flush()
        os.fsync(f.fileno())

assert not (S / 'single_lp_consumed.json').exists()
assert not (S / 'main_release.json').exists()
main = W / 'main_visible_c_v6_preflight.json'
audit = read(main)
assert audit['status'] == 'PASS_MAIN_FULL4177_LITERAL_SOURCE_CONCATENATION_AND_CORRECT_MODEL'
assert audit['all_rational_column_positions_checked'] == 2142801
assert audit['input_sha256'] == digest(P / 'exact_input.json') == '8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769'
assert audit['preparation_manifest_sha256'] == digest(P / 'freeze_manifest.json') == '0aa45d8f1517b6958ae6187b5ebbf89a3ea31926347d997a696fe20fd4b35da2'
assert digest(S / 'scaffold_manifest.json') == '4f9f1389eb6fd6fe3030c0ce37c2a20f2a3116152ad9857a9e0314f2f57fbac1'
erratum = W / 'visible_maximum_joint_v6_model_erratum.md'
assert digest(erratum) == 'a2b83e67ce90597faa005cb893da647555bbb58b0d502fd3f03c12db924172b7'
model = R / 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'
assert digest(model) == 'cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88'
source_audits = []
for name, expected in audit['independent_source_true_cost_and_domain_checks'].items():
    p = W / name
    assert digest(p) == expected
    d = read(p)
    assert d['status'].startswith('PASS')
    source_audits.append({'path': relative(p), 'sha256': expected, 'status': d['status']})
semantic = {
    'status': 'PASS_MAIN_V6_SOURCE_SCOPE_AND_REQUIRED_X_ERRATUM',
    'owner': 'Boss1', 'RUN': 'six-boss1-20261111', 'author': '/root',
    'input_sha256': audit['input_sha256'],
    'model': {'path': relative(model), 'sha256': digest(model)},
    'mandatory_erratum': {'path': relative(erratum), 'sha256': digest(erratum)},
    'X': 'Choose once from argmax_Q sum_{y in Q} 1/(P_y+1), P_y=sum_{j=1}^4 1[y in A_j], over the whole common legal catalog. This same X is used everywhere.',
    'C': 'One whole-catalog maximum bare-coverage legal label, K=|C|; it need not maximize the actual-prefix potential.',
    'O': 'A union of six legal labels attaining OPT6. Normalize only when OPT6>0; zero OPT6 is immediate in the original model.',
    'domain': 'Every finite unit-client game, finite nonempty labeled catalog, and every complete ordered-history pure SPE, with weak ties, aliases, repeated actions and empty coverage preserved.',
    'new_local_T': 'Arbitrary legal T in the new local sources specializes to the globally chosen X; it does not remove inherited X maximality.',
    'checked_true_source_audits': source_audits,
    'full_raw_main_audit': {'path': relative(main), 'sha256': digest(main)},
    'mathematical_boundary': 'These are necessary constraints, not a full SPE characterization. A value below one half or an LP feasible point is not a counterexample.',
    'optimizer_calls_by_this_release_builder': 0,
    'frozen_coefficients_or_scaffold_changed': False,
}
semantic_path = W / 'main_v6_semantic_release.json'
write_new(semantic_path, semantic)
d = read(S / 'main_release.template.json')
d.update(status='MAIN_EXPLICIT_FULL4177_RAW_V6_SINGLE_LP_RELEASE', authorized_by='/root',
         optimizer_calls_authorized=1, input_read_authorized=True,
         source_closure_read_authorized=True, planning_contract_confirmed=True)
d['explicit_main_instruction'] = (
    'Main explicitly releases exactly one full4177/513/2 highs-ds call using the frozen input and options. '
    'First read and SHA-check the mandatory independent X erratum and this semantic release; '
    'the two overbroad frozen X sentences are superseded by this exact original-model scope. '
    'Run released preflight; on any mismatch stop without consuming an optimizer call. '
    'After the sole call, recover an exact primal-dual certificate, independently verify every original row and column, '
    'compute the full optimal face and all new positive-payment diagnostics. Never rerun the optimizer, omit rows, '
    'replace original metadata, assume the old C face, or treat a necessary LP point as a full SPE.'
)
for name, key in [
    ('exact_input.json', 'input_sha256'), ('freeze_manifest.json', 'preparation_manifest_sha256'),
    ('numerical_scaling.json', 'scaling_sha256'), ('row_catalog.json', 'row_catalog_sha256'),
    ('source_review.md', 'source_review_sha256'), ('source_pins.json', 'source_pins_sha256')]:
    d[key] = digest(P / name)
d['scaffold_manifest_sha256'] = digest(S / 'scaffold_manifest.json')
names = [row['name'] for row in read(P / 'exact_input.json')['raw_rows']]
d['raw_row_order_sha256'] = sha256(json.dumps(names, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
for actual, planned in [('expected_dimensions', 'planned_dimensions_reference_only'),
                        ('expected_row_blocks', 'planned_row_blocks_reference_only'),
                        ('expected_appended_scaling', 'planned_appended_scaling_reference_only'),
                        ('solver', 'planned_solver_reference_only'),
                        ('solver_options', 'planned_solver_options_reference_only'),
                        ('preparation_manifest_count_pointers', 'planned_count_pointers_reference_only')]:
    d[actual] = d[planned]
d['source_validity_scope'] = dict.fromkeys(d['source_validity_scope'], True)
for key in ['input', 'scaling']:
    d['literal_parent'][key + '_sha256'] = digest(R / d['literal_parent'][key + '_path'])
assert d['literal_parent']['input_sha256'] == '12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac'
d['required_evidence'] = []
for role in ['main_preflight', 'all_raw_column_audit']:
    d['required_evidence'].append({'role': role, 'path': relative(main), 'sha256': digest(main),
        'expected_status': audit['status'], 'status_pointer': '/status', 'input_sha256_pointer': '/input_sha256',
        'expected_json_values': {'/raw_rows': 4177, '/variables': 513, '/equalities': 2,
                                 '/all_rational_column_positions_checked': 2142801}})
d['required_evidence'].append({'role': 'source_legality', 'path': relative(semantic_path),
    'sha256': digest(semantic_path), 'expected_status': semantic['status'], 'status_pointer': '/status',
    'expected_json_values': {'/input_sha256': d['input_sha256'], '/mandatory_erratum/sha256': digest(erratum)}})
d['mandatory_model_erratum'] = semantic['mandatory_erratum']
d['semantic_release'] = {'path': relative(semantic_path), 'sha256': digest(semantic_path)}
d['source_checkpoint'] = 'b03738737870367e2da8a091d4d6f0e26b16d892'
d['released_at_utc'] = datetime.now(timezone.utc).isoformat()
d['local_release_publication_state'] = 'Main-created locally; source packages are already pushed. Preserve release and consumption marker in the next serial checkpoint.'
write_new(S / 'main_release.json', d)
print(json.dumps({'status': d['status'], 'release_sha256': digest(S / 'main_release.json'),
                  'semantic_release_sha256': digest(semantic_path), 'input_sha256': d['input_sha256'],
                  'optimizer_calls': 0, 'source_checkpoint': d['source_checkpoint']}))
