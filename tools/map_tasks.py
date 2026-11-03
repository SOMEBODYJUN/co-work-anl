"""Git compare-and-push ownership for bounded hypergraph construction tasks."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path, PurePosixPath
import re
import uuid

import board
import cleanup
import coordination
from curation import _safe_path
import research_runtime as research
from research_runtime import _write_json

ACTIVE = {'claimed', 'blocked'}


def task_path(root, task_id):
    return _safe_path(root, 'map/tasks/' + research.identity(task_id) + '.json')


def listing(root):
    directory = _safe_path(root, 'map/tasks')
    return [json.loads(_safe_path(root, p.relative_to(root).as_posix()).read_text()) for p in sorted(directory.glob('*.json'))]


def overlap(a, b):
    x, y = PurePosixPath(a), PurePosixPath(b)
    return x == y or x in y.parents or y in x.parents


def validate(root, definition):
    research.identity(definition['task_id'])
    research.nonempty(definition, ['goal', 'registry'])
    data, objects = research.load(root, definition['registry'], verify=False)
    research.strings(definition['object_ids'], 'object_ids', True)
    if set(definition['object_ids']) - objects.keys():
        raise ValueError('Task has unknown objects')
    if definition.get('input_pins') != {oid: research.pin(objects[oid]) for oid in definition['object_ids']}:
        raise ValueError('Task input objects changed; reframe the version-bound task')
    for oid in definition['object_ids']:
        research.ref_bytes(root, objects[oid]['body'])
        for ref in objects[oid]['evidence']: research.ref_bytes(root, ref)
    if definition.get('stage') not in {'3A', '3B', '3C', '3D'}:
        raise ValueError('Explicit map construction stage required')
    research.strings(definition['write_paths'], 'write_paths', True)
    for path in definition['write_paths']:
        _safe_path(root, path)
        if not path.startswith(('map/', 'research/workspaces/')) and not re.fullmatch(r'archives/[^/]+(?:/subarchives/[^/]+)*/map(?:/.*)?', path):
            raise ValueError('Map tasks only reserve map or research workspace outputs')
    board.guard(definition)


def plan(root, record_file):
    records = json.loads(_safe_path(root, record_file).read_text())
    if isinstance(records, dict): records = [records]
    if not isinstance(records, list) or not records: raise ValueError('Explicit task definitions required')
    ids = set()
    for record in records:
        validate(root, record)
        task_id = record['task_id']
        if task_id in ids or task_path(root, task_id).exists(): raise ValueError('Duplicate/existing task; preserve ownership')
        ids.add(task_id)
    for record in records:
        _write_json(task_path(root, record['task_id']), {'definition': record, 'state': 'available', 'owner': None})
    return {'status': 'planned-local-not-pushed', 'tasks': sorted(ids)}


def transition(root, old, others, actor, operation, request_id, receipt=None, reason=None):
    new = copy.deepcopy(old)
    definition = old['definition']
    validate(root, definition)
    if operation == 'claim':
        if old['state'] not in {'available', 'handoff'} or old.get('owner'): raise ValueError('Task unavailable')
        for other in others:
            if other['definition']['task_id'] == definition['task_id'] or other['state'] not in ACTIVE: continue
            d = other['definition']
            if set(d['object_ids']).intersection(definition['object_ids']) or any(overlap(a, b) for a in d['write_paths'] for b in definition['write_paths']):
                raise ValueError('Overlapping active map task: ' + d['task_id'])
        new.update(state='claimed', owner=actor)
    elif operation == 'done':
        if old.get('owner') != actor or old['state'] not in ACTIVE: raise ValueError('Only task owner may finish')
        if not isinstance(receipt, dict): raise ValueError('Explicit coverage and already-pushed assets required')
        if set(receipt.get('coverage', {})) != set(definition['object_ids']): raise ValueError('Every input object requires a coverage result')
        data, objects = research.load(root, definition['registry'])
        relations = research.edges(root, data, objects)
        for row in receipt['coverage'].values():
            if row.get('state') not in {'linked', 'isolated-after-review', 'needs-decision'}: raise ValueError('Unknown coverage outcome')
            research.nonempty(row, ['reason', 'comparison_scope'])
        resolved = {oid: row for oid, row in receipt['coverage'].items() if row['state'] != 'needs-decision'}
        research.validate_coverage(resolved, {oid: objects[oid] for oid in resolved}, relations)
        if not receipt.get('assets'): raise ValueError('Pushed edge/coverage assets required')
        for ref in receipt['assets']:
            name = ref['path']
            if not any(name == p or PurePosixPath(p) in PurePosixPath(name).parents for p in definition['write_paths']):
                raise ValueError('Asset outside reserved write scope')
            research.ref_bytes(root, ref)
        research.check(root, definition['registry'])
        new.update(state='done', receipt=receipt, output_commit=board.git(root, 'rev-parse', 'HEAD').stdout.decode().strip())
    elif operation == 'handoff':
        if old.get('owner') != actor or old['state'] not in ACTIVE: raise ValueError('Only hand off own unfinished task')
        if not reason or not reason.strip(): raise ValueError('Concrete handoff reason required')
        new.update(state='handoff', owner=None, previous_owner=actor, reason=reason)
    else: raise ValueError('Unknown map operation')
    new['request_id'] = request_id
    board.guard(new)
    return new


def mutate(root, task_id, operation, receipt=None, reason=None):
    actor = coordination.config(root, 'wcg.actor')
    if not re.fullmatch(r'Boss[1-9][0-9]*', actor): raise ValueError('Explicit Boss identity required')
    branch = coordination.config(root, 'wcg.branch')
    if not branch: raise ValueError('Start this independent clone on the shared result branch first')
    client = board.Board(root, branch=branch, retries=8)
    pending_path = client.cache / 'map-pending' / (research.identity(task_id) + '-' + operation + '.json')
    intent_pin = research.pin({'receipt': receipt, 'reason': reason, 'operation': operation})
    if pending_path.exists():
        pending = json.loads(pending_path.read_text())
        if pending['intent_pin'] != intent_pin:
            raise ValueError('Unconfirmed request exists; resume its original receipt/reason before replacing it')
        request_id = pending['request_id']
    else:
        request_id = uuid.uuid4().hex
        _write_json(pending_path, {'task_id': task_id, 'operation': operation, 'request_id': request_id, 'intent_pin': intent_pin})
    confirmed = False
    name = task_path(root, task_id).relative_to(root).as_posix()
    for _ in range(8):
        with client.scratch() as temporary:
            directory = Path(temporary)
            cleanup.checkout_snapshot(client, directory)
            if coordination.config(root, 'wcg.workflowRun'):
                person, _ = coordination.identity_paths(root, actor)
                p = _safe_path(directory, person)
                if not p.is_file() or json.loads(p.read_text()).get('instance') != coordination.config(root, 'wcg.instance'):
                    raise ValueError('Boss identity is not registered for this map workflow')
            if not confirmed:
                coordination.verify_write(directory, branch, board.git(directory, 'rev-parse', 'HEAD').stdout.decode().strip())
                confirmed = True
            old = json.loads(task_path(directory, task_id).read_text())
            if old.get('request_id') == request_id:
                pending_path.unlink(missing_ok=True)
                return {'status': 'pushed', 'task_id': task_id, 'operation': operation,
                        'remote_tip': board.git(directory, 'rev-parse', 'HEAD').stdout.decode().strip(), 'recovered_acknowledgement': True}
            new = transition(directory, old, listing(directory), actor, operation, request_id, receipt, reason)
            _write_json(task_path(directory, task_id), new)
            board.git(directory, 'add', '--', name)
            board.git(directory, 'commit', '--quiet', '-m', f'map {operation}: {actor} {task_id}')
            pushed = board.git(directory, 'push', '--quiet', 'origin', 'HEAD:refs/heads/' + branch, check=False)
            if board.auth_rejected(pushed): raise board.AuthenticationError('Authentication rejected; stop retries and new claims')
            # Read the remote even after a transport failure: the push may have
            # committed before its acknowledgement was lost.
            _, tip, _ = cleanup.refresh_snapshot(client)
            actual = board.git(directory, 'show', tip + ':' + name, check=False)
            if not actual.returncode and json.loads(actual.stdout).get('request_id') == request_id:
                pending_path.unlink(missing_ok=True)
                return {'status': 'pushed', 'task_id': task_id, 'operation': operation, 'remote_tip': tip,
                        'limit': 'Coverage is not an independent mathematical review'}
            if pushed.returncode and not re.search(rb'non-fast-forward|fetch first|cannot lock ref|failed to update ref|stale info|incorrect old value provided', pushed.stdout + pushed.stderr, re.I):
                detail = board.SECRET.sub('[REDACTED]', pushed.stderr.decode(errors='replace'))
                raise board.BoardError('Map write not confirmed; preserve local drafts: ' + detail[:700])
    raise board.BoardError('Concurrent map write could not be confirmed')


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, required=True)
    sub = p.add_subparsers(dest='command', required=True)
    q = sub.add_parser('inventory'); q.add_argument('--registry', default=research.REGISTRY)
    q = sub.add_parser('plan'); q.add_argument('--record-file', required=True)
    sub.add_parser('list'); sub.add_parser('status')
    for command in ['claim', 'done', 'handoff']:
        q = sub.add_parser(command); q.add_argument('task_id')
        if command == 'done': q.add_argument('--receipt-file', required=True)
        if command == 'handoff': q.add_argument('--reason', required=True)
    a = p.parse_args(argv); root = a.repo.resolve()
    if a.command == 'inventory': result = research.inventory(root, a.registry)
    elif a.command == 'plan': result = plan(root, a.record_file)
    elif a.command == 'list': result = listing(root)
    elif a.command == 'status':
        rows = listing(root)
        result = {'tasks': len(rows), 'states': {s: sum(r['state'] == s for r in rows) for s in ['available', 'claimed', 'done', 'handoff']}}
    else:
        receipt = json.loads(_safe_path(root, a.receipt_file).read_text()) if a.command == 'done' else None
        result = mutate(root, a.task_id, a.command, receipt, getattr(a, 'reason', None))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    try: raise SystemExit(main())
    except (ValueError, OSError, KeyError, board.BoardError) as exc: raise SystemExit(str(exc))
