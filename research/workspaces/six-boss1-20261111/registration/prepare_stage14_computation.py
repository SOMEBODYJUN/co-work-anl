"""Promote reviewed full-type bounds and frozen interfaces, preserving old proofs."""
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
WS, REPO = HERE.parent, HERE.parent.parents[2]
PREFIX = 'research/workspaces/six-boss1-20261111/'
CID = 'customer-attraction/six-providers/cross-branch-necessary-system-20261111'
RID = 'customer-attraction/maximal-root-true-tail-income-strengthening'
TID = 'customer-attraction/shared-maximal-potential-true-tail-cross-wallet-projection'
UID = 'customer-attraction/shared-maximal-potential-optimal-union-prefix-family'
RCID = 'customer-attraction/true-last-reply-common-potential-cap-and-overlap-endpoints'


def bind(path):
    return {'path': path, 'sha256': sha256((REPO / path).read_bytes()).hexdigest()}


def main():
    target = HERE / 'stage14-computation-registry-candidate.json'
    assert not target.exists(), 'Preserve prior promotion candidate'
    assert (WS / 'universal_union_wallet_v3/manifest.json').exists()
    checked = json.loads((WS / 'main_universal_wallet_v3_check.json').read_text())
    assert checked['status'] == 'PASS_ALL_221_ROWS_257_COLUMNS_AND_NEW_ROOT_FORMULAS'
    raw = (REPO / 'research/registry.json').read_bytes()
    reg = json.loads(raw)
    objects = {o['object_id']: o for o in reg['objects']}
    comp = objects[CID]
    assert comp['version'] == 10
    assert comp['body']['sha256'] == 'f537768f9cc267303ad5764fa1824d212c38aeca8d8437b4085acc082fe3e3e9'
    assert comp['body'] == bind(comp['body']['path'])
    body = REPO / comp['body']['path']
    old = body.read_text()
    new = old.replace('status: 十个必要LP精确闭合；早期同X约束排除第十最优面；原题开放',
                      'status: 十个固定域系统及三个全类型系统精确闭合；真实根尾与同X联合约束持续推进；原题开放', 1)
    new = new.replace('truth_status: 有限必要系统的精确最优与分离；不是SPE反例或全域半覆盖定理',
                      'truth_status: 固定域与全类型必要系统的精确最优及普遍下界；不是SPE反例或半覆盖定理', 1)
    phrase = '比较覆盖归一化为 $O=1$，客户仅允许原点的16个旧hist支撑；因此以下最优值只属于这些明示的有限必要LP。'
    assert phrase in new
    new = new.replace(phrase, '比较覆盖归一化为 $O=1$，前十个系统仅允许原点的16个旧hist支撑；下表最优值只属于这些明示的有限必要LP。后文独立的217/219/221行系统保全部256个客户类型，另有普遍福利下界，不能混用两条路线的点或值。', 1)
    new = new.replace('最新进展：第十完整共同X系统已精确最优约.4941319647988424，且与20911单MC6系统同值。第九整个最优面被MC6排除，第十整个最优面又被actual第三位同X查询A6的旧AP实例排除。H3前接、51早期AP与1260共同八格投影均已核；下一系统必须允许420交叠作为真实core重选。详见本文末尾新节。',
                      '固定16hist路线最新状态：第十完整共同X系统精确最优约.4941319647988424，整个最优面已被AP39排除；下一23676系统的420交叠为真实core，唯一Actions请求仍排队。独立的全256类型路线已得到221行精确普遍界约.4311752164865684，并将旧217与219整个最优面排除；完整证明、真实根尾来源和边界见本文末尾。', 1)
    bearing = '# 跨分支新主题怎样接回真实早期IC'
    assert old[old.index(bearing):] == new[new.index(bearing):]
    new = new.rstrip() + '\n\n' + (HERE / 'stage14-computation-addition.md').read_text().strip() + '\n'
    body.write_text(new)
    comp['version'] = 11
    comp['title'] = '固定域十轮推进与全类型三轮合账：真实根尾及同X共同查询'
    comp['statement'] += (' 独立全256客户型加K的217/219/221原始行系统分别有精确匹配原对偶，最优值约.4258960956295508、.4291791015294076、.4311752164865684；全类型非负证书同时给普遍W下界，均非half。NEW与SIZE分别排除整个217与219最优面，signed全257列身份固定K并另给无优化严格界。221最优精确为999866079286562265469481/2318932167377271341801106，十正钱包含真实X两尾联合cut和最大裸主题真实根TAIL，允许全部客户与最优菜单重叠。静态C可修复旧217点54行但其真实根分支仍被排。42/236根X接口、5580同X条件ZZ、1920会员436真预算、306新平均PAIR及9投影已冻结；70槽交换候选为旧锥冗余。唯一23676云任务仍无返回点。')
    comp['quantifiers'] += ' 后文三份全256型系统覆盖任意原六人完整SPE，其非负全列对偶给普遍下界；每个精确最优点只属于所列必要系统。新217/219整面排除分别绑定其精确矩阵和正对偶，不从单点外推。'
    comp['assumptions'][0] = '前十个大规模有限LP比较覆盖O=1，限原保存点16个旧hist；后文独立217/219/221行系统含全部256个actual/X/O类型与真实全目录K，仅在OPT6>0时归一化'
    comp['assumptions'].append('全类型路线中O为六合法最优标签覆盖并，绝非新行动；C为真实最大裸大小标签，X为实际前四潜力最大标签，跨分支保同一合法角色而不冻结其他偏离的后继')
    comp['scope'] += ' 后文另给三个完整256型系统精确不足与有效普遍界，不再继承16hist域。221对偶十权及全256型余项支付整个下界；静态C补全、真X两尾Farkas和两次最优面排除各有独立来源、点/域和全列证书。'
    comp['objections'] += ' 三个全类型低点仍不是SPE反例；.4311752不是半覆盖或最佳已知界声明。全128根71行的指定K0最优不声称任意K的最优根曲线。'
    comp['keywords'] += ['全客户类型', '真实根后继', '同X两尾', '整最优面排除']
    comp['body'] = bind(comp['body']['path'])

    extras = '''
main_universal_union_wallet_check.py main_universal_union_wallet_check.json
universal_union_wallet_lp.md universal_union_wallet_lp/proof.md universal_union_wallet_lp/source_derivations.md
universal_union_wallet_lp/exact_input.json universal_union_wallet_lp/exact_certificate.json
universal_union_wallet_lp/check_certificate.py universal_union_wallet_lp/checker_output.json universal_union_wallet_lp/manifest.json
universal_union_wallet_audit.md universal_union_wallet_audit/check_exact.py universal_union_wallet_audit/audit_result.json universal_union_wallet_audit/freeze_manifest.json
universal_max_label_completion.md universal_max_label_completion/proof.md universal_max_label_completion/source_derivations.md
universal_max_label_completion/exact_input.json universal_max_label_completion/exact_completion.json universal_max_label_completion/check_completion.py universal_max_label_completion/checker_output.json universal_max_label_completion/manifest.json
main_universal_wallet_face.md main_universal_wallet_face.py main_universal_wallet_face.json
main_universal_wallet_v2_face.md main_universal_wallet_v2_face.py main_universal_wallet_v2_face.json
main_universal_wallet_v2_check.py main_universal_wallet_v2_check.json
universal_union_wallet_v2.md universal_union_wallet_v2/proof.md universal_union_wallet_v2/source_review.md
universal_union_wallet_v2/exact_input.json universal_union_wallet_v2/exact_certificate.json universal_union_wallet_v2/check_certificate.py universal_union_wallet_v2/checker_output.json universal_union_wallet_v2/manifest.json
main_universal_wallet_v3_check.py main_universal_wallet_v3_check.json
universal_union_wallet_v3.md universal_union_wallet_v3/proof.md universal_union_wallet_v3/source_review.md
universal_union_wallet_v3/exact_input.json universal_union_wallet_v3/exact_certificate.json universal_union_wallet_v3/check_certificate.py universal_union_wallet_v3/checker_output.json universal_union_wallet_v3/global_identity.json universal_union_wallet_v3/integer_residual_table.tsv universal_union_wallet_v3/numerical_scaling.json universal_union_wallet_v3/manifest.json
root_x_shared_queries.md root_x_shared_queries/direct_interface_exact.json.gz root_x_shared_queries/extended_interface_exact.json.gz root_x_shared_queries/direct_verification.json root_x_shared_queries/extended_verification.json root_x_shared_queries/freeze_manifest.json
x_conditioned_zz.md x_conditioned_zz/conditioned_upper_rows.json x_conditioned_zz/complete_point.py x_conditioned_zz/independent_audit.json x_conditioned_zz/freeze_manifest.json
early_shared_x_joint.md early_shared_x_joint/symbolic_append.json.gz early_shared_x_joint/visible_prefix_projection.json.gz early_shared_x_joint/freeze_manifest.json
early_shared_x_menu_pair_closure.md early_shared_x_menu_pair_closure/usable_pair_append.json.gz early_shared_x_menu_pair_closure/direct_BR_redundancy.json.gz early_shared_x_menu_pair_closure/averaged_prefix_projection.json.gz early_shared_x_menu_pair_closure/freeze_manifest.json
opt6_shared_x_exchange.md opt6_shared_x_exchange/report.md opt6_shared_x_exchange/candidate_rows_and_certificates.json opt6_shared_x_exchange/literal_audit.json opt6_shared_x_exchange/freeze_manifest.json
'''.split()
    paths = [objects[k]['body']['path'] for k in [RID, TID, UID, RCID]] + [PREFIX + p for p in extras]
    known = {e['path'] for e in comp['evidence']}
    comp['evidence'] += [bind(p) for p in paths if p not in known]
    comp['sources'] = list(dict.fromkeys(comp['sources'] + ['material:' + p for p in paths]))
    materials = {m['path']: m for m in reg['materials']}
    for ref, isbody in [(comp['body'], True)] + [(e, False) for e in comp['evidence']]:
        path = ref['path']
        if path in materials:
            if materials[path]['sha256'] != ref['sha256']:
                assert isbody, path
                materials[path]['sha256'] = ref['sha256']
        else:
            item = dict(ref, disposition='objects' if isbody else 'attachment', object_ids=[CID],
                        reason='精确区分固定域和全客户域；真实预算、完整系数、原对偶及共同身份边界均有核验。')
            reg['materials'].append(item)
            materials[path] = item
    target.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n')
    (HERE / 'stage14-computation.json').write_text(json.dumps(comp, ensure_ascii=False, indent=2) + '\n')
    summary = {'base_registry_sha256': sha256(raw).hexdigest(), 'candidate_sha256': sha256(target.read_bytes()).hexdigest(),
               'object_id': CID, 'version': 11, 'body': comp['body'], 'old_bearing_sections_unchanged': True,
               'objects': len(reg['objects']), 'materials': len(reg['materials'])}
    (HERE / 'stage14-computation-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')

    old_edges = ['arbitrary-anchor-AP-to-shared-X-early-queries', 'terminal-capacity-projection-to-cb45',
                 'portfolio-to-capacity-and-new-targets', 'H3-to-finite-shared-X-queries']
    for name in old_edges:
        p = REPO / 'map/edges/six-boss1-20261111' / (name + '.json')
        e = json.loads(p.read_text())
        assert CID in e['target_ids']
        for ref in e['evidence']:
            if ref['path'] == comp['body']['path']:
                ref['sha256'] = comp['body']['sha256']
        for key in ['endpoint_pins', 'evidence_pins', 'review_digest']:
            e.pop(key, None)
        e['review_note'] = e.get('review_note', '') + ' Stage14目标v11仅更新入口与另附全类型路线；本边承重旧证明段逐字未变，仍只支付原明定步骤，不支付新普遍界。'
        p.write_text(json.dumps(e, ensure_ascii=False, indent=2) + '\n')
    source_ids = ['CAG-MODEL', UID, RCID, RID, TID]
    newedge = {
        'edge_id': 'ca-six-boss1-joint-universal-wallets-pay-221-global-bound',
        'kind': 'implies', 'status': 'accepted', 'premises_mode': 'all', 'relation_mode': 'unconditional',
        'source_ids': source_ids, 'target_ids': [CID], 'reviewed_by': 'Boss1/Main six-boss1-20261111',
        'conditions': '原六人共同目录完整有序历史纯SPE；K是真实全目录最大裸大小，X为actual前四潜力最大合法标签，O为六最优合法查询并。保全部256客户型；O>0归一化，O=0直接。',
        'roles': {
            'CAG-MODEL': '支付三个actual SAFE和K−|A6|；保证所有真偏离与共同标签合法。',
            UID: '支付同一X的UP2及UP3，常数25与19。',
            RCID: '支付同一X的MX(Omean)及RC(Omean,Omean)，双均值按完整36索引对。',
            RID: '支付真实最大C根分支TAIL普遍线，非固定K0的数值外推。',
            TID: '支付同一X真实Y/T和actual钱包联合的六整数权QX。',
            CID: '十正整数预算与全部256客户余项精确合账，K列抵消，给W≥999866079286562265469481*OPT6/2318932167377271341801106。'
        },
        'explanation': '正文十整数权以S=6956796502131814025403318合账；h(v)=S*covered−T*o−ΣwR*rR(v)在全部256型非负，K余项零，故SW−T*O=ΣwR*R+Σh(v)zv≥0。独立匹配原始点另证指定221行系统最优。',
        'scope': '只支付正文221行全类型普遍下界的十预算非负合账；不支付固定16hist路线的数值最优、完整策略实现、最佳界或half。',
        'contribution': {'result': '把根部真实尾源和实际第四源真实X两尾同时接回全覆盖预算。',
                         'remaining': '真实根/actual/最优标签的跨分支共同后继尚未完整实现或排除，原half开放。'},
        'evidence': [bind(objects[k]['body']['path']) for k in source_ids] + [comp['body']] +
                    [bind(PREFIX + p) for p in ['universal_union_wallet_v3/proof.md', 'universal_union_wallet_v3/exact_input.json',
                     'universal_union_wallet_v3/exact_certificate.json', 'universal_union_wallet_v3/global_identity.json',
                     'universal_union_wallet_v3/checker_output.json', 'main_universal_wallet_v3_check.json']],
        'review_note': 'Main实读所有十预算的原始来源、两个最大标签定义与完整36平均；亲核全部221行/257列及两个新根公式，未用结构check代替数学证明。'
    }
    ep = REPO / 'map/edges/six-boss1-20261111/universal-root-tail-wallets-to-global-bound.json'
    assert not ep.exists()
    ep.write_text(json.dumps(newedge, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
