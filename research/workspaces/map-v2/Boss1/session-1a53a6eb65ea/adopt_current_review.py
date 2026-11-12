"""Apply an explicit mathematical review record after native map assembly.

The record freezes the actually read task receipts, assets and input versions.
Only those contracts are discharged; concurrent unreviewed deltas survive.
This does not compute coverage or replace the native assembler.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import research_runtime as rr


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append(row, key, note):
    if note and note not in row.get(key, ''):
        row[key] = row.get(key, '') + '\n' + note


record_path = Path(sys.argv[1]).resolve()
record_path.relative_to(ROOT)
record = read(record_path)
for material in record.get('review_materials', []):
    assert sha(ROOT / material['path']) == material['sha256'], material['path']
registry = read(ROOT / 'research/registry.json')
objects = {o['object_id']: o for o in registry['objects']}
integration_path = ROOT / 'map/integration.json'
integration = read(integration_path)
assert integration['registry_pin'] == rr.pin(registry), 'Run native assemble first'
reviewed = set()
edges = {}
receipts = []
retired_edges = set()

for saved in record.get('task_reviews', []):
    task_id = saved['task_id']
    task = read(ROOT / 'research/operations/map-v2/tasks' / (task_id + '.json'))
    receipt_path = ROOT / saved['receipt_path']
    receipt = read(receipt_path)
    assert task['state'] == 'done' and task['receipt'] == receipt, task_id
    assert sha(receipt_path) == saved['receipt_sha256'], task_id
    assert rr.pin(receipt) == saved['receipt_pin'], task_id
    assert integration['task_receipt_pins'][task_id] == saved['receipt_pin'], task_id
    assert task['definition']['input_pins'] == saved['input_pins'], task_id
    assert task['definition']['object_ids'] == saved['core_ids'], task_id
    for object_id, pin in saved['input_pins'].items():
        assert rr.pin(objects[object_id]) == pin, object_id
    reviewed.update(saved['core_ids'])
    for asset in receipt['assets']:
        path = ROOT / asset['path']
        assert sha(path) == asset['sha256'], asset['path']
        if path.suffix != '.json':
            continue
        edge = read(path)
        if not isinstance(edge, dict) or 'edge_id' not in edge:
            continue
        assert asset['path'] in registry['edge_files'], asset['path']
        edge_id = edge['edge_id']
        assert integration['edge_pins'][edge_id] == rr.pin(edge), edge_id
        for object_id in edge['source_ids'] + edge['target_ids']:
            assert edge['endpoint_pins'][object_id] == rr.pin(objects[object_id]), object_id
            reviewed.add(object_id)
        edges[edge_id] = asset
    receipts.append(task_id)

# A relation-only review preserves the owning packet's other core coverage.
# The native assembler must already have integrated the exact owning receipt.
for saved in record.get('edge_reviews', []):
    task_id = saved['owning_task_id']
    task = read(ROOT / 'research/operations/map-v2/tasks' / (task_id + '.json'))
    receipt = read(ROOT / saved['receipt_path'])
    assert task['state'] == 'done' and task['receipt'] == receipt, task_id
    assert sha(ROOT / saved['receipt_path']) == saved['receipt_sha256'], task_id
    assert rr.pin(receipt) == saved['receipt_pin'], task_id
    assert integration['task_receipt_pins'][task_id] == saved['receipt_pin'], task_id
    path = saved['path']
    asset = {'path': path, 'sha256': saved['sha256']}
    assert asset in receipt['assets'], path
    assert path in registry['edge_files'] and sha(ROOT / path) == saved['sha256'], path
    edge = read(ROOT / path)
    edge_id = saved['edge_id']
    assert edge['edge_id'] == edge_id, path
    assert rr.pin(edge) == saved['edge_pin'] == integration['edge_pins'][edge_id], edge_id
    assert edge['endpoint_pins'] == saved['endpoint_pins'], edge_id
    assert set(saved['endpoint_pins']) == set(edge['source_ids'] + edge['target_ids']), edge_id
    assert saved['review_scope'].strip(), edge_id
    for object_id, pin in saved['endpoint_pins'].items():
        assert rr.pin(objects[object_id]) == pin, object_id
        reviewed.add(object_id)
    for ref in edge['evidence']:
        assert sha(ROOT / ref['path']) == ref['sha256'], ref['path']
    edges[edge_id] = asset

for saved in record.get('retired_edge_reviews', []):
    # A removed relation is discharged only through its exact published
    # supersession, never merely because it is absent from the current graph.
    old_id, new_id = saved['old_task_id'], saved['new_task_id']
    assert new_id in receipts, new_id
    old_task = read(ROOT / 'research/operations/map-v2/tasks' / (old_id + '.json'))
    new_task = read(ROOT / 'research/operations/map-v2/tasks' / (new_id + '.json'))
    assert old_task['state'] == 'done', old_id
    assert old_id in new_task['definition'].get('supersedes', []), old_id
    path = saved['path']
    old_assets = {asset['path']: asset for asset in old_task['receipt']['assets']}
    assert old_assets[path]['sha256'] == saved['sha256'], path
    assert sha(ROOT / path) == saved['sha256'], path
    disposition = new_task['receipt']['supersession'][old_id]['assets'][path]
    assert disposition['disposition'] == 'retired', path
    assert path not in {asset['path'] for asset in new_task['receipt']['assets']}, path
    assert path not in registry['edge_files'], path
    edge = read(ROOT / path)
    edge_id = saved['edge_id']
    assert edge['edge_id'] == edge_id, edge_id
    assert edge_id not in integration['edge_pins'], edge_id
    endpoints = set(edge['source_ids'] + edge['target_ids'])
    assert set(saved['endpoint_pins']) == endpoints, edge_id
    for object_id, pin in saved['endpoint_pins'].items():
        assert rr.pin(objects[object_id]) == pin, object_id
    assert saved['reason'].strip(), edge_id
    reviewed.update(endpoints)
    retired_edges.add(edge_id)

for saved in record.get('source_reviews', []):
    object_id = saved['object_id']
    assert rr.pin(objects[object_id]) == saved['object_pin'], object_id
    for material in saved.get('materials', []):
        assert sha(ROOT / material['path']) == material['sha256'], material['path']
    reviewed.add(object_id)

append(integration, 'review_note', record['review_note'])
reviewer = record.get('reviewer', 'Boss1')
if reviewer not in integration.get('reviewed_by', ''):
    integration['reviewed_by'] = integration.get('reviewed_by', '') + '; ' + reviewer
for scope, note in record['archive_notes'].items():
    row = integration['archive_reviews'][scope]
    append(row, 'comparison_scope', note['comparison_scope'])
    append(row, 'outcome', note['outcome'])
append(integration['cross_archive_review'], 'comparison_scope', record['cross_archive_scope'])
append(integration['cross_archive_review'], 'outcome', record['cross_archive_outcome'])

published = json.loads(subprocess.run(
    ['git', 'show', 'HEAD:map/integration.json'], cwd=ROOT,
    check=True, capture_output=True, text=True).stdout)
new_pending = integration.get('pending_changes', {})
old_pending = published.get('pending_changes', {})
pending_objects = (set(new_pending.get('object_ids', [])) |
                   set(old_pending.get('object_ids', []))) - reviewed
pending_edges = (set(new_pending.get('edge_ids', [])) |
                 set(old_pending.get('edge_ids', []))) - set(edges) - retired_edges
edge_endpoints = integration.get('edge_endpoints', {})
for edge_id in pending_edges:
    pending_objects.update(edge_endpoints.get(edge_id, []))
affected = {scope for object_id in pending_objects
            for scope in integration.get('object_scopes', {}).get(object_id, [])}
pending_scopes = set(new_pending.get('archive_scopes', [])) | set(old_pending.get('archive_scopes', []))
unscoped = any(not edge_endpoints.get(edge_id) for edge_id in pending_edges)
for scope in record['archive_notes']:
    if scope not in affected and not unscoped:
        pending_scopes.discard(scope)
        row = integration['archive_reviews'][scope]
        row['unresolved'] = [x for x in row.get('unresolved', [])
                             if x != 'Updated inputs/relations require this preserved comparison to be reviewed again']
integration['pending_changes'] = {
    'object_ids': sorted(pending_objects),
    'edge_ids': sorted(pending_edges),
    'archive_scopes': sorted(pending_scopes | affected),
}
if not any(integration['pending_changes'].values()):
    cross = integration['cross_archive_review']
    cross['unresolved'] = [x for x in cross.get('unresolved', [])
                           if x != 'Updated inputs or comparisons require cross-archive integration review']
integration_path.write_text(json.dumps(integration, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({
    'status': 'EXPLICIT_CURRENT_REVIEW_ADOPTED',
    'review_id': record['review_id'],
    'review_record_sha256': sha(record_path),
    'tasks': receipts,
    'accepted_edge_count': len(edges),
    'retired_edge_count': len(retired_edges),
    'reviewed_object_count': len(reviewed),
    'pending_changes': integration['pending_changes'],
}, ensure_ascii=False))
