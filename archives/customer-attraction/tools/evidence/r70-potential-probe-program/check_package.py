"""Static only: never imports or executes the original or interface audit."""
from pathlib import Path
import ast, hashlib, json, re

E = Path(__file__).resolve().parent
A = E.parents[2]
R = E.parents[4]
body = A/'state/程序/有序自复制税势预算的全SPE终局探针--程序.md'
receipt = R/'cleanup/workspaces/Boss7/receipts-round16/b3e90092c8c176acf8e7.json'
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
source = E/'original/potential_probe.py'
assert source.stat().st_size == 2951
assert digest(source) == 'b902078f2d0486182e904be371956c1bd82bd6b9f1261d50621b56666412e8f1'
comparison_paths = [
    'state/算法/完整历史纯SPE终局全集--算法.md',
    'state/候选/相邻真实双主题的势排除预算--候选.md',
    'state/反例/调和复制税逐分支归纳的六客户边界--反例.md',
    'state/障碍/全混合终局势预算的静态行族不足--障碍.md',
    'state/反例/三人均衡调和势低于最优覆盖的十一客户证书--反例.md',
    'state/反例/五客户无拥挤SPE负载桥障碍--反例.md',
    'tools/evidence/r70-six-provider-entry/original/README.md',
    'tools/evidence/r70-six-provider-entry/original/SIX_BRIEF.md',
]
manifest = {
    'primary': {'id': 'b3e90092c8c176acf8e7', 'size': 2951,
        'sha256': digest(source), 'blob': 'b1dbb5d7605f38eb560461e5d5a28863ff41ca94',
        'path': 'research/workspaces/customer-attraction/R-70d2119f50a642dc94b386eb142f1f2d/six_5/potential_probe.py',
        'commits': ['68fad804ec5946cb296f77dc5b336308a66abf12', 'aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c'],
        'saved_path': 'original/potential_probe.py', 'full_source_read': True},
    'fully_read_comparisons': [{'path_relative_to_archive': p, 'bytes': (A/p).stat().st_size,
                               'sha256': digest(A/p)} for p in comparison_paths],
    'runtime_dependencies': 'Python standard library only',
    'unmodified_original_main_calls': 1, 'unmodified_original_one_calls': 4,
    'LP_calls': 0, 'mature_math_reruns': 0,
}
(E/'source-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
event = json.loads((E/'new-interface-event/execution.json').read_text())
audit = json.loads((E/'new-interface-event/interface-audit.json').read_text())
assert event == audit['event'] and event['status'] == audit['status'] == 'pass'
assert event['source_sha256_before'] == event['source_sha256_after'] == digest(source)
assert event['script_sha256'] == digest(E/'audit_interface.py')
assert event['original_main_calls'] == 1 and event['original_one_calls'] == 4
assert event['original_main_one_calls'] == 1 and event['additional_helper_one_calls'] == 3
assert event['LP_calls'] == event['historical_or_mature_witness_reruns'] == 0
assert event['original_main_returned_normally'] and not event['separate_original_process']
assert event['assertions_enabled']
assert (E/'new-interface-event/stderr.txt').read_bytes() == b''
assert (E/'new-interface-event/stdout.txt').stat().st_size == event['stdout_bytes'] == 91
assert audit['totals'] == {'complete_policy_count': 418, 'complete_SPE_policy_count': 211,
    'all_policy_node_action_comparisons': 5528, 'payoff_cells': 84,
    'potential_cells': 34, 'all_prefix_sets_compared': 56}
assert len(audit['cases']) == 4
assert [c['minimum_unscaled_margin'] for c in audit['cases']] == ['10/3', '0', '0', '0']
assert [c['source_return'][2] for c in audit['cases']] == [1, 9, 8, 1]
assert [c['complete_SPE_policy_count'] for c in audit['cases']] == [1, 81, 128, 1]
ast_count = json_count = 0
for p in E.rglob('*.py'):
    ast.parse(p.read_text()); ast_count += 1
for p in E.rglob('*.json'):
    if p.name != 'self-check.json': json.loads(p.read_text()); json_count += 1
assert not list(E.rglob('__pycache__'))
links = []
for p in (body, E/'README.md'):
    content = p.read_text()
    assert content.count('\\[') == content.count('\\]')
    for href in re.findall(r'\]\(([^)]+)\)', content):
        if '://' in href or href.startswith('#'): continue
        target = (p.parent/href.split('#')[0]).resolve()
        assert target.exists(), (p, href)
        links.append({'from': str(p.relative_to(R)), 'href': href})
rec = json.loads(receipt.read_text())
assert rec['id'] == 'b3e90092c8c176acf8e7' and rec['disposition'] == 'integrated'
assert all(rec[k] is True for k in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for'])
for target in rec['targets']:
    if Path(target).name != 'self-check.json': assert (R/target).is_file()
files = [body, receipt] + sorted(p for p in E.rglob('*') if p.is_file() and p.name != 'self-check.json')
result = {'status': 'pass', 'static_only': True, 'original_calls_in_this_check': 0,
    'mathematical_enumeration_calls_in_this_check': 0, 'primary_sources': 1,
    'fully_read_comparison_files': len(comparison_paths), 'python_AST_files': ast_count,
    'evidence_JSON_files_excluding_self_check': json_count, 'receipt_JSON_files': 1,
    'local_links_checked': len(links), 'receipt_targets': len(rec['targets']),
    'bindings': [{'path': str(p.relative_to(R)), 'bytes': p.stat().st_size, 'sha256': digest(p)} for p in files],
    'local_links': links}
(E/'self-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
assert all((R/target).is_file() for target in rec['targets'])
print(json.dumps({k: v for k, v in result.items() if k not in ('bindings', 'local_links')}, ensure_ascii=False))
