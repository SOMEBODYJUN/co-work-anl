"""Preserve a single untouched historical diagnostic execution outside the clone."""
from pathlib import Path
from hashlib import sha256
import datetime
import json
import os
import shutil
import subprocess
import sys
import time

BASE = Path('/workspace/scratch/c0ab78c47566')
REPO = BASE/'boss7-cleaner'
DEST = BASE/'diagonal-basic-author-runtime'
EVID = BASE/'diagonal-basic-author-new-evidence'
OLD = 'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
NEW = 'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5'
EVID.mkdir(exist_ok=False)
subprocess.run([sys.executable, '-B', str(REPO/'archives/customer-attraction/tools/evidence/combined-branch-master-program/materialize_runtime.py'), str(DEST)], check=True, capture_output=True)
for src, name in [('diagonal-basic-author-check-source.py', 'diagonal_basic_check.py'), ('diagonal-basic-zz-threshold-source.json', 'zz_threshold_exact.json')]:
    (DEST/NEW/name).write_bytes((BASE/src).read_bytes())
def inventory():
    return [{'path': str(p.relative_to(DEST)), 'bytes': p.stat().st_size, 'sha256': sha256(p.read_bytes()).hexdigest()} for p in sorted(DEST.rglob('*')) if p.is_file() and p.name != 'diagonal_basic_status.json']
before = inventory()
env = os.environ.copy()
env.pop('PYTHONOPTIMIZE', None)
env['PYTHONDONTWRITEBYTECODE'] = '1'
argv = [sys.executable, '-B', str(DEST/NEW/'diagonal_basic_check.py')]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.perf_counter()
run = subprocess.run(argv, cwd=DEST, env=env, capture_output=True)
seconds = time.perf_counter()-t
(EVID/'stdout.json').write_bytes(run.stdout)
(EVID/'stderr.txt').write_bytes(run.stderr)
after = inventory()
event = {'scope': 'one unchanged historical diagonal_basic_check.py top-level execution; 56 local basic rows only; no graph build or LP', 'started_utc': start, 'argv': argv, 'cwd': str(DEST), 'python_version': sys.version, 'assertions_enabled': True, 'exit_code': run.returncode, 'seconds': seconds, 'stdout_bytes': len(run.stdout), 'stderr_bytes': len(run.stderr), 'source_files_before': before, 'source_files_after': after, 'source_files_unchanged': before == after, 'generated_status_matches_stdout': (DEST/NEW/'diagonal_basic_status.json').read_bytes() == run.stdout}
(EVID/'execution-event.json').write_text(json.dumps(event, ensure_ascii=False, indent=2)+'\n')
assert run.returncode == 0 and not run.stderr and before == after
assert event['generated_status_matches_stdout']
print(json.dumps({k:v for k,v in event.items() if k not in ('source_files_before','source_files_after')}, indent=2))
print(run.stdout.decode())
