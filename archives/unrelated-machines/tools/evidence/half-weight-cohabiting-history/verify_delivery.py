"""Check source bytes, review chains and typographic delta; no mathematical run."""
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
    er = Path('archives/unrelated-machines/tools/evidence/half-weight-cohabiting-history')
    ws = Path('cleanup/workspaces/Boss4/r3-half-weight-cohabiting-history')

    def resolve(rel):
        p = root / rel
        return p if p.is_file() else fallback / rel

    def read_json(rel):
        return json.loads(resolve(rel).read_text())

    entries = {}
    counts = {}
    checks = []
    for name in ['source-manifest.json', 'comparison-manifest.json']:
        sources = read_json(er / name)['sources']
        counts[name] = len(sources)
        for item in sources:
            raw = resolve(item['preserved_repo_path']).read_bytes()
            if len(raw) != item['source_size'] or sha(raw) != item['source_sha256']:
                raise ValueError(('source mismatch', item['id']))
            entries[item['id']] = item
            checks.append(dict(id=item['id'], size=len(raw), sha256=sha(raw), passed=True))
    if counts != {'source-manifest.json': 5, 'comparison-manifest.json': 9}:
        raise ValueError(counts)

    def source_raw(sid):
        return resolve(entries[sid]['preserved_repo_path']).read_bytes()

    artifact_checks = []
    for item in read_json(er / 'comparison-artifacts.json')['artifacts']:
        raw = resolve(item['repo_path']).read_bytes()
        if len(raw) != item['size'] or sha(raw) != item['sha256']:
            raise ValueError(('existing artifact mismatch', item['repo_path']))
        artifact_checks.append(dict(repo_path=item['repo_path'], passed=True))
    delta = read_json(er / 'initial-final-delta.json')
    initial = source_raw(delta['initial_id'])
    final = source_raw(delta['final_id'])
    change = delta['only_replacement']
    if initial.decode().count(change['old']) != 1:
        raise ValueError('one original typographic phrase expected')
    expected = initial.decode().replace(change['old'], change['new'], 1) + delta['appended_freeze_note']
    if expected.encode() != final or len(final) - len(initial) != delta['byte_delta'] or delta['byte_delta'] != 234:
        raise ValueError('exact initial-final byte relationship')
    computed_diff = ''.join(difflib.unified_diff(initial.decode().splitlines(keepends=True), final.decode().splitlines(keepends=True), fromfile='independent-v1-original', tofile='independent-v1-final')).encode()
    saved_diff = resolve(delta['diff_path']).read_bytes()
    if computed_diff != saved_diff or sha(saved_diff) != delta['diff_sha256']:
        raise ValueError('saved unified diff')
    scopes = read_json(er / 'scope-and-sha-chain.json')
    for item in scopes['canonical_slices']:
        raw = source_raw(item['source_id'])
        start = raw.index(item['start_marker'].encode())
        end = raw.index(item['end_marker'].encode(), start + len(item['start_marker'].encode())) if item['end_marker'] else len(raw)
        if len(raw) != item['whole_size'] or sha(raw) != item['whole_sha256']:
            raise ValueError('whole canonical identity')
        if start != item['byte_start'] or end != item['byte_end_exclusive'] or sha(raw[start:end]) != item['slice_sha256']:
            raise ValueError(('canonical slice', item['formal_meaning']))
    for chain in scopes['hash_chains']:
        record = source_raw(chain['record_id'])
        for sid in chain['source_ids']:
            if sha(source_raw(sid)).encode() not in record:
                raise ValueError(('review hash chain', chain['record_id'], sid))
    finite = read_json(er / 'finite-check-provenance.json')
    if any(read_json(er / name)['mathematical_runs_this_batch'] != 0 for name in ['finite-check-provenance.json', 'quantifier-ledger.json', 'scope-and-sha-chain.json']):
        raise ValueError('must not assert new mathematical run')
    general = json.loads(source_raw('1dcf0e725e28ee55d080'))
    root_enum = json.loads(source_raw('d84e6f4ca159cee1d59f'))
    reported = finite['general']
    if general['assignment_count'] != reported['assignment_count'] or root_enum['complete_assignments_enumerated'] != reported['assignment_count']:
        raise ValueError('historical count transcription')
    if general['minimum_peak_units'] != reported['minimum_peak_units'] or root_enum['exact_opt_units'] != reported['minimum_peak_units']:
        raise ValueError('historical minimum transcription')
    if general['peak_histogram'] != reported['histogram'] or root_enum['peak_histogram_units'] != reported['histogram']:
        raise ValueError('historical histogram transcription')
    receipts = read_json(ws / 'semantic-receipts.json')
    primary_ids = {x['id'] for x in read_json(er / 'source-manifest.json')['sources']}
    if len(receipts) != 5 or {x['id'] for x in receipts} != primary_ids:
        raise ValueError('receipt count or source set')
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
                raise ValueError(('receipt target', target))
    docs = [Path('archives/unrelated-machines/state/证明/半权直接共居的精确三半间隔与双计数--证明.md'), Path('archives/unrelated-machines/state/审查/半权直接共居的陈述先行与排版终稿边界--审查.md'), er / 'README.md']
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
    copy_path = root / ws / 'copy-files.json'
    if copy_path.is_file():
        expected_files = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
        if read_json(ws / 'copy-files.json') != expected_files:
            raise ValueError('exact copy-files list')
    report = dict(check_kind='delivery-bytes-typographic-delta-scope-review-chain-only-not-mathematical-run', all_checks_passed=True, primary_source_count=5, comparison_source_count=9, source_byte_checks=checks, comparison_artifact_count=len(artifact_checks), comparison_artifact_checks=artifact_checks, exact_initial_final_delta_verified=True, delta_bytes=234, mathematical_revision=False, review_hash_chain_count=len(scopes['hash_chains']), canonical_slice_count=len(scopes['canonical_slices']), historical_json_transcription_verified=True, historical_enumerations_replayed=False, receipt_count=5, markdown_link_count=len(links), markdown_link_checks=links, mathematical_runs_this_batch=0, blind_reviews_this_batch=0, original_source_bytes_modified=False, formal_hypergraph_written=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ['check_kind', 'all_checks_passed', 'primary_source_count', 'comparison_source_count', 'comparison_artifact_count', 'delta_bytes', 'review_hash_chain_count', 'canonical_slice_count', 'receipt_count', 'markdown_link_count', 'mathematical_runs_this_batch']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
