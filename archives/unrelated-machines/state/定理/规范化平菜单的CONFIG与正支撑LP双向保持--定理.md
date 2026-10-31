---
id: "unrelated-machines/normalized-flat-config-fslp-sc-path"
kind: "theorem"
type_tag: "定理"
title: "规范化平菜单的 CONFIG(1) 与正支撑 FSLP 双向保持"
status: "known-with-internal-review"
summary: "在有限非空、每状态总值为一的规范化平菜单上，正支撑FSLP、受限平坦不相关机CONFIG(1)、树/端口路径变换及状态dummy SC像之间有显式双向证书变换；SC路径在旧值/旧阈值不超过一时保持实际值与最高有限CONFIG阈值。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_menu_full_support_lp_preservation_exact_only_review_v1.md#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_menu_full_support_lp_preservation_exact_only_review_v3.md#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_menu_full_support_lp_preservation_author_read_after_v1_v3.md#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_menu_configuration_certificate_preservation_canonical_scope_review_v3.md#全文"
legacy_ids:
  - "normalized-menu-full-support-LP-v1/v3"
  - "row3-degree9-SC-path"
---

# 规范化平菜单的 CONFIG(1) 与正支撑 FSLP 双向保持

## 对象、全部条件与精确陈述

输入是有限非空的规范化平菜单。每个 group 有非空、带索引的 states；每个 state 的非负二进制有理权重总和恰为 (1)，同一 state 内资源标签互异。允许零私有时间、零资源关联、未使用资源以及内容相同但索引不同的 states；索引身份不能合并。对 state (s) 只取其正私有支撑
\[
P_{gs}=\{u:p_{gsu}>0\};
\]
FSLP 的容量系数是 (0/1) 的正支撑成员关系，而不是 (p_{gsu})，也不把语法上出现但权重为零的关联计入容量。

**正支撑 FSLP。** 令 (λ_{gs}≥0)、(Σ_sλ_{gs}=1)，并要求每个资源 (u) 上 (Σ_{g,s:u∈ P_{gs}}λ_{gs}≤1)。在该明示域内，FSLP 可行当且仅当受限平坦不相关机实例存在完整有限的 machine-CONFIG(1) 证书（每机配置概率和为一、每个原 job 覆盖至少一）；也当且仅当相应 state-dummy SC 像存在 SC-CONFIG(1) 证书。上述等价是阈值一、完整原 job 身份和该结构化域内的结论，不是一般 UM 或任意阈值的 CONFIG 定理。

后续 tree、port-path 与 state-dummy 变换均保持正支撑 FSLP。先做规范化 (N)，再做 state-dummy (D)，可得每个 state-agent 的正行总值至多 (3)、每个实资源项目的正度至多 (9)；再做 SC 路径 (P_{SC})，旧项目被按 owner 重标并加入 unit helper，旧值或旧最高有限 CONFIG 阈值不超过一时可双向保持，最终新 helper 行值为 (2)、项目正度至多 (3)。

## 推导、证据与未完成部分

### 1. 平坦不相关机与 FSLP 的双向证书

设 (J_g) 是 group selector，(M_{gs}) 是 state 的私有机，(I_{gsu}) 是关联 job；正关联在私有端的处理时间为正，在其命名资源端为 (1)，零私有关联仍是实际 job。由 FSLP 给出 (λ_{gs}) 时，在 (M_{gs}) 以概率 (λ_{gs}) 选择 selector 加全部零私有关联（负载恰为一），以概率 (1-λ_{gs}) 选择全部 (I_{gsu})（负载仍为一）；正关联 (I_{gsu}) 在资源机上以概率 (λ_{gs}) 取其单位 singleton，剩余概率给空配置。这样 selector、所有原 state job（含未选 state 与零私有项）都被精确覆盖一，且资源容量恰由 FSLP 控制。

反向给任意完整有限 CONFIG(1) 证书。令 (α_{gs}) 为 (M_{gs}) 上含 (J_g) 的边缘概率；selector 覆盖给出 (A_g=Σ_sα_{gs}≥1)。若 (I_{gsu}) 为正私有关联，则其与 unit selector 不能同机共存，故私有覆盖 (β_{gsu}≤1-α_{gs})，而该 job 的唯一另一端资源覆盖至少 (α_{gs})。资源机上的所有原关联（包括零私有项）负载均为一，配置至多含一个，求和得 (Σ_{g,s:u∈ P_{gs}}α_{gs}≤1)。令 (λ_{gs}=α_{gs}/A_g) 即得 FSLP；只会降低资源使用。若输入证书仅给覆盖至少一，可逐 job 剪掉多余 job，并在必要时拆分一次配置权重以保持概率总和，得到有限精确覆盖证书，支持增量按 job 数多项式增长。

该证明承重于 unit selector、unit resource endpoint、state 私有总值一及 job 的两端结构；不外推到一般 UM、任意阈值、实际最优值或未知指数配置表。

### 2. Tree 与 port-path 变换

Tree 正向沿 source state 概率走 root-to-leaf；沿路径用 child-own singleton，叶用原 state，其余节点用 own singleton。每个新 own resource 恰被一次占用，原正资源边缘使用不增。反向允许目标树有多条活路径或 off-path 激活：非根节点记 parent 流 (q_v)、own 质量 (o_v)，own 资源容量给 (q_v+o_v≤1)，因此非 own 分支质量至少 (q_v)。根发送一单位质量，逐层归纳得到叶原 state 质量总和 (W_g≥1)。用 (λ_s=w_s/W_g) 归一化不会增加原资源负载；(K=1) 单叶边界直接成立。

Port-path 对资源 (u) 按全部语法 membership 列出 (d) 个 incident groups，但 (a_j) 只计正支撑状态概率。正向选 hole 分布 (h_j≥ a_j,sum h_j=1)，helper (r) 在 hole 左侧取左 port、右侧取右 port，使每个 port 的 helper 使用为 (1-h_j)。反向把每个 port 合回原资源；(d-1) helpers 各有正 singleton 总质量一，故
\[
Σ_j a_j+(d-1)≤ d,
\]
得到原容量 (sum_j a_j≤1)。(d=0) 为真正未使用资源、(d=1) 无 helper、全零 membership 和 indexed duplicate 均单独保留。

### 3. State-dummy SC 桥

固定 group 有 (K) 个 normalized states。SC 像有 (K) 名 state-agent、原 real 项和 (K-1) 枚只对本组 agents 价值一的 dummy。FSLP 正向令 agent (s) 以 (λ_s) 取其全部正 real support，其余概率均匀分到 dummy singleton；(K=1) 不做除零。反向先删 agent 对其为零价值的 items；达到阈值一且不含本组 dummy 的配置必须含完整正 real support，含 dummy 的配置可剪为一个 dummy。令 (w_s) 为前一类配置质量，则 dummy 容量给 (Σ_s(1-w_s)≤ K-1)，从而 (Σ_s w_s≥1)，再按组归一化得到 FSLP。若目标阈值 (τ>1)，每名 agent 的配置都必须含本组 dummy，所需边缘至少 (K) 而容量只有 (K-1)，故最高阈值恰为一（在 FSLP 可行时）。

实际 SC 值的桥是独立的整数论证：每组至多 (K-1) 名 agent 能拿 dummy，至少一名 agent 只拿 real support；反向给选中 agent 原 bundle、其余 agents 各一枚 dummy。当旧值 (V≤1) 时两边相等，包括 (V=0)。这一步不把 fractional CONFIG 证明冒称为实际 allocation，也不删原 UM 零 job。

### 4. SC unit-helper 路径

对任意非空 old agents、有限（可空）items、非负有理估值，资源 (u) 的正 owner 按顺序为 (i_1,\ldots,i_d)。复制 (u) 为 (z_{u,1},\ldots,z_{u,d})：只有 (i_j) 对自己的 copy 保持旧正值，其余 old agents 对该 copy 价值为零；每个 helper (r) 只对相邻 copies (z_{u,r},z_{u,r+1}) 价值一。

实际正向只在 (0<v≤1) 使用：对每个 (u) 选一个 hole，old owner 取自己的 copy，helpers 取 hole 之外的相邻 copy，所得 helper 值一。反向对任意 (v>0)，每个 helper 至少取一个正 copy（可同时取两个），(d-1) helpers 至少占用 (d-1) 个不同 copies，故 old agents 合计至多占一份；按 owner 合并回原 item 不冲突且保留 old utility。于是当 oldOPT≤1 时实际 optimum 保持；oldOPT>1 不作保持断言，oldOPT=0 用空配置/正阈值反证单列处理。

有限 CONFIG 的正向仅需 (0<t≤1)：把 old agent 的 item 重标到自己的 copy，按 old item 边缘 (a_j) 选 hole，并给 helper 两个 singleton 配置实现 prefix/tail 概率。反向对任何 (t>0)，helper 配置可能含两个 copies，仍至少消耗一个；求和 copy 容量后 old marginal 总和不超过一，再合并回原 item。不能在 (t>1) 时错误地把 helper 强行剪成 singleton。若 old 最高阈值≤1，则有限实例的阈值可达性给出最高阈值相等；阈值零另用空配置处理。

### 5. 自足的 (Q_D) 障碍与规模

对 (D≥2)，main group 的每个 state 含 (D) 个值 (1/D) 的 (g_{a,j})，另有 (D^2) 个 helper groups，每个只含 (g_{a,j}) 或 (A_a) 两个 unit singleton。任何正质量的 main bundle 在同一行取 (r) 个 (g) 会迫使 (r) 个对应 helper 共享唯一 (A_a)，故 (r≤1)，实际值 (V=1/D)；取一个 (g)、对应 helper 取 (A_a)、其余 helper 各取自己的 (g) 达到等号。FSLP 证书为 main states 各 (1/D)，每 helper 以 (1-1/D) 取 (g)、以 (1/D) 取 (A_a)，所有 (g,A) 容量恰一。

经 (N,D,P_{SC}) 后，SC CONFIG 最高值为一、实际值为 (1/D)，row total≤3、最终项目正度≤3（中间 state-dummy 像≤9），正值只有 (1) 和 (1/D)。对应平坦 UM 的 machine CONFIG(1) 可行，实际 makespan 的既有 value bridge 给 (2-1/D)。规模为 groups (D^2+1)、states (2D^2+D)、incidences (3D^2)、resources (D^2+D)，所有转换和显式有理证书大小按 (D) 多项式；不能把显式 (D^2) 家族说成 poly(log D)。

## 用途、与先有工作的关系和接续

本对象给出一个可复用的有限证书接口：当后续研究需要把 normalized menu 的 FSLP、受限 UM CONFIG(1) 或 SC 的有限 CONFIG 证书互转时，可直接引用上述转换，同时保留 zero、empty、duplicate、d=0/1、(K=1) 边界。它提供 bounded-row、正支撑和 unit-threshold 条件下的 CONFIG 障碍，但不能推出一般 UM 的任意阈值 CONFIG、真实 OPT≥1 promise 下的常数算法不存在，也不能把 (Q_D)（其实际值低于一）当作 near-two 或 NP-hardness 结果。实际 optimum 的 old-OPT≤1 前提与 fractional CONFIG 的任意有限证书前提必须在引用处显式写出。

本次直接阅读的是四份冻结的 v1/v3 Exact、author read-after 与 final canonical scope 审查记录；其中所述 canonical Exact/Proof 的外部 scratch 路径未作为当前源文件再次读取，因此本正文只采用冻结记录中已经展开的数学内容，不冒称另行核验未提供的原始 canonical 文件。未运行代码或有限枚举；“VALID/no fatal”是记录中的内部审查结论，不是外部同行评审或全局原创性认证。
