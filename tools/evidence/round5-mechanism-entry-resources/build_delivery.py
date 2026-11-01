from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-round5-mechanism-entry-resources';E=Path('tools/evidence/round5-mechanism-entry-resources');W=Path('cleanup/workspaces/Boss4/r3-round5-mechanism-entry-resources-next')
IDS=['81b9fe6fd862fbf894c3','e472b7bd82857b215f9a','9897a3c1963ad411fc18','5f95777827b702848bad','87672640237e60c7d0ed']
P='archives/customer-attraction/state/资源/一般机制入口的有限诊断与未付合同--资源.md';PC='archives/customer-attraction/state/资源/真实菜单协方差与逃逸余项的审查合同--资源.md';PM='archives/customer-attraction/state/资源/平稳查询与复制菜单的有限证据合同--资源.md';PB='archives/customer-attraction/state/障碍/最优剩余利润的局部系数与共享负载信用--障碍.md';PV='archives/customer-attraction/state/引理/单色真实后缀的饱和查询与剩余税--引理.md';PD='archives/customer-attraction/state/资源/背景信用的诊断范围与原稿证据合同--资源.md';PVA='archives/customer-attraction/state/候选/单色真实后缀的虚拟相邻税--候选.md'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
claimpath=R/'boss4-r3-next-is-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids'])
mp=C/'learning-hv-next-round5-entry-inputs/local-export-manifest.json';m=json.loads(mp.read_text());primary=[];owners=[]
for i in IDS:
 x=next(x for x in m['rows'] if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/x['path'];cp(x['local_path'],q);primary.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'headings':[l for l in b.decode().splitlines() if l.startswith('#')],'read_mode':'actual firstfull text/math reading afterHVpacket froze, beforeISclaim underparentpreworkauthorization; actualclaim/owner/SHA verified beforefinalreceipt; no fakepostclaimreread'})
assert sum(x['size'] for x in primary)==9064
js(E/'source-manifest.json',primary);cp(mp,E/'actual-primary-local-export-manifest.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners)
contexts=[]
for p in [PC,PM,PB,PV,PD,PVA]:
 b=(REPO/p).read_bytes();q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'previous actual complete derivation/fullreading reused, current whole-byte source-object comparison; no code/JSON audit falsely reread'})
js(E/'context-manifest.json',contexts)
front='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id','customer-attraction/mechanism-entry-finite-diagnostics-and-unpaid-contracts'),('kind','resource'),('type_tag','资源'),('title','一般机制入口的有限诊断与未付合同'),('status','five-entry-source-texts-completely-reviewed; finite-reports-not-universal-proof'),('summary','保五入口审查/程序用途与当前范围，新增n2保留outcomes16852及967浮点目标/0.75无对偶、19输入2503背景/终局计数的准确记录；现完整数学精确复用，0新数学执行。')])+'source_refs:\n'
for x in primary:
 for y in x['sources']:front+='  - '+json.dumps('source:'+y['commit']+':'+y['path'],ensure_ascii=False)+'\n'
front+='---\n\n# 一般机制入口的有限诊断与未付合同\n\n'
body=r'''## 五个入口是资源，不是五个新结果

五份README分别1195、1772、1315、2785、1997B，共9064B，已全文实际读完，包含每项链接、表格、最后状态/下一步与程序声明。对象始终为有限单位客户、共同有限非空目录、单位提供者、完整有序历史纯SPE，保空主题、重复及任意离轨平局。原Boss10/个人备份/停止固定人数调参/没有Git或凭据操作等均保历史，不作为当前清洗的新指令。

源文一般half未解与当前五人已有定理、六人仍开放分开；“本目录没有宣布解决Mfull”只是局部历史声明，不等于全仓现在仍OPEN。后续零根银行反例已另否定普遍逐位置Mfull/弱push等合同，以下局部例不反驳这些合同不使它们复活。

## coupling入口：同一客户状态与指定核的精确duplicate

1195B入口的主数学和全部资源角色已在[协方差与菜单换基](../资源/真实菜单协方差与逃逸余项的审查合同--资源.md)及[平稳查询资源](平稳查询与复制菜单的有限证据合同--资源.md)完整覆盖：共同客户的root会员a、真实尾负载k、v/t及CC1…4是已有ROOT的等价坐标，无一般符号预算；COH换菜单另有未付漂移，不重复认一个一般付款结果。

6286客户、六主题、三人的完整例有唯一source→uniform**完整终局槽**平稳分布p=(1,1,0,1,1,0)/4，query2价5765/4>u2821/2、gap123/4；self C<D，五纯列安全。只排指定核选择，不反该例自由mixed/self strong/half；transient query即使源质量0仍须cap，不能靠主题边际平衡忽略。

`stationary_full_slot_counterexample_6286.json`称存原客户/43动作/全矩阵与准确范围，`probe_stationary_full_menu.py`和`stationary_348_diagnostic.json`为明确核攻击的发现器/冻结记录，另一研究员单位审计在round5_audit。源入口这些角色与“没有继续微调固定m”均已明确归位；本批没有读其原code/JSON或新跑它们，不额外增加独立审稿人数，故该入口数学按精确对象duplicate。

## credible入口：四种数量不能互换

两块菜单可实现不许可直接扩三块。原C++称按五原始单位客户类型写收益、用整数集合BI计算全部历史依赖纯SPE的可实现终局集合；参数2、3，不导规范solver。终局集合按计数缓存不强制两个相同计数的有序节点选同续局，也不枚举所有完整动作图。

1772B入口新增保留outcomes数16852，必须与状态、叶、策略DAG及root终局数分开：

| 原有限对象 | 两块数值/含义 | 三块数值/含义 |
| --- | --- | --- |
| 计数前缀状态 | 12870 | 2704156 |
| 计数终局/叶 | 6435 | 1352078 |
| 程序报告保留outcomes | **16852** | 3207136 |
| 指定root目标 | 四类均可实现 | 四类均不可实现、全部last-low截面严格阻断 |

程序报告“保留outcomes”不等于root终局数，更不是完整纯策略数量；本批未读源码/全JSON，不能再增释它究竟怎样累计。理论上8主题/8槽的全部可能计数前缀数是C(16,8)=12870、终局C(15,8)=6435；12主题/12槽则为C(24,12)=2704156和C(23,12)=1352078。这只解释**模型计数空间**，不认证程序实际访问、筛选或保存结果。

另一个已给定两块完整策略DAG有13872节点，含终局目标记忆，和12870计数前缀不是同对象；相同计数可在DAG中因不同目标有多个节点。n2的root可实现终局数35、n3为200，亦不同于16852/3207136，具体有限分类在[已有资源](平稳查询与复制菜单的有限证据合同--资源.md)。原“与旧证书三个计数完全吻合”保作者报告身份，不冒本批独立输出逐字节比较。

单块六种root终局集合Q的n次积中至多一个q0=(2,1,1,0)，在n1/2/3由有限结果确认，任意n仍猜想。单实现三块全截面、一个独立余3人局部代表、任意n一般引理/容量状态是三层范围；没有新编译C++、BI或原JSON字段认证，也不因条件矩阵n4超价宣称真实SPE反例。

## global入口：M=0已证与M>0待支付分开

1315B的主数学已在[单色饱和查询与剩余税](../引理/单色真实后缀的饱和查询与剩余税--引理.md)自足保：固定背景下单色静态PNE的弱支配成立，五客户完整SPE反动态共同势最优；静态同背景结论不能移去root改行动后另一背景。

actualA B^r，r≥1，q(T)=Σ_(x∈T)1/(b_x+1+r1_B)，u_A=q(A)，M=u_A−q(B)≥0。精确M=0时根改B的最坏保底取等刚性、原末位B与改B枝末位BR共同给所有q(T)≤u_A；空B/零客户包括。空根m人且u_A=|B|/m时OPT_m≤(2−1/m)|B|≤(2−1/m)W。M>0的正剩余税仍需真实rootB后继抢先回报支付，不能由连续性或所有逐前缀安全保底推出。

原“既有两主题频次条件去重待逐字核对”现有[VA资源](../候选/单色真实后缀的虚拟相邻税--候选.md)可明确：两个不同实际覆盖次数k,l的充分筛选l(2k+1)≥k²−1，在A B^(m−1)取k1、l=m−1时自动成立；退化A=B为单色情形另有直接末位比较。故M0不声称新增已知**half适用范围**，但更强全查询预算及相对|B|的系数仍是独有有用结论，不因范围去重删掉。

`audit_local_findings.py`/`local_findings_audit.json`只被README描述为重算两个具体对象与逐客户静态式；未读代码/报告，不能补成全部r/background测试范围。`va_safe_relaxation.py`/`va_r2_safe_relaxation.json`是必要条件LP诊断，负点无完整SPE，不能叫VA或half反例。有限核验不承担一般VA；原root独立解析M0的身份也不变成当前新增一次独审。

## induction入口：利润目标、两个无限族及未付状态

r≥1、合法过去负载b，定义
\[
F_r(b)=\max_{Z\in\mathcal S^r}\sum_x\frac{c_x(Z)}{b_x+c_x(Z)},
\]
零分子取0；P是同节点真实剩余r人总利润，u_i是这些人在同一真实终局的收益。F不是覆盖集合C的总覆盖补全max|C∪Z|，两者首步缺口不能混名。

[利润/信用障碍](../障碍/最优剩余利润的局部系数与共享负载信用--障碍.md)已完整保：交叠完整SPE族n≥4精确Ftail=2(n−1)(n−2)+(7n−13)/6，系数2在n≥5失败、固定α<17/6最终失败；更简单已知all-big族u1、Ftail2n−h_n、h_n=min整数j(j+n/j)≥2√n，使任何人数无关有限α都失败。局部台阶失败不反整体F≤2P或half，真实tail额外信用恰能补根债；不把17/6留作可调通用常数，也未排所有人数依赖α_r形式。

只计背景/实际tail共同覆盖、实例无关且仅依r/b_x/c_x的Σf_r信用，f(0,c)=f(b,0)=0，已由两完整SPE无限族同f_r(1,r)冲突排除；允许负值、独占项、实例/主题或非可加信息是不同候选，仍须非循环定义和信用转移。直接取C_h=F_r−2P_h只重述根目标，不算解答。

## 967、0.75与2503：新增历史记录，不是上界证明

2785B入口比之前“34策略/19实例”摘要更精确，其数字/角色逐项保留：

| 原文件/记录 | 作者报告的范围 | 准确限制 |
| --- | --- | --- |
| `audit_profit_bellman_family.py` / `profit_bellman_family_exact.json` | n4…8共15501个剩余主题多重集合，核新利润最优值 | 全n来自解析消元，非有限SPE外推；本批未读/运行原code/JSON。 |
| `bellman_diagnostic.py` | 在既有22客户输入的另一可实现终局先发现系数2亏空 | 是明确一般候选的有限诊断，不是新的单位客户证书。 |
| `weak_gap_diagnostic.py` | OPT−W≤m minactual u与作者称更强的插入保底；后者在既有输入失败 | 不猜未读代码里的具体插入值定义；强接口失败不自动反不同的弱机会缺口，后者原文未证。 |
| `weak_gap_cone_probe.py` / `weak_gap_cone_probe_exact.json` | 每小输入至多两个终局构造**34棵完整策略**，单次优化**967个OPT−m u_i目标**，无严格违反；最大**0.75** | 0.75仅浮点候选最大值，未恢复完整有理对偶；连这些锥的认证上界都不是，更非一般桥/精确3/4最优上界。文件名`exact`不能替代证书。归一化/容差未从原码核，不擅补。 |
| `background_gap_diagnostic.py` | **19个输入、2503个背景/SPE终局计数**，检查F_r(b)−P≤r min剩余u未见违反 | 2503不是完整策略数、所有有序历史数或独立运行次数；无违只作者工具记录，不支持全称桥，也不升成全局每玩家门槛。 |

[已有信用诊断资源](背景信用的诊断范围与原稿证据合同--资源.md)已保34/19及BG-GAP未证合同，本页补精确967/2503和0.75的非证书状态。这些原程序和全部输出本批未实际取得/全文读，也未运行；不把“未读”写成已经验证或永久不可得。

若BG-GAP真对所有合法节点成立，零根F_m(0)=OPT_m、P=W且m min_i u_i≤W可给half；有限19/2503没有提供这个全称前提。也不能从有限计数直接迁移到所有actual玩家的统一收益预算。停止原固定候选的无违扫描是当时研究判断，当前仍需保可接续的未证合同。

## mixed入口：条件矩阵与真实策略是两件事

1997B入口所有数学/程序角色已在[平稳/复制资源](平稳查询与复制菜单的有限证据合同--资源.md)完整保。若n块root菜单真可由同一完整SPE实现，n≥3混合值37/10−17/(12n)，n4首超u13/4；条件矩阵本身没有构造后继。原独立核验器称从五客户类型重算矩阵/根收益/原始对偶/自由背景cap，不导solver或旧矩阵，本批未读或执行它。

last-low独立局部稿和核验器只分析ACD|AAB|AAB余三人一节点，不覆盖全部排序/截面。三块四类目标皆不可实现为credible单实现报告，mixed目录明确没有重跑大BI。固定p=uniformD和root自身≤13/4的替代子树最大插入(101/30,283/90,197/60,551/180)，B/D不足；本目录只独立重算展示profile的有理插入值，最大/可实现性来自同一credible探针，不新加一次完整BI认证。

假设n≥4真实实现，仍可得到该族另一个FM/弱完整推送失败，却不反该族自由静态extra-one或half（静态每块qB便宜、所有列满覆盖）。当前别处银行已反一般FM；这不替代此特殊复制族仍欠的可实现性，也不把原局部“未宣布解决”说成错证明。

## 阅读、资源用途与接续

[五原件清单](../../../../tools/evidence/round5-mechanism-entry-resources/source-manifest.json)保真实原字节/两个冻结来源、首读时点与实际claim交集。新增独有内容是精确有限记录/审查范围/程序用途；数学主对象按已有证明复用，两个全覆盖入口明确duplicate，不新建同一定理或空壳候选。

没有新数学程序、原CLI、LP/BI/随机或旧成功复跑。模型状态、解析任意量词、原作者有限报告、浮点未认证输出和未完成proof obligation分别保；不因OPEN或未得原代码把有用数学退休，不将入口链接自动当第三阶段超边。
'''
put(P,front+body);js(E/'formal-resource-manifest.json',[{'path':P,'bytes':(S/P).stat().st_size,'sha256':sha((S/P).read_bytes())}])
prior_packages={PC:'r3-covariance-menu-coherence-and-escape-review',PM:'r3-stationary-query-and-replicated-menu-audits',PB:'r3-d22-frontier-ledger-primary',PV:'r3-d22-frontier-ledger-primary',PD:'r3-profit-credit-and-saturated-query-source-bindings',PVA:'r3-monochromatic-tax-and-full-menu-contracts-primary'}
for x in contexts:
 old=C/prior_packages[x['path']]/x['path'];assert old.read_bytes()==(S/x['snapshot']).read_bytes();x['previous_complete_read_delivery']=str(old);x['current_equals_previous_frozen_delivery']=True
js(E/'context-manifest.json',contexts)
coverage=[
 {'id':IDS[0],'disposition':'duplicate','targets':[PC,PM,P],'units':['allmodel/oldgeneralOPEN correctedcurrent5vs6/no newrole instructions','CC rootmembership/truetail jointstate sameidentities asroot/audit andunpaidsign','6286/6themes/3players completeSPE sourceidentity/unique fullslotstationarypi/query2 5765/4-u2821/2=123/4','selfC<D/fivepurecolumns safe onlyspecifiedkernel fails/notallfreeFM/selfstrong/half','selfcontainedJSON originalmasks43actions/matrix claim notnewrawread','discoveryprobe andstationary348 twoqueryreport/independentround5_audit implementation roles exactlyreuse','transientexternalqueryzero mass stillneedsallquerycap/nofixedmultipliersearch ashistory']},
 {'id':IDS[1],'disposition':'integrated','targets':[P,PM],'units':['allunitmodel/orderedhistories/ties/frozenpersonalnotsharedclaim history','fivecustomer-type hardcodedinteger BI/no canonicalsolver/inputs2or3','n2 states12870/leaves6435/retained16852/4feasibletargets eachdistinct','n3 states2704156/leaves1352078/retained3207136/4infeasible/alllastlowcuts sourceauthorfinite record','combinatorialcountspace explanation notvisitedstates proof/13872memoryDAGdifferent/root35and200different','p=uniformD B/Dthresholdfail claimedonly notnewprobe','candidate Q^n withatmostoneq0 verifiedn1,2,3notalln/realmodulecapacityobligation','no blindn4 orparametersearch instruction executed/no Git/auth historicalstatement']},
 {'id':IDS[2],'disposition':'integrated','targets':[P,PV,PVA],'units':['samebackgroundstaticPNEweakdom vs5clientdynamicalPhi counterexample','VA exactRES/tax/constantsafequerylocalization/complementaryblockobstacle existingfullproof','M0 strongerallquerycap/allnonnegativelegalbackground/emptyandzero/rootindependentanalyticidentity','zerorootm (2-1/m)|B| welfare doesnotnewhalfapplicationrange; frequencyk1 sufficient/A=Bseparate','audit_local_findings program/report finite2objects/perclientstaticformulas source-describednotfullcoderead','va_safe_relaxation/r2JSON necessaryLPnotfullSPEcounterexample','M>0 truechangedBbranch earlyprofitpayment stillopen/no continuitystrengthening/no fixedm tuning instruction execution']},
 {'id':IDS[3],'disposition':'integrated','targets':[P,PB,PD],'units':['F_r legalactualprefix/c=0convention/profitnotcoveragecompletion/alln variableunitproviders','allbig exacthn/rootdebt ofsqrt(n) anyfinitefixedalpha fails notallalpha_r/true tailcredit','overlap n>=4 exactF/2failsn>=5/alpha<17/6asymptotic weakerthanunbounded','instancefreeadditiver/b/c overlapcredit zeroaxes bothfamilies f_r(1,r)contradiction/notallcreditstates/no tautologicaldefinition','n4to8 15501multisets finiteimplementationdiagnosticnot universalSPEproof','bellman_diagnostic known22clientotherrealizableterminal notnewcertificate','weakgap vsstrongerinsertionfloor failurelogicaldistinction/exactunreadfloor notinvented','weakcone atmost2terminal/input34fullstrategies/single967objectives/0.75floatcandidate/no fullrationalduals/notcertifiedevenfiniteconeupperbound','background19inputs2503bg-SPEterminalcounts notstrategy/history/run count/no universalbridge/no globalindividualbudget','BGGap rootconditionalhalfimplication exactmmin<=W premise notfulfilledby19cases/stoppedfixedcandidate researchhistory']},
 {'id':IDS[4],'disposition':'duplicate','targets':[PM,PC,P],'units':['localMfull unresolvedstatementhistoricalnotuniversalcurrentOPEN','conditionaln>=3 M37/10-17/(12n),n4first>13/4 notactualfullSPE','independentmatrixchecker5types/root/primaldual/freecap/no solveroroldmatrix source-only','localACD AAB AAB3remainingDdeviation37/10 onlyoneprefix/notallorders','credible sameC++n3fourrootclasses impossible/no independentbigBIreplayhere','hypotheticaln>=4 wouldFMweakfail notfreeextra/half/no realizationfromstaticmenus','uniformD root<=13/4 substitute maxima101/30,283/90,197/60,551/180 B/Dfail sameprobe/onlydisplayprofileprices independentlyrecomputed','oldstoppedspecialinstance/notcurrentcleanerstop/no unrelatednewtheorem']}
]
js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':5,'primary_bytes':9064,'primary_lines':sum(x['lines'] for x in primary),'primary_first_full_read':'IS preclaim authorized semantic preparation afterHV package freeze; exact sourcebytes reused afteractualclaim ratherthan fake secondfirstreading','dispositions':{'integrated':3,'duplicate':2},'new_formals':1,'new_theorems':0,'new_game_instances':0,'new_math_program_runs':0,'original_math_CLI_calls':0,'old_success_replays':0,'LP_BI_random_runs':0,'raw_program_and_report_fullread':False,'historical_reports':'sourceMD testimony only; 16852retainedoutcomes/967float objectives/0.75no rationalduals/19inputs2503backgroundterminalcounts distinct','combinatorial_statecounts':'definition-level starsandbars inference, notnew programoutput orvisitedstates certificate','previous_contexts_current_byteidentical':6,'local_helper_calls':1,'local_blob_attempts':5,'local_exports':5,'local_missing_blobs':0,'helper_scope':'nextcandidatebytesonly notISmath','next5_status':'byteavailability only beforeISseal; no fullsemanticread orprimaryreceipt yet','missing_retry_calls':0,'shared_Git_writes':0,'claim_done_checkpoint_show_calls':0,'network_or_lazy_fetch':0,'real_board_account_auth_operations':0,'phase3_graph_import':0,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'derived_packaging_builder_calls':2,'derived_packaging_builder_failures':1}
js(E/'read-scope-and-evidence-status.json',scope)
notes=[
 ('1195B原入口在HV封包后IS预读期已实际逐段全文读，本次核同SHA复用；题首一般OPEN、共同客户状态、6286和工具/审稿/下一步全部实际读。','同现HP协方差资源及HF完整槽资源逐项比较，所有恒等式/指定核反例/完整证书用途和独审先验已完整覆盖；与旧348输入名及另query5分开，不借名字误换输入。','duplicate：保持五纯列安全与self strong，不能以指定kernel失败反同例自由mixed/half。原code/JSON没有本批全文或执行，冻结历史不变，全部独有角色和接续义务有精确目标。'),
 ('1772B原credible入口IS预读期实际全文/每文件列表/全部计数/任意n候选及最后历史声明读完；不是把标题或先前related数学当未读原件。','现HF/HP已覆盖条件菜单、Q集合、局部last-low与13872DAG；本入口独有16852保留outcomes精确保，n2/n3的状态/叶/累计保留/root终局/完整策略DAG分别定位。组合计数只解释模型空间，不冒程序已访问证明。','integrated：新资源吸收精确有限输出角色与未证任意n容量合同，旧C++/JSON均未新读或重跑，四目标有限不可实现不升级任意块数引理、真实n4反例或一般half；全段可接续。'),
 ('1315Bglobal入口IS预读期实际全文，全部bullet内静态/动态/M0/常数背景/松弛/补全障碍及最后M>0义务均实读。','同GS饱和查询引理和FT VA候选全文/同SHA现页比对，所有主证明已保；准确消解原待核频次范围，用k1充分条件去重half适用域，同时保更强allquery与|B|系数。两程序用途及有限LP无SPE分别归档。','integrated：独有程序/报告资源角色和当前时态归位，不把新资源当重新证明一般VA，不把独立root解析历史算新独审，不因half范围已覆盖抹掉M0有用结论，不冒未读code或输出。'),
 ('2785B归纳入口IS预读期实际完整读，全部三主稿、五程序/输出及尾状态均核，不将旧34策略摘要代本入口967与0.75/2503原字段。','与GS完整无限族/可加信用障碍和GY诊断资源同SHA逐项比较；新保15501多重集合、22客户另一终局、34策略967浮点目标、19输入2503背景终局等不同计数，0.75没有全套有理对偶连局部上界亦不认证。','integrated：保同背景F定义及任意固定alpha失败、未证非循环信用/弱gap/背景gap完整合同。强插入floor失败不自动反弱桥，有限无违不补全全称量词，不虚构未读代码归一化或run数量，0重复原成功。'),
 ('1997Bmixed入口IS预读期实际全文表格、n3排除/条件n4/替代profile数值和最后停止段实读，核本地原字节与两来源。','全部数学及独立程序用途已在现HF/HP自足资源保；精确区分条件minimax、当前真实可实现性、只一局部节点、同一credible大BI和本目录仅profile有理重算，四替代值完整保。','duplicate：不是用数量判重；每独有项有精确旧目标并在新总资源定位。一般Mfull已由另源否定不替此特殊族realizability；freeextra/half未被条件资产反驳，不将旧未在本目录宣布解决当现全仓OPEN。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原15ids真实claim原字节保，本5subset/现owner/sourceSHA核后才封成功receipt。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# IS一般机制五入口资源

9064B五原件全部在HV封包后IS预读期实际完整读，现核实际pushed/synced原15ids及五owner/SHA后封包。3integrated、2duplicate；只新一资源，不新造定理/输入/程序证明。六正式数学对象与既有完整阅读交付物逐字节相同，context保绑定。

独有内容：16852保留outcomes不等12870计数状态/6435叶/13872目标记忆DAG或root35；967浮点目标最大0.75无完整有理对偶，连这些锥认证上界都不是；19输入2503背景/SPE终局计数不升全称或全局个体预算。所有code/JSON角色源文全文读，原code/JSON未本批全读/执行，作者历史数值不冒新认证。

0新数学程序/原CLI/LP/BI/随机/旧成功复跑。一次纯本地helper只核下一五入口14067B，0missing/0network，下一尚只byteavailable，不借本包receipt提前done。原冻源不改，Root先推正文依赖再done；本代理无sharedGit/账号/公屏/第三阶段mapper。
''')
put(W/'relation-review.md',r'''# 阶段二关系与去向

五入口为已证明数学、有限记录及未证合同的导航资源。coupling/mixed完整覆盖者逐项duplicate；credible精确数量、global程序审查用途/时态、induction精确有限目标和背景终局记录integrated。该划分来自实际原段去向，不由人数/文件标签/计数自动判重。

将计数前缀/计数终局/保留outcomes/root可实现集合/带目标DAG分开；stars-and-bars仅模型空间的定义级推断，不是读到未取程序的循环合同。程序独立于canonical求解器是作者实现声明，不等当前canonical实现认证。

M0数学保强全查询和|B|系数，half适用范围用既有k1筛选去重；M>0正税未付款。固定人数无违/0.75float/部分参数枚举不给全称量词。BGGap若真可蕴half仅是条件推导，19/2503不证明其前提。局部插入floor失败与另一弱gap不互相替换。

同SHA先前全读证明如实复用，0新证明/原CLI或旧成功重跑，0额外done所引用程序/JSON或下一5，0旧图导入或强制连通造边。保仍有用候选/障碍/来源，不因旧OPEN和未读原code退休材料。
''')
nextmp=C/'learning-is-next-origin-entry-inputs/local-export-manifest.json';nextm=json.loads(nextmp.read_text());assert len(nextm['rows'])==5 and nextm['missing']==[];cp(nextmp,E/'actual-next-byteavailability-local-export-manifest.json');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
nextrows=[]
for x in nextm['rows']:
 v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];q=REPO/'cleanup/progress'/f"{x['id']}.json";pr=json.loads(q.read_text()) if q.exists() else None
 if pr is None:nextrows.append({**v,'local_path':x['local_path'],'progress_observed':None,'read_status':'byteavailability only beforeISseal; notfullsemanticread/claim/primaryreceipt; Root deconflicts andactualclaims next'})
js(W/'next-candidates.json',nextrows);js(E/'packager-recovery.json',{'builder_calls':2,'initial_failure':'context assertion expected literal 常数, whereas existing full derivation says 所有相关客户背景同一d≥0','actual_scope':'only wording matcher corrected after actual samebackground formula/obstacle reread; source and math body unchanged','new_math_executions':0,'original_CLI_calls':0,'old_success_replays':0});cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex_balanced(s,left,right):
 def count(d):return sum(ord(s[i])==92 and s[i+1]==d and (i==0 or ord(s[i-1])!=92) for i in range(len(s)-1))
 return count(left)==count(right)
assert tex_balanced(chr(92)+'[x'+chr(92)+']','[',']') and not tex_balanced(chr(92)+'[x','[',']') and tex_balanced(chr(92)*2+'[2pt]','[',']')
for x in primary:
 b=(S/x['preserved_path']).read_bytes();ck('sourceexactsizeSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceexactblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('rawclaim byteidentical',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes());ck('actual5subsetownerSHA',set(IDS)&set(claim['ids'])==set(IDS) and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('actualclaim pushedsynced',claim['status']=='pushed' and claim['local_sync']['status']=='synced' and claim['local_sync']['remote_tip']==claim['remote_tip']);ck('raw15notprojection',len(claim['ids'])==15 and len(IDS)==5)
for x in contexts:ck('contextactualpreviousreadsamebytes '+x['path'],len((S/x['snapshot']).read_bytes())==x['bytes'] and sha((S/x['snapshot']).read_bytes())==x['sha256'] and Path(x['previous_complete_read_delivery']).read_bytes()==(S/x['snapshot']).read_bytes())
t=(S/P).read_text();ck('flatMATEK',all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('nonLF C0zero formal',not any(ord(c)<32 and c!='\n' for c in t));ck('trailingzero formal',all(l==l.rstrip() for l in t.splitlines()));ck('actualTeXbalanced',tex_balanced(t,'[',']') and tex_balanced(t,'(',')'))
links=[]
for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
 if '://' in dest or dest.startswith('#'):continue
 n=posixpath.normpath(str(Path(P).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('actualrelative link '+dest,q.exists());links.append({'source':P,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
ck('sourcecountsdistinct',all(x in t for x in ['16852','12870','6435','13872','3207136','1352078','2704156']));ck('floatnotbound','967' in t and '0.75仅浮点候选' in t and '连这些锥的认证上界都不是' in t);ck('backgroundcountscope','19个输入、2503个背景/SPE终局计数' in t and '2503不是完整策略数' in t);ck('onlyconditionaluniversalbridge','有限19/2503没有提供这个全称前提' in t);ck('M0strongMpositiveunpaid','half适用范围' in t and 'M>0' in t and '更强全查询预算' in t);ck('allcodeunreadnotmissingforever','未实际取得/全文读' in t and '不把“未读”写成已经验证或永久不可得' in t);ck('globalconstantbackgroundandcomplementcovered',all(x in (S/E/'context'/PV).read_text() for x in ['所有相关客户背景同一d≥0','互补块','v≤y/3']))
ck('5receipts3integrated2duplicate',len(receipts)==5 and {x['id'] for x in receipts}==set(IDS) and sum(x['disposition']=='integrated' for x in receipts)==3 and sum(x['disposition']=='duplicate' for x in receipts)==2)
for x in receipts:ck('complete semanticreceipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() or (REPO/p).exists() for p in x['targets']))
ck('exact1newformal',set(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))=={P});ck('no mathbodyoroldreplays',scope['new_math_program_runs']==scope['original_math_CLI_calls']==scope['old_success_replays']==scope['LP_BI_random_runs']==0);ck('helpernextbytesonly',len(nextm['rows'])==5 and nextm['missing']==[] and scope['local_helper_calls']==1 and scope['local_blob_attempts']==5)
for x in nextrows:ck('actualnextavailable '+x['id'],Path(x['local_path']).exists() and len(Path(x['local_path']).read_bytes())==x['size'] and sha(Path(x['local_path']).read_bytes())==x['sha256'] and x['progress_observed'] is None)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context']);bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('allnewderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_original_context_unchanged':True})
put(W/'delivery.md',f'''# IS交付

5primary9064B/{scope['primary_lines']}行全部实际原文读，3integrated+2duplicate，一新自足资源。原15ids claim {claim['remote_tip']} actualpushed/synced原字节保，仅本5subset/currentowner/sourceSHA；六正式上下文与以前全文读交付物逐字节一致。

新独有内容为16852 retainedoutcomes计数及967浮点目标/0.75未认证上界、19输入2503背景/SPE终局计数等资源合同；完整定理和条件菜单按准确对象复用，0新定理/实例/数学程序/原CLI/旧成功复跑。未读原程序/JSON的作者有限记录保身份，不扩大SPE或全参数量词。

下一{len(nextrows)}原件共14067B纯本地核齐，尚byteavailable未本批全文，不预claim/receipt；一次helper5尝试0missing0network。Root先推正文和依赖再done，本代理0sharedGit/账号或第三阶段mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'math_checks':'no new math execution; packaging checks bind actual fullread sources/previous read target bytes and author-reported finite record scopes, notuniversal theorem proof','scope':'rawsource/owner/raw15claim/coverage/links/format/existingtargetbindings/transport'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':9064,'primary_lines':scope['primary_lines'],'new_formals':1,'formal_bytes':(S/P).stat().st_size,'receipts':5,'dispositions':{'integrated':3,'duplicate':2},'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'new_original_CLI_runs':0,'old_success_replays':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
