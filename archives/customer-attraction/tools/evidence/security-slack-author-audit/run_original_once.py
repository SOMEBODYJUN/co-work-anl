"""Directly run the frozen author's finite audit once in a fresh directory."""
from pathlib import Path
import datetime
import hashlib
import json
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
code = output / 'audit_security_slack.py'
shutil.copyfile(source, code)
report = output / 'security_slack_audit.json'
before = sha(code)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
command = [sys.executable, '-I', '-B', str(code.resolve()), '--output', str(report.resolve())]
t = time.perf_counter()
result = subprocess.run(command, cwd=output, capture_output=True, timeout=60)
elapsed = time.perf_counter() - t
(output / 'stdout.txt').write_bytes(result.stdout)
(output / 'stderr.txt').write_bytes(result.stderr)
event = {
    'started_utc': started,
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'argv': command,
    'python': platform.python_version(),
    'seconds': elapsed,
    'exit_code': result.returncode,
    'assertions_enabled': True,
    'original_main_runs': 1,
    'helper_replacements_or_profile': 0,
    'additional_independent_mathematical_audits': 0,
    'LP_SPE_DP_calls': 0,
    'source_bytes': code.stat().st_size,
    'source_sha256_before': before,
    'source_sha256_after': sha(code),
    'stdout_bytes': len(result.stdout),
    'stderr_bytes': len(result.stderr),
    'frozen_report_sha256': sha(frozen),
    'new_report_sha256': sha(report) if report.is_file() else None,
    'report_byte_equal': report.read_bytes() == frozen.read_bytes() if report.is_file() else False,
    'scope': 'author 12 fixed exact examples and 700 scalar checks; no general theorem or sequential equilibrium audit',
}
(output / 'execution.json').write_text(json.dumps(event, ensure_ascii=False, indent=2) + '\n')
assert result.returncode == 0, result.stderr.decode(errors='replace')
assert before == sha(code)
assert event['report_byte_equal']
assert result.stdout == report.read_bytes()
print(json.dumps(event, ensure_ascii=False, indent=2))
