"""Materialize the frozen import layout and execute the original crosscheck once.

No source rewriting, runpy, tracing, profiling, function substitution, LP, or
full initial-game solve. The runtime must be outside the repository and empty.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
TAIL = Path('research/workspaces/customer-attraction/R-5bb00b5c3cf740f099eae62130632b56/credible_attack')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--runtime', type=Path, required=True)
    args = parser.parse_args()
    runtime = args.runtime.resolve()
    assert not runtime.exists(), 'Use a fresh runtime; do not overwrite an earlier event.'
    runtime.mkdir(parents=True)
    placements = {
        'original/crosscheck_tail_oracle.py': TAIL/'crosscheck_tail_oracle.py',
        'related/two_pool_tail_search.py': TAIL/'two_pool_tail_search.py',
    }
    placements.update({f'dependencies/customer_attraction/{n}': Path('customer_attraction')/n
                       for n in ['__init__.py', 'model.py', 'exact.py', 'certificate.py']})
    before = {}
    for source, relative in placements.items():
        target = runtime/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((HERE/source).read_bytes())
        assert sha(target) == sha(HERE/source)
        before[str(relative)] = sha(target)
    command = [sys.executable, str(runtime/TAIL/'crosscheck_tail_oracle.py')]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tick = time.perf_counter()
    result = subprocess.run(command, cwd=runtime, capture_output=True,
                            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    elapsed = time.perf_counter()-tick
    replay = HERE/'replay'
    replay.mkdir(exist_ok=True)
    (replay/'stdout.txt').write_bytes(result.stdout)
    (replay/'stderr.txt').write_bytes(result.stderr)
    produced = runtime/TAIL/'tail_oracle_crosscheck.json'
    expected = HERE/'original/tail_oracle_crosscheck.json'
    after = {relative: sha(runtime/relative) for relative in before}
    same = produced.exists() and produced.read_bytes() == expected.read_bytes()
    data = json.loads(produced.read_text()) if produced.exists() else None
    if produced.exists():
        (replay/'tail_oracle_crosscheck.json').write_bytes(produced.read_bytes())
    event = {
        'kind': 'one-plain-original-cli-in-frozen-import-layout',
        'started_utc': started,
        'elapsed_seconds': elapsed,
        'command': command,
        'cwd': str(runtime),
        'python': platform.python_version(),
        'exit_code': result.returncode,
        'stdout_bytes': len(result.stdout),
        'stderr_bytes': len(result.stderr),
        'stdout_sha256': sha(replay/'stdout.txt'),
        'stderr_sha256': sha(replay/'stderr.txt'),
        'source_sha256_before': before,
        'source_sha256_after': after,
        'sources_unchanged': before == after,
        'frozen_report_sha256': sha(expected),
        'new_report_sha256': sha(produced) if produced.exists() else None,
        'new_report_bytes': produced.stat().st_size if produced.exists() else None,
        'report_byte_equal': same,
        'saved_sample_count': len(data['samples']) if data else None,
        'all_exact_checks_passed': data.get('all_exact_checks_passed') if data else None,
        'original_main_invocations': 1,
        'original_full_parameter_search_invocations': 0,
        'full_initial_game_solve_invocations': 0,
        'strategy_certificate_expansions': 0,
        'lp_calls': 0,
        'profile_trace_runpy_or_monkeypatch': False,
    }
    (replay/'execution.json').write_text(json.dumps(event, indent=2)+'\n')
    assert result.returncode == 0
    assert not result.stderr
    assert before == after
    assert same
    assert len(data['samples']) == 12 and data['all_exact_checks_passed'] is True
    print(json.dumps({k: event[k] for k in ['exit_code', 'elapsed_seconds',
                      'report_byte_equal', 'new_report_bytes', 'new_report_sha256',
                      'saved_sample_count', 'sources_unchanged']}))


if __name__ == '__main__':
    main()
