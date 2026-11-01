#!/usr/bin/env python3
"""Run unchanged historical main once; profile return values without replacement."""
import argparse
import hashlib
import json
import platform
import runpy
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy


def plain(value):
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [plain(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def save(path, value):
    path.write_text(json.dumps(plain(value), ensure_ascii=False, indent=2) + '\n')


def fingerprint(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def csr_record(matrix):
    return {'shape': list(matrix.shape), 'data': matrix.data.tolist(),
            'indices': matrix.indices.tolist(), 'indptr': matrix.indptr.tolist()}


def csr_hash(matrix):
    raw = json.dumps(csr_record(matrix), separators=(',', ':'), sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--dependency', type=Path, required=True)
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--run-dir', type=Path, required=True)
    args = p.parse_args()
    args.run_dir.mkdir(parents=True, exist_ok=False)
    run = args.run_dir.resolve()
    src = run / 'strategy_lp.py'
    dep = run / 'spe_dp.py'
    inp = run / 'random_best.json'
    for old, new in [(args.source, src), (args.dependency, dep), (args.input, inp)]:
        shutil.copyfile(old, new)
    before = [fingerprint(path) for path in [src, dep, inp]]
    started = datetime.now(timezone.utc).isoformat()
    clock = time.perf_counter()
    active = {}
    timings = []
    fits = []
    counts = {'original_main': 0, 'solve': 0, 'strategy_constraints': 0, 'matrix': 0, 'optimize': 0, 'linprog': 0}

    def profile(frame, event, result):
        name = frame.f_code.co_name
        file = frame.f_code.co_filename
        if event == 'call':
            tag = None
            if file == str(src) and name in ['main', 'strategy_constraints', 'matrix', 'optimize']:
                tag = 'original_main' if name == 'main' else name
            elif file == str(dep) and name == 'solve':
                tag = 'solve'
            elif name == 'linprog' and frame.f_back and frame.f_back.f_code.co_filename == str(src):
                tag = 'linprog'
            if tag:
                active[id(frame)] = (tag, time.perf_counter())
                counts[tag] += 1
        elif event == 'return' and id(frame) in active:
            tag, at = active.pop(id(frame))
            timings.append({'function': tag, 'seconds_including_observer': time.perf_counter() - at})
            local = frame.f_locals
            if tag == 'solve':
                strategy = result['strategy']
                entries = [{'history': list(h), 'action': int(a)}
                           for h, a in sorted(strategy.items(), key=lambda item: (len(item[0]), item[0]))]
                save(run / 'complete-strategy.json', {'scope': 'original reconstructed complete ordered-history witness',
                     'n': 7, 'players': 6, 'node_count': len(entries), 'entries': entries})
                save(run / 'dp-return.json', {k: v for k, v in result.items() if k != 'strategy'})
            elif tag == 'strategy_constraints':
                save(run / 'constraint-keys.json', {'actual_count': result[0], 'keys': result[1]})
            elif tag == 'matrix':
                save(run / 'ic-matrix.json', csr_record(result))
            elif tag == 'linprog':
                fit = {'omit': frame.f_back.f_locals['omit'], 'result': plain(result),
                       'objective': plain(local['c']), 'A_ub_shape': list(local['A_ub'].shape),
                       'A_ub_nnz': int(local['A_ub'].nnz), 'A_ub_csr_sha256': csr_hash(local['A_ub']),
                       'b_ub': plain(local['b_ub']), 'A_eq': plain(local['A_eq']),
                       'b_eq': plain(local['b_eq']), 'bounds': plain(local['bounds']), 'method': local['method']}
                fits.append(fit)
            elif tag == 'optimize':
                save(run / 'optimize-return.json', result)

    previous_argv = sys.argv[:]
    previous_path = sys.path[:]
    sys.argv = [str(src), '--input', str(inp), '--output', str(run / 'lp_best.json')]
    sys.path.insert(0, str(run))
    sys.setprofile(profile)
    try:
        runpy.run_path(str(src), run_name='__main__')
    finally:
        sys.setprofile(None)
        sys.argv = previous_argv
        sys.path[:] = previous_path
    save(run / 'seven-lp-results.json', {'calls': fits})
    after = [fingerprint(path) for path in [src, dep, inp]]
    event = {'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
             'duration_seconds': time.perf_counter() - clock,
             'invocation': 'runpy unchanged original strategy_lp.py main; sys.setprofile observes original returns only',
             'counts': counts, 'versions': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__},
             'timings': timings, 'inputs_before': before, 'inputs_after': after,
             'helper_replacements': 0, 'additional_solve_or_LP_calls': 0,
             'original_verify_result_calls': 0, 'independent_exact_audits_in_this_event': 0,
             'files': {path.name: fingerprint(path) for path in sorted(run.glob('*.json')) if path.name != 'execution.json'}}
    save(run / 'execution.json', event)


if __name__ == '__main__':
    main()
