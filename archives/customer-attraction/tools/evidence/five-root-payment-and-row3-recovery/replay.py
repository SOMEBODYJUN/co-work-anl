#!/usr/bin/env python3
"""Replay reviewed frozen source bytes in a fresh tree; never seed output files."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
N5 = Path('research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5')
OLD = HERE.parent / 'five-prefix-interface-and-root-D-primary' / 'source-root'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', default='replay-001')
    ap.add_argument('--all-discovery', action='store_true')
    args = ap.parse_args()
    folder = HERE / args.run_dir
    folder.mkdir()
    tree = folder / 'tree'
    tree.mkdir()
    jobs = [('low_prefix/audit_root_D_payment.py', [], 'audit_root_D_payment.json')]
    if args.all_discovery:
        jobs += [('low_prefix/root_D_envelope.py', [], 'root_D_envelope.json'),
                 ('low_prefix/root_D_envelope.py', ['--simple'], 'root_D_simple.json'),
                 ('low_prefix/root_reply_chain.py', ['--depth', '2'], 'root_reply_chain2.json'),
                 ('parent/row3_relaxation.py', [], 'row3_relaxation.json')]
    scripts = {x[0] for x in jobs}
    for relative in scripts:
        dest = tree / N5 / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(OLD / N5 / relative, dest)
    inp = Path('evidence/certificates/customer_attraction/five_player_indexed_bound.json')
    (tree / inp).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OLD / inp, tree / inp)
    events = []
    for relative, extra, reportname in jobs:
        script = tree / N5 / relative
        report = script.with_name(reportname)
        assert not report.exists()
        argv = [sys.executable, str(script), *extra]
        began = time.time()
        process = subprocess.run(argv, cwd=folder, capture_output=True, text=True)
        label = Path(relative).stem + ('-simple' if extra == ['--simple'] else '')
        stdout = folder / (label + '.stdout.txt')
        stderr = folder / (label + '.stderr.txt')
        stdout.write_text(process.stdout)
        stderr.write_text(process.stderr)
        event = dict(entrypoint=relative, argv=argv, cwd=str(folder),
                     start_unix=began, elapsed_seconds=time.time()-began,
                     exit_code=process.returncode, script_sha256=digest(script),
                     report_absent_before_run=True, stderr_empty=not process.stderr,
                     stdout_sha256=digest(stdout), stderr_sha256=digest(stderr))
        if report.exists():
            frozen = OLD / N5 / Path(relative).parent / reportname
            event.update(report=str(report.relative_to(HERE)),
                         report_sha256=digest(report), frozen_report_sha256=digest(frozen),
                         report_byte_equal=report.read_bytes() == frozen.read_bytes())
        events.append(event)
        (folder/'runs.json').write_text(json.dumps(events, ensure_ascii=False, indent=2)+'\n')
        print(relative, extra, process.returncode, event.get('report_byte_equal'), flush=True)
        if process.returncode:
            raise SystemExit(process.returncode)


if __name__ == '__main__':
    main()
