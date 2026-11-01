"""Actual five semantic receipts; missing dependencies remain missing."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
S=Path(__file__).resolve().parents[4];R=S.parent.parent/'boss4-research';W=Path(__file__).resolve().parent
E=S/'archives/customer-attraction/tools/evidence/quotient-and-fixed-rank-source-primary'
Q='archives/customer-attraction/state/等价/覆盖等价标签的完整策略商--等价.md'
A='archives/customer-attraction/state/障碍/固定离轨次数截断的无常数福利障碍--障碍.md'
B='archives/customer-attraction/state/审查/五人增强必要行的索引恒等式与2396行审查边界--审查.md'
C='archives/customer-attraction/state/资料/全树收益流与势类攻击的共同表示边界--资料.md'
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def fp(p):b=p.read_bytes();return {'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
defs=[
 ('07d379bb2632770a988b','duplicate',[Q],
  '4628B完整实读：B10-DUPLICATE-COVERAGE-QUOTIENT-v1精确m≥1/覆盖映射/全历史量词、双向逐历史lift、规定类代表等于原σ动作/唯一父节点、合法代表偏离IC、收益WOPT保留及恰p边界，m0可选扩展、旧audit/JSON与全部有限case类型全保。',
  '与已真实pushed/done DB商对象全文逐构造比较，数学相同；DB原依据4273B内部审读独立重构，现补读4628B原稿，不倒称DB当时已读此源。本次读后比较非盲审；源述团队独立先验另保。',
  'duplicate到已发布DB同一数学对象，不造第二商定理。m0空策略的可选软件边界与原Claim/有限回归导航在证据README保留；原audit和输出不在本5，0原run，不冒有限实现认证或恰p极值不变。'),
 ('3171d41e04587fac0f3c','integrated',[B],
  '3216B完整读：末节点R预算和旧充分条件失败数值、2196行64列/36正dual/1.9844871781654265、特定稀疏跨族交互和条件定价、W0O1列、65列加200行/38正原子/44零行、block20重启和1024负列诊断角色。',
  '与5131B原审查逐数核，基础437行定义§1–3及两人税/三剩余背景利润公式比对。原“identity”严格分成τ=W−u−R恒等和OPT上界；有限全覆盖4人点不冒本批新CAG策略。五人half现已另证。',
  'integrated完整历史定价链、受限支撑非全型上界、特定dual分解非任意dual算法，以及缺真实根四人路径/一致性。缺原子/rows保源述障碍，不假74442或2396新复验，0原LP。'),
 ('107e8af6a50215a95107','integrated',[B],
  '5131B完整读：38严格正mass报告、W1/O与正差精确分数、旧437重用规范非独立重推、新1959索引展开/共同T组对齐、74442等式/44零行、同异索引税通式及1386/276、三人利润200行/系数25/3,5/3,20/3、原复现命令和SPE/OPT边界。',
  '全读相应背景三人5/3定理，并核基础437相关真实菜单/类型域。局部计数恒等式逐式独立重构；新增1959−1662−200=97行未在MD逐项定义，明确不能只用这两MD重新生成全2396矩阵。',
  'integrated审查来源和自足索引推导。34584B原子JSON/7904B原reviewpy/1066B旧report本地缺失，实际0原run且未取网络；精确O正差仅保原报告，不将无质量表数据改成新证书或真实half反例。'),
 ('515a8b2e831f4c684706','integrated',[A,C],
  '2843B全文：固定秩、payoff(q,a)流/势四节点投影、n2p5非势循环、匿名自拥挤攻击、DR5000+5000阴性、弱gap−189、K17601修2520sharp/效率违规、强gap−567/9效率冲突/二支持身份、全层E和全域次模Shapley提升审查各资产全部角色。',
  '与共同客户E+BC/正边际定理、同支持七层及后续二主题纠错全文比对；未提供势数组/原代码，gap字段不推测目标归一。独立推导Φ+K|q|/固定层sharp松弛及全层E递推恢复common signed，不把宽类失败当高阶非负核必要性。',
  'integrated完整资源层级、历史审计边界与准确接续。源只入口不替其代码done；原程序0次，唯一新有限run属于固定秩证明，不借给弱强势点或全称流认证。'),
 ('d93978ddf8bd55fa56e3','integrated',[A],
  '4770B全文：m,k,M,D,L整数不交目录、次数Dσ、每真正偏离q计划重算及阈外复制、合法新B供应、参数两引理、全部次数≤k真实IC、发散、m0闭式/单调均值、次数k+1省略严格行、任意非负证书排除和历史6/2计数。',
  '逐式核q取整与(ad−1)(t−1)、复制末位剩余s、根k0与k≥1分开；和固定尾深弱化是不同截断。源6495B原程序本地缺失，未冒旧CLI；新std定义核一次、四组3260节点42578含自身39318非自身，全非负，另存省略盈利行。',
  'integrated自足任意固定k无人数统一C障碍/本族阈值，明确形式策略非SPE、非固定六人否定。新run未计时0optimizer/0原import，7168参数例和9阈值只支持实现；普遍结论由完整解析证明。')]
receipts=[]
for i,disp,targets,read,compare,decision in defs:
 receipts.append({'id':i,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,
 'read_note':read,'comparison_note':compare,'decision_note':decision,'disposition':disp,'targets':targets})
save(W/'semantic-receipts.json',receipts)

comparisons=[
 (Q,'full-text','DB逐历史商与本旧原稿全数学相同，精确publication由Root明示，非仅文件存在'),
 ('archives/customer-attraction/state/定理/共同客户收益的正边际与平衡贡献--定理.md','full-text','全层E+BC/共同signed表示，不等于nonnegative'),
 ('archives/customer-attraction/state/障碍/同支持守恒与局部客户耦合的严格间隔--障碍.md','full-text','7层固定策略量词、旧15/7缺第三耦合/后续2界，不能把宽数组当共同signed'),
 ('archives/customer-attraction/state/定理/五人索引最优偏离福利界--定理.md','sections1–3 plus model/scope before multiplier table','完整437生成规则/三族T对齐及真实菜单；未在本批复读长乘子表'),
 ('archives/customer-attraction/state/定理/固定背景三人利润界--定理.md','full-text','5/3背景剩余利润和200新行合法性，非总覆盖'),
 ('archives/customer-attraction/state/障碍/固定尾深最坏保底不足半覆盖--障碍.md','full-text','固定尾深与离轨次数截断的信息不同，均有非SPE早期缺口'),
 ('archives/customer-attraction/state/反例/四人实际根总税--反例.md','full-text from DB prior comparison retained','末节点OPT≤m um+τ真查询，与本R身份一致；旧强充分条件不同'),
 ('archives/customer-attraction/state/审查/五人局部关系来源与未复跑边界--审查.md','full-text','缺全系数时保局部推导/报告元数据的先例，不以行数当新认证'),
 ('archives/customer-attraction/state/反例/全部实际菜单混合在非负删除边际势中的失败--反例.md','full-text DB authored and reviewed','不同更宽势例、完整表3/4、违反克隆，不能借它核−567强点'),
 ('archives/customer-attraction/state/定理/五人半覆盖--定理.md','full-text in prior CR/DB review reused','历史五人OPEN已过时；2396模板障碍不冲突')]
rows=[]
for path,scope,note in comparisons:
 p=R/path
 if not p.exists():
  for old in ['r3-tree-and-abstract-menu-workspace-primary','r3-terminal-clone-primary-and-review']:
   if (S.parent/old/path).exists():p=S.parent/old/path;break
 rows.append({'path':path,'actual_read_path':str(p),**fp(p),'read_scope':scope,'role':'comparison-not-primary','comparison':note})
save(E/'comparison-manifest.json',{'search_scope':'whole customer-attraction state/evidence plus local cache: 2396/1959/74442/fixed_rank/离轨秩/同支持/全层效率；then actual mathematical objects read in stated scopes','sources':rows,
 'DB_publication':{'source':'explicit parent Root attestation','body':'838d4e94c9bb0b92639d3c9efb95205730076d9c','done':'f8f962412e751ed87f3a9f2f752233a06ab53fe7'},
 'current_source_primary_scope':'Only actual five MD, programs/inputs/comparisons notdone'})

missing=json.loads((W/'unprovided-dependency-local-export-manifest.json').read_text())
assert missing['rows']==[] and len(missing['missing'])==4
save(E/'missing-dependency-boundary.json',{'confirmed_local_absent':missing['missing'],
 'method':missing['method'],'network_attempts':0,'auth_attempts':0,'after_missing_no_retry':True,
 'effects':{'2396':'Original 38 atom masses, complete2396 matrix and74442 equality check not newly verified. Preserve report claim and independently reconstruct printed index formulas only.',
 'fixed_rank':'Complete MD plan is enough for analytic proof/new reconstructed std checker, but original6495B entry remains0 runs.'},
 'other_README_named_programs':'Not supplied as these5MD; no absence claim by Git lookup was made for all other assets, no execution/source read claimed.'})
proof=json.loads((E/'reconstructed-rank-strategy-exact-check.json').read_text())
assert sum(c['constrained_ordered_nodes'] for c in proof['cases'])==3260
assert sum(c['including_self_comparisons'] for c in proof['cases'])==42578
assert sum(c['nonself_comparisons'] for c in proof['cases'])==39318
assert proof['optimizer_calls']==proof['original_program_runs']==0
N=200526280860279758462361903492339183196;D=98776232438042792564569020207300964801
assert N-2*D==2973815984194173333223863077737253594
save(W/'runtime-summary.json',{'new_definition_checker':{'path':str((E/'check_reconstructed_rank_strategy.py').relative_to(S)),**fp(E/'check_reconstructed_rank_strategy.py'),
 'entry_runs':1,'timing_recorded':False,'optimizer_calls':0,'original_program_imported_or_run':False,
 'invocation':'python -B archives/customer-attraction/tools/evidence/quotient-and-fixed-rank-source-primary/check_reconstructed_rank_strategy.py',
 'exit_code':0,'stdout_stderr_capture':'Tool returned five JSON lines, no separate stdout/stderr files or timing. Full mathematical output saved by checker.',
 'result':{'path':str((E/'reconstructed-rank-strategy-exact-check.json').relative_to(S)),**fp(E/'reconstructed-rank-strategy-exact-check.json')},
 'total_nodes':3260,'including_self':42578,'nonself':39318,'parameter_cases':7168,'secondary_copy_cases':1179},
 'original_program_new_runs':{'fixed_rank_obstruction.py':0,'review_2396.py':0,'audit_duplicate_quotient.py':0,
  'pricing_LPs':0,'potential_DR_or_sharp_audits':0},
 'old_report_counts_not_reexecuted':['74442 coefficient equalities','2396 total slacks','44 zeros','38 strictly positive atoms','weak/strong gap−189/−567','K17601/2520 sharp'],
 'read_order':'Authorized full pre-read five MD; actual claim/owners and exact bytes verified before formal staging. Complete MD rank construction read before new checker. Missing deps local-only probe, no network.'})

save(W/'relations-review.json',{'reviewer':'Boss4/credible_cap_resume','phase':'phase2 semantic relation review, not autogenerated phase3 graph',
 'new_objects':[A,B,C],'duplicate_target':Q,'relations':[
 {'type':'same-mathematical-object-source','from':'07d379bb2632770a988b','to':Q,'reason':'Original B10 proof and DB reconstruction have the same two history-recursive constructions and scope; no new quotient theorem.'},
 {'type':'weakening-obstruction','from':A,'to':'共同目录完整历史模型','reason':'All retained rank≤k rows are genuine continuations of a formal strategy, but explicit omitted rankk+1 profitable deviation precludes SPE. Only fixedk acrossm certificate constant excluded.'},
 {'type':'valid-index-aggregation','from':'two-person tax and three-remaining5/3','to':B,'reason':'Fixed whole index sums give shown coefficients with sharedT and recorded dot only; unknown crossfamily correlations not invented.'},
 {'type':'reported-template-obstruction-not-new-replay','from':B,'to':'五人half','reason':'Original positive O−2W report concerns2396 necessary rows, lacks fullσ/OPT; current missing atom files prevent new full verification. No contradiction with provedfive-half.'},
 {'type':'representation-interface','from':C,'to':'共同客户收益的正边际与平衡贡献','reason':'Potential gradients giveBC; full-layer support efficiency gives uniqueΦ recursion/common signed harmonic representation. Nonnegative clients remain extra.'}],
 'no_false_relations':['No rank formal point→half refutation','No weak/strong loose-potential point→proof high-order nonnegative kernel necessary','No source README→all subprograms done','No reported objective/zero counts→new exact certificate']})
save(W/'self-review.json',{'status':'pass','primary_count':5,'primary_bytes':20588,
 'mathematical_checks':[
 'Old quotient proof compared nonblind against DB, prescribed representative/uniqueparent/allaliasIC and p-count boundaries exact; optionalm0 separate.',
 'Rank strategy defined recursively by past actual actions/currentplan; Dσ counts true deviations, not number of labels or taildepth.',
 'Copy q includes current, totalTcountq, freshB excludes past/current; p+1≤q≤p+r and supply r−1 proved.',
 'Parameterlemma rootk0 vs k≥1/copyj<k vs j=k separated; latercopier q>p+1 and last remaining s bound exact.',
 'm0 threshold only thisfamily; source supplied omittedrankk+1 deviation proves nonSPE; no fixed6 impossibility or full-depth ban.',
 '2396 arithmetic positive difference checked, but38 masses/74442 coefficient equality/2396 slacks not re-certified withoutJSON/rows.',
 'Same/differentindex tax uses fixed global index sets and knownZ only; fullproduct independentofunknownZ; triples use commonT.',
 'New1959 includes1662 tax+200 triple+97 not enumerated byMD; no fake complete rowmatrix.',
 'Lastnode bound isinequality, τ=W−um−R isidentity; oldW30 allcovered point only reported not newgame.',
 'PublicΦ+K|q| givesU+K, ICgap invariance and terminalsharp shift(κ−1)K; fixedtotalκ≥1 only, same-support mismatch stays.',
 'Full-layerE allk yieldsuniqueΦ recursion; common signed via arbitraryextensionC, not nonnegative integercustomers or welfareproof.',
 'PotentialREADME gap fields not assigned an invented objective;DR/sharp audits not newlychecked byrank program.'],
 'execution_checks':['5 exact local blob exports,4 dependency absences no network/auth retry; whole5claim retained, current owners/sourceSHA correct','Only1 new mathematical checker/0optimizers, originals0; finiteconstrained countincludes self','3 new selfcontained pages,1 duplicateDBtarget; quoted program metadata not primarydone','No shared Git/claim/done/credential/network mutations'],
 'remaining_gaps':['Restore original2396 atoms/rows/reviewcode before newfullreplay','Potentialcounterarrays required for ownDR/sharp/gap verification','General6half independent','Root serial publishing/done and nextowner check']})

nextpath=S.parent/'credible-next-potential-local-inputs/local-export-manifest.json';nx=json.loads(nextpath.read_text())
assert nx['missing']==[] and len(nx['rows'])==5
future=[]
for r in nx['rows']:
 p=R/f'cleanup/progress/{r["id"]}.json';future.append({**r,'current_local_progress':json.loads(p.read_text()) if p.exists() else None,
 'role':'next-source-candidate-local-export-only-not-current-primary','pre_read_or_receipt_in_this_batch':False,
 'availability':'Root must verify authoritative owner before next atomic claim; local progress absence alone is not proof'})
save(W/'next-candidates.json',{'local_export_manifest':str(nextpath),'local_bytes_all_verified':True,'network_attempts':0,'sources':future})
save(W/'local-intake-events.json',{'helper':'/workspace/scratch/37f0f9248cfc/boss4-next-cache/local_blob_export.py',
 'helper_sha256':fp(S.parent/'local_blob_export.py')['sha256'],'local_export_invocations_this_continuation':3,
 'events':[{'scope':'current5primary','result':'all5present','bytes':20588},
  {'scope':'4necessary dependencies','result':'all4missing, no network/no retries'},
  {'scope':'next5candidateMD','result':'all5present, notcurrentprimary/no semanticreceipts'}],
 'these_are_readonly_intake_not_original_mathematical_experiments':True})
print(json.dumps({'primary':5,'integrated':4,'duplicate':1,'new_formal_pages':3,'new_definition_runs':1,'original_runs':0,'next_ready_local':len(future)}))
