"""Static package checks only; never import or rerun the mathematical programs."""
import ast
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DOC = ROOT / 'archives/customer-attraction/state/程序/浮点终局全集递推与完整历史有理后核程序--程序.md'
RECEIPT = ROOT / 'cleanup/workspaces/Boss7/receipts-round16/44c5afc4b6e2b6b72b90.json'

def load(p):
    return json.loads(p.read_text())

def binding(p):
    return {'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
            'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

manifest = load(HERE / 'source-manifest.json')
locations = {
    '44c5afc4b6e2b6b72b90': HERE / 'original/spe_dp.py',
    '1ee3fd3da1dc3b243cc8': HERE.parent / 'r70-strategy-lp-program/original/strategy_lp.py',
    '0feb999c7e960f46b89b': HERE.parent / 'r70-six-provider-entry/original/SIX_BRIEF.md',
    '603ccb4f4c0e5f3b4e0d': HERE.parent / 'r70-six-provider-entry/original/SIX_SEARCH.py',
    '15338f897ce896dfb4d3': HERE.parent / 'r70-six1-best-data/original/lp_best.json',
    'd9f27a00ce820bda3f97': HERE.parent / 'r70-six1-best-data/original/random_best.json',
}
source_bindings = []
for row in manifest['frozen_sources_read']:
    got = binding(locations[row['id']])
    assert got['sha256'] == row['sha256'] and got['bytes'] == row['size'], row['id']
    source_bindings.append(dict(source_id=row['id'], **got))
for row in manifest['formal_materials_read']:
    got = binding(ROOT / row['path'])
    assert got['sha256'] == row['sha256'] and got['bytes'] == row['bytes'], row['path']

execution = load(HERE / 'interface-execution.json')
audit = load(HERE / 'interface-audit.json')
assert execution['exit_code'] == 0
assert execution['source_sha256'] == binding(HERE / 'original/spe_dp.py')['sha256']
assert execution['script_sha256'] == binding(HERE / 'check_interfaces.py')['sha256']
assert audit['source_sha256'] == execution['source_sha256']
assert audit['original_solve_calls'] == audit['original_reconstruct_calls'] == 3
assert audit['original_verify_result_calls'] == 4
assert audit['original_verify_successes'] == 3 and audit['original_verify_expected_rejections'] == 1
assert audit['LP_calls'] == 0 and not audit['stored_random_or_LP_points_rerun']
assert len(audit['cases']) == 3
assert audit['cases'][2]['exact_rejection'] == {'history': [], 'alternative': 1, 'slack': '-1'}
assert load(HERE / 'interface-stdout.txt') == {k:v for k,v in audit.items() if k != 'cases'}
assert (HERE / 'interface-stderr.txt').read_bytes() == b''

receipt = load(RECEIPT)
assert receipt['id'] == '44c5afc4b6e2b6b72b90'
assert all(receipt[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
assert receipt['targets'] == [str(DOC.relative_to(ROOT))]
assert receipt['disposition'] == 'integrated'

shared_paths = [
    HERE.parent / 'r70-strategy-lp-program/replay/execution.json',
    HERE.parent / 'r70-strategy-lp-program/replay/dp-return.json',
    HERE.parent / 'r70-strategy-lp-program/replay/complete-strategy.json',
    HERE.parent / 'r70-strategy-lp-program/exact-cone-audit.json',
    HERE.parent / 'r70-six1-best-data/point-audit.json',
    HERE.parent / 'r70-six1-best-data/execution.json',
]
shared = load(shared_paths[0])
assert shared['counts']['solve'] == 1 and shared['counts']['linprog'] == 7
assert shared['original_verify_result_calls'] == 0
assert binding(shared_paths[2])['sha256'] == shared['files']['complete-strategy.json']['sha256']
dp = load(shared_paths[1])
assert [dp[k] for k in ['min_welfare','optimum','root_outcomes','states']] == [43,58,6,1716]
data = load(shared_paths[4])
assert data['status'] == 'PASS'
assert data['input_bindings'][2]['sha256'] == binding(shared_paths[2])['sha256']
assert all(data['points'][k]['comparisons'] == 137256 for k in ['random','lp_integer'])

links = []
for p in [DOC, HERE / 'README.md']:
    for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text()):
        if href.startswith(('https:','http:','#','source:')):
            continue
        target = (p.parent / href.split('#')[0]).resolve()
        assert target.exists(), (p, href)
        links.append({'from': str(p.relative_to(ROOT)), 'target': str(target.relative_to(ROOT))})

files = sorted(p for p in HERE.rglob('*') if p.is_file() and p.name != 'self-check.json')
ast_count = json_count = 0
for p in files + [RECEIPT]:
    if p.suffix == '.py':
        ast.parse(p.read_text(), filename=str(p)); ast_count += 1
    if p.suffix == '.json':
        load(p); json_count += 1
report = {
    'status': 'PASS_STATIC_ONLY',
    'scope': 'Source/event byte bindings, saved report consistency, JSON/AST, local links and receipt; no original calls, coefficient scan, LP or mathematical rerun.',
    'frozen_source_bindings': source_bindings,
    'unchanged_formal_comparison_bindings': len(manifest['formal_materials_read']),
    'shared_saved_report_bindings': [binding(p) for p in shared_paths],
    'shared_formal_read': [
        'archives/customer-attraction/state/程序/六人七主题固定完整策略的福利比线性规划程序--程序.md',
        'archives/customer-attraction/state/计算/六人不交覆盖搜索点的随机记录与锐界实例--计算.md',
    ],
    'shared_formal_scope': 'Entire current texts read, including fixed-policy dual proof and two-point integer60 arithmetic; linked by path without circular final-document SHA bindings.',
    'ast_files': ast_count, 'json_files': json_count, 'local_links': len(links),
    'links': links,
    'artifacts': [binding(p) for p in files + [DOC, RECEIPT]],
    'self_hash_excluded': True,
    'new_mathematical_runs_during_static_check': 0,
}
(HERE / 'self-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k: report[k] for k in ['status','ast_files','json_files','local_links','new_mathematical_runs_during_static_check']}))
