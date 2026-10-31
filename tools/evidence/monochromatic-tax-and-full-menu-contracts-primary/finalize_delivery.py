from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-monochromatic-tax-and-full-menu-contracts-primary';E=Path('tools/evidence/monochromatic-tax-and-full-menu-contracts-primary');W=Path('cleanup/workspaces/Boss4/r3-monochromatic-tax-and-full-menu-contracts-primary-next')
IDS=['a78d96dc6f303010aea7','1b9335bec700624bc143','276852a177c7326ea276'];P1='archives/customer-attraction/state/候选/单色真实后缀的虚拟相邻税--候选.md';P2='archives/customer-attraction/state/资料/完整真实菜单的条件对偶与旧实例账本--资料.md';P3='archives/customer-attraction/state/审查/四人冻结匹配独审的报告与复用边界--审查.md';PS=[P1,P2,P3]
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def rd(p):return json.loads((S/p).read_text())
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};claimpath=R/'boss4-r3-next-ft-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==set(IDS)
owners=[]
for i in IDS:
 x=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[i]['sha256'];owners.append(x)
cp(claimpath,E/'actual-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners);cp(Path(__file__),E/'finalize_delivery.py')
primary=rd(E/'source-manifest.json');related=rd(E/'related-source-manifest.json');contexts=rd(E/'context-manifest.json')
fj=C/'r3-static-matching-and-induction-route-primary';fe=Path('tools/evidence/static-matching-and-induction-route-primary');reused=[]
for x in json.loads((fj/fe/'reused-evidence-manifest.json').read_text()):
 b=(fj/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'];q=E/'reused-evidence'/x['path'].split('reused-evidence/',1)[1];cp(fj/x['path'],q);reused.append({'path':str(q),'bytes':len(b),'sha256':sha(b),'previous_FJ_path':x['path'],'read_status':'FJ full code/input/execution/output reading honestly reused; no new run'})
x=next(x for x in json.loads((fj/fe/'source-manifest.json').read_text()) if x['id']=='a7579960b289fff40c97');b=(fj/x['preserved_path']).read_bytes();assert sha(b)==x['sha256'];q=E/'reused-input'/x['id']/x['path'];cp(fj/x['preserved_path'],q);reused.append({'path':str(q),'bytes':len(b),'sha256':sha(b),'input_id':x['id'],'previous_FJ_path':x['preserved_path'],'read_status':'FJ complete JSON all-field reading reused; not new primary or SPE replay'})
js(E/'reused-evidence-manifest.json',reused)
scope={'primary_sources':3,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'read_timing':'all3 mathematical originals fully read as related in FJ, actual same-SHA and current-source comparison reused honestly; no pretended new first reading','new_related_full_read_sources':1,'new_related_bytes':sum(x['size'] for x in related),'new_related_id':'b874ab55470546ce897b','new_related_purpose':'R31 ClaimB proves l(2k+1)>=k^2-1 is a sufficient half screen, not a universal necessary frequency condition; full7711B read, not extra done','formal_contexts':len(contexts),'fresh_context_full_read':1,'same_SHA_previous_full_contexts':len(contexts)-1,'original_CLI_calls':0,'new_mathematical_program_calls':0,'new_full_SPE_replays':0,'new_fixed_root_arithmetic_calls':0,'new_LP_or_Nash_solver_calls':0,'new_search_or_matching_scans':0,'derived_resource_builder_calls':1,'derived_resource_builder_failures':0,'derived_literal_clarification':'price increments previously rendered with slash separators changed to explicit tuple(1,1,1,1/6); formatting only, no math run','safe_local_export_helper_calls':3,'local_blob_attempts':6,'local_exports':4,'new_missing_blobs':2,'local_calls':[{'purpose':'necessary menu audit dependencies','ids':['e15c507bf9936c1cd1c8','5c25af511b4e5ef5ee70'],'exports':0,'missing':2},{'purpose':'necessary old frequency-filter source','ids':['b874ab55470546ce897b'],'exports':1,'missing':0},{'purpose':'next candidate bytes only, not semantic primary reading','ids':['0ceafe0cf6073351cde8','cae0027749fb8ec7bd95','24a3ec78bc2dfa4cd31f'],'exports':3,'missing':0}],'prior_missing_reused_no_retry':['912d0cefccf4466d1e31','4638f7b82684049fdae6','1894bab391f4c921d293','b03448e16b1090d7a08f'],'prior_full_manifest_ancillary_missing':'f59cfbb354ecebbae0db retained in unprojected prior capture, not used as a new FT dependency','mathematical_derivations':['VA1 exact3-real-IC residual and same-background monochromatic PNEglobalPhi proof','conditional BB budget under actual-lastA prefix, full frequency sufficient-screen algebra','finite minimax SEP, Jensen static2m budget and valid conditional half implication','stronger universal cyclic/META obligations imply already-refutedFM; no explicit new solver counterexample asserted','independent-review1554 includes259self;26 nonself ties is arithmetic translation of author285, not a new scan'],'new_external_review_or_novelty_claim':False,'phase3_mapper_or_old_graph_import':0,'shared_Git_writes':0,'clean_show_claim_done_checkpoint_calls':0,'network_or_lazy_fetch':0}
assert scope['primary_bytes']==11502 and scope['primary_lines']==204 and scope['new_related_bytes']==7711;js(E/'read-scope-and-evidence-status.json',scope)
coverage=[
{'id':IDS[0],'units':['2026-10-21 directglobal same personal-area52certificate identity','every-instance/everySPE/existoptimal/existmatching exactfrozen bridge','author-standardlib/no canonical/no search/expanded52/Fraction methodology','all259orderedhistories unique dictionary and1554 inclself','285tie1269strict reported,26nonself derived count status','all1296 orderedterminals24optimal0145 repeated allowed','six distinctthemes,actual3322/four47/4/W47OPT52 nothalf','full4x4 frozen matrix/24matching2groups/min1gap/example','actualrow symmetry not policy anonymity','missing original4852/3789 versus different old10829 successfulsameinput','no more review identities/trueV/safety/transport weak bridges refuted'],'targets':[P3],'disposition':'integrated'},
{'id':IDS[1],'units':['header2026-10-25 refutedindividualFM versus2026-10-22 historicalOPEN','full r-slot Kminmax includingforcedroot versusfailedr-1tail','SEP exactforallp existpureB and samep allcolumn separation needed','r1r2strongpush sufficient, D<C aloneinsufficient','genuineinteger v<=Mfull and embeddedactualprefix monotonicity','complete independent-query Jensen/staticexpected-load2m proof and conditionalhalf','old3816themes43nodes/258/self/17/20empty/D14110C6879400/u137','Mfull2396043169/Q/p/fullvectors/pureA2513 allreportedonly, normalizationnotLPproof','audit2096/report1389 newlocalmissing and5537inputoldmissingno rerun','cyclicd_B sufficient versus samepaverage','2C<=D+M atallp symmetricNE sufficiency and currentlogicalcontradictionwithFM, notimplementation','Mpath/aggregate/FREEroot/half separate'],'targets':[P2],'disposition':'integrated'},
{'id':IDS[2],'units':['actualprefix/r+1pathAB^r model/quantifiers allT/b integer','q frozenB not truecontinuation, VA1 allthreeIC/commoncatalog/residual','VA generalr>=2crossbackground unclosed','conditionaltwo-supportlastA(k-1)A+(l-r)B leadsfullABbudget','LASTA deviation lowerbound and lastBoptimalbudget','frequencycondition sufficienthalf only, R31ClaimB exactduplicate identity','monochromaticrstaticPNE globalPhi fullproof arbitraryrealnonnegativebackground','actualSPEsuffix impliesPNE inownbackground notnewbackgroundafterT','fulloldexploration2methods/5topicsm3to5/BBB/4topicsm7A5BBfloating nofrozenfullrun','oldstopnegative instructionhistory notnewexecution','bankmenu andVA differentcontract, nohalfclaimed'],'targets':[P1],'disposition':'integrated'}]
js(E/'semantic-coverage-map.json',coverage)
notes=[('2869B独审全文先前FJ实际已读，本批同SHA逐字节核复用，日期/对象/全部方法、1554含self及285/1269、1296终局/24最优、完整矩阵和边界无遗漏。','比较FJ52客户全JSON/259策略及解析唯一与24匹配、旧origin原码/成功输入绑定；原4852代码/3789报告缺不冒读取或新盲审。','独审资源自足归位并准确区分作者内部报告与另一实现旧真实成功；26非self平局仅计数换算，不增加运行或证明范围。'),('4790B完整菜单全文FJ已实读，本批同SHA诚实复用，顶部更正和四节全部公式/概率/命令/数值完整保全。','与已发表银行Mfull/WP/extraone真反例、r2sharp、静态v因子二/前缀预算、381原缺输入及本次两新缺audit依赖比较。','SEP精确量词和两个强充分接口/静态half条件推导自足保存；旧381值只保作者记录，普遍个体FM/更强路线不再沿旧OPEN，聚合/Mpath/half另保。'),('3843B单色稿全文FJ已实读，本批同SHA复用，VA/三真比较/AB条件用途/频次去重/全局势/全部有限探索范围完整保留。','新增必要R31 7711B全文和现两覆盖AB定理全文，核频次是half充分条件；静态同背景PNE势与改变A后真实后继背景严格区分。','完整证明VA1与单色静态势并保存一般VA未付义务、BB条件预算，补足频次代数与准确方向，不以浮点阴性或银行别合同代解VA。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' actual pushed/synced原回执及当前Boss4 owner/sourceSHA已核。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 阶段二实际数学关系

独审源与52完整策略对象是来源/内部审查关系，不产生新的外审人或执行。原缺4852/3789保持缺，另一origin同SHA成功只核其实际消费的instance/actions/固定OPT目标，不覆盖所有存储JSON字段或285平局。

完整r槽FM与SEP零和对偶精确等价；全p强推送、循环列付款、META增强各是足够条件，不是同名等价。静态v因子二和若每actual节点FM则half的条件推导保真；普遍FM和逐人extraone已有银行真族，旧更强普遍条件也不能继续当无条件真目标。381缺输入旧记录只保有限非分离叙述，不能替成熟34/348/银行原件。

VA实际单色后缀合同有r1真三IC和残余；r>=2尚缺跨背景真实闭包。全B静态PNE全局Phi只在自身固定背景成立；最后A换T进入另子树不能偷用它。VA若成立可给BB收尾的AB预算，这是条件用途。独立已有频次筛选由LASTA保底和末位L直接给half充分条件，不是所有SPE必须满足的必要频次；R31ClaimB去重而不额外done。

本批无数学程序/SPE/LP/Nash复跑，不导旧图/mapper，不制作第三阶段超边或强制连通。
''')
nm=C/'learning-ft-next-readable-contexts/local-export-manifest.json';nr=json.loads(nm.read_text());cp(nm,E/'next-readable-local-manifest.json');nextrows=[]
for x in related:
 assert not (REPO/'cleanup/progress'/f"{x['id']}.json").exists();nextrows.append({**x,'local_path':str(S/x['preserved_path']),'progress_observed':None,'semantic_read_status':'full related reading done FT; not primary completed, sameSHA may honestly be reused after claim'})
for x in nr['rows']:
 assert not (REPO/'cleanup/progress'/f"{x['id']}.json").exists();b=Path(x['local_path']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256'];nextrows.append({**x,'progress_observed':None,'semantic_read_status':'actual available bytes only; mathematical full reading not yet done; no preclaim'})
assert len(nextrows)==4;js(W/'next-candidates.json',nextrows)
put(W/'delivery.md',f'''# FT交付

3primary actual claim {claim['remote_tip']} pushed/synced及owner/sourceSHA全核，3源11502B/204行此前FJ related数学已全读，同SHA诚实复用，不假装新第一读。三新自足正文/3receipt。

保独审作者报告与不同实现旧成功身份、完整r槽菜单的精确对偶和有效静态条件归约、381缺输入的完整旧数值边界、VA1和单色PNE全局势证明及BB条件用途。新全文R31源7711B核频次方向为half充分筛选，不是所有SPE必要条件。

原/new数学CLI、SPE、固定根、LP/Nash/搜索均0；safehelper3次6本地尝试=4齐2新缺，另旧4必要缺件回执复用0重试/网络。下批4实际齐件可接续，其中R31数学全文已related读、3README仅核可用原字节不冒全文。

Root按copy-files白名单精确复制，依赖正文先pushed再done；代理0sharedGit/claim/done/checkpoint/show/真实身份公屏认证/网络。FT包完成后冻结。
''')
p=E/'README.md';t=(S/p).read_text().replace('成功receipt等actual claim pushed/synced与owner核后生成','actual claim pushed/synced与owner已核，成功receipt已生成').replace('另一次R31齐；旧381','另一次R31齐；第三次只核下批3README可用字节，不冒数学实读；旧381');put(p,t)
checks=[]
def ck(n,v,detail=None):
 d={'check':n,'passed':bool(v)}
 if detail is not None:d['detail']=detail
 checks.append(d);assert v,n
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();v=inv[x['id']];ck('exact size/SHA '+x['id'],len(b)==v['size'] and sha(b)==v['sha256']);ck('exact blobSHA1 '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'])
ck('actual unprojected3 capture preserved',(S/E/'actual-claim-receipt.json').read_bytes()==claimpath.read_bytes())
for x in owners:ck('actual primary ownership '+x['id'],x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'])
for x in contexts:
 b=(S/x['snapshot']).read_bytes();ck('exact fresh/reused formal context '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
for x in reused:
 b=(S/x['path']).read_bytes();ck('exact reused evidence/input '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
ex=rd(E/'reused-evidence/replay/execution.json');out=(S/E/'reused-evidence/replay/original.stdout.txt').read_bytes();rep=rd(E/'reused-evidence/replay/origin_retraction_exact_audit.json');ck('old success actual output binding',ex['exit_code']==0 and sha(out)==ex['stdout_sha256']==ex['generated_sha256']==ex['frozen_sha256']);ck('same52 old input primary-data SHA',rep['active_fixture_sha256']==inv['a7579960b289fff40c97']['sha256']==next(x['sha256'] for x in reused if x.get('input_id')=='a7579960b289fff40c97'))
links=[]
for p in PS:
 t=(S/p).read_text();ck('flat MATEK '+p,all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('all nonLF C0 zero '+p,not any(ord(c)<32 and c!='\n' for c in t));ck('all trailing whitespace zero '+p,all(l==l.rstrip() for l in t.splitlines()));ck('display TeX balanced '+p,t.count('\\[')==t.count('\\]'))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  n=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));a=S/n if (S/n).exists() else REPO/n;ck('actual relative link '+dest,a.exists());links.append({'source':p,'destination':dest,'resolved':n,'bytes':a.stat().st_size,'sha256':sha(a.read_bytes())})
js(E/'formal-link-check.json',links)
a=(S/P1).read_text();b=(S/P2).read_text();c=(S/P3).read_text();ck('fullVA1/staticPNE/conditionalBB math','\\tag{VA1}' in a and '\\tag{PNE}' in a and '\\tag{AB-IF}' in a and '包括此前A若有' in a);ck('frequency sufficient direction and complete budget','该频次条件**足以**得到half' in a and '(k-1)(l+1)' in a and 'l(2k+1)<k²−1' in a);ck('full menu dual and author-only missing record','\\tag{SEP}' in b and '239604/3169' in b and '(1525,9362,0,0,0,4958)/15845' in b and '仅概率归一化不能证明' in b);ck('currentFM correction and sufficientMETA distinct','普遍强化因此与银行FM反例不相容' in b and '不是交付的算法或实现时界' in b);ck('whole review count/scope and rational matrix','其中26平局、1269严格' in c and '51/4 | 38/3 | 51/4 | 71/6' in c and '不同实现和研究用途' in c)
ck('full3 sources actual reused-read totals',scope['primary_bytes']==11502 and scope['primary_lines']==204);ck('no new or repeated mathematical execution',scope['original_CLI_calls']==scope['new_mathematical_program_calls']==scope['new_full_SPE_replays']==scope['new_LP_or_Nash_solver_calls']==0);ck('actual helper3calls6attempts4exports2missing',scope['safe_local_export_helper_calls']==3 and scope['local_blob_attempts']==6 and scope['local_exports']==4 and scope['new_missing_blobs']==2)
ck('exact3 complete receipts',len(receipts)==3 and {x['id'] for x in receipts}==set(IDS))
for x in receipts:
 ck('complete semantic receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']))
 for p in x['targets']:ck('actual receipt target '+p,(S/p).exists())
ck('exact3 own formal objects',sorted(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))==sorted(PS))
for x in rd(E/'formal-resource-manifest.json'):
 b=(S/x['path']).read_bytes();ck('actual formal SHA '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
for x in nextrows:
 z=Path(x['local_path']).read_bytes();ck('actual next source available '+x['id'],len(z)==x['size'] and sha(z)==x['sha256'])
obs=[]
for p in S.rglob('*'):
 if not p.is_file() or p.name in ['copy-files.json','copy-paths.txt','delivery-summary.json']:continue
 try:t=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()]
 if bad:obs.append({'path':str(p.relative_to(S)),'lines':bad,'frozen':any('/'+z+'/' in str(p.relative_to(S)) for z in ['original','related','context','context-reused','reused-evidence','reused-input'])})
ck('all derived trailing whitespace zero',not any(not x['frozen'] for x in obs));js(E/'transport-whitespace-observations.json',{'observed':obs,'frozen_originals_unchanged':True})
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'relative_links':len(links),'scope':'Actual claim/source/input/old-run binding, explicit full semantic coverage, current model/quantifier distinctions, C0/metadata/links/receipts/whitelist; not a new SPE/solver/scan or universal proof.'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  z=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(z),'sha256':sha(z)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':scope['primary_bytes'],'primary_lines':scope['primary_lines'],'new_formals':3,'formal_bytes':sum((S/p).stat().st_size for p in PS),'receipts':3,'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'claim_tip':claim['remote_tip'],'next_actual_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
