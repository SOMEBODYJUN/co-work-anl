---
id: matroid-structures/retired-matroid-exchange-distance-source-review
kind: review
type_tag: 审查
title: 公共基交换有向距离候选的来源审查与应用边界
status: proof-candidate-retained; independent-reconstruction-linked; novelty-pending
truth_status: finite-audit-and-proof-candidate; no-new-theorem-claim
review_level: full-source-read-and-cross-archive-comparison
summary: 完整读取退役选题中的公共基单交换图距离笔记；其前向闭包证明候选和原子拥塞成本接口已被现有 matroid-structures 资料对象吸收，本源补充精确 provenance、纯组合量词、有限审计覆盖与应用未闭合义务，不把它升级为普遍定理或已认证 PoA 改善。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/matroid_exchange_distance_and_girth.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/matroid_exchange_distance_and_girth.md
source_id: 837d544452f9c7279f70
source_blob: e0b282733c3bed8ffb38428660fae45ceb66ed2a
source_sha256: 71f1ac0733d14111359c43d5ecbdb74326d7885403f6e310c2fc28ba09c70fcf
source_size_bytes: 6821
related_objects:
  - archives/matroid-structures/state/资料/交换距离与等长theta相关间隙的独立接口--资料.md
  - archives/weighted-congestion/state/审查/原子扰动审计与单交换局部障碍--审查.md
  - archives/weighted-congestion/state/审查/原子拥塞重选题与失败路线--审查.md
recommended_evidence_path: archives/matroid-structures/tools/evidence/retired-topic-selection-20261031/matroid_exchange_distance_and_girth.md
---

# 阅读范围与来源身份

`clean show 837d544452f9c7279f70` 导出 6821 字节 Markdown，SHA-256 为 `71f1ac0733d14111359c43d5ecbdb74326d7885403f6e310c2fc28ba09c70fcf`；`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 内容相同。源文本明确把自己标作题源、完整证明候选、独立攻击和精确审计的组合笔记，并声明不以有限实验宣布猜想解决或主张全球新颖性。

我对照读取了 `archives/matroid-structures/state/资料/交换距离与等长theta相关间隙的独立接口--资料.md`，以及 weighted-congestion 的原子扰动审计和原子拥塞候选/失败路线对象。现有 matroid 对象已承接交换距离的前向闭包、反向秩稳定和等长 theta 的另一条独立证明；原子对象已承接局部单交换反例和有限扰动证书。因而本源不应另造同一距离定理，也不能把同档共现解释成 theta 与距离之间的数学依赖。

# 纯组合合同（候选等级）

对有限拟阵 `M=(E,I)`、秩 `k`、最小回路大小 `g`，以及允许重复的非空有限基列表 `B_1,…,B_N`，定义公共基单交换有向图：`r→s` 当且仅当某个 `B_i` 含 `r`、不含 `s` 且 `B_i-r+s` 仍为基。对任意不同的可达端点，源稿提出

`dist_D(u,v) ≤ k-g+3`。

前向层证明令 `H_j={e:d(u,e)≥j}`（含不可达元素），用基本回路得到 `H_{j+1}⊆cl(B_i∩H_j)`；最短路第 `j` 条边的见证基使 `rk(H_{j+1})≤rk(H_j)-1`；末边基本回路给 `rk(H_{L-1})≥g-1`，相加后得到上界。无回路自由拟阵、loop、coloop、平行元和非连通情形均须按源中给出的退化边界处理。这是完整可行单交换图的命题，不是基图上两个基之间的距离，也不适用于任意删弧子图。

源同时给出从终点反向闭包的独立重构：若 `P(S)=S∪{r:∃s∈S,r→s}` 且 `rk(P(S))=rk(S)`，必须利用基本回路与闭包证明 `P(P(S))=P(S)`；不能把秩停止当作无条件传递。该重构支持把结论作为自足候选保存，但仍未做外部文献穷尽或新颖性认证。

# 原子拥塞应用接口及缺口

在对称无权公共基原子拥塞、非负非减延迟和真实 PNE 下，令 `c_f(e)=d_e(f_e)`、`c_f^+(e)=d_e(f_e+1)`，并假设已用资源满足 `c_f^+(e)≤z c_f(e)`。沿交换弧的单步最优性和最短路径内部点已用，源稿得到 `c_f(u)≤z^{k-g+2}c_f^+(v)`，并尝试将其接入 Hao–Michini 的交换流框架。

这一步只是条件应用合同。仍需完整重写 `z(D)`、`ρ(D)` 的定义域、零成本约定、流端点量词和原文/后续文献覆盖；还要证明在何种延迟与 `δ=k-g` 区间指数 `δ+2` 真正改善已有 PoA，而不是只做形式改写。源没有 PNE 计算算法、UM 近似算法或已经认证的普遍 PoA 定理。

# 有限审计的准确范围

源引用的独立程序枚举 `n=0,…,5` 的带标号抽象拟阵，筛完整 basis-exchange axiom，再对非空基 profile 构造 D 并逐层 BFS；统计为 498 个拟阵、28,424 个 profile、18,833 个去重图和 242,976 个可达有序端点检查，全通过。该数字是有限运行覆盖，不是证明规模、成功概率或 `n>5` 的替代。证据脚本与输出必须作为 source-specific evidence 保留，不能把有限运行写成一般存在性或文献新颖性证明。

# 处置与接续

建议源级 `integrated` 到 matroid-structures 的既有资料对象，并保留 `proof-candidate-retained; novelty-pending` 状态；新增内容是本源的精确源定位、独立反向重构/成本接口和有限审计边界的 provenance。建议保全原字节至 frontmatter 指定 evidence 路径，随后以 source ID `837d544452f9c7279f70` 登记 `integrated`。第三阶段若建边，只能使用“来源/组合推导/应用条件/有限验证”语义；不得建立已证 theorem、跨 theta 与交换距离的推导边或从有限审计推出全参数结论。
