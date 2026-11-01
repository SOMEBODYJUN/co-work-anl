from pathlib import Path
import ast,hashlib,json,re
repo=Path('.')
work=repo/'cleanup/workspaces/Boss4/resume-harmonic-audits-20261101'
base=repo/'archives/customer-attraction/subarchives/six-providers/tools/evidence/harmonic-independent-primary'
resource='archives/customer-attraction/subarchives/six-providers/state/资源/父方调和菜单两原审计与冻结报告--资源.md'
review='archives/customer-attraction/subarchives/six-providers/state/审查/调和菜单独审的归一化与合法菜单核验范围--审查.md'
manifest=json.loads((base/'source-manifest.json').read_text())
primary={x['id']:x for x in manifest}
related_paths=[
 'archives/customer-attraction/state/定理/真实后继菜单的调和价格母式与显式债--定理.md',
 'archives/customer-attraction/state/资源/调和菜单母式的原参数审计与证书复用范围--资源.md',
 'archives/customer-attraction/state/定理/真实末两人加权分数价格包络--定理.md',
 'archives/customer-attraction/state/障碍/自适应后继与真实菜单安全值--障碍.md',
 'archives/customer-attraction/state/反例/四人总去相关的单根负差--反例.md',
 'archives/customer-attraction/state/反例/常后继菜单的调和信用与普通利润系数边界--反例.md',
 'archives/customer-attraction/tools/evidence/harmonic-tail-menu-primary/original/research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/early_price/harmonic_tail_menu_debt.md',
 'archives/customer-attraction/tools/evidence/harmonic-tail-menu-primary/original/research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/early_price/audit_harmonic_tail_menu.py',
 'archives/customer-attraction/tools/evidence/harmonic-tail-menu-primary/original/research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/early_price/harmonic_tail_menu_audit.json',
 'archives/customer-attraction/tools/evidence/continuation-security/replay-decorrelation.json']
related=[]
for name in related_paths:
 p=repo/name;b=p.read_bytes()
 related.append(dict(path=name,size=len(b),sha256=hashlib.sha256(b).hexdigest(),full_file_read=True,reader='harmonic_audits' if '四人总去相关' not in name else 'harmonic_compare',comparison_role='Related mathematical statement or historical evidence; not an additional primary completion.'))
(base/'comparison-manifest.json').write_text(json.dumps(related,ensure_ascii=False,indent=2)+'\n')
relations=[
 {'type':'review','from':['customer-attraction/harmonic-menu-parent-review-normalization-and-legal-menu-scope'],'to':['customer-attraction/all-depth-real-tail-menu-harmonic-price-identities-and-explicit-debts'],'explanation':'原父审自记先从收益重构再读母稿；V=F−aK给共同交叉项，分量展开消h时系数必须为τR+ηZ。全一般符号式已有母式定理，本对象保审查先验、独立实现与有限核验身份，不新增盲审或外审。','evidence':[primary['6fa933e36cc587485086']['sources'][0],related_paths[0]]},
 {'type':'implementation-and-finite-check','from':['customer-attraction/parent-harmonic-menu-two-original-audits-and-frozen-reports'],'to':['customer-attraction/all-depth-real-tail-menu-harmonic-price-identities-and-explicit-debts'],'explanation':'5502B实现1638阈值与280合法目录菜单/1960点；仅r2的40菜单强制末位BR，r≥3非完整SPE。3558B另从客户类型重放旧1885有序节点/22620含self比较。冻结报告各保原身份，当前未执行原入口。','evidence':[primary['a9508d5d82fc2743e7a3']['sources'][0],primary['01358becd12e98b4f96f']['sources'][0],primary['f8022194def22f79cd9c']['sources'][0],primary['1545471ca1085eada13d']['sources'][0]]},
 {'type':'specialization-with-normalization','from':['customer-attraction/all-depth-real-tail-menu-harmonic-price-identities-and-explicit-debts'],'to':['customer-attraction/parametric-weighted-two-tail-price-envelope'],'explanation':'共同背景、同一完整策略、恰一后继时Z_old=τZπ及V_old=τ²Rπ，原三IC组合即S+ηZπ+τRπ。母稿q∈[0,1]只是更宽两尾q≥0的子域；多尾不继承单人BR非负。','evidence':[related_paths[0],related_paths[2]]},
 {'type':'existing-counterexample-reuse','from':['customer-attraction/adaptive-continuation-menu-barriers','customer-attraction/parent-harmonic-menu-two-original-audits-and-frozen-reports'],'to':['customer-attraction/harmonic-menu-parent-review-normalization-and-legal-menu-scope'],'explanation':'同一12题4人26171145单位客户旧完整SPE，π4=π9=1/2，τ2、ηhalf给R−11/4、Z3、S3、组合−4和总−1；否无条件非负组合债，不反带债母式或half。89客户6题根−1/48是不同对象。','evidence':[related_paths[3],primary['1545471ca1085eada13d']['sources'][0]]},
 {'type':'independent-obligation-boundary','from':['customer-attraction/constant-tail-menu-harmonic-to-profit-conversion-coefficient-boundary'],'to':['customer-attraction/harmonic-menu-parent-review-normalization-and-legal-menu-scope'],'explanation':'常菜单族S/R/Z全0仍在r≥3否半倍普通尾利润转换，因此一般付款还要分别处理多层债和Ψ−Wtail信用过量；本独审没有支付二者。','evidence':[related_paths[5]]}
]
(base/'relation-notes.json').write_text(json.dumps(relations,ensure_ascii=False,indent=2)+'\n')
notes={
'01358becd12e98b4f96f':(
 '3558B程序全文：标准库Fraction/缓存/有序笛卡尔历史；固定12题4人输入，核正权合法mask、完整1885策略域及22620含self比较；沿原策略而仅排序终局缓存收益，核旧组合债精确读数；覆盖邻接677B报告。',
 '与作者5701B程序全文比较：后者只重算三尾而不验完整SPE，本实现独有完整历史核验；同输入已有另一5232B审计/发布replay绑定输入与源码SHA，不重复复跑。当前全仓同父程序SHA只见来源索引/治理记录，未发现当前成功运行记录。',
 '保完整代码及直接同SHA旧输入，资源明确完整SPE算法和父方原报告身份；不把排序收益缓存误当合并历史，不把原passed称当前运行。'),
'a9508d5d82fc2743e7a3':(
 '5502B程序全文：Fraction阈值网格base0..8/a0,1/followers0..12/七eta共1638；seed977714真实4标签9客户合法过去/尾菜单280，actual对角最大保证当前S，r2末位BR40；七eta随机q共1960恒等与上界；邻接报告覆盖写。',
 '与作者1728网格/2500抽象单客户程序比较：本实现1638网格和合法目录可实现性/当前S检查不同，r>=3仍不验后继理性。已读scratch一次RNG计划解码原日志/执行源码，280 τguard均过且最小1；本批复用而不重跑。',
 '独有随机目录生成域、固定先验、样本与通用证明边界全保资源；有限280不升级完整SPE；原程序/main与RNG当前均0运行。'),
'1545471ca1085eada13d':(
 '677B JSON全部16根字段完整读：源路径/SHA、1885历史、22620比较、actual(8,4,5,0)、查询4/9各half、Ψ70761167/3、R−11/4、Z3、S3、组合−4、G−1、τ2、ηhalf、原status和scope。',
 '对3558B生成字段/常数以及作者769B三尾报告和既有replay完整对账；同输入SHA be96...f898，12题大输入与89客户六题根−1/48不混。报告只绑定输入SHA，无执行源码SHA/argv/环境。',
 '原字节保全及资源逐字段表述；原内部独立完整SPE重放事件与本批静态读取分开。G−1只否无条件非负组合债，不反half或带债恒等式。'),
'f8022194def22f79cd9c':(
 '303B JSON全部7字段完整读：seed977714、1638参数、280合法菜单、1960价格点、40末位BR菜单，原status exact independent checks passed和不证明一般SPE债支付的scope。',
 '对5502B循环/计数域与原父审全文比较；七eta/40r2与作者八eta/2500单客户是不同实现。已存旧RNG窄诊断只表τguard相容，不补成这份报告数学PASS。',
 '保冻结报告及全部字段，有限域与缺少逐样本/运行绑定信息明列；不把计数正确或字段对账当新运行/普遍证明。'),
'6fa933e36cc587485086':(
 '3927B父审三节全文：原先收益重构后读母稿的内部先验，V=F−aK及R交叉式、S/τR/ηZ逐客户展开、价格端点与归一化、全eta阈值及half三类、四人组合G−1、两实现与有限域和未付义务。',
 '全文比较母式定理/原母稿/作者5701B/769B，以及加权两尾旧式Z_old=τZπ/V_old=τ²Rπ。只读子代理另全文核89客户6题区分；常菜单S/R/Z0仍半利润转换失败，债与过量势为不同缺口。',
 '一般符号式已由母式定理保存，本批新增自足审查对象保原读序、准确归一化、合法菜单与完整SPE范围及原反例解释；不把历史独审转当前盲审、外审或half证明。')}
receipts=[]
for sid,x in primary.items():
 read,comp,decision=notes[sid]
 receipts.append({'id':sid,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':read,'comparison_note':comp,'decision_note':decision,'disposition':'integrated','targets':[resource,review,str(base/'README.md'),x['preserved_at']]})
(work/'semantic-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
(base/'README.md').write_text('''# 调和菜单独审五源与证据范围

本包完整保留已领五源共13967B：两程序3558/5502B、两报告677/303B及父审3927B。五件均正常 `work.py clean show ID` 全文读取，并另行 `--out` 取得冻结原字节；size/SHA256/Git blob逐件核同。[source-manifest.json](source-manifest.json)保两冻结来源完整commit/path、实际命令与保存位置，是派生运输记录，不冒原CLI日志。

数学内容、程序全部有限域和报告每个字段见[原审计资源](../../../state/资源/父方调和菜单两原审计与冻结报告--资源.md)；原先推后读的内部先验、τ正规化和组合债反例解释见[独审对象](../../../state/审查/调和菜单独审的归一化与合法菜单核验范围--审查.md)。一般恒等式已在父档母式定理，本包不再创建一份新定理。[comparison-manifest.json](comparison-manifest.json)和[relation-notes.json](relation-notes.json)明确比较者、相关字节与逐关系证据；未改三级图或共享入口。

原树 `original/research/.../parent/` 保存两个无改写程序、报告及审查；固定依赖 `original/history/source/notes/customer_attraction/uploaded_2026-10-10/auxiliary_counterexample.json` 同SHA保存，故 `parents[5]` 根定位闭合。代码仅标准库；若将来运行会覆盖相邻报告，应先复制独立运行树。本批没有运行/import任何原程序。

旧完整SPE输入与另一5232B审计及22620比较成功记录已充分保存于[母稿证据](../../../../../tools/evidence/harmonic-tail-menu-primary/README.md)与[旧发布报告](../../../../../tools/evidence/continuation-security/replay-decorrelation.json)。本包只核输入同SHA并复用既有成功证据，不把它算成父方3558B代码当前运行。

`reused-diagnostic/` 原样保存scratch旧缓存的一次RNG消费计划窄诊断（全部280个z/τ与原执行stdin源码）。该旧诊断只核τguard，未计算势/收益/IC，也未保存280完整游戏。当前RNG、原main/import、势/收益/IC执行均为0；静态AST/JSON/YAML/链接/字节核对不能改写为数学PASS。

Boss统一checkpoint和逐源done；本包只在新独立路径交付，自身不执行Git mutation、claim、done或checkpoint。
''')
# Candidate batch is an inventory-only suggestion, never claimed or declared read.
next_ids=['4379d147f371123668a1','96663eefc37be7d22d47','7fde0e258a567562a399','c399079bea1f71770022','b4ad6beb37a59db520c6','95c70e7abc6f936b9fc6']
inv={x['id']:x for x in map(json.loads,Path('cleanup/inventory.jsonl').read_text().splitlines())}
next_rows=[]
for sid in next_ids:
 x=inv[sid];p=Path('cleanup/progress')/(sid+'.json');progress=json.loads(p.read_text()) if p.exists() else {}
 next_rows.append({'id':sid,'path':x['path'],'local_disposition':progress.get('disposition','available'),'owner':progress.get('owner'),'recommendation_only':True,'not_read_in_this_batch':True})
(work/'next-batch-suggestions.json').write_text(json.dumps({'reason':'同研究树三尾产品转移主稿/作者实现报告/父方独立实现报告审查成组六件；先由Boss核远端归属再决定，不重复本五源或当前Root另领批。','candidates':next_rows},ensure_ascii=False,indent=2)+'\n')
# Static verification only: no import, subprocess, random or mathematical program invocation.
issues=[];ast_checks=[]
for x in manifest:
 p=Path(x['preserved_at']);b=p.read_bytes();assert len(b)==x['size'];assert hashlib.sha256(b).hexdigest()==x['sha256']
 if p.suffix=='.py':
  tree=ast.parse(p.read_text());ast_checks.append({'path':str(p),'syntax':'parsed-without-import-or-execution','imports':[n.module if isinstance(n,ast.ImportFrom) else ','.join(y.name for y in n.names) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]})
 elif p.suffix=='.json':json.loads(p.read_text())
try:
 import yaml
 for name in [resource,review]:
  t=Path(name).read_text();data=yaml.safe_load(t.split('---',2)[1]);assert all(k in data for k in ['id','kind','type_tag','title','status','summary','source_refs'])
except ImportError:
 issues.append('PyYAML unavailable; metadata syntax not parsed')
links=[]
for name in [resource,review,str(base/'README.md')]:
 p=Path(name)
 for rel in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in rel or rel.startswith('#'):continue
  dest=p.parent/rel.split('#')[0];exists=dest.exists();links.append({'file':str(p),'link':rel,'exists':exists})
  if not exists:issues.append(str(p)+': '+rel)
for p in base.rglob('*.json'):json.loads(p.read_text())
for p in work.glob('*.json'):json.loads(p.read_text())
self_check={'scope':'static transport, syntax, report field reading and local-link checks only; no mathematical execution','primary_count':len(manifest),'primary_bytes':sum(x['size']for x in manifest),'ast_checks':ast_checks,'links':links,'issues':issues,'current_original_main_runs':0,'current_original_imports':0,'current_math_runs':0,'current_rng_runs':0,'git_mutations':0,'cleanup_mutations':0}
(base/'static-self-check.json').write_text(json.dumps(self_check,ensure_ascii=False,indent=2)+'\n')
assert not issues,issues
files=[resource,review]+[str(p) for p in base.rglob('*') if p.is_file()]
delivery={'status':'ready-for-boss-checkpoint-and-source-done;local-only','source_ids':list(primary),'primary_bytes':13967,'objects':[{'path':resource,'id':'customer-attraction/parent-harmonic-menu-two-original-audits-and-frozen-reports'},{'path':review,'id':'customer-attraction/harmonic-menu-parent-review-normalization-and-legal-menu-scope'}],'receipt_file':str(work/'semantic-receipts.json'),'publish_paths':[resource,review,str(base)],'files':files,'relation_review':str(base/'relation-notes.json'),'static_check':str(base/'static-self-check.json'),'next_suggestions':str(work/'next-batch-suggestions.json'),'current_math_or_rng_executions':0,'note':'Original reports retain original status. Prior RNG decode and existing full-SPE replay are reused; neither is a current new run. No Git/claim/done/checkpoint/sync/start performed.'}
(work/'delivery.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':delivery['status'],'files':len(files),'sources':len(primary),'links_checked':len(links),'issues':issues},ensure_ascii=False))
