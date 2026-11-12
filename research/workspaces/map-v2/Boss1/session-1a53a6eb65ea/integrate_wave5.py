"""Adopt the three actual wave5 mathematical reviews on a native assembly.

Keep native hashes/metadata, preserve the latest published pending, and clear
only reviewed current contracts.  A previously reviewed hypergraph edge is re-adopted only if unchanged;
otherwise its actual replacement route and current endpoints remain pending.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import research_runtime as rr

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def add(o, key, s):
    if s not in o.get(key, ''): o[key] = o.get(key, '') + '\n' + s

d = read(ROOT/'map/integration.json')
reg = read(ROOT/'research/registry.json')
assert d['registry_pin'] == rr.pin(reg), 'Native assembly metadata changed'
pins = {o['object_id']:rr.pin(o) for o in reg['objects']}
frozen = read(HERE/'wave5-three-final-validation.json')
reviewed = set(); accepted = {}; receipts = {}
for tid, saved in frozen.items():
    t = read(ROOT/'research/operations/map-v2/tasks'/(tid+'.json'))
    assert t['state']=='done', tid
    rcpath = ROOT/saved['receipt_path']; rc = read(rcpath)
    assert sha(rcpath)==saved['receipt_sha256'], tid
    assert d['task_receipt_pins'].get(tid)==rr.pin(rc), tid
    for oid,pin in saved['input_pins'].items(): assert pins[oid]==pin, (tid,oid)
    assert t['definition']['input_pins']==saved['input_pins']
    reviewed.update(t['definition']['object_ids'])
    receipts[tid]={'path':saved['receipt_path'],'sha256':sha(rcpath)}
    for a in rc['assets']:
        p=ROOT/a['path']; assert sha(p)==a['sha256'], a['path']
        if p.suffix!='.json': continue
        e=read(p)
        if not isinstance(e,dict) or 'edge_id' not in e: continue
        assert a['path'] in reg['edge_files'], a['path']
        assert d['edge_pins'].get(e['edge_id'])==rr.pin(e), e['edge_id']
        accepted[e['edge_id']]=a
        reviewed.update(e['source_ids']); reviewed.update(e['target_ids'])
assert len(accepted)==7, len(accepted)

# Re-adopt only an immutable current edge; otherwise preserve its pending route.
old=read(HERE/'latest-pending-review-result.json')
eid='exact-four-to-one-v4-and-biregularization-to-three-uniform-independent-set-9fa9ce8a7e4a75ec'
a=old['reviewed_edges'][eid]; e=read(ROOT/a['path'])
prior_reconfirmed=(sha(ROOT/a['path'])==a['sha256'] and a['path'] in reg['edge_files']
    and d['edge_pins'].get(eid)==rr.pin(e)
    and all(pins[oid]==old['reviewed_endpoint_pins'][oid] for oid in e['source_ids']+e['target_ids']))
if prior_reconfirmed:
    reviewed.update(e['source_ids']+e['target_ids']); accepted[eid]=a
    prior_note='上一轮已完整审读的perfect exact4+双正规化超图whole边及其三端此次逐SHA/pin未变，接回已成立审读；未重跑科学计算。'
else:
    prior_note='本次同步发现超图目标M-9f8033b6e1a4485b97636171b09f8218已为v5且旧9fa9边不再canonical；不能沿用上一轮v4审读清除其pending。当前替代boss2-wave6-hypergraph-repair-edfcf6a2548b4d1c仍claimed/Boss2，保留该修复路线及未复核标记。'

cag=('Boss1 wave5新增五条独立局部贡献：BG2六行、DEEP一行、PC2四行、PC3五行、最大根界1一行，'
     '合计十七条；各来源的多行放在同一边，不拆成十七个单独支撑。全部限来源登记的真实集合目录/覆盖单射子域，'
     '保持同一σ、同一个K与原actual收益；PC2外加一次u2而PC3已含u3，DEEP负预算系数也取ceil。'
     '广标签全53行由现行活跃行正文独立证明，已有whole边只从53行经6144成熟条件证书和负K余额合成half，'
     '不反向支付源53行。BG3、MAX-BG2、最大根界2的独有条件与当前未活跃理由分别实读记入isolated覆盖；'
     '两最大根的r=K/4交叉不制造无用自环。八核心5 linked/3 isolated，无新来源勘误或具体未接续比较。')
um=('Boss1 wave5正式采用旧623当前版本替代：k=2的simple bipartite Δ≤3归约、逐尾端负担双射、'
    'L(G)普通diamond排除完整保持2/3 gap和每固定c<3/2障碍，旧独立proof原SHA retained。'
    '另有blockrank→AMO cactus的whole迁移：子块任务不交、父点初载只计一次，非gate叶交换保精确消息，'
    'gate容量裁剪只用于全图预算；剩余环最小gate负担为较轻边。每环两个森林扫描及局部见证指针另付O(n)算术，'
    '2-degeneracy给OPT≤2k，原零初载整数域二分付O(n log k)，k=1单独线性，位费用另为poly(L)。'
    '不从泛型poly(L)直接推线性，也不反向扩域到异端有理/平行任务。该3B没有取代他人尚未完成的cactus主3A。'
    +prior_note)
add(d,'review_note',cag+'\n'+um)
if 'Boss1' not in d.get('reviewed_by',''): d['reviewed_by']=d.get('reviewed_by','')+'; Boss1'
add(d['archive_reviews']['archives/customer-attraction'],'comparison_scope','八个五人局部来源、五个实际活跃贡献及已存53行→half的独立后段。')
add(d['archive_reviews']['archives/customer-attraction'],'outcome',cag)
add(d['archive_reviews']['archives/unrelated-machines'],'comparison_scope','k=2取向到diamondless完整迁移、cactus与块秩的精确算法/费用比较，及已冻结超图审读的未变绑定接续。')
add(d['archive_reviews']['archives/unrelated-machines'],'outcome',um)
add(d['cross_archive_review'],'outcome','本轮把机器边任务与取向尾端的负担保持桥完整付清，CAG来源仍准确限覆盖单射子域；没有以相同名称或图类建立额外跨档保证。')

route='boss2-wave4-root-repair-5da342428ed683bc'
rt=read(ROOT/'research/operations/map-v2/tasks'/(route+'.json'))
if rt['state']=='done':
    add(d['archive_reviews']['archives/unrelated-machines'],'outcome',
        '777及03312旧绑定现已由Boss2的'+route+'正式done；本轮不重新发包，不将前轮claimed观察当作当前状态。其现行独立交付与同行整合保持原有作用范围。')

published=json.loads(subprocess.run(['git','show','HEAD:map/integration.json'],cwd=ROOT,check=True,capture_output=True,text=True).stdout)
p=d.get('pending_changes',{}); oldp=published.get('pending_changes',{})
po=(set(p.get('object_ids',[]))|set(oldp.get('object_ids',[])))-reviewed
pe=(set(p.get('edge_ids',[]))|set(oldp.get('edge_ids',[])))-set(accepted)
pending_endpoints=dict(d.get('edge_endpoints',{}))
if not prior_reconfirmed: pending_endpoints[eid]=e['source_ids']+e['target_ids']
for x in pe: po.update(pending_endpoints.get(x,[]))
ps=set(p.get('archive_scopes',[]))|set(oldp.get('archive_scopes',[]))
affected={scope for oid in po for scope in d.get('object_scopes',{}).get(oid,[])}
unscoped_edges=any(not pending_endpoints.get(x) for x in pe)
for scope in ['archives/customer-attraction','archives/unrelated-machines']:
    if scope not in affected and not unscoped_edges:
        ps.discard(scope)
        row=d['archive_reviews'][scope]
        row['unresolved']=[x for x in row.get('unresolved',[]) if x!='Updated inputs/relations require this preserved comparison to be reviewed again']
d['pending_changes']={'object_ids':sorted(po),'edge_ids':sorted(pe),'archive_scopes':sorted(ps|affected)}
(ROOT/'map/integration.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
result={'status':'WAVE5_ACTUAL_REVIEWS_ADOPTED','receipts':receipts,'new_or_replaced_edges':7,
        'unchanged_prior_hypergraph_review_reconfirmed':a if prior_reconfirmed else None,'prior_hypergraph_review_note':prior_note,'reviewed_objects':sorted(reviewed),'pending':d['pending_changes']}
Path('/workspace/scratch/1a53a6eb65ea/wave5-integration-reviewed.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'pending':d['pending_changes']},ensure_ascii=False))
