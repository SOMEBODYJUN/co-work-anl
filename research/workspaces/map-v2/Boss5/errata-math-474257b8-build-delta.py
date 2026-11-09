"""Read-only source/pin impact audit; write only isolated local delta artifacts."""
from pathlib import Path
import copy
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'research/workspaces/map-v2/Boss5'
PREFIX = 'errata-math-474257b8-'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def pin(record):
    return hashlib.sha256(json.dumps(record, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()

def save(name, value):
    path = OUT / (PREFIX + name)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return str(path.relative_to(ROOT))

def refs(value, location=''):
    found = []
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            found.append((location, value))
        for key, item in value.items():
            found.extend(refs(item, location + '/' + str(key)))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            found.extend(refs(item, location + '/' + str(i)))
    return found

registry_path = ROOT / 'research/registry.json'
registry = json.loads(registry_path.read_text())
objects = {obj['object_id']: obj for obj in registry['objects']}
all_rows = []
for path in sorted((ROOT / 'research/operations/map-v2/tasks').glob('*.json')):
    row = json.loads(path.read_text())
    if 'definition' in row and 'state' in row:
        all_rows.append((path, row))
done_successors = {}
for _, row in all_rows:
    if row['state'] == 'done':
        for old in row['definition'].get('supersedes', []):
            done_successors.setdefault(old, []).append(row['definition']['task_id'])

primary = [
    ('bamas', 'archives/unrelated-machines/state/资源/Bamas升投影MMDA与SantaClaus--资料.md',
     '/workspace/scratch/a70fb040a4fc/bamas-review-474257b8/corrected-body.md'),
    ('multiouter', 'archives/unrelated-machines/state/审查/多outer tiny-home三源实际重读与版本边界增量--审查.md',
     'research/workspaces/map-v2/Boss5/um0066-474257b8-multiouter-final-read.corrected.md'),
    ('multiouter', 'archives/unrelated-machines/state/审查/多outer tiny-home作者证明v1读后与完整算法范围增量--审查.md',
     'research/workspaces/map-v2/Boss5/um0066-474257b8-author-proof-v1.corrected.md'),
    ('q1-count', 'archives/unrelated-machines/state/审查/联合槽位与均匀束匹配有限审查--审查.md',
     'research/workspaces/map-v2/Boss5/um1766-474257b8-joint-slot-bundle-count-corrected.md'),
]
supplement = [
    ('long-chain-owner', 'archives/unrelated-machines/state/审查/最优凸包长链与私有汇点边界两源精读--审查.md',
     'research/workspaces/map-v2/Boss5/um1766-474257b8-long-chain-owner-corrected.md'),
    ('long-chain-repair', 'archives/unrelated-machines/state/审查/最优凸包长链与闭环逃逸有限审查--审查.md',
     'research/workspaces/map-v2/Boss5/um1766-474257b8-long-chain-explicit-repair-corrected.md'),
]
seventh = [
    ('joint-slot-zero-demand-branch', 'archives/unrelated-machines/state/计算/失真组实际源调度与联合槽独立程序复跑--计算.md',
     'research/workspaces/map-v2/Boss5/errata-math-474257b8-seventh-source-corrected.md'),
]
eighth = [
    ('supplied-witness-zero-demand-branch', 'archives/unrelated-machines/state/资源/失真组给定见证舍入与有效无效证书原入口--资源.md',
     'research/workspaces/map-v2/Boss5/errata-math-474257b8-eighth-source-corrected.md'),
]
ninth = [
    ('threshold-cover-zero-demand-branch', 'archives/unrelated-machines/state/算法/门槛覆盖的同见证联合槽恢复--算法.md',
     'research/workspaces/map-v2/Boss5/errata-math-474257b8-ninth-source-corrected.md'),
]

def audit(pairs, label):
    source_changes = []
    replacements = {}
    for category, path, copy_path in pairs:
        copy_abs = Path(copy_path) if Path(copy_path).is_absolute() else ROOT / copy_path
        old_sha, new_sha = sha(ROOT / path), sha(copy_abs)
        material = [m for m in registry['materials'] if m['path'] == path]
        assert len(material) == 1 and material[0]['sha256'] == old_sha, (path, material)
        replacements[path] = new_sha
        source_changes.append({'category': category, 'canonical_path': path,
            'prepared_copy_path': copy_path, 'old_sha256': old_sha, 'new_sha256': new_sha,
            'registry_material_current': material[0],
            'registry_material_proposed': {**material[0], 'sha256': new_sha},
            'material_disposition_owner_ids_and_reason_unchanged': True})
    object_changes = []
    for oid, obj in objects.items():
        proposed = copy.deepcopy(obj)
        changes = []
        for location, ref in refs({'body': proposed['body'], 'evidence': proposed['evidence']}):
            if ref['path'] not in replacements:
                continue
            before = copy.deepcopy(ref)
            ref['sha256'] = replacements[ref['path']]
            changes.append({'json_pointer': location, 'old_ref': before, 'new_ref': copy.deepcopy(ref)})
        if not changes:
            continue
        proposed['version'] = obj['version'] + 1
        preserved = {k: v for k, v in obj.items() if k not in {'version', 'body', 'evidence'}}
        assert preserved == {k: v for k, v in proposed.items() if k not in {'version', 'body', 'evidence'}}
        object_changes.append({'object_id': oid, 'current_version': obj['version'],
            'current_registration_pin': pin(obj), 'proposed_version': proposed['version'],
            'proposed_registration_pin': pin(proposed), 'ref_replacements': changes,
            'all_nonbinding_fields_unchanged': True, 'statement_unchanged': True,
            'preserved_nonbinding_fields_sha256': pin(preserved),
            'version_increment_reason': '正文/必要证据全文字节勘误使精确SHA引用变化；沿用同一命题、模型、量词、状态与声明，只按既有版本规则增一。未改动所选章节的owner也必须更新全文SHA。'})
    changes_by_id = {c['object_id']: c for c in object_changes}
    ids = set(changes_by_id)
    edges = []
    for path in registry['edge_files']:
        edge = json.loads((ROOT / path).read_text())
        endpoints = set(edge.get('source_ids', []) + edge.get('target_ids', [])) | set(edge.get('endpoint_pins', {}))
        hit_ids = sorted(endpoints & ids)
        direct = [{'json_pointer': loc, **ref} for loc, ref in refs(edge) if ref['path'] in replacements]
        evidence_pin_paths = sorted(set(edge.get('evidence_pins', {})) & set(replacements))
        if hit_ids or direct or evidence_pin_paths:
            edges.append({'path': path, 'current_sha256': sha(ROOT / path),
                'edge_id': edge['edge_id'], 'kind': edge['kind'], 'status': edge['status'],
                'changed_endpoint_ids': hit_ids, 'direct_source_refs': direct,
                'changed_evidence_pin_paths': evidence_pin_paths,
                'current_endpoint_pins': {oid: edge.get('endpoint_pins', {}).get(oid) for oid in hit_ids},
                'proposed_endpoint_pins': {oid: changes_by_id[oid]['proposed_registration_pin'] for oid in hit_ids},
                'action': '原数学关系限定核对后重新edge-bind/edge-check；由有效done的定向替代收据保留或替代全部既有资产。仅正文未直接命中不能免除端点pin变化。'})
    edge_paths = {e['path'] for e in edges}
    tasks = []
    for path, row in all_rows:
        definition = row['definition']
        core = sorted(set(definition.get('object_ids', [])) & ids)
        reads = sorted(set(definition.get('read_object_ids', [])) & ids)
        input_hits = sorted(set(definition.get('input_pins', {})) & ids)
        direct = [{'json_pointer': loc, **ref} for loc, ref in refs(definition) if ref['path'] in replacements]
        receipt = row.get('receipt', {})
        assets = [ref for ref in receipt.get('assets', []) if ref.get('path') in edge_paths]
        if not (core or reads or input_hits or direct or assets):
            continue
        tid = definition['task_id']
        effective_done = row['state'] == 'done' and tid not in done_successors
        if effective_done:
            action = 'repair-effective-done'
        elif row['state'] == 'done':
            action = 'historical-only-use-effective-successor'
        elif row['state'] == 'withdrawn':
            action = 'historical-withdrawn-no-refresh'
        else:
            action = 'refresh-same-unfinished-task'
        task = {'task_id': tid, 'task_file': str(path.relative_to(ROOT)),
            'task_file_current_sha256': sha(path), 'stage': definition['stage'],
            'state': row['state'], 'owner': row.get('owner'),
            'changed_core_ids': core, 'changed_read_ids': reads,
            'input_pin_hits': {oid: definition['input_pins'][oid] for oid in input_hits},
            'direct_source_refs': direct, 'affected_receipt_assets': assets,
            'effective_done': effective_done, 'completed_successors': done_successors.get(tid, []),
            'supersedes': definition.get('supersedes', []), 'recommended_action': action}
        if effective_done:
            task['all_prior_assets_to_dispose'] = receipt.get('assets', [])
            task['all_cores_rechecked_due_changed_read_input'] = definition.get('object_ids', []) if reads else core
        tasks.append(task)
    baseline = json.loads((ROOT / registry['baseline']['path']).read_text())
    baseline_updates = []
    for material in baseline['materials']:
        if material['path'] in replacements:
            baseline_updates.append({'path': material['path'], 'old_sha256': material['sha256'],
                'new_sha256': replacements[material['path']], 'old_pin_matches_current_bytes': material['sha256'] == sha(ROOT / material['path'])})
    result = {'schema': 1, 'audit_token': '474257b8-errata-math', 'scope': label,
        'snapshot': {'registry_path': 'research/registry.json', 'registry_sha256': sha(registry_path),
            'baseline_ref': registry['baseline'], 'canonical_edge_files_scanned': len(registry['edge_files']),
            'local_only': True, 'authoritative_remote_recheck_required_by_root': True},
        'source_changes': source_changes, 'object_deltas': object_changes,
        'material_and_baseline_advice': {'material_updates': [{'path': s['canonical_path'], 'old_sha256': s['old_sha256'], 'new_sha256': s['new_sha256']} for s in source_changes],
            'baseline_updates': baseline_updates,
            'publication_rule': '更正副本核对通过后，由根保全草稿、处理本人claimed包，再将canonical原处字节、另冻的新baseline与registry精确引用/版本一次成组发布；本文件不冻结、不更新共享登记或状态。'},
        'affected_canonical_edges': edges, 'affected_tasks': tasks,
        'grouped_repair_task_ids': [t['task_id'] for t in tasks if t['recommended_action'] in {'repair-effective-done', 'refresh-same-unfinished-task'}],
        'summary': {'sources': len(source_changes), 'object_versions_incremented_once': len(object_changes),
            'ref_replacements': sum(len(c['ref_replacements']) for c in object_changes),
            'canonical_edges_requiring_rebind': len(edges),
            'effective_done_replacements': sum(t['effective_done'] for t in tasks),
            'unfinished_refreshes': sum(t['recommended_action'] == 'refresh-same-unfinished-task' for t in tasks)}}
    return result

outputs = [(primary, 'registry-delta.json', '四canonical源的三类最小数学勘误'),
           (supplement, 'long-chain-supplement-delta.json', '1766追加两处long-chain转述勘误'),
           (primary + supplement, 'final-six-source-delta.json', '根确认同批的六canonical源最小数学勘误；每个owner仅增version一次')]
if '--seven-only' in sys.argv:
    outputs = [(primary + supplement + seventh, 'final-seven-source-delta.json',
                '根确认同批的七canonical源最小数学勘误；沿相同identity，每个owner仅增version一次')]
if '--eighth-only' in sys.argv:
    outputs = [(eighth, 'eighth-source-delta.json',
                '七源已发布后的第八源独立最小勘误；只含本源，沿原identity，唯一owner仅增version一次')]
if '--eighth-ninth-only' in sys.argv:
    outputs = [(eighth + ninth, 'eighth-ninth-source-delta.json',
                '七源已发布后的第八第九两源最小续补；不叠加旧七源，沿原identity，每个owner仅增version一次')]
for pairs, suffix, label in outputs:
    result = audit(pairs, label)
    path = save(suffix, result)
    print(json.dumps({'path': path, 'summary': result['summary'], 'repair_task_ids': result['grouped_repair_task_ids']}, ensure_ascii=False))
