from pathlib import Path
import json,hashlib,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='terminal-menu-independent-audit-and-author-scope-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');D=C/'next-terminal-menu-audit-and-author-drafts'
IDS=['001650a89c69229a86fe','d72ca414ac74c7116073','b8547eb21def15139ffe'];P='archives/customer-attraction/state/程序/八标签静态匹配与末位全回复的独立有理审计--程序.md';O='archives/customer-attraction/state/障碍/八标签末位真回复菜单的第二人偏离--障碍.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 dest=S/q;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(Path(p).read_bytes())
# This gate executes before any successful receipts/stage files are written.
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='needs-attention' and set(IDS)<=set(claim['ids']) and len(claim['ids'])==18 and claim['remote_tip']=='a322a20bf56ba482c0428cf9f3fc5790c4281bf6'
resolutionpath=C/'boss4-r3-next-lp-lq-lr-ls-atomic-claim-sync-preservation.json';resolution=json.loads(resolutionpath.read_text());assert resolution['stash'] in claim['local_sync']['detail'] and resolution['stash_kept'] and resolution['missing']==resolution['different']==[] and resolution['unmerged']=='' and resolution['untracked_count']==2 and len(resolution['tracked'])==2 and all(x['same'] for x in resolution['tracked'])
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};mf=C/'lf-next-menu-review-and-author-local-inputs/local-export-manifest.json';m=json.loads(mf.read_text());sources=[];owners=[]
for i in IDS:
 x=next(x for x in m['rows'] if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==x['size']==v['size'] and sha(b)==x['sha256']==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/v['path'];cp(x['local_path'],q);sources.append({**v,'preserved_path':str(q),'read_scope':'allactualoriginaltextfullcode/allJSONfields/authorall7sections fullread beforeactualclaim; notfalsenewfirstreading/noexecution'})
assert sum(x['size'] for x in sources)==16422
js(E/'source-manifest.json',sources);js(E/'actual-owner-snapshot.json',owners);cp(mf,E/'actual-local-source-manifest.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json');cp(resolutionpath,E/'actual-independent-sync-resolution.json')
contextpaths=[O,'archives/customer-attraction/state/反例/三人聚合末位保底--反例.md','archives/customer-attraction/state/障碍/自适应后继与真实菜单安全值--障碍.md','archives/customer-attraction/state/障碍/缺少尾部理性的环边阈值扩展障碍--障碍.md'];contexts=[]
for p in contextpaths:
 b=(REPO/p).read_bytes();q=E/'comparison'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_scope':'actualcompleteformalmathematicaltextread; LFobstruction fullbodywrite/read reused afteractualpublication, no additional oldsource done'})
lf=C/'r3-shared-omission-audit-and-terminal-menu-review-primary';assert (REPO/O).read_bytes()==(lf/O).read_bytes();js(E/'comparison-manifest.json',contexts)
relatedids=['30b5ae056026b69161f3','ca6e67cdedf4bf541f54'];relatedmf=C/'terminal-menu-after-independent-audit-local-candidates/local-export-manifest.json';relatedrows=[]
for x in json.loads(relatedmf.read_text())['rows']:
 if x['id'] not in relatedids:continue
 b=Path(x['local_path']).read_bytes();v=inv[x['id']];assert len(b)==v['size'] and sha(b)==v['sha256'];q=E/'necessary-related-original'/x['id']/v['path'];cp(x['local_path'],q);relatedrows.append({**v,'preserved_path':str(q),'read_scope':'actualfullsourcecodeandall16menurecords/12masks read asnecessary implementationcomparison; notprimaryreceipt/notrun'})
js(E/'necessary-related-manifest.json',relatedrows)
refs=[f"source:{z['commit']}:{z['path']}" for i in IDS+relatedids for z in inv[i]['sources']]
front=['---','id: customer-attraction/eight-label-independent-symbolic-terminal-menu-audit','kind: program','type_tag: 程序','title: 八标签静态匹配与末位全回复的独立有理审计','status: original-exact-finite-and-symbolic-report-reviewed; no-new-run','summary: 全120静态多重集及开扇形512末位系数审计，七组全单位终局与作者发现身份保真，不混入OPT或第二人全表职责。','source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs]+['---','',(D/'program-body.md').read_text()];put(Path(P),'\n'.join(front))
assetlinks=['\n## 原件与可复核资源\n']
for x in sources+relatedrows:
 assetlinks.append('- ['+x['id']+' '+str(x['size'])+' B 原件](../../../../'+x['preserved_path']+')')
put(Path(P),(S/P).read_text()+'\n'.join(assetlinks)+'\n')
report=json.loads((S/sources[1]['preserved_path']).read_text());code=(S/sources[0]['preserved_path']).read_text()
coverage=[{'id':IDS[0],'disposition':'integrated','targets':[P],'units':['allimports/constants/helpers/main/noexternalinputs','120backgroundlowercoefficientforallnonnegative/8upper/8minimizers','24menucollabelcoeff/512allterminalBRconecompareincludingties/unique02a>0b>=0/second02coeff','7all8^3*3unitidentity/differences/degeneracy','mainfullstdout/exclusiveoutputafterchecks/notOPTnotfullsecondtable/0run']},{'id':IDS[1],'disposition':'integrated','targets':[P],'units':['status/blindstring/120/8upper/8minimizers/24/512/all8coeffpairs','all7numericrowsN1536defv/BRsets/chosen5deviationgain/alllimits','noexecutionSHAargvversionlog/co-versionnotnewrun']},{'id':IDS[2],'disposition':'integrated','targets':[O,P],'units':['all7sections coremathfullyLFduplicate/themedistinctequalcardmaximal','36realSPEtheta12notv10/allbranchesroot10tail12/debtfreeconvexpaymentobstacle','minimalbadpoint conditional trueprefixstructure notpuremenu orcurrentOPEN','a4b50N232root33tail37,58v37/second60last62/discoverynotmincert','authorauditcode/report2actualfullrelated/16menus/12masks/bitsaggregatedFraction/twofixedsamples/OPT checked/fixedsidecaroverwrite; no extra done','remainingprobe/outputnames finite discovery and<=6negative limit notread notdone','historicalmixedmenuspostnumbers/rootplannedreview/stopscan/currentbank/five correction']}]
js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':3,'primary_bytes':16422,'all_originals_actual_full_semantic_read':True,'raw_claim_ids':len(claim['ids']),'actual_primary_subset':IDS,'raw_claim_projected':False,'raw_local_sync_status_preserved':'needs-attention','independent_sync_resolution_stash':resolution['stash'],'independent_allbytes_preserved':True,'source_code_bytes':5624,'frozen_JSON_bytes':3412,'author_MD_bytes':7386,'new_formals':1,'new_original_CLI_calls':0,'new_original_imports':0,'new_math_runs':0,'old_success_replays':0,'new_solver_LP_BI_SPE_random_checks':0,'new_derived_packaging_calls':2,'packaging_failures':0,'current_actualfullformalcontexts':4,'necessary_related_author_audit_sources':2,'necessary_related_author_audit_bytes':9747,'author_other_audit_and_probe_files':'author2fullrelated/no newreceipt/norun; cyclic2byteonly beforeseal','safe_local_helper_preparing_next4_calls':1,'next_exports':4,'next_missing':0,'own_shared_Git_claim_done_checkpoint_show_network_auth_calls':0,'phase3_mapper':0,'read_vs_execution':'source and allfrozen reportsemanticreading, fieldbindingnotnewmathematicalauditexecution; originalJSONnocodeSHAorindependentargvlog'};js(E/'read-scope-and-execution-identity.json',scope)
notes=[('5624B全部源码/常量/函数/main/写入时序实际完整读，原件size/SHA256/blob与库存和新owner核；0import/CLI。','LF障碍的完整数学已另发布；新程序资源精确补120静态背景/8双证/24系数/512全末位BR开扇形/唯一02/七单位全终局。代码不核OPT3或完整第二收益表，不与作者audit同名混绑；后者3078/6669已必要related全文比较，仅两固定正参数/确查OPT/块聚合/固定sidecar覆盖与此独审接口分清。','integrated，保符号a,t>0的全锥义务及有限样本真实作用、默认fullpayload与后置open(x)，无需重复旧成功。'),('3412BJSON全部字段/八上背景/八共同minimizers/八系数/七组全numeric与limits完整实读。','新程序对象完整两表及全部非表字段保，包括a0b1的5非唯一、1/2只选定分支；a2b9/a2b25窗口等号与零边界保。原blind字符串不冒本轮盲审，原wholeSHA不是程序执行日志。','integrated；原输出无sourceSHA/argv/Python/exit/time，不造重跑或独立日志，0新有限数学计算。'),('7386B作者七节完整原文已读，rootordering/安全值/窗口/唯一偏离/OPT及所有证据角色保；两原版本同SHA核。','核心解析数学与现LF障碍完全对应，不造第二份定理；独有36真实SPE theta≠v/最小坏点条件/232发现点/八theme最大性及作者两audit必要全文比较/未读发现probe导航，在新程序资源完整保。当前36formal全读比较，不由作者历史句直接升级证明。','integrated至旧障碍+新程序对象；原OPEN由后续银行/五人更新，原独审计划/收到数字再重构不冒新blind或外审，作者audit仅related不extra done、其余probe未读不extra done。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 完整多组原claim仅取本3实际subset，不投影改原ids。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 阶段二关系

LF障碍负责完整静态匹配证明、末位/第二全表和SPE不可补全；本程序负责独立review实现精确义务及原全部输出，作者主稿独有232发现点/前置付款动机/历史证据范围保到程序资源。源作者与独审两个先后角色分开，不把相同主题实例造为两个数学定理。

36客户源在这里仅比较已证明的theta聚合失败：theta12≠真正v10≠受限菜单z11。真实菜单旧障碍与缺末位BR的环边菜单层次不同；新八标签已保末位BR，失败在第二真实IC。此对应不否定全位置/聚合安全桥或sixhalf，不强制图连接，不导入阶段三图。
''')
put(E/'README.md',r'''# 八标签独立审计的代码/输出和作者角色

3primary16422B均实际全文实读。新1程序对象精确保5624Bstdlib/Fraction代码和3412B原JSON全部字段，另9747B作者audit必要related源码/两全输出比较；7386B作者核心数学已LF障碍准确覆盖，独有36theta动机/最小坏点条件/232发现点及原导航全部保。

代码真核120静态背景、8上分布、24菜单系数、512末位开扇形系数、唯一02、7×1536单位终局。它不核OPT或完整第二收益表。七样本不是全参数证明，符号射线断言与已自足解析页分别承担全域理由。

原执行次数/argv/版本/sourceSHA日志缺失则保缺失；0原CLI/import/数学/旧成功重跑。本轮先读两方不能变新盲审。actualclaim完整多组原字节+本3owner/SHA后才生成成功receipt；Root先推再done，无sharedGit/网络/账号/mapper。
''')
cp(D/'preclaim-reading-scope.json',E/'actual-preclaim-reading-scope.json')
nextmf=C/'terminal-menu-after-independent-audit-local-candidates/local-export-manifest.json';nm=json.loads(nextmf.read_text());assert len(nm['rows'])==4 and nm['missing']==[];nextrows=[]
for x in nm['rows']:
 b=Path(x['local_path']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256'];owner=REPO/'cleanup/progress'/f"{x['id']}.json";assert not owner.exists();nextrows.append({**inv[x['id']],'local_path':x['local_path'],'owner_observed':None,'read_status':('actualfullrelatedsemanticreadnotprimaryreceipt/norun' if x['id'] in relatedids else 'byteverifiedonlybeforethisseal; notyetsemanticread/claim/receipt/run')})
cp(nextmf,E/'next-original-local-manifest.json');js(W/'next-candidates.json',nextrows);cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in sources:
 b=(S/x['preserved_path']).read_bytes();ck('source byte '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('source blob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('rawfullclaimunaltered',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and set(IDS)<=set(claim['ids']));ck('raw18claim_recovery_preserved',(S/E/'actual-independent-sync-resolution.json').read_bytes()==resolutionpath.read_bytes() and claim['local_sync']['status']=='needs-attention' and resolution['stash_kept'] and resolution['missing']==resolution['different']==[] and resolution['unmerged']=='');ck('ownerSHA',all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('LFpublishedtargetexact',(REPO/O).read_bytes()==(lf/O).read_bytes());ck('all16422bytes',sum(x['size'] for x in sources)==16422)
ck('frozen120_24_512',report['static_uniform_lower_backgrounds']==120 and report['menu_payoff_coefficients_checked']==24 and report['all_terminal_coefficients_checked_on_a_positive_b_greater_a']==512);ck('all8backgrounds_minimizers_coeff',len(report['matching_static_upper_distribution'])==len(report['common_lower_minimizers'])==len(report['last_after_0_2_coefficients_a_b'])==8);ck('all7unitcases',[(x['a'],x['b']) for x in report['numeric_unit_cases']]==[(1,5),(2,9),(2,25),(1,1),(1,0),(0,1),(0,0)] and all(x['terminal_payoff_checks']==1536 for x in report['numeric_unit_cases']));ck('degenerateBRnotunique',report['numeric_unit_cases'][5]['br_after_0_2']==[1,3,5,7] and report['numeric_unit_cases'][5]['second_deviation_gain']=='1/2' and report['numeric_unit_cases'][6]['br_after_0_2']==list(range(8)));ck('noexecutionidentity',not any(k in report for k in ['source_sha256','argv','python','elapsed','exit_code']));ck('sourceoutputafterchecks',code.index('numeric.append(')<code.index('args.output.open("x")')<code.index('print(payload)'));ck('main_guard','if __name__ == "__main__"' in code);ck('noOPTassertsource','optimum' not in code and 'OPT3' not in code);ck('symbolicconeactualcode','delta[0]+delta[1] >= 0 and delta[1] >= 0' in code and 'delta[0]+delta[1] > 0 or delta[1] > 0' in code)
t=(S/P).read_text();ck('flatformal',all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));ck('scopekept','实际代码没有枚举OPT3' in t and 'a0b1末位5不唯一' in t);ck('author232kept','232客户点' in t and '(33,37,58,37)' in t);ck('3receipts',len(receipts)==3 and {x['id'] for x in receipts}==set(IDS) and all(x['disposition']=='integrated' for x in receipts));ck('zerooriginalexecution',scope['new_original_CLI_calls']==scope['new_original_imports']==scope['new_math_runs']==scope['old_success_replays']==0)
links=[]
for link in re.findall(r'\]\(([^)]+)\)',t):
 if ':' in link or link.startswith('#'):continue
 ok=((S/P).parent/link).resolve().exists() or ((REPO/P).parent/link).resolve().exists();links.append({'link':link,'exists':ok});ck('formal link '+link,ok)
js(E/'formal-link-check.json',links)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:tx=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen='/original/' in '/'+rel or '/comparison/' in '/'+rel;bad=[i+1 for i,l in enumerate(tx.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(tx) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('newderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_unchanged':True})
put(W/'delivery.md',f'''# 三源原审计/作者范围完整交付

3primary16422B全实读，3integrated/1新程序对象。LF完整数学精确复用不重复造定理；本对象补原实际assert、全原JSON和作者独有232点/36theta动机/条件最小坏点及历史导航。

原{len(claim['ids'])}多组claim {claim['remote_tip']} pushed、原local_sync needs-attention不改，独立187e998恢复证据2tracked/2untracked全同、无missing/different/unmerged/stash保留，本3owner/SHA核。0原CLI/import/数学/旧成功重跑，不把wholeSHA/报告blind字符串造独立执行/新盲审。

下一4实际本地齐19848B，封包前作者audit2已全文related、发现probe2仅byte，均未claim/receipt/运行不冒新认证。Root先正常push正文/证据再done，代理无sharedGit/网络/账号/mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_links':len(links),'not_new_math_execution':True,'new_formals':1})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':16422,'receipts':3,'dispositions':{'integrated':3},'new_formals':1,'new_formal_bytes':(S/P).stat().st_size,'checks':len(checks),'formal_links':len(links),'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'raw_sync_status':'needs-attention-original-preserved-with-independent-recovery','new_math_runs':0,'original_CLI_calls':0,'old_success_replays':0,'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
