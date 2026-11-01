"""Static archive closure only; no game calculation or solver call."""
import ast
import gzip
import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
REPO = next(p for p in BASE.parents if (p / 'cleanup/inventory.jsonl').exists())

def identity(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def main():
    manifest = json.loads((BASE / 'source-manifest.json').read_text())
    for s in manifest['sources']:
        p = REPO / s['stored_path']; b = p.read_bytes()
        assert identity(p) == {'bytes': s['size'], 'sha256': s['sha256']}
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == s['blob']
    for group in ('artifacts', 'shared_dependencies', 'comparisons'):
        for rec in manifest[group]:
            assert identity(REPO / rec['path']) == {'bytes': rec['bytes'], 'sha256': rec['sha256']}, rec['path']
    paths = [REPO / x['path'] for x in manifest['artifacts']]
    js = py = links = 0
    for p in paths + [BASE / 'source-manifest.json']:
        if p.suffix == '.json':
            json.loads(p.read_text()); js += 1
        if p.suffix == '.py':
            ast.parse(p.read_text(), filename=str(p)); py += 1
        if p.suffix == '.md':
            for rel in re.findall(r'\]\(([^)]+)\)', p.read_text()):
                if '://' in rel or rel.startswith('#'):
                    continue
                assert (p.parent / rel.split('#')[0]).resolve().exists(), (p, rel)
                links += 1
    audit = json.loads((BASE / 'point-audit.json').read_text())
    assert audit['script'] == identity(BASE / 'audit_saved_points.py')
    assert audit['original_main_calls'] == audit['original_function_calls'] == audit['LP_calls'] == audit['random_games'] == 0
    packed = BASE / 'point-details.json.gz'
    assert audit['details']['gzip'] == identity(packed)
    raw = gzip.decompress(packed.read_bytes())
    assert len(raw) == audit['details']['uncompressed_bytes']
    assert hashlib.sha256(raw).hexdigest() == audit['details']['uncompressed_sha256']
    detail = json.loads(raw)
    assert sum(len(x['ordered_actions']) for x in detail.values()) == 3103
    assert sum(len(y['all_ordered_history_IC']) for x in detail.values() for y in x['interpretations'].values()) == 64257
    targets = 0
    for s in manifest['sources']:
        p = REPO / 'cleanup/workspaces/Boss7/receipts-round20' / (s['id'] + '.json')
        receipt = json.loads(p.read_text())
        for rel in receipt['targets']:
            assert (REPO / rel).exists(), rel
            targets += 1
    result = {'status': 'PASS', 'mathematics_executed': False, 'original_sources': len(manifest['sources']), 'artifact_bindings': len(manifest['artifacts']), 'shared_dependency_bindings': len(manifest['shared_dependencies']), 'comparison_bindings': len(manifest['comparisons']), 'JSON_parsed': js + 1, 'Python_AST_parsed': py, 'actual_local_links': links, 'receipt_targets_checked': targets, 'lossless_detail_actions': 3103, 'lossless_detail_IC_records': 64257, 'new_math_entry_repeats': 0}
    (BASE / 'self-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result))

if __name__ == '__main__':
    main()
