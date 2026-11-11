"""Three new mathematical identities plus version 2 of the existing finite result.

The complete candidate is made from the exact current registry. Existing
identities/material owners are preserved; no source object is silently changed.
"""
from pathlib import Path
import hashlib,json,copy
B=Path(__file__).resolve().parent;R=B.parents[2]
RUN='research/workspaces/six-boss2-20261111-cross/'
manifest=json.loads((B/'formal-round4-identities.json').read_text())
ids,paths=manifest['ids'],manifest['bodies']
regpath=R/'research/registry.json'
current=json.loads(regpath.read_text())
lookup={o['object_id']:o for o in current['objects']}
assert all(ids[k] not in lookup for k in ('hierarchy','prefix','price'))
assert lookup[ids['finite']]['version']==1
def ref(path):return {'path':path,'sha256':hashlib.sha256((R/path).read_bytes()).hexdigest()}
for key,p in paths.items():assert ref(p)['sha256']==manifest['body_sha256'][key]
common='archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'
pairbody='archives/customer-attraction/state/引理/同源双末对跨枝配对与严格联合投影--引理.md'
discountbody='archives/customer-attraction/state/引理/同源真实末回复的折扣闭包与二状态精确投影--引理.md'
model=lookup['M-e394b173b9b1419588c6c380da4bd326']['model']
evidence={
 'hierarchy':[common,pairbody,*[RUN+p for p in (
  'joint_requery/formal_query_projection_hierarchy_v1.md',
  'joint_requery/portfolio_comparison/formal_portfolio_strictness.md',
  'joint_requery/portfolio_comparison/exact_single_lifts_5744_i3_m0_orb00.json',
  'joint_requery/portfolio_comparison/joint_common_denominator_5744.json',
  'joint_requery/portfolio_comparison/compare_5744.py',
  'joint_requery/portfolio_comparison/recover_single_lifts.py',
  'joint_requery/portfolio_comparison/simplify_joint_cut.py',
  'joint_requery/portfolio_master.py',
  'joint_requery/cross_query_pairs_v1.py','joint_requery/audit_cross_query_pairs_v1.py',
  'joint_requery/cross_query_pairs_v1_audit.json','joint_requery/package_cross_pairs_5775_v1.py',
  'joint_requery/recover_332_lift_5775_v1.py','joint_requery/exact_332_lift_cross_strictness_5775_v1.json',
  'joint_requery/cross_pairs_selected_5775_v1.json','joint_requery/cross_query_disagreement_identity_5775_v1.json',
  'joint_requery/portfolio_selected_5744.json',
  'master_cuts/dynamic_5744_exact.json','master_cuts/dynamic_5775_exact.json',
  'main_pair_features.py','main_cross_query_features_v1.py',
  'main_verify_single_lifts_5744.py','main_verify_single_lifts_5744.json',
  'main_verify_portfolio_500.py','main_verify_portfolio_500.json',
  'main_verify_portfolio_pair_5744.py','main_verify_portfolio_pair_5744.json',
  'main_verify_cross_pairs_5775.py','main_verify_cross_pairs_5775.json',
  'main_verify_332_lift_5775.py','main_verify_332_lift_5775.json')]],
 'prefix':[common,pairbody,discountbody,*[RUN+p for p in (
  'coverage_bridge/formal_prefix_tail.md','coverage_bridge/selected_prefix_tail_5752.json',
  'coverage_bridge/prefix_tail_requery.py','coverage_bridge/compact_prefix_tail_cuts.py',
  'coverage_bridge/prefix_tail_beta_zero_audit.json','joint_requery/portfolio_master.py',
  'joint_requery/explore_projection.py','joint_requery/separate_master.py',
  'master_cuts/dynamic_5752_exact.json','main_pair_features.py',
  'main_verify_prefix_tail_5752.py','main_verify_prefix_tail_5752.json')]],
 'price':[common,discountbody,*[RUN+p for p in (
  'main_pair/balanced_any_tail_price.md','coverage_bridge/audit_balanced_any_tail_price.md')]]}
objects=[]
def add(key,**kw):
    o={'object_id':ids[key],'version':1,**kw,'body':ref(paths[key]),
       'evidence':[ref(p) for p in dict.fromkeys(evidence[key])],
       'sources':[paths[key],'RUN:six-boss2-20261111-cross; actor:Boss2; Main personally checked proof, scope and exact certificates.']}
    objects.append(o)
add('hierarchy',title='共同真实回复的76/332/616严格投影层级与跨查询对称差信用',
    kind='strict-hierarchy-of-shared-hidden-reply-projections',truth_status='proved',model=model,
    statement='固定actual第四源、R种子、第一类非对角轨道、17个指定合法查询及充分细化可见域。共同616行投影严格包含于共同332行投影，后者严格包含于17个单Q76行投影的交。5744点的17份有理旧提升与500整数权负行证明右侧严格；5775点的79原子共同332提升与12整数权跨查询负行证明左侧严格。三额外剩余交矩按条件质量分裂细化旧提升，不偷换比较域。12权行预算413u4+164u6+14K，新增48PAIR1(Ti,Bj)相对24+24两个对角PAIR准确增加24·1_(Ti△Bj)/[(p+t+1)(p+t+2)]，与隐藏位无关，故穿过min为等式。',
    quantifiers='非严格包含与逐客户PAIR恒等式对任意原模型完整SPE、固定同一源和合法查询成立。两道严格性仅在正文明确的actual4/R/orb00/17菜单共同可见域存在两份不同有理见证；不是对每个输入都严格。',
    assumptions=['两枝第一真末主题C同时是第二枝强制动作，所有查询共用该组隐藏回复','两个剩余查询的same/off联合索引分布对全部客户相同，正确保交矩','源收益与actual六位会员同一质量关联；不同单Q提升可不同，但332/616必须共同'],
    scope='原模型合法必要行、两个完整局部投影锥的严格包含及八条绑定5775点的精确负行。',
    objections='两份见证均非完整SPE；仅整数化客户质量不能实现全部有序历史。新增同余族off行的交叠不等于均值平方。目标值上升不替代旧锥全部参数不可推出性的提升证据。')
add('prefix',title='独立初段与折扣尾闭包在同一真实末端的合法联合投影',
    kind='shared-terminal-prefix-and-discounted-tail-composition',truth_status='proved',model=model,
    statement='同源余k≥3，初段为T→真末B/C以及回同源C→真末J/V。任意非负初段合同alpha与独立非负二状态折扣尾合同beta，在合法V上接合后给(aT+aC+a_beta)r+(Aalpha+Abeta)u_m+(Dalpha+Dbeta)K≥Σ min[Ealpha+Psi_beta(v)]。源总权按三项合计；初段中间数k−3，尾段k−2。固定参数联合min至少为分别min之和；5752点16条准确负行中12条beta非零且同权分别投影非负，另4条beta零只为旧参数更新。',
    quantifiers='任意有限原模型完整SPE、合法有序源、固定合法种子和静态菜单、客户无关非负初段/尾权、0≤delta<1。有限16行的负值和固定同权严格增益仅在所绑定5752点上。',
    assumptions=['尾部统一闭包对全部合法F成立，才能用于初段的真实V','两合同共用同一V会员后取min，且全部源/末价/容量成本相加','菜单在对尾部当前主题取最大值之前固定；动态自查询另显式计权'],
    scope='一般合法组合定理及固定同权投影增益；对全体旧参数锥的严格包含尚未证明。',
    objections='beta非零不等于delta正；delta0只增加一次尾合同。固定参数的联合优于分别不能声称超过所有旧参数组合。改用另一源必须另付其实际或离轨源收益。')
add('price',title='任意尾长平衡查询权闭包给所有目录主题的统一正加性价格',
    kind='uniform-positive-customer-price-from-balanced-terminal-closure',truth_status='proved',model=model,
    statement='同源余k≥2，源权a等于静态查询总权加当前自查询权mu_*，静态q_x满足0≤q_x≤a−mu_*。折扣Bellman势Psi给b_x=Psi(0)、w_x=Psi(1)−Psi(0)。任意合法主题F同时满足Σw_x1_F≤B−Σb_x，且(1−theta)[(a−q)/(p+k−1)+(mu_*+q)/(p+k)]≤w≤(1−theta)[(a−q)/(p+1)+(mu_*+q)/(p+2)]。a>0时每客户价严格正，a0时全0。证明关键H(1,c,s)−H(0,c,s)与c和价格参数无关，随后对同一s域和同一Bellman固定点两行取min。',
    quantifiers='任意有限原模型完整SPE、同一有序源、k≥2、先固定的合法静态查询及非负价/容量权、0≤theta<1，随后对目录全部F同时量化。',
    assumptions=['平衡源权a=M；q不随被定价F改变，自查询mu_*已显式包括','每次借给其它分支合法主题均支付完整B及同一常量Σb，多个主题按总权计费','只有源在actual路径时才能把r写为实际u_i'],
    scope='一般全目录正价接口和逐客户准确上下界；未宣称此接口已单独切掉当前必要点。',
    objections='k2上下界相等且价格参数消去；k>2不能假定已取min的四边仍平衡或w与价格参数无关。不同离轨源收益不能免费合并为W。')

finite=copy.deepcopy(lookup[ids['finite']])
finite.update(version=2,title='固定16hist的5716至5783六轮必要LP精确最优值与正尾有限提升',
    body=ref(paths['finite']),
    statement=finite['statement']+'版本2在相同列域上继续认证5752、5775、5783，准确最优W分别约0.4916608461765668、0.49192027032608004、0.4926332627883867。5752原始点保持原SHA，候选等式选择修复后146正对偶全部列准确成立。5775有137正对偶，5783有160正对偶；新增对偶支撑分别5、4、3条。删去12条beta非零而保留同期7+4普通更新的5763系统有精确可行点W≈0.491714016012119，严格低于5775已证最优，给具体正尾族至少约0.00020625431396106435的严格有限目标提升。',
    quantifiers='仅正文及证据绑定SHA的六个完整有限有理矩阵、其全部非负列质量，以及指定删行系统；不是对所有客户型或所有完整SPE量化的福利常数。',
    scope='证明六个有限必要LP的准确最优值及其仍小于1/2，补具体12条正尾行对有限目标的严格贡献。一般六人命题仍开放。')
newrefs=[paths['hierarchy'],paths['prefix']]
newrefs += [RUN+p for p in (
 'master_cuts/formal_5752_5775_gap.md','master_cuts/formal_5775_tail_ablation.md','master_cuts/formal_5783_gap.md',
 'master_cuts/scaled_dual.py','master_cuts/advance_with_exact_cert.py','master_cuts/alternate_primal.py','master_cuts/ablate_positive_tail.py',
 'master_cuts/ablate_5775_positive_tail_exact.json','master_cuts/ablate_5775_positive_tail_verification.json',
 'joint_requery/portfolio_selected_5744.json','joint_requery/portfolio_selected_5752.json','joint_requery/cross_pairs_selected_5775_v1.json',
 'coverage_bridge/selected_prefix_tail_5752.json',
 'main_pair_features.py','main_cross_query_features_v1.py',
 'main_verify_portfolio_pair_5744.py','main_verify_portfolio_pair_5744.json',
 'main_verify_portfolio_pair_5752.py','main_verify_portfolio_pair_5752.json',
 'main_verify_prefix_tail_5752.py','main_verify_prefix_tail_5752.json',
 'main_verify_cross_pairs_5775.py','main_verify_cross_pairs_5775.json',
 'main_verify_tail_ablation.py','main_verify_tail_ablation.json')]
for num in (5752,5775,5783):
    for suffix in ('matrix.json.gz','exact.json','dual.json','identity.json','review_manifest.json','verification.json','config.json'):
        newrefs.append(RUN+f'master_cuts/dynamic_{num}_{suffix}')
    newrefs.append(RUN+f'main_verify_dynamic_{num}.json')
finite['evidence']=[ref(p) for p in dict.fromkeys([e['path'] for e in finite['evidence']]+newrefs)]
finite['sources'] += ['Version 2: all three new finite primal/dual certificates and exact positive-tail ablation independently replayed by Main.']
objects.append(finite)

mat={m['path']:copy.deepcopy(m) for m in current['materials']}
touched={}
for obj in objects:
    for r,isbody in [(obj['body'],True)]+[(e,False) for e in obj['evidence']]:
        path=r['path'];row=mat.get(path)
        if row:
            if row['sha256']!=r['sha256']:
                assert path==paths['finite'] and set(row['object_ids'])=={ids['finite']},(path,row)
            row={**row,'sha256':r['sha256'],'object_ids':list(row['object_ids'])}
            assert row['disposition'] in ('objects','attachment')
            if obj['object_id'] not in row['object_ids']:row['object_ids'].append(obj['object_id'])
        else:
            row={**r,'disposition':'objects' if isbody else 'attachment','object_ids':[obj['object_id']],
                 'reason':'Boss2 Main本轮实读、推导和独立准确审计后的投影层级、共享末端合同、统一正价或有限必要LP证据；范围以正文量词为准。'}
        if isbody:row['disposition']='objects'
        mat[path]=row;touched[path]=row
replacement={o['object_id']:o for o in objects}
updated=[replacement.pop(o['object_id'],o) for o in current['objects']]+list(replacement.values())
out={**current,'objects':updated,'materials':list(mat.values())}
delta={'schema':2,'base_registry':ref('research/registry.json'),'objects':objects,'materials':list(touched.values()),
       'edge_files':[],'scope':'Three new identities and finite object version 2 through 5783; existing independent proof routes preserved.'}
(B/'registration-round4-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n')
(B/'registration-round4-candidate.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_objects':3,'updated_objects':1,'touched_materials':len(touched),'candidate_objects':len(updated),'base_sha256':delta['base_registry']['sha256']},ensure_ascii=False))
