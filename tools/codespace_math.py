"""Run a useful registered computation and checkpoint its complete delivery.

This works in any existing Python environment. Codespaces are optional; normal
batch computations can use the separate explicit Actions request route.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from compute import DEFAULT_MANIFEST, run as run_experiment
from curation import _safe_path


def _json_stdout(value: str):
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return None


def _publish_paths(root: Path, paths):
    """Declare exact outgoing paths without broadening historical deletions."""
    branch = subprocess.run(['git', 'branch', '--show-current'], cwd=root,
                            capture_output=True, text=True, check=False).stdout.strip()
    if not branch:
        return list(paths)
    remote = f'origin/{branch}'
    if subprocess.run(['git', 'rev-parse', '--verify', remote], cwd=root,
                      capture_output=True, text=True, check=False).returncode:
        return list(paths)
    commits = subprocess.run(['git', 'rev-list', '--reverse', f'{remote}..HEAD'],
                             cwd=root, capture_output=True, text=True, check=False)
    selected = set(paths)
    for commit in commits.stdout.splitlines():
        names = subprocess.run(['git', 'diff-tree', '--root', '--no-commit-id',
                                '--no-renames', '--name-only', '-r', '-z', commit],
                               cwd=root, capture_output=True, check=True).stdout
        selected.update(name.decode() for name in names.split(b'\0') if name)
    return sorted(selected)


def _checkpoint(root: Path, paths, message: str, local_only: bool):
    # Local preservation must remain possible before authentication succeeds.
    if local_only:
        command = [sys.executable, str(root / 'tools' / 'checkpoint.py'),
                   '--repo', str(root), *paths, '-m', message, '--local-only']
    else:
        command = [sys.executable, str(root / 'work.py'), '--repo', str(root),
                   'checkpoint', *_publish_paths(root, paths), '--publish-only', '-m', message]
    completed = subprocess.run(command, cwd=root, capture_output=True, text=True)
    parsed = _json_stdout(completed.stdout)
    if completed.returncode == 0 and isinstance(parsed, dict):
        return parsed
    return {'status': 'local-only', 'checkpoint_error': (completed.stderr or completed.stdout).strip()[-1200:],
            'returncode': completed.returncode}


def _computation_paths(root: Path, output: str, receipt):
    """Keep this execution's exact reproduction inputs and emitted artifacts."""
    paths = {output, receipt['manifest'], receipt['stdout_file'], receipt['stderr_file']}
    paths.update(ref['path'] for ref in receipt.get('input_files', []))
    requested = [*receipt['spec'].get('outputs', []),
                 (Path(output).parent / 'checkpoints').as_posix()]
    for name in requested:
        candidate = _safe_path(root, name)
        if candidate.is_file():
            paths.add(name)
        elif candidate.is_dir():
            paths.update(p.relative_to(root).as_posix() for p in candidate.rglob('*') if p.is_file())
        tracked = subprocess.run(['git', 'ls-files', '-z', '--', ':(literal)' + name],
                                 cwd=root, capture_output=True, check=True).stdout
        paths.update(p.decode() for p in tracked.split(b'\0') if p)
    for name in paths:
        _safe_path(root, name)
    return sorted(paths)


def run(root: Path, experiment: str, output: str, message: str | None = None,
        local_only: bool = False, manifest: str = DEFAULT_MANIFEST,
        resume_from: str | None = None):
    root = root.resolve()
    output = Path(output).as_posix()
    ignored = subprocess.run(['git', 'check-ignore', '--no-index', '-q', '--', output],
                             cwd=root, capture_output=True, check=False)
    if ignored.returncode == 0:
        raise ValueError('Checkpoint output is ignored by Git; use research/checks/ or the owning archive evidence directory')
    success = run_experiment(root, experiment, output, manifest, resume_from)
    receipt = json.loads((root / output).read_text())
    paths = _computation_paths(root, output, receipt)
    message = message or 'research compute: ' + experiment
    local = _checkpoint(root, paths, message, True)
    publication = local if local_only or not local.get('commit') else _checkpoint(root, paths, message, False)
    return {'experiment': experiment,
            'experiment_status': 'completed' if success else 'failed',
            'receipt': output, 'checkpoint_paths': paths,
            'local_checkpoint': local, 'publication': publication,
            'instruction': 'A pushed checkpoint shares the exact inputs, logs, outputs and algorithm checkpoints. Local-only preserves the run here; inspect any checkpoint_error before claiming it was committed.'}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('experiment')
    parser.add_argument('--out', required=True)
    parser.add_argument('--message')
    parser.add_argument('--local-only', action='store_true')
    parser.add_argument('--manifest', default=DEFAULT_MANIFEST)
    parser.add_argument('--resume-from')
    args = parser.parse_args()
    try:
        result = run(Path(__file__).resolve().parents[1], args.experiment, args.out,
                     args.message, args.local_only, args.manifest, args.resume_from)
    except (KeyError, OSError, ValueError) as exc:
        raise SystemExit(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['experiment_status'] == 'completed' else 1)
