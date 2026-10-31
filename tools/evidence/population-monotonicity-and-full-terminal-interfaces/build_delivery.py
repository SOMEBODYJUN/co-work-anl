from pathlib import Path
import json,hashlib,re,posixpath,sys
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-population-monotonicity-and-full-terminal-interfaces';E=Path('tools/evidence/population-monotonicity-and-full-terminal-interfaces');W=Path('cleanup/workspaces/Boss4/r3-population-monotonicity-and-full-terminal-interfaces-next')
IDS=['b28e13d9c38be46a6f6c','b604a83b0410f853c05e','0d48e26ef6aadd2437dc'];P='archives/customer-attraction/state/反例/人数增加的十二客户全部均衡福利下降--反例.md';PA='archives/customer-attraction/state/审查/顺序统计残差的表达式错位与逐索引合法性--审查.md';PF='archives/customer-attraction/state/引理/完整真实菜单的逐尾稀释与额外槽信用--引理.md';PD='archives/customer-attraction/state/引理/删位归纳的有符号修复差与锚定最优边际--引理.md'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
# Only actualpushed owner-correct parentcapture unlocks successfulreceipts.
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids'])
mp=C/'ju-next-math-prework/reading-status.json';pre=json.loads(mp.read_text());primary=[];owners=[]
for i in IDS:
 x=next(x for x in pre['rows'] if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size']==x['bytes'] and sha(b)==v['sha256']==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/v['path'];cp(x['local_path'],q);primary.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_mode':'actualcomplete3MD sourceprework afterJU asparentcandidateauthorization; currentexactbytes reused notfakefirstread/rerun; actualKIclaim/currentownerSHA checked beforefinalreceipt','actual_read_note':x['read_note']})
assert sum(x['size'] for x in primary)==15061
js(E/'source-manifest.json',primary);cp(mp,E/'actual-prior-fullread-scope-not-claim.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners)
notespath=C/'next-three-math-drafts/coverage-preclaim.json';cp(notespath,E/'actual-preclaim-semantic-comparison-not-receipt.json');oldnotes=json.loads(notespath.read_text())
contexts=[]
for p in [PA,PF,PD]:
 b=(REPO/p).read_bytes();q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'actual fullcurrentformal text read inpreclaim comparison; currentSHArechecked beforefinalreceipt'})
for x in oldnotes['rows']:
 p=x.get('existing_target',x.get('existing_target_only_partial'));assert sha((REPO/p).read_bytes())==x['target_sha256']
js(E/'context-manifest.json',contexts)
f='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id','customer-attraction/twelve-unit-customer-all-SPE-welfare-decrease-three-to-four-providers'),('kind','counterexample'),('type_tag','反例'),('title','人数增加的十二客户全部均衡福利下降'),('status','proved-complete-ordered-subgame-classification-for-m3-and-m4; not-half-counterexample'),('summary','同一12单位客户三极大主题目录，全部三人SPE仅ABC/BAC覆盖12，全部四人SPE仅两A两B六排列覆盖11；保所有离轨平局与完整表，整数复制给绝对损失无界，0新原审计运行。')])+'source_refs:\n'
for x in inv[IDS[1]]['sources']:f+='  - '+json.dumps('source:'+x['commit']+':'+x['path'],ensure_ascii=False)+'\n'
f+='---\n\n'
b=(C/'next-three-math-drafts/population-body.md').read_text();b=b.replace('# 同一十二客户目录中增加人数使全部均衡福利下降','# 人数增加的十二客户全部均衡福利下降',1);old='本文目前为未认领primary前的独立草稿，尚无成功receipt、未主clone写入；全部Math原件和旧done历史不变。';assert old in b;b=b.replace(old,'原source全文、当前删位对象及本次真实认领/owner/SHA见[证据](../../../../tools/evidence/population-monotonicity-and-full-terminal-interfaces/source-manifest.json)。本页保自足数学，不额外done原程序/JSON或重跑其旧成功；原冻结文件和已有done历史不变。');b+='\n与[删位有符号预算](../引理/删位归纳的有符号修复差与锚定最优边际--引理.md)的关系是：其已正确引用本例否定人口单调预算，这里补足全部终端/续局/根分类，而非把该已done来源整体标错。\n';put(P,f+b)
js(E/'formal-resource-manifest.json',[{'path':P,'bytes':(S/P).stat().st_size,'sha256':sha((S/P).read_bytes())}])
coverage=[{'id':IDS[0],'disposition':'duplicate','targets':[PA],'units':['all7maxima/r=6-t/prefix model/sourcewholeq,U/orderstatrthseat formula','authorclaims everyH legal ASR threshold/actualargument onlyHcontainslarge seats/currentforallH unresolved notcertified false either','advertisedA/residualR/scriptRprime shift exactexistingcorrection no falseminima numericalbinding','all6positivefractions t0to5/route(0,0,0,0,1,0)/targetK123456 omitactualB0 only/otheromitsnotcovered','oldM/L/T Farkasnegativebase-12442/3967807/customercolumn notrealizableSPE','ifallRprime>=0thenR>=0/rowfamilysuperset separation implieslegal-subfamilyconditionalnoSPEwelfarecounterexample','sourceauditcommandoldrole notcurrentnewCLI orrawcode read']},
{'id':IDS[1],'disposition':'integrated','targets':[P,PD],'units':['fixed12unit6types/A6B6C5/3distinctincomparablemaxima/allm3andm4 completeorderedhistories/ties','allU_A/U_B/U_C formulas validchosenpositive denominator/OPT3OPT4=12','complete6row3personlastBRtable/allsecondmenus/rootAorBstrict/allABC BAC','complete10row4personlastBRtable BCCmiddle5/2/all6two-remainingmenus/ACconditionaltie independentlylegal','allrootchildren payoffs/rootCexcluded/eachAABB6orderedpaths realizable/onlyW11forallSPE','copiesintegerq allpayoffs/ties scale/absoluteq lossunbounded notnewmechanism/minimality/novelty/externalreview claims','oldprogramCartesian childSPE paths/directunitsFraction/3cert13nodes26nonself/4cert40nodes80nonself onlyMDreport/oldm1to5 andzero/fullboundarynotextended','existingdeletionlemma correctpartialsummary/rawrelatednotwrong; newformal givesfullsourceproof/no repeatedaudit']},
{'id':IDS[2],'disposition':'duplicate','targets':[PF],'units':['alltrueZ_i(b) fullm vsdeletedB_i m-1/sameoriginalsigma/notm+1realplayers','D/C/Cplus/e/kappa/H extraone exactglobalidentity/slacknondiscard','old36counterexamplewithoutHnotnewFTAfalse/Hnonnegative noautomaticpayment','FTAallp vsoneoptimalp enoughstaticvalue/Mpathallquerycap finite-minimax notsamequantifiers','staticOPT<=2m v(m+1) Jensenmeanload proof/allbig m+1 +m-1singleton sharp/m1endpoint','fixedmatrixM/symmetrizationcopositive notPSD/diagonalbound/fromeachcurrentIC','pairwiseoffdiag<=2W sufficientnotnecessary/two-supportsqrt criterion andsourcepositivecross squared equivalence/notallmulti support','oldGammafixedp/querypair attack securityduality+rootpadded6DAG historynotcurrentproof/run/instruction','priorfractional t_r/t_extra/integer v/fullmenu assetsnotrenamednewγ/notnewobjects/fulltreepaymentopen']}
]
js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':3,'primary_bytes':15061,'primary_lines':sum(x['lines'] for x in primary),'read_mode':'all3actuallyfullread beforeKIofficialassignment underparentauthorizednextprework; honest sameSHAreuse afteractualclaim notnewfakefirstread','current_formals_actualfullreads':3,'dispositions':{'integrated':1,'duplicate':2},'new_formals':1,'new_game_instance_discovery':0,'source_finite_completeproof':'fixed12unit m3andm4 allsubgameclassification analytically preserved, notnew numericalscan','ASR_scope':'existingadvertisedresidualvsRprime correction/forallH proofgap/conditionalrowfamily separation exactlyreuse; no originalaudit cert','FTA_scope':'existingfullextra credit/staticsharp2m/copositive/twopoints/Mpathquantifiers exactlyreuse, notnewcandidate','new_math_program_runs':0,'original_math_CLI_calls':0,'old_success_replays':0,'new_LP_BI_random_SPE_runs':0,'population_originalaudit_code_and_JSON_fullread':False,'primary_MD_oldprogramreports_notnewexecutions':True,'new_helper_export_calls':0,'localexisting_export_bytesrechecked':3,'network_or_lazy_fetch':0,'own_clean_show_claim_done_checkpoint_calls':0,'shared_Git_writes':0,'real_board_account_auth_operations':0,'phase3_graph_import':0,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'derived_packaging_builder_calls':1,'derived_packaging_builder_failures':0}
js(E/'read-scope-and-evidence-status.json',scope)
notes=[('2591BASR原README在JU后授权预读期全文读，全部定义/∀H声明/6正分数/route与六比较集/其他遗漏目标/脚本命令尾段均实际读，现核同SHA复用不伪新第一读。','现4776B审查已全文核并锁当前SHA，完整保广告A_H、残差R_H和脚本Rprime错位；rth统计论据只直接覆盖含大seat的H，普遍合法性仍需客户结构证明。六数保原报告，旧负target与Farkas行域分离保条件逻辑，不升级SPE。','duplicate：所有数学/数字/用途有精确现目标，无需再发ASR定理或锥证书。未本批全文读/执行原audit，不把当时缺件历史说成全局永久缺；source本身不因广告措辞与缺口退休，0重跑/额外done原程序。'),
('7162B人口反例全文实读，六单位兴趣型、完整三/四人末位表、六两尾菜单、根收益/全部路径、q倍缩放与原程序角色全部逐项读。','现8749B删位引理已正确摘要此例并存原related，但未自足全终局分类；新正式反例保全部表/当前与离轨IC推导/每合法平局及所有六个AABB排列实现。与删位Δ预算的关系准确，未标旧引理整体错误。','integrated：完整自足固定12客户/3和4人数的全部SPE福利下降，整数复制仅同次缩放；不反half、不宣称其他人数/最小性/外审/新颖性，原audit/JSON只有MD报告未读跑，0新数学或旧成功复跑。'),
('5308Bfull_terminal_debt原全文实读，全部定义/全局恒等式/FTA不同量词/静态锐2m/Jensen/二次式/两点平方界/旧任务先验和最后接口去重段均完整读。','现8438B完整真实菜单引理已全文同SHA比较，H+ICslack、FTA allp或某最优p、Mpath finite-minimax条件、静态锐族、copositive非PSD/对角与逐对充分/两支持sqrt条件完整覆盖；当cross>2W时原平方条件与现sqrt条件等价，不新建criterion。','duplicate：精确数学对象全覆盖，不以旧OPEN替当前判断、不由Mfull银行失败说FTA或Mpath已反。旧security_duality/padded六人DAG攻击是历史角色/计划，未冒本批代码/输入/Γ运行；无新candidate或数学执行，0额外done引用资产。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 实际完整多组claim原字节保，仅本3subset/currentowner/sourceSHA核后封成功receipt。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# KI人口反例/ASR/FTA三主源

15061B三原件全部真实全文读，1integrated+2duplicate；一新自足12单位客户3→4人全部SPE反例保6/10行末位表、6续局菜单和根分类，0新游戏发现/数学程序/原CLI/旧成功复跑。原代码/JSON未本批取得全文就只保MD历史报告，不额外done。

ASR当前审查完整保R/Rprime及∀H合法性缺口和旧有限Farkas分布条件，不把广告阈值直接认证。FTA全信用、静态锐2m、完整根/全路径/某个最优p量词、两点copositive已完整覆盖，不重复造候选。全源、当前目标SHA、实际owner/rawclaim及去向逐项保。

这些原稿的旧角色/研究计划/停止扫描不是本轮执行指令。Root先推正文依赖再done，代理0sharedGit/网络/账号公屏/mapper；下一三真实本地MD先全文比较预稿，不预claim/receipt。
''')
put(W/'relation-review.md',r'''# 阶段二关系

人口下降例给同一目录全部3人W12/全部4人W11，OPT均12；它反人口单调预算，不反half。旧删位引理已正确引用，新增自足页只是补完整分类证明，保所有离轨历史/平局与全六排列，非旧done整体纠错。

ASR每H广告合法性与rthorderstat论据有量词缺口；Rprime到广告R的非负差本身保一条条件行族分离，不造六人坏SPE。FTA一单位额外负载信用和ICslack不能删，Mfull反例不自动反跨actual全路径聚合；所有p与某个安全最优p的充分路线分别保。

旧代码/JSON角色与有限报告来自实际MD，没读跑不冒认证，三主稿全部有用内容去向完整。不额外done引用源、无第三阶段旧图导入或强制连通边，无外审或新颖性认证。
''')
nextmp=C/'ki-next-actual-local-mathematics.json';nm=json.loads(nextmp.read_text());nextrows=[]
for x in nm:
 v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];p=REPO/'cleanup/progress'/f"{x['id']}.json"
 if not p.exists():nextrows.append({**v,'local_path':x['local_path'],'authority_manifest':x['authority_manifest'],'progress_observed':None,'read_status':'actual full3sources read inauthorizedKI-nextprework; related currentformal comparison underway; notprimary/receipt','read_note':'9487Hamming true-labelradius/tail/allmcone andexplicitbadnode;7316constantA iff/background/sharedomission family/allcatalogbound;6755restrictedX/maxbeta/PRICE/sourcepreservation andfullv supportcondition alltextread'})
cp(nextmp,E/'actual-next-three-local-authorities.json');js(W/'next-candidates.json',nextrows);cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tb(s,l,r):
 def count(d):return sum(ord(s[i])==92 and s[i+1]==d and (i==0 or ord(s[i-1])!=92) for i in range(len(s)-1))
 return count(l)==count(r)
for x in primary:
 b=(S/x['preserved_path']).read_bytes();ck('sourceexactSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceexactblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('actualrawclaimpreserved',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes());ck('actualclaimpushedsynced',claim['status']=='pushed' and claim['local_sync']['status']=='synced' and claim['local_sync']['remote_tip']==claim['remote_tip']);ck('actual3subsetownerSHA',set(IDS)<=set(claim['ids']) and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners))
for x in contexts:ck('contextactualSHA '+x['path'],len((S/x['snapshot']).read_bytes())==x['bytes'] and sha((S/x['snapshot']).read_bytes())==x['sha256'])
t=(S/P).read_text();ck('flatMATEK',all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('formalC0zero',not any(ord(x)<32 and x!='\n' for x in t));ck('formaltrailingzero',all(l==l.rstrip() for l in t.splitlines()));ck('actualTeXbalanced',tb(t,'[',']') and tb(t,'(',')'));ck('full3and4andmenutables',all(x in t for x in ['| AA | 2 | 16/3 | 11/3 | B |','| CCC | 9/2 | 9/2 | 5/4 | A或B |','| BCC | 25/6 | 5/2 | 3/2 | A |','| AC | AB、BA或BB |']));ck('allrootSPEandscalecomplete',all(x in t for x in ['全部实际路径恰ABC/BAC','六个AABB有序排列都可实现','绝对下降q无界','OPT₃=OPT₄=12']));ck('olddeletionnotgloballywrong','非把该已done来源整体标错' in t);ck('noauditruninvented','未读该程序/JSON、未新执行' in t)
links=[]
for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
 if '://' in dest or dest.startswith('#'):continue
 n=posixpath.normpath(str(Path(P).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('link '+dest,q.exists());links.append({'source':P,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
ck('ASRcorrectscopeexistingtarget',all(x in (REPO/PA).read_text() for x in ['R\'_H','所有 H','-12442/3967807']));ck('FTAcorrectscopeexistingtarget',all(x in (REPO/PF).read_text() for x in ['copositive','M_{path}','2m','某个真正安全值最优']))
ck('3receipts1integrated2duplicate',len(receipts)==3 and {x['id'] for x in receipts}==set(IDS) and sum(x['disposition']=='integrated' for x in receipts)==1 and sum(x['disposition']=='duplicate' for x in receipts)==2)
for x in receipts:ck('completereceipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() or (REPO/p).exists() for p in x['targets']))
ck('exact1newformal',set(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))=={P});ck('zero mathoroldreplays',scope['new_math_program_runs']==scope['original_math_CLI_calls']==scope['old_success_replays']==scope['new_LP_BI_random_SPE_runs']==0)
for x in nextrows:ck('actualnextavailable '+x['id'],sha(Path(x['local_path']).read_bytes())==x['sha256'] and not (REPO/'cleanup/progress'/f"{x['id']}.json").exists())
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context']);bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('allnewderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_original_context_unchanged':True})
put(W/'delivery.md',f'''# KI交付

3primary15061B/{scope['primary_lines']}行真实全文/三现正式对象全文比较；1integrated+2duplicate，一新12单位客户3→4人全部SPE反例自足保所有表/续局/根分类，0新游戏发现/数学程序/原CLI/LP/BI/随机/旧成功复跑。原多组{len(claim['ids'])}ids claim{claim['remote_tip']}actualpushed/synced，原字节保本3owner/sourceSHA核。

ASR广告A/R/Rprime和∀H合法性缺口精确去现review；FTA全部额外槽/ICslack/锐静态2m/共正及Mpath不同量词去现完整引理。人口例补自足全文，不将已done删位对象整体判错，原审计未读跑不冒认证。

下一{len(nextrows)}真实本地源共{sum(x['size'] for x in nextrows)}B已全文预读/相关比较，不预claim/receipt。Root先推正文依赖再done，0sharedGit/网络/账号公屏/mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'scope':'actualsource/rawclaim/owner/wholecomparison/completeclassificationtables/links/format/transport','mathematics':'analytic sourceproof preservation andprecise duplicate comparison, no newmathematicalprogram run; checks do notsolveASRforallH orFTA'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':15061,'primary_lines':scope['primary_lines'],'new_formals':1,'formal_bytes':(S/P).stat().st_size,'receipts':3,'dispositions':{'integrated':1,'duplicate':2},'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'new_original_CLI_runs':0,'old_success_replays':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
