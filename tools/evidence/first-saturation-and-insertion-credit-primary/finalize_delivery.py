from pathlib import Path
import hashlib,json,re,posixpath

ROOT=Path('/workspace/scratch/37f0f9248cfc')
REPO=ROOT/'boss4-research';CACHE=ROOT/'boss4-next-cache'
S=CACHE/'r3-first-saturation-and-insertion-credit-primary'
E=Path('tools/evidence/first-saturation-and-insertion-credit-primary')
W=Path('cleanup/workspaces/Boss4/r3-first-saturation-and-insertion-credit-primary-next')
P1='archives/customer-attraction/state/引理/完整槽插入税与跨角色价格恒等式--引理.md'
P2='archives/customer-attraction/state/资料/首次饱和与独立审查的版本路由--资料.md'
F='archives/customer-attraction/state/资料/首次饱和前沿的审查层次与共同付款边界--资料.md'
T='archives/customer-attraction/state/引理/整数完整负载的三八源去相关界--引理.md'
M='archives/customer-attraction/state/候选/最优并集税与平均真实菜单的付款接口--候选.md'
IDS=['37817148989a4881cf37','9782838c9e2bbf41d23b','37b0cc25eda54afa70b8','a11c622290a703a0f463','3d12877308be29ef502c']
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def copy(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def read(p):return json.loads((S/p).read_text())
primary=read(E/'source-manifest.json');related=read(E/'related-source-manifest.json');contexts=read(E/'context-manifest.json')
inv={d['id']:d for d in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
claim=read(E/'actual-claim-receipt.json')
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==set(IDS)
assert (S/E/'actual-claim-receipt.json').read_bytes()==(ROOT/'boss4-r3-next-dm-claim.json').read_bytes()
copy(CACHE/'build_dm_resources.py',E/'build_resources.py')
copy(Path(__file__),E/'finalize_delivery.py')

coverage=[
 {'id':IDS[0],'prior_read':'DD related full read; identical bytes reused, no old primary completion asserted','units':['source/net same cancellation, owner and wallet','all-client complete-leaf query r and actual-prefix reset','uniform whole-row theta and zero-denominator handling','finite conservation A+B and exact FRONTIER','source-excluded first HIT and fixed J','random legal owner cut, joint-law option','financial COV-STOP versus no unweighted domination','mass coverage/MISS and explicit price conversion','owner-slot lottery, role separation and unproved row capacity','reset prevents tax telescoping, not method impossibility'],'destinations':[F,P2],'decision':'duplicate: all unique mathematical content already explicitly preserved by DD formal F; historical version/receipt routing now preserved by P2'},
 {'id':IDS[1],'prior_read':'DD related full read and full independent algebra already preserved','units':['finite integer a/n zero convention','K pair and V pair identities','all equal, zero, difference1 and difference>=2 cases','auxiliary real a extension with integer n retained','fixed m>=2 sharp limit; no SPE sharpness inference','sqrt3 real-load failure','diagonal negative remainder and two-state equality','historical independent proof method versus present reading/outer review'],'destinations':[T,P2],'decision':'duplicate: existing self-contained theorem preserves complete proof and all independent additions'},
 {'id':IDS[2],'prior_read':'DD related full read; prior target used only part, now complete primary disposition','units':['arbitrary legal integer prefix and r>=1 complete legal slots','q full marginal independent requery versus same-column query','INS proof with positive Gamma and exact zero condition','LOW general lower bound, not upper cap','real full-history all-m example and fixed-r alpha ratio','all-role sum r(T-Gamma), not each player subgame value','root/future identity and distinction from full source tax','stationary existence, full/tail kernels and r1 case','stationary theme equality is not reward balance or META law','revealed histories conditional zero versus between-history covariance'],'destinations':[P1,P2,M],'decision':'integrated: new complete static/role/stationary body expands earlier partial use; every unique source semantic unit retained'},
 {'id':IDS[3],'prior_read':'new complete 1005B read','units':['general all-m half OPEN as historical route','source already prepaid; captured actual-prefix reset requires same wallet','old no-review text compared with actual stored limited-scope review','future whole continuation coverage/profit payment, not renamed scalar tax','no new general theorem or fixed-m finite strengthening asserted'],'destinations':[P2,F],'decision':'integrated: standalone route/version/current-use resource plus existing complete construction'},
 {'id':IDS[4],'prior_read':'new complete 925B read','units':['general independent research workspace, not active cleaner role','root-only exact candidate and finite cone versus theorem','three8 independent algebra versus real SPE funds','current integer extra-one failure by Jensen, not t=v identification','fixed two-tail arbitrary-prefix theorem versus general FREE-ROOT','next cross-branch payment or mathematical review, historical route preferences not commands'],'destinations':[P2,T],'decision':'integrated: historical README remains raw; accurate present route and distinct mathematical levels made self-contained'},
]
js(E/'semantic-coverage-map.json',coverage)
obligations=[
 {'name':'complete r slots and integer legal prefix','where':P1,'manual_result':'kept including r1, repeats, empty/zero and positive query denominators'},
 {'name':'INS identity signs','where':P1,'manual_result':'same-column price Ubar-T, cross-column difference positive Gamma'},
 {'name':'background profit versus welfare','where':P1,'manual_result':'r Ubar is only remaining-player profit when b nonzero'},
 {'name':'LOW direction','where':P1,'manual_result':'max query lower bound only, no inferred cap'},
 {'name':'all-history diagnostic strategy','where':P1,'manual_result':'B-seen, A-only nonlast and last tie cases proved; W=OPT'},
 {'name':'fixed r no positive alpha','where':P1,'manual_result':'full2r/(m-1), tail2(r-1)/(m-1), thresholds preserved'},
 {'name':'diagnostic is not strong-push or half failure','where':P1,'manual_result':'all row distributions C<=L<=D, Mfull=L<u'},
 {'name':'role total identity','where':P1,'manual_result':'unconditional full-column marginal C_j not true node value'},
 {'name':'root future excludes root','where':P1,'manual_result':'n=a+k, distinct t_x and old complete source tax retained'},
 {'name':'stationary existence','where':P1,'manual_result':'finite Cesaro/compactness proof; full/tail exact relation and r1 separate'},
 {'name':'stationary law versus META','where':P1,'manual_result':'two existence statements not spliced into one law'},
 {'name':'between-history covariance','where':P1,'manual_result':'all conditional zeros do not erase covariance of conditional means'},
 {'name':'frontier semantics','where':P2,'manual_result':'same cancellation/wallet, B-E-U=OPT-2W equivalence kept; no incoming payment'},
 {'name':'stored review range','where':P2,'manual_result':'current r-definition already repaired, later mass/ownerlottery not falsely certified'},
 {'name':'source tax versus three8','where':P2,'manual_result':'complete INT keeps negative T_src; exact example shows neither complete bound dominates'},
 {'name':'root-only domain and robust inequality','where':P2,'manual_result':'all positive-depth full SPE, arbitrary root; menu equivalence only exact rewrite'},
 {'name':'existing repair conditional for proved m','where':P2,'manual_result':'half deficit after s=Delta equals old deficit-3Delta; no new six-player result'},
 {'name':'FREE-ROOT necessary empty-root case','where':P2,'manual_result':'r+1 comparison slot; tight all-A family and stronger nonempty-prefix version separate'},
 {'name':'restricted cone evidence','where':P2,'manual_result':'source author finite7/4 reported, not independently replayed or universalized'},
 {'name':'integer extra-one current correction','where':P2,'manual_result':'t<=v from Jensen; m4 4/3<19/14<=v5, polynomial positive for all m>=4'},
 {'name':'aggregate W bridge not refuted','where':P2,'manual_result':'bank W=2m and v_m<=2; individual failure not aggregate failure'},
 {'name':'stationary different contracts','where':P2,'manual_result':'fixed fractional mean, full random columns, tail static cap and reward inequality distinct'},
 {'name':'finite source boundary no code certification','where':P2,'manual_result':'1274-client source claim retained but unread audit/program JSON not certified'},
]
js(E/'analytic-obligations.json',{'method':'actual manual mathematical reconstruction/comparison; these entries are explanatory audit statements, not machine proof','obligations':obligations})
scope={'primary_sources':5,'primary_bytes':sum(r['size'] for r in primary),'primary_lines':sum(r['lines'] for r in primary),'full_actual_read':True,'prior_full_related_read_reused_ids':IDS[:3],'new_primary_completion_of_reused_ids':True,'related_sources':5,'related_bytes':sum(r['size'] for r in related),'related_full_actual_read':True,'formal_contexts':len(contexts),'formal_context_bytes':sum(r['bytes'] for r in contexts),'safe_local_export_helper_calls':3,'helper_local_git_cat_file_blob_reads':10,'direct_Git_commands_outside_helper':0,'shared_Git_writes':0,'network_or_lazy_fetch':0,'clean_show_calls':0,'new_original_mathematical_CLI_calls':0,'new_strategy_replays':0,'new_finite_scans':0,'related_audit_code_or_report_unread':['audit_stationary_extra_fractional.py','stationary_extra_fractional_audit.json','root-only finite cone program and input not replayed'],'old_same_SHA_runs_not_repeated':'Existing formal context records retained as historical evidence; not counted as new DM executions','mathematical_work':'complete analytic reconstruction; one explicitly identified conditional reuse of existing root repair and existing half theorem, not new universal payment','external_sources':'No external paper/network retrieval; finite Markov stationarity proved here from Cesaro averages','phase3':'No mapper/old graph/forced edge import'}
assert scope['primary_bytes']==24793 and scope['primary_lines']==488 and scope['related_bytes']==20908
js(E/'read-scope-and-evidence-status.json',scope)
notes=[
 ('11507B全八节全文，SOURCE-NET同一钱包、整行接纳、有限守恒/HIT、随机cut、COV-STOP、质量law、owner槽lottery及税势未采用原因完整理解；DD related同SHA全文实读精确复用，非此前primary done。','完整比较已交首次饱和8916B审查对象、当前全客户r定义、质量/owner补充；这些后加内容未因stored review存在而获当时通过。','已有自足首次饱和正文覆盖全部独有数学，按精确语义去向duplicate；本次原件与版本路由另保存，不覆写或再发已吸收定义修正。','duplicate',[F,P2]),
 ('3966B全部独立K成对证明、整数差分类、辅助实a扩展、固定m>=2极限锐族、sqrt3实负载边界及对角严格余项全文读；此前DD相关全文实读和同SHA绑定准确复用。','与3869B原三八证明及已交完整引理逐项核；独审历史先验不冒充本次盲证，3/8系数与保负源税的完整INT无统一强弱。','所有独有审查扩展已在既有完整引理自足保存，故duplicate而不新立同义数学；保非SPE锐性、整数域与未付共同预算。','duplicate',[T,P2]),
 ('7390B全文全部量词/对象/INS/LOW/诊断/ROLE/ROOT/STAT/已揭示历史段落完整实读，任意合法整数过去、完整r槽及零负载约定逐式重构；不把此前DD只作相关读取当作主源已done。','完整比较6504B全人数真实SPE重构、既有平均菜单/源税/三八及平稳成员收益反例；源到完整槽与尾槽核平稳集合、角色收益与META分布严格区分。','新增完整插入税自足引理，保全此前仅部分使用以外的角色总账、无正统一系数真实前缀例和平稳/跨历史缺口；LOW不升级价格上界，未证明一般付款。','integrated',[P1,P2]),
 ('1005B tree_credit README全文，来源日期/一般全人数身份、源已预付、captured重置、未付incoming、旧未审查断言与下一真实完整后继付款用途全部读。','比较11507B主稿、8916B实际stored review和现完整SOURCE-NET/HIT/首饱和对象；旧无独审不当现缺源，stored review也不扩到后加质量/ownerlottery。','独有路由和历史状态归入新资料页，核心数学精确去重到已有完整首饱和对象；旧角色/路线偏好不覆盖本轮cleaner指令。','integrated',[P2,F]),
 ('925B independent README全文，一般研究身份、root-only检查点、三八独审、有限锥/一般证明边界和后续跨枝付款/独立审查用途全部读。','相关root-only4419B、整数安全值4830B/1192B与当前分数定义/extra-one问题/银行反族/任意背景两尾定理完整比较；Jensen t<=v使原整数extra-one OPEN也确实过时。','新版本路由自足保候选与有限断言、真实状态更新及已证人数/两尾边界；不将个体extra-one失败扩成aggregate W桥或FREE-ROOT否定，无原程序运行或外审。','integrated',[P2,T]),
]
receipts=[]
for i,n in zip(IDS,notes):
 a,b,c,d,targets=n
 receipts.append({'id':i,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 五源24793B/488行，actual5回执pushed/synced及当前Boss4 owner/source SHA核过。','comparison_note':b,'decision_note':c,'disposition':d,'targets':targets})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 实际关系检查

完整槽插入税对象推广既有平均菜单仅在b0、r=m使用的V=mGamma到任意合法整数过去与r槽；这种一般代数不补SPE付款。全人数真实SPE诊断反驳固定r当前增量支付槽边际亏损的指定系数桥，精确不反驳同例的Mfull/强推送/half。ROLE与ROOT是同一列分布的不同坐标，不能跨角色替换原IC。

三八对象与旧完整INT分别保不同负项，本批按源负载/抽样映射解释，并未造出共同付款。首次饱和B-E-U等价half，平均META的PAY仅是充分条件；两者law和钱包不兼容自动迁移。stored review的历史范围不覆盖当前主稿后加质量law/ownerlottery。

版本路由对整数extra-one调用当前已读分数定义的Jensen t<=v及银行完整SPE反族，确实反驳旧整数首位F_r，不等同t与v；聚合W桥、一般FREE-ROOT另有量词。已交可信根修复与已证人数half只在相同m条件接入鲁棒R，不形成新六人结果。两名剩余三比较定理是准确局部接口。

这是阶段二的实际语义关系审查，已有关系给出原因和域；没有导入旧图、mapper认领、强制连通或生成第三阶段超边。
''')
candidates=[]
candidate_ids=['43fcfd09b6d0ae5d96b5','c57e4ec366e7af1be467','ef21819792cb2a9aac5f','793061843887102a114a','62fadc53e30b4b1c856b']
for i in candidate_ids:
 p=REPO/'cleanup/progress'/f'{i}.json';progress=json.loads(p.read_text()) if p.exists() else None
 assert progress is None,('candidate no longer available',i,progress)
 candidates.append({**inv[i],'progress_observed':None,'ownership_status':'no progress file at actual local check; root must claim current available intersection','actual_read_status':'full original read as DM related only; no primary done or automatic claim','local_input':next(r['local_path'] for r in related if r['id']==i)})
js(W/'next-candidates.json',candidates)
put(W/'delivery.md',f'''# 交付范围

本批实际5源、24793B/488行，原始claim `{claim['remote_tip']}` pushed/synced，owner/source SHA匹配。新增2份自足正式正文；首饱和主稿、三八独审按已交完整对象精确duplicate，两份README与D22完整增补integrated，共5条semantic receipts。

原件5、相关原件5、12份实际全文比较的现行正文快照及3次纯本地helper的真实供给manifest全部保留。0原数学CLI/新策略复演/扫描；未重跑旧同SHA成功。相关程序/JSON没有读到的范围明确不认证。完整INT负源税、后加质量/ownerlottery审查边界、Jensen t<=v的整数extra-one纠正和未付聚合/FREE-ROOT分别保清。

Root按根目录copy-files.json白名单复制，先正常推正文/依赖，后逐源done；本代理未shared Git写、领、done或checkpoint。下一5只是本地实际available候选，不预领。copy-files不包含自身及transport摘要以避免循环哈希。
''')

checks=[]
def check(name,ok,detail=None):
 row={'check':name,'passed':bool(ok)}
 if detail is not None:row['detail']=detail
 checks.append(row)
 assert ok,name
for r in primary+related:
 b=(S/r['preserved_path']).read_bytes();d=inv[r['id']]
 check('exact source bytes '+r['id'],len(b)==d['size'] and sha(b)==d['sha256'])
 check('exact local blob SHA1 '+r['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==d['blob'])
check('actual unprojected five claim preserved',set(claim['ids'])==set(IDS) and claim['status']=='pushed' and claim['local_sync']['status']=='synced')
for i in IDS:
 p=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text())
 check('current owner and source SHA '+i,p['owner']=='Boss4' and p['disposition']=='in-progress' and p['source_sha256']==inv[i]['sha256'])
check('full five source read and honest prior related reuse',scope['primary_bytes']==24793 and scope['primary_lines']==488 and len(read(E/'prior-full-read-reuse.json'))==3)
check('full five related actual input supply',scope['related_bytes']==20908 and len(related)==5)
check('local helper calls and no original math execution',scope['safe_local_export_helper_calls']==3 and scope['helper_local_git_cat_file_blob_reads']==10 and scope['new_original_mathematical_CLI_calls']==0)
for r in contexts:
 b=(S/r['snapshot']).read_bytes();check('exact actual context snapshot '+r['path'],len(b)==r['bytes'] and sha(b)==r['sha256'])
for p in [F,T,M]:
 dd=CACHE/'r3-optimal-union-menu-and-source-covariance-primary'/p
 check('existing DD target intact '+p,(REPO/p).read_bytes()==dd.read_bytes())
links=[]
for p in [P1,P2]:
 t=(S/p).read_text();b=(S/p).read_bytes()
 check('flat MATEK metadata '+p,all(re.search(r'^'+f+r':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']))
 check('all nonLF C0 zero '+p,not any(ord(c)<32 and c!='\n' for c in t))
 check('trailing whitespace zero '+p,all(l==l.rstrip() for l in t.splitlines()))
 check('all TeX display delimiters matched '+p,t.count('\\[')==t.count('\\]'))
 check('no unexpanded source placeholder '+p,'SOURCE_' not in t)
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  target=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]))
  at=S/target if (S/target).exists() else REPO/target
  check('relative formal link '+dest,at.exists())
  links.append({'source':p,'destination':dest,'resolved':target,'bytes':at.stat().st_size,'sha256':sha(at.read_bytes()),'read_source':'stage' if at.is_relative_to(S) else 'current repo'})
js(E/'formal-link-check.json',links)
check('two new formal outputs only',sorted(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))==sorted([P1,P2]))
check('exact five semantic receipts only',{r['id'] for r in receipts}==set(IDS) and len(receipts)==5)
for r in receipts:
 check('complete semantic receipt '+r['id'],all(r[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']))
 for t in r['targets']:check('receipt target exists '+t,(S/t).exists() or (REPO/t).exists())
check('all semantic source units map to self-contained targets',len(coverage)==5 and all(r['units'] and r['destinations'] for r in coverage))
check('all explicit manual analytic obligations retained',len(obligations)==23)
check('all five metadata next candidates actually available',len(candidates)==5 and all(r['progress_observed'] is None for r in candidates))
for r in read(E/'formal-resource-manifest.json'):
 b=(S/r['path']).read_bytes();check('formal resource SHA '+r['path'],len(b)==r['bytes'] and sha(b)==r['sha256'])

observed=[]
for p in sorted(S.rglob('*')):
 if not p.is_file():continue
 rel=str(p.relative_to(S))
 if rel in ['copy-files.json','copy-paths.txt','delivery-summary.json']:continue
 try:t=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()]
 if bad:observed.append({'path':rel,'lines':bad,'frozen_source_or_context':any('/'+x+'/' in rel for x in ['original','related','context'])})
check('no derived whitespace errors',not any(not r['frozen_source_or_context'] for r in observed))
js(E/'transport-whitespace-observations.json',{'rows':observed,'policy':'original and exact context snapshots remain byte frozen; derived-only whitespace errors forbidden'})
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_all_nonLF_C0':0,'formal_trailing_whitespace':0,'relative_links_checked':len(links),'scope':'source/claim/owner/hash and format checks, complete explicit manual analytic coverage and status boundaries; machine checks do not replace mathematical reasoning'})
rows=[]
excluded={'copy-files.json','copy-paths.txt','delivery-summary.json'}
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in excluded:
  b=p.read_bytes();rows.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),rows)
put(Path('copy-paths.txt'),'\n'.join(r['path'] for r in rows)+'\n')
summary={'stage':str(S),'copy_files':len(rows),'copy_bytes':sum(r['bytes'] for r in rows),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':scope['primary_bytes'],'primary_lines':scope['primary_lines'],'new_formal_objects':2,'new_formal_bytes':sum((S/p).stat().st_size for p in [P1,P2]),'semantic_receipts':5,'duplicate_sources':IDS[:2],'related_only_sources':5,'checks':len(checks),'relative_links':len(links),'original_math_program_runs':0,'safe_local_export_helper_calls':3,'claim_tip':claim['remote_tip'],'next_candidate_ids':candidate_ids,'not_performed':['shared Git writes','clean claim/done/checkpoint/show','network/lazy fetch','mapper/phase3 graph import','new original math CLI or finite strategy scan']}
js(Path('delivery-summary.json'),summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
