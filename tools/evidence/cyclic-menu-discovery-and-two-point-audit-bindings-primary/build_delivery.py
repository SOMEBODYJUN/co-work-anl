from pathlib import Path
import hashlib,json,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='cyclic-menu-discovery-and-two-point-audit-bindings-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');D=C/'author-audit-and-cyclic-discovery-drafts';IDS=['30b5ae056026b69161f3','ca6e67cdedf4bf541f54','255099afa67d45f39131','02cd2f54509e3b9c75b2'];P='archives/customer-attraction/state/程序/旋转对称末位菜单的浮点发现程序--程序.md';Q='archives/customer-attraction/state/程序/八标签静态匹配与末位全回复的独立有理审计--程序.md';O='archives/customer-attraction/state/障碍/八标签末位真回复菜单的第二人偏离--障碍.md';LQ=C/'r3-terminal-menu-independent-audit-and-author-scope-primary';LQE=Path('tools/evidence/terminal-menu-independent-audit-and-author-scope-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 d=S/q;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(Path(p).read_bytes())
# Primary receipts only after explicit actual claim, never infer from pre-read.
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids']);sync=claim['local_sync']['status'];proofpath=None
if sync=='needs-attention':
 proofpath=Path(sys.argv[2]);proof=json.loads(proofpath.read_text());assert proof['stash'] in claim['local_sync']['detail'] and proof['stash_kept'] and proof['missing']==proof['different']==[] and proof['unmerged']=='' and all(x['same'] for x in proof['tracked'])
else:assert sync=='synced'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};mp=C/'terminal-menu-after-independent-audit-local-candidates/local-export-manifest.json';m=json.loads(mp.read_text());sources=[];owners=[]
for i in IDS:
 v=inv[i];x=next(x for x in m['rows'] if x['id']==i);b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/v['path'];cp(x['local_path'],q);sources.append({**v,'preserved_path':str(q),'read_scope':'actualfullsourcecode/allJSONfieldsall16authorcolumns/all19+35orbitsandweights read beforeclaim; exactsameSHA reuse notfakefirstread'})
assert sum(x['size'] for x in sources)==19848
js(E/'source-manifest.json',sources);js(E/'actual-owner-snapshot.json',owners);cp(mp,E/'actual-local-input-manifest.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json')
if proofpath:cp(proofpath,E/'actual-independent-sync-resolution.json')
contexts=[]
for p in [Q,O]:
 b=(REPO/p).read_bytes();assert b==(LQ/p).read_bytes() if p==Q else b==(C/'r3-shared-omission-audit-and-terminal-menu-review-primary'/p).read_bytes();q=E/'comparison'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_scope':'actualpriorfullmathematicalorsoftwarewrite/read, currentpublishedexactSHA comparison'})
for i in IDS[:2]:
 q=LQE/'necessary-related-original'/i/inv[i]['path'];b=(S/sources[IDS.index(i)]['preserved_path']).read_bytes();assert (REPO/q).read_bytes()==(LQ/q).read_bytes()==b
js(E/'comparison-manifest.json',contexts)
refs=[f"source:{x['commit']}:{x['path']}" for i in IDS for x in inv[i]['sources']];front=['---','id: customer-attraction/cyclic-terminal-menu-floating-discovery-program','kind: program','type_tag: 程序','title: 旋转对称末位菜单的浮点发现程序','status: historical-finite-floating-discovery-with-later-analytic-identification; no-new-run','summary: k7三槽36尾阴性/k8第22尾正例早停，旋转实质量LP缺第二IC，232点后由Fraction/解析赋精确身份。','source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs]+['---','',(D/'cyclic-program-body.md').read_text()];put(Path(P),'\n'.join(front));put(Path(P),(S/P).read_text()+'\n## 原件资源\n\n'+'\n'.join('- ['+x['id']+' '+str(x['size'])+' B 原件](../../../../'+x['preserved_path']+')' for x in sources)+'\n')
coverage=[{'id':IDS[0],'disposition':'duplicate','targets':[Q],'units':['full12maskFractionfunctions/run2params/mainfixedoverwrite/noCLI','8menusalllastBR/120staticsblocks/8upper/unique02/second/OPT/puremenuonly','existingLQfullresourceandbyteexactoriginalasset accountforall; no newoldsuccess replay']},{'id':IDS[1],'disposition':'duplicate','targets':[Q],'units':['all2cases/masks/16menus/last_queryall8each/dvpayWOPT/status','28:9/2,11/2,7,v73/16,dev15/2,last8,W17OPT23;232:33,37,58,v37,dev60,last62,W128OPT182','existingresourcefullcoverage/rawexactasset notmerelysamecount/wholeSHA; noexecutionlogfabrication']},{'id':IDS[2],'disposition':'integrated','targets':[P],'units':['allNumPySciPycode/orbit generation/integerlabels realmassvariables','allLPconstraintsroot<=1/tail>=t/uniformstatic guarantee/lastBR>=0/missingsecond/fullSPE','candidate tail nonroot/sortedallbutlast/iteration/1e-8improve/1+1e-7early stop','outerplanned7r3,8r3,7r4 thirdskipped/mainfixedsidecar/BESTstdout/notCLI']},{'id':IDS[3],'disposition':'integrated','targets':[P],'units':['allk7k8meta/36vs22/best/tail/all19+35orbitlistandweights','7positiveorbitsmin3/19 each1/3approx/127types; 8min7/17 4/33,50/33approx/255types','minus0raw preserved/floatnoexactcert/t=37/33later232identification','58candidateexecutionobligations notnewruns orindependent percall logs/no full7r4/full8scan']}];js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':4,'primary_bytes':19848,'all4_actual_full_semantic_read':True,'dispositions':{'duplicate':2,'integrated':2},'new_formals':1,'author2_fullread_as_LQrelated_then_fresh_primary_receipts':True,'cyclic2_firstfullread_afterLQfreeze':True,'old_target_asset_current_equal_frozen_LQ':True,'raw_claim_ids':len(claim['ids']),'actual_primary_subset':IDS,'claim_projected':False,'raw_local_sync_status_preserved':sync,'independent_recovery_preserved':bool(proofpath),'original_imports':0,'original_CLI_LP_calls':0,'new_math_runs':0,'old_success_replays':0,'new_solver_random_SPE_BI_runs':0,'sourcefloat_rational_identification':'comparison to laterexact232audit/analyticfamily notnewexactLP/ICcheck','safe_local_helper_calls_next5_and_requiredoutput':2,'next5_exports':5,'necessary_next_output_exports':1,'local_missing':0,'next5_and_requiredoutput_fullread_only_no_primaryreceipt':True,'new_packaging_builder_calls':1,'packaging_failures':0,'own_shared_Git_claim_done_checkpoint_show_network_account_calls':0,'phase3_mapper':0};js(E/'read-scope-and-execution-identity.json',scope)
notes=[('3078B作者audit全部函数/常量/12mask构造/main写入完整实读，LQ必要related已有真实fullread现freshprimary交集/owner/SHA后receipt。','现LQ程序对象完整保两固定正参数、块Fraction、120背景/负载双证、全末位及OPT，接口固定sidecar覆盖与独审七样本/全扇形不同。现目标与完整既读LQ同SHA，原asset字节相同只是额外版本证据，不单凭hash判duplicate。','duplicate：源码/全部义务/有用原码已有精确去向，0重跑、不冒原argv日志/通用SPE认证。'),('6669B两case所有12mask权重/16列三收益与8末位query/全部标量status完整实读，现原artifact与LQ已发表asset全字节比较。','LQ程序对象自足28/232两点所有收益/静态/OPT及16列模式，完整数组在原asset可复核；frozen输出并无执行hash/版本/独立log不能发明。','duplicate到现程序对象；并不把它称独审512或全参数软件证据，0旧成功复跑，不额外勾原作者MD。'),('2218B源码从轨道/矩阵/候选过滤/LP约束/容差/提前停止/main副作用全读。','新程序资源逐式保normalized root/tail/static/lastBR义务及缺第二IC、实数轨道质量与单位模型差别、计划第三组未执行和固定overwrite；后续精确232族已有数学去向，不造重复定理。','integrated；0import/LP/新扫描，source依赖版本/执行log未保存不冒有。'),('7883B全两记录/19和35轨道每mask/两全weights向量/best/tail/count实际全文读，非只读summary。','新资源保7标签36有限模板与8标签第22早停、255原类型/不同轨道大小/-0.0；浮点4/33,50/33解释与后续Fraction/解析比较而非raw精确证书，所有原数组独立保。','integrated；不把58候选计数造新LP调用或当完整运行日志，不假称计划7r4已扫；该菜单非SPE/half反例。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原多组claim完整保，只取本4实际subset。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 来源与有限证据关系

作者Fraction两点audit代码/JSON在LQ已完整保，现正式primary精确duplicate，不重复造程序身份；独审另一实现的全扇形/边界域仍单独。cyclic2是前置浮点发现，实现根归一/后继高/末位BR/静态均匀保证的松弛，缺第二IC；后续232解析族与两点Fraction只是对候选精确化，非补成完整SPE。

7小目录有限阴性和8第22早停不覆盖所有菜单/整数模型，更不能否定当前half。所有源角色/先后/原输出完整去向保，不变成新blind或外审；阶段二不导入mapper超图或强制连通。
''')
put(E/'README.md',r'''# 作者两点audit与旋转浮点发现

4primary19848B全部完整语义读，2duplicate精确去现LQ程序+字节相同原asset，2integrated到1新程序对象。浮点LP缺早期IC，正例靠后续Fraction/解析精确识别但始终非SPE。

7r3查36尾，8r3第22尾正例提前停；计划7r4未进入。原19/35轨道全mask/全向量已读保，实数w不是整数单位输入，浮点rational识别不当新exactcert。0原import/LP/CLI/旧成功重跑，wholeSHA不是原运行日志。

原完整多组claim/currentowner/sourceSHA后才receipt，rawsync原值与需要的独立恢复proof另保；Root先实际push正文证据再done。本代理0sharedGit/网络账号/mapper。
''')
cp(D/'reading-scope.json',E/'actual-preclaim-reading-scope.json');cp(Path(__file__),E/'build_delivery.py')
nextmf=C/'relay-menu-probes-next-local-candidates/local-export-manifest.json';nm=json.loads(nextmf.read_text());nextrows=[]
for x in nm['rows']:
 assert not(REPO/'cleanup/progress'/f"{x['id']}.json").exists();b=Path(x['local_path']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256'];nextrows.append({**inv[x['id']],'local_path':x['local_path'],'owner_observed':None,'read_status':'actualfullsemanticpreparationread/no claimorreceipt/run'})
cp(nextmf,E/'next5-actual-local-input-manifest.json');cp(C/'relay-extra-one-actual-main-output-local/local-export-manifest.json',E/'next5-necessary-related-main-output-manifest.json');js(W/'next-candidates.json',nextrows)
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in sources:
 b=(S/x['preserved_path']).read_bytes();ck('source SHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('source blob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('unprojectedclaim',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and set(IDS)<=set(claim['ids']));ck('ownerSHA',all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('oldLQtargetexact',(REPO/Q).read_bytes()==(LQ/Q).read_bytes())
author=json.loads((S/sources[1]['preserved_path']).read_text());cyclic=json.loads((S/sources[3]['preserved_path']).read_text());ck('all16authormenus',len(author)==2 and all(len(x['menus'])==8 and all(len(z['last_query'])==8 for z in x['menus']) for x in author));ck('author2parameters',[(x['a'],x['b'],x['customers'],x['OPT3'],x['menu_W']) for x in author]==[(1,5,28,23,17),(4,50,232,182,128)]);ck('cyclictwoonly_36_22',[(x['k'],x['r'],x['menus']) for x in cyclic]==[(7,3,36),(8,3,22)]);ck('fullcyclicorbitsweights',[len(x['witness']['orbits']) for x in cyclic]==[19,35] and all(len(x['witness']['weights'])==len(x['witness']['orbits']) for x in cyclic) and [sum(map(len,x['witness']['orbits'])) for x in cyclic]==[127,255]);ck('cyclictailandfloats',[x['witness']['tail'] for x in cyclic]==[[1,3],[4,1]] and [x['best'] for x in cyclic]==[0.8333333333333333,1.121212121212121]);ck('4receipts2dup2int',len(receipts)==4 and [x['disposition'] for x in receipts]==['duplicate','duplicate','integrated','integrated']);ck('zerooriginalruns',scope['original_imports']==scope['original_CLI_LP_calls']==scope['new_math_runs']==scope['old_success_replays']==0)
t=(S/P).read_text();ck('flatformal',all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));links=[]
for link in re.findall(r'\]\(([^)]+)\)',t):
 if ':' in link or link.startswith('#'):continue
 ok=((REPO/P).parent/link).resolve().exists() or ((S/P).parent/link).resolve().exists();links.append({'link':link,'exists':ok});ck('formal link '+link,ok)
js(E/'formal-link-check.json',links)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen='/original/' in '/'+rel or '/comparison/' in '/'+rel;bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('derivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_unchanged':True})
put(W/'delivery.md',f'''# 作者audit/旋转发现四源交付

4primary19848B全实际语义读，2duplicate/2integrated、1新程序对象。原{len(claim['ids'])}claim {claim['remote_tip']} pushed，raw local_sync {sync}原字节不改，需要时独立恢复另保；本4owner/SHA、LQ实际发布目标/作者原asset相同核。

0原CLI/import/LP/数学/旧成功复跑；有限正例非SPE，7r4未跑/8早停范围保。下一5实际本地齐3809B已全文预读，另真实main输出1182B必要related，全无新claim/receipt；Root先push再done，无sharedGit/网络/账号/mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_links':len(links),'new_formals':1,'not_new_math_execution':True})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':19848,'receipts':4,'dispositions':{'duplicate':2,'integrated':2},'new_formals':1,'new_formal_bytes':(S/P).stat().st_size,'checks':len(checks),'formal_links':len(links),'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'raw_sync_status':sync,'new_math_runs':0,'original_CLI_calls':0,'old_success_replays':0,'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
