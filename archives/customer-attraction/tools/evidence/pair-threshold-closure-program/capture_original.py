"""Observe one unchanged historical pair_closure.main --master --verify run.

No LP, no second matrix generator, no replacement of historical assertions.
The callback copies locals only when the original main returns successfully.
"""
from pathlib import Path
from fractions import Fraction
from hashlib import sha256
from collections import Counter
import contextlib
import io
import json
import platform
import runpy
import sys
import time


def main():
    if len(sys.argv) != 3:
        raise SystemExit('usage: capture.py runtime-root new-output-dir')
    root = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=False)
    source = root / 'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/pair_closure.py'
    expected = 'bf72caf986685f6db6ae22106cf531d2314f19cf636621136804d685ed524f91'
    assert sha256(source.read_bytes()).hexdigest() == expected
    captured = {}
    calls = Counter()

    def observe(frame, event, arg):
        if event == 'call' and frame.f_code.co_name in ('linprog', 'solve_float', 'main'):
            calls[(frame.f_code.co_filename, frame.f_code.co_name)] += 1
        if event == 'return' and frame.f_code.co_filename == str(source) and frame.f_code.co_name == 'main':
            loc = frame.f_locals
            if 'slacks' in loc:
                captured.update({k: loc[k] for k in ('old', 'vs', 'bounds', 'names', 'slacks', 'slabs', 'overlaps', 'er', 'ys', 'full', 'nz')})

    old_argv, old_path = sys.argv[:], sys.path[:]
    stdout = io.StringIO()
    started = time.time()
    sys.path.insert(0, str(source.parent))
    sys.argv = [str(source), '--master', '--verify']
    try:
        with contextlib.redirect_stdout(stdout):
            sys.setprofile(observe)
            runpy.run_path(str(source), run_name='__main__')
    finally:
        sys.setprofile(None)
        effective_argv = sys.argv[:]
        sys.argv, sys.path = old_argv, old_path
        (out / 'stdout.txt').write_text(stdout.getvalue())
    elapsed = time.time() - started
    assert captured, 'original main did not produce a successful verify capture'
    names, slacks = captured['names'], captured['slacks']
    assert len(names) == len(slacks) == 10344
    assert captured['nz'] == 364 and len(captured['overlaps']) == 2528
    assert not any(name in ('linprog', 'solve_float') for filename, name in calls)
    generated = json.loads(json.dumps(captured['vs']))
    saved = [{k: v for k, v in x.items() if k != 'weight'} for x in captured['er']['variables']]
    assert generated == saved
    boundaries = [('old_affine', 0, 5108), ('Z_to_Z', 5108, 5168), ('PAIR_RZ', 5168, 5228), ('PAIR_ZZ', 5228, 5288), ('overlap_upper', 5288, 10344)]
    sections = {}
    for name, begin, end in boundaries:
        values = slacks[begin:end]
        sections[name] = {'begin_inclusive': begin, 'end_exclusive': end, 'rows': len(values), 'minimum': str(min(values)), 'zero': sum(x == 0 for x in values), 'positive': sum(x > 0 for x in values), 'negative': sum(x < 0 for x in values)}
    rows = [{'index': i, 'name': name, 'slack': str(value)} for i, (name, value) in enumerate(zip(names, slacks))]
    (out / 'all-row-slacks.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    imports = []
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            p = Path(filename).resolve()
            if p.is_relative_to(root) and p.is_file():
                data = p.read_bytes()
                imports.append({'path': str(p.relative_to(root)), 'size': len(data), 'sha256': sha256(data).hexdigest()})
    report = {
        'status': 'PASS_UNCHANGED_ORIGINAL_MASTER_VERIFY_WITH_PASSIVE_RETURN_CAPTURE',
        'scope': 'One original generator and exact verifier, at changed Z from pair_master_exact; not an independent second matrix generator or SPE certificate.',
        'entrypoint': str(source.relative_to(root)), 'input_argv': ['--master', '--verify'],
        'effective_argv': effective_argv[1:], 'elapsed_seconds': elapsed,
        'python': platform.python_version(), 'source_sha256': expected,
        'wrapper_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'point_sha256': sha256((source.parent / 'pair_master_exact.json').read_bytes()).hexdigest(),
        'fixed_master_sha256': sha256((source.parent / 'combined_branch_master_exact.json').read_bytes()).hexdigest(),
        'row_sections': sections, 'rows': len(slacks), 'slabs': len(captured['slabs']),
        'Z_variables': captured['nz'], 'overlap_variables': len(captured['overlaps']),
        'all_364_saved_metadata_equal_current_generated_order': True,
        'all_Z_bounds_passed_by_original': True, 'minimum_slack': str(min(slacks)),
        'W_printed_from_fixed_master': captured['old']['W'],
        'original_main_calls': sum(count for (filename, name), count in calls.items() if filename == str(source) and name == 'main'),
        'linprog_or_solve_float_calls': 0, 'imported_runtime_modules': sorted(imports, key=lambda x: x['path']),
        'stdout_sha256': sha256((out / 'stdout.txt').read_bytes()).hexdigest(),
        'all_row_slacks_sha256': sha256((out / 'all-row-slacks.json').read_bytes()).hexdigest(),
    }
    (out / 'run-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(stdout.getvalue(), end='')
    print(json.dumps({k: report[k] for k in ('status', 'elapsed_seconds', 'row_sections', 'original_main_calls', 'linprog_or_solve_float_calls')}, indent=2))


if __name__ == '__main__':
    main()
