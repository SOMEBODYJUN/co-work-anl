---
id: customer-attraction/free-fractional-epigraph-fenchel-policy-cone-probe-contracts
kind: program
type_tag: 程序
title: 自由分数门槛的上界求值与Fenchel策略锥探针
status: 三原程序及Search闭包完整保留；仅数值探索，当前0原入口且未生成新候选
summary: 给SLSQP上图问题、count/target完整策略锥、冻结p/z的全背景下界与固定子q上界的精确数学方向；区别实际W归一与OPT、integer v与free t及原数值字段。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/security/fractional_minmax_probe.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/security/optimize_fractional_floor.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/security/search_fractional_drift.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/round3_security/search_security.py
---

# 自由分数门槛的上界求值与Fenchel策略锥探针

2386/6048/2567B三原码全部函数、参数、字段与写入行为全文，必要兄弟Search6376B也全文、逐件size/SHA/blob核。原模块导入numpy/scipy，当前只文本/AST读取，0导入、0原main、0LP/SPE求解器/随机运行；原Numeric Only状态保持。源与完整可恢复相对布局见[证据目录](../../tools/evidence/free-fractional-security-program-contracts-primary/README.md)。它们有可继续用的发现合同，不是一般上界证明或完整反例证书。

## 模型、值和两个被搜索的接口

原单位客户、n名单位提供者、有限非空共同目录，完整纯SPE在全部有序历史上定义，保空题、重复选择、零客户及任意历史依赖平局。若以k标签表示，客户兴趣类型B⊆[k]、整数重数w_B表示不同单位客户；零类型不参与。canonical/Search还允许同覆盖异标签，属于标签输入扩展；若候选零权导致物理题合并，不能擅自删标签后仍借原完整策略比较。

令M_(B,a)=1_(a∈B)，合法过去背景b、剩r≥1。代码value对应[自由分数门槛](../定义/自由分数背景安全门槛--定义.md)
\[
 t_r(b)=\min_{q\in\Delta_k}\max_a
 g_a(q),\qquad
 g_a(q)=\sum_B\frac{w_BM_{B,a}}{1+b_B+(r-1)(Mq)_B}.
\tag{1}
\]
r−1是分数竞争质量，自身另占一，不是顺序玩家的承诺。静态函数可对任意非负b求值；应用SPE时b必须合法。数学定义涵盖零客户；随机搜索跳全零输入，含relative分数的记录另需正福利。

代码中同名value/字段实际不同：

| 位置 | 数学对象 | 原精度/证据 |
|---|---|---|
| fractional_minmax_probe.value | 自由分数t_r(b) | SLSQP浮点上图解；r1直接浮点max |
| Search.evaluate结果value | 真正整数竞争混合安全值v_n(0) | 有限矩阵HiGHS数值LP |
| trial.root_value/next_value | t_n(0)、t_(n−1)(1_a) | 两次value数值结果 |
| trial.query_load/next_query_load | 竞争背景分布q、q_child | 名称含query，但它们不是查询分布p |
| optimize.root_query/root_z/root_fractional_q | 查询p、逐类型逆分母z、竞争q | 最后一次saddle的浮点向量 |

真v的竞争者先选n−1个整数主题元组分布且不看query实现，free t在平均负载分母中放松，只有t≤v，不可换名或宣称等号。

设实际根行动a、根收益u。floor搜索的量是δ=u−t_n(0)；local搜索是
\[
 D=u+(n-1)t_{n-1}(\mathbf1_a)-nt_n(0).
\tag{2}
\]
child背景1_a合法，未删根玩家。前缀嵌入给t_(n−1)(1_a)≥t_n(0)，所以D=δ+(n−1)(child−root)：D<0蕴含δ<0，但δ<0不能单凭此推出D<0。沿整个真实路径对相应局部D望远镜可得ΣD=W−n t_n(0)，末位u=t_1使末项0。因此逐步非负会是强聚合的充分桥；一个负首步只攻击该局部机制，不反聚合或half。当前一般FF已被[真实银行族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)否定，不需要把旧有限阴性搜索继续当其证据。

## value的真实上图问题及数值边界

对r>1原函数取y=(q,T)，求min T，约束q≥0、Σq=1、q≤1、T≥0及每个a有T−g_a(q)≥0。令d_B=1+b_B+(r−1)(Mq)_B，其解析Jacobian为
\[
 \frac{\partial(T-g_a)}{\partial q_j}
 =(r-1)\sum_B\frac{w_BM_{B,a}M_{B,j}}{d_B^2},
 \qquad\partial_T=1.
\]
每g_a对q凸，故这是正确的凸上图数学问题。初始q均匀、T0=max g(q)，原参数SLSQP maxiter500/ftol1e−11；out.success为假即抛RuntimeError，否则直接返回out.T、out.q、重算pay向量。代码没有输出精确原始/对偶残差证书，success不能变成有理最优性。

任何**确切可行**q确实给t_r(b)≤max_a g_a(q)上界；返回的浮点T还须核其全部约束才能当可靠上界，更不能作为下界。r1时返回max_aΣwM/(1+b)、零q占位和pay；q在零竞争质量时无关，零向量不是要冒充概率分布。[凸minimax与有理下界定理](../定理/自由分数门槛的凸对偶与覆盖价格界--定理.md)另给真正下证书，单个近似优化值不承担它。

此函数接收矩阵/权重/背景，未作完整数学域或畸形输入校验。这里的合同是0/1关联、非负权/背景、r≥1、非空k；原CLI搜索不因此覆盖所有退化模型或任意无界机器整数。

## main嵌入的两份旧真SPE，不是两个新free反例

value原main没有读外部输入文件，而内嵌两个mask→整数重数字典与路径(0,3,4)。AST literal逐类与已发表原例完全相等，并全文读两份43行完整策略及其原静态证书，[绑定记录](../../tools/evidence/free-fractional-security-program-contracts-primary/embedded-case-binding.json)保全部类型/原action行。其旧充分IC验证复用，当前不重跑。

| 既有例 | 单位客户/类型 | 实际利润 | W / OPT |
|---|---|---|---|
| local_security_increment | 113 / 19 | 95/3，110/3，110/3 | 105 / 113 |
| individual_security_failure | 34 / 13 | 29/3，67/6，67/6 | 32 / 34 |

两个完整策略均根0，第二人选相反组三标签中的最小者，第三人在第二主题所属组选此前未出现的最小标签；全部重复/离轨历史保留，旧43节点×6=258含self比较已充分通过。原例来源分别是[真正整数安全值的局部付款反例](../反例/真实前缀逐步安全值付款--反例.md)、[34客户逐人混合安全值反例](../反例/三人逐人混合安全值--反例.md)。它们的匹配v3/v2证书是整数竞争安全值，不能改成free t证书。

原main依actual逐层更新b，调用r3、2、1的value；按显示终局的整数负载另用浮点算三利润，打印两条JSON行，每条有name、values、utilities、debts、aggregate，其中debts两项按(2)同样的逐步形式，aggregate=W−3·values0。它不检查完整SPE，也不自写报告。这两例作为真SPE的依据来自已发表完整证书，非这个数值脚本的注释或三利润向量。当前未生成其新stdout，不从既有整数安全值反例推它们也反自由t或推断原数值结果。

## Search的整数终局集合和count/target策略DAG

两发现器按精确旧相对路径导入兄弟R-acd…/round3_security/search_security.py，而不是默换规范库。Search取全部非空2^k−1类型，预枚举长度0…n的计数态及终局索引j。L=lcm(1,…,n)，实际占用行动a在终局ν的系数为L·1_(a∈B)/(Σ_bν_bM_(B,b))，非零分母整除L。整数w时效用比较可用整数共同分母；实现用numpy int64，精确断言须限定无机器整数溢出的实际输入范围，未提供任意位长算术保证。

对prefix计数q的各行动a，child终局集合C_a，设θ(q)=max_a min_(j∈C_a)U_a(j)，则
\[
 R(q)=\bigcup_a\{j\in C_a:U_a(j)\ge\theta(q)\}.
\tag{3}
\]
每个非规定孩子可独立选使偏离者收益最低的子SPE，故阈值给可实现终局的必要充分条件；不同有序孩子是不同子树。缓存集合不把同计数历史指定为同一个续局，也不枚举所有完整策略图。浮点w会使这些比较变成浮点，不能沿用“整数DP精确”认证任意非整数种子。

policy_cone以(root counts0,target j)开始，状态是(q,j)，同q不同target分别保。规定行动可通向同target，root用指定first_action、其余用第一个可行行动；每个偏离b送到旧权重下该child集合中使U_b最小的target。对所有孩子递归、相同(q,j)共享，深度每次增一，故可沿有序历史携带target展开完整策略。它不是仅按q的Markov图，也不是任意挑未相容子局。

每状态/每行动的规定−真实偏离收益系数形成Γ，非零整数系数行先精确去重再转float/L。固定这些孩子选择后，w≥0、Γw≥0足以使**同一份**展开策略成为SPE；不必在新w下重新求最差child集合，因为真实完整动作图已固定。但原输出policy只存prefix/target/action，未显式保存全部偏离target边，恢复还需同版本Search终局索引/原种子和确定选择过程；它不是直接交给通用有序策略验证器的actions表。

Search.evaluate还总会解一次真正整数混合安全值浮点LP，并计算min_welfare、worst_counts、静态终局PNE偏离等元数据，即便调用者只要outcomes。原drift的errors可能来自这层LP或value的SLSQP；不能全叫自由值求解失败。搜索的整数SPE存在性、这项数值v、全策略图和后续数值t是四层不同证据。

兄弟Search的standalone main是另一发现入口，导入该类不会执行它：默认n4/k5/trials3000/seconds120/seed763031，只把有非PNE最差SPE终局的记录入至多30项bank，80%从bank改1…4个权/幅度−10…10，否则产生0…19稀疏权，去通用类型；按相对整数安全值缺口排序，浮点gap<−1e−7早停，写EXPLORATORY/best/bank。它没有在本三主源中被调用或额外done，不能把它的参数/输出与55秒free-drift main混成一次运行。

## Fenchel冻结行为什么给全背景下界

固定查询概率p，ρ=Mp，任取z_B≥0。对c_B=1+b_B>0及任意x_B≥0，
\[
 \frac1{c_B+x_B}\ge2z_B-(c_B+x_B)z_B^2,
\quad\text{差}=\frac{[1-z_B(c_B+x_B)]^2}{c_B+x_B}\ge0.
\]
定义a_B=ρ_B(2z_B−c_Bz_B²)，D_(j,B)=M_(B,j)ρ_Bz_B²。对任意竞争q'，乘非负w_Bρ_B求和、再对q'取min得
\[
 \boxed{t_r(b)\ge L_{p,z}(w):=a\cdot w-(r-1)\max_jD_j\cdot w.}
\tag{4}
\]
这是对全部背景q'的精确下界，p/z不必最优；有理p/z/w使它可独立精确核。它正是[现凸切线下证书](../定理/自由分数门槛的凸对偶与覆盖价格界--定理.md)在源程序所用a/D形式的展开，不授另一新静态定理。

saddle先用value得q，取z=逆分母，并构造二阶倒数加权Gram H_(j,a)=Σ_Bw_BM_(B,j)M_(B,a)z_B²；H不是普通对数势的一阶梯度。另用LP找查询p：Σp=1、p≥0、只在pay_a≥v−1e−6的活动query上，要求H_jp≤κ且q_j>1e−7处取等。这是给定查询下背景最优性的近似KKT及查询活动条件，不是精确全鞍点证明。

LP失败时实际代码取**全部活动query的均匀p**，不是注释所写的某个“best active pure query”。任何确切概率p都可用于(4)，因此回退不需要冒最优性；浮点p的符号/归一仍须重构核实。lower字段直接用a·w−(r−1)max Dw，value字段仍是SLSQP结果，两者不等同。

## optimize的LP实际归一与上界方向

从输入种子选根action/可实现target，使当前数值δ或D最低，固定该完整策略锥G=Γ与root收益向量u、root叶覆盖向量c。随后将w缩放使c·w=1，**这是所选实际终局福利W归一，不是OPT、最优比较元组覆盖或全部SPE最小福利归一**。

kind=floor时冻结根p/z。以h≥D_jw表示max Fenchel代价，LP目标为
\[
 (u-a)\cdot w+(n-1)h=u\cdot w-L_{p,z}(w),
\]
在精确数据下是δ的上界。kind=local另外冻结child分数背景q_c，置
\[
 E_{jB}=\frac{M_{Bj}}{1+M_{B,a}+(n-2)(Mq_c)_B},
 \quad U_c(w)=\max_jE_jw\ge t_{n-1}(\mathbf1_a).
\]
n2时child质量0、q占位无关。以T≥E_jw上界child值，目标
\[
 \boxed{(u-na)\cdot w+n(n-1)h+(n-1)T
 =u\cdot w+(n-1)U_c(w)-nL_{p,z}(w)}
\tag{5}
\]
在h/T紧时是D的上界。全部约束为w≥0、G w≥0、c·w=1、h/T≥0及上述各行；负**精确上界**加精确完整SPE证书会给相应接口反例。代码当前没有这项理性化认证，故负lp.fun/actual_debt仍仅候选。

最后一个w坐标是全目录通用客户，bounds[-3]=(0,0)正将它移除。对此绝对δ/D搜索可给直接理由：增加K通用单位客户，使任意n人终局每人增K/n、IC差不变；合法过去有n−r次通用覆盖，静态分母(n−r)+1+(r−1)=n，所以每层t也增K/n，δ与D增量均0。福利/归一和相对分数仍会变，不能将此性质迁移到任意其它客户删除。

每轮LP后重新用数值saddle评估root/child。trace的9字段是iteration、linear_upper、actual_debt、root_value、root_Fenchel_lower、next_value、root_utility、min_spe_margin、support。名actual_debt是**更新浮点oracle后的估计值**，不是已精确认证的真实数学D；min_spe_margin也只是float G@w最小值。严格负1e−8或相邻两轮debt差<1e−10会停止；两条都是探索停机规则，不是全局完备性或收敛证明。

成功记录14字段保status=NUMERIC_CANDIDATE_ONLY、n/k/kind、initial、root_counts/root_action、weights/trace、root_query/root_z/root_fractional_q、policy/rows。initial被map(int)，只对原整数种子的保真解释成立，不能对任意输入浮点种子声称无损；最终weights仍浮点，没有清分母或全有序IC独立核验。local的child值只在trace中，没有保存构成最后上界的完整child q证书，不能仅凭root向量和该标量形成独立exact反例。

LP失败只回status消息与已有trace。main要求seed JSON及--output，可选kind=floor/local、count默认10、rounds15；取bank优先，否则best或单记录，最多前count种子，None跳过；每处理一项覆盖写status=NUMERIC_EXPLORATION_ONLY/results，stdout另有seed序号/status/trace。没有完整种子尝试就不能从文件缺失推全部失败，保存results也不是通用证明。

## search_fractional_drift的随机输入和输出合同

默认n3/k5/seconds55/seed73679。初次生成每非空类型0…14权（以0.5保留）；有bank时80%从至多20条已接受记录复制，改1…4个随机坐标、幅度−9…9截0；始终去全类型，跳全零。成功trial才加计数并入bank，bank按relative_debt升序、可含重复；只捕RuntimeError累计errors，受墙钟时间控制，固定seed不保证不同速度得到同样试次数。

trial对各可支持根行动选使当前玩家利润最低的可实现target，用两次数值value算(2)。记录debt、relative_debt、root_value/next_value、action/terminal/utility、query_load/next_query_load，并附n/k/整数weights。relative_debt分母是Search给出的**所有SPE中的最小福利**，而所存terminal是该action下最小根收益叶，两者未必同一终局；不能把它自动解释为D/W_actual。

每轮覆盖输出status=NUMERIC_EXPLORATION_ONLY、seed/trials/errors/elapsed/best/bank；best按relative而非绝对debt，某trial的绝对debt<−1e−6才早停。它没有输出完整policy或有理Fenchel/child证书。整数DP可支持该根叶的SPE存在性，不等于浮点free值严格分离已被证明。原函数和随机过程完整保留，但本批未调用或产生一份新输出，未把可能同名的旧报告按文件名绑定成此次实际运行。

## 闭包、旧证据与接续方式

四源码在source-root按冻结相对路径保全，兄弟import可正确定位；运行依赖仅标准库、numpy、scipy.optimize及这四个原文件，无自动网络/优化器版本锁记录。两个main的CLI seed是调用者指定JSON，不从文件名猜实际旧argv。原113/34例/证书属于主probe内嵌literal的外部比较，不是它运行时读入的文件；两份旧小replay保已充分IC成功，当前0重演。

[原8qt完整claim与源指纹](../../tools/evidence/free-fractional-security-program-contracts-primary/README.md)区分三primary、Search必要related及四个已发表例/证书，不额外done。没有恢复缺少的历史stdout、运行时间或完整数值搜索报告，也没有制造新数学入口。

复用时可把p/z及child q改为确切概率有理数，重构原固定完整策略的全部真实分支，清整数客户并核G/原SPE，再以(4)—(5)证严格负差；若改root背景，Search的零根终局模型也需显式保过去，不能只因value接受b就说整个发现器已支持合法非零背景SPE。对一般问题仍应依据现已知FF反族限定目标；局部D、自由t聚合、真正整数v聚合和六人half分别有其未付义务。
