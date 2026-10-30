#!/usr/bin/env python3
"""Replay preserved sources in a fresh external snapshot, with immutable logs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--git-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    evidence, out = args.evidence.resolve(), args.output_dir.resolve()
    assert args.git_dir.is_dir(), 'Read-only Git metadata location must exist'
    out.mkdir(parents=True, exist_ok=False)
    snapshot = out / 'original'
    shutil.copytree(evidence / 'original', snapshot)
    for item in json.loads((evidence / 'provenance.json').read_text()):
        # Later comparison-only dependencies are kept under related/, not
        # executed. The actual original/ snapshot remains the same 20 files.
        if not (evidence / 'original' / item['path']).is_file():
            continue
        assert sha(snapshot / item['path']) == item['sha256']
    helper = Path(__file__).resolve().with_name('extract_adaptive_once.py')
    shutil.copyfile(helper, out / helper.name)
    (out / 'tmp').mkdir()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_NO_LAZY_FETCH='1',
               GIT_DIR=str(args.git_dir.resolve()), GIT_WORK_TREE=str(snapshot),
               TMPDIR=str(out / 'tmp'))
    jobs = [
        ('complement', [sys.executable, 'tests/audits/kfac_complement_reduction.py',
                        '--output', str(out / 'complement-replay.json')],
         'tests/audits/kfac_complement_reduction.py'),
        ('adaptive', [sys.executable, str(out / helper.name), '--script',
                      'tests/audits/kfac_adaptive_reset.py', '--output',
                      str(out / 'adaptive-export.json')], 'tests/audits/kfac_adaptive_reset.py'),
        ('frozen', [sys.executable, 'tests/audits/kfac_frozen_overload.py'],
         'tests/audits/kfac_frozen_overload.py'),
        ('tests', [sys.executable, '-m', 'tests.test_complement_reduction'],
         'tests/test_complement_reduction.py'),
    ]
    records = []
    for name, command, script in jobs:
        started = time.monotonic()
        result = subprocess.run(command, cwd=snapshot, env=env, text=True, capture_output=True)
        stdout, stderr = out / (name + '.stdout.txt'), out / (name + '.stderr.txt')
        stdout.write_text(result.stdout)
        stderr.write_text(result.stderr)
        records.append({'name': name, 'command': command, 'cwd': str(snapshot),
                        'exit_code': result.returncode, 'seconds': time.monotonic() - started,
                        'source_sha256': sha(snapshot / script),
                        'stdout_sha256': sha(stdout), 'stderr_sha256': sha(stderr),
                        'environment': {k: env[k] for k in ('PYTHONDONTWRITEBYTECODE',
                                                            'GIT_NO_LAZY_FETCH', 'GIT_DIR',
                                                            'GIT_WORK_TREE', 'TMPDIR')}})
        (out / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
        print(json.dumps({'name': name, 'exit_code': result.returncode}), flush=True)
    assert all(r['exit_code'] == 0 for r in records), 'Inspect preserved failure logs'

if __name__ == '__main__':
    main()
