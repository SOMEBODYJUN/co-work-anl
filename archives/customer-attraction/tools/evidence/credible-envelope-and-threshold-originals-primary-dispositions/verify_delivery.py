"""Verify staged bytes and an explicit concrete package dependency, never mathematics."""
from pathlib import Path
import hashlib
import json
import sys


def main():
    stage = Path(sys.argv[1]).resolve()
    repository = Path(sys.argv[2]).resolve()
    evidence = stage / 'archives/customer-attraction/tools/evidence/credible-envelope-and-threshold-originals-primary-dispositions'
    workspace = stage / 'cleanup/workspaces/Boss4/r3-credible-envelope-and-threshold-originals-primary-dispositions'
    read = lambda p: json.loads(p.read_text())
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    manifest = read(evidence / 'content-manifest.json')
    for row in manifest['files']:
        p = stage / row['path']
        assert p.stat().st_size == row['size'] and sha(p) == row['sha256']
    required = read(evidence / 'required-general-package.json')
    general = Path(required['general_stage'])
    copylist = general / required['copylist_target']
    assert sha(copylist) == required['copylist_sha256']
    for rel in read(copylist):
        assert (general / rel).is_file(), rel
    bindings = read(evidence / 'reuse-bindings.json')['rows']
    for row in bindings:
        p = general / row['target_path']
        assert str(p) == row['staged_path']
        assert p.stat().st_size == row['size'] and sha(p) == row['sha256']
        q = repository / row['target_path']
        if q.is_file():
            assert sha(q) == row['sha256']
    sources = read(evidence / 'source-manifest.json')['rows']
    gate = read(evidence / 'ownership-gate.json')
    assert gate['claim_status'] == 'pushed' and gate['claim_local_sync'] == 'synced'
    owners = {r['id']: r for r in gate['owner_records']}
    for row in sources:
        p = general / row['target_path']
        b = p.read_bytes()
        assert len(b) == row['size'] and sha(p) == row['sha256']
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == row['blob']
        o = owners[row['id']]
        assert (o['owner'], o['disposition'], o['source_sha256']) == ('Boss4', 'in-progress', row['sha256'])
        assert row['exact_prior_normal_show_reused'] and row['no_new_normal_show_for_this_source']
    receipts = read(workspace / 'semantic-receipts.json')
    assert {r['id'] for r in sources} == {r['id'] for r in receipts}
    for row in receipts:
        assert row['disposition'] == 'duplicate'
        assert row['full_file_reviewed'] and row['related_material_checked'] and row['unique_content_accounted_for']
        for rel in row['targets']:
            assert (stage / rel).is_file() or (general / rel).is_file()
    assert not (stage / 'archives/customer-attraction/state').exists()
    files = read(workspace / 'copy-files.json')
    assert sorted(files) == sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file())
    result = dict(status='PASS-STAGED-DEPENDENCY-STRUCTURE-ONLY', primary_files=2, primary_bytes=13928,
                  duplicate_receipts=2, reused_files=len(bindings), new_mathematical_bodies=0,
                  new_original_copies=0, general_copy_files_required=len(read(copylist)),
                  currently_published_reuse_files=sum((repository / r['target_path']).is_file() for r in bindings),
                  requires_general_before_checkpoint_done=True, original_source_imports=0,
                  mathematical_CLI_runs=0, LP_MILP_DP_runs=0, new_mathematical_program_runs=0,
                  note='All reused bytes exist in frozen GENERAL stage; absence from canonical repository is not represented as publication.')
    (evidence / 'self-check-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
