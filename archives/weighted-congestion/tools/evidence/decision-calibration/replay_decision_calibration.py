#!/usr/bin/env python3
"""Replay preserved calibration/repair/recovery programs to a NEW directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / 'original'
PREFIX = 'tests/audits/weighted_congestion/decision_methods/'
JOBS = {
    'calibration': ('calibration_audit.py', 'calibration_audit.json'),
    'repair': ('repair_audit.py', 'repair_audit.json'),
    'recovery': ('recovery_scope_audit.py', 'recovery_scope_audit.json'),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(a, b, path='$'):
    if type(a) != type(b):
        return [{'path': path, 'frozen': a, 'replay': b}]
    if isinstance(a, dict):
        out = []
        for key in sorted(a.keys() | b.keys()):
            if key not in a or key not in b:
                out.append({'path': path + '.' + key, 'frozen': a.get(key), 'replay': b.get(key),
                            'missing_from': 'frozen' if key not in a else 'replay'})
            else:
                out += differences(a[key], b[key], path + '.' + key)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [{'path': path, 'frozen': a, 'replay': b}]
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in differences(x, y, path + f'[{i}]')]
    return [] if a == b else [{'path': path, 'frozen': a, 'replay': b}]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', nargs='+', choices=list(JOBS), default=list(JOBS))
    parser.add_argument('--output-dir', type=Path, default=HERE / 'replay-new')
    args = parser.parse_args()
    required = [ORIGINAL / PREFIX / JOBS[key][0] for key in args.only]
    if 'recovery' in args.only:
        required.append(ORIGINAL / 'history/source/notes/weighted_congestion/structural_view_and_positive_results_reference.md')
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        parser.error('Missing dependencies; no audit started: ' + ', '.join(missing))
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    records, comparisons = [], []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_NO_LAZY_FETCH='1')
    for key in args.only:
        script, frozen_name = JOBS[key]
        target = out / frozen_name
        command = [sys.executable, PREFIX + script, '--output', str(target)]
        started = time.monotonic()
        result = subprocess.run(command, cwd=ORIGINAL, env=env, capture_output=True, text=True)
        (out / (script + '.stdout.txt')).write_text(result.stdout)
        (out / (script + '.stderr.txt')).write_text(result.stderr)
        records.append({'name': key, 'command': command, 'cwd': str(ORIGINAL),
                        'exit_code': result.returncode, 'seconds': time.monotonic() - started,
                        'source_sha256': sha(ORIGINAL / PREFIX / script),
                        'output': str(target), 'output_sha256': sha(target) if target.exists() else None})
        (out / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
        if result.returncode:
            raise RuntimeError(f'{key}: exit {result.returncode}; see saved stderr')
        frozen = ORIGINAL / 'evidence/runs/weighted_congestion/decision_methods' / frozen_name
        changes = differences(json.loads(frozen.read_text()), json.loads(target.read_text()))
        comparisons.append({'name': key, 'frozen': str(frozen), 'all_differences': changes,
                            'all_fields_exactly_equal': not changes})
        (out / 'comparison.json').write_text(json.dumps(comparisons, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'name': key, 'exit': 0, 'all_field_differences': len(changes)}), flush=True)
    assert all(row['all_fields_exactly_equal'] for row in comparisons), 'Inspect complete saved differences'


if __name__ == '__main__':
    main()
