from pathlib import Path
import hashlib,json,ast,re,shutil
import yaml
stage=Path('.').resolve();repo=Path('/workspace/scratch/37f0f9248cfc/boss4-resume-20261101');e=stage/'archives/customer-attraction/subarchives/six-providers/tools/evidence/common-terminal-exchange-primary';w=stage/'cleanup/workspaces/Boss4/resume-common-terminal-exchange-20261101'
base='archives/customer-attraction/subarchives/six-providers/state/'
A=base+'引理/共同终局交换与负载匹配的条件福利证书--引理.md';B=base+'障碍/共享终局多惩罚扩张的外组末位门槛--障碍.md';C=base+'资源/共同终局局部审计与碰撞自由联合锥的有限记录--资源.md';D=base+'审查/共同终局交换的读后重构与负载推广范围--审查.md';objs=[A,B,C,D]
# Source code does not call resolve() on this local-audit output path.
for p in [stage/C,w/'build.py']:
 s=p.read_text();p.write_text(s.replace('及绝对output路径','及其计算的邻接output路径'))
fingerprints=[]
for manifest,folder in [('source-manifest.json','original'),('comparison-manifest.json','comparison'),('runtime-dependency-manifest.json','original')]:
 for x in json.loads((e/manifest).read_text()):
  p=e/folder/x['path'];b=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  assert len(b)==x['size'] and hashlib.sha256(b).hexdigest()==x['sha256'] and blob==x['blob'],x['id']
  fingerprints.append(dict(id=x['id'],role=manifest,path=str(p.relative_to(stage)),size=len(b),sha256=x['sha256'],blob=blob))
(e/'source-fingerprints.json').write_text(json.dumps(fingerprints,ensure_ascii=False,indent=2)+'\n')
formal=['archives/customer-attraction/state/反例/三人碰撞自由族福利障碍--反例.md','archives/customer-attraction/state/计算/固定策略锥精确证书与重放--计算.md','archives/customer-attraction/state/引理/同终局近包含差集罚金的全深度追随下界--引理.md','archives/customer-attraction/state/引理/共同末位报价与隐藏回复投影--引理.md','archives/customer-attraction/state/引理/真实后继利润与共同末价的离散下包络--引理.md']
fm=[]
for rel in formal:
 dst=e/'formal-comparison'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(repo/rel,dst);b=dst.read_bytes();fm.append(dict(path=rel,full_file_reviewed=True,size=len(b),sha256=hashlib.sha256(b).hexdigest()))
(e/'formal-comparison-manifest.json').write_text(json.dumps(fm,ensure_ascii=False,indent=2)+'\n')
ids={r:yaml.safe_load((stage/r).read_text().split('---',2)[1])['id'] for r in objs}
relations=[
 dict(id='same-terminal-to-load-matching',type='joint-real-IC-derivation',objects=[ids[A]],source_ids=['ac8556aa858004c9c7dd','5babe33fcadabc3f17fe'],evidence='同sigma早偏离IC+同b同q利润相等+具体g末位BR；LOAD逐客户比较后匹配各行一次相加。',conditions='完美匹配、合法扩张主题及最优遗漏覆盖均额外承重；不推普遍存在'),
 dict(id='exchange-blocks-many-punisher-lift',type='template-obstruction-derivation',objects=[ids[A],ids[B]],source_ids=['ac8556aa858004c9c7dd'],evidence='A_i枝末B与早B枝同完整多重集，外组仅C_h给x_i>=x_h/2+a_h；k>=2无不动点置换给sum a<=sum x/2。',conditions='惩罚主题只触本组/储备；3/2比率还要比较组合全覆盖；k1未涵盖'),
 dict(id='literal-audit-only-implements-obstruction-formulas',type='finite-implementation-not-universal-proof',objects=[ids[B],ids[C]],source_ids=['ce80d82078657ab1c96f','de7d2ca3a52fabb5df32'],evidence='t2..8,k2/3的Counter/末位收益与352标量；14cases/56外组行字段完整保全，没有完整sigma或全IC。',conditions='程序未启动；历史JSON无当前运行绑定；t2 bool不是全树认证'),
 dict(id='single-punisher-family-not-universal-upper-bound',type='comparison-and-template-generalization-boundary',objects=[ids[B],'customer-attraction/collision-free-family-welfare-obstruction'],source_ids=['ac8556aa858004c9c7dd'],evidence='旧x2/a1/q1完整Q/B归纳给存在型OPT/W趋3/2；本多惩罚literal t>2末位失败，不能冒另有效SPE。',conditions='不授任意碰撞自由SPE<=3/2，不否half'),
 dict(id='same-terminal-near-containment-distinct-interface',type='comparison',objects=[ids[A],'cag-same-terminal-near-containment-difference-penalty-full-depth-floor'],source_ids=['ac8556aa858004c9c7dd'],evidence='两者均用单位客户同终局份额；旧页同一个偏离叶不同主题用U\\T罚金，本页两个真节点同主题同q转末位BR。',conditions='不可用另一SPE可实现计数或任意叶置换替本见证'),
 dict(id='joint-milp-proposes-exact-cone-endpoints',type='implementation-and-evidence-boundary',objects=[ids[C],'customer-attraction/strategy-cone-exact-evidence'],source_ids=['0f2ae6c9b2f95ee9a3ca','a9f9cb78fe45cbe23cbe'],evidence='在同canonical joint/LP上加collisionfree零类型及metadata guard；浮点只提动作图，Fraction完整IC和规范verifier才能认证端点。',conditions='m4无候选，m3一个ratio1点，无全局/固定锥最优对偶；无新run'),
 dict(id='parent-read-after-source-and-load-extension',type='historical-review-and-extension',objects=[ids[A],ids[D]],source_ids=['5babe33fcadabc3f17fe','ac8556aa858004c9c7dd'],evidence='父审先读作者再定义重构，独立提出可拥挤LOAD版；作者吸收推广。',conditions='非盲审/外审/新颖性认证，当前清洗知情')]
(e/'relations.json').write_text(json.dumps(dict(status='human-reviewed-relations;shared-map-not-written',relations=relations),ensure_ascii=False,indent=2)+'\n')
(e/'README.md').write_text('''# 共同终局交换、条件负载匹配与多惩罚失败模板证据

六primary原字节34957B保于original完整冻结路径，source-manifest.json有两来源提交/路径/SHA/blob；acquisition保存本次normal-show和新clone六条owner进度。Root正式claim21 pushed 8a85c0dc0392c613b5a1f744f3ef715f5a325389，agent只读与外部stage写。

comparison保存四份正常show相关源：R486 credible README和m3p6完整JSON，以及canonical joint MILP和固定策略LP完整源码。runtime-dependency-manifest说明七依赖按原树保于original（joint/LP两源与related重叠），其余由已发布strategy-cones同SHA复用。当前全文读joint/LP和__init__/model/certificate；exact/credible_variants仅依赖保全/既有清洗资源引用，不冒本次全文审查或done。所有17份源副本、15个不同源ID均核size/SHA/Git blob。

五份当前正式数学对象全文比较并快照于formal-comparison。它们保既有完整碰撞自由3/2下界族、固定策略锥证据、同叶近包含与末位报价的独立合同。新四对象在../../../state/：同终局交换/条件匹配、共享终局多惩罚障碍、双程序有限记录和父审读序。

本次原main/import/收益或IC重算/solver/MILP/扫描均0；只全文理解、解析重推和静态JSON/AST/YAML/链接/指纹检查。六主源无同SHA新执行绑定，冻结报告按历史记录保留；没有为了重造PASS跑已低信息/已失败搜索。局部352/14/56不是完整SPE认证；m3端点只是比率1可行点；m4 metadata失败为null结论，修后当前代码不冒前版执行。

运行原程序前应将original完整树复制到另一个独立目录；局部audit会覆盖邻接JSON，collisionfree --out会覆盖目标。此处不执行原件，不将原程序提供给当前用户自动长时搜索。必要运行环境为Python、NumPy、SciPy；完整有序策略和字节指纹均保留。

relations.json为已人工斟酌的身份/条件推导/模板障碍/实现/审查关系，没有改共享map或总目录。delivery、六条semantic receipts与copy-manifest由Root串行落地、checkpoint后再done，本agent不声称发布或勾选。
''')
(e/'REVIEW.md').write_text('''# 实质自查

共同终局行逐个核两条真比较与同主题同计数等号，g须具体属于同sigma；LOAD保alpha0/空集，匹配仅选行一次，OPT-W保I/G差值并用遗漏覆盖。多惩罚OUTSIDE依外组负载1/0和same multiset，k>=2 derangement不可删除；比率3/2还承重全覆盖。literal t>2 actual-last和punishment-last均盈利，t2局部等号不冒全树证书。

两程序职责分开。局部脚本只造14组显式终局/56行及352条件标量，不建sigma。碰撞自由wrapper在当前canonical function用两次源码replace再exec定义；当前guard已修，失败JSON属于前过程说明。MILP输出不是数学上界，后固定cone的精确端点不认证锥最优；objective和实际OPT/W保不同量。m3 singleton完整表可按全新标签性质人工作直接解析核对，但无新程序IC复跑。

冻结JSON根/case/row字段、全部14行数值、bool比较域和m4 null结论已逐字读。父审先读作者后的重构与root负载推广先验分开；未伪称盲审/外审。全仓精确名/代码SHA检索未见本wrapper或local audit已有同SHA新执行记录，未据缺记录而重复低信息实验。source-fingerprints仅字节检查，static-self-check仅结构/链接，不替数学判断。
''')
read={
'a9f9cb78fe45cbe23cbe':'全文552B、5根字段及5参数：m4/p7/70秒/path0..3/portfolio3..6；记录MILP后float(None)导致无report/action graph，guard修复且未重跑，mathematical_conclusion为null。',
'0f2ae6c9b2f95ee9a3ca':'全文3094B；parents5原根、imports、inspect源码两替换与exec、CLI、唯一根路径/portfolio、MILP后固定锥LP、Fraction恢复/零类型约束/整数clone/两路完整IC、OPT枚举、报告覆盖写及stdout。',
'de7d2ca3a52fabb5df32':'全文14679B：3根字段352和14case；每case11字段、t2..8/k2,3的所有客户/W/OPT/末位/布尔；全部56个有序i!=h行、每行6字段原Fraction字符串均完整读取。',
'ce80d82078657ab1c96f':'全文2950B标准库局部审计；显式tuple单位客户/合法目录、actual/静态比较union、两枝Counter及last/early/outside收益、352条件标量网格、main邻接JSON覆盖和stdout；没有完整策略或SPE搜索。',
'ac8556aa858004c9c7dd':'全文10228B五节：同sigma两真节点same b/q交换、含拥挤的LOAD完美匹配与遗漏覆盖、k>=2任意q异质奖励交叠多惩罚门槛、literal t>2两次末位失败、有限两搜索/修复和root推广历史。',
'5babe33fcadabc3f17fe':'全文3454B：root先读作者后定义重构（明确非盲），同b/q真收益转移、多惩罚derangement，独立提出c*负载推广及E重叠/alpha0/空I/零W边界，匹配存在和遗漏覆盖仍未证。'}
comp={
'a9f9cb78fe45cbe23cbe':'与当前collisionfree wrapper及canonical joint全文核metadata guard前后；相关README/m3完整报告只另有ratio1点。无动作图的失败不并入候选或数值上界，未重跑。',
'0f2ae6c9b2f95ee9a3ca':'全文读canonical joint7637B和固定LP20567B；与已清洗策略锥资源核浮点/精确层、有效M、全有序域；规范model/certificate全文核端点验证/OPT接口；同SHA依赖复用，m3/m4报告分开。',
'de7d2ca3a52fabb5df32':'与主audit每字段构造、主数学literal公式及父审全文对账；352只满足前件点，14case/56行非全树IC，BestReply bool仅比较A0；m3真策略JSON不是本局部报告。',
'ce80d82078657ab1c96f':'与14679B报告及数学主稿/父审全文核14/56/352范围；原单惩罚无限族另有完整Q/B归纳，不能借局部t2pass认证所有k或修t>2。未运行脚本覆盖原输出。',
'ac8556aa858004c9c7dd':'全仓精确终局/负载关键词及代码SHA检索后，全文比较五formal：既有collisionfree完整族、近包含同叶罚金、共同末位报价/后继下包络、策略锥资源。新same-terminal跨真节点与条件matching不等于旧罚金递归或全局上界，未发现后来已证普遍matching。',
'5babe33fcadabc3f17fe':'对主稿§1-4逐步重构和扩域，保root先读作者后审及独立建议推广时间；对现formal区别存在型3/2构造、同叶追随、条件匹配和任意SPE/六人half。原内审不冒当前盲审。'}
target={
'a9f9cb78fe45cbe23cbe':[C], '0f2ae6c9b2f95ee9a3ca':[C], 'de7d2ca3a52fabb5df32':[B,C], 'ce80d82078657ab1c96f':[B,C], 'ac8556aa858004c9c7dd':[A,B,C,D], '5babe33fcadabc3f17fe':[A,D]}
reason={
'a9f9cb78fe45cbe23cbe':'retained：无数学端点但保准确失败参数/缺失action graph/metadata guard修复且未重复的可接续运行史；资源解释null结论并保原件，不伪造上界。',
'0f2ae6c9b2f95ee9a3ca':'integrated：保完整可复用有限candidate算法、原根/依赖/CLI/碰撞自由类型及真全历史核验合同；低信息原attempts保范围，不把程序或超时升普遍结果。',
'de7d2ca3a52fabb5df32':'integrated：保全所有字段及有限公式数据，资源完整表述何者是局部pass/明确末位失败，原JSON不冒当前运行绑定；一般证明由解析障碍承担。',
'ce80d82078657ab1c96f':'integrated：标准库逐客户构造与Counter/倒数检查独有实现保于证据及资源，程序能重算局部模板但无完整sigma；无须重复已有局部算术报告。',
'ac8556aa858004c9c7dd':'integrated：拆自足交换/条件负载matching与共享终局多punisher障碍，保每项承重见证/全覆盖/范围边界，原有限实现/历史接续进资源；未完成普遍匹配不退休。',
'5babe33fcadabc3f17fe':'integrated：独有原审查读序及root拥挤推广身份进审查和条件引理；解析核通过但不冒外审/新颖性/普遍half。'}
receipts=[dict(id=s,full_file_reviewed=True,related_material_checked=True,unique_content_accounted_for=True,read_note=read[s],comparison_note=comp[s],decision_note=reason[s],disposition='retained' if s.startswith('a9f9') else 'integrated',targets=target[s]) for s in read]
(w/'semantic-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
# Structure-only report reading; no utility, IC, scalar audit or solver execution.
pref=e/'original/research/workspaces/customer-attraction/R-486bb9adb8cd4d9a940dbf3b1ab0b1de/credible'
r=json.loads((pref/'common_terminal_audit.json').read_text());assert len(r['cases'])==14 and all(len(x)==11 for x in r['cases']);assert sum(len(x['common_terminal_comparisons']) for x in r['cases'])==56
q=json.loads((e/'comparison/research/workspaces/customer-attraction/R-486bb9adb8cd4d9a940dbf3b1ab0b1de/credible/cf_m3p6.json').read_text());policy=q['exact_endpoint']['strategy']['actions'];assert len(policy)==43;assert len({tuple(x['history']) for x in policy})==43;assert all(x['action'] not in x['history'] for x in policy)
qa=dict(status='passed-static-only;not-a-mathematical-run-or-publication',primary_source_count=6,primary_source_bytes=34957,frozen_copies=len(fingerprints),unique_frozen_ids=len({x['id'] for x in fingerprints}),formal_objects=[],broken_links=[],mathematical_entry_runs=0,original_imports=0,payoff_or_ic_replays=0,solver_milp_search_runs=0,git_mutations=0,clean_mutations=0,structural_report_reading=dict(cases=14,common_terminal_rows=56,cf_m3_policy_rows=43,all_policy_actions_fresh=True))
for rel in objs:
 p=stage/rel;s=p.read_text();m=yaml.safe_load(s.split('---',2)[1]);assert all(k in m for k in ['id','kind','type_tag','title','status','summary','source_refs']);assert s.count('\\[')==s.count('\\]')
 for link in re.findall(r'\]\(([^)]+)\)',s):
  if link.startswith(('https:','http:','#')):continue
  dst=(p.parent/link.split('#')[0]).resolve();dr=dst.relative_to(stage)
  if not dst.exists() and not (repo/dr).exists():qa['broken_links'].append(dict(source=rel,target=link))
 qa['formal_objects'].append(dict(path=rel,id=m['id'],size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),full_final_text_read=True))
assert not qa['broken_links'],qa['broken_links']
for p in e.rglob('*.json'):json.loads(p.read_text())
for p in list(e.rglob('*.py'))+[w/'build.py']:ast.parse(p.read_text())
(e/'static-self-check.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
(w/'SELF-CHECK.md').write_text('''# 自查交付

六primary34957B、4正常show related和7runtime副本的size/SHA/blob全核同，共15不同源ID。五formal全文快照。四最终正文已全文回读，模型/量词/alpha0/I空/零W/k1边界、shared terminal/full-cover假设、代码/报告区别、父审先验逐项核对。改正正文case字段数量为11、runtime/related去重说明、未resolve的output路径措辞；未改原字节。

静态JSON结构解析给14cases/56比较行、m3policy43不同历史且各动作未用；这只核原表结构，数学结论由正文解析论证或原报告身份承担，不调用payoff/IC/solver。YAML/稳定ID/源引用/显示数学括号/overlay链接/AST均通过。没有Git、clean mutation、shared map或目录写。所有文件只在common-terminal-exchange-stage。

0原main、0import、0收益/IC复跑、0MILP/LP/搜索。失败和低信息历史尝试未重复，原guard前版没有伪造源码绑定。局部真引理/模板障碍/有限证据均不关闭六人half或普遍匹配。
''')
inv={x['id']:x for x in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())}
nexts=[]
for sid in ['f51dcc0ad5619beb9b24','0b3a5a7ce66b26314f44']:
 x=inv[sid];pp=repo/'cleanup/progress'/f'{sid}.json';progress=json.loads(pp.read_text()) if pp.exists() else None
 nexts.append(dict(id=sid,path=x['path'],sha256=x['sha256'],current_local_progress=progress,reason='本批已正常show全文旁读且保原件；如尚未primary清洗，可由Root按实际状态正式claim独立处理，不重复已done项。'))
(w/'next-candidates.json').write_text(json.dumps(nexts,ensure_ascii=False,indent=2)+'\n')
delivery=dict(status='ready-for-root-copy-checkpoint-and-done;not-published-by-this-agent',stage_root=str(stage),repo_root=str(repo),primary_source_ids=list(read),primary_bytes=34957,primary_count=6,formal_targets=objs,formal_object_count=4,related_normal_show_count=4,runtime_dependencies=7,unique_related_and_runtime_ids=9,current_formal_full_comparisons=5,receipts='cleanup/workspaces/Boss4/resume-common-terminal-exchange-20261101/semantic-receipts.json',evidence_root=str(e.relative_to(stage)),new_mathematical_runs=0,new_original_program_runs=0,git_mutations=0,clean_state_mutations=0,source_claim_commit='8a85c0dc0392c613b5a1f744f3ef715f5a325389',root_action='Copy manifest exact staged paths into new repo only, checkpoint math/evidence first, then six receipts done; related/runtime sources not additional done.',result='完整局部交换和条件拥挤matching证书、共享终局多惩罚解析障碍、两程序/冻结有限输出范围与父审读序；未增一般福利界或half反例。',material_limits=['完美匹配/LOAD/最优漏集覆盖并未普遍保证','多惩罚3/2模板比率还需full-cover，k1未涵盖','14局部cases不是完整SPE；BestReply布尔只比较A0','m4没有图或证书；m3只ratio1可行点，无最优上界','当前guard已修，失败报告不绑定当前字节执行','exact.py/credible_variants依赖只复用已清洗原字节，不冒本轮全文审查'])
(w/'delivery.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n')
files=[dict(path=str(p.relative_to(stage)),size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(stage.rglob('*')) if p.is_file() and p.name!='copy-manifest.json']
(w/'copy-manifest.json').write_text(json.dumps(dict(stage_root=str(stage),files=files,copy_policy='same relative paths to new repo; do not delete unrelated files; copy manifest itself separately'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status='ready',formal_objects=4,receipts=6,stage_files=len(files)+1,primary_bytes=34957,unique_frozen_ids=15,broken_links=0),ensure_ascii=False))
