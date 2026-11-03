#!/usr/bin/env python3
"""Replay unchanged primary entrypoints in a fresh tree; keep originals immutable."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REL = Path('research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--discovery', action='store_true')
    args = ap.parse_args()
    folder = HERE / ('replay-discovery-001' if args.discovery else 'replay-exact-001')
    folder.mkdir()
    tree = folder / 'tree'
    tree.mkdir()
    source = HERE / 'source-root'
    for path in source.rglob('*.py'):
        dest = tree / path.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
    inp = Path('evidence/certificates/customer_attraction/five_player_indexed_bound.json')
    (tree / inp).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / inp, tree / inp)
    if args.discovery:
        jobs = [
            ('low_prefix/root_D_envelope.py', [], 'root_D_envelope.json'),
            ('low_prefix/root_D_envelope.py', ['--simple'], 'root_D_simple.json'),
            ('low_prefix/root_reply_chain.py', ['--depth', '2'], 'root_reply_chain2.json'),
            ('parent/row3_relaxation.py', [], 'row3_relaxation.json'),
        ]
    else:
        jobs = [
            ('induction/audit_root_share_interface.py', [], None),
            ('induction/audit_two_prefix_interface.py', [], 'audit_two_prefix_interface.json'),
            ('parent/audit_root_share_polynomial.py', [], 'audit_root_share_polynomial.json'),
            ('parent/audit_two_prefix_from_slacks.py', [], 'audit_two_prefix_from_slacks.json'),
            ('low_prefix/audit_root_D_payment.py', [], 'audit_root_D_payment.json'),
        ]
    runs = []
    for relative, extra, report_name in jobs:
        path = tree / REL / relative
        report = path.with_name(report_name) if report_name else None
        assert report is None or not report.exists()
        began = time.time()
        result = subprocess.run([sys.executable, str(path), *extra], cwd=folder,
                                capture_output=True, text=True)
        stem = Path(relative).stem + ('-simple' if extra == ['--simple'] else '')
        (folder / (stem + '.stdout.txt')).write_text(result.stdout)
        (folder / (stem + '.stderr.txt')).write_text(result.stderr)
        event = {'entrypoint': relative, 'argv': [sys.executable, str(path), *extra],
                 'cwd': str(folder), 'start_unix': began, 'elapsed_seconds': time.time()-began,
                 'exit_code': result.returncode, 'script_sha256': sha(path),
                 'stdout_sha256': sha(folder / (stem+'.stdout.txt')),
                 'stderr_empty': not result.stderr, 'report_absent_before_run': True}
        if report is not None and report.exists():
            frozen = source / REL / Path(relative).parent / report_name
            event.update(report=str(report.relative_to(folder)), report_sha256=sha(report),
                         frozen_report_sha256=sha(frozen),
                         report_byte_equal=report.read_bytes() == frozen.read_bytes())
        runs.append(event)
        (folder / 'runs.json').write_text(json.dumps(runs, ensure_ascii=False, indent=2)+'\n')
        print(relative, extra, 'exit', result.returncode, 'equal', event.get('report_byte_equal'), flush=True)
        if result.returncode:
            raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
