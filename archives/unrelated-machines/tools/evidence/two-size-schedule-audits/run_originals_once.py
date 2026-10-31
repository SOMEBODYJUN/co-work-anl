#!/usr/bin/env python3
"""Run each of the three unchanged source entrypoints once in a fresh cwd."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys
import time

here = Path(__file__).resolve().parent
cases = {
    'count': 'divisible_two_size_neutral_repair.py',
    'labels': 'divisible_two_size_neutral_independent.py',
    'fixed': 'fixed_work_convex_local_minimum.py',
}
runs = here / 'runs'
for name in cases:
    if (runs / (name + '-001')).exists():
        raise SystemExit('Refuse a repeated run: ' + name)
assert sys.flags.optimize == 0
for name, filename in cases.items():
    source = here / 'original' / filename
    run_dir = runs / (name + '-001')
    run_dir.mkdir(parents=True, exist_ok=False)
    assert not list(run_dir.iterdir())
    command = [sys.executable, str(source)]
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    clock = time.monotonic()
    with (run_dir / 'stdout.txt').open('xb') as out, (run_dir / 'stderr.txt').open('xb') as err:
        result = subprocess.run(command, cwd=run_dir, stdout=out, stderr=err,
                                timeout=300, check=False)
    duration = time.monotonic() - clock
    meta = {
        'case': name, 'command': command, 'cwd': str(run_dir),
        'initial_directory_empty': True, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'python_version': sys.version, 'optimization_level': sys.flags.optimize,
        'started_at': start, 'duration_seconds': duration,
        'exit_code': result.returncode, 'entrypoint_invocations': 1,
        'input': 'No CLI arguments or external input; original hardcoded parameter sets only.',
        'stdout_sha256': hashlib.sha256((run_dir / 'stdout.txt').read_bytes()).hexdigest(),
        'stderr_bytes': (run_dir / 'stderr.txt').stat().st_size,
    }
    with (run_dir / 'run.json').open('x') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({'case': name, 'exit_code': result.returncode,
                      'seconds': duration, 'stderr_bytes': meta['stderr_bytes']}), flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
