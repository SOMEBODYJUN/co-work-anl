from pathlib import Path
import json,hashlib,re,posixpath,sys
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-four-subdirectory-audit-entry-identities';E=Path('tools/evidence/four-subdirectory-audit-entry-identities');W=Path('cleanup/workspaces/Boss4/r3-four-subdirectory-audit-entry-identities-next')
IDS=['ed0a6bb8caa16847d4d1','70a01bf10930353cc5a9','3b7f90e41798f75e91a2','448c9fc7f2c58db34353'];P='archives/customer-attraction/state/资源/四个子目录入口的审计实现与复用身份--资源.md';PH='archives/customer-attraction/state/定理/真实退出缺陷的统一与异质前缀修复--定理.md';PL='archives/customer-attraction/state/引理/真实偏离枝的收益与覆盖范围--引理.md';PJ='archives/customer-attraction/state/资源/来源回撤与异质修复入口的全树付款边界--资源.md';PB='archives/customer-attraction/state/候选/后继超额保留的最小收益价格桥--候选.md';JH=C/'r3-cag-reserved-debt-restart-and-triangular-primary';JN=C/'r3-origin-retraction-and-credible-entry-resources'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
# No execution before parent supplies actual raw JU claim. No projected receipt.
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids'])
resolutionpath=C/'boss4-r3-next-jp-jq-jt-ju-js-atomic-claim-sync-preservation.json';resolution=json.loads(resolutionpath.read_text());assert claim['remote_tip']=='7963768ac29480c33567e42b2c82937bba0e8bbb' and claim['local_sync']['status']=='needs-attention' and resolution['missing']==resolution['different']==[] and resolution['unmerged']=='' and resolution['stash_kept'] and resolution['untracked_count']==2 and len(resolution['tracked'])==2 and all(x['same'] for x in resolution['tracked']) and resolution['stash'] in claim['local_sync']['detail']
mp=C/'learning-jn-next-entry-and-blind-review-inputs/local-export-manifest.json';m=json.loads(mp.read_text());primary=[];owners=[]
for i in IDS:
 x=next(x for x in m['rows'] if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/x['path'];cp(x['local_path'],q);primary.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_mode':'JU actualcomplete sourceMD text/math afterJN44freeze inauthorized preclaimprep, notmerely previousbyteavailability; actualclaim/owner/SHA guard beforefinalreceipts'})
assert sum(x['size'] for x in primary)==4686
js(E/'source-manifest.json',primary);cp(mp,E/'original-five-export-manifest-with-owned-blind-source.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json');cp(resolutionpath,E/'actual-independent-sync-resolution.json');js(E/'actual-primary-ownership-snapshot.json',owners)
jhmap=json.loads((JH/'tools/evidence/cag-reserved-debt-restart-and-triangular-primary/resource-targets.json').read_text());CP=list(jhmap.values());PS=jhmap['b1f6a04d07d6835f8d19'];PE=jhmap['f3f1ec02ccbbf002fe96'];PM=jhmap['7e9387a45a48bb0410fa'];PO=jhmap['89f64465d29696938faf'];contexts=[]
for p in [PH,PL,PJ,*CP,PB]:
 b=(REPO/p).read_bytes();q=E/'context'/p;cp(REPO/p,q);z={'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'actual complete currentformal or frozenotherlineformal reading; current wholebytes checked before receipt'}
 if p in CP:assert b==(JH/p).read_bytes();z['equals_read_JH_delivery']=True
 if p in [PL,PJ]:assert b==(JN/p).read_bytes();z['equals_read_JN_delivery']=True
 contexts.append(z)
assert sha((REPO/PS).read_bytes())=='2d73316de5a2ba1648aac23dafbca038ab0d95dc35c3522a0a6596a238eedb09'
js(E/'context-manifest.json',contexts);cp(JH/'tools/evidence/cag-reserved-debt-restart-and-triangular-primary/resource-targets.json',E/'actual-JH-target-map.json')
programids=['d3d430c1938a29ce99c2','48a2a60361a45c8678ed','f390f53649e416176fef','11e83f89dec391d5b2fe','73780fead77dbf46e31f','06068e36ffe4499b4538','be025ded1b19d3bde56c','fefdf3d7d3b163ccccc5','0833067167a458cefed7','09b45477ce038ad47480','812138243ac7b61465a0']
js(E/'referenced-program-report-inventory-metadata-only.json',[{**inv[i],'read_status':'inventory metadata andsourceMD describedrole only; rawprogram/report notfullread orrun byJU'} for i in programids])
f='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id','customer-attraction/four-subdirectory-audit-entry-implementation-identities'),('kind','resource'),('type_tag','资源'),('title','四个子目录入口的审计实现与复用身份'),('status','four-entrytexts-completely-read; mathematics-exact-reuse; originalcode-not-audited'),('summary','四README全部用途/读序归位；分开credible与parent同名75产品实现，精确复用真实枝/尾储备/ξ-η与最小收益行候选，不重复造候选、定理或旧运行。')])+'source_refs:\n'
for x in primary:
 for y in x['sources']:f+='  - '+json.dumps('source:'+y['commit']+':'+y['path'],ensure_ascii=False)+'\n'
f+='---\n\n# 四个子目录入口的审计实现与复用身份\n\n'
body=r'''## 四入口的范围与真实读取

1577B credible、1254B direct、722B menu、1133B optimal_gap，共4686B，全部完整实读，包括页尾备份/无Git/无外部消息声明与后加bounded review段。两个冻结来源同字节，按各sourceID保原件。不把另已由JH认领的3920B blind稿混成本4主源；不把当轮研究者命令或停止扫描当当前cleaner指令。

单位客户/单位玩家、共同有限非空目录、固定每个有序历史的纯SPE，空/重复/零及任意平局保留。原一般half OPEN与当前五人half另已证、六人仍未由本页解决分开；原“不产生新half范围”保历史和本机制边界。以下只新增资源身份，数学按完整现目标逐项复用，0新定理/游戏/数学运行。

## credible：两个同名75产品程序必须分开

1577B入口主数学由[完整异质修复定理](../定理/真实退出缺陷的统一与异质前缀修复--定理.md)全保：任意标记银行/固定层蛋糕、全部有序历史与联合坐标偏离，损耗2Σδ+maxδ改善统一(2j+1)maxδ，零缺陷另拼合。先盲重构再全文对稿、原内部审查未fatal、外审/新颖性未认证均为实际历史，不算本次新独审。

原作者marked-bank程序及JSON只有限核任意标记规则，非全m证明。作者75客户产品是**credible子目录**实现；父方产品在parent子目录，不能把两个同名文件当同一个实现、相同SHA或同一次运行：

| 程序/输出 | sourceID与大小 | 冻结SHA256与证据身份 |
| --- | --- | --- |
| credible/audit_heterogeneous_product.py | f390f53649e416176fef，5862 B | 0dec865dfd88f4530c0e5839ab24313a03da43bb6fc9c042d35285ded2a0c0bb；本credible入口所指作者实现 |
| credible/audit_heterogeneous_product.json | 11e83f89dec391d5b2fe，73799 B | 31cea0eaccac2a55a16663119f9bc0760609e2d41f59c16469c813ffa37111f1；其生成输出，未本批全字段读 |
| parent/audit_heterogeneous_product.py | 73780fead77dbf46e31f，6096 B | 6870c2baf0adc700d3efb671590b37920ca1a6fccc8efd9c60e13c1c6eb1c5c5；根README所指父方另实现 |
| parent/audit_heterogeneous_product.json | 06068e36ffe4499b4538，1136 B | 47236cd248459d5dd8b4dcc2bf61dc5966f372da11d7e6bdad4dd75b97aedd51；父方输出，未本批全字段读 |

此表来自inventory精确元数据，不宣称从文件大小推断输出字段或实现独立性。原credible入口报75单位客户、缺陷(5,9)、层{1,2}/{2}、343有序决策历史、6174联合比较、W71/OPT75，gap成本37对统一45，均按原MD记录；现定理已保其数学/回归角色。源根README父方另报5832最优终局，不能因为主数相同就把它反填作者JSON字段。本次没有读或执行这两py/JSON，不把历史“standalone/不导solver”升成当前代码审计。

target checkpoint的重复punisher和去PB背景两尝试已在[共享遗漏真实末位资源](共享遗漏惩罚与无背景移植的真实末位障碍--资源.md)完整保：前者要其他真实枝先消除末位D外选项，后者两个充分标量IC相冲突。都非half反例/一般不可能性；E内共同份额须精确抵消，只有其他动作也避E才具体为b/r。源称只写自己的credible子树、没有commit/push/外部消息只保历史，不授权当前真实账号动作。

## direct与menu：完整覆盖者精确duplicate

1254B direct入口的全部数学与程序用途已由[额外槽饱和与枝范围资源](额外槽饱和势与真实偏离分支覆盖上界--资源.md)及[真实枝引理](../引理/真实偏离枝的收益与覆盖范围--引理.md)自足保：

- 旧静态OPT≤2mθextra是共享计数，不重认福利信用；θ的下标包含一个额外查询者，竞争背景m槽、真实游戏仍m人。
- 自由入场势只给固定multiset插删饱和，不能控制同原σ早期改行动后的整尾reset。所有真实最大主题枝有Cauchy覆盖**上界**，不等actualW下界或已付OPT。
- 八旧完整SPE输入/证书各不同，脚本按有序policy重建actual路径，用Fraction精确枚举额外槽背景；保存脚本不新增运行，未重新认证各输入全部IC。无违不证候选或全策略锥。
- 原五人结论只条件指本路线；现五人已另证。更强逐人theta桥已被完整银行族否定；聚合桥不因逐人失败自动否定。原direct入口没得到一般新福利下界。

722B menu入口的全部精确数学/程序角色由[完整推送储备资源](完整终局推送的自身折扣与末两位储备--资源.md)完整保：完整m槽P、删当前槽C、真实当前D不能互换；额外自身折扣、真末两人L/V/Q及actual末列reserve均正确，后两reserve不能双花。m5尚有三项early debt未被这套恒等式支付，不能据原OPEN说当前五人half未证。

probe仅一份形式完整策略锥、63非空客户型、两个预选p、浮点阴性无精确对偶；不成该锥认证，更不成所有输入定理。原“actual-root Mpath OPEN”没有被一个非零任意背景PB子SPE反例替代，也不等银行否Mfull。这里不重跑同阴性扫描，EARLY-PAY或较弱真实Mpath共同付款仍是原资源的准确义务。

## optimal_gap：最小收益行候选已有完整去向

1133B原入口列stopping_barrier：非法restart替代、保ξ/η一般式、m5代入及一个未证最小收益行接口。原全文7771B已由JH资源[最优补全真实重启差](最优补全的真实重启差与保留信用停界--资源.md)自足保，JU完整实读该目标后，并与其清洗者核过精确范围。**不另发同候选。**

特别同一完整σ、actual全局最小收益位置i、达到全局OPT_m的**m元组**T_j，R_i=Σ_j u_i(h_i,T_j;同原真后继)。若
\[
R_i+\sum_{j>i}(u_j-u_i)\ge OPT_m-W,
\]
则IC R_i≤m u_i和(i−1)u_i≤Σ_(j<i)u_j给左端≤i u_i+Σ_(j>i)u_j≤W，从而half。这只是未证接口的正确充分性，不证明候选自身；不换成剩余r元组、不冻结强制后继、零实例不需除法。该R_i是真子树收益行，不是[全客户价格B(u_i)桥](../候选/后继超额保留的最小收益价格桥--候选.md)的左侧，不能仅按类似后继超额预算判为同一定义。

stopping原数学中的ρ/ξ/η/θ/Γ、静态低λ和C_A−C_B两真尾reset已在该资源完整保。m5旧基线6049/15625不反现五人定理，也不证明更强保ξ省η候选。test_eta_budget及JSON只是seed723/1000样本有限诊断，完整count-based BI为合法子类而非所有有序历史策略；原入口不提出更多同样采样，不能把阴性当全称正面。

最后bounded review两项亦已保：triangular盲稿在读application前独立重构greedy iff、逐坐标最大解/首失败负cut，是原读序，不算JU新的blind；[三角工具资源](非负严格三角回撤的最大解与失败割--资源.md)明确泛非负t无需行和1、价格可>1，仅真实来源路由才另有[0,1]界。application是固定flow回撤含放松d'≤旧u规范化后的单一2u cap，不证明全输入成功或新真实IC。[来源回撤入口资源](来源回撤与异质修复入口的全树付款边界--资源.md)已保共同角色余额，不能一context一份u反复付款。

## 来源与执行边界

[四原件](../../../../tools/evidence/four-subdirectory-audit-entry-identities/source-manifest.json)保实际全文范围/两个冻结版本/原多组认领交集与现owner/sourceSHA；全部JH对象逐字节绑定其已全文读的交付版本，最小收益行目标SHA256 2d73316de5a2ba1648aac23dafbca038ab0d95dc35c3522a0a6596a238eedb09。数学来源与程序/报告元数据分开，不额外done JH五主或所引用py/JSON。

一次safe localhelper尝试下一五原程序，0export/5missing，原missing清单完整保，不同blob重试/网络回退均0。这里只报告那次本地不可得，不说全局永久没有源；若Root后来正常show，保独立新读取记录而不覆盖旧missing。现JU新数学程序、原CLI、LP/BI/随机、旧成功复跑全0；不借来源回撤旧PASS扩到75作者/父方两个程序。新资源保准确用途，不导旧图或第三阶段mapper、不认证外审和新颖性。
'''
put(P,f+body);js(E/'formal-resource-manifest.json',[{'path':P,'bytes':(S/P).stat().st_size,'sha256':sha((S/P).read_bytes())}])
missingmp=C/'learning-ju-next-program-inputs/local-export-manifest.json';miss=json.loads(missingmp.read_text());assert miss['rows']==[] and len(miss['missing'])==5;cp(missingmp,E/'first-local-program-availability-five-missing.json');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
coverage=[{'id':IDS[0],'disposition':'integrated','targets':[P,PH,PO],'units':['allfullmodel/oldOPENcurrent5vs6 scope','arbitrarymarkedbank/layercake/fulldeviation/zeroendpoint/cost2sumdelta+D vsuniform2j+1D allproof alreadyformal','historyblind-beforeauthor thenindependentreview/nofatal/no externalnovelty notnewreview','author markedbank exactfinite notallm/author credible75product vs parent samebasename distinctcodeSHA andJSONsize','75deficits5,9/layersI12,I2/343orderedhist6174jointcomparison/cost37vs45/W71OPT75 sourceMDreport notnewrun','targetexactrepeatedpunisher reservoiroutsideoption/PB literalconflict nocounterexample/nogeneralimpossibility','onlyactorcredible subtree andnoGitexternalmessages frozenhistory no newcommand']},
{'id':IDS[1],'disposition':'duplicate','targets':[PE,PL,P],'units':['fullgeneralunitmodel/originalhistoryquantifiers','oldOPT2mthetaextra staticnotnew welfarecredit','unprovedsaturationdynamicexchange/givenSPEsuffixreset vsglobalpotential','alltruebranchCauchyupperbound notactualrootWlowerbound/nopaidOPT','m5routeconditionalnotcurrent5theoremunproved','8existingcertonce exactFraction mbackgroundenum/orderedpolicy actualpath/notnewICaudit orscript-save run','currentindividualtheta bankrefuted vsaggregate distinct/no broadnegativeextension','oldsubagentnoGit/msgs frozenrole']},
{'id':IDS[2],'disposition':'duplicate','targets':[PM,P],'units':['rootactualMpath vsarbitraryPBbackground/SPEreachability distinct/Mfullbank notMpath false','fullterminalowndiscount vsdeletedforcedtail /exactpaidtwolast reserve /notdoublecountactualcolumnandpushdiscount','earlydebt/m5threeearlyterms notnewfullpayment/current5trueelsewhere','singlefixedformalpolicycone63types/twopreselectedp/floatnegative/noexactduals/nopositiveproposal','EARLY-PAYorweakMpath trueICobligation notresolvedbyrepeatingnegative scan','noGitexternalmsg history notexecutable']},
{'id':IDS[3],'disposition':'duplicate','targets':[PS,CP[-1],P],'units':['invalidrestartsubstitution/C_A-C_B unpaidsigned truechild/retainedxi eta generalidentity/m5oldpressure separatecurrent5','minimalpayoffrowcandidate R_i fromglobaloptimalmtuple/sameoriginalsigma/fullIC/minimumrole sufficientproof completeJHnotnewpriceB object','test_eta finite1000seed723 negative notproofengine/fullcountBIlegal subclass no newruns','nexttrue successorICaggregate notlowlambda alone','boundedreviewblindbeforeapplication greedyiff/greatestness/explicitnegativecut history','applicationfixedflowdprime relaxation/common2ucap/notuniversalsuccess/no newIC']}
]
# Exact blind target is selected by source ID, never by dictionary order.
coverage[-1]['targets']=[PS,jhmap['657caca9d3baac5508e2'],P]
js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':4,'primary_bytes':4686,'primary_lines':sum(x['lines'] for x in primary),'primary_first_full_read':'JU authorizedpreclaim actualfull fourREADME paragraphs/list/table/endnotes afterJN44frozen; notfake postclaimfirstread','dispositions':{'integrated':1,'duplicate':3},'new_formals':1,'new_theorems_candidates_or_game_instances':0,'new_math_program_runs':0,'original_math_CLI_calls':0,'old_success_replays':0,'LP_BI_random_runs':0,'raw_program_JSON_fullread':False,'inventory_program_metadata_only':programids,'current_formal_complete_reads':len(contexts),'JH_complete_formals_read':5,'JH_otheragent_confirmation':'facility_front_resume explicitlyconfirmed fullminrow contract inPS SHA2d73316...; JU wholetext actuallyread','JH_fiveprimary_not_done_by_JU':True,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'raw_claim_status':'pushed','raw_local_sync_status_preserved':'needs-attention','independent_sync_resolution':'actual Rootproof: preservedstash2tracked2untracked/0missingdifferentunmerged; originalreceipt notrewritten synced','helper_calls':1,'local_blob_attempts':5,'local_exports':0,'local_missing_blobs':5,'missing_retry_calls':0,'code_missing_scope':'firststrictlocalblob attempt only; laterRootnormalshow allowed independenthistory notretroactive localPASS','next_candidates_metadata_scan':'localexisting authorizedexportmanifest metadata/byteSHA revalidation, notnew semanticreading ornetwork','shared_Git_writes':0,'claim_done_checkpoint_show_calls':0,'network_or_lazy_fetch':0,'real_board_account_auth_operations':0,'phase3_graph_import':0,'derived_packaging_builder_calls':1,'derived_packaging_builder_failures':0}
js(E/'read-scope-and-evidence-status.json',scope)
notes=[('1577Bcredible README全部条目/数字/审查先后和最后个人分支/noGit/外部消息段全文实读。','现完整异质编译、JH共享遗漏与JN入口逐项比对，数学已自足；独有credible作者75实现与parent同名不同字节逐sourceID/size/SHA归位，不以相同343/6174计数当同代码或一次run。','integrated：一资源保准确作者/父方程序/JSON身份及有限报告边界，0新代码读/运行，不从未外审标签抹去有用已证数学，不执行旧角色或真实消息/Git。'),
('1254Bdirect README全列表/尾段实读，原8例诊断和脚本保存不新增检查、静态公式旧身份完整保。','JH额外槽资源与JN真实枝引理完整同SHA比对，静态计数/势最大/动态reset/所有偏离枝Cauchy及八原例各范围完整覆盖；按当前银行修逐人theta旧OPEN，聚合仍另判断。','duplicate：全部独有数学和程序用途有精确现目标，不因newREADME再发同引理。分支上界不是actual福利下界，原m5方法条件不反当前五人已证；0重跑八例或旧同SHA。'),
('722Bmenu README两条及最后EARLY-PAY/不再阴性段全文读，准确fixedcone/63类型/两p/floatno dual范围。','JH完整推送资源全文保P/C/D、尾L/V/Q和末列不双花/earlydebt/m5及rootMpath量词，已覆盖所有本入口用途；PB非零背景不替actualroot问题，银行Mfull不是Mpath自动反例。','duplicate：无需新储备或菜单候选，原浮点诊断不认证锥/全称、不加原CLI或LP；无Git/外部消息仅源历史，不切当前cleaner身份。'),
('1133Boptimal README两节全部全文，含后加bounded review的两独审先后/放松d prime/未新增IC与universal状态。','与JH7771数学资源真全文/清洗者确认及SHA2d73316...核：全局最小actual位置i、全局最优m元组T及R真强制行的未证充分候选已完整自足，不误判现B(v)价格桥或剩余r行；blind/application工具按准确固定flow范围。','duplicate：不再发同候选/greedy算法或新blind审查，seed723/1000阴性不作proof engine，0额外done JH主稿/引用程序输出；五人现定理未证明更强该候选，跨真尾restart仍需付款。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原23ids claim保完整pushed/needs-attention；Root独立恢复proof原字节保，核本4owner/sourceSHA后封receipt，不伪写synced。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# JU四子目录审计入口

四README4686B全文实读，1integrated+3duplicate，一新资源；没有新候选/引理/游戏，0数学程序/原CLI/LP/BI/随机/旧成功复跑。JH五现资源全部全文实读并核发布树与成熟stage全字节一致，最小收益行合同已完整自足，不再重复造候选；可信75作者与父方实现同名不同SHA必须分开。

原23ids实际claim为pushed，local_sync原needs-attention保持。Root独立resolution明确stash保留、2tracked/2untracked全部同字节、0missing/different/unmerged，本4owner/sourceSHA核。没有将原receipt改为synced。

一次safehelper5程序全missing，原清单保，不重复/回退网络。inventory元数据/来源README角色不等真实源码或JSON全读。下一候选只从现已授权本地导出清单复核未领字节，未全文/未primaryreceipt。Root先推正文依赖再done，0sharedGit/身份账号公屏/第三阶段mapper。
''')
put(W/'relation-review.md',r'''# 阶段二关系

credible作者75产品代码/输出与parent另实现必须各source身份保留；同名/同数值不证同SHA或同一次运行。程序角色来自实际README全文，完整源码与真依赖没有读就不冒认证。

direct、menu、optimal数学全部已有精确自足目标，逐段duplicate而非依文件数/标签判断。最小收益行使用global最优m元组及同原σ的真实强制行，非剩余r元组或全客户B(v)价格；JH已给完整条件推导，候选未证。Cauchy枝覆盖是上界，tail储备仅付末两位，早期不同真尾reset仍待共同付款。

源旧五人方法未过与现五人已证不冲突，银行否逐人theta不反聚合，Mfull被否不自动反rootMpath。原盲重构、application有限合同与本次知情清洗分别保，不新增外审/新颖性；0额外done JH五主或引用py/JSON/next，0phase3图导入或强造连通。
''')
# Three actual stillunclaimed mathematical nextsources already present in authorized local caches.
scan=json.loads((C/'ju-prework-available-local-candidate-scan.json').read_text());nextids=['b28e13d9c38be46a6f6c','b604a83b0410f853c05e','0d48e26ef6aadd2437dc'];nextrows=[]
for i in nextids:
 x=next(x for x in scan if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=REPO/'cleanup/progress'/f'{i}.json'
 if not q.exists():nextrows.append({**v,'local_path':x['local_path'],'authority_manifest':x['authority_manifest'],'progress_observed':None,'read_status':'actual localbytesverified only; notfullsemanticread/claimed/receipt byJU'})
for j,x in enumerate(nextrows):cp(x['authority_manifest'],E/'next-original-export-authorities'/f'{j+1}.json')
js(W/'next-candidates.json',nextrows);cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tb(s,l,r):
 def count(d):return sum(ord(s[i])==92 and s[i+1]==d and (i==0 or ord(s[i-1])!=92) for i in range(len(s)-1))
 return count(l)==count(r)
for x in primary:
 b=(S/x['preserved_path']).read_bytes();ck('sourceSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('rawclaim full23byteidentical',len(claim['ids'])==23 and (S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes());ck('actual4subsetownerSHA',set(IDS)<=set(claim['ids']) and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('rawattentionnotfakesynced',claim['status']=='pushed' and claim['local_sync']['status']=='needs-attention');ck('independentresolutionretained',(S/E/'actual-independent-sync-resolution.json').read_bytes()==resolutionpath.read_bytes() and resolution['missing']==resolution['different']==[] and resolution['unmerged']=='' and all(x['same'] for x in resolution['tracked']) and resolution['stash_kept'])
for x in contexts:ck('contextreadbytes '+x['path'],sha((S/x['snapshot']).read_bytes())==x['sha256'] and len((S/x['snapshot']).read_bytes())==x['bytes'])
ck('minrowtargetexactfullreadSHA',sha((S/E/'context'/PS).read_bytes())=='2d73316de5a2ba1648aac23dafbca038ab0d95dc35c3522a0a6596a238eedb09');ck('allJHpublishedtreeequalsfullreadstage',all((REPO/p).read_bytes()==(JH/p).read_bytes() for p in CP));ck('two75codedistinctbyteidentities',inv['f390f53649e416176fef']['sha256']!=inv['73780fead77dbf46e31f']['sha256'] and inv['11e83f89dec391d5b2fe']['sha256']!=inv['06068e36ffe4499b4538']['sha256'])
t=(S/P).read_text();ck('flatMATEK',all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('formalC0zero',not any(ord(x)<32 and x!='\n' for x in t));ck('formaltrailingzero',all(l==l.rstrip() for l in t.splitlines()));ck('actualTeXbalance',tb(t,'[',']') and tb(t,'(',')'));links=[]
for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
 if '://' in dest or dest.startswith('#'):continue
 n=posixpath.normpath(str(Path(P).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('link '+dest,q.exists());links.append({'source':P,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
ck('all4sourcesroles',all(x in t for x in ['credible','direct','menu','optimal_gap','bounded review']));ck('minrowmnotrnotprice','m元组' in t and '不换成剩余r元组' in t and '不是' in t and '全客户价格' in t);ck('missingonlylocalnotforever','0export/5missing' in t and '不说全局永久没有源' in t);ck('all4receipt1integrated3duplicate',len(receipts)==4 and {x['id'] for x in receipts}==set(IDS) and sum(x['disposition']=='integrated' for x in receipts)==1 and sum(x['disposition']=='duplicate' for x in receipts)==3)
for x in receipts:ck('completereceipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() or (REPO/p).exists() for p in x['targets']))
ck('exact1formal',set(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))=={P});ck('no oldsuccessornewmath',scope['new_math_program_runs']==scope['original_math_CLI_calls']==scope['old_success_replays']==scope['LP_BI_random_runs']==0);ck('first5localmissingnotretried',miss['rows']==[] and len(miss['missing'])==5 and scope['helper_calls']==1 and scope['missing_retry_calls']==0)
for x in nextrows:ck('actualnextmetadataavailable '+x['id'],sha(Path(x['local_path']).read_bytes())==x['sha256'] and not (REPO/'cleanup/progress'/f"{x['id']}.json").exists())
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context']);bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('allnewderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_original_context_unchanged':True})
put(W/'delivery.md',f'''# JU交付

4primary4686B/{scope['primary_lines']}行完整实读，1integrated+3duplicate，一新资源；0新数学对象发现/候选/游戏/程序/原CLI/LP/BI/随机/旧成功复跑。JH五自足资源与JN相关对象全文比较，最小收益行准确duplicate，不再造同候选。两个75同名程序/JSON仅库存元数据和入口角色区分，不冒源码认证。

原{len(claim['ids'])}ids claim{claim['remote_tip']}真实pushed、local_sync原needs-attention保持；Root独立恢复proof原字节保，stash保留/2tracked2untracked同字节/0missing/different/unmerged，本4owner/sourceSHA核。没有伪写synced/投影原receipt。

下一5代码首次localhelper全missing，不重试；另实际已授权本地缓存核得{len(nextrows)}未领数学源共{sum(x['size'] for x in nextrows)}B，只byte未全文/未claim。Root若正常show代码，保单独读取历史不覆盖旧missing。Root先推正文依赖再done，0sharedGit/账号公屏/第三阶段mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'scope':'exactsource/owner/raw23claim+independentresolution/JHfullreadtargets/metadataonlycode/coverage/links/format/transport','mathematics':'no newmathrun, existing selfcontainedproofs/conditionalcandidate precise reuse; these checks do notprove globalhalf ororiginalcode claims'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':4686,'primary_lines':scope['primary_lines'],'new_formals':1,'formal_bytes':(S/P).stat().st_size,'receipts':4,'dispositions':{'integrated':1,'duplicate':3},'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'new_original_CLI_runs':0,'old_success_replays':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'raw_local_sync':'needs-attention-preserved-plus-independent-recoveryproof','next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
