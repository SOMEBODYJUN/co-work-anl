"""Apply only Boss1's actual mathematical review to the latest native assembly."""
from pathlib import Path
import hashlib
import json
import sys
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import research_runtime as rr

def read(p): return json.loads(p.read_text())
def add(container, key, text):
    if text not in container.get(key, ''):
        container[key] = container.get(key, '') + '\n' + text

d = read(ROOT / 'map/integration.json')
reg = read(ROOT / 'research/registry.json')
assert d['registry_pin'] == rr.pin(reg), 'Use the latest native assembly first'
pins = {o['object_id']: rr.pin(o) for o in reg['objects']}
primary = ['boss1-six-cycle-3a-1c349baa3fc5420b',
           'boss1-six-cycle-3a-d7469a7763ca64c6',
           'boss5-asahiro-sha-current-repair-16bd7e5e49c5be05']
peer = ['map-repair-7491db9b84448830', 'map-repair-a78e71b42e9bd669',
        'unrelated-machines-3a-3a-09e5f7fd803e7a8d']
reviewed_inputs = {}; reviewed_core = set(); edges = {}; receipts = {}
for tid in primary + peer:
    t = read(ROOT / 'research/operations/map-v2/tasks' / (tid + '.json'))
    assert t['state'] == 'done', tid
    receipt_path = ROOT / 'map/receipts' / (tid + '.json')
    rc = read(receipt_path)
    assert d['task_receipt_pins'].get(tid) == rr.pin(rc), ('receipt metadata changed', tid)
    for oid, pin in t['definition']['input_pins'].items():
        assert pins[oid] == pin, (tid, oid)
        reviewed_inputs[oid] = pin
    reviewed_core.update(t['definition']['object_ids'])
    if tid == primary[2]:
        # All four current MMO/PARTITION/target contracts were independently read.
        reviewed_core.update(t['definition']['read_object_ids'])
    receipts[tid] = {'path': receipt_path.relative_to(ROOT).as_posix(),
                     'sha256': hashlib.sha256(receipt_path.read_bytes()).hexdigest()}
    for asset in rc['assets']:
        p = ROOT / asset['path']; raw = p.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == asset['sha256'], p
        if p.suffix != '.json': continue
        e = json.loads(raw)
        if not isinstance(e, dict) or 'edge_id' not in e: continue
        assert 'source_ids' in e and 'target_ids' in e, p
        assert asset['path'] in reg['edge_files'], p
        assert d['edge_pins'].get(e['edge_id']) == rr.pin(e), ('edge metadata changed', e['edge_id'])
        edges[e['edge_id']] = asset
assert len(edges) == 19, len(edges)

cag = ('Boss1本轮将两个六提供者聚合对象的主3A比较正式接入：十三条现行canonical按原路径原SHA复用，'
       '全部为准确局部贡献，原共同ALL和conditional模式保留，十五个declared来源接口逐对闭合。'
       '固定16hist的十份有限最优、自由ZZ与单结构624闭包不升级为全类型保证；'
       '十二标签根菜单排所有六A顺序与指定A5的首个失败分开，计数集合缓存不等于全局计数策略。'
       '全部512客户型的3056整面排除与统一改善独立：δ真实损失、ROOT270的C外余量、六actual SAFE(C)、'
       '全部64列旧余款和自由E_C符号共同给约.4417591884普遍界；没有达到half或构成SPE反例。'
       'Root实际独立推导与证据边界见six-packets-root-math-review.md，两worker实际读范围和机器解析分列。')
mmo = ('Boss1正式采用Asahiro当前v4修复的三条whole归约，旧三资产逐一replaced。'
       '正二进制PARTITION逐下标平行边保持精确半分；三边路(w_i,B,w_i)的中边强制和逐端降载给简单SP、'
       '树宽2而不冒称简单外平面；安全显式join的伪多项式性足付弱标签，未使用印刷快速指数。'
       '两个私有B anchor给实际最大件承诺，统一全输入位多项式finder加验证决定PARTITION；'
       '给定目标路径Q=(0,B)、U=4B、h=0不受反驳。该正式交付现在支付旧pending绑定，旧3D报告不是替代品。')
peer_note = ('Boss1另完成两份Kun修复和BLMRS可达反例的独立3D采用。'
             '两次孤点补齐的误差、非二分绝对谱、固定模数相对稠密阶数及M不依赖k的量词完整；'
             '同签名CSP结论经异型高围长桥、有限模板反链marker、现代二分以及低元/零元剖面分支得到，'
             '保有限析取且不倒填历史作者证明。BLMRS q>=16从合法外层达到第一次入口重叠，'
             '且另有阈值1可行解，只反驳冻结v1 Lemma30(1)的全称不交性。'
             '已done的09e5两核心可以采用；最新71b与566d旧绑定已由Boss2 wave4联合正式repair交付，'
             '不再称绑定修复未交，但完整资源算法仍open，给定见证舍入保持条件局部贡献。详见additional-peer-math-review.md及三份fresh报告。')
add(d, 'review_note', cag + '\n' + mmo + '\n' + peer_note)
if 'Boss1' not in d.get('reviewed_by', ''): d['reviewed_by'] = d.get('reviewed_by','') + '; Boss1'
for scope in ['archives/customer-attraction', 'archives/customer-attraction/subarchives/six-providers']:
    row = d['archive_reviews'][scope]
    add(row, 'comparison_scope', '两个六提供者当前聚合核心及十五个实际来源比较，十三条既有局部贡献。')
    add(row, 'outcome', cag)
row = d['archive_reviews']['archives/unrelated-machines']
add(row, 'comparison_scope', '当前四端点MMO修复、Kun四核心及BLMRS两个精确反例核心的实际3D复核。')
add(row, 'outcome', mmo + '\n' + peer_note)
add(d['cross_archive_review'], 'outcome',
    'Boss1本轮的取向到实际调度/未知目标搜索只通过明列的端点资格、权和anchor映射；'
    'CAG必要矩阵、Kun关系结构及BLMRS拟阵递归各守自身模型，未据术语相似补免费跨档迁移。')

published = json.loads(subprocess.run(['git', 'show', 'HEAD:map/integration.json'], cwd=ROOT, check=True, capture_output=True, text=True).stdout)
pending = d.get('pending_changes', {})
preserved = published.get('pending_changes', {})
po = (set(pending.get('object_ids', [])) | set(preserved.get('object_ids', []))) - reviewed_core
pe = (set(pending.get('edge_ids', [])) | set(preserved.get('edge_ids', []))) - set(edges)
# A reviewed endpoint still needed by an unreviewed relation remains pending there.
for eid in pe: po.update(d.get('edge_endpoints', {}).get(eid, []))
ps = set(pending.get('archive_scopes', [])) | set(preserved.get('archive_scopes', []))
affected = {scope for oid in po for scope in d.get('object_scopes', {}).get(oid, [])}
for scope in ['archives/customer-attraction', 'archives/customer-attraction/subarchives/six-providers']:
    if scope not in affected and not any(eid.startswith(('ca-', 'cag-', 'customer-attraction', 'boss2-six-cross')) for eid in pe):
        ps.discard(scope)
        row = d['archive_reviews'][scope]
        row['unresolved'] = [s for s in row.get('unresolved', []) if s != 'Updated inputs/relations require this preserved comparison to be reviewed again']
d['pending_changes'] = {'object_ids': sorted(po), 'edge_ids': sorted(pe), 'archive_scopes': sorted(ps | affected)}
(ROOT / 'map/integration.json').write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
result = {'status':'SIX_MMO_AND_THREE_PEER_PACKETS_ADOPTED', 'receipts': receipts,
          'reviewed_input_pins': reviewed_inputs, 'reviewed_primary_and_whole_contracts': sorted(reviewed_core),
          'reviewed_edges': edges, 'remaining_pending': d['pending_changes']}
(HERE / 'six-mmo-integration-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status':result['status'], 'edges':len(edges),
                  'remaining_pending_counts':{k:len(v) for k,v in d['pending_changes'].items()}}, ensure_ascii=False))
