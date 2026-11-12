"""Main's reviewed Stage19 return; preserve prior bodies and canonical edge list.

No optimization, Git operation, map inclusion, or frozen-source mutation occurs
here.  A separately written review record pins the exact drafts Main read.
"""
from pathlib import Path
from hashlib import sha256
import copy
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
PREFIX = str(WS.relative_to(REPO)) + '/'
CID = 'customer-attraction/six-providers/cross-branch-necessary-system-20261111'
NID = 'M-a90ca74cfdc848cb8f628fac8dd35f0a'
NEW = 'customer-attraction/internal-safe-exact-domains-and-ordered-menu-projection'
MODEL = 'CAG-MODEL'
JP = 'customer-attraction/ordered-middle-safe-joint-tail-projection'
PAIR = 'M-e960d7f4ebca40a38760eb3ae044cc19'
RC = 'customer-attraction/true-last-reply-common-potential-cap-and-overlap-endpoints'
TX = 'customer-attraction/shared-maximal-potential-true-tail-cross-wallet-projection'
OLD_REGISTRY = '3657faa7878fc9440c63513deb2c55409d1a3c1d3641295a32749e97bee97ca5'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def bind(path):
    path = str(path)
    return {'path': path, 'sha256': digest(REPO/path)}


def write_new(path, obj):
    with path.open('x') as stream:
        stream.write(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')


def add_refs(obj, paths):
    refs = {ref['path']: ref for ref in obj['evidence']}
    for path in paths:
        ref = bind(path)
        if path in refs:
            assert refs[path]['sha256'] == ref['sha256'], path
        else:
            obj['evidence'].append(ref)
            refs[path] = ref
    obj['sources'] = list(dict.fromkeys(obj['sources'] + ['material:'+p for p in paths]))


def files(groups):
    return [PREFIX+folder+'/'+name for folder, names in groups.items() for name in names]


def main():
    target = HERE/'stage19-registry-candidate.json'
    assert not target.exists(), 'Do not overwrite a consumed promotion.'
    assert digest(REPO/'research/registry.json') == OLD_REGISTRY
    review = json.loads((HERE/'stage19-main-review.json').read_text())
    assert review['status'] == 'MAIN_FULL_DRAFT_AND_SOURCE_SCOPE_REVIEW_COMPLETE'
    for path, expected in review['draft_sha256'].items():
        assert digest(REPO/path) == expected, path
    reg = json.loads((REPO/'research/registry.json').read_text())
    original = copy.deepcopy(reg)
    objects = {o['object_id']: o for o in reg['objects']}
    assert NEW not in objects and objects[CID]['version'] == 13 and objects[NID]['version'] == 2
    old_bodies = {oid: copy.deepcopy(objects[oid]['body']) for oid in [CID, NID]}
    expected = {CID: 'da4170266fe281f57228c922f5387dddb6d11291c68da0612cccd2d7f47e1fc7',
                NID: '25e68dd35cedd7bc507092111a96fb8dd1b26f2e507275597915c763c5376676'}
    archive = HERE/'previous_revisions'
    archive.mkdir(exist_ok=True)
    revisions = []
    for oid, name in [(CID, 'cross_branch_computation_v13.md'), (NID, 'source3_root_projection_v2.md')]:
        ref = old_bodies[oid]
        assert ref['sha256'] == expected[oid] == digest(REPO/ref['path'])
        dest = archive/name
        assert not dest.exists()
        dest.write_bytes((REPO/ref['path']).read_bytes())
        revisions.append({'object_id': oid, 'version': objects[oid]['version'],
                          'former_body': ref, 'preserved_copy': bind(dest.relative_to(REPO)),
                          'last_confirmed_old_commit': '81a3d423605707021f797c393f37099420d5d43a'})
    write_new(archive/'stage19-version-map.json', {
        'reason': 'Canonical bodies extended after complete Main review; frozen historical pins remain unchanged.',
        'replay': 'Use the pinned historical commit, or the exact preserved body bytes named below.',
        'revisions': revisions})

    # New owner keeps the generic JP theorem at its existing identity.
    draft = (HERE/'stage19_new_internal_lemma/body.md').read_text()
    old_heading = '## 7. 证据、适用边界与接续'
    before, evidence = draft.split(old_heading, 1)
    extension = (HERE/'stage19_parameter_extensions.md').read_text()
    extension = extension[extension.index('## 7. λ 延拓'):]
    new_text = before.rstrip()+'\n\n'+extension.strip()+'\n\n## 9. 证据、适用边界与接续'+evidence
    new_text = new_text.replace('全部精确程序和必要输入在',
        '本版另包含λ230/160/550的完整连续域、根λ零新增恒等式及δ180全条件包络。全部精确程序和必要输入在', 1)
    body_path = 'archives/customer-attraction/state/引理/联合内部偏离的完整参数域与同菜单条件投影--引理.md'
    assert not (REPO/body_path).exists()
    (REPO/body_path).write_text(new_text.rstrip()+'\n')
    lemma = {
        'object_id': NEW, 'version': 1, 'title': '联合内部偏离的完整参数域与同菜单条件投影',
        'kind': 'lemma', 'truth_status': 'proved', 'model': objects[NID]['model'],
        'statement': '固定任一真实源节点，以源IC、内部SAFE、每个真实尾大小帽和末BR先作同分支非负合账，再按全部有序尾会员取最小。正文给出固定半帽族完整参数域、67顶点及536纯行；外六强制内五排同索引的准确条件投影及181cell有限化；坐标最小帽两套各137顶点及1096纯行/137ordered行、第二源28点C-only及28点基底耦合域。另以λ双锚给第二源完整低段10面16点、第三至第五源24闭域共110次顶点及550行，根λ换元与旧19面90点域全域相同；τ4向τ5连续转移的全部真实尾损失由180条端点行无损生成。所有域、最小值、弱达到态与完整513列身份均在所明定预算/锚/范围内准确。',
        'quantifiers': '每份原六人完整有序历史纯SPE、任一真实第1至第5源节点、任意合法强制T、任意六元合法查询列表（可重复）及各明定参数域全部实参数；同一策略决定每个有序历史的真实续局。u_i是该源节点实际继续收益，不能把被强制源赋予免费新IC。O只是六查询覆盖并，应用福利时另取OPT6；C-only额外要求T为真正全目录最大标签C。',
        'assumptions': ['所有预算权非负，质量等式乘子自由；零总负载按零份额处理。',
                        'query会员均值先保真实索引重数；ordered内层排除同索引而非排除同标签。',
                        '完整域声明限各节指定帽、锚及λ或δ范围；不以采样点或浮点求解替代全状态比较。',
                        '局部尾最小值允许逐客户独立取min，仅产生必要放松，不假定这些尾能共同实现。',
                        '原513列应用保全部512九位客户型及独立K；数值除数25与实际源IC权分开。'],
        'scope': '本对象承担一般JP的具体完整参数求解、真实双锚、同菜单条件相关性和无损有限生成。一般JP、九预算source3重查询及全局LP证书仍由各原owner承担。任意平局、空主题、重复行动、同覆盖异标签与零客户均保留。',
        'objections': '不是任意钱包或任意参数的最优性结论，不证明完整SPE可实现性或六人half。根λ族在明确预算范围内无新信息；s=9,δ=0旧锚失败由真实条件损失处理。自由C等式不能用于任意T，ordered q=1/5端点不外推到更大q。',
        'body': bind(body_path), 'evidence': [], 'sources': [],
        'keywords': ['真实内部偏离','完整参数域','同菜单异索引','全部弱平局','最小容量帽','双锚λ延拓','连续δ条件包络','无损有限生成']}
    new_groups = {
        'all_source_joint_reweighted_safe': ['proof.md','exact_family.json','parameter_polytopes.json','freeze_manifest.json'],
        'all_source_ordered_menu_cells': ['proof.md','exact_family.json','parameter_cells.json','freeze_manifest.json'],
        'source2_cap_coupled_internal_safe': ['proof.md','exact_family.json','parameter_polytope.json','freeze_manifest.json'],
        'source2_minimal_cap_safe': ['proof.md','exact_family.json','parameter_polytope.json','freeze_manifest.json'],
        'all_source_minimal_cap_safe': ['proof.md','exact_family.json','parameter_domains.json','freeze_manifest.json'],
        'ordered_minimal_cap': ['proof.md','exact_family.json','parameter_domains.json','freeze_manifest.json'],
        'source2_lambda_strip': ['proof.md','exact_family.json','parameter_domains.json','freeze_manifest.json'],
        'source2_lambda_anchor_complete': ['proof.md','exact_family.json','parameter_domains.json','freeze_manifest.json'],
        'later_sources_lambda_cells': ['proof.md','analytic_review.md','exact_family.json','parameter_domains.json','freeze_manifest.json'],
        'source1_lambda_complete': ['proof.md','analytic_review.md','parameter_domains.json','old_row_correspondence.json','freeze_manifest.json'],
        'source2_conditional_redistribution': ['proof.md','exact_family.json','exact_envelopes.json','affine_family.json','all_weak_minimum_tables.json','freeze_manifest.json']}
    main_checks = ['main_all_source_joint_check','main_ordered_cells_check','main_cap_coupled_complete_check',
                   'main_minimal_cap_source2_check','main_all_source_minimal_cap_safe_check','main_ordered_minimal_cap_check',
                   'main_source2_lambda_strip_check','main_source2_lambda_anchor_complete_check',
                   'main_later_lambda_check','main_source2_delta_check']
    new_evidence = files(new_groups)+[objects[MODEL]['body']['path'],objects[JP]['body']['path']]
    new_evidence += [PREFIX+n+'.json' for n in main_checks]
    new_evidence += [PREFIX+'main_source1_lambda_closure_review.md', PREFIX+'registration/stage19-source-comparison.md',
                     PREFIX+'registration/stage19_parameter_extensions.md', PREFIX+'registration/stage19-main-review.json']
    for name in main_checks:
        assert json.loads((WS/(name+'.json')).read_text())['status'].startswith('PASS'), name
    add_refs(lemma, new_evidence)
    reg['objects'].append(lemma)
    objects[NEW] = lemma

    root = objects[NID]
    root_path = REPO/root['body']['path']
    old_root = root_path.read_text()
    assert 'version: 2\n' in old_root
    root_text = old_root.replace('version: 2\n','version: 3\n',1)
    root_text += '\n'+(HERE/'stage19-root270-addition.md').read_text().strip()+'\n'
    root_path.write_text(root_text)
    root['version'] = 3
    root['statement'] += ' 在同一真正最大C根分支再支付真实第四源P25，得到16877573861922720u≥1767904008200582K+337340181272013O。其全128型非负余项还给规范残差R270≥1087978231314917|C\\O|/84387869309613600，故ROOT270取等必要有C⊆O；仍允许任意六合法查询并。'
    root['quantifiers'] += ' 新ROOT270中P25只在该根分支的真实第四源节点使用，并强制合法B6；其后继重新由同一策略继续，不给强制根C免费最优性。'
    root['assumptions'].append('ROOT270正付款另含同根真实第四源的P25，K帽付款和两自由质量项均保全；C在O外严格余项取完整32态的准确最小值。')
    root['scope'] += ' 新增ROOT270完整十预算、131列身份及严格C在O外余项；未改变C36/C30及原三条根线。'
    root['objections'] += ' ROOT270只扩展明列特殊根付款，不并入一般P25家族的全部结论；匹配270行必要锥只在明定K处最优，不是原SPE或任意K根曲线最优。'
    root['body'] = bind(root['body']['path'])
    root_groups = {
        'maximal_root_tail_wallet_v3': ['proof.md','exact_input.json','exact_certificate.json','literal_certificate_check.json','freeze_manifest.json'],
        'maximal_root_tail_wallet_v3_audit': ['audit_result.json','bridge_audit_result.json','freeze_manifest.json'],
        'main_root270_strict_outside': ['proof.md','ROOT270_STRICT_C_OUTSIDE.json','check_result.json','freeze_manifest.json']}
    add_refs(root, files(root_groups)+[lemma['body']['path'],PREFIX+'visible_c_source2_equality_audit/root270_formula_erratum.md',
                                     PREFIX+'registration/stage19-root270-addition.md'])

    comp = objects[CID]
    comp_path = REPO/comp['body']['path']
    old_comp = comp_path.read_text()
    heading = '# 跨分支新主题怎样接回真实早期IC'
    intro, old_bearing = old_comp.split(heading,1)
    intro = intro.replace('status: 十个固定域及六个全类型系统精确闭合；三次完整最优面排除与严格普遍改进；原题开放',
                          'status: 固定域与全类型精确必要系统持续推进；完整面排除及普遍界0.4417591884174316401633；原题开放')
    intro = intro.replace('后文独立的217/219/221/225/546/867行系统保全部256个客户类型，另有普遍福利下界',
                          '后文独立路线先保全部256型，再显式保最大合法C的全部512型，已到3056行精确系统并有严格普遍改善')
    marker = '独立全256类型路线现有867行'
    start = intro.index(marker)
    end = intro.index('\n',start)
    intro = intro[:start]+('独立全类型路线现已显式保全部512个actual/X/O/C客户型及独立K，完整3056行必要系统精确最优约.44175890250014965，其整个最优面由同一真实C分支的SAFE4/5等号冲突排除。再以真实δ切割、根C在O外余项及六actual SAFE(C)付款，无新增LP得到普遍界 W≥0.4417591884174316401633 OPT6。此系数仍低于half。完整来源、精确分数及边界见本文末尾。')+intro[end:]
    additions = ['stage19-computation-addition.md','stage19_v5_global_addition.md','stage19-gamma36-addition.md']
    comp_text = intro+heading+old_bearing
    assert comp_text[comp_text.index(heading):] == old_comp[old_comp.index(heading):]
    for name in additions:
        addition = (HERE/name).read_text()
        if addition.startswith('<!--'):
            addition = addition[addition.index('-->')+3:].lstrip()
        comp_text += '\n'+addition.strip()+'\n'
    comp_path.write_text(comp_text)
    comp['version'] = 14
    comp['title'] = '同源跨枝必要系统：完整客户型、整面排除及精确普遍改善'
    comp['statement'] += ' 显式保最大合法C后，全部512客户型及独立K的1002/1003/1586/3056原始行必要系统均有精确匹配原对偶，系数分别约.44033436822146094、.44034016362630934、.4411521416736506、.44175890250014965；各完整最优面另被真实C分支等号排除。3056的完整18零余量列/秩12六参数面迫u2=K/5、C⊆O、R3=R4=R5=C，但真实SAFE4/5应同取K/5而N5−N4=(1−K)/36>0。不依赖最优面，δ=1/144真切割与ROOT270严格C外余项、六actual SAFE(C)及旧列余款合账，给准确普遍系数60031108172895495982435367008072256807714132617609/135891023315105974064184556965981156861873793636093≈.4417591884174316401633。'
    comp['quantifiers'] += ' 新全513列必要LP取O=OPT6最优六并，OPT6>0归一化；其精确最优仅属对应完整原始矩阵。各新增普遍福利证书的正付款另逐源核可用于任意六合法查询并，未把零权OPT上帽扩域。3056全最优面保所有零对偶余量列、全部原行限制和非负条件；严格统一改善由显式非负全列身份给出。'
    comp['assumptions'][0] += '；后续1002/1003/1586/3056系统扩至全部512个actual/X/O/C型与独立K、加|C|−K真实等式，仍保30条rhs=−1原行'
    comp['assumptions'].append('内部偏离沿真实源自己的有序前缀；源IC权、正数值除数和自由等式乘子分开。新δ损失由全尾真实最小值支付，不假定转移后仍在旧锚域。')
    comp['scope'] += ' 本版另给ROOT270、四个全512型系统、完整1586/3056面与两个无LP全局改善；γ36证书全部513列及3056权由Main独立准确核查。4177准备及其后计算尚不在本版最优性声明内。'
    comp['objections'] += ' 当前普遍系数约.4417591884仍非half或最佳精确值。3056旧面排除不单独推出统一间隙；统一间隙另由δ/根/SAFE(C)付款证明。734真C模板仍未绑定新点且无phase-I消费。'
    comp['keywords'] = list(dict.fromkeys(comp['keywords']+['显式最大合法标签','全512客户型','完整参数域','同菜单条件投影','连续δ切割','统一非负合账']))
    comp['body'] = bind(comp['body']['path'])
    # Refresh all canonical references to the two extended bodies, before adding new evidence.
    changed_paths = {old_bodies[oid]['path']:objects[oid]['body'] for oid in [CID,NID]}
    hit_objects = set()
    for obj in reg['objects']:
        for ref in obj.get('evidence',[]):
            if ref['path'] in changed_paths:
                ref['sha256'] = changed_paths[ref['path']]['sha256']
                hit_objects.add(obj['object_id'])
    assert hit_objects <= {CID,NID}, hit_objects
    comp_groups = {
        'visible_maximum_joint_solve': ['proof.md','exact_certificate.json','optimal_face.json','freeze_manifest.json'],
        'visible_maximum_joint_v2_solve': ['proof.md','exact_certificate.json','optimal_face.json','freeze_manifest.json'],
        'visible_maximum_joint_v4_solve': ['proof.md','exact_certificate.json','optimal_face.json','true_branch_face_functionals.json','freeze_manifest.json'],
        'visible_maximum_joint_v5': ['exact_input.json','source_review.md','freeze_manifest.json'],
        'visible_maximum_joint_v5_solve': ['proof.md','exact_certificate.json','optimal_face.json','current_positive_source_state_checks.json','true_branch_face_functionals.json','freeze_manifest.json'],
        'main_delta_uniform_improvement': ['proof.md','exact_certificate.json','all513_global_identity_checks.json','freeze_manifest.json'],
        'delta_uniform_audit': ['proof.md','certificate_gamma36.json','certificate_gamma72.json','all513_identity_gamma36.json','all64_p1_Oonly_debits.json','positive_source_scope_check.json','freeze_manifest.json']}
    comp_evidence = files(comp_groups)+[lemma['body']['path'],root['body']['path']]
    comp_evidence += [PREFIX+n for n in ['main_visible_c_certificate_check.json','main_visible_c_v2_certificate_check.json',
        'main_visible_c_v4_certificate_check.json','main_visible_c_v5_certificate_check.json','main_gamma36_certificate_check.py',
        'main_gamma36_certificate_check.json','main_ordered181_face_review.json']]
    comp_evidence += [PREFIX+'registration/'+n for n in additions]+[PREFIX+'registration/stage19-main-review.json']
    add_refs(comp, comp_evidence)
    assert json.loads((WS/'main_gamma36_certificate_check.json').read_text())['status'] == 'PASS_MAIN_GAMMA36_ALL513_UNIVERSAL_IDENTITY'

    # Reverse-material ownership closure. All unrelated objects/materials stay byte-semantically intact.
    materials = {m['path']:m for m in reg['materials']}
    for obj in [lemma,root,comp]:
        for ref,is_body in [(obj['body'],True)]+[(x,False) for x in obj['evidence']]:
            path = ref['path']
            assert digest(REPO/path) == ref['sha256'], path
            if path not in materials:
                mat = dict(ref,disposition='objects' if is_body else 'attachment',object_ids=[],
                           reason='Main完整实读、真实历史非负付款及准确域/全列复核；必要系统与完整SPE结论分清。')
                materials[path] = mat
                reg['materials'].append(mat)
            mat = materials[path]
            if mat['sha256'] != ref['sha256']:
                assert path in changed_paths, path
                mat['sha256'] = ref['sha256']
            if obj['object_id'] not in mat['object_ids']:
                mat['object_ids'].append(obj['object_id'])
    assert reg['edge_files'] == original['edge_files']
    assert [o for o in reg['objects'] if o['object_id'] not in {CID,NID,NEW}] == [o for o in original['objects'] if o['object_id'] not in {CID,NID}]
    write_new(target,reg)
    write_new(HERE/'stage19-objects.json',[lemma,root,comp])

    # Refresh only the eight affected canonical edges. New inclusion is deferred to map receipt/assemble.
    affected = []
    edge_dir = REPO/'map/edges/six-boss1-20261111'
    for rel in original['edge_files']:
        path = REPO/(rel if isinstance(rel,str) else rel['path'])
        edge = json.loads(path.read_text())
        if not {CID,NID}.intersection(edge['source_ids']+edge['target_ids']):
            continue
        assert path.parent == edge_dir
        for ref in edge['evidence']:
            if ref['path'] in changed_paths:
                ref['sha256'] = changed_paths[ref['path']]['sha256']
        for field in ['endpoint_pins','evidence_pins','review_digest']:
            edge.pop(field,None)
        if path.name == 'complete-history-and-PAIR-to-source3-requery.json':
            old_whole = edge.pop('whole_result')
            edge['contribution'] = {'result':old_whole.replace('联合推出目标全部结论','联合推出目标v2保留的全部旧结论'),
                                    'remaining':'现目标v3新增ROOT270及C在O外严格余项另需同根真实第四源P25；该项由新内部参数域对象及新增完整联合边支付，本旧边不再声称整条目标成立。'}
            edge['scope'] += ' Stage19保旧v2准确贡献；不单独支付v3新增ROOT270。'
        edge['review_note'] += ' Stage19由Main实读新增正文后刷新目标/前提版本及SHA；原承重证明逐字保留，本边仅支付明列旧贡献，不自动扩展到新增参数域或γ36。'
        path.write_text(json.dumps(edge,ensure_ascii=False,indent=2)+'\n')
        affected.append(str(path.relative_to(REPO)))
    assert len(affected) == 8

    def edge_base(edge_id,sources,targets):
        return {'edge_id':edge_id,'kind':'implies','status':'accepted','premises_mode':'all',
                'relation_mode':'unconditional','source_ids':sources,'target_ids':targets,
                'reviewed_by':'Boss1/Main six-boss1-20261111',
                'review_note':'Main完整实读正文与来源，逐真实预算核方向/条件；独立准确检查完整参数域、全部弱态、原尺度和全列恒等式。'}
    e1 = edge_base('ca-six-boss1-true-internal-wallets-to-complete-domains',[MODEL,JP],[NEW])
    e1.update(conditions='原完整六人模型；任意真实源节点及合法T、六元可重复查询；取各明列非负参数域。C-only另取真正最大C。',
        roles={MODEL:'支付任一真实节点自身IC、内部SAFE、尾大小帽及末BR，保证共同标签可在不同真实历史查询。',
               JP:'给actual源一般同尾联合投影的合法结构；任意离轨真实源使用模型同样逐项重证，非免费迁移收益。',
               NEW:'准确求固定帽、最小帽与双锚的全状态min/完整域，再保真实索引相关性证明ordered及δ无损有限化。'},
        explanation='先按COST相加所有真实非负预算，零总负载按零份额；逐客户全部尾态比较给各锚的必要且充分面。单缺/双缺证据证明面必要，全余项分解证明充分。ordered保持q=(d−t)/5，连续d=1最小另证；δ保所有仿射尾的完整最优区间和弱端态。各闭域有界且行分片仿射，全部顶点/断点凸生成其整个连续族。',
        scope='整个新对象明列预算族、域、条件菜单投影及其准确有限生成；不支付全局LP最优或SPE实现。',
        whole_result='在正文每节限定的预算、锚和范围内，推出新对象全部完整域/准确最小值/无损有限生成结论；一般JP身份仍归原对象，根λ零新增只在所述族内。',
        evidence=[objects[MODEL]['body'],objects[JP]['body'],lemma['body'],bind(PREFIX+'registration/stage19-main-review.json')]+[bind(PREFIX+n+'.json') for n in main_checks])
    e2 = edge_base('ca-six-boss1-pair-and-internal-domains-pay-full-root-requery',[MODEL,PAIR,NEW],[NID])
    e2.update(conditions='任意合法两行动历史和六合法查询；根结论另取真正最大C及actual根收益u。新P25在根分支自己的真实第四源，强制其合法B6；各历史保同一σ。',
        roles={MODEL:'支付全部旧九预算、根IC、同根大小帽与真实SAFE，并允许新内部偏离自己的续局。',
               PAIR:'支付保重复索引的PAIR36/PAIR30及其有序异索引平均。',
               NEW:'以第四源固定帽θ=s=0专门化支付P25；其余新域不被误当必要前提。',
               NID:'旧九预算包络和三根线保持；再以十预算精确权及两个自由质量项支付ROOT270与η|C\\O|。'},
        explanation='先按旧完整证明支付C36/C30、30索引增益、actual提升和三根线。新P25在同根真实第四节点使用，十项正权合账后全131列准确、128余项非负；对c=1,o=0的32型逐项扣η仍非负。故新根线及C⊆O取等必要性成立，未把发现锥OPT帽扩域。',
        scope='NID v3全体明列结论；容量反馈比较仍只在O≥K，所有根付款本身允许任意六查询并。',
        whole_result='联合推出C36/C30、m30−m36≥43o/6、actual全类型提升、原三条根线及取等/容量反馈，再推出ROOT270和R270≥η|C\\O|，覆盖目标v3完整陈述。',
        evidence=[objects[o]['body'] for o in [MODEL,PAIR,NEW,NID]]+files_as_refs(root_groups))
    e3 = edge_base('ca-six-boss1-visible-C-true-wallets-to-global-gamma36',[MODEL,RC,TX,NID,NEW],[CID])
    e3.update(conditions='原六人完整纯SPE、真正最大合法C、实际前四共同势最大合法X；完整3056必要LP取O=OPT6且O>0归一化。其正权付款另对任意六查询并核实，零权OPT上帽不作推广前提。',
        roles={MODEL:'付actual SAFE6(X/Omean)、六actual SAFE_i(C)、真实偏离合法性和覆盖W=Σu_i；由各安全分母≤6付W−K。',
               RC:'付实际RC(X,Omean)正行，保同一X与真实末回复、任意重叠及索引重复。',
               TX:'付TRUE_X_TAIL_CUT的真实同支联合尾投影，不能改用冻结后继。',
               NID:'付actual C30、ROOT270及严格根C外余项，二者在各自真实源使用。',
               NEW:'付两条第二源C及A5/A6正行、完整弱态与δ=1/144真损失切割。',
               CID:'用全部513列准确对偶合账给α3056；完整零余量面结合真实SAFE等号被排；以δ/根/六SAFE(C)和64列旧余款给γ36普遍改善。'},
        explanation='十条正来源逐项合法。原3056对偶全513列非负、两自由等式处理准确；其18零余量列完整面固定C⊆O、K<1，真实两C行紧迫R3=R4=R5=C，SAFE4/5应相等却N5−N4>0。统一改善独立于此面：Δ=(O−K+Cout−E_C)/36−M1/72，负M1项用完整64列旧余款付，Cout项用ROOT270余项付，再加γ(W−K)，给(1+γ)W−(α+γ)O的全513列非负身份。',
        scope='只支付3056的原模型普遍系数、完整面不可实现性和γ72/γ36精确普遍改善；必要LP匹配原始算术见目标证据。不声称各早期固定域值全域有效，不把零权BG/UP当正付款。',
        contribution={'result':'得到W≥60031108172895495982435367008072256807714132617609 OPT6/135891023315105974064184556965981156861873793636093，并严格排除整个3056旧最优面的完整SPE实现。',
                      'remaining':'仍需支付2W−OPT6或构造满足每个离轨最优性的精确SPE；本边不支付目标内各历史有限系统的独立最优性或未绑定734模板。'},
        evidence=[objects[o]['body'] for o in [MODEL,RC,TX,NID,NEW,CID]]+files_as_refs({'visible_maximum_joint_v5_solve':['exact_certificate.json','optimal_face.json','proof.md'],
                   'delta_uniform_audit':['proof.md','certificate_gamma36.json','positive_source_scope_check.json']})+[bind(PREFIX+'main_visible_c_v5_certificate_check.json'),bind(PREFIX+'main_gamma36_certificate_check.json')])
    new_edges = []
    for filename,edge in [('true-internal-wallets-to-complete-domains.json',e1),
                          ('pair-and-internal-domains-to-full-root-requery.json',e2),
                          ('visible-C-true-wallets-to-global-gamma36.json',e3)]:
        path = edge_dir/filename
        write_new(path,edge)
        new_edges.append(str(path.relative_to(REPO)))
    write_new(HERE/'stage19-registration-summary.json',{'status':'PREPARED_REVIEWED_BODIES_REGISTRY_AND_UNBOUND_EDGES',
        'old_registry_sha256':OLD_REGISTRY,'candidate_sha256':digest(target),
        'objects':[{'object_id':o['object_id'],'version':o['version'],'body':o['body'],'evidence_count':len(o['evidence'])} for o in [lemma,root,comp]],
        'preserved_unrelated_objects':len(original['objects'])-2,'old_edge_count':len(original['edge_files']),
        'new_edge_count':3,'affected_existing_edges':affected,'new_edges':new_edges,
        'canonical_edge_list_unchanged':True,'next':'research register; bind/check the eleven edges; checkpoint; scoped replacement map receipt and assemble.'})
    print(json.dumps({'status':'PREPARED','objects':len(reg['objects']),'materials':len(reg['materials']),
                      'existing_edges_refreshed':len(affected),'new_edges':len(new_edges),'canonical_edges_unchanged':len(reg['edge_files'])},ensure_ascii=False))


def files_as_refs(groups):
    return [bind(path) for path in files(groups)]


if __name__ == '__main__':
    main()
