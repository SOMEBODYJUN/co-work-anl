"""Check delivered bytes and stated review chains/scope, not pool mathematics."""
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
    er = Path('archives/unrelated-machines/tools/evidence/shared-outside-small-pool-history')
    def resolve(rel):
        path = root / rel
        return path if path.is_file() else fallback / rel
    entries = {}
    counts = {}
    checks = []
    for name in ['source-manifest.json', 'comparison-manifest.json']:
        sources = json.loads((root / er / name).read_text())['sources']
        counts[name] = len(sources)
        for item in sources:
            raw = resolve(item['preserved_repo_path']).read_bytes()
            if len(raw) != item['source_size'] or sha(raw) != item['source_sha256']:
                raise ValueError(('source mismatch', item['id']))
            entries[item['id']] = item
            checks.append({'id': item['id'], 'size': len(raw), 'sha256': sha(raw), 'passed': True})
    if counts != {'source-manifest.json': 5, 'comparison-manifest.json': 8}:
        raise ValueError(counts)
    def source_raw(sid):
        return resolve(entries[sid]['preserved_repo_path']).read_bytes()
    scope = json.loads((root / er / 'scope-and-sha-chain.json').read_text())
    canonical = resolve(scope['canonical_repo_path']).read_bytes()
    if sha(canonical) != scope['canonical_whole_sha256'] or len(canonical) != scope['canonical_whole_size']:
        raise ValueError('canonical identity')
    for key, marker in [('pool_section', b'## 5.'), ('combined_scope_comparison', b'## 4.')]:
        part = scope[key]
        start = canonical.index(marker)
        end = len(canonical)
        if start != part['byte_start'] or end != part['byte_end_exclusive'] or sha(canonical[start:end]) != part['slice_sha256']:
            raise ValueError(('section identity', key))
    root_review = source_raw(scope['root_primary_source_id'])
    for sid in scope['root_nine_source_ids']:
        if sha(source_raw(sid)).encode() not in root_review:
            raise ValueError(('root nine source chain', sid))
    after = scope['pool_proof_read_after']
    after_raw = source_raw(after['source_id'])
    for key in ['exact_id', 'proof_id', 'independent_id']:
        if sha(source_raw(after[key])).encode() not in after_raw:
            raise ValueError(('proof read-after chain', key))
    for name in ['finite-check-provenance.json', 'quantifier-ledger.json']:
        if json.loads((root / er / name).read_text())['mathematical_runs_this_batch'] != 0:
            raise ValueError('must not assert a new mathematical run')
    receipts = json.loads((root / 'cleanup/workspaces/Boss4/r3-shared-outside-small-pool/semantic-receipts.json').read_text())
    if len(receipts) != 5 or len({item['id'] for item in receipts}) != 5:
        raise ValueError('receipt count')
    for item in receipts:
        for key in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for']:
            if item.get(key) is not True:
                raise ValueError((item['id'], key))
        for key in ['read_note', 'comparison_note', 'decision_note']:
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError((item['id'], key))
        if item['disposition'] not in {'integrated', 'retained', 'duplicate', 'retired'}:
            raise ValueError(item['id'])
        for target in item['targets']:
            if not resolve(target).is_file():
                raise ValueError(('missing receipt target', target))
    docs = [Path('archives/unrelated-machines/state/定理/共享返回池的全模式最优值与原样解码--定理.md'), Path('archives/unrelated-machines/state/审查/共享返回池的全模式审查与有限检查归属--审查.md'), er / 'README.md']
    links = []
    for rel in docs:
        for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)', (root / rel).read_text()):
            if '://' in url or url.startswith('#'):
                continue
            candidate = (root / rel.parent / url.split('#', 1)[0]).resolve()
            dest = candidate.relative_to(root)
            if not resolve(dest).is_file() and candidate != args.output.resolve():
                raise ValueError(('missing link', str(rel), url))
            links.append({'from': str(rel), 'to': str(dest), 'passed': True})
    report = {'check_kind': 'delivery-source-scope-and-review-chain-only-not-mathematical-run', 'all_checks_passed': True, 'primary_source_count': 5, 'comparison_source_count': 8, 'source_byte_checks': checks, 'root_nine_source_hash_chain_verified': True, 'pool_exact_proof_independent_hash_chain_verified': True, 'canonical_whole_and_section_scope_verified': True, 'receipt_count': 5, 'markdown_link_count': len(links), 'markdown_link_checks': links, 'finite_4328_not_replayed': True, 'mathematical_runs_this_batch': 0, 'blind_reviews_this_batch': 0, 'original_source_bytes_modified': False, 'formal_hypergraph_written': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ['check_kind', 'all_checks_passed', 'primary_source_count', 'comparison_source_count', 'receipt_count', 'markdown_link_count', 'mathematical_runs_this_batch']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
