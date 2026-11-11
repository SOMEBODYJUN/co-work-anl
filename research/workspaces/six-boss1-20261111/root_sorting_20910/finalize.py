"""Freeze the completed finite obligation without modifying cloud inputs."""
from pathlib import Path
from datetime import datetime, timezone
import gzip
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = HERE.parents[3]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(p):
    if str(p).endswith('.gz'):
        with gzip.open(p, 'rt') as f:
            return json.load(f)
    return json.loads(Path(p).read_text())


def write(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')


def main():
    model = read(HERE/'symbolic_matrix_exact.json.gz')
    certificate = read(HERE/'root_completion_exact.json.gz')
    audit = read(HERE/'primal_independent_audit.json')
    assert audit['status'] == 'INDEPENDENT_EXACT_ROOT_SORTING_COMPLETION_PASS'
    assert audit['certificate_sha256'] == sha(HERE/'root_completion_exact.json.gz')
    assert audit['matrix_sha256'] == certificate['matrix_sha256'] == sha(HERE/'symbolic_matrix_exact.json.gz')
    request = read(HERE/'actions_request.json')
    for item in request['required_inputs']:
        assert sha(REPO/item['path']) == item['sha256']
    download_path = BASE/'compute_dispatch/root-sorting-download-input-audit.json'
    download = read(download_path)
    assert download['status'] == 'DOWNLOADED_INPUTS_AND_BYTE_IDENTICAL_OUTPUTS_VERIFIED'
    for item in download['runtime_outputs']:
        assert sha(REPO/item['path']) == item['sha256']
    prephase = read(HERE/'freeze_prephase_manifest.json')
    historic = {
        str((HERE/'execution_manifest.json').relative_to(REPO)): HERE/'prephase_execution_manifest.json',
        str(HERE.with_suffix('.md').relative_to(REPO)): HERE/'prephase_report.md',
    }
    for item in prephase['artifacts']:
        target = historic.get(item['path'], REPO/item['path'])
        assert sha(target) == item['sha256'], item['path']
    for source in model['sources']:
        assert sha(BASE/source['path']) == source['sha256']
    analysis = read(HERE/'completion_analysis.json')
    execution = read(HERE/'execution_manifest.json')
    assert [(r['step'], r['returncode']) for r in execution] == [
        ('model', 0), ('verify_inherited', 0), ('verify_symbolic', 0),
        ('recover_primal', 0), ('verify_result', 0)]
    for r in execution:
        assert sha(HERE/r['source_snapshot']) == r['source_sha256']
        assert sha(HERE/r['stdout']) == r['stdout_sha256']
        assert sha(HERE/r['stderr']) == r['stderr_sha256']
    summary = dict(status='COMPLETED_EXACT_ROOT_SORTING_NONSEPARATION',
                   point_sha256=certificate['point_sha256'],
                   matrix_sha256=certificate['matrix_sha256'],
                   certificate_sha256=sha(HERE/'root_completion_exact.json.gz'),
                   independent_audit_sha256=sha(HERE/'primal_independent_audit.json'),
                   principal_rows=438, principal_positive=427, principal_zero=11,
                   inequalities=36776, mass_equalities=38, positive_mu=120,
                   canonical_min=2700, canonical_L=9572,
                   local_optimization_calls=0, total_optimization_calls=1,
                   exact_recovery_attempts=1, exact_recovery_failures=0,
                   all_four_dispatch_inputs_unchanged=True, cloud_outputs_byte_identical=11,
                   all_prephase_artifact_bytes_preserved=len(prephase['artifacts']),
                   no_common_coupling_claim=True, original_half_remains_open=True,
                   finite_obligation_completed=True,
                   next='Release; only a separately assigned new-point obligation may reuse this symbolic envelope. No further cb45 common-kernel expansion.')
    receipt = dict(utc=datetime.now(timezone.utc).isoformat(), argv=[sys.executable, '-B', str(Path(__file__).resolve())],
                   finalizer_sha256=sha(__file__), completed_integrity_checks=summary)
    write(HERE/'finalization_receipt.json', receipt)
    output = json.dumps(summary, ensure_ascii=False)+'\n'
    (HERE/'finalization.stdout.txt').write_text(output)
    excluded = {HERE/'freeze_manifest.json'}
    artifacts = [p for p in HERE.rglob('*') if p.is_file() and p not in excluded]+[HERE.with_suffix('.md')]
    manifest = dict(**summary, utc=receipt['utc'], cloud=dict(request_id=download['request_id'],
                    run_id=43087374448, job_id=130755301713, artifact_id=13887921002,
                    source_commit='e4b9a8702cab8fe47ca4370fd5d025ee3b7d70cc',
                    zip_sha256='ce4f97f63d2ff2a69fa5f448e33dcdc7b9ac75d0234a8930393a1b3a758d65a7',
                    download_audit_path=str(download_path.relative_to(REPO)), download_audit_sha256=sha(download_path)),
                    sources=model['sources'], exact_face=analysis['exact_face'],
                    executed_steps=[dict(step=r['step'], returncode=r['returncode'], elapsed_seconds=r['elapsed_seconds']) for r in execution],
                    inactive_alternative='recover_farkas.py prepared but not executed; exact feasible witness obviates it.',
                    artifacts=[dict(path=str(p.relative_to(REPO)), sha256=sha(p), bytes=p.stat().st_size) for p in sorted(artifacts)])
    write(HERE/'freeze_manifest.json', manifest)
    print(output, end='')


if __name__ == '__main__':
    main()
