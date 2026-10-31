"""Run frozen board suites only in new temporary file-only Git fixtures.

Never imports the user's active checkout, remote configuration or credentials.
The test credentials are the explicit synthetic strings in the frozen tests.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

E = Path(__file__).resolve().parent
S = E.parents[2]
SCOPE = Path('research/weighted_congestion_frontier')
sources = json.loads((E / 'source-manifest.json').read_text())
deps = json.loads((E / 'dependency-manifest.json').read_text())
records = {x['id']: x for x in sources + deps}
out = E / 'runs'
out.mkdir(exist_ok=True)
env = {k: v for k, v in os.environ.items()
       if not k.startswith(('GIT_', 'WCG_')) and k not in ('SSH_AUTH_SOCK', 'SSH_ASKPASS')}
env.update(GIT_ALLOW_PROTOCOL='file', GIT_TERMINAL_PROMPT='0',
           GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null',
           GIT_CONFIG_SYSTEM='/dev/null', PYTHONDONTWRITEBYTECODE='1')

summary = []
for variant, board_id, checkpoint_id in [
    ('legacy', '673a94bf8c2a50db4be5', 'f4ad07192854bfc106ad'),
    ('main', '99da839bfd62db2365a0', 'db6af3d64d99cc147969'),
]:
    ids = [board_id, checkpoint_id, '8bf0d5ec0cfafef1274c',
           '207fa0dc8920b57c0653', '35511e58709fa3bd7815', '988a0574030a7fded769']
    with tempfile.TemporaryDirectory(prefix='board-audit-', dir=S) as temp:
        root = Path(temp)
        materialized = []
        for ident in ids:
            x = records[ident]
            raw = (S / x['saved_path']).read_bytes()
            assert len(raw) == x['size'] and hashlib.sha256(raw).hexdigest() == x['sha256']
            dest = root / x['path']
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
            dest.chmod(0o755 if x['mode'] == '100755' else 0o644)
            materialized.append({'id': ident, 'path': x['path'], 'sha256': x['sha256'],
                                 'bytes': len(raw), 'mode': x['mode']})
        subprocess.run(['git', 'init', '--quiet', str(root)], cwd=root, env=env,
                       check=True, capture_output=True, timeout=30)
        command = [sys.executable, '-m', 'unittest', 'discover', '-s', str(SCOPE / 'tests'), '-v']
        started = time.monotonic()
        try:
            result = subprocess.run(command, cwd=root, env=env, capture_output=True,
                                    text=True, timeout=180)
            stdout, stderr, code = result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired as exc:
            stdout = (exc.stdout or b'').decode(errors='replace') if isinstance(exc.stdout, bytes) else exc.stdout or ''
            stderr = (exc.stderr or b'').decode(errors='replace') if isinstance(exc.stderr, bytes) else exc.stderr or ''
            code = 'timeout'
        (out / (variant + '.stdout.txt')).write_text(stdout)
        (out / (variant + '.stderr.txt')).write_text(stderr)
        report = {'variant': variant, 'returncode': code,
                  'seconds': round(time.monotonic() - started, 3), 'command': command,
                  'fixture_root_kind': 'fresh temporary repository; removed after run',
                  'source_inputs': materialized,
                  'git_version': subprocess.check_output(['git', '--version'], cwd=root, env=env, text=True).strip(),
                  'python_version': sys.version,
                  'environment_guards': {k: env[k] for k in ('GIT_ALLOW_PROTOCOL', 'GIT_TERMINAL_PROMPT',
                      'GIT_CONFIG_NOSYSTEM', 'GIT_CONFIG_GLOBAL', 'GIT_CONFIG_SYSTEM', 'PYTHONDONTWRITEBYTECODE')},
                  'real_remote_network_credentials_used': False,
                  'scope': 'new isolated software fixture result, not mathematical proof, current production or real authentication certification'}
        (out / (variant + '.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        summary.append({'variant': variant, 'returncode': code, 'seconds': report['seconds']})
        print(json.dumps(summary[-1]), flush=True)
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
