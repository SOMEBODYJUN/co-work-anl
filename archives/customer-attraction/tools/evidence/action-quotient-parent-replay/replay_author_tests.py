"""Run the byte-identical author suite once in isolation.

This is a current replay wrapper, not the unavailable historical parent runner
and not another independent implementation of the complete quotient tests.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import copyfile
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    primary = BASE / 'original/action_quotient_replay.json'
    frozen = json.loads(primary.read_text())
    assert sha(primary) == '55f8b8ff482456604a8b32c650c62309d892197290e2da58070d370b36cd96b2'
    compiler = BASE / 'related/duplicate_action_quotient.py'
    tests = BASE / 'related/test_duplicate_action_quotient.py'
    author_report = BASE / 'related/duplicate_action_quotient_test_report.json'
    assert sha(compiler) == frozen['compiler_sha256']
    assert sha(tests) == frozen['test_sha256']
    expected = json.loads(author_report.read_text())
    assert len(expected) == 9 and {k: frozen[k] for k in expected} == expected
    output = BASE / 'replay'
    output.mkdir(exist_ok=True)
    environment = os.environ.copy()
    environment.pop('PYTHONOPTIMIZE', None)
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    started = time.monotonic()
    with TemporaryDirectory(prefix='isolated-author-', dir=output) as tmp:
        temp = Path(tmp)
        for path in (compiler, tests):
            copyfile(path, temp / path.name)
            assert sha(temp / path.name) == sha(path)
        result = subprocess.run([sys.executable, '-B', str(temp / tests.name)], cwd=temp,
                                env=environment, capture_output=True, timeout=180)
    elapsed = time.monotonic() - started
    (output / 'author-stdout.json').write_bytes(result.stdout)
    (output / 'author-stderr.txt').write_bytes(result.stderr)
    parsed = json.loads(result.stdout) if result.returncode == 0 else None
    event = {
        'status': 'PASS' if result.returncode == 0 and parsed == expected else 'FAIL',
        'operation': 'unchanged author __main__ CLI replay in temporary isolated directory',
        'wrapper_is_original_parent_runner': False,
        'new_independent_full_test_implementation': False,
        'command': ['python3', '-B', 'test_duplicate_action_quotient.py'],
        'python_version': platform.python_version(),
        'assertions_enabled': True,
        'pythonoptimize_environment_removed': True,
        'exit_code': result.returncode,
        'elapsed_seconds': elapsed,
        'compiler_sha256': sha(compiler),
        'test_sha256': sha(tests),
        'stdout_bytes': len(result.stdout),
        'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
        'stderr_bytes': len(result.stderr),
        'author_report_byte_identical': result.stdout == author_report.read_bytes(),
        'all_nine_author_fields_equal': parsed == expected,
        'all_nine_parent_data_fields_equal': parsed == {k: frozen[k] for k in expected},
        'parent_extra_fields': ['review', 'compiler_sha256', 'test_sha256'],
        'review_field_scope': 'Historical provenance declaration, not generated or independently proved by author tests.'
    }
    (output / 'execution-event.json').write_text(json.dumps(event, indent=2) + '\n')
    assert event['status'] == 'PASS' and not result.stderr
    assert event['author_report_byte_identical']
    print(json.dumps(event, indent=2))


if __name__ == '__main__':
    main()
