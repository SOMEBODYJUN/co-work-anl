#!/usr/bin/env python3
"""Replay the three unchanged exact audits into a fresh directory.

Only Python's standard library is required. The original ten source hashes are
verified first. Frozen evidence is never overwritten. Finite checks do not prove
the real-parameter theorems or extend their structural hypotheses.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True,
                    help='A new directory; an existing directory is refused')
    args = ap.parse_args()
    base = Path(__file__).resolve().parent
    for item in json.loads((base / 'source-manifest.json').read_text()):
        assert digest(base / 'original' / item['path']) == item['sha256'], item['path']
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    audit = base / 'original/tests/audits/weighted_congestion'
    specs = [
        ('incidence-author', 'verify_incidence_forest.py',
         'incidence_forest/author.json'),
        ('incidence-independent', 'independent_incidence_forest.py',
         'incidence_forest/independent.json'),
        ('directed-fanout', 'verify_directed_fanout_forcing_cut.py',
         'directed_fanout_forcing_cut_audit.json'),
    ]
    rows = []
    for name, script, frozen_name in specs:
        destination = out / (name + '.json')
        command = [sys.executable, str(audit / script)]
        if name != 'incidence-independent':
            command += ['--output', str(destination)]
        proc = subprocess.run(command, cwd=base, text=True, capture_output=True)
        if proc.returncode:
            (out / (name + '.stderr.txt')).write_text(proc.stderr)
            raise SystemExit(f'{name} failed: exit {proc.returncode}')
        if name == 'incidence-independent':
            destination.write_text(proc.stdout)
        replayed = json.loads(destination.read_text())
        frozen = base / 'original/evidence/runs/weighted_congestion' / frozen_name
        rows.append({'name': name, 'command': command, 'returncode': proc.returncode,
                     'status': replayed['status'], 'frozen_sha256': digest(frozen),
                     'replay_sha256': digest(destination),
                     'byte_identical': frozen.read_bytes() == destination.read_bytes(),
                     'json_equal': json.loads(frozen.read_text()) == replayed})
    report = {'python_version': sys.version, 'scope': 'finite audits only', 'runs': rows}
    (out / 'comparison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
