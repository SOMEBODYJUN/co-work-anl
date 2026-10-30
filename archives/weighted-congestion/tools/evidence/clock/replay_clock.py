"""Replay frozen standard-library clock audits into a fresh directory.

The default is a new `replay-new` directory beside this script. Existing
outputs are never overwritten. This runner is an implementation resource,
not an additional mathematical test or general proof.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

PAIRS = [
    ('verify_lift', 'lift'), ('independent_lift', 'independent_lift'),
    ('independent_actual_clock_certificate', 'independent_actual_clock_certificate'),
    ('independent_clock_degree_barrier', 'independent_clock_degree_barrier'),
    ('independent_clock_margin_padding', 'independent_clock_margin_padding'),
    ('verify_actual_clock_margins', 'actual_clock_margins'),
    ('independent_actual_clock_geometry', 'independent_actual_clock_geometry'),
    ('verify_clock_margin_padding', 'clock_margin_padding'),
    ('verify_clock_degree_barrier', 'clock_degree_barrier'),
    ('verify_clock_compiler', 'cycle_lock_triad'), ('independent_clock', 'independent_clock'),
    ('verify_uniform_clock_budget', 'uniform_clock_budget'),
    ('independent_uniform_clock_budget', 'independent_uniform_clock_budget'),
    ('verify_full_uniform_clock', 'full_uniform_clock_degree80'),
    ('independent_full_uniform_clock', 'independent_full_uniform_clock_degree80'),
    ('verify_cycle_certificate', 'cycle_certificate'),
]
REQUIRES_OUTPUT = {'independent_lift', 'independent_clock'}
METADATA = {'python', 'python_version', 'command', 'invocation', 'environment',
            'canonical_manuscript_sha256'}

def unwrap(report):
    return report['result'] if isinstance(report.get('result'), dict) and 'source_sha256' in report else report

def differences(a, b, path=''):
    if type(a) is not type(b):
        return [dict(path=path, frozen=a, replay=b)]
    if isinstance(a, dict):
        rows = []
        for key in sorted(set(a) | set(b)):
            if key not in a or key not in b:
                rows.append(dict(path=path+'/'+key, frozen=a.get(key), replay=b.get(key)))
            else:
                rows.extend(differences(a[key], b[key], path+'/'+key))
        return rows
    if isinstance(a, list):
        if len(a) != len(b):
            return [dict(path=path, frozen_length=len(a), replay_length=len(b))]
        return [row for i, (left, right) in enumerate(zip(a, b))
                for row in differences(left, right, path+'/'+str(i))]
    return [] if a == b else [dict(path=path, frozen=a, replay=b)]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    target = args.output_dir.resolve() if args.output_dir else root/'replay-new'
    target.mkdir(parents=True, exist_ok=False)
    results = []
    for program, frozen_name in PAIRS:
        script = root/'original/tests/audits/weighted_congestion/cyclic_clone'/(program+'.py')
        output = target/(program+'.json')
        command = [sys.executable, str(script)]
        if program in REQUIRES_OUTPUT:
            command += ['--output', str(output)]
        result = subprocess.run(command, cwd=root, capture_output=True, text=True)
        (target/(program+'.stderr')).write_text(result.stderr)
        if program in REQUIRES_OUTPUT:
            (target/(program+'.stdout')).write_text(result.stdout)
        else:
            output.write_text(result.stdout)
        if result.returncode:
            raise RuntimeError(f'{program} exited {result.returncode}: {result.stderr}')
        old = unwrap(json.loads((root/'original/evidence/runs/weighted_congestion/cyclic_clone'/(frozen_name+'.json')).read_text()))
        new = unwrap(json.loads(output.read_text()))
        all_diff = differences(old, new)
        math_diff = [r for r in all_diff if r['path'].split('/')[1] not in METADATA]
        results.append(dict(program=program, exit_code=result.returncode,
                            command=command, source_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
                            output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                            all_differences=all_diff, mathematical_differences=math_diff))
    report = dict(python=sys.version, programs=results,
                  all_mathematical_outputs_match=all(not row['mathematical_differences'] for row in results))
    (target/'comparison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(output_dir=str(target), programs=len(results),
                          all_mathematical_outputs_match=report['all_mathematical_outputs_match'])))
    if not report['all_mathematical_outputs_match']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
