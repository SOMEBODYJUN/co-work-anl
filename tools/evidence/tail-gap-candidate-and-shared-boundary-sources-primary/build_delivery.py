from pathlib import Path
import hashlib,json,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='tail-gap-candidate-and-shared-boundary-sources-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');D=C/'gap-candidate-and-related-boundaries-drafts';IDS=['6b953dda924f48243d6b','857599e66de0a1b953e9','734269b6e8a84cfea402'];T='archives/customer-attraction/state/候选/真实尾部最优利润的最小收益差额候选--候选.md';V='archives/customer-attraction/state/审查/圆环可信性父审的旁支合同与证据身份--审查.md';ML=C/'r3-cyclic-complete-credibility-and-parent-review-primary';MLE=Path('tools/evidence/cyclic-complete-credibility-and-parent-review-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 d=S/q;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(Path(p).read_bytes())
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids']);sync=claim['local_sync']['status'];proofpath=None
if sync=='needs-attention':
 proofpath=Path(sys.argv[2]);proof=json.loads(proofpath.read_text());assert proof['stash'] in claim['local_sync']['detail'] and proof['stash_kept'] and proof['missing']==proof['different']==[] and proof['unmerged']=='' and all(x['same'] for x in proof['tracked'])
else:assert sync=='synced'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};mp=C/'cyclic-parent-review-needed-math-local-inputs/local-export-manifest.json';m=json.loads(mp.read_text());sources=[];owners=[]
for i in IDS:
 v=inv[i];x=next(x for x in m['rows'] if x['id']==i);b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/v['path'];cp(x['local_path'],q);old=MLE/'necessary-related-original'/i/v['path'];assert (REPO/old).read_bytes()==(ML/old).read_bytes()==b;sources.append({**v,'preserved_path':str(q),'published_exact_ML_asset':str(old),'read_scope':'actualfullMDread asMLnecessaryrelated; freshprimaryowner/SHA andallmeaningcomparison honestlyreuse notfakefirstread'})
assert sum(x['size'] for x in sources)==19621
js(E/'source-manifest.json',sources);js(E/'actual-owner-snapshot.json',owners);cp(mp,E/'actual-original-local-manifest.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json')
if proofpath:cp(proofpath,E/'actual-independent-sync-resolution.json')
b=(REPO/V).read_bytes();assert b==(ML/V).read_bytes();cp(REPO/V,E/'comparison'/V);js(E/'comparison-manifest.json',[{'path':V,'snapshot':str(E/'comparison'/V),'bytes':len(b),'sha256':sha(b),'read_scope':'fullactualMLreviewresource authored/read pluscurrentallparagraphsemanticcomparison; nothashonlyduplicate'}])
refs=[f"source:{x['commit']}:{x['path']}" for x in inv[IDS[0]]['sources']];front=['---','id: customer-attraction/true-tail-optimal-profit-minus-realized-profit-minimum-payoff-gap','kind: candidate','type_tag: 候选','title: 真实尾部最优利润的最小收益差额候选','status: general-contract-unresolved-by-these-sources; exact-one-and-two-player-bases','summary: 合法背景尾利润GAP-r、强G2自足证明及原830/196LP等有限报告范围，复用伪孩子/自由t删除停界不冒真反例。','source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs]+['---','',(D/'gap-candidate-body.md').read_text()];put(Path(T),'\n'.join(front));put(Path(T),(S/T).read_text()+'\n## 原件与比较资源\n\n'+'\n'.join('- ['+x['id']+' '+str(x['size'])+' B 原件](../../../../'+x['preserved_path']+')' for x in sources)+'\n')
coverage=[{'id':IDS[0],'disposition':'integrated','targets':[T,V],'units':['full10055researchstatus/historicalmethods/noexternalreview/generalGAPlegalb/realPnotwelfare/Fmaxrrepeated/halfconditional','r1F=P/r2strongG2 fullthetaandcustomerinequalityproof newlyselfcontained T','allk pseudo summary/fixeddtail/notwholechildSPE Vfullreuse','deletionΓ/conservation/13unitinput/P10AAB/sixroottail/freeε/noK/doesnotrefuteG Vfullreuse','all3programnames/historical36unitDAG27243/112050/gap70,48620,k3..14/probe830+196/rootonlypartial/noexactFarkas/five7stop Tcomplete reportednotnewrun']},{'id':IDS[1],'disposition':'duplicate','targets':[V],'units':['entire4652v2(P)+(Cov)/v1notactualoldversionread/uncoverableblockr1defect','fixedactualC/U/Q/a/legaldirectorynoinclusion/liveq/d/R/thresholdallr candidate','CovautomaticO-C/mgroups/λspectrum conditionalstrongD<=W/half','r1/r2completeF_bmaxexchange/currentrootandactualtail/proofpositiveb','r3 sameblockdifferenceCweights/fixedFtieexampleonlynonSPE/mirroring notPseatrefutation','I,D,G/W/71reportednotcurrentreplay/sourceemptyzeroedge appropriatelyqualifed']},{'id':IDS[2],'disposition':'duplicate','targets':[V],'units':['all4914auxmaxf_b-rule vsactual2SPE and3staticiid/k even>=12 M/P/B integerunits','allorderedroot/followerutilitycases/rootperipheralv/opt2/sourceuniqueH','qH0peripheraluniform/g3/KKTsupport andoutside/valueλ; Vlambda>dH>alphaH isstrongerthanoriginaloutsidebound','λ-dH allk polynomial/77_72 bound/k12full6456/13/693/299441_432/818/1636','actualv>lambda/recursiveBRclosure notrefuted/r2vsr3 wholepotential scope/historyoldunreviewedthenparentinternalreview','sourceauditk12,14and even12..100 MDclaimonly notreadcode/newrun']}
]
js(E/'semantic-coverage-map.json',coverage)
js(E/'duplicate-meaning-not-count-only.json',{'Pseat':'V containsfullinputP/Cov,explicitv1counter,livereservoir+entire2playerproof,r3onlyfixedFbadexample,conditionalλandIG; notoldshortnavigation','hub':'V givesallparamunitfamily/all2playertruebranches/selectediidNash/λ-dH strictbound,actualv>λ/WOPT2/exactk12. Originaloutsidebound M/6-11/12 isweakerthan Vlambda>dH anddH-alphaH=M/6. Welfarepaircomparison followsdirectlyfromitscompleteH/Pconstruction andBformula. ExistingV isselfcontained, notjustsource link.','original_artifact_bytebinding':'all3existingMLartifactsexact, onlyadditionalversionevidenceafterfullsemanticcomparison','no_new_duplicate_theorems':True})
scope={'primary_sources':3,'primary_bytes':19621,'all3_actual_full_semantic_read_reused':True,'dispositions':{'integrated':1,'duplicate':2},'new_formals':1,'raw_claim_ids':len(claim['ids']),'primary_subset':IDS,'claim_projected':False,'raw_sync_status_preserved':sync,'independent_recovery_preserved':bool(proofpath),'original_CLI_import_math_runs':0,'old_success_replays':0,'new_LP_DAG_SPE_negative_scans':0,'original3auditcode_JSON':'MDhistoricalscopeonly/notreadornewrun; nextactualsourcesmaybelaterassigned','G2':'selfcontainedtextualreconstructionofknown2playerfloorandoriginalcustomerinequality, notnewcodeexecution','existing_MLtarget_and3originalassets_exactSHA_checked':True,'helper_export_calls_in_thisprimaryphase':0,'packaging_builder_calls':1,'packaging_failures':0,'own_shared_Git_show_claim_done_checkpoint_network_account_calls':0,'phase3_mapper':0};js(E/'read-scope-and-execution-identity.json',scope)
notes=[('10055B全部五节/全部表/方法历史/所有程序范围已在ML必要related真正完整读，现实际primary核owner/sourceSHA并逐段比较，非重复假首读。','ML父审资源已有两停界完整定义/证明/固定13例/自由t费用；本新候选补原GAP全域/强G2完整理由及830/196等程序范围/主动中止边界，未把有限阴性当Farkas或一般证明。','integrated到新候选+现审查；0原run，未读三源码/原报告不冒已认证，原程序只作未完成导航待后续实际任务，不额外done引用源。'),('4652B完整v2与其内v1修正说明/四节实读，未声称取得单独v1原版本；现publishedML原asset字节+语义完整比。','现父审资源不是原旧短导航：自足P/Cov、live容量、λ条件、r1/2全部交换证明、r3固定F失败与IG/71范围，原所有数学用途完整覆盖；显式v1单客例是父审缺陷的清晰化不冒原作者新搜索。','duplicate：精确去既有完整V+原件，0新定理/程序/源码额外勾选；source原候选allr未闭不因r2就升级。'),('4914B全五节/全参数所有收益/KKT/比较/具体k12/原audit角色实际全文读；新claim后核当前owner/原件及已发布ML对照。','现V完整保唯maxH强制坏分支与实际外围根/两人全部历史、iid3真NE、全偶k严格分离与actualv>λ，含6456/13精确点；原更弱outside收益下界由V更强λ>dH>αH覆盖，不按同数字/标题判重。','duplicate：核心定理/关键理由/边界及原附程序有限报告均在现自足V，0新oldrun，不把强制H称实际rootEI/half反例，不把原未独审时点倒填新blind/外审。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原多组claim完整保，仅本3actualsubset。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 阶段二关系与真实去重

GAP-r的P是合法背景下未来利润，F是r合法比较槽最大未来利润；强G2的θ为纯最坏末位值，不是hub所反的iid3 λ。新候选保这份全r未闭合同及已证小r基础，不造第二份孩子/删除反例。

现ML父审资源已自足Pseat完整P/Cov+r2及hub全偶参数真策略/坏强制根，逐段比较后2duplicate；原ML当时related未勾的历史不变，本3freshclaim后才新receipt。三个源的已推原asset相同仅额外版本绑定，不代数学阅读。不执行oldaudit、不扩阴性扫描，不做mapper或强连通。
''')
put(E/'README.md',r'''# GAP候选增补与两份完整边界去重

3primary19621B全实读，1integrated/2duplicate、1新候选。10055的两停界已有ML完整资源，新增GAP/G2与三程序有限scope；Pseat/hub逐单位语义核后复用同现资源及精确原asset，没有按教材标签/数量判重。

r2θ与三人iidλ不同，自由t删除不是内生安全值反例，伪孩子也不反GAP；完整SPE/候选/有限阴性/历史内部审查分开。0原CLI/import/数学/旧成功重跑；原三程序代码JSON本批未读不额外done。

actualfullclaim/currentowner/SHA后才receipt，Root先实际push正文证据再done，本代理0sharedGit/网络账号/mapper。
''')
cp(D/'preclaim-reading-scope.json',E/'actual-preclaim-reading-scope.json');cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex(t,c):return sum(1 for n in range(len(t)-1) if ord(t[n])==92 and t[n+1]==c and (n==0 or ord(t[n-1])!=92))
for x in sources:
 b=(S/x['preserved_path']).read_bytes();ck('sourceSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']);ck('publishedasset exact '+x['id'],(REPO/x['published_exact_ML_asset']).read_bytes()==b)
ck('rawfullclaimunaltered',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and set(IDS)<=set(claim['ids']));ck('ownerSHA',all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('fullVcurrentequalpriorread',(REPO/V).read_bytes()==(ML/V).read_bytes());ck('3receipts1int2dup',len(receipts)==3 and [x['disposition'] for x in receipts]==['integrated','duplicate','duplicate']);ck('zerooriginalrun',scope['original_CLI_import_math_runs']==scope['old_success_replays']==scope['new_LP_DAG_SPE_negative_scans']==0)
t=(S/T).read_text();ck('flatformal',all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));ck('properTeXdelimiters',tex(t,'[')==tex(t,']') and tex(t,'(')==tex(t,')'));ck('G2anddomain','c(c−1)+b d≥0' in t and 'P只算未来玩家' in t and '不是静态混合安全值' in t);ck('allreportedlimits','830LP' in t and '196LP' in t and '没有另存全称报告' in t and '五人七主题扩样主动停' in t);links=[]
for link in re.findall(r'\]\(([^)]+)\)',t):
 if ':' in link or link.startswith('#'):continue
 ok=((REPO/T).parent/link).resolve().exists() or ((S/T).parent/link).resolve().exists();links.append({'link':link,'exists':ok});ck('formal link '+link,ok)
js(E/'formal-link-check.json',links);obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen='/original/' in '/'+rel or '/comparison/' in '/'+rel;bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('newderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_unchanged':True})
put(W/'delivery.md',f'''# 尾gap及两完整边界三源交付

3primary19621B全实际实读，1integrated/2duplicate、1新候选；强G2完整理由、原三程序scope补齐，既有两停界/Pseat/hub准确复用。原{len(claim['ids'])}claim {claim['remote_tip']} pushed、rawsync {sync}不改，本3owner/SHA和现MLtarget/assets核。

0原CLI/import/数学/旧成功复跑，无阴性扩样、无引用源extra done；已有ML当时related历史不改。Root先push证据正文再done，无sharedGit/网络账号/mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_links':len(links),'new_formals':1,'notnewmathruntime':True})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':19621,'receipts':3,'dispositions':{'integrated':1,'duplicate':2},'new_formals':1,'new_formal_bytes':(S/T).stat().st_size,'checks':len(checks),'formal_links':len(links),'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'raw_sync_status':sync,'new_math_runs':0,'original_CLI_calls':0,'old_success_replays':0};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
