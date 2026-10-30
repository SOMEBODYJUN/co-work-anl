#!/usr/bin/env python3
"""Replay preserved Fraction audits into a new directory; never rewrite originals."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    original = base / 'original'
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    tasks = [
        ('mixture-author', original / 'tests/audits/weighted_congestion/ordinal_potentials/verify_common_power_mixture.py', []),
        ('mixture-independent', original / 'tests/audits/weighted_congestion/ordinal_potentials/independent_common_power_mixture.py', []),
        ('affine-two-type', original / 'tests/audits/weighted_congestion/power_bridge/verify_affine_two_type.py', []),
        ('resource-bridge', original / 'tests/audits/weighted_power_bridge.py', ['--output', str(out / 'resource-bridge.json')]),
        ('path-review-restored', base / 'restored_path_review_code.py', []),
    ]
    records = []
    for name, program, extra in tasks:
        command = [sys.executable, str(program), *extra]
        result = subprocess.run(command, cwd=original, capture_output=True, text=True)
        (out / (name + '.stdout')).write_text(result.stdout)
        (out / (name + '.stderr')).write_text(result.stderr)
        records.append({'name': name, 'command': command, 'exit_code': result.returncode,
                        'code_sha256': hashlib.sha256(program.read_bytes()).hexdigest()})
        (out / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
        print(name, result.returncode, flush=True)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
