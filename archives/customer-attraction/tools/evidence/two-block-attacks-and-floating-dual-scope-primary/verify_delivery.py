"""Structural delivery check only; never imports or executes mathematical sources."""
from pathlib import Path
import hashlib
import json
import re
import sys


def main():
    stage = Path(sys.argv[1]).resolve()
    repository = Path(sys.argv[2]).resolve()
    evidence = stage / 'archives/customer-attraction/tools/evidence/two-block-attacks-and-floating-dual-scope-primary'
    workspace = stage / 'cleanup/workspaces/Boss4/r3-two-block-attacks-and-floating-dual-scope-primary'
    read = lambda p: json.loads(p.read_text())
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    resolve = lambda rel: stage / rel if (stage / rel).is_file() else repository / rel
    manifest = read(evidence / 'content-manifest.json')
    for row in manifest['files']:
        p = stage / row['path']
        assert p.is_file() and p.stat().st_size == row['size'] and digest(p) == row['sha256'], row['path']
    sources = read(evidence / 'source-manifest.json')['rows']
    owners = read(evidence / 'ownership-gate.json')
    assert owners['claim_status'] == 'pushed' and owners['claim_local_sync'] == 'synced'
    by_id = {row['id']: row for row in owners['owner_records']}
    for row in sources:
        p = stage / row['target_path']
        assert p.stat().st_size == row['size'] and digest(p) == row['sha256']
        b = p.read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == row['blob']
        o = by_id[row['id']]
        assert (o['owner'], o['disposition'], o['source_sha256']) == ('Boss4', 'in-progress', row['sha256'])
    dependencies = read(evidence / 'dependency-bindings.json')['rows']
    for row in dependencies:
        p = repository / row['published_path']
        assert p.stat().st_size == row['size'] and digest(p) == row['sha256']
    comparisons = read(evidence / 'comparison-bindings.json')['full_formal_objects_read']
    for row in comparisons:
        p = repository / row['path']
        assert p.stat().st_size == row['size'] and digest(p) == row['sha256']
    receipts = read(workspace / 'semantic-receipts.json')
    assert {r['id'] for r in receipts} == {r['id'] for r in sources}
    for row in receipts:
        assert row['full_file_reviewed'] and row['related_material_checked'] and row['unique_content_accounted_for']
        assert row['current_original_mathematical_entries'] == row['current_new_mathematical_entries'] == 0
        for path in row['targets']:
            assert resolve(path).is_file(), path
    links = 0
    ids = []
    for p in stage.rglob('*.md'):
        if '/original/' in str(p):
            continue
        t = p.read_text()
        if '/state/' in str(p):
            assert t.startswith('---\n')
            front = t.split('---', 2)[1]
            for key in ['id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs']:
                assert re.search(r'^' + key + r':', front, re.M), (p, key)
            ids.append(re.search(r'^id:\s*(.+)$', front, re.M).group(1))
        for path in re.findall(r'\[[^\]]*\]\(([^)]+)\)', t):
            if path.startswith(('http:', 'https:', '#')):
                continue
            path = path.split('#')[0]
            q = (p.parent / path).resolve()
            try:
                rel = q.relative_to(stage)
            except ValueError:
                raise AssertionError(('outside-stage-relative-link', p, path))
            assert resolve(rel).is_file(), (p, path)
            links += 1
    assert len(ids) == len(set(ids)) == 2
    copylist = read(workspace / 'copy-files.json')
    actual = sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file())
    assert sorted(copylist) == actual
    result = dict(status='PASS-STRUCTURE-ONLY', primary_files=len(sources), primary_bytes=sum(r['size'] for r in sources),
                  dependency_files=len(dependencies), comparison_objects=len(comparisons), semantic_receipts=len(receipts),
                  formal_objects=len(ids), checked_markdown_links=links, copy_files=len(copylist),
                  original_source_imports=0, original_mathematical_CLI_runs=0, LP_runs=0, IC_replay_runs=0,
                  new_mathematical_program_runs=0, note='File hashes, links, owner snapshots and metadata only; not a numerical or theorem checker.')
    (evidence / 'self-check-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
