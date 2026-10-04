# 两阶段设施选址：可生长的研究基础

**最新可计算子类（2026-10-04）：**[地点图局部权种 DP](research/current/multi_facility/local_weight_box_dp.md)在轻客户选项的地点 primal 图固定树宽、每站不同轻权种类数固定时，精确判定和构造贪心盒内客户均衡；与浅层存在性定理合用产出完整多项式因子 2 续局。它包含此前[逐名关联树宽与度数选择器](research/current/multi_facility/bounded_incidence_box.md)，允许每站客户数增长。[入向星形算法](research/current/multi_facility/inward_star_box.md)处理叶先开、中心后开、任意多叶和异轻权，直接按动态键逐客构造完整盒内均衡及因子 2 续局；一个严格贪心族证明其中心可有任意多不同轻权。这两份文件分别记录精确类型约束、复杂度，以及星形不变量和分离族；一般混合交叠仍开放。

**最新精确选择器边界（2026-10-04）：**[SC-K-BOX-POTENTIAL-STRONG-HARD](research/current/multi_facility/polytime_frontier.md#sc-k-box-potential-strong-hard-exact-boxed-potential-optimization)证明，精确优化贪心完整盒内的全局客户势函数强 NP 难，甚至全部公共轻客户分配都自动在盒内。它复用已有 3-PARTITION 族，堵住将浅层存在性证明中的全局最小点直接当作多项式算法的路线；同族本身已有易求精确设施均衡，故不构成因子 2 构造困难性。[命题身份](research/current/multi_facility/claims.md#sc-k-box-potential-strong-hard----exact-full-box-potential-oracle)和[失败机制](FAILED_ROUTES.md#精确求贪心完整盒内全局客户势最小值作为通用选择器强-np-难)记录准确边界。当前真正缺口仍是异重部分交叠的一般盒内均衡存在性及高效选择，或绕开盒条件的证书。

**最新稀疏关联算法（2026-10-04）：**[逐名客户关联树宽与度数定理](research/current/multi_facility/bounded_incidence_box.md)把贪心负载盒内的精确客户均衡判定写成有限域树分解 DP。固定轻客户—站点二部图的树宽与**两侧逐名最大度数**时，能按输入位长多项式精确判定并选出盒内均衡；结合已有浅层有向图存在性证明，在两类条件同时成立的输入上得到完整的多项式因子 2 续局。一般输入的多项式因子 2 构造仍开放，且“只有树宽有界”没有这个运行时间保证。

**最新条件算法（2026-10-03）：**[轻客户锚定星形分量定理](research/current/multi_facility/polytime_frontier.md#sc-k-star-light-greedy-2-unequal-light-weights-on-anchored-star-edges)允许任意多叶、每条边任意不同轻权，以及冻结的跨分量重客户。按叶边权重递减、跨叶最小当前负载选择，每名轻客户仅处理一次，保住贪心负载盒并构造精确客户 NE；与[盒内离轨完成](research/current/multi_facility/polytime_frontier.md#sc-k-greedy-singleton-reset-and-sc-k-greedy-box-to-2)组合成位长多项式完整 2 倍续局。[严格三站例](examples/multi_facility/greedy_star_edges.json)不属旧 RANGE、ALL-OR-ONE、NESTED-ANCHOR 或 UNIFORM-LIGHT 条件。一般部分交叠图仍开放。

**最新算法边界（2026-10-03）：**[两异重轻客户参数族](research/current/multi_facility/polytime_frontier.md#sc-k-two-light-lower-potential-no-lower-bounded-potential-can-overflow-with-two-weights)证明，贪心布局上即使已有盒内精确客户均衡，对不同轻权客户最小化**带全部下盒的精确势**仍可能唯一选到越上盒的均衡。这隔离了同重费用流逆路径论证的失效；全输入位长多项式 2 倍算法及盒内 NE 的普遍存在性依然开放。[失败机制](FAILED_ROUTES.md#在异重轻客户下用下盒约束的全局势最小化替代同重费用流错误)、[逐命题记录](research/current/multi_facility/claims.md#sc-k-two-light-lower-potential-no----unequal-light-weights-defeat-the-flow-extension)、[整数输入](examples/multi_facility/greedy_two_light_potential.json)与[精确审查](tests/audits/kfac_two_light_potential.py)给出恢复入口。

这里的**现行研究资产是重新写出的数学说明**，集中在 [research/current](research/current)；可执行算法集中在 [facility_spe](facility_spe)。原始手稿、旧证明笔记和上一轮整理稿进入 [history](history)。旧的 astra_alg、astra_local、astra_ring、asym_research 根目录已退出当前树；[迁移记录](research/path_migration.json)保留来源，而不让旧实验命名决定未来结构。

**Research Goal / 当前前沿：**从精确客户均衡与全部偏离续局出发，找能跨模型规模复用的近似 SPE 结构。[任意设施数共同目录定理](research/current/multi_facility/uniform_two.md)在内部证明层给出与设施数 $k$ 无关的因子 2 存在性；最佳常数是否低于 2、能否多项式时间构造仍开放。[方向价值与审查](research/K_FACILITY_AUDIT_2026-10-02.md)分清稳定性与覆盖效率。双侧任意长、每跨对最多一共有客户时的尖锐因子由 [SPARSE-RHO-ALL](research/current/heterogeneous/sparse_unbounded_rho.md) 的内部证明闭合为 $\rho$。共同目录的实例最优倍率判定已由[五地点新归约](research/current/shared/five_site_exact_hardness.md)覆盖每个固定有理 $1<a<\phi$，加上三地点 $a=1$；恰三、四地点的高倍率细分类仍开放。[实时研究状态](RESEARCH_STATE.md)、[命题入口](CLAIMS.md)、[失败路线](FAILED_ROUTES.md)与[路线图](research/ROADMAP.md)定位后续证明义务。

**A 篇后续（2026-10-02）：** [同址正规形](research/current/shared/instance_complexity_barriers.md)把共同目录**实例最优**精确算法的指数参数改为异址交叠 $\kappa_{\ne}$，并构造完整同址对半续局；[单交叠小目录阶梯](research/current/shared/small_sparse_catalogs.md)得到“至多 $N$ 个共同地点”的紧确普遍因子 $N=1,2:1$，$N=3:\sqrt2$，$N=4:\sqrt[3]4$，$N\ge5:\phi$。三、四地点结果有匹配的正有理下界；五地点把原六地点下界的可选目录缩小。[三地点全局归约](research/current/shared/three_site_exact_hardness.md)证明固定有理 $1\le a<(1+\sqrt3)/2$ 的判定弱 NP 完全；[五地点全局归约](research/current/shared/five_site_exact_hardness.md)进一步证明**每个固定有理 $1<a<\phi$** 的同类判定弱 NP 完全，保留三地点旧 Claim 的作用域。[原子粒度桥](research/current/shared/atomic_granularity.md)给小异址单体交叠时优于最坏 $\phi$ 的可构造实例保证。以上均是内部证明，尚无外部评审或完整新颖性核查；[独立内部数学及价值审查](research/FIVE_SITE_AUDIT_2026-10-02.md)区分本次受限类强化与已发表的一般模型困难性。

**研究状态：**共同目录的黄金比上界已有完整主稿、现行 Markdown 全分支重写及多轮内部审读；[六地点共同目录下界](research/current/shared/sharp_phi_lower.md)现已补出全布局与有理化证明，二者联合给出尖锐阈值。异构目录的因子 2 构造有成文主稿。受限稀疏 ρ 命题已有逐分支重写，[双方任意长单交叠的 ρ 上界](research/current/heterogeneous/sparse_unbounded_rho.md)本轮给出新全称证明；与原 2×2 下界合并即为同类尖锐阈值。程序能为具体输入生成证书；共享证书另有[独立定义级检查器](facility_spe/cli/verify_phi.py)。以上都尚未经过外部同行评审；内部证明、实例证书与学术发表分别标注。参见[命题与状态登记](research/current/claims.md)及[五轴状态表](research/review_status.json)。

**任意 k 的高效构造关口（2026-10-02）：**[计算前沿](research/current/multi_facility/polytime_frontier.md)将因子 2 存在性证明拆为两项算法义务。给定符合预算的在轨状态，偏离后的客户精确纯 NE 可用已发表的受限并行机算法在输入位长多项式时间完成；而原证明所用的全局字典序精确选址，连相同 reach 的共同目录也强 NP 难。四项预算只需要多项式邻域的局部最优，故有一个明确的 PLS 搜索上界，但目前没有多项式收敛界。真正缺口是同时找到可计算的在轨选址与客户 NE；原证明的全局最优不能直接当算法。
进一步的 SC-K-GREEDY-BUDGET 用多项式贪心造出**全部**转移预算；一个四客户实例显示在固定选址上将客户修到精确 NE 会破坏原预算。它把缺口集中到两者的**兼容构造**，仍未给出全 $k$ 高效 2 倍算法。
新[计算前沿](research/current/multi_facility/polytime_frontier.md)进一步证明：贪心后严格改派客户始终保持未开地点的 2 倍偏离者容量界；旧的同重数分量子类已能多项式构造 2 倍完整续局，后续见下段更强结果。五地点整数例表明客户改派后冻结存续地点逐站装箱会失败；加强的六地点例表明即使允许任意跨站重分，旧证明要求的全局 $2a$ 容量状态也可能根本不存在，尽管偏离者在某个精确 NE 中只获 $a$ 以下。这些反例不否定在别的客户均衡选取下得到 2 倍证书。

**本轮新检查（2026-10-03）：**[计算前沿](research/current/multi_facility/polytime_frontier.md)把贪心全异址输出的旧 3 倍界**提升为位多项式 2 倍**：首开的最大 reach $R$ 地点保留 $R/2$ 再加座得分，故最后分数 $\gamma\ge R/2$；同速客户均衡算法保留每家至少 $\gamma$，任意偏离收益均至多 $R$。更宽的**重数类区间证书**按每个已占地点的设施重数分组，用同速均衡算法修复组内客户，并逐客户核查跨重数激励；单设施源的客户池预算处理地点消失。它包含“权重小于 $\gamma$ 的客户不跨重数”子类，还允许一部分跨重数的轻客户和多地点 $q=1$ 分量，严格扩展旧条件子类。两个[精确整数例](research/current/multi_facility/polytime_frontier.md#sc-k-greedy-repair-order-no-exact-repair-order-can-lose-factor-two)又证明：任意严格改派顺序、甚至每步选择**最重可改善客户**，都可能到达真正超过 2 倍的在轨 NE；同一贪心布局另有好 NE。因此下一关是对**区间证书不成立的混合重数输入**选择合适的在轨均衡或改变选址。全输入多项式 2 倍构造仍开放。

**继续推进（2026-10-03）：**[双地点混合重数分量定理](research/current/multi_facility/polytime_frontier.md#sc-k-two-site-component-greedy-2-mixed-multiplicities-in-a-two-site-component)把上述条件类进一步扩到任意多个交叠分量，只要每个分量重数一致或仅有两个地点。双地点分量按共有客户权重递减、只从较高重数向较低重数做严格改善；每客户至多移动一次，保住负载区间及源地点消失时的装箱预算。它能处理区间证书失败的轻跨重数客户。另有两条[固定布局选均衡障碍](research/current/multi_facility/polytime_frontier.md#sc-k-greedy-fixed-lexmax-no-the-fixed-layout-lexmax-can-select-the-bad-ne)：精确字典序最大客户分配可以唯一选中坏 NE；另一份整数例连**全局客户势函数最小值**也唯一选中坏 NE，分别在离轨所有混合均衡中超过 2 倍。同布局仍有好 NE。全输入位长多项式 2 倍算法继续开放，下一步聚焦含至少三个地点且重数不等的交叠分量。

**再推进一层（2026-10-03）：**[全站共有或单站私有分量定理](research/current/multi_facility/polytime_frontier.md#sc-k-all-or-one-component-greedy-2-arbitrarily-many-mixed-multiplicity-sites)允许一个分量有**任意多**个不同重数的地点：只要求每名客户在这个分量的已占选项要么只有一站，要么是全部站。把全站共有客户按权重递减放到当前单位设施负载最低的地点，可多项式地得到精确客户 NE，保住负载区间和所有偏离预算；此前双地点类是它的特例。三地点 $(3,2,1)$ 整数例使旧区间证书失败却满足新条件。相反，一份[三地点链形交叠例](research/current/multi_facility/polytime_frontier.md#sc-k-descent-only-trap-no-three-site-partial-overlap-needs-an-upward-return)证明所有严格向低重数改派的路径都在一个非 NE 状态停下，必须允许客户向高重数返回；该例仍有精确客户 NE，不是 2 倍反例。因此前沿已缩到**三站及以上混合重数、部分客户只覆盖其中某些站**的交叠结构及其选均衡机制。

**部分交叠的新闭合（2026-10-03）：**[嵌套锚站定理](research/current/multi_facility/polytime_frontier.md#sc-k-nested-anchor-greedy-2-a-partial-overlap-mixed-component)允许任意大的混合重数分量中存在真正的部分交叠：首开地点覆盖所有多选项客户，且这些客户按权非增排列时已占选项集逐步扩张。受限列表分配的“最后入站客户”给精确 NE，共同锚站保住所有贪心负载盒，私有储备处理单设施源消失，因此得到位长多项式完整 2 倍续局。三站 $(3,2,1)$ 严格例不满足旧 ALL-OR-ONE 或 RANGE；交换两个客户的选项集使同一列表法失败，却仍有另一个 NE。一般非嵌套、无共同锚站的三站交叠仍开放。

**离轨瓶颈再收紧（2026-10-03）：**[原单设施站重置引理与盒内续局定理](research/current/multi_facility/polytime_frontier.md#sc-k-greedy-singleton-reset-and-sc-k-greedy-box-to-2)表明：对贪心布局上任何原 $q=1$ 设施，只要在轨收益 $a\ge\gamma$，离轨客户可独立重置到最初贪心分配，给偏离者构造收益至多 $2\gamma\le2a$ 的精确纯 NE，**不需要**在轨客户分配保持私有储备。于是只要找到所有站总重在 $[q_t\gamma,(q_t+1)\gamma]$ 的精确站纯/站内均匀 NE，就能多项式完成完整 2 倍续局。新的[同重轻客户费用流定理](research/current/multi_facility/polytime_frontier.md#sc-k-uniform-light-flow-2-partial-overlaps-without-a-common-anchor)在所有低于 $\gamma$ 的多选项客户同重 $\delta$ 时，用带站点下界的整数凸费用流选出盒内 NE；一条反向同重运输路径排除上盒溢出。它包含无共同锚站的三站链 $(3,2,1)$ 严格例。不同轻权的一般情形尚未闭合。

## 先判断输入属于哪条命题

| 目标 | 同时要求 | 可得到什么 | 从哪里开始读 |
| --- | --- | --- | --- |
| 共同目录的普遍构造 | 两设施同一非空地点目录；正权重、显式覆盖；强制服务；客户最小化实际负载；允许每个布局各选精确独立混合 NE | 因子不超过 \(\phi=(1+\sqrt5)/2\) 的一个纯选址证书；**不是**实例最优因子 | [共享定理、证明与算法](research/current/shared/README.md) |
| 任意设施数共同目录 | 任意 $k\ge2$ 家带标签设施共用同一非空地点目录；正权原子客户与完整精确续局 | **存在**因子至多 2 的纯选址证书；目前构造为有限穷举，2 的尖锐性未证 | [任意 $k$ 证明与审查](research/current/multi_facility/README.md) |
| 任意异构目录的普遍构造 | 两个非空目录可不同；同一负载模型；选用纯客户 NE 延续 | 因子不超过 2 的证书；整数反例族表明异构类不能统一降到 2 以下 | [异构分支](research/current/heterogeneous/README.md) |
| 稀疏异构的较小常数 | **每个跨目录地点对至多一名共有客户，且一侧目录至多两地点** | 现行内部证明给出尖锐普遍因子 \(\rho=2\cos(\pi/7)\)；外部评审未进行 | [受限 \(\rho\) 全分支证明](research/current/heterogeneous/restricted_rho.md) |
| 双方任意长的单交叠目录 | 每个跨目录地点对至多一名共有客户；双方目录大小任意 | 新内部证明给完整纯 NE 续局的普遍因子 \(\rho\)；原受限类 2×2 下界证明同一阈值尖锐 | [SPARSE-RHO-ALL](research/current/heterogeneous/sparse_unbounded_rho.md) |
| 某一个输入的最优因子 | 两设施同一线性负载模型；接受对共有客户数指数增长的时间 | 支持区间枚举给该实例最优因子；短证书单独仅证明“达到” | [局部几何与精确方法](research/current/local_and_exact/README.md) |

完整的客户最优反应式、延续量词和编码界限在[规范模型](research/current/model.md)。[使用说明](USAGE.md)列出可直接运行的命令与证书语义。

## 定义和推导地图

- 输入的带标签布局、客户覆盖、正权原子与实际负载费用在 [model.md §1](research/current/model.md) 定义；两设施公共客户的独立混合 NE 在 §2 化为条件成本差。§3 对全部布局的 NE 选择定义完整续局及真实的全目录偏离威胁。
- `model/NE` → 局部支持几何 → 共同目录固定菜单与全目录环 → 局部强弦 → `SC-PHI-E`；编码有理输入加位复杂度给 `SC-PHI-A`，联合六地点同类下界才得 `SC-PHI-SHARP`。[共享证明顺序](research/current/shared/README.md)。
- `model/NE` → 真实异址坐标极小值与同址对半 NE → `SC-DIAG-NORMAL` → `SC-OFFDIAG-FPT`：指数参数只用不同地点客户交叠，完整证书在所有同址布局均对半。[结构与算法](research/current/shared/instance_complexity_barriers.md)。这条边不证明无界交叠的 `DEC_a` 多项式。
- `LOCAL-HARD` 的精确局部差额谱 + **三地点可实现覆盖及六类布局守卫** → `SC-THREE-DEC1-HARD`、`SC-THREE-DECa-HARD`：全局 $\mathrm{DEC}_a$ 对每个固定有理 $1\le a<(1+\sqrt3)/2$ 弱 NP 完全；不把已发表的更多设施异构目录难性误移到本类。[完整归约和端点预算](research/current/shared/three_site_exact_hardness.md)。
- SUBSET SUM 三态局部极值 + 严格强制宏原子的双向 NE 等价 + 五地点正权守卫及全部带标签布局 → `SC-FIVE-DECa-HARD`：对每个固定有理 $1<a<\phi$，即使两个设施有相同的恰五地点目录，$\mathrm{DEC}_a$ 仍弱 NP 完全；这与旧三地点端点障碍相容。[全证明](research/current/shared/five_site_exact_hardness.md)、[审查与价值边界](research/FIVE_SITE_AUDIT_2026-10-02.md)。
- 已知可拆分客户的精确选址势 + 本模型 (NE) 的单体误差 → `SC-GRANULAR-APPROX`：$\theta<R_{\max}$ 时完整原子续局因子至多 $(R_{\max}+\theta)/(R_{\max}-\theta)$。[两设施证明](research/current/shared/atomic_granularity.md)。固定布局运输引理 `LOCAL-ATOM-WARDROP-k` 的尖锐误差 $(k-1)\theta/2$ 说明不能把两设施的任意 NE 误差常数照搬到全 $k$，[一般局部证明](research/current/local_and_exact/atomic_wardrop_gap.md)。
- `model/NE` + **共同目录且异址单交叠** → 按 reach 全序选纯 NE、同址重客户菜单 → 分别证明 `SC-SPARSE-3` ($\sqrt2$) 与 `SC-SPARSE-4` ($\sqrt[3]4$)；各自正有理族给匹配下界。`SC-SPARSE-5` 的上界另依赖 `SC-PHI-E`，下界是原六地点 $\phi$ 族的五地点合法限制。这是**至多地点数的阶梯**，不是把异构 `\rho` 类包含进去。[逐式证明](research/current/shared/small_sparse_catalogs.md)。
- `model/NE` → 异构纯菜单、全目录环 → `HC-2-UP`；与双交叠下界 `HC-2-LOW` 合取才得异构 sharp 2。`HC-RHO` 给单交叠且一侧最多两地点的已知锐性；移除长度条件由新 `SPARSE-RHO-ALL` 全称上界证明，结合该下界解决 [Q-SPARSE](research/questions/sparse_catalogs.md)。[异构证明顺序](research/current/heterogeneous/README.md)。
- `CORE-LIFT` 只保留全目录真实威胁而不保证核心短。[SPARSE-LONG-CYCLE](research/current/heterogeneous/sparse_long_cycles.md)在单交叠下构造任意长唯一环，反驳无条件短核心推断；它与普遍倍率 $\rho$ 问题之间没有反例蕴含。
- [SPARSE-BAD-LONG](research/current/heterogeneous/sparse_bad_long_cycles.md)在**确实没有 `r` 稳定格**、`3/2<r<ρ` 时构造任意长唯一精确回应环；新命题版本 `SPARSE-BAD-LONG-ALL` 证明同一失败机制覆盖每个 `1≤r<ρ`，所有高行仍只用一种重客户身份。它排除阈值以下的统一短**精确回应闭核心**，但不排除更弱的坏见证压缩；在 `ρ` 处不冲突于 `SPARSE-RHO-ALL`。
- `model/NE` → 固定纯平局优先级 → 全目录最佳回应逐边比较 → `SPARSE-HIGH-ACYCLIC` → `SPARSE-BALANCED-R`：[高 reach 条件传播](research/current/heterogeneous/sparse_high_reach_barrier.md)对任意 `r≥1` 给出坏环低区必经和 reach 平衡子类上界；它是新全类 `ρ` 证明的依赖，而非全称证明本身。
- `SPARSE-HIGH-ACYCLIC` → 首个高到低边界、单客户同一身份容量、`q(ρ)=0` → `SPARSE-RHO-ALL`：新证明直接排除任意长坏环的首个低区入口，**不**压缩回应核心。旧条件结果仍是一般 `r` 的独立量化边界；原“低区回返阻碍”在 `r=ρ` 已消除。
- `MF-MODEL` → 全局字典序选址与消失源地点的转移预算 → 超重原子隔离装箱与严格改善的纯 NE 修复 → `SC-K-2-E`：任意 $k$ 共同目录有因子 2 完整精确续局。[全证明](research/current/multi_facility/uniform_two.md)。该结果不依赖两设施的 $\phi$ 证明，也不覆盖异构目录或三次客户费用；证书的达到性、普遍定理和论文新颖性各自独立。

关键 dependency、attacks 和 scope 边可交互查看[数学超图](research/index.html)，精确文字与证据状态以[现行命题登记](research/current/claims.md)和证明页为准。

新增计算依赖：受限同速并行机 Nashification + 宏客户隔离 → MF-PURE-CAP-POLY；3-PARTITION → SC-K-LEXMAX-STRONG-HARD（只攻击精确全局选址）；按末次加座时序的贪心比较 → SC-K-GREEDY-BUDGET；首开与末次加座得分 → SC-K-GREEDY-MAX-MULT（初始客户占据最大最终重数地点）；贪心末次分数 + 严格客户改派的排序负载单调性 → SC-K-GREEDY-UNOPENED-2；贪心相同重数 $q\ge2$ + 文献算法保留上下负载 → SC-K-EQUAL-MULT-GREEDY-2；各客户交叠分量内同重数并隔离单点 $q=1$ → SC-K-COMPONENT-MULT-GREEDY-2；贪心全异址 + 同一文献算法 → SC-K-DISTINCT-GREEDY-3；五地点客户改派反例 → SC-K-GREEDY-STATIC-PACK-NO；六地点增加新目标的强制客户反例 → SC-K-GREEDY-CAP-INFEASIBLE；单客户改派与单设施迁移的有限邻域 → SC-K-LOCAL-PLS → 条件性多项式离轨完成。这些边均在[计算前沿](research/current/multi_facility/polytime_frontier.md)证明，不能用精确 lexmax 强困难性推出完整因子 2 构造困难。

本轮新增依赖：首开最大 reach 地点的持续再加座分数 + 同速均衡的最小负载保持 → SC-K-DISTINCT-GREEDY-2；按重数分组的均衡负载区间 + 跨组客户条件成本证书 + 贪心单设施地点客户池 → SC-K-RANGE-GREEDY-2。轻客户交叠图条件与全重交叠条件是该区间证书的可检查充分特例。严格客户改派顺序的两个有限反例只攻击“任意终点均安全”和“最重客户优先均安全”，不攻击区间证书或贪心布局的存在性。

双地点新依赖：贪心初始最大重数归属 + 两站负载差 $\Delta$ 的递减扫描 + 向低重数严格改派保留负载区间 + 单设施站原重站客户回收恒等式 → SC-K-TWO-SITE-COMPONENT-GREEDY-2。有限选择障碍：首份整数例的全部地点纯分配最小负载比较 → SC-K-GREEDY-FIXED-LEXMAX-NO；第二份整数例的客户势函数精确变化与仅两项客户 NE 分类 → SC-K-GREEDY-FIXED-POTENTIAL-NO。两者只排除固定贪心选址后的指定客户选择规则。

任意大分量新依赖：贪心最大重数首站 + 全站共有客户按权递减的最小单位负载分配 + 首站余额控制负载区间 + 单设施站私有客户储备 → SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2；它按输出范围包含双地点定理，证明机制另有独立内容。三地点 H--M--L 的唯一下降改派路径及强制上升回返 → SC-K-DESCENT-ONLY-TRAP-NO，只限制不能回返的客户修复规则。

新部分交叠依赖：贪心最大重数共同锚站 + 按权非增而选项集递增的受限列表分配 + 私有客户储备 → SC-K-NESTED-ANCHOR-GREEDY-2；全站共有是特例。反序选项集的三站例仅攻击无条件列表规则，不攻击贪心布局；它的精确复算由 `tests/audits/kfac_nested_anchor.py` 给出。

新离轨与流依赖：贪心初始最大重数归属 + 原 $q=1$ 客户池上界 + 原初始预算 (8) + 多项式有界装箱修复 → SC-K-GREEDY-SINGLETON-RESET；与给定精确在轨负载盒结合 → SC-K-GREEDY-BOX-TO-2。把全部轻多选项客户视为同重整数流 + 每站最低负载约束 + 逆向运输路径严格降势 → SC-K-UNIFORM-LIGHT-FLOW-2，再调用 BOX-TO-2。盒内 NE 是充分入口；后述 RESET-PACK 另能认证越盒的在轨 NE。

新阶段的 [重置客户池与双 LPT 证明](research/current/multi_facility/polytime_frontier.md#sc-k-reset-pack-interface-reset-based-off-path-completion-beyond-the-box) 允许构造一个站点越上盒但仍有完整 2 倍续局的纯客户 NE；同稿的有向轻路径算法覆盖边际不同轻权的 P4。固定占站数/不同权数的类型 ILP 与固定全目录/不同权数的 XP 构造见[参数化证明](research/current/multi_facility/type_compression.md)。一般全输入位长多项式 2 倍仍开放。

[三站异轻权链的存在性证明](research/current/multi_facility/three_site_chain_box.md)采用完整盒内势最小和整批上游退回交换；尚无位长多项式选取该最小点的算法。

[四站汇聚路径的三轻客户子类](research/current/multi_facility/converging_path_box.md)另给有限步盒内 NE 构造，超出所有边同向的 PATH 条件。

[浅层有向轻客户图存在性](research/current/multi_facility/height_two_box.md)将三站链的整池交换推广到任意分叉和汇合，但仍缺多项式盒内势最小选择器。

[汇聚路径四步构造](research/current/multi_facility/converging_four_moves.md)放宽先前七步小类的初始负载及重数条件，仍保留每边一轻客户。

## 如何追踪一项研究结论

[命题登记](research/current/claims.md)固定适用域与状态；[现行资产索引](ASSETS.md)把命题连到新稿、实现、检验及历史来源。[数学超图](research/index.html)的节点是定义、引理、反例和结论；一条推导超边要求**所有列出的共同前提**，不是旧文件之间的链接。其[数据](research/graph.json)和[维护规则](research/README.md)可直接核查。GitHub 预览 HTML 时显示源码，下载 HTML 后可使用交互查看器。

[下一阶段研究路线](research/ROADMAP.md)区分新数学问题与现有资产的交付。新问题从 [research/questions](research/questions) 开始；新分支在 research/current/ 下增长，代码、证据、反例分别进入各自目录。[新增研究规则与命题模板](research/GROWTH.md)规定如何写量词、证明链、实现合同、状态和证据；[AGENTS.md](AGENTS.md)让后续研究协作者在改动前执行同一套规则。不能仅搬来一份旧稿或通过有限测试就升级定理。

| 仓库区域 | 职责 |
| --- | --- |
| [research/current](research/current) | 此轮重新撰写的现行模型、命题、数学推导和算法解释 |
| [facility_spe](facility_spe) / [multi_facility_spe](multi_facility_spe) / [tests](tests) | 双设施与任意设施数分别使用规范代码包；回归与独立比较有明确适用范围 |
| [examples](examples) / [evidence](evidence) | 输入实例、实例证书、冻结实验记录 |
| [history](history) | 原始手稿、旧笔记、失效路线和上一版整理文本；用作来源而非现行入口 |

## 下次接手时先读哪些文件

| 完整路径 | 为什么存在；什么时候使用 |
| --- | --- |
| `README.md`、`RESEARCH_STATE.md`、`CLAIMS.md`、`FAILED_ROUTES.md` | 恢复目标、前沿、命题身份和失效机制；接手任何新问题先读。它们是地图，证明仍在链接的现行数学稿。 |
| `research/current/model.md`、`research/current/claims.md` | 核对客户 NE、完整续局量词、各定理的精确作用域及审查状态；提出新命题或改模型前读。 |
| `research/ROADMAP.md`、`research/questions/three_facilities.md`、`research/questions/sparse_catalogs.md` | 两个当前主攻的价值门槛、首个判别关口、已知上下界与停损理由；选题时读。 |
| `research/current/heterogeneous/sparse_long_cycles.md`、`FAILED_ROUTES.md` | 任意长精确威胁环的正整数构造、完整证明及其**仅限于无条件短核心**的排除范围；攻击稀疏证明路线时读。 |
| `research/current/heterogeneous/sparse_high_reach_barrier.md` | 新增 `SPARSE-HIGH-ACYCLIC` 与 `SPARSE-BALANCED-R` 的全部量词、平局与零 reach 证明、两处独立边界攻击；研究坏环如何穿越低 reach 区时读。 |
| `research/current/heterogeneous/sparse_unbounded_rho.md` | `SPARSE-RHO-ALL` 全类尖锐阈值的精确范围、固定完整纯续局、首个高到低边界引理、客户身份强制相同、三次式矛盾与独立攻击；接手 Q-SPARSE 或审查新上界时先读。 |
| `research/current/heterogeneous/sparse_bad_long_cycles.md` | 旧版 `3/2<r<ρ` 与新版本全部 `1≤r<ρ` 的真实坏倍率任意长回应环、明示 `7/4` 有理权族、一般开参数与精确核心失败机制；检验任何条件性短核心或身份代表引理时读。 |
| `research/current/shared/instance_complexity_barriers.md`、`facility_spe/exact/shared_offdiag.py`、`tests/test_shared_offdiag.py` | 同址正规形的精确最优值公式、零收益与完整对半续局证明；异址交叠参数的支持枚举实现及独立比较。研究低于 $\phi$ 的实例判定或高同址交叠输入时先读；程序证书核验不代替全称证明。 |
| `research/current/shared/three_site_exact_hardness.md` | 将局部 SUBSET SUM 客户谱嵌入三地点共同目录，逐一堵住同址、AB、AC、BC 的所有逃逸；证明固定有理 $1\le a<(1+\sqrt3)/2$ 的弱 NP 完全性，列出两套守卫及端点正权预算障碍。研究下一段复杂度前沿时先读，切勿把端点当模型相变。 |
| `research/current/shared/five_site_exact_hardness.md`、`research/FIVE_SITE_AUDIT_2026-10-02.md` | 五地点新覆盖、强制桥宏原子和全布局守卫证明每个固定有理 $1<a<\phi$ 的弱 NP 完全性；审查页核对原目标同一性、2024 年广义困难性优先权边界及与 A/B 成果的相对价值。研究实例复杂度或组织 A 篇时读。 |
| `research/current/multi_facility/uniform_two.md`、`research/K_FACILITY_AUDIT_2026-10-02.md` | 任意 $k$ 的共同目录因子 2 存在性证明、逐式逆审、方法边界及面向领域的价值解释；研究多设施稳定性时先读。无多项式构造或因子 2 尖锐性结论。 |
| `research/current/multi_facility/bounded_incidence_box.md` | 固定逐名轻客户—站点二部关联图树宽 `tau` 与两侧最大度 `d` 的精确盒内 NE 有限域 DP、树分解转换和位复杂度；结合浅层有向图存在性得完整多项式因子 2。审查稀疏交叠算法时读；只有树宽有界、类型合并或一般输入均不由本命题覆盖。 |
| `research/current/multi_facility/polytime_frontier.md` | 精确全局字典序选址的强 NP 难性、多项式局部邻域、贪心预算、全异址 **2 倍**与重数类区间证书；双地点混合重数、任意大“全站共有或单站私有”及“嵌套锚站部分交叠”分量的多项式构造，均处理单设施源预算。给出坏修复、固定布局字典序、势最小化、无条件锚站列表失败和三站下降改派停在非 NE 的不同障碍。攻全 $k$ 高效算法时先读；非嵌套或无共同锚站的混合重数部分交叠仍开放。 |
| `examples/multi_facility/greedy_nested_anchor.json`、`tests/audits/kfac_nested_anchor.py` | 三站五客户正整数例及独立 Fraction 复算：严格贪心、嵌套选项列表得到精确 NE、旧 RANGE 失败；交换两个选项集后无条件列表法非 NE，但另一分配仍是 NE。检验嵌套锚站证明的有限边界时读，不能代替全称证明。 |
| `examples/multi_facility/greedy_star_edges.json`、`tests/audits/kfac_star_edges.py` | 六设施、三站锚定星形的严格整数分离例和独立 Fraction 检查；两名异重轻客户的 HM/HL 选项不可比，旧 RANGE、ALL-OR-ONE、NESTED-ANCHOR、UNIFORM-LIGHT 均不适用。审查 SC-K-STAR-LIGHT-GREEDY-2 的实际条件、单步修复及盒/NE 时读；脚本不证明普遍算法。 |
| `examples/multi_facility/greedy_two_light_potential.json`、`tests/audits/kfac_two_light_potential.py` | 七设施、四站、仅两名异重轻客户的四态势障碍输入；精确脚本重算严格贪心、全部下盒、唯一越上盒势极小与仍存在的盒内 NE。考虑异重费用流扩展或势选择规则时读；一般无限族由 `polytime_frontier.md` 的代数证明。 |
| `examples/multi_facility/greedy_uniform_light_flow.json`、`tests/audits/kfac_uniform_light_flow.py` | 无共同锚站的三站链正整数例及独立 Fraction 复算：严格贪心、所有轻多选项客户同重、下界势最小唯一盒内 NE、旧 RANGE 失败。阅读费用流新定理的严格超出旧子类例时使用；有限枚举不证明一般定理。 |
| `examples/multi_facility/greedy_descent_trap.json`、`tests/audits/kfac_descent_trap.py` | 六客户、三地点 H--M--L 的整数输入与独立 Fraction 审查：六次无并列贪心、唯一三步下降改派、被迫上升回返及其后的精确 NE。检验“只允许重数下降”或照搬双站递减扫描的算法时读；该例不否定 2 倍布局。 |
| `examples/multi_facility/greedy_cap_obstruction.json`、`tests/audits/kfac_greedy_cap.py` | 六地点十顾客的精确整数输入与独立 Fraction 检查：重算确定性贪心得分、五次严格客户改派、在轨精确 NE、B/E/G 的强制 $44>41$ 容量障碍和偏离者仅获 $20$ 的离轨精确 NE。研究 SC-K-GREEDY-CAP-INFEASIBLE 的算术或试图修改装箱接口时运行；有限检查不替代文件中的全称定理证明。 |
| `examples/multi_facility/greedy_repair_order_escape.json`、`tests/audits/kfac_greedy_repair_order.py` | 第一份六地点整数输入和独立 Fraction 审核：贪心得分、五步严格客户改善、坏终点精确 NE、B→G 在所有混合 NE 强制 $32/15$ 倍；新增全部 16 个地点纯分配的精确枚举，核查该坏终点也是固定贪心布局唯一 lexmax。同布局另一终点保留四预算。设计客户修复规则时读；只证明固定实例的失效。 |
| `examples/multi_facility/greedy_potential_escape.json`、`tests/audits/kfac_greedy_potential.py` | 第二类六地点整数选择障碍：十客户显式覆盖、固定贪心布局全部 16 种地点纯分配的 Fraction 枚举，两项精确客户 NE 势值 86200 与 86264，唯一全局势最小者在所有离轨混合 NE 中遭受 $215/107>2$ 倍偏离。检查任何“势函数最小化就能选好 NE”的路线时读；有限检验配合证明页的两项 NE 分类与势差恒等式。 |
| `examples/multi_facility/greedy_heaviest_escape.json`、`tests/audits/kfac_greedy_heaviest.py` | 第二份整数输入及每步**唯一最重可改善客户**的审核，终点离轨强制倍率 $88/43$；另一个终点仍保留四预算。评估按重量排序的修复策略时读，不能据此否定贪心选址的存在性。 |
| `research/current/shared/atomic_granularity.md`、`research/current/local_and_exact/atomic_wardrop_gap.md` | 前者将已知可拆分客户 SPE 特化为两设施对照，证明任意精确原子 NE 的误差与完整续局倍率，并给宏原子必要条件；后者对固定 $k$ 布局证明尖锐 $(k-1)\theta/2$ 误差与链族。做实例敏感构造、归约粒度限制或多设施延伸时读；局部误差不等于全 $k$ SPE。 |
| `research/current/shared/small_sparse_catalogs.md` | 单交叠的最多 2/3/4/5 地点紧确普遍因子、纯菜单全分支、三/四地点正有理族、五地点原下界剪枝。构造有限目录论文主题、比较目录规模机制或攻击平局零收益时读；五地点下界同时回读 `shared/sharp_phi_lower.md`。 |
| `examples/shared/sparse_four_rational.json` | 四地点五客户下界族的 $z=19/12,\varepsilon=1/1000$ 精确输入；实例最优倍率 $6327/4000$，用于验证 $\sqrt2$ 无法延伸到四地点。复现例子而非证明全称族时读。 |
| `research/PUBLICATION_REVIEW.md` | 本轮独立数学审读、证据回归、文献优先权缺口、两篇论文的严格贡献分配与投稿准备状态；组织投稿时读，不能用期刊判断替代命题证明。 |
| `tests/audits/sparse_bad_long_cycles.py`、`examples/heterogeneous/sparse/bad_long_n3.json`、`evidence/runs/2026-10-01/sparse_bad_long_cycles.json` | 从真实客户覆盖生成输入，按 Fraction 重算唯一 NE、全部布局因子及全目录严格回应；冻结 `n=1,2,3,10,30,100`，只是算术攻击，不能代替全 `n,r` 证明。 |
| `tests/audits/sparse_high_reach.py`、`evidence/runs/2026-10-01/sparse_high_reach.json` | 不调用规范求解器的精确分数审查、固定 seed 和冻结结果：包含原六客户下界、修正后长环小例、随机矩形 incidence；复核新定理边界时运行脚本重生记录。有限审查不代替全称证明。 |
| `research/questions/cubic_costs.md`、`research/questions/instance_complexity.md` | 非线性费用机制和实例最优判定的条件性预研；遇到跨成本原则、参数算法或困难性归约时读。 |
| `research/graph.json`、`research/review_status.json`、`research/assets.json` | 数学合取/反例边、逐命题审查层、证明与实现和证据的对照；状态升级或新增 Claim 时一起更新。 |
| `research/GROWTH.md`、`AGENTS.md` | 新问题、证明、代码和冻结证据的落点与检查命令；开始修改前读。 |

当前没有选定公共软件许可或外部证明认证。要用于具体研究输入，请按[条件表](ASSETS.md)选择算法，运行后核查证书，并把普遍定理状态与实例验证结论分开报告。
