from pathlib import Path
import hashlib,json,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='shared-seats-probe-scope-and-review-history-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');D=C/'shared-seats-entrance-and-probe-scope-drafts'
IDS=['e730733ff3146f1a9bd9','34ead0e38af5c08cf938','52b1c782e458f410044a'];PROBES=['0da9b22c0235c8d60a32','7f135c486ea538542a18','8f0545ba3822ebcb4a36','c141dd3d493d865ea8ae','2132682e0de90747076e'];CAN=['999293c4e866618a72f6','14e0922138e43b337600','52369ae591b07d52c7df']
P='archives/customer-attraction/state/资源/平行共享遗漏的有限筛查与盲审入口--资源.md';N='archives/customer-attraction/state/程序/唯一最大主题选根边界的两份有理审计--程序.md';V='archives/customer-attraction/state/审查/圆环可信性父审的旁支合同与证据身份--审查.md';H='archives/customer-attraction/state/反例/支持外枢轴修复与静态查询平均的两人分离族--反例.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 d=S/q;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(Path(p).read_bytes())
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids']);assert len(set(claim['ids']))==len(claim['ids'])
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};mps=[C/'hub-audits-required-review-context-local-inputs/local-export-manifest.json',C/'shared-seats-readme-next-local-input/local-export-manifest.json',C/'shared-seats-required-probe-sources-local-inputs/local-export-manifest.json'];rows=[x for p in mps for x in json.loads(p.read_text())['rows']];sources=[];related=[];owners=[]
for i in IDS+PROBES+CAN:
 v=inv[i]
 if i in CAN:p=REPO/'tools/evidence/collaboration-model-and-cag-audit-primary/related-inputs'/i/v['path']
 else:p=Path(next(x for x in rows if x['id']==i)['local_path'])
 b=p.read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/('original' if i in IDS else 'frozen-canonical-dependencies' if i in CAN else 'necessary-related-original')/i/v['path'];cp(p,q);rec={**v,'preserved_path':str(q),'actual_read_scope':'all original text/code, current counterpart fullsemanticread; no new program execution/import'};(sources if i in IDS else related).append(rec)
 if i in IDS:
  owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner)
assert sum(x['size'] for x in sources)==12485 and sum(inv[i]['size'] for i in PROBES)==14031
js(E/'source-manifest.json',sources);js(E/'necessary-related-manifest.json',related);js(E/'actual-owner-snapshot.json',owners);cp(claimpath,E/'actual-unprojected-claim-receipt.json')
for j,p in enumerate(mps):cp(p,E/'actual-local-manifests'/f'input-{j+1}.json')
comp=[]
for p in [N,V,H]:
 b=(REPO/p).read_bytes()
 if p==N:assert b==(C/'r3-max-standalone-hub-two-original-audits-primary'/p).read_bytes()
 if p==H:assert len(b)==5013 and sha(b)=='8010da26ec4a576b6f810007c83616207825b6fed882e00fa9e7ed4ea56ff403'
 q=E/'comparison'/p;cp(REPO/p,q);comp.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'scope':'actual complete corresponding formal read and exact source-domain/semanticcomparison; no extra source done'})
js(E/'comparison-manifest.json',comp)
refs=[f"source:{s['commit']}:{s['path']}" for i in IDS+PROBES+CAN for s in inv[i]['sources']];front=['---','id: customer-attraction/parallel-shared-omission-finite-probes-and-review-history','kind: resource','type_tag: 资源','title: 平行共享遗漏的有限筛查与盲审入口','status: historical-finite-probe-reports; source-level-domain-audit; general-parallel-candidate-open','summary: 完整保平行块P/Cov及r2停界、五有限探针的预筛和策略锥量词、默认次数与原报告差别及两种hub家族；本批0新运行。','source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs]+['---','',(D/'resource-body.md').read_text()];put(Path(P),'\n'.join(front));put(Path(P),(S/P).read_text()+'\n## 原件与读取资源\n\n'+'\n'.join('- ['+x['id']+' '+str(x['size'])+' B 原件](../../../../'+x['preserved_path']+')' for x in sources+related)+'\n')
coverage=[{'id':IDS[0],'disposition':'duplicate','targets':[N,V],'units':[{'source_unit':'complete customer design/M even/privatepositive/Huniquemax/intersection','target':N,'location':'输入构造与同一完整策略'},{'source_unit':'alllastBR/rootanytie/allspeperipheral/qdefinition','target':N,'location':'同一完整策略、静态iid值及每份SPE proof'},{'source_unit':'g3/directdelta/M≥6k² recurrence/all-evenk/65/432','target':N,'location':'45公式参数及真正全偶参数证明'},{'source_unit':'staticH vs realH vsqaverage/notaveragebridgecounter','target':N,'location':'静态iid值'},{'source_unit':'originalbeforeauthor/parentinputreadorder','target':N,'location':'原数学先验历史'}]},{'id':IDS[1],'disposition':'duplicate','targets':[N,V],'units':[{'source_unit':'sections1-2positiveintegerdesign/allBR/repeat/root/OPTallSPE','target':N,'location':'输入构造、全BR和每份SPE数学；父审补完整OPT差'},{'source_unit':'section3Nash/notsecurityopt/threequantities/v>lambda','target':N,'location':'静态iid值和原数学先验'},{'source_unit':'section4 independentM≥6k² polynomial proof andauthor77/72 derivative','target':N,'location':'全偶参数证明；V中作者下界'},{'source_unit':'section5k12/14alltable/countsincludingself/45finite vsallk','target':N,'location':'显式全部报告内容及45参数'},{'source_unit':'internalpassed/no fatal/blindthenauthor/comparisonnotexternalnovelty','target':N,'location':'原数学先验历史与原输出绑定'}]},{'id':IDS[2],'disposition':'integrated','targets':[P,N,V],'units':['all4090text/history/generalI-Gformula/71reportedcounter narrowerPnotrefutation','privateassignmenttwogaps/P+Cov/v1uncoverabler1/r2fixedbackground/allrcandidate','allfivehistoricalnegative/unrunreports matchedfullrealcode/moreprecisescope/0newCLI','30000claimvsdefault10000/noargvlog/finitecount≠solvercount/notalltiecones','laterhubblindchronology/internalunit12,14/all-evenproof/threepayoffsnotqaveragecounter','newstandaloneprobe resource with188? NO actual192/448 and195/451/511/728 exactdomains']}]
coverage[2]['units'][-1]='newstandaloneprobe resource with192/448 Ctypes,195/451variables and511/728nonselfIC source-derived counts'
js(E/'semantic-coverage-map.json',coverage)
notes=[('2916B全稿实际读：输入合法、两个完整历史BR类、任意平局根、静态g3/给定q、严格差式和M≥6k²全偶归纳、原先盲读身份及语义边界。','逐段比较已发布NM两原审计程序资源与ML父审完整数学。相同M/2−1族；对照5013B支持外M/3族后明确不同平均桥。独立归纳/所有SPE与原执行有限范围已有明确去向。','duplicate：所有数学/历史由NM+ML自足覆盖，原件仍按本独立sourceID保；没有新增blind/run/定理，0重复成功CLI。'),('5479B五节与完整两行有理表全部读：整数客户/重叠、所有BR和OPT、三个查询量、两种全参数证明、有限45与先盲后读内部状态。','NM资源完整保程序/解析/读序/单位2和45区别；ML保作者77/72路线和v>lambda等代数。逐项coverage定位，未以“review通过”或同名标签代替语义比对。','duplicate：目标NM+ML精确覆盖，无外审/新颖性/新全参数运行认证；原source/现targetSHA均绑，原冻结报告未倒填日志。'),('4090B入口从原日期、四项当前结论、五有限探针、继续条件至hub后续全读。另完整实读五源码14031B及3规范依赖24784B；原始运行日志未取得不冒实跑。','全仓精确检索及实际全文对照ML/NM/NC5。入口数学已有ML/NM，但五探针seed/预筛/LP变量/抽样策略/有理化/固定sidecar与原报告范围尚无完整资源，故补新自足对象；两不同hub不混。','integrated：新资源准确保一般I/G和平行P+Cov/r2/全r缺口，新增源码层scope限定标为本次阅读推断，历史30000/1/5-6不升为新PASS，spectrum历史未运行。本批0执行/import，相关5code和canonical3均不extra done。')]
assert sum(inv[i]['size'] for i in CAN)==24784
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' actual full多组claim/currentowner/sourceSHA核；不投影原回执。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
scope={'primary_sources':3,'primary_bytes':12485,'actual_full_primary_semantic_read':True,'read_reuse':'twoMD actualcomplete firstread as NMrelated thencurrent primary semanticfullcomparison; READMEfirstfullafterNMsealed; fiveprobes actualcomplete beforeclaim; no fabricated firstread','necessary_related_program_sources':5,'necessary_related_program_bytes':14031,'necessary_canonical_dependencies':3,'canonical_bytes':24784,'all_related_actual_fullread':True,'new_formals':1,'dispositions':{'integrated':1,'duplicate':2},'raw_claim_ids':len(claim['ids']),'raw_claim_status':claim['status'],'raw_sync_status_preserved':claim['local_sync']['status'],'raw_claim_projected':False,'own_original_CLI_calls':0,'own_original_module_import_calls':0,'own_new_math_or_solver_runs':0,'own_successful_same_SHA_reruns':0,'new_blind_or_external_review':0,'oldNMsourceSHA_success_reused_without_rerun':True,'historical_negative_probe_report_has_new_execution_provenance':False,'scope_limit':'sourcecode analysis/old author reports/new readscope only; notnewLPoptimality or allparameter/allSPE audit','independent_packager_calls':1,'phase3_mapper':0,'sharedGit_show_claim_done_checkpoint_network_auth_calls':0};js(E/'read-scope-and-execution-identity.json',scope)
put(W/'relation-review.md',r'''# 阶段二关系判断

新资源把平行P+Cov候选的局部r≤2证明与五有限程序的真实输入/策略锥域分开。ML父审已有完整定义/局部证明/模板障碍，故入口已有数学据其对照；五程序新范围不可仅据主题相近duplicate。基础D0与完整谱、固定两席一席谱、历史负面LP与全参数证明分别保。

两hub审查稿完整被NM+ML覆盖，各原ID逐段定位，原盲后读历史不成为本次盲审。另NC5是M/3真正q平均失败，NM是M/2−1仅maxstandaloneH失败、q平均成功；输入域/策略不同，不能相互扩张结论。五probe及3canonical仅必要相关依赖，本批不extra done或复跑。此处说明阶段二复用/范围关系，不做阶段三mapper或强制图边。
''')
put(E/'README.md',r'''# 平行共享遗漏入口与审查稿

三主源12485B全部实读，五探针14031B、三规范依赖24784B完整源读；两hub审查稿已被NM+ML全语义覆盖各记duplicate，README五探针历史与实际程序范围新资源integrated。本包0原CLI/0import/0数学或LP执行/0成功复跑。

默认10000不冒历史30000argv，随机并集W预筛非实际单outsideW，150/40/12是外seed而非成功LP，单份完整策略锥非所有tie，浮点LP命中有理化verifier仅查SPE未重断言目标越界。原负面报告没有本批执行绑定，未运行spectrum保无结果；所有源码和真正读取位置存档，不把源码存在当历史运行。

原多组claim原字节，本3subset/currentowner/sourceSHA核；Root正文先push后逐源done。相关五程序/三规范源/NC5及旧目标不额外done，冻结输入不改，0sharedGit/网络/账号/mapper。
''')
cp(Path(__file__),E/'build_delivery.py');cp(D/'preclaim-reading-scope.json',E/'actual-preclaim-reading-scope.json')
nextrows=[]
for i in PROBES:
 p=REPO/'cleanup/progress'/f'{i}.json';owner=json.loads(p.read_text()) if p.exists() else None;x=next(x for x in rows if x['id']==i);nextrows.append({**inv[i],'local_path':x['local_path'],'current_owner':owner,'actual_full_related_read':True,'new_runs':0,'candidate_only':True,'available_at_snapshot':owner is None})
js(W/'next-candidates.json',nextrows)
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex(t,c):return sum(1 for n in range(len(t)-1) if ord(t[n])==92 and t[n+1]==c and (n==0 or ord(t[n-1])!=92))
for x in sources+related:
 b=(S/x['preserved_path']).read_bytes();ck('sourceSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('unprojectedclaim',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and set(IDS)<=set(claim['ids']));ck('actualowners',all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('3receiptIDs',len(receipts)==3 and {x['id'] for x in receipts}==set(IDS));ck('2duplicate1integrated',sum(x['disposition']=='duplicate' for x in receipts)==2 and sum(x['disposition']=='integrated' for x in receipts)==1)
for x in comp:ck('currenttargetSHA '+x['path'],sha((REPO/x['path']).read_bytes())==x['sha256'] and sha((S/x['snapshot']).read_bytes())==x['sha256'])
t=(S/P).read_text();ck('flatmetadata',all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));ck('TeXbalanced',tex(t,'[')==tex(t,']') and tex(t,'(')==tex(t,')'));links=[]
for link in re.findall(r'\]\(([^)]+)\)',t):
 if ':' in link or link.startswith('#'):continue
 ok=((REPO/P).parent/link).resolve().exists() or ((S/P).parent/link).resolve().exists();links.append({'link':link,'exists':ok});ck('link '+link,ok)
js(E/'formal-link-check.json',links);ck('sourceonly0CLI',scope['own_original_CLI_calls']==scope['own_original_module_import_calls']==scope['own_new_math_or_solver_runs']==0);ck('readonlyrelatednotdone',{x['id'] for x in receipts}.isdisjoint(PROBES+CAN));ck('probevariableandICscope','192/195' in t and '448/451' in t and '73/511' in t and '91/728' in t);ck('historyvsdefaultscope','10000' in t and '30000' in t and '未运行' in t)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+x+'/' in '/'+rel for x in ['original','necessary-related-original','frozen-canonical-dependencies','comparison'])
 bad=[{'offset':i,'ord':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n'];trail=[i+1 for i,line in enumerate(t.splitlines()) if line.rstrip()!=line]
 if bad or trail:obs.append({'path':rel,'frozen':frozen,'C0':bad,'trailing_lines':trail})
 if not frozen:assert not bad and not trail,rel
js(E/'transport-format-observations.json',obs);js(W/'self-check.json',{'passed':all(x['passed'] for x in checks),'checks':checks,'check_count':len(checks),'whole_repo_completion_claimed':False,'original_CLI_or_new_math_runs':0,'formal_links':len(links),'C0_scope':'derived allC0exceptLF; frozenobservednotmodified; TeXdelimitersignoreescapedrowbreaks'})
put(W/'delivery.md','''# 共享遗漏三主源交付

3primary12485B全实读/逐源去向：2duplicate到NM+ML完整数学及原盲读序，1integrated补新五探针范围资源。5code14031B+3canonical24784B均必要相关完整读，不extra done。原full多组capture/subset/owner/SHA核，正文先push再done。

本批0原CLI/0import/0新math或LP/0成功后重复；原30000/1/5-6负面报告无新增执行绑定，默认10000/预筛/抽样单策略/有理化未复核目标局限精确保。另P=M/3与M/2−1两hub族不同，0新blind/外审/novelty/mapper。
''')
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and p.name not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'files':len(files),'bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_sources':3,'primary_bytes':12485,'formal_objects':1,'formal_bytes':(S/P).stat().st_size,'integrated':1,'duplicate':2,'checks':len(checks),'links':len(links),'originalCLI':0,'new_math_or_solver_runs':0};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False))
