"""Check source bytes, document links, and lossless table serialization only.

Does not import/run original code, compute payoffs, test IC, or solve anything.
"""
from pathlib import Path
from itertools import product
import ast
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
RECORD = REPO / 'cleanup/workspaces/Boss3/resume-20261102/a5'


def check():
    sources = json.loads((HERE / 'source-manifest.json').read_text())
    receipts = json.loads((RECORD / 'semantic-receipts.json').read_text())
    delivery = json.loads((RECORD / 'delivery.json').read_text())
    assert len(sources) == len(receipts) == 20
    assert {x['id'] for x in sources} == {x['id'] for x in receipts}
    assert len({x['id'] for x in sources}) == 20
    parsed_py = 0
    parsed_json = 0
    payload = {}
    for x in sources:
        p = REPO / x['evidence_path']
        raw = p.read_bytes()
        assert len(raw) == x['size']
        assert hashlib.sha256(raw).hexdigest() == x['sha256']
        suffix = p.suffix
        if suffix == '.py':
            ast.parse(raw.decode(), filename=x['path'])
            parsed_py += 1
        elif suffix == '.json':
            payload[p.name] = json.loads(raw)
            parsed_json += 1
    for row in receipts:
        assert all(row[k] is True for k in ('full_file_reviewed',
            'related_material_checked', 'unique_content_accounted_for'))
        assert all(row[k] for k in ('read_note', 'comparison_note', 'decision_note'))
        assert row['disposition'] == 'integrated'
        for target in row['targets']:
            assert (REPO / target).is_file(), target
    docs = [REPO / p for p in delivery['formal_objects']]
    link_count = 0
    for p in docs + [HERE / 'README.md']:
        content = p.read_text()
        assert '<!--' not in content, p
        if p in docs:
            assert content.startswith('---\n')
            head = content.split('---', 2)[1]
            for k in ('id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs'):
                assert re.search(r'^' + k + ':', head, re.M), (p, k)
        for href in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
            if '://' not in href and not href.startswith('#'):
                assert (p.parent / href.split('#', 1)[0]).resolve().exists(), (p, href)
                link_count += 1
    counter = next(p for p in docs if p.name.startswith('十单位'))
    encoded = re.findall(r'^\|([0-4])\|(∅|[0-4]+)\|`([0-4]+)`\|$',
                         counter.read_text(), re.M)
    decoded = {}
    for depth, prefix, actions in encoded:
        d = int(depth)
        pref = () if prefix == '∅' else tuple(map(int, prefix))
        suffixes = list(product(range(5), repeat=d-len(pref)))
        assert len(actions) == len(suffixes)
        for tail, action in zip(suffixes, actions):
            key = pref + tail
            assert key not in decoded
            decoded[key] = int(action)
    certificate = payload['terminal_share_padding_exact.json']['certificate']
    old = {tuple(a['history']): a['action'] for a in certificate['actions']}
    assert len(old) == len(certificate['actions']) == len(decoded) == 781
    assert decoded == old
    wallet = next(p for p in docs if p.name.startswith('五人实际'))
    tab = re.findall(r'^\|([01]{5})\|([^|]+)\|([^|]+)\|$', wallet.read_text(), re.M)
    old_states = payload['audit_actual_union_wallet.json']['states']
    raw_records = {(tuple(s['actual']), s['query']): s['residue'] for s in old_states}
    restored = {(tuple(map(int, bits)), q): value
                for bits, v0, v1 in tab for q, value in enumerate((v0, v1))}
    assert len(restored) == len(raw_records) == 64
    assert restored == raw_records
    point = next(x for x in sources if x['path'].endswith('/exact_current_source_own_index_v1.json'))
    for name in ('audit_actual13_projection.json', 'audit_mixed_optimal_queries.json'):
        assert payload[name]['source_sha256'] == point['sha256']
    assert payload['actual13_projection.json']['source_exact_point_sha256'] == point['sha256']
    return {'status': 'PASS', 'source_files': len(sources),
            'source_bytes': sum(x['size'] for x in sources),
            'python_AST_only': parsed_py, 'json_parsed': parsed_json,
            'formal_docs': len(docs), 'local_links': link_count,
            'policy_table_rows': len(encoded), 'policy_records_lossless': len(decoded),
            'wallet_table_records_lossless': len(restored), 'receipts': len(receipts),
            'original_math_runs': 0, 'new_math_checker_runs': 0,
            'scope': 'asset identity and serialization; no payoff/IC/LP/BI execution'}


if __name__ == '__main__':
    result = check()
    (HERE / 'artifact-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    (RECORD / 'self-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False))
