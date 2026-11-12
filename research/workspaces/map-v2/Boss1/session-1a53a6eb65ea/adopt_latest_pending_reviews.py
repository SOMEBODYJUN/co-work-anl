"""Adopt actual narrow 3D reviews after integrate_six_and_mmo.py.

Run the two helpers in this order on a native assembly.  The first helper
preserves the latest published unresolved pending; this one clears only its
independently read current contracts.  Neither invents native metadata.
"""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import research_runtime as rr

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def add(o, k, s):
    if s not in o.get(k, ''): o[k] = o.get(k, '') + '\n' + s

d = read(ROOT / 'map/integration.json')
reg = read(ROOT / 'research/registry.json')
assert d['registry_pin'] == rr.pin(reg)
pins = {o['object_id']: rr.pin(o) for o in reg['objects']}
tasks = ['boss5-mz-visual-repair-3c1fe8fa00844a15',
         'boss5-mz-visual-repair-9fa9ce8a7e4a75ec',
         'boss5-localfix-repair-8c728e95a224313d',
         'boss2-wave4-repair-8a7f75234096249d']
expected = {
 'um-129516aa-minrep-source-and-sparsification-pay-conditional-parameter-repair':'a2bbdc8edaedb3c5c1c1ae1cdf595b796af41ba709ac9692ec2f520c41676605',
 'exact-four-to-one-v4-and-biregularization-to-three-uniform-independent-set-9fa9ce8a7e4a75ec':'b88c501a9db991931813fb90707a0b0b3595195597a57a0b6339ab6f765379fc',
 'exact-four-to-one-v4-to-eight-color-independent-set-8c728e95a224313d':'2154e7f238a0764c054b871cab7fb3ecf47bc02d57a23851d8a3dc9e98a5d27a',
 'eight-color-independent-set-v4-to-three-color-gap-8c728e95a224313d':'7fcb8fcc3c8612224e9a3af03f9cc5111e89de3e13159a0b8520ee646af56c13',
 'blmrs-resource-rounding-finishes-local-search-heavy-light':'3ebb41af1effd7bd92064cbb826963c2a39d9ca79f115c112a2eba4916cae20f',
}
reviewed = set(); edges = {}; receipts = {}
for tid in tasks:
    t = read(ROOT / 'research/operations/map-v2/tasks' / (tid + '.json'))
    assert t['state'] == 'done', tid
    rcpath = ROOT / 'map/receipts' / (tid + '.json')
    rc = read(rcpath)
    assert d['task_receipt_pins'].get(tid) == rr.pin(rc), tid
    for oid, pin in t['definition']['input_pins'].items():
        assert pins[oid] == pin, (tid, oid)
    receipts[tid] = {'path':rcpath.relative_to(ROOT).as_posix(), 'sha256':sha(rcpath)}
    for a in rc['assets']:
        p = ROOT / a['path']
        assert sha(p) == a['sha256'], a['path']
        if p.suffix != '.json': continue
        e = read(p)
        if not isinstance(e, dict) or 'source_ids' not in e: continue
        assert a['path'] in reg['edge_files'], a['path']
        assert d['edge_pins'].get(e['edge_id']) == rr.pin(e), e['edge_id']
        assert all(pins[oid] == pin for oid,pin in e['endpoint_pins'].items())
        for ref in e.get('evidence', []):
            if isinstance(ref,dict) and 'path' in ref and 'sha256' in ref:
                assert sha(ROOT/ref['path']) == ref['sha256'], ref['path']
        if e['edge_id'] in expected: assert sha(p) == expected[e['edge_id']]
        edges[e['edge_id']] = a
        reviewed.update(e['source_ids']); reviewed.update(e['target_ids'])
assert set(expected) <= set(edges), set(expected)-set(edges)
assert len(edges) == 6, len(edges)

pcp = ('Boss1追加独立3D实读：MinRep的两前提参数修复保持conditional whole；'
       '旧δ=1/g与d=Θ(g log g)只付(1+Θ(log g))N，源先固定误差再选R的顺序不可倒置。'
       'Γ=5γ0/4、δ≤1/d及.03/sqrtΓ>g付严格2N/>2gN；正规化、实际字母表和log³g各自收费。'
       '三一致超图则由perfect exact4及独立近值保持双正规化共同给whole：度克隆均匀化、整数流逐边舍入误差、'
       '有向分层的约束ID边际、低影响解码、固定δ常数顺序及整数云无权化均付清。'
       'exact4→八色→三色两条whole当前链也已新读；induced-list桥不能由普通soundness替代，'
       '固定k先取t4=2^(2^k)、C=b(b(t4))和δ<1/C，再用二次arc反推。'
       '共享v4 MZ抽取勘误不进入FMW/GS20图与超图承重段。阅读与成熟合同复用边界见三个报告及graph附录。')
bl = ('Boss1采用已done的Boss2 wave4 BLMRS联合repair：71b两资产逐一replaced，566d补向量等价两资产原SHA retained。'
      '新边只从给定重轻见证出发；限制U→补分数基→舍入→零延拓独立向量→补原整数基逐步合法，'
      '一般值V/(2α)与两值大阈值V/α两个入口的条件分别明列。'
      '已有可达反例直接否定冻结v1递归不交性，完整a3仍open；保留的combined-rank证书和递归计数仍以前提成立为条件。'
      '历史审查中71b待修是当时状态，现由正式任务boss2-wave4-repair-8a7f75234096249d解决版本替代，未解决算法开放义务。')
route = ('Boss1新读623与777原数学及当前source：623的k=2简单二部Δ≤3构造、负载双射与非诱导diamondless证明成立，'
         '777的W/d向上舍入和安全平方表DP完整给等时双端FPTAS贡献。二者旧证据绑定尚须正式repair；'
         '777由claimed Boss2任务boss2-wave4-root-repair-5da342428ed683bc承接，623待按最新队列发布。'
         '不据本3D审读清除这两条非canonical旧边、四端点或整个UM范围。')
add(d,'review_note',pcp+'\n'+bl+'\n'+route)
row=d['archive_reviews']['archives/unrelated-machines']
add(row,'comparison_scope','MinRep条件参数修复、perfect exact4三项模型迁移、BLMRS给定见证收尾及两条取向接口的独立3D比较。')
add(row,'outcome',pcp+'\n'+bl+'\n'+route)
add(d['cross_archive_review'],'outcome','本轮PCP/图/超图、资源拟阵和取向到调度均按各自显式解码与常数顺序使用；未生成无证明的CAG跨模型边。')
before=d['pending_changes']
po=set(before.get('object_ids',[]))-reviewed
pe=set(before.get('edge_ids',[]))-set(edges)
for eid in pe: po.update(d.get('edge_endpoints',{}).get(eid,[]))
d['pending_changes']={'object_ids':sorted(po),'edge_ids':sorted(pe),
                      'archive_scopes':before.get('archive_scopes',[])}
assert len(po)==5 and len(pe)==2, d['pending_changes']
(ROOT/'map/integration.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
result={'status':'CURRENT_PCP_AND_BLMRS_REVIEW_ADOPTED','receipts':receipts,'reviewed_edges':edges,
        'reviewed_endpoint_pins':{oid:pins[oid] for oid in sorted(reviewed)},
        'remaining_pending':d['pending_changes'],
        'observation_correction':'graph worker曾观察本地尚未发布的空pending草案；Boss已恢复HEAD全部旧pending，仅按实际完成审查逐项清除，未发布空pending。'}
(HERE/'latest-pending-review-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'edges':len(edges),'pending':d['pending_changes']},ensure_ascii=False))
