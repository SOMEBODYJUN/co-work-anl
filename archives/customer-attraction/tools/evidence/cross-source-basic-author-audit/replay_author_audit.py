"""Run the unmodified historical fourteen-row auditor once in a frozen tree.

This is orchestration, not another coefficient generator or a full-graph run.
The 49-file input manifest is an availability check, not a loaded-file trace.
"""
from datetime import datetime, timezone
from fractions import Fraction
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

import numpy
import scipy

AUTHOR_SHA = '5113ef5d4f46b5d2c40b6fc9dcb3c1788fa4d3ea6677bf89a462560d4a53275b'
AUTHOR_PATH = 'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3/audit_cross_source_basic.py'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', required=True, type=Path)
    parser.add_argument('--runtime', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    evidence = args.repository / 'archives/customer-attraction/tools/evidence'
    manifest_path = evidence / 'combined-branch-master-program/rerun/available-frozen-files-manifest.json'
    available = json.loads(manifest_path.read_bytes())
    source = evidence / 'cross-source-graph-program/related/audit_cross_source_basic.py'
    assert source.stat().st_size == 3019 and sha(source) == AUTHOR_SHA
    target = args.runtime / AUTHOR_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        assert target.read_bytes() == source.read_bytes()
    else:
        shutil.copyfile(source, target)
    inputs = available + [{'path': AUTHOR_PATH, 'size': 3019, 'sha256': AUTHOR_SHA}]
    for record in inputs:
        path = args.runtime / record['path']
        assert path.stat().st_size == record['size']
        assert sha(path) == record['sha256'], record['path']
    previous_slacks = json.loads((evidence / 'cross-source-graph-program/added-row-slacks.json').read_bytes())['split_point']
    independent_negatives = {v['name']: v['slack'] for v in previous_slacks
                            if Fraction(v['slack']) < 0}
    args.out.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, '-B', str(target.resolve())]
    record = {
        'scope': 'One unmodified author audit_cross_source_basic.py entrypoint; only fourteen added rows, no inherited build, full-graph verification, priced/optimum rows or optimization.',
        'argv': command, 'cwd': str(args.runtime.resolve()),
        'python': platform.python_version(), 'numpy': numpy.__version__,
        'scipy': scipy.__version__, 'assertions_enabled_in_wrapper': __debug__,
        'child_uses_no_O_flag': True,
        'source_sha256': AUTHOR_SHA,
        'source_bytes': target.stat().st_size,
        'available_frozen_inputs_checked': len(inputs),
        'available_manifest_sha256': sha(manifest_path),
        'available_manifest_scope': '49 shared available frozen files plus this auditor; not a claim that all files were loaded.',
        'ROOT_marker_scope': 'Existing shared runtime work.py is a root-location marker only; not executed by this entrypoint.',
        'started_utc': datetime.now(timezone.utc).isoformat(),
    }
    started = time.monotonic()
    process = subprocess.run(command, cwd=args.runtime, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=False)
    record['wall_seconds'] = time.monotonic() - started
    record['finished_utc'] = datetime.now(timezone.utc).isoformat()
    record['exit_code'] = process.returncode
    for key, data in [('stdout', process.stdout), ('stderr', process.stderr)]:
        (args.out / (key + '.txt')).write_bytes(data)
        record[key + '_bytes'] = len(data)
        record[key + '_sha256'] = hashlib.sha256(data).hexdigest()
    record['all_prechecked_frozen_bytes_unchanged'] = all(
        (args.runtime / v['path']).stat().st_size == v['size']
        and sha(args.runtime / v['path']) == v['sha256'] for v in inputs)
    (args.out / 'execution.json').write_text(json.dumps(record, indent=2) + '\n')
    assert process.returncode == 0 and not process.stderr
    assert record['all_prechecked_frozen_bytes_unchanged']
    result = json.loads(process.stdout)
    assert set(result) == {'scope', 'coefficient_comparisons', 'types_including_K',
                           'old_point_negative_rows'}
    assert result['coefficient_comparisons'] == 14 * (64 * 7 * 7 + 1) == 43918
    assert result['types_including_K'] == 3137
    assert result['old_point_negative_rows'] == independent_negatives
    comparison = {
        'status': 'PASS', 'scope': 'Original author output matched the finite domain and the two exact negative split-point slacks in the earlier new independent audit; no new independent full graph.',
        'original_output_fields': result,
        'prior_independent_slacks_file': 'cross-source-graph-program/added-row-slacks.json',
        'prior_independent_slacks_sha256': sha(evidence / 'cross-source-graph-program/added-row-slacks.json'),
        'all_four_output_fields_checked': True,
        'all_fourteen_slacks_printed_by_original': False,
        'two_negative_values_match_independent_audit': True,
        'current_original_runs': 1,
    }
    (args.out / 'comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    print(json.dumps({'exit_code': process.returncode,
                      'coefficient_comparisons': result['coefficient_comparisons'],
                      'types_including_K': result['types_including_K'],
                      'negative_rows': result['old_point_negative_rows'],
                      'wall_seconds': record['wall_seconds'],
                      'all_frozen_bytes_unchanged': record['all_prechecked_frozen_bytes_unchanged']}, indent=2))


if __name__ == '__main__':
    main()
