# 加权原子拥塞博弈：成果目录与研究入口

当前主目标 **WC-TARGET v1 仍开放**。团队已经保存奇数环的完整全状态下界证明及内部独立审查；全类存在性上界与下界之间仍有对数缺口。本页按数学成果组织阅读，不要求先通读协作工具、原始分支或全部证据文件。

精确对象采用 [MODEL](../../weighted_congestion_frontier/MODEL.md)：有限正权玩家、有限资源子集策略、非负系数次数至多 d 的多项式费用；玩家成本为所用资源费用之和，α-PNE 使用弱不等式。不同玩家数、资源支持、权密度、费用规则和证书量词不能省略。

## 第一次接手：按这个顺序读

1. [模型与全类目标](../../weighted_congestion_frontier/MODEL.md)：固定费用、真实单方偏离和普遍阈值 a_*(d)。
2. [奇数环线性重置总稿](odd_ring_linear.md)：先理解目前最强增长下界的资源机制、显式结果与剩余缺口。
3. [奇数环总证明](odd_ring/cohort_lower_bound_and_envelope.md)：需要调用下界或包络时，读全状态覆盖、系数闭环、有限有理实现及精确适用范围。
4. [逐资源与全状态独立审查](../../reviews/weighted_congestion/odd_ring_independent/REVIEW.md)、[精确包络独立审查](../../reviews/weighted_congestion/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md)：区分已覆盖义务、有限核验与未认证的新颖性。
5. [精确命题账本](../../weighted_congestion_frontier/CLAIMS.md)、[当前前沿](../../weighted_congestion_frontier/RESEARCH_STATE.md)、[失败机制](../../weighted_congestion_frontier/FAILED_ROUTES.md)：选取当前义务后，再从下表进入所需工具。

首屏摘要不能替代上述精确陈述。完整逐文件中文名称、用途、程序和冻结输出见 [研究文件目录](../../weighted_congestion_frontier/FILES.md)。

## 主结果与共同机制

令

\[
T_d=\max_{R>1}\frac{R(1+R)^d+1}{(1+R)^d+R^{d+1}},\qquad d\ge2.
\]

[同次数奇环总证明](odd_ring/cohort_lower_bound_and_envelope.md)给出：每个 α<T_d 都有有限正有理权、正有理系数、全部资源次数恰为 d 的游戏没有 α-PNE。因此 a_*(d)≥T_d∼d/ln d。已核对文献给出的全类存在上界仍为 d；外部同行评审和全球优先权均未认证。

[线性重置总稿](odd_ring_linear.md)给出显式 E_d=d/[(d+1)d^(1/(d+1))−d]，并在该因子本身排除均衡。线性重置与同次数实现属于同一奇环机制；R=1/t 使两份标量包络逐项相同。它们各自保留作者来源和实际审查，不能作为两个独立突破重复计算。

全状态覆盖 → 正系数闭环 → 有限实现 → 下界，是存在的证明链。**正局部测试的精确包络只限制这套证书**；一般多成员群组的实际游戏阈值仍未解决。每组只有一名群组玩家时的 min{2,T_d} 存在界另有严格输入限制。

## 按成果名称查找

| 成果包名称 | 正文入口与内容 | 作用与边界 |
| --- | --- | --- |
| 跨主题提取：正占用核交互秩与闭包 | [独立数学接口](../positive_kernels/README.md)及[完整证明](../positive_kernels/occupancy_rank_faces.md) | 源于局部成本正展开；低active秩排除高次数且大支持的正项，顶差分给锐坏项预算。只有零成本动作定向时直接返回MODEL；未给selector/全类存在桥 |
| 近线性倍率的真实改善环 | [循环窗口复制证明](cyclic_clone_improvement_cycles.md)、[冻结攻击](../../reviews/weighted_congestion/ordinal_potentials/cyclic_clone_improvement_cycles_review.md) | α<ρ_d、ρ_d/d→1时有真实改善闭环且全空为精确PNE；排除任意全局全边下降势，仍不排除选择动态/均衡存在 |
| 共同幂混合的坏全局最小点 | [同一四玩家构造](common_power_mixture_obstruction.md)、[独立攻击](../../reviews/weighted_congestion/ordinal_potentials/common_power_mixture_review.md) | 全部非零非负共同μ（含连续）均选坏最小点，d≥32、α<d/16；限保留原系数的目标族，有精确PNE |
| 统一低泄漏锚定时钟预算的普适次数障碍 | [一般证明](uniform_clock_budget_barrier.md)、[独立重构攻击](../../reviews/weighted_congestion/ordinal_potentials/uniform_clock_budget_barrier_review.md) | 任strict双轮输入及anchor，统一δ预算迫使D>2(α+1)ln(2α)、全部q≥D有αlnq/q<α/(α+1)<1；仅封闭预算调参路线，actual差/非均匀clock可重试 |
| 三次锚定时钟次数保持障碍 | [完整证书](anchored_clock_degree_barrier.md)、[独立强化审查](../../reviews/weighted_congestion/ordinal_potentials/anchored_clock_degree_barrier_review.md) | 指定4player p3基体，degree≤3有保边障碍；同稿第4节原全三元统一M在80次实际锁定但不满足(U)，独立双路证书，非最优/非增长族 |
| 循环窗口前沿商与不同步反例 | [一般表示与12玩家反例](class_front_phase_quotient.md)、[独立攻击](../../reviews/weighted_congestion/ordinal_potentials/class_fronts_review.md) | 扭转相位商/端点表精确；严格环可有稳定错位front，同权clock不新增front内出口；仍有内部改善 |
| 局部矩成本压缩与暂态择证 | [完整表示](template_certificates/selector_local_moments.md)、[独立攻击](../../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md) | D维全成本空间，≤D正resource+零费markers，dual≤D+1support；one-mover矩/门槛；第11节在完整proper锥同时植入近d真实唯一坏环与暂态dual，任意dual需正暂态质量，非每selector存在界 |
| 异权仿射全签名成本刚性 | [同一正文§9–10](template_certificates/selector_local_moments.md)、[独立重构](../../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)及正文所接精确code/run | WC-AFFINE-FULL-SIGNATURE-RIGIDITY-v1；非全等正权、同玩家/权/标签保全部成本，任意有限degree只能用全用户线性资源。有限成本锥极射线；等权反边界，有全0精确PNE，仅限制保真小支持归约 |
| 双轮环的锚定三元全状态锁定 | [编译证明](anchored_cycle_lock.md)、[独立重构攻击](../../reviews/weighted_congestion/ordinal_potentials/anchored_cycle_lock_review.md) | 保持玩家/权重/两动作，新增2L个单项式，使全部状态无αPNE；q=max(p,D)依δ、B/η及n，尚无目标量级次数控制 |
| 有限可动权类三角排序混合势 | [一般证明与推论](weight_bands/finite_weight_class_potentials.md)、[重构攻击](../../reviews/weighted_congestion/weight_types/finite_weight_classes_reconstruction_review.md) | A=Σ((d−1)/A)^j；有限k任意人数/权比，固定背景可吸收，窄簇损失R^d。d≥16且k≤ln d/lnln d给2d/ln d；k无界仍趋d |
| 两权类别双排序混合势 | [一般证明](weight_bands/two_weight_order_blend.md)、[独立攻击](../../reviews/weighted_congestion/weight_types/two_weight_order_blend_review.md) | 全局仅两种权值、任意人数/权比有(1+√(4d−3))/2-PNE，所有严格该因子改善终止。不能外推任意权类 |
| 择证平稳与循环支撑边界 | [完整证明](template_certificates/stationary_selector_obstruction.md)、[独立攻击](../../reviews/weighted_congestion/template_certificates/stationary_selector_obstruction_review.md) | 单位速度平稳dual损失无界；仿射循环有权重dual；recurrent支撑等价全模板αFIP，强于PNE存在 |
| 有向分叉强迫割均衡 | [一般证明](directed_fanout_forcing_cut.md)、[独立攻击](../../reviews/weighted_congestion/directed_fanout_forcing_cut_review.md) | 唯一源主资源＋私有双人侧资源＋UF下，α≥T_d有全反位PNE；不含共享多hub侧资源或UF失败 |
| 严格反例规范形与普遍阈值端点 | [一般证明](template_certificates/integer_counterexample_normal_form.md)、[独立攻击](../../reviews/weighted_congestion/template_certificates/integer_counterexample_normal_form_review.md) | 固定实α反例可限制整数权/单位单项式；新core允许删玩家，进一步人人≥2非空antichain空交策略，且所有α同一lift；a_*端点可行，仍无规模截止/匹配上界 |
| 有序权组的尾部负载冻结 | [一般证明与参数锐式](weight_bands/ordered_tail_freezing.md)、[独立攻击](../../reviews/weighted_congestion/weight_bands/ordered_tail_freezing_review.md) | 任意分组给A=max(b/a)(1+L/a)^d；可拼接密集同权群。两权级最佳A恰min{H,(1+K/H)^d}，固定次数仍可无界 |
| 阶跃DAG极值幅度的多项式全入状态 | [实际成本证明](step_dag/polynomial_extremal_all_in.md)、[独立冻结攻击](../../reviews/weighted_congestion/step_dag/polynomial_extremal_all_in_review.md) | 精确幅度(N)下全入状态有max{1+1/q,B_d(q)}保证，d≥16统一4√(d/ln d)；不要求低漏，但任意幅度尚未覆盖 |
| DAG端点低泄漏次数预算 | [检测充要条件](polynomial_curvature/dag_low_leakage_budget.md)、[冻结审查](../../reviews/weighted_congestion/polynomial_curvature/dag_low_leakage_budget_review.md) | z(z−1)ΣP_k z^(k−1)≤1恰可行；固定ε的辅助源门槛锐为√d量级。未控制高平台或真实全状态偏离 |
| 有限动作模板与全状态择证对偶 | [自足证明](template_certificates/finite_action_duality.md)、[独立重构](../../reviews/weighted_congestion/template_certificates/finite_action_duality_review.md) | 关联签名保持全部真实成本；任意资源数化为有限列，逐全状态selector有精确primal/dual替代。尚无全模板统一倍率 |
| 奇数环下界与精确证书包络 | [总证明](odd_ring/cohort_lower_bound_and_envelope.md)、[线性重置总稿](odd_ring_linear.md)、[可变次数接口](odd_ring_linear/README.md) | 增长下界主线；精确包络是证书界。一般群组实际阈值开放 |
| 文献两攻击公式的锐渐近 | [成果入口](source_envelope/README.md)、[锐渐近证明](source_envelope/sharp_asymptotic_envelope.md)、[统一机制上限](source_ceiling/README.md) | 优化指定源公式，不能作为全类存在上界；另一份推导仍按候选保存 |
| 完整对称两列拓扑还原 | [第三版完整证明](source_topology/symmetric_two_column_reduction.md) | 在所写倍率范围内将实际非存在还原至源公式；不含异权或非对称资源 |
| 三十二次源参数符号上界 | [参数消元与整数符号证明](source_degree32/symmetric_source_interval_certificate.md) | 覆盖指定源公式的全部合法实参数，为有限拓扑分离提供前提 |
| 四玩家十四资源非对称构造 | [固定实例与成本表](crossover/README.md)、[拓扑分离](crossover/separation.md)、[缩权极限族](crossover/limit_family.md) | 有限下界、次数外推失败与极限运输分别记录；固定玩家数不构成增长族 |
| 资源局部权密度与锐矩估计 | [一般证明](weight_density.md) | 稀疏权谱下的结构存在界；密度参数在全类没有统一控制 |
| 资源局部势拼接与两尺度路径 | [共同接口](power_bridge.md)、[路径障碍](power_bridge/path_obstruction.md)、[两权组分片势](power_bridge/affine_two_type.md) | 共享乘子可拼接，但固定次线性幂不能覆盖任意密集权谱；两精确权组有锐跨度界 |
| 局部窄权带与跨带障碍 | [份额、存在界及选择器证明](weight_bands/README.md) | 局部权比存在界；跨带混合差分、标准势线性损失只约束指定方法 |
| 潜在用户密度填充 | [投影与提升证明](density_padding/optional_user_density_padding.md) | 已占权重区间的最小人数可任意填充，有限倍率均衡逐一保持；不否定最大稀疏密度上界 |
| 高次费用与资源最小份额 | [份额势与必要条件](high_degree_share.md)、[独立攻击](../../reviews/weighted_congestion/high_degree_share_review.md) | 每资源最低正次数和最小潜在权份额给近精确势；固定正权向量的高次保证对所有有限拓扑一致趋1；非全类界 |
| 资源用户支持与双人资源界 | [资源支持存在界](resource_support.md)、[双人资源互补网络](odd_ring_linear/pair_obstruction/PAIR_OBSTRUCTION.md) | 限制有界支持小构件的放大；没有全类常数或多项式时间结论 |
| 三玩家整数二次实例 | [完整成本表与最优倍率](quadratic_triad/three_player_integer_obstruction.md) | 有限精确证明；所引独立审查原件未找到，不补造审查通过 |
| 文献源公式二次包络 | [有理参数上界](quadratic_source/source_family_envelope.md) | 指定源公式的有限次数边界，与三玩家实例分开比较 |
| 阶跃模拟曲率与三负载凸包络 | [前缀模拟障碍](polynomial_curvature/three_load_curvature_bound.md)、[精确三点最优工具](polynomial_curvature/three_point_polynomial_envelope.md) | 排除保持源平台形状的直接模拟；改变权重、拓扑或状态覆盖须另论 |
| 异权端点强制还原 | [单一轻权还原证明](heterogeneous_endpoint/endpoint_reduction.md) | 只作用于所写两类端点强制不等式，不是全部异权拓扑等价 |
| 互补多列拓扑的二倍逃逸 | [存在与三列锐性证明](multicolumn/complement_column_escape.md) | 排除指定共同轻权、多列关联方式的放大；不排除全部多列构造 |
| 任意玩家乘子与依游戏可分序势障碍 | [现行完整重构](separable_ordinal_obstruction.md)、[冻结证明独立攻击](../../reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md) | 线性障碍只针对全部改善边下降的可分证书；所构游戏有全空精确均衡，不排除全局选态 |
| 有向无环阶跃依赖辅助模型 | [路径计数与精确阈值](step_dag/step_dependency_threshold.md) | 费用为阶跃函数，属于辅助模型；迁入当前多项式类需要新证明 |

这些包中的 theorem、obstruction、counterexample、review 和 evidence 是不同类型的资产。同包材料可以互相指向，但来源相同、通过有限计算或位于 current 都不自动提升数学状态。

依游戏可分最小点目标的范围另已精确澄清：`WC-GAME-SPECIFIC-MINIMIZER-EQUIVALENCE-v1` 在[序势现行稿第四节](separable_ordinal_obstruction.md)证明其与该游戏的α-PNE存在等价；[范围审查](../../reviews/weighted_congestion/ordinal_potentials/minimizer_scope_review.md)防止将全改善下降障碍外推。该等价把任意目标状态作为输入，不给新存在界。

## 从当前义务继续

- **全类 O(d/ln d) 存在性。** 可用[全状态择证对偶](template_certificates/finite_action_duality.md)寻找依完整selector的概率证书；必须对所有权重、动作数和selector给统一估计。[真实近d循环](cyclic_clone_improvement_cycles.md)已排除只在回返状态找dual/让全部改善终止的一般路线；仍可依完整selector在暂态分配质量或选择部分改善。结构势路线先读权密度、资源拼接和窄权带三包，核对稠密尺度及共享乘子的未解接口；[边际势和序势候选](../../questions/weighted_congestion/README.md)只按实际审查等级使用。
- **跨权组与阶跃模拟。** [双排序混合势](weight_bands/two_weight_order_blend.md)已越过两权尾部参数无界，给统一平方根次数界；[三角排序](weight_bands/finite_weight_class_potentials.md)已覆盖任意有限k，并精确吸收固定玩家背景；剩余缺口是无界可动类别或无法用少量窄簇覆盖的权谱。 [冻结界](weight_bands/ordered_tail_freezing.md)的逐资源β缩放不可省略；不能再希望仅优化潜在尾部参数得到统一倍率。[DAG泄漏预算](polynomial_curvature/dag_low_leakage_budget.md)只限制指定低高端点系统，[极值幅度全入界](step_dag/polynomial_extremal_all_in.md)已直接容纳任意过冲和泄漏，但只在幅度(N)下；实际占用与任意幅度仍须另证。
- **超越现有奇环下界。** 先读奇环精确包络，再看非对称缩权族、曲率和多列逃逸；需要改变全状态覆盖机制，不能把证书失效当实际均衡存在。
- **一般群组奇环的实际阈值。** 从总证明的单成员子类与[单冲突图独立证明](../../reviews/weighted_congestion/odd_ring_parameters/SINGLETON_NOTE.md)起步，明确多成员使哪一步状态表示失效。

已有路线是搜索种子，不限制可尝试的方法。候选、反例和可复用工具可以按真实层级保存；重要状态提升仍须闭合实际证明义务并接受独立攻击。

## 程序、证据与时点状态

程序统一从仓库根运行 `python3 tests/audits/weighted_congestion/replay.py --list` 选择具体核验，再把代码路径传给同一程序。它在临时目录恢复原相对布局，避免覆盖冻结证据。Decimal 诊断、浮点发现、有限有理枚举和整数符号证书在文件目录中分别命名。

部分详细稿保留撰写时的 pending 标签或历史相对路径。现行逐命题审查查[主题账本](../../weighted_congestion_frontier/CLAIMS.md)及[五轴表](../../review_status.json)，实际审查范围查对应审查正文；没有审查记录的结论不能靠入口摘要升级。不可变原件及恢复路径见 [INTEGRATION](../../weighted_congestion_frontier/INTEGRATION.json)。

**负向接续接口。** 先读[真实双轮环](cyclic_clone_improvement_cycles.md)，限制为原两个动作，再读[锚定锁定](anchored_cycle_lock.md)及其独立审查/两类精确证据。全状态覆盖已闭合；[统一预算普适障碍](uniform_clock_budget_barrier.md)已证明该预算对全部输入均有α ln q/q<1，不能只继续调输入环。剩余须让实际时钟差、非统一费用/次数或其他机制的编译后q取得无界α ln q/q；此障碍不是任意时钟或全类方法障碍。

**规范域接续。** [空交反链核心](template_certificates/integer_counterexample_normal_form.md)第7节将包含支配、固定者及必选背景从反例剥去；先读其新ID与单向lift，再读[独立攻击](../../reviews/weighted_congestion/template_certificates/antichain_core_normal_form_review.md)和两份代码/证据。此步骤不限制真正可动类别数，不能替代无界权谱的存在或非存在桥。

## 共享侧资源与实际时钟的精确接口

- [同权共享侧资源截断势及直接源预算](shared_side_truncated_potential.md)：`WC-SHARED-SIDE-TRUNCATED-ROSENTHAL-v1`在unique-light/source、最坏负载UF下给A_d≤2d/ln d；`WC-SHARED-SIDE-BUDGET-POTENTIAL-v1`独立给d≥0、α≥1的AS+B判据。固定light边际→source重置误差→主预算→全anti局部势最小点是证明链；跨source、多light或异权hub未被覆盖。先读精确对象，再看[冻结攻击](../../reviews/weighted_congestion/shared_side_truncated_potential_review.md)及正文中的代码/证据合同。
- [锚定双轮时钟真实有向差分](anchored_clock_actual_margins.md)：`WC-ANCHORED-ACTUAL-MARGIN-INTERFACE-v1`给合法g、非法g+ΣΔ、n+L充分LP、保环必要ΣS预算及逐次数κ稳定条件。不能把必要预算当充分条件或firstopp失败当PNE。固定四玩家43次全状态证书与uniform91选值均精确复验；没有最优性或增长族结论。第九节另证固定结构、纯三次和空交反链输入的真实余量依赖不可消去：每个cap都可由private费用padding阻止指定保环clock，仍不排健康余量增长族。[先重构与冻结攻击](../../reviews/weighted_congestion/ordinal_potentials/actual_clock_margins_review.md)和三路代码/显式输入/证据均从正文进入。

全类题保持OPEN。下一步应控制无界类的全局选态、跨source预算或实际clock在增长输入族上的α ln q/q；只调已被封闭的uniform公式不能完成负向目标。

## 潜在与实际共占高度的接续

[原三角势正文第11–13节](weight_bands/finite_weight_class_potentials.md)用两个新ID登记共占高度扩展：`WC-WEIGHT-INTERACTION-HEIGHT-POTENTIAL-v1`允许全局任意多权值，只需潜在可动玩家降权图height=k；`WC-REALIZED-INTERACTION-CHAIN-CYCLE-v1`给严格α闭词的实际共占链必要条件α<A_(d,k)。原有限权类、固定背景、窄簇取整三个ID不变。共同层秩→身份子集排序边际→全状态势最小/闭词端点望远镜是证明链；同层异权不能按全局代表权计数。[独立重构与攻击](../../reviews/weighted_congestion/weight_types/interaction_height_review.md)、两路代码和证据由正文进入。

目前需控制的是无界交互高度的选态，而不仅是全局权类数。长链不是无PNE充分条件；低单点高度不是PNE必要。动态重排会换势，尚无累计图高度控制、SCC统一出口或全类瞬态dual。
