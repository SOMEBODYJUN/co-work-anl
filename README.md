# 两阶段设施选址：可生长的研究基础

这里的**现行研究资产是重新写出的数学说明**，集中在 [research/current](research/current)；可执行算法集中在 [facility_spe](facility_spe)。原始手稿、旧证明笔记和上一轮整理稿进入 [history](history)。旧的 astra_alg、astra_local、astra_ring、asym_research 根目录已退出当前树；[迁移记录](research/path_migration.json)保留来源，而不让旧实验命名决定未来结构。

**Research Goal / 当前前沿：**从精确客户均衡与全部偏离续局出发，找能跨模型规模复用的近似 SPE 结构。[任意设施数共同目录定理](research/current/multi_facility/uniform_two.md)在内部证明层给出与设施数 $k$ 无关的因子 2 存在性；最佳常数是否低于 2、能否多项式时间构造仍开放。[方向价值与审查](research/K_FACILITY_AUDIT_2026-10-02.md)分清稳定性与覆盖效率。双侧任意长、每跨对最多一共有客户时的尖锐因子由 [SPARSE-RHO-ALL](research/current/heterogeneous/sparse_unbounded_rho.md) 的内部证明闭合为 $\rho$。共同目录的实例最优倍率判定已由[五地点新归约](research/current/shared/five_site_exact_hardness.md)覆盖每个固定有理 $1<a<\phi$，加上三地点 $a=1$；恰三、四地点的高倍率细分类仍开放。[实时研究状态](RESEARCH_STATE.md)、[命题入口](CLAIMS.md)、[失败路线](FAILED_ROUTES.md)与[路线图](research/ROADMAP.md)定位后续证明义务。

**A 篇后续（2026-10-02）：** [同址正规形](research/current/shared/instance_complexity_barriers.md)把共同目录**实例最优**精确算法的指数参数改为异址交叠 $\kappa_{\ne}$，并构造完整同址对半续局；[单交叠小目录阶梯](research/current/shared/small_sparse_catalogs.md)得到“至多 $N$ 个共同地点”的紧确普遍因子 $N=1,2:1$，$N=3:\sqrt2$，$N=4:\sqrt[3]4$，$N\ge5:\phi$。三、四地点结果有匹配的正有理下界；五地点把原六地点下界的可选目录缩小。[三地点全局归约](research/current/shared/three_site_exact_hardness.md)证明固定有理 $1\le a<(1+\sqrt3)/2$ 的判定弱 NP 完全；[五地点全局归约](research/current/shared/five_site_exact_hardness.md)进一步证明**每个固定有理 $1<a<\phi$** 的同类判定弱 NP 完全，保留三地点旧 Claim 的作用域。[原子粒度桥](research/current/shared/atomic_granularity.md)给小异址单体交叠时优于最坏 $\phi$ 的可构造实例保证。以上均是内部证明，尚无外部评审或完整新颖性核查；[独立内部数学及价值审查](research/FIVE_SITE_AUDIT_2026-10-02.md)区分本次受限类强化与已发表的一般模型困难性。

**研究状态：**共同目录的黄金比上界已有完整主稿、现行 Markdown 全分支重写及多轮内部审读；[六地点共同目录下界](research/current/shared/sharp_phi_lower.md)现已补出全布局与有理化证明，二者联合给出尖锐阈值。异构目录的因子 2 构造有成文主稿。受限稀疏 ρ 命题已有逐分支重写，[双方任意长单交叠的 ρ 上界](research/current/heterogeneous/sparse_unbounded_rho.md)本轮给出新全称证明；与原 2×2 下界合并即为同类尖锐阈值。程序能为具体输入生成证书；共享证书另有[独立定义级检查器](facility_spe/cli/verify_phi.py)。以上都尚未经过外部同行评审；内部证明、实例证书与学术发表分别标注。参见[命题与状态登记](research/current/claims.md)及[五轴状态表](research/review_status.json)。

**任意 k 的高效构造关口（2026-10-02）：**[计算前沿](research/current/multi_facility/polytime_frontier.md)将因子 2 存在性证明拆为两项算法义务。给定符合预算的在轨状态，偏离后的客户精确纯 NE 可用已发表的受限并行机算法在输入位长多项式时间完成；而原证明所用的全局字典序精确选址，连相同 reach 的共同目录也强 NP 难。四项预算只需要多项式邻域的局部最优，故有一个明确的 PLS 搜索上界，但目前没有多项式收敛界。真正缺口是同时找到可计算的在轨选址与客户 NE；原证明的全局最优不能直接当算法。
进一步的 SC-K-GREEDY-BUDGET 用多项式贪心造出**全部**转移预算；一个四客户实例显示在固定选址上将客户修到精确 NE 会破坏原预算。它把缺口集中到两者的**兼容构造**，仍未给出全 $k$ 高效 2 倍算法。
新[计算前沿](research/current/multi_facility/polytime_frontier.md)进一步证明：贪心后严格改派客户始终保持未开地点的 2 倍偏离者容量界；若贪心结果的每个占据地点恰有相同的 $q\ge2$ 家设施，则可借受限同速机器的多项式均衡算法同时恢复在轨精确 NE 与全部预算，得到该**可识别子类**上的多项式 2 倍完整续局。若贪心把 $k$ 家分到 $k$ 个不同地点，现有接口给多项式 3 倍续局。一般不等重数（含单设施源消失）的全 $k$ 多项式 2 倍目标仍开放；两条子类结论不冒充它的解决。

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

新增计算依赖：受限同速并行机 Nashification + 宏客户隔离 → MF-PURE-CAP-POLY；3-PARTITION → SC-K-LEXMAX-STRONG-HARD（只攻击精确全局选址）；按末次加座时序的贪心比较 → SC-K-GREEDY-BUDGET；贪心末次分数 + 严格客户改派的排序负载单调性 → SC-K-GREEDY-UNOPENED-2；贪心相同重数 $q\ge2$ + 文献算法保留上下负载 → SC-K-EQUAL-MULT-GREEDY-2；贪心全异址 + 同一文献算法 → SC-K-DISTINCT-GREEDY-3；单客户改派与单设施迁移的有限邻域 → SC-K-LOCAL-PLS → 条件性多项式离轨完成。这些边均在[计算前沿](research/current/multi_facility/polytime_frontier.md)证明，不能用精确 lexmax 强困难性推出完整因子 2 构造困难。

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
| `research/current/multi_facility/polytime_frontier.md` | 强 NP 难的精确全局字典序选址、足以证明预算的多项式局部邻域、贪心预算与空地点容量回收，以及文献算法保留负载上下界所给的等重数 $q\ge2$ 时完整多项式 2 倍和全异址时 3 倍子类算法；攻全 $k$ 高效算法时先读。一般不等重数与单设施源消失仍未解决。 |
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
