"""Writes final semantic records only after actualpushed/synced+owner checks.
No Git/network/auth/math-program execution. A pendingclaim writesnothing.
"""
from pathlib import Path
import hashlib,json,subprocess
WS=Path(__file__).resolve().parent;stage=WS.parents[3]
assert stage.name=='r3-r642-entry-and-residual-primary'
root=stage.parent.parent;repo=root/'boss4-research'
ev=stage/'archives/customer-attraction/tools/evidence/r642-entry-and-residual-primary'
cp=root/'boss4-r3-next-fx-claim.json'
if not cp.is_file():raise SystemExit('Actualclaim capture stillpending; finalsuccess records notwritten')
assert not (WS/'semantic-receipts.json').exists(),'Finalrecords alreadywritten; do not repeat'
c=json.loads(cp.read_text());m=json.loads((WS/'intake-local-export-manifest.json').read_text())
ids={x['id'] for x in m['rows']}
assert c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and set(c['ids'])==ids
owners=[];sources=[]
for x in m['rows']:
 p=ev/'original'/x['path'];b=p.read_bytes()
 assert len(b)==x['size'] and hashlib.sha256(b).hexdigest()==x['sha256']
 assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==x['blob']
 o=json.loads((repo/'cleanup/progress'/f"{x['id']}.json").read_text())
 assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
 owners.append({'id':x['id'],'record':o});sources.append(dict(x,role='primary',saved_path=str(p.relative_to(stage)),local_bytes_verified=True))
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
(WS/'claim-receipt.json').write_bytes(cp.read_bytes())
put(WS/'claim-observation.json',{'status':c['status'],'actor':c['actor'],'remote_tip':c['remote_tip'],'local_sync_status':c['local_sync']['status'],'capture':str(cp),'capture_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'all_actual_claim_ids':c['ids'],'claimed_primary_ids':sorted(ids),'full_original_receipt_retained':True,'local_working_tree_owners':owners,'read_order':'Parentauthorized completepreread/externaldraft; no successrecords beforeactualcapture/owner. No mathematicalentries needed.'})
pre=json.loads((WS/'preclaim-preparation-observation.json').read_text());pre['historical_observation_phase']='beforeactualclaim capture existed';pre['superseded_by']='claim-observation.json';put(WS/'preclaim-preparation-observation.json',pre)
put(ev/'primary-manifest.json',{'primary_count':3,'primary_bytes':12989,'method':'safeexistinglocal bytes size/SHA256/blobSHA1 allverified; fullprimaryread; no network/auth/lazyload','sources':sources})
version='archives/customer-attraction/state/资料/二十七客户残余反例的原标签与完整回复版本--资料.md'
crosswalk='archives/customer-attraction/state/资源/R642一般半覆盖工作区的恢复身份与对象对照--资源.md'
notes=[
('cfc4019b25d1ca46441c','8624B全文：原Boss2/R642恢复身份/3基点/6sol-ultra内部研究者、目录读取条件与无文件不猜结果、66运输及两独审的38旧菜单负值、64→2396/38/44/74442历史、前缀ID与fixedrank、无势/有限DR非CAG、14PFR存在性反例、待补全深度义务。','与已处理原数学正文/FP aligned、EF前缀/PFR、DJ fixedrank、DU势范围比较；源private/未shared/一般OPEN是历史，不重开five或抹EF真实发表。恢复哈希不猜祖先/当前HEAD，不执行旧actor/start/resume。','integrated完整恢复/索引资源对象，保66/两独审只是源述未新验，精确旧coords排点非全型界；所有成熟/未付接口分域。仅3actual主源、不因目录列表额外done；0原/0新数学run。',[crosswalk]),
('e4600ec51417390aab18','2941B正式主源全文：去重残余组合加强式、27单位10块/6×6末收益/完整reply、六根全6/W13、T/S残余14与原OPT14/half12、Q/R可信循环、原audit42/全pair及两发现LP角色。','与DU旁读段、正式保护遗漏例、residual27独立replay全文比较；原标签到formal映射保持客户/表，但reply正式Q后的S不同旧R。两BR末7且根6，解析保持fullSPE，不冒同policy或旧报告已认证此动作表。BT/BS仍有利最优，固定Ymax不混存在有利O。','integrated独立原标签/回复版本资料：全部表/21opt/版本差异及一行平局替换完整自足。旧DU仅旁读本源未done，现正式处置；0新程序，复用共同收益/OPT，原1739audit/326report缺不能称原run。',[version,crosswalk]),
('1d11b851517a41a09494','1424B全文：通用K真实菜单去对角/客户择行限制、独立audit只JSON与冻结output用途、prefix独立代数重构、14PFR唯一OPT/全部matching收费、受限支撑与全型定价义务/团队资产不能自动升格。','逐项比现ER一般引理/AE64、EFprefix/PFR及Root旧PFR纠错；原auditcode曾safehelper缺，本报告266B本地亦缺；文档列运行命令不等本轮执行。内部作者复核非外审。','integrated与总入口共同资源，保各对象是普遍证明/有限实现/结构子类/反例而非一般half；源若未报告不能猜工作完成。0原/0新数学entry，不执行旧共享状态命令。',[crosswalk])]
receipts=[]
for i,read,comp,dec,targets in notes:receipts.append(dict(id=i,full_file_reviewed=True,related_material_checked=True,unique_content_accounted_for=True,read_note=read,comparison_note=comp,decision_note=dec,disposition='integrated',targets=targets))
put(WS/'semantic-receipts.json',receipts)
put(ev/'runtime-record.json',{'status':'analytic-version-comparison-no-new-mathematical-entry-needed','original_entries':0,'new_mathematical_entries':0,'external_solver_calls':0,'old_math_reruns':0,'metadata_finalizer_runs':1,'basis':'Exactsamecustomercover/payoffmatrixandOPT dataalreadyreplayed; variantreply notsamepolicy, onebranchBR7/root6 unchanged analyticallyprovesnewfullSPE. No programreplayfabricated.','not_run':['missingR642residualaudit','menuaudit','round3transport/independentaudits','DU/EF/ER/FB/FPchecks'],'no_new_stdout_stderr_timer_claim':True})
dep=json.loads((WS/'dependency-local-export-manifest.json').read_text())
put(ev/'dependency-boundary.json',{'safe_local_export':dep,'network_attempts':0,'auth_attempts':0,'missing_retry':False,'original_entries':0,'no_extra_primary_done':True,'earlier_aligned38JSON':'FPconfirmedmissing; not retried inFX'})
report=repo/'archives/customer-attraction/tools/evidence/residual-27/replay/residual_counterexample_audit.json'
verification=repo/'archives/customer-attraction/tools/evidence/residual-27/verification.json'
put(ev/'sufficient-data-reuse.json',{'new_runs':0,'old_report':{'path':str(report.relative_to(repo)),'size':report.stat().st_size,'sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'read_scope':'full2596B report: alltypes/paymatrix/reply/root/21pairs/OPT/quantifierboundary'},'old_verification':{'path':str(verification.relative_to(repo)),'sha256':hashlib.sha256(verification.read_bytes()).hexdigest(),'historicalprogress_fields_not_currentownership':True},'R642_to_formal_labels':['A','B','T','Q','R','S'],'R642_reply_in_formal_labels':['B','R','R','S','S','R'],'canonical_reply':['B','R','R','R','S','R'],'different_prefix':'formalQ=R642S, index3','two_reply_values':{'last_player':7,'root_player':6},'exact_policy_replay_reuse':False,'reused':'samecustomerpaymatrixand21pairOPT; newbranchreplacementICproofisanalytic','not_new_counterexample_discovery':True})
terms='R-64201cd12083425899e2d643ec9bc087/README.md|residual_portfolio_obstruction|next_boss/README.md|R642一般半覆盖'
r=subprocess.run(['rg','-n','--glob','*.md',terms,str(repo)],capture_output=True,text=True);assert r.returncode in(0,1);(ev/'repository-related-search.txt').write_text(r.stdout)
comp=[('archives/customer-attraction/state/反例/零背景保护遗漏与超额利润价格--反例.md','fullread unit27matrix/21pairs andquantifiers; differentoffpathreply'),('archives/customer-attraction/state/计算/二十七客户遗漏反例的标签等价与单位核验--计算.md','fullread existingprogram/replaycontract; notre-executed'),('archives/customer-attraction/state/定理/两人匿名势的静态安全支付与无势循环边界--定理.md','header/residualsection selectedread, exactDUmapping/onebranchdifference alreadypreserved; sourcewascomparisonnotdone')]
put(ev/'comparison-review.json',{'whole_repository_MD_search':{'command':['rg','-n','--glob','*.md',terms,str(repo)],'matching_lines':len(r.stdout.splitlines()),'retained':'repository-related-search.txt','search_not_fullread':True},'formal_comparisons':[{'path':p,'sha256':hashlib.sha256((repo/p).read_bytes()).hexdigest(),'scope':scope} for p,scope in comp],'prior_full_read_carryover':['ERmenu/prefix/PFR','FP38alignedandrootcompletion','DJfixedrank','DUabstractvsCAG'],'all_actual3_primary_full_read':True,'primary_bytes':12989,'no_extra_source_done':True})
put(WS/'next-scope-note.json',{'current_actual_scope':sorted(ids),'no_added_primary_or_candidates':True,'reason':'Parentexplicitlyrequestedthreeactualsources; no extraoriginalsourcewas read/claimed/done tofillabatch. Nextgroup suppliedbyRootafterauthoritativeledgercheck.'})
print(json.dumps({'status':'final-records-written-after-actualclaim','remote_tip':c['remote_tip'],'primary_count':3,'primary_bytes':12989,'mathematical_entries':0},ensure_ascii=False))
