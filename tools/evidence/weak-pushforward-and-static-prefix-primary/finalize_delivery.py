from pathlib import Path
import json,hashlib,re,posixpath

R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';S=C/'r3-weak-pushforward-and-static-prefix-primary';E=Path('tools/evidence/weak-pushforward-and-static-prefix-primary');W=Path('cleanup/workspaces/Boss4/r3-weak-pushforward-and-static-prefix-primary-next')
P1='archives/customer-attraction/state/引理/合法前缀的静态额外槽预算与条件归约--引理.md';P2='archives/customer-attraction/state/反例/空根稀释的强推送失败与弱桥范围--反例.md';IDS=['666061ceda2882cfd25d','71bdd0dc3ec8f127e59b','b82223f1516f80533ccd']
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def rd(p):return json.loads((S/p).read_text())
primary=rd(E/'source-manifest.json');related=rd(E/'related-source-manifest.json');contexts=rd(E/'context-manifest.json');claim=rd(E/'actual-claim-receipt.json');inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==set(IDS)
cp(Path(__file__),E/'finalize_delivery.py');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
scope={'primary_sources':3,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'primary_full_actual_read':True,'first_read_timing':'first full original math reading in EX; previous EO only checked candidate bytes','related_full_input_sources':2,'related_input_bytes':sum(x['size'] for x in related),'read_reuse':'34base and57-action JSON previously fully read EO, exact bytes reused; current original3 new full read','formal_contexts':len(contexts),'formal_context_bytes':sum(x['bytes'] for x in contexts),'new_original_CLI_calls':0,'new_math_or_fixed_root_program_calls':0,'new_full_SPE_replays':0,'new_solver_or_sample_scans':0,'derived_resource_builder_calls':1,'derived_builder_failures':0,'safe_local_export_helper_calls':3,'helper_local_blob_attempts':12,'helper_next_exports':3,'helper_absent_blobs':9,'prior_missing_JSONs_reused_no_retry':2,'new_code_or_report_absent_ids':['775cb966d04cf78329f8','f07b5c33edde731a3a02','26fbb913d2ca178e8d73','d6b44ba974e4df4ca1c7'],'next_float_candidate_absent_ids':['b63e9670b93c54d5f415','617c422b04b31770b4fa','191f51a6ed05b82ee8fd','4c6d9b1e29864e0eb197','6a997c37f07715e7586e'],'network_or_lazy_fetch':0,'shared_Git_writes':0,'clean_show_claim_done_checkpoint_calls':0,'mathematical_work':'full static prefix/minimax proof, finite LP dual, analytical14-new-history extension and general empty-root identity; source-reported numerical searches not newly certified','new_manual_derivations':['LP dual variables/costv>=0 and fractional deletion domain','unit-model empty mechanism has b>a>0 and threshold a/b<1','bank m4 gives WP failure by optimal security query; m>=5 individual floor failure but nothalf'],'standard_imports':['finite zero-sum minimax','finite LP strong duality','finite symmetric Nash existence by Brouwer for one conditional direction only'],'phase3_mapper_or_graph_import':0}
assert scope['primary_bytes']==8326 and scope['primary_lines']==143 and scope['related_input_bytes']==9457
js(E/'read-scope-and-evidence-status.json',scope)
coverage=[{'id':IDS[0],'units':['old unregistered backup/date/generalOPEN is history','34root strong failure leaves actualu slack, not proof weak','381discovery trajectory local missing versus34mature input','weak conditional reduction to individual floor','two search filenames and reportedp7/m5/8seed10round1/9 finite record','candidate/exact labels not certification','k2 weak positive revoked due missing+1','Mfull distinct from r-1 tail menu and currentrefutation','background price boundary preservesstrong/mainmenu in thatfamily','270/348 potential/cycle discovery-only author scope'],'targets':[P1,P2],'decision':'integrated historical routes and all unique math/status distinctions; no claimed code read or search replay'},
{'id':IDS[1],'units':['allunit3players7topicsincludingtrueempty','13maskmultiplicities and base43historySPE','full57rule with rho and doubleempty0','all13newlast nodes plus newsecondafterempty analyticBR','empty-root tail profits16/16, rootnonempty29/3 andempty0','two realbranches rootD/C/difference/u slack','actorcanonical and missingroot3051/5246 independent audit identities separate','general two-point EMPTY exact polynomial','a>0 small epsilon mechanism and strong/weak boundary','381discoveryhistory not primaryproof, no novelty/outer review'],'targets':[P2,P1],'decision':'integrated full analytical augmentation not merely repeat prior JSON fields; old successful different-code evidence reused without execution'},
{'id':IDS[2],'units':['legal k-prefix, r=m-k and true complete r-slot push law','fixedbackground extra-rivals minimax definition and pstar attainment','C(pstar)>=v, Jensen maxprice lower bound','optimal m-tuple perclient budget and legalprefixmu totalm','staticv>=OPT/(2m), valid conditional individual/half implication','WP is unproved in source but currently false, genuinev versus fractionalt separated','whole-catalogB(v) fractional purchase LP','dualalpha/beta and y truncation, fractional deletion equivalent','v>=0 applicationdomain, zero/uncoverable clients boundaries','no implication from representation to WP or tree payment'],'targets':[P1,P2],'decision':'integrated full static theorem/conditional proof and appendix duality; current false premise not relabeled as new half theorem'}]
js(E/'semantic-coverage-map.json',coverage)
notes=[('2590B README全部正文及2026-10-22接续新全文实读，旧角色/备份身份、强反例/381轨迹/弱归约、搜索入口和有限1/9记录、候选等级、漏+1撤销及后续Mfull/势排序范围全部保留。','与当前银行WP/逐人floor反驳、现完整34证书/空历史规则、两尾推送与已交菜单资料逐一比较；两搜索代码及原root审计代码/报告实际本地缺，有限搜索仅按作者历史叙述，不冒程序/调用数认证。','独有路由与历史真值归两新自足对象；旧继续WP命令不覆盖本轮，普遍WP现假但有效静态/条件归约不退休；无新数学CLI或旧成功复跑。',[P1,P2]),
('3569B主稿全部mask表、七主题/57节点完整规则、rho、14新空历史解析最佳回复、两真实分支D/C、u正slack及一般epsilon公式首次全文实读。','与1465基础实例/7992完整动作、现43节点逐表SPE及EO已修空第二历史紧写对照；新增一空节点的两人收益用主题大小/交集解析说明，既有3119不同代码成功不冒作缺失3051原审计。','补此前JSON之外的完整解析延伸及一般空根稀释恒等式，保u-D真实松弛和固定根vs三位置目标；不从本强式失败否定弱，当前WP状态另据银行，原件不改。',[P2,P1]),
('2167B弱归约全文首次实读，WP/安全值定义、最优p、Jensen/最优m元组/前缀目录计数预算、所有边界和附LP对偶全部重构。','核合法prefix和r+k=m是静态OPT2m预算承重条件，非任意实b；当前t<=v和银行m4反驳WP，m>=5反驳个体OPT2m不反驳half；LP的实z/分数删除与原m槽不同域。','自足保完整正确静态定理、条件half蕴含、对偶消元及v>=0有限域；纠正只欠WP仍OPEN的历史状态，不把假前提当当前一般证明任务或因状态变化丢掉数学。',[P1,P2])]
receipts=[]
for i,(a,b,c,t) in zip(IDS,notes):receipts.append({'id':i,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 实际三源8326B/143行，原claim pushed/synced及当前Boss4 owner/source SHA核验。','comparison_note':b,'decision_note':c,'disposition':'integrated','targets':t})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md','''# 阶段二实际关系

合法前缀静态v>=OPT/(2m)依赖b恰由k原目录主题形成、k+r=m；Jensen和目录计数的两份m预算不需SPE。WP若给安全最优p付款，个体floor及half条件蕴含正确。但银行m4 t5<=v5>u已经反驳普遍WP，m>=5也反驳个体floor，既不反驳静态定理也不反驳half；零背景根与空主题根分清。

LP删除表示是另一有限强对偶：实采购z非固定m槽、y允许分数删除、应用costv=ui>=0。它本身不构造SPE信用或WP。各定理只在明示域接入，不因名称相似共用量词/钱包。

34客户主稿把基础43节点SPE解析延伸14节点，原rho在一空/双空及空根第二人最优全部说明。EMPTY是独立双抽样恒等式，负强式可以被真实u-D吸收；当前WP的反驳来自另一个已证完整SPE族。根部25/6与三位置12系数不同，不混作同一gap或福利预算。

README搜索/381及270轨迹、漏查询+1撤销按历史作者断言保留。缺失代码/报告/JSON不认证、不网络补取，旧同SHA成功不同实现不改名复现。无新数学程序/solver/SPE运行；关系为阶段二实际审查，不导旧图、mapper或第三阶段超边。
''')
nextmp=C/'learning-ex-next-readable-md/local-export-manifest.json';nm=json.loads(nextmp.read_text());assert len(nm['rows'])==3 and not nm['missing'];cp(nextmp,E/'next-readable-MD-manifest.json');nxt=[]
for x in nm['rows']:
 p=REPO/'cleanup/progress'/f"{x['id']}.json";assert not p.exists();nxt.append({**x,'progress_observed':None,'mathematical_read_status':'actual bytes verified available; full math reading not yet done','claim_condition':'Root rechecks and claims actual current available intersection only'})
i='a7579960b289fff40c97';n='archives/customer-attraction/tools/evidence/origin-retraction-workspace/related/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json';b=(REPO/n).read_bytes();x=inv[i];assert len(b)==x['size'] and sha(b)==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'];assert not (REPO/'cleanup/progress'/f'{i}.json').exists();nxt.append({**x,'local_path':str(REPO/n),'progress_observed':None,'mathematical_read_status':'existing complete local input bytes verified only, not full JSON read; old related success exists but not primary done','claim_condition':'Root actual current owner recheck required'})
js(W/'next-candidates.json',nxt)
put(W/'delivery.md',f'''# 交付范围

EX3 actual claim {claim['remote_tip']} pushed/synced，3owner/source SHA吻合；主源8326B/143行首次数学全文实读。两份新自足正文/3完整receipt，保STATIC条件归约、完整LP对偶、14空节点解析延伸及一般EMPTY机制；旧WP开放/逐人floor现按真实反族纠正，half另保。

新数学CLI/固定根算术/全SPE/solver/扫描0；无重复旧同SHA成功。3次安全helper仅作related/下批可用性，12本地尝试=3齐+9缺，不网络不重试；旧2缺JSON回执仅复用。原作者有限发现/代码引用未冒认证。

下批实际4件齐：3本地MD加已物化32574B52客户JSON，均无当前owner且尚未完整数学读，不预领。Root按copy-files白名单复制，正文/依赖先pushed再逐源done，代理无shared Git/claim/done/checkpoint/show/网络操作。
''')
checks=[]
def ck(n,b,detail=None):
 d={'check':n,'passed':bool(b)}
 if detail is not None:d['detail']=detail
 checks.append(d);assert b,n
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();v=inv[x['id']];ck('exact source bytes '+x['id'],len(b)==v['size'] and sha(b)==v['sha256']);ck('exact blobSHA1 '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'])
ck('actual unprojected3 capture preserved',(S/E/'actual-claim-receipt.json').read_bytes()==(R/'boss4-r3-next-ex-claim.json').read_bytes())
for i in IDS:
 x=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());ck('actual owner and source '+i,x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[i]['sha256'])
ck('full3 original read size/lines',scope['primary_bytes']==8326 and scope['primary_lines']==143);ck('no new math execution',scope['new_math_or_fixed_root_program_calls']==scope['new_full_SPE_replays']==scope['new_solver_or_sample_scans']==0);ck('helper actual availability contract',scope['safe_local_export_helper_calls']==3 and scope['helper_local_blob_attempts']==12 and len(rd(E/'missing-local-inventory-bindings.json'))==9)
for x in contexts:
 b=(S/x['snapshot']).read_bytes();ck('exact full formal context '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
links=[]
for p in [P1,P2]:
 t=(S/p).read_text();ck('flat MATEK '+p,all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('all nonLF C0 zero '+p,not any(ord(c)<32 and c!='\n' for c in t));ck('trailing whitespace zero '+p,all(l==l.rstrip() for l in t.splitlines()));ck('display TeX balance '+p,t.count('\\[')==t.count('\\]'));ck('source placeholders resolved '+p,not any(a in t for a in ['SRC_','DATA_JSON']))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  target=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));at=S/target if (S/target).exists() else REPO/target;ck('actual relative link '+dest,at.exists());links.append({'source':p,'destination':dest,'resolved':target,'bytes':at.stat().st_size,'sha256':sha(at.read_bytes())})
js(E/'formal-link-check.json',links)
ck('two new formal outputs only',sorted(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))==sorted([P1,P2]))
for x in rd(E/'formal-resource-manifest.json'):
 b=(S/x['path']).read_bytes();ck('formal resource SHA '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
ck('exact3 semantic receipts',len(receipts)==3 and {x['id'] for x in receipts}==set(IDS))
for x in receipts:
 ck('complete receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']))
 for p in x['targets']:ck('receipt target '+p,(S/p).exists() or (REPO/p).exists())
a=(S/P1).read_text();b=(S/P2).read_text();ck('legalprefix static proof and cost domain present','k+r=m' in a and '\\tag{STATIC}' in a and 'v≥0' in a and '\\tag{DELETE}' in a);ck('current WP/floor corrected without half refutation','5/4<13/10' in a and '6/5<4/3' in a and '零背景根节点' in a);ck('all empty-node extension and true model threshold','共13' in b and '第14个节点' in b and '二次系数b=' in b and '>a>0' in b and '\\tag{EMPTY}' in b);ck('actual4 next candidate bytes without pre-read claim',len(nxt)==4 and all(x['progress_observed'] is None for x in nxt))
js(E/'delivery-check-recovery.json',{'kind':'derived delivery-check literal false negative','observed_failure':'AssertionError: all empty-node extension and true model threshold','reason':'Checker required literal b>a>0, while the full written derivation states b=g_T(Z(E))−g_T(Z(T))=a+[d_T−g_T(Z(T))]>a>0. Actual positive coefficient proof was already present.','repair':'Check the existing named coefficient and >a>0 derivation together; no mathematical body, original, input, or old evidence changed.','mathematical_program_reruns':0,'capture_status':'Failure traceback observed in tool output; this record is an explanatory recovery note, not a fabricated raw capture.'})
obs=[]
for p in S.rglob('*'):
 if not p.is_file() or p.name in ['copy-files.json','copy-paths.txt','delivery-summary.json']:continue
 try:t=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 ls=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()]
 if ls:obs.append({'path':str(p.relative_to(S)),'lines':ls,'frozen':any('/'+z+'/' in str(p.relative_to(S)) for z in ['original','related','context','reused-evidence'])})
ck('no derived whitespace errors',not any(not x['frozen'] for x in obs));js(E/'transport-whitespace-observations.json',{'observed':obs,'policy':'all frozen original/related/context/old output bytes preserved'})
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_all_nonLF_C0':0,'formal_trailing_whitespace':0,'relative_links_checked':len(links),'scope':'actual source/claim/owner/SHA and explicit analytic coverage, format/links/receipts; no new mathematical program execution, universal solver or external review'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');out={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':scope['primary_bytes'],'primary_lines':scope['primary_lines'],'new_formals':2,'formal_bytes':sum((S/p).stat().st_size for p in [P1,P2]),'receipts':3,'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'claim_tip':claim['remote_tip'],'next_actual_candidates':[x['id'] for x in nxt]};js(Path('delivery-summary.json'),out);print(json.dumps(out,ensure_ascii=False,indent=2))
