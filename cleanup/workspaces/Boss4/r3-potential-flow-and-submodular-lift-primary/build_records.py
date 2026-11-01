"""Only the actual five DU Markdown sources receive semantic receipts."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parents[4];R=S.parent.parent/'boss4-research';W=Path(__file__).resolve().parent
E=S/'archives/customer-attraction/tools/evidence/potential-flow-and-submodular-lift-primary'
A='archives/customer-attraction/state/定理/共同删除势的全域效率与单调次模提升--定理.md'
B='archives/customer-attraction/state/定理/两人匿名势的静态安全支付与无势循环边界--定理.md'
C='archives/customer-attraction/state/审查/全树收益运输的普遍弧与有限势反例范围--审查.md'
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def fp(p):b=p.read_bytes();return {'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
defs=[
 ('553d139efa8a213044e2',[C,A,B],
 '5770B全文：真实有序行先求续局再收益端点压缩/弧方向、根需求与独立pQ供给、全部同主题无缩放iff及不同主题不可能、势超边、无势k5、84有限点弱/强完整检查计数与具体标量/效率冲突、K存在引理/最小17601声明、全层E恢复共同signed接口。',
 '全文比较既有TC-DIL-1及共同E+BC定理/DJ入口资源。长稿新增定义gap为W−3固定p保底、明确有限N6单纯形，不倒填DJ只读README时已知。γ1对应f_q≤f_r反向无缩放行，公共平移需先保全部该行。',
 'integrated精确图合同/条件平移与有限报告身份。原84值JSON/脚本本地缺失，0程序，不冒新SPE/DR/sharp认证；强203034与202782写清后者减前者−252。缺共同signed早于非负客户，不虚称高阶非负核必需。'),
 ('c6278b6311945dbf104c',[A],
 '2937B全文：全域积分有限界、删除边际指数、own/crossDR、自拥挤混合h≥0、F导数/E/纯态、分部积分局部sharp、TC-DIL-1时钟内部独立性与全部锋利系数加强、rank2C非coverage、无聚合安全/half。',
 '与5197B作者全文及既有完整TC-DIL-1时钟证明逐步比较，源作者只局部sharp，审读加强至全部q/r。审读未显式覆盖作者末节反向刻画，不因同日同路径倒填历史审核范围；当前应用独立核其假设。',
 'integrated全域正定理和原内部审读身份，反向由本批共同Φ/E/支配收敛解析重构承担。无代码/数值运行，不借历史hash作当前全文byte认证。'),
 ('f6f1b032078026fa0a6c',[A,C],
 '5197B全文：有限全域C、随机标签积分、有限性/收益式、全域单调DR/自拥挤/E/harmonic/局部sharp、min(|S|,2)严格包含、GF2 probe计划，以及后补全域E+单调DR反向和L→∞有限层限制。',
 '固定同一个Φ:整个Z≥0P、Φ0、所有U=共同删除边际为承重前提，收益空间需E+BC；绝不把裸E与按计数递减当Shapley可积性。加任意signedC积分绝对有限说明，反向先唯一递推再极限恢复C单调/次模。',
 'integrated完整双向证明及非coverage三标签显式signed表示/势公式。TC既有结果补全作者未声称的全部sharp，仍不推出任何一般福利；matroid_bundle_probe未提供0run，有限反例不被升级全域延拓。'),
 ('938e6235114c47185059',[B],
  '3161B全文：任意k≥5匿名循环/完整根与末回复/自拥挤/匹配静态v2、势反对称循环排除、k5全正/唯一末回复矩阵、两人exact-potential h+K正边界循环Q证明、残余曲线已否及废日志边界。',
  '与source553k5同一例区分全族/正效用变体及新增正界；既有CAG单后继恒等式为特殊h+K。安全取得2941B旧残余稿，和已有27客户矩阵比对，客户重标相同但一个离轨平局不同，保原完整策略，不假逐字同。',
  'integrated两人定理/完整无势全族及严格边界、残余F1/F2失败量词。原循环脚本missing0run，解析全族计数不是原程序输出；无势W总效用非客户覆盖，CAG残余例half正余量。'),
 ('9912db97ebcb52e902e4',[C,B,A],
  '3118B全文：旧Boss2备份身份、固定策略有限Φ cone/strong开关、20固定查询/最后弱点、强run结束后占位、二次势5000有限阴性、残余1000阴性与删全客户曲线日志、发现/Fraction回代/独审/外审分层。',
  '5770B长稿强点−567更新旧占位，不把原“无反例不证明”变仍无反例。弱点纯态满拥挤零与正混合收益的CAG矛盾按源说明定位；全域lift同类但更强E合同与84点有限DR不同。',
  'integrated全部程序/输入版本角色，不从导航替程序done或认证，不重扫已否残余候选。原声称独立发现和旧署名保先验，不触发当前注册；0原/0新数值run，无外审/新颖性认证。')]
receipts=[]
for i,targets,read,compare,decision in defs:
 receipts.append({'id':i,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,
 'read_note':read,'comparison_note':compare,'decision_note':decision,'disposition':'integrated','targets':targets})
save(W/'semantic-receipts.json',receipts)

comparisons=[
 ('archives/customer-attraction/state/定理/递减共同边际的锋利同主题稀释--定理.md','full-text','TC-DIL-1 ratebudget/内部钟独立性/锐性与全q,r假设'),
 ('archives/customer-attraction/state/定理/共同客户收益的正边际与平衡贡献--定理.md','full-text prior DJ read retained and used','E+BC/共同signed与非negative区分；势中BC自动'),
 ('archives/customer-attraction/state/障碍/同支持守恒与局部客户耦合的严格间隔--障碍.md','full-text prior DJ read retained','终局同支持不够/二主题纠错边界'),
 ('archives/customer-attraction/state/引理/单后继去相关恒等式--引理.md','full-text','h+K两人正界的CAG固定背景特殊结构'),
 ('archives/customer-attraction/state/反例/零背景保护遗漏与超额利润价格--反例.md','full-text','27客户完整6×6表与原2941B一平局不同；Y/Fm量词'),
 ('archives/customer-attraction/state/计算/二十七客户遗漏反例的标签等价与单位核验--计算.md','full-text','另一labelmap与程序证据已有充分原run，不重复'),
 ('archives/customer-attraction/state/反例/唯一最优组合的全遗漏支付--反例.md','full-text','27例多最优与后续唯一最优存在性失败不同'),
 ('archives/customer-attraction/state/资料/全树收益流与势类攻击的共同表示边界--资料.md','full-text DJ authored/reviewed','原入口gap标签未定义；本长稿新定义不回填旧阅读'),
 ('archives/customer-attraction/state/反例/全部实际菜单混合在非负删除边际势中的失败--反例.md','full-text DB authored/reviewed','较宽Phi_m/Phi_m−1菜单例不替全层E或DR反例认证'),
 ('archives/customer-attraction/state/定理/五人半覆盖--定理.md','full-text prior source review retained','旧一般OPEN不覆盖五人已证，六人身份独立')]
rows=[]
for path,scope,note in comparisons:
 p=R/path
 if not p.exists():
  for old in ['r3-quotient-and-fixed-rank-source-primary','r3-tree-and-abstract-menu-workspace-primary']:
   if (S.parent/old/path).is_file():p=S.parent/old/path;break
 rows.append({'path':path,'actual_read_path':str(p),'read_scope':scope,'role':'comparison-not-primary',**fp(p),'comparison':note})
save(E/'comparison-manifest.json',{'whole_repo_queries':'global lifting/TC-DIL/common Phi/E+BC/同支持/残余基数/F2Y/residual_portfolio; all listed objects actually read in stated scopes','sources':rows,
 'prior_DJ_state':'Root received/copied DJ29; no specific pushed commit newly attested here. Ensure DJ link target published with/before DU body done; existence not remote proof.'})

dep=json.loads((E/'dependency-boundary.json').read_text());assert len(dep['provided_comparison_sources'])==1 and len(dep['confirmed_local_missing'])==4
assert 10458-3*3549==-189 and 10458+3*17601==63261 and 3549+17601==21150 and 63261-3*21150==-189
assert 51168+67800+65910==184878 and 184878-3*61815==-567 and 202782-203034==-252
save(W/'runtime-summary.json',{'original_program_runs':0,'new_numerical_experiments':0,'optimizer_calls':0,
 'proof_method':'Analytic all-k cycle/minimax/cycle-BR proof and full-domain integral/recursion/dominated-convergence proofs; no finite experiment used for universal claims.',
 'finite_reports_not_new_certified':['weak/strong84point values','168monotone252DR210selfcrowding','210transfer18pure258SPE21background','Kmin17601/2520sharp270gamma1','15/9support conflicts'],
 'scalar_arithmetic_checked_only':'reported scalar sums/gaps and orientation were checked; not a reconstruction of missing tables/strategy.',
 'missing_original_programs':'Local helper confirmed weak/strongJSON,weak independentaudit,cycle script absent; no network/auth retry. Other named probes not provided, not asserted absent by lookup.',
 'already_sufficient_prior_experiment':'27customer original exact audit preserved in published resource; one new legal-tie version verified analytically from same full matrix, not rerun.',
 'intake_helpers_this_continuation':{'current_primary5':'reused preceding exact local export,0 new fetch','dependencies':1,'next_candidates':1,'all_network_attempts':0},
 'read_order':'All5MD pre-read fully, actual pushed/owner/SHA verified before formal staging; necessary2941B comparison fully read before analytic version comparison.'})
save(W/'relations-review.json',{'reviewer':'Boss4/credible_cap_resume','phase':'phase2 semantic relationship reasons, not automated phase3 graph',
 'objects':[A,B,C],'relations':[
 {'type':'exact-characterization-with-premises','from':A,'to':'共同客户收益E+BC','reason':'SamePhi deletion assumption givesBC; all-layerE supplies uniqueness; globalmonoDR iffCmono-submod requiresL arbitrarilylarge. NakedE and coordinate monotonicity excluded.'},
 {'type':'application-strengthening','from':'TC-DIL-1','to':A,'reason':'Same nonnegative decreasing marginalDeltaC, exactclocklaw unchanged, gives allsharp beyond authorlocalinequality; not a secondnewdilutiontheorem.'},
 {'type':'assumption-boundary','from':B,'to':C,'reason':'Nonpotential selfcrowdingcycle defeats statearc-onlyuniversal bridge; h+Ksymmetry proves2personpositiveboundary, no claim for3+real followers.'},
 {'type':'finite-vs-global-domain','from':C,'to':A,'reason':'84point DR and listed conditions need notextendtoN6; weakstrongfailE/common signed, so cannot refute globalE+monoDR C model or coverage half.'},
 {'type':'same-client-table-different-tie-policy','from':'2941B residual comparison','to':'27customer published counterexample','reason':'Exactlabelmap preservescustomers/paymatrix; one offpath replychangesRtoS atformalQ. BothBR/rootu6, not identicalfullpolicies; F2Y14>13 same failure.'}],
 'no_false_edges':['No submodular-noncoverage rank2 example→welfarecounter','No negative reportgap→newSPE certification','No bareE→Shapleyintegrability','No sourceREADME→all linked programsdone']})
save(W/'self-review.json',{'status':'pass','primary_count':5,'primary_bytes':20183,
 'mathematical_checks':[
 'Explicit commonΦ:entireZ≥0P,Φ0,allU deletion marginal retained throughout converse;BC not inferred from裸E+decreasingU.',
 'Integral finite for monoC and absolutefinite for arbitraryfiniteC; own/crossDR, selfcrowd exponentqa+1 and fullFderivative endpoints correct.',
 'Reverse uniqueall-layerE recursion then qa1,L→∞ dominatedconvergence recoversCmono/submod; fixedm finite arrays not covered.',
 'Fullsharp usesg=DeltaC≥0 decreasing and samefunction, qa/ra positive, exactTCclockwithin-process independence preserved.',
 'Cmin(|S|,2) pairmass1/triple−1 givesthirdalternating−1 and explicitglobalharmonicΦ; noefficiencygap claimed.',
 'Anonymous2player exactpotential iffA=h+Ksym; beta cycle uniform Q rootIC proof andactualBRgivebothu≥v.',
 'Cycle k≥5 uniformrowcolmatching, anti-cycle−k; strictpositive5lastunique10/rootall2 stilltied/anticycle−40; notCAGcoverage.',
 'Flowarc orientation alternative→prescribed, sourcepQ independent; certificateonlysufficient fixedp unlesspoptimal.',
 'Universal unscalediff uses same population, singleton/Pminuslabel tests; gamma1sharp is opposite orientationf_q≤f_r, premise not dropped.',
 'PublicK fixes onlygamma>1negative rows oncegamma1 holds; same-layerE difference invariant, harmonicnotpreserved.',
 'Reported−189/−567 scalararithmetic and strongsecond-minusfirst−252 checked, not84data/programcertified.',
 'Residual old2941 labels A,B,T,S,Q,R→A,B,T,Q,R,S; reply atformalQ isS versus existingR legaltie, notmerge. FixedY F2>W different from favourableoptimalO quantifier.'],
 'source_and_execution_checks':['All5 actualprimary local bytesverified; full5originalreceipt/owner snapshot; no sharedGit/claim/done/network','Only1comparisonMD besidesprimaries; missing4 no retry/auth; none additionallydone','Originalrun0/newnumeric0/solver0; analytic proofnotprogramclaimed','Authorforward/internalreview and authorpostaddedconverse scopes distinguished; no externalreview/novelty'],
 'limits':['Original84point tables and audit code required before newfullcheck','No globalE+submod welfare theorem beyond stated2person result','PriorDJ link target must be published with/before DU done','Root authoritative owner check for nextcandidate group']})

nxpath=S.parent/'credible-next-prefix-local-inputs/local-export-manifest.json';nx=json.loads(nxpath.read_text());assert nx['missing']==[] and len(nx['rows'])==5
future=[]
for r in nx['rows']:
 p=R/f'cleanup/progress/{r["id"]}.json';future.append({**r,'local_progress':json.loads(p.read_text()) if p.exists() else None,'role':'next-source-local-export-only-not-primary','pre_read_or_receipt_in_this_batch':False,'availability':'Root must verify authoritative owner; local progress absence not enough'})
save(W/'next-candidates.json',{'local_export_manifest':str(nxpath),'all5_local_bytes_verified':True,'network_attempts':0,'sources':future})
print(json.dumps({'primary':5,'receipts':len(receipts),'integrated':5,'new_formal_pages':3,'mathematical_runs':0,'comparison_objects':len(rows),'next_local':len(future)}))
