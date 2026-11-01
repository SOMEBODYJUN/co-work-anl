from pathlib import Path
import json,hashlib
B=Path('/workspace/scratch/37f0f9248cfc/warm-dag-search-stage');W=B/'cleanup/workspaces/Boss4/resume-warm-dag-search-20261101';E=B/'archives/customer-attraction/subarchives/six-providers/tools/evidence/warm-dag-discovery-primary';S=B/'archives/customer-attraction/subarchives/six-providers/state'
M=json.loads((E/'source-manifest.json').read_text());I={x['id']:x for x in M}
P=['0cce6d9347944260698c','23a9decde7450d02d501','29d0b0997f32f56dd8cf']
def front(i,k,t,title,status,summary):
 f={'id':i,'kind':k,'type_tag':t,'title':title,'status':status,'review_level':'three-frozen-primary-full-read;complete-implementation-dependencies-read;informed-analytic-reconstruction;no-current-optimizer-or-policy-replay','summary':summary,'cleanup_primary_ids':P}
 text='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in f.items())+'source_refs:\n'
 for r in M:
  for x in r['sources']:text+='  - '+json.dumps('source:'+x['commit']+':'+x['path'],ensure_ascii=False)+'\n'
 return text+'---\n\n'
prog=S/'程序/完整终局见证的热启动向量与受限搜索合同--程序.md';calc=S/'计算/两人两主题热启动原始对偶证书与版本边界--计算.md'
for p in [prog,calc]:p.parent.mkdir(parents=True,exist_ok=True)
raw='../../tools/evidence/warm-dag-discovery-primary/original/research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/'
prog.write_text(front('customer-attraction/warm-start-outcome-witness-DAG-adapter-contract','program','程序','完整终局见证的热启动向量与受限搜索合同','complete-source-contract-and-seed-feasibility-reconstruction;floating-search-only;sample-version-mismatch-preserved','以精确BI全部终局构造与原DAG同索引的y/z/x/t热向量，保自由重数/非Markov见证、private HiGHS适配、cold/二元局部分支/菜单限制及固定policy精确恢复；旧样本非当前脚本运行绑定。')+r'''# 完整终局见证的热启动向量与受限搜索合同

## 数学对象、来源与使用范围

本对象完整保存9844B冻结warm_dag_search.py的输入、索引、优化域、输出和局部限制，不将实现启动成功改为福利定理。三主源共12485B：原程序9844B、两人两主题报告2491B、历史workspace元资料150B。均正常clean show全文读/导出并核大小/SHA；owner已按新clone当前progress核为Boss4。

通用底层是有限单位客户、m≥1单位提供者、p≥1共同标签、全部有序历史纯SPE。非空兴趣类型B⊆[p]的整数重数表示不同单位客户；浮点MILP暂用非负实数质量，精确有理点清分母才回单位客户。空主题、重复行动、同覆盖不同标签和全部平局保留。原集合目录的互异覆盖只是标签接口的子域，程序不强制p个标签覆盖互异。

底层[终局见证DAG完整历史等价](../../../../state/等价/终局见证DAG的完整历史可实现性--等价.md)已经给精确存在性和M=1扩展。本程序只给该系统完整可行向量及solver adapter；不假设计数统一动作，不枚举每份完整策略，也不改写[计数净化严格分离](../../../../state/反例/完整历史与计数统一策略的严格分离--反例.md)。

全部原件、完整依赖布局、版本表见[证据说明](../../tools/evidence/warm-dag-discovery-primary/README.md)。2491B小报告对应的warm源码哈希与本9844B冻结程序不同；当前源码不能借该报告称已执行通过。小报告的数学点可独立解析认证，见[两人原始对偶证书](../计算/两人两主题热启动原始对偶证书与版本边界--计算.md)。本次未import或执行warm/原DAG/LP/SPE搜索。

## 依赖、根目录与导入行为

原程序向上寻找第一个含customer_attraction/__init__.py的目录作为ROOT，插入ROOT和ROOT/tests/audits；import规范ExactSPESolver、固定策略锥helper中的instance_from_clones/coverage_row/dot/serializable。再按固定相对路径动态导入R-3d6f…/true_spe_search/outcome_dag_milp.py，后者的完整9778B冻结SHA为c7d5507591d395be7353cea1e2f07cd5f4390f5bc15e3120fa51607f094cba4f。

原代码在顶层import NumPy、SciPy和scipy.optimize._highspy._core，依赖其私有HighsLp、_Highs、setSolution等接口。这是**冻结实现的接口身份**，本次未检测当前安装版本是否仍可运行，也未把私有接口故障当数学障碍。main guard只防止自动执行main；import本模块仍会加载科学库、搜索ROOT、动态导入旧DAG，因此当前也不import它作“只读检查”。

证据original目录按原相对布局保warm程序、底层DAG、20567B策略锥helper及customer_attraction四文件（init/model/exact/certificate）。未改原代码或创建冒充旧源码的shim。另保6193B研究README、3471B审计脚本作related；后者读取的外部Markov原输入不属于这份最小warm运行闭包，本批未执行该审计或下载其全部有限输入。

## 全部CLI与真实优化域

| 参数 | 默认/合同 |
|---|---|
| --players | 5；程序要求m>0 |
| --topics | 7；程序要求p>0 |
| --root | 逗号整数向量；默认(m,0,…,0)，长度p、总和m；还须通过精确oracle成员检查 |
| --seed-file | 可选JSON；只取exact_candidate.integer_clones，不复用其动作表/根/参数/对偶 |
| --portfolio | 可选逗号标签元组；默认按seed单标签私有客户数降序、标签升序取前min(m,p)个 |
| --floor | 可选float目标下界；未给时按seed比较覆盖/seed实际覆盖自动给一条float下界 |
| --seconds | 30，传HiGHS time_limit；不包括精确集合构造和后续固定锥LP，不能称整个命令硬墙钟上限 |
| --seed | 20261021，HiGHS random_seed |
| --radius | 可选二元Hamming局部半径；有意义的预期域为非负整数，parser未专门拒负半径 |
| --cold | 不把seed向量传setSolution；仍先构造并检查同一seed，不等于没有oracle预处理 |
| --restrict-outcomes | 把非seed保留目标的y上界置零，限制旧seed的终局菜单 |
| --output | 必填Path；write_text写最终缩进JSON，现文件会覆盖；不自动建缺失父目录 |

缺省seed类型向量有2^p−1项，只有singleton类型非零：标签a的私有客户数max(q_a,1)。如给seed-file则替换整个向量。initial_vector检查p,m、向量长度、构造合法规范Instance、q确在精确可实现根终局集及根福利正；非法或非SPE可实现seed不能充当热启动。全零根福利被明确拒绝。它没有把输入根终局强制为当前seed唯一根终局。

固定p,m、根q和portfolio后，原build联合优化**所有**类型的非负实数重数及二元DAG见证，W(q)=1，每个主题质量≤1，阈值t∈[0,1]；没有传fixed_clones。seed仅提供可行起点，不把自由客户变量固定为seed。M=1的通用理由是：根SPE中每个角色查询任意T都可保证|T|/m，全部m角色IC相加给|T|≤W(q)，故归一化后任意子博弈个人利润≤1；完整证明已在底层等价对象。

目标是给定portfolio的覆盖/W(q)，不是自动遍历所有最优比较支持，也不是MILP中直接最大OPT/W。默认portfolio合法且至多m；显式CLI没有验证标签范围、互异或支持数≤m。helper coverage_row用sum(1<<a)拼mask，重复标签可发生二进制进位，不能解释为并集；不合法显式portfolio不能称半覆盖比较。当前小报告的(0,1)满足所有合法条件。若seed-file有交集客户，默认按singleton质量排序只是启发式，不保证取到真正OPT支持；最终另计算的optimal_welfare与固定目标value应分别读。

## initial_vector：全部计数状态、相同变量索引与可行性证明

记R(k)为规范ExactSPESolver在过去计数k的全部可实现终局，

\[
M(k)=\max_b\min_{d\in R(k+e_b)}u_b(d).
\]

它的集合值逆向归纳缓存不固定同计数历史的一个动作。所有非终局R(k)非空；c∈R(k)当且仅当至少一个行动a使c∈R(k+e_a)且u_a(c)≥M(k)。调用solver.outcomes()先算全部集合，q∈R(0)才接受。

程序按深度0…m列所有p维非负计数states，并列总数m的leaves；below[k]={c≥k:|c|=m}。变量顺序与旧DAG完全相同：先2^p−1个客户质量；逐state列y[k,c]，每个非终局state后插t[k]；再对每个非终局k、每行动a、每c∈below[k+e_a]交错列z[k,c,a]和x[k,a,c]。不只seed向量长度相同，还需这份完整同序约定；当前底层哈希已绑定，不能随意替换构建器后沿用。

令s=W(q)>0，客户质量seed_w=w/s。取：

- 非根Y(k)=R(k)，根Y(0)={q}；y在对应集合置1，其余0。终局R(c)={c}，因此所有终局y均1。
- t[k]=M(k)/s。
- 对每个c∈Y(k)，取按标签从小到大第一个a，满足c∈R(k+e_a)且u_a(c)≥M(k)，将相应z置1；其它z零。
- 对每个k、每个a，选R(k+e_a)中使(u_a(c),c)按字典序最小的d，将x[k,a,d]置1。其当前行动利润≤M(k)。

这给原精确DAG所有约束：Σ_a z=y；被选实现终局保留于孩子y，且u_a(c)/s≥t；每行动恰一个x、该惩罚在孩子y中，且u_a(d)/s≤t。未选约束由归一化利润/阈值[0,1]和M1自动松弛。W(q)归一化、质量界及终局/根y固定值亦满足。所有二元位由0/1直接赋值，阈值是规范精确量转float。

因此数学可行性来自底层精确等价与oracle集合递推，不是因为残差容差小便变成精确证明。对同计数不同目标c，所选a可不同；展开时真实状态是有序历史h与desired终局c，非计数Markov限制。返回meta有seed_root_outcomes、seed_exact_optimum、seed_welfare和规范缓存stats；main另计construction_seconds。

## WarmSolver：残差、局部分支和菜单限制的逐式含义

adapter接收旧build传入的目标c、integrality、Bounds、LinearConstraint，将稀疏矩阵转CSC并复制变量上下界。如--restrict-outcomes，只遍历事先按同索引重建的全部y位置，把seed[j]<0.5者上界置0；其它变量界未另改，x/z通过原约束只能使用被保留孩子。固定输入的真实终局菜单被限制为旧seed可实现菜单，这只是原模型合法子集，不排除全SPE。

先assert目标长度等于seed长度，再计算

\[
\max\{(lb-A\,seed)_+,(A\,seed-ub)_+,
(low-seed)_+,(seed-high)_+\}
\]

全部分量最大值，超过1e−8即拒。这个检查在加入局部分支行**之前**做，且只核float行/界残差，不把它称独立精确IC或一般可行性证明。二元整性由seed构造得到；此adapter没有另算integrality残差。

如给radius R，令J₁为seed二元位1的集合，J₀为0的集合，添加

\[
\sum_{j\in J_0}b_j-\sum_{j\in J_1}b_j\le R-|J_1|,
\]

等价于Σ_{J₀}b_j+Σ_{J₁}(1−b_j)≤R。因此仅限制y/z/x二元见证离seed的Hamming距离；客户质量和阈值连续变量不在半径中。它限制搜索范围，不修改原SPE约束。负R会排空此邻域，原代码未先作专门非负校验，不能把失败解释为原模型不存在解。

随后直接填HighsLp：连续/整数列类型、列成本/界、行界、CSC列起点/行指标/值。设置output_flag=False、time_limit、random_seed、mip_rel_gap=0、threads=1；passModel必须返回kOk。若非cold，将**全部变量**索引/值传setSolution并核返回kOk；API接纳起点不证明整数MIP已求全局最优。

h.run()后取solution/info/model status。只当status=kOptimal时adapter返回status0，否则统一status1；不能把这个简化status1自动解释为同一种不可行/时限/错误。solution.value_valid决定x是否返回，fun来自info目标。warm.info记录seed供给、最大残差、seed float目标、原status字符串、实测solver秒、节点数、有限时才保留的float gap和符号翻转dual bound，以及radius和restricted布尔。float dual_bound明确名为not_certificate。

旧build从返回x按z/x最大值选择见证，每个被选值须≥0.9，然后递归展开所有有序历史，规定分支保持desired终局，其余分支用共同惩罚终局。0.9门槛和MILP状态均只是发现步骤；最终数学有效性由下节精确重算承担。

## 固定完整policy的有理恢复及其对偶量词

main用warm替换dag.milp，然后调用同一build；搜索后先stdout打印stage=mip_finished_before_exact_policy_reoptimization及solver信息。接着若有cone，调用旧dag.exact_optimize(cone,objective)。它优化的是**刚展开的这一份完整动作表**客户锥，不再是原全部见证MILP。

对该完整策略σ，构造全部真实有序历史的收益差，去零、去重后按Fraction元组字典序排序为Γ；客户r≥0、Γr≥0、实际覆盖w·r=1。浮点LP给候选后，各坐标用Fraction(float).limit_denominator(10^7)恢复；若非负/全部Γ或归一化有一项失败，改在浮点正支持（>1e−8）上取近活跃行（残差<1e−7），用精确消元恢复顶点。恢复后仍须完整非负/Γ/归一化检查，失败报告certified=False。

通过后清公共分母、除整数gcd得不同单位客户克隆；independently_verify按所有有序历史和全部动作，用直接Fraction效用核真实后继，不调用规范均衡验证器，但仍属于同一代码依赖闭包而非外部新审查者。它还另用规范Instance算实际福利与至多m主题最优覆盖。

对偶从LP marginals恢复β及μ，逐类型严格核

\[
\beta\ge0,\quad\mu\ge0,\quad
\beta w-\Gamma^\top\mu\ge objective.
\]

若有效，它只给该固定policy锥的精确目标上界；若又等于可行原始值才标dual_optimal。certified=True首先表示原始点和完整SPE已精确核，即使未恢复对偶也可能如此，不能把它读成全MIP全局最优。

后续固定policy LP没有重新加入MILP的floor、二元radius或整套y菜单约束，也未重新优化其它动作表；其原始/对偶认证合同是非负完整policy客户锥。半径和菜单用来发现policy，不是这份LP精确上界的新增全域前提。单个返回policy的精确值不能排除别的SPE或目标反例。

## 全部输出、副作用与样本版本断口

最终result包括scope、universal_bound_proved=False、random seed；environment中的Python/SciPy/NumPy版本、**当前文件自身SHA**和旧DAG文件SHA；parameters完整CLI配置；warm_seed meta；solver adapter信息；原milp统计；exact_candidate或None。serializable将Fraction转字符串、tuple转list、dict key转字符串。最终输出路径write_text覆盖写，stdout最后brief删exact_candidate里的strategy、integer_clones、dual_support；完整文件才保全部证书。stage消息已出现不保证后续LP已完成或最终文件已写成。

本9844B程序SHA为6e4195ac3155401980f26a0255ec55d8d6a11e93355b04bd9b6b436f4dfcc7bf；2491B报告自报warm_script_sha256为20a37c1c93c56f810bf19eafb401b340b23f05d7e55b11a792ebe547f1982c45，**不相同**。报告旧DAG SHA却与当前9778B一致。本批未取得20a37…源码，不能补造差异发生在何行，也不通过重跑当前版本来替代旧版本执行认证。文件内容可作为历史运行及独立可算证书保留，而非当前9844B脚本的已验证运行。

研究README报告五人七主题cold/warm性能、42有限seed检查及9/5/23/14完整证书，都是它所指原文件的历史层。本批读了README与3471B审计源码，未将其全部大报告/42输出当primary读取、未复跑这些成功实验；不填造新性能数字。较早大规模DAG启动失败已在[原DAG计算资源](../../../../state/计算/终局见证DAG的原审计与固定锥预算复核--计算.md)准确保存，热启动属于实现接续。

## 150B元资料的完整身份与处置

workspace.json四字段原样为schema=1、save=customer-attraction、actor=R-44b24f3962bd4f68a4b6913610c0d417、instance=47c2dd9a35e747ea9286ade9660b79c1。它是旧协作工作区路由/身份元数据，不是客户实例、DAG状态、策略、客户重数、数学假设或本次Boss身份；不加载它切换当前工作区，也不把opaque instance键当模型输入。四字段完整保在原件和本资源，处置retained只保来源身份，不另造数学命题。

## 关系、现状与可接续边界

完整历史模型→终局见证等价提供数学基础；本程序以精确R(k)构造起点并适配私有求解器；旧DAG负责原MIP与完整展开，固定策略锥负责有理原始/对偶，2491B小点提供一份历史有限证据及可直接解析的数学样本。源代码版本与运行报告的断口单独保留，不混成一条当前运行认证。

本次原CLI/import/MIP/LP/oracle执行/全策略重放均0，仅取源、逐字节核/源表/链接检查。一般两层见证构造、float残差、固定policy精确证书、全局福利命题各有自己的量词。当前五人half已有别证，六人目标没有由本warm工具解决；同一短时配置的重复阴性运行不增加一般信息。源作者外审和新颖性未认证，逐关系理由另保工作区relation-evidence.json，未自动更新第三阶段超图。
''')
calc.write_text(front('customer-attraction/two-player-two-topic-warm-start-fixed-policy-certificate-version-boundary','computation','计算','两人两主题热启动原始对偶证书与版本边界','exact-small-certificate-analytically-reconstructed;historical-float-run;warm-script-hash-mismatch','完整保存2491B两人小报告字段及三个历史策略，直接重构两个固定锥收益行和β3/2原始对偶；旧warm运行SHA不匹配当前源码，浮点MIP最优不冒一般最优。')+r'''# 两人两主题热启动原始对偶证书与版本边界

## 固定客户与全部有序策略的解析认证

三兴趣类型按(A,B,AB)排序，原integer_clones=(2,1,0)：A有两名私有单位客户，B有一名，二主题不交。两名单位提供者顺序选共同目录A,B。完整动作表只有三个决策历史：

| 历史 | 规定动作 | 真实完成 |
|---|---|---|
| ∅ | A | AA |
| A | A | AA |
| B | A | BA |

末位见A时，规定A得1，改B得1；末位见B时，规定A得2，改B得1/2；根规定A沿AA得1，改B后真实续局BA使根得1。三项非自身松弛分别0、0、3/2，故全三历史构成完整纯SPE。客户W(AA)=2，选择AB覆盖3，所以OPT₂=3、比率3/2；不存在half违反（2W−OPT=1）。不是六人证书，也不假定严格或唯一根行动。

## 这张固定policy客户锥的全部精确原始/对偶

任意非负客户质量(a,b,c)，actual AA覆盖w·r=a+c。完整三个真实非自比较中根与历史A的型行相同，去重/去零并按Fraction字典序排序，恰为

\[
\Gamma_0=(1/2,-1,0),\qquad
\Gamma_1=(1,-1/2,0).
\]

第一行来自A均分收益(a+c)/2与偏离B在AB得b+c/2，第二行来自BA的A得a+c/2与改BB得(b+c)/2。两行共同要求a≥2b及a≥b/2，后者在非负域中由前者蕴含；这是原固定完整策略锥，不是任意二人策略的行集。

归一化a+c=1，比较portfolio(A,B)目标v=(1,1,1)，即(a+b+c)/(a+c)。原始点r=(1,1/2,0)可行，目标3/2，清分母即原(2,1,0)。取β=3/2、μ₀=1、μ₁=0：

\[
\beta w-\Gamma^\top\mu-v
=(3/2,0,3/2)-(1/2,-1,0)-(1,1,1)
=(0,0,1/2)\ge0.
\]

这严格认证该policy锥的精确最优3/2，dual_support索引0就是上面明示排序的Γ₀。不能换另一动作表或行排序后沿用该索引。它也不由求解器float状态证明全见证MIP的最优；当前已知两主题一般基准另可从末位IC得出，见[原DAG有限审计与基准](../../../../state/计算/终局见证DAG的原审计与固定锥预算复核--计算.md)，本样本不重认新福利定理。

以上是直接有理代数和全部三真实比较，未执行原程序或新验证实现；一般warm seed构造/限制见[程序合同](../程序/完整终局见证的热启动向量与受限搜索合同--程序.md)。

## 原2491B报告的全部配置与字段

原件ID23a9decde7450d02d501，SHA2d2a4eb6a6db86b22add605dff9b977995230538c87a503f1525b5d3b5797866。文件root共9个字段组，下列完整展开所有内容，不把brief当完整文件。

| 组 | 原字段和值 |
|---|---|
| scope | warm-start full-history outcome DAG search; optional explicit subset restrictions; floating search plus exact full-policy verification |
| universal_bound_proved / seed | false / 20261021 |
| environment | python3.12.14、scipy1.17.0、numpy2.3.5；warm_script_sha256=20a37c1c93c56f810bf19eafb401b340b23f05d7e55b11a792ebe547f1982c45；original_dag_sha256=c7d5507591d395be7353cea1e2f07cd5f4390f5bc15e3120fa51607f094cba4f |
| parameters | players2、topics2、root[2,0]、portfolio[0,1]、requested_solver_seconds1.0、seed_file=null、objective_floor=null、cold=false、local_branching_radius=null、restrict_outcomes=false |
| warm_seed | seed_root_outcomes2、seed_exact_optimum3、seed_welfare字符串2；seed_stats={count_states6,terminal_states3,retained_outcomes8}；construction_seconds0.00034374899996691965 |
| solver | warm_start_supplied=true、warm_start_max_constraint_violation0.0、seed_objective_float1.5、solver_status=HighsModelStatus.kOptimal、solver_seconds0.00039105099995140336、mip_nodes0、mip_gap_float0.0、dual_bound_float_not_certificate1.5、local_branching_radius=null、restricted_outcome_candidates=false |
| milp | topics2、players2、root_counts[2,0]、variables32、binary26、rows49、status0、message=HighsModelStatus.kOptimal、seconds0.0011071809999521065、floating_value1.5、floating_bound_not_a_certificate=true |
| exact_candidate | certified=true、value字符串3/2、integer_clones[2,1,0]、exact_dual_bound字符串3/2、dual_optimal=true、dual_support[[0,字符串1]]、welfare2、optimal_welfare3、nodes3、deviation_checks3；strategy含terminal_counts[2,0]及上节完整三个history/action记录 |

root9字段组数中scope、universal_bound_proved、seed分别独立；environment/parameters/warm_seed/solver/milp/exact_candidate共六，合计九。上述程序秒数/状态/残差是**冻结历史测量**，不是本次新run。construction、solver和milp三个时间口径不同，不能合成墙钟或性能保证；mip_nodes0、gap0与kOptimal只保float求解器记录身份。

原norm seed的两个根可实现终局与六计数state/三terminal/八retained来自原oracle统计；它不是全部有序策略的数量。当前完整三动作表只给一份实现，不枚举所有SPE。

## 必须保留的源码版本差别

| 对象 | SHA256 | 与本冻结源码绑定 |
|---|---|---|
| 本9844B warm_dag_search.py（0cce…） | 6e4195ac3155401980f26a0255ec55d8d6a11e93355b04bd9b6b436f4dfcc7bf | 当前主源 |
| 本2491B报告自报warm_script_sha256 | 20a37c1c93c56f810bf19eafb401b340b23f05d7e55b11a792ebe547f1982c45 | 不匹配；本批未取得该源码版本 |
| 本9778B旧DAG依赖/报告original_dag_sha256 | c7d5507591d395be7353cea1e2f07cd5f4390f5bc15e3120fa51607f094cba4f | 匹配，原字节已核 |

报告有环境与源码hash，比无版本日志更具体，但仍没有完整argv或原exit/stderr事件；parameters不能自动冒成原shell命令。没有把未知20a37…源码推测成当前某几行变化，也不以重跑6e419…覆盖历史版本断口。

报告的数学原始点/三历史策略/精确对偶完全显式，所以上两节可自足证明它陈述的固定锥结果，不依赖未知旧warm版本的正确性；这不为9844B当前adapter或其所有选项额外认证。当前版本完整行为由程序对象实读说明，已有历史成功实验无须为清洗重复运行。

## 来源、关系与不推出的结论

本primary JSON与9844B程序及150B元资料均全文处理；required-related9778B旧DAG、20567B策略锥helper、规范模型/精确oracle/证书及6193BREADME/3471B审计源码亦实际全文读。旧DAG source hash与其已归档成功原审计证据匹配，故未重复旧60次MILP或两次固定锥回归；也未跑本warm小点或大规模实验。

该小证书实现了底层终局见证存在性的一份合法输入，展示固定policy原始对偶可用，而非给一般MILP浮点界加精确等级。Warm版本差是来源/实现认证边界，不改变已明写策略的直接数学验证。三人非Markov/五人七主题/六人half都须各自证据；不由两人样本作人数外推，无外审和新颖性认证。
''')
# Historical root group count check is structural data-reading, not mathematical verification.
report=json.loads((B/I['23a9decde7450d02d501']['local_path']).read_text())
(E/'version-and-execution-scope.json').write_text(json.dumps({'primary_files':3,'primary_bytes':12485,'frozen_warm_script_sha256':I['0cce6d9347944260698c']['sha256'],'report_warm_script_sha256':report['environment']['warm_script_sha256'],'warm_script_matches':I['0cce6d9347944260698c']['sha256']==report['environment']['warm_script_sha256'],'original_DAG_matches':I['ba24829ca8aa642f892c']['sha256']==report['environment']['original_dag_sha256'],'current_original_cli_runs':0,'current_imports':0,'current_MILP_calls':0,'current_LP_calls':0,'current_oracle_calls':0,'current_policy_replay_implementation_runs':0,'new_math_implementation_runs':0,'analytical_reconstruction':'three explicit history comparisons; two fixed-policy exact rows; beta3/2 mu(row0)1 and residual(0,0,1/2); warm-seed feasibility from existing outcome-DAG theorem','old_report_version_source_obtained':False,'no_runtime_dependency_versions_verified':True,'root_report_field_count':len(report)},ensure_ascii=False,indent=2)+'\n')
(E/'README.md').write_text('''# 完整DAG热启动的原代码、小证书与元资料

正式说明：[程序合同](../../../state/程序/完整终局见证的热启动向量与受限搜索合同--程序.md)、[两人原始对偶证书](../../../state/计算/两人两主题热启动原始对偶证书与版本边界--计算.md)。

三主源12485B位于original原目录布局：9844B warm_dag_search.py、2491B warm_m2p2_final.json、150B workspace.json。source-manifest.json给11个本批实际全文读取并保留的源原件（3主源、8related/依赖）、全部大小/SHA/blob/双冻结来源。original根下model/exact/certificate/init、tests/audits策略锥helper、R3d6旧DAG满足warm脚本的路径查找布局；NumPy/SciPy私有接口依赖仍须单独满足，当前未import或执行。

小报告自报warm源码20a37…与当前6e419…不匹配；旧DAGc7d550…匹配。版本与零运行边界保于version-and-execution-scope.json，不把历史小报告绑成当前程序执行；小点数学已完整解析重构。

本related审计audit_warm_start.py还引用外部Markov报告，本包未替它补齐该审计运行数据；6193BREADME的42回归/大规模报告仅按历史所述，未借此称本次读完或复跑它们。不得对这些related源额外done。
''')
print(json.dumps({'formal_paths':[str(p.relative_to(B)) for p in [prog,calc]],'root_fields':len(report),'warm_hash_match':False,'math_runs':0},ensure_ascii=False))
