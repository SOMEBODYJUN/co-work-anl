from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-hamming-constant-shared-and-source-preserving-kernels';E=Path('tools/evidence/hamming-constant-shared-and-source-preserving-kernels');W=Path('cleanup/workspaces/Boss4/r3-hamming-constant-shared-and-source-preserving-kernels-next')
IDS=['ea63a17109a10d528f3e','ff20bcd67e5bd5867fb1','7126e26f38757594fdb7'];P1='archives/customer-attraction/state/障碍/标签汉明邻域与完整末尾的删行障碍--障碍.md';P2='archives/customer-attraction/state/构造/实际遗漏全共享的常值均衡近二族--构造.md';P3='archives/customer-attraction/state/引理/来源客户保留的最大系数退款与支持条件--引理.md'
CTX=['archives/customer-attraction/state/资源/静态源占用反例与零遗憾紧族的审查和范围--资源.md','archives/customer-attraction/state/障碍/固定离轨次数截断的无常数福利障碍--障碍.md','archives/customer-attraction/state/引理/合法真实分支的枢轴保护与递增中继--引理.md','archives/customer-attraction/state/推论/最大主题根近饱和的覆盖阈值--推论.md','archives/customer-attraction/state/审查/同客重置父审的纯流范围与核版本--审查.md','archives/customer-attraction/state/资料/重置密度的初始化守卫与整行付款边界--资料.md','archives/customer-attraction/state/引理/同客重置流的逐接收点密度--引理.md','archives/customer-attraction/state/定理/同节点安全净券与最大标量剪枝--定理.md']
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
claimpath=R/'boss4-r3-next-kq-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids'])
mp=C/'ki-next-actual-local-mathematics.json';m=json.loads(mp.read_text());primary=[];owners=[]
for i in IDS:
 x=next(x for x in m if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/v['path'];cp(x['local_path'],q);cp(x['authority_manifest'],E/'original-export-authorities'/f'{i}.json');primary.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_mode':'KI-next authorizedactual fullpreclaim3MD in2untruncatedbatches, allmathematics/status/lastprogramrecords read; currentexactbytes reusedafteractualKQclaim, nofake reread or newrun'})
assert sum(x['size'] for x in primary)==23558
js(E/'source-manifest.json',primary);cp(mp,E/'actual-preclaim-local-source-availability.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners)
contexts=[]
for p in CTX:
 b=(REPO/p).read_bytes();q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'KQ actualentirecurrentformal mathematicaltext read in4untruncated outputbatches; fullproof/domain/scope compared notjustkeywordsearch'})
js(E/'context-manifest.json',contexts)
def front(i,kind,tag,title,status,summary,sid):
 f='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id',i),('kind',kind),('type_tag',tag),('title',title),('status',status),('summary',summary)])+'source_refs:\n'
 for x in inv[sid]['sources']:f+='  - '+json.dumps('source:'+x['commit']+':'+x['path'],ensure_ascii=False)+'\n'
 return f+'---\n\n'
specs=[(P1,'hamming-body.md','customer-attraction/fixed-label-hamming-neighborhood-and-complete-tail-row-truncation','obstruction','障碍','标签汉明邻域与完整末尾的删行障碍','complete-analytic-parameter-family; full-formal-policy-not-SPE; no-full-Gamma-separation','任意m/k/r保护固定标签Hamming带、actual路径与全部末尾真实IC，显式省略负行；H_d+k+r福利及锥分离全部自足，别于相对σ行为偏离计数，原8例仅MD历史。',IDS[0]),(P2,'shared-body.md','customer-attraction/fully-shared-actual-omission-constant-SPE-near-two-family','construction','构造','实际遗漏全共享的常值均衡近二族','complete-constant-policy-iff-and-background-form; near-two-not-half-counterexample','保常值A全历史iff及合法背景版、全部遗漏共享/零浪费整数族、退化去重与同目录全部SPE的(2−1/m)界；是既有根饱和机制的精确共享实例，0重跑原8树。',IDS[1]),(P3,'kernel-body.md','customer-attraction/customer-origin-preservation-max-coefficient-refund-and-support-condition','lemma','引理','来源客户保留的最大系数退款与支持条件','proved-local-nonnegative-representations-and-positive-input-support-iff; global-wallet-open','restricted-X重采与逐客户不重采分开，一次βmax整行退款、uniform-subset PRICE及同客取消严格增载自足；full-v X支持iff明定h>0，跨context共同cap未证。',IDS[2])]
for p,fn,i,k,t,title,status,summary,sid in specs:
 b=(C/'next-three-after-ki-drafts'/fn).read_text();assert b.startswith('# '+title+'\n');b+='\n原件精确SHA/冻结版本、全读范围、相关正文与真实多组认领见[本批证据](../../../../tools/evidence/hamming-constant-shared-and-source-preserving-kernels/source-manifest.json)。全部原件未改，原程序/输出/审稿仅按实际MD阅读范围归源，不额外done引用资产或执行旧角色命令。\n';put(p,front(i,k,t,title,status,summary,sid)+b)
js(E/'formal-resource-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha((S/p).read_bytes())} for p in [P1,P2,P3]])
coverage=[{'id':IDS[0],'disposition':'integrated','targets':[P1,CTX[0],CTX[1]],'units':['allm>=1 k0..m-1 n=m-k/r0..n-1 d>=1 commonmultipleL/allpositive disjointunit themes/p=2m-k optionalempty','fullorderedpolicy exactactual A/freshB protectede/fixedfirstwrongt beyondr/tailfresh; fixedlabelHamming notD_sigma relativebehavior','alltailIC/allprotectednonactualIC/exactactualrootdeviationdenominatorD_i/oldfutureAorB empty/self allcases','actualW L(Hd+r+k)/OPT mL/halfnegativecondition/d1m1boundaries','explicitbadnode B1..B(r+1) cB1=d freshdeviationL vsL/d/notSPE nofullGamma counterexample','rowcone nonnegw retainedI/targetnegative needsomittedrow notuniversalproof/globalhalf','fixedk r0 unbounded/asymptotic k+r overm alpha<1/2 /notinterchangealgorithmcost','m7 k1 r0 L60A10,12,15,20,30,60 W207OPT420 bad-50; m10 sum2 L840W3963OPT8400','all8finiteoldFractionreports/countrepresentatives18564 vs657early12483comp/bigsamplednotexhaustive/no codeJSONnewread orrun','originalearlierparentreviewpending/laterreportedblindcomplete historicalnotnewreview/externalminimalitynovelty unclaimed']},
{'id':IDS[1],'disposition':'integrated','targets':[P2,CTX[2],CTX[3]],'units':['constantA completeSPE iff forallT |A-T|>=m|T-A| rootnecessary allhistorysufficient intersectionscancel','legitimatefixedbackground b/r iffSUM_A-T1/(b+r)>=SUM_T-A1/(b+1)/fixedacrosssubtree/no freecrossbranchglue','m>=2 a>=1 Kma+1/x,y/binaryanchoredQ sizea/2m-1distinct inclusionmax/total(2m-1)a+1','allA^m fullSPE/pay a+1/m/W ma+1/OPTfullcoverage withA+oneperQ/ratio2-1/mminuscorrection/a1limit2/fixedmclassical','allactualmissing shared2max/no missedglobalprivate/zeroG/D<W not71falsebridge/laminar/extremeassumptionsnotgeneral m>=3','variablea_j>=0/maxempty0/zeroQsingletondedup not2m-1maxima/LIMIT K-1>=mmax/allslotsmoreblocks noover2','allCONSTcatalogOPT<=(2-1/m)K/anySPE ui>=K/m W>=K/globalnotnewhalfclass/currentrootE0rigidity','all8originaltree15632/138792sourceMDreport/defaultprintexclusiveoutput/31nodem3a2 notnewrun orcodeJSONread','historicalreviewreceiptpending notnewexternalorclaimednovelty']},
{'id':IDS[2],'disposition':'integrated','targets':[P3,CTX[4],CTX[5],CTX[6],CTX[7]],'units':['fullcontextB/a/actualresetA andu_i/vxDx/Jsets/qnx/PminusN/ell positive exactID','oncewhole actualprefix e>=0 notperclientIC/pastactualsink/futuretrueprescribedcontext','fixedglobalX positiveincoming nuX/DX/PX/NX/Frefund[0,ui]/exactconservation/receive nuXpositive/fixedXresampleswithinX notoriginx','PRICE directeachcustomer uniformsubsetsubprob row convexmix; anynonnegative roleprice Theta maxS sums/(1+size) andkcut ascorollary notkcutalone proof','changeddenom nuX<=fullv notoldCLIP subroute/no beta orcolumncapimprovement','allh_x samecontext aggregate origin/maxbetax once fullIC/refund F<=betamaxui/layercake totalcoefficientmaxnot sum singleton','u_i0 nopositiveincoming/zeroh andzero supports no0/0','fullsamecustomerpositive-negative cancellation PprimeNprimeidentity/remainingpositive impliescA>cB/nonterminalsamexstrictboundedload/notarbitrarydrop','originproportionalresplitlinearflows/current samecustomer butactualcurrentwholewallet notphysicalx/notmergeorderedcontexts','originalfullv fixedbeta h/v/supportedXcapacityiff PX>=(v-ui)+ explicitlypositiveh/zerohtrivial/currentbeta min(v,u)/noSPEguarantee orRESIDUALCAP counterexample','samecustomerinventory/loadincrease notsharedactualwallet/PRICEbound notwholecap/newlocalrepresentation notfullhalf/mathprogram0','existingR65parentonlypureflow andcurrentpartialmaxrefund proofreuse notfakehistoricalwholekernelaudit/newblind']}
]
js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':3,'primary_bytes':23558,'primary_lines':sum(x['lines'] for x in primary),'primary_fullread':'actualall3MDtext/math/sourceprogram-status paragraphs inKI-next authorizedpreclaim prep, exactSHA reusedafteractual17claim notfakefirstreading','current_formal_fullreads':len(CTX),'new_formals':3,'dispositions':{'integrated':3},'new_theorems_or_game_instance_discovery_claimed':0,'mathematical_work':'completeanalytic preservation/expandedmissingPRICEstep andpositiveinputzeroendpoint explicit; notnewnumericalproof orglobalhalf','new_math_program_runs':0,'original_math_CLI_calls':0,'old_success_replays':0,'new_LP_BI_random_SPE_runs':0,'original_program_JSON_or_blindreview_fullread':False,'old_MDFraction_audit_counts':'sourceattributedonly, notnewPASS/exhaustivebigsampleorcanonicalcodecert','helper_export_calls':0,'existing_authorized_local_bytes_rechecked':3,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'network_or_lazy_fetch':0,'own_clean_show_claim_done_checkpoint_calls':0,'shared_Git_writes':0,'real_board_account_auth_operations':0,'phase3_graph_import':0,'derived_packaging_builder_calls':2,'derived_packaging_builder_failures':1}
js(E/'read-scope-and-evidence-status.json',scope)
notes=[('9487B原稿所有九节参数/完整策略/在轨与保护带及末尾证明/福利/负行/锥与极限/两小例/最后程序与审查追加状态全部全文实读，同SHA已有related不冒新第一读。','现8242资源只摘要该源，现固定rank障碍用相对σ行为离轨D_sigma，本源是相对固定A标签的Hamming半径r并加完整尾深k，数学合同不同。新自足对象保每类真实节点、旧A/未来A/B/空主题和明确L/d-L负行、全参数锥范围，不靠8有限例外推。','integrated：完整形式策略删行障碍而非SPE/half反例或完整Γ分离，不虚加m6结论。18564计数代表覆盖对应尾部顺序只因该尾策略依计数；大参数样本不叫穷尽。原8程序/JSON及盲审文本未读跑，source晚补父方/第二代理审查按原时序保，0新外审/新颖性。'),
('7316B共享近二稿全部常值iff/固定背景版/整数目录/遗漏归属/退化/全catalog界及程序报告全文读，未以hub引用数学只读摘要当全源。','现hub引理只用此族作合法缺边与预算取等；现最大主题根饱和含E0目录刚性。新构造完整保常值全历史iff、固定b/r的子树必要充分、所有漏客共享/零浪费、a_j零去重和全目录所有SPE(2-1/m)上界，明确这是已知机制共享实例而非新half适用域。','integrated：自足原整数压力族和解析边界，近二不越二，D<W不反71客户加强桥。原8树15632/138792及31节点仅sourceMD记录，未读取/运行原代码JSON或将其与hub局部审计混成同run，0新增游戏/外审/新颖性。'),
('6755B来源保留核六节全部符号/正负边/固定X/一次max系数/取消/PRICE/原full-v支持条件/共同钱包未证段全文读；现5936审查7098资料6567密度9131SAFE全部真全文比较。','现资料已完整保βmax退款，仍需自足restricted-X支持/重采、每客户uniform-subset子概率PRICE、完整同客取消后严格增载、原full-v限定X的局部iff。新引理从子概率行直接给任意非负price，不从仅kcut误推；iff明定h>0，h0另零方案，不虚假扩量词。','integrated：局部新合法表示/真实DAG/库存origin合流与一次IC系数准确保，非逐客IC、非actual同x物理券、非full-v CLIP子路由；不声称beta下降/角色共同cap/RESIDUALCAP/half。原R65父审只纯密度，不倒填已审全核或称新blind；无原代码主源/新有限例/数学程序运行。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 实际完整17ids claim原字节保，只本3subset/currentowner/sourceSHA核后封成功receipt。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# KQ Hamming/共享常值/保客户核

三原稿23558B完整实际读，八现正式对象完整比较，3integrated/3自足对象。原17ids actualclaim保原字节，仅本3owner/sourceSHA核，不投影原receipt，不额外done原程序/JSON/盲审文本。

Hamming是相对固定标签路径，不是σ行为偏离计数；完整策略删行负点非SPE/完整Γ/half反例。共享常值有全历史iff/固定背景版/全部遗漏共享压力族和全catalog半界，近二不越二不重认已知半界首次。来源核一次βmax整行退款、directuniform-subset PRICE、正输入full-v X支持iff与零端点齐，跨context实际共同钱包仍开放。

0原CLI/新数学程序/LP/BI/随机/旧成功复跑。原有限8参数/8树与审查按MD原时序保，不当新PASS/外审/新颖性。所有原字节、相关SHA、逐段覆盖/关系与自查精确保；Root先推正文依赖再done，代理无sharedGit/网络账号公屏/mapper。
''')
put(W/'relation-review.md',r'''# 阶段二关系

Hamming/r+完整尾/k共给一套被删真实行的精确保护，旧D_sigma固定行为离轨是不同索引族；原完整σ不是SPE，明示badrow支持删行锥分离但不扩完整Γ。全参数/比例界靠解析非有限样本。

共享常值CONST/BG是整子树iff，换枝后原当前IC仍需付；全部遗漏两共享/零浪费族与经典allbig/根E0目录刚性相连，不是新half子类。hub只先前用其一项合法银行预算，这里补完整原构造和一般同目录界。

来源保留核与现βmax退款证明精确复用，restrictedX/单客origin两个分母分清；PRICE从真实uniform-subset子概率直接证明，full-v SUPPORT只正incoming iff，zeroh独立平凡。保库存/负载增长/逐context退款不合成角色多context cap，纯flow父审不自动审wholeIC新核。

三主source完整关系/有用缺口保，不额外done依赖或凑第三阶段连通；0新数学执行/外审/新颖性，也不把未闭目标当保留这些工具的前提。
''')
nextmp=C/'kq-next-actual-frozen-output-candidates.json';nm=json.loads(nextmp.read_text());nextrows=[]
for x in nm:
 v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];p=REPO/'cleanup/progress'/f"{x['id']}.json"
 if not p.exists():nextrows.append({**v,'local_path':x['local_path'],'actual_normal_show_capture':x['actual_normal_show_capture'],'progress_observed':None,'read_status':x['prior_actual_complete_read']+'; stillnotprimary, no newclaim/receipt/run'})
cp(nextmp,E/'actual-next-frozen-output-read-status.json');js(W/'next-candidates.json',nextrows);cp(Path(__file__),E/'build_delivery.py')
js(E/'packager-recovery.json',{'builder_calls':2,'first_failure':'quantifier matcher expected literal 不是actual(i,x), body correctly says 不表示current是actual(i,x)物理同客券','correction':'checker phrase only; no mathematical body/source changes','new_math_program_runs':0,'original_CLI_calls':0,'old_success_replays':0})
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tb(s,l,r):
 def count(d):return sum(ord(s[i])==92 and s[i+1]==d and (i==0 or ord(s[i-1])!=92) for i in range(len(s)-1))
 return count(l)==count(r)
for x in primary:
 b=(S/x['preserved_path']).read_bytes();ck('originalexactSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('originalexactblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('raw17claimpreserved',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and len(claim['ids'])==17);ck('actualclaimpushedsynced',claim['status']=='pushed' and claim['local_sync']['status']=='synced' and claim['local_sync']['remote_tip']==claim['remote_tip']);ck('actual3subsetownerSHA',set(IDS)<=set(claim['ids']) and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners))
for x in contexts:ck('currentfullreadcontext '+x['path'],sha((S/x['snapshot']).read_bytes())==x['sha256'] and len((S/x['snapshot']).read_bytes())==x['bytes'])
links=[]
for p in [P1,P2,P3]:
 t=(S/p).read_text();ck('flatMATEK '+p,all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('formalC0zero '+p,not any(ord(x)<32 and x!='\n' for x in t));ck('formaltrailingzero '+p,all(l==l.rstrip() for l in t.splitlines()));ck('actualTeXbalanced '+p,tb(t,'[',']') and tb(t,'(',')'))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  n=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('link '+dest,q.exists());links.append({'source':p,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
t1=(S/P1).read_text();t2=(S/P2).read_text();t3=(S/P3).read_text();ck('labelHamming_notbehavior_fulltail',all(x in t1 for x in ['固定标签前缀','不是相对σ规定动作的行为偏离次数','全部|h|≥n','L/d-L<0','不是原half反例']));ck('allmparameterandfiniteboundaries',all(x in t1 for x in ['0≤k≤m−1','0≤r≤n−1','d1时','18564','657','12483','大参数尾部仅固定种子样本']));ck('sharedallomissionsanddegenerate',all(x in t2 for x in ['每个actual遗漏客户','极大全局私有客户','零块会退化','max空集取0','全部SPE满足OPT≤(2−1/m)W']));ck('sharedfixedbackgroundnotglue','b/r在整个子树固定' in t2 and 'BG不是免费粘合定理' in t2);ck('uniformsubsetPRICE directstrongerthanjustcut',all(x in t3 for x in ['uniform-subset子概率核的凸组合','不是声称单独知道所有k-cut','\\Theta(\\lambda)','1+|E_x|']));ck('SUPPORTpositivehzeroexplicit','正输入h>0' in t3 and 'h0时全零方案平凡可行' in t3 and '(v-u_i)_+' in t3);ck('aggregateoriginbeforemaxglobalwalletopen','先合并所有origin' in t3 and '不表示current是actual(i,x)物理同客券' in t3 and '没有证明同actual角色跨contexts' in t3);ck('partialcancellationnotstrictload','完整取消后' in t3 and '不能把仅部分取消' in t3)
ck('3receiptsallintegrated',len(receipts)==3 and {x['id'] for x in receipts}==set(IDS) and all(x['disposition']=='integrated' for x in receipts))
for x in receipts:ck('completereceipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() or (REPO/p).exists() for p in x['targets']))
ck('exact3newformal',set(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))=={P1,P2,P3});ck('zero originalCLI/math/replay',scope['new_math_program_runs']==scope['original_math_CLI_calls']==scope['old_success_replays']==scope['new_LP_BI_random_SPE_runs']==0)
for x in nextrows:ck('actualnextfullreadoutput '+x['id'],sha(Path(x['local_path']).read_bytes())==x['sha256'] and not (REPO/'cleanup/progress'/f"{x['id']}.json").exists())
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context']);bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('allnewderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_original_context_unchanged':True})
put(W/'delivery.md',f'''# KQ交付

3primary23558B/{scope['primary_lines']}行完整实读，八现正式数学对象全部全文比较；3integrated/3自足对象。原17ids claim{claim['remote_tip']}actualpushed/synced原字节保，仅本3owner/sourceSHA。0新数学程序/原CLI/LP/BI/随机/SPE/旧成功复跑，原code/JSON/盲审文本未读就只保MD历史。

Hamming/行为离轨不同、形式策略非SPE/完整Γ分离；共享常值iff与背景版、遗漏全共享近二/全catalog界；保客户一次βmax退款/直接uniformsubsetPRICE/正hfullv支持iff及零端点完整。共同钱包仍开放，旧半界去重不抹有用构造，无新外审或新颖性。

下一{len(nextrows)}原冻结JSON共{sum(x['size'] for x in nextrows)}B已JZ真实全部字段读，未primarydone，可实际claim后按JZ精确目标duplicate，不因已copy复勾。Root先推正文依赖再done，0sharedGit/网络/账号公屏/mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'scope':'actualoriginal/owner/raw17claim/fullmathcomparison/quantifiers/PRICEproof/supportendpoints/links/format/transport','mathematics':'analytic sourceproof preservation andsource-domain distinctions; 0newmathematicalprogram runs; checks do notprove globalwallet orhalf'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':23558,'primary_lines':scope['primary_lines'],'new_formals':3,'formal_bytes':sum((S/p).stat().st_size for p in [P1,P2,P3]),'receipts':3,'dispositions':{'integrated':3},'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'new_original_CLI_runs':0,'old_success_replays':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
