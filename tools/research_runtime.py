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


def prepare_inputs(root, output, scope='repository', coverage_note=None, paths=None):
    """Keep the current prepare-inputs CLI while sharing its real Git denominator."""
    if not isinstance(coverage_note, str) or not coverage_note.strip():
        raise ValueError('A concrete coverage note is required')
    import registration
    return registration.prepare_inputs(root, output, scope, coverage_note.strip(), paths=paths)


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
        if edge.get('status') != 'accepted' or edge.get('kind') not in positive:
            continue
        for oid in edge['target_ids']:
            incoming.setdefault(oid,[]).append((eid,'forward'))
        if edge.get('kind') == 'equivalent_to':
            for oid in edge['source_ids']:
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
                'all_premises': list(premises), 'conclusion_ids': list(conclusions),
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
        return e.get('status') in statuses and (not relation_kinds or e.get('kind') in relation_kinds)
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
    picked = [ev(eid) for eid in sorted(related)]
    return {'seed_ids': ids, 'hops': hops, 'navigation_only': True, 'registry': registry, 'registry_pin': pin(data),
            'support_semantics': 'OR between support_options; ALL within each option. Conditions and unpaid premises remain explicit. This is not automated proof acceptance.',
            'proof_closure_object_ids': sorted(proof_objects), 'support_options': support,
            'objects': [ov(i) for i in sorted(required)], 'edges': picked,
            'refutations': [e for e in picked if e.get('kind') == 'refutes'],
            'research_leads': [e for e in picked if e['edge_id'] not in proof_edges and e.get('kind') != 'refutes'],
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
              'task': 'Solve this exact problem freely. Use any useful mathematical method. Save substantive progress and explicit gaps.',
              'launch': {'fork_turns': 'none', 'model': 'gpt-6.1-sol', 'reasoning_effort': 'ultra',
                         'instruction': 'Start a fresh-history solver with the declared model and effort unless the user explicitly requests inherited history. Supply this packet and the matching solver prompt.'},
              'limit': 'Context selection is not a file-system access-control boundary.'}
    if profile == 'full':
        result['context'] = context(root, spec['seed_ids'], registry, spec.get('hops', 0),
            edge_ids=spec.get('edge_ids'), edge_statuses=spec.get('edge_statuses'), relation_kinds=spec.get('relation_kinds'))
        result['registry_pin'] = result['context']['registry_pin']
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
                             'instruction': 'Main launches every roster slot through the actual platform; init itself launches no model.'},
             'registry_pin': packets['full'].get('registry_pin'),
             'context_snapshot': {
                 'objects': {o['object_id']: o['registration_pin'] for o in packets['full']['context']['objects']},
                 'edges': {e['edge_id']: e['declaration_pin'] for e in packets['full']['context']['edges']}},
             'packet_pins': {profile: pin(value) for profile, value in packets.items()},
             'note': 'No agents were launched by this command; Main starts them through the Work orchestration API.'}
    _write_json(path, state)
    return {'status': 'initialized-local-not-pushed', 'run': path.relative_to(root).as_posix(),
            'packets': [str((home / ('packet-' + p + '.json')).relative_to(root)) for p in packets],
            'solver_count': len(roster), 'solver_roster': roster, 'agents_launched': 0}


def update_run(root, run_id, solver_id, profile, note, next_action, state, feedback=None, agent_id=None, ack_feedback=False):
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
    if roster and (solver_id not in roster or roster[solver_id] != profile):
        raise ValueError('Use a declared Solver roster slot with its original profile')
    old = run['solvers'].get(solver_id, {})
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
    _write_json(_safe_path(root, (path.parent / 'events' / (event_id + '.json')).relative_to(root).as_posix()), event)
    run['solvers'][solver_id] = dict(event, latest_event=event_id)
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
        changes['registry_error'] = str(exc)
        warnings.append('Saved notes and packets remain recoverable; the current registry needs attention: '+str(exc))
    head = subprocess.run(['git','rev-parse','HEAD'],cwd=root,capture_output=True,text=True)
    roster = run.get('solver_roster', SOLVER_ROSTER)
    return {'run':run,'solver_count':run.get('solver_count',len(roster)),'solver_roster':roster,
            'packet_bindings':packet_bindings,'event_history':histories,
            'recent_feedback':{i:s.get('feedback') for i,s in run['solvers'].items() if s.get('feedback')},
            'pending_feedback':{i:s.get('feedback') for i,s in run['solvers'].items()
                                if s.get('feedback_pending', bool(s.get('feedback'))) and s.get('feedback')},
            'version_changes':changes,'recovery_warnings':warnings,
            'local_head':head.stdout.strip() if not head.returncode else None,
            'instruction':'Continue the recorded agent. If unavailable, restore the same input profile from its saved packet, latest readable immutable note, concrete feedback and event lineage. Version changes are targeted reading tasks, not a reason to discard existing mathematics or rescan the whole repository.',
            'publication':'Local HEAD is not remote confirmation; checkpoint and verify pushed separately.'}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--registry', default=REGISTRY)
    sub = p.add_subparsers(dest='command', required=True)
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
    q = sub.add_parser('edge-bind'); q.add_argument('edge_file')
    q = sub.add_parser('edge-check'); q.add_argument('edge_file')
    q = sub.add_parser('packet'); q.add_argument('spec'); q.add_argument('--profile', choices=['obstacle', 'full'], required=True)
    q = sub.add_parser('init'); q.add_argument('run_id'); q.add_argument('--spec', required=True)
    q = sub.add_parser('resume'); q.add_argument('run_id')
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
    a = p.parse_args(argv); root = a.repo.resolve()
    if a.command == 'inventory': result = inventory(root, a.registry)
    elif a.command == 'inputs':
        import registration
        result = registration.prepare_inputs(root,a.out,a.scope,a.coverage_note,a.paths_file)
    elif a.command == 'prepare-inputs': result = prepare_inputs(root, a.output, a.scope, a.coverage_note, a.path)
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
        edge = json.loads(_safe_path(root,a.edge_file).read_text())
        verify_endpoints(root,edge,objs)
        result = edge_bindings(root,edge,objs)
    elif a.command == 'edge-check': result = check_edge(root, a.edge_file, a.registry)
    elif a.command == 'packet': result = packet(root, json.loads(_safe_path(root, a.spec).read_text()), a.profile, a.registry)
    elif a.command == 'init': result = init_run(root, a.run_id, a.spec, a.registry)
    elif a.command == 'resume': result = resume(root, a.run_id)
    elif a.command == 'compute':
        import codespace_math
        result = codespace_math.run(root, a.experiment, a.out, a.message, a.local_only, a.manifest, a.resume_from)
    else: result = update_run(root, a.run_id, a.solver, a.profile, a.note, a.next, a.state, a.feedback, a.agent_id, a.ack_feedback)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError) as exc:
        raise SystemExit(str(exc))
