"""Replay three original rational audits and check their preserved inputs.

The eight-client audits hard-code the game/policy; checking that those constants
match the separately preserved example and certificate is part of this wrapper.
No optimizer or repository solver is used. This wrapper is a replay/integration
check, not a claim of a new independent mathematical review.
"""
import argparse
import hashlib
import importlib.util
import json
from itertools import product
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'source-manifest.json').read_text())
    for row in manifest['original_files']:
        data = (ROOT / row['path']).read_bytes()
        assert len(data) == row['size']
        assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']

    main8 = load_module('cce_eight_original', ROOT / 'source/tests/audits/customer_attraction_eight_cce.py')
    independent8 = load_module('cce_eight_original_independent', ROOT / 'source/tests/audits/customer_attraction_eight_cce_independent.py')
    instance = json.loads((ROOT / 'source/examples/customer_attraction/eight_cce_welfare_gap.json').read_text())
    certificate = json.loads((ROOT / 'source/evidence/certificates/customer_attraction/eight_cce_welfare_gap.json').read_text())
    clients = [frozenset(row['topics']) for row in instance['customers'] for _ in range(row['multiplicity'])]
    key = lambda c: tuple(sorted(c))
    assert instance['players'] == 3 and len(instance['topics']) == 4
    assert sorted(clients, key=key) == sorted(map(frozenset, main8.CUSTOMERS), key=key)
    assert sorted(clients, key=key) == sorted(independent8.CLIENTS, key=key)
    policy = {tuple(row['history']): row['action'] for row in certificate['actions']}
    histories = [h for d in range(3) for h in product(range(4), repeat=d)]
    assert len(policy) == len(certificate['actions']) == len(histories) == 21
    assert set(policy) == set(histories)
    assert all(policy[h] == main8.action(h) == independent8.action(h) for h in histories)
    path = ()
    while len(path) < 3:
        path += (policy[path],)
    assert [path.count(a) for a in range(4)] == certificate['terminal_counts'] == [1, 2, 0, 0]

    tasks = [
        ('customer_attraction_eight_cce.py', 'replay-eight-main.json', False),
        ('customer_attraction_eight_cce_independent.py', 'replay-eight-independent.json', True),
        ('customer_attraction_worst_cce_welfare.py', 'replay-thirteen-independent.json', True),
    ]
    rows = []
    with tempfile.TemporaryDirectory() as temporary:
        for script, expected, option in tasks:
            output = Path(temporary) / expected
            command = [sys.executable, str(ROOT / 'source/tests/audits' / script)]
            command += ['--output', str(output)] if option else [str(output)]
            subprocess.run(command, check=True, capture_output=True, text=True)
            actual = json.loads(output.read_text())
            saved = json.loads((ROOT / expected).read_text())
            assert actual == saved, script
            frozen = next(x for x in manifest['replay_comparison'] if x['replay_path'] == expected)
            assert hashlib.sha256((ROOT / expected).read_bytes()).hexdigest() == frozen['replay_sha256']
            rows.append({'script': script, 'full_report_equal_to_saved_replay': True,
                         'saved_replay_previously_equal_to_frozen_source': frozen['structurally_equal'],
                         'frozen_source_id': frozen['frozen_id']})
    report = {'status': 'passed', 'original_byte_files': len(manifest['original_files']),
              'eight_client_input_and_all_21_policy_rows_match_both_audits': True,
              'eight_client_terminal_counts_match_certificate': True,
              'audit_replays': rows,
              'scope': 'Original audit replay plus input integration; not new external review, minimality, or a six-player counterexample.'}
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        with args.output.open('x') as target:
            target.write(rendered)
    print(rendered, end='')


if __name__ == '__main__':
    main()
