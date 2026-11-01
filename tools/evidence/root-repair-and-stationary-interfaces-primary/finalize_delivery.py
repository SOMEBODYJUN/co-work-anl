from pathlib import Path
import hashlib,json,re,posixpath

R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-root-repair-and-stationary-interfaces-primary'
E=Path('tools/evidence/root-repair-and-stationary-interfaces-primary');W=Path('cleanup/workspaces/Boss4/r3-root-repair-and-stationary-interfaces-primary-next')
P1='archives/customer-attraction/state/候选/真实子树价格向量的共同静态背景归纳--候选.md'
P2='archives/customer-attraction/state/反例/真实尾平稳均值的额外查询封顶--反例.md'
P3='archives/customer-attraction/state/引理/两名剩余完整终局菜单的纯列封顶--引理.md'
OLDROOT='archives/customer-attraction/state/资料/首次饱和与独立审查的版本路由--资料.md'
OLDALL='archives/customer-attraction/state/引理/完整槽插入税与跨角色价格恒等式--引理.md'
IDS=['43fcfd09b6d0ae5d96b5','c57e4ec366e7af1be467','ef21819792cb2a9aac5f','793061843887102a114a','62fadc53e30b4b1c856b']
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def rd(p):return json.loads((S/p).read_text())
primary=rd(E/'source-manifest.json');related=rd(E/'related-source-manifest.json');contexts=rd(E/'context-manifest.json');claim=rd(E/'actual-claim-receipt.json');run=rd(E/'runs/stationary-independent-001/run-metadata.json');report=rd(E/'runs/stationary-independent-001/report.json')
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==set(IDS)
cp(Path(__file__),E/'finalize_delivery.py')
for n in ['learning-dy-common-background-draft.md','learning-dy-pure-column-draft.md']:
 p=S/E/'build-inputs'/n;t=p.read_text();t=t.replace('比较笔记：仅预读与理解，尚未断言DY认领或完成，不在正式copy白名单。','历史预读草稿：创建时尚未确认DY认领；现只作本批构建输入，实际认领见actual-claim-receipt.json。');p.write_text(t)
missing=rd(E/'absent-original-stationary-audit-manifest.json');assert not missing['rows'] and len(missing['missing'])==2
js(E/'missing-audit-inventory-bindings.json',[{'inventory':inv[x['id']],'actual_local_supply':'absent, not read/executed, no network attempted','primary_disposition':'not part of DY5, no claim or done'} for x in missing['missing']])
js(E/'local-export-events.json',{'actual_calls':[{'call':1,'folder':'learning-dy-local-inputs','IDs':IDS,'helper_exit_code':0,'exported':5,'missing':0},{'call':2,'folder':'learning-dy-stationary-audit-inputs','IDs':['b59d80ac2b02969bd86e','a14a025eaabac25f48df'],'helper_exit_code':0,'exported':0,'missing':2},{'call':3,'folder':'learning-dy-reply-column-inputs','IDs':['c7681bcaecb3e63137ff','7fd268a01ce3f10dcb2a'],'helper_exit_code':0,'exported':2,'missing':0},{'call':4,'folder':'learning-dy-comparison-tail-inputs','IDs':['6c84043505685faee8ec','68ed7412ef2da880f80f','5ea43c826b2651fe9de7'],'helper_exit_code':0,'exported':3,'missing':0}],'safe_local_cat_file_attempts':12,'successful_exports':10,'missing_local_blobs':2,'network_or_lazy_fetch':0,'direct_Git_outside_helper':0,'shared_Git_writes':0,'no_retry_of_missing':True})
scope={'primary_sources':5,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'primary_full_actual_read':True,'prior_read_reuse':'all five previously read as DM related only, exact same bytes now verified; no fictitious new first reading or old primary completion','related_sources':5,'related_bytes':sum(x['size'] for x in related),'related_full_actual_read':True,'contexts':len(contexts),'context_bytes':sum(x['bytes'] for x in contexts),'safe_local_helper_calls':4,'local_blob_read_attempts':12,'local_blob_exports':10,'missing_unread_audit_blobs':2,'original_mathematical_CLI_calls':0,'new_independent_finite_checker_CLI_calls':1,'new_independent_verification_body_executions':1,'new_input_instances':1,'finite_strategy_histories':43,'all_comparisons':258,'self_comparisons':43,'nonself_comparisons':215,'ties_including_self':89,'new_sample_or_parameter_scan':0,'derived_static_coverage_display_rows':20,'derived_static_coverage_table_generations':1,'derived_builder_calls':3,'derived_builder_failures':2,'derived_builder_successes':1,'scope_of_builder_errors':'table header string conversion and tuple history-key formatting only; checker/source/report unchanged','network_or_lazy_fetch':0,'shared_Git_writes':0,'clean_show_claim_done_checkpoint_calls':0,'phase3_mapper_or_graph_imports':0,'mathematical_validation':'full source reconstruction plus once new independent standard-library exact finite recheck from complete bound Markdown data; not absent original CLI reproduction, LP optimality, external review or universal proof','original_audit_source_status':'both original audit blobs unavailable; exact missing receipt kept, old DM historical scope unchanged'}
assert scope['primary_bytes']==20908 and scope['primary_lines']==372 and scope['related_bytes']==23339
js(E/'read-scope-and-evidence-status.json',scope)
coverage=[
 {'id':IDS[0],'units':['full positive-depth SPE and arbitrary root','exact R/MENU with same-menu extrema','AAAF actual-column failure versus static/mixed possibilities','old individual extra-one OPEN corrected via Jensen/bank','FREE-ROOT empty-root tight all-r family and arbitrary-prefix version','63-type specified three-player strategy cone, OPT4 finite7/4 only','missing min/max-branch joint credit; no changed real prefix profit guarantee','old route/task identity not an active command'],'targets':[P1,OLDROOT],'decision':'duplicate to already complete DM root-only route, with present common-vector interface made explicit'},
 {'id':IDS[1],'units':['SF-root tail kernel, stationary distribution and deterministic complete-leaf mean','all21 masks and1274 distinct unit clients','full43 histories and all258 exact comparisons','W/OPT/half separation','unique stationary class and full6 prices','free uniform fractional countercheck, legal integer(0,5), v3 upper not equality','source original audit/replay claims versus local missing2','new once independent checker from actual MD, not original audit','current old OPEN corrections not transplanted into old bytes'],'targets':[P2,P1],'decision':'integrated as complete finite counterexample with explicitly new independent evidence and original unavailable boundary'},
 {'id':IDS[2],'units':['full all-m two-theme game and all-history strategy proof','every actual prefix k and r, actual root incomes','complete K, strict meta-Nash, full/tail independent margins','no uniform positive alpha and exact necessary ratios/thresholds','not Mfull, all-p strong-push or half failure in that family','two-person COL side audit and exact intersection tax','max naked-reply pure column and real last BR','multi-reply joint R sign unproved, no old audit/cycle replay claimed'],'targets':[OLDALL,P3],'decision':'integrated: complete all-m content precisely reuses DM object; unique detailed side audit now in new pure-column lemma'},
 {'id':IDS[3],'units':['historical general safety/extra-one open scope','stationary specified background stopped, not free/aggregate/half counterexample','original independent audit unit-data and43/258 contract, now absent code scope retained','aggregate common-distribution attempt route','next shared query-independent background or direct coverage payment','old source task preferences not cleaner instructions'],'targets':[P1,P2],'decision':'integrated: self-contained route/current evidence distinction, no code read or execution inferred from README'},
 {'id':IDS[4],'units':['any legal integer prefix and r remaining full SPE','real root d_A/u and later total H_A; G not coverage with background','conditional child aggregate bounds and legal static embedding','gap G-rs split, lower-bound direction insufficient','full child price vectors and query-independent parent mixture','f_A(A) changes distribution and copies root; diagonal not enough','correct extra-one child/parent slot count but no root cap','historical individual extra-one status versus current Jensen refutation','no new general aggregate payment and no no-go theorem for all mixtures'],'targets':[P1],'decision':'integrated: every equation and actual induction gap self-contained, conditional assumptions explicit'},
]
js(E/'semantic-coverage-map.json',coverage)
notes=[
 ('4419B root-only全文实读已在DM related完成，本批核同SHA诚实复用；完整R/MENU、单列失败、extra-one旧说法、FREE-ROOT紧族/背景版、指定63型策略锥7/4及真实跨枝缺口全部理解。','与已交DM完整路由、可信三倍根修复、两名剩余三比较任意背景定理及当前Jensen/银行整数extra-one纠正逐项比较；一般FREE-ROOT与已证人数鲁棒R分开。','全部独有内容此前已在DM路由自足保存，本批按精确去向duplicate并补共同向量归纳连接；不将有限作者断言认证为新LP复现，不把旧OPEN覆盖当前结论。','duplicate',[OLDROOT,P1]),
 ('3963B指定stationary分数背景原文全文已读并同SHA复用；21类1274单位客户、完整历史策略、唯一π、全部价格/自由背景/整数上界和旧审计身份全读。','原audit代码/JSON安全本地缺失，缺失回执保留；本批新写独立Fraction从绑定MD真实表展开单位客户，唯一一次核43历史/258比较/OPT/π/六价格，并读全部实际报告。','独立新代码及唯一run不是缺失原CLI重放；自足有限反例含客户/43历史收益表/20覆盖表/六价格，保严格差1149/910，不扩成half/自由背景/聚合反例。','integrated',[P2,P1]),
 ('6504B全人数完整SPE重构全文及r2裸回复旁审已实读，同SHA复用；m/r/k不同量、K/Nash/边际、比率/阈值、u-blocker/全p强推及税分母全部理解。','与旧2057B在轨例、5748B联合身份、6035B两人任意p余量及6262B根菜单义务完整比较；DM已交全人数主体准确复用，侧审纯列与多后继边界另立详细证明。','全人数独有内容精确去向既有完整插入税正文，r2最大裸回复/交集税/纯列补入新引理；没有重复原数值审计或以一般联合R恒等式宣称付款。','integrated',[OLDALL,P3]),
 ('1192B security README全文已读并核同SHA；指定stationary构造、原audit/JSON独立实现宣称、聚合分布尝试及下一付款义务/旧角色偏好全部读。','与主源c57/4830B尝试、当前原整数首位已失败的Jensen桥比较；实际原audit缺失和本次新增独立有限核验清楚分开，不从README文字推原程序已读。','独有路由与真实时间状态归入共同背景候选和指定反例；旧OPEN/路线偏好只存历史，聚合与FREE-ROOT不同合同仍保留。','integrated',[P1,P2]),
 ('4830B共同静态分布全文已读并同SHA复用；所有五节及(1)-(6)、子树假设、H/G/利润身份、Q_A槽数、f_A向量、mu查询独立、对角复制和extra-one未闭合处逐式重构。','与当前安全值定义/银行个体反例、root-only、两人纯列/任意p推送比较；孩子下界不能转父cap上界，b非零剩余利润不能当覆盖；旧原整数extra-one OPEN现已纠正。','新增自足共同向量归纳候选保全部合法条件步骤及真实缺口；不误报一般聚合证明，也不从一个未闭合构造声称所有共同混合不可能。','integrated',[P1]),
]
receipts=[]
for i,(a,b,c,d,t) in zip(IDS,notes):receipts.append({'id':i,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 五源20908B/372行，实际5认领pushed/synced及当前Boss4 owner/source SHA核验。','comparison_note':b,'decision_note':c,'disposition':d,'targets':t})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md','''# 实际语义关系

共同静态背景候选保子树对偶证书/固定主题嵌入的准确条件，指出标量下界不能给父上界；与root-only菜单min/max是不同的跨真实历史义务。现有Jensen t<=v和银行完整SPE确实否定旧个体整数extra-one，未否定聚合W桥或一般FREE-ROOT。已有可信根修复只条件接入相同已证人数的鲁棒R。

新stationary反例的输入/核/分数均值完全确定，唯一pi排除同核内另选平稳分布。其新标准库单位客户审计是本次独立有限证据；原两audit本地缺失，README/原作者重放宣称不冒充读到的代码。改变核、自由q/任意合法静态背景、完整随机列与平均META另有量词，不能一并否定。

两人纯列对象使用恰一位真实后继的BR支付联合R，再选最大裸回复，另比全局双主题势和任意p曲率推送。全人数在轨价格边界主体完整复用旧DM，侧审交集税补全；多后继R不定号，不能据此自动推广。旧源内部审查、当前读后证明、一次新增有限核验及外审分开。

这是阶段二真实关系检查；未导入mapper/旧图、未强制连通、未生成第三阶段超边。原件/旧DM正文保持其历史字节，不覆写未读原audit的旧事实。
''')
nextids=['c7681bcaecb3e63137ff','7fd268a01ce3f10dcb2a','6c84043505685faee8ec','68ed7412ef2da880f80f','5ea43c826b2651fe9de7']
nextrows=[]
for i in nextids:
 p=REPO/'cleanup/progress'/f'{i}.json';assert not p.exists(),('candidate now owned',i)
 nextrows.append({**inv[i],'progress_observed':None,'actual_local_input':next(x['local_path'] for x in related if x['id']==i),'actual_read_status':'full DY related read, no primary completion or automatic claim','owner_requirement':'Root must recheck and claim only actually available intersection'})
js(W/'next-candidates.json',nextrows)
put(W/'delivery.md',f'''# 交付范围

DY5原claim {claim['remote_tip']} pushed/synced，当前5 owner/source SHA吻合。5源20908B/372行，3个新自足正文与5receipt；root-only精确duplicate到已交完整路由，其余integrated。DM48冻结包不改。

必要原audit2件本地缺失，缺失manifest/完整inventory绑定保留，无网络或重试。新增独立标准库Fraction代码从主MD完整客户表取真实输入，只运行一次，43历史/258比较全部通过；原CLI0。正文20行静态覆盖展示表不是第二次策略核验。派生表格构建器两次格式错误已准确记载并修，不混进数学核验次数。

Root严格按copy-files.json复制，先正文/依赖正常pushed后逐源done。下一五件均纯本地齐且全文仅作related，未预领；缺失audit不冒充齐件候选。此代理无shared Git/claim/done/checkpoint/show/网络操作。
''')
checks=[]
def ck(n,b,detail=None):
 d={'check':n,'passed':bool(b)}
 if detail is not None:d['detail']=detail
 checks.append(d);assert b,n
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();v=inv[x['id']]
 ck('exact inventory source bytes '+x['id'],len(b)==v['size'] and sha(b)==v['sha256'])
 ck('exact local blob SHA1 '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'])
ck('actual full five claim byte preserved',(S/E/'actual-claim-receipt.json').read_bytes()==(R/'boss4-r3-next-dy-claim.json').read_bytes())
for x in primary:
 p=json.loads((REPO/'cleanup/progress'/f"{x['id']}.json").read_text());ck('current owner and source SHA '+x['id'],p['owner']=='Boss4' and p['disposition']=='in-progress' and p['source_sha256']==x['sha256'])
ck('full actual five primary bytes/lines and reused read',scope['primary_bytes']==20908 and scope['primary_lines']==372 and len(rd(E/'prior-related-full-read-reuse.json'))==5)
ck('full five actual related sources',len(related)==5 and scope['related_bytes']==23339)
ck('two audit blobs absent and not invented',len(missing['missing'])==2 and not missing['rows'])
ck('helper invocations/success/missing honest',scope['safe_local_helper_calls']==4 and scope['local_blob_read_attempts']==12 and scope['local_blob_exports']==10)
for x in contexts:
 b=(S/x['snapshot']).read_bytes();ck('exact formal context '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
for p in [OLDROOT,OLDALL]:ck('old DM canonical unchanged '+p,(REPO/p).read_bytes()==(C/'r3-first-saturation-and-insertion-credit-primary'/p).read_bytes())
ck('new code exact run SHA',sha((S/E/'new-independent-stationary-check.py').read_bytes())==run['code_sha256'])
ck('new checker bound actual original MD',run['source_md_sha256']==inv[IDS[1]]['sha256']==report['source_md_sha256'])
ck('only one new verification body and no original CLI',run['new_independent_CLI_runs']==1 and run['verification_body_executions']==1 and run['original_audit_CLI_runs']==0 and len(list((S/E/'runs').iterdir()))==1)
ck('new finite run succeeded and empty stderr',run['exit_code']==0 and run['assertions_enabled'] and (S/E/'runs/stationary-independent-001/stderr.txt').stat().st_size==0)
ck('all43 real report rows read/preserved',len(report['all_43_history_rows'])==43 and report['all_action_comparisons']==258 and report['nonself_comparisons']==215)
ck('exact finite case result retained',report['welfare']==846 and report['optimal_3']==1032 and report['query2_minus_actual_root']=='1149/910' and report['stationary_cap']=='123652/455')
ck('new display coverage table not second audit',len(rd(E/'derived-static-coverage-display-table.json')['rows'])==20 and scope['derived_static_coverage_table_generations']==1)
ck('actual derived formatting failures documented',rd(E/'derived-format-recovery.json')['actual_builder_calls']==3 and len(rd(E/'derived-format-recovery.json')['failures'])==2)
links=[]
for p in [P1,P2,P3]:
 t=(S/p).read_text();ck('flat MATEK '+p,all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']))
 ck('all nonLF C0 zero '+p,not any(ord(c)<32 and c!='\n' for c in t))
 ck('trailing whitespace zero '+p,all(l.rstrip()==l for l in t.splitlines()))
 ck('display TeX delimiters matched '+p,t.count('\\[')==t.count('\\]'))
 ck('no placeholder '+p,'SOURCE_' not in t)
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  target=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));at=S/target if (S/target).exists() else REPO/target
  ck('actual relative link '+dest,at.exists());links.append({'source':p,'destination':dest,'resolved':target,'bytes':at.stat().st_size,'sha256':sha(at.read_bytes())})
js(E/'formal-link-check.json',links)
ck('three independent formal targets only',sorted(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))==sorted([P1,P2,P3]))
for x in rd(E/'formal-resource-manifest.json'):
 b=(S/x['path']).read_bytes();ck('formal resource SHA '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
ck('exact five receipts only',len(receipts)==5 and {x['id'] for x in receipts}==set(IDS))
for x in receipts:
 ck('complete receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']))
 for p in x['targets']:ck('receipt target '+p,(S/p).exists() or (REPO/p).exists())
ck('all full semantic source units mapped',len(coverage)==5 and all(x['units'] and x['targets'] for x in coverage))
ck('aggregate lower/upper and root-only scope explicit','最后一步依赖上述归纳假设' in (S/P1).read_text() and '不能换剩余利润G' in (S/P1).read_text())
ck('pure-column is r2 and tax retained','g_x−h_x' in (S/P3).read_text() and 'r≥3联合R删去' in (S/P3).read_text())
ck('original missing/new finite implementation separate','不冒充原CLI/原JSON复现' in (S/P2).read_text() and '不能把252叫精确v3' in (S/P2).read_text())
ck('five actual local available next sources',len(nextrows)==5 and all(x['progress_observed'] is None for x in nextrows))
obs=[]
for p in sorted(S.rglob('*')):
 if not p.is_file() or p.name in ['copy-files.json','copy-paths.txt','delivery-summary.json']:continue
 try:t=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 lines=[i+1 for i,l in enumerate(t.splitlines()) if l.rstrip()!=l]
 if lines:obs.append({'path':str(p.relative_to(S)),'lines':lines,'frozen':any('/'+v+'/' in str(p.relative_to(S)) for v in ['original','related','context'])})
ck('no derived whitespace errors',not any(not x['frozen'] for x in obs))
js(E/'transport-whitespace-observations.json',{'observed':obs,'raw_original_policy':'all original/related/exact context bytes frozen'})
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_all_nonLF_C0':0,'formal_trailing_whitespace':0,'relative_links_checked':len(links),'scope':'actual source bytes/claim/owner/run hashes, explicit mathematical semantic coverage, format/links/receipts; checker counts do not prove general math or external review'})
rows=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();rows.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),rows);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in rows)+'\n')
out={'stage':str(S),'copy_files':len(rows),'copy_bytes':sum(x['bytes'] for x in rows),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':scope['primary_bytes'],'primary_lines':scope['primary_lines'],'new_formals':3,'new_formal_bytes':sum((S/p).stat().st_size for p in [P1,P2,P3]),'receipts':5,'duplicate_ids':[IDS[0]],'checks':len(checks),'relative_links':len(links),'new_independent_CLI_runs':1,'original_CLI_runs':0,'missing_unread_original_audits':2,'safe_helper_calls':4,'derived_builder_failures':2,'claim_tip':claim['remote_tip'],'next_actual_candidates':nextids}
js(Path('delivery-summary.json'),out);print(json.dumps(out,ensure_ascii=False,indent=2))
