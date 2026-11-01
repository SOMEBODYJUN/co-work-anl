from pathlib import Path
import hashlib,json,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='max-standalone-hub-two-original-audits-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');D=C/'hub-two-implementations-audit-drafts';IDS=['81f38224b31a6f5ea6f1','185971a2bf2d4583b6db','ccd5246fbbd5e1b77f16','05d1df3217d3cdd6647b'];RELATED=['e730733ff3146f1a9bd9','34ead0e38af5c08cf938'];P='archives/customer-attraction/state/程序/唯一最大主题选根边界的两份有理审计--程序.md';V='archives/customer-attraction/state/审查/圆环可信性父审的旁支合同与证据身份--审查.md';ML=C/'r3-cyclic-complete-credibility-and-parent-review-primary'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 d=S/q;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(Path(p).read_bytes())
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids']) and len(claim['ids'])==8 and claim['remote_tip']=='a9b4a4e86ef6d8083be4588073e6f8546b862316';inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};mps=[C/'hub-author-and-independent-audits-next-local-inputs/local-export-manifest.json',C/'hub-audits-required-review-context-local-inputs/local-export-manifest.json'];rows=[x for p in mps for x in json.loads(p.read_text())['rows']];sources=[];related=[];owners=[]
for i in IDS+RELATED:
 x=next(x for x in rows if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/('original' if i in IDS else 'necessary-related-original')/i/v['path'];cp(x['local_path'],q);rec={**v,'preserved_path':str(q),'read_scope':'actualentirecode/full45formulaJSONand2explicitarrays/allindependentJSON/related2MD fullsemanticread beforeexecution; historicalblindnotnew'};(sources if i in IDS else related).append(rec)
 if i in IDS:
  owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner)
assert sum(x['size'] for x in sources)==29126 and sum(x['size'] for x in related)==8395
js(E/'source-manifest.json',sources);js(E/'necessary-related-manifest.json',related);js(E/'actual-owner-snapshot.json',owners);cp(claimpath,E/'actual-unprojected-claim-receipt.json')
for j,p in enumerate(mps):cp(p,E/'actual-local-manifests'/f'input-{j+1}.json')
loc=json.loads((C/'nm-original-cli-actual-location.json').read_text());fixture=Path(loc['fixture']);run=json.loads(Path(loc['manifest']).read_text());assert run['all_passed'] and run['original_CLI_calls']==2 and run['original_module_import_calls']==run['reruns_after_success']==0 and run['distinct_unit_inputs']==2 and run['new_unit_input_runs']==4 and [x['code_id'] for x in run['runs']]==[IDS[0],IDS[2]];runmap=[]
for p in sorted(fixture.rglob('*')):
 if p.is_file():
  q=E/'actual-execution-fixture'/p.relative_to(fixture);cp(p,q);runmap.append({'actual_path':str(p),'archived_path':str(q),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
js(E/'actual-run-artifact-map.json',runmap);cp(C/'nm_run_hub_original_cli_once.py',E/'actual-executed-cli-wrapper.py');cp(C/'nm-original-cli-actual-location.json',E/'actual-run-location.json')
for x in run['input_bindings']:
 b=Path(x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']==inv[x['id']]['sha256']
for x in run['runs']:
 assert x['exit_code']==0 and x['failure'] is None and x['source_sha256']==inv[x['code_id']]['sha256'] and not x['output_preexisted'] and x['output']['byte_equal_frozen_report'] and x['output']['stdout_JSON_matches_expected_projection'];assert sha(Path(x['output']['path']).read_bytes())==inv[x['output']['frozen_report_id']]['sha256'] and Path(x['stderr']['path']).read_bytes()==b''
assert run['runs'][0]['stdout']['bytes']==2686 and not run['runs'][0]['output']['stdout_exact_full_output_bytes'] and run['runs'][1]['stdout']['bytes']==1118 and run['runs'][1]['output']['stdout_exact_full_output_bytes']
b=(REPO/V).read_bytes();assert b==(ML/V).read_bytes();cp(REPO/V,E/'comparison'/V);js(E/'comparison-manifest.json',[{'path':V,'snapshot':str(E/'comparison'/V),'bytes':len(b),'sha256':sha(b),'read_scope':'fullpriorMLmathematicalreviewauthored/read/currentexactpublishedversion compared; oldwhen-code-unread historykept'}])
refs=[f"source:{x['commit']}:{x['path']}" for i in IDS+RELATED for x in inv[i]['sources']];front=['---','id: customer-attraction/max-standalone-hub-two-definition-level-original-audits','kind: program','type_tag: 程序','title: 唯一最大主题选根边界的两份有理审计','status: two-original-CLI-runs-passed; fixed-unit-input-and-finite-scalar-scope','summary: 作者闭式iid单位审计与独审有序对单位枚举分开，45标量/全偶参数证明/原先盲后读及stdout合同精确保，真根外围不反half。','source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs]+['---','',(D/'program-body.md').read_text()];put(Path(P),'\n'.join(front));put(Path(P),(S/P).read_text()+'\n## 原件与实际运行资源\n\n'+'\n'.join('- ['+x['id']+' '+str(x['size'])+' B 原件](../../../../'+x['preserved_path']+')' for x in sources+related)+'\n- [实际run-manifest](../../../../'+str(E/'actual-execution-fixture/execution-records/run-manifest.json')+')\n')
coverage=[{'id':IDS[0],'disposition':'integrated','targets':[P],'units':['all4603code/guard/mainfixedoverwrite/stdonly/noexternalinputfiles','unit12/14 clientlikes->topics/allBRsets/specifiedfullpolicy/OPTallpairs','iidclosedgperunit vsindependentorderedpairs/allpurequeriesKKTnotsecurityopt','45formulaallfields/extra2formula callsnot47games/stdoutprojectionnotfile','actualCLI1source57003e/output19704exact/stdout2686projection/stderr0']},{'id':IDS[1],'disposition':'integrated','targets':[P],'units':['full19704 all45parameterrecords and2completeexplicitarrays/k12k14allfields','standalone/rootpay/static_alpha/actual1,2/14,16nodes/182,240inclusive','45finiteformula notallkevidence/general_evidence historicaltargetOPEN/statusauthornotindependent','currentactualsamefrozenbytes externalnewSHAlognotrewriteoriginal']},{'id':IDS[2],'disposition':'integrated','targets':[P],'units':['all3701top-level/no guard/units sets/intersections/BR/fullselector/OPT','allorderedperipheraliidpairs6integerdenominator/unitloop vsauthorg/noauthorimports','qavgactualrootv notalphaH/dH/lambda;45scalarM>=6k²onlyfinite','actualCLI1sourcea7e322/output1118exact/stdoutfull/stderr0/newunit2notgeneralproof']},{'id':IDS[3],'disposition':'integrated','targets':[P],'units':['full1118alltwoexpandedrecords/status/source/finite45description','k12/14M/private/intersection/N/p/histories/IC/Hreal/periphreal/Hstatic/lambda/gap/qavg/WOPT','countformulalogicalICincludingown notassertcounter/actualsinglepolicy notallselectorenumeration','newexactfrozenbyte output+runtime sourceSHA originaloldreportnotnewblind']}
];js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':4,'primary_bytes':29126,'necessary_related_MD_sources':2,'necessary_related_MD_bytes':8395,'related_primary_receipts':0,'all4_plus2actual_fullsemanticread':True,'raw_claim_ids':8,'actual_primary_subset':IDS,'claim_projected':False,'raw_sync_status_preserved':'synced','new_formals':1,'dispositions':{'integrated':4},'original_CLI_calls':2,'new_original_math_audit_runs':2,'original_module_import_calls':0,'reruns_after_success_of_captured_sourceSHAs':0,'distinct_unit_inputs':2,'unit_instance_audit_invocations':4,'finite_scalar_parameter_count_per_implementation':45,'new_general_theorems':0,'new_blind_review_or_external_review_claims':0,'mathematical_scope':'fixed2playerunitfamily/higher3staticiid givenq; notgenericNashfindingalgorithm/securityopt/canonicalCAGimplementation','safe_local_export_calls_primary_and_related':2,'safe_nextREADME_export_calls':1,'local_missing':0,'packaging_builder_calls':2,'packaging_failures':0,'preseal_math_layout_normalization':'stray single slash at polynomial line end replaced by aligned display; same exact polynomial/no frozen source edits','own_shared_Git_show_claim_done_checkpoint_network_account_calls':0,'phase3_mapper':0};js(E/'read-scope-and-execution-identity.json',scope)
notes=[('4603B原码所有函数/guard/main/内置构造和写入stdout合同全文读，actualclaim/owner/SHA后才实际CLI，source文件不改。','现ML父审已有数学家族，本新程序补显式单位建模、全两人IC/OPT、closedg与独审orderedpairs差别、45公式范围及source变量m其实core M，非提供者数。','integrated，原CLI恰1次exit0，19704输出与冻结全byte同；2686stdout投影按原合同核，不当全JSON，成功后不重复，不新授一般Nash/half。'),('19704B全部45公式记录、两显式对象的所有sizes/rootpay/staticAlpha数组及metadata完整实读。','新资源以闭式+两个显式全表保所有行意义，原完整数组/大有理数原件保；45标量有限不是所有k/不同47份SPE，原targetOPEN/statusauthor不倒改。','integrated，newruntime输出与本冻结源逐byte同、原输出原无hash不倒填日志，原数学全k证据归MD解析而非有限表。'),('3701B独审原码从单位ID构造、全部交集/BR与完整策略、直接iid对枚举/45回归至无guard顶层输出全文读。','新资源逐式保作者/独审真正不同实现、零hub质量q、三个收益和actualq平均v；必要两MD先盲后读和独立M≥6k²证明全读保存，当前清洗者有先验不冒新blind。','integrated，原CLI恰1次exit0/stderr0，1118输出全byte同；2单位实例/45scalar不是通用solver/所有策略枚举，原module import0。'),('1118B全status/source/两实例每字段/finite_scalar_regression完整实读；原8多组claim原样仅本4subset。','新资源精确保14/16历史、182/240含自身义务、6456/27442客户及三收益/λ/gap/qavg/WOPT，独立报告count为公式不是实际assert次数，不混作者counter。','integrated，新当前日志sourceSHA与原报告分开保，stdout=file但不是作者stdout，0成功后重复；relatedMD2不extra done。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' complete原8claim/currentowner/sourceSHA精确核，不投影。','comparison_note':b,'decision_note':c,'disposition':'integrated','targets':[P]})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 阶段二关系

ML/MT保数学辅助规则边界，NM新程序资源保两实现/原报告/真实一次CLI。作者逐单位建模后用g3闭式，独审逐单位枚举有序iid对；两者相同输入/策略不成为两个新游戏。q的静态λ、H的静态α_H和真实d_H及q平均真实v都分开，actualrootv>λ不反half。

45回归与全k解析证据分开；先盲重构→后作者对照是原internalreview历史，本轮knowncontext不冒盲审。related2MD仅依赖不extra done，原报告未有执行hash不倒填；当前各原CLI已成功捕获，后续不重复。不做phase3mapper/强制连通。
''')
put(E/'README.md',r'''# hub两原审计的完整软件合同

4primary29126B全实读，必要2MD8395B全读，1新程序对象/4integrated。作者guard/独审top-level、unit2/45scalar、g3闭式/有序iid对、IC含自身计数/完整policy范围精确保。

两个真实原CLI各1次在新空副本实际通过，原码SHA/argv/env/version/time/stdout/stderr/输出保，19704与1118两个新文件均与冻结源全byte同。作者stdout2686投影不是全文件，独审stdout1118是全文件。newmathoriginal2、unit审计4但只有2不同games、moduleimport0、成功后重复0；不新授已充分数学/新blind/外审。

原8fullclaim/currentowner/SHA后才receipt，related2不extra done。Root先push正文证据再done，代理0sharedGit/网络账号/mapper。
''')
cp(D/'preclaim-reading-scope.json',E/'actual-preclaim-reading-scope.json');cp(D/'actual-prepack-reading-scope.json',E/'actual-prepack-reading-scope.json');cp(Path(__file__),E/'build_delivery.py')
nextmp=C/'shared-seats-readme-next-local-input/local-export-manifest.json';nm=json.loads(nextmp.read_text());assert len(nm['rows'])==1 and nm['missing']==[];nextrows=[]
for i in RELATED+['52b1c782e458f410044a']:
 p=REPO/'cleanup/progress'/f'{i}.json';assert not p.exists();x=next(x for x in rows+nm['rows'] if x['id']==i);b=Path(x['local_path']).read_bytes();assert len(b)==inv[i]['size'] and sha(b)==inv[i]['sha256'];nextrows.append({**inv[i],'local_path':x['local_path'],'owner_observed':None,'read_status':'actualfullnecessaryrelatedread/notprimarydone' if i in RELATED else 'actualbyteverifiedonlybeforeNMseal/no fullsemanticread/no claimorreceipt'})
js(W/'next-candidates.json',nextrows);cp(nextmp,E/'next-readme-actual-local-manifest.json')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex(t,c):return sum(1 for n in range(len(t)-1) if ord(t[n])==92 and t[n+1]==c and (n==0 or ord(t[n-1])!=92))
for x in sources+related:
 b=(S/x['preserved_path']).read_bytes();ck('sourceSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('raw8claim',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and len(claim['ids'])==8 and set(IDS)<=set(claim['ids']));ck('ownerSHA',all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('2actualPASS',run['all_passed'] and all(x['exit_code']==0 and x['stderr']['bytes']==0 and x['output']['byte_equal_frozen_report'] and x['output']['stdout_JSON_matches_expected_projection'] for x in run['runs']));ck('differentstdoutcontract',not run['runs'][0]['output']['stdout_exact_full_output_bytes'] and run['runs'][1]['output']['stdout_exact_full_output_bytes']);ck('correctactualcounts',run['original_CLI_calls']==2 and run['original_module_import_calls']==0 and run['distinct_unit_inputs']==2 and run['new_unit_input_runs']==4 and run['finite_scalar_parameters_per_implementation']==45)
for x in runmap:ck('runtime archive '+x['archived_path'],sha((S/x['archived_path']).read_bytes())==x['sha256'])
author=json.loads((S/sources[1]['preserved_path']).read_text());independent=json.loads((S/sources[3]['preserved_path']).read_text());ck('all45authorparameters',[x['k'] for x in author['formula_even_parameters']]==list(range(12,101,2)) and len(author['explicit'])==2);ck('all2unitrecords',[(x['k'],x['total_customers'],x['full_ordered_histories'],x['exact_deviation_comparisons']) for x in author['explicit']]==[(12,6456,14,182),(14,27442,16,240)]);ck('all2independentrecs',[(x['k'],x['unit_customers'],x['histories'],x['all_comparisons_including_own']) for x in independent['expanded_instances']]==[(12,6456,14,182),(14,27442,16,240)]);ck('fullexplicitarrays',all(len(x['standalone_sizes'])==len(x['root_payoffs'])==len(x['static_alpha'])==x['k']+1 for x in author['explicit']));ck('4integrated_receipts',len(receipts)==4 and {x['id'] for x in receipts}==set(IDS) and all(x['disposition']=='integrated' for x in receipts))
t=(S/P).read_text();ck('flatformal',all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));ck('properTeX',tex(t,'[')==tex(t,']') and tex(t,'(')==tex(t,')'));links=[]
for link in re.findall(r'\]\(([^)]+)\)',t):
 if ':' in link or link.startswith('#'):continue
 ok=((REPO/P).parent/link).resolve().exists() or ((S/P).parent/link).resolve().exists();links.append({'link':link,'exists':ok});ck('link '+link,ok)
js(E/'formal-link-check.json',links);obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen='/original/' in '/'+rel or '/necessary-related-original/' in '/'+rel or '/comparison/' in '/'+rel or '/actual-execution-fixture/' in '/'+rel;bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('newderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_actualruntime_original_unchanged':True})
put(W/'delivery.md',f'''# hub作者/独审四源交付

4primary29126B+必要MD2共8395B全真实实读，4integrated/1新程序资源。原8claim {claim['remote_tip']} pushed/synced原字节、本4owner/SHA核。两实际原CLI各1次exit0/stderr0，新19704/1118文件与冻结源byte同，stdout投影/全文分别正确。

neworiginalmath2、unit审计4但distinctgames2，45scalar每实现仅有限；原import0/成功后重复0。不新授全偶参数数学或新blind；related2MD不extra done。Root先push再done，代理无sharedGit/网络账号/mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_links':len(links),'new_formals':1,'new_original_CLI_calls':2,'new_math_original_runs':2})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':29126,'related_MD_bytes':8395,'receipts':4,'dispositions':{'integrated':4},'new_formals':1,'new_formal_bytes':(S/P).stat().st_size,'checks':len(checks),'formal_links':len(links),'raw_claim_ids':8,'claim_tip':claim['remote_tip'],'raw_sync_status':'synced','original_CLI_calls':2,'new_math_original_runs':2,'distinct_unit_inputs':2,'unit_audit_invocations':4,'original_module_imports':0,'reruns_after_success':0,'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
