from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';GS=C/'r3-d22-frontier-ledger-primary';S=C/'r3-profit-credit-and-saturated-query-source-bindings';E=Path('tools/evidence/profit-credit-and-saturated-query-source-bindings');W=Path('cleanup/workspaces/Boss4/r3-profit-credit-and-saturated-query-source-bindings-next')
IDS=['5807ac87276a9bc80ce0','0efa8da260f6c6ee8015','9bf8a294ee059185147e','86390a643a36ea35f311','bdd683848aab07c77142']
P='archives/customer-attraction/state/资源/背景信用的诊断范围与原稿证据合同--资源.md'
P2='archives/customer-attraction/state/障碍/最优剩余利润的局部系数与共享负载信用--障碍.md';P3='archives/customer-attraction/state/引理/单色真实后缀的饱和查询与剩余税--引理.md';P4='archives/customer-attraction/state/障碍/双向隔离惩罚的福利上限与逃逸预算--障碍.md';P1='archives/customer-attraction/state/资源/真实分支十项合同与菜单可实现性账本--资源.md'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
# Authoritative actual capture must exist and succeed before packaging primary receipts.
claimpath=R/'boss4-r3-next-gy-claim.json'
if not claimpath.exists():raise SystemExit('GY actual capture not yet present; no primary/receipt generated')
claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids'])
resolutionpath=C/'boss4-r3-next-gu-to-gy-atomic-claim-sync-preservation.json';resolution=json.loads(resolutionpath.read_text());assert resolution['receipt']=='boss4-r3-next-gu-to-gy-atomic-claim' and resolution['stash']=='aad9b887a8a70fc30fb8cb633bc074f76de9d437' and resolution['missing']==[] and resolution['different']==[] and resolution['unmerged']=='' and resolution['stash_kept'] and len(resolution['tracked'])==2 and all(x['same'] for x in resolution['tracked']) and resolution['untracked_count']==2
assert claim['local_sync']['status']=='needs-attention' and resolution['stash'] in claim['local_sync']['detail']
cp(resolutionpath,E/'actual-independent-claim-sync-preservation.json')
previous=json.loads((GS/'tools/evidence/d22-frontier-ledger-primary/related-source-manifest.json').read_text());primary=[];owners=[]
for i in IDS:
 x=next(x for x in previous if x['id']==i);v=inv[i];b=(GS/x['preserved_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/x['path'];cp(GS/x['preserved_path'],q);primary.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'first_full_read':'GS actual full every section math text; reuse samebyte in GY rather than pretending reread/replay','prior_exact_snapshot':str(GS/x['preserved_path']),'headings':[l for l in b.decode().splitlines() if l.startswith('#')]})
assert sum(x['size'] for x in primary)==34224
js(E/'source-manifest.json',primary);cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners)
contexts=[]
for p in [P1,P2,P3,P4]:
 b=(REPO/p).read_bytes();assert b==(GS/p).read_bytes(),p;q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'reading':'GS original full derivation/preparation and actual final body review; GY exact whole-byte equality to accepted GS4 packet, no fictional rereading or new independent proof','prior_stage':str(GS/p)})
js(E/'context-manifest.json',contexts);cp(GS/'tools/evidence/d22-frontier-ledger-primary/read-scope-and-evidence-status.json',E/'actual-prior-GS-read-scope.json');cp(GS/'tools/evidence/d22-frontier-ledger-primary/formal-resource-manifest.json',E/'actual-prior-GS-formal-manifest.json');cp(GS/'delivery-summary.json',E/'actual-prior-GS-delivery-summary.json')
# The three already fully covered original proofs are retained as dependency snapshots, not new primary.
relatedids=['efb09bff2fbae18ba384','c9ccc7817c179b3b1396','73e78b9e31ec4e9518da','4fa30e438229f7d5436d'];related=[]
for i in relatedids:
 x=next(x for x in previous if x['id']==i);v=inv[i];b=(GS/x['preserved_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];q=E/'related'/i/x['path'];cp(GS/x['preserved_path'],q);related.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_mode':'GS entire actual mathematical reading honestly reused sameSHA; comparison only no additional primary/done'})
js(E/'related-source-manifest.json',related)
front='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id','customer-attraction/background-credit-diagnostic-scope-and-original-evidence-contracts'),('kind','resource'),('type_tag','资源'),('title','背景信用的诊断范围与原稿证据合同'),('status','complete-source-role-and-evidence-binding; remaining-opportunity-gap-candidate-unproved'),('summary','补原信用稿34策略/19实例有限诊断用途及合法背景弱机会缺口的未证合同；五源逐节对已自足解析对象，四源已有完整数学去向精确duplicate，不重复定理或旧运行。')])+'source_refs:\n'
for x in primary:
 for y in x['sources']:front+='  - '+json.dumps('source:'+y['commit']+':'+y['path'],ensure_ascii=False)+'\n'
front+='---\n\n# 背景信用的诊断范围与原稿证据合同\n\n'
body=r'''## 模型、利润与没有被局部反例解决的合同

有限单位客户、有限共同非空主题目录、单位顺序提供者，完整纯SPE在每个合法有序历史指定行动及真实后继，允许空主题、重复及任意离轨平局。合法固定前缀过去负载b，余r人，比较利润
\[
F_r(b)=\max_{Z\in\mathcal S^r}\sum_x\frac{c_x(Z)}{b_x+c_x(Z)},\qquad F_0(b)=0,
\]
零分子取零。P是同节点原SPE真实剩余r人总利润，u_i是这些人在**原真实终局**的收益。F不是覆盖补全、额外查询或任意可自由改写的过去。

7329B原交叠族利润稿末尾保留两个独立候选：零根OPT_m−W≤m u_i的弱机会缺口，以及合法背景
\[
F_r(b)-P\le r\min_{i\text{ remaining}}u_i.\tag{BG-GAP}
\]
**该稿没有证明BG-GAP，有限阴性诊断也不支持其全称成立；两个Bellman反族没有在稿中反驳它。** 不把BG-GAP与另有反例的逐人静态门槛、FM、强D≥C、总覆盖前缀余额混同。

本资源的直接逻辑说明：若某节点BG-GAP成立，r·min u_i≤Σu_i=P，于是F_r(b)≤2P；零根F_m(0)=OPT_m,P=W才得half。这是它的充分用途，不是新增证明。类似地，原零根机会缺口若对每名i真成立，选最小u_i可得OPT_m≤2W。当前真值必须各依独立证据，不能从“逐人OPT/(2m)下界失败”直接否定这个含W的不同合同。

## 34棵策略与19个实例：原稿明确限制的用途

5412B信用稿的“为什么已有有限数据不能决定剩余义务”完整保留以下身份：

| 作者历史诊断 | 实际优化或观察对象 | 不能承担的义务 |
| --- | --- | --- |
| 34棵完整策略的弱机会缺口优化 | OPT−W≤m u_i这一候选的有限策略集合；未覆盖全部策略 | 没有优化一般信用函数，更不提供所有目录/人数/全部SPE证明；样本非负不支持普遍真值。 |
| 19个实例的背景利润诊断 | 有限节点F_r−P与当前收益的数值 | 没有一般可计算C、跨分支转移、根/终端边界；不能当BG-GAP或信用合同认证。 |

这两个计数只按**实际已全文读的作者MD历史记录**归档。本批没有取得/全字段读取其原输入、代码、输出与每次run记录；未尝试导出不写成“文件缺失”。不把34或19当本批覆盖数、原程序运行次数或已独立重核样本。已成功的其他同SHA审计也不借名称移到这两个诊断上。

真正尚缺的非循环信用对象可表达为
\[
F_r(b)\le2P_h+C_h,\quad
\Delta_h+C_{hA}-C_h\le2u_h,\quad
\Delta_h=F_r(b)-F_{r-1}(b+1_A),\quad
C_{terminal}\ge0,\ C_{empty}\le0.
\]
直接定义C_h=F_r−2P_h只令局部式成等式，根C≤0重述主问题。有限数据没有给独立根边界。任意可行新状态须区分真实分支替代/目录结构，不能仅加入更多参数就称完成。

## 两族证明已归位，诊断不能替代其全称量词

[最优利润和共享信用障碍](../障碍/最优剩余利润的局部系数与共享负载信用--障碍.md)已自足完整保存：

- 全A大主题/单例族的每历史策略，u=1,W=n,OPT=2n−1，Ftail=2n−h_n，h_n=min整数j(j+n/j)；根差h_n−1无界。每个有限α用平方n=q²构造严格失败，所有n量词由解析规范化与AM-GM承担。
- 交叠族的完整SPE来源与全整数槽消元，Ftail=2(n−1)(n−2)+(7n−13)/6；n≥5的系数二余额负、α<17/6必要下界与n4边界，但尾部真实信用仍付清，half余量2(n−1)>0。
- 两族同r=n−1对实例无关、仅依共同负载的同一f_r(1,r)施加冲突上下界，n≥16排除f(0,c)=f(b,0)=0的可加模板；不排有独占项、目录或实例信息、非可加信用。

原交叠稿与独审报告各自n4…8合15501计数候选、all-big独审的n2…8只核有限实现。这里没有读或新运行对应原代码/JSON，不能把有限作者计数变成当前普遍证明。两个无限族本身同样不证明一般half；它们精确排局部系数和写定模板。

## 已完整覆盖的三个主稿与完整证书义务

[饱和查询引理](../引理/单色真实后缀的饱和查询与剩余税--引理.md)已保9011B单色稿的全部独有数学：同背景静态弱支配、五客户动态势反例、逐前缀安全保底、RES正税、M=0取等刚性与空/零边界、空根(2−1/m)|B|推论、同常数背景查询定位、必要LP点不能补完整SPE及互补块方案冲突。它未证明一般M>0或VA2，不借LP必要条件造反例；本次只按同SHA原稿和已有精确去向duplicate，不另发同一个引理。

[双向隔离障碍](../障碍/双向隔离惩罚的福利上限与逃逸预算--障碍.md)已保7216B主稿全部结构假设、三真实比较、k1/零/正偶等号、原全人数族存在性来源；新E逃逸缺口也已连到独立探索稿。任意k的证明不是有限样本外推，隔离假设不泛化为所有SPE。全A5256B主稿的全部历史证明、精确F、无界实α量词与信用区间亦已在利润对象覆盖，不再造重复障碍定理。

隔离主稿最后要求的half反例交付合同仍准确适用：必须有有限整数客户兴趣类型与共同目录、真实人数m及福利W、一个合法m主题组合见证OPT_m>2W、所有有序决策历史的行动或能填满它们的明确递归，以及每个节点每个合法偏离沿**同一原策略真实后继**的本人收益比较。坏终局、在轨比较或可行必要条件点均不足。这里是既有模型下的证书用途说明，不新增一份SPE或认证未读策略。

## 原件、版本和审查责任

五份34224B原件首次全文实读均发生在GS必要related阶段，GY逐件核实际完整字节/SHA256/blobSHA1后诚实复用；不伪称新第一读或盲审。[逐源清单](../../../../tools/evidence/profit-credit-and-saturated-query-source-bindings/source-manifest.json)保两个冻结提交相同内容、原路径及精确先前快照。全仓检查没有发现这五路径在冻结两版本间的新内容；当前正文必须与已交GS精确hash一致才可duplicate。

本资源新增保存34/19诊断的准确证据边界；BG-GAP已有[动态信用来源入口](../资料/动态信用背景探针来源与开放边界--资料.md)，本页只补清晰公式和逐源绑定，不当成首次提出的新候选。该入口配套的[末位余项分解](../引理/任意背景的末位利润精确余项分解--引理.md)实际证明F_r−P≤(r−1)v，v为真实末位收益；只有额外v=min_i u_i才能替换最小收益。不能把末位比较当BG-GAP的一般证明。两页原有TeX损伤在本批保原字节/SHA及精确位置，不覆写其他owner的历史正文。既有三自足数学对象不覆写、不重命名。原“先盲重构/内部root复核”的历史先验不改成当前新增独立审稿人。新增数学程序/原CLI/LP/BI/随机/旧成功重跑均0，不执行真实账号/公屏/身份或网络操作；无外审、新颖性或算法时界认证。
'''
put(P,front+body);js(E/'formal-resource-manifest.json',[{'path':P,'bytes':(S/P).stat().st_size,'sha256':sha((S/P).read_bytes())}])
# Existing non-GS resources were actually read in full GY, including their visible formula damage.
oldcontexts=[];formatfind=[]
for n in ['archives/customer-attraction/state/资料/动态信用背景探针来源与开放边界--资料.md','archives/customer-attraction/state/引理/任意背景的末位利润精确余项分解--引理.md']:
 before=S/E/'format-recovery/before'/n;b=before.read_bytes();q=E/'context'/n;cp(before,q);oldcontexts.append({'path':n,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'GY entire actual text and math, all sections; source status/history read without overwriting other owner'});t=b.decode();formatfind.append({'path':n,'before_sha256':sha(b),'bytes':len(b),'nonLF_C0':[{'character_offset':i,'code':ord(c),'context_repr':repr(t[max(0,i-15):i+25])} for i,c in enumerate(t) if ord(c)<32 and c!='\n'],'observed_text_condition':'multiple visible lost LaTeX backslashes as well as C0; record only, no shared overwrite or undocumented repair','mathematical_status':'formula semantics understood from complete text; typography defects do not invalidate the old proved algebra'})
contexts+=oldcontexts;js(E/'context-manifest.json',contexts);js(E/'observed-unowned-formal-format-defects.json',formatfind)
coverage=[
{'id':IDS[0],'disposition':'duplicate','targets':[P2,'archives/customer-attraction/state/资料/动态信用背景探针来源与开放边界--资料.md',P],'units':['legalbg/Fprofitdefinition vscoverage andfullhistory assumptions','allunitclientgroups x=n-2 and explicitstrategy reference tofullyreadSPEproof','fullintegercount expression/b0 b>=1 exactelimination withn4ties','P0/P1 exactF formula/n5negative11/15/alpha<17/6 quantifier','u/W/OPT/rootdelta/tailV/slack/globalhalf positive','15501n4to8finiteauthorrun notnewcertified','bothzero-rootweakopportunity andBG-GAP notproved bythisfamily; existingindependentdynamiccreditentry nowexplicitlymapped']},
{'id':IDS[1],'disposition':'duplicate','targets':[P2,P],'units':['allfinitealpha quantifier andemptyroot legalcompleteSPE','allhistoriesA proof includingrepeatedsingletons/anyties','exactintegerF normalization allk/zero numerator','h_nbounds/ceil/squareexact/n3 coefficienttwo fails','tailcredit h-2/rootdebt h-3/globalmargin1','noncircularcreditinterface root/terminal/interval2-h<=C<=3-h','basefamily known/newprofitanalysis only andoriginalfiniteaudit codeonlyrole']},
{'id':IDS[2],'disposition':'integrated','targets':[P2,P],'units':['generalcredit sufficientinterface andcircularF-2Pexcluded','allbignegativeinterval; instanceswithoutnonnegativecredit','exactuniversal f_r(b,c) template onlyload/r/noinstanceinfo/twozeroaxes/negativeallowed','samef(1,n-1)tworealSPEfamilies inequalities/n>=16 analyticconflict','allowexclusive/theme/global/nonadditive notautomaticallysufficient','relativepercustomernegativecredit scalewhy sharedload insufficient','34completestrategy weakgapdiagnostics notallstrategies/nocreditfunctionoptimization','19instances backgroundF-P/currentu diagnostic notgeneralstate/transfer/rootboundary','no finite search decides universal credit orhalf; newresource preserves diagnostics precisely']},
{'id':IDS[3],'disposition':'duplicate','targets':[P3,P],'units':['staticB^rPNE allCineq/weakdominance proof/trueprefixguarantee notdynamicdominance','fiveclient full4nodes replypaytable/roots2/Phi5vs6/W5vs4 notVAorhalf counter','VAfullbg/r/rootM>=0,lastBR RES/ sufficientpositive-tax condition notproved','M0termwiseequality realrootB/actualBend/changedend excludesstrictsupersets/emptyboundary','emptyroot(2-1/m)|B| range dedupvsalreadyfrequencyk1','constantbg eq8eq9/query>1-2/r localization','5clientnecessaryLP point allvaluesnotSPE due rootB>=3/2','fourcomplementaryblockvariant x/y/z/v constraints andv<=y/3 vsstrict> conflict onlyspecificdesign','generalr>=2 VA/Mpositive tax stillneedrealrootB truthfulresponse']},
{'id':IDS[4],'disposition':'duplicate','targets':[P4,P],'units':['k>=1/mk+1 exactfullclientpartition/catalogBsubset+arbitraryextraNsubsets','actualC1...CkD andbothrealoffpathbranches intermediateavoidpool notimaginedpunishment','samev two branches oldprefix kept exact/formulas','x>=v>=d>=x/2+y andS/Y/OPT/W exactbound/algebra','k1no derangement/d0allzero/positiveeven d andpointwiseequality','sharpfamily existence separate Q/Bfullhistory proof notnecessaryconditionrealization','architectureescapes multiplecoverers/crossgroup/precoveredD notgeneralhalfproof','originaldiscovery/root/independentblindproof actualhistorynoexternalreview','allm halfcounterexample certificate duties withallorderednodes/realdeviations notbadterminal orLPpoint']}
]
js(E/'semantic-coverage-map.json',coverage)
readscope={'primary_sources':5,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'first_full_read':'GS related role; entire original mathematical texts read then and exact sameSHA now reuse, no pretended first read/repeated source audit','GY_work':'each original section mathematically compared to accepted GS self-contained objects, existing dynamic-credit entry and exact-remainder fulltext, frozen-version identities and evidence roles','primary_dispositions':{'integrated':1,'duplicate':4},'new_formals':1,'new_theorems_or_counterexamples':0,'preexisting_GS_objects_reused':4,'preexisting_GS_proof_objects':3,'existing_other_formals_fully_read_GY':2,'related_original_texts_sameSHA_reused':4,'related_extra_done':0,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'new_original_CLI_calls':0,'new_math_program_runs':0,'old_success_replays':0,'new_SPE_LP_BI_random_runs':0,'new_local_helper_calls':0,'network_or_lazy_fetch':0,'shared_Git_writes':0,'claim_done_checkpoint_show_calls':0,'real_board_account_auth_or_role_operations':0,'phase3_graph_import':0,'finite_counts':'15501/n4to8,n2to8,34strategies,19instances are originalMD reports, not newrun/sample/universalcoverage claims','original_audits_read':'no new originalcode/JSON fullread or claims of source acquisition failure; priorGS independent originalmathnotes preserved','unowned_format_defects':'actual28nonLF-C0 oldlemma plus1TAB oldresource, precise originalhash/offsets in report; frozen snapshots untouched; not auto-corrected','new_derived_builder_invocations':4,'derived_packaging_timing':'one preliminary body packaging, one finalization stopped by naive cases-linebreak delimiter count, one packaging inspected before release, one final packaging after removing escape-sensitive character comparison; none is a mathematical run','new_derived_builder_failures':1,'raw_local_sync_status':claim['local_sync']['status'],'actual_resolution':'Root explicit independent recovery preservation retained separately, no rewrite of needs-attention rawclaim','body_dependent_condition':'all4 accepted GS targets must currently exist and be exactwholebyte same as GS delivered originals before receipt finalization'}
js(E/'read-scope-and-evidence-status.json',readscope)
notes=[
('7329B原稿GS必要related已逐节全文读，本批核同SHA诚实复用，全部计数优化/背景定义/整数消元/严格域/信用值与原有限回归角色逐项比较。','其主要解析已完整在GS利润障碍，BG-GAP末尾另有现行动态信用资源，GY全文读该入口及末位余项引理确认v末位与min不能无条件换；零根机会缺口独立。','duplicate：不造第二个17/6障碍或重新跑15501旧计数；明确当前去向与既有BG-GAP，只补整体资源证据绑定，不视为新候选。'),
('5256B all-big主稿在GS已完整实读，GY完整字节SHA核同，复用全部历史策略、精确所有整数k规范化/平方人数无界量词/尾信用区间及原程序有限角色。','已完整包含于既有利润障碍：旧实例族的新F分析和任意有限实α范围未遗漏；同已读独审精确证明比对，不把任意n解析结论缩成n2to8测试。','duplicate：主证明与全部独有公式已归位，不新造反例族/新颖性/独立审稿人数，不重跑原有限审计，half正裕量1与原模型保持。'),
('5412B信用义务主稿在GS已全部数学读完，本批核同字节，逐段核 sufficient合同/循环定义排除/同r函数模板/两族冲突/未证状态和最后诊断段。','主体n≥16不可能性已自足；本批发现GS正文未完整记录最后34策略弱缺口/19实例背景利润诊断用途，故新资源精确补其对象、有限范围和不承担一般信用证明的边界。','integrated：已有障碍+一份有用证据资源保全部独有内容，没有新定理/扫描/信用构造；函数的instance-independence/双零轴承重，允许独占或非可加的未完成义务仍开放。'),
('9011B单色稿GS已全文读，GY核同SHA逐节对照原静态支配/五客户表/VA剩余税/M0/常背景/必要LP点及互补块失败，未新读程序或伪重跑。','现饱和查询引理包含全部解析/数值展示与未付正税；核全r和合法bg、空B/零客户、v_B取等、真枝末位和原末位两种BR，而非同背景静态势偷换。','duplicate：准确去向涵盖全部独有数学；保M>0/VA2未证和必要点非SPE，五客户4节点动态势反例不称half或VA反例，0新运行。'),
('7216B隔离主稿GS已全部实读，GY核同SHA复用完整假设/证明/等号边界/逃逸范围/来源与证书交付义务。','现隔离障碍完整保两个真实偏离枝、v早晚相同和旧前缀不变、x>=v>=d、OPT满覆盖见证及精确锐率、k1/d0/d偶数，锐例完整策略仍来自独立全历史族。','duplicate：仅条件架构上限而非所有SPE定理；半反例需合法整数客户/严格OPT>2W见证/全有序历史策略和所有真偏离比较，不能用必要条件点冒替。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 实际原认领回执未投影，五ID交集/owner/sourceSHA核齐。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# 五主稿与已交解析正文的精确绑定

5原件34224B在GS已实际全文读，GY原字节/SHA核同后逐节与四既有自足对象比较，不假装重新首读或重复程序。4duplicate：交叠利润/全A无界/M0单色/双向隔离；1integrated信用稿：主体证明已有，补34策略与19实例有限诊断的独有用途及未证接口资源。

现有动态信用入口及末位余项页GY全文实际读，BG-GAP已有入口，不当新候选；末位v界与min_i界清楚隔开。旧页发现28C0/1TAB和已丢TeX反斜杠，仅保原SHA/精确定位，不覆其他owner正文，数学状态不因此倒置。正文为1资源0新定理，已有GS目标只快照不覆盖。

0新数学/原CLI/SPE/LP/BI/随机/旧成功复跑/helper/network/sharedGit/账号或公屏行为。不把34/19或原15501/n2to8当新run次数。Root先推正文依赖再done；完整多组claim原字节保留，只按本5交集/owner核生成receipt。
''')
put(W/'relation-review.md',r'''# 阶段二关系

五源的解析主结论已有GS三数学对象：交叠F与all-big精确F同用排实例无关共同负载信用；M0查询从真rootB取等和两个真实末节点得出，不是静态支配的动态推论；隔离三比较只在指定结构内给上界，不把必要条件变完整策略。

本批资源新增34/19有限诊断的语义与未证对象，既有背景缺口BG-GAP按独立动态信用入口复用，并将真实末位v的已证界和min收益的候选分开。局部Bellman失败不反half，finite阴性不证一般信用，复杂化状态也不是完成。

四duplicate逐源说明全部实际读段和准确原件去向；不是按同标题/字数/已有done来源作自动重复判定。不重复原数学程序、SPE、LP或已成功检查，不进入第三阶段图导入，不强制连通。
''')
nextids=['efb09bff2fbae18ba384','c9ccc7817c179b3b1396','73e78b9e31ec4e9518da','4fa30e438229f7d5436d','66007ee43711768dbc97'];nextrows=[]
for i in nextids:
 x=next(x for x in previous if x['id']==i);q=REPO/'cleanup/progress'/f'{i}.json';pr=json.loads(q.read_text()) if q.exists() else None;b=(GS/x['preserved_path']).read_bytes();assert len(b)==inv[i]['size'] and sha(b)==inv[i]['sha256']
 if pr is None:nextrows.append({**inv[i],'local_path':str(GS/x['preserved_path']),'progress_observed':None,'read_status':'GS entire original text actually read as related; no primaryreceipt or originalprogram/report certification; can honestly reuse fullread after new actualclaim'})
js(W/'next-candidates.json',nextrows)
# Root has explicitly reported actual GS checkpoint and done pushes; bind those reports without fabricating a remote read.
gsprogress=[]
for i in ['45e100f077a8140e075a','2af13b75b47002b37dd9','f0a5782a749aa4578fc7','844fdc7b457c263049cf']:
 x=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert x['disposition']=='integrated' and x['source_sha256']==inv[i]['sha256'];gsprogress.append(x)
js(E/'actual-GS-publication-and-target-binding.json',{'actual_checkpoint_pushed':'50b4cd81ada9c439a7ace88af8911738188fb998','actual_done_pushed':'ff40e003c09886c872568e0cdddf29f6c457f176','report_source':'Root explicit parent message after body-only preparation; no claim of independent remote fetch by this agent','local_exact_target_hashes':[x for x in contexts if x['path'] in [P1,P2,P3,P4]],'actual_current_primary_GS_progress':gsprogress,'GY_raw_claim_kept_needs_attention':True,'separate_GY_recovery_kept':True,'repair_shared_application':'proposal-only in this packet; no two-target shared overwrite in copy whitelist'})

# Recovery proposals remain under evidence and cannot overwrite their two shared targets by transport.
rep=json.loads((S/E/'format-recovery/replacement-manifest.json').read_text());assert len(rep)==2
for x in rep:
 assert not (S/x['target']).exists()
 cp(S/x['before_path'],E/'repair-before-binding'/x['target'])
cp(Path(__file__),E/'build_delivery.py')
def tex_balanced(s,left,right):
 def count(delim):
  return sum(ord(s[i])==92 and s[i+1]==delim and (i==0 or ord(s[i-1])!=92) for i in range(len(s)-1))
 return count(left)==count(right)
assert tex_balanced(chr(92)+'['+'x'+chr(92)+']','[',']')
assert not tex_balanced(chr(92)+'['+'x','[',']')
assert tex_balanced(chr(92)*2+'[2pt]','[',']')

checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();ck('source exactsize SHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('source exactGitblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('raw23claim retained byteidentical',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and len(claim['ids'])==23);ck('actual5intersection no projection',set(IDS)&set(claim['ids'])==set(IDS));ck('rawattention notrewritten',claim['local_sync']['status']=='needs-attention' and json.loads((S/E/'actual-unprojected-claim-receipt.json').read_text())['local_sync']['status']=='needs-attention');ck('separate real recovery preserved',(S/E/'actual-independent-claim-sync-preservation.json').read_bytes()==resolutionpath.read_bytes() and resolution['missing']==resolution['different']==[] and resolution['unmerged']=='' and resolution['stash_kept'])
for x in owners:ck('sourceactualowner '+x['id'],x['owner']=='Boss4' and x['source_sha256']==inv[x['id']]['sha256'])
for x in contexts:ck('context snapshot '+x['path'],len((S/x['snapshot']).read_bytes())==x['bytes'] and sha((S/x['snapshot']).read_bytes())==x['sha256'])
for p in [P1,P2,P3,P4]:ck('currentGSactualtarget exactwholebyte '+p,(REPO/p).read_bytes()==(GS/p).read_bytes())
t=(S/P).read_text();ck('flatMATEK',all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('formalC0zero',not any(ord(c)<32 and c!='\n' for c in t));ck('formalwhitespacezero',all(l==l.rstrip() for l in t.splitlines()));ck('TeXbalanced',t.count('\\[')==t.count('\\]') and t.count('\\(')==t.count('\\)'));links=[]
for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
 if '://' in dest or dest.startswith('#'):continue
 n=posixpath.normpath(str(Path(P).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('actualrelative link '+dest,q.exists());links.append({'source':P,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
ck('newresource only 34and19evidence roles','34棵完整策略' in t and '19个实例' in t and '已有[动态信用来源入口]' in t);ck('BGcandidate not terminalv theorem','F_r(b)-P\\le r\\min' in t and 'F_r−P≤(r−1)v' in t);ck('1integrated4duplicate',sum(x['disposition']=='integrated' for x in receipts)==1 and sum(x['disposition']=='duplicate' for x in receipts)==4)
for x in receipts:ck('complete semantic receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() or (REPO/p).exists() for p in x['targets']))
ck('allnewmathzero',all(readscope[k]==0 for k in ['new_original_CLI_calls','new_math_program_runs','old_success_replays','new_SPE_LP_BI_random_runs','new_local_helper_calls']))
for x in rep:
 before=(S/x['before_path']).read_bytes();after=(S/x['proposed_path']).read_bytes();ck('exactrepairbefore '+x['target'],sha(before)==x['before_sha256'] and len(before)==x['before_bytes']);ck('exactrepairafter '+x['target'],sha(after)==x['proposed_sha256'] and len(after)==x['proposed_bytes']);u=after.decode();ck('proposed allC0andwhitespacezero '+x['target'],not any(ord(c)<32 and c!='\n' for c in u) and all(l==l.rstrip() for l in u.splitlines()));ck('proposedmetadata unchanged '+x['target'],before.decode().split('---',2)[1]==u.split('---',2)[1]);ck('proposedTeXbalanced '+x['target'],tex_balanced(u,'[',']') and tex_balanced(u,'(',')'));ck('proposal notsharedoverwrite '+x['target'],not (S/x['target']).exists());patch=json.loads((S/x['patch_json']).read_text());ck('encodedactualdiff exactSHA '+x['target'],patch['before_sha256']==x['before_sha256'] and patch['after_sha256']==x['proposed_sha256'] and patch['unified_diff'].startswith('--- a/'))
ck('originalC0exactcounts',[len(x['nonLF_C0']) for x in rep]==[1,28]);ck('correct3originalsourcesfullyread',sum(x['bytes'] for x in json.loads((S/E/'format-recovery/actual-correct-source-manifest.json').read_text()))==8038)
for x in nextrows:ck('actualnextlocal '+x['id'],Path(x['local_path']).exists() and sha(Path(x['local_path']).read_bytes())==x['sha256'] and x['progress_observed'] is None)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context','before','correct-frozen-source','repair-before-binding']);bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('allnewderived nonLF C0 trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_before_math_sources_unchanged':True,'proposal_format_clean':True})
put(W/'delivery.md',f'''# GY交付

5主源34224B全部于GS已related全文实读，GY核同SHA并逐节对照；4duplicate/1integrated、1新增证据资源，0新定理。4既有GS对象当前全字节核同后才出receipt；原23ids pushed {claim['remote_tip']} 回执仍needs-attention，另保实际Root stash恢复核，绝不改写或伪投影。

新资源补信用稿34策略/19实例有限诊断，BG-GAP另有当前入口，不冒新候选/普遍结论。4必要旧数学review同SHA复用，动态信用两页实际全文新读；其正确原README1250/数学6149/JSON639也全文读，代码没有本批读或运行。2完整格式修复提案含原beforeSHA/28C0+1TAB精确定位/全部丢反斜杠逐式恢复/原文及encodedpatch/完整after；只保evidence proposed，Root审读后串行beforeSHA核再apply，本白名单不直接覆写这两shared路径。

0新数学CLI/SPE/LP/BI/随机/旧成功/helper/network/sharedGit/真实身份行为。下一{len(nextrows)}件本地必要related已全文读，尚无primary认领receipt；Root新claim后可准确接续。正文依赖先pushed再done。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'newformal_nonLF_C0':0,'newformal_trailing_whitespace':0,'repair_proposed_nonLF_C0':0,'repair_proposed_trailing_whitespace':0,'scope':'byte/owner/rawclaim+independentrecovery/exactGSreuse/coverage/receipt/links/format/proposal bindings; no mathrun or formula correctness certified by counters'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':34224,'primary_lines':readscope['primary_lines'],'new_formals':1,'new_formal_bytes':(S/P).stat().st_size,'receipts':5,'dispositions':{'duplicate':4,'integrated':1},'checks':len(checks),'relative_links':len(links),'repair_proposals':2,'repair_apply_status':'not applied; before/proposed/patch only, no shared-target overwrite in whitelist','new_math_runs':0,'raw_claim_ids':len(claim['ids']),'raw_sync_status':claim['local_sync']['status'],'independent_recovery_retained':True,'claim_tip':claim['remote_tip'],'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
