"""Verify historical source bytes and scope only; do not run mathematical code."""
from pathlib import Path
import argparse
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
    er = Path('archives/unrelated-machines/tools/evidence/machine-uniform-history')
    ws = Path('cleanup/workspaces/Boss4/r3-machine-uniform-history')

    def resolve(rel):
        path = root / rel
        return path if path.is_file() else fallback / rel

    def read_json(rel):
        return json.loads(resolve(rel).read_text())

    entries = {}
    counts = {}
    byte_checks = []
    for name in ['source-manifest.json', 'comparison-manifest.json']:
        sources = read_json(er / name)['sources']
        counts[name] = len(sources)
        for item in sources:
            raw = resolve(item['preserved_repo_path']).read_bytes()
            if len(raw) != item['source_size'] or sha(raw) != item['source_sha256']:
                raise ValueError(('source mismatch', item['id']))
            entries[item['id']] = item
            byte_checks.append(dict(id=item['id'], size=len(raw), sha256=sha(raw), passed=True))
    if counts != {'source-manifest.json': 5, 'comparison-manifest.json': 6}:
        raise ValueError(counts)

    def source_raw(sid):
        return resolve(entries[sid]['preserved_repo_path']).read_bytes()

    scope = read_json(er / 'scope-and-sha-chain.json')
    canonical = source_raw(scope['canonical_id'])
    if len(canonical) != scope['whole_size'] or sha(canonical) != scope['whole_sha256']:
        raise ValueError('canonical whole identity')
    if scope['whole_size'] != 8046 or len(scope['canonical_sections']) != 5:
        raise ValueError('canonical formal scope')
    for item in scope['canonical_sections']:
        start = canonical.index(item['start_marker'].encode())
        end = canonical.index(item['end_marker'].encode(), start + len(item['start_marker'].encode())) if item['end_marker'] else len(canonical)
        if start != item['byte_start'] or end != item['byte_end_exclusive'] or sha(canonical[start:end]) != item['slice_sha256']:
            raise ValueError(('section mismatch', item['section']))
    for chain in scope['hash_chains']:
        record = source_raw(chain['record_id'])
        for sid in chain['source_ids']:
            if sha(source_raw(sid)).encode() not in record:
                raise ValueError(('source chain', chain['record_id'], sid))
    final = source_raw(scope['primary_final_source_id'])
    if sha(canonical).encode() not in final:
        raise ValueError('final whole canonical chain')
    guard = read_json(er / 'guard-and-version-ledger.json')
    for item in guard['verbatim_source_fragments']:
        if item['fragment'].encode() not in source_raw(item['source_id']):
            raise ValueError(('guard/version original wording', item['source_id']))
    for name in ['scope-and-sha-chain.json', 'proof-variants-and-quantifiers.json', 'non-run-provenance.json']:
        if read_json(er / name)['mathematical_runs_this_batch'] != 0:
            raise ValueError('must not assert new mathematical run')
    receipts = read_json(ws / 'semantic-receipts.json')
    primary_ids = {x['id'] for x in read_json(er / 'source-manifest.json')['sources']}
    if len(receipts) != 5 or {x['id'] for x in receipts} != primary_ids:
        raise ValueError('receipt source set')
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
    docs = [Path('archives/unrelated-machines/state/证明/容量查询返回的平行元证明与双增广实现--证明.md'), Path('archives/unrelated-machines/state/审查/逐机统一交换的五稿原义与封装前件--审查.md'), er / 'README.md']
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
    copy_list_check_mode = 'not-present'
    if copy_path.is_file():
        listed = read_json(ws / 'copy-files.json')
        if not isinstance(listed, list) or listed != sorted(set(listed)):
            raise ValueError('copy-files must be a sorted unique list')
        for rel in listed:
            if Path(rel).is_absolute() or '..' in Path(rel).parts or not resolve(rel).is_file():
                raise ValueError(('invalid or missing listed copy file', rel))
        if (root / 'cleanup/inventory.jsonl').is_file():
            copy_list_check_mode = 'repository-listed-files-exist'
        else:
            copy_list_check_mode = 'staging-exact-file-list'
            expected_files = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
            if listed != expected_files:
                raise ValueError('exact staging copy-files mismatch')
    report = dict(check_kind='delivery-source-bytes-review-chain-scope-and-wording-only-not-mathematical-run', all_checks_passed=True, primary_source_count=5, comparison_source_count=6, source_byte_checks=byte_checks, review_hash_chain_count=len(scope['hash_chains']), canonical_section_count=5, guard_source_fragment_count=len(guard['verbatim_source_fragments']), original_guard_wording_verified=True, no_v1_author_Proof_invented=True, receipt_count=5, markdown_link_count=len(links), markdown_link_checks=links, mathematical_runs_this_batch=0, blind_reviews_this_batch=0, original_source_bytes_modified=False, old_main_source_done_repeated=False, formal_hypergraph_written=False)
    report['copy_list_check_mode'] = copy_list_check_mode
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ['check_kind', 'all_checks_passed', 'primary_source_count', 'comparison_source_count', 'review_hash_chain_count', 'canonical_section_count', 'guard_source_fragment_count', 'receipt_count', 'markdown_link_count', 'mathematical_runs_this_batch']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
