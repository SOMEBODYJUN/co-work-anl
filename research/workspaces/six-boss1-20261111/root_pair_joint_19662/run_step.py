"""Record an actually executed owned script, its exact argv, files and exit."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    script = sys.argv[1]
    assert script in ('discover.py', 'recover.py', 'verify_completion.py', 'source_audit.py')
    argv = [sys.executable, '-B', str(HERE/script), *sys.argv[2:]]
    output = HERE/(Path(script).stem+'_stdout.txt')
    errors = HERE/(Path(script).stem+'_stderr.txt')
    started = time.time()
    proc = subprocess.run(argv, cwd=REPO, capture_output=True, text=True)
    output.write_text(proc.stdout)
    errors.write_text(proc.stderr)
    manifest_path = HERE/'execution_manifest.json'
    old = json.loads(manifest_path.read_text()) if manifest_path.exists() else {'runs': []}
    owned = [{'path': str(p.relative_to(REPO)), 'sha256': digest(p)}
             for p in sorted(HERE.iterdir()) if p.is_file() and p != manifest_path]
    inputs = []
    source = HERE/'inputs_exact.json'
    if source.exists():
        inputs = json.loads(source.read_text())['sources']
    old['runs'].append({'actual_argv': argv, 'cwd': str(REPO), 'exit_code': proc.returncode,
        'started_unix': started, 'elapsed_seconds': time.time()-started,
        'script_sha256': digest(HERE/script), 'runner_sha256': digest(__file__),
        'read_only_source_bindings': inputs,
        'stdout': {'path': str(output.relative_to(REPO)), 'sha256': digest(output)},
        'stderr': {'path': str(errors.relative_to(REPO)), 'sha256': digest(errors)},
        'owned_files_after_execution': owned})
    manifest_path.write_text(json.dumps(old, indent=2)+'\n')
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    raise SystemExit(proc.returncode)


if __name__ == '__main__':
    main()
