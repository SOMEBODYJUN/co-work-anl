"""Apply only the three reviewed receipts; preserve unrelated pending changes."""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import research_runtime as rr

TASKS = [
    'boss1-hypergeo-endpoint-refresh-repair-f31d22275b70a2bd',
    'customer-attraction-3a-3a-b7bf2892514415df',
    'customer-attraction-3a-3a-bc7462157647be8f',
]
def read(path):
    return json.loads(path.read_text())

registry = read(ROOT / 'research/registry.json')
current = {o['object_id']: rr.pin(o) for o in registry['objects']}
integration_path = ROOT / 'map/integration.json'
d = read(integration_path)
before = read(HERE / 'preassemble-first-three.json')
reviewed_objects = {}
reviewed_edges = {}
receipts = {}
coverage_counts = {}
for tid in TASKS:
    task = read(ROOT / 'research/operations/map-v2/tasks' / (tid + '.json'))
    assert task['state'] == 'done', tid
    definition = task['definition']
    for oid, expected in definition['input_pins'].items():
        assert current[oid] == expected, (tid, oid, 'changed input')
        reviewed_objects[oid] = expected
    rp = ROOT / 'map/receipts' / (tid + '.json')
    receipt = read(rp)
    receipts[tid] = {'path': rp.relative_to(ROOT).as_posix(),
                     'sha256': hashlib.sha256(rp.read_bytes()).hexdigest()}
    assert tid in d['task_receipt_pins'], (tid, 'not assembled')
    coverage_counts[tid] = len(receipt['coverage'])
    for asset in receipt['assets']:
        path = ROOT / asset['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == asset['sha256'], path
        assert asset['path'] in registry['edge_files'], (path, 'not canonical')
        edge = read(path)
        reviewed_edges[edge['edge_id']] = {'path': asset['path'], 'sha256': asset['sha256']}

assert sum(coverage_counts.values()) == 64
assert len(reviewed_edges) == 39
note = ('Boss1 session-1a53a6eb65ea：实质审完三份恢复交付的64核心、22条新写或替换关系及17条原路径原SHA保留关系。'
        'P7全局索引/J整源、真T2联合七包络、十三行max必要投影、signed H4/owner与PC条件归约、'
        'superset席位到sunflower全锐界及三尾真实负返还均按原目标核范围。'
        '完整推导、局部贡献和条件前提分开，四支持线不冒成第五阈值。'
        '实际有限复核及Boss独立代数详见research/workspaces/map-v2/Boss1/session-1a53a6eb65ea/first-three-review.md。'
        '旧新pending取并集，仅清本轮已done且当前pins逐项吻合的实读对象和39关系，其他源修复及未交单环包继续保留。')
if note not in d['review_note']:
    d['review_note'] += '\n' + note
if 'Boss1' not in d['reviewed_by'].split('; '):
    d['reviewed_by'] += '; Boss1'
row = d['archive_reviews']['archives/customer-attraction']
scope_note = '本轮64核心恢复比较：同σ真后继、索引菜单、静态安全量词、结构子域、signed预算与指定反例资格；准确范围见本轮三收据及Boss实质审查。'
if scope_note not in row['comparison_scope']:
    row['comparison_scope'] += '\n' + scope_note
if note not in row['outcome']:
    row['outcome'] += '\n' + note
opening = 'Boss1本轮：一般half、PC动态比较、H4/owner普遍付款、一般三尾跨角色预算和非sunflower目录预算仍开放；已完成的特例及条件接口不替代这些义务。'
if opening not in row.setdefault('open_math', []):
    row['open_math'].append(opening)
cross = d['cross_archive_review']
cross_note = 'Boss1本轮三包在同一客户吸引模型内完成精确范围比较，未据主题相似建立其它存档模型迁移；六人单环另包尚在交付。'
if cross_note not in cross['outcome']:
    cross['outcome'] += '\n' + cross_note

old_pending = before.get('pending_changes', {})
new_pending = d.get('pending_changes', {})
edge_pending = (set(old_pending.get('edge_ids', [])) | set(new_pending.get('edge_ids', []))) - set(reviewed_edges)
object_pending = (set(old_pending.get('object_ids', [])) | set(new_pending.get('object_ids', []))) - set(reviewed_objects)
for eid in edge_pending:
    object_pending.update(d.get('edge_endpoints', {}).get(eid, []))
scope_pending = set(old_pending.get('archive_scopes', [])) | set(new_pending.get('archive_scopes', []))
for oid in object_pending:
    scope_pending.update(d.get('object_scopes', {}).get(oid, []))
d['pending_changes'] = {'object_ids': sorted(object_pending), 'edge_ids': sorted(edge_pending),
                        'archive_scopes': sorted(scope_pending)}
for scope, unresolved in before.get('archive_unresolved', {}).items():
    if scope in d['archive_reviews']:
        row = d['archive_reviews'][scope]
        row['unresolved'] = list(dict.fromkeys(row.get('unresolved', []) + unresolved))
cross['unresolved'] = list(dict.fromkeys(cross.get('unresolved', []) + before.get('cross_archive_unresolved', [])))
integration_path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
result = {'status': 'THREE_REVIEWED_RECEIPTS_INTEGRATED_OTHER_PENDING_PRESERVED',
          'receipts': receipts, 'coverage_counts': coverage_counts,
          'reviewed_object_pins': reviewed_objects, 'reviewed_edges': reviewed_edges,
          'remaining_pending': d['pending_changes'],
          'scope': 'Actual three-packet integration only; open mathematics and whole-stage work continue.'}
(HERE / 'first-three-integration-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'core_count': sum(coverage_counts.values()),
                  'edge_count': len(reviewed_edges), 'input_count': len(reviewed_objects),
                  'remaining_pending_counts': {k: len(v) for k, v in d['pending_changes'].items()}}, ensure_ascii=False))
