"""Check preserved bytes, scope/hash chains, receipts and links; no math runs."""
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
    er = Path('archives/unrelated-machines/tools/evidence/shared-outside-four-task-history')
    def resolve(rel):
        p = root / rel
        return p if p.is_file() else fallback / rel
    entries = {}
    counts = {}
    bytechecks = []
    for name in ['source-manifest.json', 'comparison-manifest.json']:
        sources = json.loads((root / er / name).read_text())['sources']
        counts[name] = len(sources)
        for item in sources:
            raw = resolve(item['preserved_repo_path']).read_bytes()
            if len(raw) != item['source_size'] or sha(raw) != item['source_sha256']:
                raise ValueError(('source mismatch', item['id']))
            entries[item['id']] = item
            bytechecks.append({'id': item['id'], 'size': len(raw), 'sha256': sha(raw), 'passed': True})
    if counts != {'source-manifest.json': 5, 'comparison-manifest.json': 12}:
        raise ValueError(counts)
    def source_raw(sid):
        return resolve(entries[sid]['preserved_repo_path']).read_bytes()
    scope = json.loads((root / er / 'scope-and-sha-chain.json').read_text())
    canonical = resolve(scope['canonical_repo_path']).read_bytes()
    if sha(canonical) != scope['canonical_whole_sha256'] or len(canonical) != scope['canonical_whole_size']:
        raise ValueError('canonical identity')
    for key, start_marker, end_marker in [('root_primary_scope', b'## 2.', b'## 4.'), ('four_job_canonical_context', b'## 4.', b'## 5.')]:
        part = scope[key]
        start = canonical.index(start_marker)
        end = canonical.index(end_marker)
        if start != part['byte_start'] or end != part['byte_end_exclusive'] or sha(canonical[start:end]) != part['slice_sha256']:
            raise ValueError(('section identity', key))
    root_review = source_raw(scope['root_primary_scope']['source_id'])
    for sid in scope['root_primary_scope']['five_history_ids']:
        if sha(source_raw(sid)).encode() not in root_review:
            raise ValueError(('root history chain', sid))
    after = scope['four_job_proof_read_after']
    after_raw = source_raw(after['source_id'])
    for key in ['exact_id', 'proof_id', 'independent_id']:
        if sha(source_raw(after[key])).encode() not in after_raw:
            raise ValueError(('four-job review chain', key))
    finite = json.loads((root / er / 'finite-check-provenance.json').read_text())
    spectrum = json.loads((root / er / 'assignment-spectrum.json').read_text())
    if finite['mathematical_runs_this_batch'] != 0 or spectrum['mathematical_runs_this_batch'] != 0:
        raise ValueError('metadata must not assert new mathematical run')
    receipts = json.loads((root / 'cleanup/workspaces/Boss4/r3-shared-outside-four-task/semantic-receipts.json').read_text())
    if len(receipts) != 5 or len({x['id'] for x in receipts}) != 5:
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
        for rel in item['targets']:
            if not resolve(rel).is_file():
                raise ValueError(('missing receipt target', rel))
    docs = [Path('archives/unrelated-machines/state/构造/共享外端四任务环的完整负载谱--构造.md'), Path('archives/unrelated-machines/state/审查/共享外端四环的全谱审查与章节边界--审查.md'), er / 'README.md']
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
    report = {'check_kind': 'delivery-source-scope-and-hash-identity-only-not-mathematical-run', 'all_checks_passed': True, 'primary_source_count': 5, 'comparison_source_count': 12, 'source_byte_checks': bytechecks, 'root_global_five_history_hash_chain_verified': True, 'four_job_exact_proof_independent_hash_chain_verified': True, 'canonical_whole_and_sections_verified': True, 'receipt_count': 5, 'markdown_link_count': len(links), 'markdown_link_checks': links, 'symbolic_table_not_evaluated_as_experiment': True, 'mathematical_runs_this_batch': 0, 'blind_reviews_this_batch': 0, 'original_source_bytes_modified': False, 'formal_hypergraph_written': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ['check_kind', 'all_checks_passed', 'primary_source_count', 'comparison_source_count', 'receipt_count', 'markdown_link_count', 'mathematical_runs_this_batch']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
