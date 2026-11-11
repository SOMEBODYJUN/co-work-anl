"""Save exact execution records inside this task's permitted write scope."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import subprocess
import sys
import time

here = Path(__file__).resolve().parent
assert len(sys.argv) == 2 and sys.argv[1] in ('build', 'verify')
stage = sys.argv[1]
source = here / (stage + '.py')
argv = [sys.executable, '-B', str(source)]
started_utc = datetime.now(timezone.utc).isoformat()
started = time.perf_counter()
result = subprocess.run(argv, cwd=Path.cwd(), capture_output=True)
elapsed = time.perf_counter()-started
(here / (stage + '.stdout.txt')).write_bytes(result.stdout)
(here / (stage + '.stderr.txt')).write_bytes(result.stderr)
record = dict(stage=stage, argv=argv, cwd=str(Path.cwd()), started_utc=started_utc,
              completed_utc=datetime.now(timezone.utc).isoformat(), elapsed_seconds=elapsed,
              exit_code=result.returncode, python=platform.python_version(), optimizer_calls=0,
              source_sha256=sha256(source.read_bytes()).hexdigest(),
              stdout_sha256=sha256(result.stdout).hexdigest(), stderr_sha256=sha256(result.stderr).hexdigest())
(here / ('execution_' + stage + '.json')).write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record, indent=2), flush=True)
if result.stdout:
    print(result.stdout.decode()[-5000:], flush=True)
if result.stderr:
    print(result.stderr.decode(), file=sys.stderr, flush=True)
raise SystemExit(result.returncode)
