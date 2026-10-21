# 加权原子拥塞博弈：成果目录与研究入口

本次全类`Cd/ln d`存在命题已有**严格否定证明**。`WC-LINEAR-DEGREE-ALLSTATE-NONEXISTENCE-v1`：每整数d≥2^20都有有限正有理权、正有理纯d次资源费用、每人两个非空不交动作的MODEL游戏；每个纯状态有合法偏离C_i(s)>(d/10)C_i(t_i,s_−i)。由`WC-MATCHING-LOG-UPPER-NEGATIVE-v1`的量词选择，原题绝对C,d0不存在。本文入口、精确账本和配套审查均与该范围一致；外部评审/新颖性未认证。

采用[MODEL](../../weighted_congestion_frontier/MODEL.md)：有限正权玩家、有限资源子集策略、非负系数次数至多d的费用；玩家成本为资源费用之和，偏离后按真实负载计费。允许空策略和零费用不妨碍反例位于正费用两动作子类。

## 第一次接手：按这个顺序读

1. [MODEL](../../weighted_congestion_frontier/MODEL.md)和[唯一验收标准](../../weighted_congestion_frontier/ACCEPTANCE.md)，明确全状态与全部量词。
2. [线性次数的全状态无均衡族与匹配对数上界的严格否定](linear_degree_allstate_lower_bound.md)：第2—3节完整基体/健康预算，第4—5节全部错位前沿，第6节非法状态修复，第7节同次数，第8节否定量词。
3. [分阶段独立重构和最终稿审查](../../reviews/weighted_congestion/ordinal_potentials/linear_degree_allstate_review.md)与[从原题开始的独立攻击](../../reviews/weighted_congestion/ordinal_potentials/linear_degree_allstate_clean_attack.md)：均绑定冻结hash，核对修复及攻击范围。
4. 正文第10节给原有精确审计；[独立审查补节](../../reviews/weighted_congestion/ordinal_potentials/linear_degree_allstate_review.md#补充复核整数次数预算与完整多类拼装)另给免对数的整数预算证明、[完整多类拼装审计](../../../tests/audits/weighted_congestion/cyclic_clone/independent_multiclass_assembly.py)与[冻结结果](../../../evidence/runs/weighted_congestion/cyclic_clone/linear_degree_multiclass_assembly.json)。有限计算不是一般证明。
5. [精确Claim](../../weighted_congestion_frontier/CLAIMS.md)、[五轴状态](../../review_status.json)、[当前义务](../../weighted_congestion_frontier/RESEARCH_STATE.md)与[目录](../../weighted_congestion_frontier/FILES.md)，再按下表选择结构工具。

## 面向评审读者的连续主稿

[完整英文PDF](linear_threshold_article.pdf)与[LaTeX源稿](linear_threshold_article.tex)将已审线性下界重构为自足文章：主定理及模型 → 同权类前沿编译 → 完整循环窗口与预算 → 全部错位前沿 → 同次数拼装 → 对数保证否定及Theta(d)推论。没有把旧方法障碍或小反例并入主线凑篇幅。稿件[审读与产物核查](../../reviews/weighted_congestion/linear_threshold_article_review.md)绑定源/PDF hash，说明已处理问题、引用边界及实际十页视觉检查；[BibTeX](linear_threshold_references.bib)与源稿同目录。原规范数学正文和Claim身份不变，成稿不等于外审、优先权或录用认证。

## 主结果与依赖

健康邻接反向短窗口与正向全返回给α=p/10双扫环、B*/η=exp(O(log²p))；单个环不是非存在。任意类前沿相位差若离两个短区间，heavy端点给出口；否则短差累计，末类返回端点按parity选择方向，有限缺陷低于余量，从而全部product-front有统一η0=H/4出口。同类010/101锚定时钟再以最早异位单人修复覆盖其余状态；p≥2^20时实际新增degree直接取p，得到全状态无(p/10)-PNE。完整正文从资源定义重建每一环节，不导入外部存在定理。

WC-TARGET v1的原长期身份保留。新下界a_*(d)≥d/10与[单列Paper Fact一般上界d](../../weighted_congestion_frontier/CLAIMS.md#wc-lit-upper-d-v1--paper-fact)合用确定增长阶Θ(d)；精确常数与有限d最优阈值仍未知。已核文献d-PNE证明未在本包重新认证，且不是否定证明前提。

旧[奇环同次数总证明](odd_ring/cohort_lower_bound_and_envelope.md)仍给每α<T_d的有理反例，T_d∼d/ln d；[线性重置实现](odd_ring_linear.md)属于同一奇环机制。其第10节另以稳定区间/双取向证明一般同权cohort、同费副本奇环的实际阈值恰T_d，无UF假设。这是准确的子类阈值，无法排除新循环窗口结构。

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
| 奇环择证的无界跨玩家补偿 | [原矩接口正文§12–13](template_certificates/selector_local_moments.md)、[独立重构攻击](../../reviews/weighted_congestion/template_certificates/selector_mover_support_review.md) | 完整/proper锥中dual可行，但每个α<2^d须覆盖全部n名移动者及两方向，最小state支撑2n；min-index在端点骤降为2。只排固定人数截断，非无均衡 |
| 异权仿射全签名成本刚性 | [同一正文§9–10](template_certificates/selector_local_moments.md)、[独立重构](../../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)及正文所接精确code/run | WC-AFFINE-FULL-SIGNATURE-RIGIDITY-v1；非全等正权、同玩家/权/标签保全部成本，任意有限degree只能用全用户线性资源。有限成本锥极射线；等权反边界，有全0精确PNE，仅限制保真小支持归约 |
| 双轮环的锚定三元全状态锁定 | [编译证明](anchored_cycle_lock.md)、[独立重构攻击](../../reviews/weighted_congestion/ordinal_potentials/anchored_cycle_lock_review.md) | 保持玩家/权重/两动作，新增2L个单项式，使全部状态无αPNE；q=max(p,D)依δ、B/η及n，原合同依实例；新专用增长族另见本页主结果 |
| 有限可动权类三角排序混合势 | [一般证明与推论](weight_bands/finite_weight_class_potentials.md)、[重构攻击](../../reviews/weighted_congestion/weight_types/finite_weight_classes_reconstruction_review.md) | A=Σ((d−1)/A)^j；有限k任意人数/权比，固定背景可吸收，窄簇损失R^d。d≥16且k≤ln d/lnln d给2d/ln d；k无界仍趋d |
| 两权类别双排序混合势 | [一般证明](weight_bands/two_weight_order_blend.md)、[独立攻击](../../reviews/weighted_congestion/weight_types/two_weight_order_blend_review.md) | 全局仅两种权值、任意人数/权比有(1+√(4d−3))/2-PNE，所有严格该因子改善终止。不能外推任意权类 |
| 择证平稳与循环支撑边界 | [完整证明](template_certificates/stationary_selector_obstruction.md)、[独立攻击](../../reviews/weighted_congestion/template_certificates/stationary_selector_obstruction_review.md) | 单位速度平稳dual损失无界；仿射循环有权重dual；recurrent支撑等价全模板αFIP，强于PNE存在 |
| 有向分叉强迫割均衡 | [一般证明](directed_fanout_forcing_cut.md)、[独立攻击](../../reviews/weighted_congestion/directed_fanout_forcing_cut_review.md) | 唯一源主资源＋私有双人侧资源＋UF下，α≥T_d有全反位PNE；不含共享多hub侧资源或UF失败 |
| 严格反例规范形与普遍阈值端点 | [一般证明](template_certificates/integer_counterexample_normal_form.md)、[独立攻击](../../reviews/weighted_congestion/template_certificates/integer_counterexample_normal_form_review.md) | 固定实α反例可限制整数权/单位单项式；新core允许删玩家，进一步人人≥2非空antichain空交策略，且所有α同一lift；a_*端点可行，仍无规模截止/匹配上界 |
| 有序权组的尾部负载冻结 | [一般证明与参数锐式](weight_bands/ordered_tail_freezing.md)、[独立攻击](../../reviews/weighted_congestion/weight_bands/ordered_tail_freezing_review.md) | 任意分组给A=max(b/a)(1+L/a)^d；可拼接密集同权群。两权级最佳A恰min{H,(1+K/H)^d}，固定次数仍可无界 |
| 阶跃DAG极值幅度的多项式全入状态 | [实际成本证明](step_dag/polynomial_extremal_all_in.md)、[独立冻结攻击](../../reviews/weighted_congestion/step_dag/polynomial_extremal_all_in_review.md) | 精确幅度(N)下全入状态有max{1+1/q,B_d(q)}保证，d≥16统一4√(d/ln d)；不要求低漏，但任意幅度尚未覆盖 |
| DAG端点低泄漏次数预算 | [检测充要条件](polynomial_curvature/dag_low_leakage_budget.md)、[冻结审查](../../reviews/weighted_congestion/polynomial_curvature/dag_low_leakage_budget_review.md) | z(z−1)ΣP_k z^(k−1)≤1恰可行；固定ε的辅助源门槛锐为√d量级。未控制高平台或真实全状态偏离 |
| 有限动作模板与全状态择证对偶 | [自足证明](template_certificates/finite_action_duality.md)、[独立重构](../../reviews/weighted_congestion/template_certificates/finite_action_duality_review.md) | 关联签名保持全部真实成本；任意资源数化为有限列，逐全状态selector有精确primal/dual替代。尚无全模板统一倍率 |
| 奇数环下界与精确证书包络 | [总证明](odd_ring/cohort_lower_bound_and_envelope.md)、[线性重置总稿](odd_ring_linear.md)、[可变次数接口](odd_ring_linear/README.md) | 增长下界及正测试包络；第10节以全新实际选态证明闭合一般cohort拓扑阈值恰T_d，无UF假设。独立[重构攻击](../../reviews/weighted_congestion/odd_ring_parameters/general_cohort_actual_upper_review.md)和两路代码/冻结记录见正文10.9；仅该拓扑，不是全类阈值 |
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

## 补充结构接口与准确边界

| 对象 | 读取入口 | 范围与当前关系 |
| --- | --- | --- |
| 全部类前沿的次数可控条件编译 | [条件定理](class_front_phase_quotient.md#条件编译接口全部同权类前沿出口到全状态非存在)、[独立审查](../../reviews/weighted_congestion/ordinal_potentials/class_front_allstate_compiler_review.md) | 以前沿全覆盖及B/η为前提；新主结果提供有效增长输入，闭合该先前缺口。旧strict-sweep稳定前沿反例仍正确。 |
| 共享侧资源、实际clock预算与跨源反馈 | [完整接口](shared_side_truncated_potential.md)、[实际clock差分](anchored_clock_actual_margins.md) | 同权/异权hub、UFτ、局部R/K及ατ≥Kd等各有精确版本；四玩家固定次数证书仍仅有限实例，不改为增长族。 |
| 固定hub的轻响应 | [显式阈值与单遍删除](fixed_hub_light_threshold_response.md) | 存在/FIP为Milchtaich1996已知特例；hub真实偏离冻结lights，重选后成本不能直接lift。 |
| 共占高度与实际闭词链 | [三角势第11—13节](weight_bands/finite_weight_class_potentials.md)、[独立审查](../../reviews/weighted_congestion/weight_types/interaction_height_review.md) | 固定降权共占图height给存在界；长链不是无PNE充分条件，动态换秩也不自动拼势。 |
| 完整成本近似小支持障碍 | [矩接口](template_certificates/selector_local_moments.md)、[独立审查](../../reviews/weighted_congestion/template_certificates/approximate_support_review.md) | 允许改权仍有乘性失真；辅助玩家/只保均衡lift是不同合同。 |
| 潜在使用森林及挂树私人成本归约 | [自足证明](incidence_forest_private_reduction.md) | 森林exactPNE、单核心挂树保degree与全部α固定lift；单环已有72/71边界。 |
| 依游戏可分最小点的量词 | [第四节](separable_ordinal_obstruction.md)、[范围审查](../../reviews/weighted_congestion/ordinal_potentials/minimizer_scope_review.md) | 与该游戏的PNE存在等价，不从全改善边下降障碍推任意选态不可能。 |

## 后续可独立接续的义务

- 核查/简化新线性下界的一般证明，优化1/10与次数起点；任何新fatal objection仍须立即登记并阻止升级。
- 刻画a_*(d)的精确首项常数与有限d值；增长阶Θ(d)不等于最优常数或某有限游戏达到sup。
- 文献优先权、外部同行评审及发表另行进行；不把内部审查当外部认证。
- 结构子类存在界、反例规范形和表示接口继续各按原范围复用；全类o(d)存在命题已被线性全状态族否定，不能继续当未解目标。

## 程序、证据与时点状态

本次五份审计的完整运行入口见主证明第10节，标准库整数/Fraction、无随机seed、冻结输出防覆盖。其他旧程序可从仓库根用`python3 tests/audits/weighted_congestion/replay.py --list`定位；其旧冻结证据不原位改写。

[FILES](../../weighted_congestion_frontier/FILES.md)与[CATALOG](../../CATALOG.md)记录具体用途；[assets.json](../../assets.json)给文件合同，[review_status.json](../../review_status.json)分别记录证明、内审、外审和实现。旧正文或审查中的OPEN/pending仅是该冻结时点状态，不改变现行新Claim；无审查记录的其他候选不因主问题完成而升级。不可变原件与来源恢复见[INTEGRATION](../../weighted_congestion_frontier/INTEGRATION.json)。

第三路[全相位独立攻击](../../reviews/weighted_congestion/ordinal_potentials/linear_degree_full_phase_attack.md)另记录完整小参数phase对与类位串审计；其实际接收种子顺序、最终hash、独立代码及冻结结果从该审查进入。

[既有Pro简报](../../weighted_congestion_frontier/PRO_BRIEF.md)、[精确攻题任务](../../weighted_congestion_frontier/prompts/PRO_ATTACK.md)及[冻结来源映射](../../weighted_congestion_frontier/PRO_BRIEF_SOURCES.json)保留解题前2c49228及其前序快照的模型与工具整理；其中旧OPEN判断不再代表现行状态。独立复查当前结果应先读本页新自足证明及审查，冻结旧来源不原位修改。

## 结构用于决策：本轮恢复入口

[成果恢复与用途](decision_methods/source_recovery.md)固定可读地基、既有英文稿和无法从当前 main 恢复的来源。后续方法以原游戏的真实偏离、稳定性与社会成本分别核验；本轮按用户指定接续，不改变其他模型的主攻或原有结果身份。
