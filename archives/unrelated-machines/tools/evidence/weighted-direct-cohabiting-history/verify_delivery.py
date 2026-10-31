"""Verify delivered bytes, recorded scope and review chains; no mathematical run."""
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
    er = Path('archives/unrelated-machines/tools/evidence/weighted-direct-cohabiting-history')
    ws = Path('cleanup/workspaces/Boss4/r3-weighted-direct-cohabiting')

    def resolve(rel):
        p = root / rel
        return p if p.is_file() else fallback / rel

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
            byte_checks.append({'id': item['id'], 'size': len(raw), 'sha256': sha(raw), 'passed': True})
    if counts != {'source-manifest.json': 5, 'comparison-manifest.json': 15}:
        raise ValueError(counts)

    def source_raw(sid):
        return resolve(entries[sid]['preserved_repo_path']).read_bytes()

    scopes = read_json(er / 'scope-and-sha-chain.json')
    for item in scopes['canonical_slices']:
        raw = source_raw(item['source_id'])
        start = raw.index(item['start_marker'].encode())
        end = raw.index(item['end_marker'].encode(), start + len(item['start_marker'].encode())) if item['end_marker'] else len(raw)
        if len(raw) != item['whole_size'] or sha(raw) != item['whole_sha256']:
            raise ValueError(('canonical identity', item['source_id']))
        if start != item['byte_start'] or end != item['byte_end_exclusive'] or sha(raw[start:end]) != item['slice_sha256']:
            raise ValueError(('canonical slice', item['formal_meaning']))
    for chain in scopes['hash_chains']:
        record = source_raw(chain['record_id'])
        for sid in chain['source_ids']:
            if sha(source_raw(sid)).encode() not in record:
                raise ValueError(('review hash chain', chain['record_id'], sid))
    finite = read_json(er / 'finite-check-provenance.json')
    quantifiers = read_json(er / 'quantifier-ledger.json')
    if finite['mathematical_runs_this_batch'] != 0 or quantifiers['mathematical_runs_this_batch'] != 0 or scopes['mathematical_runs_this_batch'] != 0:
        raise ValueError('must not assert new mathematical run')
    general = json.loads(source_raw('1dcf0e725e28ee55d080'))
    root_enum = json.loads(source_raw('d84e6f4ca159cee1d59f'))
    c = finite['C_context']
    if general['assignment_count'] != c['assignment_count'] or root_enum['complete_assignments_enumerated'] != c['assignment_count']:
        raise ValueError('historical assignment-count transcription')
    if general['minimum_peak_units'] != c['minimum_peak_units'] or root_enum['exact_opt_units'] != c['minimum_peak_units']:
        raise ValueError('historical optimum transcription')
    if general['peak_histogram'] != c['peak_histogram'] or root_enum['peak_histogram_units'] != c['peak_histogram']:
        raise ValueError('historical histogram transcription')
    receipts = read_json(ws / 'semantic-receipts.json')
    primary_ids = {x['id'] for x in read_json(er / 'source-manifest.json')['sources']}
    if len(receipts) != 5 or {x['id'] for x in receipts} != primary_ids:
        raise ValueError('receipt count or source identity')
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
    docs = [Path('archives/unrelated-machines/state/证明/直接共居的严格身份与异权三半共同调度--证明.md'), Path('archives/unrelated-machines/state/审查/直接共居异权合同的独立证据与跨稿范围--审查.md'), er / 'README.md']
    links = []
    for rel in docs:
        for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)', resolve(rel).read_text()):
            if '://' in url or url.startswith('#'):
                continue
            candidate = (root / rel.parent / url.split('#', 1)[0]).resolve()
            dest = candidate.relative_to(root)
            if not resolve(dest).is_file() and candidate != args.output.resolve():
                raise ValueError(('missing link', str(rel), url))
            links.append({'from': str(rel), 'to': str(dest), 'passed': True})
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
    report = dict(check_kind='delivery-source-scope-and-review-chain-only-not-mathematical-run', all_checks_passed=True, primary_source_count=5, comparison_source_count=15, source_byte_checks=byte_checks, review_hash_chain_count=len(scopes['hash_chains']), canonical_slice_count=len(scopes['canonical_slices']), historical_C_JSON_fields_match=True, historical_C_enumeration_replayed=False, receipt_count=5, markdown_link_count=len(links), markdown_link_checks=links, mathematical_runs_this_batch=0, blind_reviews_this_batch=0, original_source_bytes_modified=False, formal_hypergraph_written=False)
    report['copy_list_check_mode'] = copy_list_check_mode
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ['check_kind', 'all_checks_passed', 'primary_source_count', 'comparison_source_count', 'review_hash_chain_count', 'canonical_slice_count', 'receipt_count', 'markdown_link_count', 'mathematical_runs_this_batch']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
