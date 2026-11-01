---
id: "unrelated-machines/raw-sh3-subtree-inclusion-review"
kind: "review"
type_tag: "审查"
title: "原作业SH3子树流与包含容量双源续审查"
status: "integrated-scoped-necessary-system"
truth_status: "general-conditional-flow-plus-exact-inclusion-obstruction; no-global-SH3-gap"
review_level: "full-source-read-and-audit-boundary-check"
scope: "raw degree-six common moment conditional subtree flow and binomial inclusion-capacity cut"
source_refs:
  - "source:b997f7b969b6a8dfe08e:research/current/unrelated_machines/raw_sh3_conditional_subtree_flow_and_inclusion_capacity.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/raw_sh3_conditional_subtree_flow_and_inclusion_capacity_review.md"
legacy_ids:
  - "UM-RAW-SH3-CONDITIONAL-SUBTREE-FLOW-AND-INCLUSION-CUT-v2"
---

# 1. 读取范围和稳定身份

完整读取当前 canonical 正文、相关 SH3/CONFIG/树流审查、原始 Bamas 论文的正文片段与本源链接的规范审计程序/冻结 JSON。inventory 稳定源 `b997f7b969b6a8dfe08e` 的路径为 `research/current/unrelated_machines/raw_sh3_conditional_subtree_flow_and_inclusion_capacity.md`，SHA-256 `d36fa70bfea517257af13a0054432ed0dae65e4c623f5ffa1e9acecc178ba516`，大小 19125 bytes，冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。正式身份是 `UM-RAW-SH3-CONDITIONAL-SUBTREE-FLOW-AND-INCLUSION-CUT-v2`；旧 v1 草稿不另计。

本源的结论是必要系统内的条件流和明确包含容量切，不是一个可计算的完整 SH3/SDP 解算器，也不是 `UM-TARGET-v1` 的近二 gap 或困难性。关键限制是新流不保留原共同矩，辅助子树问题不含上游 home 和其他外来 unit jobs；对指定阈值/合同的 FAIL 是 sound，但 UNKNOWN 没有可行性保证。

# 2. 合同、量词和三阶零范数支付

定义域是分层 DAG 的完整 UM：unique-home native jobs 在 home 上时间 `1/k_v`，后继 unit 端时间 1；额外 unit-only 入口只在 unit 菜单；sink 无 home。固定 `1<=T<2`，共同 degree-six 泛函 `L` 满足原 Boolean/one-hot 理想、全局 `M3` PSD、每机次数至多二的物理负载 localizer PSD，并要求每行完整 CONFIG(T) 的一阶和同机二阶与同一 L 相容。

由于 `T<2`，合法配置不能含同机两个不同 unit 端，故 `L(RR')=0`。在 M3 中 `RR'` 是零范数向量，零向量正交性把含该 pair 的次数三/四/至六乘积全部归零。由此可将 unit 流入计数、导出计数和补项的至多三项乘积视为非负平方：这里使用的是共同 M3 与 CONFIG 的交合，不是把 PSD 非对角元直接当非负。

# 3. 正质量入口的 parent-bounded 子树流

取位于机器 v 的非 home unit 入口 E，令 `p=L(E)>0`。定义 `b_u=L(E C_u)`、`y_(u,j,w)=L(E C_u x_(u,j,w))`、`S_u=sum y`。零范数和 one-hot 给出每个 job/弧的流上界、`0<=b_u<=p`；每行负载 localizer 给
\[
S_u\ge k_u(2-T)b_u.
\]
另由 `L(E x)-L(E C_u x)>=0` 得后继流守恒上界。沿 DAG 拓扑从入口活动量 `a_v=p` 开始，按比例 `f=(a_u/b_u)y`（或精确配额 `r_u a_u/S_u`）构造一个 canonical fractional subtree flow。活动量不超过 p，每行导出至少 `r_u` 倍活动量；sink 只收流，不承担导出覆盖。

该流的意义必须严格写成“从一个正质量入口推出辅助子树必要流”。它不是原共同点的矩扩展，也不免费安排上游 native job、其他 selector 或完整原实例。若明确的辅助有理 LP 不可行，可据此对指定合同输出 sound FAIL；单个入口或单个候选点被拒绝不能单独证明 `OPT>T`。一阶零端点可以按 M3 零列删除并迭代，但不得删原 job 或整个 home。

一般 `r_u=k_u(2-T)` 是实数，不能自动取 ceil；只有整数 `h_u=(T-1)k_u` 时，active home 边际落在 hypersimplex，可拆成有限个等基数 home 子集并配对 incoming 标签，仍只匹配新流一阶、不匹配原二阶或外来 jobs。`k_u=1` 且完整 CONFIG 给出额外 home/incoming pair 零矩时，走廊不衰减；仅有 incoming/incoming 零矩则不能免费推出该强化。

# 4. 包含族的共同容量切

取 `q` 为正四倍数、`m>=100q`，以 q-subset 机器 U_S、2q-subset 中间机器 B_W、q-subset 终端 Z_R 构造三层原作业；selector 在 U 上，f jobs 从 U 可去包含 S 的 B，e jobs 从 B 可去包含 R 的 Z。设置
\[
N=\binom mq,\ C=\binom{m-q}q, K=\binom{2q}q, G=\binom m{2q},
\]
并令 `d1=floor(C/(K s1))`、`d2=floor(K/s2)`。任意正质量 selector 入口必须满足
\[
\delta d_1(\delta d_2-M)\le H,
\]
其中 H 是与固定 S 交叠至少 q/4 的终端数，M 是其余终端数，`delta=2-T`。若严格违反，直接得到 sound FAIL。

证明同时有矩流和真实整数计数两条线：第一层由 row localizer 迫使至少 `delta d1 p` 的 B 流，第二层每 B 再迫使 `delta d2` 的终端流；每 B 在 H_S 外最多 M 个终端，H_S 只能接 H 个 unit jobs，故总需求超过容量。正文还显式列出 CONFIG(1) 一阶证书和完整实际调度上界，避免把一个分数行证书误写成整数最优。

二项式估计给 `H/C` 指数小、`M/K` 指数小；对固定 `a,b,delta`、`s1<=q^a,s2<=q^b`，q 足够大时左侧/C 至少多项式量级而 H/C 指数下降，因而固定任何有理 `T<2` 的此辅助系统最终 FAIL。该渐近反证是指定 SH3/CONFIG 合同的结构障碍，不能升级成 raw SH3 的 near-two gap：系统并未给出一个满足全部 global rows 的共同点，而不是仅仅由有限审计没找到。

# 5. 证据、文献范围和接续

规范程序对 120 个二项式 case 检查、85 个严格 FAIL，并重放作者原 CLI 与规范 CLI 得到相同冻结 JSON；小 `q=2,m=6` 原矩 fixture 检查 45 machines、106 jobs、750 finite entries 和 11/6 的完整路径调度。有限结果不承担一般 q/m 证明，也没有生成巨大族全部矩、枚举全部调度或调用一般 SDP。

原始 Bamas 论文只作为 graph/assignment-LP/subtree 定义和计数背景，正文明确未把全文审查或文献常数改写成当前 theorem。source 的独立审查已把作者实际读后、代码哈希和文献覆盖分开；本页保留这一证据层级。

第三阶段关系图可记录：`共同 M3 + 完整 row CONFIG` -> `正入口 parent-bounded flow` -> `指定辅助 LP sound FAIL`；以及 `包含层计数 + 共享终端容量` -> `固定 T<2 的结构切`。边上必须注明“辅助子树/指定合同”，不能连接成原 UM 的全局 decoder。

开放义务是：让子树流同时携带上游/下游所有原 jobs 的共同 owner，细分或多层路径不破坏每终端容量上界，或构造一个真正 global SH3 near-two 点。当前源没有完成这些义务，故 `UM-TARGET-v1` 仍 OPEN。

逐源处置：`b997f7b969b6a8dfe08e` 为 `integrated`；完整定义、三阶流推导、实数配额边界、包含容量切、有限审计和未闭共同 owner 义务均写入本页。
