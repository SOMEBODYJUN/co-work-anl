"""Run an explicitly registered command and retain a reproducible result receipt."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

from curation import _safe_path, _write_json


def run(root, name, output):
    manifest_path = root / 'research/experiments.json'
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('schema') != 1 or name not in manifest['experiments']:
        raise ValueError('Unknown registered experiment')
    experiment = manifest['experiments'][name]
    command = experiment['command']
    if not isinstance(command, list) or not command or any(not isinstance(x, str) for x in command):
        raise ValueError('Command must be an argument list, never a shell string')
    if type(experiment['timeout_seconds']) is not int or not 1 <= experiment['timeout_seconds'] <= 900:
        raise ValueError('Experiment timeout must be 1..900 seconds')
    command = [sys.executable if arg == '{python}' else arg for arg in command]
    env = {k: v for k, v in os.environ.items() if not any(x in k.upper() for x in ('TOKEN', 'SECRET', 'PASSWORD', 'ASKPASS'))}
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONHASHSEED'] = str(experiment.get('seed') or 0)
    start = time.monotonic()
    status = 'completed'
    try:
        completed = subprocess.run(command, cwd=root, env=env, capture_output=True, timeout=experiment['timeout_seconds'])
        code, stdout, stderr = completed.returncode, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as exc:
        status = 'timeout'; code = None; stdout = exc.stdout or b''; stderr = exc.stderr or b''
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True)
    dirty = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=root, capture_output=True, text=True)
    result = {'experiment': name, 'status': status, 'exit_code': code,
              'at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'elapsed_seconds': round(time.monotonic() - start, 3),
              'commit': head.stdout.strip() if head.returncode == 0 else None, 'tracked_tree_dirty': bool(dirty.stdout.strip()),
              'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
              'command_file_sha256': {arg: hashlib.sha256((root / arg).read_bytes()).hexdigest() for arg in experiment['command'] if (root / arg).is_file()},
              'python': platform.python_version(), 'platform': platform.platform(), 'spec': experiment,
              'stdout': stdout.decode(errors='replace'), 'stderr': stderr.decode(errors='replace'),
              'interpretation': 'Command output only; inspect the declared finite domain and proof obligations before any mathematical conclusion.'}
    _write_json(_safe_path(root, output), result)
    return code == 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('experiment'); parser.add_argument('--out', required=True)
    args = parser.parse_args()
    try: success = run(Path(__file__).resolve().parents[1], args.experiment, args.out)
    except (ValueError, OSError, KeyError) as exc: raise SystemExit(str(exc))
    print('Receipt:', args.out)
    raise SystemExit(0 if success else 1)
