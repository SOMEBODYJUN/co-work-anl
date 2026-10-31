from pathlib import Path
import hashlib,json,re,sys
R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';SLUG='cyclic-complete-credibility-and-parent-review-primary';S=C/('r3-'+SLUG);E=Path('tools/evidence')/SLUG;W=Path('cleanup/workspaces/Boss4')/('r3-'+SLUG+'-next');D=C/'cyclic-full-spe-classification-drafts';IDS=['44b9984032aaaf8c1c03','b5c500d25729ef39128d','0529db2ca84292e185cb','b8d2b3fae6f6787ee50a','88ae2e8b7ad81e7d0bb1'];RELATED=['6b953dda924f48243d6b','857599e66de0a1b953e9','734269b6e8a84cfea402'];T='archives/customer-attraction/state/定理/八标签圆环族的完整可信子局与最小首位收益--定理.md';V='archives/customer-attraction/state/审查/圆环可信性父审的旁支合同与证据身份--审查.md';OB='archives/customer-attraction/state/障碍/八标签末位真回复菜单的第二人偏离--障碍.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 d=S/q;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(Path(p).read_bytes())
# Gate before any primary receipt/stage mutation. This is not a claim command.
claimpath=Path(sys.argv[1]);claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids']);sync=claim['local_sync']['status'];proofpath=None
if sync=='needs-attention':
 proofpath=Path(sys.argv[2]);proof=json.loads(proofpath.read_text());assert proof['stash'] in claim['local_sync']['detail'] and proof['stash_kept'] and proof['missing']==proof['different']==[] and proof['unmerged']=='' and all(x['same'] for x in proof['tracked'])
else:assert sync=='synced'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};mps=[C/'relay-cyclic-full-spe-next-local-inputs/local-export-manifest.json',C/'relay-cyclic-full-spe-required-local-inputs/local-export-manifest.json',C/'cyclic-parent-review-needed-math-local-inputs/local-export-manifest.json'];rows=[x for p in mps for x in json.loads(p.read_text())['rows']];sources=[];related=[];owners=[]
for i in IDS+RELATED:
 v=inv[i];x=next(x for x in rows if x['id']==i);b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/('original' if i in IDS else 'necessary-related-original')/i/v['path'];cp(x['local_path'],q);row={**v,'preserved_path':str(q),'read_scope':'actualentireprimaryornecessaryrelated MD/code/allJSON3regions6instances fullysemanticallyread beforeactualclaim, notfakefirstread/no originalexecution'};(sources if i in IDS else related).append(row)
 if i in IDS:
  owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner)
assert sum(x['size'] for x in sources)==26767 and sum(x['size'] for x in related)==19621
js(E/'source-manifest.json',sources);js(E/'necessary-related-manifest.json',related);js(E/'actual-owner-snapshot.json',owners);cp(claimpath,E/'actual-unprojected-claim-receipt.json')
if proofpath:cp(proofpath,E/'actual-independent-sync-resolution.json')
for n,p in enumerate(mps):cp(p,E/'actual-local-manifests'/f'input-{n+1}.json')
contextpaths=[OB,'archives/customer-attraction/state/障碍/固定旧背景正信用与连续调和替换的停界--障碍.md','archives/customer-attraction/state/障碍/聚合尾部删除稀释恒等式--障碍.md'];contexts=[]
for p in contextpaths:
 b=(REPO/p).read_bytes();q=E/'comparison'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_scope':'actualfullformaltext semanticcomparison; generalD3D9/Pseatshortnavigationnotfullparentreviewduplicate'})
assert (REPO/OB).read_bytes()==(C/'r3-shared-omission-audit-and-terminal-menu-review-primary'/OB).read_bytes();js(E/'comparison-manifest.json',contexts)
def formal(p,id,title,kind,typ,status,summary,ids,body):
 refs=[f"source:{x['commit']}:{x['path']}" for i in ids for x in inv[i]['sources']];front=['---','id: '+id,'kind: '+kind,'type_tag: '+typ,'title: '+title,'status: '+status,'summary: '+summary,'source_refs:']+['  - '+json.dumps(x,ensure_ascii=False) for x in refs]+['---','',body];put(Path(p),'\n'.join(front));assets=[x for x in sources+related if x['id'] in ids];put(Path(p),(S/p).read_text()+'\n## 原件与证据资源\n\n'+'\n'.join('- ['+x['id']+' '+str(x['size'])+' B 原件](../../../../'+x['preserved_path']+')' for x in assets)+'\n')
formal(T,'customer-attraction/cyclic-eight-label-complete-SPE-minimum-root-classification','八标签圆环族的完整可信子局与最小首位收益','theorem','定理','proved-for-entire-positive-integer-family; original-symbolic-report-reviewed-no-new-run','三域完整BR/孩子SPE充要阈值，Umin与Wmin分段及两73节点策略达到，危险菜单不能补成真EI反例。',IDS,(D/'theorem-body.md').read_text())
formal(V,'customer-attraction/cyclic-parent-review-auxiliary-contracts-and-evidence','圆环可信性父审的旁支合同与证据身份','review','审查','historical-internal-review-and-self-contained-auxiliary-scope; no-new-independent-runtime-audit','保父审先验及GAP伪摘要、自由t删除45/2对11ε、坏maxhub规则和PseatCov/r2边界，引用源不额外done。',[IDS[2],IDS[0]]+RELATED,(D/'parent-review-resource-body.md').read_text())
report=json.loads((S/sources[-1]['preserved_path']).read_text());code=(S/sources[-2]['preserved_path']).read_text();coverage=[{'id':IDS[0],'targets':[T,V],'units':['all3199READMEhistoricalroles/oldOPEN/paths/28menu/232audits/500scope','newcompleteclassificationentry/73and584accuratesourcecontract/currentbankandfivevs-six','alllinkedcode/reportnotactuallyread notfaked/relatedsource5noextra done']},{'id':IDS[1],'targets':[T],'units':['all7sectionsunitfamily/domain/positive-real-vs-integer/completepureSPEquantifiers','all3regimeBR/reflection/L=maxmin/CHILD iff/tieindependenthistorysufficiency','8vs6feasiblepairs/rootmin/welfare/allSPEoptimalb>a/b=a jump','twofullrelativepolicies/all73orderedhistories/strictv4comparison/currentfalsegeneralEI andopenothers']},{'id':IDS[2],'targets':[T,V],'units':['full3667allsections/independentpriorcyclicthencompare/historyscope','GAPdefinition+rdisjointkunitpseudo summaryproof/fixeddepthnotwholechildSPE','13realreportdata/deletionconservation/freeεnotendogenoust/Γ45/2vs11ε','sharedKQCONST reused/maxstandalonehubactualSPEv>lambda/no EIcounter','Pseatv1Covfix/fullv2r2exchange/r3onlyfixedFbadmenu/I,G71limit','independentotherauditpy/jsonnotread/notnewblind; related3fullforsemanticsnotextradone']},{'id':IDS[3],'targets':[T],'units':['all5060code/stdFraction/symboliccoeffmaps/rootsecondlast','nonnegative3regions endpoint/slope/strictness; BR/minBR/L/feasible/rootfloor assertions','6numericfull73/584,exactuniform120lower notexplicitupper/OPTliteralnotsearch','no mainguard top-levelclassification+6audit+fixedoverwrite/stdoutinstancesonly/no CLI/import']},{'id':IDS[4],'targets':[T],'units':['all7476JSON3regions/full8BRs/8,8,6feasible/rootmin/securitycoeff','all6casefields73/584/terminal/rootmin/v4/gap/L/childsets/WminOPT/status','sourceversionco-locationnotactualexecutionhash/argv/versionlog/current0run']}];js(E/'semantic-coverage-map.json',[dict(x,disposition='integrated') for x in coverage])
scope={'primary_sources':5,'primary_bytes':26767,'necessary_related_sources':3,'necessary_related_bytes':19621,'all8_actual_full_semantic_read':True,'new_formals':2,'dispositions':{'integrated':5},'raw_claim_ids':len(claim['ids']),'primary_subset':IDS,'claim_projected':False,'raw_sync_status_preserved':sync,'independent_recovery_preserved':bool(proofpath),'actual_existingfullformalcomparisons':3,'oldfullpositivefamilyproof_uses_symbolic_classification_and_policy':'notfromsixsampleextrapolation','original_import_CLI_math_runs':0,'old_success_replays':0,'new_LP_SPE_BI_or_negative_scans':0,'independent_parent_cyclic_audit':'MDhistoricalassertion only notreadcode/report/notnewexternalreview','other13DAG_and_hub_audit':'MDrelatedfullread, code/packet notreadornewrun here','initial_materialization_calls':3,'initial_exports':8,'initial_missing':0,'materialization_phase':'beforeclaimalreadyrecordedinprecedingMDpreparation, nonewreadretryafterclaim','packaging_builder_calls':2,'packaging_failures':1,'own_shared_Git_show_claim_done_checkpoint_network_account_calls':0,'phase3_mapper':0};js(E/'read-scope-and-execution-identity.json',scope)
notes=[('3199B全部入口/历史状态/菜单与完整分类/每个导航原先实读，actual新claim仅本5交集和owner/sourceSHA核。','新定理保全部可信性全参数内容，审查资源保真实独审时序和各源码/报告角色；既有LF只菜单失败，不能因同8标签判整页duplicate，旧500/28/232已MD/LQ/LX资源明确去向。','integrated到两正式对象；旧OPEN/no-sharedClaim是历史，原角色规则不执行，不对引用来源额外done。'),('7365B全7节/所有表/证明/参数/两完整策略实读，finite/fullSPE/每份量词逐项保。','新定理自足CHILD必要充分/L阈值/两分段UminWmin与达到性，包含b=a真实平局跃变；现LF仅b>a菜单障碍不包含完整族最小均衡分类。','integrated；普遍结论由解析有限表+全历史策略，不由六有限例外推，不证明一般EI/half。'),('3667B父审全所有段实读，必要3related原稿19621B全读补其未展开定义/精确费用/候选假设。','新审查资源自足GAP-r伪孩子总结反例、固定d末尾范围、删除守恒与13人自由t无界比、maxhub强制坏分支但真SPE好、PseatCov及r≤2/三人缺口；现普通D3D9/短导航全文比均非整页覆盖。','integrated；先盲后对照只原角色历史，parent独立audit另两文件未读/13DAG与hub原code未执行不冒cert，不额外done3related、不把一般EI/Mfull旧OPEN继承现在。'),('5060B原源码所有全局执行/函数/系数表/三域循环/六实例/写入输出完整实读，未import/CLI。','定理保真实仿射程序义务及六73/584原报告，代码没有main guard，uniform120仅下界比值/OPT返回公式不冒上证或优化枚举，stdout仅instances与文件wholeout区别保。','integrated；0原成功复跑/新solver，原SHA绑定是字节版本非独立运行日志，源码自带assert不是本轮已执行。'),('7476B全JSON每个三域BR/可行对/两系数数组与六参数全标量/所有child列表实读。','定理完整BR反射表/8vs6全集与六报告数值表全部保，状态字符串归原有限报告；对应所有正参数证明来自解析，不只是count/hash。','integrated；原无sourceSHA/argv/Python/exit/time日志不发明，0新的数学运行/全树复核扩样。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' full多组原receipt原样不投影，实际primaryonly。','comparison_note':b,'decision_note':c,'disposition':'integrated','targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 阶段二关系

同一八标签族的浮点发现、指定末位BR菜单失败、独审实现和这里完整SPE分类角色不同。新定理用完整孩子BR+最低可信阈值的iff保全部早期IC，不造第二份菜单定理，亦不把本族正结论推广一般EI。

父审跨四旁支是审查来源而非一个新万能钱包。GAP伪列只反摘要归纳；自由t删除只反deficit-only；坏hub是强制根并非actual；Pseat只补Cov并证r2/保r3未闭。相关3完整原稿仅必要比较，不额外done或制造mapper/图连通。
''')
put(E/'README.md',r'''# 完整圆环可信性与父审旁支

5份primary共26767 B，另3份必要related共19621 B全部完整实读，2自足正式对象/5integrated。圆环定理保全参数BR/L/CHILD iff/两段UminWmin/两73节点策略和六实例全表；父审资源完整保其他数学的模型、费用、缺口与独立时序。

原5060程序top-level立即分类/六audit/覆盖固定JSON，本轮0import/CLI。原输出无执行SHA/独立argv日志；uniform静态下界与OPT literal不冒源码未核的上对偶/OPT搜索。父审独立程序、13DAG/hub audit本批未跑也不假认证。

raw多组claim与rawsync原字节、owner/SHA门控后才receipt，必要时Root独立恢复另保。Root先实际push正文/证据再done；0sharedGit/网络账号/mapper/旧成功复跑。
''')
cp(D/'reading-scope.json',E/'actual-preclaim-reading-scope.json');cp(C/'ml-format-checker-recovery.json',E/'derived-format-checker-recovery.json');cp(Path(__file__),E/'build_delivery.py');nextrows=[]
for x in related:
 p=REPO/'cleanup/progress'/f"{x['id']}.json";owner=json.loads(p.read_text()) if p.exists() else None
 if owner is None:nextrows.append({**inv[x['id']],'local_path':next(y['local_path'] for y in rows if y['id']==x['id']),'owner_observed':None,'read_status':'actualfullnecessaryrelatedread butnotprimarydone; rootmayassignlater, no preclaim'})
js(W/'next-candidates.json',nextrows)
checks=[]
def texcounts(t,c):return sum(1 for n in range(len(t)-1) if ord(t[n])==92 and t[n+1]==c and (n==0 or ord(t[n-1])!=92))
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in sources+related:
 b=(S/x['preserved_path']).read_bytes();ck('sourceSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('rawclaimunaltered',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and set(IDS)<=set(claim['ids']));ck('ownerSHA',all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('3affine6instances',len(report['affine_regions'])==3 and [x['region'] for x in report['affine_regions']]==['lt','eq','gt'] and len(report['instances'])==6);ck('feasiblecounts8_8_6',[len(x['feasible']) for x in report['affine_regions']]==[8,8,6]);ck('all6samplefields',[(x['a'],x['b']) for x in report['instances']]==[(2,1),(1,1),(1,2),(1,5),(4,50),(1,100)] and all(x['nodes']==73 and x['comparisons']==584 for x in report['instances']));ck('codehasnomain', '__main__' not in code and "(HERE/'cyclic_family_complete_spe_audit.json').write_text" in code and "print(json.dumps(out['instances']" in code);ck('noexecutionmetadata',not any(k in report for k in ['source_sha256','argv','python','exit_code','elapsed']));ck('5completereceipts',{x['id'] for x in receipts}==set(IDS) and all(x['disposition']=='integrated' for x in receipts));ck('zerooriginalruns',scope['original_import_CLI_math_runs']==scope['old_success_replays']==scope['new_LP_SPE_BI_or_negative_scans']==0)
links=[]
for p in [T,V]:
 t=(S/p).read_text();ck('flat '+p,all('\n'+k+':' in t for k in ['id','kind','type_tag','title','status','summary','source_refs']));ck('balancedTeX '+p,texcounts(t,'[')==texcounts(t,']') and texcounts(t,'(')==texcounts(t,')'))
 for link in re.findall(r'\]\(([^)]+)\)',t):
  if ':' in link or link.startswith('#'):continue
  ok=((REPO/p).parent/link).resolve().exists() or ((S/p).parent/link).resolve().exists();links.append({'from':p,'link':link,'exists':ok});ck('link '+link,ok)
js(E/'formal-link-check.json',links)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen='/original/' in '/'+rel or '/necessary-related-original/' in '/'+rel or '/comparison/' in '/'+rel;bad=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(t) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('derivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_unchanged':True})
put(W/'delivery.md',f'''# 圆环完整分类与父审五源交付

5份primary共26767 B，另3份必要related共19621 B全部真实完整读，5integrated/2正式对象；全参数论证与原有限软件范围/各旁支费用量词分开。原{len(claim['ids'])}claim {claim['remote_tip']} pushed、rawsync {sync}不改，本5owner/SHA核。

0原CLI/import/数学/旧成功复跑，原top-level程序不执行；原无执行log不发明。3related不extra done。Root先push证据正文再done，无sharedGit/网络账号/mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'formal_links':len(links),'new_formals':2,'notnewmathruntime':True})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':26767,'necessary_related_bytes':19621,'receipts':5,'dispositions':{'integrated':5},'new_formals':2,'new_formal_bytes':sum((S/p).stat().st_size for p in [T,V]),'checks':len(checks),'formal_links':len(links),'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'raw_sync_status':sync,'new_math_runs':0,'original_CLI_calls':0,'old_success_replays':0,'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
