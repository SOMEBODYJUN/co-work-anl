"""Small per-RUN research records built on research_runtime, never a prover.

The only worker/event state is run.json plus its existing immutable events.
studio.json indexes versioned applications, artifacts, reviews and backflow
plans. All checks below validate declarations and byte bindings, not their
mathematics. Actual agents and Git publication belong to Work and checkpoint.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import sys

import research_runtime as runtime
from curation import _safe_path
from research_frontier import repository_snapshot


LINES = {'main': 'full', 'independent': 'obstacle',
         'informed-a': 'full', 'informed-b': 'full'}
ARTIFACT_STATES = {'draft', 'candidate', 'established', 'conditional', 'finite',
                   'refuted', 'failed', 'open'}
HASH = re.compile(r'[0-9a-f]{64}')


def _json(root, name):
    return json.loads(_safe_path(root, name).read_text(encoding='utf-8'))


def _ref(root, name):
    path = _safe_path(root, name)
    return {'path': path.relative_to(root).as_posix(),
            'sha256': runtime.digest(path.read_bytes())}


def _actor(root):
    result = subprocess.run(['git', 'config', '--local', '--get', 'wcg.actor'],
                            cwd=root, capture_output=True, text=True)
    value = result.stdout.strip()
    if result.returncode or not re.fullmatch(r'Boss[1-9][0-9]*', value):
        raise ValueError('Bind this clone to the explicit Boss with work.py start first')
    return value


def _names(run_id):
    runtime.identity(run_id)
    return ('research/runs/' + run_id, 'research/workspaces/' + run_id)


def _own(root, run_id, name, *, line=None, workspace=False):
    """Never read a control record or write a note in another RUN/line."""
    home, work = _names(run_id)
    path = _safe_path(root, name)
    relative = path.relative_to(root).as_posix()
    prefixes = [work + '/'] if workspace else [home + '/', work + '/']
    if line:
        prefixes = [work + '/' + line + '/']
    if not any(relative.startswith(prefix) for prefix in prefixes):
        raise ValueError('Use this RUN\'s own ' + ('line ' + line if line else 'workspace') + ' path')
    return path


def _studio(root, run_id):
    home, _ = _names(run_id)
    index = _json(root, home + '/studio.json')
    if index.get('schema') != 1 or index.get('run_id') != run_id:
        raise ValueError('Invalid studio index')
    if index.get('owner') != _actor(root):
        raise ValueError('This studio belongs to another Boss; use its own clone/RUN')
    snapshot = repository_snapshot(root, index['opening_snapshot']['branch'])
    if snapshot['remote'] != index['opening_snapshot']['remote']:
        raise ValueError('Studio origin changed; recover its original repository route')
    run = _json(root, home + '/run.json')
    return index, run


def _save_index(root, run_id, index):
    home, _ = _names(run_id)
    runtime._write_json(_safe_path(root, home + '/studio.json'), index)


def _record(root, run_id, record_file):
    _own(root, run_id, record_file, workspace=True)
    value = _json(root, record_file)
    if not isinstance(value, dict):
        raise ValueError('record-file must contain one JSON object')
    return value


def _store(root, run_id, category, item_id, record):
    home, _ = _names(run_id)
    runtime.identity(item_id)
    revision = runtime.pin(record)
    name = home + '/studio/' + category + '/' + item_id + '/' + revision + '.json'
    path = _safe_path(root, name)
    if path.exists() and _json(root, name) != record:
        raise ValueError('Immutable record collision')
    if not path.exists():
        runtime._write_json(path, record)
    return {**_ref(root, name), 'revision_pin': revision}


def _read_indexed(root, run_id, reference):
    _own(root, run_id, reference['path'])
    ref = {key: reference[key] for key in ('path', 'sha256')}
    record = json.loads(runtime.ref_bytes(root, ref))
    if runtime.pin(record) != reference.get('revision_pin'):
        raise ValueError('Stale record revision pin')
    return record


def _references(root, values, label, *, nonempty=False):
    if not isinstance(values, list) or (nonempty and not values):
        raise ValueError(label + ' must be an explicit reference list')
    for ref in values:
        runtime.ref_bytes(root, ref)


def _line_note(root, run_id, line_id, ref, run):
    _own(root, run_id, ref['path'])
    prefix = _names(run_id)[1] + '/' + line_id + '/'
    if ref['path'].startswith(prefix):
        return
    current = run['solvers'].get(line_id, {}).get('latest_event')
    seen = set()
    while current and current not in seen:
        seen.add(current)
        event = _json(root, _names(run_id)[0] + '/events/' + runtime.identity(current) + '.json')
        if event['note'] == ref:
            return
        current = event.get('continuation_of')
    raise ValueError('Artifact note must belong to its actual line, not another researcher')


def _evidence_or_debt(root, row, paid_states):
    runtime.nonempty(row, ['state'])
    if row['state'] in paid_states:
        runtime.ref_bytes(root, row['proof_ref'])
        return set()
    if row['state'] not in {'open', 'gap', 'open-obligation', 'explicit-assumption'}:
        raise ValueError('Unknown payment state: ' + row['state'])
    return {runtime.identity(row.get('obligation_id'))}


def init(root, run_id, spec_file, registry=runtime.REGISTRY, *, expect_branch, expect_remote=None):
    snapshot = repository_snapshot(root, expect_branch)
    if expect_remote is not None and snapshot['remote'] != expect_remote:
        raise ValueError('Expected remote differs from this clone')
    owner = _actor(root)
    home, work = _names(run_id)
    if _safe_path(root, home + '/studio.json').exists():
        raise ValueError('Studio exists; use studio status and preserve its records')
    if runtime.run_path(root, run_id).exists():
        raise ValueError('Existing RUN is preserved; resume it, or choose a new studio RUN')
    spec = _json(root, spec_file)
    if spec.get('template_only') is True:
        raise ValueError('Fill the real target references and remove template_only before opening a research RUN')
    # Validate both inputs before init writes anything. No library results enter
    # the obstacle packet, even though all workers share a filesystem.
    obstacle = runtime.packet(root, spec, 'obstacle', registry)
    initialized = runtime.init_run(root, run_id, spec_file, registry, mode='open')
    run = _json(root, home + '/run.json')
    runtime._write_json(_safe_path(root, home + '/packet-obstacle.json'), obstacle)
    run['packet_pins']['obstacle'] = runtime.pin(obstacle)
    run['solver_roster'] = [{'solver_id': key, 'profile': value} for key, value in LINES.items()]
    run['solver_count'] = len(LINES)
    run['subagent_count'] = 3
    run['launch_plan'] = {'platform': 'Work', 'mode': 'studio', 'subagent_count': 3,
                          'instruction': 'Main plus three mathematical lines; record actual Work launches, never infer liveness from saved IDs.'}
    runtime._write_json(runtime.run_path(root, run_id), run)
    index = {'schema': 1, 'run_id': run_id, 'owner': owner, 'opening_snapshot': snapshot,
             'artifacts': {}, 'applications': {}, 'freezes': {}, 'reviews': {}, 'backflow_plans': {}}
    _save_index(root, run_id, index)
    for line_id in LINES:
        name = work + '/' + line_id + '/journal.md'
        path = _own(root, run_id, name, line=line_id)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('# ' + line_id + '\n\n## Current mathematical obligation\n\n## Derivation and evidence\n\n## Unpaid obligations and next action\n', encoding='utf-8')
    return {**initialized, 'status': 'studio-initialized-local-not-pushed',
            'studio': home + '/studio.json', 'workspace': work,
            'solver_count': 4, 'subagent_count': 3, 'solver_roster': run['solver_roster'],
            'packets': [home + '/packet-' + profile + '.json' for profile in ('obstacle', 'full')],
            'agents_launched': 0}


def line(root, run_id, line_id, note, next_action, agent_id, session_tag, *,
         state='working', feedback=None, ack_feedback=False, model=None,
         reasoning_effort=None, fork_turns=None, read_ledger=None):
    index, run = _studio(root, run_id)
    if line_id not in LINES:
        raise ValueError('Use main, independent, informed-a or informed-b')
    _own(root, run_id, note, line=line_id)
    runtime.nonempty({'agent_id': agent_id, 'session_tag': session_tag}, ['agent_id', 'session_tag'])
    old = run['solvers'].get(line_id, {})
    if old.get('session_tag') != session_tag or old.get('agent_id') != agent_id:
        if line_id != 'main' and any(value is None for value in (model, reasoning_effort, fork_turns)):
            raise ValueError('A new session/agent requires its actual model, reasoning effort and fork mode')
    ledger = None
    if read_ledger:
        _own(root, run_id, read_ledger, line=line_id)
        ledger = _json(root, read_ledger)
        runtime.nonempty(ledger, ['note'])
        _references(root, ledger.get('reads'), 'reads')
        if line_id == 'independent':
            packet = _json(root, _names(run_id)[0] + '/packet-obstacle.json')
            inputs = packet['input_refs']
            allowed = [inputs['problem'], *inputs['definitions'], *inputs['obstacles']]
            own_prefix = _names(run_id)[1] + '/independent/'
            if any(ref not in allowed and not ref['path'].startswith(own_prefix) for ref in ledger['reads']):
                raise ValueError('Independent input contains informed material; preserve this RUN and open an explicit new input contract')
    result = runtime.update_run(root, run_id, line_id, LINES[line_id], note,
                                next_action, state, feedback, agent_id, ack_feedback,
                                model, reasoning_effort, fork_turns,
                                session_tag=session_tag, read_ledger=ledger)
    return {**result, 'session_tag': session_tag, 'platform_liveness': 'not-verified'}


def _validate_application(root, run_id, record, index, run, *, ancestry=None):
    runtime.identity(record['application_id'])
    if record.get('line') not in {'main', 'informed-a', 'informed-b'}:
        raise ValueError('Only informed lines adopt graph results')
    if record.get('problem_spec_pin') != run['spec_pin']:
        raise ValueError('Application must bind this RUN original spec pin')
    spec = _json(root, run['spec'])
    if runtime.pin(spec) != run['spec_pin']:
        raise ValueError('Original spec changed; recover it before adopting results')
    data, objects = runtime.load(root, run['registry'], verify=False)
    catalog, _ = runtime.relation_catalog(root, data)
    if record.get('edge_id') not in catalog:
        raise ValueError('Unknown application edge')
    name, edge = catalog[record['edge_id']]
    runtime.check_edge(root, name, run['registry'])
    if record.get('edge_declaration_pin') != runtime.pin(edge):
        raise ValueError('Stale application edge declaration pin')
    endpoints = set(edge['source_ids'] + edge['target_ids'])
    if record.get('object_pins') != {oid: runtime.pin(objects[oid]) for oid in endpoints}:
        raise ValueError('Application must bind every endpoint object pin')
    direction = record.get('direction')
    if direction not in {'forward', 'reverse'} or (direction == 'reverse' and edge['kind'] != 'equivalent_to'):
        raise ValueError('Reverse adoption requires an equivalence')
    if edge['kind'] not in runtime.LOGICAL or edge['kind'] == 'refutes':
        raise ValueError('Context/refutation edges are evidence, not positive support applications')
    runtime.require_edge_result(edge)
    premises = edge['source_ids'] if direction == 'forward' else edge['target_ids']
    bindings = record.get('premise_bindings')
    if not isinstance(bindings, list) or len(bindings) != len(premises) or {row.get('source_id') for row in bindings} != set(premises):
        raise ValueError('Every ALL premise needs exactly one explicit binding')
    runtime.nonempty(record, ['source_to_target_mapping', 'actual_result', 'remaining'])
    _references(root, record.get('evidence_refs'), 'evidence_refs', nonempty=True)
    debts = set()
    for row in bindings:
        runtime.nonempty(row, ['local_statement', 'applicability'])
        if row.get('source_pin') != runtime.pin(objects[row['source_id']]):
            raise ValueError('Stale premise object pin')
        debts |= _evidence_or_debt(root, row, {'established-here'})
    bridge = record.get('bridge_obligation')
    if not isinstance(bridge, dict):
        raise ValueError('Explicit composition bridge required')
    runtime.nonempty(bridge, ['statement'])
    debts |= _evidence_or_debt(root, bridge, {'global-whole-argument-applies', 'new-bridge-established'})
    if record.get('conditions_text') != edge['conditions']:
        raise ValueError('Preserve the complete edge conditions text')
    conditions = record.get('condition_discharge')
    if not isinstance(conditions, list) or not conditions:
        raise ValueError('Explicit condition discharge required, including an unconditional edge\'s applicability')
    if edge['conditions'] not in [row.get('condition') for row in conditions]:
        raise ValueError('Condition records must cover the full declared conditions')
    for row in conditions:
        runtime.nonempty(row, ['condition', 'argument'])
        debts |= _evidence_or_debt(root, row, {'established'})
    applicability = record.get('applicability')
    if not isinstance(applicability, dict):
        raise ValueError('Explicit model, quantifier and scope applicability required')
    runtime.nonempty(applicability, ['model', 'quantifiers', 'scope'])
    expected_scope = 'contribution' if 'contribution' in edge else 'whole'
    if record.get('result_scope') != expected_scope:
        raise ValueError('A partial contribution cannot establish the whole target')
    if expected_scope == 'contribution':
        remaining = record.get('target_remaining')
        if not isinstance(remaining, dict) or remaining.get('statement') != edge['contribution']['remaining']:
            raise ValueError('Preserve the contribution remaining obligation')
        runtime.identity(remaining.get('obligation_id'))
    ancestry = set(ancestry or ()) | {record['application_id']}
    dependencies = record.get('depends_on_applications')
    if not isinstance(dependencies, list):
        raise ValueError('Explicit upstream application list required')
    inherited, seen, target_remaining = set(), set(), {}
    for dependency in dependencies:
        aid = runtime.identity(dependency.get('application_id'))
        if aid in ancestry or aid in seen:
            raise ValueError('Conditional application cycle or duplicate dependency cannot pay itself')
        seen.add(aid)
        ref = index['applications'].get(aid)
        if ref is None or dependency.get('revision_pin') != ref['revision_pin']:
            raise ValueError('Unknown or stale upstream application revision')
        upstream = _read_indexed(root, run_id, ref)
        # Recursively recheck selected dependencies, not all research records.
        outcome = _validate_application(root, run_id, upstream, index, run, ancestry=ancestry)
        inherited |= set(outcome['unpaid_obligation_ids'])
        for oid, statement in outcome['target_remaining'].items():
            if oid in target_remaining and target_remaining[oid] != statement:
                raise ValueError('Inherited target obligation has conflicting statements')
            target_remaining[oid] = statement
    for binding in bindings:
        dependency = binding.get('from_application')
        if dependency is not None and dependency not in dependencies:
            raise ValueError('Premise application source must name its exact declared upstream revision')
    runtime.strings(record.get('inherited_unpaid_obligation_ids'), 'inherited_unpaid_obligation_ids')
    if set(record['inherited_unpaid_obligation_ids']) != inherited:
        raise ValueError('Inherited upstream debt must be preserved in full')
    discharges = record.get('discharged_obligations')
    if not isinstance(discharges, list):
        raise ValueError('Explicit discharged_obligations list required')
    paid = set()
    for row in discharges:
        oid = runtime.identity(row.get('obligation_id'))
        if oid not in inherited or oid in paid:
            raise ValueError('Discharge must name an actual distinct inherited debt')
        runtime.ref_bytes(root, row['proof_ref'])
        paid.add(oid)
    debts |= inherited - paid
    # A proposed bridge may guide research but its missing argument remains due.
    if edge['status'] != 'accepted':
        debts.add('edge-' + edge['edge_id'] + '-argument')
    runtime.strings(record.get('unpaid_obligation_ids'), 'unpaid_obligation_ids')
    if set(record['unpaid_obligation_ids']) != debts:
        raise ValueError('Application unpaid obligations omit or invent a premise, condition, bridge or inherited debt')
    if expected_scope == 'contribution':
        remaining = record['target_remaining']
        oid = remaining['obligation_id']
        if oid in target_remaining and target_remaining[oid] != remaining['statement']:
            raise ValueError('Inherited target obligation has conflicting statements')
        target_remaining[oid] = remaining['statement']
    return {'unpaid_obligation_ids': sorted(debts), 'result_scope': expected_scope,
            'target_remaining': target_remaining}


def adopt(root, run_id, record_file):
    index, run = _studio(root, run_id)
    record = _record(root, run_id, record_file)
    outcome = _validate_application(root, run_id, record, index, run)
    aid = record['application_id']
    ref = _store(root, run_id, 'applications', aid, record)
    index['applications'][aid] = ref
    _save_index(root, run_id, index)
    return {'status': 'application-recorded-not-a-proof', 'application_id': aid, **ref, **outcome,
            'dependency_check_scope': 'Explicit application dependencies only; proof text is not parsed for hidden dependencies.'}


def artifact(root, run_id, record_file):
    index, run = _studio(root, run_id)
    record = _record(root, run_id, record_file)
    aid = runtime.identity(record['artifact_id'])
    line_id = record.get('line')
    if line_id not in LINES or record.get('state') not in ARTIFACT_STATES:
        raise ValueError('Explicit artifact line and mathematical state required')
    runtime.nonempty(record, ['kind', 'statement'])
    note = record['note_ref']
    _line_note(root, run_id, line_id, note, run)
    runtime.ref_bytes(root, note)
    solver = run['solvers'].get(line_id)
    if not solver or not solver.get('agent_id'):
        raise ValueError('Record the actual line agent before its artifact')
    authors = record.get('authors')
    runtime.strings(authors, 'authors', True)
    if solver['agent_id'] not in authors:
        raise ValueError('Artifact authors must include its recorded line agent')
    runtime.strings(record.get('unpaid_obligation_ids'), 'unpaid_obligation_ids')
    _references(root, record.get('evidence_refs'), 'evidence_refs')
    _references(root, record.get('publication_refs'), 'publication_refs')
    applications = record.get('applications')
    if not isinstance(applications, list):
        raise ValueError('Explicit artifact applications list required')
    if line_id == 'independent' and applications:
        raise ValueError('Independent artifacts cannot adopt informed graph applications')
    for selected in applications:
        ref = index['applications'].get(selected['application_id'])
        if ref is None or ref['revision_pin'] != selected.get('revision_pin'):
            raise ValueError('Artifact selects a stale or unknown application')
    # A stable immutable copy allows the working journal to keep evolving.
    home, _ = _names(run_id)
    snapshot_name = home + '/studio/artifact-notes/' + runtime.digest(runtime.ref_bytes(root, note)) + '.md'
    snapshot = _safe_path(root, snapshot_name)
    if not snapshot.exists():
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(runtime.ref_bytes(root, note))
    record = copy.deepcopy(record)
    record['note_ref'] = _ref(root, snapshot_name)
    record['line_event_id'] = solver['latest_event']
    ref = _store(root, run_id, 'artifacts', aid, record)
    index['artifacts'][aid] = ref
    _save_index(root, run_id, index)
    return {'status': 'artifact-saved-local-not-pushed', 'artifact_id': aid, **ref}


def _application_refs(root, run_id, selections, index, run):
    refs, debts, target_remaining = [], set(), {}
    for selected in selections:
        aid = selected['application_id']
        ref = index['applications'].get(aid)
        if ref is None or ref['revision_pin'] != selected.get('revision_pin'):
            raise ValueError('Application revision changed; inspect its actual consumers')
        application = _read_indexed(root, run_id, ref)
        outcome = _validate_application(root, run_id, application, index, run)
        debts |= set(outcome['unpaid_obligation_ids'])
        for oid, statement in outcome['target_remaining'].items():
            if oid in target_remaining and target_remaining[oid] != statement:
                raise ValueError('Target obligation identity has conflicting statements')
            target_remaining[oid] = statement
        refs.append(ref)
    return refs, debts, target_remaining


def _application_content(root, run_id, selections, index):
    """Review the actual adopted argument and every declared payment input."""
    refs, seen = [], set()
    run = _json(root, _names(run_id)[0] + '/run.json')
    if selections:
        data, objects = runtime.load(root, run['registry'], verify=False)
        catalog, _ = runtime.relation_catalog(root, data)
    queue = list(selections)
    while queue:
        selected = queue.pop()
        aid = selected['application_id']
        if aid in seen:
            continue
        seen.add(aid)
        ref = index['applications'][aid]
        application = _read_indexed(root, run_id, ref)
        refs.append({key: ref[key] for key in ('path', 'sha256')})
        edge_path, edge = catalog[application['edge_id']]
        refs.append(_ref(root, edge_path))
        refs.extend(edge['evidence'])
        for oid in dict.fromkeys(edge['source_ids'] + edge['target_ids']):
            refs.extend([objects[oid]['body'], *objects[oid]['evidence']])
        refs.extend(application['evidence_refs'])
        payments = [*application['premise_bindings'], application['bridge_obligation'],
                    *application['condition_discharge'], *application['discharged_obligations']]
        refs.extend(row['proof_ref'] for row in payments if 'proof_ref' in row)
        queue.extend(application['depends_on_applications'])
    return refs


def _input_content(root, run):
    spec = _json(root, run['spec'])
    if runtime.pin(spec) != run['spec_pin']:
        raise ValueError('Original spec bytes changed')
    refs = [_ref(root, run['spec'])]
    for profile, expected in run['packet_pins'].items():
        name = _names(run['run_id'])[0] + '/packet-' + profile + '.json'
        packet = _json(root, name)
        if runtime.pin(packet) != expected:
            raise ValueError('Saved packet bytes changed')
        inputs = packet.get('input_refs', spec)
        refs.extend([_ref(root, name), inputs['problem'], *inputs['definitions'], *inputs['obstacles']])
    _references(root, refs, 'original inputs')
    return refs


def _publication_content(root, item, run):
    """Expand the explicit batch/edge inputs without requiring duplicate refs."""
    refs, declarations, objects = [], [], {}
    for publication in item['publication_refs']:
        raw = runtime.ref_bytes(root, publication)
        try:
            document = json.loads(raw)
        except (ValueError, UnicodeError):
            continue
        if not isinstance(document, dict):
            continue
        if document.get('schema') == 2 and isinstance(document.get('objects'), list):
            objects.update((obj['object_id'], obj) for obj in document['objects'])
            for obj in document['objects']:
                refs.extend([obj['body'], *obj['evidence']])
            refs.extend({key: row[key] for key in ('path', 'sha256')} for row in document['materials'])
        elif {'edge_id', 'source_ids', 'target_ids'} <= document.keys():
            declarations.append(document)
            refs.extend(document['evidence'])
    if declarations:
        canonical = _safe_path(root, run['registry'])
        existing = runtime.load(root, run['registry'], verify=False)[1] if canonical.exists() else {}
        existing.update(objects)
        for edge in declarations:
            for oid in set(edge['source_ids'] + edge['target_ids']):
                if oid not in existing:
                    raise ValueError('Publication edge endpoint requires its registered object or reviewed batch: ' + oid)
                refs.extend([existing[oid]['body'], *existing[oid]['evidence']])
    return refs


def freeze(root, run_id, artifact_id, freeze_id=None):
    index, run = _studio(root, run_id)
    ref = index['artifacts'].get(runtime.identity(artifact_id))
    if ref is None:
        raise ValueError('Unknown artifact')
    item = _read_indexed(root, run_id, ref)
    applications, debts, target_remaining = _application_refs(root, run_id, item['applications'], index, run)
    debts |= set(item['unpaid_obligation_ids'])
    refs = [item['note_ref'], *item['evidence_refs'], *item['publication_refs'],
            {'path': ref['path'], 'sha256': ref['sha256']}, *_input_content(root, run),
            *_publication_content(root, item, run),
            *_application_content(root, run_id, item['applications'], index)]
    refs = list({runtime.pin(ref): ref for ref in refs}.values())
    _references(root, refs, 'frozen content')
    runtime.strings(item['unpaid_obligation_ids'], 'unpaid_obligation_ids')
    fid = runtime.identity(freeze_id or artifact_id + '-' + ref['revision_pin'][:12])
    if fid in index['freezes']:
        raise ValueError('Freeze ID already exists; retain the old review version')
    record = {'freeze_id': fid, 'artifact_id': artifact_id, 'artifact_ref': ref,
              'spec_pin': run['spec_pin'], 'packet_pins': run['packet_pins'],
              'application_refs': applications, 'content_refs': refs,
              'unpaid_obligation_ids': sorted(debts), 'target_remaining': target_remaining,
              'authors': item['authors'], 'state': item['state']}
    saved = _store(root, run_id, 'freezes', fid, record)
    index['freezes'][fid] = saved
    _save_index(root, run_id, index)
    return {'status': 'frozen-local-not-pushed-not-reviewed', 'freeze_id': fid, **saved}


def _current_freeze(root, run_id, freeze_id, index, run):
    ref = index['freezes'].get(freeze_id)
    if ref is None:
        raise ValueError('Unknown freeze ID')
    frozen = _read_indexed(root, run_id, ref)
    if frozen['spec_pin'] != run['spec_pin'] or frozen['packet_pins'] != run['packet_pins']:
        raise ValueError('Frozen input contract changed')
    if index['artifacts'].get(frozen['artifact_id']) != frozen['artifact_ref']:
        raise ValueError('Artifact has a new revision; old review cannot cover new content')
    item = _read_indexed(root, run_id, frozen['artifact_ref'])
    _application_refs(root, run_id, item['applications'], index, run)
    _references(root, frozen['content_refs'], 'frozen content')
    # Also check original source bytes for freezes made before input expansion.
    _input_content(root, run)
    return ref, frozen, item


def review(root, run_id, record_file):
    index, run = _studio(root, run_id)
    record = _record(root, run_id, record_file)
    rid = runtime.identity(record['review_id'])
    ref, frozen, _ = _current_freeze(root, run_id, record['freeze_id'], index, run)
    if record.get('freeze_revision_pin') != ref['revision_pin']:
        raise ValueError('Review must bind the exact frozen revision')
    runtime.nonempty(record, ['reviewer_agent_id', 'scope'])
    if record['reviewer_agent_id'] in frozen['authors'] or record.get('independent') is not True:
        raise ValueError('Review requires an independent nonauthor declaration')
    if record['reviewer_agent_id'] == run['solvers'].get('independent', {}).get('agent_id'):
        raise ValueError('The original-only independent line cannot read informed review inputs; use a fresh challenger')
    if record.get('verdict') not in {'approve', 'changes-required', 'inconclusive'}:
        raise ValueError('Explicit review verdict required')
    _own(root, run_id, record['report_ref']['path'], workspace=True)
    runtime.ref_bytes(root, record['report_ref'])
    if record.get('reviewed_content_refs') != frozen['content_refs']:
        raise ValueError('Review must enumerate the exact frozen content hashes')
    if record.get('evidence_level') not in {'internal-independent', 'formal', 'external'}:
        raise ValueError('Explicit evidence level required; this command does not certify it')
    resolutions = record.get('resolves_review_ids', [])
    runtime.strings(resolutions, 'resolves_review_ids')
    if resolutions:
        runtime.nonempty(record, ['resolution_argument'])
    for review_id in resolutions:
        previous = index['reviews'].get(review_id)
        if previous is None:
            raise ValueError('Review resolution must reference an existing exact report')
        previous = _read_indexed(root, run_id, previous)
        if previous['freeze_id'] != record['freeze_id'] or previous['freeze_revision_pin'] != ref['revision_pin']:
            raise ValueError('Review resolution must cover the same exact frozen revision')
    saved = _store(root, run_id, 'reviews', rid, record)
    if rid in index['reviews'] and index['reviews'][rid] != saved:
        raise ValueError('Review ID is immutable; use a new ID for a new report')
    index['reviews'][rid] = saved
    _save_index(root, run_id, index)
    return {'status': 'review-declaration-bound-structure-only', 'review_id': rid, **saved,
            'mathematics_verified_by_program': False}


def promote(root, run_id, record_file):
    """Prepare a checked backflow plan, never publish or change truth_status."""
    import registration
    index, run = _studio(root, run_id)
    record = _record(root, run_id, record_file)
    pid = runtime.identity(record['plan_id'])
    freeze_ref, frozen, item = _current_freeze(root, run_id, record['freeze_id'], index, run)
    selected = index['reviews'].get(record.get('review_id'))
    if selected is None:
        raise ValueError('An independent exact-version review is required before backflow')
    report = _read_indexed(root, run_id, selected)
    runtime.ref_bytes(root, report['report_ref'])
    if report['freeze_id'] != frozen['freeze_id'] or report['freeze_revision_pin'] != freeze_ref['revision_pin'] or report['verdict'] != 'approve':
        raise ValueError('Review does not approve this exact frozen revision')
    objections = set()
    for review_id, review_ref in index['reviews'].items():
        other = _read_indexed(root, run_id, review_ref)
        if (other['freeze_id'] == frozen['freeze_id'] and other['freeze_revision_pin'] == freeze_ref['revision_pin']
                and other['verdict'] != 'approve'):
            objections.add(review_id)
    if objections - set(report.get('resolves_review_ids', [])):
        raise ValueError('Unresolved independent review objections block backflow; record their substantive resolution')
    if record.get('claim_scope') not in {'local-result', 'whole-target'}:
        raise ValueError('Explicit backflow claim_scope required')
    if frozen['state'] not in {'established', 'conditional', 'finite', 'refuted', 'open'}:
        raise ValueError('Drafts, candidates and failed attempts remain research artifacts')
    if frozen['unpaid_obligation_ids'] and frozen['state'] not in {'conditional', 'open'}:
        raise ValueError('Unpaid obligations block an established backflow claim')
    if record['claim_scope'] == 'whole-target' and (frozen['unpaid_obligation_ids'] or frozen['state'] != 'established'):
        raise ValueError('Whole-target claim still has unpaid or conditional obligations')
    runtime.nonempty(record, ['scope_argument'])
    batch_ref = record['registration_batch_ref']
    _own(root, run_id, batch_ref['path'], workspace=True)
    batch = json.loads(runtime.ref_bytes(root, batch_ref))
    validation = registration.validate_batch(root, batch)
    requested = record.get('object_ids')
    runtime.strings(requested, 'object_ids', True)
    objects = {obj['object_id']: obj for obj in batch['objects']}
    if set(requested) != set(objects):
        raise ValueError('Backflow plan must account for every batch object')
    truths = {'established': {'proved', 'definition'}, 'conditional': {'conditional'},
              'finite': {'finite'}, 'refuted': {'refuted'}, 'open': {'open'}}
    content = {(ref['path'], ref['sha256'], ref.get('section')) for ref in frozen['content_refs']}
    target_discharges = record.get('target_discharges', [])
    if not isinstance(target_discharges, list):
        raise ValueError('target_discharges must be an explicit list')
    covered = set()
    for row in target_discharges:
        oid = runtime.identity(row.get('obligation_id'))
        runtime.nonempty(row, ['argument'])
        ref = row['proof_ref']
        runtime.ref_bytes(root, ref)
        if oid in covered or oid not in frozen['target_remaining']:
            raise ValueError('Target discharge must name a distinct real contribution remaining obligation')
        if (ref['path'], ref['sha256'], ref.get('section')) not in content:
            raise ValueError('Target discharge proof was not among the reviewed frozen bytes')
        covered.add(oid)
    if record['claim_scope'] == 'whole-target' and covered != set(frozen['target_remaining']):
        raise ValueError('A contribution cannot close the whole target until every target remaining obligation is explicitly discharged')
    if (batch_ref['path'], batch_ref['sha256'], batch_ref.get('section')) not in content:
        raise ValueError('Registration batch metadata was not among the reviewed frozen bytes')
    for material in batch['materials']:
        if (material['path'], material['sha256'], None) not in content:
            raise ValueError('Publication material was not among the reviewed frozen bytes')
    for obj in objects.values():
        if obj['truth_status'] not in truths[frozen['state']]:
            raise ValueError('Batch truth_status exceeds the reviewed artifact state')
        for reference in [obj['body'], *obj['evidence']]:
            if (reference['path'], reference['sha256'], reference.get('section')) not in content:
                raise ValueError('Publication body/evidence was not among the reviewed frozen bytes')
    edge_refs = record.get('edge_refs')
    _references(root, edge_refs, 'edge_refs')
    for ref in edge_refs:
        if (ref['path'], ref['sha256'], ref.get('section')) not in content:
            raise ValueError('New edge declaration was not among the reviewed frozen bytes')
        for evidence in _json(root, ref['path'])['evidence']:
            if (evidence['path'], evidence['sha256'], evidence.get('section')) not in content:
                raise ValueError('New edge evidence was not among the reviewed frozen bytes')
    # Compose the explicit delta into the existing registry, preserving its
    # historical registration baseline and all unrelated identities. This is
    # the same object/material format consumed by existing research register.
    canonical_path = _safe_path(root, run['registry'])
    previous = _json(root, run['registry']) if canonical_path.exists() else {
        'schema': 2, 'objects': [], 'materials': [], 'edge_files': []}
    old = {obj['object_id']: obj for obj in previous['objects']}
    for oid, obj in objects.items():
        if oid in old and obj != old[oid] and obj['version'] <= old[oid]['version']:
            raise ValueError('Changed object requires a new version')
    combined = dict(old)
    combined.update(objects)
    materials = {row['path']: copy.deepcopy(row) for row in previous['materials']}
    for row in batch['materials']:
        before = materials.get(row['path'])
        if before and before['sha256'] == row['sha256'] and {
                before['disposition'], row['disposition']} <= {'objects', 'attachment'}:
            materials[row['path']] = registration.merge_material(before, row)
        else:
            materials[row['path']] = copy.deepcopy(row)
    proposed = copy.deepcopy(previous)
    proposed.update(objects=[combined[key] for key in sorted(combined)],
                    materials=[materials[key] for key in sorted(materials)])
    proposed['edge_files'] = list(dict.fromkeys(previous.get('edge_files', []) + [ref['path'] for ref in edge_refs]))
    proposed['backflow_guard'] = {'registry': run['registry'],
                                 'base_sha256': runtime.digest(canonical_path.read_bytes()) if canonical_path.exists() else None}
    runtime.load(root, provided=proposed)
    candidate_name = record.get('candidate_registry_path', _names(run_id)[1] + '/backflow/' + pid + '/proposed.json')
    _own(root, run_id, candidate_name, workspace=True)
    if not candidate_name.startswith(_names(run_id)[1] + '/backflow/' + pid + '/'):
        raise ValueError('Candidate output belongs in this plan\'s dedicated backflow directory')
    if candidate_name in {batch_ref['path'], run['spec']} or any(
            ref['path'] == candidate_name for ref in frozen['content_refs']):
        raise ValueError('Candidate output cannot overwrite its input or reviewed content')
    # Validate each explicit edge against the in-memory merged objects first.
    for ref in edge_refs:
        edge = _json(root, ref['path'])
        runtime.verify_endpoints(root, edge, combined)
        for oid in set(edge['source_ids'] + edge['target_ids']):
            for reference in [combined[oid]['body'], *combined[oid]['evidence']]:
                if (reference['path'], reference['sha256'], reference.get('section')) not in content:
                    raise ValueError('Publication edge endpoint body/evidence was not among the reviewed frozen bytes')
        runtime.edges(root, dict(proposed, edge_files=[ref['path']]), combined)
    runtime._write_json(_safe_path(root, candidate_name), proposed)
    candidate = _ref(root, candidate_name)
    checks = [runtime.check_edge(root, ref['path'], candidate_name) for ref in edge_refs]
    plan = {**record, 'freeze_ref': freeze_ref, 'review_ref': selected,
            'candidate_registry_ref': candidate,
            'validation': validation, 'edge_checks': checks,
            'base_registry_ref': _ref(root, run['registry']) if canonical_path.exists() else None,
            'status': 'backflow-plan-ready-local-not-published',
            'commands': [['python', 'work.py', 'research', 'register', '--record-file', candidate_name],
                         *[['python', 'work.py', 'research', 'edge-check', ref['path']] for ref in edge_refs],
                         ['python', 'work.py', 'research', 'check'],
                         ['python', 'work.py', 'research', 'build']],
            'instruction': 'Main reviews and serially registers/checkpoints these exact bytes using existing tools. This receipt did not change canonical registration, prove mathematics or confirm a push.'}
    saved = _store(root, run_id, 'backflow-plans', pid, plan)
    index['backflow_plans'][pid] = saved
    _save_index(root, run_id, index)
    return {'status': plan['status'], 'plan_id': pid, **saved,
            'candidate_registry_ref': candidate,
            'commands': plan['commands'], 'canonical_registry_modified': False,
            'checkpoint_review_args': ['--review-plan', saved['path']],
            'publication_instruction': 'After register/check/build, checkpoint the exact publication paths with these review arguments; checkpoint verifies the final pushed commit against the frozen review.'}


def status(root, run_id, session_tag=None):
    index, run = _studio(root, run_id)
    recovered = runtime.resume(root, run_id)
    lines = {}
    for line_id, profile in LINES.items():
        saved = run['solvers'].get(line_id, {})
        tag = saved.get('session_tag')
        lines[line_id] = {'profile': profile, 'agent_id': saved.get('agent_id'),
                          'saved_session_tag': tag, 'state': saved.get('state', 'not-dispatched'),
                          'session_match': None if session_tag is None else bool(tag and tag == session_tag),
                          'action': 'inspect-platform-before-followup' if tag and tag == session_tag else 'recover-input-notes-feedback-and-check-platform',
                          'platform_liveness': 'not-verified'}
    issues = []
    for fid in index['freezes']:
        try:
            _current_freeze(root, run_id, fid, index, run)
        except (ValueError, OSError, KeyError, TypeError) as exc:
            issues.append({'freeze_id': fid, 'error': str(exc)})
    application_issues = []
    for aid, ref in index['applications'].items():
        try:
            application = _read_indexed(root, run_id, ref)
            _validate_application(root, run_id, application, index, run)
        except (ValueError, OSError, KeyError, TypeError) as exc:
            application_issues.append({'application_id': aid, 'error': str(exc)})
    return {'studio': index, 'lines': lines, 'recovery': recovered,
            'frozen_version_issues': issues, 'application_version_issues': application_issues,
            'agents_launched': 0,
            'publication': 'Local records only; use checkpoint and verify pushed separately.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--registry', default=runtime.REGISTRY)
    sub = parser.add_subparsers(dest='command', required=True)
    q = sub.add_parser('init'); q.add_argument('run_id'); q.add_argument('--spec', required=True)
    q.add_argument('--expect-branch', required=True); q.add_argument('--expect-remote')
    q = sub.add_parser('status'); q.add_argument('run_id'); q.add_argument('--session-tag')
    q = sub.add_parser('line'); q.add_argument('run_id'); q.add_argument('--line', choices=LINES, required=True)
    q.add_argument('--note', required=True); q.add_argument('--next', required=True)
    q.add_argument('--agent-id', required=True); q.add_argument('--session-tag', required=True)
    q.add_argument('--state', choices=sorted(runtime.STATES), default='working')
    group = q.add_mutually_exclusive_group(); group.add_argument('--feedback'); group.add_argument('--ack-feedback', action='store_true')
    q.add_argument('--model'); q.add_argument('--reasoning-effort'); q.add_argument('--fork-turns', choices=['none', 'all'])
    q.add_argument('--read-ledger')
    for command in ('artifact', 'adopt', 'review', 'promote'):
        q = sub.add_parser(command); q.add_argument('run_id'); q.add_argument('--record-file', required=True)
    q = sub.add_parser('freeze'); q.add_argument('run_id'); q.add_argument('--artifact', required=True); q.add_argument('--freeze-id')
    args = parser.parse_args(argv)
    root = args.repo.resolve()
    if args.command == 'init':
        result = init(root, args.run_id, args.spec, args.registry,
                      expect_branch=args.expect_branch, expect_remote=args.expect_remote)
    elif args.command == 'status':
        result = status(root, args.run_id, args.session_tag)
    elif args.command == 'line':
        result = line(root, args.run_id, args.line, args.note, args.next, args.agent_id,
                      args.session_tag, state=args.state, feedback=args.feedback,
                      ack_feedback=args.ack_feedback, model=args.model,
                      reasoning_effort=args.reasoning_effort, fork_turns=args.fork_turns,
                      read_ledger=args.read_ledger)
    elif args.command == 'freeze':
        result = freeze(root, args.run_id, args.artifact, args.freeze_id)
    else:
        result = globals()[args.command](root, args.run_id, args.record_file)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, TypeError) as error:
        raise SystemExit(str(error))
