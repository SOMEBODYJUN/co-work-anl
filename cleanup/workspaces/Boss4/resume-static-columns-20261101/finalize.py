from pathlib import Path
import json,hashlib,re,ast
import yaml
stage=Path('.').resolve(); repo=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
e=stage/'archives/customer-attraction/subarchives/six-providers/tools/evidence/static-column-and-query-primary'
w=stage/'cleanup/workspaces/Boss4/resume-static-columns-20261101'
sbase='archives/customer-attraction/subarchives/six-providers/state/'
A=sbase+'引理/静态分母返回恒等式与同父双边容量--引理.md'
B=sbase+'引理/强制未来利润的真实查询投影与反向分裂--引理.md'
C=sbase+'引理/同子枝前缀利润的非负共同回推--引理.md'
D=sbase+'引理/共同覆盖者请求的逐客户联合投影--引理.md'
E=sbase+'审查/静态列与查询投影的历史审查及强菜单停界--审查.md'
objs=[A,B,C,D,E]
obj_ids={r:yaml.safe_load((stage/r).read_text().split('---',2)[1])['id'] for r in objs}
rels=[
 dict(id='sd-fixed-parent-matrix',type='identity-and-explicit-capacity',objects=[obj_ids[A]],source_ids=['71ba6b57cc3e3d8e6cb5','9c613946f6641758cb8e'],reason='SD的第一类正标签恰定义同一q；ROW与COLUMN由同矩阵逐客户计数同时成立，不能换成两个存在性证书。',scope='同Z同B，合计theta_i<=L；叶代数不需SPE'),
 dict(id='row-enables-retained-first-edge-reverse',type='derivation',objects=[obj_ids[A],obj_ids[B]],source_ids=['36b9bc7cc4211abd8d56','9c613946f6641758cb8e'],reason='ROW给r=u-P_B>=0；SD真实整行ell>=0使F>=0，删min(P_W,F)后保全部B边得非负REVERSE。',scope='同一自然context整行；方向actual到off-history，不导出付款'),
 dict(id='query-projection-fixes-synthetic-domain',type='domain-repair',objects=[obj_ids[A],obj_ids[B]],source_ids=['36b9bc7cc4211abd8d56','71ba6b57cc3e3d8e6cb5'],reason='多次强制使过去利润不是真prescribed；PROJ在相同合法历史的true query与whole-IC下非负守恒表示为current/future真利润。',scope='任意合法F，保同一sigma；未给全网吸收/共同系数'),
 dict(id='one-child-joint-prefix-stronger-than-separate-projection',type='joint-capacity-interface',objects=[obj_ids[B],obj_ids[C]],source_ids=['c51f7faac28bb42e7a8c','36b9bc7cc4211abd8d56'],reason='PROJ逐角色修域；PUSH用同W全部prefix共享b_x<=c_W给同B的合计L界，仍不得多W或旧suffix免费叠加。',scope='同B/W共有i前缀；不共享direct/第二类资金'),
 dict(id='common-coverer-projection-preserves-customer-density',type='counting-capacity',objects=[obj_ids[C],obj_ids[D]],source_ids=['71ba6b57cc3e3d8e6cb5','c51f7faac28bb42e7a8c'],reason='common-incidence请求先合并，输出common与R-new支持不交；最大密度<=L r/c_F。它扩展共同客户合计，但不含F-exclusive输入。',scope='任意两叶固定客户；无需IC，不证明所有future claim付款'),
 dict(id='three-disjoint-parent-supports',type='compatible-sum-under-support-contract',objects=[obj_ids[A],obj_ids[D]],source_ids=['71ba6b57cc3e3d8e6cb5'],reason='fresh B_l\\C、own-intersection B_l∩S_l、static-new (C∩B_l)\\S_l两两不交，密度各<=L才可共同占L u_l(B)。',scope='固定B、持续逐客户支持；whole-profit重采尚未保持'),
 dict(id='price-does-not-transfer-hit',type='non-implication',objects=[obj_ids[B],'customer-attraction/net-coupon-global-role-hitting-and-fresh-source-suffix-bounds'],source_ids=['36b9bc7cc4211abd8d56'],reason='原HIT使用current actual终点值0；PROJ current为另natural续节点。抽象两层各二元uniform-subset可给目标3/4，只反仅凭局部合同的继承，不声称真实CAG反例。',scope='区分局部PRICE与最终HIT；未更新共享图'),
 dict(id='coordinate-initialization-is-related-not-free-global-capacity',type='comparison',objects=[obj_ids[A],'customer-attraction/full-client-coordinate-inventory-two-budget-initialization'],source_ids=['09e88a6b11f6264a6a83'],reason='共享静态分母/coverer列计数，但初始化reference=T且已有两预算和未付future，与本SD direct/不同W债非同一资金。',scope='不将旧RAW-cap升级为后加强密度合同'),
 dict(id='bank-updates-readme-open-status',type='later-counterexample-updates-historical-scope',objects=[obj_ids[E],'customer-attraction/cartesian-bank-full-root-menu-low-value-symmetric-nash-failure'],source_ids=['09e88a6b11f6264a6a83'],reason='四人完整零根银行给Mfull=59/36>u=4/3、B4=19/14；反一般Mfull/extra-one而非half，更新round7原OPEN。',scope='保根完整r槽；不从任意背景外推')
]
(e/'relations.json').write_text(json.dumps(dict(status='human-reviewed-relationship-notes-for-later-mapping;no-shared-map-written',relations=rels),ensure_ascii=False,indent=2)+'\n')
(e/'README.md').write_text('''# 静态分母、同父列与真实查询投影证据

五主源37731B全部为Markdown，已正常clean show逐字全文取得；原字节在original按完整冻结路径保存，原show回执在acquisition，source-manifest.json保两冻结提交、SHA256、Git blob、owner及原进度身份。source-fingerprints.json用纯字节核size/SHA/blob，不运行数学。

十份related也经本次normal clean show完整实读，comparison-manifest.json与comparison保各原件；不替其owner认领或done。包括4内部审查/父审、fresh因果稿、强pair范围稿、两份完整菜单原稿以及3355B对角菜单程序和10478B原报告。程序报告只读，不启动main，不重做已停止强候选测试。

八份当前正式对象全文比较并快照在formal-comparison，逐份hash见formal-comparison-manifest.json。它们给模型、SAFE、HIT/source-time、坐标初始化、平均D比较反例、强聚合非空填充、银行Mfull反例与extra-one状态校正。

四自足引理和一审查对象在../../../state/的相应类别。所有量词/静态叶与真SPE域/原审查读序/当前知情整理分开。SD、COLUMN、PROJ、PUSH和共同客户密度为局部已证组件；不同孩子、旧请求、direct与第二类、环和whole-profit重采的共同actual容量均未证，六人half未闭合。

原数学入口/收益IC重算/搜索/solver调用均0。本次只做全文比较、解析逐式重构、指纹/AST/YAML/链接静态自查。未从父审另一348客户脚本的历史说明冒领当前执行，也未把六份旧有限pass当一般强桥证据。

relations.json是已有人判断的关系及条件备忘，未改共享map/总目录。语义receipt、delivery和copy-manifest由Root串行落地及checkpoint/done；此目录本身不声称已推送或勾选。
''')
(e/'REVIEW.md').write_text('''# 当前实质核读

逐式重推SD两段倒数差；按same-Z发送者数与d_i>=c_B核COLUMN，按新增B coverer数<=d_i-1核同q的ROW，分别common/actual-only得到精确密度。全文自查时将theta全1等号的L说明补为theta_i=L取上界等号，L1是原exact特例；无新增数学实验。

PROJ的d-N=(1+共同其它coverer)/(c_F c_R)>0，未来边只在l>j；current whole-IC在原history，alpha<=1。其PRICE只描述一层，原GLOBAL-HIT的current终点假设不成立。保B边REVERSE先用ROW留P_B，r=v+P_W-F分r>=v/r<=v两例，不需要F<=v，不另领退款。方向保actual到off-history。

PUSH的refund按共同coverer数非负，共享prefix b<=c_W一次给全部prefix的同父列界；矩阵列次随机而非行概率。源稿非减价格式方向已重推，ancestry栈只提供一次域修复有限；两个独审叶例显式阻已有suffix或多孩子免费叠加。COMMON-PROJ只接common incidences，输出密度r/c_F，F-exclusive与新客户显式留外。

README全部导航、旧强D>=C/pair阴性测试、34/348旧证据和后来的真正空根银行状态逐一比较；average D、actual u、Mfull、全路径预算、half没有互相冒用。当前没有外审、新颖性、独立盲审重演、福利证明或新实例发现。
''')
readnotes={
'09e88a6b11f6264a6a83':'全文4094B：六项导航逐项辨识fresh-source因果、最优坐标初始化、固定B列、单孩子prefix、query-projection/反向核；读取强全菜单六证书测试停止及34客户D<C、348客户pair、任意背景PB三种停界和后续未付义务。',
'9c613946f6641758cb8e':'全文5515B：固定同Z同B及不同W_i、全部来源合计theta_i<=L；q^B支持、共同COLUMN、精确density、同q严格ROW、空域/零分母；与prefix差别、direct/第二类/旧请求/跨B禁叠及restricted profit不能替ell。',
'36b9bc7cc4211abd8d56':'全文9922B六节：原合同后未读证明的历史重构；SD两段、两类边利润域、一次reset/多强制closure；任意synthetic PROJ、current/future真context及守恒；PRICE/源时间与两层抽象3/4阻HIT继承；保B边REVERSE取消和方向/循环限制。',
'c51f7faac28bb42e7a8c':'全文6728B：同一B/W共同前缀、q+/q-与safe refund、共享b_x<=c_W列、零利润比值、列次随机PUSH、非减价格/后缀利润、递增强制栈一次有限域修复；多孩子/旧suffix/重入循环边界。',
'71ba6b57cc3e3d8e6cb5':'全文11472B八节：真实返回whole-IC与静态d，SD/EXCESS和两类份额；单reset/强制位置集域；PROJ及共同支付未付；COMMON-PROJ common-incidence联合密度、exclusive限制；STATIC-CAP精确密度和fresh/own/static三块不交支持。'}
comparisons={
'09e88a6b11f6264a6a83':'全仓检索后全文读10 related（manifest列全ID）和8当前formal：fresh后缀定理已吸收源时间；坐标初始化原RAW-cap不能混本SD；读3355B/10478B强菜单六例原程序/全字段，34根D<C、348pair/任意背景PB量词分开。后来银行完整零根已反Mfull/extra-one，原OPEN按历史保存。无重复运行。',
'9c613946f6641758cb8e':'全文比较global主稿§8、coupling SD主审、related root reverse审查及independent fixed-parent审查；重推common/actual-only两分母、同q ROW/COLUMN。与已有坐标初始化的reference=T域及已付预算不同；共同客户输入/旧请求须另守同一支持。',
'36b9bc7cc4211abd8d56':'全文比较global SD主稿、fixed-column主稿、root reverse相关原文；与SAFE和HIT正式对象核current终点差异，故不把局部PRICE移成HIT/吸收。与prefix原稿/两份相关审查核单角色PROJ和同孩子joint cap不同。历史内审不冒当前盲审。',
'c51f7faac28bb42e7a8c':'全文读related coupling blind transfer、independent prefix与root reverse；其RET/COLUMN/零分母校正一致，独审给已有suffix/多child的具体SPE叶边界及H-overlap/MARG可选域。与source-time非增价格及common-incidence投影分别保方向/输入合同。',
'71ba6b57cc3e3d8e6cb5':'全文比较三其它数学主源、root/independent相关审查及8 formal；SD完整IC与已有SAFE方向/分母不同，STATIC-CAP与坐标初始化只共享计数机制；PROJ current不满足旧HIT终点；common-only与exclusive/new-client支持明确分开，未找到已有正式同SD对象。'}
targets={
'09e88a6b11f6264a6a83':[E],
'9c613946f6641758cb8e':[A,E],
'36b9bc7cc4211abd8d56':[A,B,E],
'c51f7faac28bb42e7a8c':[C,E],
'71ba6b57cc3e3d8e6cb5':[A,B,D,E]}
decisions={
'09e88a6b11f6264a6a83':'integrated：导航不是独立福利定理，但原审查/接续先验、已停止测试真实有限域和三失败桥身份有独有内容；审查对象完整保导航并更新后来银行状态。相关未领取源仅旁读，不重复done。',
'9c613946f6641758cb8e':'integrated：显式同q双边运输及精确余量独有，解析证明自足保存；只控制第一类同B合计列，保严格ROW/空域和共同系数守卫，不升级为整网actual cap。',
'36b9bc7cc4211abd8d56':'integrated：独有synthetic真query域修复、局部PRICE不能直接继承HIT及保B边REVERSE完整保存；原先读合同后重构历史另记。局部非负守恒不冒吸收、实际付款或half。',
'c51f7faac28bb42e7a8c':'integrated：单W整组prefix无穷范数不增、价格及有限ancestry域修复完整保留，原证明无需SPE处明确；多W/旧suffix免费叠加不能由合同推出，不把未付当退休。',
'71ba6b57cc3e3d8e6cb5':'integrated：SD整行ell有利项及真实后继、强制域、COMMON-PROJ和STATIC三块支持全部进入自足正文；普遍局部真式与全图未闭容量分开，保全原件/具体来源关系。'}
receipts=[dict(id=sid,full_file_reviewed=True,related_material_checked=True,unique_content_accounted_for=True,read_note=readnotes[sid],comparison_note=comparisons[sid],decision_note=decisions[sid],disposition='integrated',targets=targets[sid]) for sid in readnotes]
(w/'semantic-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
# Exact next candidate IDs are recommendations only; no claim is attempted.
inv={x['id']:x for x in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())}
nexts=[dict(id=x['id'],path=x['path'],size=x['size'],sha256=x['sha256'],reason='Root所建议R44 saved/warm程序及冻结报告；待Root正式claim后完整实质清洗，不在本批done。') for x in inv.values() if '/true_counterexample/' in x['path'] and Path(x['path']).name in ['audit_saved_policies.py','audit_warm_start.py','saved_policy_audit.json','warm_seed_audit.json']]
(w/'next-candidates.json').write_text(json.dumps(nexts,ensure_ascii=False,indent=2)+'\n')
# Static QA only: fingerprints, YAML, local links with staged overlay, JSON, Python parsing.
qa=dict(mathematical_entry_runs=0,original_program_imports=0,payoff_or_ic_replays=0,solver_or_search_runs=0,git_mutations=0,clean_state_mutations=0,formal_objects=[],broken_links=[],source_fingerprint_files=15)
for rel in objs:
 p=stage/rel; s=p.read_text(); meta=yaml.safe_load(s.split('---',2)[1]); assert all(k in meta for k in ['id','kind','type_tag','title','status','summary','source_refs'])
 assert s.count('\\[')==s.count('\\]')
 for link in re.findall(r'\]\(([^)]+)\)',s):
  if link.startswith(('http:','https:','#')):continue
  target=link.split('#')[0]; resolved=(p.parent/target).resolve(); reltarget=resolved.relative_to(stage)
  if not resolved.exists() and not (repo/reltarget).exists():qa['broken_links'].append(dict(source=rel,target=link))
 qa['formal_objects'].append(dict(path=rel,id=meta['id'],size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),full_final_text_read=True))
assert not qa['broken_links'],qa['broken_links']
for p in e.rglob('*.json'):json.loads(p.read_text())
for p in (w/'build.py',):ast.parse(p.read_text())
qa['validation']='passed-static-only;not-a-mathematical-or-publication-certificate'
(e/'static-self-check.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
(w/'SELF-CHECK.md').write_text('''# 完整性和静态自查

五主源37731B、十related源按size/SHA256/Git blob核同，全文原件保全；八当前formal全读及快照有hash。五份最终正文逐字全文回读，frontmatter/稳定ID/精确source引用、数学显示括号、overlay相对链接、JSON及build语法静态核均通过。唯一回读修订是精确密度上界等号明确theta_i=L（theta1/L1是特例），不靠运行验证数学。

解析自查覆盖SD符号/真实W、零分母、fixed B合计theta、同q双边、PROJ真history/未来支持、PRICE与HIT差别、reverse方向/退款一次、prefix列而非行合同、价格方向、common-only域、强D/actual u/Mfull/half逻辑和历史状态。未发现未处置主源内容。

0数学入口、0原import、0IC/收益复跑、0solver/扫描、0Git或clean状态变更。只在指定独立新文件写入；Root协调后所有进一步写入转clone外stage。没有claim/done/checkpoint或共享map/总目录变动。
''')
delivery=dict(status='ready-for-root-copy-checkpoint-and-done;not-yet-published-by-this-agent',stage_root=str(stage),repo_root=str(repo),source_ids=list(readnotes),primary_source_count=5,primary_source_bytes=37731,related_frozen_source_count=10,current_formal_full_comparisons=8,formal_targets=objs,object_ids=list(obj_ids.values()),semantic_receipts='cleanup/workspaces/Boss4/resume-static-columns-20261101/semantic-receipts.json',evidence_root=str(e.relative_to(stage)),new_mathematical_runs=0,new_original_program_runs=0,git_mutations=0,cleanup_state_mutations=0,mathematical_result='四个任意人数局部引理/接口及一历史审查；没有新的共同福利界，六人half未闭合。',root_actions='复制copy-manifest所列stage文件到repo同相对路径（覆盖本线旧副本以纳入density wording修订）；Root串行checkpoint后按semantic-receipts做done；不计related源为本批done。',next_candidates='cleanup/workspaces/Boss4/resume-static-columns-20261101/next-candidates.json',material_limits=['同B第一类容量不含direct/第二类/旧请求/多B总和','PROJ current为续context，HIT/吸收须重证','PUSH仅一孩子，common-projection仅common incidences','原README的Mfull/extra-one OPEN已按银行后续反例校正','原六例JSON保历史有限阴性，没有新执行绑定'])
(w/'delivery.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n')
# The transport manifest deliberately excludes itself.
files=[dict(path=str(p.relative_to(stage)),size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(stage.rglob('*')) if p.is_file() and p.name!='copy-manifest.json']
(w/'copy-manifest.json').write_text(json.dumps(dict(stage_root=str(stage),files=files,copy_policy='exact staged files to same repo-relative paths; no unrelated deletions; no credential files'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status='ready',objects=5,receipts=5,stage_files=len(files)+1,primary_bytes=37731,related=10,current_formal=8,broken_links=0,next_candidates=len(nexts)),ensure_ascii=False))
