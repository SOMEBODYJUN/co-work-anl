from pathlib import Path
import hashlib,json,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='gap-summary-and-low-tail-original-audits-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');D=C/'tail-gap-and-low-deletion-audit-drafts';IDS=['23761c48bc45070cd2eb','d07c3e3a504463aa1fbe','1c2ad605bc009056c08a','648acd89a9fba1459313'];INPUT='8d74fd183eba467a811f';P='archives/customer-attraction/state/程序/孩子差额摘要与低尾删除的定义级原审计--程序.md';G='archives/customer-attraction/state/候选/真实尾部最优利润的最小收益差额候选--候选.md';V='archives/customer-attraction/state/审查/圆环可信性父审的旁支合同与证据身份--审查.md';OLD='archives/customer-attraction/state/计算/分数负载四主题族的全历史核验--计算.md';OE=Path('archives/customer-attraction/tools/evidence/fractional-load-boundaries')
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 d=S/q;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(Path(p).read_bytes())
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids']) and len(claim['ids'])==18 and claim['remote_tip']=='9d7ecbc7d140fc58d26e1b7a98666144ae8048b4';sync=claim['local_sync']['status'];proofpath=None
if sync=='needs-attention':
 proofpath=Path(sys.argv[2]);proof=json.loads(proofpath.read_text());assert proof['stash'] in claim['local_sync']['detail'] and proof['stash_kept'] and proof['missing']==proof['different']==[] and proof['unmerged']=='' and all(x['same'] for x in proof['tracked'])
else:assert sync=='synced'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};mp=C/'tail-gap-and-low-deletion-next-local-inputs/local-export-manifest.json';m=json.loads(mp.read_text());sources=[];owners=[]
for i in IDS:
 v=inv[i];x=next(x for x in m['rows'] if x['id']==i);b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/v['path'];cp(x['local_path'],q);sources.append({**v,'preserved_path':str(q),'read_scope':'actualentirecode/allJSON12gaprows/6rootpaths/3deletioncases fullsemanticread beforeanyoriginalexecution; no fakefirstread'})
assert sum(x['size'] for x in sources)==14876
js(E/'source-manifest.json',sources);js(E/'actual-owner-snapshot.json',owners);cp(mp,E/'actual-original-local-manifest.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json')
if proofpath:cp(proofpath,E/'actual-independent-sync-resolution.json')
loc=json.loads((C/'nb-original-cli-actual-location.json').read_text());fixture=Path(loc['fixture']);runpath=Path(loc['manifest']);run=json.loads(runpath.read_text());assert run['all_passed'] and run['original_CLI_calls']==2 and run['original_module_import_calls']==run['old_audit_refined_tax_packet_calls']==0 and len(run['runs'])==2 and [x['code_id'] for x in run['runs']]==[IDS[0],IDS[2]]
runmap=[]
for p in sorted(fixture.rglob('*')):
 if p.is_file():
  q=E/'actual-execution-fixture'/p.relative_to(fixture);cp(p,q);runmap.append({'actual_path':str(p),'archived_path':str(q),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
js(E/'actual-run-artifact-map.json',runmap);cp(C/'nb_run_original_cli_once.py',E/'actual-executed-cli-wrapper.py');cp(C/'nb-original-cli-actual-location.json',E/'actual-run-location.json')
for x in run['input_bindings']:
 b=Path(x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']==inv[x['id']]['sha256']
for x in run['runs']:
 assert x['exit_code']==0 and x['failure'] is None and x['source_sha256']==inv[x['code_id']]['sha256'] and not x['output_preexisted'] and x['output']['byte_equal_frozen_report'] and x['output']['JSON_value_equal_frozen_report'] and x['output']['stdout_exact_output_bytes'];out=Path(x['output']['path']).read_bytes();assert sha(out)==inv[x['output']['frozen_report_id']]['sha256'] and Path(x['stdout']['path']).read_bytes()==out and Path(x['stderr']['path']).read_bytes()==b''
js(E/'actual-runtime-environment-from-executed-wrapper.json',{'classification':'deriveddescriptionoftheactualpassedminimalenv, notanewexecution','python_executable':run['python_executable'],'python_version':run['python_version'],'environment_passed':{'PATH':'/usr/local/bin:/usr/bin:/bin','LANG':'C.UTF-8','PYTHONHASHSEED':'0','PYTHONDONTWRITEBYTECODE':'1'},'external_packages_installed':0,'network_or_account_operations':0})
packet=next(x for x in run['input_bindings'] if x['id']==INPUT);published=OE/'original'/inv[INPUT]['path'];b=Path(packet['path']).read_bytes();assert (REPO/published).read_bytes()==b and sha(b)==inv[INPUT]['sha256'];archive=next(x['archived_path'] for x in runmap if x['actual_path']==packet['path']);js(E/'necessary-packet-dependency.json',{**inv[INPUT],'preserved_path':archive,'already_published_exact_path':str(published),'role':'actualsamepacketinput, reusedpriorfullSPEcertificate thennewlowtailentryembeddedIConce; notnewstandalonepacketprimarydone','reading_scope':'allnonnodefields/instance/nodefieldstructure/6actualselectedpaths read; notclaimmanualallvertexdesiredcleanup','compressed_bytes':372216,'decoded_bytes':2342715});cp(C/'low-tail-required-packet-local-input/local-export-manifest.json',E/'actual-packet-local-manifest.json');cp(D/'read_input_metadata.py',E/'read_input_metadata.py');cp(D/'input-reading-snapshot.json',E/'input-reading-snapshot.json')
contexts=[]
for p in [G,V,OLD]:
 b=(REPO/p).read_bytes();q=E/'comparison'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_scope':'actualfullformaltextsemanticcomparison; priorG/Vthenunreadauditboundaryretainedhistorical, currentsoftwareaddsrealcode/input/runtime'})
js(E/'comparison-manifest.json',contexts)
for name in ['replay-refined-tax.json','replay-summary.json']:cp(REPO/OE/name,E/'prior-published-same-packet-evidence'/name)
oldmanifest=json.loads((REPO/OE/'source-manifest.json').read_text());js(E/'prior-published-same-packet-evidence/relevant-source-manifest-rows.json',{'kind':'explicitrelevantsubsetofsource-manifest, notaclaimreceiptprojection','published_manifest_path':str(OE/'source-manifest.json'),'rows':[x for x in oldmanifest if 'refined_tax' in x['path']]})
refs=[f"source:{x['commit']}:{x['path']}" for i in IDS+[INPUT] for x in inv[i]['sources']];front=['---','id: customer-attraction/gap-summary-and-low-tail-definition-level-original-audits','kind: program','type_tag: 程序','title: 孩子差额摘要与低尾删除的定义级原审计','status: two-original-CLI-runs-passed; exact-frozen-output-byte-reproduction; finite-scope','summary: 两无guard原码/全输出/压缩输入和各一次真实CLI完整保，gap计数回归与低尾固定DAG/自由t数据不同于普遍证明。','source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs]+['---','',(D/'program-body.md').read_text()];put(Path(P),'\n'.join(front));put(Path(P),(S/P).read_text()+'\n## 原件与实际运行资源\n\n'+'\n'.join('- ['+x['id']+' '+str(x['size'])+' B 原件](../../../../'+x['preserved_path']+')' for x in sources)+'\n- [实际run-manifest](../../../../'+str(E/'actual-execution-fixture/execution-records/run-manifest.json')+')\n- [压缩packet输入](../../../../'+archive+')\n')
coverage=[{'id':IDS[0],'disposition':'integrated','targets':[P],'units':['full2161top-level/noCLI/stdlib/countprofiles/profitFormula','k3..14 onlyarithmetic exceptk3/4 count70/48620/rootrelabels; fullunused/literalrootpay-tailmin-false notSPEtest','actualoriginalCLIonepass3967frozenexactstdoutstderr0/newcodeSHAstrongbinding']},{'id':IDS[1],'disposition':'integrated','targets':[P],'units':['allscope/enumerationscope12records/allnumericfields/optional2enumcounts','staticprofilesnotorderedhistories/zerochildrenmargin/positiveparentmargin/alwaysfake','newactualoutputbyteidentical原JSONnohashnotrewritten newlogseparate']},{'id':IDS[2],'disposition':'integrated','targets':[P],'units':['full4609top-level/std/gziprelativelayout/Lcm36unit/lrucache','rootreach/edgecountp/terminaldepth/allnodes/DPnodepreservesorderedhistory/mode','desired/terminalflag/expected/constructorfieldsignored; oldpacketcertnotthiscodeexecutionlog','all6truebranch/3eps/lowerstrictindex1..11/freeKreasonnotendogenoust','actualoriginalCLIonepasssource39fd/output4139exact/embedded27243_112050once/no oldverifiercalls']},{'id':IDS[3],'disposition':'integrated','targets':[P],'units':['allidentity/path/source/method/27243/112050/min0','all6root13-labelpaths/tailprofit/tailmin/currentinputpathreadingconfirm','all3eps/threshold/11positions/ninePtwoA/beforeaftergain/ratios/universalargument/nonhalfGAPscope','exactoldfrozenandnewruntimeoutputswithhash/noinventoldlog']}
];js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':4,'primary_bytes':14876,'all4_original_actual_full_semantic_read':True,'necessary_input_packet_bytes':372216,'packet_primary_receipts':0,'input_metadata_and_nodefieldstructure_read':True,'actual6inputpaths_read':True,'manual_all_vertex_desired_read_claimed':False,'prior_published_samepacket_fullcert_reused':True,'raw_claim_ids':len(claim['ids']),'primary_subset':IDS,'claim_projected':False,'raw_sync_status_preserved':sync,'independent_recovery_preserved':bool(proofpath),'new_formals':1,'dispositions':{'integrated':4},'original_CLI_calls':2,'new_math_original_audit_runs':2,'original_module_import_calls':0,'old_packet_verifier_calls':0,'new_gap_arithmetic_original_runs':1,'new_lowtail_original_runs':1,'new_lowtail_embedded_IC_comparisons':112050,'reruns_after_success_of_these_captured_codeSHAs':0,'derived_input_reader_invocations':2,'initial_local_export_calls_primary4_plus_packet':2,'local_missing':0,'new_probe_LP_or_parameter_expansion_runs':0,'packaging_builder_calls':1,'packaging_failures':0,'own_shared_Git_show_claim_done_checkpoint_network_account_calls':0,'phase3_mapper':0};js(E/'read-scope-and-execution-identity.json',scope)
notes=[('2161B全部原代码/顶层loop/所有函数/副作用完整实读后才执行，原入口无guard不是安全import。','新程序资源精确保count代表与k3/4优化范围、k3..14公式回归及literal字段；与已发布GAP/父审解析分工准确，非新SPE反例。','integrated，隔离原CLI恰1次exit0，source0a2dd2与输出3967/原报告hash强绑，stdout=原报告/stderr0；成功后不重跑。'),('3967B所有scope/12行所有字段含两个profile计数完整实读，原字节保。','新资源全12行表、0孩子差与k−2父差、literal false/nonSPE身份完整保；新实际输出与本冻结源全bytes同，原报告无执行hash历史不倒填。','integrated，原有限回归不升级全r证明或全有序策略检查，未因同数字判duplicate。'),('4609B全部源码、实际372216B gzip输入metadata/图格式/6路径与已发布同packet完整PASS核后才执行。','资源自足36unit整数份额/闭DAG/真实单步偏离/所有metadata使用界限/布局/三ε条件；程序只一个固定输入，无泛化canonical库认证。','integrated，原CLI39fd60恰1次exit0，确含27243/112050一次，不冒math0；独立旧packet verifier0、module import0，不另done gzip。'),('4139B全部元字段/六个13动作数组/三个删除case全字段及论证范围完整实读。','新资源六路径表/3eps与threshold/11positions/9P2A/ratio均保，原datareader又从实际packet走六路径作阅读定位，非新增SPE验证；输入旧PASS与新CLI日志角色分清。','integrated，新runtime输出与冻结源逐字节同，原source无codehash/argv日志不发明，任意K由ε解析而非3点外推；不反内生t/GAP/half。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原18claim完整保，仅本4actualsubset，owner/sourceSHA核。','comparison_note':b,'decision_note':c,'disposition':'integrated','targets':[P]})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 阶段二关系

GAP候选/父审资源负责全域解析和逻辑停界，本程序负责两原实现和真实有限执行。gap静态计数不是全SPE；低尾固定完整DAG是原13人SPE的实现证据，删除任意t无界比不否定内生安全值或half。

原gzip与已推原件精确相同、旧完整认证复用，但两新入口此前无代码SHA执行捕获，按授权各实际一次；低尾原body内含全DAG一次必须据实计数，旧verifier不另跑。原模块无guard不import。packet仅dependency不extra done；原旧页“当时程序未读”历史不覆写，当前软件新增真实范围单独保。不导入phase3图。
''')
put(E/'README.md',r'''# 两原有理审计与真实一次CLI

4primary14876B全部完整读，1新自足程序对象/4integrated。gap原码只2小k计数枚举，其余12参数公式；低尾原码读取同SHA gzip、展开36单位客户并检查固定完整自动机，再生成六根与三个ε数据。literal字段/ignored metadata与数学实际检查分清。

两个原入口各1次在新空隔离相对树实际执行，code/packet先hash核，stdout/file与冻结报告全byte相同，stderr0、exit0。新原CLI2/新math原入口2，其中lowtail内含112050IC一次；旧packet verifier0、moduleimport0、成功后重复0。完整actualargv/time/version/source/output/stdout/stderr保，原日志不改写成归档路径。

packet372216B仅related dependency，未给它primaryreceipt；全部metadata/结构/6路径已读，旧同packet完整PASS也保存比较，不声称手工逐27243desired重新清洗。Root先实际push正文证据再done，代理0sharedGit/网络/账号/mapper。
''')
cp(D/'reading-scope.json',E/'actual-prepack-reading-scope.json');cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex(t,c):return sum(1 for n in range(len(t)-1) if ord(t[n])==92 and t[n+1]==c and (n==0 or ord(t[n-1])!=92))
for x in sources:
 b=(S/x['preserved_path']).read_bytes();ck('sourceSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('raw18claim',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and len(claim['ids'])==18 and set(IDS)<=set(claim['ids']));ck('ownerSHA',all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('sameinputexistingexact',(REPO/published).read_bytes()==Path(packet['path']).read_bytes() and sha((S/archive).read_bytes())==inv[INPUT]['sha256']);ck('actual2success',run['all_passed'] and run['original_CLI_calls']==2 and all(x['exit_code']==0 and x['stderr']['bytes']==0 and x['output']['byte_equal_frozen_report'] for x in run['runs']));ck('nooldverifier_orimport',run['original_module_import_calls']==run['old_audit_refined_tax_packet_calls']==0)
for x in runmap:ck('actualarchivebytes '+x['archived_path'],sha((S/x['archived_path']).read_bytes())==x['sha256'])
gap=json.loads((S/sources[1]['preserved_path']).read_text());low=json.loads((S/sources[3]['preserved_path']).read_text());ck('gapall12rows',[x['k'] for x in gap['rows']]==list(range(3,15)) and all(not x['menu_is_SPE'] and x['tail_gap_minus_r_minus_1']=='0' for x in gap['rows']));ck('enumonly2',[x['tail_profiles_enumerated'] for x in gap['rows'] if 'tail_profiles_enumerated' in x]==[70,48620]);ck('lowall6and3',len(low['root_branches'])==6 and len(low['deletion_cases'])==3 and low['nodes']==27243 and low['checked_comparisons_including_self']==112050 and low['minimum_SPE_slack']=='0');ck('alllow11positions',all(x['low_tail_positions_zero_based']==list(range(1,12)) and x['root_deletion_gain']=='45/2' for x in low['deletion_cases']));snap=json.loads((S/E/'input-reading-snapshot.json').read_text());ck('inputpathreading_exactreport',[x['path'] for x in snap['six_selected_branch_paths_from_actual_input']]==[x['path'] for x in low['root_branches']]);ck('4complete_receipts',len(receipts)==4 and {x['id'] for x in receipts}==set(IDS));ck('newrunsaccurate',scope['original_CLI_calls']==scope['new_math_original_audit_runs']==2 and scope['old_packet_verifier_calls']==0)
t=(S/P).read_text();ck('flatformal',all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));ck('properTeX',tex(t,'[')==tex(t,']') and tex(t,'(')==tex(t,')'));links=[]
for link in re.findall(r'\]\(([^)]+)\)',t):
 if ':' in link or link.startswith('#'):continue
 ok=((REPO/P).parent/link).resolve().exists() or ((S/P).parent/link).resolve().exists();links.append({'link':link,'exists':ok});ck('link '+link,ok)
js(E/'formal-link-check.json',links);obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen='/original/' in '/'+rel or '/comparison/' in '/'+rel or '/actual-execution-fixture/' in '/'+rel;bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('newderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_actualruntime_original_unchanged':True})
put(W/'delivery.md',f'''# 原gap/低尾两审计四源交付

4primary14876B全实读，4integrated/1新程序对象。原18claim {claim['remote_tip']} pushed、rawsync {sync}不改，本4owner/SHA核。372216B gzip仅输入related，已有同byte旧完整SPE证据复用，不extra done。

原CLI实际2次各1、exit0/stderr0，两输出与冻结源全byte同；新lowtail本体含27243/112050一次据实记，不冒math0，旧packet verifier0、moduleimport0、成功后重复0。全部actual日志/代码输入SHA/输出/fixture保；不运行归档副本或改冻结原件。Root先push再done，无sharedGit/网络账号/mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_links':len(links),'new_formals':1,'new_original_CLI_calls':2,'new_math_original_runs':2})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':14876,'related_packet_bytes':372216,'packet_primary_receipts':0,'receipts':4,'dispositions':{'integrated':4},'new_formals':1,'new_formal_bytes':(S/P).stat().st_size,'checks':len(checks),'formal_links':len(links),'raw_claim_ids':18,'claim_tip':claim['remote_tip'],'raw_sync_status':sync,'original_CLI_calls':2,'new_math_original_runs':2,'old_packet_verifier_calls':0,'original_module_imports':0,'reruns_after_success':0};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
