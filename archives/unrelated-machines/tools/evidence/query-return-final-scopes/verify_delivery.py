"""Delivery byte/scope/provenance checks only; never run mathematical algorithms."""
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
    parser.add_argument('--dependency-root', type=Path, action='append', default=[])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    fallback = args.fallback_root.resolve() if args.fallback_root else root
    roots = [root, fallback] + [p.resolve() for p in args.dependency_root]
    er = Path('archives/unrelated-machines/tools/evidence/query-return-final-scopes')
    ws = Path('cleanup/workspaces/Boss4/r3-query-return-final-scopes')

    def resolve(rel):
        for base in roots:
            if (base / rel).is_file():
                return base / rel
        return root / rel

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
    if counts != {'source-manifest.json': 5, 'comparison-manifest.json': 19}:
        raise ValueError(counts)

    def source_raw(sid):
        return resolve(entries[sid]['preserved_repo_path']).read_bytes()

    artifacts = read_json(er / 'comparison-artifacts.json')['artifacts']
    artifact_checks = []
    for item in artifacts:
        raw = resolve(item['repo_path']).read_bytes()
        if len(raw) != item['size'] or sha(raw) != item['sha256']:
            raise ValueError(('artifact mismatch', item['repo_path']))
        artifact_checks.append(dict(repo_path=item['repo_path'], passed=True))
    if artifacts[0]['sha256'] != 'fa93beb7acbe8cbc96ce8da05c30e69584bd6c5828bb6e1ab164497150b45b1c' or artifacts[0]['size'] != 13950:
        raise ValueError('exact old dependency')
    scopes = read_json(er / 'scope-and-sha-chain.json')
    for key, item in scopes['canonical_slices'].items():
        raw = source_raw(item['source_id'])
        start = raw.index(item['start_marker'].encode())
        end = raw.index(item['end_marker'].encode(), start + len(item['start_marker'].encode())) if item['end_marker'] else len(raw)
        if len(raw) != item['whole_size'] or sha(raw) != item['whole_sha256']:
            raise ValueError(('whole canonical', key))
        if start != item['byte_start'] or end != item['byte_end_exclusive'] or sha(raw[start:end]) != item['slice_sha256']:
            raise ValueError(('canonical slice', key))
    primary_ids = {x['id'] for x in read_json(er / 'source-manifest.json')['sources']}
    if set(scopes['primary_source_formal_scope']) != primary_ids:
        raise ValueError('one explicit formal scope per primary source')
    for sid, item in scopes['primary_source_formal_scope'].items():
        if set(item['formal_slices']) & set(item['context_slices']):
            raise ValueError(('formal/context overlap', sid))
        for key in item['formal_slices'] + item['context_slices']:
            if key not in scopes['canonical_slices']:
                raise ValueError(('unknown canonical slice', key))
    for chain in scopes['hash_chains']:
        record = source_raw(chain['record_id'])
        for sid in chain['source_ids']:
            if sha(source_raw(sid)).encode() not in record:
                raise ValueError(('original review hash chain', chain['record_id'], sid))
    for name in ['finite-check-provenance.json', 'quantifier-ledger.json', 'scope-and-sha-chain.json']:
        if read_json(er / name)['mathematical_runs_this_batch'] != 0:
            raise ValueError('must not assert new mathematical run')
    finite = read_json(er / 'finite-check-provenance.json')['C_general']
    general = json.loads(source_raw('1dcf0e725e28ee55d080'))
    root_enum = json.loads(source_raw('d84e6f4ca159cee1d59f'))
    if general['assignment_count'] != finite['assignment_count'] or root_enum['complete_assignments_enumerated'] != finite['assignment_count']:
        raise ValueError('historical count transcription')
    if general['minimum_peak_units'] != finite['minimum_units'] or root_enum['exact_opt_units'] != finite['minimum_units']:
        raise ValueError('historical minimum transcription')
    if general['peak_histogram'] != finite['histogram'] or root_enum['peak_histogram_units'] != finite['histogram']:
        raise ValueError('historical histogram transcription')
    initial = source_raw('996c66f141c443ca1e59').decode()
    final = source_raw('9f07bfa921f3817ab375').decode()
    prefix = initial.replace('精确1/3-2实际间隔', '精确YES1／NO3/2实际间隔', 1)
    suffix = '\n排版冻结说明：首写v1（SHA 7f9caf5f91d72a512f983c9b887e10e5adf64d5eaefd88ac7d53096489bacf5f）保原字节。本final只将§7一处非正式间隔写法精确为YES1／NO3/2，不改任何公式、证明或结论。\n'
    if final != prefix + suffix or len(final.encode()) - len(initial.encode()) != 234:
        raise ValueError('C initial/final exact typographic-only change')
    receipts = read_json(ws / 'semantic-receipts.json')
    if len(receipts) != 5 or {x['id'] for x in receipts} != primary_ids:
        raise ValueError('receipt count or primary identity')
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
    docs = [Path('archives/unrelated-machines/state/审查/查询返回三接口的最终认证范围与历史身份--审查.md'), Path('archives/unrelated-machines/state/资源/查询返回终审的原件链与有限运行资源--资源.md'), er / 'README.md']
    links = []
    dependency_stage_links = []
    for rel in docs:
        for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)', resolve(rel).read_text()):
            if '://' in url or url.startswith('#'):
                continue
            candidate = (root / rel.parent / url.split('#', 1)[0]).resolve()
            dest = candidate.relative_to(root)
            actual = resolve(dest)
            if not actual.is_file() and candidate != args.output.resolve():
                raise ValueError(('missing link', str(rel), url))
            origin = next((str(base) for base in roots if actual == base / dest), str(root))
            check = dict(source=str(rel), target=str(dest), resolution_root=origin, passed=True)
            links.append(check)
            if actual.is_file() and any(actual == base / dest for base in roots[2:]):
                dependency_stage_links.append(str(dest))
    copy_path = root / ws / 'copy-files.json'
    if copy_path.is_file():
        expected = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
        if read_json(ws / 'copy-files.json') != expected:
            raise ValueError('exact copy-files list')
    report = dict(check_kind='delivery-source-bytes-formal-scope-and-provenance-only-not-mathematical-run', all_checks_passed=True, primary_source_count=5, comparison_source_count=19, source_byte_checks=byte_checks, artifact_count=4, artifact_checks=artifact_checks, review_hash_chain_count=5, canonical_slice_count=5, explicit_formal_scope_count=5, whole_hash_not_entire_file_certification=True, historical_json_transcription_verified=True, C_typographic_delta_verified=True, mathematical_runs_this_batch=0, blind_reviews_this_batch=0, historical_enumerations_replayed=False, receipt_count=5, markdown_link_count=len(links), markdown_link_checks=links, temporary_dependency_stage_links=sorted(set(dependency_stage_links)), required_copy_order='half-weight C prior28files before this final-scope batch', original_source_bytes_modified=False, formal_hypergraph_written=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ['check_kind', 'all_checks_passed', 'primary_source_count', 'comparison_source_count', 'artifact_count', 'review_hash_chain_count', 'canonical_slice_count', 'receipt_count', 'markdown_link_count', 'temporary_dependency_stage_links', 'mathematical_runs_this_batch']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
