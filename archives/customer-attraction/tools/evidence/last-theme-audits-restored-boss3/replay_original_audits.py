"""Replay the two frozen audits once each in their required relative layout.

The evidence directory contains original/<source-id>/<basename>, the four
canonical customer_attraction modules under dependencies/, and the unchanged
cascade implementation under related-original/.  Output directories must be new.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--evidence', type=Path, required=True)
    ap.add_argument('--runtime', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    a.runtime.mkdir(parents=True, exist_ok=False)
    a.output.mkdir(parents=True, exist_ok=False)
    rel = Path('research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/counterexample')
    dest = a.runtime / rel
    dest.mkdir(parents=True)
    expected = json.loads((a.evidence / 'source-manifest.json').read_text())
    dependency_rows = json.loads((a.evidence / 'dependency-manifest.json').read_text())
    for row in expected:
        original = a.evidence / 'original' / row['id'] / Path(row['path']).name
        assert original.stat().st_size == row['size'] and sha(original) == row['sha256']
        if original.suffix == '.py':
            shutil.copy2(original, dest / original.name)
    for row in dependency_rows:
        source = a.evidence / row['evidence_path']
        assert source.stat().st_size == row['size'] and sha(source) == row['sha256']
        target = a.runtime / row['runtime_path']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    pairs = [
        ('last_theme_containment_audit.py', 'bdbe93a9ea1b9f5fcac3', 'last_theme_containment_audit.json'),
        ('last_theme_residual_refinement_audit.py', '069cde4ed129907397f7', 'last_theme_residual_refinement_audit.json'),
    ]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    events = []
    for script, report_id, report in pairs:
        started = time.time()
        tick = time.monotonic()
        process = subprocess.run([sys.executable, '-B', str(dest / script)], cwd=a.runtime,
                                 env=env, capture_output=True)
        elapsed = time.monotonic() - tick
        stem = Path(script).stem
        (a.output / (stem + '.stdout')).write_bytes(process.stdout)
        (a.output / (stem + '.stderr')).write_bytes(process.stderr)
        old = a.evidence / 'original' / report_id / report
        event = {
            'script': str(rel / script), 'script_sha256': sha(dest / script),
            'started_unix': started, 'elapsed_seconds': elapsed,
            'exit_code': process.returncode, 'stdout_bytes': len(process.stdout),
            'stdout_sha256': hashlib.sha256(process.stdout).hexdigest(),
            'stderr_bytes': len(process.stderr),
            'stderr_sha256': hashlib.sha256(process.stderr).hexdigest(),
            'frozen_report_sha256': sha(old),
            'stdout_equals_frozen_report': process.stdout == old.read_bytes(),
            'python': platform.python_version(), 'assertions_enabled': __debug__,
            'numpy': importlib.metadata.version('numpy'),
            'scipy': importlib.metadata.version('scipy'),
            'original_entry_runs_for_this_event': 1,
        }
        events.append(event)
        (a.output / 'events.json').write_text(json.dumps(events, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(event, ensure_ascii=False), flush=True)
        assert process.returncode == 0, 'Original audit failed; stop without retry.'
        parsed = json.loads(process.stdout)
        (a.output / (stem + '.parsed.json')).write_text(json.dumps(parsed, ensure_ascii=False, indent=2) + '\n')
        assert event['stdout_equals_frozen_report'], 'Keep mismatch as evidence; do not silently replace.'
    print(json.dumps({'original_cli_runs': 2, 'all_byte_equal': True}, ensure_ascii=False))


if __name__ == '__main__':
    main()
