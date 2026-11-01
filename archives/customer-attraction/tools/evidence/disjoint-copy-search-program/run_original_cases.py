"""Three distinct original parameter invocations; read-only return observation."""
from pathlib import Path
from fractions import Fraction
import contextlib
import datetime
import gzip
import hashlib
import io
import json
import math
import platform
import runpy
import shutil
import sys
import time

import numpy as np
import scipy


def norm(x):
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, np.ndarray):
        return norm(x.tolist())
    if isinstance(x, np.generic):
        return norm(x.item())
    if isinstance(x, float) and not math.isfinite(x):
        return {'nonfinite_float': repr(x)}
    if isinstance(x, dict):
        return {str(k): norm(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [norm(v) for v in x]
    if x is None or isinstance(x, (str, int, float, bool)):
        return x
    raise TypeError(type(x).__name__)


def write_json(path, obj):
    path.write_text(json.dumps(norm(obj), ensure_ascii=False, indent=2, allow_nan=False) + '\n')


source = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
if output.exists():
    raise FileExistsError(output)
output.mkdir(parents=True)
cases = [
    ('old-open', ['--copies', '2', '--scale2', '1', '--mode', 'open', '--oldpreferred'],
     'copies_old_open.json'),
    ('open-default', ['--copies', '2', '--scale2', '1', '--mode', 'open'], 'copies_open.json'),
    ('finish-scale2', ['--copies', '2', '--scale2', '2', '--mode', 'finish'], 'copies_finish2.json'),
]
summaries = []
for name, arguments, old_name in cases:
    directory = output / name
    directory.mkdir()
    code = directory / 'disjoint_copy_probe.py'
    shutil.copyfile(source, code)
    target = directory / 'report.json'
    source_hash = hashlib.sha256(code.read_bytes()).hexdigest()
    states = []
    payments = []
    lp_records = []
    main_record = {}

    def observer(frame, event, arg):
        if event != 'return':
            return
        filename = frame.f_code.co_filename
        function = frame.f_code.co_name
        values = frame.f_locals
        if filename == str(code):
            if function == 'solve':
                terminal = 'options' not in values
                states.append([
                    list(values['q']), list(values['flags']), list(arg),
                    None if terminal else int(values['x']),
                    None if terminal else int(values['floor']),
                    [] if terminal else [int(item[0]) for item in values['options']],
                ])
            elif function == 'pay':
                payments.append([list(values['q']), [int(x) for x in arg]])
            elif function == 'main':
                for key in ['k', 'n', 'types', 'w', 'inc', 'L', 'nodes', 'root',
                            'term', 'path', 'ups', 'sec', 'exact_root', 'pairs']:
                    main_record[key] = norm(values[key])
                main_record['parameters'] = vars(values['a']).copy()
                main_record['parameters']['output'] = str(main_record['parameters']['output'])
                main_record['caches'] = {
                    key: values[key].cache_info()._asdict() for key in ['solve', 'pay', 'flag_next']
                }
        elif function == 'linprog' and Path(filename).name == '_linprog.py':
            lp_records.append({
                'inputs': norm({key: values[key] for key in
                                ['c', 'A_ub', 'b_ub', 'A_eq', 'b_eq', 'bounds', 'method']}),
                'result': norm(dict(arg)),
            })

    command = [str(code), *arguments, '--output', str(target)]
    original_argv = sys.argv
    stdout, stderr = io.StringIO(), io.StringIO()
    began = datetime.datetime.now(datetime.timezone.utc).isoformat()
    clock = time.perf_counter()
    error = None
    try:
        sys.argv = command
        sys.setprofile(observer)
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            runpy.run_path(str(code), run_name='__main__')
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
    finally:
        sys.setprofile(None)
        sys.argv = original_argv
    seconds = time.perf_counter() - clock
    (directory / 'stdout.txt').write_text(stdout.getvalue())
    (directory / 'stderr.txt').write_text(stderr.getvalue())
    write_json(directory / 'main-capture.json', main_record)
    with gzip.open(directory / 'original-state-and-pay-capture.json.gz', 'wt', encoding='utf-8') as stream:
        json.dump({'state_fields': ['counts', 'flags', 'chosen_terminal', 'action',
                                  'max_scaled_payoff', 'all_maximizing_actions'],
                   'states': states, 'pay_fields': ['terminal_counts', 'scaled_topic_payoffs'],
                   'pay': payments}, stream, separators=(',', ':'))
    with gzip.open(directory / 'original-linprog-capture.json.gz', 'wt', encoding='utf-8') as stream:
        json.dump(lp_records, stream, separators=(',', ':'), allow_nan=False)
    by_counts = {}
    for row in states:
        if row[3] is not None:
            by_counts.setdefault(tuple(row[0]), []).append(row)
    differing = [rows for rows in by_counts.values() if len({r[3] for r in rows}) > 1]
    differing.sort(key=lambda rows: (sum(rows[0][0]), rows[0][0]))
    old = json.loads((Path(__file__).resolve().parent / 'original' / old_name).read_text())
    current = json.loads(target.read_text()) if target.exists() else {}
    shared_exact_keys = ['status', 'copies', 'scale2', 'mode', 'oldpreferred', 'states',
                         'path', 'payoffs', 'W', 'root_security_exact']
    comparison = {'legacy_missing_keys': sorted(set(current) - set(old)),
                  'shared_discrete_fields': {key: {'old': old[key], 'new': current[key],
                                                 'same': old[key] == current[key]}
                                            for key in shared_exact_keys if key in old and key in current},
                  'legacy_seconds_retained_without_rewriting': old.get('seconds')}
    write_json(directory / 'legacy-comparison.json', comparison)
    event = {
        'started_utc': began, 'seconds_with_read_only_observer': seconds,
        'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__,
        'invocation': ['runpy original __main__', *command], 'error': error,
        'original_main_runs': 1, 'assertions_enabled': True, 'helper_replacements': 0,
        'captured_solve_returns': len(states), 'captured_pay_returns': len(payments),
        'captured_linprog_returns': len(lp_records),
        'extra_original_math_calls': 0, 'additional_independent_IC_checks': 0,
        'source_sha256_before': source_hash,
        'source_sha256_after': hashlib.sha256(code.read_bytes()).hexdigest(),
        'stdout_bytes': len(stdout.getvalue().encode()), 'stderr_bytes': len(stderr.getvalue().encode()),
        'equal_counts_with_different_actions': len(differing),
        'history_flag_examples': differing[:4],
    }
    write_json(directory / 'execution.json', event)
    assert error is None, event
    assert event['source_sha256_before'] == event['source_sha256_after']
    assert len(lp_records) == 6
    summaries.append({key: event[key] for key in
                      ['seconds_with_read_only_observer', 'captured_solve_returns',
                       'captured_pay_returns', 'captured_linprog_returns',
                       'equal_counts_with_different_actions']})
    print(json.dumps({'case': name, **summaries[-1]}), flush=True)
write_json(output / 'three-case-summary.json', {'distinct_parameter_invocations': 3,
           'original_main_runs': 3, 'original_linprog_calls': 18,
           'additional_independent_mathematical_audits': 0, 'cases': summaries})
