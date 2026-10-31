from pathlib import Path
import json,hashlib,re,posixpath

R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';S=C/'r3-two-tail-pushforward-and-full-menu-boundaries-primary';E=Path('tools/evidence/two-tail-pushforward-and-full-menu-boundaries-primary');W=Path('cleanup/workspaces/Boss4/r3-two-tail-pushforward-and-full-menu-boundaries-primary-next')
P1='archives/customer-attraction/state/引理/末位真实回复推送的锐曲率与双分支式--引理.md';P2='archives/customer-attraction/state/反例/后继边际价格付款的两类尺度障碍--反例.md';P3='archives/customer-attraction/state/资料/完整根菜单的联合势义务与排序边界--资料.md'
OLD1='archives/customer-attraction/state/引理/完整槽插入税与跨角色价格恒等式--引理.md';OLD2='archives/customer-attraction/state/引理/两名剩余完整终局菜单的纯列封顶--引理.md'
IDS=['c7681bcaecb3e63137ff','7fd268a01ce3f10dcb2a','6c84043505685faee8ec','68ed7412ef2da880f80f','5ea43c826b2651fe9de7']
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def rd(p):return json.loads((S/p).read_text())
primary=rd(E/'source-manifest.json');related=rd(E/'related-source-manifest.json');ctx=rd(E/'context-manifest.json');claim=rd(E/'actual-claim-receipt.json');run=rd(E/'runs/new-branch-arithmetic-001/run-metadata.json');report=rd(E/'runs/new-branch-arithmetic-001/report.json');missing=rd(E/'missing-unread-inventory.json')
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};assert set(claim['ids'])==set(IDS) and claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced'
cp(Path(__file__),E/'finalize_delivery.py');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
reuse=[]
for x in primary:
 old=C/'r3-root-repair-and-stationary-interfaces-primary/tools/evidence/root-repair-and-stationary-interfaces-primary/related'/x['id']/x['path'];assert old.read_bytes()==(S/x['preserved_path']).read_bytes();reuse.append({'id':x['id'],'sha256':x['sha256'],'prior_full_read_role':'DY related only, not prior primary completion','same_original_bytes':True,'old_path':str(old),'present_path':x['preserved_path'],'reading_note':'honest complete previous read reused and pertinent passages checked; no fictitious first reading'})
js(E/'prior-full-related-read-reuse.json',reuse)
scope={'primary_sources':5,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'primary_full_actual_read':True,'prior_related_read_reused_ids':IDS,'related_sources':3,'related_bytes':sum(x['size'] for x in related),'related_full_actual_read':True,'formal_contexts':len(ctx),'formal_context_bytes':sum(x['bytes'] for x in ctx),'safe_local_export_helper_calls':1,'local_blob_attempts':3,'local_blob_exports':1,'missing_unread_reports':2,'network_or_lazy_fetch':0,'new_original_CLI_calls':0,'new_full_history_SPE_replays':0,'new_solver_calls':0,'new_game_or_sample_scans':0,'new_fixed_branch_arithmetic_CLI_calls':1,'new_branch_arithmetic_body_executions':1,'branch_inputs':2,'branches_evaluated':13,'derived_builder_calls':1,'derived_builder_failures':0,'orchestration_parse_failures_before_execution':1,'effect_of_parse_failure':'one edit wrapper did not execute, then corrected; no file mutation or mathematical call occurred before retry','shared_Git_writes':0,'clean_show_claim_done_checkpoint_calls':0,'phase3_graph_or_mapper':0,'reused_SPE_evidence':'348 input SHA bound to prior origin-retraction successful full43/258 audit;34 input SHA bound to prior parent independent57/342 audit; neither repeated','new_math_scope':'once fixed-root K/Phi/delta/R and rational parameter specialization; does not certify missing791 or273B report; universal r2 proofs analytic','minimality':'five clients minimal only in explicit h/L family, ten-client source point retained; s13 threshold only within singleton family; no global minimality claim'}
assert scope['primary_bytes']==23339 and scope['primary_lines']==381 and scope['related_bytes']==20418
js(E/'read-scope-and-evidence-status.json',scope)
coverage=[
 {'id':IDS[0],'units':['arbitraryr complete COL with Y excluding current root','joint R definition not individual best-response sign','r2 exact BR and g/h overlap tax','max naked reply pure column and strict scalar acyclicity','actual348 high-insertion cycle versus not menu failure','mixed PAY fixedp/Q equivalence, samep drift cancellation and real e slack','old formula audit stated but missing273 report not read','actual historical independent role/review versus present evidence'],'targets':[OLD2,P3],'decision':'full integrated, old r2 detailed lemma precisely reused; new ledger/cycle/state resource retains remaining unique units'},
 {'id':IDS[1],'units':['allh>=0,L>=1 actual legal-prefix domain and two-tail full SPE','complete matrix preserving root and background','pureMETA p, tail/full independent query prices','ratios2/(h+1),4/(h+1), strict thresholds h2/h4','fixedalpha no-go not weaker max-price bridge failure','old h2L2 ten-client worked point and original minimum-wording error','same-family h2L1 five-unit specialization, no global minimality'],'targets':[P2,OLD1],'decision':'integrated analytic boundary and precisely bounded source-word correction; raw unchanged'},
 {'id':IDS[2],'units':['real b>=0/actualinteger prefix distinction and no current-root optimality premise','D/C independence and p/q/j membership expansion','whole-theme BR totalL>=0 not per-customer signs','exact sharp curvature decomposition','deterministic two-branch PAIR identity and membership proof','one-client arbitraryb,t equality plus independent-review full equality conditions','current-u implication only if current optimal','34+empty 57history342nonself strong failure versus actual positive u slack','larger distinct input unread and old weak/general status corrected'],'targets':[P1,P3],'decision':'integrated full proof/equality/quantifier supplement; old source-code audit not fabricated'},
 {'id':IDS[3],'units':['later2026-10-25 correction distinct from old body OPEN','fullroot minmax/static embedding and sufficient half chain','lowMETA existence sufficient but logically stronger, abstract2x2 not realized-CAG claim','r2 global pair-potential pure defense','reported791 strict potential descent, local report missing, not newly certified','348 true high-insertion two-cycle and good columns0/3','old8person DAG pending not retroactively certified','three-singleton nonSPE pseudo-menu with actual second deviation','root/last/floor/META template insufficiency','samep/tail average price debt not general funding, Mpath exact domain needed'],'targets':[P3,P2],'decision':'integrated complete historical/resource distinction; general individual menu refuted not left current OPEN'},
 {'id':IDS[4],'units':['emptybackground2players disjoint A2 and s singleton family','fullstrategy lastalwaysA, all root actions tied u1','all t prices D/C, TailPrice exact gap','t1/3,s13 15clients14labels gap1/351','p not META, maxM/strongpush/half all maintained','all-family parameter threshold12 via exact square factor','only family minimality, no global minimum/extra general theorem'],'targets':[P2,P1],'decision':'integrated all-parameter analytic counterfamily and preserved target distinctions'},
]
js(E/'semantic-coverage-map.json',coverage)
notes=[
 ('5748B全文已在DY related实读，本批核同SHA诚实复用；全部COL/两人最大裸回复/正税/无环标量/二环边界/混合PAY/审计范围各节完整理解。','与已交DY纯列引理、5009B独审、完整348 JSON及现来源回撤成功输入绑定逐项比较；旧fullSPE核验不替附带K/Phi认证，故仅新增根算术。','r2全部细节精确复用已有引理，其余混合义务与二环/联合R正值归新资料；273B原审计摘要本地缺，未冒读/重跑；多后继不套R<=0。',[OLD2,P3]),
 ('2057B合法前缀全文实读，同SHA旧related读取复用；参数/完整两人策略、实际原前缀可达、K/Nash、tail/full两种比率、严格阈值和未反驳主式全部理解。','与6504B已交全人数显式完整SPE及空背景反族比较；原L>=1而称h2L2十客户最小不成立，同族h2L1五客户直接满足既有全历史证明，正确范围明确。','独有两尾特化、旧十客户展示及本族最小措辞勘误自足归新两类尺度反例；不泛称全模型最小或原half失败，原字节不改。',[P2,OLD1]),
 ('6035B任意p完整推送全文及独立稿5009B全部读，诚实复用既有related阅读；包括二元展开、总BR、非负曲率、PAIR、实背景、锐族和三人失败/松弛边界。','独审全等号条件保留且不再冒称本次盲审；原7992B/57动作完整读，核同SHA既有342非自身成功，不复跑；固定根算术确认D−C−7/120、u−C1037/120。','新增自足PUSH/PAIR与全部等号条件，保当前最优性非前提、共同目录/独立性承重及r>=3停界；较大不同输入只保原引用未冒读。',[P1,P3]),
 ('6262B全部含2026-10-25更正头、旧2026-10-22正文，菜单minimax/META/纯列/势与环失败/非SPE模板/后续债务逐节全文理解。','与当前银行根Mfull反例、两人纯列/锐推送、完整348数据及既有成功审计、791缺失独审回执对照；抽象2x2矩阵不称真实CAG实例，八人候选仍仅原历史未核。','新资料自足保所有独有逻辑例/必要条件及历史真值修正；791原数值明确作者有限断言，348新正R不扩大纯列/混合失败；不把Mpath名字当现状认证。',[P3,P2]),
 ('3237B空背景TailPrice反族全文已读并同SHA复用；全部s/t策略、价格、零根slack、s13点、非META身份及本族阈值完整理解。','与合法实际过去META例、任意p两尾PUSH及较弱max-price式比较；用3(1−t)^2−12t(1−2t)=3(1−3t)^2完整证明本族阈值，数值代入不作搜索。','自足保全参数解析反例及真正被否定的加强式；C<=D、Mfull和half在此例保持，不用任意p反例否定META限定推送或宣称全模型最小。',[P2,P1]),
]
receipts=[]
for i,(a,b,c,t) in zip(IDS,notes):receipts.append({'id':i,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 实际五源23339B/381行，原claim pushed/synced与owner/source SHA核验。','comparison_note':b,'decision_note':c,'disposition':'integrated','targets':t})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md','''# 实际阶段二关系检查

PUSH/PAIR只靠一位真实末位BR并允许任意实背景，不要求当前首位最优；得到u封顶时才用当前SPE。全等号与单客户锐族是解析结论，不由有限样本证明。与旧最大裸回复纯列均为两尾正确接口，但一个先选固定列、一个按任意p同分布推送，不能互换抽样。

两类TailPrice反族分别是非零实际过去的纯META p与空背景的非META p，均保弱max-price、全p两尾强推送及half。旧十客户最小措辞被同域L1五客户纠正，仅该显式家族最小；singleton阈值12也仅族内。实际模型/量词不同不合并成一个反例输入。

完整COL和PAY保存同一真实菜单的R/正税/漂移/slack；Mfull=minmax、低META及静态安全值可行域不同。当前普遍个体Mfull已被银行反族否定，旧条件half蕴含仍成立。348同SHA旧全SPE成功只复用其已核字段；本批新一次根算术核K/Phi并给联合R12/税6，未复跑树。好列0/3使二环不否定该例菜单。791/273原报告缺失保作者断言，不回填旧八人候选已认证。

根IC/末位BR/floor/META的三singleton伪菜单明确非SPE，只作为模板不足。原审查先验、当前读后推导、旧运行和本次算术分开；无外审/新颖性。未导旧图、mapper或第三阶段超边，不强制造连通。
''')
nextids=['38f33a2ab903eb816fc8','23b69044426c185f1653','f218c3c894b4635ecca2'];nxt=[]
for i in nextids:
 p=REPO/'cleanup/progress'/f'{i}.json';assert not p.exists(),('candidate now owned',i);x=next(x for x in related if x['id']==i);nxt.append({**inv[i],'actual_local_input':x['local_path'],'progress_observed':None,'actual_read_scope':'full EG related read including all JSON fields/actions; not primary done','claim_condition':'Root must recheck actual available/owner; no automatic next claim'})
js(W/'next-candidates.json',nxt)
put(W/'delivery.md',f'''# 交付范围

EG5 actual claim {claim['remote_tip']} pushed/synced，实际五owner及source SHA吻合；主源23339B/381行。新增3份自足正文、5条integrated receipts，复用DM/DY两正式页而不覆写。正文/依赖先正常推送，再逐源done。

1次新固定根算术0.069458058秒exit0/stderr空；旧348/34输入同SHA全SPE成功不复跑，原CLI/solver/新样本扫描0。新R12税6/34差值/参数代入单独保存。1次安全helper读3对象，仅5009B独审齐，791独审JSON与273B摘要缺，缺失原回执和inventory完整保存，无网络或重试。

原十客户最小措辞按同域L1五客户纠正，只认证本族、不抹原展示或原件；空背景singleton阈值12解析保留。下一3实际本地齐且全文related读过，尚未预领；缺失两件不冒充齐件候选。Root按copy-files白名单精确复制，代理无共享Git/claim/done/checkpoint/show/网络操作。
''')
checks=[]
def ck(n,b,detail=None):
 d={'check':n,'passed':bool(b)}
 if detail is not None:d['detail']=detail
 checks.append(d);assert b,n
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();i=inv[x['id']];ck('exact inventory source '+x['id'],len(b)==i['size'] and sha(b)==i['sha256']);ck('exact blobSHA1 '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==i['blob'])
ck('unprojected actual5 capture byte preserved',(S/E/'actual-claim-receipt.json').read_bytes()==(R/'boss4-r3-next-eg-claim.json').read_bytes())
for x in primary:
 p=json.loads((REPO/'cleanup/progress'/f"{x['id']}.json").read_text());ck('actual owner and source '+x['id'],p['owner']=='Boss4' and p['disposition']=='in-progress' and p['source_sha256']==x['sha256'])
ck('full5 primary and honest previous related reuse',scope['primary_bytes']==23339 and scope['primary_lines']==381 and len(reuse)==5);ck('actual3 related all fields full read',len(related)==3 and scope['related_bytes']==20418);ck('missing2 exact not invented',len(missing)==2 and all(not x['read'] and not x['done'] for x in missing))
for x in ctx:
 b=(S/x['snapshot']).read_bytes();ck('exact formal context '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
ck('new root arithmetic code bound SHA',sha((S/E/'calculate-menu-diagnostics.py').read_bytes())==run['code_sha256']);ck('one arithmetic call no full SPE replay',run['invocations']==1 and run['verification_body_executions']==1 and run['old_full_history_replays']==0 and len(list((S/E/'runs').iterdir()))==1);ck('new arithmetic actual success',run['exit_code']==0 and run['assertions_enabled'] and (S/E/'runs/new-branch-arithmetic-001/stderr.txt').stat().st_size==0)
ck('348 positiveR and tax6 retained',all(x['joint_R']=='12' and x['intersection_tax']=='6' for x in report['cycle348']['two_edges']));ck('34 strong versus actual slack retained',report['empty34']['D_minus_C']=='-7/120' and report['empty34']['u_minus_C']=='1037/120');ck('smaller same-family and singleton scope retained',report['smaller_same_family_specialization']['unit_clients']==5 and report['empty_tailprice']['violation']=='1/351')
links=[]
for p in [P1,P2,P3]:
 t=(S/p).read_text();ck('flat MATEK '+p,all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('all nonLF C0 zero '+p,not any(ord(c)<32 and c!='\n' for c in t));ck('trailing whitespace zero '+p,all(l.rstrip()==l for l in t.splitlines()));ck('TeX display balance '+p,t.count('\\[')==t.count('\\]'));ck('source placeholders resolved '+p,not any(v in t for v in ['SRC_','EVID']))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  target=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));at=S/target if (S/target).exists() else REPO/target;ck('actual relative link '+dest,at.exists());links.append({'source':p,'destination':dest,'resolved':target,'bytes':at.stat().st_size,'sha256':sha(at.read_bytes())})
js(E/'formal-link-check.json',links)
ck('exact3 new formal objects',sorted(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))==sorted([P1,P2,P3]))
for x in rd(E/'formal-resource-manifest.json'):
 b=(S/x['path']).read_bytes();ck('formal resource binding '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
ck('exact five semantic receipts',len(receipts)==5 and {x['id'] for x in receipts}==set(IDS))
for x in receipts:
 ck('complete receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']))
 for p in x['targets']:ck('receipt target exists '+p,(S/p).exists() or (REPO/p).exists())
ck('all unique semantic units mapped',len(coverage)==5 and all(x['units'] and x['targets'] for x in coverage));ck('analytic PAIR/equality statements present','j_x=p_x' in (S/P1).read_text() and '\\tag{PAIR}' in (S/P1).read_text());ck('family lower threshold and no global minimum','3(1-3t)^2' in (S/P2).read_text() and '不声称全模型最小' in (S/P2).read_text());ck('author-only791 not certified','原稿明确有限断言' in (S/P3).read_text());ck('three actual available next candidates',len(nxt)==3 and all(x['progress_observed'] is None for x in nxt))
obs=[]
for p in S.rglob('*'):
 if not p.is_file() or p.name in ['copy-files.json','copy-paths.txt','delivery-summary.json']:continue
 try:t=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 lines=[i+1 for i,l in enumerate(t.splitlines()) if l.rstrip()!=l]
 if lines:obs.append({'path':str(p.relative_to(S)),'lines':lines,'frozen':any('/'+v+'/' in str(p.relative_to(S)) for v in ['original','related','context','reused-old-run-records'])})
ck('no derived whitespace errors',not any(not x['frozen'] for x in obs));js(E/'transport-whitespace-observations.json',{'observed':obs,'policy':'exact original/context/old-run bytes frozen; derived errors forbidden'})
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_all_nonLF_C0':0,'formal_trailing_whitespace':0,'relative_links_checked':len(links),'scope':'actual source/claim/owner/run SHA, explicit analytic semantic coverage, formatting/links/receipts; finite arithmetic and counters do not prove universal results or external review'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');out={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':scope['primary_bytes'],'primary_lines':scope['primary_lines'],'new_formals':3,'new_formal_bytes':sum((S/p).stat().st_size for p in [P1,P2,P3]),'semantic_receipts':5,'checks':len(checks),'relative_links':len(links),'new_fixed_branch_arithmetic_calls':1,'original_CLI_calls':0,'full_SPE_replays':0,'missing_unread_reports':2,'claim_tip':claim['remote_tip'],'next_actual_candidates':nextids};js(Path('delivery-summary.json'),out);print(json.dumps(out,ensure_ascii=False,indent=2))
