"""Explicit mathematical registration and small, recoverable Work contexts.

No model SDK or external service is required. Records are declarations by their
authors; structural checks and version pins never certify mathematical truth.
"""
from __future__ import annotations

import argparse
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

# Every new mathematical run gets the same three platform launch slots.  The
# role split preserves the useful blind-vs-informed comparison while making the
# model/effort choice explicit and machine-readable for Work orchestration.
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
        oid = identity(obj.get('object_id'))
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
    seen = set()
    for row in data['materials']:
        (ref_bytes if verify else reference)(root, {k: row[k] for k in ('path', 'sha256')})
        if row['path'] in seen:
            raise ValueError('Duplicate material disposition')
        seen.add(row['path'])
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
            refs = [obj['body']] if row['disposition'] == 'objects' else obj['evidence']
            if row['disposition'] in {'objects', 'attachment'} and row['path'] not in {r['path'] for r in refs}:
                raise ValueError('Material owner must reference these bytes')
    for obj in objects.values():
        if obj['body']['path'] not in seen:
            raise ValueError('Every registered body requires a material disposition')
    return data, objects


def register(root, record_file, registry=REGISTRY):
    """Publish an explicit reviewed registration locally, preserving identity."""
    data = json.loads(_safe_path(root, record_file).read_text())
    _, objects = load(root, registry, provided=data)
    edges(root, data, objects)
    destination = _safe_path(root, registry)
    if destination.exists():
        # Previous byte pins are expected to be stale when explicitly updating
        # a changed proof. Read identity/version metadata without re-admitting
        # those old bytes; validate the entire incoming declaration above.
        previous = json.loads(destination.read_text())
        old = {identity(obj['object_id']): obj for obj in previous['objects']}
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
            'review_digest': edge_digest(edge),
            'note': 'Mechanical bindings only; no review or acceptance is performed'}


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
        if edge['status'] == 'accepted':
            nonempty(edge, ['reviewed_by', 'review_note'])
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


def check_edge(root, edge_file, registry=REGISTRY, verify=True):
    """Validate one proposed/accepted edge before it enters the canonical registry.

    Stage-3 workers intentionally do not edit ``registry.json``.  This command
    gives ``map done`` a real semantic gate for the edge it is delivering,
    instead of relying on the registry's current ``edge_files`` list.
    """
    data, objects = load(root, registry, verify=verify)
    name = _safe_path(root, edge_file).relative_to(root).as_posix()
    relations = edges(root, dict(data, edge_files=[name]), objects, verify=verify)
    edge = relations[next(iter(relations))]
    return {'status': 'edge-structure-valid-not-a-mathematical-verdict',
            'edge_file': name, 'edge_id': edge['edge_id'],
            'edge_status': edge['status'], 'registry': registry,
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
        integration_check(root, data, objects, relations)
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
                if not e or e['status'] != 'accepted' or oid not in e['source_ids'] + e['target_ids']:
                    raise ValueError('Linked coverage must name a real accepted incident edge')


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


def search(root, query, registry=REGISTRY, limit=20):
    _, objects = load(root, registry, verify=False)
    terms = query.casefold().split()
    ranked = []
    for oid, obj in objects.items():
        text = json.dumps({k: obj[k] for k in ('title', 'statement', 'model', 'keywords') if k in obj}, ensure_ascii=False).casefold()
        score = sum(text.count(term) for term in terms)
        if score:
            ranked.append((score, oid, obj))
    return [{'object_id': oid, 'version': obj['version'], 'title': obj['title'], 'truth_status': obj['truth_status'], 'path': obj['body']['path'], 'binding_status': 'unchecked-until-open'}
            for _, oid, obj in sorted(ranked, key=lambda row: (-row[0], row[1]))[:limit]]


def context(root, ids, registry=REGISTRY, hops=2):
    if not 0 <= hops <= 10:
        raise ValueError('Use an explicit hop window from 0 to 10; larger reading may be requested separately')
    data, objects = load(root, registry, verify=False)
    relations = edges(root, data, objects, verify=False)
    if not ids or any(i not in objects for i in ids):
        raise ValueError('Known seed object IDs required')
    reached, picked = set(ids), {}
    for _ in range(hops):
        previous = set(reached)
        for eid, edge in relations.items():
            endpoints = set(edge['source_ids'] + edge['target_ids'])
            if edge['status'] == 'accepted' and endpoints.intersection(previous):
                picked[eid] = edge
                reached.update(endpoints)
    for oid in reached:
        ref_bytes(root, objects[oid]['body'])
        for ref in objects[oid]['evidence']: ref_bytes(root, ref)
    for edge in picked.values():
        for ref in edge['evidence']: ref_bytes(root, ref)
    return {'seed_ids': ids, 'hops': hops, 'navigation_only': True,
            'objects': [objects[i] for i in sorted(reached)], 'edges': list(picked.values()),
            'instruction': 'Read body and evidence on demand. All source_ids of a hyperedge are joint premises. Adjacency never proves a statement.'}


def packet(root, spec, profile, registry=REGISTRY):
    if profile not in {'obstacle', 'full'}:
        raise ValueError('Only obstacle and full solver profiles are used')
    identity(spec['problem_id'])
    target = read_ref(root, spec['problem'])
    definitions = [read_ref(root, ref) for ref in spec['definitions']]
    obstacles = [read_ref(root, ref) for ref in spec['obstacles']]
    result = {'problem_id': spec['problem_id'], 'profile': profile, 'target': target,
              'definitions': definitions, 'obstacles': obstacles,
              'task': 'Solve this exact problem freely. Use any useful mathematical method. Save substantive progress and explicit gaps.',
              'launch': {'fork_turns': 'none', 'model': 'gpt-6.1-sol', 'reasoning_effort': 'ultra',
                         'instruction': 'Start a fresh-history solver with the declared model and effort. Supply only this packet and the matching solver prompt.'},
              'limit': 'Context selection is not a file-system access-control boundary; unrestricted tools can read other files.'}
    if profile == 'full':
        result['context'] = context(root, spec['seed_ids'], registry, spec.get('hops', 2))
        result['retrieval'] = {'registry': registry, 'commands': ['research search', 'research show', 'research context']}
    return result


def run_path(root, run_id):
    return _safe_path(root, 'research/runs/' + identity(run_id) + '/run.json')


def init_run(root, run_id, spec_file, registry=REGISTRY):
    path = run_path(root, run_id)
    if path.exists():
        raise ValueError('Run exists; resume it instead')
    spec = json.loads(_safe_path(root, spec_file).read_text())
    packets = {p: packet(root, spec, p, registry) for p in ('obstacle', 'full')}
    home = path.parent
    for profile, value in packets.items():
        _write_json(home / ('packet-' + profile + '.json'), value)
    roster = copy.deepcopy(SOLVER_ROSTER)
    state = {'schema': 2, 'run_id': run_id, 'problem_id': spec['problem_id'], 'state': 'working',
             'spec': spec_file, 'spec_pin': pin(spec), 'registry': registry, 'solvers': {},
             'solver_count': len(roster), 'solver_roster': roster,
             'launch_plan': {'platform': 'Work', 'exact_count': len(roster),
                             'instruction': 'Launch every roster slot before solving; Main is not an extra Solver.'},
             'packet_pins': {profile: pin(value) for profile, value in packets.items()},
             'note': 'This command writes packets and a fixed launch plan; Work starts all three platform Solver agents.'}
    _write_json(path, state)
    return {'status': 'initialized-local-not-pushed', 'run': path.relative_to(root).as_posix(),
            'packets': [str((home / ('packet-' + p + '.json')).relative_to(root)) for p in packets],
            'solver_count': len(roster), 'solver_roster': roster, 'agents_launched': 0}


def update_run(root, run_id, solver_id, profile, note, next_action, state, feedback=None, agent_id=None):
    identity(solver_id)
    if profile not in {'obstacle', 'full'} or state not in STATES or not next_action.strip():
        raise ValueError('Explicit solver profile, state and concrete next action required')
    if feedback is not None and not feedback.strip():
        raise ValueError('Concrete feedback required')
    path = run_path(root, run_id)
    run = json.loads(path.read_text())
    old = run['solvers'].get(solver_id, {})
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
             'agent_id': agent_id or old.get('agent_id'), 'feedback': feedback}
    _write_json(_safe_path(root, (path.parent / 'events' / (event_id + '.json')).relative_to(root).as_posix()), event)
    run['solvers'][solver_id] = dict(event, latest_event=event_id)
    _write_json(path, run)
    return {'status': 'saved-local-not-pushed', 'event_id': event_id, 'continuation_of': event['continuation_of']}


def resume(root, run_id):
    path = run_path(root, run_id)
    run = json.loads(path.read_text())
    spec = json.loads(_safe_path(root, run['spec']).read_text())
    if pin(spec) != run['spec_pin']:
        raise ValueError('Problem spec changed; explicitly reframe instead of silently resuming another problem')
    for profile, expected in run['packet_pins'].items():
        saved = json.loads((path.parent / ('packet-' + profile + '.json')).read_text())
        if pin(saved) != expected:
            raise ValueError('Saved solver packet changed; do not silently alter the context')
    for solver in run['solvers'].values():
        ref_bytes(root, solver['note'])
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True)
    roster = run.get('solver_roster', SOLVER_ROSTER)
    return {'run': run, 'local_head': head.stdout.strip() if not head.returncode else None,
            'solver_count': run.get('solver_count', len(roster)), 'solver_roster': roster,
            'instruction': 'Continue each recorded Solver with its existing history. If unavailable, launch the same roster slot fresh with the same profile packet, note, events and pending feedback.',
            'publication': 'Local HEAD is not remote confirmation; checkpoint and verify status=pushed separately.'}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--registry', default=REGISTRY)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('inventory')
    q = sub.add_parser('freeze'); q.add_argument('--inputs-file', required=True); q.add_argument('--out', default='research/registration/baseline.json')
    q = sub.add_parser('compose'); q.add_argument('--manifest', required=True); q.add_argument('--out', default='research/registration/proposed.json')
    q = sub.add_parser('registration-check'); q.add_argument('--final', action='store_true')
    q = sub.add_parser('new-id'); q.add_argument('--count', type=int, default=1)
    q = sub.add_parser('register'); q.add_argument('--record-file', required=True)
    for command in ('check', 'build'):
        q = sub.add_parser(command); q.add_argument('--final', action='store_true')
    q = sub.add_parser('search'); q.add_argument('query'); q.add_argument('--limit', type=int, default=20)
    q = sub.add_parser('show'); q.add_argument('object_id'); q.add_argument('--body', action='store_true')
    q = sub.add_parser('context'); q.add_argument('ids', nargs='+'); q.add_argument('--hops', type=int, default=2)
    q = sub.add_parser('edge-bind'); q.add_argument('edge_file')
    q = sub.add_parser('edge-check'); q.add_argument('edge_file')
    q = sub.add_parser('packet'); q.add_argument('spec'); q.add_argument('--profile', choices=['obstacle', 'full'], required=True)
    q = sub.add_parser('init'); q.add_argument('run_id'); q.add_argument('--spec', required=True)
    q = sub.add_parser('resume'); q.add_argument('run_id')
    q = sub.add_parser('compute', help='Run one registered experiment and checkpoint its receipt immediately')
    q.add_argument('experiment'); q.add_argument('--out', required=True)
    q.add_argument('--message'); q.add_argument('--local-only', action='store_true')
    q = sub.add_parser('save'); q.add_argument('run_id'); q.add_argument('--solver', required=True)
    q.add_argument('--profile', choices=['obstacle', 'full'], required=True); q.add_argument('--note', required=True)
    q.add_argument('--next', required=True); q.add_argument('--state', choices=sorted(STATES), default='working')
    q.add_argument('--feedback'); q.add_argument('--agent-id')
    a = p.parse_args(argv); root = a.repo.resolve()
    if a.command == 'inventory': result = inventory(root, a.registry)
    elif a.command in {'freeze', 'compose', 'registration-check', 'new-id'}:
        import registration
        if a.command == 'freeze': result = registration.freeze(root, a.inputs_file, a.out)
        elif a.command == 'compose': result = registration.compose(root, a.manifest, a.out)
        elif a.command == 'registration-check': result = registration.check(root, a.registry, a.final)
        else: result = registration.new_ids(a.count)
    elif a.command == 'register': result = register(root, a.record_file, a.registry)
    elif a.command in {'check', 'build'}: result = globals()[a.command](root, a.registry, a.final)
    elif a.command == 'search':
        if a.limit < 1: raise ValueError('Positive display limit required')
        result = search(root, a.query, a.registry, a.limit)
    elif a.command == 'show':
        _, objs = load(root, a.registry, verify=False); result = copy.deepcopy(objs[a.object_id])
        ref_bytes(root, result['body'])
        for ref in result['evidence']: ref_bytes(root, ref)
        if a.body: result['body_text'] = read_ref(root, result['body'])
    elif a.command == 'context': result = context(root, a.ids, a.registry, a.hops)
    elif a.command == 'edge-bind':
        _, objs = load(root, a.registry); result = edge_bindings(root, json.loads(_safe_path(root, a.edge_file).read_text()), objs)
    elif a.command == 'edge-check': result = check_edge(root, a.edge_file, a.registry)
    elif a.command == 'packet': result = packet(root, json.loads(_safe_path(root, a.spec).read_text()), a.profile, a.registry)
    elif a.command == 'init': result = init_run(root, a.run_id, a.spec, a.registry)
    elif a.command == 'resume': result = resume(root, a.run_id)
    elif a.command == 'compute':
        import codespace_math
        result = codespace_math.run(root, a.experiment, a.out, a.message, a.local_only)
    else: result = update_run(root, a.run_id, a.solver, a.profile, a.note, a.next, a.state, a.feedback, a.agent_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError) as exc:
        raise SystemExit(str(exc))
