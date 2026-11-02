"""Replay the literal potential audit once; keep frozen source/output immutable."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

PACKAGE = Path('archives/customer-attraction/tools/evidence/eight-customer-static-potential-obstruction-primary')
DEPENDENCY = Path('archives/customer-attraction/tools/evidence/independent-cce-ordered-count-versions-primary')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument('--evidence-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output-dir', type=Path, required=True,
                        help='New directory outside the tracked source package.')
    args = parser.parse_args()
    repo, package, out = args.repo_root.resolve(), args.evidence_root.resolve(), args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((package/'source-manifest.json').read_text())
    originals = {}
    for source in manifest['sources']:
        relative = Path(source['preserved_path']).relative_to(PACKAGE)
        path = package/relative
        data = path.read_bytes()
        assert len(data) == source['size']
        assert sha(data) == source['sha256']
        originals[source['id']] = path

    # Reuse the existing successful sigmaC evidence; do not execute its verifier.
    dep = repo/DEPENDENCY
    dep_source = dep/'original/count_policy_cce_audit.json'
    dep_report = dep/'runs/eight-count/report.json'
    dep_event = json.loads((dep/'runs/eight-count/execution.json').read_text())
    assert dep_event['exit_code'] == 0
    assert dep_source.read_bytes() == dep_report.read_bytes()
    old_spe = json.loads(dep_report.read_text())
    assert old_spe['actual_outcome'] == [0, 1, 1]
    assert old_spe['actual_payoffs'] == ['2', '2', '2']
    assert len(old_spe['all_spe_rows']) == 21 and old_spe['comparisons'] == 84

    run = out/'unmodified-source-run'
    run.mkdir()
    program = run/'potential_bottleneck_audit.py'
    original_program = originals['59c0c5f7f7a65885c085']
    shutil.copyfile(original_program, program)
    started = datetime.now(timezone.utc).isoformat()
    before = time.monotonic()
    command = [sys.executable, '-I', str(program)]
    result = subprocess.run(command, cwd=run, capture_output=True, check=False)
    elapsed = time.monotonic()-before
    (out/'stdout.txt').write_bytes(result.stdout)
    (out/'stderr.txt').write_bytes(result.stderr)
    execution = {
        'entry': 'potential_bottleneck_audit.py', 'arguments': [],
        'command': command, 'cwd': str(run),
        'isolation': 'unmodified copy; python -I; assertions enabled; fresh clone-external directory',
        'started_utc': started, 'duration_seconds': elapsed,
        'exit_code': result.returncode, 'program_sha256': sha(program.read_bytes()),
        'stdout_sha256': sha(result.stdout), 'stderr_sha256': sha(result.stderr),
    }
    (out/'execution.json').write_text(json.dumps(execution, indent=2)+'\n')
    assert result.returncode == 0 and not result.stderr
    report_bytes = program.with_suffix('.json').read_bytes()
    (out/'report.json').write_bytes(report_bytes)
    frozen = originals['79b4b2410bad830ee158'].read_bytes()
    assert report_bytes == frozen == result.stdout
    report = json.loads(report_bytes)
    assert report['static_ordered_profiles'] == 64
    assert report['static_comparisons'] == 768
    assert len(report['all_pne']) == 12
    assert {tuple(sorted(row['profile'])) for row in report['all_pne']} == {(1,1,2),(1,1,3),(1,2,3)}
    verification = {
        'primary_source_sha256_checks': len(originals),
        'original_static_subprocess_runs': 1,
        'new_instance_searches': 0,
        'new_sigmaC_runs': 0,
        'report_byte_exact': True, 'report_json_equal': True,
        'stdout_equals_report_bytes': True,
        'static_ordered_profiles': 64, 'all_ordered_pne_count': 12,
        'potential_identity_assertions': 192,
        'reported_static_comparisons': 768,
        'reported_static_comparisons_meaning': '64*3*4 nominal candidate space. all(...) short-circuits; this is not an instrumented count of executed comparisons.',
        'sigmaC_reused_report': str(DEPENDENCY/'runs/eight-count/report.json'),
        'sigmaC_reused_report_sha256': sha(dep_report.read_bytes()),
        'sigmaC_reused_execution': str(DEPENDENCY/'runs/eight-count/execution.json'),
        'sigmaC_reused_complete_histories': 21,
        'sigmaC_reused_including_self_comparisons': 84,
        'execution': execution,
    }
    (out/'verification.json').write_text(json.dumps(verification, indent=2)+'\n')
    print(json.dumps({k:v for k,v in verification.items() if k!='execution'}, indent=2))


if __name__ == '__main__':
    main()
