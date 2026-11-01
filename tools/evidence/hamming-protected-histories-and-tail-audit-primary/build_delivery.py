from pathlib import Path
import hashlib,json,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='hamming-protected-histories-and-tail-audit-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');D=C/'hamming-restored-code-and-output-drafts';IDS=['5aac5094836dd72710f5','f7e6aa5cd7487b8e8b16'];P='archives/customer-attraction/state/程序/标签汉明保护与真尾计数的有限审计--程序.md';M='archives/customer-attraction/state/障碍/标签汉明邻域与完整末尾的删行障碍--障碍.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 d=S/q;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(Path(p).read_bytes())
# Never run this builder before Root supplies this batch's actual claim.
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids']);syncstatus=claim['local_sync']['status'];resolutionpath=None
if syncstatus=='needs-attention':
 resolutionpath=Path(sys.argv[2]);resolution=json.loads(resolutionpath.read_text());assert resolution['stash'] in claim['local_sync']['detail'] and resolution['stash_kept'] and resolution['missing']==resolution['different']==[] and resolution['unmerged']=='' and all(x['same'] for x in resolution['tracked'])
else:assert syncstatus=='synced'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};mp=C/'learning-hamming-originals-normal/actual-source-manifest.json';m=json.loads(mp.read_text());sources=[];owners=[]
for i in IDS:
 x=next(x for x in m['rows'] if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];cap=json.loads(Path(x['actual_normal_show_capture']).read_text());assert cap['output']==x['local_path'] and cap['source']==v;owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/v['path'];cp(x['local_path'],q);cp(x['actual_normal_show_capture'],E/'actual-normal-show-captures'/Path(x['actual_normal_show_capture']).name);sources.append({**v,'preserved_path':str(q),'actual_local_path':x['local_path'],'read_scope':'actualentirecode/allJSONfields8cases/alltails/allnegativewitnesses read beforeactualclaim; exactsameSHA reused notfakefirstread'})
assert sum(x['size'] for x in sources)==13923
js(E/'source-manifest.json',sources);js(E/'actual-owner-snapshot.json',owners);cp(mp,E/'actual-normal-show-manifest.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json');
if resolutionpath:cp(resolutionpath,E/'actual-independent-sync-resolution.json')
cp(C/'kx-next-hamming-and-shared-audit-inputs/local-export-manifest.json',E/'actual-first-local-missing-history.json')
old=C/'r3-hamming-constant-shared-and-source-preserving-kernels';assert (REPO/M).read_bytes()==(old/M).read_bytes();cp(REPO/M,E/'comparison'/M);js(E/'comparison-manifest.json',[{'path':M,'snapshot':str(E/'comparison'/M),'bytes':(REPO/M).stat().st_size,'sha256':sha((REPO/M).read_bytes()),'read_scope':'KQactualfullmathematicalwrite/read reused/currentpublishedsameexactSHA; oldthenunreadcodehistorykept'}])
refs=[f"source:{x['commit']}:{x['path']}" for i in IDS for x in inv[i]['sources']];front=['---','id: customer-attraction/hamming-label-protected-history-and-fresh-tail-finite-audit','kind: program','type_tag: 程序','title: 标签汉明保护与真尾计数的有限审计','status: original-finite-checks-and-expected-negative-witnesses-reviewed; no-new-execution','summary: 八参数保护球与真正计数尾的精确/样本范围，负IC是预期认证而非全SPE通过，原localmissing及后来normalshow各保真实时序。','source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs]+['---','',(D/'program-body.md').read_text()];put(Path(P),'\n'.join(front))
put(Path(P),(S/P).read_text()+'\n## 原件及读取证据\n\n'+'\n'.join('- ['+x['id']+' '+str(x['size'])+' B 原件](../../../../'+x['preserved_path']+')' for x in sources)+'\n')
report=json.loads((S/sources[1]['preserved_path']).read_text());code=(S/sources[0]['preserved_path']).read_text();cases=report['cases']
coverage=[{'id':IDS[0],'disposition':'integrated','targets':[P],'units':['allstdlib/class/helpers/main/fixed8parameters/optionaloutputoverwriteguard','disjointintegerblockpay size/count notexplicitunitloop','protectedfullorderedHamming/notbehavior/everyactualnode/overlapnotdistinctsum','onlycountdependentsuffix countrepresentative proof/exhaustive<=25000 orsorted1000samplededup/seed/scopelabel','formulaW/OPTanalyticnotsearch/expectednegativegamma/d1null','min_gamma computednotreported/stdout2LFfile1LF/openxafter8calculations/noCLIrepeat']},{'id':IDS[1],'disposition':'integrated','targets':[P],'units':['allstatus/generalproofscope/all8parameterrecords/allAsizes/allactualterminals','allprotectedcounts/all_onpathfields/WOPT/ratio/gaps','all7tailrows totals71520021856427132468682510815753124550 andsamples987102010191018','all7negativewitnessesinclduplicatedm7/-4/-50/-735/d1null','co-versionnotexternallog/firstmissingandactualnewnormalshowfactnotmathematicalrun']}];js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':2,'primary_bytes':13923,'all_original_code_and_JSON_semantic_read':True,'raw_claim_ids':len(claim['ids']),'primary_subset':IDS,'claim_projected':False,'raw_sync_status_preserved':syncstatus,'independent_recovery_preserved':bool(resolutionpath),'new_formals':1,'original_CLI_calls':0,'original_imports':0,'new_math_runs':0,'old_success_replays':0,'new_LP_SPE_BI_random_audit_runs':0,'original_random_sample_scope':'read original deterministic samples; no generated newmathsamples','normal_read_captures_verified':2,'first_local_missing_history_preserved':True,'new_helper_export_retry_calls':0,'own_shared_Git_show_claim_done_checkpoint_network_account_calls':0,'packaging_builder_calls':1,'packaging_failures':0,'phase3_mapper':0};js(E/'read-scope-and-execution-identity.json',scope)
notes=[('6541B全部源码与入口/依赖/参数/输出/采样逻辑实际完整读，normalshow唯一capture及sourceSHA/blob/actual新owner核；0原import/CLI。','KQ障碍完整任意参数数学已有，本程序补互不交块Fraction实现、完整有序保护、count-dependent尾才可压缩、25000阈值/固定seed抽样去重、OPT解析非枚举、预期负gamma与min_gamma不输出。','integrated；原八case成功不代表全SPE，stdout双LF/文件单LF且open(x)后置精确保，恢复原件不重跑旧成功，不覆写KQ当时未读事实。'),('7382B原JSON所有八组/全部A_sizes/actual/保护数/每尾scope/总域/实查/所有negative witness和null完整读，字节与库存及normalshow绑定。','新程序对象两全统计表与负节点表完整自足，m7加空18564穷举变27132域987样本、大尾1020/1019/1018准确，保护/onpath/tail重叠不混加。全部数值在原asset完整保，不将比率>2说SPE反例。','integrated；原JSON无sourceSHA/argv/Python/exit/time独立执行日志，normalshow仅取源证据非数学run。首次localmissing和后授权取齐并存，未因此额外done原数学源。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原多组claim原样保，仅本2实际subset。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 阶段二关系

KQ障碍负责任意参数完整形式策略/标签汉明保护/真尾/球外负IC和渐近删行结论；新程序负责对应原实现与八份冻结有限范围。代码按disjoint integerblocks而不是显式unitloop；tail count不变量支持该域压缩，early有序球不能压缩。

有限passed包含核实预期负IC，非全SPE认证；比率超二不是half反例。当前取回原件补过去真实未读取范围，不反向覆写旧页/首次missing。0新数学/额外done原MD/阶段三图导入。
''')
put(E/'README.md',r'''# 真实恢复的Hamming两原件

2primary13923B代码和JSON现已完整实读，1自足程序对象。原第一次localmissing原字节保；父级正常show两capture真实取得，size/SHA256/blob核。读源capture不是数学执行日志，原JSON未给sourceSHA/argv/version也不发明。

全部八case/七尾条目/七负节点完整去向。protected有序球、实际路径和freshB尾计数有重叠不混加；大尾仅deterministic_sample_only，不由fixedseed变穷举。status通过包含预期negative，非全SPE通过。

0原CLI/import/数学重跑/扩阴性扫描/共享Git/网络账号。已有KQ数学精确复用，保当时未读代码历史。完整原claim+本2owner后才receipt，Root先推正文证据再done。
''')
cp(D/'reading-scope.json',E/'actual-preclaim-reading-scope.json');cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in sources:
 b=(S/x['preserved_path']).read_bytes();ck('source SHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('source blob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('unprojectedactualclaim',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and set(IDS)<=set(claim['ids']));ck('ownerSHA',all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('priorKQtargetsameSHA',(REPO/M).read_bytes()==(old/M).read_bytes());ck('all8casefields',len(cases)==8 and [(x['players'],x['suffix'],x['radius'],x['empty_theme_added']) for x in cases]==[(1,0,0,False),(3,0,0,False),(5,0,2,False),(6,2,1,False),(7,1,0,False),(7,1,0,True),(10,1,1,False),(10,2,0,False)])
ck('7tailrecordsexact',sum(len(x['tail_checks']) for x in cases)==7 and [(x['scope'],x['checked_representatives'],x['total_count_representatives']) for c in cases for x in c['tail_checks']]==[('exhaustive_count_representatives',715,715),('exhaustive_count_representatives',2002,2002),('exhaustive_count_representatives',18564,18564),('deterministic_sample_only',987,27132),('deterministic_sample_only',1020,4686825),('deterministic_sample_only',1019,1081575),('deterministic_sample_only',1018,3124550)]);ck('allbadwitnessfields',cases[0]['uncredible_node'] is None and [x['uncredible_node']['gamma'] for x in cases[1:]]==['-4','-4','-4','-50','-50','-735','-735']);ck('originalsourceguardandseed','if __name__ == "__main__"' in code and 'random.Random(104729 + 100 * m + 10 * k + r)' in code);ck('sourceexclusiveoutputafteraudit',code.index('"cases": [audit')<code.index('args.output.open("x", encoding="utf-8")')<code.index('print(text)'));ck('noexecutionidentityreport',not any(k in report for k in ['source_sha256','argv','python','elapsed','exit_code']));ck('min_gamma_notreported','min_gamma' in code and 'minimum_slack' not in report and all('minimum_slack' not in x for x in cases));ck('2fullreceipts',len(receipts)==2 and {x['id'] for x in receipts}==set(IDS) and all(x['disposition']=='integrated' for x in receipts));ck('zerooriginalruns',scope['original_CLI_calls']==scope['original_imports']==scope['new_math_runs']==scope['old_success_replays']==0)
t=(S/P).read_text();ck('flatformal',all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));ck('scopepreserved','实现并未逐客户展开' in t and '不是全p^q有序历史直接遍历' in t and '局部变量min_gamma' in t and '不是half反例' in t)
for link in re.findall(r'\]\(([^)]+)\)',t):
 if ':' not in link and not link.startswith('#'):ck('formal link '+link,((REPO/P).parent/link).resolve().exists() or ((S/P).parent/link).resolve().exists())
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen='/original/' in '/'+rel or '/comparison/' in '/'+rel;bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('derivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_unchanged':True})
put(W/'delivery.md',f'''# Hamming恢复代码/报告两源交付

2primary13923B全部真实完整读，2integrated/1程序对象；原KQ数学不重造。原localmissing与后来normalshow双capture真实边界保，全8case/7尾scope/7预期negative完整去向。

原{len(claim['ids'])}claim {claim['remote_tip']} pushed、local_sync原{syncstatus}不改（若needs-attention另保Root独立恢复证据），本2owner/SHA核。0原CLI/import/数学/旧成功复跑，无扩阴性扫描或sharedGit。Root先推证据正文再done。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'new_formals':1,'not_new_math_execution':True})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':13923,'receipts':2,'dispositions':{'integrated':2},'new_formals':1,'new_formal_bytes':(S/P).stat().st_size,'checks':len(checks),'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'raw_sync_status':syncstatus,'new_math_runs':0,'original_CLI_calls':0,'old_success_replays':0};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
