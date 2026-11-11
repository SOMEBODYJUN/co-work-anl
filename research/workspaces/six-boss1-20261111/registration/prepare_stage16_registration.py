"""Main promotes reviewed Stage16 mathematics without changing the edge index."""
from pathlib import Path
from hashlib import sha256
import copy
import json

HERE = Path(__file__).resolve().parent
WS, REPO = HERE.parent, HERE.parent.parents[2]
PREFIX = 'research/workspaces/six-boss1-20261111/'
CID = 'customer-attraction/six-providers/cross-branch-necessary-system-20261111'
NID = 'M-a90ca74cfdc848cb8f628fac8dd35f0a'
MODEL = 'CAG-MODEL'
UID = 'customer-attraction/shared-maximal-potential-optimal-union-prefix-family'
RCID = 'customer-attraction/true-last-reply-common-potential-cap-and-overlap-endpoints'
TID = 'customer-attraction/shared-maximal-potential-true-tail-cross-wallet-projection'
PID = 'customer-attraction/shared-true-terminal-reply-query-portfolio-and-reweighted-requery'
BGID = 'customer-attraction/one-prefix-five-profit-exclusive-charge'


def bind(path):
    return {'path': path, 'sha256': sha256((REPO/path).read_bytes()).hexdigest()}


def main():
    target = HERE/'stage16-registry-candidate.json'
    assert not target.exists(), 'Preserve the published preparation and make a new correction if needed'
    raw = (REPO/'research/registry.json').read_bytes()
    assert sha256(raw).hexdigest() == 'd64780069880f642a62f7db4c711bd18117e1a062cf76cde1abb566486ddd7e5'
    reg = json.loads(raw)
    old_edge_files = list(reg['edge_files'])
    objects = {obj['object_id']: obj for obj in reg['objects']}
    assert NID not in objects and objects[CID]['version'] == 11
    assert bind(objects[CID]['body']['path']) == objects[CID]['body']
    for rel, expected in [
        ('universal_union_wallet_v5/manifest.json', '4046a3490f5c1a4e8c6dc72e2642aa9e4cb8c4c538c414df3f2cb8f7249431c3'),
        ('universal_union_wallet_v6/manifest.json', 'fa5a8c0f9d313dee6d6f4b1a205a863d0f90f8b9a8d92ed41e74ad55ca1b52b3'),
        ('actual_source2_nested_requery/freeze_manifest.json', '1090ce67dec8ee30e27014d634d883ad67864a20f94b9bc33e36c94909106d70'),
        ('main_root30_cap4_strict_bound/manifest.json', '99a9396d888a4d52e757e53a2d7abae45e4cac60ce356f75caf7694445aa1e6b')]:
        assert bind(PREFIX+rel)['sha256'] == expected
    assert json.loads((WS/'main_universal_wallet_v6_check.json').read_text())['status'] == 'PASS_MAIN_ALL867_ROWS257_COLUMNS_AND_INDEPENDENT_P25_REBUILD'

    # Main has read the complete derivation and all root-parameter identities.
    draft = HERE/'stage16_new_lemma/body.md'
    assert sha256(draft.read_bytes()).hexdigest() == 'ea90cd908a69723b725225bdeee9fe9d95912b651d1359952fcbdc31ecaf41b8'
    lemma = json.loads((HERE/'stage16_new_lemma/object.draft.json').read_text())[0]
    assert lemma['object_id'] == NID
    body_path = REPO/lemma['body']['path']
    assert not body_path.exists()
    body = draft.read_text().replace('source-proof-and-independent-exact-audit-read; pending-Main-canonical-review',
                                     'Main-reviewed-complete-source-proof-and-full-column-exact-identities', 1)
    body = body.replace('第三十一倍、第二十五倍等其他源组合族', '31倍、25倍等其他源组合族')
    body_path.write_text(body)
    lemma['body'] = bind(lemma['body']['path'])
    # Draft section fields described uses, rather than exact ATX titles. Bind the
    # whole source bytes instead; the mathematical use remains explicit in body.
    for ref in lemma['evidence']:
        ref.pop('section', None)
        assert bind(ref['path']) == ref
    lemma['evidence'] += [bind(PREFIX+'registration/stage16_new_lemma/'+name)
                          for name in ['draft_exact_check.py', 'draft_exact_check.json']]
    lemma['sources'] = list(dict.fromkeys(lemma['sources']+['material:'+ref['path'] for ref in lemma['evidence']]))
    reg['objects'].append(lemma)
    objects[NID] = lemma

    comp = objects[CID]
    cp = REPO/comp['body']['path']
    old = cp.read_text()
    assert comp['body']['sha256'] == '0a36d2485d3385b541fedce4769a410c4aa182e6cef27f635a28886a6864ebfb'
    new = old.replace('status: 十个固定域系统及三个全类型系统精确闭合；真实根尾与同X联合约束持续推进；原题开放',
                      'status: 十个固定域及六个全类型系统精确闭合；三次完整最优面排除与严格普遍改进；原题开放', 1)
    new = new.replace('后文独立的217/219/221行系统保全部256个客户类型，另有普遍福利下界',
                      '后文独立的217/219/221/225/546/867行系统保全部256个客户类型，另有普遍福利下界', 1)
    old_intro = '独立的全256类型路线已得到221行精确普遍界约.4311752164865684，并将旧217与219整个最优面排除；完整证明、真实根尾来源和边界见本文末尾。'
    assert old_intro in new
    new = new.replace(old_intro, '独立全256类型路线现有867行匹配精确原对偶值约.440065512041364，其整个最优面仍被真实根大小等号排除；Main另用第四尾容量帽及W≥K给无新LP普遍界约.4400737002661185。225、546、867三个完整面均已精确排除。完整真实来源和边界见本文末尾。', 1)
    bearing = '# 跨分支新主题怎样接回真实早期IC'
    assert old[old.index(bearing):] == new[new.index(bearing):]
    new = new.rstrip()+'\n\n'+(HERE/'stage16-computation-addition.md').read_text().strip()+'\n'
    cp.write_text(new)
    comp['version'] = 12
    comp['title'] = '固定域十轮与全类型六轮推进：真实重查询、容量反馈及整面排除'
    comp['statement'] += (' 新增全256型225/546/867原始行系统分别有精确匹配原对偶，普遍系数约.43743468994980583、.4391243746776041、.440065512041364；三者整个最优面分别由真实第二源覆盖刚性、P31同支尾大小等号、真实最大根CAP2/CAP4等号排除。九预算的C30、30异索引RC/PAIR及全部源P31/P25均保任意重叠和弱平局，P25直接支付后才比较R31分解。再加同根CAP4及真实W≥K可无新LP证明W≥891124490754754277833367477478333164168*OPT6/2024943754229983091736619905135906627503≈.4400737002661185OPT6。背景五尾利润经六删一投影保K微小负系数；751内部真源模板保持未绑定点、0优化。')
    comp['quantifiers'] += ' 新225/546/867及严格改善继续是全部256客户型的原模型普遍必要付款；O=0直接处理。整个最优面均由完整零余项域的准确秩及全部原行可行区间确定，真实分支等号与signed面身份分开。新根线允许任意六合法查询并，比较支配只在O≥K；全局福利代入O=OPT6。'
    comp['assumptions'][0] = '前十个大规模有限LP比较覆盖O=1，限原保存点16个旧hist；后文217/219/221/225/546/867行系统含全部256个actual/X/O类型与真实全目录K，仅在OPT6>0时归一化'
    comp['assumptions'] += ['P25只在真正最优的源节点使用；被强制source2不能被赋予该新节点IC。内部source3/4/5和C30必须读该真实外层分支自己的前缀及收益。',
                            'W−K由六个actual源各真改同一个最大合法标签C的收益地板付款，不由最优面数值或未付等式推出。']
    comp['scope'] += ' 新三个全型系统、三个完整面排除、两个320行真实源族、背景删槽利润投影、根CAP2/CAP4反馈与严格全域合账均给实际证据。751只是点无关必要模板，尚不认领固定点可行性或Farkas；根270新探索不列作本版已核结果。'
    comp['objections'] += ' 新.4400737是合法普遍下界但未宣称最佳或half。225/546/867低点均已被真实分支等号排除；数值可行性不证明任何完整SPE。背景大oracle继承已登记来源，仅本次条件表及投影独立复核。'
    comp['keywords'] = list(dict.fromkeys(comp['keywords']+['P25真实容量付款', '三十异索引', '根容量反馈', '严格全域界', '内部真实源']))
    comp['body'] = bind(comp['body']['path'])

    groups = {
        'v3_optimum_joint_face': ['proof.md', 'face_certificate.json', 'manifest.json'],
        'maximal_root_tail_wallet_v2': ['proof.md', 'exact_input.json', 'exact_certificate.json', 'literal_certificate_check.json', 'freeze_manifest.json'],
        'main_thirty_index_strengthening': ['proof.md', 'exact_certificate.json', 'requery30_envelopes.json', 'check_and_build.py'],
        'main_all_source31_family': ['proof.md', 'exact_family.json', 'build_exact.py'],
        'main_all_source25_family': ['proof.md', 'exact_family.json', 'build_exact.py', 'manifest.json'],
        'main_background_projection': ['proof.md', 'exact_projection.json', 'build_exact.py'],
        'background_projection_audit': ['proof.md', 'audit_result.json', 'rebuild_independent.py', 'SHA256SUMS'],
        'v4_source2_identity': ['proof.md', 'exact_face_certificate.json', 'literal_check.json', 'check_literal.py', 'freeze_manifest.json'],
        'main_root30_capacity_feedback': ['proof.md', 'exact_certificate.json', 'manifest.json'],
        'main_root30_cap4_strict_bound': ['proof.md', 'exact_certificate.json', 'build_exact.py', 'manifest.json'],
        'main_root30_cap4_strict_bound_audit': ['proof.md', 'audit_result.json', 'global_audit_certificate.json', 'manifest.json'],
        'actual_source2_nested_requery_audit': ['check_exact.py', 'audit_result.json', 'freeze_manifest.json'],
        'actual_source2_nested_requery': ['derivation.md', 'source_review.md', 'symbolic_coefficients.py', 'row_catalogue.json', 'literal_symbolic_check.json', 'freeze_manifest.json']
    }
    # Actual filenames in the frozen bundles are inspected, never fabricated.
    for folder in ['universal_union_wallet_v4', 'universal_union_wallet_v5', 'universal_union_wallet_v6']:
        groups[folder] = ['proof.md', 'source_review.md', 'exact_input.json', 'exact_certificate.json',
                          'global_identity.json', 'manifest.json']
    extras = [f'{folder}/{file}' for folder, files in groups.items() for file in files]
    extras += ['main_universal_wallet_v4_check.py', 'main_universal_wallet_v4_check.json',
               'main_universal_wallet_v5_check.py', 'main_universal_wallet_v5_check.json',
               'main_universal_wallet_v6_check.py', 'main_universal_wallet_v6_check.json',
               'source31_family_audit.md', 'actual_source2_opt_requery_audit/root30_context.md',
               'actual_source2_nested_requery_audit.md',
               'universal_union_wallet_v5/face_signed_identities.json',
               'universal_union_wallet_v5/equality_diagnostic.json',
               'universal_union_wallet_v6/face_signed_identities.json',
               'universal_union_wallet_v6/root_equality_diagnostic.json',
               'universal_union_wallet_v6/optimum_face_diagnostic.json',
               'registration/stage16-computation-addition.md']
    paths = [objects[oid]['body']['path'] for oid in [NID, PID, BGID]]+[PREFIX+name for name in extras]
    for path in paths:
        assert (REPO/path).is_file(), path
    known = {ref['path'] for ref in comp['evidence']}
    comp['evidence'] += [bind(path) for path in paths if path not in known]
    comp['sources'] = list(dict.fromkeys(comp['sources']+['material:'+path for path in paths]))

    materials = {material['path']: material for material in reg['materials']}
    for obj in [lemma, comp]:
        for ref, is_body in [(obj['body'], True)]+[(ref, False) for ref in obj['evidence']]:
            path = ref['path']
            if path in materials:
                material = materials[path]
                if material['sha256'] != ref['sha256']:
                    assert is_body and obj['object_id'] == CID
                    material['sha256'] = ref['sha256']
            else:
                material = dict(ref, disposition='objects' if is_body else 'attachment', object_ids=[obj['object_id']],
                                reason='真实完整历史预算、明确查询量词与全部客户型精确非负付款；不把有限必要点认作完整SPE。')
                reg['materials'].append(material)
                materials[path] = material
    assert reg['edge_files'] == old_edge_files, 'Canonical inclusion must use the mapper receipt/assemble workflow'
    target.write_text(json.dumps(reg, ensure_ascii=False, indent=2)+'\n')
    (HERE/'stage16-objects.json').write_text(json.dumps([lemma, comp], ensure_ascii=False, indent=2)+'\n')

    edge_dir = REPO/'map/edges/six-boss1-20261111'
    affected = []
    for path in sorted(edge_dir.glob('*.json')):
        edge = json.loads(path.read_text())
        if CID not in edge['source_ids']+edge['target_ids']:
            continue
        for ref in edge['evidence']:
            if ref['path'] == comp['body']['path']:
                ref['sha256'] = comp['body']['sha256']
        for field in ['endpoint_pins', 'evidence_pins', 'review_digest']:
            edge.pop(field, None)
        edge['review_note'] += ' Stage16目标v12追加独立全型新结果，原承重段从跨分支新主题标题起逐字保留；本边仍只支付原明列局部步骤，不自动支付新增P25/根反馈或全域界。'
        path.write_text(json.dumps(edge, ensure_ascii=False, indent=2)+'\n')
        affected.append(str(path.relative_to(REPO)))

    edge = copy.deepcopy(json.loads((HERE/'stage16_new_lemma/relations.draft.json').read_text())['edges'][0])
    edge['status'] = 'accepted'
    edge['reviewed_by'] = 'Boss1/Main six-boss1-20261111'
    for ref in edge['evidence']:
        ref.pop('section', None)
        assert ref == bind(ref['path'])
    edge['evidence'] += [lemma['body'], bind(PREFIX+'registration/stage16_new_lemma/draft_exact_check.json')]
    edge['review_note'] = ('Main亲读完整九预算、完整矩区间及两个自由质量项，核PAIR30的异索引与重复标签；亲核根十预算全部128型及u/K/O参数。独立草稿核验再重建两套2048态与三套131列。核心无需前两人最优性；根推论另付最大裸标签及真实根IC；没有把发现锥的最优性扩域。')
    new_edges = [('complete-history-and-PAIR-to-source3-requery.json', edge)]
    sources = [MODEL, UID, RCID, TID, NID, PID]
    global_edge = {
        'edge_id': 'ca-six-boss1-source3-portfolio-and-root-pay-v4-v6-global-bounds',
        'kind': 'implies', 'status': 'accepted', 'premises_mode': 'all', 'relation_mode': 'unconditional',
        'source_ids': sources, 'target_ids': [CID], 'reviewed_by': 'Boss1/Main six-boss1-20261111',
        'conditions': '原六人共同有限目录完整有序历史纯SPE；K真实最大裸大小，X在actual前四P全目录最大潜力，O=OPT6由六合法可重复标签实现。全部256客户型；O=0直接，O>0同除归一。所有原始行和对偶付款使用未缩放精确系数。',
        'roles': {
            MODEL: '支付actual末位真实SAFE、同一根尾CAP4的附加付款和六actual源各真改最大C后相加的W−K预算；不冻结各偏离后继。',
            UID: '提供共同实际P最大X的UP2；各轮其余正UP按原公式付款。',
            RCID: '支付actual MX(Omean)与对任意合法查询对的RC；30有序异索引平均给o/(3(P+1))强成本。',
            TID: '支付同一真实第四源X的Y/T与actual RC共同约束得到的QX，保全256型联合尾最小值。',
            NID: '支付actual C30及真正最大C根分支的ROOT30、ROOT30-CAP2；同一真实根余项和CAP4再给已证定量反馈。',
            PID: '一般组合恒等式取α=0、P31各β=μ=1/31；P25中间β=1/50、末β=μ=1/25并放大，联合真实尾大小帽和末BR支付所有源族。',
            CID: '三份完整全列非负合账给225/546/867普遍界；进一步以λrootδ4的W−K预算给.4400737002661185严格全域改善。'
        },
        'explanation': '先由各真实源预算证明P31/P25、C30、RC30和根线，再按冻结原始对偶逐256客户及K列精确合账。v6的12正行、243正客户余项和零K余项给W−α6O=ΣλR+Σrz。新的根R4=R2−δ4(O−K)有独立非负根付款；加β(W−K)其中β=λrootδ4得(1+β)W−(α6+β)O非负。旧系统匹配原始点只认证指定必要锥最优；面不可实现性另由正文证据承担。',
        'scope': '只支付本目标末节的225/546/867全型普遍下界及ROOT-CAP4严格改善；不支付背景原53证明、固定16hist数值、未绑定751层的Farkas或half。',
        'contribution': {'result': '全部真实源组合、真实第三源与最大根容量共同接回覆盖目标，并用六个实际源的W−K付款得到明确严格全域系数。',
                         'remaining': '仍需完整支付2W−OPT6或给满足每个离轨历史的纯SPE反例；本节必要系统低点均不能提供该反例。'},
        'evidence': [objects[oid]['body'] for oid in sources]+[comp['body']]+[bind(PREFIX+name) for name in [
            'main_all_source25_family/proof.md', 'main_all_source31_family/proof.md',
            'universal_union_wallet_v4/proof.md', 'universal_union_wallet_v5/proof.md',
            'universal_union_wallet_v6/proof.md', 'universal_union_wallet_v6/exact_certificate.json',
            'main_universal_wallet_v6_check.json', 'main_root30_cap4_strict_bound/proof.md',
            'main_root30_cap4_strict_bound/exact_certificate.json',
            'main_root30_cap4_strict_bound_audit/proof.md',
            'main_root30_cap4_strict_bound_audit/global_audit_certificate.json']],
        'review_note': 'Main亲自推导P31/P25及两轮根容量反馈，全文核各正预算owner的模型/节点/系数，独立重放三轮所有原行与257列并直接重建P25全82240列；whole目标仍含其它独立内容，所以准确标为局部贡献。'
    }
    new_edges.append(('source3-portfolio-root-to-v4-v6-global-bounds.json', global_edge))
    bg_edge = {
        'edge_id': 'ca-six-boss1-background-five-profit-pays-six-deletion-projection',
        'kind': 'implies', 'status': 'accepted', 'premises_mode': 'all', 'relation_mode': 'unconditional',
        'source_ids': [BGID], 'target_ids': [CID], 'reviewed_by': 'Boss1/Main six-boss1-20261111',
        'conditions': '原共同目录完整SPE；actual首标签作一位背景，其后五个真实收益和V=W−u1；六合法比较索引可重复，按删除每一索引得五比较。保原53权、κ=226487/10^21与全部负条件余项。',
        'roles': {BGID: '提供任意一背景真实五尾的完整53源利润身份与隐藏域条件下界，不把五尾新覆盖混作利润。',
                  CID: '先对隐藏五会员位取min，再将六索引逐个删除平均，最后对真实重数d∈[o,6o]投影；得到全部256客户型及−κK列的BG必要行。'},
        'explanation': '原2V−R5=ΣλS+κK+Σρ，经条件表下界m，再六删一得到g_b(A,d)的两项准确平均，保d0/d6端点与索引重数；逐客户取gbar后得2(W−u1)−κK−Σgbar z≥0。两份6144表、384min和257列均有Main及独立重建。',
        'scope': '只支付末节BG完整投影及正确的利润/容量/删除损失；原大型oracle及53源证明继承owner，本阶段未重新运行。BG在v5/v6的对偶权0，不算其下界正付款。',
        'contribution': {'result': '将已登记一背景五尾全域证书实际代入六人路径，得到保共同K的完整客户型必要行。',
                         'remaining': 'BG单行不排v4/v5/v6代表点，不证明六人half或整策略可实现性。'},
        'evidence': [objects[BGID]['body'], comp['body']]+[bind(PREFIX+name) for name in [
            'main_background_projection/proof.md', 'main_background_projection/exact_projection.json',
            'background_projection_audit/proof.md', 'background_projection_audit/audit_result.json']],
        'review_note': 'Main实读owner第3/4节与承重条件，亲自推导六删一；独立审计再核12288表项、4096菜单和257列。负余项与极小K列原样保留，不把继承大域核验认作本次新运行。'
    }
    new_edges.append(('background-five-profit-to-six-deletion-projection.json', bg_edge))
    for name, edge in new_edges:
        path = edge_dir/name
        assert not path.exists()
        path.write_text(json.dumps(edge, ensure_ascii=False, indent=2)+'\n')
        affected.append(str(path.relative_to(REPO)))
    summary = {
        'status': 'PREPARED_MAIN_REVIEWED_NOT_REGISTERED_OR_PUSHED',
        'base_registry_sha256': sha256(raw).hexdigest(), 'candidate_sha256': sha256(target.read_bytes()).hexdigest(),
        'objects': len(reg['objects']), 'materials': len(reg['materials']),
        'new_lemma': {'object_id': NID, 'body': lemma['body']},
        'computation': {'object_id': CID, 'version': 12, 'body': comp['body']},
        'old_bearing_body_unchanged': True, 'canonical_edge_index_unchanged': True,
        'edge_files_requiring_bind_check': affected,
        'review_correction': 'Draft evidence section labels were descriptive, not exact ATX headings; replaced with verified whole-file refs before registration.'
    }
    (HERE/'stage16-registration-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
