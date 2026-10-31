from pathlib import Path
import hashlib,json,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='shared-seats-five-probe-programs-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');IDS=['0da9b22c0235c8d60a32','7f135c486ea538542a18','8f0545ba3822ebcb4a36','c141dd3d493d865ea8ae','2132682e0de90747076e'];P='archives/customer-attraction/state/资源/平行共享遗漏的有限筛查与盲审入口--资源.md';NU=C/'r3-shared-seats-probe-scope-and-review-history-primary';PREP=C/'shared-seats-five-program-primary-preparation/actual-full-source-semantic-preparation.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 d=S/q;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(Path(p).read_bytes())
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids']);assert len(set(claim['ids']))==len(claim['ids']);inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};mp=C/'shared-seats-required-probe-sources-local-inputs/local-export-manifest.json';rows=json.loads(mp.read_text())['rows'];assert not json.loads(mp.read_text())['missing'];sources=[];owners=[]
for i in IDS:
 v=inv[i];x=next(x for x in rows if x['id']==i);b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/'original'/i/v['path'];cp(x['local_path'],q);sources.append({**v,'preserved_path':str(q),'read_scope':'actual full code read as NU necessaryrelated beforeclaim, then currentprimary complete semanticcomparison; no fabricatedfirstread/no CLI/import'});o=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==v['sha256'];owners.append(o)
assert sum(x['size'] for x in sources)==14031
b=(REPO/P).read_bytes();assert b==(NU/P).read_bytes();q=E/'comparison'/P;cp(REPO/P,q);target={'path':P,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'fullsemanticcomparison':'complete samepublishedNU resource already preserves all5source unique contracts incl exact code-specific differences, source level deductions/historicalreports notnewexecution'};js(E/'comparison-target.json',target);cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-owner-snapshot.json',owners);js(E/'source-manifest.json',sources);cp(mp,E/'actual-local-source-manifest.json');cp(PREP,E/'actual-preclaim-full-source-understanding.json');cp(NU/'tools/evidence/shared-seats-probe-scope-and-review-history-primary/necessary-related-manifest.json',E/'canonical-and-original-context-manifest-from-prior-NU.json')
prep=json.loads(PREP.read_text());coverage=[];receipt=[]
headings=['随机集合值BI','固定完整策略锥、命中后的有理化','固定完整策略锥、命中后的有理化','随机集合值BI、原未运行状态','固定完整策略锥、命中后的有理化']
notes=[('2743B全部顶层/argv/随机输入/全计数BI/命中canonical分支/覆盖文件及stdout实读，真实输入内置；L/load int64默认有界，m/g任意未验证。','默认10000与旧README30000无argv绑定；并集W预筛会跳过实际单outside低W，命中才Fraction终局存在性复核且不导完整策略。'),('2789B全部seed/192+3类型/完整策略抽取/73历史511非自身IC/HiGHS模型/有理化SPE复核/写入实读。','150为seed尝试非LP成功数，一份随机完整策略非全tie；W=1/零块/目标sumU，命中后无严格目标再次断言。'),('2815B全部三outside修改、448+3变量、40尝试、91历史728非自身IC、完整候选写入实读。','路径3outside各一次使名义C全覆盖，与随机脚本单outside不同；两groups锥同名sidecar覆盖，原负面无新日志。'),('2806B所有与groups相同BI以及完整top-m谱float/预筛/命中验证和独立输出文件实读。','未运行是原历史并且本次0运行；BI整数不使谱float变Fraction，命中只核SPE可达未精确复核严格谱。'),('2878B全部固定谱目标[-1.5,-1,0]、12尝试、448+3/728IC、有理化和精确ratio输出实读。','只算第一块两席/第二块一席，不是完整top3谱或全编号配置；约5/6是历史有限浮点报告，未新认证LP最优。')]
for i,h,(read,note) in zip(IDS,headings,notes):
 coverage.append({'id':i,'disposition':'duplicate','targets':[P],'actual_unique_units':prep['source_code_semantic_units'][i],'complete_target_sections':h,'no_new_proof_or_execution':True});receipt.append({'id':i,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':read+' 全文先作NUrelated，现在主源逐项完整语义核，非假装重新第一读；本批真实多组capture/subset/currentowner/sourceSHA核。','comparison_note':note+' 当前NU正式资源完整已有，target原字节与冻结交付同；规范model/exact/certificate24784B已真实全文读并绑SHA，所有生成输入/输出合同与有限量词均核。','decision_note':'duplicate到已发布NU资源；原程序作为本sourceID原字节另保，29语义单元定位，0原CLI/import/新math或LP/旧成功或旧负面重扫。原历史结果不是本次sourceSHA运行，无日志不补造，无新反例/定理。','disposition':'duplicate','targets':[P]})
js(E/'semantic-coverage-map.json',coverage);js(W/'semantic-receipts.json',receipt)
scope={'primary_sources':5,'primary_bytes':14031,'full_source_semantic_units':sum(len(x['actual_unique_units']) for x in coverage),'new_formals':0,'dispositions':{'duplicate':5},'raw_claim_ids':len(claim['ids']),'raw_claim_projected':False,'raw_sync_status_preserved':claim['local_sync']['status'],'actual_full_code_read':True,'original_CLI_calls':0,'original_module_import_calls':0,'new_math_or_solver_runs':0,'successful_same_SHA_reruns':0,'historical_negative_scans_repeated':0,'old_spectrum_notrun_preserved':True,'new_blind_or_external_review':0,'sourcelevel_reading_deductions':'upperboundWprecheck/defaultiterations/singlecertcones/postrationalgoal/matchingfilename facts from actualsource, notnewexecution','canonical_dependencies_already_NU_fullread_only_no_extra_done':True,'independent_packager_calls':1,'own_sharedGit_claim_done_checkpoint_show_network_auth_calls':0,'phase3_mapper':0};js(E/'read-scope-and-execution-identity.json',scope)
put(E/'README.md','''# 五个平行遗漏探针原程序

五主源14031B全部全文，输入生成/规范依赖/输出/数值与量词合同已由此前NU资源自足保。现在每源29独有语义单元与当前正式目标逐项比，全部duplicate，非按同题名或代码数量判定。原码每ID原字节保，原全多组claim/currentowner/sourceSHA精确核，不投影回执。

0CLI/0import/0新数学或LP/0重复旧负面扫描；未运行spectrum不冒结果，旧30000/1/约5-6无sourceSHA执行日志不补造。浮点锥是完整给定策略的有限搜索域，不能扩大一般P+Cov/全r量词；有理化只核SPE未重断言严格目标。规范依赖已NU完整实读/存档，未extra done。
''')
put(W/'relation-review.md','''# 阶段二关系

五程序以原同一P+Cov窄目录生成/固定完整策略锥检查相关目标：基础D0、完整谱、固定两席一席谱分别保。当前NU正式资源完整含全部独有软件/数学合同，故五逐源duplicate；不是重复授一般定理或重跑旧negative。此前NU只给这5context无额外done，现在实际认领后各给独立source receipt，原读序据实复用。

不做phase3mapper，不强制图连通。浮点发现、命中有理SPE验证、严格目标复验、全人数候选证明是不同义务；旧日志缺失如实保。
''')
cp(Path(__file__),E/'build_delivery.py');nextrows=[]
for mf in [C/'cyclic-parent-independent-audit-local-preparation/local-export-manifest.json',C/'tail-gap-cone-probe-local-preparation/local-export-manifest.json']:
 for x in json.loads(mf.read_text())['rows']:
  p=REPO/'cleanup/progress'/f"{x['id']}.json";owner=json.loads(p.read_text()) if p.exists() else None;nextrows.append({**x,'owner_snapshot':owner,'available_at_snapshot':owner is None,'actual_full_source_read_as_preparation':True,'claimed_or_receipt_assumed':False,'new_original_runs':0})
js(W/'next-candidates.json',nextrows)
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in sources:
 b=(S/x['preserved_path']).read_bytes();ck('sourceSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('blobSHA '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('rawclaim',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and set(IDS)<=set(claim['ids']));ck('ownerSHA',all(o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==inv[o['id']]['sha256'] for o in owners));ck('currentpublishedtarget',sha((REPO/P).read_bytes())==target['sha256'] and (S/q).read_bytes()==(REPO/P).read_bytes());ck('5duplicate',len(receipt)==5 and {x['id'] for x in receipt}==set(IDS) and all(x['disposition']=='duplicate' and x['targets']==[P] for x in receipt));ck('29actualunits',scope['full_source_semantic_units']==29);ck('0executions',scope['original_CLI_calls']==scope['new_math_or_solver_runs']==scope['original_module_import_calls']==0);ck('0newformal',not (S/'archives').exists());ck('spectrumunrun',scope['old_spectrum_notrun_preserved'])
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+n+'/' in '/'+rel for n in ['original','comparison']);bad=[{'offset':i,'ord':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n'];trail=[j+1 for j,l in enumerate(t.splitlines()) if l.rstrip()!=l]
 if bad or trail:obs.append({'path':rel,'frozen':frozen,'C0':bad,'trailing_lines':trail})
 if not frozen:assert not bad and not trail,rel
js(E/'transport-format-observations.json',obs);js(W/'self-check.json',{'passed':all(x['passed'] for x in checks),'check_count':len(checks),'checks':checks,'mathematical_runs':0,'new_formals':0,'whole_repo_done_claimed':False});put(W/'delivery.md','''# 五程序逐源去重交付

五主源14031B/29源码语义单元完整实读/逐项对当前已发布NU资源；5duplicate，0新正式对象。原全多组claim/subset/owner/SHA精确核，原码原字节独立保。

0CLI/import/math或LP/旧negative重扫，历史未运行spectrum仍无结果，不把原README报告补成sourceSHA运行。原规范依赖NU已全读仅复用，0extra done/mapper/共享Git。Root先push本依赖证据再done。
''')
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and p.name not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'files':len(files),'bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_sources':5,'primary_bytes':14031,'formal_objects':0,'duplicate':5,'checks':len(checks),'originalCLI':0,'new_math_or_solver_runs':0};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False))
