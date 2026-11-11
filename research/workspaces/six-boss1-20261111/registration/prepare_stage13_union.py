"""Serial Main promotion of the universal coverage-union prefix family."""
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
PREFIX = 'research/workspaces/six-boss1-20261111/'
OID = 'customer-attraction/shared-maximal-potential-optimal-union-prefix-family'
BODY = 'archives/customer-attraction/state/引理/共同最大潜力主题的覆盖并前缀界--引理.md'
MODEL = 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'
H3ID = 'customer-attraction/shared-maximal-potential-three-tail-prefix-bound'
H3BODY = 'archives/customer-attraction/state/引理/共同最大潜力主题的三尾前接不等式--引理.md'


def bind(p):
    return {'path': p, 'sha256': sha256((REPO / p).read_bytes()).hexdigest()}


def section(path, start, end=None):
    s = (WS / path).read_text()
    s = s[s.index(start):]
    if end:
        s = s[:s.index(end)]
    return s


def main():
    raw = (REPO / 'research/registry.json').read_bytes()
    reg = json.loads(raw)
    assert not any(o['object_id'] == OID for o in reg['objects'])
    assert not (REPO / BODY).exists()
    assert bind(MODEL)['sha256'] == 'cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88'
    assert bind(PREFIX + 'averaged_menu_prefix_audit/freeze_manifest.json')['sha256'] == 'b08b3685c759eecb6d8a149e3b4500ce867bd8cf61717a4748e17906e5cfcc2e'
    # The frozen audit binds all mathematical sources before this formal promotion.
    header = '''---
id: "customer-attraction/shared-maximal-potential-optimal-union-prefix-family"
kind: "lemma"
type_tag: "引理"
title: "同一最大潜力主题的覆盖并前缀界与平均重数修正"
status: "proved-universal-necessary-bounds"
truth_status: "proved"
scope: "原六人完整历史纯SPE的任意六合法标签覆盖并；前三源31/25/19与第四源既有H3=10；一般平均重数另有显式修正"
source_refs:
  - "local:archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md"
  - "local:research/workspaces/six-boss1-20261111/main_averaged_menu_prefix.md"
  - "local:research/workspaces/six-boss1-20261111/main_optimal_union_prefix.md"
  - "local:research/workspaces/six-boss1-20261111/averaged_menu_prefix_audit/union_bridge.md"
  - "local:research/workspaces/six-boss1-20261111/main_union_comparison.md"
---

# 同一最大潜力主题的覆盖并前缀界与平均重数修正

本页保留完整普遍付款、全类型证明和限定系数锥的精确边界。原六人half问题仍开放。
同一actual前四最大f_P标签X，对任意六合法标签覆盖并U，前三源的系数是31、25、19，
第四源使用既有H3的10。覆盖并不是新增的合法行动；付款始终来自六条原合法查询。

本文的大X条件覆盖推论只是透明的代入例子。Main实读旧根近饱和正文后确认它被旧结果
支配，不能当成扩大已证区域；完整比较在最后一部分。新正文的独有承重是各源的细界、
显式平均重数修正、覆盖并桥和完整最优盒，不认领一般half或真实SPE锐性。

## A. 普遍覆盖并命题及正确付款

'''
    union = section('main_optimal_union_prefix.md', '## 1. 普遍覆盖并界')
    average = section('main_averaged_menu_prefix.md', '## 1. 原模型、量词与待证不等式')
    boxes_fixed = section('averaged_menu_prefix_audit.md', '## 5. 固定 θ=1/6', '## 7. 当前 dT=1')
    boxes_union = section('averaged_menu_prefix_audit/union_bridge.md', '## 3. 两个 θ 值', '## 5. 正式条件覆盖引理')
    comparison = section('main_union_comparison.md', '## 1. 实读并复核的旧结果')
    chunks = [header, union, '\n\n## B. 平均重数版本与完整解析余项证明\n\n', average,
              '\n\n## C. 两个精确系数锥及完整非唯一最优面\n\n', boxes_fixed, boxes_union,
              '\n\n## D. 与既有更强根粗覆盖界的比较\n\n', comparison]
    text = ''.join(chunks)
    # Route workspace-relative links from the formal body without changing frozen sources.
    for name in ['main_averaged_menu_prefix.md', 'main_optimal_union_prefix.md',
                 'main_prefix_safety_maxx_family.md', 'maxb_h3_bridge.md',
                 'main_union_comparison.md', 'averaged_menu_prefix_audit.md']:
        text = text.replace('](' + name + ')', '](../../../../' + PREFIX + name + ')')
    (REPO / BODY).write_text(text.rstrip() + '\n')
    extras = [
        'main_averaged_menu_prefix.md', 'main_averaged_menu_prefix.py', 'main_averaged_menu_prefix.json',
        'main_optimal_union_prefix.md', 'main_optimal_union_prefix.json', 'main_optimal_union_prefix_check.py',
        'averaged_menu_prefix_audit.md', 'averaged_menu_prefix_audit/verify_independent.py',
        'averaged_menu_prefix_audit/audit_result.json', 'averaged_menu_prefix_audit/restricted_cone_certificate.json',
        'averaged_menu_prefix_audit/union_bridge.md', 'averaged_menu_prefix_audit/verify_union_bridge.py',
        'averaged_menu_prefix_audit/union_bridge.json', 'averaged_menu_prefix_audit/union_bridge_certificates.json',
        'averaged_menu_prefix_audit/freeze_manifest.json',
        'main_union_comparison.md', 'main_union_comparison.json',
        'fourth_averaged_menu_cone.md', 'fourth_averaged_menu_cone/certificate.json',
        'fourth_averaged_menu_cone/union_domain_audit_128.json']
    evidence = [bind(MODEL), bind(H3BODY)] + [bind(PREFIX + p) for p in extras]
    evidence += [bind('archives/customer-attraction/state/推论/最大主题根近饱和的覆盖阈值--推论.md'),
                 bind('archives/customer-attraction/state/引理/任意人数近饱和根主题刚性--引理.md')]
    obj = {
        'object_id': OID, 'version': 1,
        'title': '同一最大潜力主题的覆盖并31/25/19前缀界与平均重数修正',
        'kind': 'lemma', 'truth_status': 'proved',
        'model': '有限单位客户、有限非空共同标签目录、六位单位提供者、每份完整有序历史纯SPE；终局客户按覆盖者均分。',
        'statement': '沿任意实际路径固定一次全目录f_P最大标签X，P为actual前四负载。对任意六合法标签覆盖并U，C_i u_i−(C_i−1)Σ_X1/(b_i+7−i)≥(1/6)Σ_U[x/(b_i+7−i)+(1−x)/(b_i+1)]，i=1,2,3的C为31,25,19；第四源由H3给10。前三源对原六查询重数d/6另有精确逐型修正Π=max_{0≤j≤r−2}j[d/(6n(n+j))−a*/(n+k)]，仅加于X外；a*=(5r−6)/(r(r−1))。完整非对称2r权锥在固定θ1/6及并集θ∈{0,1/6}域上最优均6r−5，全部中间MAX自由度分别为正文两个精确盒。',
        'quantifiers': '每个有限原六人实例、每份完整有序历史纯SPE、沿其同一实际路径选定的每个f_P最大标签X、任意六合法查询标签及其覆盖并U；允许查询标签重复，覆盖可重叠。系数锥另对所有全客户固定、各自独立的2r个非负权取逐型要求。',
        'assumptions': [
            'X仅在actual前四负载P上一次全目录取最大，不逐客户/源/查询重选',
            '源真改X后沿原策略真实续局；SAFE改末标签后重新取该标签自己的真实后继',
            '覆盖并预算由六条合法末位IC平均加d−o非负差支付，不把U加入行动目录、不删任何客户',
            '固定θ锥与θ0/1/6并集锥的中间MAX上端不同；任意平均d版保其显式Π'],
        'scope': '全域普遍必要界及其完整明定预算锥最优面；第四源10复用既有H3。有限16hist只是后续应用，不是本引理论域。',
        'objections': '没有证明一般2W≥OPT6，没有完整SPE反例。31/25/19是指定预算锥的最佳而非真实SPE锐性；普通大X条件half推论已被旧根近饱和粗界支配，不另认新进展。',
        'body': bind(BODY), 'evidence': evidence,
        'sources': [BODY] + ['material:' + p['path'] for p in evidence],
        'keywords': ['共同目录', 'same-X', 'OPT6覆盖并', '真实末位查询平均', 'SAFE', '完整非对称锥', 'six-providers']}
    reg['objects'].append(obj)
    mats = {m['path']: m for m in reg['materials']}
    for ref, isbody in [(obj['body'], True)] + [(e, False) for e in evidence]:
        if ref['path'] in mats:
            assert mats[ref['path']]['sha256'] == ref['sha256'], ref['path']
        else:
            new = dict(ref, disposition='objects' if isbody else 'attachment', object_ids=[OID],
                       reason='普遍覆盖并与平均重数真实付款、完整全型解析证明及独立精确系数锥审查；明确旧粗界支配。')
            reg['materials'].append(new)
            mats[ref['path']] = new
    out = HERE / 'stage13-union-registry-candidate.json'
    assert not out.exists()
    out.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n')
    (HERE / 'stage13-union-object.json').write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    summary = {'base_registry_sha256': sha256(raw).hexdigest(), 'object_id': OID,
               'body': obj['body'], 'objects': len(reg['objects']), 'materials': len(reg['materials'])}
    (HERE / 'stage13-union-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    edge = {
        'edge_id': 'ca-six-boss1-complete-history-and-H3-pay-union-prefix',
        'kind': 'implies', 'status': 'accepted', 'premises_mode': 'all',
        'relation_mode': 'unconditional', 'reviewed_by': 'Boss1/Main six-boss1-20261111',
        'source_ids': ['CAG-MODEL', H3ID], 'target_ids': [OID],
        'conditions': '恰六人；X固定最大化同一actual前四f_P；U为任意六合法标签覆盖并，保所有客户。',
        'roles': {'CAG-MODEL': '支付原源真IC/合法末标签SAFE、同一X的MAX、真实末节点六查询IC及d−o非负弱化。',
                  H3ID: '只支付第四源C4=10；前三源新权及全类型证明独立由原模型重建。',
                  OID: '得到前三源31/25/19和第四源10的普遍并集必要式，附平均Π与指定锥边界。'},
        'explanation': '先取强制X真实分支；六份末IC平均的d/6可加非负差变成o/6。固定α=5(r−1)、末SAFE=r、中间MAX=a*、末query=1，四角余项在θ=0/1/6全非负；C=6r−5。C4由已证H3对查询分子仿射并用相同弱化。三个支撑下界和中间MAX盒在正文逐系数证明，不借假想客户型的SPE可实现性。',
        'scope': '支付任意覆盖并U的完整必要不等式；不支付一般half或完整策略实现。',
        'contribution': {'result': '同一最大潜力标签对多个实际前缀的普遍覆盖并查询接口。',
                         'remaining': '还需将各源及跨真实分支约束共同支付到2W；新粗大小条件被旧根界支配。'},
        'evidence': [bind(MODEL), bind(H3BODY), obj['body'],
                     bind(PREFIX + 'main_averaged_menu_prefix.md'),
                     bind(PREFIX + 'averaged_menu_prefix_audit/union_bridge.md'),
                     bind(PREFIX + 'main_union_comparison.md')],
        'review_note': 'Main亲推原份额恒等式和全域四角证明，全文实读独立审稿及H3，核U不是合法新增动作、X与P固定、SAFE重取真实后继；比较并保留旧根强界。结构检查不替代数学审读。'}
    ep = REPO / 'map/edges/six-boss1-20261111/complete-history-H3-to-union-prefix.json'
    assert not ep.exists()
    ep.write_text(json.dumps(edge, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
