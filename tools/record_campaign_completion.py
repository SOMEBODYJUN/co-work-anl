#!/usr/bin/env python3
"""Record an already-submitted note's actual completion in its campaign log.

This does not audit, submit, invent reviews or infer a missing before-inventory.
All audit gates and the task's committed submission must already be satisfied.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(plan_path, note_id, before_path):
    plan = read(plan_path)
    logs = plan['execution_log']
    if [x['note_id'] for x in logs] != plan['notes'][:len(logs)]:
        raise ValueError('existing execution log is not the required ordered prefix')
    if len(logs) >= len(plan['notes']) or plan['notes'][len(logs)] != note_id:
        raise ValueError('only the next campaign note may be recorded')
    tasks = [read(p) for p in (ROOT / 'tasks').rglob('*.json')]
    task = next(x for x in tasks if x.get('note_id') == note_id)
    if task['status'] != 'done' or task['run'] != plan['boss_run']:
        raise ValueError('the actual task must already be submitted under this RUN')
    project = ROOT / task['workspace'] / 'project'
    completion = task['completion']
    for relative, expected in completion['files'].items():
        if sha(ROOT / relative) != expected:
            raise ValueError('submitted file bytes changed: ' + relative)
    report, ledger, participants = (read(project / name) for name in
        ['audit-report.json', 'ledger.json', 'audit/campaign/participants.json'])
    if (report['audit_pass'] is not True or report['content_resolved'] is not True or
        report['unresolved_count'] != 0 or
        report['snapshot_sha256'] != completion['snapshot_sha256']):
        raise ValueError('the current actual report does not satisfy completion')
    agents = [x['id'] for x in participants['subagents']]
    if (len(agents) != 3 or len(set(agents)) != 3 or len(ledger['final_rounds']) != 3 or
        set(agents) != {x['reviewer_id'] for x in ledger['final_rounds']}):
        raise ValueError('three actual participants and their three final reviews are required')
    prior_agents = {a for item in logs for a in item['subagents']}
    if prior_agents.intersection(agents):
        raise ValueError('a subagent identity was reused between notes')
    if participants['model'] != 'gpt-6.2-sol' or participants['reasoning_effort'] != 'max':
        raise ValueError('agent configuration differs from the user instruction')
    if participants['run'] != plan['boss_run'] or participants['note_id'] != note_id:
        raise ValueError('participant registration belongs to another note/RUN')
    before = read(before_path)
    if before['note_id'] != note_id:
        raise ValueError('the before-inventory belongs to another note')
    keys = ['source_units', 'target_units', 'recoveries', 'issues',
            'page_checks', 'region_checks', 'final_rounds']
    counts = {key: len(ledger[key]) for key in keys}
    current_commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                    capture_output=True, text=True, check=True).stdout.strip()
    item = {'note_id': note_id, 'run': plan['boss_run'], 'subagents': agents,
            'model': participants['model'], 'reasoning_effort': participants['reasoning_effort'],
            'review_protocol': ledger['review_policy']['mode'],
            'record_counts_before': before['record_counts'], 'record_counts_after': counts,
            'before_inventory': str(before_path.relative_to(ROOT)),
            'before_inventory_sha256': sha(before_path),
            'unresolved_before': before['unresolved_count'], 'unresolved_after': 0,
            'audit_pass': True, 'content_resolved': True,
            'snapshot_sha256': completion['snapshot_sha256'],
            'body_sha256': {name: sha(project / name) for name in
                           ['source-transcript.md', 'study-notes.md']},
            'audit_report': str((project / 'audit-report.json').relative_to(ROOT)),
            'submission_commit': current_commit, 'completed': True,
            'recorded_at': datetime.now(timezone.utc).isoformat()}
    logs.append(item)
    write(plan_path, plan)
    state_path = ROOT / 'work' / plan['boss_run'] / 'checkpoint.json'
    state = read(state_path)
    state['active_notes'] = []
    state['completed_notes'] = [x['note_id'] for x in logs]
    state['current_note'] = None
    state['current_status'] = 'completed_note_recorded'
    state['current_counts'] = counts
    state['current_snapshot_sha256'] = completion['snapshot_sha256']
    state['next_action'] = ('Claim ' + plan['notes'][len(logs)] + ' and create three new agents for that note only.'
                            if len(logs) < len(plan['notes']) else 'Run the complete campaign validator.')
    write(state_path, state)
    print(json.dumps(item, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--note', required=True)
    parser.add_argument('--before', type=Path, required=True)
    args = parser.parse_args()
    record(args.plan.resolve(), args.note, args.before.resolve())
