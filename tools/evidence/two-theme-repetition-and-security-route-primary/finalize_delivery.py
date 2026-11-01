from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-two-theme-repetition-and-security-route-primary';E=Path('tools/evidence/two-theme-repetition-and-security-route-primary');W=Path('cleanup/workspaces/Boss4/r3-two-theme-repetition-and-security-route-primary-next')
IDS=['b874ab55470546ce897b','0ceafe0cf6073351cde8','cae0027749fb8ec7bd95','24a3ec78bc2dfa4cd31f'];P1='archives/customer-attraction/state/定理/重复首主题终局的严格二倍界--定理.md';P2='archives/customer-attraction/state/资源/两覆盖结构与成对安全工作区的准确接续--资源.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def rd(p):return json.loads((S/p).read_text())
claimpath=R/'boss4-r3-next-fu-claim.json'
if not claimpath.exists():
 print(json.dumps({'status':'waiting-actual-claim','path':str(claimpath),'successful_semantic_receipts_written':False}));raise SystemExit(0)
claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==set(IDS)
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};owners=[]
for i in IDS:
 x=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[i]['sha256'];owners.append(x)
cp(claimpath,E/'actual-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners);cp(Path(__file__),E/'finalize_delivery.py')
primary=rd(E/'source-manifest.json');related=rd(E/'related-source-manifest.json');contexts=rd(E/'context-manifest.json');run=E/'runs/new-convex-correction-001';meta=rd(run/'run-metadata.json');report=rd(run/'stdout.json')
scope={'primary_sources':4,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'primary_read_status':'7711B full FT related reading reused after exactSHA check; other3 README5951B first full semantic reading FU, previousFT availability only','new_related_code_sources':1,'new_related_code_bytes':5375,'related_code_role':'background_pair_probe.py complete code/real CLI/config/LP input contract read, not run or extra primary done','full_current_formal_contexts_fresh':5,'full_previous_same_SHA_formal_contexts':len(contexts)-5,'additional_partial_context':{'path':'archives/customer-attraction/state/障碍/完整策略树平均与独立同分布福利桥--障碍.md','actual_read':'lines1..115 only; no full-file claim or primary completion'},'new_mathematical_execution_count':1,'new_execution_type':'new exact polynomial identities for newly discovered source convex-weight defect; all symbolic coefficients and one m2 sanity, no game','new_execution_elapsed_seconds':meta['elapsed_seconds'],'new_execution_exit':meta['exit_code'],'original_CLI_calls':0,'old_success_replays':0,'new_SPE_or_game_history_checks':0,'new_LP_or_Nash_solves':0,'new_random_or_matching_scans':0,'new_check_code_sha256':meta['code_sha256'],'new_check_stdout_sha256':meta['stdout_sha256'],'source_correction':'lambda numerator m²-m-1 becomes m²-m+1; interval remainder becomes m(3m-1); source gamma/beta valid with repair','correction_not_applied':'frozen original and shared prior pages remain exact bytes; separate proposed-only source and before/after SHA given','old_named_audit_not_materialized':'audit_two_theme_terminal.py and two_theme_terminal_audit.json have no matching frozeninventory/current evidence-tree names; original code/run not read or certified','safe_local_helper_calls':2,'local_blob_attempts':10,'local_exports':1,'local_missing_blobs':9,'new_source_code_actual_id':'2db24df0ce02d6fd610c','missing_dependencies':['211d296e09ebde9261d7','18d110e80f374a53458a','c10125cad4e93091bac7','79a007ae223609d3137c','4789e4082bbf9cfe27ca'],'missing_next_programs':['cc432169e3e815183107','2acc558092002deedd85','4c4118f59f0c8493e2f0','1101265dd6065cf6fbcd'],'additional_cached_candidate_lookup':'local export manifests only; availableMDs24 observed with exact bytes/no progress, no mathematical reads or new Git/blob attempts','derived_builder_calls':1,'derived_builder_failures':0,'network_or_lazy_fetch':0,'shared_Git_writes':0,'clean_show_claim_done_checkpoint_calls':0,'phase3_mapper_or_graph_import':0,'math_status_boundaries':['AB/repeated-first theorem valid with explicit correction; BB/general two-support distinct','frequency condition sufficient, not necessary for all SPE','PB arbitrary legalbackground refuted, actual-root reachability not proven; realaggregate not refuted','actualscaled M exacttax refuted by another13player case, iidZ/fullterminaltax/truev different','260 authorfinite floatingcones not originalrun reproduced or globalproof']}
assert scope['primary_bytes']==13662 and scope['primary_lines']==273;js(E/'read-scope-and-evidence-status.json',scope)
js(E/'unmaterialized-named-audit-files.json',{'names':['audit_two_theme_terminal.py','two_theme_terminal_audit.json'],'frozen_inventory_same_name_matches':[],'current_formal_evidence_tree_same_name_matches':[],'read_or_executed_original':False,'scope':'actual rg on inventory and archives/customer-attraction/tools/evidence; not a claim about every private external cache','source_claim':'author says exact formula/boundary/SPE audits, but unprovided implementation is not taken as authentication of defective formula'})
coverage=[
{'id':IDS[0],'units':['ClaimA complete model/m>=2/AandBmaycoincide/W0m1 edges','all3realIC and expandedU_R/U_B/U_T/CLOSE residual','allm optimal union P/L budgets repeated allowed','originalweight line143 and interval line149 defect preserved','correctlambda+1 exactsolution and intervalm(3m-1)','originalgamma/beta unchanged/fullpositive proof/m2m3m5 constants','ClaimB lastA deviation and lastBbudget/frequency sufficient direction','fiveplayer two-support structural corollary/current generalfive theorem separate','source relationships last-rank/containment/commoncatalogclosure','old internal reconstruction and unmaterializedaudit originalcount notcertified','newonce polynomial check exactdomain notSPE/LP/globalhalf'],'targets':[P1,P2]},
{'id':IDS[1],'units':['R31 historicalpersonalrole/newID/restoreclone/origin/main/sixresearcherconfiguration/privatecommunication/checkpoint status','fullmodel arbitraryoldn target allhistory/empty/tie/repeat0','header2026-10-25 arbitrarybackgroundpairrefuted viaweakerPBextra notrootactual','strongweak iidnottruev','terminaltax probe/formerbad-schema skip floatingcandidateexactrecovery','all7directories mathematical roles','weakQ/additiveprice candidates notV/R orproved','localassets notautomatically shared or canonical','oldnextinstruction/independentreviewnotnewroleorpermissionflow'],'targets':[P2]},
{'id':IDS[2],'units':['truev_r(b) withr-1opponents independentquery fullmodel','firsttwopaircandidate and valid grouping/embed/oddlast conditionalaggregate','currentheaderrefutation versusbodyoldOPEN','actualbackground probe integerinitialpolicy/allorderedGamma/exactrowdedup notanonymization','floating alternation normalizepair1 fixedpcone thenzerossafetyLP','fullauthor260range/densities/backgrounds/twoqueryseeds/max7/maxratio1 historicalonly','actual5375code default160 versus260/reportmissing and CLIthresholds/configlist','large/SSR progress notcountedcompleted and missingdependencies boundaries'],'targets':[P2]},
{'id':IDS[3],'units':['2026-10-21 internalrole/generaltargetoldOPEN noanonymity/fixedtie/frozenreply','common singletheme alpha/G/M definitions and unconditionalOPT<=mM+W-G','candidate mM<=W+G conditionalhalf and preexistingorigin notnewclaim','current13playerexacttax failure versus4theme weakbridge only and truev preservation','no completegeneralproof or truehalf counterexample claimed'],'targets':[P2]}]
js(E/'semantic-coverage-map.json',coverage)
notes=[('7711B作者数学稿FT已related全文，本批核同SHA诚实复用，全ClaimA/B、三真实IC/三个展开、P/L、β及边界、频次筛选和来源/审查身份全保。','与现AB一般定理、FT VA原频次方向、完整源第143/149行及新增一次精确多项式报告比较；原具名audit未实际取得，标签不代代数。','原λ和区间等式笔误给定位/原SHA/两处最小未应用提案；修正+1后保原γ/β并完整证真，不覆旧AB正文或将旧done整体标错。'),('3148B总README首次完整语义读，头部后续更正、完整模型、旧clone/身份/团队/交流、七目录全部用途和停止/接续规则无遗漏。','PB-extra任意背景真反例、真v全位置pair、强弱iid、完整终局税/弱Q-R资源和当前五人定理逐一比较，旧角色命令只作来源。','自足路由对象保所有有用资产，纠正body旧OPEN而不扩大背景到actual根，不用陈旧目录指针替一般half证明或本次额外审批。'),('1976B aggregate README首次全文；v_r背景/首两人/嵌入条件推论、全部260浮点范围/参数/大r与SSR边界全部读。','真实5375B程序全文及实际配置/默认160/阈值/输入矩阵对照，312/330输出和SSR依赖缺；PB-extra更弱已败故旧前提OPEN失效，根真aggregate独立。','完整保有效条件分组与软件合同；260仅作者有限记录，无原argv/输入/日志认证，本批未运行LP/原CLI或把未来参数算完成。'),('827B globalproof README首次全文，旧身份/任意完整历史方法、alpha/G/M、无条件代数、未付mM桥与既有出处全部读。','现实际分数缩放对象的四主题弱反族与另13人精确税反例全文比较，分清两例作用、真正v、iid及fullterminaltax。','保OPT<=mM+W-G静态真式和条件half蕴含，原精确付款桥已假明确更新，不新造命题/反例或重演旧自动机。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' actual pushed/synced原回执及当前Boss4 owner/sourceSHA已核。','comparison_note':b,'decision_note':c,'disposition':'integrated','targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 阶段二关系

原ClaimA由共同目录真实末两人闭包和两覆盖预算推出；本批定位两处源凸合笔误并给最小修复，目标γ/β和现更一般AB定理保持真。新增多项式核验只审该纠错的精确系数，不是SPE/优化器或旧具名审计复现。ClaimB充分频次与一般BB收尾分开，不把变换有序历史当可信操作。

任意合法背景首两人pair由PB-extra更弱合同反驳，但背景是否actual根可达另有条件；原分组=>根真v聚合是条件逻辑，并非反例已推翻聚合。实际缩放M的mM≤W+G由13人证书否定，保静态OPT式；不同四主题反族只否另一弱桥。iidZ、真正v、添加价、全主题Q、分区R及fullterminaltax都保各自量词，不跨钱包。

5375B程序真实保持全部有序动作，只去重等Γ行；交替浮点安全LP/质量锥没有整数恢复，260无分离仅旧报告。源角色/团队/交流作历史，未开启数学Agent或代替本轮清洗授权。关系限阶段二，不导旧图或强制连边。
''')
nextrows=[]
for x in related:
 if not (REPO/'cleanup/progress'/f"{x['id']}.json").exists():nextrows.append({**x,'local_path':str(S/x['preserved_path']),'progress_observed':None,'semantic_read_status':'full related program already read FU; not run/primary completed, may honestly reuse after actualclaim','routing':'own-line actual available candidate'})
found=json.loads((C/'learning-fu-extra-actual-MD-candidates.json').read_text());wanted=['69e5bc7ef67a198bb9f9','f8eefcc1f4a30ba6cad2','dc0567b7f627ad5b3565']
for i in wanted:
 x=next(x for x in found if x['id']==i)
 if (REPO/'cleanup/progress'/f'{i}.json').exists():continue
 z=Path(x['local_path']).read_bytes();assert len(z)==x['size'] and sha(z)==x['sha256'];nextrows.append({**x,'progress_observed':None,'semantic_read_status':'cached exact available bytes only; no new semantic read/claim','routing':'Root-FN related cache alternative only; Root must ensure not already planned for another work line before assigning; no preemption or preclaim'})
js(W/'next-candidates.json',nextrows);js(E/'next-candidate-routing.json',{'own_line_actual':[x['id'] for x in nextrows if x['routing'].startswith('own')],'root_global_alternatives':[x['id'] for x in nextrows if x['routing'].startswith('Root')],'not_available_same_R31_programs':scope['missing_next_programs'],'policy':'Do not pad current4primary or steal other-line pending groups; alternatives only for Root authoritative current scheduling.'})
put(W/'delivery.md',f'''# FU交付

actual4 claim {claim['remote_tip']} pushed/synced与owner/sourceSHA全核。主源13662B/273行，7711B全文复用、3README5951B首次全读。两新自足正文/4receipt；原λ及区间等式纠错保原γ/β、未动冻结源或旧AB页。

新增标准库多项式检查一次{meta['elapsed_seconds']:.9f}秒exit{meta['exit_code']}，只核新纠错系数和m2 sanity；旧CLI/SPE/LP/优化/审计复跑0。5375B真程序全文新读，260浮点原报告缺不冒重演。helper2次10本地尝试1齐9缺，无网络/重试。

Root按copy-files白名单串行复制，先正文依赖pushed再done。下批ownline实际1源5375B程序，另3本地RootFN相关数学稿仅供Root全局去重调度备选，不预抢其他线。代理无sharedGit/领/done/checkpoint/show/真实账号公屏动作。
''')
p=E/'README.md';t=(S/p).read_text().replace('成功receipt等实际claim pushed/synced与owner后生成','actual claim pushed/synced与owner已核，成功receipt已生成');put(p,t)
checks=[]
def ck(n,v,detail=None):
 d={'check':n,'passed':bool(v)}
 if detail is not None:d['detail']=detail
 checks.append(d);assert v,n
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();v=inv[x['id']];ck('exact size/SHA '+x['id'],len(b)==v['size'] and sha(b)==v['sha256']);ck('exact blobSHA1 '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'])
ck('actual unprojected4 capture',(S/E/'actual-claim-receipt.json').read_bytes()==claimpath.read_bytes())
for x in owners:ck('actual owner '+x['id'],x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'])
for x in contexts:
 b=(S/x['snapshot']).read_bytes();ck('exact full/fresh/reused context '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
ck('new check actual once success',meta['execution_count']==1 and meta['exit_code']==0 and (S/run/'stderr.txt').read_bytes()==b'');ck('new code/input/output SHA identity',sha((S/E/'new-convex-correction-check.py').read_bytes())==meta['code_sha256'] and sha((S/run/'stdout.json').read_bytes())==meta['stdout_sha256'] and meta['source_sha256']==inv[IDS[0]]['sha256']);ck('new algebra result not an SPE claim',report['status']=='passed-new-correction-algebra-only' and report['m2_sanity']['old_a_b']==['13/16','29/16'] and report['m2_sanity']['corrected_a_b']==['23/16','23/16'] and report['original_claimed_positivity_identity_residual']==[0,2])
cor=rd(E/'correction/minimal-replacements.json');orig=next(x for x in primary if x['id']==IDS[0]);proposed=(S/cor['proposed_path']).read_bytes();ck('original beforeSHA frozen and repair un-applied',cor['before_sha256']==inv[IDS[0]]['sha256']==sha((S/orig['preserved_path']).read_bytes()) and cor['applied_to_original_or_shared_page'] is False);ck('exact proposed2replacement derivedSHA',sha(proposed)==cor['proposed_sha256'] and len(cor['changes'])==2)
links=[]
for p in [P1,P2]:
 t=(S/p).read_text();ck('flat MATEK '+p,all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('all nonLF C0 zero '+p,not any(ord(c)<32 and c!='\n' for c in t));ck('all trailing whitespace zero '+p,all(l==l.rstrip() for l in t.splitlines()));ck('display TeX balanced '+p,t.count('\\[')==t.count('\\]'))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  n=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));at=S/n if (S/n).exists() else REPO/n;ck('actual relative link '+dest,at.exists());links.append({'source':p,'destination':dest,'resolved':n,'bytes':at.stat().st_size,'sha256':sha(at.read_bytes())})
js(E/'formal-link-check.json',links)
a=(S/P1).read_text();b=(S/P2).read_text();ck('full structural proof and minimal correction','\\tag{CLOSE}' in a and '\\tag{P}' in a and '\\tag{L}' in a and '\\tag{WEIGHT}' in a and '\\tag{MIX}' in a and '(m^2-m+1)' in a and 'm(3m-1)>0' in a);ck('sourceboundaries/old audit/not whole-done dismissal','不是所有两主题SPE的必要频次' in a and '它原数学保持正确' in a and '未读/执行它们' in a);ck('current PB and exactM-tax correction','2v_(r+1)(b)≤2v_r(b)' in b and '29481/123025>0' in b and '同一查询保证s>u' in b);ck('actualread program config/scope','--trials160' in b and '260不是CLI默认160' in b and '代码没有自动有理恢复' in b)
ck('exact full4 source totals',scope['primary_bytes']==13662 and scope['primary_lines']==273);ck('accurate run count scope',scope['new_mathematical_execution_count']==1 and scope['original_CLI_calls']==scope['old_success_replays']==scope['new_SPE_or_game_history_checks']==scope['new_LP_or_Nash_solves']==0);ck('actual2helper10attempts1export9missing',scope['safe_local_helper_calls']==2 and scope['local_blob_attempts']==10 and scope['local_exports']==1 and scope['local_missing_blobs']==9)
ck('exact4 complete semantic receipts',len(receipts)==4 and {x['id'] for x in receipts}==set(IDS))
for x in receipts:
 ck('complete receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']))
 for p in x['targets']:ck('actual receipt target '+p,(S/p).exists())
ck('exact2 new formal files',sorted(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))==sorted([P1,P2]))
for x in rd(E/'formal-resource-manifest.json'):
 z=(S/x['path']).read_bytes();ck('exact formal SHA '+x['path'],len(z)==x['bytes'] and sha(z)==x['sha256'])
for x in nextrows:
 z=Path(x['local_path']).read_bytes();ck('actual next readable and ownerrouting '+x['id'],len(z)==x['size'] and sha(z)==x['sha256'] and x['progress_observed'] is None)
obs=[]
for p in S.rglob('*'):
 if not p.is_file() or p.name in ['copy-files.json','copy-paths.txt','delivery-summary.json']:continue
 try:t=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()]
 if bad:obs.append({'path':str(p.relative_to(S)),'lines':bad,'frozen':any('/'+z+'/' in str(p.relative_to(S)) for z in ['original','related','context','context-reused','correction'])})
ck('all derived trailing whitespace zero',not any(not x['frozen'] for x in obs));js(E/'transport-whitespace-observations.json',{'observed':obs,'originals_unchanged':True,'proposed_source_is_unapplied_derived_only':True})
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'scope':'Source/claim/SHA/correction and new once-polynomial-run bindings, complete proof/quantifier/route coverage, metadata/C0/links/receipts/transport; not new SPE/LP or generalhalf verification'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  z=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(z),'sha256':sha(z)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':scope['primary_bytes'],'primary_lines':scope['primary_lines'],'new_formals':2,'formal_bytes':sum((S/p).stat().st_size for p in [P1,P2]),'receipts':4,'checks':len(checks),'relative_links':len(links),'new_math_runs':1,'old_replays':0,'claim_tip':claim['remote_tip'],'own_line_next':[x['id'] for x in nextrows if x['routing'].startswith('own')],'root_global_alternatives':[x['id'] for x in nextrows if x['routing'].startswith('Root')]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
