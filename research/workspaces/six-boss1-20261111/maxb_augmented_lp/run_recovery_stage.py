"""Record exact postprocessing stages on one preserved discovery array.

This driver never calls an optimizer. It retains the actual source and
dependency hashes, stdout, stderr, and exit code even when recovery fails.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import json
import os
import platform
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['sameW', 'freeW', 'dual', 'verify'])
    parser.add_argument('--output', default='recovery')
    args = parser.parse_args()
    out = (HERE / args.output).resolve()
    assert out.is_relative_to(HERE) and out != HERE and out.is_dir()
    record_path = out / ('execution_' + args.stage + '.json')
    assert not record_path.exists(), 'Each labeled recovery stage is retained once.'
    if args.stage == 'verify':
        source = HERE / 'verify_certificates.py'
        argv = [sys.executable, '-B', str(source), '--output', str(out)]
        dependency = [source, HERE / 'exact_matrix.json.gz', out / 'augmented_lp_exact.json', out / 'exact_dual_certificate.json']
    else:
        source = out / 'recover.py'
        argv = [sys.executable, '-B', str(source), args.stage]
        dependency = [source, out / 'recovery_model.py', out / 'exact_matrix.json.gz', out / 'floating_solver_arrays.npz',
                      out / 'epigraph_structure.json', out / 'zz_envelope_structure.json', out / 'inherited_dual_lower_bound.json']
        if args.stage == 'dual':
            dependency += [out / 'augmented_lp_exact.json', out / 'primal_exact_audit.json']
    snapshots = out / 'executed_sources'
    snapshots.mkdir(exist_ok=True)
    for p in dependency:
        if p.suffix == '.py':
            snapshot = snapshots / (p.stem + '_' + sha(p) + '.py')
            if not snapshot.exists():
                snapshot.write_bytes(p.read_bytes())
    record = {'argv': argv, 'cwd': str(REPO), 'stage': args.stage,
              'source_sha256': sha(source), 'driver_sha256': sha(Path(__file__)),
              'dependency_sha256': {str(p.relative_to(HERE)): sha(p) for p in dependency},
              'python': platform.python_version(), 'started_utc': datetime.now(timezone.utc).isoformat(),
              'optimizer_calls': 0, 'exact_elimination_limit_seconds': 600}
    stdout = out / (args.stage + '_stdout.txt')
    stderr = out / (args.stage + '_stderr.txt')
    started = time.monotonic()
    with stdout.open('w') as f, stderr.open('w') as g:
        process = subprocess.run(argv, cwd=REPO, stdout=f, stderr=g,
                                 env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'MAXB_EXACT_TIME_LIMIT': '600'})
    record.update(exit_code=process.returncode, elapsed_seconds=time.monotonic() - started,
                  finished_utc=datetime.now(timezone.utc).isoformat(), stdout_sha256=sha(stdout), stderr_sha256=sha(stderr),
                  status='SUCCESS' if process.returncode == 0 else 'FAILED_ALL_EVIDENCE_RETAINED')
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(record, ensure_ascii=False, indent=2), flush=True)
    raise SystemExit(process.returncode)


if __name__ == '__main__':
    main()
