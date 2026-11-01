from pathlib import Path
import hashlib,json,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='cyclic-affine-independent-and-gap-cone-programs-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');IDS=['0469d834f1fa594d17cd','7675bf8f6df8386e7b8b','ce3d3a0f96d70256d082','5bec0a04abf5397875a6','223821b7c0764e19ada5'];RELATED=['1304b665e9736f039253','e101d8e91123357aa120'];P='archives/customer-attraction/state/程序/八标签圆环的仿射独审合同--程序.md';T='archives/customer-attraction/state/程序/固定完整策略对尾部聚合差额的锥攻击--程序.md';CT='archives/customer-attraction/state/定理/八标签圆环族的完整可信子局与最小首位收益--定理.md';CG='archives/customer-attraction/state/候选/真实尾部最优利润的最小收益差额候选--候选.md';V='archives/customer-attraction/state/审查/圆环可信性父审的旁支合同与证据身份--审查.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 d=S/q;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(Path(p).read_bytes())
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids']);inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};mps=[C/'cyclic-parent-independent-audit-local-preparation/local-export-manifest.json',C/'tail-gap-cone-probe-local-preparation/local-export-manifest.json',C/'tail-gap-cone-probe-real-reported-inputs/local-export-manifest.json'];rows=[x for p in mps for x in json.loads(p.read_text())['rows']];sources=[];related=[];owners=[]
for i in IDS+RELATED:
 v=inv[i];x=next(x for x in rows if x['id']==i);b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/('original' if i in IDS else 'necessary-related-original')/i/v['path'];cp(x['local_path'],q);rec={**v,'preserved_path':str(q),'read_scope':'entire original code/text/all JSONfields and all259/85actions; actualfullread preclaim then currentprimary comparison; no fabricatednewfirstread'};(sources if i in IDS else related).append(rec)
 if i in IDS:
  o=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==v['sha256'];owners.append(o)
assert sum(x['size'] for x in sources)==13982 and sum(x['size'] for x in related)==30602
loc=json.loads((C/'cyclic-parent-original-cli-actual-location.json').read_text());run=json.loads(Path(loc['manifest']).read_text());assert loc['all_passed'] and run['all_passed'] and run['original_CLI_calls']==run['original_main_math_body_calls_confirmed']==1 and run['original_module_import_calls']==run['successful_same_SHA_reruns']==0 and run['source_sha256']==inv[IDS[0]]['sha256'] and run['exit_code']==0 and run['stderr']['bytes']==0 and run['output']['byte_equal_frozen'] and run['output']['stdout_exact_full_output'];assert Path(loc['claim_path']).read_bytes()==claimpath.read_bytes()
js(E/'source-manifest.json',sources);js(E/'necessary-related-input-manifest.json',related);js(E/'actual-owner-snapshot.json',owners);cp(claimpath,E/'actual-unprojected-claim-receipt.json')
for j,p in enumerate(mps):cp(p,E/'actual-local-manifests'/f'input-{j+1}.json')
fixture=Path(loc['fixture']);runmap=[]
for p in sorted(fixture.rglob('*')):
 if p.is_file():q=E/'actual-cyclic-original-fixture'/p.relative_to(fixture);cp(p,q);runmap.append({'actual_path':str(p),'archived_path':str(q),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
js(E/'actual-run-artifact-map.json',runmap);cp(C/'run_cyclic_parent_independent_original_once.py',E/'actual-executed-once-wrapper.py');cp(C/'cyclic-parent-original-cli-actual-location.json',E/'actual-run-location.json')
comp=[]
for p in [CT,CG,V]:
 b=(REPO/p).read_bytes();q=E/'comparison'/p;cp(REPO/p,q);comp.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'scope':'fullformalactualread andpreviousversion identity/knownold-unread history retained; no extra source done'})
js(E/'comparison-manifest.json',comp)
pb=(C/'cyclic-parent-independent-audit-drafts/program-body-preclaim.md').read_text();pb='# 八标签圆环的仿射独审合同\n\n4789B独审源码及525B全报告完整实读，旧父审当时未取的身份保原。实际claim/owner/sourceSHA后，本次新隔离副本原CLI恰1次通过，完整stdout和新报告均与冻结525B全byte相同；不倒填旧日志、不冒新盲审或全人数定理。\n\n'+pb[pb.index('## 参数和直接会员计算'):];pb=pb[:pb.index('若后续实际认领且需要')];pb=pb.replace('本草稿也未import','本轮未import').replace('本草稿','本资源');pb=pb.replace('人类全参数分类/完整BR区间和两组简洁策略见现有圆环定理','人类全参数分类/完整BR区间和两组简洁策略见[现有圆环定理](../定理/八标签圆环族的完整可信子局与最小首位收益--定理.md)');pb+='## 本次原入口的真实执行\n\n'+run['python']['version_stdout'].strip()+'，原码SHA '+run['source_sha256']+'。新空repo相对目录，原入口argv/cwd/环境/起止时间完整保存，实耗'+str(round(run['elapsed_seconds'],6))+'秒，exit0/stderr0；新报告525B、stdout525B均与原报告全byte同。原CLI1/已确认main数学主体1/原moduleimport0/成功后重复0；Python身份查询另1，不算数学审计。\n\n55参数审计各73节点/584含自身比较，共32120；静态五参数600背景加40对偶等式分别保。显式单位ID展开0；现有全参数定理由原解析承担，无新定理/新blind/外审。尾部gap兄弟探针本批仍0运行，旧negative不重扫。\n'
tb=(C/'tail-gap-cone-probe-drafts/resource-body-preclaim.md').read_text()
tb='# 固定完整策略对尾部聚合差额的锥攻击\n\n1192B入口/7040B源码/436B两行旧报告完整实读，并实读两份策略JSON全部259/85动作。当前实际认领后写本资源；旧入口待盲审/一般OPEN是其原历史，既有GAP局部证明和后来一般EI反例分开。本程序本批0CLI/0import/0新LP，旧negative不复扫；同批圆环原入口1次不混到这里。\n\n'+tb[tb.index('## 它攻击的数学量'):];tb=tb[:tb.index('本草稿只做源/输入读取')];tb=tb.replace('此草稿','此资源').replace('本草稿','本资源');tb+='本程序只做完整源/输入阅读与数学合同比较，本批0原CLI/0import/0新LP或SPE审计。旧报告继续只有两行有限null，无新增执行hash；[GAP-r](../候选/真实尾部最优利润的最小收益差额候选--候选.md)全r仍缺证明或真反例，r≤2、伪孩子和自由门槛删除各有准确归位。已有[孩子差额/低尾删除原审计](孩子差额摘要与低尾删除的定义级原审计--程序.md)的成功sourceSHA入口也不重复。\n'
def formal(path,title,ident,status,summary,body,ids):
 refs=[f"source:{s['commit']}:{s['path']}" for i in ids for s in inv[i]['sources']];head=['---','id: '+ident,'kind: program','type_tag: 程序','title: '+title,'status: '+status,'summary: '+summary,'source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs]+['---','',body];put(Path(path),'\n'.join(head))
formal(P,'八标签圆环的仿射独审合同','customer-attraction/cyclic-eight-label-affine-independent-original-audit','one-original-CLI-passed; exact-parameter-family-scope-no-new-general-theorem','保55有理划分与完整旋转策略、32120含自身比较和静态600加40对偶，原code一次0.8秒新隔离通过且525B全byte同，非新blind。',pb,IDS[:2])
formal(T,'固定完整策略对尾部聚合差额的锥攻击','customer-attraction/fixed-complete-strategy-tail-gap-cone-attack-scope','full-source-input-read; historical-two-input-floating-negative-only-no-new-run','全兴趣类型固定真策略锥/各真实背景终局和比较计数义务，830与196为LP尝试非成功数，保有理IC及正gap复验而权非负未再断言。',tb,IDS[2:]+RELATED)
for p,ss in [(P,sources[:2]),(T,sources[2:]+related)]:put(Path(p),(S/p).read_text()+'\n## 原件与实际证据资源\n\n'+'\n'.join('- ['+x['id']+' '+str(x['size'])+' B 原件](../../../../'+x['preserved_path']+')' for x in ss)+'\n'+('- [本次唯一原CLI完整日志](../../../../'+str(E/'actual-cyclic-original-fixture/execution-records/run-manifest.json')+')\n' if p==P else ''))
coverage=[{'id':IDS[0],'targets':[P],'units':['all4789code/guard/importglobalPAY/builtin12interesttypeaffine/nocanonicalimports','all64pairs3rolecoeff/lastBR/minsecondfloor/feasibleallpairs/rootminpiece/strictV','27positivecrossings55allcells/breakpoints/builtinpositiveq/completepolicy73x8inclself','static5q120backgroundlower plus8dualeachnotcount600','explicitlowrootterminalcoeff/q5trueBR/preassignednotSPE','actualneworiginalCLI1/same525stdoutfile/stderr0/nounitIDexpansion/notnewallmtheorem']},{'id':IDS[1],'targets':[P],'units':['all525all9fields/statusscope/27/55/32120/600/rootformula/Vformula','finiteqstatic vs55rootarrangement/actualstderr0/outputfullbytebinding notoldhistoryinvented']},{'id':IDS[2],'targets':[T,CG],'units':['all1192entry/date/internalbackup/awaitblind/notsharedchange/generalOPENhistorical','GAP-r+2barriers/deletionoldreport/summaryarithmeticnotnewrun','floatingconediscoverer/no oldwitness/needchildinnerIC/absolutevsdeficit','previousNBprogramactualsameSHAsuccessnotrepeat/oldhistorystays']},{'id':IDS[3],'targets':[T],'units':['all7040code/guard/ROOT/CLIexplicitpathsdefaultglob/caps/overwriteaftereachinput','readstrategypolicyfieldsfullkeys/dimensionfromdeclaredcounts/parserlimits/notcanonicalverifier','allnonemptytypes/actualσfinish/FractionfullICdedupzero/normalizationLP','r>=3 only/states(b,c)keepsdifferentrealcontinuations/allremainingoccupiedtopics/allqweakcompositions','LPchecksattempts/tolerances/failurecontinue/notexactdualnegative','rationalizationallICslack+strictgapchecked/nonnegativeweightsnotasserted/noInstance','exactreported2realinputfull259/85fields/actions/noextra primarydone/oldargvunknown','hitpayloadallfields/fixedwitnesssidecar/nulloldscope/notnewhalf or GAPproof']},{'id':IDS[4],'targets':[T],'units':['all436twoJSONrows/paths/p6m4rows305states7checks830 null/p4m4rows82states5checks196 null','rowsdistinctnonzero vsrawhistories/statesm4onlydepth0/1/checksLPattemptnotcountsuccess','noargs/version/sourceSHA/log/dualrecord/noallinputglobscopebinding/no newrun'] }];js(E/'semantic-coverage-map.json',coverage)
notes=[('4789B从全部会员Fraction系数/PAY全64对、BR/floor/可行对、仿射交点/完整旋转策略/静态5q600背景和另40对偶、guard/固定写入全文实读；内置输入无外部文件。','当前ML全参数定理/父审全文比较，原当时未取独审事实保留。55root划分不自动扩静态5q的域；本次sourceSHA真入口恰1次525输出全同，原读序非本次盲审。'),('525B全9字段/27正断点55探点32120含自身比较600静态背景/root分段/V及原status全部读。','新实际stdout525和文件525逐byte同；不把原报告无hash倒填旧执行，不将含自行动数写为严格偏离，不加40对偶到600字段。'),('1192B全入口从2026历史/一般状态、候选与两个停界、两audit及固定锥链接到后续义务实际全读。','GAP-r数学当前候选/父审已自足，两原audit已NB成功不重跑；此入口历史与最后probe的具体软件域本新资源补全，相关源不extra done。'),('7040B所有读取/递归缓存/全IC/状态/比较计数/LP/有理化/写入与CLI全读；两真实策略30602B全部259/85动作和字段已读。','当前GAP候选保局部解析，不由830/196null证明全r；source固定策略重赋所有兴趣重数，源码确查有理全IC及正gap但未再检查权非负，具体parser边界保清；0新negative执行。'),('436B全部两行各8字段及两个witness:null全读，两个报出源文件已核原字节全读。','305/82是去重非零IC行，7/5只m4余r≥3的深0/1，830/196是LP尝试含失败；原argv/sourceSHA/版本/成功状态/对偶缺失，不补成当前执行或普遍证据。')]
receipts=[]
for x,(a,b) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' actual原多组capture/subset/currentowner/sourceSHA核，前related全文诚实复用不冒第一读。','comparison_note':b,'decision_note':'integrated，独有完整软件/数学合同已自足归位，原件/依赖/当前目标版本/执行身份分别保。本批仅cyclic原CLI1/main数学主体确认1；gap0/原import0/成功后重复0，无新一般定理、blind、外审或mapper。','disposition':'integrated','targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
scope={'primary_sources':5,'primary_bytes':13982,'related_true_input_sources':2,'related_true_input_bytes':30602,'all_primary_and_related_full_semantic_read':True,'related_primary_receipts':0,'new_formals':2,'integrated':5,'raw_claim_ids':len(claim['ids']),'raw_claim_projected':False,'raw_sync_status_preserved':claim['local_sync']['status'],'original_CLI_calls':1,'confirmed_original_main_math_body_calls':1,'original_module_import_calls':0,'successful_same_SHA_reruns':0,'original_gap_negative_scans_repeated':0,'new_explicit_unit_ID_expansions':0,'cyclic_parameter_probe_audits':55,'cyclic_inclusive_action_obligations':32120,'static_background_checks':600,'additional_static_dual_equalities':40,'new_general_theorems':0,'new_blind_external_reviews':0,'preclaim_fullread_drafts_then_actualclaim_andonce_sourceCLI':True,'packaging_builder_calls':2,'preseal_editorial_refresh':'normalized strictroot ratio /a matches source q=b/a; waitingheading clarified after actualPASS; no frozen source/rerun changes','own_sharedGit_claim_done_checkpoint_show_network_accounts':0,'phase3_mapper':0};js(E/'read-scope-and-execution-identity.json',scope)
for p,n in [(C/'cyclic-parent-independent-audit-local-preparation/preclaim-full-source-understanding.json','actual-cyclic-preclaim-reading.json'),(C/'tail-gap-cone-probe-local-preparation/preclaim-full-source-and-input-understanding.json','actual-gap-preclaim-reading.json')]:cp(p,E/n)
put(E/'README.md','''# 圆环独审与尾部gap锥程序

五主源13982B全实读，另两真实策略30602B全部259/85动作/字段实读，5integrated/2新程序对象。原全多组claim/subset/owner/sourceSHA核，旧页当时未读保历史。

唯一cyclic原入口在新空副本恰1次exit0/stderr0，stdout525B/新525B报告与冻结全byte同，完整argv/env/Python/time/source/输出哈希保。55参数各73历史584含自身，共32120；静态五q600背景+40对偶另计，0单位ID展开/原import/成功后重复。一般族靠原解析，不新授定理或盲审。

gap旧negative0重扫；830/196只是LP尝试，305/82是去重IC行，7/5只深0/1，null无新执行/精确对偶。命中后确核有理IC和正gap，但没再断言权非负；原默认glob/argv未绑定，保具体复用边界。相关输入不extra done，无共享Git/网络/账号/mapper。
''')
put(W/'relation-review.md','''# 阶段二关系

圆环人类完整分类已ML保，本新独审对象加真实独立会员仿射实现/55参数完整策略/5q静态匹配和唯一新sourceSHA执行，未把两个静态/动态benchmark混用。旧父审当时未取这2件事实不倒改，新文件现在全读/实际执行另有证据。

GAP-r全r候选和伪菜单/删除停界已有数学对象；新程序保其固定策略全兴趣锥及两份真输入的有限LP范围，0旧negative重扫。均为实现/有限检查/证据身份的关系，不做phase3mapper、强行图连通或把阴性作普遍证明。根prefix/b/c及只攻击r>=3与完整IC全树范围分开；两真输入不extra done。
''')
cp(Path(__file__),E/'build_delivery.py');nextmp=C/'shared-family-author-and-review-local-preparation/local-export-manifest.json';nextrows=[]
for x in json.loads(nextmp.read_text())['rows']:
 p=REPO/'cleanup/progress'/f"{x['id']}.json";o=json.loads(p.read_text()) if p.exists() else None;nextrows.append({**x,'current_owner':o,'available_at_snapshot':o is None,'actual_fullread_as_preparation':True,'new_original_runs':0,'successful_receipts':0})
js(W/'next-candidates.json',nextrows);cp(C/'shared-family-author-and-review-local-preparation/preclaim-full-source-understanding.json',E/'next-candidate-actual-preparation-only.json')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex(t,c):return sum(1 for n in range(len(t)-1) if ord(t[n])==92 and t[n+1]==c and (n==0 or ord(t[n-1])!=92))
for x in sources+related:
 b=(S/x['preserved_path']).read_bytes();ck('sourceSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('fullclaimunprojected',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and set(IDS)<=set(claim['ids']));ck('ownerSHA',all(o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==inv[o['id']]['sha256'] for o in owners));ck('5integratedreceipts',len(receipts)==5 and {x['id'] for x in receipts}==set(IDS) and all(x['disposition']=='integrated' for x in receipts));ck('1actualcyclicPass',run['all_passed'] and run['exit_code']==0 and run['stderr']['bytes']==0 and run['output']['byte_equal_frozen'] and run['output']['stdout_exact_full_output']);ck('actualcounts',run['original_CLI_calls']==run['original_main_math_body_calls_confirmed']==1 and run['original_module_import_calls']==run['successful_same_SHA_reruns']==0);ck('all9outputfields',len(run['original_full_report'])==9 and run['original_full_report']['positive_breakpoints']==27 and run['original_full_report']['parameter_probes_including_all_breakpoints']==55 and run['original_full_report']['ordered_history_deviation_comparisons']==32120 and run['original_full_report']['static_count_profiles_checked']==600)
for x in runmap:ck('runtimearchive '+x['archived_path'],sha((S/x['archived_path']).read_bytes())==x['sha256'])
for x in comp:ck('currentcomparisonSHA '+x['path'],sha((REPO/x['path']).read_bytes())==x['sha256'] and sha((S/x['snapshot']).read_bytes())==x['sha256'])
links=[]
for p in [P,T]:
 t=(S/p).read_text();ck('flatmetadata '+p,all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));ck('TeXbalance '+p,tex(t,'[')==tex(t,']') and tex(t,'(')==tex(t,')'))
 for link in re.findall(r'\]\(([^)]+)\)',t):
  if ':' in link or link.startswith('#'):continue
  ok=((REPO/p).parent/link).resolve().exists() or ((S/p).parent/link).resolve().exists();links.append({'formal':p,'link':link,'exists':ok});ck('link '+link,ok)
js(E/'formal-link-check.json',links);ck('inputrows25985',[len(json.loads(Path(next(x for x in rows if x['id']==i)['local_path']).read_text())['actions']) for i in RELATED]==[259,85]);ck('gapoldreport2',len(json.loads((S/sources[4]['preserved_path']).read_text()))==2);ck('gap0oldnegative',scope['original_gap_negative_scans_repeated']==0)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+n+'/' in '/'+rel for n in ['original','necessary-related-original','comparison']);bad=[{'offset':i,'ord':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n'];trail=[i+1 for i,l in enumerate(t.splitlines()) if l.rstrip()!=l]
 if bad or trail:obs.append({'path':rel,'frozen':frozen,'C0':bad,'trailing_lines':trail})
 if not frozen:assert not bad and not trail,rel
js(E/'transport-format-observations.json',obs);js(W/'self-check.json',{'passed':all(x['passed'] for x in checks),'check_count':len(checks),'checks':checks,'formal_links':len(links),'actual_original_CLI':1,'original_gap_runs':0,'whole_repo_completion_claimed':False,'C0derivedexceptLF':True,'TeXignoreescapedrowbreak':True});put(W/'delivery.md','''# 圆环独审与tailgap五主源交付

5primary13982B全实读，2真实策略30602B全部259/85动作字段实读；5integrated/2自足程序对象。原full多组claim/subset/currentowner/sourceSHA核，旧父审/候选页当时未读的历史不覆。

新cyclic原CLI恰1次/main数学主体确认1/exit0/stderr0，525B stdout及新报告与冻结全byte同；55参数/32120含自身、600静态背景及另40对偶分开。gap原CLI0/旧negative0重复，原import0/成功后重复0。无新一般定理/blind/外审/mapper，Root先push证据正文再done。
''')
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and p.name not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'files':len(files),'bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_sources':5,'primary_bytes':13982,'related_input_bytes':30602,'formal_objects':2,'formal_bytes':sum((S/p).stat().st_size for p in [P,T]),'integrated':5,'checks':len(checks),'links':len(links),'original_CLI':1,'confirmed_math_main':1,'original_gap_runs':0};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False))
