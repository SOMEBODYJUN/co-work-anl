"""Run one registered computation and make its checkpoint part of the run.

This is the concrete Work/Codespaces bridge: a Solver chooses an experiment
already listed in ``research/experiments.json``; the command records the exact
execution receipt, creates a local Git checkpoint immediately, and then tries
to publish that checkpoint.  A failed push never discards the local result.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from compute import run as run_experiment


def _json_stdout(value: str):
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return None


def _publish_paths(root: Path, output: str):
    """Include every path in local-only commits before asking checkpoint.py to push.

    The checkpoint auditor deliberately refuses to publish a new receipt while
    an older local commit would travel outside the requested scope.  A normal
    Codespace run therefore publishes the whole outstanding research delta,
    while the first local leg still stages only the new receipt.
    """
    branch = subprocess.run(['git', 'branch', '--show-current'], cwd=root,
                            capture_output=True, text=True, check=False).stdout.strip()
    if not branch:
        return [output]
    remote = f'origin/{branch}'
    if subprocess.run(['git', 'rev-parse', '--verify', remote], cwd=root,
                      capture_output=True, text=True, check=False).returncode:
        return [output]
    commits = subprocess.run(['git', 'rev-list', '--reverse', f'{remote}..HEAD'],
                             cwd=root, capture_output=True, text=True, check=False)
    paths = {output}
    for commit in commits.stdout.splitlines():
        names = subprocess.run(['git', 'diff-tree', '--root', '--no-commit-id',
                                '--no-renames', '--name-only', '-r', commit],
                               cwd=root, capture_output=True, text=True, check=False)
        paths.update(name for name in names.stdout.splitlines() if name)
    # A path deleted by a local commit is still covered by its nearest existing
    # directory; checkpoint.py accepts the directory and audits the historical
    # deletion without trying to stage a nonexistent file.
    result = []
    for name in sorted(paths):
        candidate = root / name
        if candidate.exists() or subprocess.run(['git', 'ls-files', '--', name],
                                                cwd=root, capture_output=True,
                                                text=True, check=False).stdout.strip():
            result.append(name)
            continue
        parent = Path(name).parent
        while parent != Path('.') and not (root / parent).exists():
            parent = parent.parent
        result.append(parent.as_posix() if parent != Path('.') else '.')
    return list(dict.fromkeys(result))


def _checkpoint(root: Path, output: str, message: str, local_only: bool):
    # Call checkpoint.py directly for the local leg.  The top-level work.py
    # intentionally validates its configured external token before dispatching
    # any checkpoint command, while a local commit must remain possible offline.
    if local_only:
        command = [sys.executable, str(root / 'tools' / 'checkpoint.py'),
                   '--repo', str(root), output, '-m', message, '--local-only']
    else:
        command = [sys.executable, str(root / 'work.py'), '--repo', str(root),
                   'checkpoint', *_publish_paths(root, output), '-m', message]
    completed = subprocess.run(command, cwd=root, capture_output=True, text=True)
    parsed = _json_stdout(completed.stdout)
    if completed.returncode == 0 and isinstance(parsed, dict):
        return parsed
    # The receipt and local commit are intentionally retained even when the
    # remote credential or network is unavailable.
    return {'status': 'local-only', 'checkpoint_error': (completed.stderr or completed.stdout).strip()[-1200:],
            'returncode': completed.returncode}


def run(root: Path, experiment: str, output: str, message: str | None = None,
        local_only: bool = False):
    root = root.resolve()
    output = Path(output).as_posix()
    ignored = subprocess.run(['git', 'check-ignore', '--no-index', '-q', '--', output],
                             cwd=root, capture_output=True, check=False)
    if ignored.returncode == 0:
        raise ValueError('Checkpoint output is ignored by Git; use research/checks/ or the owning archive evidence directory')
    success = run_experiment(root, experiment, output)
    message = message or 'research compute: ' + experiment

    # First make a local checkpoint without depending on GitHub auth.  A
    # second invocation publishes that exact commit when credentials work.
    local = _checkpoint(root, output, message, True)
    publication = local if local_only else _checkpoint(root, output, message, False)
    return {'experiment': experiment,
            'experiment_status': 'completed' if success else 'failed',
            'receipt': output,
            'local_checkpoint': local,
            'publication': publication,
            'instruction': 'A pushed checkpoint is shared; local-only means the receipt and commit remain recoverable here.'}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('experiment')
    parser.add_argument('--out', required=True)
    parser.add_argument('--message')
    parser.add_argument('--local-only', action='store_true')
    args = parser.parse_args()
    try:
        result = run(Path(__file__).resolve().parents[1], args.experiment, args.out,
                     args.message, args.local_only)
    except (KeyError, OSError, ValueError) as exc:
        raise SystemExit(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['experiment_status'] == 'completed' else 1)
