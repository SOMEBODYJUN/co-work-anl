"""Reconcile one prepared source supplement; never mutate canonical/old DONE."""
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'tools'))
import registration
import research_runtime as runtime

TASK = 'register-boss3-source-closure-0079-30'
OUT = ROOT / 'research/workspaces/p25-register-v2/Boss6/source-closure-0079'
SOURCE = ROOT / 'research/workspaces/p25-register-v2/Boss3/0079-evidence-closure'


def read(path):
    return json.loads(path.read_text())


def ref(path):
    return {'path': path.relative_to(ROOT).as_posix(),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


task_path = ROOT / f'research/operations/p25-register-v2/tasks/{TASK}.json'
task = read(task_path)
assert task['state'] == 'claimed' and task['owner'] == 'Boss6'
definition = task['definition']
candidate_path = SOURCE / 'schema2-supplement-candidate.json'
assert ref(candidate_path)['sha256'] == '9343d61ebb29fd9d610eb202b1778725b4e7cfa56fc9fd036f9f32cfef89bbac'
candidate = read(candidate_path)
canonical_path = ROOT / 'research/registry.json'
canonical_ref = ref(canonical_path)
canonical = read(canonical_path)
owners = {o['object_id']: o for o in canonical['objects']}
materials = {m['path']: m for m in canonical['materials']}

# Check the prepared freeze, rather than treating a README as its byte binding.
manifest = read(SOURCE / 'manifest.json')
manifest_checks = []
for item in manifest['files']:
    path = ROOT / item['path']
    actual = ref(path)
    assert actual['sha256'] == item['sha256']
    assert path.stat().st_size == item['bytes']
    manifest_checks.append(actual)

field_comparisons = []
new_refs = {}
all_refs = {}
direct_body_refs = []
for incoming in candidate['objects']:
    old = owners[incoming['object_id']]
    changes = sorted(k for k in set(incoming) | set(old)
                     if incoming.get(k) != old.get(k))
    assert changes == ['evidence', 'version'], (incoming['object_id'], changes)
    assert incoming['version'] == old['version'] + 1
    assert all(e in incoming['evidence'] for e in old['evidence'])
    added = [e for e in incoming['evidence'] if e not in old['evidence']]
    for e in [incoming['body'], *incoming['evidence']]:
        runtime.ref_bytes(ROOT, e)
        all_refs[json.dumps(e, sort_keys=True)] = e
    for e in added:
        new_refs.setdefault(json.dumps(e, sort_keys=True),
                            {'ref': e, 'object_ids': []})['object_ids'].append(incoming['object_id'])
    body = dict(incoming['body'])
    text = runtime.ref_bytes(ROOT, body).decode()
    headings = [h for h in runtime.heading_sections(text) if h[1] == 2]
    if 'section' not in body and headings:
        body['section'] = headings[0][0]
    if body not in direct_body_refs:
        direct_body_refs.append(body)
    field_comparisons.append({
        'object_id': incoming['object_id'],
        'canonical_version': old['version'],
        'canonical_record_pin': runtime.pin(old),
        'delivered_version': incoming['version'],
        'delivered_record_pin': runtime.pin(incoming),
        'truth_status': incoming['truth_status'],
        'changed_fields_only': changes,
        'body_and_all_mathematical_fields_preserved': True,
        'all_old_evidence_preserved': True,
        'new_evidence': added,
    })

assert len(new_refs) == 37
assert sum(len(x['new_evidence']) for x in field_comparisons) == 45

# Exact supplementary passages read to settle multi-claim pages and condition
# boundaries. Other mature proofs remain at their original complete references.
support_sections = [
    ('weighted-congestion', '定理/局部窄权带的Shapley份额势--定理.md', '两种权序与局部包络'),
    ('weighted-congestion', '定理/高次费用最小潜在权份额势--定理.md', '纯d次反例的小潜在份额必要条件'),
    ('weighted-congestion', '定理/高次费用最小潜在权份额势--定理.md', '固定有限正权向量的幂提升统一趋1'),
    ('weighted-congestion', '定理/完整锚定门的稳定集合与有限修复--定理.md', '完整等权类门及强支配'),
    ('weighted-congestion', '定理/完整锚定门的稳定集合与有限修复--定理.md', '全部稳定集合的三分支证明'),
    ('weighted-congestion', '构造/短窗网格分离的全状态近一反例--构造.md', '固定n的显式阈值及每固定c的全尾部'),
    ('facility-games', '引理/客户相关续局与纯负载费用变换的精确边界--引理.md', '纯NE与逐实现严格占优的单调变换'),
    ('facility-games', '构造/单交叠精确回应核心的长环与亚ρ坏族--构造.md', '一、每边n站的普通正整数长环'),
]
support_refs = []
for archive, name, title in support_sections:
    r = ref(ROOT / 'archives' / archive / 'state' / name)
    r['section'] = title
    runtime.read_ref(ROOT, r)
    support_refs.append(r)
calibration = ROOT / 'archives/weighted-congestion/state/反例/唯一精确均衡与共同尺度图势不相容--反例.md'
calibration_preamble = calibration.read_text().split('## 连自由')[0]

material_preservation = []
for row in candidate['materials']:
    old = materials[row['path']]
    assert row['sha256'] == old['sha256']
    assert set(old['object_ids']) <= set(row['object_ids'])
    if old['disposition'] == 'needs-decision':
        assert row['disposition'] == 'needs-decision'
    if row['disposition'] == 'objects':
        assert row['object_ids'] == old['object_ids']
    material_preservation.append({
        'path': row['path'], 'sha256': row['sha256'],
        'previous_disposition': old['disposition'],
        'disposition': row['disposition'],
        'previous_object_ids': old['object_ids'],
        'object_ids': row['object_ids'], 'lost_owners': [],
    })

# Other candidates are protected input, not silently absorbed by this task.
fragments = read(SOURCE / 'owner-acceptance-fragments.json')
protected_candidates = []
for item in fragments['candidate_bases_checked']:
    path = ROOT / item['ref']['path']
    actual = ref(path)
    assert actual == item['ref']
    d = read(path)
    overlap = sorted(set(o['object_id'] for o in d['objects']) &
                     set(o['object_id'] for o in candidate['objects']))
    assert not overlap
    protected_candidates.append({'ref': actual, 'objects': len(d['objects']),
                                 'materials': len(d['materials']),
                                 'overlap_with_this_41': overlap,
                                 'handling': 'unchanged; 21 fragments remain with their original unique master candidates'})

old_done = []
ids = {o['object_id'] for o in candidate['objects']}
for path in (ROOT / 'research/registration/batches').glob('*.json'):
    if path.stem == TASK:
        continue
    t = ROOT / f'research/operations/p25-register-v2/tasks/{path.stem}.json'
    if not t.exists() or read(t).get('state') != 'done':
        continue
    d = read(path)
    overlap = [o for o in d.get('objects', []) if o['object_id'] in ids]
    if overlap:
        for o in overlap:
            assert o == owners[o['object_id']], (path, o['object_id'])
        old_done.append({'batch': ref(path),
                         'receipt': ref(ROOT / f'research/registration/receipts/{path.stem}.json'),
                         'object_ids': [o['object_id'] for o in overlap],
                         'canonical_record_equality': True})

# Preserve all notices, including unresolved primary registration, without
# claiming metadata acceptance from a route or from a shared body path.
notice_review = []
for request in read(SOURCE / 'external-owner-requests.json')['requests']:
    oid = request.get('canonical_object_id') or request['target_actual_id']
    exact_owner = owners.get(oid)
    same_body = [o['object_id'] for o in canonical['objects']
                 if o['body']['path'] == request['target_ref']['path']]
    primary_tasks = []
    for historic in request['target_tasks']:
        p = ROOT / f"research/operations/p25-register-v2/tasks/{historic['task_id']}.json"
        current = read(p) if p.exists() else {}
        primary_tasks.append({'task_id': historic['task_id'],
                              'current_local_state': current.get('state'),
                              'current_local_owner': current.get('owner')})
    notice_review.append({
        'notice_id': request['notice_id'],
        'target_actual_id': request['target_actual_id'],
        'target_ref': request['target_ref'],
        'source_refs': request['source_refs'],
        'exact_id_current_canonical': oid if exact_owner else None,
        'same_body_canonical_candidates_not_an_identity_decision': same_body,
        'exact_sources_currently_in_exact_target_record':
            [r for r in request['source_refs']
             if exact_owner and r in [exact_owner['body'], *exact_owner['evidence']]],
        'primary_tasks': primary_tasks,
        'metadata_accepted_by_this_task': False,
        'handling': 'nonblocking duplicated historical navigation; primary task obligations and existing unresolved source/identity decisions stay separate',
        'blocks_this_36_material_supplement': False,
    })

routes = read(SOURCE / 'route-comparison.json')['routes']
math_review = []
for item in field_comparisons:
    oid = item['object_id']
    comparisons = [r['comparison'] for r in routes
                   if any(d.get('target_object_id') == oid
                          for d in r['claim_decisions'])]
    # Original prose calls K a local type count on route61. K is instead the
    # source-hub/minimum-side-hub weight ratio defined by the preserved record.
    comparisons = [s.replace('K局部类型数和R权比不可互换',
                             'K为source hub与side最小hub的局部权比，R为side内部hub权比，二者不可互换')
                   for s in comparisons]
    math_review.append({'object_id': oid, 'decision': 'same mathematical identity; optional exact historical scope evidence only',
                        'comparisons': comparisons})

batch_path = ROOT / f'research/registration/batches/{TASK}.json'
assert not batch_path.exists(), 'Do not overwrite an already delivered task batch'
# Keeping the complete mature record bytes also retains all old objections and
# source provenance. Current canonical was compared before this copy.
batch_path.parent.mkdir(parents=True, exist_ok=True)
batch_path.write_bytes(candidate_path.read_bytes())
result = registration.validate_batch(ROOT, candidate,
                                     expected_materials=definition['materials'],
                                     baseline_ref=definition['baseline'],
                                     peer_objects=None)
assert canonical_ref == ref(canonical_path)

reading = {
    'task_id': TASK, 'owner': 'Boss6',
    'governance_read': ['AGENTS.md', 'research/PHASE3_READINESS.md',
                        'research/IMPLEMENTATION.md registration section and full two-object example',
                        'prompts/02.5-3-worker.md', ref(task_path)],
    'prepared_reading_reused': ref(SOURCE / 'reading-scope.json'),
    'prepared_full_proof_policy': 'Reuse the mature complete body/evidence chain; no new cleaning, proof reconstruction, old audit execution, or all-source full-text claim.',
    'direct_precise_body_statement_passages': direct_body_refs,
    'direct_support_sections': support_refs,
    'direct_calibration_preamble': {'ref': ref(calibration), 'characters': len(calibration_preamble),
                                   'range_description': 'file start through text before the unique heading 连自由全状态势也无法补救'},
    'direct_optional_source_sections': list(new_refs.values()),
    'source_sections_read_completely': len(new_refs),
    'source_acceptance_occurrences': 45,
    'body_statement_passages': len(direct_body_refs),
    'body_statement_characters': sum(len(runtime.read_ref(ROOT, r)) for r in direct_body_refs),
    'additional_support_sections': len(support_refs),
    'additional_support_characters': sum(len(runtime.read_ref(ROOT, r)) for r in support_refs),
    'optional_source_characters': sum(len(runtime.read_ref(ROOT, x['ref'])) for x in new_refs.values()),
    'not_claimed': 'Not the full two metadata pages, all 93 routes or all old proofs freshly read. All 41 exact mathematical records compared with current canonical; full original sources/route review retained at the prepared pins.',
    'budget': {'context_capacity_not_platform_measured': True,
               'task_definition_context_plan': definition.get('context_plan'),
               'source_prepared_budget_reused_as_history_not_zero_new_reading': read(SOURCE / 'reading-scope.json')['budget'],
               'actual_runtime_token_usage': None},
}
write(OUT / 'reading-review.json', reading)
review = {
    'task_id': TASK, 'status': 'mature-local-not-pushed-not-DONE',
    'canonical_ref': canonical_ref, 'task_ref': ref(task_path),
    'prepared_candidate': ref(candidate_path), 'prepared_manifest': ref(SOURCE / 'manifest.json'),
    'manifest_files_verified': manifest_checks,
    'objects': len(candidate['objects']), 'materials': len(candidate['materials']),
    'field_comparisons': field_comparisons, 'mathematical_decisions': math_review,
    'material_owner_preservation': material_preservation,
    'other_unique_master_candidates_protected': protected_candidates,
    'old_done_assets_protected': old_done,
    'source_fragment_policy': 'Only the standalone 41 objects/36 materials are delivered. The 21 merge-fragments and third metadata page are not automatically received; preserve the original unique master candidates and their full owners/evidence.',
    'external_notices_current_observation': notice_review,
    'proof_reference_check': {'unique_exact_body_evidence_refs': len(all_refs),
                              'all_sha_and_official_unique_sections_valid': True,
                              'meaning': 'Structural integrity only; mature mathematical proof scopes retained, optional metadata is not substituted for proof.'},
    'validation_expected_materials_and_baseline_peer_objects_none': result,
    'new_ids': 0, 'new_edges': 0, 'math_status_changes': 0,
    'old_owner_losses': [], 'existing_needs_decision_cleared_by_route_only': [],
    'canonical_and_original_candidates_and_old_DONE_mutated': False,
    'cross_version_policy': 'At this pinned canonical all 41 objects are v1 and have no changed mathematical fields. Incoming v2 adds evidence only. A later canonical revision requires a new comparison and union, never blind replacement by this v2.',
}
write(OUT / 'validation-review.json', review)
receipt = {
    'schema': 2, 'task_id': TASK, 'owner': 'Boss6', 'stage': 'registration',
    'baseline': definition['baseline'], 'batch_file': ref(batch_path),
    'assets': [ref(batch_path)], 'status': 'mature-local-not-yet-pushed-not-DONE',
    'candidate_provenance': ref(candidate_path), 'canonical_observation': canonical_ref,
    'validation': result,
    'semantic_comparison': {'objects': 41, 'materials': 36, 'new_objects': 0,
                            'changed_fields_only': ['evidence', 'version'],
                            'all_old_mathematical_fields_and_evidence_preserved': True,
                            'all_old_material_owners_preserved': True,
                            'added_optional_source_ref_occurrences': 45,
                            'unique_added_optional_source_sections': 37,
                            'truth_status_changes': 0, 'new_ids': 0, 'new_edges': 0},
    'reading_review': ref(OUT / 'reading-review.json'),
    'validation_review': ref(OUT / 'validation-review.json'),
    'source_boundary': 'Two source pages are attachment only for the actual 37 weighted-congestion and 4 facility-game owners. Other metadata routes do not certify acceptance; original excluded dispositions are legitimate, existing primary-task/source doubts are not erased, and 21 other master-candidate fragments are outside this task.',
    'ready_for_parent': 'Parent serial checkpoint/push and done; no Git write, queue mutation, board post, old DONE edit, canonical edit or edge creation performed by this worker.',
}
receipt_path = ROOT / f'research/registration/receipts/{TASK}.json'
assert not receipt_path.exists()
write(receipt_path, receipt)
print(json.dumps({'batch': ref(batch_path), 'receipt': ref(receipt_path),
                  'reading_review': ref(OUT / 'reading-review.json'),
                  'validation_review': ref(OUT / 'validation-review.json'),
                  'validation': result}, ensure_ascii=False, indent=2))
