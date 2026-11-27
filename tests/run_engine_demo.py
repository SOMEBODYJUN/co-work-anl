#!/usr/bin/env python3
"""Exercise the actual CLI through first and incremental engineering cycles.

All numeric inputs and conclusions are explicit synthetic fixtures. This is an
engineering replay, not the substantive economic research report.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

REPO = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = args.out.resolve()
    if root.exists() and any(root.iterdir()):
        raise SystemExit('Use a new empty output directory to preserve earlier receipts')
    root.mkdir(parents=True, exist_ok=True)
    transcript = []

    def call(*words, expected=0):
        cmd = [sys.executable, str(REPO / 'crisis.py'), '--workspace', str(root), *words]
        run = subprocess.run(cmd, text=True, capture_output=True, cwd=REPO)
        record = {'args': list(words), 'exit_code': run.returncode}
        try:
            result = json.loads(run.stdout if run.returncode == 0 else run.stderr)
        except ValueError:
            raise RuntimeError(run.stdout + run.stderr)
        record['result'] = result
        transcript.append(record)
        if run.returncode != expected:
            raise RuntimeError(f'Unexpected CLI exit {run.returncode}: {result}')
        return result

    def write(name, content):
        file = root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps(content, ensure_ascii=False, indent=2) if not isinstance(content, str) else content)
        return str(file)

    def source(value):
        return {'id': 'F1', 'kind': 'fact', 'url': 'fixture://engineering/income',
                'source_family': 'synthetic-engineering-fixture', 'observation_period': 'synthetic-month-1',
                'published_at': '2020-01-01', 'event_id': 'engineering-fixture',
                'text': f'SYNTHETIC ENGINEERING TEST ONLY: monthly income assumption {value}',
                'targets': ['J1'] if value == 9000 else [],
                'impact_note': 'First synthetic fixture, before graph construction'}

    def phases(phase_ids, cycle):
        for phase in phase_ids:
            name = f'engineering_steps/cycle{cycle}/{phase}.md'
            write(name, f'# Engineering replay: {phase}\n\nSynthetic fixture cycle {cycle}; actual CLI handler executed.\n')
            call('stage', '--id', phase, '--files', name, '--note', 'Synthetic engineering replay artifact')

    def accept_proposal(pid, target, old, new, revision=1, replacement=None):
        proposal = {'id': pid, 'target': target, 'base_revision': revision, 'action': 'replace',
                    'old_statement': old, 'new_statement': new, 'new_evidence': ['F1'],
                    'reason': 'The explicit synthetic income assumption changed; recompute the dependent fixture conclusion'}
        if replacement is not None:
            proposal['replacement'] = replacement
        call('proposal', '--file', write(f'engineering_steps/{pid}.json', proposal))
        call('proposal-review', '--id', pid, '--verdict', 'pass', '--reviewer', 'engineering-reviewer',
             '--note', 'Inspected the proposed fixture delta and the referenced current source')
        call('apply', '--id', pid)

    first = call('init')
    call('ingest', '--file', write('engineering_steps/source1.json', source(10000)))
    call('search-log', '--file', write('engineering_steps/search.json', {
        'query': 'synthetic engineering fixture income', 'topic': 'engineering', 'period': 'synthetic-month-1',
        'results': [], 'note': 'Deliberate zero-result fixture, no network research represented'}))
    reused = call('search-plan', '--query', 'synthetic engineering fixture income', '--topic', 'engineering', '--period', 'synthetic-month-1')
    assert reused['decision'] == 'reuse'
    edge = {'id': 'H1', 'tails': ['J1', 'F1'], 'head': 'J2', 'mode': 'ALL', 'conditions': [],
            'mechanism': 'Joint synthetic income premise and its fixture interpretation',
            'counterevidence': [], 'falsifier': 'Synthetic fixture assumptions change', 'lag': 'One fixture step'}
    call('graph-put', '--file', write('engineering_steps/graph.json', {
        'nodes': [{'id': 'J1', 'kind': 'judgment', 'statement': 'Synthetic income assumption is 10000', 'evidence': ['F1']},
                  {'id': 'J2', 'kind': 'judgment', 'statement': 'Recompute synthetic household outcome from income 10000', 'evidence': []}],
        'edges': [edge]}))
    write('formal/engineering_result.md', '# Engineering replay only\n\nSynthetic monthly income assumption: 10000.\n')
    phases(first['stages'], 1)
    call('review', '--verdict', 'pass', '--files', 'formal/engineering_result.md', '--note', 'First engineering cycle reviewed', '--reviewer', 'engineering-reviewer')
    release1 = call('release', '--files', 'formal/engineering_result.md', '--judgment', 'Engineering fixture 10000; no macroeconomic conclusion')
    update = call('init', '--mode', 'update')
    call('ingest', '--file', write('engineering_steps/source2.json', source(9000)))
    pending = call('graph-status')
    assert set(pending['unresolved']) == {'J1', 'J2'}
    accept_proposal('P-J1', 'J1', 'Synthetic income assumption is 10000', 'Synthetic income assumption is 9000')
    accept_proposal('P-H1', 'H1', edge['mechanism'], '', replacement={**edge, 'mechanism': 'Joint synthetic income 9000 and its revised interpretation'})
    accept_proposal('P-J2', 'J2', 'Recompute synthetic household outcome from income 10000', 'Recompute synthetic household outcome from income 9000')
    write('formal/engineering_result.md', '# Engineering replay only\n\nSynthetic monthly income assumption: 9000.\n')
    phases(update['stages'], 2)
    call('review', '--verdict', 'pass', '--files', 'formal/engineering_result.md', '--note', 'Second engineering cycle reviewed', '--reviewer', 'engineering-reviewer')
    release2 = call('release', '--files', 'formal/engineering_result.md', '--judgment', 'Engineering fixture 9000; no macroeconomic conclusion')
    call('review', '--verdict', 'reject', '--note', 'Deliberate engineering refusal test')
    call('release', '--files', 'formal/engineering_result.md', '--judgment', 'Must be rejected', expected=2)
    call('review', '--verdict', 'pass', '--files', 'formal/engineering_result.md', '--note', 'Rechecked fixture after deliberate refusal', '--reviewer', 'engineering-reviewer')
    final = call('release', '--files', 'formal/engineering_result.md', '--judgment', 'Engineering replay complete: fixture 9000')
    write('engineering_steps/cli_transcript.json', transcript)
    summary = {'engineering_only': True, 'first_cycle': release1['cycle'], 'update_cycle': release2['cycle'],
               'first_stages': len(first['stages']), 'update_stages': len(update['stages']),
               'search_reused': True, 'transitive_invalidation': pending['unresolved'],
               'proposal_reviews': 3, 'refusal_blocked_release': True, 'release': final}
    write('engineering_steps/demo_summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
