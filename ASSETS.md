# 现行研究资产：命题而非旧文件的清单

本表以[共同模型](research/current/model.md)为起点。每行沿着**同一组前提 → 数学结论 → 本轮新写的推导 → 程序/验证 → 待补义务**阅读；源 ZIP 中的旧文仅在 [history/source](history/source) 作追溯。[逐文件来源解释表](research/source_crosswalk.md)把 68 个原始文件或旧代码路径逐一连接到新稿中的判断。[assets.json](research/assets.json)为机器可读的逐命题文件关系，[数学超图](research/graph.json)记录证明所需的合取前提，[旧路径表](research/path_migration.json)记录每个迁移与退出的入口。

| 命题 | 必须同时成立的条件与所获结论 | 本轮新写的数学资产 | 规范实现和实例检验 | 尚待完成 |
| --- | --- | --- | --- | --- |
| SC-PHI-E/A | **相同非空目录**、正权重、强制服务、线性实际负载成本、逐布局存在性选择独立混合精确 NE；二进制有理输入才谈位复杂度。构造一个因子 ≤φ 的证书，非实例最优。 | [完整集成主稿](history/source/manuscripts/shared_phi/main.tex)、[精确命题](research/current/shared/theorems.md)、[现行全分支证明](research/current/shared/README.md)、[算法与证书](research/current/shared/algorithm.md) | [共享构造](facility_spe/shared_phi.py)、[独立实例检查器](facility_spe/cli/verify_phi.py)、[753 实例回归及全游戏三混合 C 例](tests/test_shared_phi.py) | 全分支现行 Markdown 经内部交叉审读；独立检查器证明指定实例的达到性；无外部同行评审 |
| SC-PHI-SHARP | 上界 SC-PHI-E 与六地点下界都在**同一个共同目录、正有理数**实例类。最优普遍因子为上确界 φ。 | [全布局下界与统一有理扰动](research/current/shared/sharp_phi_lower.md)明确修正原图权重并逐项重算 | [整数输入](examples/shared/sharp_lower_rational.json)、[精确实例最优证书](evidence/certificates/shared/sharp_lower_rational.json) | 有限整数例不代替全称扰动证明；修正版尚无外部同行评审 |
| HC-2-UP/LOW/SHARP | 两个非空目录可不同；相同负载模型。四种子纯延续得 ≤2；另一六顶点**异构**族的最优因子趋于 2。下界不属于共享目录类。 | [四种子](research/current/heterogeneous/four_seed_algorithm.md)、[任意环](research/current/heterogeneous/full_catalog_cycle.md)、[下界逐格计算](research/current/heterogeneous/sharp_two_lower.md) | [异构构造](facility_spe/heterogeneous_two.py)、[回归](tests/test_heterogeneous.py)、[M=1000 输入](examples/heterogeneous/tight_two_M1000.json) | 完整环分类及优先权的外部复核 |
| HC-RHO | **同时**每跨目录地点对至多一名公共客户、至少一侧目录至多两个地点。内部证明的尖锐普遍因子 ρ。 | [严格分类、平局、短目录提升与下界全文](research/current/heterogeneous/restricted_rho.md) | [单交叠实例精确求解](facility_spe/exact/single_overlap.py)、[下界输入](examples/heterogeneous/rho_lower.json) | 当前全分支重写经过内部核对；外部审查未进行；双侧目录均任意大的范围另由 [SPARSE-RHO-ALL](research/current/heterogeneous/sparse_unbounded_rho.md) 闭合 |
| SPARSE-RHO-ALL / SPARSE-BAD-LONG / SPARSE-BAD-LONG-ALL | 两设施、双侧任意有限目录、每跨对至多一名公共客户。固定 reach 优先级的完整纯 NE 规则给出尖锐普遍因子 ρ；坏长环旧版本量化 `3/2<r<ρ`，新版本证明所有 `1≤r<ρ` 均无固定大小的精确回应闭核心。 | [全类上界与机制](research/current/heterogeneous/sparse_unbounded_rho.md)、[阈值以下长环与新版本](research/current/heterogeneous/sparse_bad_long_cycles.md) | [单交叠实例最优求解](facility_spe/exact/single_overlap.py)、[固定 `7/4` 精确长环审查](tests/audits/sparse_bad_long_cycles.py) | 新全称证明和构造经多路线内部审查；外部审稿与完整优先权调查未完成；有限审查不是全称证明 |
| CORE-LIFT / HC-MONOTONE | 核心引理需两方非负收益、各布局可独立选延续且坐标极小值可达；单调迁移需两设施、相同的客户函数作用于两边且限**纯**客户延续。 | [核心等式和逐实现符号证明](research/current/heterogeneous/core_lift_and_monotone.md) | 核心为结构证明，无独立求真极小值的快速程序；纯四种子代码仍以线性输入运行 | 真实极小值可计算性、混合 NE 保持均不由这些结论给出 |
| LOCAL-CHORD-IFF/POLY | 单个局部布局的两处可达量 U≥V>φU/2、公共重 C<V/φ，需**双侧配额**。最大原子判别控制强弦构造，可有三名以上混合者。 | [局部 NE 几何与判别](research/current/local_and_exact/local_geometry_and_chord.md)、[全分支构造与交换界](research/current/shared/local_chord_full.md) | [强弦程序](facility_spe/local/strong_chord.py)、[局部审计](tests/audits/strong_chord_iff.py) | 交换界与退化分支已在现行全文重写并经内部审读；外部复核尚未进行；局部端点最优不等于全局平方最优 |
| EXACT-KAPPA | 两设施、正有理权重、线性成本、全部独立混合精确 NE；最大合法交叠 κ。算**该实例**最优因子，时间对 κ 指数。 | [支持区间与全局最优判据](research/current/local_and_exact/exact_algorithms_and_extensions.md) | [枚举求解](facility_spe/exact/bounded_overlap.py)、[实例及证书](evidence/certificates/heterogeneous/tight_two_M1000.json) | 简短证书只验达到值，最优性需完整支持枚举推导 |
| DP-W / FPT-D / LOCAL-HARD | 固定局部布局；DP 用总重 W 的正整数公共权重；FPT 用显式列出的 d 种有理权重；困难性用二进制整数。 | [谱 DP、固定维归约和困难性](research/current/local_and_exact/exact_algorithms_and_extensions.md) | [DP 代码](facility_spe/exact/threshold_dp.py)、[有限困难性审计](tests/audits/hardness_enum.py) | DP 为伪多项式；FPT 尚未实现；局部困难性不推出普遍构造困难 |
| MITM-EXACT | 共同目录实例或一个局部布局，正有理线性负载，接受指数时间与空间。 | [半枚举的单谷目标论证](research/current/local_and_exact/exact_algorithms_and_extensions.md) | [MITM 程序](facility_spe/exact/mitm.py)、[延迟环审计](tests/test_lazy_ring.py) | 延迟剪枝没有多项式最坏界；不能自动推广到异构接口 |
| QUAD-EQ / QUAD-PHI | **恰好两设施**、强制服务、客户在两设施使用同一个严格递增二次函数。局部 NE/CE/CCE 约束与线性模型同形；φ 转移以 SC-PHI-E 成立为前提。 | [逐实现代数等式](research/current/local_and_exact/exact_algorithms_and_extensions.md) | 无新的通用求解器；沿用线性结论需先满足条件 | 任意凸成本的混合对应不成立 |
| POLY-CONT | 两领导者非负收益，布局间可独立选后续；每布局收益集为显式多项式规模有理多面体并可实现概率见证。 | [LP 形式及可实现性条件](research/current/local_and_exact/exact_algorithms_and_extensions.md) | 尚无实现 | 不等于一般非线性客户博弈的多项式算法 |

## 来源、证据、增长

- [原始手稿](history/source/manuscripts)及[旧局部证明](history/source/notes)保留可核对的原始推导；[上一轮整理稿](history/curation-2026-10-01)不再作为现行证明入口。真正失败或被后续结论替代的尝试见[历史说明](history/README.md)。
- [测试](tests)给有限实例事实，[冻结记录](evidence/runs)说明当时运行规模，[证书](evidence/certificates)验证一个实际输入。它们与普遍证明和实例最优证明分别记录。
- 新研究按[增长协议](research/GROWTH.md)进入[问题区](research/questions)或[现行分支](research/current)，以新命题 ID 更新索引和超边。任何旧材料都不能只靠重新命名取得现行证明地位。
