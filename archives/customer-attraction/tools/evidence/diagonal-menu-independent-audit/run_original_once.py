#!/usr/bin/env python3
"""One unchanged original CLI call; hashes and output identity only, no row reimplementation."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

def digest(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--input', type=Path, required=True)
    ap.add_argument('--expected', type=Path, required=True)
    ap.add_argument('--work', type=Path, required=True)
    args = ap.parse_args()
    work = args.work.resolve()
    if (work / 'execution.json').exists():
        raise RuntimeError('Existing event: refusing an accidental repeat')
    expected_hashes = {
        'source': (1516, '77d3111966fa0274781c7fe811378f7d5d234d8ab6d292c1f68e6cc6cdaff1d6'),
        'input': (34584, 'ce1f9d8b1036256b7e40e1eb5c990fdcc4f33c7fed3f2aa796bdf8245b9d0c4f'),
        'expected': (480, 'fd11ff0aac0ced093a383a5313df9b6201ac60aae8220177d5e7c672dea09261'),
    }
    originals = {k: getattr(args, k).resolve() for k in expected_hashes}
    before = {k: digest(p) for k, p in originals.items()}
    for k, pair in expected_hashes.items():
        assert (before[k]['bytes'], before[k]['sha256']) == pair
    root = work / 'runtime'
    source = root / 'round3_independent' / 'audit_diagonal_menu.py'
    data = root / 'next_credible' / 'enhanced_2396_exact_obstruction.json'
    source.parent.mkdir(parents=True, exist_ok=True)
    data.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(originals['source'], source)
    shutil.copyfile(originals['input'], data)
    runtime_before = {'source': digest(source), 'input': digest(data)}
    env = os.environ.copy()
    removed_optimize = 'PYTHONOPTIMIZE' in env
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    argv = [sys.executable, str(source)]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    start = time.perf_counter()
    process = subprocess.run(argv, cwd=source.parent, env=env, capture_output=True)
    elapsed = time.perf_counter() - start
    (work / 'stdout.txt').write_bytes(process.stdout)
    (work / 'stderr.txt').write_bytes(process.stderr)
    output = source.parent / 'audit_diagonal_menu.json'
    if output.exists():
        shutil.copyfile(output, work / 'audit_diagonal_menu.json')
    after = {k: digest(p) for k, p in originals.items()}
    runtime_after = {'source': digest(source), 'input': digest(data)}
    event = {
        'kind': 'one unmodified original normal CLI execution; no profile or trace wrapper',
        'started_utc': started,
        'argv': argv,
        'cwd': str(source.parent),
        'python_version': sys.version,
        'elapsed_seconds': elapsed,
        'exit_code': process.returncode,
        'environment_changes': {'PYTHONOPTIMIZE_removed_if_present': removed_optimize,
                                'PYTHONDONTWRITEBYTECODE': '1'},
        'original_paths': {k: str(v) for k, v in originals.items()},
        'before': before, 'after': after,
        'runtime_before': runtime_before, 'runtime_after': runtime_after,
        'originals_unchanged': before == after,
        'runtime_code_and_input_unchanged': runtime_before == runtime_after,
        'stdout': digest(work / 'stdout.txt'), 'stderr': digest(work / 'stderr.txt'),
        'output': digest(output) if output.exists() else None,
        'output_equals_frozen_bytes': output.exists() and output.read_bytes() == originals['expected'].read_bytes(),
        'stdout_equals_frozen_bytes': process.stdout == originals['expected'].read_bytes(),
        'execution_scope': {
            'original_main_processes_launched': 1,
            'profile_or_trace': False,
            'input_atom_records': 38,
            'lp_solver_calls': 0,
            'spe_searches': 0,
            'random_searches': 0,
            'repeated_2396_or_1326_row_audits': 0,
            'new_independent_38_term_implementations': 0,
            'note': 'Scope from unchanged source and frozen input, not dynamic function instrumentation.'
        }
    }
    (work / 'execution.json').write_text(json.dumps(event, ensure_ascii=False, indent=2) + '\n')
    assert process.returncode == 0
    assert event['originals_unchanged'] and event['runtime_code_and_input_unchanged']
    assert event['output_equals_frozen_bytes'] and event['stdout_equals_frozen_bytes']
    assert not process.stderr
    print(json.dumps({'exit_code': process.returncode, 'elapsed_seconds': elapsed,
                      'output_equals_frozen_bytes': event['output_equals_frozen_bytes'],
                      'mathematical_pass_flag': json.loads(output.read_text())['passes_necessary_inequality']}, indent=2))

if __name__ == '__main__':
    main()
