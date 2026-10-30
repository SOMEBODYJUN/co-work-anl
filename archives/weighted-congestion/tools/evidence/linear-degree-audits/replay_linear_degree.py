#!/usr/bin/env python3
"""Replay preserved linear-family audits once into a NEW output directory."""
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
PREFIX = 'tests/audits/weighted_congestion/cyclic_clone/'
RUNS = [
    ('independent_linear_degree_sweep', 'linear_degree_sweep_independent.json'),
    ('independent_linear_degree_front', 'linear_degree_front_independent.json'),
    ('clean_attack_linear_degree', 'linear_degree_clean_attack.json'),
    ('independent_linear_degree_allphases', 'linear_degree_allphases_independent.json'),
    ('verify_linear_degree_front_cover', 'linear_degree_front_cover.json'),
    ('independent_multiclass_assembly', 'linear_degree_multiclass_assembly.json'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def diff(a, b, path='$'):
    if type(a) != type(b):
        return [{'path': path, 'frozen': a, 'replay': b}]
    if isinstance(a, dict):
        out = []
        for key in sorted(a.keys() | b.keys()):
            if key not in a or key not in b:
                out.append({'path': path + '.' + key, 'frozen': a.get(key), 'replay': b.get(key),
                            'missing_from': 'frozen' if key not in a else 'replay'})
            else:
                out.extend(diff(a[key], b[key], path + '.' + key))
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [{'path': path, 'frozen': a, 'replay': b}]
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in diff(x, y, path + f'[{i}]')]
    return [] if a == b else [{'path': path, 'frozen': a, 'replay': b}]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=HERE / 'replay-new')
    parser.add_argument('--only', nargs='+', choices=[name for name, _ in RUNS],
                        help='Run only named audits; useful for a previously missing dependency.')
    args = parser.parse_args()
    selected = [(name, frozen) for name, frozen in RUNS if args.only is None or name in args.only]
    required = [ORIGINAL / PREFIX / (name + '.py') for name, _ in selected]
    required.append(ORIGINAL / 'research/current/weighted_congestion/linear_degree_allstate_lower_bound.md')
    if any(name == 'verify_linear_degree_front_cover' for name, _ in selected):
        required.append(ORIGINAL / 'examples/weighted_congestion/cyclic_clone/linear_degree_front_audit.json')
    if any(name == 'independent_linear_degree_front' for name, _ in selected):
        required.append(ORIGINAL / PREFIX / 'independent_linear_degree_sweep.py')
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        parser.error('Missing dependencies; no audit started: ' + ', '.join(missing))
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    records, comparisons = [], []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for name, frozen in selected:
        script = PREFIX + name + '.py'
        target = out / (name + '.json')
        cmd = [sys.executable, script]
        author = name == 'verify_linear_degree_front_cover'
        if author:
            cmd += ['--input', 'examples/weighted_congestion/cyclic_clone/linear_degree_front_audit.json',
                    '--output', str(target)]
        started = time.monotonic()
        proc = subprocess.run(cmd, cwd=ORIGINAL, capture_output=True, text=True, env=env)
        (out / (name + '.stderr.txt')).write_text(proc.stderr)
        if author:
            (out / (name + '.stdout-summary.json')).write_text(proc.stdout)
        else:
            target.write_text(proc.stdout)
        records.append({'script': script, 'command': cmd, 'cwd': str(ORIGINAL),
                        'exit_code': proc.returncode, 'seconds': time.monotonic() - started,
                        'source_sha256': sha(ORIGINAL / script),
                        'output': str(target), 'output_sha256': sha(target) if target.exists() else None})
        (out / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
        if proc.returncode:
            raise RuntimeError(f'{script}: exit {proc.returncode}; saved stderr')
        old = json.loads((ORIGINAL / 'evidence/runs/weighted_congestion/cyclic_clone' / frozen).read_text())
        changes = diff(old, json.loads(target.read_text()))
        metadata_paths = {'$.command', '$.metadata.command', '$.metadata.source_path', '$.metadata.input_path',
                          '$.metadata.cwd', '$.metadata.repository_head'}
        mathematical = [d for d in changes if not any(
            d['path'] == p or d['path'].startswith(p + '[') for p in metadata_paths)]
        comparisons.append({'script': script, 'frozen': frozen, 'all_differences': changes,
                            'mathematical_differences': mathematical,
                            'mathematics_exactly_equal': not mathematical})
        (out / 'comparison.json').write_text(json.dumps(comparisons, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'script': name, 'exit': 0, 'differences': len(changes),
                          'mathematical_differences': len(mathematical)}), flush=True)
    assert all(c['mathematics_exactly_equal'] for c in comparisons), 'Inspect saved complete differences'


if __name__ == '__main__':
    main()
