from pathlib import Path
import hashlib,json,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='cycle-and-negative-probe-program-contracts-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');D=C/'cycle-and-two-negative-program-contract-drafts';IDS=['126fabd080a72b013d4e','3d8f13d9e0a9c5f16ea4','3988bf9efd14eb0a0b85','b1714abde49b4caf1bf2'];CAN=['999293c4e866618a72f6','14e0922138e43b337600','52369ae591b07d52c7df'];P='archives/customer-attraction/state/程序/环菜单有理回归与两种负面发现器的原程序合同--程序.md';B='archives/customer-attraction/state/障碍/严格根尾排序不能支付静态额外槽阈值--障碍.md';TAX='archives/customer-attraction/state/资源/完整终局税候选的策略锥浮点反例搜索合同--资源.md';OZ=C/'r3-global-menu-thresholds-and-deficit-continuity-primary'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 d=S/q;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(Path(p).read_bytes())
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids']) and len(claim['ids'])==24 and claim['remote_tip']=='36bea7b95047e83d4ca011ddff3f1266ebff278a';inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};mps=[C/'global-threshold-and-tail-review-local-preparation/local-export-manifest.json',C/'global-load-and-abstract-probes-related/local-export-manifest.json'];rows=[x for p in mps for x in json.loads(p.read_text())['rows']];sources=[];canonical=[];owners=[]
for i in IDS+CAN:
 v=inv[i];src=REPO/'tools/evidence/collaboration-model-and-cag-audit-primary/related-inputs'/i/v['path'] if i in CAN else Path(next(x for x in rows if x['id']==i)['local_path']);b=src.read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/('original' if i in IDS else 'frozen-canonical-dependencies')/i/v['path'];cp(src,q);rec={**v,'preserved_path':str(q),'read_scope':'entirecode/allJSONfields earlieractualOZcontext then currentprimary semantic/softwarecomparison; canonical3 fullread forAPI not historicalenvironmentcertification'};(sources if i in IDS else canonical).append(rec)
 if i in IDS:
  o=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==v['sha256'];owners.append(o)
assert sum(x['size'] for x in sources)==24681 and sum(x['size'] for x in canonical)==24784;js(E/'source-manifest.json',sources);js(E/'canonical-dependency-manifest.json',canonical);js(E/'actual-owner-snapshot.json',owners);cp(claimpath,E/'actual-unprojected-claim-receipt.json')
for j,p in enumerate(mps):cp(p,E/'actual-local-manifests'/f'input-{j+1}.json')
loc=json.loads((C/'cycle-threshold-original-cli-actual-location.json').read_text());run=json.loads(Path(loc['manifest']).read_text());assert loc['all_passed'] and run['all_passed'] and run['original_CLI_calls']==run['confirmed_original_top_level_math_body_calls']==1 and run['main_function_invocations']==run['original_module_import_calls']==run['successful_same_SHA_reruns']==run['negative_load_CLI_calls']==run['negative_abstract_CLI_calls']==0 and run['source_sha256']==inv[IDS[0]]['sha256'] and run['output']['byte_equal_frozen'] and run['output']['stdout_exact_expected_projection'] and not run['output']['stdout_exact_full_output'];assert Path(loc['claim_path']).read_bytes()==claimpath.read_bytes();fixture=Path(loc['fixture']);runmap=[]
for p in sorted(fixture.rglob('*')):
 if p.is_file():q=E/'actual-cycle-original-fixture'/p.relative_to(fixture);cp(p,q);runmap.append({'actual_path':str(p),'archived_path':str(q),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
js(E/'actual-run-artifact-map.json',runmap);cp(C/'run_cycle_threshold_original_once.py',E/'actual-executed-once-wrapper.py');cp(C/'cycle-threshold-original-cli-actual-location.json',E/'actual-run-location.json');comp=[]
for p in [B,TAX]:
 b=(REPO/p).read_bytes()
 if p==B:assert b==(OZ/p).read_bytes()
 q=E/'comparison'/p;cp(REPO/p,q);comp.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'scope':'actual fullmathematicscompared; OZ earliercontext0run historykept, no oldformal overwritten; no extra source done'})
js(E/'comparison-manifest.json',comp)
t=(D/'program-body-preclaim.md').read_text();t='# 环菜单有理回归与两种负面发现器的原程序合同\n\n四主源24681B全部原码/全JSON实际全文读，OZ相关身份据实复用，actual24项原回执/owner/sourceSHA后主源整理。本批仅确定环原入口必要1次通过，两个52秒negative保持0。数学已由OZ对象自足，本页补三程序不同真实输入/输出/计数，非重复授定理。\n\n'+t[t.index('## 3238B环回归'):];t=t.replace('OZ主数学对象对相关源码当时未执行的时间身份保原；后续若新增某原入口的真实日志，需另记sourceSHA且成功后不重复。','OZ当时相关源码未执行是准确历史。本PM现在新增环原CLI1，不回写OZ的0运行时序；sourceSHA和实际日志另保，成功后不重复。');t+='\n## 本次环原入口的实际指纹\n\n'+run['python']['version_stdout'].strip()+'，sourceSHA '+run['source_sha256']+'；新空repo相对副本、干净环境，实耗'+str(round(run['elapsed_seconds'],6))+'秒，exit0/stderr0。新17177B完整文件与冻结全byte同；stdout1609B精确七字段投影，非17177B文件。原CLI1/顶层数学主体确认1/main函数0/原import0/成功重复0；Python身份查询另1。\n\n37基础菜单、12静态组、1061背景、165 odd菜单均按原范围核，未把odd作为全背景枚举或把重复h1当独立实例。两个negative原CLI/import/新LP均0，旧ddf DAG/cyclic8/shared源也0重复；无新真实SPE/half反例或盲审。\n';refs=[f"source:{s['commit']}:{s['path']}" for i in IDS+CAN for s in inv[i]['sources']];head=['---','id: customer-attraction/cycle-exact-regressions-and-two-negative-discovery-program-contracts','kind: program','type_tag: 程序','title: 环菜单有理回归与两种负面发现器的原程序合同','status: one-deterministic-original-CLI-passed; two-negative-probes-source-only-not-replayed','summary: 四源完整软件合同，确定环17177文件/1609摘要匹配；1460计划与52秒早停、1296非1300、两tested含义及float未认证分开。','source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs]+['---','',t];put(Path(P),'\n'.join(head));put(Path(P),(S/P).read_text()+'\n## 原件、依赖与实际日志\n\n'+'\n'.join('- ['+x['id']+' '+str(x['size'])+' B 原件](../../../../'+x['preserved_path']+')' for x in sources+canonical)+'\n- [唯一环原CLI完整日志](../../../../'+str(E/'actual-cycle-original-fixture/execution-records/run-manifest.json')+')\n')
prep=json.loads((D/'preclaim-full-source-understanding.json').read_text());coverage=[{'id':i,'targets':[P,B] if i in IDS[:2] else [P,TAX] if i==IDS[2] else [P,B],'units':prep['unique_semantic_units'][i]} for i in IDS];js(E/'semantic-coverage-map.json',coverage)
notes=[('3238B所有std函数和顶层base/static/odd循环、ROOT/固定sidecar/stdout投影全文实读，内置所有单位集合/参数全理解。','OZ已有全部无穷数学，原code仍需精确保37/12/1061/165及odd只标量lower/rotcap；新原CLI1 source6f66/full17177原byte同，1609stdout七字段不混。'),('17177B完整4字段、37菜单每profile/utility/firstprofitable、12静态query全数组、5odd行逐项真实读。','所有表值/半径/原notSPE模型范围与源代码/已发布OZ完整比较，base和odd重复h1不造202不同输入。当前实际file/stdout合同分别核，不发明旧运行身份。'),('1938B全部计划参数/seed/兴趣类型和重数输入/全SPE终局/负gap/证书/输出/tested/时间和目录假设全文实读，canonical3全源码24784B实读解释API。','1460是计划且可52秒早停，原README无日志不认证全部完成；tested不含当前hit；strategy是history字符串dict非canonical actions；负面无需重扫/环境不倒填。'),('2328B全部连续typeweight/feat/menus/queryp/LP行/δ阈值/计数/输出/52秒检查与顶层依赖全文实读。','k4r3实际6^4=1296非1300，其他菜单各一p不优化全p；tested含失败/当前LP，与前probe不同；只float payload无Fraction单位/完整SPE/静态精确核，不认证反例，不重扫。')]
receipts=[]
for x,(a,b) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原24rawclaim/subset/currentowner/sourceSHA核，原related全文诚实复用非伪首次读。','comparison_note':b,'decision_note':'integrated，新自足程序对象补全部独有软件合同，不重造OZ数学。原CLI仅确定环1/顶层数学主体1/main0/import0/成功重复0，两个52秒negative0；原件/历史/新日志分别保，canonical依赖不extra done，0mapper/外审/新blind。','disposition':'integrated','targets':x['targets']})
js(W/'semantic-receipts.json',receipts);scope={'primary_sources':4,'primary_bytes':24681,'actual_all_primary_fullread':True,'canonical_dependencies':3,'canonical_bytes':24784,'canonical_not_claimed_or_done_again':True,'new_formals':1,'integrated':4,'unique_semantic_units':sum(len(x['units']) for x in coverage),'raw_claim_ids':24,'raw_claim_projected':False,'raw_sync_status_preserved':'synced','original_cycle_CLI_calls':1,'confirmed_top_level_mathbody_calls':1,'main_function_calls':0,'original_import_calls':0,'successful_sameSHA_reruns':0,'negative_load_CLI_calls':0,'negative_abstract_CLI_calls':0,'old_DAG_cyclic8_shared_calls':0,'base_rootmenus':37,'static_parameter_groups':12,'static_backgrounds':1061,'odd_menus':165,'not_distinct_202_instances':True,'odd_not_full_background_enumeration':True,'new_general_theorems_or_genuineSPEs':0,'new_blind_external_review':0,'original_negative_historical_environment_verified':False,'packaging_builder_calls':1,'own_sharedGit_show_claim_done_checkpoint_network_auth_calls':0,'phase3_mapper':0};js(E/'read-scope-and-execution-identity.json',scope);cp(D/'preclaim-full-source-understanding.json',E/'actual-preclaim-full-source-understanding.json');cp(Path(__file__),E/'build_delivery.py')
put(E/'README.md','''# 四源三程序的精确合同

4primary24681B全实读，canonical3源码24784B只作API/冻结依赖语义解释，不extra done或绑定原旧环境。1新程序资源，补输入配方/输出schema/tested/停止位置/float边界，OZ已有无穷数学不重授。

确定环source6f66原CLI唯一1次/顶层数学主体1/main0/import0，0.130974秒exit0/stderr0。17177全文件与冻结byte同，1609stdout七字段摘要正确；37/12/1061/165与odd未枚举全背景/重复h1精确保，两个52秒negative0次/无新LP。

L探针1460只是计划且52秒可早停，tested不含命中例；抽象LP首块1296非1300，tested包含当前LP，float payload未经整数/SPE精确认证。原旧PASS/negative不被改写，新日志sourceSHA独立保。原24fullclaim/owner/sourceSHA后receipt，Root先push后done，无共享Git/账号/mapper。
''');put(W/'relation-review.md','''# 阶段二关系

OZ保形式环无界停界/负载L候选的数学身份，本对象补三个不同程序真实输入输出与执行。环为exact静态/非SPE菜单回归；L为合法整数全纯SPE终局的负面oracle；abstract为固定p/无SPE的浮点菜单LP。不能将共享目录或近似名称当作相同逻辑接口、全部查询/实例认证。

一个新确定环入口只核其有限实现，不新授无穷证明、真实SPE或half；两个negative0重扫，canonical API源已全读非历史环境认证。oldOZ context0运行保真实时序，当前PM新sourceSHA实际日志另记。不做phase3mapper/强连通，不extra done旧源/依赖。
''')
nextmp=C/'round4-direct-query-and-private-exit-local-preparation/local-export-manifest.json';nextrows=[]
for x in json.loads(nextmp.read_text())['rows']:
 p=REPO/'cleanup/progress'/f"{x['id']}.json";o=json.loads(p.read_text()) if p.exists() else None;nextrows.append({**x,'current_owner':o,'available_at_snapshot':o is None,'actual_bytes_verified':True,'semantic_read_at_delivery':False,'candidate_only_no_claim_receipt_or_run':True})
js(W/'next-candidates.json',nextrows);cp(nextmp,E/'next-local-byte-manifest-only.json');checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex(t,c):return sum(1 for n in range(len(t)-1) if ord(t[n])==92 and t[n+1]==c and (n==0 or ord(t[n-1])!=92))
for x in sources+canonical:
 b=(S/x['preserved_path']).read_bytes();ck('sourceSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('raw24unprojected',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and len(claim['ids'])==24 and set(IDS)<=set(claim['ids']));ck('ownerSHA',all(o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==inv[o['id']]['sha256'] for o in owners));ck('4integrated',len(receipts)==4 and {x['id'] for x in receipts}==set(IDS) and all(x['disposition']=='integrated' for x in receipts));ck('actual1PASS',run['all_passed'] and run['exit_code']==0 and run['stderr']['bytes']==0 and run['output']['byte_equal_frozen']);ck('projectioncontract',run['output']['bytes']==17177 and run['stdout']['bytes']==1609 and run['output']['stdout_exact_expected_projection'] and not run['output']['stdout_exact_full_output']);ck('onlydeterministicCLI',run['original_CLI_calls']==run['confirmed_original_top_level_math_body_calls']==1 and run['main_function_invocations']==run['original_module_import_calls']==run['successful_same_SHA_reruns']==run['negative_load_CLI_calls']==run['negative_abstract_CLI_calls']==0)
for x in runmap:ck('runtimearchive '+x['archived_path'],sha((S/x['archived_path']).read_bytes())==x['sha256'])
for x in comp:ck('currentcomparisonSHA '+x['path'],sha((REPO/x['path']).read_bytes())==x['sha256'] and sha((S/x['snapshot']).read_bytes())==x['sha256'])
f=run['original_full_report'];ck('reportall4fields',len(f)==4 and len(f['cases'])==4 and len(f['odd_r'])==5);ck('actualcountscope',[run['stdout_projection'][k] for k in ['base_menus','static_cases','backgrounds','odd_menus','k7_v4']]==[37,12,1061,165,'8/7']);t=(S/P).read_text();ck('flatmetadata',all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));ck('TeXbalance',tex(t,'[')==tex(t,']') and tex(t,'(')==tex(t,')'));ck('testedand1296scope','1296' in t and '1300' in t and 'tested' in t and '52秒' in t);links=[]
for link in re.findall(r'\]\(([^)]+)\)',t):
 if ':' in link or link.startswith('#'):continue
 ok=((REPO/P).parent/link).resolve().exists() or ((S/P).parent/link).resolve().exists();links.append({'link':link,'exists':ok});ck('link '+link,ok)
js(E/'formal-link-check.json',links);obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+n+'/' in '/'+rel for n in ['original','comparison','frozen-canonical-dependencies']);bad=[{'offset':i,'codepoint':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n'];trail=[i+1 for i,l in enumerate(t.splitlines()) if l.rstrip()!=l]
 if bad or trail:obs.append({'path':rel,'frozen':frozen,'C0':bad,'trailing_lines':trail})
 if not frozen:assert not bad and not trail,rel
js(E/'transport-format-observations.json',obs);js(W/'self-check.json',{'passed':all(x['passed'] for x in checks),'checks':checks,'check_count':len(checks),'links':len(links),'new_original_CLI':1,'negative_CLI':0,'whole_repo_completion_claimed':False,'allC0derivedexceptLFchecked':True});put(W/'delivery.md','''# PM四主源交付

4primary24681B全实读/23语义单元，4integrated/1新程序合同，canonical3源码24784B已全读只依赖不extra done。原24rawclaim/subset/currentowner/sourceSHA精确核。

确定环原CLI1/顶层数学主体1/main函数0/import0/重复0，17177文件全byte同，1609stdout只是摘要；37/12/1061/165按原有限域保。两个52秒negative0运行，L tested不含当前命中/abstract包含当前LP，1296非1300，float未精确认证。OZ数学/旧0运行时序不改，Root先push证据正文再done。
''');files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and p.name not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'files':len(files),'bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_sources':4,'primary_bytes':24681,'canonical_dependency_bytes':24784,'formal_objects':1,'formal_bytes':(S/P).stat().st_size,'integrated':4,'checks':len(checks),'links':len(links),'original_CLI':1,'top_level_mathbody':1,'main_function':0,'negative_CLI':0};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False))
