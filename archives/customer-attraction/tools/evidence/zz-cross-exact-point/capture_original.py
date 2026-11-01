"""One unchanged original cross verifier with passive return observation."""
from pathlib import Path
from fractions import Fraction as F
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
        raise SystemExit('usage: capture.py runtime-root new-event-output')
    root, out = map(lambda s: Path(s).resolve(), sys.argv[1:])
    out.mkdir(parents=True, exist_ok=False)
    folder = root / 'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5'
    src = folder / 'zz_threshold_closure.py'
    inputs = {
        'zz_threshold_closure.py': '959d52f297152b1f2ae5e07834c56ed94f87a5cef0cf252acf2a2d0071a0b7eb',
        'zz_cross_exact.json': '239ab62a100cd77f12cc9b8d131048e87babccb2103c781953af33909c364111',
        'cross_source_priced_optimum_exact.json': '955c456ad3381a8cdc72139ba9ccc73dfe70297183e72727ae6ad165dc80e947',
    }
    for name, digest in inputs.items():
        assert sha256((folder / name).read_bytes()).hexdigest() == digest
    captured, calls = {}, Counter()
    def observe(frame, event, arg):
        if event == 'call' and frame.f_code.co_name in ('main', 'linprog'):
            calls[frame.f_code.co_filename, frame.f_code.co_name] += 1
        if event == 'return' and frame.f_code.co_filename == str(src) and frame.f_code.co_name == 'main' and 'slacks' in frame.f_locals:
            captured.update({k: frame.f_locals[k] for k in ('old', 'vs', 'bounds', 'names', 'cols', 'base', 'mapping', 'report', 'ys', 'slacks')})
    stdout = io.StringIO()
    saved_argv, saved_path = sys.argv[:], sys.path[:]
    sys.argv = [str(src), '--cross', '--priced', '--optimum', '--verify']
    sys.path.insert(0, str(folder))
    start = time.time()
    try:
        with contextlib.redirect_stdout(stdout):
            sys.setprofile(observe)
            runpy.run_path(str(src), run_name='__main__')
    finally:
        sys.setprofile(None)
        argv = sys.argv[1:]
        sys.argv, sys.path = saved_argv, saved_path
        (out / 'stdout.txt').write_text(stdout.getvalue())
    elapsed = time.time() - start
    assert captured and len(captured['slacks']) == 4987 and len(captured['ys']) == 302
    assert json.loads(json.dumps(captured['vs'])) == [{k: v for k, v in z.items() if k != 'weight'} for z in captured['report']['variables']]
    assert not any(name == 'linprog' for filename, name in calls)
    slacks = captured['slacks']
    row_records = [{'index': i, 'name': n, 'slack': str(s)} for i, (n, s) in enumerate(zip(captured['names'], slacks))]
    (out / 'all-row-slacks.json').write_text(json.dumps(row_records, ensure_ascii=False, indent=2) + '\n')
    # Evaluate the already-built affine map, not another constraint generator.
    lifted = [b + sum((q * captured['ys'][j] for j, q in mm), F()) for b, mm in zip(captured['base'], captured['mapping'])]
    (out / 'affine-lifted-weights.json').write_text(json.dumps([str(y) for y in lifted], indent=2) + '\n')
    sections = {}
    for name, left, right in [('old_cross_affine', 0, 4927), ('Z_to_Z', 4927, 4987)]:
        part = slacks[left:right]
        sections[name] = {'begin': left, 'end_exclusive': right, 'rows': len(part), 'minimum': str(min(part)), 'positive': sum(y > 0 for y in part), 'zero': sum(y == 0 for y in part), 'negative': sum(y < 0 for y in part)}
    imports = []
    for mod in list(sys.modules.values()):
        path = getattr(mod, '__file__', None)
        if path:
            p = Path(path).resolve()
            if p.is_relative_to(root) and p.is_file():
                b = p.read_bytes()
                imports.append({'path': str(p.relative_to(root)), 'bytes': len(b), 'sha256': sha256(b).hexdigest()})
    for name, digest in inputs.items():
        assert sha256((folder / name).read_bytes()).hexdigest() == digest
    result = {
        'status': 'PASS_UNCHANGED_ORIGINAL_ZZ_CROSS_PRICED_OPTIMUM_VERIFY',
        'scope': 'Original 4987-row generator/verifier at this new Z; passive main-return capture. Not a second independent matrix implementation or SPE certificate.',
        'python': platform.python_version(), 'effective_argv': argv, 'elapsed_seconds': elapsed,
        'entrypoint': str(src.relative_to(root)), 'input_hashes_before_and_after': inputs,
        'capture_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'original_main_calls': calls[str(src), 'main'], 'linprog_calls': 0,
        'variables': len(captured['ys']), 'all_saved_descriptors_match_generated_order': True,
        'sections': sections, 'total_rows': len(slacks), 'minimum_slack': str(min(slacks)),
        'W_printed_from_fixed_source': captured['old']['W'],
        'actual_imported_runtime_modules': sorted(imports, key=lambda x: x['path']),
        'artifacts': {p.name: {'bytes': p.stat().st_size, 'sha256': sha256(p.read_bytes()).hexdigest()} for p in out.iterdir() if p.is_file()},
    }
    (out / 'execution.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(stdout.getvalue(), end='')
    print(json.dumps({k: result[k] for k in ('status', 'elapsed_seconds', 'original_main_calls', 'linprog_calls', 'sections')}, indent=2))


if __name__ == '__main__':
    main()
