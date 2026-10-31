"""Check source/diff/scope/table transcription only; no mathematical algorithm."""
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import re


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--fallback-root', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    fallback = args.fallback_root.resolve() if args.fallback_root else root
    er = Path('archives/unrelated-machines/tools/evidence/protected-cycle-exchange-history')
    ws = Path('cleanup/workspaces/Boss4/r3-protected-cycle-exchange-history')

    def resolve(rel):
        p = root / rel
        return p if p.is_file() else fallback / rel

    def read_json(rel):
        return json.loads(resolve(rel).read_text())

    entries = {}
    counts = {}
    checks = []
    for name in ['source-manifest.json', 'comparison-manifest.json']:
        items = read_json(er / name)['sources']
        counts[name] = len(items)
        for item in items:
            raw = resolve(item['preserved_repo_path']).read_bytes()
            if len(raw) != item['source_size'] or sha(raw) != item['source_sha256']:
                raise ValueError(('source mismatch', item['id']))
            entries[item['id']] = item
            checks.append(dict(id=item['id'], size=len(raw), sha256=sha(raw), passed=True))
    if counts != {'source-manifest.json': 5, 'comparison-manifest.json': 7}:
        raise ValueError(counts)

    def source_raw(sid):
        return resolve(entries[sid]['preserved_repo_path']).read_bytes()

    scope = read_json(er / 'scope-and-sha-chain.json')
    canonical = source_raw(scope['canonical_id'])
    section = scope['section9']
    start = canonical.index(section['start_marker'].encode())
    if len(canonical) != scope['whole_size'] or sha(canonical) != scope['whole_sha256']:
        raise ValueError('canonical whole identity')
    if start != section['byte_start'] or len(canonical) != section['byte_end_exclusive'] or sha(canonical[start:]) != section['slice_sha256']:
        raise ValueError('canonical section9 slice')
    for chain in scope['hash_chains']:
        record = source_raw(chain['record_id'])
        for sid in chain['source_ids']:
            if sha(source_raw(sid)).encode() not in record:
                raise ValueError(('source review hash chain', chain['record_id'], sid))
    versions = read_json(er / 'version-diffs-and-invariants.json')
    for item in versions['diffs']:
        before = source_raw(item['v1_id'])
        after = source_raw(item['v2_id'])
        expected = ''.join(difflib.unified_diff(before.decode().splitlines(keepends=True), after.decode().splitlines(keepends=True), fromfile='original-v1', tofile='original-v2')).encode()
        saved = resolve(item['diff_repo_path']).read_bytes()
        if expected != saved or sha(saved) != item['diff_sha256']:
            raise ValueError(('original diff mismatch', item['diff_repo_path']))
        if len(before) != item['v1_size'] or len(after) != item['v2_size'] or len(after) - len(before) != item['byte_delta']:
            raise ValueError('diff byte counts')

    def fragment(sid, start_marker, end_marker):
        raw = source_raw(sid)
        start = raw.index(start_marker.encode())
        end = raw.index(end_marker.encode(), start + len(start_marker.encode())) if end_marker else len(raw)
        return raw[start:end]

    for item in versions['unchanged_original_fragments']:
        before = fragment(item['v1_id'], item['v1_start'], item['v1_end'])
        after = fragment(item['v2_id'], item['v2_start'], item['v2_end'])
        if before != after or len(before) != item['size'] or sha(before) != item['sha256']:
            raise ValueError(('nonempty original invariant', item['name']))
    witnesses = read_json(er / 'ten-job-witness-records.json')
    transcription_checks = 0
    for row in witnesses['table_rows']:
        for sid in witnesses['author_table_sources']:
            if row['author_source_row'].encode() not in source_raw(sid):
                raise ValueError(('author original table transcription', row['machine']))
            transcription_checks += 1
        if row['read_after_two_column_row'].encode() not in source_raw(witnesses['rank_other_table_source']):
            raise ValueError(('two-column original table transcription', row['machine']))
        transcription_checks += 1
    for line in witnesses['canonical_original_lines']:
        if line.encode() not in source_raw(witnesses['canonical_read_source']):
            raise ValueError(('canonical original line transcription', line))
        transcription_checks += 1
    for name in ['scope-and-sha-chain.json', 'ten-job-witness-records.json', 'quantifiers-and-non-run.json']:
        if read_json(er / name)['mathematical_runs_this_batch'] != 0:
            raise ValueError('must not assert new mathematical run')
    receipts = read_json(ws / 'semantic-receipts.json')
    primary_ids = {x['id'] for x in read_json(er / 'source-manifest.json')['sources']}
    if len(receipts) != 5 or {x['id'] for x in receipts} != primary_ids:
        raise ValueError('receipt count or primary set')
    for item in receipts:
        for key in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for']:
            if item.get(key) is not True:
                raise ValueError((item['id'], key))
        for key in ['read_note', 'comparison_note', 'decision_note']:
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError((item['id'], key))
        if item['disposition'] not in {'retained', 'integrated', 'duplicate', 'retired'}:
            raise ValueError(item['id'])
        for target in item['targets']:
            if not resolve(target).is_file():
                raise ValueError(('missing receipt target', target))
    docs = [Path('archives/unrelated-machines/state/证明/共享子句保护环的全任务单位调度--证明.md'), Path('archives/unrelated-machines/state/审查/共享子句保护环的空式修订与双手工解--审查.md'), er / 'README.md']
    links = []
    for rel in docs:
        for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)', resolve(rel).read_text()):
            if '://' in url or url.startswith('#'):
                continue
            candidate = (root / rel.parent / url.split('#', 1)[0]).resolve()
            dest = candidate.relative_to(root)
            if not resolve(dest).is_file() and candidate != args.output.resolve():
                raise ValueError(('missing link', str(rel), url))
            links.append(dict(source=str(rel), target=str(dest), passed=True))
    copy_list_check_mode = 'not-present'
    if (root / ws / 'copy-files.json').is_file():
        listed = read_json(ws / 'copy-files.json')
        if not isinstance(listed, list) or listed != sorted(set(listed)):
            raise ValueError('copy-files must be sorted and unique')
        for rel in listed:
            if Path(rel).is_absolute() or '..' in Path(rel).parts or not resolve(rel).is_file():
                raise ValueError(('bad or missing copy path', rel))
        if (root / 'cleanup/inventory.jsonl').is_file():
            copy_list_check_mode = 'repository-listed-files-exist'
        else:
            copy_list_check_mode = 'staging-exact-file-list'
            actual = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
            if listed != actual:
                raise ValueError('exact staging copy-list mismatch')
    report = dict(check_kind='delivery-source-diff-scope-and-transcription-only-not-mathematical-run', all_checks_passed=True, primary_source_count=5, comparison_source_count=7, source_byte_checks=checks, review_hash_chain_count=len(scope['hash_chains']), canonical_section9_verified=True, canonical_other_sections_not_certified=True, original_diff_count=len(versions['diffs']), invariant_original_fragment_count=len(versions['unchanged_original_fragments']), original_table_string_checks=transcription_checks, table_transcription_only_not_eligibility_or_load_program=True, receipt_count=5, markdown_link_count=len(links), markdown_link_checks=links, copy_list_check_mode=copy_list_check_mode, mathematical_runs_this_batch=0, blind_reviews_this_batch=0, original_source_bytes_modified=False, other_Boss_formal_page_modified=False, formal_hypergraph_written=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['check_kind', 'all_checks_passed', 'primary_source_count', 'comparison_source_count', 'review_hash_chain_count', 'original_diff_count', 'invariant_original_fragment_count', 'original_table_string_checks', 'receipt_count', 'markdown_link_count', 'copy_list_check_mode', 'mathematical_runs_this_batch']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
