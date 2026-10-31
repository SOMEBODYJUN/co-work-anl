---
id: retired-topic-selection/main-problem-scope-and-value-contract
kind: resource
type_tag: 资料
title: 主攻问题范围、完成价值与旧原子NE课题的关系
status: historical-research-contract-integrated; no-new-theorem
truth_status: scope-and-value-analysis-only
review_level: full-source-read-cross-archive-comparison
summary: "完整读取退役选题范围合同；准确区分BMKP、原子博弈、公平分配、Group GAP、重边EF与工具候选的模型和量词，保留主目标验收合同、完成价值与不应外推的边界。该源不增加已解决数学Claim。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/main_problem_scope_and_value.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/main_problem_scope_and_value.md
source_id: f3c595eee624f818eb87
source_blob: 3fcfb2939650115f79f43a6fbb626130dd905e46
source_sha256: 5dd729923b256f012ade99bb097b1539b430c1a1d165084df3f53e11c97397f7
source_size: 12374
related_objects:
  - archives/bottleneck-knapsack/state/资料/双容量BMKP候选的三模块与完整目标--资料.md
  - archives/weighted-congestion/state/资料/非对称拟阵纯精炼均衡候选与证明承重边界--资料.md
  - archives/fair-allocation/state/资料/可加公平与副本前缀目标的候选反例分层--资料.md
  - archives/weighted-congestion/state/资料/全类近似门槛的模型与研究验收合同--资料.md
---

# 来源身份与判断层级

`clean show f3c595eee624f818eb87` 导出的冻结文件为 12,374 字节，SHA-256 为 `5dd729923b256f012ade99bb097b1539b430c1a1d165084df3f53e11c97397f7`；`legacy-cleanup` 与 `main` 两个来源提交内容相同。它是 2026-10-20 的选题合同和价值判断，不是证明、审计或外部优先权认证。全文实际回答旧原子 NE 课题的关系、作者明确开口、自然子例和完成后的研究价值，并明确“不启动几十个团队或承诺解题时间”。因此本对象保存模型边界与研究决策，不把其中的 proposed target 当成已解决结论。

# 模型分离

旧加权原子拥塞问题要求玩家选择资源集合，费用依总权重负载变化，并同时满足每个玩家的单方偏离不等式；来源只读取仓库中已有的 `Cd/log d` 目标已被内部结果否定及线性增长阶记录，没有在本源重新审定。BMKP 是中央 max-min 背包优化：物品有公共重量/利润，每个箱有容量，求严格不超容量且不交的箱内物品，使最小利润最大化，可 unused 物品但不能通过舍弃箱子提高目标。两者只有资源分配、交换、流/匹配等工具层相邻，没有已建立的保持目标/保证的归约；不得把拥塞均衡结论自动迁移为 BMKP 算法。

同样，AP-02 属于原子博弈的非对称精炼均衡计算，不能与旧拥塞存在阈值或 BMKP 近似目标合并。公平分配、Group GAP、一般重边 EF 和拟阵候选均各自保留输入、输出、估值/容量与存在性量词；共同写“分配”不产生模型依赖。

# 来源中的主目标合同

- `SEL-BMKP-CONST-K-v1`：固定整数 `K` 和 `0<epsilon<2/3`，容量至多 `K` 种、每类箱数任意、容量比无上界，公共正有理重量/非负有理利润，要求输入位长多项式时间输出硬容量 `(2/3-epsilon)` 近似。两容量是首个自然子例，不解 `K>=3`；现有 BMKP 三模块对象仍把联合供给、全部损失、位复杂度和全算法覆盖列为未闭义务。
- `SEL-MATROID-PERFECT-ASYM-v1`：有限无权玩家各有任意拟阵、独立性 oracle，非负非减有理延迟表，不要求共同策略集、rank 或共同相对内点；输出各玩家一个基，使原 normal-form profile 为 trembling-hand perfect equilibrium。affine 延迟、共同相对内点只是有意义的子合同，不能替代一般非减延迟量词。对应候选边界已由独立对象保存。
- 公平分配主目标：四人共同 laminar 约束下的完整 EF1 与 ordered no-envy，以及任意人数/类型数的 goods-with-copies SD-EF1。K8/K12、三人 copies 和有限样本只是自然子例/证据；不能由固定表格或随机 profile 推出连续估值或任意类型数定理。
- Group GAP 越过半容量阈值：存在固定 `eta>0,rho>0`，组总尺寸至多 `(1/2+eta)m` 时保持完整组和硬容量并给多项式 `rho` 近似；利润可依 bin，不能缩成已知 GMKP 逃避原问题。该合同是研究目标候选，不是已运行算法。

来源还列出一般 multigraph EF、有限权重势/资源 LP 分类、cloning 识别和拟阵 PoA 等储备方向；它们的完整收益取决于原文开口和新义务是否闭合，不因作者身份或文件数量自动升级。

# 价值与开放边界

来源的价值判断是条件性的：完成固定 `K` BMKP 会把同容量近紧保证推进到自然多容量类别；完成一般非对称拟阵精炼均衡会填补普通 NE 与 perfect equilibrium 的组合类边界；完成四人 laminar 或任意人数 copies 会分别扩展公平分配的自然离散边界；跨过 Group GAP 半容量阈值会改变其选组/预留容量工具的已知范围。这些是研究收益说明，不是存在性、难度或新颖性证明。

本次比较确认：同仓现有 BMKP、非对称拟阵候选、公平 copies/K8、Group GAP 和拥塞资料分别保存了各自的条件与障碍；本源独有内容是把它们放在同一套“模型关系—主要开口—完整验收合同—完成价值”框架中，并明确哪些只是子例、有限实验、候选或待查文献。第三阶段最多建立“范围合同→对应候选对象”的资料/来源边，不建立跨模型 derives/refutes 边。

处置为 `integrated` 资料资源。它不启动团队、不承诺时间、不认证作者声望或外部新颖性，也不改变任何现有定理、开放问题或六人 Q-CAG-HALF 的模型与量词。
