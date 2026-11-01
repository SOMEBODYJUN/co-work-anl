"""Run the unmodified frozen finite audit once in a fresh directory."""
import datetime
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


source, frozen, output = map(Path, sys.argv[1:])
if output.exists():
    raise FileExistsError(output)
output.mkdir(parents=True)
runtime = output / 'runtime'
runtime.mkdir()
code = runtime / 'audit_floor_only_protection.py'
shutil.copyfile(source, code)
before = sha(code)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.perf_counter()
command = [sys.executable, '-I', '-B', str(code.resolve())]
result = subprocess.run(command, cwd=runtime, capture_output=True, timeout=60)
seconds = time.perf_counter() - t
(output / 'stdout.txt').write_bytes(result.stdout)
(output / 'stderr.txt').write_bytes(result.stderr)
report = runtime / 'floor_only_protection_audit.json'
if report.exists():
    shutil.copyfile(report, output / 'floor_only_protection_audit.json')
event = {
    'started_utc': started,
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'argv': command,
    'python': platform.python_version(),
    'seconds': seconds,
    'exit_code': result.returncode,
    'assertions_enabled': True,
    'original_main_runs': 1,
    'profile_or_helper_replacements': 0,
    'independent_mathematical_audits': 0,
    'SPE_DP_LP_calls': 0,
    'source_bytes': code.stat().st_size,
    'source_sha256_before': before,
    'source_sha256_after': sha(code),
    'stdout_bytes': len(result.stdout),
    'stderr_bytes': len(result.stderr),
    'frozen_report_sha256': sha(frozen),
    'new_report_sha256': sha(report) if report.exists() else None,
    'report_byte_equal': report.read_bytes() == frozen.read_bytes() if report.exists() else False,
    'scope': 'one original finite 18-root arithmetic audit; no complete strategy or general-player execution',
}
(output / 'execution.json').write_text(json.dumps(event, ensure_ascii=False, indent=2) + '\n')
assert result.returncode == 0, result.stderr.decode(errors='replace')
assert before == sha(code)
assert event['report_byte_equal']
print(json.dumps(event, ensure_ascii=False, indent=2))
