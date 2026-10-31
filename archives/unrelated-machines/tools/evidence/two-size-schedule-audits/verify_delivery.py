#!/usr/bin/env python3
"""Verify preserved files and completed runs only; do not rerun entrypoints."""
import ast
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
stage = here.parents[4]
manifest = json.loads((here / 'manifest.json').read_text())
for group in ('originals', 'comparisons'):
    for row in manifest[group]:
        data = (stage / row['evidence_path']).read_bytes()
        assert len(data) == row['size']
        assert hashlib.sha256(data).hexdigest() == row['sha256']
assert sorted(p.name for p in (here / 'runs').iterdir()) == ['count-001', 'fixed-001', 'labels-001']
names = {'count': 'divisible_two_size_neutral_repair.py',
         'labels': 'divisible_two_size_neutral_independent.py',
         'fixed': 'fixed_work_convex_local_minimum.py'}
for name in ('count', 'labels', 'fixed'):
    run = here / 'runs' / (name + '-001')
    meta = json.loads((run / 'run.json').read_text())
    assert meta['exit_code'] == 0 and meta['stderr_bytes'] == 0
    assert meta['optimization_level'] == 0 and meta['entrypoint_invocations'] == 1
    assert meta['initial_directory_empty'] is True
    assert Path(meta['command'][1]).name == names[name]
    assert hashlib.sha256((here / 'original' / names[name]).read_bytes()).hexdigest() == meta['source_sha256']
    assert (run / 'stderr.txt').read_bytes() == b''
    assert hashlib.sha256((run / 'stdout.txt').read_bytes()).hexdigest() == meta['stdout_sha256']
old = json.loads((here / 'comparisons/divisible_two_size_neutral_repair_audit.json').read_text())
assert json.loads((here / 'runs/count-001/stdout.txt').read_text()) == old['runs'][0]['result']
assert ast.literal_eval((here / 'runs/labels-001/stdout.txt').read_text()) == old['runs'][1]['result']
assert (here / 'runs/fixed-001/stdout.txt').read_bytes() == (here / 'comparisons/fixed_work_convex_local_minimum_audit.json').read_bytes()
print(json.dumps({'frozen_sources_checked': 10, 'actual_new_original_entrypoints': 3,
                  'all_exit_zero_assert_enabled': True, 'neutral_results_equal_frozen': True,
                  'fixed_stdout_byte_identical': True, 'mathematical_entrypoints_rerun_by_verifier': 0},
                 ensure_ascii=False, indent=2))
