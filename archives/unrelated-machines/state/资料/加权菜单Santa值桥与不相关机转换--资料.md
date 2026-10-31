---
id: "unrelated-machines/weighted-menu-santa-value-bridge"
kind: "bridge"
type_tag: "资料"
title: "加权菜单 Santa 值桥与不相关机转换"
status: "proved-with-explicit-model-boundary"
summary: "在每个 state 的 private 系数总和恰为1、每个 resource 为独立 unit machine、每个 group 只有一个 selector 且保留全部 incidence jobs 的明确模型中，Santa 最小值 V 与对应不相关机 makespan 满足 OPT_UM=2−V；给定 t 的 V≥t 与 makespan≤2−t 等价。来源只认证 canonical §1–3，不扩张到 §4–6 菜单规模、一般 Santa/UM hardness 或 degree-two 后端。"
source_refs:
  - "clean:71d9b4b2e2e41a07b8c5"
  - "clean:17da21202b0a1b39bd70"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_weighted_menu_santa_canonical_scope_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66f48:history/source/notes/unrelated_machines/normalized_weighted_menu_santa_final_scope_note.md"
---

# 对象身份与读取范围

本页处理两份同一 canonical 对象的冻结读取记录，但只认证其 `UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1`（canonical §1–3）。canonical 文件全文另含归一化 XOS 菜单规模 Claim（§4–6）；本页明确已读但不把它并入 Santa 值桥的证明。菜单规模的独立 Exact/Proof/read-after 归档在[归一化 XOS 菜单阈值规模下界](../障碍/归一化XOS菜单阈值规模下界--障碍.md)。

| clean ID | 原路径 | 源 SHA-256 | 大小 | 本轮用途 |
|---|---|---|---:|---|
| `71d9b4b2e2e41a07b8c5` | `history/source/notes/unrelated_machines/normalized_weighted_menu_santa_canonical_scope_review.md` | `af52cc08b9cf363124c4dcd82d29da6bdc5c8d88b046593e78218878bc4657d0` | 5,735 B | 完整读取 §1–6；认证 §1–3 的模型、双向转换、值身份和位复杂度边界 |
| `17da21202b0a1b39bd70` | `history/source/notes/unrelated_machines/normalized_weighted_menu_santa_final_scope_note.md` | `0f762e97ec6084e120d0c145027ea41b496b522e2316c2fb5e235e35b8be27e8` | 1,573 B | 完整读取最终 scope 延续；确认唯一变更在 §5 非本认证范围，§1–3 前缀 hash 不变 |

canonical 组合版本的数学字节 hash 在来源中记录为 `42450690b6dc42cf8a40371071a890aa14e272ef6295c7853c4f1b9bb7fdfcad`；最终 scope note 记录后续版本 hash `ce1c320ecd4d3833030307e4b4e3f4959ecd187281187c5914e80bddae8d13c5`。这两个组合 hash 是来源内部版本识别，不替代本批 clean 源 SHA。

原件导出和哈希 manifest 位于 `archives/unrelated-machines/tools/evidence/normalized-weighted-menu-santa-20261031/`。

# 精确模型

对象由有限个 nonempty groups、有限显式 indexed menu states、有限 real resources 组成。每个 group (g) 的每个 state (s) 给出非负 private 系数 (p_{g,s,u})，满足

\[
 \sum_{u}p_{g,s,u}=1.
\]

允许零项和重复 indexed states，但必须保留 state 的 indexed 身份。每个 resource 是一台独立 unit machine；每个 state 是一个独立 private machine/root；每个 group 有一个 unit selector；每个原 state-resource incidence 是一枚不同的 job。没有额外 jobs、资格约束或隐式复制；尤其同一 resource 上不同 incidence jobs 不被复制成不同 real items。所有原 incidence jobs 在反向 UM schedule 中保留。

对应 Santa 型实例含一个 state agent、每个 real resource 一个 real item，以及每个 group 的 (K_g-1) 枚不可拆单 owner dummy。dummy 对本组的全部 agents 价值一，对外组价值零。这个 dummy 数只用于表达“同组 menu states 的选择”，不是额外 real resources，也不允许将同一 resource 的多份 incidence 当成多枚 item。

令 (V\in[0,1]) 为该 Santa 实例的最优最小价值，令 (C) 为对应 UM 的 makespan。来源的精确值身份为

\[
 \operatorname{OPT}_{\mathrm{SC}}=V,
 \qquad
 \operatorname{OPT}_{\mathrm{UM}}=2-V.
 \tag{1}
\]

更强的阈值形式是：对任意给定 (t\in[0,1])，

\[
 V\ge t
 \quad\Longleftrightarrow\quad
 \operatorname{OPT}_{\mathrm{UM}}\le 2-t.
 \tag{2}
\]

来源只声称值身份和给定阈值的双向可行性，不声称输入时给出 (V)、不求解最优值，也不把这一步包装成一般 Santa 或 UM hardness。

# 双向转换与公式

## 1. 从资源 bundles 到 Santa allocation

给每个 group 一个真实 resource bundle (B_g)，先在该 bundle 上选择一个 attaining state（有限 menu 中直接取最大 clause）。其余同组 agents 各拿不同 own dummy。由于每个 state 的 private 总和恰为一，dummy 的共同值足以支持相同的目标下界。不同 group 的 real bundles 不交；dummy 为 private owner，不与 real resource 复制混淆。此构造把一份完整 resource allocation 转成 Santa allocation，并保持每 group 的 menu value。

## 2. 从 Santa allocation 到一个 state/group bundle

每组 (K_g-1) 枚 own dummies 不能覆盖该组的 (K_g) 个 agents，至少有一个 agent 没有自己的 dummy。foreign dummy 对该 agent 价值零，因此该 agent 的真实 resource bundle 在其所选 state 下至少达到 Santa 的最小价值。每个 real item 只有一个 owner，所以把这些 real items 记为 (B_g) 后，它们两两不交。此步只选一个 state/group bundle，不能把多个 state 的 bundles 拼接成一个 group 的值；(K_g=1) 时条件自动成立。

## 3. 资源 allocation 到完整 UM schedule

给定每个 group 的 bundle (B_g) 和 attaining state (s_g)，在 (s_g) 的 private root 执行该 group 的 selector。仅把 (s_g) 对 allocated positive resources 的 incidence jobs 放到对应 resource machines；该 state 的其余 jobs 留在自己的 private root；所有未选 state 的全部 incidence jobs 也留各自 private root。这样每个 selector/incidence identity 恰执行一次，零 private job 留根且不改变值。

若该 state 在 (B_g) 上的实际 value 为 (a_g=\sum_{u\in B_g}p_{g,s_g,u})，则 selected root 的负载正好是

\[
 1+\sum_{u\notin B_g}p_{g,s_g,u}=2-a_g.
 \tag{3}
\]

未选 roots 的负载为一；由于 bundles 不交，每个 resource machine 至多接收一枚 incidence，负载至多一。因此若所有 (a_g\ge t)，完整 UM schedule 的 makespan 至多 (2-t)。特别地，(V=1) 时 UM makespan 为一；(t=0) 时两边都只要求总可行性。

## 4. UM schedule 到 Santa allocation

反向取任一完整 UM schedule，makespan 记为 (C<2)。每台 resource machine 至多接收一枚 unit incidence。对每个 selector 所在 state，选取其实际导出的 resource bundle (B_g)。因该 state 的 private load 是 selector 一加未导出 incidence 的时间，恰为

\[
 a_g=2-L_{\mathrm{root},g}\ge2-C.
 \tag{4}
\]

不同 selector 的 bundles 不交，因为每个 real resource machine 至多承担一枚 incidence。故得到 Santa allocation 的最小 group value 至少 (2-C)。若 (C\ge2)，来源不再声称独占性，只把该分支视为零目标；这正是值身份中 (V=0\) 或 UM optimum 为二的退化边界。

将 (3) 的正向上界与 (4) 的反向下界合并，得到 (1) 和阈值等价 (2)。这是一份实际 schedule/assignment 的双向见证，不是仅对配置 LP 或摘要的数值关系。

# 规模、规范化与明确的限制

对给定 allocations 的扫描、全部 (n+I) 原 jobs 的回填、状态/资源/selector 的显式枚举，以及二进制有理时间的部分和均为输入长度多项式。来源明确区分 real-row 总量一与 full-row 总量 (K_g)；不能把 state-agent degree、resource degree 和 Santa 的 dummy 结构混用。未选 state jobs 不能删除，因为完整 UM schedule 必须保留全部原 incidence。

若给定一个共同阈值 (T>0) 的 Santa 缩放，值身份按同一尺度变成 (\operatorname{OPT}_{\mathrm{UM}}=2T-\operatorname{OPT}_{\mathrm{SC}})；不能因不知道 optimum 就沿用未知的归一化。若只有 (W\le1) 而非每 state 总量恰一，需要先在 augmented resources 上重新定义 (V)，不能把原 (V) 静默代入式 (1)。

来源还给出：式 (3) 方向的 YES (\le1\) 与 SC 值一、以及 NO (>2-\delta) 与 SC 值小于 \(\delta) 的严格方向；SC 值为一与二分之一的源只导出 UM 阈值一与 (3/2)，本身不提供趋二的 source。resource 的 group-degree 与 SC 的 state-agent degree 不可互换，不能免费调用 degree-two SC 后端。canonical 对外部 degree-three embedding 和其它 hardness 说法只保留为条件接口，本批没有重新读取其所链源文件的字节，故不把它们认证为本页定理。

# 两份来源的版本比较

| 内容 | 71d9 canonical scope review | 17da final scope note | 本页处置 |
|---|---|---|---|
| §1–3 模型、双向转换、OPT 身份 | 完整全文读，指定 §1–3 通过 | 确认 §1–3 prefix 未变 | 作为值桥证明范围保留 |
| §4–6 菜单规模 | 读到但明确不认证 | 唯一文字改动在 §5，且仍不在认证范围 | 转交独立菜单规模障碍页，不并入本页 |
| 版本/hash | canonical 组合 hash `42450690…dfcad` | 新版组合 hash `ce1c320…d13c5`，§1–3 prefix hash `e8f0de…e68bf6` | 仅作为 provenance，clean 源哈希另列 |
| 软件/枚举/外审 | 明确无运行 | 明确无运行 | 不把读取记录升级为实验或第三方证明 |

# 结论与接续

这是一个已按其明确模型证明的值桥：在每 state private 总量恰为一、每 resource 是独立 unit machine、每 group 一个 selector、全部 incidence jobs 保留的条件下，Santa 最小值和 UM makespan 通过 (2-V) 互换。它可为第三阶段提供一个**条件性 source interface**，但仍需另行构造真正的 SC source、验证其 degree/资源约束、证明 source 的 yes/no gap，并把任何额外 normalization 或 dummy 操作写入完整对象。

本页不声称：

- 一般 Santa Claus 或一般不相关机的 NP-hardness；
- resource degree 两级或任意 bounded-degree 的自动降阶；
- canonical §4–6 的菜单规模证明已由本页重做；
- 给定值桥足以覆盖主线近二目标或当前六人 SPE 模型。

本轮两源均完整实读，比较了定义域、量词、每一条 job 的保留、零分支、(C<2) 的严格反向阈值和版本边界；未运行软件、未生成有限实验。原件和 manifest 在 evidence 目录，本页归档为资料，不直接改写主稿。
