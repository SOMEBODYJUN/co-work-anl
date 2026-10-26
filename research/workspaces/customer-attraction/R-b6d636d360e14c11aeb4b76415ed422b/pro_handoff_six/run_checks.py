"""Optional portable replays in an isolated temporary copy of the source."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
A = 'research/workspaces/customer-attraction/'
NEW = A + 'R-a8ee6fdb155c47da95540775b4a6a2db/'
ZERO = A + 'R-23ab27f8efb44f1faca2699d45886250/general_n/'
FIVE = 'customer_attraction/proofs/half5_exact_v1/'
NAMES = ('half5-local', 'half5-main', 'zero-reset', 'suffix-envelope',
         'joint-atoms', 'root-extension')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', nargs='+', choices=NAMES)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    results = []
    with tempfile.TemporaryDirectory(prefix='cag-six-replay-') as temp:
        source = Path(temp) / 'source'
        shutil.copytree(ROOT / 'source', source)
        jobs = {
            'half5-local': ([FIVE + 'components/verify_local_components.py'], source),
            'half5-main': ([FIVE + 'verify_certificate.py', '--manifest',
                            FIVE + 'row_manifest.json', '--output',
                            str(Path(temp) / 'half5-main.json')], source),
            'zero-reset': ([ZERO + 'independent_zero_source.py'], source),
            'suffix-envelope': ([NEW + 'parent/verify_suffix_envelope.py'], source),
            'joint-atoms': ([NEW + 'closure/verify_joint_atoms.py'], source),
            'root-extension': ([NEW + 'closure/root_extension.py', '--verify'], source),
        }
        env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
                   PYTHONDONTWRITEBYTECODE='1')
        env['PYTHONPATH'] = str(source)
        for name in args.only or NAMES:
            command, cwd = jobs[name]
            start = time.monotonic()
            print('Running ' + name, flush=True)
            completed = subprocess.run([sys.executable, *command], cwd=cwd,
                                       env=env, text=True, capture_output=True)
            record = {'name': name, 'returncode': completed.returncode,
                      'seconds': round(time.monotonic() - start, 3),
                      'stdout': completed.stdout, 'stderr': completed.stderr}
            results.append(record)
            print(json.dumps({k: v for k, v in record.items()
                              if k not in ('stdout', 'stderr')}), flush=True)
            if completed.returncode:
                print(completed.stdout)
                print(completed.stderr, file=sys.stderr)
                break
    passed = len(results) == len(args.only or NAMES) and all(
        row['returncode'] == 0 for row in results)
    report = {'status': 'PASS' if passed else 'FAIL',
              'scope': 'portable replay of the named original checks; no new independent proof implementation; six-person half remains OPEN',
              'results': results}
    if args.output:
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'checks': len(results)}))
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
