"""Semantic/source/relationship records for only the four actual MD primaries."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parents[4];R=S.parent.parent/'boss4-research'
W=Path(__file__).resolve().parent;E=S/'archives/customer-attraction/tools/evidence/tree-and-abstract-menu-workspace-primary'
A='archives/customer-attraction/state/候选/全部实际节点真实竞争菜单的共同混合--候选.md'
B='archives/customer-attraction/state/反例/全部实际菜单混合在非负删除边际势中的失败--反例.md'
C='archives/customer-attraction/state/等价/覆盖等价标签的完整策略商--等价.md'
D='archives/customer-attraction/state/资源/调和删除势与终局负载税的历史停点--资源.md'
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def fp(p):b=p.read_bytes();return {'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
primary=json.loads((E/'primary-manifest.json').read_text())['sources']
rec=[]
defs=[
('0625693da7f9a719c3f3',[A,B],
 '4842B完整实读：实际前缀强制a后同σ真实续局、删位置i菜单Ci/并集M、cap的独立查询量词、A与更强B、静态v桥、任意signed删除边际势外推、所有脚本/未落盘变体的有限范围及选择偏差、势层二部图/非负流未证义务。',
 '全文比较静态安全值2m−1精确证明、单节点真实菜单障碍、LAST不同背景域、匿名势客户相容性；本组global具体非负势反例已否宽外推，不能继续写其“global正在攻击、无反例”为当前状态。五人half别证/六人焦点保真。',
 'integrated自足A/B合同、蕴含及OPT≤(2−1/m)W条件用途、signed自由势模板不许偷非负余项、全部历史样本数与未落盘边界。原程序未本地提供，0原run，不用零反例升级一般定理；与抽象负例分域。'),
('24499e9900947a066aad',[B,A,D],
 '1480B完整实读：个人备份/原OPEN身份、非负匿名删除势反例的cap3/4与W2、违反克隆最坏性、不导入发现器的原审计声明、发现LP/浮点JSON角色、请求tree_dual非完成认证、逐层核性质及停止强残余/C1旧路线。',
 '与4103B反例原表逐项对照；真正CAG七客户C1反例和61客户根税/全终局税分开。其audit/LP/发现JSON本4未提供，仅历史程序合同，不虚称原程序实读或已复现。',
 'integrated构造来源与真实范围，明确请求内部核验不等于外审。保“精确势+克隆支配是否足够”未证、旧强残余导航未提供本4新见证，不以signed例冒CAG或half反例。'),
('2d96dc190eb13fd72263',[B,A],
 '4103B完整实读：全10个F/6个G势参数、18查询值、全部13动作、第二层收益表/根三分支、三实际位置背景、Q/p匹配3/4证书、严格正整体平移、CAG逐客户克隆支配必要性及3>1失败。',
 '对比tree更宽候选和representation当时未完成探针；新标准库定义检查一次0优化器，27叶/18查询/13节点39含自身26非自身、九真实强制分支及全部上下界通过。既有匿名势相容性阻止任意势编译客户；不借别的CAG反例认证本图。',
 'integrated完整自足有限反例并直接推导各菜单值3/4、1、1，从而B差3/4。A差1/12，两差整体效用加d不变。原1787B审计未提供0原run，新checker不冒同字节复现或原发现。'),
('1dc5c46e53c79b3c249d',[C,D,A,B],
 '4273B完整实读：根/题基线阅读及真实后继瓶颈、未读Boss10前独立想到商/识别既有后停建/独审评语、唯一父节点/规定类代表/合法类偏离、覆盖路径而非恰p极值；调和势和见证树停点、全终局税未算未证/61例算术、菜单和任意势探针计划/仅SciPy可用。',
 '独立重构双向逐有序历史商证明，不依缺失4628B商原稿布尔结论；比较CF/CR固定图重复标签达到性。全终局税与已有后续搜索合同/61客户实际根税全文对照，确认271/10和651/10>61。后续global势反例纠正当时尚无反例，不回填后续154策略给本源。',
 'integrated商等价自足证明、历史独立审读先验和不能保动作表/恰p的边界；资源保调和势比例损失、删除势/真实见证树未付、F候选常数与具体正余量。未开始程序不虚造执行，旧身份不触发当前认证/注册。')]
for i,targets,read,compare,decision in defs:
 rec.append({'id':i,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,
  'read_note':read,'comparison_note':compare,'decision_note':decision,'disposition':'integrated','targets':targets})
save(W/'semantic-receipts.json',rec)

related=[
('archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md','严格集合目录与标签扩展、每份完整有序历史SPE、客户整数与收益/覆盖'),
('archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md','v_m下界OPT/(2m−1)，查询与背景抽样独立；并集菜单限制的值≥v_m'),
('archives/customer-attraction/state/障碍/自适应后继与真实菜单安全值--障碍.md','单个i菜单≤ui已假，含36客户精确z1=11>10与静态v3=10；不否所有实际节点并集候选'),
('archives/customer-attraction/state/候选/实际末前背景的聚合安全值--候选.md','LAST是实际末前负载+单阻挡者，不是本A背景并集'),
('archives/customer-attraction/state/障碍/匿名计数势的客户相容性--障碍.md','自由匿名势表不必调和客户相容、signed/非负可实现分开'),
('archives/customer-attraction/state/资源/完整终局税候选的策略锥浮点反例搜索合同--资源.md','同一F未证、154策略阴性不回填；规范固定图/有理化停止点'),
('archives/customer-attraction/state/审查/R105交叉分支与regret修复障碍接续审查--审查.md','独立重构/真实后继/全终局税及旧浮点阴性为不同来源'),
('archives/customer-attraction/state/反例/四人实际根总税--反例.md','61客户AAAF完整证明；实际负载18×3/12×4/8×1，重算全终局税'),
('archives/customer-attraction/state/计算/末位克隆独审入口与两份固定锥证书--计算.md','CR成熟资源给B重复覆盖固定图和C1域；不将商路径等价升级固定图/恰p极值'),
('archives/customer-attraction/state/反例/逐人末位二倍保底的七客户反例--反例.md','真正CAG的C1反例，不与本abstract势例混作half'),
('archives/customer-attraction/state/定理/五人半覆盖--定理.md','原历史一般OPEN不覆盖当前五人已证；六人问题独立')]
rows=[]
for path,note in related:
 p=R/path
 if not p.exists():
  p=S.parent/'r3-terminal-clone-primary-and-review'/path
 rows.append({'path':path,'actual_full_read_path':str(p),'role':'comparison-not-primary','full_text_read':True,**fp(p),'comparison':note})
save(E/'comparison-manifest.json',{'query_scope':'rg over all current customer-attraction state/evidence plus local mature packages: cap_M/聚合菜单/全终局税/duplicate商/abstract_menu/39比较; actual full text read of listed objects, not filename-only inference','sources':rows,
 'CR_dependency_note':'CR59 mature package received/copied by Root, pending serial push per Root. Repo-copy existence is not independently asserted remote publication; Root confirms prior object targets before DB done.'})

missing=[('audit_abstract_menu.py','历史Fraction审计，不导入发现器；未在本4提供，不虚称读码/执行'),
 ('abstract_menu_lp.py','原浮点发现器未提供，不重构原inputs/status'),('abstract_menu_counterexample.json','原浮点点未提供；原文明确整数势证明不依它'),
 ('menu_search.py','原固定CAG图/查询锥扫描，只有README合同'),('abstract_cone.py','原signed势固定图锥扫描，只有README合同'),
 ('abstract_test.py','原随机势逆归纳扫描，只有README合同'),('probe_potential_menu.py','representation原下一探针，README当时仅恢复笔记'),
 ('duplicate_coverage_quotient.md','源引用的旧商原稿未提供；新逐历史构造承担数学证明，不额外done')]
save(E/'unprovided-related-source-boundary.json',{'network_or_lazy_loading_attempts':0,'clean_show_calls':0,
 'unprovided_related_sources':[{'name':a,'scope':b,'original_runs_this_batch':0} for a,b in missing],
 'not_a_missing_mathematical_definition':'Four primaries explicitly print complete F/G/action/matrix/minimax tables; finite example is proved from these tables and new checker. No historical program execution claimed.'})
check=E/'textual-abstract-example-exact-check.json';proof=json.loads(check.read_text())
save(W/'runtime-summary.json',{'new_definition_entry':'archives/customer-attraction/tools/evidence/tree-and-abstract-menu-workspace-primary/check_textual_abstract_example.py',
 'new_entry_source':fp(check.with_name('check_textual_abstract_example.py')),'new_entry_runs':1,'timing_recorded':False,'optimizer_calls':0,
 'invocation':'python -B archives/customer-attraction/tools/evidence/tree-and-abstract-menu-workspace-primary/check_textual_abstract_example.py',
 'cwd_at_execution':str(S),'exit_code':0,'console_observation':'Tool returned one JSON summary and no additional diagnostic lines; stdout/stderr were not saved separately. Full mathematical result saved by entry.',
 'output':{'path':str(check.relative_to(S)),**fp(check)},
 'original_program_runs':0,'original_discovery_or_auditor_reproduction_claimed':False,
 'exact_scope':{k:proof[k] for k in ['node_count','including_self_comparisons','nonself_comparisons','root_path','root_utilities','W_total_utility','exact_union_cap','W_over_m','A_violation','sum_menu_values','B_violation']},
 'read_order':'All four provided MD fully read and hashes checked before new definition checker. Pre-reading authorized by Root; actual pushed/synced13 and working owners verified before formal primary staging/receipts.'})
save(W/'relations-review.json',{'reviewer':'Boss4/credible_cap_resume','objects':[A,B,C,D],'phase':'semantic relationship review; no automatic phase3 hyperedges',
 'relations':[
 {'type':'refutation-of-generalization','from':B,'to':A,'reason':'B is a full nonnegative anonymous deletion-potential game with cap>W/m, refuting only the wide potential extrapolation. Clone inequality fails3≤1, so no CAG/half refutation edge.'},
 {'type':'conditional-use','from':'静态混合安全值的锐目录计数界--定理.md','to':A,'reason':'v≤cap(M) and v≥OPT/(2m−1), so A would imply OPT≤(2−1/m)W. Static bound alone does not pay actual welfare.'},
 {'type':'representation','from':C,'to':'共同目录完整历史模型--定义.md','reason':'Two recursive constructions preserve achievable ordered coverage paths and OPT; strategies/menu diagnostics/fixed number of distinct labels not identical.'},
 {'type':'historical-candidate-comparison','from':D,'to':'完整终局税候选的策略锥浮点反例搜索合同--资源.md','reason':'Same F(c), but this source stopped before computation. Later154 finite strategies not this source execution; 61 point has positive full-tax slack.'}],
 'no_false_edges':['No B→CAG-half refutation','No quotient→arbitrary signed potential customer implementation','No random-zero-count→universal certificate','No request-for-review→completed external review']})
save(W/'self-review.json',{'status':'pass','primary_count':4,'primary_bytes':14698,'reviewer':'Boss4/credible_cap_resume',
 'mathematical_checks':[
  'A/B exact actual-prefix real branches, deletion index, M actual-only not full tree; static column count merging distinct from policy count restriction.',
  'v≤cap(M), B⇒A and conditional OPT constant2−1/m directions correct; LAST and single-menu failures distinct.',
  'F/G tables cover all10/6 multisets, query matrix all18 and original action mapping13; exact check all27 profiles/39 including13self,26nonself.',
  'Q/p give upper/lower3/4; menu values3/4,1,1; positive translation preserves A1/12 and B3/4 gaps.',
  'Abstract W is sum utilities, not customer coverage; nonnegative/strictly positive utility not enough for clone3>1 and customer realizability.',
  'Quotient lift chosen representative must equal originalσ at lifted history; unique parent prevents conflicts; alternate representative deviation follows sameσ; converse all aliases validated.',
  'Quotient preserves actual ordered class path/OPT but changes |labels| and need not preserve original menus/fixed graph optimum.',
  'Harmonic potential not equalW; no invalid inference that a proven upper bound onΦ would fail to boundW. Source has no such budget.',
  'Full terminal tax counts allm, 18*3/4+12*4/5+8/2=271/10; 651/10−61=41/10; candidate remains unproved.',
  'Historical random variants not frozen, finite evidence/selection bias preserved, no new generic flow/external review/newness claims.'],
 'source_checks':['Original full13 receipt unprojected; actual4 current Boss4 owners/sourceSHAs; original4 local-only size/SHA256/blobSHA1','Original missing code count0 and no fetch attempt; new checker exactly1 standard-library run0optimizer','Only these4 semantic receipts; comparisons/quoted missing source/candidates notdone','New independent stage only; no shared Git/claim/done/credential/network operations'],
 'remaining_gaps':['CAG A/B general budget未证','精确势+克隆必要性质是否足够未证','完整终局税F未证','原未提供程序与临时变体无法声称复跑','Root verifies prior CR publication and candidate authoritative owners']})

inventory=[json.loads(x) for x in (R/'cleanup/inventory.jsonl').read_text().splitlines()]
candidate_ids=['07d379bb2632770a988b','3171d41e04587fac0f3c','107e8af6a50215a95107','515a8b2e831f4c684706','d93978ddf8bd55fa56e3']
nextrows=[]
for cid in candidate_ids:
 row=next(x for x in inventory if x['id']==cid);progress=R/f'cleanup/progress/{cid}.json'
 nextrows.append({**row,'local_working_progress_record':json.loads(progress.read_text()) if progress.exists() else None,
  'status':'metadata-only candidate; Root must verify authoritative current owner and exact existing local bytes before claim; missing local progress is not availability proof',
  'source_read_or_receipt_in_this_batch':False,'network_requested':False})
save(W/'next-candidates.json',{'scope':'Five concrete adjacent Markdown inventory candidates; no preclaim/primary receipts/source read','sources':nextrows})
print(json.dumps({'receipts':len(rec),'formal_pages':4,'new_definition_runs':1,'old_program_runs':0,'comparison_objects':len(rows),'next_candidates':len(nextrows)}))
