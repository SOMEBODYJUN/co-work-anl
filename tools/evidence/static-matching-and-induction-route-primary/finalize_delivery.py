from pathlib import Path
import json,hashlib,re,posixpath

R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-static-matching-and-induction-route-primary';E=Path('tools/evidence/static-matching-and-induction-route-primary');W=Path('cleanup/workspaces/Boss4/r3-static-matching-and-induction-route-primary-next')
IDS=['1180cae0f024e775d79a','a7579960b289fff40c97','50c0718e3bf1ceb1d744','bb80664d0d0c61cbe335'];P1='archives/customer-attraction/state/反例/最优组合冻结匹配的一单位缺口--反例.md';P2='archives/customer-attraction/state/资料/双尾推送与单色续局的版本接口--资料.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def rd(p):return json.loads((S/p).read_text())
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};claimpath=R/'boss4-r3-next-fj-claim.json';claim=json.loads(claimpath.read_text())
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==set(IDS)
ownership=[]
for i in IDS:
 x=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[i]['sha256'];ownership.append(x)
cp(claimpath,E/'actual-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',ownership);cp(Path(__file__),E/'finalize_delivery.py')
primary=rd(E/'source-manifest.json');related=rd(E/'related-source-manifest.json');contexts=rd(E/'context-manifest.json')
reusedpaths=set()
for m in ['r3-weak-pushforward-and-static-prefix-primary/tools/evidence/weak-pushforward-and-static-prefix-primary/context-manifest.json','r3-two-tail-pushforward-and-full-menu-boundaries-primary/tools/evidence/two-tail-pushforward-and-full-menu-boundaries-primary/formal-resource-manifest.json']:
 for x in json.loads((C/m).read_text()):
  n=x['path']
  if not any(t in n for t in ['笛卡尔银行','末位真实回复推送','后继边际价格付款']) or n in reusedpaths:continue
  b=(REPO/n).read_bytes();assert sha(b)==x['sha256'];q=E/'context-reused'/n;cp(REPO/n,q);contexts.append({'path':n,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_status':'previously fully read EX/EG; current same SHA verified, no pretended new first reading','previous_manifest':m});reusedpaths.add(n)
assert len(reusedpaths)==4;js(E/'context-manifest.json',contexts)
scope={'primary_sources':4,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'primary_full_actual_semantic_read':True,'JSON_reading':'Original lossless tree: 10 top fields, full instance22 customer records, both certificate fields including all259 histories/actions in slices0..129 and130..258, actual/payoffs/counts/unique support/min query/min matching/all24 assignment pairs; pretty first450lines also read. No tail omitted.','previous_EX_role':'availability only, not prior full primary reading','related_full_text_sources':3,'related_full_text_bytes':sum(x['size'] for x in related),'fresh_current_formal_contexts':7,'same_SHA_previous_full_formal_contexts':4,'original_CLI_calls':0,'new_mathematical_program_calls':0,'new_full_SPE_replays':0,'new_matching_or_optimization_scans':0,'new_fixed_root_arithmetic_calls':0,'reused_successes':'same original10829B origin audit, old once-six-fixture run including identical52 input; current contribution is reading/binding only, not an extra run or extra samples','scope_not_expanded':'origin consumes instance+actions and rechecks fixed optimal tuple; does not certify original all_assignments/unique_optimal_supports fields. Complete matching and unique support explained analytically in new body.','safe_local_export_helper_calls':1,'helper_local_blob_attempts':6,'helper_exports':3,'helper_absent_blobs':3,'absent_ids':['4638f7b82684049fdae6','1894bab391f4c921d293','b03448e16b1090d7a08f'],'derived_builder_calls':2,'derived_builder_failures':1,'builder_recovery':'one source-record dictionary indexing error before body writing, corrected file-only rerun; mathematical executions remain0','network_or_lazy_fetch':0,'shared_Git_writes':0,'clean_show_claim_done_checkpoint_calls':0,'phase3_mapper_or_graph_import':0,'mathematical_addition':'manual/private-client unique OPT support proof; baseline price increments classify all24 frozen matchings; faithful full-policy rendering; current route truth correction','no_current_claim':'new solver optimality, global52 minimality, universal half, external review, or novelty'}
assert scope['primary_bytes']==39393 and scope['primary_lines']==2551 and scope['related_full_text_bytes']==11502;js(E/'read-scope-and-evidence-status.json',scope)
coverage=[
{'id':IDS[0],'units':['exact every-instance/every-SPE/exist-optimal/exist-assignment frozenQ<=W claim','all22 unit customer rows and full policy/actual values','all optimal supports/repeats quantified','4x4 frozen matrix and all24 matching values','unconditional OPT<=Q+(1-1/m)W proof and weaker threshold (1+1/m)W','search/cone/integer discovery exact finite author scope, no optimizer premise','old independent review identity versus locally missing original code/report','Q versus realV versus partitionR and current half boundaries'],'targets':[P1],'disposition':'integrated'},
{'id':IDS[1],'units':['all10 top fields','all instance topics/customer interests/multiplicities/players','both certificate fields, all259 distinct ordered histories/actions','actual3322/welfare47/optimum52/four47/4 payoffs','terminal_counts002200 is not full strategy','unique_optimal_supports0145 and min matching0514/query48','every24 target/query record, two12-item rational groups','input identity to old actual SPE validation; unconsumed附带fields not falsely included'],'targets':[P1],'disposition':'integrated'},
{'id':IDS[2],'units':['personal backup/oldrole and generalOPEN dated scope','r2sharp theorem arbitrarybackground/p versus r>=3; realBRslack','old weakWP OPEN current refuted separately from34strong example','full root menu/META route and r2pure defense/791/348/nonSPE obligations','individualmixed/extraoneOPEN corrected to bank counterfamily','tail strengthening15unit14topic s13t1/3 gap1/351 nonMETA and originalreviewpending scope','full source pointers and no repeated negative scans as proof'],'targets':[P2],'disposition':'integrated'},
{'id':IDS[3],'units':['2026-10-22 personal history/currenttarget separated','VA handoff r1 identity and same-background staticmonochrome PNEglobalPhi independent lemma','frequencyfilterduplicate status and crossbackground missing obligation','probe floating/no frozenfullrun and actual missingcode','r-slot fullminimax versus r-1 tail menu and old381 rational record author-only','historical next FM route versus currentbankrefutation; extraone/free-root/half separated'],'targets':[P2],'disposition':'integrated'}]
js(E/'semantic-coverage-map.json',coverage)
notes=[
('4111B主稿全部正文、22客户表、精确存在量词、259节点证书说明、最优支持与24匹配、条件弱化和发现/审查边界首次数学全文实读。','同32574B原JSON全字段、2869B独审全文、既有origin全策略代码/旧run绑定、当前Q/R精确资源和净差真实V逐项比较。','两项解析穷尽明确唯一0145与全24值；整主题Q反例完整归位，不冒真实V/R/half失败或发现solver最优性。'),
('32574B原JSON完整无损树实读，10顶层字段、22类单位客户、全部259有序history/action、两certificate字段及所有24target/query项；没有未读尾部。','旧同SHA origin程序已成功核本输入259节点1554含自身比较，本批核真实依赖/代码/执行SHA而不重跑；该代码未消费all_assignments/unique支持，故补解析穷尽而不扩大旧run范围。','原字节完整归档，259动作表与全部24匹配逐项进新正文；JSON存储断言、已有定义级SPE和新手工推导身份分清，不把再读算一次新验证。'),
('1406B归纳README全部段落和三个后续稿指针、锐式、强弱推送、完整菜单/META、tail价格族及旧审查状态完整实读。','与现r2sharp、TAIL15客户解析、银行m4全菜单/弱式/整数extraone反驳、348/791证据和根+末BR非SPE模板比较。','自足资源准确保每条用途和量词，原OPEN/独审待安排保历史而当前普遍个体目标按真反例纠正，r2正面和half不被误退休。'),
('1302B树README全部日期/个人备份及VA稿、浮点探针、完整r槽接口用途和下一步全文实读。','3843B VA全文与4790B fullmenu全文均已实际比较；原两独审及探针代码实际本地缺，旧381数字仅按作者记录；当前FM/extraone失败与VA跨背景义务区分。','保r1真恒等式、单色同背景全局势独立引理及频次筛选去重来源；原静态引理不替真实多后继，不用少量浮点阴性或菜单名字代一般证明。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' pushed/synced原回执与当前Boss4 owner/sourceSHA实际核验。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 阶段二实际关系

52客户完整有序SPE和唯一最优支持/所有匹配共同反驳强冻结Q≤W。完整SPE旧成功只消费instance/actions；最优唯一和24Q的解析穷尽单独保，不能从同一文件SHA跳成全部附带断言均被旧程序认证。Q、真实改历史V、分区一次收费R有不同分母/回复/去重规则，强Q失败不代替其他桥；本例弱Q阈值仍满足，分区R普遍失败来自另一个14客户真例。

两README是同工作区不同资源角色，个人命令作历史。r2任意背景强推送保真；r>=3强失败不直接反弱/菜单，但当前普遍弱WP、个体FM/整数extraone另已有银行真反族。静态v≥OPT/(2m)与条件half蕴含保真，聚合/自由根/六人half不混。

单色静态全B的PNE全局势引理和r1三真实比较独立有效。跨背景多后继义务不因该势引理或阴性浮点样本关闭。旧381/791有限作者记录与缺输入当前边界保留。本批仅数学关系审查，不生成第三阶段mapper/超图或强制连边。
''')
nextrows=[]
for x in related:
 assert not (REPO/'cleanup/progress'/f"{x['id']}.json").exists()
 nextrows.append({**x,'local_path':str(S/x['preserved_path']),'progress_observed':None,'primary_read_status':'already full related mathematical read in FJ, not primary completed; may honestly reuse same SHA after actual claim','claim_condition':'Root rechecks actual current ownership and pushed intersection only'})
js(W/'next-candidates.json',nextrows)
put(W/'delivery.md',f'''# 交付

FJ4 actual claim {claim['remote_tip']} pushed/synced，4owner及sourceSHA吻合。四主源39393B/2551行，三MD首次完整数学读取，32574B JSON全部字段/259策略动作/24匹配无损分块实读。两个新自足对象/4receipt。

完整52客户冻结匹配强桥反例保22客户与全259节点、唯一0145解析及24项两价格穷尽，和真实V/分区R/half阈值分清。两README旧WP/FM/extraoneOPEN按银行真族纠正，保r2定理、VA跨背景与同背景静态势不同职责。

原CLI、新数学/全SPE/固定根/优化扫描均0，旧同SHA成功只复用。安全本地helper1次6尝试=3必要MD齐+3缺，无网络。派生builder1次记录字典索引失败后修正重写，原件与数学程序未改。下批3实际可读relatedMD已全文比较但未primary done，可诚实复用。

Root按copy-files.json精确白名单串行复制，依赖正文先pushed后逐源done；本代理未sharedGit/claim/done/checkpoint/show/认证/公屏/网络。
''')
rp=E/'README.md';t=(S/rp).read_text().replace('实际claim/owner与成功receipt待Root pushed后独立生成','实际claim/owner已核pushed/synced，成功receipt已独立生成，正文仍待Root串行推送后done');put(rp,t)
checks=[]
def ck(n,v,detail=None):
 d={'check':n,'passed':bool(v)}
 if detail is not None:d['detail']=detail
 checks.append(d);assert v,n
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();v=inv[x['id']];ck('exact size/SHA '+x['id'],len(b)==v['size'] and sha(b)==v['sha256']);ck('exact blobSHA1 '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'])
ck('actual unprojected4 capture preserved',(S/E/'actual-claim-receipt.json').read_bytes()==claimpath.read_bytes())
for x in ownership:ck('actual primary ownership '+x['id'],x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'])
for x in contexts:
 b=(S/x['snapshot']).read_bytes();ck('exact current/read-reused context '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
old=rd(E/'reused-evidence-manifest.json')
for x in old:
 b=(S/x['path']).read_bytes();ck('exact old evidence '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
ex=rd(E/'reused-evidence/replay/execution.json');out=(S/E/'reused-evidence/replay/original.stdout.txt').read_bytes();report=rd(E/'reused-evidence/replay/origin_retraction_exact_audit.json');inputs=rd(E/'reused-evidence/replay-input-manifest.json')
ck('old actual success and output binding',ex['exit_code']==0 and sha(out)==ex['stdout_sha256']==ex['generated_sha256']==ex['frozen_sha256'] and ex['generated_bytes_equal_frozen']);ck('exact primary consumed old input binding',report['active_fixture_sha256']==inv[IDS[1]]['sha256'] and next(x for x in inputs if x['id']==IDS[1])['sha256']==inv[IDS[1]]['sha256'])
fixture=next(x for x in report['audits'] if x['name']=='unchanged_52_unit_complete_SPE_max_future');ck('old52 scope kept distinct',fixture['complete_history_IC_checks']==1554 and fixture['m']==4 and fixture['unit_clients']==52)
d=json.loads((S/next(x['preserved_path'] for x in primary if x['id']==IDS[1])).read_text());ck('full actual JSON schema',set(d)=={'instance','certificate','actual','welfare','optimum','payoffs','unique_optimal_supports','minimum_query','minimum_assignment','all_assignments'} and set(d['certificate'])=={'terminal_counts','actions'});ck('full original fields policy/assignment counts',len(d['instance']['customers'])==22 and len(d['certificate']['actions'])==259 and len(d['all_assignments'])==24)
links=[]
for p in [P1,P2]:
 t=(S/p).read_text();ck('flat MATEK '+p,all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('all nonLF C0 zero '+p,not any(ord(c)<32 and c!='\n' for c in t));ck('trailing whitespace zero '+p,all(l==l.rstrip() for l in t.splitlines()));ck('TeX display balanced '+p,t.count('\\[')==t.count('\\]'));ck('all generated placeholders resolved '+p,not any(k in t for k in ['CUSTOMERS','THIRD','LAST','MATCH']))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  n=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));a=S/n if (S/n).exists() else REPO/n;ck('actual relative link '+dest,a.exists());links.append({'source':p,'destination':dest,'resolved':n,'bytes':a.stat().st_size,'sha256':sha(a.read_bytes())})
js(E/'formal-link-check.json',links)
a=(S/P1).read_text();b=(S/P2).read_text();ck('full259 policy rendered without count-only summary',all('| '+str(x)+','+str(y)+' |' in a for x in range(6) for y in range(6)) and '根规定3' in a and '(2,0,3,3,2,0)' in a);ck('all24 stored assignments actually preserved',all('| '+','.join(map(str,x['target']))+' | '+x['query']+' |' in a for x in d['all_assignments']));ck('complete analytic counterproof and weak scope','此槽必须为0' in a and '281/6' in a and '2·3!=12' in a and '(1+1/m)W' in a and '263/12' in a);ck('both route current truth and positive components','4/3<19/14=t5≤v5' in b and 'r=1、r=2的强式有效' in b and '同背景的有效独立引理' in b and '不支付VA缺的跨背景比较' in b)
ck('correct primary full read totals',scope['primary_bytes']==39393 and scope['primary_lines']==2551);ck('no mathematical runs repeated',scope['original_CLI_calls']==scope['new_mathematical_program_calls']==scope['new_full_SPE_replays']==scope['new_matching_or_optimization_scans']==0);ck('actual helper and missing contract',scope['safe_local_export_helper_calls']==1 and scope['helper_local_blob_attempts']==6 and len(rd(E/'missing-local-inventory-bindings.json'))==3)
ck('exact4 complete receipts',len(receipts)==4 and {x['id'] for x in receipts}==set(IDS))
for x in receipts:
 ck('complete semantic receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']))
 for p in x['targets']:ck('actual receipt target '+p,(S/p).exists())
ck('exact2 own new formals',sorted(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))==sorted([P1,P2]))
for x in rd(E/'formal-resource-manifest.json'):
 z=(S/x['path']).read_bytes();ck('formal resource SHA '+x['path'],len(z)==x['bytes'] and sha(z)==x['sha256'])
ck('next3 actually readable and not primary done',len(nextrows)==3 and all(Path(x['local_path']).exists() and sha(Path(x['local_path']).read_bytes())==x['sha256'] for x in nextrows))
obs=[]
for p in S.rglob('*'):
 if not p.is_file() or p.name in ['copy-files.json','copy-paths.txt','delivery-summary.json']:continue
 try:t=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()]
 if bad:obs.append({'path':str(p.relative_to(S)),'lines':bad,'frozen':any('/'+z+'/' in str(p.relative_to(S)) for z in ['original','related','context','context-reused','reused-evidence'])})
ck('all derived trailing whitespace zero',not any(not x['frozen'] for x in obs));js(E/'transport-whitespace-observations.json',{'observed':obs,'frozen_originals_unchanged':True})
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'scope':'Actual source and input/old-execution SHA binding, complete analytical coverage, metadata/C0/links/receipts/transport; not another SPE/matching run or universal proof.'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  z=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(z),'sha256':sha(z)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':scope['primary_bytes'],'primary_lines':scope['primary_lines'],'new_formals':2,'formal_bytes':sum((S/p).stat().st_size for p in [P1,P2]),'receipts':4,'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'claim_tip':claim['remote_tip'],'next_actual_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
