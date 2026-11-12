"""Explicit mathematical registration and small, recoverable Work contexts.

No model SDK or external service is required. Records are declarations by their
authors; structural checks and version pins never certify mathematical truth.
"""
from __future__ import annotations

import argparse
from collections import deque
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import uuid

from curation import _safe_path, formal_paths

REGISTRY = 'research/registry.json'
LOGICAL = {'implies', 'refutes', 'specializes', 'transfers', 'equivalent_to'}
CONTEXT = {'motivates', 'cites', 'sourced_from', 'implements', 'checks', 'corrects', 'supersedes'}
TRUTHS = {'definition', 'proved', 'conditional', 'conjecture', 'open', 'refuted', 'finite', 'unassessed'}
STATES = {'working', 'needs-feedback', 'blocked', 'candidate', 'paused', 'closed'}
IDENT = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,95}')
OBJECT_IDENT = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.:-]*(?:/[A-Za-z0-9][A-Za-z0-9_.:-]*)*')

# Comparison runs retain their original blind-vs-informed launch slots.
# Ordinary research dispatches obligations on demand with the same explicit
# worker defaults, unless the user selects another model or effort.
WORKER_LAUNCH = {'model': 'gpt-6.1-sol', 'reasoning_effort': 'ultra', 'fork_turns': 'none'}
SOLVER_ROSTER = [
    {'solver_id': 'obstacle-1', 'profile': 'obstacle', 'model': 'gpt-6.1-sol',
     'reasoning_effort': 'ultra', 'fork_turns': 'none'},
    {'solver_id': 'full-1', 'profile': 'full', 'model': 'gpt-6.1-sol',
     'reasoning_effort': 'ultra', 'fork_turns': 'none'},
    {'solver_id': 'full-2', 'profile': 'full', 'model': 'gpt-6.1-sol',
     'reasoning_effort': 'ultra', 'fork_turns': 'none'},
]


def _write_json(path, data):
    """A crash leaves either the previous JSON or the complete new JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, prefix='.research-', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
            stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and temporary.exists(): temporary.unlink()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(value):
    if not isinstance(value, str) or not IDENT.fullmatch(value):
        raise ValueError('Use a stable simple ID: letters, numbers, dot, dash, underscore')
    return value


def object_identity(value):
    """Mathematical IDs are lookup keys, never workspace or task paths.

    Existing archive identities use slash namespaces and colon-qualified Claims.
    Keep those IDs while retaining identity() for every filename-bearing ID.
    """
    if not isinstance(value, str) or len(value) > 512 or not OBJECT_IDENT.fullmatch(value):
        raise ValueError('Use a stable mathematical ID, preserving slash namespaces and colon-qualified Claims')
    return value


def pin(record):
    return digest(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def nonempty(record, keys):
    for key in keys:
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise ValueError('Explicit nonempty field required: ' + key)


def strings(value, label, nonempty_list=False):
    if not isinstance(value, list) or (nonempty_list and not value) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError(label + ' must be a list of nonempty strings')
    if len(value) != len(set(value)):
        raise ValueError('Duplicate ' + label)


def heading_sections(text):
    """ATX headings outside fenced code. Duplicate titles need another locator."""
    lines = text.splitlines(keepends=True)
    found, fence, start = [], None, 0
    frontmatter = text.startswith('---\n')
    for index, line in enumerate(lines):
        if frontmatter:
            if index and line.strip() == '---':
                frontmatter = False
            start += len(line)
            continue
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1] and not line[marker.end():].strip():
                fence = None
        elif fence is None:
            h = re.match(r'^ {0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$', line.rstrip('\r\n'))
            if h:
                found.append((h[2], len(h[1]), start))
        start += len(line)
    return found


def section(text, title=None):
    if title is None:
        return text
    headings = heading_sections(text)
    matches = [row for row in headings if row[0] == title]
    if len(matches) != 1:
        raise ValueError('Section title missing or ambiguous: ' + str(title))
    _, level, start = matches[0]
    end = next((pos for _, depth, pos in headings if pos > start and depth <= level), len(text))
    return text[start:end]


def reference(root, ref):
    if not isinstance(ref, dict) or not {'path', 'sha256'} <= ref.keys() or ref.keys() - {'path', 'sha256', 'section'}:
        raise ValueError('A reference needs path, sha256, and optional exact section title')
    path = _safe_path(root, ref['path'])
    if not re.fullmatch(r'[0-9a-f]{64}', str(ref['sha256'])):
        raise ValueError('Invalid SHA-256 binding')
    return path


def ref_bytes(root, ref):
    path = reference(root, ref)
    data = path.read_bytes()
    if digest(data) != ref['sha256']:
        raise ValueError('Stale content binding: ' + ref['path'])
    if 'section' in ref:
        section(data.decode('utf-8'), ref['section'])
    return data


def read_ref(root, ref):
    return section(ref_bytes(root, ref).decode('utf-8'), ref.get('section'))


def load(root, name=REGISTRY, provided=None, verify=True):
    data = json.loads(_safe_path(root, name).read_text()) if provided is None else provided
    if data.get('schema') != 2 or not isinstance(data.get('objects'), list) or not isinstance(data.get('materials'), list):
        raise ValueError('Expected explicit v2 registration; do not auto-admit old file listings')
    objects = {}
    for obj in data['objects']:
        oid = object_identity(obj.get('object_id'))
        if oid in objects:
            raise ValueError('Duplicate object ID: ' + oid)
        nonempty(obj, ['title', 'kind', 'model', 'statement', 'quantifiers', 'scope', 'objections'])
        if type(obj.get('version')) is not int or obj['version'] < 1 or obj.get('truth_status') not in TRUTHS:
            raise ValueError('Object requires version >= 1 and a separate truth_status')
        strings(obj.get('assumptions'), 'assumptions')
        strings(obj.get('sources'), 'sources')
        strings(obj.get('keywords', []), 'keywords')
        (ref_bytes if verify else reference)(root, obj['body'])
        if not isinstance(obj.get('evidence'), list):
            raise ValueError('Explicit evidence list required')
        for ref in obj['evidence']:
            (ref_bytes if verify else reference)(root, ref)
        objects[oid] = obj
    seen, material_by_path = set(), {}
    for row in data['materials']:
        (ref_bytes if verify else reference)(root, {k: row[k] for k in ('path', 'sha256')})
        if row['path'] in seen:
            raise ValueError('Duplicate material disposition')
        seen.add(row['path'])
        material_by_path[row['path']] = row
        nonempty(row, ['reason'])
        if row.get('disposition') not in {'objects', 'attachment', 'excluded', 'needs-decision'}:
            raise ValueError('Explicit material disposition required')
        ids = row.get('object_ids', [])
        strings(ids, 'object_ids')
        if any(i not in objects for i in ids):
            raise ValueError('Unknown material owner')
        if row['disposition'] in {'objects', 'attachment'} and not ids:
            raise ValueError('Mathematics and attachments require mathematical owners')
        for oid in ids:
            obj = objects[oid]
            refs = [obj['body']] + obj['evidence'] if row['disposition'] == 'objects' else obj['evidence']
            if row['disposition'] in {'objects', 'attachment'} and row['path'] not in {r['path'] for r in refs}:
                raise ValueError('Material owner must reference these bytes')
    for obj in objects.values():
        if obj['body']['path'] not in seen:
            raise ValueError('Every registered body requires a material disposition')
        material = material_by_path[obj['body']['path']]
        if material['disposition'] != 'objects' or obj['object_id'] not in material.get('object_ids', []):
            raise ValueError('Every live object body must remain declared mathematics owned by that object: ' + obj['object_id'])
    return data, objects


def register(root, record_file, registry=REGISTRY):
    """Publish an explicit reviewed registration locally, preserving identity."""
    data = json.loads(_safe_path(root, record_file).read_text())
    _, objects = load(root, registry, provided=data)
    # Registration is independently usable before graph construction. A changed
    # object may leave incident edge reviews stale; map check/build evaluates
    # those reviews rather than blocking an unrelated identity update here.
    destination = _safe_path(root, registry)
    if destination.exists():
        # Previous byte pins are expected to be stale when explicitly updating
        # a changed proof. Read identity/version metadata without re-admitting
        # those old bytes; validate the entire incoming declaration above.
        previous = json.loads(destination.read_text())
        old = {object_identity(obj['object_id']): obj for obj in previous['objects']}
        if len(old) != len(previous['objects']): raise ValueError('Duplicate previous object IDs')
        for oid, obj in objects.items():
            if oid in old and obj != old[oid] and obj['version'] <= old[oid]['version']:
                raise ValueError('Changed object requires a new version: ' + oid)
            if oid in old and obj['version'] < old[oid]['version']:
                raise ValueError('Object version cannot go backwards: ' + oid)
        removed = set(old) - objects.keys()
        dispositions = data.get('retired_objects', {})
        if any(not isinstance(dispositions.get(oid), str) or not dispositions[oid].strip() for oid in removed):
            raise ValueError('Retired IDs require explicit recoverable reasons; do not silently drop objects')
    _write_json(destination, data)
    return {'status': 'registered-local-not-pushed', 'objects': len(objects), 'registry': registry}


def edge_digest(edge):
    return pin({k: v for k, v in edge.items() if k not in {'endpoint_pins', 'evidence_pins', 'review_digest'}})


def edge_bindings(root, edge, objects, verify=True):
    ids = edge['source_ids'] + edge['target_ids']
    return {'endpoint_pins': {oid: pin(objects[oid]) for oid in sorted(set(ids))},
            'evidence_pins': {r['path']: digest(ref_bytes(root, r)) if verify else r['sha256'] for r in edge['evidence']},
            'review_digest': edge_digest(edge)}


def require_edge_result(edge):
    if (edge['status'] == 'accepted' and edge['kind'] in LOGICAL
            and 'contribution' not in edge
            and not (isinstance(edge.get('whole_result'), str) and edge['whole_result'].strip())):
        raise ValueError('Accepted logical edge needs whole_result or a proof-step contribution: ' + edge['edge_id'])


def edges(root, data, objects, verify=True):
    result = {}
    for name in data.get('edge_files', []):
        edge = json.loads(_safe_path(root, name).read_text())
        eid = identity(edge.get('edge_id'))
        if eid in result:
            raise ValueError('Duplicate edge ID')
        if edge.get('kind') not in LOGICAL | CONTEXT or edge.get('status') not in {'accepted', 'proposed', 'rejected'}:
            raise ValueError('Unknown relation kind/status')
        strings(edge.get('source_ids'), 'source_ids', True)
        strings(edge.get('target_ids'), 'target_ids', True)
        if any(oid not in objects for oid in edge['source_ids'] + edge['target_ids']):
            raise ValueError('Unknown mathematical endpoint')
        if edge.get('premises_mode') != 'all':
            raise ValueError('Joint premises must remain one ALL hyperedge')
        nonempty(edge, ['conditions', 'explanation', 'scope'])
        roles = edge.get('roles')
        if not isinstance(roles, dict) or set(roles) != set(edge['source_ids'] + edge['target_ids']) or any(not isinstance(v, str) or not v.strip() for v in roles.values()):
            raise ValueError('Explain the mathematical role of every endpoint')
        if not isinstance(edge.get('evidence'), list) or not edge['evidence']:
            raise ValueError('Exact relation evidence required')
        for ref in edge['evidence']:
            (ref_bytes if verify else reference)(root, ref)
        if edge.get('relation_mode') not in {'unconditional', 'conditional', 'context'}:
            raise ValueError('Explicit relation_mode required')
        if 'contribution' in edge:
            contribution = edge['contribution']
            if (edge['kind'] not in LOGICAL or edge['relation_mode'] == 'context'
                    or not isinstance(contribution, dict) or set(contribution) != {'result', 'remaining'}):
                raise ValueError('A logical contribution requires result and remaining: ' + eid)
            nonempty(contribution, ['result', 'remaining'])
        if 'whole_result' in edge:
            if edge['kind'] not in LOGICAL or 'contribution' in edge:
                raise ValueError('A whole result and a proof-step contribution are distinct: ' + eid)
            nonempty(edge, ['whole_result'])
        if edge['status'] == 'accepted':
            nonempty(edge, ['reviewed_by', 'review_note'])
            if edge['kind'] in LOGICAL and set(edge['source_ids']) == set(edge['target_ids']):
                raise ValueError('A mathematical relation must compare distinct sets of objects: ' + eid)
            pins = edge_bindings(root, edge, objects, verify)
            for key in ('endpoint_pins', 'evidence_pins', 'review_digest'):
                if edge.get(key) != pins[key]:
                    raise ValueError('Stale or missing accepted relation binding: ' + eid + ' / ' + key)
            if edge['kind'] in LOGICAL:
                if edge['relation_mode'] == 'context':
                    raise ValueError('Logical relations need logical conditions')
                if edge['relation_mode'] == 'unconditional' and any(objects[oid]['truth_status'] not in {'definition', 'proved'} for oid in edge['source_ids']):
                    raise ValueError('Open, finite, conditional or refuted premises require a conditional relation')
            elif edge['relation_mode'] != 'context':
                raise ValueError('Contextual links cannot act as proofs')
        result[eid] = edge
    return result


def verify_endpoints(root, edge, objects):
    for oid in set(edge['source_ids'] + edge['target_ids']):
        if oid not in objects:
            raise ValueError('Unknown mathematical endpoint: ' + oid)
        ref_bytes(root,objects[oid]['body'])
        for ref in objects[oid]['evidence']:
            ref_bytes(root,ref)


def check_edge(root, edge_file, registry=REGISTRY, verify=True):
    """Validate one proposed/accepted edge before it enters the canonical registry.

    Stage-3 workers intentionally do not edit ``registry.json``.  This command
    gives ``map done`` a real semantic gate for the edge it is delivering,
    instead of relying on the registry's current ``edge_files`` list.
    """
    data, objects = load(root, registry, verify=False)
    name = _safe_path(root, edge_file).relative_to(root).as_posix()
    edge = json.loads(_safe_path(root,name).read_text())
    if verify: verify_endpoints(root,edge,objects)
    relations = edges(root, dict(data, edge_files=[name]), objects, verify=verify)
    edge = relations[next(iter(relations))]
    if name not in data.get('edge_files', []):
        require_edge_result(edge)
    return {'status': 'edge-structure-valid-not-a-mathematical-verdict',
            'edge_file': name, 'edge_id': edge['edge_id'],
            'edge_status': edge['status'], 'registry': registry,
            'proof_scope': 'step' if 'contribution' in edge else 'whole' if edge['kind'] in LOGICAL else 'context',
            'objects': sorted(set(edge['source_ids'] + edge['target_ids']))}


def inventory(root, registry=REGISTRY):
    path = _safe_path(root, registry)
    known = {}
    if path.exists():
        data, _ = load(root, registry)
        known = {r['path']: r for r in data['materials']}
    return [{'path': p.relative_to(root).as_posix(), 'sha256': digest(p.read_bytes()),
             'registration': known.get(p.relative_to(root).as_posix(), {}).get('disposition', 'unregistered')}
            for p in formal_paths(root)]


def prepare_inputs(root, output, scope='repository', coverage_note=None, paths=None):
    """Keep the current prepare-inputs CLI while sharing its real Git denominator."""
    if not isinstance(coverage_note, str) or not coverage_note.strip():
        raise ValueError('A concrete coverage note is required')
    import registration
    return registration.prepare_inputs(root, output, scope, coverage_note.strip(), paths=paths)


def _map_registration_pin(data):
    # Assembly may add or remove relation files before their first publication.
    return pin({key: value for key, value in data.items() if key != 'edge_files'})


def _map_queue_snapshot(root, registry=None):
    """Read the live bound queue, or an explicitly identified Git snapshot."""
    root = Path(root).resolve()
    top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root,
                         capture_output=True, text=True)
    if top.returncode or Path(top.stdout.strip()).resolve() != root:
        return [], {'source': 'not-a-published-queue-snapshot'}
    import coordination

    bound_run = coordination.config(root, 'wcg.workflowRun')
    role = coordination.config(root, 'wcg.role')
    if bound_run and role == 'mapper':
        import map_tasks

        with map_tasks.latest(root, 'map') as (snapshot, ctx):
            tip = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=snapshot, text=True).strip()
            provenance = {
                'source': 'latest-published-workflow', 'tip': tip, 'workflow_run': bound_run}
            if registry is not None:
                published = json.loads(map_tasks._ensure(snapshot, registry).read_bytes())
                provenance['registration_input_pin'] = _map_registration_pin(published)
            return map_tasks.listing(snapshot, ctx=ctx), provenance

    branch = coordination.config(root, 'wcg.branch') or subprocess.check_output(
        ['git', 'branch', '--show-current'], cwd=root, text=True).strip()
    for revision in ['refs/remotes/origin/' + branch, 'HEAD']:
        tip = subprocess.run(['git', 'rev-parse', '--verify', revision], cwd=root, capture_output=True, text=True)
        if not tip.returncode:
            break
    if tip.returncode:
        return [], {'source': 'not-a-published-queue-snapshot'}
    commit = tip.stdout.strip()
    prefix = 'research/operations/map-v2/tasks/'
    names = subprocess.run(['git', 'ls-tree', '-r', '--name-only', '-z', commit, '--', prefix],
                           cwd=root, capture_output=True)
    if names.returncode:
        raise ValueError('Could not read map task names from ' + revision)
    rows = []
    for name in names.stdout.decode('utf-8').split('\0'):
        if name.endswith('.json'):
            saved = subprocess.run(['git', 'show', commit + ':' + name], cwd=root, capture_output=True)
            if saved.returncode:
                raise ValueError('Could not read published map task: ' + name)
            rows.append(json.loads(saved.stdout))
    return rows, {'source': revision, 'tip': commit, 'workflow_run': 'map-v2'}


def _effective_map_done(rows):
    done = [row for row in rows if row['state'] == 'done']
    replaced = {task_id for row in done for task_id in row['definition'].get('supersedes', [])}
    return {row['definition']['task_id']: row for row in done
            if row['definition']['task_id'] not in replaced}


def _map_inputs_current(definition, current_pins):
    ids = definition['object_ids'] + definition.get('read_object_ids', [])
    try:
        expected = {oid: current_pins[oid] for oid in ids}
    except KeyError:
        return False
    return definition.get('input_pins') == expected


def validate_map_follow_ups(definition, receipt, rows, objects, *, final=False):
    """A confirmed deferred comparison names a real task in the same queue."""
    requested = receipt.get('follow_up_tasks', [])
    strings(requested, 'follow_up_tasks')
    overlaps = (definition.get('context_plan') or {}).get('overlap_comparisons', [])
    deferred = {(item['core_id'], item['peer_id']): item['stage']
                for item in overlaps if item['status'] == 'follow-up'}
    closed = receipt.get('closed_overlaps', [])
    if not isinstance(closed, list):
        raise ValueError('closed_overlaps must be a list of deferred pairs with reasons')
    for entry in closed:
        if not isinstance(entry, dict):
            raise ValueError('closed_overlaps requires core_id, peer_id and reason')
        nonempty(entry, ['core_id', 'peer_id', 'reason'])
        pair = (entry['core_id'], entry['peer_id'])
        if pair not in deferred:
            raise ValueError('Unknown or repeated closed overlap: ' + ' / '.join(pair))
        del deferred[pair]
    if not requested and not deferred:
        return
    origin = definition['task_id']
    origin_core = set(definition['object_ids'])
    published = {row['definition']['task_id']: row for row in rows}
    replacements = {old: row for row in published.values() if row['state'] == 'done'
                    for old in row['definition'].get('supersedes', [])}

    def question(task):
        plan = task.get('context_plan')
        value = plan.get('comparison_question') if isinstance(plan, dict) else None
        return ' '.join(value.split()) if isinstance(value, str) else ''

    scheduled = []
    for task_id in requested:
        identity(task_id)
        label = f'Map follow-up {task_id} from {origin}'
        if task_id not in published or task_id == origin:
            raise ValueError(label + ' must be a different published comparison task')
        task_row = published[task_id]
        original = task_row['definition']
        seen = {task_id}
        while task_row['definition']['task_id'] in replacements:
            task_row = replacements[task_row['definition']['task_id']]
            replacement_id = task_row['definition']['task_id']
            if replacement_id in seen or replacement_id == origin:
                raise ValueError(label + ' has an invalid supersession chain')
            seen.add(replacement_id)
        target = task_row['definition']
        ids = set(target['object_ids'] + target.get('read_object_ids', []))
        original_ids = set(original['object_ids'] + original.get('read_object_ids', []))
        comparison_ids = set(original['object_ids']) if len(original['object_ids']) > 1 else original_ids
        stage = original['stage']
        if (stage not in {'3B', '3C'} or stage != target['stage']
                or definition['registry'] != original['registry']
                or definition['registry'] != target['registry']
                or not question(original) or question(original) != question(target)
                or len(comparison_ids) < 2 or not comparison_ids & origin_core
                or not comparison_ids <= ids or ids - objects.keys()):
            raise ValueError(label + ' must retain the same scoped 3B/3C question with a related registered endpoint')
        paths = [objects[oid]['body']['path'] for oid in comparison_ids]
        archives = {path.split('/')[1] for path in paths if path.startswith('archives/')}
        if (not all(path.startswith('archives/') for path in paths)
                or (stage == '3B' and len(archives) != 1)
                or (stage == '3C' and len(archives) < 2)):
            raise ValueError(label + ' must use 3B within one archive or 3C across archives')
        if task_row['state'] == 'withdrawn' or (final and task_row['state'] != 'done'):
            raise ValueError(label + ' has no completed successor. Publish the comparison or repair its originating receipt.')
        if not _map_inputs_current(target, {oid: pin(objects[oid]) for oid in ids}):
            raise ValueError(label + ' has stale registered inputs. Reframe the comparison on the current versions.')
        scheduled.append((stage, comparison_ids))
    for pair, stage in deferred.items():
        if not any(layer == stage and set(pair) <= ids for layer, ids in scheduled):
            raise ValueError('Deferred overlap needs a matching follow_up_tasks ID or a mathematical reason in closed_overlaps: '
                             + ' / '.join(pair))


def _map_queue_final_check(root, registry, data, objects, relations, review):
    rows, snapshot = _map_queue_snapshot(root, registry)
    if snapshot.get('source') == 'latest-published-workflow':
        if snapshot['registration_input_pin'] != _map_registration_pin(data):
            raise ValueError('Local registration input differs from the published registry; run work.py sync and review affected map tasks before final verification')
    if not rows:
        if snapshot.get('source') == 'latest-published-workflow':
            raise ValueError('Publish and complete the map task queue before final verification')
        return
    active = [row['definition']['task_id'] for row in rows if row['state'] not in {'done', 'withdrawn'}]
    if active:
        raise ValueError('Published map queue still has unfinished tasks: ' + ', '.join(active))
    done = _effective_map_done(rows)
    expected = {task_id: pin(row['receipt']) for task_id, row in done.items()}
    if review.get('task_receipt_pins', {}) != expected:
        raise ValueError('Completed map receipts differ from the assembled integration; sync and map assemble again')
    covered = {oid for row in done.values() for oid in row['receipt']['coverage']}
    missing = sorted(objects.keys() - covered)
    if missing:
        raise ValueError(f'Published map receipts lack coverage for {len(missing)} registered objects; examples: '
                         + ', '.join(missing[:5]))
    current_pins = {oid: pin(obj) for oid, obj in objects.items()}
    edge_files = set(data.get('edge_files', []))
    for task_id, row in done.items():
        definition = row['definition']
        if definition['registry'] != registry or not _map_inputs_current(definition, current_pins):
            raise ValueError('Published map receipt has stale inputs; repair task ' + task_id)
        receipt = row['receipt']
        if any(c['state'] == 'needs-decision' for c in receipt['coverage'].values()):
            raise ValueError('Published map receipt has unresolved coverage; repair task ' + task_id)
        validate_map_follow_ups(definition, receipt, rows, objects, final=True)
        try:
            validate_coverage(receipt['coverage'], {oid: objects[oid] for oid in definition['object_ids']}, relations)
        except ValueError as exc:
            raise ValueError(f'Published map receipt needs repair: {task_id}: {exc}. '
                             f'Use research map-draft --repair-task {task_id}.') from exc
        for asset in receipt['assets']:
            contents = ref_bytes(root, asset)
            if asset['path'].endswith('.json'):
                try:
                    output = json.loads(contents)
                except (ValueError, UnicodeError):
                    continue
                if isinstance(output, dict) and 'edge_id' in output and asset['path'] not in edge_files:
                    raise ValueError('Published map edge is missing from the integration: ' + asset['path'])


def check(root, registry=REGISTRY, final=False):
    data, objects = load(root, registry)
    relations = edges(root, data, objects)
    missing = [r['path'] for r in inventory(root, registry) if r['registration'] == 'unregistered']
    pending = [r['path'] for r in data['materials'] if r['disposition'] == 'needs-decision']
    if final and (missing or pending):
        raise ValueError('Final coverage incomplete: %d unregistered, %d needs-decision' % (len(missing), len(pending)))
    if final:
        from registration import check as registration_check
        registration_check(root, registry, final=True)
        coverage = json.loads(_safe_path(root, 'map/coverage.json').read_text())
        validate_coverage(coverage, objects, relations)
        review = integration_check(root, data, objects, relations)
        _map_queue_final_check(root, registry, data, objects, relations, review)
    return {'status': 'structure-valid-not-a-mathematical-verdict', 'objects': len(objects), 'edges': len(relations),
            'unregistered_materials': len(missing), 'pending_materials': len(pending), 'final_coverage': not missing and not pending}


def validate_coverage(coverage, objects, relations):
    if not isinstance(coverage, dict) or set(coverage) != set(objects):
        raise ValueError('Every registered mathematical object requires a map coverage decision')
    for oid, row in coverage.items():
        if row.get('state') not in {'linked', 'isolated-after-review'}:
            raise ValueError('Final graph still has an unresolved relation decision')
        nonempty(row, ['reason', 'comparison_scope', 'object_pin'])
        if row['object_pin'] != pin(objects[oid]):
            raise ValueError('Stale map coverage decision: ' + oid)
        if row['state'] == 'linked':
            strings(row.get('edge_ids'), 'coverage edge_ids', True)
            for eid in row['edge_ids']:
                e = relations.get(eid)
                if (not e or e['status'] != 'accepted' or e['kind'] not in LOGICAL
                        or oid not in e['source_ids'] + e['target_ids']):
                    raise ValueError('Linked coverage must name an accepted mathematical relation for this object')


def object_scopes(objects):
    scopes = set()
    for obj in objects.values():
        name = obj['body']['path']
        if name.startswith('archives/'):
            deepest = re.match(r'archives/[^/]+(?:/subarchives/[^/]+)*', name)[0]
            parts = deepest.split('/')
            scopes.update('/'.join(parts[:i]) for i in range(2, len(parts) + 1, 2))
    return scopes


def integration_check(root, data, objects, relations):
    review = json.loads(_safe_path(root, 'map/integration.json').read_text())
    nonempty(review, ['reviewed_by', 'review_note'])
    if review.get('registry_pin') != pin(data): raise ValueError('Stale integration registry review')
    expected = {eid: pin(e) for eid, e in relations.items() if e['status'] == 'accepted'}
    if review.get('edge_pins') != expected: raise ValueError('Stale integration edge reviews')
    if set(review.get('archive_reviews', {})) != object_scopes(objects):
        raise ValueError('Every archive/subarchive requires a cross-batch integration review')
    for row in [*review['archive_reviews'].values(), review.get('cross_archive_review', {})]:
        nonempty(row, ['comparison_scope', 'outcome'])
        if row.get('unresolved') != []: raise ValueError('Integration still has unresolved relationship decisions')
    return review


def build(root, registry=REGISTRY, final=False):
    report = check(root, registry, final)
    data, objects = load(root, registry)
    relations = edges(root, data, objects)
    graph = {'schema': 2, 'status': 'registered-coverage' if final else 'registered-partial',
             'trust': 'Author-declared mathematical reviews; no automated truth certification',
             'registry': registry, 'registry_pin': pin(data), 'nodes': objects,
             'edges': {i: e for i, e in relations.items() if e['status'] == 'accepted'}}
    outputs = ['map/graph-v2.json']
    for scope in sorted(object_scopes(objects)):
        outputs.append(scope + '/map/graph-v2.json')
    for output in outputs:
        scope = output.rsplit('/map/', 1)[0] if '/map/' in output else ''
        local = {oid for oid, obj in objects.items() if not scope or obj['body']['path'].startswith(scope + '/')}
        selected = {eid: e for eid, e in graph['edges'].items() if local.intersection(e['source_ids'] + e['target_ids'])}
        required = local | {oid for e in selected.values() for oid in e['source_ids'] + e['target_ids']}
        view = dict(graph, scope=scope or '.', nodes={oid: objects[oid] for oid in sorted(required)}, edges=selected,
                    boundary_nodes=sorted(required - local))
        _write_json(_safe_path(root, output), view)
    return dict(report, projections=outputs, publication='local-not-pushed')


def inspect_reference(root, ref, *, body=False):
    """Read a selected reference without turning stale bytes into a global outage."""
    report = {'reference': copy.deepcopy(ref), 'status': 'unavailable'}
    try:
        path = reference(root, ref)
        data = path.read_bytes()
        report['current_sha256'] = digest(data)
        report['status'] = 'current' if report['current_sha256'] == ref['sha256'] else 'changed'
        if body:
            report['text'] = section(data.decode('utf-8'), ref.get('section'))
    except (ValueError, OSError, UnicodeError) as exc:
        report['error'] = str(exc)
        report['status'] = 'unavailable'
    return report


def object_view(root, obj, *, body=False):
    result = copy.deepcopy(obj)
    result['registration_pin'] = pin(obj)
    binding = inspect_reference(root, obj['body'], body=body)
    if 'text' in binding:
        result['body_text'] = binding.pop('text')
    result['body_binding'] = binding
    result['evidence_bindings'] = [inspect_reference(root, ref) for ref in obj['evidence']]
    result['binding_status'] = ('current' if all(r['status'] == 'current' for r in
        [binding, *result['evidence_bindings']]) else 'requires-refresh')
    return result


def relation_catalog(root, data):
    """Index declarations for navigation; validate only selected relations below."""
    result, errors, ambiguous = {}, [], set()
    for name in data.get('edge_files', []):
        try:
            edge = json.loads(_safe_path(root, name).read_text())
            eid = identity(edge.get('edge_id'))
            if eid in result or eid in ambiguous:
                previous = result.pop(eid, None)
                ambiguous.add(eid)
                raise ValueError('Ambiguous duplicate edge ID: ' + eid +
                    (' also declared in ' + previous[0] if previous else ''))
            if not isinstance(edge.get('source_ids'), list) or not isinstance(edge.get('target_ids'), list):
                raise ValueError('Relation endpoints must be explicit lists')
            if any(not isinstance(i, str) for i in edge['source_ids'] + edge['target_ids']):
                raise ValueError('Relation endpoint IDs must be strings')
            result[eid] = (name, edge)
        except (ValueError, OSError, AttributeError, TypeError) as exc:
            errors.append({'path': name, 'error': str(exc)})
    return result, errors


def relation_view(root, data, objects, name, edge):
    result = copy.deepcopy(edge)
    result['path'] = name
    result['declaration_pin'] = pin(edge)
    errors = []
    try:
        edges(root, dict(data, edge_files=[name]), objects, verify=False)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        errors.append(str(exc))
    evidence = edge.get('evidence', [])
    if not isinstance(evidence, list):
        errors.append('Selected relation evidence must be an explicit list')
        evidence = []
    result['evidence_bindings'] = [inspect_reference(root, ref) for ref in evidence]
    if any(r['status'] != 'current' for r in result['evidence_bindings']):
        errors.append('One or more selected relation evidence references need refreshing')
    result['binding_status'] = 'requires-refresh' if errors else 'current'
    result['binding_errors'] = errors
    return result


def search(root, query, registry=REGISTRY, limit=20, *, model=None, truth_statuses=None, kinds=None):
    _, objects = load(root, registry, verify=False)
    terms = query.casefold().split()
    ranked = []
    for oid, obj in objects.items():
        if model and model.casefold() not in obj['model'].casefold():
            continue
        if truth_statuses and obj['truth_status'] not in truth_statuses:
            continue
        if kinds and obj['kind'] not in kinds:
            continue
        text = json.dumps({k: obj[k] for k in ('title', 'statement', 'model', 'scope',
            'quantifiers', 'assumptions', 'keywords', 'aliases', 'legacy_ids') if k in obj}, ensure_ascii=False).casefold()
        score = sum(text.count(term) for term in terms) + sum(20 for term in terms if term in oid.casefold())
        if score or not terms:
            ranked.append((score, oid, obj))
    return [{'object_id': oid, 'version': obj['version'], 'title': obj['title'], 'kind': obj['kind'],
             'model': obj['model'], 'scope': obj['scope'], 'truth_status': obj['truth_status'],
             'objections': obj['objections'], 'path': obj['body']['path'], 'binding_status': 'unchecked-until-open'}
            for _, oid, obj in sorted(ranked, key=lambda row: (-row[0], row[1]))[:limit]]


def context(root, ids, registry=REGISTRY, hops=0, *, edge_ids=None, edge_statuses=None, relation_kinds=None):
    """Complete positive support branches first; optional graph hops add navigation."""
    if hops < 0:
        raise ValueError('Navigation hops must be nonnegative')
    data, objects = load(root, registry, verify=False)
    catalog, unreadable = relation_catalog(root, data)
    if not ids or any(i not in objects for i in ids):
        raise ValueError('Known seed object IDs required')
    chosen = set(edge_ids or [])
    if chosen - catalog.keys():
        raise ValueError('Unknown selected edge IDs: ' + ', '.join(sorted(chosen - catalog.keys())))
    statuses = set(edge_statuses or ['accepted', 'proposed'])
    if statuses - {'accepted', 'proposed', 'rejected'}:
        raise ValueError('Unknown relation status filter')
    if relation_kinds and set(relation_kinds) - (LOGICAL | CONTEXT):
        raise ValueError('Unknown relation kind filter')
    positive = LOGICAL - {'refutes'}
    cache, views = {}, {}
    def ov(oid):
        if oid not in views:
            views[oid] = object_view(root, objects[oid])
        return views[oid]
    def ev(eid):
        if eid not in cache:
            name, edge = catalog[eid]
            cache[eid] = relation_view(root, data, objects, name, edge)
        return cache[eid]
    incoming, incident = {}, {}
    for eid, (_, edge) in catalog.items():
        for oid in set(edge['source_ids'] + edge['target_ids']):
            incident.setdefault(oid,set()).add(eid)
        if edge.get('status') != 'accepted' or edge.get('kind') not in positive or 'contribution' in edge:
            continue
        sources, targets = set(edge['source_ids']), set(edge['target_ids'])
        # A shared endpoint is already an assumption in either direction.
        for oid in targets - sources:
            incoming.setdefault(oid,[]).append((eid,'forward'))
        if edge.get('kind') == 'equivalent_to':
            for oid in sources - targets:
                incoming.setdefault(oid,[]).append((eid,'reverse'))
    required, queue, expanded, support = set(ids), deque(ids), set(), {}
    proof_edges = set()
    while queue:
        target = queue.popleft()
        if target in expanded:
            continue
        expanded.add(target)
        options = incoming.get(target,[])
        selected_options = [option for option in options if option[0] in chosen]
        if selected_options:
            options = selected_options
        support[target] = []
        for eid,direction in sorted(options):
            e = ev(eid)
            premises = e['source_ids'] if direction == 'forward' else e['target_ids']
            conclusions = e['target_ids'] if direction == 'forward' else e['source_ids']
            unknown = [i for i in e['source_ids'] + e['target_ids'] if i not in objects]
            endpoint_errors = [i for i in e['source_ids'] + e['target_ids']
                if i in objects and ov(i)['binding_status'] != 'current']
            unpaid = [{'object_id': i, 'truth_status': objects[i]['truth_status'],
                       'binding_status': ov(i)['binding_status'], 'objections': objects[i]['objections']}
                      for i in premises if i in objects and
                      (objects[i]['truth_status'] not in {'definition', 'proved'} or ov(i)['binding_status'] != 'current')]
            support[target].append({'edge_id': eid, 'direction': direction,
                'all_premises': list(premises), 'conclusion_ids': [i for i in conclusions if i not in premises],
                'conditions': e.get('conditions'), 'scope': e.get('scope'), 'relation_mode': e.get('relation_mode'),
                'explanation': e.get('explanation'), 'evidence': e.get('evidence', []),
                'unpaid_premises': unpaid, 'unknown_endpoints': unknown,
                'endpoint_binding_changes': endpoint_errors,
                'current_declared_support': not unknown and not endpoint_errors and e['binding_status'] == 'current',
                'premise_support_options': list(premises)})
            proof_edges.add(eid)
            # Every member of a selected ALL relation is included, irrespective of hop count.
            for oid in e['source_ids'] + e['target_ids']:
                if oid in objects:
                    required.add(oid)
            queue.extend(i for i in premises if i in objects and i not in expanded)
    proof_objects = set(required)
    related = set(proof_edges)
    def allowed(e):
        return e['edge_id'] in chosen or (e.get('status') in statuses
            and (not relation_kinds or e.get('kind') in relation_kinds))
    # Direct failures and concrete research leads are useful even with zero navigation hops.
    candidates = set().union(*(incident.get(oid,set()) for oid in proof_objects))
    for eid in candidates:
        e = catalog[eid][1]
        if allowed(e) and set(e['source_ids'] + e['target_ids']).intersection(proof_objects):
            if eid not in proof_edges:
                related.add(eid)
                required.update(i for i in e['source_ids'] + e['target_ids'] if i in objects)
    for _ in range(hops):
        previous = set(required)
        candidates = set().union(*(incident.get(oid,set()) for oid in previous))
        for eid in candidates:
            e = catalog[eid][1]
            if allowed(e) and set(e['source_ids'] + e['target_ids']).intersection(previous):
                related.add(eid)
                required.update(i for i in e['source_ids'] + e['target_ids'] if i in objects)
        if required == previous:
            break
    if missing := chosen - related:
        raise ValueError('Selected edges do not connect to this seed context: ' + ', '.join(sorted(missing))
                         + '. Seed one of their endpoints or increase navigation hops.')
    picked = [ev(eid) for eid in sorted(related)]
    return {'seed_ids': ids, 'hops': hops, 'navigation_only': True, 'registry': registry, 'registry_pin': pin(data),
            'support_semantics': 'OR between support_options; ALL within each option. Conditions and unpaid premises remain explicit. Proof-step contributions stay in research_leads with their result and remaining obligations.',
            'proof_closure_object_ids': sorted(proof_objects), 'support_options': support,
            'objects': [ov(i) for i in sorted(required)], 'edges': picked,
            'refutations': [e for e in picked if e.get('kind') == 'refutes' and 'contribution' not in e],
            'research_leads': [e for e in picked if e['edge_id'] not in proof_edges
                               and (e.get('kind') != 'refutes' or 'contribution' in e)],
            'unavailable_edge_files': unreadable,
            'instruction': 'Read the selected body and exact evidence on demand. Accepted is an author declaration, not a mathematical verdict. Navigation hops do not truncate selected logical ALL-premise closure. Context links and proposed/rejected relations never supply proved premises.'}


def packet(root, spec, profile, registry=REGISTRY):
    if profile not in {'obstacle', 'full'}:
        raise ValueError('Only obstacle and full solver profiles are used')
    identity(spec['problem_id'])
    target = read_ref(root, spec['problem'])
    definitions = [read_ref(root, ref) for ref in spec['definitions']]
    obstacles = [read_ref(root, ref) for ref in spec['obstacles']]
    result = {'problem_id': spec['problem_id'], 'profile': profile, 'target': target,
              'definitions': definitions, 'obstacles': obstacles,
              'input_refs': {key: copy.deepcopy(spec[key]) for key in ('problem', 'definitions', 'obstacles')},
              'task': 'Keep this exact original problem and its conditions. The current concrete assignment takes priority: continue a long-lived research line, extract an applicable argument, or independently challenge the specified claim. Return to the requesting researcher; use any useful mathematical method and save substantive progress and explicit gaps.',
              'launch': {'fork_turns': 'none', 'model': 'gpt-6.1-sol', 'reasoning_effort': 'ultra',
                         'instruction': 'Supply this packet with the current concrete assignment and matching task prompt. Follow up the existing researcher for a continuing line; launch a fresh-history worker for temporary reading, independent challenge or a genuinely new line. Apply the declared model and effort to actual launches unless the user selects otherwise; preserve comparison input isolation.'},
              'limit': 'Context selection is not a file-system access-control boundary.'}
    if 'collaboration_scope' in spec:
        result['collaboration_scope'] = _collaboration_scope(root, spec['problem']['path'], spec['collaboration_scope'])
    if profile == 'full':
        seeds = spec.get('seed_ids', [])
        strings(seeds, 'seed_ids')
        if seeds:
            result['context'] = context(root, seeds, registry, spec.get('hops', 0),
                edge_ids=spec.get('edge_ids'), edge_statuses=spec.get('edge_statuses'), relation_kinds=spec.get('relation_kinds'))
            result['registry_pin'] = result['context']['registry_pin']
        else:
            if spec.get('edge_ids'):
                raise ValueError('Select relevant seed objects for the requested proof branches; omit both when no prior results are needed')
            result['context'] = {'seed_ids': [], 'registry': registry, 'objects': [], 'edges': [],
                'support_options': {}, 'proof_closure_object_ids': [], 'refutations': [], 'research_leads': [],
                'instruction': 'No prior mathematical results selected. Start from the exact problem, definitions and obstacles; retrieve genuinely relevant results later, without inserting unrelated seeds.'}
        result['retrieval'] = {'registry': registry, 'commands': ['research search', 'research show', 'research context']}
    return result


def run_path(root, run_id):
    return _safe_path(root, 'research/runs/' + identity(run_id) + '/run.json')


def _saved_research_inputs(root, run):
    """Use immutable input declarations, never a silently edited current spec."""
    saved_scope = None
    for profile, expected in run['packet_pins'].items():
        path = run_path(root, run['run_id']).parent / ('packet-' + profile + '.json')
        saved = json.loads(path.read_text())
        if pin(saved) != expected:
            raise ValueError('Saved packet changed for ' + run['run_id'])
        saved_scope = saved.get('collaboration_scope')
        refs = saved.get('input_refs')
        if refs is not None:
            break
    else:
        # Compatibility with packets predating input_refs.
        spec = json.loads(_safe_path(root, run['spec']).read_text())
        if pin(spec) != run['spec_pin']:
            raise ValueError('Saved spec changed for ' + run['run_id'])
        refs = spec

    def exact(ref):
        if (not isinstance(ref, dict) or not {'path', 'sha256'} <= ref.keys()
                or not isinstance(ref['sha256'], str)
                or not re.fullmatch(r'[0-9a-f]{64}', ref['sha256'])):
            raise ValueError('Exact problem/definition reference required')
        _safe_path(root, ref['path'])
        if 'section' in ref and (not isinstance(ref['section'], str) or not ref['section'].strip()):
            raise ValueError('Explicit section title required')
        return {key: ref[key] for key in ('path', 'sha256', 'section') if key in ref}

    return ({'problem': exact(refs['problem']),
             'definitions': sorted((exact(ref) for ref in refs['definitions']), key=pin)},
            saved_scope)


def _collaboration_scope(root, problem_path, declared=None):
    """Route within the saved problem's archive, never a clone's configuration."""
    if declared is not None:
        _safe_path(root, declared)
        if not re.fullmatch(r'archives/[^/]+(?:/subarchives/[^/]+)*', declared):
            raise ValueError('collaboration_scope must name an archive or subarchive directory')
    parts = Path(problem_path).parts
    if len(parts) < 3 or parts[0] != 'archives':
        return declared
    stop = 2
    while stop + 2 < len(parts) and parts[stop] == 'subarchives':
        stop += 2
    scope = '/'.join(parts[:stop])
    _safe_path(root, scope)
    if declared is not None and declared != scope:
        raise ValueError('collaboration_scope conflicts with the problem archive: expected ' + scope)
    return scope


def _collaboration_route(root, inputs, declared_scope):
    fingerprint = pin(inputs)
    scope = _collaboration_scope(root, inputs['problem']['path'], declared_scope)
    return {'status': 'retired',
            'input_fingerprint': fingerprint, 'collaboration_scope': scope,
            'shared_workspace': None, 'shared_entry': None, 'shared_entry_exists': False,
            'legacy_shared_workspace': None, 'legacy_shared_entry': None}


def peers(root, run_id):
    """Find exact-input peers without treating arbitrary problem_id as identity.

    This is a local-snapshot discovery aid, not a lease, a task claim, a remote
    refresh, or a proof that the listed researchers are currently running.
    """
    run = json.loads(run_path(root, run_id).read_text())
    inputs, declared_scope = _saved_research_inputs(root, run)
    route = _collaboration_route(root, inputs, declared_scope)
    matches, related, revisions, warnings = [], [], [], []
    for path in sorted((_safe_path(root, 'research/runs')).glob('*/run.json')):
        try:
            other = json.loads(path.read_text())
            identity(other['run_id'])
            if run_path(root, other['run_id']) != path:
                raise ValueError('Run ID does not match its directory')
            other_inputs, other_scope = _saved_research_inputs(root, other)
            if other_inputs['problem']['path'] != inputs['problem']['path']:
                continue
            exact_inputs = other_inputs == inputs
            row = {'run_id': other['run_id'], 'problem_id': other['problem_id'],
                   'same_run': other['run_id'] == run_id, 'declared_state': other['state'],
                   'spec': other['spec'], 'workspace': str(Path(other['spec']).parent),
                   'main_notes': [{'solver_id': sid, 'note': solver['note'],
                                   'next_action': solver['next_action']}
                                  for sid, solver in other.get('solvers', {}).items()
                                  if sid.casefold() == 'main'],
                   'saved_solver_count': len(other.get('solvers', {}))}
            row.update(_collaboration_route(root, other_inputs, other_scope))
            if other_inputs['problem'] != inputs['problem']:
                row.update(problem=other_inputs['problem'], definitions=other_inputs['definitions'],
                           instruction='The target source has a different SHA or section. Read both saved formulations and check their mathematical relationship before reusing results; this is not an exact-input peer.')
                revisions.append(row)
            elif exact_inputs:
                matches.append(row)
            else:
                row['definitions'] = other_inputs['definitions']
                related.append(row)
        except (ValueError, OSError, KeyError, TypeError) as exc:
            warnings.append({'run': path.relative_to(root).as_posix(), 'error': str(exc)})
    scopes = {row['collaboration_scope'] for row in matches if row['collaboration_scope']}
    scope_conflicts = []
    if len(scopes) > 1:
        scope_conflicts = [{key: row[key] for key in ('run_id', 'collaboration_scope', 'shared_entry', 'legacy_shared_entry')}
                           for row in matches if row['collaboration_scope']]
    return {**route, 'inputs': inputs,
            'peer_runs': matches, 'same_target_different_definitions': related,
            'same_target_revisions': revisions,
            'scope_conflicts': scope_conflicts,
            'discovery_warnings': warnings,
            'instruction': 'Research boards and collaboration pages have been retired and deleted. Inspect peer RUNs, saved mathematical workspaces and exact inputs only; do not create or recreate a shared board. Research-agent design is paused until hypergraph closeout. Exact-source matching is not proof of mathematical equivalence; revisions and scope conflicts need source comparison. Saved states do not establish live agents. This command neither contacts peers nor claims work.'}


def init_run(root, run_id, spec_file, registry=REGISTRY, *, mode='comparison'):
    path = run_path(root, run_id)
    if path.exists():
        raise ValueError('Run exists; resume it instead')
    spec = json.loads(_safe_path(root, spec_file).read_text())
    profiles = ('full',) if mode == 'open' else ('obstacle', 'full')
    packets = {profile: packet(root, spec, profile, registry) for profile in profiles}
    if mode == 'open':
        packets['full']['launch'] = {
            **WORKER_LAUNCH,
            'instruction': 'Dispatch the current concrete assignment with these worker defaults unless the user selects otherwise; record the actual agent ID and settings. Keep long-lived researchers on their continuing mathematical lines. Temporary readers and independent challengers answer the assigned question and return to its requester. Main combines the resulting mathematics without replaying every derivation.',
        }
    home = path.parent
    for profile, value in packets.items():
        _write_json(home / ('packet-' + profile + '.json'), value)
    roster = [] if mode == 'open' else copy.deepcopy(SOLVER_ROSTER)
    if mode == 'open':
        launch_plan = {'platform': 'Work', 'mode': 'open',
                       'instruction': 'Main assigns actual mathematical obligations as needed; init itself launches no model.'}
    else:
        launch_plan = {'platform': 'Work', 'exact_count': len(roster),
                       'instruction': 'Main launches every roster slot through the actual platform; init itself launches no model.'}
    state = {'schema': 2, 'run_id': run_id, 'problem_id': spec['problem_id'], 'state': 'working',
             'spec': spec_file, 'spec_pin': pin(spec), 'registry': registry, 'solvers': {},
             'solver_count': len(roster), 'solver_roster': roster,
             'launch_plan': launch_plan,
             'registry_pin': packets['full'].get('registry_pin'),
             'context_snapshot': {
                 'objects': {o['object_id']: o['registration_pin'] for o in packets['full']['context']['objects']},
                 'edges': {e['edge_id']: e['declaration_pin'] for e in packets['full']['context']['edges']}},
             'packet_pins': {profile: pin(value) for profile, value in packets.items()},
             'note': 'No agents were launched by this command; Main starts them through the Work orchestration API.'}
    if state['registry_pin'] is None:
        state.pop('registry_pin')
    _write_json(path, state)
    return {'status': 'initialized-local-not-pushed', 'run': path.relative_to(root).as_posix(),
            'packets': [str((home / ('packet-' + p + '.json')).relative_to(root)) for p in packets],
            'solver_count': len(roster), 'solver_roster': roster, 'agents_launched': 0,
            'collaboration': peers(root, run_id) if mode == 'open' else None}


def update_run(root, run_id, solver_id, profile, note, next_action, state, feedback=None, agent_id=None, ack_feedback=False,
               model=None, reasoning_effort=None, fork_turns=None):
    identity(solver_id)
    if profile not in {'obstacle', 'full'} or state not in STATES or not next_action.strip():
        raise ValueError('Explicit solver profile, state and concrete next action required')
    if feedback is not None and not feedback.strip():
        raise ValueError('Concrete feedback required')
    if feedback is not None and ack_feedback:
        raise ValueError('Send new feedback or acknowledge the pending feedback, not both in one save')
    path = run_path(root, run_id)
    run = json.loads(path.read_text())
    roster = {s['solver_id']: s['profile'] for s in run.get('solver_roster', [])}
    on_demand = run.get('launch_plan', {}).get('mode') == 'open'
    if on_demand and profile not in run['packet_pins']:
        raise ValueError('Use the packet profile saved for this run')
    if not on_demand and roster and (solver_id not in roster or roster[solver_id] != profile):
        raise ValueError('Use a declared Solver roster slot with its original profile')
    old = run['solvers'].get(solver_id, {})
    same_agent = agent_id is None or agent_id == old.get('agent_id')
    launch = copy.deepcopy(old.get('launch', {})) if same_agent else {}
    if fork_turns is not None and fork_turns not in {'none', 'all'}:
        raise ValueError('fork_turns must be none or all')
    for key, val in (('model', model), ('reasoning_effort', reasoning_effort), ('fork_turns', fork_turns)):
        if val is not None:
            if not isinstance(val, str) or not val.strip():
                raise ValueError('Explicit launch setting required: ' + key)
            launch[key] = val
    old_pending = old.get('feedback_pending', bool(old.get('feedback')))
    if old and old['profile'] != profile:
        raise ValueError('Do not silently change a solver context profile')
    note_bytes = _safe_path(root, note).read_bytes()
    note_bytes.decode('utf-8')
    # Immutable events retain the previous result and all pending feedback.
    event_id = uuid.uuid4().hex
    snapshot = _safe_path(root, (path.parent / 'notes' / (event_id + '.md')).relative_to(root).as_posix())
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_bytes(note_bytes)
    ref = {'path': snapshot.relative_to(root).as_posix(), 'sha256': digest(note_bytes)}
    event = {'event_id': event_id, 'continuation_of': old.get('latest_event'), 'solver_id': solver_id,
             'profile': profile, 'note': ref, 'next_action': next_action, 'state': state,
             'agent_id': agent_id or old.get('agent_id'),
             'feedback': feedback if feedback is not None else old.get('feedback'),
             'feedback_inherited': feedback is None and old.get('feedback') is not None,
             'feedback_pending': feedback is not None or (old_pending and not ack_feedback),
             'feedback_acknowledged': bool(ack_feedback and old_pending)}
    if launch:
        event['launch'] = launch
    _write_json(_safe_path(root, (path.parent / 'events' / (event_id + '.json')).relative_to(root).as_posix()), event)
    run['solvers'][solver_id] = dict(event, latest_event=event_id)
    if on_demand and solver_id not in roster:
        run['solver_roster'].append({'solver_id': solver_id, 'profile': profile})
        run['solver_count'] = len(run['solver_roster'])
    _write_json(path, run)
    return {'status': 'saved-local-not-pushed', 'event_id': event_id, 'continuation_of': event['continuation_of']}


def resume(root, run_id):
    path = run_path(root, run_id)
    run = json.loads(path.read_text())
    warnings, packet_bindings, histories = [], {}, {}
    try:
        spec = json.loads(_safe_path(root, run['spec']).read_text())
        if pin(spec) != run['spec_pin']:
            warnings.append('The current spec changed. Continue the saved original packet or explicitly create a newly framed run; do not silently substitute the new target.')
    except (ValueError, OSError) as exc:
        warnings.append('Current spec unavailable; use the saved packet: ' + str(exc))
    packets = {}
    for profile, expected in run['packet_pins'].items():
        relative = (path.parent / ('packet-' + profile + '.json')).relative_to(root).as_posix()
        try:
            saved = json.loads(_safe_path(root, relative).read_text())
            packets[profile] = saved
            packet_bindings[profile] = {'path': relative, 'status': 'current' if pin(saved) == expected else 'changed'}
            if pin(saved) != expected:
                warnings.append('Saved '+profile+' packet differs from its original pin; recover its prior bytes from the published run before claiming the same input.')
        except (ValueError, OSError) as exc:
            packet_bindings[profile] = {'path': relative, 'status': 'unavailable', 'error': str(exc)}
    for solver_id, solver in run['solvers'].items():
        chain, seen, current = [], set(), solver.get('latest_event')
        while current:
            if current in seen:
                warnings.append('Continuation history has a cycle for '+solver_id)
                break
            seen.add(current)
            try:
                identity(current)
                event_path = path.parent/'events'/(current+'.json')
                event = json.loads(event_path.read_text())
                chain.append(dict(event, event_path=event_path.relative_to(root).as_posix(),
                                  note_binding=inspect_reference(root,event['note'])))
                current = event.get('continuation_of')
            except (ValueError, OSError, KeyError) as exc:
                warnings.append('Missing continuation event for '+solver_id+': '+str(exc))
                break
        histories[solver_id] = chain
        note = inspect_reference(root,solver['note'])
        if note['status'] != 'current':
            warnings.append('Latest note needs recovery for '+solver_id+'; inspect the preceding immutable events.')
    changes = {'saved_registry_pin': run.get('registry_pin'), 'registry_changed': None,
               'objects_changed': [], 'edges_changed': [], 'new_incident_edges': [], 'stale_selected_refs': []}
    try:
        data, objects = load(root,run['registry'],verify=False)
        changes['current_registry_pin'] = pin(data)
        changes['registry_changed'] = run.get('registry_pin') not in {None,pin(data)}
        snapshot = run.get('context_snapshot',{})
        if not snapshot and 'full' in packets:
            ctx = packets['full'].get('context',{})
            snapshot = {'objects':{o['object_id']:o.get('registration_pin',pin({k:v for k,v in o.items()
                if k not in {'registration_pin','body_binding','evidence_bindings','binding_status','body_text'}})) for o in ctx.get('objects',[])},
                'edges':{e['edge_id']:e.get('declaration_pin') for e in ctx.get('edges',[])}}
        catalog, _ = relation_catalog(root,data)
        selected_objects = set(snapshot.get('objects', {}))
        for eid, (name, edge) in catalog.items():
            if eid not in snapshot.get('edges', {}) and selected_objects.intersection(edge['source_ids'] + edge['target_ids']):
                changes['new_incident_edges'].append({'edge_id': eid, 'path': name,
                    'kind': edge.get('kind'), 'status': edge.get('status'),
                    'instruction': 'Relation absent from the saved selected context; open its current context before using it.'})
        for oid, expected in snapshot.get('objects',{}).items():
            obj = objects.get(oid)
            if obj is None or pin(obj) != expected:
                changes['objects_changed'].append({'object_id':oid,'saved_pin':expected,
                    'current_pin':pin(obj) if obj else None,'current_version':obj.get('version') if obj else None})
            if obj:
                view = object_view(root,obj)
                if view['binding_status'] != 'current':
                    changes['stale_selected_refs'].append({'object_id':oid,'body':view['body_binding'],
                        'evidence':view['evidence_bindings']})
        for eid, expected in snapshot.get('edges',{}).items():
            current = catalog.get(eid)
            if current is None or expected is not None and pin(current[1]) != expected:
                changes['edges_changed'].append({'edge_id':eid,'saved_pin':expected,
                    'current_pin':pin(current[1]) if current else None})
            elif current:
                view = relation_view(root,data,objects,current[0],current[1])
                if view['binding_status'] != 'current':
                    changes['stale_selected_refs'].append({'edge_id':eid,'errors':view['binding_errors']})
    except (ValueError, OSError, KeyError) as exc:
        no_initial_results = ('full' in packets and not run.get('registry_pin')
                              and not packets['full'].get('context', {}).get('objects'))
        if (no_initial_results and isinstance(exc, FileNotFoundError)
                and exc.filename == str(_safe_path(root, run['registry']))):
            changes['registry_available'] = False
            changes['instruction'] = 'This run selected no prior results; continue its saved original problem and notes. A registry is not required before doing mathematics.'
        else:
            changes['registry_error'] = str(exc)
            warnings.append('Saved notes and packets remain recoverable; the current registry needs attention: '+str(exc))
    head = subprocess.run(['git','rev-parse','HEAD'],cwd=root,capture_output=True,text=True)
    roster = run.get('solver_roster', SOLVER_ROSTER)
    collaboration = None
    if run.get('launch_plan', {}).get('mode') == 'open':
        try:
            collaboration = peers(root, run_id)
        except (ValueError, OSError, KeyError, TypeError) as exc:
            collaboration = {'status': 'input-recovery-required', 'error': str(exc),
                             'instruction': 'Recover the original saved input before matching peers; continue recovering notes and feedback below.'}
    return {'run':run,'solver_count':run.get('solver_count',len(roster)),'solver_roster':roster,
            'collaboration': collaboration,
            'packet_bindings':packet_bindings,'event_history':histories,
            'recent_feedback':{i:s.get('feedback') for i,s in run['solvers'].items() if s.get('feedback')},
            'pending_feedback':{i:s.get('feedback') for i,s in run['solvers'].items()
                                if s.get('feedback_pending', bool(s.get('feedback'))) and s.get('feedback')},
            'version_changes':changes,'recovery_warnings':warnings,
            'local_head':head.stdout.strip() if not head.returncode else None,
            'instruction':'Continue the recorded agent. If unavailable, restore the same input profile from its saved packet, latest readable immutable note, concrete feedback and event lineage. Version changes are targeted reading tasks, not a reason to discard existing mathematics or rescan the whole repository.',
            'publication':'Local HEAD is not remote confirmation; checkpoint and verify pushed separately.'}


def _map_repair_reasons(row, current_pins):
    reasons = []
    if not _map_inputs_current(row['definition'], current_pins):
        reasons.append('changed-registration-input')
    if any(value['state'] == 'needs-decision' for value in row['receipt']['coverage'].values()):
        reasons.append('needs-decision')
    return reasons


def draft_map_repairs(root, task_ids, output, registry, task_prefix, context_options=None):
    """Refresh changed inputs on unfinished work and replace affected done batches."""
    import registration

    root = Path(root).resolve()
    identity(task_prefix)
    data, objects = load(root, registry, verify=False)
    rows, snapshot = _map_queue_snapshot(root)
    done = _effective_map_done(rows)
    pending = {row['definition']['task_id']: row for row in rows
               if row['state'] not in {'done', 'withdrawn'}}
    occupied = {row['definition']['task_id'] for row in rows}
    active_targets = {old_id for row in rows if row['state'] not in {'done', 'withdrawn'}
                      for old_id in row['definition'].get('supersedes', [])}
    current_pins = {oid: pin(obj) for oid, obj in objects.items()}
    retired = data.get('retired_objects', {})
    canonical_assets = set(data.get('edge_files', []))
    budget = registration.context_budget(**(context_options or {}))
    tasks = []
    for old_id in dict.fromkeys(task_ids):
        identity(old_id)
        if old_id in pending:
            definition = pending[old_id]['definition']
            ids = definition['object_ids'] + definition.get('read_object_ids', [])
            if definition['registry'] != registry or set(ids) - objects.keys():
                raise ValueError('Unfinished repair needs the same registry and surviving object IDs: ' + old_id)
            if _map_inputs_current(definition, current_pins):
                continue
            context = copy.deepcopy(definition.get('context_plan') or {})
            refs = [ref for oid in ids for ref in [objects[oid]['body'], *objects[oid]['evidence']]]
            unique = list({json.dumps(ref, sort_keys=True): ref for ref in refs}.values())
            if 'overlap_comparisons' in context:
                context['overlap_comparisons'] = [pair for pair in context['overlap_comparisons']
                                                  if pair['peer_id'] in objects]
                for pair in context['overlap_comparisons']:
                    basis = objects[pair['peer_id']]['body']
                    if basis in objects[pair['core_id']]['evidence']:
                        pair['basis'] = basis
            payload = [objects[oid] for oid in ids]
            task_budget = context.get('budget') or budget
            reading = registration.reading_cost(root, unique, metadata=payload, model=task_budget['model'])
            reading['task_overhead_tokens'] = 32 * len(ids)
            reading['estimated_tokens'] += reading['task_overhead_tokens']
            read_changed = any(definition['input_pins'].get(oid) != current_pins[oid]
                               for oid in definition.get('read_object_ids', []))
            recheck = [oid for oid in definition['object_ids']
                       if read_changed or definition['input_pins'].get(oid) != current_pins[oid]]
            context.pop('reading_passes', None)
            context.update(budget=task_budget, reading_refs=unique, reading=reading,
                           oversized=reading['estimated_tokens'] > task_budget['reading_tokens'],
                           requires_export=bool(reading['unmeasured_refs']),
                           recheck_core_object_ids=recheck,
                           note='Resume the same question on current inputs. Reuse valid draft work and read changed sources in order.')
            tasks.append({**definition, 'input_pins': {oid: current_pins[oid] for oid in ids},
                          'context_plan': context})
            continue
        if old_id not in done or done[old_id]['definition']['registry'] != registry:
            raise ValueError('Repair requires an unfinished or effective done task for this registry: ' + old_id)
        if old_id in active_targets:
            raise ValueError('A repair is already in the queue; resume it or withdraw a stale replacement: ' + old_id)
        old = done[old_id]
        definition = old['definition']
        old_core = definition['object_ids']
        removed = [oid for oid in old_core if oid not in objects]
        if any(not isinstance(retired.get(oid), str) or not retired[oid].strip() for oid in removed):
            raise ValueError('Repair requires explicit registry retirement for missing core IDs: ' + old_id)
        core = [oid for oid in old_core if oid in objects]
        reads = [oid for oid in definition.get('read_object_ids', []) if oid in objects] if core else []
        inputs = {oid: current_pins[oid] for oid in core + reads}
        task_id = identity(task_prefix + '-repair-' + pin({'supersedes': old_id, 'registry': registry,
                                                            'inputs': inputs})[:16])
        stem = task_id
        revision = 1
        while task_id in occupied:
            revision += 1
            task_id = identity(stem + '-' + str(revision))
        assets = old['receipt']['assets']
        write_paths = ['map/edges/' + task_id, 'map/receipts/' + task_id + '.json']
        if core:
            # A previous noncanonical edge can only be retained if the new
            # task reserves its exact path. Preserve its required old SHA.
            write_paths.extend(ref['path'] for ref in assets if ref['path'] not in canonical_assets)
        payload = [objects[oid] for oid in core + reads]
        refs = [ref for obj in payload for ref in [obj['body'], *obj['evidence']]]
        reading_refs = list({json.dumps(ref, sort_keys=True): ref for ref in refs}.values())
        reading = registration.reading_cost(root, reading_refs, metadata=payload, model=budget['model'])
        reading['task_overhead_tokens'] = 32 * len(payload)
        reading['estimated_tokens'] += reading['task_overhead_tokens']
        read_changed = any(definition['input_pins'].get(oid) != current_pins.get(oid)
                           for oid in definition.get('read_object_ids', []))
        recheck = [oid for oid in core if read_changed
                   or old['receipt']['coverage'][oid]['state'] == 'needs-decision'
                   or definition['input_pins'].get(oid) != current_pins[oid]]
        reasons = _map_repair_reasons(old, current_pins)
        if not reasons:
            # An explicit repair can address a bad receipt or asset even
            # when every registered object still has the same version.
            reasons = ['receipt-review']
            recheck = core
        tasks.append({'task_id': task_id, 'stage': definition['stage'], 'registry': registry,
                      'supersedes': [old_id], 'object_ids': core, 'read_object_ids': reads,
                      'input_pins': inputs, 'write_paths': list(dict.fromkeys(write_paths)),
                      'goal': 'Resolve the changed inputs or unanswered comparison in ' + old_id
                              + '; reuse still valid coverage, and explicitly dispose each prior asset.',
                      'context_plan': {'budget': budget, 'reading': reading,
                                       'reading_refs': reading_refs,
                                       'oversized': reading['estimated_tokens'] > budget['reading_tokens'],
                                       'requires_export': bool(reading['unmeasured_refs']),
                                       'prior_assets': assets, 'retired_core_object_ids': removed,
                                       'recheck_core_object_ids': recheck,
                                       'repair_reasons': reasons,
                                       'note': 'Read the previous task and receipt. Carry forward valid work. '
                                               'If needed, read the same scope in ordered passes. '
                                               'A retirement-only task lists no coverage or new assets.'}})
        old_context = definition.get('context_plan', {})
        for field in ('comparison_question', 'comparison_priority', 'scope_hint'):
            if field in old_context:
                tasks[-1]['context_plan'][field] = old_context[field]
        old_groups = old_context.get('comparison_groups', [])
        groups = [[oid for oid in group if oid in inputs] for group in old_groups]
        groups = [group for group in groups if group]
        if len(groups) > 1:
            tasks[-1]['context_plan']['comparison_groups'] = groups
    _write_json(_safe_path(root, output), tasks)
    return {'status': 'map-repairs-draft-local-not-pushed', 'path': output,
            'tasks': len(tasks), 'core_objects': sum(len(t['object_ids']) for t in tasks),
            'queue_snapshot': snapshot,
            'instruction': 'Review the refreshed inputs and prior assets, then map plan. '
                           'Unfinished work keeps its task ID and owner. Replacements of done work dispose each prior asset.'}


def map_overlap_candidates(objects, deepest=None):
    """Assign exact proof references to one core's comparison."""
    if deepest is None:
        deepest = {oid: max(object_scopes({oid: obj}), key=len, default='.')
                   for oid, obj in objects.items()}

    def locator(ref):
        return ref['path'], ref['sha256'], ref.get('section')

    owners, directed = {}, {}
    for oid, obj in objects.items():
        owners.setdefault(locator(obj['body']), []).append(oid)
        if obj['kind'].casefold() not in {'definition', 'model', '定义', '模型'}:
            directed[oid] = {}
    for oid, targets in directed.items():
        for ref in objects[oid]['evidence']:
            matches = owners.get(locator(ref), ())
            if len(matches) == 1:
                peer = matches[0]
                if (peer in directed and peer != oid
                        and deepest[oid].startswith('archives/') and deepest[peer].startswith('archives/')):
                    targets[peer] = ref
    return {oid: {peer: ref for peer, ref in targets.items()
                  if oid < peer or oid not in directed[peer]}
            for oid, targets in directed.items()}


def plan_map_overlap(root, objects, core, read_ids, groups, budget, output_tokens,
                     overlaps, *, contextual=(), cache=None, deepest=None):
    """Measure shared reads and keep exact comparisons that need a separate pass."""
    import registration

    cache = {} if cache is None else cache
    reads = list(read_ids)
    assigned = set(core + reads)
    group_of = {oid: i for i, group in enumerate(groups) for oid in group}
    comparisons = [{'core_id': oid, 'peer_id': peer, 'basis': ref, 'status': 'follow-up'}
                   for oid in core for peer, ref in overlaps.get(oid, {}).items()
                   if group_of.get(peer) != group_of[oid]]
    comparisons.sort(key=lambda item: (
        objects[item['core_id']]['body']['path'] != item['basis']['path'],
        'section' not in item['basis'], item['core_id'], item['peer_id']))
    scopes = deepest if deepest is not None else {
        oid: max(object_scopes({oid: objects[oid]}), key=len, default='.')
        for item in comparisons for oid in (item['core_id'], item['peer_id'])}

    def local(item):
        return scopes[item['core_id']] == scopes[item['peer_id']]

    for item in comparisons:
        core_archive = scopes[item['core_id']].split('/')[:2]
        peer_archive = scopes[item['peer_id']].split('/')[:2]
        item['stage'] = '3B' if core_archive == peer_archive else '3C'

    def measure(ids):
        payload = [objects[oid] for oid in ids]
        refs = [ref for obj in payload for ref in [obj['body'], *obj['evidence']]]
        metadata = {'objects': payload, 'overlap_comparisons': comparisons} if comparisons else payload
        reading = registration.reading_cost(root, refs, metadata=metadata, cache=cache, model=budget['model'])
        reading['task_overhead_tokens'] = 32 * len(ids)
        reading['estimated_tokens'] += reading['task_overhead_tokens']
        return payload, refs, reading

    payload, refs, reading = measure(core + reads)
    oversized = (output_tokens > budget['output_tokens']
                 or reading['estimated_tokens'] > budget['reading_tokens'])
    issues = {}
    if not oversized and not reading['unmeasured_refs']:
        peers = dict.fromkeys([item['peer_id'] for item in comparisons if local(item)] + list(contextual))
        for oid in peers:
            if oid in assigned:
                continue
            try:
                trial_payload, trial_refs, trial = measure(core + reads + [oid])
            except (ValueError, OSError) as exc:
                issues[oid] = str(exc)
                continue
            if not trial['unmeasured_refs'] and trial['estimated_tokens'] <= budget['reading_tokens']:
                reads.append(oid)
                assigned.add(oid)
                payload, refs, reading = trial_payload, trial_refs, trial
    for item in comparisons:
        item['status'] = 'in-packet' if item['peer_id'] in assigned else 'follow-up'
        if item['status'] == 'in-packet':
            item.pop('stage')
    return reads, payload, refs, reading, oversized, comparisons, issues


def draft_map_tasks(root, output='map/planned-tasks.json', registry=REGISTRY,
                    stage='3A', object_ids=None, task_prefix='map',
                    context_options=None, max_objects=None, scope=None, comparison=None, *,
                    queue_rows=None, required_reads=None):
    """Draft bounded reading comparisons; never infer or accept a relation.

    One complete registered object is a unit. The first layer drafts local
    groups. Later layers carry one explicitly chosen mathematical comparison.
    """
    import posixpath
    from urllib.parse import unquote, urlsplit
    import registration

    root = Path(root).resolve()
    if stage not in {'3A', '3B', '3C'}:
        raise ValueError('Draft mathematical comparisons for 3A/3B/3C; 3D is shared integration')
    identity(task_prefix)
    data, objects = load(root, registry, verify=False)
    deepest = {oid: max(object_scopes({oid: obj}), key=len, default='.')
               for oid, obj in objects.items()}
    archive = {oid: '/'.join(local.split('/')[:2]) for oid, local in deepest.items()}
    selected = list(dict.fromkeys(object_ids if object_ids is not None else sorted(objects)))
    if not selected or set(selected) - objects.keys():
        raise ValueError('Select actual registered mathematical objects before drafting map batches')
    if max_objects is not None and (type(max_objects) is not int or max_objects < 1):
        raise ValueError('Optional maximum core-object count must be positive')
    if scope is not None:
        if stage != '3A' or not re.fullmatch(r'archives/[^/]+(?:/subarchives/[^/]+)*', scope):
            raise ValueError('3A --scope takes an archive or subarchive path')
        selected = [oid for oid in selected if deepest[oid] == scope or deepest[oid].startswith(scope + '/')]
        if not selected:
            raise ValueError('No selected objects in this archive or subarchive: ' + scope)
    if stage != '3A':
        if object_ids is None or len(selected) < 2 or not isinstance(comparison, str) or not comparison.strip():
            raise ValueError('3B/3C require the exact endpoint IDs and a concrete --comparison question')
        origins = {archive[oid] for oid in selected}
        if '.' in origins or (stage == '3B' and len(origins) != 1) or (stage == '3C' and len(origins) < 2):
            raise ValueError('3B compares objects within one archive; 3C compares objects across archives')
        if max_objects is not None and len(selected) > max_objects:
            raise ValueError('This question exceeds --max-objects; choose a smaller complete comparison or use staged reading')
        comparison = comparison.strip()
        selected.sort(key=lambda oid: (deepest[oid], oid))
    elif comparison is not None:
        raise ValueError('Use --comparison for the explicitly selected 3B/3C frontier')
    budget = registration.context_budget(**(context_options or {}))
    required_reads = required_reads or {}
    measure_text = lambda text: registration.text_cost(text, budget['model'])
    queue_snapshot = {'source': 'not-a-published-queue-snapshot', 'skipped_current_core_objects': 0}
    if stage == '3A':
        if queue_rows is None:
            rows, queue_snapshot = _map_queue_snapshot(root)
        else:
            rows, queue_snapshot = queue_rows, {'source': 'compaction-pinned-queue'}
        rows = [row for row in rows if row['definition'].get('registry') == registry]
        done = _effective_map_done(rows)
        active = [row['definition'] for row in rows if row['state'] not in {'done', 'withdrawn'}]
        active_targets = {task_id for definition in active for task_id in definition.get('supersedes', [])}
        current_pins = {oid: pin(obj) for oid, obj in objects.items()}
        repairs = {task_id: reasons for task_id, row in done.items()
                   if (reasons := _map_repair_reasons(row, current_pins))}
        reserved = {oid for definition in active if definition['stage'] == '3A'
                    for oid in definition['object_ids']}
        reserved.update(oid for row in done.values() if row['definition']['stage'] == '3A'
                        for oid in row['definition']['object_ids'])
        skipped = len(reserved.intersection(selected))
        selected = [oid for oid in selected if oid not in reserved]
        queue_snapshot.update(skipped_current_core_objects=skipped,
                              repair_task_ids=sorted(repairs.keys() - active_targets),
                              repair_in_progress_task_ids=sorted(repairs.keys() & active_targets),
                              stale_active_task_ids=sorted(d['task_id'] for d in active
                                                           if not _map_inputs_current(d, current_pins)),
                              note='Published cores are reserved. Use --repair-task for changed inputs or '
                                   'unresolved done coverage. Hand off and reframe stale active work.')
    if not selected:
        _write_json(_safe_path(root, output), [])
        return {'status': 'map-repairs-needed' if queue_snapshot.get('repair_task_ids') else 'no-new-map-tasks',
                'path': output, 'tasks': 0, 'core_objects': 0,
                'queue_snapshot': queue_snapshot,
                'instruction': 'Resume the published queue, draft --repair-task for listed IDs, or finish '
                               'integration; do not map plan an empty task array.'}
    cache, units, neighbors, candidates_for = {}, {}, {}, {}
    body_owners, exact_owners = {}, {}

    def exact_ref(ref):
        return ref['path'], ref['sha256'], ref.get('section')

    for oid, obj in objects.items():
        body_owners.setdefault(obj['body']['path'], []).append(oid)
        exact_owners.setdefault(exact_ref(obj['body']), []).append(oid)

    def text_reference(ref):
        key = (ref['path'], ref['sha256'])
        if key not in texts:
            # Only a declared exact section is inspected for reading links;
            # another Claim elsewhere on the same page is not silently used.
            texts[key] = registration._context_text(reference(root, ref), ref_bytes(root, ref))
        return section(texts[key], ref.get('section')) if texts[key] is not None else ''

    def reading_links(oid):
        obj = objects[oid]
        exact, hints = set(), set()
        for ref in obj['evidence']:
            exact.update(exact_owners.get(exact_ref(ref), ()))
            hints.update(body_owners.get(ref['path'], ()))
        text = text_reference(obj['body'])
        for raw in re.findall(r'\]\(\s*(?:<([^>]+)>|([^\s)]+))', text):
            target = unquote(raw[0] or raw[1])
            split = urlsplit(target)
            if split.scheme or split.netloc or (not split.path and not split.fragment):
                continue
            name = (posixpath.normpath(posixpath.join(posixpath.dirname(obj['body']['path']), split.path))
                    if split.path else obj['body']['path'])
            if name.startswith('../') or name.startswith('/'):
                continue
            hints.update(body_owners.get(name, ()))
        return exact - {oid}, hints - {oid}

    def continued_reading(refs, reading):
        """Exact, ordered reading windows; the original mathematical refs stay intact."""
        allowance = budget['reading_tokens'] - reading['metadata_tokens'] - reading['task_overhead_tokens']
        if allowance < 5:
            raise ValueError('The object metadata leaves no reading window; narrow the complete comparison or increase the real context budget')
        spans, originals, guide = {}, {}, []
        for ref in refs:
            key = (ref['path'], ref['sha256'])
            originals.setdefault(key, []).append(ref.get('section'))
            text = text_reference(ref)
            full = texts[key]
            if full is None:
                guide.append({'source': {'path': key[0], 'sha256': key[1]},
                              'requires_readable_export': True,
                              'continuation': 'Read/export this evidence with its appropriate tool; keep the owning object and its obligations.'})
                continue
            if 'section' in ref:
                start = next(position for title, _, position in heading_sections(full) if title == ref['section'])
                interval = (start, start + len(text))
            else:
                interval = (0, len(full))
            spans.setdefault(key, []).append(interval)
        for key, intervals in spans.items():
            full = texts[key]
            for start, end in registration._merged_intervals(intervals):
                cursor = start
                width = 2 * allowance
                while cursor < end:
                    # Size the next pass from observed density rather than
                    # repeatedly measuring the full unread suffix.
                    stop = min(end, cursor + width)
                    cost = measure_text(full[cursor:stop])
                    while cost['estimated_tokens'] > allowance and stop > cursor + 1:
                        width = max(1, (stop - cursor) * allowance * 9 // (cost['estimated_tokens'] * 10))
                        stop = cursor + width
                        cost = measure_text(full[cursor:stop])
                    width = max(1, (stop - cursor) * allowance // max(1, cost['estimated_tokens']))
                    if stop < end:
                        # Prefer complete paragraphs/lines. A very long line
                        # still has exact consecutive character windows.
                        boundary = full.rfind('\n\n', cursor, stop)
                        if boundary > cursor:
                            boundary += 2
                        else:
                            boundary = full.rfind('\n', cursor, stop)
                            if boundary > cursor:
                                boundary += 1
                        if cursor < boundary < stop:
                            boundary_cost = measure_text(full[cursor:boundary])
                            if boundary_cost['estimated_tokens'] <= allowance:
                                stop, cost = boundary, boundary_cost
                    guide.append({'source': {'path': key[0], 'sha256': key[1]},
                                  'declared_sections': list(dict.fromkeys(originals[key])),
                                  'start_char': cursor, 'end_char_exclusive': stop,
                                  'start_line': full.count('\n', 0, cursor) + 1,
                                  'end_line': full.count('\n', 0, max(cursor, stop - 1)) + 1,
                                  'estimated_tokens': cost['estimated_tokens'],
                                  'token_count_is_estimate': cost['token_count_is_estimate'],
                                  'continuation': 'Continue this same complete object in order; retain its model, quantifiers, hypotheses, established steps and unpaid obligations in the saved note. No partial pass means done.'})
                    cursor = stop
        for index, item in enumerate(guide, 1):
            item['pass'] = index
        return guide

    texts = {}
    model = {oid: ' '.join(obj['model'].split()).casefold() for oid, obj in objects.items()}
    unspecified = {oid for oid, label in model.items()
                   if re.search(r'沿用该正文|exact.*(?:cited|frozen) body|exact.*in the.*body', label)}
    definitions = {oid for oid, obj in objects.items()
                   if obj['kind'].casefold() in {'definition', 'model', '定义', '模型'}}
    overlaps = map_overlap_candidates(objects, deepest) if stage == '3A' else {}
    for oid in selected:
        obj = objects[oid]
        refs = [obj['body'], *obj['evidence']]
        shared_refs = [ref for peer in required_reads.get(oid, ()) for ref in
                       [objects[peer]['body'], *objects[peer]['evidence']]]
        units[oid] = {'key': oid, 'refs': [*refs, *shared_refs], 'metadata': obj,
                      'estimated_output_tokens': max(1200, measure_text(
                          json.dumps(obj, ensure_ascii=False))['estimated_tokens'] + 400)}
        exact, hints = reading_links(oid) if stage == '3A' else (set(), set())
        neighbors[oid] = {peer for peer in exact if deepest[peer] == deepest[oid]
                          and (model[peer] == model[oid] or peer in definitions)}
        candidates_for[oid] = exact | hints

    # Informal source links are discovery hints. They do not join comparison
    # families, select endpoints, or turn common definitions into hubs.
    parent = {oid: oid for oid in selected}
    def find(oid):
        while parent[oid] != oid:
            parent[oid] = parent[parent[oid]]
            oid = parent[oid]
        return oid
    def union(left, right):
        a, b = find(left), find(right)
        if a != b:
            parent[max(a, b)] = min(a, b)

    pages, models = {}, {}
    selected_set = set(selected)
    families = {}
    packs = []
    if stage == '3A':
        for oid in selected:
            obj = objects[oid]
            if oid in definitions:
                continue
            source = exact_ref(obj['body']) if oid in unspecified else obj['body']['path']
            page_key = (deepest[oid], model[oid], source)
            union(oid, pages.setdefault(page_key, oid))
            # A repeated placeholder such as "see the cited body" never
            # supplies the model for two distinct proof files.
            if oid not in unspecified:
                model_key = (deepest[oid], model[oid], ' '.join(obj['scope'].split()),
                             posixpath.dirname(obj['body']['path']))
                union(oid, models.setdefault(model_key, oid))
                for other in neighbors[oid].intersection(selected_set).difference(definitions):
                    union(oid, other)
        for oid in selected:
            families.setdefault((deepest[oid], find(oid)), []).append(oid)
    else:
        # Splitting an explicit comparison into arbitrary cross-archive pairs
        # changes its question. Keep all endpoints and use staged reading if large.
        members = [units[oid] for oid in selected]
        output_tokens = sum(item['estimated_output_tokens'] for item in members)
        comparison_scope = archive[selected[0]] if stage == '3B' else '.'
        packs.append((comparison_scope, selected[0], {'units': members,
                                                      'estimated_output_tokens': output_tokens}))
    for (scope, family), ids in sorted(families.items()):
        # Within a family, keep direct source neighbors close without forming
        # a transitive all-pairs comparison obligation.
        pending = set(ids)
        order, frontier = [], deque()
        while pending:
            if not frontier:
                frontier.append(min(pending, key=lambda i: (-len(neighbors[i] & pending),
                                                           objects[i]['body']['path'], i)))
            oid = frontier.popleft()
            if oid not in pending:
                continue
            pending.remove(oid); order.append(units[oid])
            frontier.extend(sorted(neighbors[oid] & pending,
                                   key=lambda i: (objects[i]['body']['path'], i)))
        result = registration.pack_units(root, order, budget,
                                         max_items=max_objects or len(order), cache=cache)
        packs.extend((scope, family, pack) for pack in result['packs'])

    def comparison_priority(group):
        if len(group) < 2:
            return 2
        if (any(neighbors[oid].intersection(group) for oid in group)
                or len({objects[oid]['body']['path'] for oid in group}) < len(group)):
            return 0
        return 1

    if stage == '3A' and max_objects != 1:
        # Let one claim carry several small comparisons in the same scope.
        # Each family remains an independent comparison group within the task.
        small = {}
        separate = []
        for scope, family, pack in packs:
            members = pack['units']
            reading_tokens = pack['reading']['estimated_tokens']
            output_tokens = pack['estimated_output_tokens']
            if (pack['oversized'] or pack['requires_export'] or
                    (len(members) > 1 and (reading_tokens > budget['reading_tokens'] // 3
                                           or output_tokens > budget['output_tokens'] // 3))):
                separate.append((scope, family, pack))
                continue
            small.setdefault(scope, []).append({
                'key': members[0]['key'], 'family': family, 'members': members,
                'refs': [ref for item in members for ref in item['refs']],
                'metadata': [item['metadata'] for item in members],
                'estimated_output_tokens': output_tokens,
                'reading_tokens': reading_tokens,
                'priority': comparison_priority([item['key'] for item in members]),
            })
        # pack_units accounts for one task entry per group here. Leave room
        # for the additional per-object entries in the expanded task.
        object_overhead = 32 * (budget['output_tokens'] // 1200)
        group_budget = {**budget, 'reading_tokens': max(1, budget['reading_tokens'] - object_overhead)}
        for scope, groups in small.items():
            # Give a longer standalone object a chance to share a claim with
            # a short group before moving on to the next long object.
            pending = deque(sorted(groups, key=lambda group: (-group['reading_tokens'],
                                                               objects[group['key']]['body']['path'], group['key'])))
            order = []
            while pending:
                order.append(pending.popleft())
                if pending:
                    order.append(pending.pop())
            windows = [[]]
            core_count = 0
            for group in order:
                size = len(group['members'])
                if max_objects is not None and core_count + size > max_objects:
                    windows.append([])
                    core_count = 0
                windows[-1].append(group)
                core_count += size
            for window in windows:
                result = registration.pack_units(root, window, group_budget, max_items=len(window), cache=cache)
                for pack in result['packs']:
                    packed_groups = sorted(pack['units'], key=lambda group: group['priority'])
                    pack['comparison_groups'] = [[item['key'] for item in group['members']] for group in packed_groups]
                    pack['units'] = [item for group in packed_groups for item in group['members']]
                    separate.append((scope, packed_groups[0]['family'], pack))
        packs = sorted(separate, key=lambda item: (item[0], item[2]['units'][0]['key']))

    tasks, oversize, reading_totals = [], [], {'chars': 0, 'utf8_bytes': 0, 'estimated_tokens': 0}
    for scope, family, packed in packs:
        core = [unit['key'] for unit in packed['units']]
        groups = packed.get('comparison_groups', [core])
        reads = sorted({peer for oid in core for peer in required_reads.get(oid, ())} - set(core))
        common_context = sorted(set().union(*(neighbors[oid] for oid in core)) & definitions)
        reads, payload, mandatory_refs, reading, oversized, boundary, deferred_issues = plan_map_overlap(
            root, objects, core, reads, groups, budget, packed['estimated_output_tokens'],
            overlaps, contextual=common_context, cache=cache, deepest=deepest)
        deferred = set().union(*(candidates_for[oid] for oid in core)) - set(core)
        all_ids = [*core, *reads]
        pins = {oid: pin(objects[oid]) for oid in all_ids}
        task_key = {'stage': stage, 'core': core, 'inputs': pins}
        if comparison:
            task_key['comparison'] = comparison
        task_id = task_prefix + '-' + stage.lower() + '-' + pin(task_key)[:16]
        unique_refs = {json.dumps(ref, sort_keys=True): ref for ref in mandatory_refs}
        priority = (0 if any(item['status'] == 'in-packet' for item in boundary)
                    else min(map(comparison_priority, groups)))
        context_plan = {'budget': budget, 'reading': reading,
                        'estimated_output_tokens': packed['estimated_output_tokens'],
                        'oversized': oversized,
                        'requires_export': bool(reading['unmeasured_refs']),
                        'reading_refs': list(unique_refs.values()),
                        'deferred_candidate_ids': sorted(deferred.difference(reads)),
                        'deferred_candidate_issues': deferred_issues,
                        'comparison_priority': priority,
                        'family_hint': family, 'scope_hint': scope,
                        'status': 'complete-declared-references-planned',
                        'note': 'Local proof families are scheduled first. Informal links are separate discovery hints. '
                                'Read any newly discovered necessary premise through read-add; '
                                'do not truncate a proof or treat a deferred candidate as paid evidence.'}
        if comparison:
            context_plan['comparison_question'] = comparison
            context_plan['note'] = 'Compare the stated mathematical question on all selected endpoints; if large, resume the same question in reading passes.'
        if len(groups) > 1:
            context_plan['comparison_groups'] = groups
            context_plan['note'] += ' Compare each group separately unless there is a concrete mathematical connection across groups.'
        if boundary:
            context_plan['overlap_comparisons'] = boundary
            context_plan['note'] += ' The core owns its exact overlap comparison. Inspect the cited dependency; carry a confirmed unfinished comparison forward as a named task.'
        if oversized:
            oversize.append(task_id)
            context_plan['status'] = 'complete-object-requires-staged-reading'
            context_plan['note'] += ' Preserve this complete object/comparison frontier; read its exact declared sections in successive turns, '
            context_plan['note'] += 'saving the hypotheses, established steps and remaining obligations between turns.'
            context_plan['reading_passes'] = continued_reading(mandatory_refs, reading)
        if reading['unmeasured_refs']:
            context_plan['status'] = 'complete-object-requires-readable-evidence'
            context_plan['note'] += ' Read/export the actual non-text evidence with its appropriate tool; '
            context_plan['note'] += 'raw binary bytes are not a measured token budget.'
        tasks.append({'task_id': task_id, 'stage': stage, 'registry': registry,
                      'object_ids': core, 'read_object_ids': reads,
                      'input_pins': pins,
                      'write_paths': ['map/edges/' + task_id, 'map/receipts/' + task_id + '.json'],
                      'goal': comparison or ('Read and compare the complete assigned mathematical objects in ' + scope +
                              '; preserve model, quantifiers, hypotheses, exact refutation targets and open obligations. '
                              'Create only explained useful relations; shared definitions do not imply hub edges.'),
                      'context_plan': context_plan})
        for key in reading_totals:
            reading_totals[key] += reading[key]
    destination = _safe_path(root, output)
    tasks.sort(key=lambda task: (task['context_plan']['comparison_priority'],
                                 task['context_plan']['scope_hint'],
                                 objects[task['object_ids'][0]]['body']['path']))
    _write_json(destination, tasks)
    return {'status': 'map-tasks-draft-local-not-pushed', 'path': output,
            'tasks': len(tasks), 'core_objects': len(selected),
            'queue_snapshot': queue_snapshot,
            'core_counts': [len(task['object_ids']) for task in tasks],
            'reading_files_per_task': [len({ref['path'] for ref in task['context_plan']['reading_refs']}) for task in tasks],
            'reading_totals': reading_totals, 'oversized_tasks': oversize,
            'instruction': 'Review the actual mathematical families, then map plan this task array. '
                           'A task is a batch, not a file or an automatic edge. '
                           '3B/3C require the actual comparison frontier; any Boss can integrate in 3D.'}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--registry', default=REGISTRY)
    sub = p.add_subparsers(dest='command', required=True)
    def reading_options(parser):
        parser.add_argument('--model', default='gpt-6.1-sol')
        parser.add_argument('--context-tokens', type=int)
        parser.add_argument('--context-source', choices=['official-default', 'platform-reported', 'user-specified'])
        parser.add_argument('--used-tokens', type=int)
        parser.add_argument('--reserve-tokens', type=int)
        parser.add_argument('--output-tokens', type=int)
        parser.add_argument('--context-mode', choices=['fresh', 'inherited'], default='fresh')

    def reading_plan(args):
        return {'model': args.model,
                'context_tokens': args.context_tokens if args.context_tokens is not None else 500000,
                'window_source': args.context_source or ('user-specified' if args.context_tokens is not None else 'official-default'),
                'used_tokens': args.used_tokens, 'reserve_tokens': args.reserve_tokens,
                'output_tokens': args.output_tokens, 'inherited': args.context_mode == 'inherited'}

    sub.add_parser('inventory')
    q = sub.add_parser('inputs'); q.add_argument('--out', default='research/registration/inputs.json')
    q.add_argument('--scope', choices=['repository','partial'], default='repository')
    q.add_argument('--coverage-note', required=True); q.add_argument('--paths-file')
    q = sub.add_parser('prepare-inputs', help='Freeze a byte inventory for 2.5.3; no mathematical admission')
    q.add_argument('--output', default='research/registration/inputs.json')
    q.add_argument('--scope', choices=['repository', 'partial'], default='repository')
    q.add_argument('--coverage-note', required=True)
    q.add_argument('--path', action='append', default=[])
    q = sub.add_parser('freeze'); q.add_argument('--inputs-file', required=True); q.add_argument('--out', default='research/registration/baseline.json')
    q = sub.add_parser('compose'); q.add_argument('--manifest', required=True); q.add_argument('--out', default='research/registration/proposed.json')
    q = sub.add_parser('batches-draft', help='Draft whole registration batches from real frozen materials and a reading budget')
    q.add_argument('--baseline', default='research/registration/baseline.json')
    q.add_argument('--output', default='research/registration/tasks.json')
    q.add_argument('--max-materials', type=int, default=200)
    q.add_argument('--task-prefix', default='register')
    q.add_argument('--include-registered', action='store_true')
    reading_options(q)
    q = sub.add_parser('map-draft', help='Draft related complete-object comparisons within a declared context budget')
    q.add_argument('--output', default='map/planned-tasks.json')
    q.add_argument('--stage', choices=['3A', '3B', '3C'], default='3A')
    q.add_argument('--object-id', action='append')
    q.add_argument('--objects-file')
    q.add_argument('--scope', help='3A: start in this archive or subarchive, such as archives/facility-games/subarchives/common-two')
    q.add_argument('--comparison', help='3B/3C: concrete mathematical question on the selected endpoints')
    q.add_argument('--repair-task', action='append', help='Refresh unfinished or replace completed work on current inputs')
    q.add_argument('--task-prefix', default='map')
    q.add_argument('--max-objects', type=int)
    reading_options(q)
    q = sub.add_parser('registration-check'); q.add_argument('--final', action='store_true')
    q = sub.add_parser('assignments-draft', help='Optional scheduling draft; review it before publishing actual CAS tasks')
    q.add_argument('--baseline', default='research/registration/baseline.json')
    q.add_argument('--owners', required=True)
    q.add_argument('--output', default='research/registration/assignments.draft.json')
    q.add_argument('--batch-size', type=int, default=80)
    q = sub.add_parser('assignments-check'); q.add_argument('--assignment-file', default='research/registration/assignments.json')
    q = sub.add_parser('new-id'); q.add_argument('--count', type=int, default=1)
    q = sub.add_parser('register'); q.add_argument('--record-file', required=True)
    for command in ('check', 'build'):
        q = sub.add_parser(command); q.add_argument('--final', action='store_true')
    q = sub.add_parser('search'); q.add_argument('query'); q.add_argument('--limit', type=int, default=20)
    q.add_argument('--model'); q.add_argument('--truth-status', action='append', choices=sorted(TRUTHS)); q.add_argument('--kind', action='append')
    q = sub.add_parser('show'); q.add_argument('object_id'); q.add_argument('--body', action='store_true')
    q = sub.add_parser('context'); q.add_argument('ids', nargs='+'); q.add_argument('--hops', type=int, default=0)
    q.add_argument('--edge', action='append'); q.add_argument('--edge-status', action='append', choices=['accepted','proposed','rejected'])
    q.add_argument('--relation-kind', action='append', choices=sorted(LOGICAL|CONTEXT))
    q = sub.add_parser('edge-bind'); q.add_argument('edge_file'); q.add_argument('--write', action='store_true')
    q = sub.add_parser('edge-check'); q.add_argument('edge_file')
    q = sub.add_parser('packet'); q.add_argument('spec'); q.add_argument('--profile', choices=['obstacle', 'full'], required=True)
    q = sub.add_parser('init'); q.add_argument('run_id'); q.add_argument('--spec', required=True)
    q.add_argument('--mode', choices=['comparison', 'open'], default='comparison')
    q = sub.add_parser('resume'); q.add_argument('run_id')
    q = sub.add_parser('peers', help='Find same-input runs and their shared research workspace in this snapshot')
    q.add_argument('run_id')
    q = sub.add_parser('compute', help='Run one registered experiment and checkpoint its receipt immediately')
    q.add_argument('experiment'); q.add_argument('--out', required=True)
    q.add_argument('--manifest', default='research/experiments.json'); q.add_argument('--resume-from')
    q.add_argument('--message'); q.add_argument('--local-only', action='store_true')
    q = sub.add_parser('save'); q.add_argument('run_id'); q.add_argument('--solver', required=True)
    q.add_argument('--profile', choices=['obstacle', 'full'], required=True); q.add_argument('--note', required=True)
    q.add_argument('--next', required=True); q.add_argument('--state', choices=sorted(STATES), default='working')
    feedback_group = q.add_mutually_exclusive_group()
    feedback_group.add_argument('--feedback'); feedback_group.add_argument('--ack-feedback', action='store_true')
    q.add_argument('--agent-id')
    q.add_argument('--model'); q.add_argument('--reasoning-effort')
    q.add_argument('--fork-turns', choices=['none', 'all'])
    a = p.parse_args(argv); root = a.repo.resolve()
    if a.command == 'inventory': result = inventory(root, a.registry)
    elif a.command == 'inputs':
        import registration
        result = registration.prepare_inputs(root,a.out,a.scope,a.coverage_note,a.paths_file)
    elif a.command == 'prepare-inputs': result = prepare_inputs(root, a.output, a.scope, a.coverage_note, a.path)
    elif a.command == 'batches-draft':
        import registration
        result = registration.draft_registration_tasks(root, a.baseline, a.output,
            max_materials=a.max_materials, task_prefix=a.task_prefix,
            context_options=reading_plan(a), include_registered=a.include_registered)
    elif a.command == 'map-draft':
        ids = a.object_id
        comparison = a.comparison
        if a.objects_file:
            selected = json.loads(_safe_path(root, a.objects_file).read_text())
            if isinstance(selected, dict):
                saved_comparison = selected.get('comparison')
                if comparison is not None and saved_comparison is not None and comparison != saved_comparison:
                    raise ValueError('Give the same comparison in the file and command, or use only one')
                comparison = comparison if comparison is not None else saved_comparison
                selected = selected.get('object_ids')
            strings(selected, 'selected object IDs', True)
            ids = list(dict.fromkeys([*(ids or []), *selected]))
        if a.repair_task:
            if ids or a.max_objects is not None or a.scope is not None or comparison is not None:
                raise ValueError('Repair uses the complete surviving scope of the named task; omit object selection and limits')
            result = draft_map_repairs(root, a.repair_task, a.output, a.registry, a.task_prefix,
                                       context_options=reading_plan(a))
        else:
            result = draft_map_tasks(root, output=a.output, registry=a.registry,
                stage=a.stage, object_ids=ids, task_prefix=a.task_prefix,
                context_options=reading_plan(a), max_objects=a.max_objects,
                scope=a.scope, comparison=comparison)
    elif a.command in {'freeze', 'compose', 'registration-check', 'assignments-draft', 'assignments-check', 'new-id'}:
        import registration
        if a.command == 'freeze': result = registration.freeze(root, a.inputs_file, a.out)
        elif a.command == 'compose': result = registration.compose(root, a.manifest, a.out)
        elif a.command == 'registration-check': result = registration.check(root, a.registry, a.final)
        elif a.command == 'assignments-draft':
            result = registration.draft_assignments(root, a.baseline, [x.strip() for x in a.owners.split(',') if x.strip()], a.output, a.batch_size)
        elif a.command == 'assignments-check': result = registration.check_assignments(root, a.assignment_file)
        else: result = registration.new_ids(a.count)
    elif a.command == 'register': result = register(root, a.record_file, a.registry)
    elif a.command in {'check', 'build'}: result = globals()[a.command](root, a.registry, a.final)
    elif a.command == 'search':
        if a.limit < 1: raise ValueError('Positive display limit required')
        result = search(root,a.query,a.registry,a.limit,model=a.model,truth_statuses=a.truth_status,kinds=a.kind)
    elif a.command == 'show':
        _, objs = load(root,a.registry,verify=False)
        result = object_view(root,objs[a.object_id],body=a.body)
    elif a.command == 'context':
        result = context(root,a.ids,a.registry,a.hops,edge_ids=a.edge,edge_statuses=a.edge_status,relation_kinds=a.relation_kind)
    elif a.command == 'edge-bind':
        _, objs = load(root,a.registry,verify=False)
        path = _safe_path(root,a.edge_file)
        edge = json.loads(path.read_text())
        verify_endpoints(root,edge,objs)
        result = edge_bindings(root,edge,objs)
        if a.write:
            edge.update(result)
            _write_json(path, edge)
    elif a.command == 'edge-check': result = check_edge(root, a.edge_file, a.registry)
    elif a.command == 'packet': result = packet(root, json.loads(_safe_path(root, a.spec).read_text()), a.profile, a.registry)
    elif a.command == 'init': result = init_run(root, a.run_id, a.spec, a.registry, mode=a.mode)
    elif a.command == 'resume': result = resume(root, a.run_id)
    elif a.command == 'peers': result = peers(root, a.run_id)
    elif a.command == 'compute':
        import codespace_math
        result = codespace_math.run(root, a.experiment, a.out, a.message, a.local_only, a.manifest, a.resume_from)
    else: result = update_run(root, a.run_id, a.solver, a.profile, a.note, a.next, a.state, a.feedback, a.agent_id, a.ack_feedback,
                             a.model, a.reasoning_effort, a.fork_turns)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError) as exc:
        raise SystemExit(str(exc))
