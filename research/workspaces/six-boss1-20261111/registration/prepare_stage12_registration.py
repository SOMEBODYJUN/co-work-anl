"""Main serial promotion: exact W10, whole-face AP exclusion and H3 lemma."""
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
PREFIX = 'research/workspaces/six-boss1-20261111/'
CID = 'customer-attraction/six-providers/cross-branch-necessary-system-20261111'
HID = 'customer-attraction/shared-maximal-potential-three-tail-prefix-bound'
APID = 'B10-AP-v1'
HPATH = 'archives/customer-attraction/state/引理/共同最大潜力主题的三尾前接不等式--引理.md'

def bind(path):
    return {'path': path, 'sha256': sha256((REPO / path).read_bytes()).hexdigest()}

def capacity(text):
    m = '# 一条不花实际末位收益的显式容量行'
    i = text.index(m)
    j = text.find('\n# ', i + len(m))
    return text[i:j if j >= 0 else None]

def main():
    raw = (REPO / 'research/registry.json').read_bytes()
    reg = json.loads(raw)
    byid = {o['object_id']: o for o in reg['objects']}
    assert APID in byid and 'CAG-MODEL' in byid
    comp = byid[CID]
    assert comp['version'] == 9
    assert comp['body'] == bind(comp['body']['path'])
    assert comp['body']['sha256'] == 'afb2fb1e0ef66364146ded221bc443364cb9e34cc8d48aeccd8d2df16b10a55c'
    assert HID not in byid
    body = REPO / comp['body']['path']
    old = body.read_text()
    new = old.replace('status: 九个必要LP精确闭合；共同最大主题容量投影排除第九点；原题开放',
                      'status: 十个必要LP精确闭合；早期同X约束排除第十最优面；原题开放', 1)
    marker = '| 完整624共同隐藏提升：20910行、20585列 | 精确原始与531个正对偶行权匹配 | 0.49304863960834766 |'
    assert marker in new
    new = new.replace(marker, marker + '\n| 完整共同X提升：22297行、21021列（20911单cut同值） | 463正对偶匹配；单cut投影452正权独立核验 | 0.4941319647988424 |', 1)
    new = new.replace('第六、七、八、九轮再次提高', '第六、七、八、九、十轮再次提高', 1)
    old_latest = '最新进展：第九点已被共同最大潜力主题的普遍必要式MC6精确排除；其438主行根排序包络和177条RZE单查询仍各有精确完成。新22297×21021完整共同X系统已装配，最优值待解。详见本文末三节。'
    assert old_latest in new
    new = new.replace(old_latest, '最新进展：第十完整共同X系统已精确最优约.4941319647988424，且与20911单MC6系统同值。第九整个最优面被MC6排除，第十整个最优面又被actual第三位同X查询A6的旧AP实例排除。H3前接、51早期AP与1260共同八格投影均已核；下一系统必须允许420交叠作为真实core重选。详见本文末尾新节。', 1)
    new = new.replace('当前主线继续在第九精确点上补强真实Z后继，并处理根尾的跨根与反向共同约束。',
                      '该阶段主线在第九精确点补强真实Z后继和跨根共同约束；当前状态见后续第十系统。', 1)
    new = new.replace('排除的是该具体原始点的全部共同X扩展，尚未据此排除旧系统整个最优面。',
                      '本节直接排除该具体原始点的全部共同X扩展；整个旧最优面的排除由后文独立对偶恒等式承担。', 1)
    new = new.replace('# 下一有限系统：完整共同X提升', '# 完整共同X提升的冻结输入（现已精确闭合）', 1)
    new = new.replace('旧531正对偶零扩展仍精确给W≥W9，但未声称新最优值。',
                      '准备阶段的旧531正对偶零扩展精确给W≥W9；新的匹配最优证书见下一节。', 1)
    new = new.replace('未求解。唯一下一发现入口为maxb_augmented_lp/full_lift/actions_request.json，\n实际结果必须再接完整精确原始/对偶，不以Actions绿色或浮点值替代。',
                      '未另行数值求解，后已由完整X对偶投影认证同值。唯一完整X发现入口为\nmaxb_augmented_lp/full_lift/actions_request.json；其真实结果和精确证书见下一节。', 1)
    new = new.rstrip() + '\n\n' + (HERE / 'stage12-computation-addition.md').read_text().strip() + '\n'
    assert capacity(new) == capacity(old)
    body.write_text(new)
    comp['version'] = 10
    comp['title'] = '十个必要系统的精确最优、同X早期分离与共同交叠边界'
    comp['statement'] = comp['statement'].replace('；不是旧最优面全排除。', '；其整个旧最优面后来由signed identity排除。')
    comp['statement'] = comp['statement'].replace('旧下界零扩展有效，新最优待求。', '旧下界零扩展有效，后续新精确最优如下。')
    comp['statement'] += (' 第十完整22297×21021系统精确最优W10约.4941319647988424，463正行权，完整原始/对偶和11164规范辅助独立PASS；新12行及新列余项消为γ倍MC6，故20911单cut也同值且452正行权。旧整个W9最优面signed identity给独立严格下界.4931316100867487，非当时精确最优。H3-X给全类型常数10，指定七预算逐型锥最优仍10；新点17行全正。旧任意锚AP对actual1/2/3的常数43、65/2、23生成51行，新点仅actual3→A6为负；通过全局相反行与3384步非负面零传播，AP39在整个W10最优面恒等于−2387360308883849167939463658247160398139890481107232380975950684899327/167642800338353195761909644781419248132422636155436956133783540969055432，精确排除整面但未给新定量下界。210组X/RZ或X/B4共同八格投影给1260行，当前固定y有5条O6负，420y在下一系统需升真实core。')
    comp['scope'] = comp['scope'].replace('九轮精确系统分别绑定各点', '十轮精确系统分别绑定各点')
    comp['scope'] += (' 当前第十点SHA5b1b...被AP39排除，且整个W10最优面有完整精确面证明。单cut与完整X仅目标最优值同等，不宣称投影可行域相等。六面八格是局部充要合同，5处失败仅及给定x/y，不排其重选；未证明跨组全客户律或完整SPE。')
    comp['quantifiers'] += ' H3及早期AP均在各自真实来源使用同一个合法X；AP39整面结论只对冻结22297矩阵的W10面，六面合同对任意非负二元组质量局部成立。'
    comp['assumptions'].append('22297中420新y仍为单查询虚拟上包络；追加own六面后必须作为真实core，不能继续canonical_min；旧10744辅助按各自不变合同保留')
    comp['body'] = bind(comp['body']['path'])

    hfiles = '''
maxb_h3_bridge.md
maxb_h3_bridge/rows_17.json
maxb_h3_audit.md
maxb_h3_audit/independent_check.py
maxb_h3_audit/audit_result.json
maxb_h3_pair_strength.md
maxb_h3_pair_strength/check_exact.py
maxb_h3_pair_strength/exact_certificate.json
maxb_h3_pair_strength/verification.json
main_h3_on_5b1b.json
'''.split()
    sources = [byid['CAG-MODEL']['body']['path'], byid[APID]['body']['path']]
    hevidence = [bind(p) for p in sources] + [bind(PREFIX + p) for p in hfiles]
    hlemma = {
        'object_id': HID, 'version': 1,
        'title': '同一末两位最大潜力主题向第四位真实三尾源的常数10前接',
        'kind': 'lemma', 'truth_status': 'proved', 'model': byid['CAG-MODEL']['model'],
        'statement': '六人完整SPE任意三行动有序历史h，按σ取第四行动A并令P=b+1_A；固定同一全目录f_P最大标签X。强制第四位X后取真实Y,Z，则对每个合法Q有10u4−9Σ_X1/(b+3)≥Σ_(X∩Q)1/(b+3)+Σ_(Q\\X)1/(b+1)。四份预算为源IC、两份同X最大性和真实末位查询，全部128客户型余项解析非负。再加TP(Q,X),TP(Q,Q),TP(X,X)的指定七权逐型锥最小C仍为10，完整最优面为(10,α,2,1,0,0,0),1≤α≤6/5。',
        'quantifiers': '每个原六人共同目录完整有序历史纯SPE、每条合法三行动前缀（可离轨）、每个按该前缀真实续局定义的全目录f_P最大标签X及每个合法Q。七权最优仅对正文明确的非负全局预算权和128逐型余项锥。',
        'assumptions': ['b是三名过去行动者的负载，故0≤b≤3；不直接推广到更大任意背景', 'X只选一次且保持共同标签会员；其最大性针对P=b+a而非1/(b+3)', 'h强制X后的Y/Z与进一步强制Q后的回复都由同一完整σ在对应有序历史给出'],
        'scope': '全客户类型解析必要式及特定证书锥的精确最优；17轨道只是有限查询接口。允许全部空/零/重复/别名/弱平局。',
        'objections': 'C=10不是已认证的真实SPE锐性；新点17行全部正不意味着普遍式无效或全局冗余。没有完整SPE反例或六人half闭合；未知交叠上包络不保证共同实现。',
        'body': bind(HPATH), 'evidence': hevidence,
        'sources': list(dict.fromkeys(['canonical:' + sources[0], 'material:' + sources[1]] + ['material:' + p['path'] for p in hevidence])),
        'keywords': ['共同目录', 'same-X', '真实三尾', '早期源', '逐型非负证书', 'six-providers']
    }
    reg['objects'].append(hlemma)
    extras = '''
maxb_augmented_lp/full_lift/discovery_recovery_report.md
maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json
maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json
maxb_augmented_lp/full_lift/recovery/certificate_verification.json
maxb_augmented_lp/full_lift/recovery/new_row_activity.json
maxb_augmented_lp/full_lift/recovery/optimality_analysis.json
maxb_augmented_lp/full_lift/recovery/freeze_manifest.json
maxb_augmented_lp/full_lift/compact_projection/augmented_lp_exact.json
maxb_augmented_lp/full_lift/compact_projection/exact_dual_certificate.json
maxb_augmented_lp/full_lift/compact_projection/certificate_verification.json
maxb_augmented_lp/full_lift/compact_projection/projection_derivation.json
maxb_augmented_lp/full_lift/old_optimum_face/report.md
maxb_augmented_lp/full_lift/old_optimum_face/old_optimal_face_cut_identity.json
maxb_augmented_lp/full_lift/old_optimum_face/strict_lower_bound_certificate.json
maxb_augmented_lp/full_lift/old_optimum_face/verify_identity_and_lower.py
maxb_augmented_lp/full_lift/old_optimum_face/independent_audit.json
compute_dispatch/maxb-full-artifact-audit.json
compute_dispatch/receive_maxb_full_artifact.py
early_x_anchor_queries.md
early_x_anchor_queries/rows_51.json
early_x_anchor_queries/ap_source_audit.md
early_x_anchor_queries/verification.json
early_x_anchor_queries/evaluation_on_5b1b.json
early_x_anchor_queries/freeze_manifest.json
main_ap3_cut_audit.py
main_ap3_cut_audit.json
early_ap_optimum_face.md
early_ap_optimum_face/primitive_obstruction.json
early_ap_optimum_face/facial_zero_closure/closure_certificate.json.gz
early_ap_optimum_face/facial_zero_closure/expanded_signed_identity.json
early_ap_optimum_face/facial_zero_closure/identity_support_provenance.json.gz
early_ap_optimum_face/facial_zero_closure/verify_closure_and_identity.py
early_ap_optimum_face/facial_zero_closure/independent_audit.json
early_ap_optimum_face/freeze_manifest.json
root_x_joint_contract.md
root_x_joint_contract/own_blocks.json
root_x_joint_contract/verification.json
main_common_X_pair_facets.md
common_x_own_lift/report.md
common_x_own_lift/own_facets.json
common_x_own_lift/verification.json
common_x_own_lift/fullX_5b1b_fixed_diagnostic.json
common_x_own_lift/fullX_5b1b_report.md
common_x_own_lift/fullX_5b1b_crosscheck.json
common_x_own_lift/delivery_manifest.json
'''.split()
    paths = list(dict.fromkeys([HPATH, byid[APID]['body']['path']] + [PREFIX + p for p in hfiles + extras]))
    known = {e['path'] for e in comp['evidence']}
    comp['evidence'] += [bind(p) for p in paths if p not in known]
    comp['sources'] = list(dict.fromkeys(comp['sources'] + ['material:' + p for p in paths]))
    mats = {m['path']: m for m in reg['materials']}
    for obj in (comp, hlemma):
        for e, bodyflag in [(obj['body'], True)] + [(e, False) for e in obj['evidence']]:
            path = e['path']
            if path in mats:
                m = mats[path]
                if m['sha256'] != e['sha256']:
                    assert path == comp['body']['path']
                    m['sha256'] = e['sha256']
            else:
                m = dict(bind(path), disposition='objects' if bodyflag else 'attachment',
                         object_ids=[obj['object_id']], reason='Main实读真实源预算、局部投影及精确全行列/面传播证书，保各自域与点/整面边界。')
                reg['materials'].append(m)
                mats[path] = m
            if bodyflag:
                m['disposition'] = 'objects'
                if obj['object_id'] not in m.setdefault('object_ids', []):
                    m['object_ids'].append(obj['object_id'])
    target = HERE / 'stage12-registry-candidate.json'
    assert not target.exists()
    target.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n')
    for obj, name in ((comp, 'stage12-computation.json'), (hlemma, 'stage12-h3-lemma.json')):
        (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    summary = {'base_registry_sha256': sha256(raw).hexdigest(),
               'candidate_sha256': sha256(target.read_bytes()).hexdigest(),
               'objects': [{k: o[k] for k in ('object_id', 'version', 'body')} for o in (comp, hlemma)],
               'total_objects': len(reg['objects']), 'total_materials': len(reg['materials']),
               'capacity_bearing_section_unchanged': True}
    (HERE / 'stage12-registration-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
