"""Static source/data inventory only: never imports a frozen research module.

No LP, BI, IC validation, equilibrium oracle, or native entry point runs here.
Every JSON leaf is consumed for an exhaustive typed leaf digest; the large
pressure strategy is also losslessly encoded by complete ordered levels.
"""
from pathlib import Path
from itertools import product
import ast
import hashlib
import json
import shutil

REPO = Path('/workspace/scratch/5158eb3789b3/boss7-cleaner')
STAGE = Path('/workspace/scratch/5158eb3789b3/boss7-staging/rcd-row')
WORK = REPO / 'cleanup/workspaces/Boss7/resume-current-20261102'
EVIDENCE = STAGE / 'evidence'
ids = json.loads((WORK / 'rcd-claimed-groups.json').read_text())['induction_row']
metadata = {r['id']: r for r in json.loads((WORK / 'rcd-prepared-sources.json').read_text())}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def leaves(value, pointer=''):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from leaves(item, pointer + '/' + key.replace('~', '~0').replace('/', '~1'))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from leaves(item, pointer + '/' + str(index))
    else:
        yield [pointer, type(value).__name__, value]

inventory = []
for source_id in ids:
    entry = metadata[source_id]
    raw = (WORK / 'rcd-prepared-raw' / source_id).read_bytes()
    assert len(raw) == entry['size'] and sha(raw) == entry['sha256']
    dst = EVIDENCE / 'original' / entry['path']
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(raw)
    record = {'id': source_id, 'path': entry['path'], 'size': len(raw), 'sha256': sha(raw)}
    if entry['path'].endswith('.py'):
        tree = ast.parse(raw)
        record['ast_parsed_only'] = True
        record['functions'] = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        record['imports_not_executed'] = [ast.unparse(n) for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
    if entry['path'].endswith('.json'):
        value = json.loads(raw)
        atoms = list(leaves(value))
        record['root_keys'] = list(value)
        record['all_scalar_leaves_consumed'] = len(atoms)
        record['typed_leaf_stream_sha256'] = sha(json.dumps(atoms, ensure_ascii=False, separators=(',', ':')).encode())
    inventory.append(record)

pressure = json.loads((WORK / 'rcd-prepared-raw/ba927fc3db4af6fae727').read_text())
policy_rows = pressure['strategy']['actions']
policy = {tuple(r['history']): r['action'] for r in policy_rows}
expected = [h for d in range(5) for h in product(range(8), repeat=d)]
assert len(policy_rows) == len(policy) == len(expected) == 4681
assert list(policy) == expected
assert all(isinstance(a, int) and 0 <= a < 8 for a in policy.values())
levels = [''.join(str(policy[h]) for h in product(range(8), repeat=d)) for d in range(5)]
assert sum(map(len, levels)) == 4681
assert all(policy[h] == int(levels[len(h)][sum(a * 8 ** (len(h)-i-1) for i, a in enumerate(h))]) for h in expected)
customers = pressure['endpoint']['customers']
assert len(customers) == 39
assert all(isinstance(r['multiplicity'], int) and r['multiplicity'] > 0 for r in customers)
assert all(r['topics'] and len(set(r['topics'])) == len(r['topics']) and all(0 <= a < 8 for a in r['topics']) for r in customers)
old_pressure = REPO / 'archives/customer-attraction/tools/evidence/last-profit-pressure-two-cone-inputs-primary/source-root/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/repeated_upgrade_attempt_m5.json'
old = json.loads(old_pressure.read_bytes())
assert pressure['strategy'] == old['strategy']
pressure_index = {
    'root_fields': {k: v for k, v in pressure.items() if k not in ('endpoint', 'strategy')},
    'endpoint': pressure['endpoint'],
    'strategy_terminal_counts': pressure['strategy']['terminal_counts'],
    'ordered_action_encoding': 'complete levels in lexicographic product(range(8),repeat=depth); depth 0..4; one action digit per ordered history',
    'strategy_action_levels': levels,
    'exact_actions_reconstructed_in_original_order': True,
    'old_source': str(old_pressure.relative_to(REPO)),
    'old_source_sha256': sha(old_pressure.read_bytes()),
    'strategy_equals_old_source': True,
    'endpoint_equals_old_source': pressure['endpoint'] == old['endpoint'],
    'endpoint_unit_count': sum(r['multiplicity'] for r in customers),
    'endpoint_positive_types': len(customers),
    'inspection_scope': 'all records consumed; schema/history coverage/order and old-strategy identity only; no payoff/IC/LP rerun',
}

named = json.loads((WORK / 'rcd-prepared-raw/649e5c0cf63cf4d1d607').read_text())
input_paths = [
    REPO / 'archives/customer-attraction/tools/evidence/direct-surplus-compact-wallet-primary/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/tree/compact_strongA_independent.json',
    REPO / 'archives/customer-attraction/tools/evidence/strong-adjacent-discovery-and-simplification-programs-primary/source-root/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/strong_adjacent_gap_attack.json',
    REPO / 'archives/customer-attraction/tools/evidence/direct-root-floor-and-helper-five-primary/related/430dbf178a40e324cba1/root_standalone_helper_exact_counterexample.json',
]
input_index = []
for report, path in zip(named['reports'], input_paths):
    raw = path.read_bytes()
    assert sha(raw) == report['sha256']
    data = json.loads(raw)
    if 'topic_order' in data:
        m, k = 3, len(data['topic_order'])
        lookup = {s: i for i, s in enumerate(data['topic_order'])}
        p = {(): lookup[data['root']]}
        p.update({(a,): lookup[data['second'][a]] for a in range(k)})
        p.update({(a,b): lookup[data['terminal'][a][b]] for a,b in product(range(k),repeat=2)})
        types = [{'topics': r, 'multiplicity': 1} for r in data['customers']]
    else:
        ins = data.get('endpoint', data.get('instance'))
        cert = data.get('strategy', data.get('certificate'))
        m, k = ins['players'], len(ins['topics'])
        p = {tuple(r['history']): r['action'] for r in cert['actions']}
        types = ins['customers']
    assert (m,k) == (report['players'], report['topics'])
    assert set(p) == {h for d in range(m) for h in product(range(k),repeat=d)}
    assert all(0 <= a < k for a in p.values())
    atoms = list(leaves(data))
    input_index.append({'source_in_report': report['source'], 'existing_repo_path': str(path.relative_to(REPO)), 'sha256': sha(raw), 'size': len(raw), 'all_scalar_leaves_consumed': len(atoms), 'typed_leaf_stream_sha256': sha(json.dumps(atoms,separators=(',',':')).encode()), 'players': m, 'topics': k, 'complete_policy_records_consumed': len(p), 'customer_records_consumed': len(types), 'scope': 'byte identity and consumed-input structure only; no IC or comparator replay'})

helper = REPO / 'archives/customer-attraction/tools/evidence/last-profit-pressure-two-cone-inputs-primary/source-root/tests/audits/customer_attraction_strategy_lp.py'
helper_tree = ast.parse(helper.read_bytes())
coverage = next(n for n in helper_tree.body if isinstance(n,ast.FunctionDef) and n.name == 'coverage_row')
helper_record = {'existing_repo_path': str(helper.relative_to(REPO)), 'original_source_path': 'tests/audits/customer_attraction_strategy_lp.py', 'sha256': sha(helper.read_bytes()), 'size': helper.stat().st_size, 'read_parts': ['dot', 'payoff_row', 'coverage_row', 'StrategyCone complete implementation', 'integer_clones', 'instance_from_clones', 'independently_verify'], 'coverage_row_literal_ast': ast.unparse(coverage), 'duplicate_argument_boundary': 'coverage_row sums 1<<a without set; attack_weak_assignment passes replacement multisets, so repeated-slot alternative constraints can use carry masks instead of the actual union. The distinct target itself is unaffected.'}
for name, value in [('source-inspection.json',inventory), ('pressure-complete-field-index.json',pressure_index), ('named-input-bindings.json',input_index), ('dependency-helper-binding.json',helper_record), ('report-field-index.json',{'rootfree_named_pressure':named, 'weak_assignment_attack':json.loads((WORK/'rcd-prepared-raw/9823e13a1816e6297535').read_text())})]:
    (EVIDENCE / name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(EVIDENCE/'source-manifest.json').write_text(json.dumps([metadata[s] for s in ids],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'sources':len(inventory),'json_sources':sum('root_keys' in r for r in inventory),'pressure_policy_actions':len(policy),'pressure_types':len(customers),'named_input_bindings':len(input_index),'native_imports':0,'native_runs':0,'LP':0,'BI':0,'IC_replays':0},ensure_ascii=False))
