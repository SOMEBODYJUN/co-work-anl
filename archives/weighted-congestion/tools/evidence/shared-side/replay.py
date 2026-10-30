#!/usr/bin/env python3
"""Replay preserved exact audits; compare every JSON field and every saved case.

The source proofs, not these finite executions, carry the real-parameter claims.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT / 'original'
RUNS = [
    ('verify_shared_side_truncation', 'author'),
    ('independent_shared_side_truncation', 'independent'),
    ('independent_shared_side_budget', 'budget_boundaries'),
    ('verify_multisource_shared_side', 'multisource_author'),
    ('independent_multisource_shared_side', 'multisource_independent'),
    ('verify_multisource_forcing_target_tradeoff', 'forcing_target_author'),
    ('independent_multisource_force_tradeoff', 'multisource_force_tradeoff_independent'),
    ('verify_multisource_forcing_exact_threshold', 'forcing_exact_threshold_author'),
    ('independent_multisource_force_increment', 'multisource_force_increment_independent'),
    ('verify_multisource_reset_increment', 'reset_increment_author'),
    ('independent_multisource_reset_increment', 'reset_increment_independent'),
    ('verify_heterogeneous_sorted_side', 'heterogeneous_author'),
    ('independent_heterogeneous_sorted_side', 'heterogeneous_independent'),
    ('verify_heterogeneous_reset_increment', 'heterogeneous_reset_increment_author'),
    ('independent_heterogeneous_reset_increment', 'heterogeneous_reset_increment_independent'),
]

def differences(old, new, path=''):
    if type(old) is not type(new):
        return [{'path': path, 'old': old, 'new': new}]
    if isinstance(old, dict):
        answer = []
        for key in sorted(old.keys() | new.keys()):
            name = f'{path}/{key}'
            if key not in old or key not in new:
                answer.append({'path': name, 'old': old.get(key), 'new': new.get(key)})
            else:
                answer.extend(differences(old[key], new[key], name))
        return answer
    if isinstance(old, list):
        if len(old) != len(new):
            return [{'path': path + '/length', 'old': len(old), 'new': len(new)}]
        return [diff for i, pair in enumerate(zip(old, new))
                for diff in differences(*pair, f'{path}/{i}')]
    return [] if old == new else [{'path': path, 'old': old, 'new': new}]

def run(pair):
    script, report = pair
    path = Path('tests/audits/weighted_congestion') / (script + '.py')
    started = time.monotonic()
    result = subprocess.run([sys.executable, '-B', str(path)], cwd=ORIGINAL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    output = ROOT / 'replay' / (report + '.json')
    output.write_bytes(result.stdout)
    if result.stderr:
        output.with_suffix('.stderr.txt').write_bytes(result.stderr)
    row = {'script': str(path), 'returncode': result.returncode,
           'seconds': round(time.monotonic() - started, 3),
           'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
           'source_sha256': hashlib.sha256((ORIGINAL / path).read_bytes()).hexdigest()}
    if result.returncode == 0:
        frozen_path = ORIGINAL / 'evidence/runs/weighted_congestion/shared_side_truncation' / (report + '.json')
        frozen = json.loads(frozen_path.read_text())
        fresh = json.loads(result.stdout)
        diff = differences(frozen, fresh)
        row['differences'] = diff
        allowed = {'/python', '/python_version', '/command'}
        row['all_mathematical_and_input_fields_equal'] = all(d['path'] in allowed for d in diff)
        row['byte_equal'] = frozen_path.read_bytes() == result.stdout
        row['summary'] = fresh.get('summary', fresh.get('counts', fresh.get('coverage',
                          {k:v for k,v in fresh.items() if k not in ('cases','results')})))
    return row

def main():
    (ROOT / 'replay').mkdir(exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(run, pair) for pair in RUNS]):
            row = future.result()
            rows.append(row)
            print(row['script'], row['returncode'], row.get('all_mathematical_and_input_fields_equal'), flush=True)
    rows.sort(key=lambda row: row['script'])
    result = {'python': sys.version, 'runs': rows,
              'all_passed': all(row['returncode'] == 0 and row.get('all_mathematical_and_input_fields_equal') for row in rows)}
    (ROOT / 'replay' / 'comparison.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    assert result['all_passed'], 'Inspect exact differences and stderr; do not hide changed evidence.'

if __name__ == '__main__':
    main()
