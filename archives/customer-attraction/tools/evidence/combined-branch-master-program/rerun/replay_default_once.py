"""Current cleanup orchestration: one untouched combined --verify entrypoint.

This file is outside the repository while the parent holds repository writes.
No build monkeypatch, profiler, LP solve, or historical entrypoint alteration.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import time
import numpy
import scipy

ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT / 'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/combined_branch_master.py'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    assert sys.flags.optimize == 0
    manifest = json.loads((ROOT / 'current-frozen-files-manifest.json').read_text())
    for row in manifest:
        data = (ROOT / row['path']).read_bytes()
        assert len(data) == row['size'] and sha(data) == row['sha256']
    out = ROOT / 'default-verify'
    out.mkdir(exist_ok=False)
    command = [sys.executable, '-B', str(PROGRAM), '--verify']
    record = {'scope': 'one unmodified default combined_branch_master.py --verify; no optimization mode',
              'started_utc': datetime.now(timezone.utc).isoformat(), 'argv': command, 'cwd': str(ROOT),
              'python': sys.version, 'numpy': numpy.__version__, 'scipy': scipy.__version__,
              'assertions_enabled': True, 'entrypoint_source_sha256': sha(PROGRAM.read_bytes()),
              'available_frozen_files_prechecked': len(manifest),
              'ROOT_marker': 'current real repository work.py copied solely for path discovery; not imported or executed',
              'ROOT_marker_sha256': sha((ROOT / 'work.py').read_bytes()),
              'built_in_flags': ['--priced', '--optimum', '--old-query-cuts', '--mixed-pair']}
    (out / 'execution.json').write_text(json.dumps(record, indent=2) + '\n')
    start = time.monotonic()
    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
    record.update({'finished_utc': datetime.now(timezone.utc).isoformat(),
                   'wall_seconds': time.monotonic() - start, 'exit_code': result.returncode})
    for name, data in [('stdout', result.stdout), ('stderr', result.stderr)]:
        (out / (name + '.txt')).write_bytes(data)
        record[name + '_bytes'] = len(data)
        record[name + '_sha256'] = sha(data)
    for row in manifest:
        data = (ROOT / row['path']).read_bytes()
        assert len(data) == row['size'] and sha(data) == row['sha256']
    record['all_prechecked_frozen_bytes_unchanged'] = True
    (out / 'execution.json').write_text(json.dumps(record, indent=2) + '\n')
    print(result.stdout.decode())
    print(result.stderr.decode())
    print(json.dumps(record, indent=2))
    assert result.returncode == 0


if __name__ == '__main__':
    main()
