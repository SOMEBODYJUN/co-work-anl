"""Replay either restored hard-coded original audit in a fresh external directory."""
from argparse import ArgumentParser
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ap = ArgumentParser()
ap.add_argument('--case', choices=['ancestor', 'degree'], required=True)
ap.add_argument('--run-dir', type=Path, required=True)
args = ap.parse_args()
root = Path(__file__).resolve().parent
manifest = json.loads((root / 'source-manifest.json').read_text())['rows']
names = {'ancestor': ('audit_ancestor_reset.py', 'ancestor_reset_exact.json'),
         'degree': ('audit_degree_two_independent.py', 'degree_two_independent_exact.json')}
program_name, report_name = names[args.case]
program_row = next(r for r in manifest if Path(r['path']).name == program_name)
report_row = next(r for r in manifest if Path(r['path']).name == report_name)
source = root / 'original' / program_row['path']
frozen = root / 'original' / report_row['path']
for p, row in [(source, program_row), (frozen, report_row)]:
    data = p.read_bytes()
    if len(data) != row['size'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('frozen input fingerprint mismatch')
if args.run_dir.exists():
    raise ValueError('run directory must not exist')
args.run_dir.mkdir(parents=True)
copied = args.run_dir / program_name
shutil.copyfile(source, copied)
env = os.environ.copy()
env['PYTHONOPTIMIZE'] = '0'
env['PYTHONDONTWRITEBYTECODE'] = '1'
command = [sys.executable, str(copied)]
started = time.monotonic()
result = subprocess.run(command, cwd=args.run_dir, env=env, capture_output=True)
elapsed = time.monotonic() - started
(args.run_dir / 'stdout.txt').write_bytes(result.stdout)
(args.run_dir / 'stderr.txt').write_bytes(result.stderr)
output = args.run_dir / report_name
event = {
    'case': args.case,
    'mode': 'one unchanged original entry, isolated new directory, no source import beforehand',
    'argv': command, 'cwd': str(args.run_dir),
    'python': sys.version, 'returncode': result.returncode,
    'wall_seconds': elapsed,
    'PYTHONOPTIMIZE': '0', 'PYTHONDONTWRITEBYTECODE': '1',
    'source_sha256': program_row['sha256'],
    'source_unchanged_after_run': copied.read_bytes() == source.read_bytes(),
    'frozen_report_sha256': report_row['sha256'],
    'output_exists': output.exists(),
    'original_entry_invocations': 1,
    'repository_solver_optimizer_random_author_degree_audit_calls': 0,
}
if output.exists():
    generated = output.read_bytes()
    event.update({'output_size': len(generated),
                  'output_sha256': hashlib.sha256(generated).hexdigest(),
                  'byte_identical_to_frozen_report': generated == frozen.read_bytes(),
                  'structured_identical_to_frozen_report': json.loads(generated) == json.loads(frozen.read_bytes()),
                  'stdout_identical_to_report': result.stdout == generated})
(args.run_dir / 'event.json').write_text(json.dumps(event, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(event, ensure_ascii=False, indent=2))
if result.returncode or not event.get('byte_identical_to_frozen_report'):
    raise SystemExit(1)
