"""Run either inspected original insurer audit once in a fresh external folder."""
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ap = ArgumentParser()
ap.add_argument('--case', choices=['blind', 'sharp'], required=True)
ap.add_argument('--run-dir', type=Path, required=True)
args = ap.parse_args()
base = Path(__file__).resolve().parent
rows = json.loads((base / 'source-manifest.json').read_text())['rows']
stem = 'insurer_blind_audit' if args.case == 'blind' else 'insurer_three_sharp_audit'
program_row = next(r for r in rows if Path(r['path']).name == stem + '.py')
report_row = next(r for r in rows if Path(r['path']).name == stem + '.json')
program = base / 'original' / program_row['path']
frozen = base / 'original' / report_row['path']
for path, row in [(program, program_row), (frozen, report_row)]:
    raw = path.read_bytes()
    if len(raw) != row['size'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
        raise ValueError('original source fingerprint mismatch')
if args.run_dir.exists():
    raise ValueError('run directory must not exist')
args.run_dir.mkdir(parents=True)
copied = args.run_dir / program.name
shutil.copyfile(program, copied)
environment = os.environ.copy()
environment['PYTHONOPTIMIZE'] = '0'
environment['PYTHONDONTWRITEBYTECODE'] = '1'
argv = [sys.executable, str(copied)]
start_utc = datetime.now(timezone.utc).isoformat()
start = time.monotonic()
result = subprocess.run(argv, cwd=args.run_dir, env=environment, capture_output=True)
elapsed = time.monotonic() - start
(args.run_dir / 'stdout.txt').write_bytes(result.stdout)
(args.run_dir / 'stderr.txt').write_bytes(result.stderr)
output = args.run_dir / frozen.name
event = {
    'case': args.case, 'original_entry_invocations': 1,
    'mode': 'unchanged hard-coded original entry; no import beforehand; fresh isolated directory',
    'argv': argv, 'cwd': str(args.run_dir), 'started_utc': start_utc,
    'python': sys.version, 'returncode': result.returncode, 'wall_seconds': elapsed,
    'PYTHONOPTIMIZE': '0', 'PYTHONDONTWRITEBYTECODE': '1',
    'source_sha256': program_row['sha256'],
    'source_unchanged_after_run': copied.read_bytes() == program.read_bytes(),
    'frozen_report_sha256': report_row['sha256'], 'output_exists': output.exists(),
    'native_ordered_tree_BI_and_full_replay': args.case == 'blind',
    'native_set_valued_count_BI': args.case == 'sharp',
    'native_fixed_seed_generated_subtheme_cases': 24 if args.case == 'sharp' else 0,
    'native_seed': 7362129 if args.case == 'sharp' else None,
    'additional_random_search_or_new_parameters': 0,
    'canonical_repository_solver_or_optimizer_calls': 0,
    'parent_seven_input_or_author_compiler_entries': 0,
}
if output.exists():
    raw = output.read_bytes()
    event.update({'output_size': len(raw),
                  'output_sha256': hashlib.sha256(raw).hexdigest(),
                  'byte_identical_to_frozen_report': raw == frozen.read_bytes(),
                  'structured_identical_to_frozen_report': json.loads(raw) == json.loads(frozen.read_bytes()),
                  'stdout_identical_to_report': result.stdout == raw})
(args.run_dir / 'event.json').write_text(json.dumps(event, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(event, ensure_ascii=False, indent=2))
if result.returncode or not event.get('byte_identical_to_frozen_report'):
    raise SystemExit(1)
