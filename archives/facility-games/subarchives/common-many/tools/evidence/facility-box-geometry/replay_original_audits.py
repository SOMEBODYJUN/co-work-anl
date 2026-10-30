#!/usr/bin/env python3
"""Run the seven preserved box-geometry audits once into a fresh directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / 'original'
NAMES = ('kfac_box_lexmax', 'kfac_converging_four_moves',
         'kfac_converging_path', 'kfac_depth_three_box', 'kfac_height_two',
         'kfac_star_edges', 'kfac_path_edges')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--only', nargs='+', choices=NAMES, default=list(NAMES))
    ap.add_argument('--output-dir', type=Path, default=HERE / 'replay-new')
    args = ap.parse_args()
    required = [ORIGINAL / 'tests/audits' / (name + '.py') for name in args.only]
    fixture = {'kfac_converging_four_moves': 'greedy_converging_four_moves.json',
               'kfac_star_edges': 'greedy_star_edges.json'}
    required += [ORIGINAL / 'examples/multi_facility' / fixture[name]
                 for name in args.only if name in fixture]
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        ap.error('Missing saved dependencies: ' + ', '.join(missing))
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    records = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for name in args.only:
        relative = 'tests/audits/' + name + '.py'
        script = ORIGINAL / relative
        command = [sys.executable, relative]
        started = time.monotonic()
        result = subprocess.run(command, cwd=ORIGINAL, env=env,
                                capture_output=True, text=True)
        stdout, stderr = out / (name + '.stdout.txt'), out / (name + '.stderr.txt')
        stdout.write_text(result.stdout)
        stderr.write_text(result.stderr)
        records.append({'name': name, 'command': command, 'cwd': str(ORIGINAL),
                        'exit_code': result.returncode, 'seconds': time.monotonic() - started,
                        'source_sha256': sha(script), 'stdout_sha256': sha(stdout),
                        'stderr_sha256': sha(stderr), 'python': platform.python_version()})
        (out / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
        print(json.dumps({'name': name, 'exit_code': result.returncode}), flush=True)
    if any(r['exit_code'] for r in records):
        raise SystemExit('At least one original audit failed; inspect preserved stderr.')


if __name__ == '__main__':
    main()
