#!/usr/bin/env python3
"""Replay six preserved exact audits into a new directory; retain every JSON difference."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / 'original'
PREFIX = 'tests/audits/weighted_congestion/cyclic_clone/'
FROZEN = ORIGINAL / 'evidence/runs/weighted_congestion/cyclic_clone'
JOBS = [
    ('verify_class_fronts.py', 'class_fronts.json', []),
    ('independent_class_fronts.py', 'independent_class_fronts.json', []),
    ('verify_class_internal_clock_compiler_obstruction.py', 'class_internal_clock_compiler_obstruction_author.json',
     ['--input', 'examples/weighted_congestion/class_internal_clock_compiler_obstruction.json']),
    ('independent_class_internal_clock_compiler.py', 'class_internal_clock_compiler_obstruction_independent.json', []),
    ('verify_front_allstate_compiler.py', 'front_allstate_compiler_author.json',
     ['--input', 'examples/weighted_congestion/class_front_allstate_compiler.json']),
    ('independent_front_allstate_compiler.py', 'front_allstate_compiler_independent.json',
     ['--input', 'examples/weighted_congestion/class_front_allstate_compiler.json']),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(a, b, path='$'):
    if type(a) is not type(b):
        return [{'path': path, 'frozen': a, 'replay': b}]
    if isinstance(a, dict):
        out = []
        for key in sorted(a.keys() | b.keys()):
            if key not in a or key not in b:
                out.append({'path': path + '.' + key, 'frozen': a.get(key), 'replay': b.get(key),
                            'missing_from': 'frozen' if key not in a else 'replay'})
            else:
                out.extend(differences(a[key], b[key], path + '.' + key))
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [{'path': path, 'frozen': a, 'replay': b}]
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in differences(x, y, path + f'[{i}]')]
    return [] if a == b else [{'path': path, 'frozen': a, 'replay': b}]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=HERE / 'replay-new')
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    runs, comparisons = [], []
    for script, frozen, extra in JOBS:
        cmd = [sys.executable, PREFIX + script, *extra]
        started = time.monotonic()
        proc = subprocess.run(cmd, cwd=ORIGINAL, capture_output=True, text=True, check=False)
        stdout = output / (script.removesuffix('.py') + '.json')
        stdout.write_text(proc.stdout)
        (output / (script + '.stderr.txt')).write_text(proc.stderr)
        runs.append({'script': PREFIX + script, 'command': cmd, 'cwd': str(ORIGINAL),
                     'exit_code': proc.returncode, 'seconds': time.monotonic() - started,
                     'source_sha256': digest(ORIGINAL / PREFIX / script),
                     'stdout': str(stdout), 'stdout_sha256': digest(stdout)})
        if proc.returncode:
            raise RuntimeError(f'{script}: exit {proc.returncode}; see saved stderr')
        old = json.loads((FROZEN / frozen).read_text())
        wrapper = {k: v for k, v in old.items() if k != 'result'} if 'result' in old else None
        if 'result' in old:
            old = old['result']
        diff = differences(old, json.loads(proc.stdout))
        metadata = {'$.command', '$.input', '$.input_path', '$.fixture.input', '$.python'}
        math_diff = [d for d in diff if not any(d['path'] == key or d['path'].startswith(key + '[') for key in metadata)]
        comparisons.append({'script': script, 'frozen': str(FROZEN / frozen),
                            'frozen_wrapper': wrapper, 'differences': diff,
                            'mathematical_differences': math_diff,
                            'mathematics_exactly_equal': not math_diff})
        print(json.dumps({'script': script, 'exit': proc.returncode,
                          'differences': len(diff), 'mathematical_differences': len(math_diff)}), flush=True)
    (output / 'manifest.json').write_text(json.dumps({'python': platform.python_version(), 'runs': runs}, indent=2) + '\n')
    (output / 'comparison.json').write_text(json.dumps(comparisons, ensure_ascii=False, indent=2) + '\n')
    assert all(x['mathematics_exactly_equal'] for x in comparisons), 'Inspect complete saved differences'


if __name__ == '__main__':
    main()
