"""Assemble a small reviewed increment over the exact current registry."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;R=B.parents[2]
root='research/workspaces/six-boss2-20261111-cross/'
ids={'pair':'M-e394b173b9b1419588c6c380da4bd326','discount':'M-b233ef00a9c34e189817cdfb7a495107','finite':'M-ddceaa3d53064498b3e833a32e1f3b6f'}
bodies={
 'pair':'archives/customer-attraction/state/引理/同源双末对跨枝配对与严格联合投影--引理.md',
 'discount':'archives/customer-attraction/state/引理/同源真实末回复的折扣闭包与二状态精确投影--引理.md',
 'finite':'archives/customer-attraction/subarchives/six-providers/state/计算/同源跨枝增强必要图的精确最优值与半界缺口--计算.md'}
def ref(p):return {'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest()}
model='有限单位客户、有限非空共同标签目录，标签覆盖可空、可相同；单位提供者观察全部有序历史依次各行动一次，客户终局在覆盖者间均分。完整纯SPE在全部合法有序历史对全部合法偏离满足同一完整策略真实后继下的弱IC。保任意平局、重复行动与零客户。'
common='archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'
evidence={
 'pair':[
 common,
 'archives/customer-attraction/state/引理/三十四权同源双分支的真实行锥与精确计数消元--引理.md',
 'archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md',
 *[root+p for p in ['joint_requery/actual_signature_witness.json','joint_requery/strict_projection_witness.json','joint_requery/find_actual_projection.py','joint_requery/explore_projection.py','joint_requery/separate_master.py','joint_requery/selected_cuts_5716.json','master_cuts/merged_5716_exact.json','main_verify_pair.py','main_verify_pair.json']]],
 'discount':[
 common,'archives/customer-attraction/state/引理/共享真实末回复的组合查询投影与同源重配权--引理.md',
 *[root+p for p in ['coverage_bridge/new5716_joint_discounted.json','coverage_bridge/joint_discounted_requery.py','coverage_bridge/audit_discounted_cuts.py','coverage_bridge/discounted_audit_and_finite_depth.json','coverage_bridge/new5727_single_portfolio_cut.json','main_verify_discounted.py','main_verify_discounted.json','main_verify_portfolio_5727.py','main_verify_portfolio_5727.json','main_pair/balanced_discount_proof.md','main_pair/continuous_discount.py','main_pair/continuous_discount_5727.json','master_cuts/merged_5716_exact.json','master_cuts/dynamic_5727_exact.json']]],
 'finite':[
 common,bodies['pair'],bodies['discount'],
 'archives/customer-attraction/state/计算/同源再查询与容量报价的三份冻结切面包--计算.md',
 'archives/customer-attraction/state/计算/实际末主题分支分离器与四菜单补价原点核验--计算.md',
 'archives/customer-attraction/tools/evidence/b-family-menu-prices-boss3/original/research_2/all_menu_prices_exact.json',
 *[root+p for p in [
 'master_cuts/master_5716_exact.json.gz','master_cuts/merged_5716_exact.json','master_cuts/dual_exact.json','master_cuts/cuts_24_exact.json','master_cuts/matrix_identity.json','master_cuts/materialization.json','master_cuts/merge_master.py','master_cuts/certify_dual.py','master_cuts/verify_certificate.py','master_cuts/certificate_verification.json',
 'master_cuts/dynamic_5727_matrix.json.gz','master_cuts/dynamic_5727_exact.json','master_cuts/dynamic_5727_dual.json','master_cuts/dynamic_5727_identity.json','master_cuts/dynamic_5727_review_manifest.json','master_cuts/dynamic_5727_verification.json','master_cuts/extend_master.py',
 'master_cuts/dynamic_5744_matrix.json.gz','master_cuts/dynamic_5744_exact.json','master_cuts/dynamic_5744_dual.json','master_cuts/dynamic_5744_identity.json','master_cuts/dynamic_5744_review_manifest.json','master_cuts/dynamic_5744_verification.json','master_cuts/dynamic_5744_config.json','master_cuts/advance_master.py','master_cuts/fixed_domain_summary.json','master_cuts/inspect_fixed_domain.py',
 'main_verify_5716.py','main_verify_5716.json','main_verify_dual_5716.json','main_verify_primal_dual.py','main_verify_dynamic_5744.json','main_verify_pair.py','main_verify_pair.json','main_verify_discounted.py','main_verify_discounted.json','main_verify_pair_5727.py','main_verify_pair_5727.json','main_verify_portfolio_5727.py','main_verify_portfolio_5727.json','static_optimality_boundary.md',
 'joint_requery/selected_cuts_5716.json','joint_requery/selected_cuts_5727.json','coverage_bridge/new5716_joint_discounted.json','coverage_bridge/new5727_single_portfolio_cut.json']]]}
objects=[]
def add(key,**kw):
 objects.append({'object_id':ids[key],'version':1,**kw,'body':ref(bodies[key]),'evidence':[ref(p) for p in dict.fromkeys(evidence[key])],'sources':[bodies[key],'RUN:six-boss2-20261111-cross; actor:Boss2; Main independently verified load-bearing identities and exact inputs.']})
add('pair',title='同源双末对跨枝PAIR先合账再投影及actual关联域严格增强',kind='general-local-inequality-and-strict-cone-separation',truth_status='proved',model=model,
 statement='任意同一源h余k≥3，强制T后真尾B/C，再回同源强制同一C后真尾J/V。将34预算锥和两枝强PAIR以非负权合并，两源权和1，得r+A u_m+D K≥Σ min F，隐藏域16(k−2)^2且保共享C。k3、actual第四源p∈{0,1,2,3}有九行整数证书71198u4+925K≥Σ[(65146t+6052q)/(p+1+2t)+925t]。一个13原子actual六位关联提升满足全部34旧行及16末价/容量行，而新整数尺度余量为−90896/19269，故严格超出旧34投影锥。另五条有理行精确分离绑定SHA的5716点。',
 quantifiers='任意有限实例、完整有序历史纯SPE、任意固定合法源/主题/有限查询菜单及客户无关非负权；九行闭式只限k3与p=0..3。严格性是指定局部关联域及完整旧锥上的存在性。',
 assumptions=['两个强制分支都回到同一有序源并沿同一完整策略','所有查询标签属于共同目录；PAIR自交平均按同一索引取乘积','中间位只经人数进入时才用16(k−2)^2压缩'],
 scope='一般合法必要行、旧34锥严格增强、五个固定输入切面；主问题仍开放。',
 objections='不主张逐客户IC、共同最小态可实现、不同离轨源收入可相加或half；九行闭式p=4已失效；旧抽象见证的非法actual背景不用于本actual严格性。')
add('discount',title='同一源真实末回复的折扣最大值闭包与二状态精确消元',kind='general-local-discounted-query-closure',truth_status='proved',model=model,
 statement='固定源h余k≥2，令C(T)为强制T后的真实末主题。非负源/实际末价/容量/查询权给同一预算B≥ΣH_x(t,c,s)。若0≤θ<1且V_x(t)−θV_x(c)≤H_x(t,c,s)对所有局部位成立，则每个合法种子T0有B≥(1−θ)ΣV_x(1_T0)。有限共同目录上取辅助加性V最大的主题给有限证明。二状态Bellman式各起点仅需三个有理候选；k2平衡源权a=M时二循环不决定最小，固定有限输入的连续θ最小可由有理折点精确求得。绑定5716点有六条精确负行，其中五条θ>0；固定最强参数需18轮截断才首次为负，且在5727点整个连续θ族不再分离。',
 quantifiers='任意有限客户/有限非空共同标签目录、任意完整纯SPE、同一固定源、固定合法种子及查询菜单、客户无关非负实权、0≤θ<1；有理参数给有理投影。',
 assumptions=['查询菜单固定后才对当前重查询主题取辅助最大值','所有C(T)均来自同一策略且属于同一共同目录','外部预算B每步相同；真实末位、实际末价和共同容量各按总权计账'],
 scope='一般折扣必要不等式、精确二状态投影、平衡权连续参数有限化；所列数值范围仅绑定各输入SHA。',
 objections='θ=1只作极限且丢当前种子位；常量查询中仍可保种子。四状态120扫描只有θ0一条普通portfolio负行，不构成四状态增益或全族冗余证明。六人全局共同付款未完成。')
add('finite',title='固定16hist的5716、5727、5744行必要LP精确最优值',kind='exact-finite-necessary-LP-optima',truth_status='finite',model=model+'本对象仅研究固定16hist、4849列、非负有理质量的明示必要系统；母矩阵含OPT单换行，比较六元组取最优。',
 statement='以5692行原点及母矩阵为起点，合并三冻结包24个不同向量得5716行精确最优W≈0.4900905644294647；再加6折扣/portfolio和5共享PAIR行得5727行W≈0.4901508813179543；再加16更早源PAIR和1单步portfolio得5744行W≈0.4908340074462763。正文给全部精确大分数、原始可行点及匹配非负有理对偶，所有行/列标准库复核通过。各轮新增正对偶支撑分别2、4、3条，故相应5694、5720、5730子系统有同样最优。全部16可用hist均d=1，纯静态OPT替换在该支持自动成立。',
 quantifiers='仅所绑定SHA的三个完整有限有理矩阵及其全部非负列质量；不是对所有客户型或所有完整SPE量化的福利常数。',
 assumptions=['列描述符、O归一向量和W目标在三轮完全相同','新增行使用已证明的同源真实IC预算并由Main独立全列重建','各轮原始/对偶证书绑定具体矩阵和点SHA；W相同不替代隐藏完成一致'],
 scope='证明这三个有限必要LP的准确最优值及其小于1/2；确认旧具体点被合法缺行排除后可改隐藏质量继续可行。',
 objections='无共同目录、全部新主题联合会员或全有序历史策略实现；有理质量整数化不补SPE。固定支持达到half也不自动证明一般题；零对偶权不表示全域逻辑冗余。')
current=json.loads((R/'research/registry.json').read_text())
old_ids={o['object_id'] for o in current['objects']}
assert not old_ids.intersection(o['object_id'] for o in objects),'New-object increment already applied; do not duplicate'
mat={m['path']:dict(m) for m in current['materials']}
changed={}
for o in objects:
 for refobj,isbody in [(o['body'],True)]+[(r,False) for r in o['evidence']]:
  p=refobj['path'];row=mat.get(p)
  if row:
   assert row['sha256']==refobj['sha256'],p
   assert row['disposition'] in ('objects','attachment'),p
   row={**row,'object_ids':list(row['object_ids'])}
   if o['object_id'] not in row['object_ids']:row['object_ids'].append(o['object_id'])
  else:
   row={**refobj,'disposition':'objects' if isbody else 'attachment','object_ids':[o['object_id']],'reason':'Boss2实读并核对的同源跨枝/折扣闭包及有限必要LP证据；具体范围由对象正文限定。'}
  if isbody:row['disposition']='objects'
  mat[p]=row;changed[p]=row
out={**current,'objects':current['objects']+objects,'materials':list(mat.values())}
delta={'schema':2,'base_registry':ref('research/registry.json'),'objects':objects,'materials':list(changed.values()),'edge_files':[],'scope':'Boss2 reviewed research increment; existing object identities and records unchanged.'}
(B/'registration-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n')
(B/'registration-candidate.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_objects':len(objects),'touched_materials':len(changed),'candidate_objects':len(out['objects']),'base_sha256':delta['base_registry']['sha256']},ensure_ascii=False))
