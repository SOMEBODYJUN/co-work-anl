from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-r2fc-independent-review-aliases-primary';E=Path('tools/evidence/r2fc-independent-review-aliases-primary');W=Path('cleanup/workspaces/Boss4/r3-r2fc-independent-review-aliases-primary-next');IDS=['3ca59320d9a683dcd8bc','992b04bab8f16d66d7de','6b66b057437b1c9c596c'];GE=C/'r3-r2fc-coverage-security-and-review-entries-primary';GEE=Path('tools/evidence/r2fc-coverage-security-and-review-entries-primary')
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
claimpath=R/'boss4-r3-next-gm-claim.json';claim=json.loads(claimpath.read_text());respath=C/'boss4-r3-next-gm-gn-go-atomic-claim-sync-preservation.json';resolution=json.loads(respath.read_text())
assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids'])
assert claim['local_sync']['status']=='needs-attention' and resolution['stash'] in claim['local_sync']['detail']
assert resolution['receipt']=='boss4-r3-next-gm-gn-go-atomic-claim' and resolution['missing']==resolution['different']==[] and resolution['unmerged']=='' and resolution['stash_kept'] is True and resolution['untracked_count']==2 and len(resolution['tracked'])==2 and all(x['same'] for x in resolution['tracked'])
owners=[]
for i in IDS:
 x=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[i]['sha256'];owners.append(x)
cp(claimpath,E/'actual-unprojected-claim-receipt.json');cp(respath,E/'independent-sync-preservation-resolution.json');js(E/'actual-primary-ownership-snapshot.json',owners)
source_rows=[];raw=json.loads((GE/GEE/'related-source-manifest.json').read_text());oldaliases=json.loads((GE/GEE/'independent-review-original-aliases.json').read_text());oldctx={x['path']:x for x in json.loads((GE/GEE/'context-manifest.json').read_text())};targets={};aliases=[]
for x in raw:
 assert x['id'] in IDS;b=(GE/x['preserved_path']).read_bytes();v=inv[x['id']];assert len(b)==v['size'] and sha(b)==v['sha256'];q=E/'original'/x['id']/x['path'];cp(GE/x['preserved_path'],q);source_rows.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_status':'full actual original math read GE as necessary related; GM sameSHA reuse, not new first reading'})
 a=next(a for a in oldaliases if a['related_source_id']==x['id']);v=a['canonical_source'];p=REPO/'cleanup/progress'/f"{v['id']}.json";pr=json.loads(p.read_text());assert pr['disposition']=='integrated' and pr['source_sha256']==v['sha256']==x['sha256'];assert v['size']==x['size'] and v['blob']==x['blob'];aliases.append({'primary_id':x['id'],'canonical_source':v,'canonical_current_progress':pr,'same_size_SHA256_blobSHA1':True,'identity_basis':'frozen inventory and actual workspace bytes bind to the same content object; no newly exported/re-read canonical original','original_GE_related_manifest':str(GEE/'related-source-manifest.json')})
 for n in pr['targets']:
  z=(REPO/n).read_bytes();assert sha(z)==oldctx[n]['sha256'];q=E/'target-snapshots'/n;cp(REPO/n,q);targets[n]={'path':n,'snapshot':str(q),'bytes':len(z),'sha256':sha(z),'read_status':'GE fully read mathematical target; GM current sameSHA recheck only, no redundant reread'}
js(E/'source-manifest.json',source_rows);js(E/'canonical-alias-and-done-binding.json',aliases);js(E/'existing-target-manifest.json',list(targets.values()));cp(GE/GEE/'actual-related-local-supply-manifest.json',E/'prior-complete-source-supply.json')
scope={'primary_sources':3,'primary_bytes':sum(x['size'] for x in source_rows),'primary_lines':sum(x['lines'] for x in source_rows),'read_reuse':'all3 complete original independent proofs actually read GE, currentGM sameSHA byte checked; existingcanonical targets GEfullread currentSHAunchanged','canonical_alias_sources':['781c2fa3ff062d072d72','34736d33cf814fa93dcd','af985f9071d31ebfd9f4'],'existing_math_targets':len(targets),'new_formal_math_objects':0,'duplicate_decision_basis':'exact content identity and actual complete unique-content-to-existing-target map, not filename/count/oldPASS','raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'raw_claim_local_sync_status':claim['local_sync']['status'],'raw_claim_modified':False,'independent_recovery_evidence':'Root supplied exact preservation capture:stash90bb618e...2tracked+2untracked same,0missing/different/unmerged,stashkept;current3owner/sourceSHA checked','independent_resolution_file':str(respath),'new_original_CLI_calls':0,'new_math_or_SPE_or_LP_runs':0,'old_success_replays':0,'new_canonical_full_rereads':0,'new_safe_helper_calls':2,'new_local_blob_attempts':7,'new_local_exports':7,'new_missing_blobs':0,'first_helper':'round3family3 readability only, later explicitlyreservedbyRootGC/GJ, excluded fromnext/currentprimary','second_helper':'fourD22rootentries physicalbytes only, not semanticreading/preclaim','network_or_lazy_fetch':0,'shared_Git_writes':0,'clean_show_claim_done_checkpoint_calls':0,'phase3_mapper_or_graph_import':0,'review_counts':'pathaliases do not create new independently informed reviewer, solver implementation or run','derived_builder_calls':1,'derived_builder_failures':0}
assert scope['primary_bytes']==29189 and len(targets)==6;js(E/'read-scope-and-evidence-status.json',scope)
unitmaps=[
{'id':IDS[0],'canonical':'781c2fa3ff062d072d72','units':[{'source':'§1 fullformaltypes/m>=1/p>=1/completeσ notpreassumedSPE/S andS+','target':'固定人数完整策略的覆盖矩表示--定理.md §§1,3,4'},{'source':'§2 positiveintegralPhi/triangularspan/laststar/countgraph/fullinterestcodimension proof','target':'固定人数完整策略的覆盖矩表示--定理.md §§2–3'},{'source':'§3 exposing functional/m1counter/p1zero-functional/pointedcone','target':'覆盖矩锥极射线与自适应类型稀疏化--定理.md §§1–2'},{'source':'§4 sixmisreadings signedcone/finite-types/Knotcoordinatepositive/distinctlabels/raysnotEF/wholehistories','target':'表示/实现锥两定理的边界及完整数值合同'},{'source':'§6 CR1reversepayoff/CR4freshSPE uniqueimplementation/weakerinequalityfolding/m1','target':'表示定理§2,4及精确保留激励数值的折叠与末层方向边界--障碍.md §§1–2'},{'source':'§6 CR5rationalkernelsparsification/distinctcoverage/clear denominators/alloldobjectionsclosed','target':'覆盖矩锥极射线与自适应类型稀疏化--定理.md §§3–4及计算资源来源审查段'}],'boundary':'sourcewrittenreview coversCR1–5; targetobstruction also containslaterCR6, which is NOT credited tothissource review'},
{'id':IDS[1],'canonical':'34736d33cf814fa93dcd','units':[{'source':'2026-10-21 originalreviewer unread-discovery/code/standardlib scope','target':'五客户无拥挤SPE负载桥障碍--反例.md 审查身份/复现'},{'source':'all5unitclients/4distinctthemes/fullroot+4reply strategy','target':'同对象 ExactStatement'},{'source':'all4x4lastprofits/4realrootprofits20incl5self andfrozenvsreal difference','target':'同对象 全部末历史与根节点核验'},{'source':'actualCD unsharedcounts11011/u2,2/W4/OPT5 andallf0=0f1=1class counter','target':'同对象 福利/最优值与无拥挤障碍'},{'source':'16orderedterminal auditpointer/no half/novelty/minimalityclaim','target':'同对象 复现/范围; originalcode execution notnewlyrerun'}],'boundary':'same review pathalias, not a second independent implementer or newrun'},
{'id':IDS[2],'canonical':'af985f9071d31ebfd9f4','units':[{'source':'allk>=1/m=k+1/3k2clients/3k1themes/existence notallSPE','target':'三人碰撞自由族福利障碍--反例.md ExactStatement (stablefilename, allk theorem)'},{'source':'Bstate baseandfreshA3ceiling/oldBs2/hazardofcontinuingfreshC','target':'同对象 §2 B状态'},{'source':'Qstate multipleoldA/arbitrarymarkedoldA/base/gfreshC/all8deviationclasses/freshBseparate','target':'同对象 §3 Q状态'},{'source':'orderedhistories/decreasingheight/disjointchildsubtrees/targetfinalprofits/notforcingallstartconstructionsconsistent','target':'同对象 §1,4 全部粘合边界'},{'source':'actualallCiD/W2k2/OPT3k2/no oracle/exactratio/f0class necessaryf1>=3/2not sufficient','target':'同对象 §5'},{'source':'independent originalproof withoutglobaldiscovery/oracle thenrootcrosscheck/nohalf/externalnovelty','target':'同对象 依赖和异议状态'}],'boundary':'not only3players despite stablefilename; finitek verification not universalproof basis'}]
js(E/'full-semantic-duplicate-coverage-map.json',unitmaps)
receipts=[]
for x in source_rows:
 a=next(a for a in aliases if a['primary_id']==x['id']);ts=a['canonical_current_progress']['targets'];u=next(u for u in unitmaps if u['id']==x['id']);receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':f"{x['size']}B/{x['lines']}行原独审此前GE已实际全文实读，含全部证明/补审/边界/依赖，本批sameSHA诚实复用，不假称第一读。原多组12IDs actualpushed回执保needs-attention，Root独立保全恢复记录及本3当前owner/sourceSHA实际核后才封包。",'comparison_note':f"与已integrated canonical源{u['canonical']}大小/SHA256/blobSHA1完全相同；六现行目标均与GE已全文读快照同SHA，未重复读取规范数学。逐节完整映射及源审查先验/范围在evidence保留。",'decision_note':'精确duplicate：没有额外数学或新独立审查人数，来源路径别名完整归档；源所有独有内容已在列出自足对象/精确资源。'+u['boundary']+' 本批0数学/CLI/SPE/LP/旧成功重跑；不额外donecanonical旧源。','disposition':'duplicate','targets':ts})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# 三份独审源的精确内容别名

三新primary是R2fc independent_mechanism下14428B覆盖表示、3971B五客户、10790B任意k族独审，共29189B。GE已实际全文读，本批逐sourceID核当前owner/sourceSHA及原字节，与已完成canonical来源大小/SHA256/Git blob相同；不重读GE已全文读且当前SHA未变的规范数学，不重复任何旧程序。

完整内容去向见full-semantic-duplicate-coverage-map.json：覆盖原稿§1–6全部定义/独立证明/后续CR1,4,5补审/边界关闭；五客户原稿的全部集合/5节点20比较/16终局/纯负载函数类范围；任意k原稿的B/Q两个加强状态、全部危险偏离、有序子树粘合与精确OPT。它们已经是自足现行正文，无需另造相同命题或复制一份新数学页。

CR成文独审范围1–5，不把目标页另有CR6当它的审查成果；五客户与族不反half；族是所有k的存在式不是所有SPE固定一路径，也不因旧稳定文件名含三人缩小m。原未读发现稿/代码的先验属于原审查者，当前知情清洗不称新盲审、外审或实现。路径别名不增加审稿人数。

原claim完整12IDs、pushed且local_sync needs-attention，原字节不改。Root另给保全恢复证据，stash2tracked/2untracked全同、0missing/different/unmerged，stash保留；本3owner/sourceSHA再次核验后才写duplicate receipts。不是重写回执制造synced或代理操作共享Git。

新数学/CLI/SPE/LP/导入/旧成功重跑0。round3_family三MD只核可用字节后Root明确已接手，已从下一批排除，未读数学/认领/写receipt。下一真实可用是D22四总入口，原字节齐但未开始语义清洗，需Root正式认领。
''')
put(W/'relation-review.md',r'''# 阶段二关系

本批关系是同内容不同路径的sourcealias和已有正文精确去向。三审查对应canonical源已integrated，当前六数学目标与已全文读快照同SHA；无独有证明残缺、无新增命题。duplicate依据不是标题或计数，而是原字节对象相同加逐节语义映射。

CR1–5与CR6、signedspan与非负方向、真客户锥与形式标签、五客户与任意k族、存在与全称、有限审计与一般归纳的边界保持；不增加第三名/新独审身份。原多组pushed但sync冲突的历史和独立恢复证据保真，不倒造synced。

来源关系供后续phase3实际解释；本批不导旧图或强制造边，不重done旧canonical源或RootGC/GJ的round3稿。
''')
cp(C/'learning-gm-next-readable-round3/local-export-manifest.json',E/'excluded-Root-reserved-round3-availability.json');mp=C/'learning-gm-next-d22-root-entries/local-export-manifest.json';nr=json.loads(mp.read_text());cp(mp,E/'next-D22-available-local-manifest.json');nextrows=[]
for x in nr['rows']:
 assert not (REPO/'cleanup/progress'/f"{x['id']}.json").exists();b=Path(x['local_path']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256'];nextrows.append({**x,'progress_observed':None,'read_status':'byteavailability verified only; not semanticread/primaryclaimed','routing':'Root must current-recheck and atomically claim actual available subset'})
js(W/'next-candidates.json',nextrows)
put(W/'delivery.md',f'''# GM交付

3primary29189B/同SHA完整独审，原{len(claim['ids'])}IDs pushed {claim['remote_tip']}原capture保needs-attention不改，独立Root保全resolution及3owner核后生成3duplicate receipts。六既有自足数学目标逐SHA同GE全读快照，0规范正文冗余重读，0新数学页、0旧程序/新数学运行。

全部原件、canonical integrated记录/大小SHA256blob、目标快照/完整逐节去向保全。Root先push本证据/receipt依赖再done，不额外重donecanonical源。下一D22四入口35961B实字节齐未数学读，Root已接手round3三稿明确排除。
''')
cp(Path(__file__),E/'build_delivery.py');checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in source_rows:
 b=(S/x['preserved_path']).read_bytes();v=inv[x['id']];ck('exactprimarySHA '+x['id'],len(b)==v['size'] and sha(b)==v['sha256']);ck('exactprimaryblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'])
ck('raw12claim unchanged',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and len(claim['ids'])==12 and claim['local_sync']['status']=='needs-attention');ck('independentresolution unchanged',(S/E/'independent-sync-preservation-resolution.json').read_bytes()==respath.read_bytes());ck('realpreservationcondition',resolution['missing']==resolution['different']==[] and resolution['unmerged']=='' and resolution['stash_kept'] and all(x['same'] for x in resolution['tracked']))
for x in owners:ck('actualownercurrent '+x['id'],x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'])
for x in aliases:ck('exactcanonicalintegratedalias '+x['primary_id'],x['canonical_current_progress']['disposition']=='integrated' and x['same_size_SHA256_blobSHA1'])
for n,x in targets.items():
 b=(S/x['snapshot']).read_bytes();ck('unchangedGEalreadyfullyreadtarget '+n,len(b)==x['bytes'] and sha(b)==x['sha256']==oldctx[n]['sha256'])
ck('complete3duplicate receipts',len(receipts)==3 and {x['id'] for x in receipts}==set(IDS) and all(x['disposition']=='duplicate' for x in receipts))
for x in receipts:
 ck('fullsemanticreceipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']))
 for n in x['targets']:ck('actualcanonicaltarget '+n,(REPO/n).exists())
ck('all3completeunitmaps',len(unitmaps)==3 and all(len(x['units'])>=5 and x['boundary'] for x in unitmaps));ck('nofillernewmathpages',not (S/'archives').exists());ck('zeronewmath/replays',scope['new_original_CLI_calls']==scope['new_math_or_SPE_or_LP_runs']==scope['old_success_replays']==scope['new_canonical_full_rereads']==0);ck('actual3sourcetotal',scope['primary_bytes']==29189 and len(source_rows)==3);ck('only4nextD22notRootreserved',len(nextrows)==4 and sum(x['size'] for x in nextrows)==35961 and not {x['id'] for x in nextrows}&{'b617f9e6100f01667e87','1803e6b90277a9e341b3','3fe258fe754dcc2d0dd6'})
for x in nextrows:
 b=Path(x['local_path']).read_bytes();ck('nextactualbytes '+x['id'],len(b)==x['size'] and sha(b)==x['sha256'])
obs=[]
for p in S.rglob('*'):
 if not p.is_file() or p.name in ['copy-files.json','copy-paths.txt','delivery-summary.json']:continue
 try:t=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 ls=[i+1 for i,l in enumerate(t.splitlines()) if l!=l.rstrip()]
 if ls:obs.append({'path':str(p.relative_to(S)),'lines':ls,'frozen':any('/'+z+'/' in str(p.relative_to(S)) for z in ['original','target-snapshots'])})
ck('derivedtrailingwhitespacezero',not any(not x['frozen'] for x in obs));js(E/'transport-whitespace-observations.json',{'observed':obs,'originals_unchanged':True});js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'new_formal_objects':0,'existing_self_contained_targets':len(targets),'scope':'exactoriginal-alias/SHA/oldtarget and independentRootrecovery/owner/completecoverage/receipt/transport checks; no math or canonicalreread or oldrun'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');out={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':29189,'primary_lines':scope['primary_lines'],'new_formals':0,'existing_targets':len(targets),'receipts':3,'all_disposition':'duplicate','checks':len(checks),'new_math_runs':0,'raw_claim_tip':claim['remote_tip'],'raw_claim_sync_status':claim['local_sync']['status'],'independent_preservation_resolved':True,'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),out);print(json.dumps(out,ensure_ascii=False,indent=2))
