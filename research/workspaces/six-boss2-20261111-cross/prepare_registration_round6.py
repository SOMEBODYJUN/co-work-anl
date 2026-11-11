"""Preserve the canonical registry while promoting two versions and one lemma."""
from pathlib import Path
import copy
import hashlib
import json

B=Path(__file__).resolve().parent
R=B.parents[2]
RUN='research/workspaces/six-boss2-20261111-cross/'
manifest=json.loads((B/'formal-round6-identities.json').read_text())
ids,paths=manifest['ids'],manifest['bodies']
current=json.loads((R/'research/registry.json').read_text())
lookup={o['object_id']:o for o in current['objects']}
assert lookup[ids['hierarchy']]['version']==1
assert lookup[ids['finite']]['version']==2
assert ids['shared_rz'] not in lookup


def ref(p):
    path=R/p
    assert path.is_file(),p
    return {'path':p,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


for key in ('hierarchy','shared_rz'):
    assert ref(paths[key])['sha256']==manifest['initial_sha256'][key]
assert ref(paths['finite'])['sha256']==json.loads((B/'formal-finite-round6.json').read_text())['body_sha256']
common='archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'
prefix='archives/customer-attraction/state/引理/共享真实末端的独立初段与折扣尾闭包--引理.md'
discount='archives/customer-attraction/state/引理/同源真实末回复的折扣闭包与二状态精确投影--引理.md'
portfolio='archives/customer-attraction/state/引理/共享真实末回复的组合查询投影与同源重配权--引理.md'
frechet='archives/customer-attraction/state/障碍/固定末回复四态边缘的Fréchet共同扩张障碍--障碍.md'
fullspe='archives/customer-attraction/state/程序/复制税的固定策略锥与全SPE最小税递推--程序.md'
newpaths={
 'hierarchy':[
 'joint_requery/formal_reverse_terminal_strictness_v1.md',
 'joint_requery/reverse_terminal_5799_one_v1.json',
 'joint_requery/actual_padding_616_vs_624_strictness_5799_v1.json',
 'joint_requery/complete624_actual4_R00_v1_contract.md',
 'joint_requery/complete624_actual4_R00_v1_matrix.json.gz',
 'joint_requery/complete624_actual4_R00_v1_mapping.json',
 'main_reverse_terminal_features_v1.py',
 'main_verify_reverse_terminal_strictness_v1.py','main_verify_reverse_terminal_strictness_v1.json',
 'main_verify_complete624_v1.py','main_verify_complete624_v1.json'],
 'shared_rz':[
 'coverage_bridge/formal_shared_rz_income_bridge_v1.md',
 'coverage_bridge/selected_prefix_tail_5752.json',
 'coverage_bridge/mainline_zero_capacity_v1.md','coverage_bridge/mainline_zero_capacity_v1.json',
 'coverage_bridge/zero_capacity_rows_v1.py',
 'coverage_bridge/shared_rz_zero_capacity_v1.md',
 'coverage_bridge/shared_rz_zero_capacity_v1.py','coverage_bridge/shared_rz_zero_capacity_v1.json',
 'coverage_bridge/a6_query_credit_hidden_map_v1.md',
 'coverage_bridge/strong_a6_transfer_v1.md','coverage_bridge/strong_a6_transfer_v1.py',
 'coverage_bridge/strong_a6_transfer_v1.json',
 'main_zero_capacity_features_v1.py',
 'main_verify_zero_capacity_v1.py','main_verify_zero_capacity_v1.json',
 'main_verify_strong_a6_transfer_v1.py','main_verify_strong_a6_transfer_v1.json',
 'main_pair_features.py'],
 'finite':[
 'master_cuts/formal_5786_gap.md','master_cuts/formal_5799_gap.md',
 'master_cuts/formal_complete_zz_11418_gap_v1.md',
 'master_cuts/complete_zz_extension_contract_v1.md',
 'master_cuts/build_complete_zz_v1.py','master_cuts/solve_complete_zz_v1.py',
 'master_cuts/solve_complete624_v1.py',
 'master_cuts/full_history_probe_contract_v1.md',
 'master_cuts/formal_twelve_label_probe_v1.md',
 'master_cuts/prepare_full_history_probe_v1.py','master_cuts/full_history_fixed_catalog_dp_v1.py',
 'master_cuts/full_history_probe_12label_v1.json',
 'master_cuts/full_history_probe_12label_v1_result.json',
 'master_cuts/full_history_probe_12label_v1_menus.json.gz',
 'master_cuts/full_history_probe_12label_v1_witnesses.json.gz',
 'master_cuts/full_history_probe_12label_v1_execution.json',
 'master_cuts/twelve_label_tail_direct_v1.json','master_cuts/explain_twelve_label_tail_v1.py',
 'main_verify_cross_pairs_v2.py','main_verify_cross_pairs_5783_three.json',
 'main_verify_neighbor_5786.py','main_verify_neighbor_5786.json',
 'main_verify_complete_zz_v1.py','main_verify_complete_zz_v1.json',
 'main_verify_extended_primal_dual_v1.py','main_verify_complete_zz_5799_v1.json',
 'main_verify_zz_projection_v1.py','main_verify_zz_projection_v1.json',
 'main_verify_explicit_primal_dual_v2.py','main_verify_complete624_opt_v2.json',
 'main_verify_624_projection_v1.py','main_verify_624_projection_v1.json',
 'main_verify_twelve_label_input_v1.py','main_verify_twelve_label_input_v1.json',
 'main_verify_full_history_probe_v1.py','main_verify_full_history_probe_v1.json',
 'joint_requery/complete624_actual4_R00_v1_matrix.json.gz',
 'joint_requery/complete624_actual4_R00_v1_mapping.json',
 'joint_requery/complete624_actual4_R00_v1_contract.md',
 'main_verify_complete624_v1.py','main_verify_complete624_v1.json',
 'master_cuts/neighbor_bridge_review_v1.md',
 'master_cuts/neighbor_bridge_5786_addendum_v1.md',
 'master_cuts/neighbor_5786_selected_13_v1.json']
}
for n in (5786,5799):
    for suffix in ('matrix.json.gz','exact.json','dual.json','identity.json','review_manifest.json','verification.json','config.json'):
        newpaths['finite'].append(f'master_cuts/dynamic_{n}_{suffix}')
    newpaths['finite'].append(f'main_verify_dynamic_{n}.json')
for suffix in ('matrix.json.gz','mapping.json','exact.json','dual.json','original4849_exact.json','verification.json','basis.json'):
    newpaths['finite'].append('master_cuts/complete_zz_5799_v1_'+suffix)
for suffix in ('exact.json','dual.json','original4849_exact.json','verification.json','basis.json'):
    newpaths['finite'].append('master_cuts/complete624_actual4_R00_opt_v2_'+suffix)

extra_formal={
 'hierarchy':[common],
 'shared_rz':[common,prefix,discount],
 'finite':[paths['hierarchy'],prefix,portfolio,frechet,fullspe]
}


def allrefs(key,existing=()):
    return [ref(p) for p in dict.fromkeys([e['path'] for e in existing]+extra_formal[key]+[RUN+p for p in newpaths[key]])]


hier=copy.deepcopy(lookup[ids['hierarchy']])
hier.update(version=2,title='共同真实回复的76/332/616/624严格投影层级与全权有限提升等价',
 body=ref(paths['hierarchy']),
 statement=hier['statement']+'版本2加入原R/Z真实末节点对同一宏B/C/J/V的八条零预算查询。经一份确定actual000101、六旧词全111的6δ质量补齐，57可见型77原子通过全部616预算，但16整数权624行严格负；因此在共同17-hist或一般actual关联域上P624严格小于P616。原两严格见证以新增hist质量0嵌入。另证固定可见边缘下，一份完整隐藏提升等价于全部非负原始行权投影，包括源总权0；不是SPE实现定理。',
 quantifiers='合法行与非严格包含对任意原模型完整SPE及相同合法历史结构成立；三道严格性在共同17-hist/一般actual关联域存在三个有理见证，支撑分别16、16、17。第三道严格性不声称原固定16hist域；完整624有限表示仍只用原16hist。',
 scope='四层完整局部投影的严格链、对称差恒等式、原末背景反查及全部非负权与共同有限提升的双向等价。',
 objections='三份有理见证不是完整SPE。旧5799点本已违反616，严格性由另行actual质量补齐承担；不得用新正权或数值改善代替旧族全部参数可行证明。')
hier['assumptions'][-1]='源收益与actual六位质量关联；单Q可分别提升，332/616/624须各自共同提升，比较严格性使用同一D17域'
hier['evidence']=allrefs('hierarchy',hier['evidence'])
hier['sources'] += ['Version 2: Main independently checked every new coefficient, actual-linked padding witness and the separation-theorem equivalence. Frozen old evidence preserved.']

finite=copy.deepcopy(lookup[ids['finite']])
finite.update(version=3,title='固定16hist十个必要LP的准确最优值、完整局部闭包与指定十二标签SPE排除',
 body=ref(paths['finite']),
 model=finite['model'].replace('本对象仅研究固定16hist、4849列、非负有理质量的明示必要系统；母矩阵含OPT单换行，比较六元组取最优。',
 'LP部分限固定16hist、原4849语义前缀及明示非负辅助提升；母矩阵含OPT单换行，比较六元组取最优。另研究由其中一份边缘构造的唯一十二标签有限整数客户目录之全部完整SPE。'),
 statement=finite['statement']+'版本3准确认证5786及5799最优均约0.49265432731768616；完整39类ZZ自由min提升11418×7639保持同值，完整单结构624提升12666×12631的准确最优约0.49265618211149476，929正原始列和516正对偶全矩阵相配。旧点被切与最优值增加分开；ZZ辅助非真交集。由闭ZZ实际/T边缘制备唯一12标签48兴趣类型的整数博弈，完整SPE根终局集合只有六T各一次，故该目录最坏W/OPT6=1；六A目标的A5在指定前四历史偏T1时，每个可信末回复T2..T6均严格获益。',
 quantifiers='十份正文绑定SHA的有限必要矩阵与非负质量，以及一份指定十二标签/48整数客户类型输入的全部完整有序历史纯SPE；不量化任意目录的全域福利常数。',
 scope='十份有限LP精确原始/对偶，指定有限投影机制的闭包，正尾消融，和一份真实有限目录的全SPE排除。六人一般命题仍OPEN。',
 assumptions=['原4849语义列及旧行按前缀保持，扩展目标/归一新系数为0','新增机制经Main核真实预算及系数；完整原/对偶证书独立逐Fraction检查','完整SPE菜单缓存计数集合而非一份全局计数策略；巨大整数用任意精度，弱平局全保'],
 objections='必要LP点未给全目录完整历史实现。12标签阴性只排除该固定目录，不排除添加新主题；固定支持达到half也不自动证明原题。零新对偶不表示全域冗余。')
finite['evidence']=allrefs('finite',finite['evidence'])
finite['sources'] += ['Version 3: Main full matrix primal/dual replay, independent full624 coefficient audit, and independently recomputed all full-history SPE menus plus a complete witness DAG for the fixed twelve-label input.']

rz={
 'object_id':ids['shared_rz'],'version':1,
 'title':'共享真实R/Z边的四态覆盖信用与保持末端的实际收入转移',
 'kind':'shared-real-terminal-edge-coverage-and-income-bridge','truth_status':'proved',
 'model':lookup[ids['hierarchy']]['model'],
 'statement':'设同一真实Z末节点在前缀P后强制R，已有A(r)、B(z)两合同；非负权满足alphaΔA≥lambda*q/((P+1)(P+2))与betaΔB≥lambda/(P+1)，则共同四态min恰alpha*A0+beta*B0+lambda*q/(P+1)，同权复制R准确损失lambda*q/((P+1)(P+2))。六人49:10零容量实例保同一R^C/Z^C，保持真实末端v的隐藏映射给21669*a6/D客户信用，最终148951u4−1278u6≥(10857/2)OPT6−(88871/9)W。覆盖税在强移账后由类型复制证明准确不变；U/C障碍表明该最终逐客户方式尚不能支付u4。',
 'quantifiers':'一般四态引理对任意有限共同目录完整纯SPE、固定真实边、固定合法查询凸组合及满足逐客户两差界的共同非负权成立。整数实例对任意原六人SPE、任意达到OPT6的六个可重复合法标签成立；不假设分区或客户型独立。',
 'assumptions':['R与Z必须是同一真实末回复边的主题；两处r共用，真实Z查询背景为P+r','两个初段/尾合同完整支付同一actual u4及末价；静态Bj→Cj不改宏隐藏b','非负IC权及共同C标签跨索引身份保留；尾合同先对所有合法F量化，再用于真实v','强收入信用用保持v的映射，所有负基线及四个a6=1负型重新计税'],
 'scope':'普遍必要收入/覆盖不等式、同权共享增益和直接隐藏映射证明；未闭合半覆盖付款。',
 'objections':'负u6系数来自移去已证正客户收入信用，不是负IC权。同权复制R比较不等于全部参数锥严格包含；仍有148951u4费用，U/C只否定所显示局部付款法，不是SPE反例。',
 'body':ref(paths['shared_rz']),'evidence':allrefs('shared_rz'),
 'sources':[paths['shared_rz'],'RUN:six-boss2-20261111-cross; actor:Boss2; Main fully read the proof and independently reconstructed all finite rational constants and the v-preserving map.']
}
objects=[hier,finite,rz]
changed_bodies={paths['hierarchy'],paths['finite']}
edited_ids={o['object_id'] for o in objects}
for o in current['objects']:
    if o['object_id'] not in edited_ids:
        assert not any(r['path'] in changed_bodies for r in [o['body']]+o.get('evidence',[])),o['object_id']
mat={m['path']:copy.deepcopy(m) for m in current['materials']}
touched={}
for o in objects:
    for r,isbody in [(o['body'],True)]+[(e,False) for e in o['evidence']]:
        p=r['path']
        if p in mat:
            row=copy.deepcopy(mat[p])
            if row['sha256']!=r['sha256']:
                assert p in changed_bodies,(p,row['sha256'],r['sha256'])
                assert set(row['object_ids']).issubset(edited_ids),(p,row['object_ids'])
            row['sha256']=r['sha256']
            assert row['disposition'] in ('objects','attachment')
            if o['object_id'] not in row['object_ids']:row['object_ids'].append(o['object_id'])
        else:
            row={**r,'disposition':'objects' if isbody else 'attachment','object_ids':[o['object_id']],
                 'reason':'Boss2 Main核准的严格投影、共享真实末边收入合同、有限准确LP或指定真目录完整SPE证据；量词以承重正文为准。'}
        if isbody:row['disposition']='objects'
        mat[p]=row
        touched[p]=row
replace={o['object_id']:o for o in objects}
updated=[replace.pop(o['object_id'],o) for o in current['objects']]+list(replace.values())
candidate={**current,'objects':updated,'materials':list(mat.values())}
delta={'schema':2,'base_registry':ref('research/registry.json'),'objects':objects,
       'materials':list(touched.values()),'edge_files':[],
       'scope':'Existing hierarchy v2, existing finite computation v3, and one new general shared-RZ income bridge; no proof of the original half bound.'}
for name,data in [('registration-round6-candidate.json',candidate),('registration-round6-delta.json',delta)]:
    p=B/name
    assert not p.exists()
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_objects':1,'updated_objects':2,'touched_materials':len(touched),'base_sha256':delta['base_registry']['sha256']},ensure_ascii=False))
