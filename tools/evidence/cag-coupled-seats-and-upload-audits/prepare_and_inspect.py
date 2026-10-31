"""Read/validate real dependency fields, preserve exact bytes, prepare safe mirror.

No primary auditor, upstream self-test, search CLI, Git or network is executed.
"""
from pathlib import Path
from fractions import Fraction
from itertools import product
from collections import Counter
import hashlib
import importlib.metadata
import json

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'tools/evidence/cag-coupled-seats-and-upload-audits'
sources = json.loads((E / 'source-manifest.json').read_text())
deps = json.loads((E / 'dependency-manifest.json').read_text())
all_rows = sources + deps
byid = {r['id']: r for r in all_rows}
counts = Counter()

def walk(x):
    counts[type(x).__name__] += 1
    if isinstance(x, dict):
        for k, v in x.items():
            assert isinstance(k, str)
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)
    else:
        assert type(x) in (int, str, bool, float, type(None))

mirror = E / 'replay-tree'
packs = {}
for row in all_rows:
    raw = (ROOT / row['saved_path']).read_bytes()
    assert len(raw) == row['size'] and hashlib.sha256(raw).hexdigest() == row['sha256']
    dst = mirror / row['path']
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(raw)
    if row['path'].endswith('.json'):
        packs[row['id']] = json.loads(raw)
        walk(packs[row['id']])

prefix = packs['6d08e55bce1a5336932c']
inst = prefix['instance']
assert inst['players'] == 3 and len(inst['topics']) == 5 and len(prefix['rows']) == 3
assert sum(c['multiplicity'] for c in inst['customers']) == 124
assert all(type(c['multiplicity']) is int and c['multiplicity'] > 0 and
           c['topics'] and all(type(a) is int and 0 <= a < 5 for a in c['topics'])
           for c in inst['customers'])
assert prefix['path'] == [0, 4, 2]

manifest = packs['3617ba0356de807577c2']
upload_ids = ['e01fef9e2ba26f1fd0e2', 'e19d793c64bcdc37ccd0',
              'f6081a79c3dc3cb6c4db', '453b0dc560ab17fdf1ac']
for ident in upload_ids:
    row = byid[ident]
    assert manifest[Path(row['path']).name] == row['sha256']
cert = packs['e19d793c64bcdc37ccd0']
assert set(cert) == {'status', 'm', 'n', 'weights', 'target', 'policy'}
assert cert['m'] == 12 and cert['n'] == 4
weights = {int(k): v for k, v in cert['weights'].items()}
assert set(weights) == set(range(1, 4096))
assert all(type(v) is int and v > 0 for v in weights.values())
assert sum(weights.values()) == 26171145 and min(weights.values()) == 1 and max(weights.values()) == 15091
policy = {tuple(r['history']): r['action'] for r in cert['policy']}
assert len(policy) == len(cert['policy']) == 1885
assert set(policy) == {h for d in range(4) for h in product(range(12), repeat=d)}
assert all(type(a) is int and 0 <= a < 12 for a in policy.values())
assert cert['target'] == [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]

random_old = packs['bd8eb256f44a2cc7e18c']
assert random_old['all_checks_passed'] and random_old['source_sha256'] == byid['24f446797606924d0916']['sha256']
uploaded_old = packs['f1acdd55c80eb7a7df09']
assert uploaded_old['audit_program_sha256'] == byid['9d31cb84f11929de63c3']['sha256']
assert uploaded_old['original_sha256_manifest'] == manifest
assert uploaded_old['input_certificate_sha256'] == byid['e19d793c64bcdc37ccd0']['sha256']
assert uploaded_old['uploaded_program_sha256'] == byid['f6081a79c3dc3cb6c4db']['sha256']
assert uploaded_old['original_sha256_manifest_file_sha256'] == byid['3617ba0356de807577c2']['sha256']
assert uploaded_old['saved_policy_replay']['comparisons_including_chosen_actions'] == 22620

result = {
    'status': 'passed-input-byte-and-structure-readiness', 'all_related_JSON_fields_traversed': True,
    'field_types': dict(counts),
    'prefix_input': {'unit_customers': 124, 'players': 3, 'topics': 5, 'path': prefix['path'],
                     'source_contains_strategy': False, 'all_11_customer_types_and_3_claimed_rows_read': True},
    'uploaded_certificate': {'interest_masks': 4095, 'unit_customers': 26171145,
        'ordered_policy_rows': 1885, 'all_actual_schema_values_checked': True,
        'numeric_read_scope': 'full keys/status/parameters/target and vector structure read; all integers retained and exact old run binds full certificate; not human word-for-word reading every numeric digit'},
    'reused_runs': {'random': {'same_primary_code_SHA': True, 'no_project_dependencies': True},
        'uploaded': {'same_primary_code_SHA': True, 'same_four_original_file_SHA_chain': True,
            'large_definition_replay': 'exact same code and complete certificate bound',
            'tiny_comparators': 'old successful 209-case report retained; it does not list search/canonical code SHAs, so not retrocertified against every current dependency',
            'new_CLI_executions': 0}},
    'numpy_installed_version_read_only_probe': importlib.metadata.version('numpy'),
    'uploaded_old_numpy_version': uploaded_old['numpy_version'],
    'uploaded_late_metadata_dependency': 'original CLI calls git rev-parse 8f9bcf4 in ROOT after all math; isolated mirror has no such history; no fake ref, no shared Git access or needless repeat',
    'canonical_code_dependencies': 'four exact previously full-read code SHAs reused, no new code run',
    'new_runs_planned': ['prefix raw CLI once with fresh output', 'priced projection raw CLI once', 'nine-plus arithmetic raw CLI once'],
    'additional_related_sources_done': 0,
}
(E / 'input-structure-and-run-readiness.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'sources': len(sources), 'dependencies': len(deps), 'old_same_SHA_runs_reused': 2,
                  'planned_new_primary_CLI_runs': 3, 'numpy': result['numpy_installed_version_read_only_probe']}))
