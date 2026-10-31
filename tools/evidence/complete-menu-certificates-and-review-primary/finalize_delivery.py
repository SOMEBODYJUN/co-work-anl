from pathlib import Path
import json,hashlib,re,posixpath

R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';S=C/'r3-complete-menu-certificates-and-review-primary';E=Path('tools/evidence/complete-menu-certificates-and-review-primary');W=Path('cleanup/workspaces/Boss4/r3-complete-menu-certificates-and-review-primary-next')
P='archives/customer-attraction/state/资料/完整根查询证书的字段与审计范围--资料.md';OLD1='archives/customer-attraction/state/引理/末位真实回复推送的锐曲率与双分支式--引理.md';OLD2='archives/customer-attraction/state/资料/完整根菜单的联合势义务与排序边界--资料.md';IDS=['38f33a2ab903eb816fc8','23b69044426c185f1653','f218c3c894b4635ecca2']
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def rd(p):return json.loads((S/p).read_text())
primary=rd(E/'source-manifest.json');related=rd(E/'related-source-manifest.json');contexts=rd(E/'context-manifest.json');claim=rd(E/'actual-claim-receipt.json');binding=rd(E/'structural-and-field-binding.json');inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==set(IDS)
cp(Path(__file__),E/'finalize_delivery.py');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
scope={'primary_sources':3,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'full_original_read':True,'prior_full_read_reuse':'all three fully read as EG related; never previously primary done; exact bytes reused','related_full_code_sources':2,'related_code_bytes':10829+3119,'related_base_instance_sources':1,'related_base_instance_bytes':1465,'formal_contexts':4,'formal_context_bytes':sum(x['bytes'] for x in contexts),'new_original_CLI_calls':0,'new_math_or_fixed_root_arithmetic_calls':0,'new_full_SPE_replays':0,'new_solver_or_sample_scans':0,'new_structural_builder_attempts':2,'successful_structural_binding_passes':1,'failed_structural_attempts':1,'failure_scope':'invalid proposed compact policy at three empty-second off-path histories, caught before formal body/receipt; exact original actions unchanged','standalone_difference_extraction_calls':1,'new_math_runs_caused_by_recovery':0,'safe_local_helper_calls_for_next_availability':1,'helper_cat_file_attempts':5,'helper_exported_next_sources':3,'missing_next_blobs':2,'primary_Git_or_clean_show_reads':0,'shared_Git_writes':0,'network_or_lazy_fetch':0,'claim_done_checkpoint_calls':0,'old_evidence_scope':'two old complete-SPE successes and one prior EG fixed-root arithmetic result with exact same input/code hashes; no new execution counts borrowed','unreviewed_related_inputs':'origin main also consumed52-client and boundary fixtures previously certified; current primary treatment only348 and34, no claim to reprocess those other inputs','new_inferences':'manual fixed-input polynomial comparison and exact serialized-field/policy/version bindings, not universal safety or half proof','phase3':'no mapper/old graph/forced connection'}
assert scope['primary_bytes']==20418 and scope['primary_lines']==1311
js(E/'read-scope-and-evidence-status.json',scope)
coverage=[{'id':IDS[0],'units':['historical candidate-only blind reconstruction then discoverer comparison','common catalog/real nonnegative background/current-root optimality not needed','same-p independent query and independent reply copy','whole-theme BR K=L nonnegative not each client covariance','exact three-term identity/strict positive cases','complete equality iff L0 and j=p on positive p clients','single-client arbitraryb,t sharpness and zero/empty boundaries','symbol r_x=j_x/K=L, not a matrix'],'targets':[OLD1,P],'decision':'duplicate to complete existing sharp-curvature proof, added precise resource/version notation map'},
{'id':IDS[1],'units':['all11 top keys, instance18 positive types/348 unit clients','full43 ordered actions and shared compact rule','terminal_counts and six forced paths','six forced-root incomes distinct from actual player vector','all6 Phi304 not welfare','all36 root-query K entries and two cycle edges/caps','root_u and verification counting215nonself versus258all','origin audit consumes onlyinstance/actions; flowK3x3 different','prior EG arithmetic independently covers side values; no rerun'],'targets':[P,OLD2],'decision':'integrated field-complete certificate resource preserving data, mathematical use and exact audit consumption'},
{'id':IDS[2],'units':['all14 top keys, source_instance1465 exact base extension only','full13 types/34 unit clients/seven topics including true empty','full57 ordered actions and14 added nodes','three off-path compact-rule mismatches caught and corrected to source','terminal_counts/seven paths/seven root incomes/probability','two root entries D/C/root gaps all tied to old EG','kind label not a valid literal truth assertion, actualD<C<u','verification342nonself versus399all from exact parent source','root polynomial coefficient25/6 versus three-position aggregate12','old code top-level effects and true successful input binding'],'targets':[P,OLD1],'decision':'integrated all fields/data/version plus new self-contained distinction of root and aggregate targets'}]
js(E/'semantic-coverage-map.json',coverage)
notes=[('5009B内部独审全文已实读并核同SHA复用EG related；全部定义/独立副本、逐客户展开、总BR符号、实背景/无根最优前提、完整等号与逐参数锐族、先盲后对照次序均理解。','与已交EG锐曲率引理/发现稿逐一核，r_x=j_x、独审K=slack L而非任一矩阵；现有正文已经完整保所有独有审查补充，不将本次读后整理称盲证/外审。','已有自足引理完整覆盖本源，精确duplicate；新资源保符号/版本/证据去向，不新立同义数学或重跑任何已有程序。','duplicate',[OLD1,P]),
('7417B JSON全部11主键、18客户条目、43有序动作、终局计数、六路径/根收益/Phi/K、cycle/entry/root_u/verification全部全文读，EG related同SHA诚实复用。','补全文读10829B原origin代码、旧完整输出/执行/输入绑定；其消费instance/actions和3x3付款流K不同于本6x6根查询K。EG同输入新算术已核附带数学，当前只作字段相等绑定。','自足资源完整保单位数据/策略规则/全K及数值用途；旧SPE258含自身与源215非自身分清，未把回撤报告零K或PASS误当根矩阵/全部附带字段证明。','integrated',[P,OLD2]),
('7992B JSON全部14主键、13客户类型、57有序动作、计数/七路径/七收益、p、两entry、D/C/两gap/verification全读；source_instance1465B本体也全文核SHA和逐条结构。','补全文读3119B父审计及实际stdout/旧成功记录；根D/C与三位置聚合D/H/G、系数25/6和12不同。紧写初稿在三离轨空第二历史被结构断言拦下，按原数组修正而不改原σ或旧run。','新资源保存完整基文件追加空标签边界及kind字串真值纠正，按算式D<C<u；旧342非自身/399全部比较、import执行副作用均保清，不新增数学CLI/SPE重放。','integrated',[P,OLD1])]
receipts=[]
for i,(a,b,c,d,t) in zip(IDS,notes):receipts.append({'id':i,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 实际三源20418B/1311行，原claim pushed/synced与当前Boss4 owner/source SHA吻合。','comparison_note':b,'decision_note':c,'disposition':d,'targets':t})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md','''# 阶段二实际语义关系

两份JSON是两个不同客户输入的完整有限策略和根数学数据；共享43个六标签历史动作不令不同权重自动都SPE。空主题追加14有序节点须按原数组保留，三历史紧写错误已被真实结构断言发现并纠正，不以计数摘要替代策略。

既有两原程序全SPE成功只覆盖其实际消费字段；origin付款流K与root查询K不同，父方三位置D/H/G与root law D/C不同。EG旧算术补核两JSON根侧值，当前不重复运行。固定输入根与全位置多项式不同，强桥/弱福利/自由Q/half不混同；原kind文字不能代替精确D<C<u。

独审源完整等号、实背景、共同目录和单客户锐性已经自足保于锐曲率对象，按精确去向duplicate；本轮读后归档不重领独立盲证身份。新资源关系是原数据/已证有限输入/程序消费/新增旧算术/实际结构绑定分层，未导mapper/旧图或第三阶段超边，不强制连通。
''')
nextmp=C/'learning-eo-next-local-candidates/local-export-manifest.json';n=json.loads(nextmp.read_text());cp(nextmp,E/'next-local-availability-manifest.json');js(E/'next-missing-inventory.json',[{'inventory':inv[x['id']],'reason':x['reason'],'scope':'candidate availability only, unread absent blob, no primary claim'} for x in n['missing']]);assert len(n['rows'])==3 and len(n['missing'])==2
nxt=[]
for x in n['rows']:
 p=REPO/'cleanup/progress'/f"{x['id']}.json";assert not p.exists(),('next candidate now owned',x['id']);nxt.append({**x,'progress_observed':None,'read_status':'bytes size/SHA256/blobSHA1 available; mathematical full preread not yet done','claim_condition':'Root must claim actual current available intersection; no automatic claim'})
js(W/'next-candidates.json',nxt)
put(W/'delivery.md',f'''# 交付范围

EO3 actual claim {claim['remote_tip']} pushed/synced，三owner/source SHA吻合；三源20418B/1311行。新增1份完整证书资源、3receipt（独审精确duplicate、两JSON integrated），原件、相关两代码/基实例、旧执行/输出及EG旧算术完整保全。

本批数学CLI/固定根重算/全SPE/solver/扫描0；只新增结构绑定。初次紧写策略在3离轨空第二历史被断言拦下，差异记录和修正保留，原100动作及旧run未改。scope记录2次构建尝试、1次成功结构pass，不称两次数学审计。

下一3实际本地齐但尚未数学全文读，另2候选原blob缺失；只提供实际齐件metadata，不预领、不虚填完成。Root按copy-files.json白名单复制，先正文及依赖pushed再逐源done；代理无共享Git/claim/done/checkpoint/show/网络。
''')
checks=[]
def ck(n,b,detail=None):
 d={'check':n,'passed':bool(b)}
 if detail is not None:d['detail']=detail
 checks.append(d);assert b,n
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();v=inv[x['id']];ck('exact inventory bytes '+x['id'],len(b)==v['size'] and sha(b)==v['sha256']);ck('exact blob SHA1 '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'])
ck('actual unprojected3 capture exact bytes',(S/E/'actual-claim-receipt.json').read_bytes()==(R/'boss4-r3-next-eo-claim.json').read_bytes())
for i in IDS:
 x=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());ck('actual owner and source SHA '+i,x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[i]['sha256'])
ck('full actual3 read scope',scope['primary_bytes']==20418 and scope['primary_lines']==1311);ck('both actual code and base read',scope['related_code_bytes']==13948 and scope['related_base_instance_bytes']==1465)
for x in contexts:
 b=(S/x['snapshot']).read_bytes();ck('exact formal context '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
for x in rd(E/'old-evidence-manifest.json'):
 b=(S/x['preserved_path']).read_bytes();ck('exact actual old evidence '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
failure=rd(E/'structural-first-attempt-difference.json');bad=next(x['mismatches'] for x in failure['rows'] if x['source_id']==IDS[2]);ck('actual failed compact rule differences preserved',len(bad)==3 and [x['actual_source_action'] for x in bad]==[4,3,3]);ck('successful full action-field pass after correction',binding['compact_rule_matches_every_serialized_action'] and binding['all43_six_label_history_actions_shared']);ck('not a new numeric audit',binding['new_mathematical_runs']==0 and scope['new_math_or_fixed_root_arithmetic_calls']==0)
ck('full certificate counts and base append version mapped',binding['terminal_count_fields_match_EG_actual_roots'] and all(binding['base1465_vs_extended7992'].values()));ck('kind true order not inherited text',binding['kind_metadata_correction']['actual_exact_order']=='D<C<u')
t=(S/P).read_text();ck('flat MATEK',all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('all nonLF C0 zero',not any(ord(c)<32 and c!='\n' for c in t));ck('trailing whitespace zero',all(l==l.rstrip() for l in t.splitlines()));ck('TeX display balance',t.count('\\[')==t.count('\\]'));ck('source placeholders resolved',not any(v in t for v in ['SRC_','OLD_ORIGIN','TYPES348','TYPES34','ROOTPATHS','QUERYK','EVID']))
links=[]
for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
 if '://' in dest or dest.startswith('#'):continue
 target=posixpath.normpath(str(Path(P).parent/dest.split('#',1)[0]));at=S/target if (S/target).exists() else REPO/target;ck('actual relative link '+dest,at.exists());links.append({'source':P,'destination':dest,'resolved':target,'bytes':at.stat().st_size,'sha256':sha(at.read_bytes())})
js(E/'formal-link-check.json',links)
ck('one new formal only',[str(p.relative_to(S)) for p in (S/'archives').rglob('*.md')]==[P])
for x in rd(E/'formal-resource-manifest.json'):
 b=(S/x['path']).read_bytes();ck('formal resource binding',len(b)==x['bytes'] and sha(b)==x['sha256'])
ck('exact3 complete semantic receipts',len(receipts)==3 and {x['id'] for x in receipts}==set(IDS))
for x in receipts:
 ck('complete receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']))
 for p in x['targets']:ck('receipt target '+p,(S/p).exists() or (REPO/p).exists())
ck('all unique fields semantic destinations',len(coverage)==3 and all(x['units'] and x['targets'] for x in coverage));ck('root and full position polynomials separate','25}6e^2' in t and '-e+12e^2' in t and '+1/50' in t);ck('query and payment K separate','3×3付款传播矩阵' in t and '6×6根查询矩阵' in t);ck('old source code side effects stated','import也会执行' in t and '覆写同名报告' in t);ck('three next actual local candidates not pre-read-claimed',len(nxt)==3 and all(x['progress_observed'] is None for x in nxt))
obs=[]
for p in S.rglob('*'):
 if not p.is_file() or p.name in ['copy-files.json','copy-paths.txt','delivery-summary.json']:continue
 try:z=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 lines=[i+1 for i,l in enumerate(z.splitlines()) if l!=l.rstrip()]
 if lines:obs.append({'path':str(p.relative_to(S)),'lines':lines,'frozen':any('/'+v+'/' in str(p.relative_to(S)) for v in ['original','related','context','reused-evidence','reused-EG-arithmetic'])})
ck('no derived whitespace errors',not any(not x['frozen'] for x in obs));js(E/'transport-whitespace-observations.json',{'observed':obs,'policy':'frozen originals/related/context/old evidence not normalized'})
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_all_nonLF_C0':0,'formal_trailing_whitespace':0,'relative_links_checked':len(links),'scope':'actual source/claim/owner/hash, complete serialized-field and policy comparisons, semantic distinctions, formatting/links; no new mathematical run or universal certification'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');out={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':scope['primary_bytes'],'primary_lines':scope['primary_lines'],'new_formals':1,'formal_bytes':(S/P).stat().st_size,'semantic_receipts':3,'duplicate_ids':[IDS[0]],'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'structural_attempts':2,'successful_structural_passes':1,'claim_tip':claim['remote_tip'],'next_actual_candidates':[x['id'] for x in nxt]};js(Path('delivery-summary.json'),out);print(json.dumps(out,ensure_ascii=False,indent=2))
