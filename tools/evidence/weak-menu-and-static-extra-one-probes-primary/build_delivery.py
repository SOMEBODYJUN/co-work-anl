from pathlib import Path
import hashlib,json,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='weak-menu-and-static-extra-one-probes-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');D=C/'relay-weak-and-extra-one-menu-probe-drafts';BASE=['706cb0fdafd4c67fb857','76a108de3728a0cf95d4','117af000285f5a7ad0aa','2e8c4b8ee660abbc2275','def4c1b537d60068fd29'];EXTRA='765aff43fda8e38968fe';IDS=BASE+([EXTRA] if '--include-main-output' in sys.argv else []);ALL=BASE+[EXTRA];P='archives/customer-attraction/state/程序/任意尾菜单的弱平均与静态额外槽探针--程序.md';CY='archives/customer-attraction/state/程序/旋转对称末位菜单的浮点发现程序--程序.md';OB='archives/customer-attraction/state/障碍/八标签末位真回复菜单的第二人偏离--障碍.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 d=S/q;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(Path(p).read_bytes())
# Include EXTRA as primary only when Root explicitly assigns it, never just
# because some other workstream's full atomic receipt contains the id.
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids']);sync=claim['local_sync']['status'];proofpath=None
if sync=='needs-attention':
 proofpath=Path(sys.argv[2]);proof=json.loads(proofpath.read_text());assert proof['stash'] in claim['local_sync']['detail'] and proof['stash_kept'] and proof['missing']==proof['different']==[] and proof['unmerged']=='' and all(x['same'] for x in proof['tracked'])
else:assert sync=='synced'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};manpaths=[C/'relay-menu-probes-next-local-candidates/local-export-manifest.json',C/'relay-extra-one-actual-main-output-local/local-export-manifest.json'];rows=[x for p in manpaths for x in json.loads(p.read_text())['rows']];sources=[];related=[];owners=[]
for i in ALL:
 v=inv[i];x=next(x for x in rows if x['id']==i);b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/('original' if i in IDS else 'necessary-related-original')/i/v['path'];cp(x['local_path'],q);row={**v,'preserved_path':str(q),'read_scope':'actualallcode/allJSONfields fullsemanticpreclaimread reused honestly/no newrun'};(sources if i in IDS else related).append(row)
 if i in IDS:
  owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner)
js(E/'source-manifest.json',sources);js(E/'necessary-related-manifest.json',related);js(E/'actual-owner-snapshot.json',owners);cp(claimpath,E/'actual-unprojected-claim-receipt.json')
if proofpath:cp(proofpath,E/'actual-independent-sync-resolution.json')
for n,p in enumerate(manpaths):cp(p,E/'actual-local-manifests'/f'input-{n+1}.json')
contexts=[]
for p,stage in [(CY,C/'r3-cyclic-menu-discovery-and-two-point-audit-bindings-primary'),(OB,C/'r3-shared-omission-audit-and-terminal-menu-review-primary')]:
 b=(REPO/p).read_bytes();assert b==(stage/p).read_bytes();q=E/'comparison'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_scope':'actualcompletepriorbodywrite/read and currentpublishedexactSHA; referencesnotadditionalprimarydone'})
js(E/'comparison-manifest.json',contexts)
refs=[f"source:{x['commit']}:{x['path']}" for i in ALL for x in inv[i]['sources']];front=['---','id: customer-attraction/arbitrary-tail-menu-weak-average-and-extra-static-slot-probes','kind: program','type_tag: 程序','title: 任意尾菜单的弱平均与静态额外槽探针','status: historical-finite-floating-diagnostics-and-explicit-producer-binding-gaps; no-new-run','summary: 两个不同LP/弱平均59/48非SPE菜单、strict生产调用与500case摘要driver缺口、真实六主题一LP残差全部保真。','source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs]+['---','',(D/'program-body.md').read_text()];put(Path(P),'\n'.join(front));put(Path(P),(S/P).read_text()+'\n## 原件资源\n\n'+'\n'.join('- ['+x['id']+' '+str(x['size'])+' B 原件](../../../../'+x['preserved_path']+')' for x in sources+related)+'\n')
coverage={BASE[0]:['all92B3fields500/best1/status; unknownactualdriver/inputs/logs','notboundtooneLPmain/oldMD<=6onlyhistory/notuniversalproof'],BASE[1]:['allimports/function/main/base/p/inputvalidationboundaries','root<=1/tail>=t/allrslotstaticp>=t/noBR/noSPE/onefixed6themeLP','writesextra_one_menu_probe.jsononlysuccess/notabstract500/sameactual1182fullread'],BASE[2]:['all485fields15menus/floating59_48/tails/15weights/integer3and2/-0','manualdirectsharesJ59/48/last1to2 invalid/duplicatecovers/notfullSPE'],BASE[3]:['all1400code/candidate multisetmenus/objectiveJvsstatic/noBR/stricttailthreshold','besttol/earlystop/oneLPpertail/mainonlyFalse/fixedoverwrite/noCLI'],BASE[4]:['all540fields1296/float0.8333/tails/15weights/rawprecision/-0','strictTruecompatiblebutdefaultmainnotproducer/noexactdriverlog/finiteinrestrictedtemplate'],EXTRA:['all1182fields6tails/uniformp/t0.8889/63weightsincluding4tinynegative/allresiduals','oneLPmaincompatible/nointegerrecovery/noexecutionSHA/unknownwhole500driverdistinct']}
js(E/'semantic-coverage-map.json',[{'id':i,'disposition':'integrated','targets':[P],'units':coverage[i]} for i in IDS])
scope={'primary_sources':len(IDS),'primary_bytes':sum(inv[i]['size'] for i in IDS),'necessary_related_sources':len(related),'necessary_related_bytes':sum(x['size'] for x in related),'all6_source_semantics_read':True,'new_formals':1,'raw_claim_ids':len(claim['ids']),'actual_assigned_primary_subset':IDS,'claim_projected':False,'optional_main_output_primary_only_by_explicit_assignment':EXTRA in IDS,'raw_local_sync_status_preserved':sync,'independent_recovery_preserved':bool(proofpath),'original_import_CLI_LP_calls':0,'new_math_program_runs':0,'old_success_replays':0,'new_negative_scans':0,'manual_math':'direct59/48expansionofthegivenintegerwitness, notoriginal/newLPcertificate','producer_gaps':['abstract500driver andinputsnotprovided','strictTrueinvocationnotrecordedbydefaultmain'],'safe_local_export_calls_beforeclaim':5,'primary6_export_calls':2,'following_math5_export_calls':2,'following_parent_review_related_export_calls':1,'primary_and_related_exports':6,'following_math_exports':5,'following_parent_review_related_exports':3,'local_missing':0,'packaging_builder_calls':1,'packaging_failures':0,'own_shared_Git_show_claim_done_checkpoint_network_account_calls':0,'phase3_mapper':0};js(E/'read-scope-and-execution-identity.json',scope)
notes={BASE[0]:('92B全部三字段全文读，非只看文件名；500/best1/有限无见证原含义完整保。','所读1292B main仅1LP且输出extra_one_menu_probe.json，不是此结构producer；source原作者MD称最高六主题仅历史描述，未取得500输入driver/log，不伪绑定。','integrated到程序资源，原作者有限声明/真实缺口全部保，不以缺底层日志反造500新运行或普遍证明。'),BASE[1]:('1292B全部函数/main/NumPySciPy依赖/默认6尾/p/baseNone/输出时序实读，真实1182B同名main输出也全字段读。','资源逐式区分静态额外槽约束与另1400B弱平均目标；函数不验一般p/base，main仅1LP，不验证BR/全策略，原63weights tiny负残差不当unit证书。','integrated，0import/CLI/LP；浮点阴性不普遍化，原同版本字节不造sourceSHA运行日志。'),BASE[2]:('485B全部fields/四tails/15weights/-0/total15/obj全文读。','弱平均J数学由源码自足解释，整数mask3=3/mask12=2直接展开59/48及末位改2严格有利，标签覆盖重复，不误标静态值或SPE。','integrated，精确算式是原整数witness的文本展开非新LP/外审；原浮点发现/提前停范围保。'),BASE[3]:('1400B完整代码/目标/候选过滤/严格参数/容差/main副作用实读。','完整资源保默认4x3/False只生成weak文件；strict540虽兼容显式函数选项但无生产调用保存，程序从未要求末位BR/更早IC。','integrated，固定sidecar源码不执行，0新扫描，不将无严格正例当任意目录定理。'),BASE[4]:('540B完整JSON每字段/15项weights和精度/四tails/1296/0.83333实读。','strict=True函数参数与默认False main身份严格区分，1296是受限6^4域相容记录，不冒独立逐call/exactdual或已得生产日志。','integrated，全部原数据和绑定缺口准确去向，0重跑/四舍五入删除残差/全域状态升级。'),EXTRA:('1182B全六尾/p/t及63项weights含tiny负数/正残差真实全文读，新primary仅在Root明确加入后receipt。','它与1292B main固定输入/格式相容，但不是abstract500报告；资源保全63数组/主要mask及四负残差，不自动恢复整数非负输入。','integrated，0新原LP/数值IC/整数恢复，sourceSHA/版本/独立argv日志原无则不造。')}
receipts=[]
for i in IDS:
 a,b,c=notes[i];receipts.append({'id':i,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' full多组原claim原字节仅取本actualassignedsubset，当前owner/sourceSHA核。','comparison_note':b,'decision_note':c,'disposition':'integrated','targets':[P]})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 阶段二关系

两个LP仅共享根/尾排序松弛：weak平均完整列query，extraone对固定p的全部r静态背景给保证。它们都缺真实尾SPE；weak整数正值甚至末位不是BR。cyclic发现后来加末位BR仍缺第二IC，LF解析障碍准确隔离该承重条件；不能把这三层诊断合成完整SPE证据。

strict输出/500摘要与main生产身份的缺口公开保；原文件自己已全读，未知底层driver不虚补run或普遍结论。阶段二不创建mapper/强制图连接，不额外done相关代码或证书。
''')
put(E/'README.md',r'''# 弱平均、静态额外槽与生产绑定

实际分配primary全部完整读，必要main输出也全文读；1自足程序对象，所有原码/JSON独立保。两浮点LP目标与代码真实main分开，strict函数参数/500摘要driver不足不假绑定。

weak原整数witness直算59/48但末位偏离2>1且覆盖标签重复，非SPE/half反例。extraone真实单LP含tiny负重数；不能舍去残差说精确单位实例。原依赖版本/argv/sourceSHA/独立solver日志缺则保缺。

0原CLI/import/LP/旧成功复跑/新阴性扫描；完整原claim/currentowner后才receipt，extra1182只有Root明确分配才计primary，绝不因全多组receipt包含就自动抢源。Root先push正文证据再done，代理0sharedGit/网络账号/mapper。
''')
cp(D/'reading-scope.json',E/'actual-preclaim-reading-scope.json');cp(Path(__file__),E/'build_delivery.py')
nextpaths=[C/'relay-cyclic-full-spe-next-local-inputs/local-export-manifest.json',C/'relay-cyclic-full-spe-required-local-inputs/local-export-manifest.json'];nextrows=[]
for j,mp in enumerate(nextpaths):
 cp(mp,E/'next-math5-actual-local-manifests'/f'input-{j+1}.json')
 for x in json.loads(mp.read_text())['rows']:
  assert not(REPO/'cleanup/progress'/f"{x['id']}.json").exists();b=Path(x['local_path']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256'];nextrows.append({**inv[x['id']],'local_path':x['local_path'],'owner_observed':None,'read_status':'actualfull5semanticoriginalsread; otherfamilies inparentreview targetcomparisonpending; no preclaim/receipt'})
assert len(nextrows)==5 and sum(x['size'] for x in nextrows)==26767
js(W/'next-candidates.json',nextrows)
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in sources+related:
 b=(S/x['preserved_path']).read_bytes();ck('source SHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('source blob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('actualunprojectedclaim',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and set(IDS)<=set(claim['ids']));ck('ownerSHA',all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));objects={x['id']:json.loads((S/x['preserved_path']).read_text()) for x in sources+related if x['path'].endswith('.json')};ck('allabstract92fields',objects[BASE[0]]=={'cases':500,'best':1.0,'status':'finite diagnostic only; no violation found'});ck('weak15fields',objects[BASE[2]]['total']==15 and objects[BASE[2]]['best']==1.2291666666666667 and objects[BASE[2]]['witness']['weights'][2]==3.0 and objects[BASE[2]]['witness']['weights'][11]==2.0);ck('strict1296fields',objects[BASE[4]]['total']==1296 and len(objects[BASE[4]]['witness']['weights'])==15 and objects[BASE[4]]['best']==0.8333333333333331);ck('actualsingleoutput63weights',len(objects[EXTRA]['weights'])==63 and objects[EXTRA]['t']==0.8888888888889426 and all(objects[EXTRA]['weights'][mask-1]<0 for mask in [9,12,20,34]));ck('allreceiptsassignedonly',{x['id'] for x in receipts}==set(IDS) and len(receipts)==len(IDS));ck('zerooriginalruns',scope['original_import_CLI_LP_calls']==scope['new_math_program_runs']==scope['old_success_replays']==scope['new_negative_scans']==0)
t=(S/P).read_text();ck('flatformal',all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));ck('producerboundaries','没有500case扫描入口' in t and 'main只调用False' in t and '59/48' in t and 'mask9、12、20、34' in t);links=[]
for link in re.findall(r'\]\(([^)]+)\)',t):
 if ':' in link or link.startswith('#'):continue
 ok=((REPO/P).parent/link).resolve().exists() or ((S/P).parent/link).resolve().exists();links.append({'link':link,'exists':ok});ck('formal link '+link,ok)
js(E/'formal-link-check.json',links)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen='/original/' in '/'+rel or '/necessary-related-original/' in '/'+rel or '/comparison/' in '/'+rel;bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('derivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_unchanged':True})
put(W/'delivery.md',f'''# 小菜单两LP原码/输出交付

{len(IDS)}primary{sum(inv[i]['size'] for i in IDS)}B全部实读，另{len(related)}必要related{sum(x['size'] for x in related)}B完整保；1自足程序对象/全部assignedintegrated。原{len(claim['ids'])}claim {claim['remote_tip']} pushed、rawsync {sync}不改，本subset owner/SHA核。

两不同目标/strictmain差异/500driver缺口/真实63weights残差完整保。0原CLI/import/LP/新阴性扫描/旧成功复跑，不造SPE/单位/exactdual证书。Root先推再done，代理无sharedGit/网络/账号/mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_links':len(links),'new_formals':1,'not_new_math_execution':True})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':sum(inv[i]['size'] for i in IDS),'related_bytes':sum(x['size'] for x in related),'receipts':len(IDS),'dispositions':{'integrated':len(IDS)},'new_formals':1,'new_formal_bytes':(S/P).stat().st_size,'checks':len(checks),'formal_links':len(links),'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'raw_sync_status':sync,'new_math_runs':0,'original_CLI_calls':0,'old_success_replays':0,'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
