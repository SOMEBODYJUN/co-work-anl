"""Record the actual argv, immutable inputs, stdout/stderr, and output hashes."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = HERE.parents[3]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def entry(path):
    return {'path': str(path.relative_to(REPO)), 'sha256': digest(path),
            'bytes': path.stat().st_size}


def main():
    sources = [BASE/'peer_augmented_lp/augmented_lp_exact.json',
               BASE/'root_old_tail_joint/joint_completion_exact.json',
               BASE/'root_old_tail_joint/input_snapshot_exact.json',
               BASE/'cross_root_pricing/joint_completion_exact.json',
               BASE/'cross_root_pricing/projection_inputs_exact.json',
               BASE/'background_five_bridge/fixed53_b0_profit.json',
               BASE/'background_five_bridge/fixed53_b1_profit.json']
    before = [entry(p) for p in sources]
    runs = []
    jobs = [('interface.py', ['previous_witness_28_exact.json']),
            ('extend_certificate.py', ['inputs_exact.json', 'joint_completion_exact.json']),
            ('verify_completion.py', ['independent_audit.json'])]
    for script, outputs in jobs:
        argv = [sys.executable, str((HERE/script).relative_to(REPO))]
        start = time.monotonic()
        proc = subprocess.run(argv, cwd=REPO, capture_output=True, text=True)
        stdout = HERE/(Path(script).stem+'_stdout.txt')
        stderr = HERE/(Path(script).stem+'_stderr.txt')
        stdout.write_text(proc.stdout)
        stderr.write_text(proc.stderr)
        run = {'argv': argv, 'cwd': str(REPO), 'returncode': proc.returncode,
               'elapsed_seconds': time.monotonic()-start,
               'script': entry(HERE/script),
               'stdout': entry(stdout), 'stderr': entry(stderr),
               'outputs': [entry(HERE/o) for o in outputs if (HERE/o).exists()]}
        runs.append(run)
        print(proc.stdout, end='')
        if proc.returncode:
            print(proc.stderr, file=sys.stderr)
            break
    assert [entry(p) for p in sources] == before
    report = {'scope': 'Local exact extension and independent verification only; no optimization or pricing executed.',
              'actual_argv': [sys.executable, *sys.argv], 'cwd': str(REPO),
              'inputs': before,
              'sources': [entry(HERE/s) for s, _ in jobs]+[entry(Path(__file__))],
              'runs': runs,
              'all_successful': len(runs) == len(jobs) and all(r['returncode'] == 0 for r in runs)}
    (HERE/'execution_manifest.json').write_text(json.dumps(report, indent=2)+'\n')
    assert report['all_successful']


if __name__ == '__main__':
    main()
