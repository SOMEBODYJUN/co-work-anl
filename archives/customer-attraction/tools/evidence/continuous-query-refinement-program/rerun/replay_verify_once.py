"""One original refinement --verify replay; no adaptive discovery run."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json
import subprocess
import sys
import time
import numpy
import scipy

ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT / 'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3/refine_continuous_queries.py'


def main():
    assert sys.flags.optimize == 0
    sources = json.loads((ROOT / 'frozen-input-manifest.json').read_text())
    def check():
        for rec in sources:
            data = (ROOT / rec['path']).read_bytes()
            assert len(data) == rec['size'] and sha256(data).hexdigest() == rec['sha256']
    check()
    out = ROOT / 'original-verify'
    out.mkdir(exist_ok=False)
    argv = [sys.executable, '-B', str(PROGRAM), '--verify']
    event = {'scope': 'one unmodified refine_continuous_queries.py --verify; no LP discovery',
             'started_utc': datetime.now(timezone.utc).isoformat(),
             'argv': argv, 'cwd': str(ROOT), 'python': sys.version,
             'numpy': numpy.__version__, 'scipy': scipy.__version__,
             'assertions_enabled': True, 'prechecked_frozen_files': len(sources),
             'program_sha256': sha256(PROGRAM.read_bytes()).hexdigest(),
             'root_marker': 'comment-only work.py for ancestor path discovery; never imported/executed'}
    (out / 'execution.json').write_text(json.dumps(event, indent=2) + '\n')
    start = time.monotonic()
    result = subprocess.run(argv, cwd=ROOT, capture_output=True, check=False)
    event.update(finished_utc=datetime.now(timezone.utc).isoformat(),
                 wall_seconds=time.monotonic()-start, exit_code=result.returncode)
    for name, data in [('stdout', result.stdout), ('stderr', result.stderr)]:
        (out / (name + '.txt')).write_bytes(data)
        event[name + '_bytes'] = len(data)
        event[name + '_sha256'] = sha256(data).hexdigest()
    check()
    event['frozen_bytes_unchanged'] = True
    event['trace_file_created'] = (PROGRAM.parent / 'continuous_refinement_trace.json').exists()
    (out / 'execution.json').write_text(json.dumps(event, indent=2) + '\n')
    print(result.stdout.decode())
    print(result.stderr.decode())
    print(json.dumps(event, indent=2))
    assert result.returncode == 0 and not event['trace_file_created']


if __name__ == '__main__':
    main()
