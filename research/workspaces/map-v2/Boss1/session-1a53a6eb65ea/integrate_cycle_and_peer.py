"""Add the reviewed cycle packet and the independently reviewed matroid packet."""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import research_runtime as rr

def read(p): return json.loads(p.read_text())
d = read(ROOT / 'map/integration.json')
registry = read(ROOT / 'research/registry.json')
pins = {o['object_id']: rr.pin(o) for o in registry['objects']}
tasks = ['boss1-six-cycle-3a-6f1717619ab2bf55', 'unrelated-machines-3a-3a-2cfc52a90592a978']
inputs = {}; edges = {}; receipts = {}
for tid in tasks:
    task = read(ROOT / 'research/operations/map-v2/tasks' / (tid + '.json'))
    assert task['state'] == 'done' and tid in d['task_receipt_pins'], tid
    for oid, expected in task['definition']['input_pins'].items():
        assert pins[oid] == expected, (tid, oid)
        inputs[oid] = expected
    path = ROOT / 'map/receipts' / (tid + '.json')
    receipt = read(path)
    receipts[tid] = {'path': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    for asset in receipt['assets']:
        p = ROOT / asset['path']; raw = p.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == asset['sha256'], p
        if p.suffix != '.json': continue
        edge = json.loads(raw)
        if not isinstance(edge, dict) or 'edge_id' not in edge: continue
        assert asset['path'] in registry['edge_files'], p
        edges[edge['edge_id']] = asset
assert len(edges) == 3

note = ('Boss1 session-1a53a6eb65ea补充：已实质核入单环两核两边及Boss2两值作业拟阵一核一条ALL条件迁移。'
        '单环到旧两节点/三节点v2是whole：八奇集化简、较大own单集、两cross各可独担缺口、两上端点、固定全局权和三项充要均有独立解析推导；'
        '父Fréchet只贡献恒等式和自由基准。两值Santa开放接口加封顶/对偶/同值解码桥完整推出7/4+epsilon条件保证；'
        'Root核阈值网格非单调成功不变量及参数恒等式，fresh审查完整来源见peer-matroid-3d/audit-2cfc52a90592a978.md。'
        'q>=16外层可达反例只否冻结Lemma30入口不交性，不否对偶桥；71b旧绑定待另行repair，不据源审查冒称其修复或09e5主覆盖完成。'
        '本次连同前三包共采用67核心、42条准确关系；只清当前已交付且pins吻合的范围。')
if note not in d['review_note']: d['review_note'] += '\n' + note
for scope, summary in [
    ('archives/customer-attraction', '父Fréchet固定四态必要界到同模型精确单环的自由基准贡献；普通目录half仍开放。'),
    ('archives/customer-attraction/subarchives/six-providers', '精确单环完整支付旧v2两节点六面、任意非负权支持/三项充要、严格例和全部旧奇集界；不升级多环或SPE实现。'),
    ('archives/unrelated-machines', '两值Santa开放算法接口与已证封顶对偶桥用一条ALL迁移，终点为完整原整数基job保证；源算法及冻结递归修复仍开放。')]:
    row = d['archive_reviews'][scope]
    if summary not in row['comparison_scope']: row['comparison_scope'] += '\n' + summary
    if note not in row['outcome']: row['outcome'] += '\n' + note
cross = d['cross_archive_review']
summary = 'Boss1只采用两份具有实际映射的关系：同客户模型内的单环专化，以及restricted resource-matroid Santa到job-matroid原基调度的条件转移。没有据“环”或“拟阵”等名称新造跨存档同构。'
if summary not in cross['outcome']: cross['outcome'] += '\n' + summary

pending = d.get('pending_changes', {})
pending_objects = set(pending.get('object_ids', [])) - set(inputs)
pending_edges = set(pending.get('edge_ids', [])) - set(edges)
for eid in pending_edges: pending_objects.update(d.get('edge_endpoints', {}).get(eid, []))
pending_scopes = set(pending.get('archive_scopes', []))
affected_scopes = {s for oid in pending_objects for s in d.get('object_scopes', {}).get(oid, [])}
# The two customer-attraction changes were exactly the cap and cycle inputs.
# All remaining changed relations are unrelated-machine relations; do not clear them.
for scope in ['archives/customer-attraction', 'archives/customer-attraction/subarchives/six-providers']:
    if scope not in affected_scopes and not any(eid.startswith(('ca-', 'cag-', 'customer-attraction')) for eid in pending_edges):
        pending_scopes.discard(scope)
        row = d['archive_reviews'][scope]
        row['unresolved'] = [s for s in row.get('unresolved', []) if s != 'Updated inputs/relations require this preserved comparison to be reviewed again']
d['pending_changes'] = {'object_ids': sorted(pending_objects), 'edge_ids': sorted(pending_edges), 'archive_scopes': sorted(pending_scopes | affected_scopes)}
(ROOT / 'map/integration.json').write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
result = {'status': 'CYCLE_AND_CONDITIONAL_MATROID_TRANSFER_ADOPTED', 'receipts': receipts,
          'reviewed_object_pins': inputs, 'reviewed_edges': edges, 'remaining_pending': d['pending_changes'],
          'review_scope': 'Two done packets only. The old 71b binding and its owner/source repair remain pending.'}
(HERE / 'cycle-and-peer-integration-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'edges': len(edges), 'remaining_pending_counts': {k:len(v) for k,v in d['pending_changes'].items()}}, ensure_ascii=False))
