from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re,shutil
stage=Path(__file__).resolve().parents[4];repo=stage.parent.parent/'boss4-research';ev=Path('archives/unrelated-machines/tools/evidence/capacity-half-slot-and-row-reviews');ws=Path('cleanup/workspaces/Boss4/r3-capacity-half-slot-and-row-reviews')
def j(path,x):
 p=stage/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def s(path,x):
 p=stage/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x.strip()+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((stage/ev/'manifest.json').read_text());by={x['id']:x for x in m['records']};objs=json.loads((stage/ws/'object-paths.json').read_text())
# Preserve a previously reconstructed historical body only after its exact documented hash matches.
old=stage.parent/'r3-unrestricted-minwork-row-audits/archives/unrelated-machines/tools/evidence/unrestricted-minwork-row-audits/verified-historical-prefix/row-spread-v1.md'
assert sha(old)=='8b1abf7a149759cb2f9c7424c380181442990e0f7ee913273a1c1091526f3e00'
p=stage/ev/'verified-historical-versions/joint-slot-prefix-v1.md';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(old.read_bytes())
body=(stage/by['8e7fbfe13b8dcfeb9ec6']['target']).read_bytes();section=body[body.index(b'## 7.'):];assert hashlib.sha256(section).hexdigest()=='8037f85bb3b67b6a9f57553d36367388ec4d0e2597a5b348ee5f5828eaf0c2dc';(stage/ev/'verified-historical-versions/machine-config-frozen-section7.md').write_bytes(section)
# Read-only inventory fixtures are separate from primary executions.
half=json.loads((stage/by['12b601da50cee4eab718']['target']).read_text())['actual_joint_rounding_certificate'];j(ev/'fixtures/parity-half-unit-complete-input-and-witness.json',half)
formal=[
'archives/unrelated-machines/state/审查/极小超载星容量耦合与最小工作面支撑障碍有限审查--审查.md',
'archives/unrelated-machines/state/审查/全局基数与逐行均匀相关读出边界有限审查--审查.md',
'archives/unrelated-machines/state/审查/全局行基数过滤与多外层单态小home双源审查--审查.md',
'archives/unrelated-machines/state/审查/配置激活与有限覆盖增量审计--审查.md',
'archives/unrelated-machines/state/问题/任务级共同容量的算法义务--问题.md']
related=[]
for rel in formal:
 q=repo/rel;related.append({'path':rel,'sha256':sha(q),'size':q.stat().st_size,'scope':'full text read in current or preceding same-task batch; current bearing sections compared; not modified','relation':'older finite evidence/problem statement; new pages preserve original-code and review identity without replacing its source disposition'})
j(ev/'related-formal-material.json',related)
# Preserve the exact previously recorded scope suggestion; this batch does not apply it.
suggestion='independent 在 k=3..128 只运行 127 个 scalar/representative 样本'
q=repo/formal[3];assert suggestion in q.read_text();snapshot=ev/'existing-formal-snapshots'/q.name;(stage/snapshot).parent.mkdir(parents=True,exist_ok=True);(stage/snapshot).write_bytes(q.read_bytes())
j(ev/'comparison-findings.json',{'applied_to_old_objects':False,'old_scope_clause':suggestion,'old_object':formal[3],'old_sha256':sha(q),'snapshot':str(snapshot),'evidence':'compact_config_probe_audit.json independent.scalar.k_range=[2,128],cases=127; representative.runs only k=3..8 with queries18/27/44/77/142/271; current independent implementation read in preceding batch and current SHA verified','minimal_suggestion':'将该句改为：独立程序另对 k=2..128 共127个参数仅作标量检查；完整实例代表延伸仅在 k=3..8 检查18/27/44/77/142/271项，非全配置枚举。','prior_delivery':'same exact scope finding already supplied with compact-count-and-configuration-audits; not a new old-source disposition'})
j(ev/'runtime-dependencies-and-run-binding.json',{
 'new_original_program_runs':0,'reason':'Both executable primaries have adequate exact-SHA historical runs and complete finite outputs. Reviews already record their actual old executions; no duplicate run is needed to account for current-source semantic content. Current verification only parses source AST and validates frozen data.',
 'bindings':[
 {'primary_id':'698bdcab0669d55a1efa','sha256':by['698bdcab0669d55a1efa']['sha256'],'historical_record':by['e024705ef6909102d311']['target'],'payload':'reports.capacity_pair_reproduced.json','historical_command':'python3 tests/audits/unrelated_machines/capacity_one_star_pair.py','python':'3.12.14','base_commit':'974813e88ff9f80cdda9a1f817be990ce1d90816','historical_exit_code':None,'new_stdout':False,'imports':['collections.defaultdict','fractions.Fraction','itertools.combinations','json','platform'],'external_input_files':[]},
 {'primary_id':'3366609734cf33d87e19','sha256':by['3366609734cf33d87e19']['sha256'],'historical_record':by['12b601da50cee4eab718']['target'],'payload':'actual_joint_rounding_certificate','historical_command':'python3 tests/audits/unrelated_machines/half_unit_joint_slot.py > <scratch-new.json>','python':'3.12.14','base_commit':'f68299b86b1e12a2b62ce852fa4ce2f27e6e67d2','historical_exit_code':None,'new_stdout':False,'imports':['fractions.Fraction','itertools.combinations','json'],'external_input_files':[]}
 ],
 'review_program_bindings':{'c76da606d8c2e7e8fe35':{'historical_record':by['fad6c1261ebf89ea2271']['target'],'actual_personal_execution':'compact_config_probe_independent.py; primary hash only, no personal line-read of primary implementation','manual_common_base_scalar_check':'Historical review narrative only; not an archived canonical command/stdout and not an explicit current scalar-main assertion.'},'1f64a487c666cbeb751d':{'historical_records':[by[x]['target'] for x in ['292abbaeaee297858760','99fabfaf306e1766cd1e']],'actual_commands':['row_count_probe.py','compact_count_escape.py','independent_row_count_escape.py','multirow_count_extension.py'],'main_and_transitive_dependencies':'All named originals retained under dependencies; full code was read in preceding primary batch; current SHA rechecked. compact main imports old pair/row probe; multirow uses independent build_family only; config primary imports compact build only; independent counterparts use standard library only.'}},
 'nonclaims':['No new execution, process timing, numeric exit code or freshly generated primary stdout.','Aggregated JSON contains unrelated audits; keeping their bytes does not treat those sources as primary done.','Verifier fixture checks do not execute has_schedule or capacity.audit.']})
j(ev/'version-bindings.json',{
 'row_review':{'initial_body_sha256':'78b9b5b9ee288a783b07925834ee064e7bbee2737d306bf69771559887a5cc50','multirow_body_sha256':'da4737f6408b59c87a4c1c986c365cd6558ccf3651f5e13ce17d3b6b6b498c6f','historical_prefix_comparison':'Reported actual comparison in primary review from957f04b; intermediate whole bodies not newly reconstructed here. Current introduction and appendedMP differ, so not falsely declared exact old bytes.','old_minimal_star_body':'be27a3e92dc1da3050cedb911798fb35b78a370afc011fbe5dde519f7cf31837','old_block_body':'962897812a6eb8e3c27962567625120792bea7407bb2c6598c31dbe2c54c4b0c','merged_block_body':'8cf637c20618062a98d4038e7873987acf06bf426a583a6a678d974d7b103ba3','current_row_body':by['8e7fbfe13b8dcfeb9ec6']['sha256'],'scope':'Old§1–5 plus explicitly later multirow appendix; not independently discovered/currentMP§7.'},
 'machine_config_review':{'recorded_whole_versions':['63fa15647111e5300cf63f0c2057c969ddf6a917f0ce1c213bf521c96514f859','52b1987db1d2c91687e5cef3157173ece7b9f33250f42cc8190770459105b1d0','95f4873702d73ca8b76d7b1aab4d9eb27b5f5ddee2bb683830a5ae7cf08d5db3','028314a66eb613a1f132a14cc745c3f9a2a070317cceb8e82fe1f348bcad7e37',by['8e7fbfe13b8dcfeb9ec6']['sha256']],'actual_preserved_frozen_section':str(ev/'verified-historical-versions/machine-config-frozen-section7.md'),'section_sha256':hashlib.sha256(section).hexdigest(),'middle_whole_bytes':'Only recorded identities; not fabricated or newly checked as whole files.','scope':'Original§6 proof, later§7 renumbered; colleague multirow§6 explicitly outside independent proof scope.'},
 'half_unit':{'current_code_sha256':by['3366609734cf33d87e19']['sha256'],'old_full_body_sha256':sha(p),'old_full_body_evidence':str(p.relative_to(stage)),'old_full_body_method':'Exact previously restored current§1–6 prefix, matched documented8b1 SHA; copied here after checksum.','current_full_body_sha256':by['8880cf5284ef95a424b1']['sha256'],'earlier_code_before_prefix_assertions':'Narrative only, old bytes/hash not supplied; final c07code did get actual reviewer read/run.','later_common_b_domain':'Different§7 and construction. Current parity fixture has3 positive small incidences perR, outside at-most2 class.'}})
units=[
 {'id':'698bdcab0669d55a1efa','units':['build(k) machine/job/time/config list and exact size counts','explicit_pair four formulas, reversed V orientation and None product meaning','audit per-machine normalization, real capacity, complete coverage, eligibility and all-machine-pair loop','factorized product proof, implicit versus actually checked entries','irreducible boolean iff k>=3, minimum eligibilityk','main finite k3..12 output and symbolic OPT-field status'],'destination':objs[0]},
 {'id':'3366609734cf33d87e19','units':['hardcoded parity triples and no perfect pair','all10machines/14jobs/34finite edges and Fraction certificate','all-row load1, spread/prefix/floor assertions','sorted exact interval buckets, augmenting covering matching, actual loads3/2','complete bounded-capacity assignment recursion at1and3/2','full printed matrix/certificate/assignment and one-instance scope; final strengthened-code history'],'destination':objs[1]},
 {'id':'c76da606d8c2e7e8fe35','units':['deep-tree/path prior and candidate-recipe disclosure before independent reconstruction','globalX mass/localR demand and uniform fullCONFIG construction','all7pin classes, empty/full/subset and k2 boundary','general integer value, safe deletion versus unsafe all-target rejection correction','common-base first-moment contradiction as oldcut explanation, not newClaim','O(k4) support/O(logk) coefficient bound, no enumeration/generaloracle','independent true runs/scalar and expanded scopes, initialfloatbug/currentFraction fix','primary hash-only/no-line-read limitation, whole-body renumber/parallelmerge/navigationSHAchain'],'destination':objs[3]},
 {'id':'1f64a487c666cbeb751d','units':['Exact-first reconstruction, frozen oldscope/table and all bearing code identities','safe rowcount filtering and contraction-matroid weight algorithm/bitcomplexity','allpool domination only fixedH/c','compact integer lower/upper, allavoid/pin witnesses, GPC2 and no-star/no-small-domain rule','general acceptinggap upper, target-dependent blockcut adapter','actual three old runs and exactfinite DP versus fullschedule scope','concurrent halfunit merge and unchanged oldcut explanation','later multirow additional proof with precise G centerbudget, onehelper and directR rearrangement versus codeinactiveR version','sharp zemptyHall rank7/17, fixedrquantifiers, actual50319/30 boundaries','later sparseconditioned/rowspread merge is read-after relationship, not new independent mathematics'],'destination':objs[2]}
];j(ev/'source-semantic-units.json',units)
receipts=[]
notes={
'698bdcab0669d55a1efa':('逐行读全 build、四类 explicit_pair、反向重标、audit 全机器对/因子化分支、不可约与 main。核完整7067B/f2a SHA，理解k块原矩阵、配置和OPT字段不执行求最优。','与当前minimal-star§1–6、旧聚合run capacity_pair 字段、既有极小星正式页及紧凑族新N块实现全文/此前实读比较。旧完整历史run同SHA且充分，复用不重跑。','独有函数合同、四类完整公式与列和、全pair显式/乘积计数、k2可约界和后续仅局部复用已自足保存。一般gap证明保留既有归属，未虚构全局联合/一般oracle。'),
'3366609734cf33d87e19':('clean show实际导出4018B/c07原件并逐行全读：全部输入、Fraction点、最终前缀/floor断言、槽桶与增广、精确双阈值全资格回溯及完整stdout字段。','读旧冻结完整输入/x/assignment与8b1主文、当前ab1a新增§7；核最终代码SHA和旧真实run。独立给出奇偶NO到OPT3/2证明，区分跨度2与R含3条small而非至多2的新域。','保全10机14任务34边的实际矩阵/证书/调度、16槽与完整匹配算法、真实回溯范围及代码加强史。充分同SHA旧run复用，未虚构新运行、回溯计数或原审查主源done。'),
'c76da606d8c2e7e8fe35':('核9057B/27d SHA后全文读完审查顺序、全部pin攻击、共同base增量、复杂度、程序/float修正/未逐行主实现限制及全部结尾节号/并行合稿hash说明。','与当前a075正文§7逐字hash8037、主fff/独立9f代码此前逐行读和当前核SHA、冻结主/独立JSON、旧配置正式页范围句比较。初审整稿中间版本只按原文身份保留，不声称补读不存在原字节。','自足保留均匀单项配置装配、全部类型/边界、MP失败只能删C的纠正、一阶矩共同base矛盾、真实非零信息先验与冻结链。旧审查hash-only主实现不倒填；127scalar与较大完整代表分开。'),
'1f64a487c666cbeb751d':('核13640B/ad94 SHA并全文读完旧表/安全证明/位复杂度/全池支配/紧凑族攻击/旧cut适配/实际run/同期半单位合稿、追加多行证明与末尾稀疏条件/跨度同步记录。','与当前row正文及精确依赖代码此前实读、真实row/multirow聚合数据、旧minimal-star和joint-block版本身份、既有全局计数正式页比较。保初始78b与追加da473、MP8037另审，不由当前整稿反推旧审查scope。','完整安全性/最大权收缩拟阵/固定H全池支配、计数独立见证、动态B的cut、真实U多行G尖锐预算及两种R实现证明均自足保存。有限DP/Hall/50319/30不称一般求解；同期读后更新先验如实保留。')}
for sid in [x['id'] for x in units]:
 u=next(x for x in units if x['id']==sid);a,b,c=notes[sid]
 receipts.append({'id':sid,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a,'comparison_note':b,'decision_note':c,'disposition':'integrated','targets':[u['destination'],by[sid]['target'],str(ev/'manifest.json'),str(ev/'runtime-dependencies-and-run-binding.json'),str(ws/'数学自查.md')]})
j(ws/'semantic-receipts.json',receipts)
# Actual local available candidates, never a claim operation.
ids=['88d24b9e7bfa6073a305','a790489613b14e894206','bd5630362d6fbba23966','d2a76cc583499921b3ea','1e0d47d8b4a911adfb02'];inv={x['id']:x for x in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())};n=[]
for sid in ids:
 hit=[]
 for pth in (repo/'cleanup/checklists').glob('*.md'):
  for line in pth.read_text().splitlines():
   if sid in line:hit.append({'path':str(pth.relative_to(repo)),'line':line})
 assert len(hit)==1 and 'unread' in hit[0]['line'] and '未认领' in hit[0]['line'],(sid,hit)
 e=inv[sid];n.append({k:e[k] for k in ['id','path','size','sha256']}|{'local_status':'unread / 未认领','local_checklist':hit[0]['path'],'reason':'adjacent explicit configuration-count/activation/finite-cover original programs; frozen aggregate results already exist but original executable still needs primary full read','not_claimed_here':True})
j(ws/'next-candidates.json',{'status':'local snapshot only; parent must resolve latest ownership and perform actual claim','excluded':'08e1e1abef90b6ce07b6 belongs to Boss2; not proposed again or primary disposed here','candidates':n})
s(ev/'README.md','''# 容量一原程序、半单位原入口与两份审查证据

四个 primary 原件位于 original，inventory SHA/size/定位在 manifest.json。comparisons、dependencies、historical-runs 是完整原字节比较材料，不因旁读而新增其 primary done。

两个可执行主源均只使用标准库及硬编码输入，旧 run 与实际主源 SHA 相符且范围充分；本批不重跑原入口。runtime-dependencies-and-run-binding.json 保留真实旧命令/字段/未知退出码。half-unit 的完整冻结矩阵、分数点与整数分配另存 fixtures；验证它不等于再运行原回溯。

verified-historical-versions 中8b1正文来自此前精确恢复并再次核hash，8037节来自当前a075原件实际切片；其他中间整稿只有原审查记载hash，version-bindings.json明确区分。comparison-findings 仅复述前批已提出的scalar/expanded范围修订，不覆盖旧页。

四个自足正文位于state/资源与state/审查；源语义单元、当前既有对象SHA和逐源收据均可核。新原程序执行0，未记录虚构耗时、退出码、全文外审或新颖性。
''')
s(ws/'数学自查.md',r'''# 数学自查

已全文实读4主源并理解各语义单元；代码标准库依赖、原输入和旧run身份核齐。没有以旧comparison代替本次primary阅读。

1. 容量一族：m=k²+3k−1、n=2k²+k、有限边2k³+4k²；与紧凑共享族的O(k³)机器及O(k⁴)边不同。配置归一/覆盖与四类pair边际逐式重算，G–G/R–R循环只在各自k索引。主循环k3..12，k2的G可约，零质量项正负条件分清。OPT字段不是计算搜索；一般整数证明已自足。
2. 半单位：10机器、14任务、34有限边，全分数负载1；R2槽、S2槽、元素1槽，共16而非14，不假称覆盖匹配占满所有槽。实际assign从原P复核，max3/2；NO3DM证明与半整数格给精确下界。回溯只有cap1/3/2的布尔结果，没有杜撰搜索节点数。R每行3small，不属于后来至多2small新域。
3. 行计数：其他机只有count约束；安全性用真实T调度的外送匹配。权在任务上而非边，故收缩横截拟阵贪心适用。全池支配必须固定H/c。B变化的r_B系数不能固定到θ端点。多行补位至多一个，代码让R所属块非活跃与正文直接重排是两个合法版本；尖锐只证明特定z空pin失败，Hall秩不是全调度求解。
4. 完整配置：所有pin类型穷尽，特别空V/fullZ与R固定Z的中心修改不能漏；均匀d_j/q是完整配置y，不是仅load点。MP不是所有整数可行输入的必要条件，失败只安全删C。共同base混合恒等式才强制z≥2(k−1)>1，各自延伸没有这些恒等式。独立支持O(k4)与每个显式pin多项式，不等于枚举全部C多项式。
5. 先验：原rowreview Exact-first后读稿，后来另审multirow；MP审查先读旧构造/候选配方，独立实现后读新证明，主实现只核hash。清洗者当前/前批逐行读取不倒填原review的独立性。旧scalar人工共同base运算与规范scalar代码不同证据身份。
6. 证据：全部冻结源size/SHA、旧run程序hash、实际half矩阵/证书、8037节与8b1旧正文核验。新原入口运行0，未知旧退出码保null，验证脚本不导入primary。已有共享正文不改，前批scalar范围建议保持未应用。

既有数学对象已吸收的主证明不重复授予定理；新资源保存完整实现及公式，新审查保存独有重构、异议、版本与不同范围。一般UM目标、外审、优先权仍未关闭。''')
s(ws/'关系与来源证据.md',r'''# 关系判断及来源证据

这属于阶段二正文入库时的关系判断，不复制旧超图、不为连通造边。

| 参与对象 | 关系、共同前提与限制 | 证据 |
|---|---|---|
| 容量一原程序 → 既有极小星容量审查 | 原程序实现其k块配置/GPC2分支，补全四类公式及显式/因子化执行边界；不能转为高阶joint | f2a原件、e024聚合reports.capacity_pair、旧be27正文§3–4 |
| 容量一 → 紧凑共享逃逸 | 旧R–R/V–R局部组件可复用；新族扩大至N块并改G–G/V–G、加z，其整数下界须重证 | c260/f2a实际import与原review§3 |
| 半单位实际原入口 → 行跨度2联合槽正面接口 | 同一个完整P的fractional前缀/真实matching见证；一般证明另承载，不由单例推出 | c07原件、12b完整input/x/assignment、旧8b1正文 |
| 半单位 → 后来common-b两small类 | 仅比较不同域，无实例包含边：半单位R有3small；后来归约删除该源机 | 当前ab1a§5与§7.6 |
| rowreview → 全局安全过滤/紧凑族 | 初始精确声明重构后的证据/论证审查，78b旧范围；multirow后来追加另有da473身份 | ad94原审查、292/99运行记录 |
| multirow正文与独立实现 | 同一G尖锐预算，正文R分支可直接重排，代码统一非活跃并补位；两者不是字节复制证明 | 原review追加§7与10d实际代码 |
| MPreview → 完整配置延伸 | 提供均匀配置装配的独立实现、MP安全语义纠正与共同base一阶矩解释；非候选未知盲审 | 27dc全文、9f代码、fad完整JSON、8037节 |
| MP共同base解释 → 旧条件块cut | 相同R槽/逃逸数量机制，不另立一项新Claim；一般分离/统一舍入仍缺 | 原review共同base段和rowreview§4 |

现有对象的读取范围、SHA记录在related-formal-material.json。旧4页及问题页保持不改；新增四对象与它们是实现/来源/有限检查/合同边界关系，不能拼成一般UM算法或困难性。08e主源属于Boss2，只必要比较既有记录，不新增其receipt。''')
s(ws/'delivery.md','''# 交付

4份正式认领来源，4篇自足数学资源/审查，逐源收据在semantic-receipts.json。复制范围仅copy-files.json列出的独立文件，由Root串行保存；本代理没有执行Git、claim、done、checkpoint或spawn。

原件、依赖、真实历史run及完整半单位输入/证书已保全。本批新原程序执行0；验证仅核冻结数据和身份。未知旧退出码/耗时未填造。旧页不改，已有scalar范围纠正建议只是再次准确指向原证据。

五个本地未处置候选见next-candidates.json，父代理须复核实时归属并正式认领。当前文件尚不能称已推送，需父代理实际正常checkpoint完成。
''')
print(json.dumps({'receipts':len(receipts),'new_original_program_runs':0,'next_candidates':ids},ensure_ascii=False))
