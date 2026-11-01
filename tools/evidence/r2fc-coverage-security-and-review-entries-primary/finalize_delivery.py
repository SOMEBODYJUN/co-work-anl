from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-r2fc-coverage-security-and-review-entries-primary';E=Path('tools/evidence/r2fc-coverage-security-and-review-entries-primary');W=Path('cleanup/workspaces/Boss4/r3-r2fc-coverage-security-and-review-entries-primary-next');P='archives/customer-attraction/state/资源/覆盖矩与扩大势入口的模型和独审合同--资源.md';IDS=['7ff889463b6b3535ac58','0d9f1d7b2cb2dafd4296','44357124372fb651a98f']
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def rd(p):return json.loads((S/p).read_text())
claimpath=R/'boss4-r3-next-ge-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids']);assert set(IDS)&set(claim['ids'])==set(IDS);primary=rd(E/'source-manifest.json');related=rd(E/'related-source-manifest.json');contexts=rd(E/'context-manifest.json');owners=[]
for i in IDS:
 x=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());v=next(v for v in primary if v['id']==i);assert x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==v['sha256'];owners.append(x)
cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners);cp(Path(__file__),E/'finalize_delivery.py')
scope={'primary_sources':3,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'read_timing':'GE first complete mathematical reading of all3entryREADME; earlierGB6144byteavailability only','related_full_mathematical_sources':3,'related_bytes':sum(x['size'] for x in related),'related_role':'complete14428CRreview/3971fiveclientreview/10790allkfamilyreview read, not extra done; canonical aliases hashchecked','full_actual_current_formal_contexts':len(contexts),'current_context_publication':'working-copy snapshots preserved; this packet does not invent RootGC4 or other context checkpoint/done status','new_original_CLI_calls':0,'new_math_program_runs':0,'new_SPE_or_LP_checks':0,'new_DR_or_PM_or_rank_audits':0,'old_success_replays':0,'new_helper_calls':1,'local_blob_attempts':7,'local_exports':3,'local_missing_codes':4,'missing_source_ids':['237a9c14a68cbe08a526','3bcc00f6fc8a8ac6756c','4efc80407211435b8fa1','9c88e282902193a10afc'],'canonical_code_read':'existing11313program bytes/hash only and published full computation object; not newly full-code read or run','canonical_report_read':'actualbytes/hash versus workspace13248frozeninventory binding; not a new export/full-field read of workspace report','raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'semantic_distinctions':['CR1to6signedspace/nonnegativeICcone/trueclientcone differ, m1/p1/finite-type boundaries','PMglobalanchor allproper-subcatalog obstruction is fakeglobalmoment, not legalSPE counterexample','CAGsupport budget pluspure diagonal necessary for6Phi mixed equation','DR3players6actions/P161v56 expandedmodel not CAGcoverage/half','CRwrittenreview1to5 not6; PM2mentalreview no newwrittenfile; originalreviewerpriorunread discovery distinct from current informedcleaning','workspace11506source versuscanonical11313differentSHA, frozen13248report sameboundnot sameprogram certification','fiveclient/anyk sameSHA aliases do not create another reviewer/person/newalgorithmrun'],'mathematical_work':'full object/quantifier/proof-role comparisons and self-contained entry resource; no new universal half or solver claim','derived_builder_calls':1,'derived_builder_failures':0,'network_or_lazy_fetch':0,'shared_Git_writes':0,'clean_show_claim_done_checkpoint_calls':0,'phase3_mapper_or_graph_import':0}
assert scope['primary_bytes']==6144 and scope['primary_lines']==37 and scope['related_bytes']==29189;js(E/'read-scope-and-evidence-status.json',scope)
coverage=[
{'id':IDS[0],'units':['oldmodel and true strong/weak aggregate notsolved','expandedDR3person6action u0/105/56/P161/v56 notCAG/currentnewdefinitioncheckidentity','supportbudget and6Phi mixedrepeat withpurediagonal premisenowexplicit','drprobe/numericalgroup artifacts notexact sourcecases/no falseperpatterncompletion','degenerate randompolicy cones and actualpotential/groups design notpositiveproof','oldindependentreviewpending versus newRootcheck notoldCLI','oldroot/noGit/work/token instructions historical only'],'targets':[P]},
{'id':IDS[1],'units':['allcoverage_moment_geometry roles CR1to6 includinghypothesis/domain rows','Fractionauthoraudit/rank/positivecoeff/extreme/SPEtests canonicalversiondistinct','PM1to3 proofroles/formalpositiveglobalbudget/allproper-localmodels/familyunbounded','old21834types502moments onlyauthorcodeclaimnotnewrun','oldR7ecoverageassetunlocated and sharedmobiuspriorwork/newnessnotcertified','onlypreservinginequality weakerthan exactallrowvalues CR4notapplicable','generalhalf needsnonnegativeICmultipliers and globalKdual notsignedspan','PM2latermentalcheck no newwrittenreview distinctfromCR2/3writtenreview','lateststoplocalfamilies and goactualsigma historicalnotnewinstruction'],'targets':[P]},
{'id':IDS[2],'units':['2026-10-21 oldsubrole noGit/outgoing rootcheckpoint historical','CR1to5 writtenreview/signedspace/extremeray/boundarym1p1/finitetypes/lineality/distinctlabels','fiveclientindependentunread-discovery history/full5nodes20inclself/16outcomes/nohalf','loadfunctionf0f1 normalizationclass allhighcoeffs unaffected','allk Q/B strengthenedmultipleoldA/freshB/realorderedhistorygluing/OPT3k2/W2k2 existence notforall','originalunitclientaudit4k+JSON claims and actualmissingcode readscope','oldpure-red/bluepaymentcounterfamily abandoned nothalf-equivalence','no unresolvedfatal versusnotgeneralhalfproof/noexternalnovelty'],'targets':[P]}]
js(E/'semantic-coverage-map.json',coverage)
notes=[('1506B安全入口全部段落首次数学实读，原CAG/强弱真v、扩大DR/P161、support预算/混合重复式、全部数值文件角色/退化锥/下一步历史完整保留。','完整读现DR自足证明及Root新定义核验范围，核不是CAG；展开support预算和混合式的纯对角前提，原3967验证源码缺不冒其CLI。','原有用预算与扩大模型失败准确归位；不将六动作当六玩家、不把161称CAG覆盖W，不因浮点阴性或旧独审待完成改变六人half/真聚合量词。'),('2886B覆盖入口首次全文读，每个稿件/程序/JSON用途、CR1…6、PM1…3、已有先行工具/未找到旧稿、精确资料与不等式合同、最后非负乘子义务全保。','全读十份当前正式数学及3独审原文，核m1/p1/全类型/极射线/CR4m>=2/CR6m>=2、PM2心算无文件；工作码11506缺且不同于11313成功码，冻结报告只做inventory/实际hash绑定不冒源码同版。','自足资源不把signedspan或局部真矩当half证书；原PM计数只作者有限声明，保当前证明及作用边界，原code未取得不假认证。'),('1752B独立机制README首次全文读，原角色、三类成文独审/五客户audit入口、无拥挤任意k、旧纯遗漏失败、原CR1…5异议关闭与未付量完整保全。','实际全文读对应14428/3971/10790独审，核原先未读发现稿/代码的审查先验、Q多旧A/freshB/全历史粘合和单客户负载类规范化；与canonical已done三原件同SHA，不增加审查人数。','独核来源与数学用途自足保留，缺4128原码不造新run；CR6和PM范围不倒扩，任意k存在式不误改forallSPE或仅三人，也不抢RootGC4主源。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原始22IDs pushed/synced回执保未投影，本3交集及当前Boss4 owner/sourceSHA已核。','comparison_note':b,'decision_note':c,'disposition':'integrated','targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(W/'relation-review.md',r'''# 阶段二关系

三入口各有独立资源身份：安全入口保扩大模型与CAGsupport预算隔界；覆盖入口连接CR表示/正性/稀疏化与PM全局正矩；独核入口保不同先验/成文与心算/有限代码范围。完整signedspan、非负Γ乘子锥、真实客户K锥不能混作同一正性。

CR4精确全部数值合同强于保SPE不等式；CR6形式非SPE不反half。PM真子目录合法而全局假仅为表示障碍。CAGsupport+纯对角才推出混合重复式，DR边际势反例恰缺该预算且三人终局已不能客户实现。当前原模型真v聚合/六人half不由扩大DR失败否定。

独审CR1…5不倒扩CR6，PM2心算不新增成文审稿人；五客户及任意k存在性完整归纳与有限oracle不同。三个workspace独审与canonical逐SHA同，路径别名不增加独立人数。11506缺工作码/11313旧成功码不同，13248输出inventory绑定相同不认证缺码执行。

本批新数学/原CLI/旧成功复跑0，只有真实读取/模型与版本审查。RootGC4仅比较现行正文，不额外认领/done；不导旧图、强制连边或进入mapper。
''')
nextrows=[]
for x in related:
 p=REPO/'cleanup/progress'/f"{x['id']}.json";assert not p.exists();aliases=[z for z in rd(E/'independent-review-original-aliases.json') if z['related_source_id']==x['id']];assert len(aliases)==1 and aliases[0]['canonical_progress']['disposition']=='integrated';nextrows.append({**x,'local_path':str(S/x['preserved_path']),'progress_observed':None,'semantic_read_status':'all related original text already fully read GE; no primary completion; sameSHA canonical already integrated','canonical_sameSHA_source_id':aliases[0]['canonical_source']['id'],'next_disposition_hint':'after actualclaim and precise current-target comparison, exactduplicate receipts may be appropriate; no pretended reread or extra reviewer'})
js(W/'next-candidates.json',nextrows)
put(W/'delivery.md',f'''# GE交付

actual原{len(claim['ids'])}IDs claim {claim['remote_tip']} pushed/synced原字节保留；本3交集/owner/sourceSHA核齐，不改造三ID投影回执。3primary6144B/37行全部首次数学实读，3必要独审related29189B全文实读，十正式对象全文比较；1新自足资源/3receipt。

CR1…6/PM1…3及独核范围、m1/p1/m>=2、全类型/非负乘子/客户锥、support混合式纯对角前提、扩大DR非CAG与现独立定义检查边界完整保存。11506缺工作码/11313已成功码不同，13248输出只核冻结inventory与实际canonical字节hash绑定。新数学CLI/SPE/LP/DR/PM/旧成功复跑0。

helper1次7本地尝试3独审MD齐4代码缺，无网络或重试。下一三个可读独审已全文related读且与canonical已done同SHA；Root正式认领后可准确duplicate，不能新增审查人数。Root先推正文依赖再done，代理无sharedGit/show/领/done/checkpoint/账号通信。
''')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();ck('exactsize/SHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('exactblobSHA1 '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('original unprojected22claim preserved',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes());ck('onlyactual3intersection primary',len(set(IDS)&set(claim['ids']))==3 and len(claim['ids'])==22)
for x in owners:ck('actualowner '+x['id'],x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==next(z['sha256'] for z in primary if z['id']==x['id']))
for x in contexts:
 b=(S/x['snapshot']).read_bytes();ck('exactfull-context '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
ver=rd(E/'audit-version-binding.json');ck('missingcode notcanonical11313',ver['same_program_bytes'] is False and ver['workspace_program']['size']==11506 and ver['canonical_program_observed_bytes']==11313);ck('reportinventoryactualcanonical hash binding',ver['same_report_size_SHA_bound'] and ver['workspace_frozen_report']['sha256']==ver['canonical_report_observed_sha256'] and ver['workspace_frozen_report']['size']==ver['canonical_report_observed_bytes']==13248)
for x in rd(E/'independent-review-original-aliases.json'):ck('exactcanonicalreviewalias '+x['related_source_id'],x['sameSHA']==x['canonical_source']['sha256']==next(z['sha256'] for z in related if z['id']==x['related_source_id']) and x['canonical_progress']['disposition']=='integrated')
t=(S/P).read_text();ck('flatMATEK',all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('allnonLF C0zero',not any(ord(c)<32 and c!='\n' for c in t));ck('trailingwhitespacezero',all(l==l.rstrip() for l in t.splitlines()));ck('TeXdisplaybalanced',t.count('\\[')==t.count('\\]'));links=[]
for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
 if '://' in dest or dest.startswith('#'):continue
 n=posixpath.normpath(str(Path(P).parent/dest.split('#',1)[0]));p=S/n if (S/n).exists() else REPO/n;ck('actualrelativelink '+dest,p.exists());links.append({'source':P,'destination':dest,'resolved':n,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
js(E/'formal-link-check.json',links)
ck('CR1to6scope allpreserved',all(x in t for x in ['CR1 /','CR2 /','CR3 /','CR4 /','CR5 /','CR6 /','CR4 / 精确OPT外折叠障碍 | m≥2','CR6 / 后续方向边界 | m≥2']));ck('supportdiagonal domainbeforemixed','\\tag{SUPPORT}' in t and '\\tag{REPEAT}' in t and '再用这个纯对角关系' in t);ck('PMandindependentscope','未另写独立审查文件' in t and 'CR6不在该成文独审范围' in t and '21834' in t and '502' in t);ck('expandedmodelnotCAG','P不称CAG覆盖W' in t and 'u=(0,105,56)' in t and '弱P−(5/2)v=21>0' in t);ck('allactualreadtotals',scope['primary_bytes']==6144 and scope['primary_lines']==37 and scope['related_bytes']==29189 and len(contexts)==10);ck('allmathrunszero',scope['new_original_CLI_calls']==scope['new_math_program_runs']==scope['old_success_replays']==0);ck('helper1call7attempts3exports4missing',scope['new_helper_calls']==1 and scope['local_blob_attempts']==7 and scope['local_exports']==3 and scope['local_missing_codes']==4)
ck('exact3complete receipts',len(receipts)==3 and {x['id'] for x in receipts}==set(IDS))
for x in receipts:ck('complete semanticreceipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']))
ck('actualreceipt target',(S/P).exists());ck('only1newformal',list((S/'archives').rglob('*.md'))==[S/P])
for x in rd(E/'formal-resource-manifest.json'):
 b=(S/x['path']).read_bytes();ck('exactformalSHA',len(b)==x['bytes'] and sha(b)==x['sha256'])
for x in nextrows:
 b=Path(x['local_path']).read_bytes();ck('actualnextaliasavailable '+x['id'],len(b)==x['size'] and sha(b)==x['sha256'] and x['progress_observed'] is None)
obs=[]
for p in S.rglob('*'):
 if not p.is_file() or p.name in ['copy-files.json','copy-paths.txt','delivery-summary.json']:continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 ls=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()]
 if ls:obs.append({'path':str(p.relative_to(S)),'lines':ls,'frozen':any('/'+z+'/' in str(p.relative_to(S)) for z in ['original','related','context'])})
ck('allderivedwhitespacezero',not any(not x['frozen'] for x in obs));js(E/'transport-whitespace-observations.json',{'observed':obs,'frozen_originals_unchanged':True});js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'scope':'actualraw22claim/source/owner/hash, complete models/review/version coverage, format/C0/links/receipts/transport; no newmath CLI/SPE/LP or oldsuccess replay'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':6144,'primary_lines':37,'new_formals':1,'formal_bytes':(S/P).stat().st_size,'receipts':3,'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'next_alias_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
