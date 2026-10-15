# 当前研究前沿

## 当前主攻：加权原子拥塞

当前协作集中判定全类 O(d/ln d) 近似纯均衡存在命题，完成须给一般肯定证明或严格否定证明；常数和次数起点不能依赖博弈规模或权重。精确量词与唯一门槛见[本题验收](research/weighted_congestion_frontier/ACCEPTANCE.md)。局部引理、方法障碍和有限实例仍可入库，不能替代该完成标准。

WC-TARGET v1 保持 OPEN。所有已发现远端研究分支的独有成果已经进入共同分类；精确去处见 [FILES.md](research/weighted_congestion_frontier/FILES.md)。旧公屏和旧会话不作为状态来源。

最重要的已保存进展是奇环 hub/cohort 的有限全状态非存在构造：
T_d=max_(R>1)[R(1+R)^d+1]/[(1+R)^d+R^(d+1)]∼d/ln d，因而 a_*(d)≥T_d。
R1 的线性重置实现与 R3 的同次数实现归属于共同机制，保留原作者和各自独立审查。它们不是两项互不相关的突破。[现行数学入口](research/current/weighted_congestion/README.md)说明精确范围。

全类上界仍是已核对文献 d。关键未解义务是全类 O(d/ln d) 存在性，或绕开当前全部 light-forcing 测试的更强全状态非存在机制。一般 cohort 奇环的实际均衡阈值也不能从证书失效推出。

固定权重与动作数的[全状态线性证书接口](research/current/weighted_congestion/template_certificates/finite_action_duality.md)已独立重构：关联签名消去任意资源数，逐selector给非负系数/primal与概率dual替代。[严格反例整数规范形与闭端点](research/current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)又消去固定倍率反例的实参数：规范形仍无规模界，普遍阈值端点可行。尚无统一C,d0；[最小点选择等价](research/current/weighted_congestion/separable_ordinal_obstruction.md)也只澄清旧势障碍的量词。 [空交反链核心](research/current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md#7-去包含支配与必选背景的空交反链核心)进一步把反例限制为人人至少两非空、无包含、空交策略，并给所有α≥1同时有效的单向lift；允许删玩家，不给规模界。

## 工具、边界与待审项

- 已保存：[高次份额势](research/current/weighted_congestion/high_degree_share.md)及两套独立精确审计，提供实例相关近精确界、纯高次必要小份额和固定正权向量的一致高次极限。
- 已保存：文献源包络锐渐近与完整对称两列拓扑限制、稀疏权密度势及拼接、局部窄权带势、密度 padding、有限非对称拓扑分离、三负载曲率、异权端点还原、多列逃逸与辅助 step-DAG。
- 已独立重构并攻击：[任意玩家乘子与依游戏资源可分序势障碍](research/current/weighted_congestion/separable_ordinal_obstruction.md)，精确范围只含所写边际夹逼与全部改善边下降证书，所构游戏仍有精确均衡。
- 待审：普适复制桥的其他推论、保守多项式端点扩展及完整两列轨道稿。它们有正文或精确计算，不能因入 main 就称为已审定理。
- 已知来源欠账：三玩家稿所引 resource_cone 独立审查、非分离 frontier 的原证明/程序未在任何已观察分支中找到。保留可读材料，按真实缺失范围标注。
- 世界新颖性、外部同行评审均未认证；本轮整理没有将其补成事实。

[有序权组冻结](research/current/weighted_congestion/weight_bands/ordered_tail_freezing.md)新增依分组的结构存在界与两权级精确参数限制：即使最佳分组，潜在尾部参数也不能全类统一。[DAG端点泄漏预算](research/current/weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md)给任意DAG指定检测系统的可行充要条件；固定泄漏的辅助源门槛仅有平方根量级。下一步须超出这些潜在参数和检测合同；主目标不变。

新增[两权类别双排序混合势](research/current/weighted_congestion/weight_bands/two_weight_order_blend.md)：全局仅两权时，任意cohort人数/权比均有平方根次数存在界；完整一般证明和独立攻击已核对。有限k扩展见下述三角势；真正缺口为无界可动类别，不把两权范围升级为全类。

[循环窗口复制的真实近d改善环](research/current/weighted_congestion/cyclic_clone_improvement_cycles.md)将旧可分势障碍提升为任意全局全边下降势障碍，仍有全空精确PNE。[共同幂混合最小点障碍](research/current/weighted_congestion/common_power_mixture_obstruction.md)另直接排除指定连续目标族的全部最小点。全类存在性仍OPEN；环本身不能当无均衡；[锚定三元全状态锁定](research/current/weighted_congestion/anchored_cycle_lock.md)已将严格双轮环编译成无α-PNE，但新增次数依实例。[统一低泄漏锚定时钟预算的普适次数障碍](research/current/weighted_congestion/uniform_clock_budget_barrier.md)已证明满足现行统一预算的全部输入均有α ln q/q<α/(α+1)<1；负向前沿须改用实际时钟差、非统一预算或其他全状态机制；[三次锚定架构证书](research/current/weighted_congestion/anchored_clock_degree_barrier.md)已排除在指定基体上保持原degree的方案，未排常数倍degree。正向仍需选步或超出这些目标族的选态。

[有限可动权类的三角排序势](research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)已给A_(d,k)隐式界，固定k为d^(1−1/k)，任意固定背景精确吸收、k个R窄簇损失R^d。d≥16且k≤ln d/lnln d的明确子类达到2d/ln d；无界可动类别时A趋d，唯一全类题仍OPEN。真正前沿已收缩为无界可动权类的选态桥或全状态增长反例，不再把固定背景或仅两类稠密cohort当未解接口。

## 其他长期资产

E1 提取的[正占用核](research/current/positive_kernels/README.md)新增独立结构：任意阶数的暴露面、任意有限次数统一的锐坏项质量预算，以及加入unanimity方向的准确闭包。源为boss4正Möbius展开，三PK身份不修改原WC Claim。一次零质量边界错误已由实际审计发现并修复；低背景检测不能提供无界次数稳定预算。下一桥是一般签名的符号差分控制及selector可行性；当前没有均衡存在增量。

设施选址保留共同目录双设施尖锐界、复杂度边界、任意设施数因子 2 存在性与有限构造；一般位多项式构造继续开放。顺序客户吸引保留真实完整 SPE、结构类福利界和失败桥，一般半覆盖继续开放。它们分别从根 README 的模型表进入，无需当前拥塞研究者先通读。

## 持续施工与保存

按 [GROWTH](research/GROWTH.md) 先固定 claim 再落正确目录；完成可复用阶段内容和相应核验后立即 checkpoint 到 main，不创建研究分支。候选可以按候选保存。公屏可自由研讨有启发的未完成 idea、卡点和合作问题，不要求先成稿或审查；致命反驳及时核查登记。普通排错和逐轮日志无需强制汇报或入库。

根 README 保持稳定地图。本文件只呈现现在，过程提交留在 Git 历史。具体文件状态、来源和冻结证据分开登记，见 [仓库工作程序](research/REPOSITORY_GUIDE.md) 与 [逐文件索引](research/weighted_congestion_frontier/FILES.md)。

研究读取现从[按问题分流的总目录](research/README.md)进入，各专题按证明链组织；[中文资产总目录](research/CATALOG.md)登记具体文件名、作用和状态依据。现行数学审查按模型归位，投稿旧判断从历史来源追溯，旧路线用固定 Git 版本恢复。命名与导航整理没有新增或升级数学结论。

已审新边界：[择证循环支撑](research/current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)中单位速度平稳dual无界损失，仿射按移动者权重有显式dual，仅支撑recurrent states等价全模板αFIP；一般存在路线不应无证增加此要求。[有向分叉强迫割均衡](research/current/weighted_congestion/directed_fanout_forcing_cut.md)在UF下对异权light/多出侧/自环给α≥T_d全反位PNE。真正未解是全类统一dual估计或新全状态primal；可判别的下界逃逸点为UF失败、侧资源多hub共享及动作副本非对称，当前无闭合机制。

[阶跃DAG极值幅度的多项式全入状态](research/current/weighted_congestion/step_dag/polynomial_extremal_all_in.md)已直接控制真实多项式成本：不要求低漏/平台保真，幅度(N)下d≥16给4√(d/ln d)状态。全类题仍OPEN；当前最具体新缺口是任意卫星幅度如何归约或怎样选择其他稳定light集合，不能只改变已锚定费用形状。

[有限次局部矩与全成本压缩](research/current/weighted_congestion/template_certificates/selector_local_moments.md)将签名接口细化为D维完整成本空间、≤D正单项式资源保真表示和≤D+1支撑dual；完整proper锥另可同时实现近d真实唯一坏环和完全暂态dual，任何dual暂态质量必须为正；这是已知两机制的同时化，不给任意selector方法。奇环缺陷择证另迫使任意α<2^d的dual同时覆盖全部移动者，两方向均有正质量，最小状态支撑恰2n；等权可行例已排除固定人数的局部补偿截断。真正未解仍是每个selector的moment hull与resource polar是否在统一倍率相交。[循环窗口前沿商与不同步反例](research/current/weighted_congestion/class_front_phase_quotient.md)提供相对phase表示，但类内clock不能自动给错位front出口，故负向仍需新同步/离front覆盖机制。两包均未完成唯一全类题。

[共享侧资源截断势](research/current/weighted_congestion/shared_side_truncated_potential.md)把同权hub、unique-light/source、最坏负载UF子类扩到任意共享hub子集，给A_d≤2d/ln d；独立AS+B判据覆盖部分非UF实例。[实际时钟差分与预算](research/current/weighted_congestion/anchored_clock_actual_margins.md)给非统一clock的O(n²)充分LP、必要总预算和κ稳定条件，固定四玩家43次证书优于原uniform91选值但不称最优。原全三元、统一M架构另有80次全状态证书却不满足(U)，故(U)对原架构也非必要；这仍不是增长族。实际接口另证：固定人数/权谱/α/纯三次亦可用private成本压低环余量，阻止任意预给degree cap的保环三元clock；健康余量增长输入仍未排除。真正缺口仍是无界可动权类的全类选态、跨source/预算外反馈或次数效率可增长的全状态族。

[共占图高度与实际改善环必要链](research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)把三角势参数从全局权类数放宽为同一降权共占图的路径高度；全局权种数可无界。实际严格改善闭词也必须跨越相应高度门槛，各弧可来自不同端点。仍无全类高度控制；动态换秩改变势，缺少高链SCC出口或瞬态dual。

[局部成本接口的刚性边界](research/current/weighted_congestion/template_certificates/selector_local_moments.md)把“资源数量可压缩”与“资源用户支持可缩小”分开：非全等权全用户仿射成本要求全用户线性资源，即使允许任意有限degree。只限制完整成本保真归约；全类相交义务和唯一题仍未闭合。

跨source的同权hub侧反馈在UFmulti下已由真实Rosenthal势闭合到1+√d；不再把“共享多个source的light”本身当成逃逸机制。当前负向需UF失败、异权hub或其他架构。正向也不能仅靠固定有限失真的小资源支持全成本归约：degree1原表在允许改权后仍有定量失真障碍。类内有序三元clock通用编译器另被strict sweep中的严格精确PNE前沿阻止；所写任意次数/幅度均无效，但更高倍率专用输入类、跨类或其他arity不在排除范围。全类未解仍是无界可动权类的选态或次数效率可增长全状态族。

[跨源共享侧资源的强迫与目标倍率分离](research/current/weighted_congestion/shared_side_truncated_potential.md)第九节（`WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v1`）给出独立新身份：同权hub、唯一main source及二元同费副本下，UF强迫τ>1与目标α只需(τ−1)(α−1)≥d，无大小排序。d≥16取τ=1+ln d即得α=1+d/ln d≤2d/ln d；旧平方根Claim为τ=α的特例。v2（`WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v2`）保留主费用增量，把条件进一步降为α(τ−1)≥d，τ≥d+1给精确PNE，τ=1+ln d给d/ln d。v1身份与原证据保留；两版本独立重构/冻结攻击及新旧双路Fraction已接入原稿。仍缺异权hub、强迫失败时的稳定light/反馈控制与全类非势选态，WC-TARGET保持OPEN。

[跨源共享侧资源的强迫与目标倍率分离](research/current/weighted_congestion/shared_side_truncated_potential.md)第九节（`WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v1`）给出独立新身份：同权hub、唯一main source及二元同费副本下，UF强迫τ>1与目标α只需(τ−1)(α−1)≥d，无大小排序。d≥16取τ=1+ln d即得α=1+d/ln d≤2d/ln d；旧平方根Claim为τ=α的特例。独立先重构后冻结攻击及双路Fraction证据已接入原稿。仍缺异权hub、强迫失败时的稳定light/反馈控制与全类非势选态，WC-TARGET保持OPEN。

异权hub的局部比子类已由[降序侧势](research/current/weighted_congestion/shared_side_truncated_potential.md)第十节闭合：任意多权类、UFhet、α≥R与(α−1)²≥Kd给全antiPNE，旧同权Claim不变。当前真正未解是无界局部R/K或强迫失败的选态；单副本R边际损失在线性资源上可锐，不能直接把这个势的局部估计换成统一常数。
