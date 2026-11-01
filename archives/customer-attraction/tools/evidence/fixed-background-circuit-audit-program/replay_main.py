#!/usr/bin/env python3
"""One unchanged original main; observe returned locals, never rerun helpers."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import platform
import runpy
import shutil
import sys
import time


def plain(x):
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, dict):
        return {str(k): plain(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [plain(v) for v in x]
    return x


def digest(path):
    b = path.read_bytes()
    return {'path': str(path), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(path, value):
    path.write_text(json.dumps(plain(value), ensure_ascii=False, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args()
    args.run_dir.mkdir(parents=True, exist_ok=False)
    run = args.run_dir.resolve()
    source = run / 'audit_fixed_background.py'
    shutil.copyfile(args.source, source)
    before = digest(source)
    counts = Counter()
    observations = {'base': [], 'four': [], 'aggregate': [], 'all_unit': [], 'six': []}
    names = {'verify_case': 'base', 'verify_four': 'four', 'verify_aggregate': 'aggregate',
             'verify_all_unit': 'all_unit', 'verify_six': 'six'}
    start = time.perf_counter()
    started = datetime.now(timezone.utc).isoformat()

    def profile(frame, event, value):
        if frame.f_code.co_filename != str(source):
            return
        name = frame.f_code.co_name
        if event == 'call':
            counts[name] += 1
        elif event == 'return' and name in names:
            local = frame.f_locals
            record = {'original_function': name, 'returned': value}
            for key in ['M', 'bg', 'r', 's', 'k', 'loads', 'd', 'expected', 'actual', 'patterns', 'rows', 'circuits']:
                if key in local:
                    record[key] = local[key]
            observations[names[name]].append(record)

    previous_argv = sys.argv[:]
    sys.argv = [str(source)]
    sys.setprofile(profile)
    try:
        runpy.run_path(str(source), run_name='__main__')
    finally:
        sys.setprofile(None)
        sys.argv = previous_argv
    original_seconds = time.perf_counter() - start
    # These are already computed original objects, serialized after main returns.
    raw = json.dumps(plain(observations), ensure_ascii=False, separators=(',', ':')).encode()
    (run / 'original-observations.json.gz').write_bytes(gzip.compress(raw, mtime=0))
    observation_summary = {}
    for family, records in observations.items():
        observation_summary[family] = {
            'calls': len(records),
            'matrix_entries_serialized': sum(sum(len(row) for row in item.get('rows', [])) for item in records),
            'basis_vectors_serialized': sum(len(item.get('circuits', [])) for item in records),
            'basis_coefficients_serialized': sum(sum(len(row) for row in item.get('circuits', [])) for item in records),
            'returned_records': [item['returned'] for item in records],
        }
    save(run / 'observation-summary.json', observation_summary)
    event = {'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
             'observed_original_main_seconds': original_seconds, 'total_seconds': time.perf_counter() - start,
             'invocation': 'runpy unchanged original main, standard-library profile observes original returns; no helper replacement',
             'python': platform.python_version(), 'assertions_enabled': __debug__,
             'source_before': before, 'source_after': digest(source),
             'original_function_call_events': dict(sorted(counts.items())),
             'observer_scope': 'original returned local matrices/bases and metadata, serialized once after main; not a new rank/nullspace audit',
             'helper_replacements': 0, 'additional_original_helper_calls': 0,
             'optimization_calls': 0, 'SPE_solver_calls': 0, 'new_independent_mathematical_audits': 0,
             'observation_payload_uncompressed_bytes': len(raw),
             'files': {p.name: digest(p) for p in sorted(run.iterdir()) if p.is_file() and p.name != source.name}}
    save(run / 'execution.json', event)


if __name__ == '__main__':
    main()
