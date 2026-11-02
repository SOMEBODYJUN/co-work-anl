"""Execute one unmodified original function AST, never the old random driver.

The expected TypeError is evidence of the archived implementation boundary,
not a negative result for a mathematical inequality. No replacement function,
mock Instance, missing helper, LP, or SPE search is used.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import ast
import datetime
import hashlib
import json
import platform
import subprocess
import sys
import time
import traceback

BASE = Path(__file__).resolve().parent
RELATIVE_SOURCE = (
    'original/research/workspaces/customer-attraction/'
    'R-b28b3013e6464e70862b4993359a6964/independent_attack/theta_dp.py'
)


def fingerprint(path):
    data = path.read_bytes()
    return {'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def worker(repo):
    dependencies = json.loads((BASE / 'dependency-manifest.json').read_text())
    rows = dependencies['canonical_reused_files']
    for row in rows:
        got = fingerprint(repo / row['preserved_repo_path'])
        assert got == {'size': row['size'], 'sha256': row['sha256']}
    roots = {(repo / row['preserved_repo_path']).parent.parent for row in rows}
    assert len(roots) == 1
    sys.path.insert(0, str(next(iter(roots))))
    from customer_attraction import Instance

    source = BASE / RELATIVE_SOURCE
    text = source.read_text()
    module = ast.parse(text, filename=str(source))
    matches = [node for node in module.body
               if isinstance(node, ast.FunctionDef) and node.name == 'best_opt_dp']
    assert len(matches) == 1
    selected = matches[0]
    isolated = ast.Module(body=[selected], type_ignores=[])
    namespace = {'Fraction': Fraction}
    exec(compile(isolated, str(source), 'exec'), namespace)
    # This is a legal member of the source's p=3, m=6..10, multiplicity 0..20
    # domain. The failure occurs before any ls entry is read.
    instance = Instance.from_topic_sets(({0}, set(), set()), players=6)
    try:
        namespace['best_opt_dp'](instance, [])
    except TypeError as error:
        assert str(error) == "argument of type 'int' is not iterable"
        failure = {'type': type(error).__name__, 'message': str(error),
                   'traceback': traceback.format_exc()}
    else:
        raise AssertionError('The archived literal function did not fail as expected')
    result = {
        'status': 'expected-original-function-TypeError-observed',
        'scope': 'one unmodified selected function; no original module/driver execution',
        'source': {'relative_path': RELATIVE_SOURCE, **fingerprint(source)},
        'function': {'name': selected.name, 'line': selected.lineno,
                     'end_line': selected.end_lineno,
                     'original_AST_unmodified': True},
        'instance': instance.to_dict(),
        'ls_argument': [],
        'failure_before_ls_is_read': True,
        'exception': failure,
        'original_best_opt_dp_function_calls': 1,
        'original_module_imports': 0,
        'original_random_driver_iterations': 0,
        'canonical_SPE_solver_calls': 0,
        'LP_calls': 0,
        'corrected_bitmask_DP_calls': 0,
        'synthetic_replacement_helpers': 0,
        'mathematical_negative_result': False,
        'python': platform.python_version(),
    }
    out = BASE / 'replay'
    out.mkdir(exist_ok=True)
    (out / 'literal-failure.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('exception', 'instance')}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--worker', action='store_true')
    args = parser.parse_args()
    if args.worker:
        worker(args.repo.resolve())
        return
    command = [sys.executable, '-I', str(Path(__file__).resolve()),
               '--repo', str(args.repo.resolve()), '--worker']
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    before = time.monotonic()
    process = subprocess.run(command, capture_output=True, text=True)
    out = BASE / 'replay'
    out.mkdir(exist_ok=True)
    (out / 'stdout.txt').write_text(process.stdout)
    (out / 'stderr.txt').write_text(process.stderr)
    event = {'argv': command, 'start_utc': started,
             'elapsed_seconds': time.monotonic() - before,
             'returncode': process.returncode,
             'driver': fingerprint(Path(__file__)),
             'stdout': fingerprint(out / 'stdout.txt'),
             'stderr': fingerprint(out / 'stderr.txt')}
    (out / 'execution-record.json').write_text(
        json.dumps(event, ensure_ascii=False, indent=2) + '\n')
    print(process.stdout, end='')
    print(process.stderr, end='', file=sys.stderr)
    print(json.dumps(event, ensure_ascii=False, indent=2))
    if process.returncode:
        raise SystemExit(process.returncode)


if __name__ == '__main__':
    main()
