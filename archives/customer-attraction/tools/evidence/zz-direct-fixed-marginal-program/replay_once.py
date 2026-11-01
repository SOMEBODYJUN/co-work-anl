"""Copy an exact source closure and invoke zz_direct.py once in isolation.

No original function is replaced; no trace/profile/runpy instrumentation.
The runtime has only a root-location work.py marker, not the repository CLI.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    runtime = args.output / 'runtime'
    runtime.mkdir()
    manifest = json.loads(args.manifest.read_text())
    for rec in manifest:
        data = (args.repo / rec['source_repo_path']).read_bytes()
        assert len(data) == rec['bytes'] and digest(data) == rec['sha256']
        dst = runtime / rec['runtime_path']
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
    source = args.source.read_bytes()
    assert digest(source) == 'fe4d34b7a51cc3f6f7225ac71d7c69c081cfe2681b192cc7a04228e17d002695'
    program = runtime / 'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/zz_direct.py'
    program.parent.mkdir(parents=True)
    program.write_bytes(source)
    (runtime / 'work.py').write_text('# Root-location marker only; never imported or executed.\n')
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    argv = [sys.executable, '-B', str(program)]
    started = time.monotonic()
    record = {
        'operation': 'one unmodified zz_direct.py direct Python subprocess',
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'argv': argv, 'cwd': str(runtime), 'python': sys.version,
        'source_sha256': digest(source), 'dependency_files': len(manifest),
        'source_modifications': False, 'trace_or_profile': False,
        'runpy': False, 'LP_calls': 0, 'old_3889_verifier_calls': 0,
        'root_marker': 'inert work.py for original path discovery',
    }
    result = subprocess.run(argv, cwd=runtime, env=env, capture_output=True, timeout=60)
    record.update({'finished_utc': datetime.now(timezone.utc).isoformat(),
                   'elapsed_seconds': time.monotonic()-started, 'exit_code': result.returncode})
    for name, data in [('stdout',result.stdout), ('stderr',result.stderr)]:
        (args.output/(name+'.txt')).write_bytes(data)
        record[name+'_bytes'] = len(data)
        record[name+'_sha256'] = digest(data)
    assert result.returncode == 0, result.stderr.decode()
    report_bytes = (program.parent/'zz_direct_status.json').read_bytes()
    report = json.loads(report_bytes)
    assert report == json.loads(result.stdout)
    assert report_bytes == result.stdout
    (args.output/'zz_direct_status.json').write_bytes(report_bytes)
    for rec in manifest:
        assert digest((runtime/rec['runtime_path']).read_bytes()) == rec['sha256']
    assert program.read_bytes() == source
    record.update({'input_bytes_unchanged': True,
                   'report_bytes': len(report_bytes),
                   'report_sha256': digest(report_bytes),
                   'report_byte_identical_stdout': True,
                   'rows': report['rows'], 'negative_rows': len(report['negative_rows']),
                   'minimum_slack': report['minimum_slack']})
    (args.output/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))


if __name__ == '__main__':
    main()
