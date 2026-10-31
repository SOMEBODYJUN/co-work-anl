from pathlib import Path
import json, hashlib, re
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='shared-omission-audit-and-terminal-menu-review-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');D=C/'lf-shared-audit-and-menu-review-drafts'
IDS=['218b9c0afd232e720c7a','a863ea48f22c76a1d877','5911bb1e25c90dd73580','3d9ac34ee71b4a777b02']
P='archives/customer-attraction/state/程序/共享遗漏常值均衡的定义级八树审计--程序.md';O='archives/customer-attraction/state/障碍/八标签末位真回复菜单的第二人偏离--障碍.md'
K='archives/customer-attraction/state/构造/实际遗漏全共享的常值均衡近二族--构造.md'
G1='archives/customer-attraction/state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md';G2='archives/customer-attraction/state/反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md';F='archives/customer-attraction/state/定理/五人半覆盖--定理.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,x):put(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 dest=S/q;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(Path(p).read_bytes())
claimpath=R/'boss4-r3-next-lf-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and len(claim['ids'])==17 and set(IDS)<=set(claim['ids']) and claim['remote_tip']=='b204a4422089b67af558bbfa1558184d64ccdc23'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};manpaths=[C/'kx-next-hamming-and-shared-audit-inputs/local-export-manifest.json',C/'kx-next-shared-audit-readme-input/local-export-manifest.json',C/'kx-next-shared-menu-review-context/local-export-manifest.json'];mats=[json.loads(x.read_text()) for x in manpaths];sources=[];owners=[]
for i in IDS:
 v=inv[i];x=next(x for m in mats for x in m['rows'] if x['id']==i);b=Path(x['local_path']).read_bytes();assert len(b)==x['size']==v['size'] and sha(b)==x['sha256']==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];p=E/'original'/i/v['path'];cp(x['local_path'],p);sources.append({**v,'preserved_path':str(p),'actual_local_path':x['local_path'],'read_scope':'entireactualoriginal semanticread includingallcode/JSONfields31actions/allREADME/assertions/all8379Bproofandtables; priorfirstreadhonestlyreused and exactsamebytesrechecked'});owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner)
assert sum(x['size'] for x in sources)==20872
js(E/'source-manifest.json',sources);js(E/'actual-primary-ownership-snapshot.json',owners);cp(claimpath,E/'actual-unprojected-claim-receipt.json')
for n,p in enumerate(manpaths):cp(p,E/'actual-local-read-manifests'/f'attempt-{n+1}.json')
contexts=[]
for p in [K,G1,G2,F]:
 b=(REPO/p).read_bytes();q=E/'comparison'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'scope':'KQsharedfullanalyticcomparison actuallyread; bankandfive currentstatement/status compared usingpriorfullmathematicalreading pluscurrenttargetedpass, currentcombinedcatwastruncated so notclaimednewfullreadingofallfiveproof; contextcopy itself notnewsource done'})
js(E/'comparison-manifest.json',contexts)
def refs(ids):
 return [f"source:{s['commit']}:{s['path']}" for i in ids for s in inv[i]['sources']]
def formal(p,id,title,kind,type_tag,status,summary,ids,body):
 rows=['---','id: '+id,'kind: '+kind,'type_tag: '+type_tag,'title: '+title,'status: '+status,'summary: '+summary,'source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs(ids)]+['---','',body];put(Path(p),'\n'.join(rows))
formal(P,'customer-attraction/shared-omission-constant-eight-tree-definition-audit','共享遗漏常值均衡的定义级八树审计','program','程序','finite-original-report-and-full-source-reviewed; no-new-execution','单位客户Fraction全有序八树与31节点生成证书分开，保OPT支持枚举等价、默认stdout及独占写入时序。',IDS[:3],(D/'shared-program-body.md').read_text())
formal(O,'customer-attraction/eight-label-terminal-BR-menu-second-deviation','八标签末位真回复菜单的第二人偏离','obstruction','障碍','proved-menu-nonextendability-in-stated-window; historical-independent-internal-review','静态v4=(23a+10b)/16双证与真实末位全回复证明9a/2<b≤25a/2菜单不能补成完整SPE，含精确边界与两全表。',[IDS[3],IDS[2]],(D/'menu-obstruction-body.md').read_text())
report=json.loads((S/sources[1]['preserved_path']).read_text());cases=report['cases'];cert=report['complete_finite_certificate'];code=(S/sources[0]['preserved_path']).read_text()
coverage=[{'id':IDS[0],'disposition':'integrated','targets':[P],'complete_units':['allimports/build/unitutility/allorderedhistoryfullIC/combinationssupportsOPT/allassertions+Gliteral','main8casesonly/optionalexclusiveoutputaftercalculations/stdoutwithoutcertificate','small_certificate31actions generatednotninth auditedcase/noexternaldependencies/noexecutionhashlog']},{'id':IDS[1],'disposition':'integrated','targets':[P],'complete_units':['status/scope/all8casefields/totals15632and138792','all5explicitcovers/all31orderedactions/actual000','allmin0/degree2/G0/eightdistinctinputsnotreplaycounts/co-versionnotindependentlog']},{'id':IDS[2],'disposition':'integrated','targets':[P,O],'complete_units':['CONST/BG/near2 alreadyfullKQnotnewtheorem','bothauditsandindependentmenusreview uniquev4/fullBRboundary accountedfor','historicalroleinstructions notcurrentcommands/repeatedroutesand71Gscope/currentfive vs sixOPEN','menureviewprogramJSON onlynavigationnotreadordone']},{'id':IDS[3],'disposition':'integrated','targets':[O],'complete_units':['all6sections historicalbefore/afterreadorder/authororbit/noexternalreview','unit8triple4distinctpair/N/degeneracy/fullPAY/menuvaluesW','integerbalancinglowerbound+8rotationmatchingupper/allnonnegativev4','last04allBR/windowclosedupperopenlower/alldifferences','all8last02payoffs/gaps/uniqueBRexacta>0b>=0/forcedsecondgain','all8secondBRsetsandpaysets/opencone rays/all64prefixrotation/6worsttailmoves','a1b5allnumbers/OPT3proof/nonhalf/currentbankcorrection/MDauditcountsnotcurrentcodeverified']}]
js(E/'semantic-coverage-map.json',coverage)
readscope={'primary_sources':4,'primary_bytes':20872,'all_originals_full_semantic_read':True,'code_bytes':4037,'original_JSON_bytes':6708,'README_bytes':1748,'independent_review_MD_bytes':8379,'all_eight_cases_fields_read':True,'all_certificate_actions_read':31,'original_CLI_calls':0,'original_module_imports':0,'new_mathematical_runs':0,'old_success_replays':0,'new_solver_random_LP_BI_SPE_runs':0,'review_audit_code_JSON':'notread/notexecuted/notdone; MDreportedfinitecountsaccuratelyattributed','new_formals':2,'existing_shared_general_family_theorem':'precise reuse notnew theorem','raw_claim_ids':17,'primary_intersection':IDS,'raw_claim_projected':False,'claim_sync':'synced-original','own_shared_Git_or_claim_done_checkpoint_show_calls':0,'network_lazyfetch_real_account_operations':0,'phase3_mapper':0,'safe_local_helper_calls_for_next':1,'safe_next_exports':3,'safe_next_missing':0,'next_code_JSON_author_MD':'byteverifiedonlybeforeLFseal; notyetsemanticread','packaging_builder_calls':1,'packaging_failures':0}
js(E/'read-scope-and-execution-identity.json',readscope)
notes=[('4037B实际完整源码全部函数/main/导入/写入时序已读，byte/SHA256/blobSHA1/新17原claim本4owner核；无原import/CLI。','已有KQ构造自足CONST/BG及一般族，本批新程序资源补真实显式单位客户/全部有序史/不同支持OPT等价、所有assert及G0字段数学来源。main8组，m3a2仅small_certificate生成，open(x)在八audit之后。','integrated到新程序对象；解析普遍证明不由有限八树替代，冻结通过非本轮新run，无历史argv/sourceSHA日志不冒有。'),('6708B原JSON全字段/八case/全部31有序history动作/五覆盖/000路径实际读，源bytes与库存及当前owner核。','新程序对象完整八行表和15632/138792总数、零slack/度2/G0都有语义去向，完整31映射原件保。m3a2证书仅生成非第九audit，case计数不当CLI次数。','integrated；与源码同版本逐项对应但原JSON无代码hash/argv/Python/退出码/时间，不把co-version当独立旧运行日志，0新复跑。'),('1748BREADME全部链接/路线/作者历史状态实际全文读；相关7316B一般族完整既读、8379B菜单独审现primary完整读。','近二数学已有KQ准确去向；README独有菜单审查不止导航，v4双证/全部偏离/窗口现新障碍全文保。源码输出用途现程序对象保；其列的另两菜单audit文件本批仅导航未读不extra done。','integrated到程序+障碍；旧禁git消息和主目标OPEN只是2026-10-23历史，五人现已证/六人仍开放，71G加强桥和当前银行逐人/Mfull失败分开。'),('8379B六节全部定义/证明/两表/数值/先盲后读次序/附报告范围实际完整读，当前owner/sourceSHA精确核。','全仓检索未见其73/16、23a+10b、9a/2窗口完整对象；新障碍自足静态整数双证、每列末位真BR、强制偏离及开扇形全回复，原author对偶同轨道仅按此MD已读比较记，不冒本轮读作者程序。','integrated；不是SPE反例/half反例/真正逐人extra-one反例。原内审通过身份、当时OPEN与当前银行反族分开，原审计代码JSON未读/未run，0新数学运行不发明外审/新颖性。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 完整17原receipt原样保，只取本4实际交集，不投影。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 关系与对象分工

现KQ一般共享遗漏构造负责CONST/BG、任意m/a及支架全部SPE福利界；本程序对象负责其独立定义级实现/原八份有限报告/小证书和执行边界。原README把这些导航到同一数学目录；不为数量重复造一般定理。

新菜单障碍以同单位模型另一个三人八标签族证明“指定每列末位BR仍不足完整SPE”。静态v4是query前固定三竞争主题的安全值，完整真实后继由第二次偏离强制；不可把两观察顺序或菜单与完整σ混同。两整表、窗口和退化边界完整保，不是简单导航。

原独审先盲后读和MD自报程序范围照原身份保，当前整理不变成新盲审。五人half他证、银行逐人extra-one/Mfull他例与本非SPE菜单身份分开，聚合桥不被额外误否。阶段二明确这些关系但不创建阶段三图边、不强制连通。
''')
put(E/'README.md',r'''# 共享遗漏定义级审计与末位菜单审查

四primary20872B完整实读：4037B纯stdlib/Fraction代码、6708B全JSON/31动作、1748B入口、8379B独审六节及两完整表。2自足正式对象、4integrated；已有一般族数学准确复用，未重复造定理。

原8case15632历史/138792含自身比较；m3a2的31节点是生成证书而非main第9审计。默认stdout删证书，--output独占新建在八计算之后。冻结输出没sourceSHA/argv/runtime独立日志，不因co-version说当前新run。

菜单解析双证v4=(23a+10b)/16保完整窗口和全部末位/第二BR边界；主窗口真实强制第二偏离排除任意SPE补全，福利又过half。原先盲后读是作者历史，原另两菜单审计源码JSON本批未读/未跑，不额外done。

原17claim实际pushed/synced及本4owner/sourceSHA核后才写成功receipts；0原CLI/import/数学重跑/共享Git/网络或账号操作。Root先推实际正文/证据再逐源done。
''')
nextmf=C/'lf-next-menu-review-and-author-local-inputs/local-export-manifest.json';nm=json.loads(nextmf.read_text());assert not nm['missing'] and len(nm['rows'])==3;nextrows=[]
for x in nm['rows']:
 p=REPO/'cleanup/progress'/f"{x['id']}.json";assert not p.exists();b=Path(x['local_path']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256'];nextrows.append({**inv[x['id']],'local_path':x['local_path'],'owner_observed':None,'read_status':'actualbyteverifiedonlybeforeLFfreeze; no primaryreceipt/no semanticread/no mathrun'})
cp(nextmf,E/'next-original-local-input-manifest.json');js(W/'next-candidates.json',nextrows)
cp(D/'preclaim-reading-scope.json',E/'actual-preclaim-reading-scope.json');cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in sources:
 b=(S/x['preserved_path']).read_bytes();ck('source sizeSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('source blob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('actualraw17claim',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and len(claim['ids'])==17 and set(IDS)<=set(claim['ids']));ck('currentownerSHA',all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('20872all4',sum(x['size'] for x in sources)==20872)
ck('8completeJSONcases',len(cases)==8 and [(x['players'],x['block_size']) for x in cases]==[(m,a) for m in range(2,6) for a in (1,3)]);ck('allfrozenfinitecounts',report['totals']=={'ordered_histories':15632,'action_comparisons_including_self':138792} and all(x['minimum_slack']=='0' and x['actual_only_waste']==0 and x['omitted_maximal_degree']==2 for x in cases));ck('31completegeneratedactions',len(cert['actions'])==31 and cert['actual_path']==[0,0,0] and all(x['action']==0 for x in cert['actions']) and [len(x['history']) for x in cert['actions']]==[0]+[1]*5+[2]*25);ck('smallcertificateinput',cert['topics']==[[0,1,2,3,4,5,6],[0,7,8],[1,7,8],[0,9,10],[1,9,10]] and cert['unit_customer_count']==11)
ck('noaudit3_2call','audit(3, 2)' not in code and 'for m in range(2, 6) for a in (1, 3)' in code);ck('originalwritesafteraudits',code.index('reports = [audit')<code.index('args.output.open("x")')<code.index('print(json.dumps'));ck('originalmainhasguard','if __name__ == "__main__"' in code);ck('noexecutionmetadataJSON',not any(k in report for k in ['source_sha256','argv','python','elapsed','exit_code']))
for p in [P,O]:
 t=(S/p).read_text();ck('flatmetadata '+p,t.startswith('---\n') and all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));ck('TeX displaybalanced '+p,t.count('\\[')==t.count('\\]'));ck('TeX inlinebalanced '+p,t.count('\\(')==t.count('\\)'))
pt=(S/P).read_text();ot=(S/O).read_text();ck('program9thauditboundary','不是第九份程序已核验树' in pt and '八份核验**之后**' in pt);ck('menu fullwindow/allboundaries','9a/2<b\\le25a/2' in ot and 'a=0,b>0' in ot and 'b=a' in ot and 'a>0,b≥0' in ot);ck('fulltwotables',all('| '+str(i)+' |' in ot for i in range(8)) and '23/6' in ot and '5/2' in ot);ck('reviewcodeJSONnotclaimedread','本批未读或运行那份审计代码/JSON' in ot);ck('currentglobalstates','完整根菜单反例' in ot and '六人half仍需' in ot and '不是half反例' in ot);ck('all4receipts',len(receipts)==4 and {x['id'] for x in receipts}==set(IDS) and all(x['disposition']=='integrated' for x in receipts));ck('zerooriginalruns',readscope['original_CLI_calls']==readscope['original_module_imports']==readscope['new_mathematical_runs']==readscope['old_success_replays']==0)
links=[]
for p in [P,O]:
 t=(S/p).read_text()
 for link in re.findall(r'\]\(([^)]+)\)',t):
  if ':' in link or link.startswith('#'):continue
  target=((S/p).parent/link).resolve();repo=((REPO/p).parent/link).resolve();ok=target.exists() or repo.exists();links.append({'from':p,'link':link,'exists_in_stage_or_current_repo':ok});ck('formal link '+link,ok)
js(E/'formal-link-check.json',links)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen='/original/' in '/'+rel or '/comparison/' in '/'+rel;bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('derivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_original_and_comparison_unchanged':True})
put(W/'delivery.md',f'''# LF四源完整交付

4primary20872B全实读，2正式对象；共享族通用定理已有KQ，本批只补完整定义级实现/有限输出与小证书；菜单独审的静态双证/两全表/边界新自足保。4integrated、0额外引用source done。

原17receipt {claim['remote_tip']} pushed/synced原字节、本4owner/sourceSHA已核；不投影。0原CLI/import/数学/LP/SPE/旧成功复跑。菜单另两审计代码JSON未读不冒认证；MD历史自报和真正本轮阅读分开。

下一3本地齐16422B，LF封包前仅byte未语义读，未claim/receipt；Root持续串行认领保存，本代理无sharedGit/网络/账号操作。先推本批实际正文/证据再done。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_links':len(links),'new_formals':2,'scope':'full4source/alluniqueproofs/tables/codeinput/executionboundary/currentsemanticcomparison/actualclaimownerSHA/sourcebyte/formalformat/links','not_a_new_mathematical_audit_run':True})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':20872,'receipts':4,'dispositions':{'integrated':4},'new_formals':2,'new_formal_bytes':sum((S/p).stat().st_size for p in [P,O]),'checks':len(checks),'formal_links':len(links),'raw_claim_ids':17,'claim_tip':claim['remote_tip'],'raw_sync_status':'synced','new_math_runs':0,'original_CLI_calls':0,'old_success_replays':0,'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
