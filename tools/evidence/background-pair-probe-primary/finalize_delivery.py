from pathlib import Path
import json,hashlib,re,posixpath,ast
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-background-pair-probe-primary';E=Path('tools/evidence/background-pair-probe-primary');W=Path('cleanup/workspaces/Boss4/r3-background-pair-probe-primary-next');P='archives/customer-attraction/state/程序/合法背景首对安全值的交替锥探针--程序.md';I='2db24df0ce02d6fd610c'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def rd(p):return json.loads((S/p).read_text())
claimpath=R/'boss4-r3-next-gb-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and claim['ids']==[I];owner=json.loads((REPO/'cleanup/progress'/f'{I}.json').read_text());primary=rd(E/'source-manifest.json');x=primary[0];assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256'];cp(claimpath,E/'actual-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',[owner]);cp(Path(__file__),E/'finalize_delivery.py')
scope={'primary_sources':1,'primary_bytes':5375,'primary_lines':x['lines'],'full_code_read':'FU actual full code read reused honestly GB with sameSHA, plus new whole-repository source/old-caller comparison; no pretended fresh first reading','program_functions':['representation','policy_cone','security','cone_step','main'],'new_original_CLI_calls':0,'new_module_imports':0,'new_math_program_runs':0,'new_SPE_game_or_LP_checks':0,'old_success_replays':0,'FU_polynomial_check_replays':0,'new_analytical_derivations':['ideal exactIC pair-normalized weights bounded by k(ell+n)','fullinterest type gives every formalpolicy a rational feasible baseline ratio1, not upperbound or solver output','rational reconstruction/clearing denominators obligations for real unit counterexample','actualmain integer coefficient range and eachtrial LP static upperbound, not old actual count'],'old_module_use':'sameSHA5375 loaded as base by3194 oldcaller, callsrepresentation/policy_cone only; old75sample entry13.116131986exit0 not newmain run/security/coneStep validation','old_historical_main_records':'260 and later500 are separate author reports, absent original bound outputs and no new trials or inferred LP counts','prior_missing_dependencies':'312/330 reports and SSR code/report preserved in prior rawlocal supply; no retries','new_safe_helper_calls':1,'new_local_blob_attempts':3,'new_local_exports':3,'new_missing_blobs':0,'new_helper_purpose':'next3README byteavailability only, not primary mathematical read','formal_contexts':[{'path':z['path'],'read_status':z['read_status']} for z in rd(E/'context-manifest.json')],'derivation_domain':'exactrational ideal LP identities/IC; doubleΓ/HiGHS floatoutputs require independent exact checking','network_or_lazy_fetch':0,'shared_Git_writes':0,'clean_show_claim_done_checkpoint_calls':0,'phase3_mapper_or_graph_import':0,'derived_builder_calls':1,'builder_display_recovery':'terminal print line202 came from latercontext variable; primarymanifest always131, terminal printfixed without sourceprogram rerun'}
assert x['lines']==131;js(E/'read-scope-and-evidence-status.json',scope)
js(E/'semantic-coverage-map.json',[{'id':I,'units':['allimports/guard/5functions complete source','nonemptytype/member/sunk/repeatedn-1backgrounds/query+1/L integerdomain','allorderedwalk+fullactions/actual/truechildrenIC/exactintegerdedup thenfloat','pairdenominator actualincludesown player/clamp0 convention','security variablesobjectiveallstaticcolumns/simplex/bounds/failure','coneStep variables/Gamma/normalizedpair/beta/safetyallcolumns/failure','idealnormalizationbounded and allinterestbaseline1 completeanalyticalproof','seed/allnormalandlargeconfigs/backgrounddensities/weights','two starts/max7/three thresholds/max29staticLPcallsnotactual','allresult/incumbent/candidatefields/rootemptyhistorykey/floatnotunitcertificate','progress/trials/errorIO/noParentMkdir/nonpositiveTrials/earlyreturn','olddependencyuse actualsameSHA versus main historical260500','PB/currentroottruev/extraone/half model distinctions'],'targets':[P],'disposition':'integrated'}])
receipt={'id':I,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':'5375B/131行全部源码FU已逐函数完整实读，GB核同SHA诚实复用；representation/policy_cone/security/cone_step/main、参数/所有JSON字段/阈值/异常/历史函数调用全部整理。actualGB pushed/synced和Boss4 owner/sourceSHA已核。','comparison_note':'完整读实际3194B旧调用者、旧来源与EXECUTIONS捕获、现额外槽审查；回应资源仅1..135行历史探针表明确标范围；FU全读PB真反例同SHA复用，1976B旧README/缺报告不冒main重跑或260输出认证。','decision_note':'新增自足程序对象精确区分整数初始全策略与近似Γ/浮点LP，保全部量词；给理想归一化有界性及全兴趣ratio1基线解析证，旧模块函数使用不等于main或security/coneStep执行。新增原CLI/模块/数学/LP/SPE运行0，无half/外审/新颖性认证。','disposition':'integrated','targets':[P]};js(W/'semantic-receipts.json',[receipt])
put(W/'relation-review.md',r'''# 阶段二关系

源码实现固定完整有序σ的真实IC锥和独立静态查询零和LP，先生成精确整数初始策略、再用double约束改实质量，不能用初始正确性免费认证近似w。P归一与全兴趣基线的解析说明只用于理想精确LP，不把浮点ratio1升级一般pair正定理。

同SHA作为其它扫描的依赖已有真实函数使用；旧3194调用者只用representation/policy_cone，自己的强聚合目标和零背景与本非零背景首对main不同。260/500作者历史不加成新样本，不冒模块guard被突破。本批不重跑这些或FU一次多项式。

任意合法背景pair已由更弱PBextra反驳，但背景actualroot可达性、根真聚合、全位置pair和六人half分别保量词。程序不导入旧图或认mapper，关系为阶段二实现/条件模型/有限证据边界。
''')
nm=C/'learning-gb-next-readable-README/local-export-manifest.json';nr=json.loads(nm.read_text());nextrows=[]
for z in nr['rows']:
 b=Path(z['local_path']).read_bytes();assert len(b)==z['size'] and sha(b)==z['sha256'];p=REPO/'cleanup/progress'/f"{z['id']}.json";pr=json.loads(p.read_text()) if p.exists() else None;nextrows.append({**z,'current_progress':pr,'semantic_read_status':'actual bytes only, no GE mathematical full read yet','routing':'Root already separately authorized GE3; sourceIDs must match raw22claim intersection, not a projected receipt'})
js(W/'next-candidates.json',nextrows)
put(W/'delivery.md',f'''# GB交付

单source5375B/131行，actual claim {claim['remote_tip']} pushed/synced、owner/sourceSHA吻合。完整代码同SHA复用，1新自足程序正文/1完整receipt。新增理想LP归一有界/全兴趣基线解析与main/function运行界，0源CLI/模块导入/数学/LP/SPE/旧成功复跑。

旧3194调用者与未投影EXECUTIONS完整原捕获保留，不把四旧entry记本源码执行。builder终端行数影子变量202已修，来源manifest自始正确131，格式恢复另记。Root依白名单精确复制、先推依赖正文再done；GB包成熟后冻结。

下一GE3已另授权，3README共6144B实字节齐，GB未读数学；Root实际22ID原回执交集/owner将另核，不与RootGC4四globalproof源重叠。
''')
rp=E/'README.md';put(rp,(S/rp).read_text().replace('成功receipt在actualclaim/owner后生成','actualclaim/owner已核，成功receipt已生成'))
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
b=(S/x['preserved_path']).read_bytes();ck('exact primarysize/SHA',len(b)==x['size']==5375 and sha(b)==x['sha256']);ck('exact primaryGit blobSHA1',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']);ck('actual raw1claim', (S/E/'actual-claim-receipt.json').read_bytes()==claimpath.read_bytes());ck('actual currentowner',owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256'])
tree=ast.parse(b.decode());names={z.name for z in tree.body if isinstance(z,ast.FunctionDef)};ck('whole5functions structurally inspected withoutexecution',names==set(scope['program_functions']));ck('sourceguard noimport-run',"if __name__=='__main__':" in b.decode())
for z in rd(E/'related-source-manifest.json'):
 q=(S/z['preserved_path']).read_bytes();ck('exact related1976source',len(q)==z['size'] and sha(q)==z['sha256'])
for z in rd(E/'context-manifest.json'):
 q=(S/z['snapshot']).read_bytes();ck('exact fullorpartial explicitcontext '+z['path'],len(q)==z['bytes'] and sha(q)==z['sha256'])
for z in rd(E/'reused-module-evidence-manifest.json'):
 q=(S/z['path']).read_bytes();ck('exact oldmoduleevidence '+z['path'],len(q)==z['bytes'] and sha(q)==z['sha256'])
ck('oldcomparison source exactsameSHA',sha((S/E/'reused-module-evidence/comparison/2db24df0ce02d6fd610c/source').read_bytes())==x['sha256']);ex=rd(E/'reused-module-evidence/runs/EXECUTIONS.json');er=next(z for z in ex if z['source_id']=='bf46dd86db65a5613aec');caller=(S/E/'reused-module-evidence/original/bf46dd86db65a5613aec/source').read_bytes();ck('oldcaller code/execution identity',sha(caller)==er['script_sha256'] and er['exit_code']==0 and er['invocations']==1);ct=caller.decode();ck('actualcaller uses2functions notmain',all(a in ct for a in ['base.representation','base.policy_cone']) and all(a not in ct for a in ['base.main(', 'base.security(', 'base.cone_step(']))
t=(S/P).read_text();ck('flatMATEK',all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('all nonLF C0zero',not any(ord(c)<32 and c!='\n' for c in t));ck('all trailingwhitespacezero',all(l==l.rstrip() for l in t.splitlines()));ck('TeXdisplaybalanced',t.count('\\[')==t.count('\\]'));links=[]
for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
 if '://' in dest or dest.startswith('#'):continue
 n=posixpath.normpath(str(Path(P).parent/dest.split('#',1)[0]));p=S/n if (S/n).exists() else REPO/n;ck('actual relativelink '+dest,p.exists());links.append({'source':P,'destination':dest,'resolved':n,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
js(E/'formal-link-check.json',links)
ck('fullexactLP/normalization/baseline math','理想cone_step至少能达到z=1/2' in t and 'Σ_Jw_J≤Σ_aL_a≤k(ℓ+n)u1≤k(ℓ+n)' in t and '代码存的是double近似Γ' in t);ck('all sourceoutput/threshold/limits','最多29次LP调用' in t and 'default160不能认证作者260' in t and '两个改善阈值不同' in t and '非正走空循环' in t);ck('genuinezero-denominatorconvention','分子0时贡献0' in t);ck('scopezeroexecutionnotold500maincert',scope['new_original_CLI_calls']==scope['new_module_imports']==scope['new_math_program_runs']==scope['old_success_replays']==0)
for z in rd(E/'formal-resource-manifest.json'):
 q=(S/z['path']).read_bytes();ck('formalbytes/SHA',len(q)==z['bytes'] and sha(q)==z['sha256'])
ck('exact1complete semanticreceipt',receipt['id']==I and all(receipt[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']));ck('receipt actualtarget',(S/P).exists());ck('exact1ownformal',list((S/'archives').rglob('*.md'))==[S/P]);ck('primarycorrect131lines',x['lines']==131 and len(b.splitlines())==131);ck('actualnext3metadataonly',len(nextrows)==3 and sum(z['size'] for z in nextrows)==6144)
obs=[]
for p in S.rglob('*'):
 if not p.is_file() or p.name in ['copy-files.json','copy-paths.txt','delivery-summary.json']:continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 ls=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()]
 if ls:obs.append({'path':str(p.relative_to(S)),'lines':ls,'frozen':any('/'+z+'/' in str(p.relative_to(S)) for z in ['original','related','context','reused-module-evidence'])})
ck('all derivedwhitespacezero',not any(not z['frozen'] for z in obs));js(E/'transport-whitespace-observations.json',{'observed':obs,'frozen_originals_unchanged':True});js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'scope':'Actualclaim/source/hash and oldmodule usage binding, fullmath/software contract plus staticAST/format/link/receipt checks; no sourceprogram/LP/SPE execution'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  q=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(q),'sha256':sha(q)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(z['path'] for z in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(z['bytes'] for z in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':[I],'primary_bytes':5375,'primary_lines':131,'new_formals':1,'formal_bytes':(S/P).stat().st_size,'receipts':1,'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'old_replays':0,'claim_tip':claim['remote_tip'],'next_GE3':[z['id'] for z in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
