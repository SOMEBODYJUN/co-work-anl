from pathlib import Path
import json,hashlib,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-frozen-bank-product-and-push-report-bindings';E=Path('tools/evidence/frozen-bank-product-and-push-report-bindings');W=Path('cleanup/workspaces/Boss4/r3-frozen-bank-product-and-push-report-bindings-next');JZ=C/'r3-marked-bank-products-and-extra-theta-programs';JE=Path('tools/evidence/marked-bank-products-and-extra-theta-programs')
IDS=['48a2a60361a45c8678ed','11e83f89dec391d5b2fe','06068e36ffe4499b4538','0833067167a458cefed7'];P1='archives/customer-attraction/state/程序/任意标记保险与两个不等缺陷产品的原审计--程序.md';P3='archives/customer-attraction/state/程序/固定三人完整推送的两分布浮点探针--程序.md'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
# Successful receipts are not produced until Root supplies actual fresh4claim.
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='needs-attention' and set(IDS)<=set(claim['ids'])
resolutionpath=C/'boss4-r3-next-kx-ky-kz-atomic-claim-sync-preservation.json';resolution=json.loads(resolutionpath.read_text());assert claim['remote_tip']=='3a1edbfdaf4df9e254220eabb8d20ada807d9f32' and resolution['stash'] in claim['local_sync']['detail'] and resolution['stash_kept'] and resolution['missing']==resolution['different']==[] and resolution['unmerged']=='' and resolution['untracked_count']==2 and len(resolution['tracked'])==2 and all(x['same'] for x in resolution['tracked'])
mp=C/'learning-jz-frozen-output-original/actual-source-manifest.json';m=json.loads(mp.read_text());published=json.loads((JZ/JE/'frozen-output-manifest.json').read_text());primary=[];owners=[];objects={}
for i in IDS:
 x=next(x for x in m['rows'] if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size']==x['size'] and sha(b)==v['sha256']==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];cap=json.loads(Path(x['actual_normal_show_capture']).read_text());assert cap['source']==v and cap['output']==x['local_path'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);old=next(y for y in published if y['id']==i);assert (REPO/old['preserved_path']).read_bytes()==b==(JZ/old['preserved_path']).read_bytes();q=E/'original'/i/v['path'];cp(x['local_path'],q);cp(x['actual_normal_show_capture'],E/'actual-normal-show-captures'/Path(x['actual_normal_show_capture']).name);primary.append({**v,'preserved_path':str(q),'already_published_exact_asset':old['preserved_path'],'read_mode':'JZ actualallJSONsemanticfields read completely then exactsameSHA reusedasnewprimary afterfreshclaim, notfake firstread/countonly/recopyasproof; authorall343actions read throughbijective jointlabels; currentoldpublishedartifact byteidentical'});objects[i]=json.loads(b)
assert sum(x['size'] for x in primary)==87477
js(E/'source-manifest.json',primary);cp(mp,E/'actual-original-normal-show-manifest.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json');cp(resolutionpath,E/'actual-independent-sync-resolution.json');js(E/'actual-primary-ownership-snapshot.json',owners)
contexts=[]
for p in [P1,P3]:
 b=(REPO/p).read_bytes();assert b==(JZ/p).read_bytes();q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'JZactualfullprogramresource textualsemanticcomparison reused; currentexactpublishedbytes matchfrozenpriorcomplete-readingdelivery'})
js(E/'context-manifest.json',contexts)
for n in ['frozen-evidence-binding-and-runtime-boundary.json','read-scope-and-evidence-status.json','frozen-output-reading/author75-all343-joint-policy-lossless.json']:
 cp(JZ/JE/n,E/'actual-prior-JZ-semantic-reading-evidence'/n)
bank=objects[IDS[0]];author=objects[IDS[1]];parent=objects[IDS[2]];probe=objects[IDS[3]]
assert parent['source_sha256']==inv['73780fead77dbf46e31f']['sha256'] and parent['passed'] and parent['python']=='3.12.14'
coverage=[{'id':IDS[0],'disposition':'duplicate','targets':[P1],'units':['fullsummaryscope/allpassed26games518forcedchild15353cumulative75913inclself/generalproof filename','all26records m2..5 everymarkednonlastsubset/normalorder/Wbank m+k/OPT2m-1/eachchildcounts/cap1/min0','nonuniqueabsolutehistories acrosschildaudits/finiteimplementation notallmSPEproof','sourceco_versionJSONnoexecutionSHA/argv/time metadata/no newrun']},
{'id':IDS[1],'disposition':'duplicate','targets':[P1],'units':['allmetadata oldoriginalscale6/oldpay3,3,24/deficits5,9/D9R14/37vs45/layers{0,1},{1}/scales5,4','75unit/18jointtheme/343orderednode/6174jointIC/min0/actualjointpath/pay17,21,33/W71O75gap-67/notcounterexample','all343history/action fullread viaexactlabel9a+3b+c/losslesspublishedrepresentation/shapeall0,1,2histories','authorcodeexpands75individualclients distinctfromparentblockFraction/currentoutputno sourceSHA/no newaudit']},
{'id':IDS[2],'disposition':'duplicate','targets':[P1],'units':['allidentity/scope/Python3.12.14/sourceSHA6870matches6096code','oldsize6,24/oldAAB/deficits5,9/bank10,10,5 and8,8,4/onebasedmarks12,2','actualjointpath/pay17,21,33/customer75/W71OPT75/343nodes/6174inclself/5832OPT/min0/passed/generallink/notcounterexample','originalinternalSHA binding notindependent savedargv/exit/time/stdoutlog orcurrentrun','parentorderedterminalsets/aggregateblockshares originalgameequalnotauthorbyteidentity']},
{'id':IDS[3],'disposition':'duplicate','targets':[P3],'units':['allcandidate/policy/types63/258inclselfIC/twop rationalstrings/full4LPobjects/warning','pushgaps-0.125,-0.09104938271604927/uniform-0.125,-0.09722222222222224 exactstoredfloats','allweightmasks3objects {2,4,16,32}1/6+{9}1/3 vsfirstuniform 6singletons1/6','floatFractiondisplaynotrationalICrecheck/exactdual/wholeconecert/no sourceSHAorexecutionversion','fixed6labelpolicy maycollapsecoverage/necessaryICformalcone notnewcompleteunitSPE/FTA false/globalhalf']}
]
js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':4,'primary_bytes':87477,'primary_read':'actualall4JSONcomplete semanticfieldreading duringJZ-related cleanup; exactbyte/wholemeaningcomparison afternewactualclaim, notnewfirstreading','bank_records_actualcomplete_read':26,'author_full_jointpolicy_actualcomplete_read':343,'parent_all_fields_sourceSHA_read':True,'probe_all_4LP_objects_and_weights_read':True,'new_formals':0,'dispositions':{'duplicate':4},'original_JSON_assets_already_exact_published':4,'existing_program_formals_current_equal_priorread':2,'parent_report_internal_SHA_not_externalexecutionlog':True,'other3reports_no_sourceSHA_no_fakehashrunbinding':True,'new_math_program_runs':0,'original_math_CLI_calls':0,'original_module_imports':0,'new_LP_BI_random_SPE_theta_runs':0,'old_success_replays':0,'new_helper_export_calls':0,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'shared_Git_writes':0,'own_clean_show_claim_done_checkpoint_calls':0,'network_or_lazy_fetch':0,'real_board_account_auth_operations':0,'phase3_graph_import':0,'derived_packaging_builder_calls':1,'derived_packaging_builder_failures':0}
js(E/'read-scope-and-evidence-status.json',scope)
notes=[('11150B原JSON26条记录及summary全部在JZ实际全文读，现核新primary同SHA/原showcapture/完整owner，诚实复用既有完整阅读不假装再次第一读。','当前7889B原审计程序对象对全部markednormal/低退出/BIFraction及输出范围自足，精确保26/518/15353累计/75913含self；原每m/mark的normal_order和W/OPT/min/cap已在同字节发布原asset保，完整程序语义可复原，不由数量自动判重。','duplicate：无独有内容丢失，精确目标+原assetSHA完整保。JSON all_passed是原有限报告，source无执行SHA/时间/独立日志不捏造，0新math/原CLI/旧成功；不升级任意m定理或extra done原code。'),
('73799B作者75原JSON全部标量与343个有序联合history/action已JZ逐行以9a+3b+c双射实读，roundtrip等每条原坐标；现逐字节核原asset及当前原程序对象。','7889B程序对象完整保作者计数终局集合/固定两层银行/全坐标退出/逐75客户IC/5832OPT；与父方不同源码/表示分开。全部原policy在已发布artifact及先前完整阅读表示中精确去向，不把6174比较当运行次数或对同名父方报告判同byte。','duplicate：cost37/45、负gap和非反例身份都保，原输出无sourceSHA不冒同SHA执行日志，0新IC/75重跑。此JSON被正式认领后才写独立receipt，不因JZ拷过related就直接勾。'),
('1136B父方报告全字段JZ实际全文读，包括Python/sourceSHA/oldnew参数/343/6174/5832、passed/min0/非反例及proof路径；现新claim后精确字节/owner核。','原程序对象已完整保父方有序终局集合和块Fraction实现；报告内部sourceSHA确等6870...原6096B代码、Python3.12.14原值，准确区别这个内部绑定和未保存的外部argv/退出码/时长/stdout日志。','duplicate：全部数据/有限范围与有用强绑定已有自足目标，不声称当前run/外审/一般half。0重复旧成功、不把父方称作者同实现，不额外done任何引用code/JSON之外源。'),
('1392Bprobe原JSON所有字段/两p/四gap/四weights/warning已JZ全文实读，现核新primary同SHA并逐对象对应P3软件合同。','4119B程序对象完整保固定43/258/63类型/两p四浮点LP、所有四storedgap精确显示和两权重profile；权重有理展示未重验IC/无exactdual，标签可能同覆盖，不能由floatnegative认证原模型全锥。','duplicate：完整原asset及自足解释均有精确去向，source无版本/执行SHA/外部日志则不冒运行绑定；0原import/LP/新程序/旧阴性重跑，不把Mfull/FTA/Mpath/half真值混用。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原完整actualclaim仅取本4subset/currentowner/sourceSHA，不投影原多组receipt。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# 四冻结报告的完整语义去重

四primary87477B全部真实完整JSON阅读已在JZ完成：26marked记录、作者75全部343联合策略条目、父方sourceSHA全部字段、probe四LP与全部weights。新actualclaim/currentowner/sourceSHA后才正式逐源receipt，不因已copy、数量或仅wholeSHA判数学完成。

它们与当前已发布JZ原asset逐字节相同，两个正式程序资源与JZ完整读交付版本同SHA；完整数学/软件范围及所有输出用途已有明确目标，4duplicate/0新formal。新manifest逐源给exactpublishedasset路径、SHA和normalshowcapture，源字节独立另保便于审阅。

父方旧报告内部sourceSHA6870...强绑原程序，但没有独立argv/退出码/时长/stdout捕获就不声称有；其他三输出无sourceSHA，co-version字节绑定不是旧run日志。所有passed/floatnegative仅其原有限范围，非全m/完整锥/一般half/外审认证。0新原import/CLI/LP/BI/SPE或旧成功复跑，不额外done代码或16已属其他人的theta输入。

Root先推证据/已有目标确认后done；0sharedGit/网络/账号公屏/mapper，不造重复数学对象。
''')
put(W/'relation-review.md',r'''# 阶段二关系与精确去向

26marked报告是有限低退出子树实现输出；作者75报告是显式单位客户展开的联合策略/全节点检查；父方75是独立有序/块份额实现的内部hash报告。这是不同来源/有限证据作用，不能按同名与同数值合并程序身份。

probe的四negative/两权重仅数值诊断，原有理展示没有exactdual或复核IC；不会因被冻结转成证明。四JSON全部字段和政策已有现程序资源+精确原asset保，逐sourceduplicate准确；旧报告内部sourceSHA、wholeassetSHA与独立执行日志三个概念分别保。

此批0新对象发现/数学运行，不重勾已done原code或theta16输入。无外审/新颖性升级、无第三阶段自动图导入或强制连通。
''')
cp(Path(__file__),E/'build_delivery.py')
scope['raw_local_sync_status_preserved']='needs-attention';scope['independent_resolution']='Rootactual728249...stash2tracked2untrackedallbytespreserved0missing/different/unmerged; rawclaimnotrewrittensynced';scope['helper_calls_preparingnext']=2;scope['next_local_blob_attempts']=5;scope['next_local_exports']=3;scope['next_local_missing']=2;scope['next_missing_retry_calls']=0;js(E/'read-scope-and-evidence-status.json',scope)
put(E/'claim-and-recovery-scope.md',f'''# 实际认领与独立恢复

原13项receipt实际pushed {claim['remote_tip']}，local_sync原needs-attention保留；不把Root另完成的恢复证据改写进原回执。独立proof保存stash {resolution['stash']}，2tracked/2untracked全同，0missing/different/unmerged且stash保留。本4实际owner/sourceSHA逐项核。

完整JSON含义在JZ实际已读，此次完整语义逐项对应既有程序资源；既有asset全字节相同只是额外版本绑定，不能单凭该hash代替阅读。0新数学运行/外部操作。
''')
nextids=['218b9c0afd232e720c7a','a863ea48f22c76a1d877','5911bb1e25c90dd73580'];nextmanifests=[C/'kx-next-hamming-and-shared-audit-inputs/local-export-manifest.json',C/'kx-next-shared-audit-readme-input/local-export-manifest.json'];nms=[json.loads(p.read_text()) for p in nextmanifests];assert len(nms[0]['missing'])==2 and len(nms[0]['rows'])==2 and len(nms[1]['rows'])==1 and nms[1]['missing']==[];nextrows=[]
for j,p in enumerate(nextmanifests):cp(p,E/'next-original-local-attempts'/f'attempt-{j+1}.json')
for i in nextids:
 x=next(x for z in nms for x in z['rows'] if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];p=REPO/'cleanup/progress'/f'{i}.json'
 if not p.exists():nextrows.append({**v,'local_path':x['local_path'],'progress_observed':None,'read_status':'actuallocalbytesverified only beforeKXseal; notyetfullsourcecode/JSON/READMEsemanticread, no primaryreceipt/claim/run'})
js(W/'next-candidates.json',nextrows);cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in primary:
 b=(S/x['preserved_path']).read_bytes();ck('exactsourceSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('exactsourceblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']);ck('actualpublishedassetbyteequal '+x['id'],(REPO/x['already_published_exact_asset']).read_bytes()==b)
ck('raw13claimbyteidentical',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and len(claim['ids'])==13);ck('actual4subsetownerSHA',set(IDS)<=set(claim['ids']) and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('rawneedsattentionpreserved',claim['status']=='pushed' and claim['local_sync']['status']=='needs-attention');ck('independentresolutionpreserved',(S/E/'actual-independent-sync-resolution.json').read_bytes()==resolutionpath.read_bytes() and resolution['missing']==resolution['different']==[] and resolution['unmerged']=='' and all(x['same'] for x in resolution['tracked']) and resolution['stash_kept'])
for x in contexts:ck('exactfullreadformalcontext '+x['path'],sha((S/x['snapshot']).read_bytes())==x['sha256'] and (REPO/x['path']).read_bytes()==(JZ/x['path']).read_bytes())
ck('bank26recordsallfieldsread',len(bank['records'])==bank['bank_games']==26 and bank['exit_children']==518 and bank['ordered_decision_histories']==15353 and bank['all_action_comparisons']==75913 and bank['all_passed'] and all(x['maximum_forced_exit_payoff']=='1' and x['minimum_IC_margin']=='0' for x in bank['records']));ck('author75all343sourcefieldsread',len(author['actions'])==author['full_ordered_decision_histories']==343 and author['customers']==75 and author['topics']==18 and author['all_joint_action_IC_comparisons']==6174 and author['heterogeneous_half_gap_loss']=='37' and author['old_uniform_half_gap_loss']=='45' and author['half_gap']==-67 and not author['target_counterexample'])
authorread=json.loads((S/E/'actual-prior-JZ-semantic-reading-evidence/frozen-output-reading/author75-all343-joint-policy-lossless.json').read_text());dec=lambda a:[a//9,(a%9)//3,a%3];ck('all343actualreadrepresentationexact',authorread['roundtrip_exact'] and authorread['source_sha256']==inv[IDS[1]]['sha256'] and [{'history':[dec(a) for a in r['history_joint_labels']],'action':dec(r['action_joint_label'])} for r in authorread['all_policy_entries']]==author['actions'] and authorread['all_nonaction_fields']=={k:v for k,v in author.items() if k!='actions'})
ck('parentinternalhashnotreexecution',parent['source_sha256']==inv['73780fead77dbf46e31f']['sha256'] and parent['passed'] and parent['ordered_decision_histories']==343 and parent['all_joint_action_comparisons_including_self']==6174 and parent['terminal_profiles_for_OPT']==5832 and parent['python']=='3.12.14');ck('other3havenoexecutionhash',all('source_sha256' not in x for x in [bank,author,probe]));ck('probe4rawfloatsandwarnings',probe['all_history_IC']==258 and probe['types']==63 and [x['gap'] for x in probe['push']]==[-0.125,-0.09104938271604927] and [x['gap'] for x in probe['uniform']]==[-0.125,-0.09722222222222224] and 'not certificates' in probe['warning']);ck('probeallweightobjectscovered',len(probe['push'])==len(probe['uniform'])==2 and all('weights' in x and 'p' in x for z in ['push','uniform'] for x in probe[z]))
ck('4complete_duplicate_receipts',len(receipts)==4 and {x['id'] for x in receipts}==set(IDS) and all(x['disposition']=='duplicate' for x in receipts))
for x in receipts:ck('completereceipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((REPO/p).exists() for p in x['targets']))
ck('nonewformal',not(S/'archives').exists());ck('zero mathCLIimportreplay',scope['new_math_program_runs']==scope['original_math_CLI_calls']==scope['original_module_imports']==scope['new_LP_BI_random_SPE_theta_runs']==scope['old_success_replays']==0)
for x in nextrows:ck('actualnextlocalavailable '+x['id'],sha(Path(x['local_path']).read_bytes())==x['sha256'] and not(REPO/'cleanup/progress'/f"{x['id']}.json").exists())
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context']);bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('allnewderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_original_context_unchanged':True})
put(W/'delivery.md',f'''# KX四冻结输出交付

4primary87477B已全部完整语义读并重新对应现程序对象：26records、343fulljointpolicy、parent内部sourceSHA/全部参数、四floatLP全gap/weights。原asset与JZ已发布文件字节精确相同，2正式对象同完整既读交付SHA；4duplicate、0新formal/数学对象，不只因hash或已copy判完成。

原13claim{claim['remote_tip']}真实pushed、local_sync原needs-attention不改；独立728249...proof原字节保，2tracked2untracked同字节/0missingdifferentunmerged/stash保留，本4owner/sourceSHA核。0原CLI/import/LP/BI/SPE/旧成功复跑，不额外donecode或16已他人处置theta输入。

下一{len(nextrows)}实际本地齐件{sum(x['size'] for x in nextrows)}B，仅byte未全文/未claim；两safehelper5尝试3export2missing，缺的hammingcode/report不重试/网络回退。Root先推证据确认目标再done，代理0sharedGit/账号公屏/mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'new_formals':0,'derived_nonLF_C0':0,'derived_trailing_whitespace':0,'scope':'all4JSONsemantics/preciseoldtargetassetbinding/raw13claim+independentresolution/owner/wholefieldcoverage/format/transport','mathematics':'no newmathruns; fieldbinding/roundtrip isnotnewSPEorLPcert; internalreportSHA isnotexternallog'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':87477,'new_formals':0,'receipts':4,'dispositions':{'duplicate':4},'checks':len(checks),'new_math_runs':0,'new_original_CLI_runs':0,'old_success_replays':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'raw_sync_status':'needs-attention-original-preserved-plus-independent-recovery','next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
