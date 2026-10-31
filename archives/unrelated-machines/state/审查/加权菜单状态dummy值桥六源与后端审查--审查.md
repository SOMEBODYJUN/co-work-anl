---
id: "unrelated-machines/weighted-menu-state-dummy-bridge-six-source-backend-audit"
kind: "review"
type_tag: "审查"
title: "加权菜单 state-dummy 值桥六源与后端审查"
status: "integrated"
truth_status: "exact-bridge-with-explicit-domain; finite-backend-audit-passed; no-general-hardness"
review_level: "full-read-comparison-plus-runnable-finite-audit"
summary: "六份 weighted_menu 冻结源给出同一归一化 state-dummy Santa 值桥及其独立审查；两份压缩程序提供显式 degree-two、W≤1 后端和有限夹具审计。值桥确认 OPT_SC=V、OPT_UM=2−V 及给定阈值的双向解码，但不扩张为一般 Santa/UM 硬度或 degree-two 后端。"
source_refs:
  - "clean:66c02ab103dfc9b7ba29"
  - "clean:8629950ab119d7e0bef2"
  - "clean:6db603641caeca5e5460"
  - "clean:76b7fd4a1ca40900f16c"
  - "clean:ef3264a3be9018961b2b"
  - "clean:f6caeecc72965c8e8dcf"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/weighted_menu_initial_audit_degree_two_weighted_menu_backend.py.gz#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/weighted_menu_initial_degree_two_weighted_menu_backend.py.gz#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/weighted_menu_state_dummy_sc_value_bridge_exact.md#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/weighted_menu_state_dummy_sc_value_bridge_independent_review.md#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/weighted_menu_state_dummy_sc_value_bridge_proof.md#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/weighted_menu_state_dummy_sc_value_bridge_proof_read_after_review.md#全文"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/weighted_menu_initial_audit_degree_two_weighted_menu_backend.py.gz#全文"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/weighted_menu_initial_degree_two_weighted_menu_backend.py.gz#全文"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/weighted_menu_state_dummy_sc_value_bridge_exact.md#全文"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/weighted_menu_state_dummy_sc_value_bridge_independent_review.md#全文"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/weighted_menu_state_dummy_sc_value_bridge_proof.md#全文"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/weighted_menu_state_dummy_sc_value_bridge_proof_read_after_review.md#全文"
related_objects:
  - "../资料/加权菜单Santa值桥与不相关机转换--资料.md"
  - "../定理/规范化菜单的三态资源度三正规形--定理.md"
  - "../../tools/evidence/weighted-menu-state-dummy-backend-20261031/README.md"
---

# 1. 来源身份与实际读取范围

本批六份冻结源分成两类，不能把它们计作六个定理。

| clean ID | 冻结内容 | SHA-256 | 本批独有内容 |
|---|---|---|---|
| `8629950ab119d7e0bef2` | `weighted_menu_initial_degree_two_weighted_menu_backend.py.gz` | `ae6706b743df06202e7b3799013eadb68df77931c244f122125a7d81300ec69d` | 显式 degree-two weighted-menu 后端；精确有理输入、forced-largest 与两匹配着色阈值过程 |
| `66c02ab103dfc9b7ba29` | `weighted_menu_initial_audit_degree_two_weighted_menu_backend.py.gz` | `c57f8cda7c13432942fea54c60c8584f37cfe2dff76f3f88700ae7023a11329e` | 五个 weighted-menu 夹具、七个原始后端夹具、非法输入拒绝与 1200-agent 非递归探针 |
| `6db603641caeca5e5460` | `weighted_menu_state_dummy_sc_value_bridge_exact.md` | `1a4de6d19c3f038685e822d471f0d3f388e6fb23bae780aec96e4802147b8a15` | 归一化值桥的完整定义、双向 assignment 转换、复杂度与 gap 责任边界 |
| `76b7fd4a1ca40900f16c` | `weighted_menu_state_dummy_sc_value_bridge_independent_review.md` | `ae57bf15737c54e6aadf8732869c242622ad75110facc2dbaed5fb8f7549320b` | 未读作者 Proof 的 Exact-first 独立量词与 pigeonhole/边界重构 |
| `ef3264a3be9018961b2b` | `weighted_menu_state_dummy_sc_value_bridge_proof.md` | `5decc348be346acd663478d1c13a768d0e7d06c407abacf593fc09018ff34665` | 作者逐步 Proof：值等式、完整原 jobs 回填、`C<2` 逆向、复杂度与 gap 转换 |
| `f6caeecc72965c8e8dcf` | `weighted_menu_state_dummy_sc_value_bridge_proof_read_after_review.md` | `5decc348be346acd663478d1c13a768d0e7d06c407abacf593fc09018ff34665` | Proof read-after；逐节比较并确认没有删 jobs、分割 dummy、错误 degree 外推或 `C=2` 偷换 |

`ef3264...` 与 `f6ca...` 指向相同 Proof 字节；后者是读取顺序和范围的独立记录，不是第二份 Proof。两份程序和解压副本、夹具输出及运行结果保存在 [backend evidence](../../tools/evidence/weighted-menu-state-dummy-backend-20261031/README.md)。

六个路径在冻结清单中同时出现在 `legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`；本批按内容 SHA 去重，未把同字节双快照计为新的数学对象。

# 2. 归一化值桥的稳定数学对象

设有限非空 group 集为 (G)，每个 group (g) 有显式非空 indexed states (A_g)，每个 state 在显式资源宇宙 (U) 上给出互异资源的非负二进制有理权 (p_{gsu})，并满足

\[
\sum_{u\in S_{gs}}p_{gsu}=1.
\]

允许零时间 incidence、重复但带不同索引的 states 和未使用资源；不允许在 state 内重复同一 resource。原 UM 具有：每个 state 一台 private machine；每个 resource 一台 unit resource machine；每组一个耗时一的 selector；每个 state-resource incidence 是一枚独立原 job，在 private 端耗时 (p_{gsu})，在 resource 端耗时一；全部原 jobs（含未选 state 和零时间 job）必须保留。

令

\[
a_{gs}(B)=\sum_{u\in B}p_{gsu},\qquad
f_g(B)=\max_{s\in A_g}a_{gs}(B),
\]

并令 (V) 为对两两不交的资源束 (B_g\subseteq U) 最大化 \(\min_g f_g(B_g)) 的值。构造 Santa 实例：每个 state 一个 agent，每个 resource 一个 real item；每组增加 (K_g-1) 个不可拆、单 owner 的 own dummy，每个 dummy 对本组全部 state agents 价值一、对外组价值零；real item 对 state agent 的价值为同一 (p_{gsu})。

Exact、独立 Exact-first review、作者 Proof 和 Proof read-after 一致确认

\[
\operatorname{OPT}_{SC}=V,\qquad
\operatorname{OPT}_{UM}=2-V,
\tag{1}
\]

且对任何给定 (t\in[0,1])，Santa 存在最小效用至少 (t) 的 allocation，当且仅当 UM 存在完整实际调度使峰值不超过 (2-t)。这是一条给定 assignment/schedule 的可逆转换，不是求 (V) 或求最优 UM 的算法。

# 3. 值桥的承重步骤与边界

## 3.1 资源束到 Santa

给每个 group 两两不交的 (B_g)，在菜单中选达到 (f_g(B_g)) 的 state；该 state agent 得到 (B_g) 的 real items，其余 (K_g-1) 个 state agents 各得一个不同 own dummy。由于每个 state 的 real 总价值恰为一且 (f_g(B_g)\le1)，Santa 最小效用至少为 \(\min_g f_g(B_g)\)。这给出 \(\operatorname{OPT}_{SC}\ge V\)。

## 3.2 Santa 到每组一个 state

任一合法 Santa allocation 中，每组只有 (K_g-1) 枚 own dummy，却有 (K_g) 个本组 agents；至少有一个 agent 没有 own dummy。它从外组 dummy 得零值，全部正效用来自自己实际获得的 real items (B_g)，故 (a_{gs}(B_g)\ge t)。不同组选择的 real bundles 两两不交，因为每个 real item 只有一个 owner；所以 (V\ge t)。这一步禁止把同组多个 state agents 的 real bundles 拼接。(K_g=1)、dummy 被浪费/外送/集中分配以及零值 real items 均已覆盖；若把 item 允许共享，pigeonhole 论证会失效。

## 3.3 Santa 到完整 UM

对 3.2 的 (s(g),B_g)，将 selector 放在 (s(g)) 的 private machine；仅把该 state 中属于 (B_g) 的 incidence jobs 外送到各自 resource machine；所有其它原 jobs（特别是所有未选 state jobs）留在其原 private machine。selected private load 为

\[
1+\sum_{u\notin B_g}p_{gsu}=2-a_{gs}(B_g),
\]

resource load 至多一，未选 private load 为一，因此若 (a_{gs}(B_g)\ge t)，得到峰值至多 (2-t)。每个原 job 恰分配一次，零 private job 可留 private 而不改变质量。

## 3.4 完整 UM 到 Santa 与严格 (C<2)

对任一实际峰值 (C<2) 的完整 UM schedule，取每组 selector 的实际 state。该 state 的 incidence job 只有 private 端或相应 resource 端；因为每个 resource 上的外送 incidence 都耗时一，严格 (C<2) 保证每台 resource 至多接一枚。取实际外送资源束 (B_g)，则

\[
a_{gs}(B_g)=2-L_{\mathrm{private},g}\ge2-C,
\]

且各 (B_g) 两两不交，得到 Santa allocation 的最小效用至少 (2-C)。当 (C\ge2) 时不使用资源唯一性，目标退化为零；这正确保留了 (V=0)、(\operatorname{OPT}_{UM}=2) 和峰值二端点。与正向上界合并即得 (1)。

## 3.5 复杂度与不外推

对象大小按显式 states、resources、incidences 和二进制有理值计；Santa 有 (S=\sum_gK_g) 个 agents、(|U|) 个 real items 和 (S-|G|) 个 dummies。dummy-incidence 数为

\[
\sum_g K_g(K_g-1)\le S^2,
\]

且所有 assignment 转换只扫描显式 allocations、菜单与原 jobs。real item 的 Santa agent degree 可随同组 state 数增长；原 resource 的 group-degree 不能直接变成 Santa agent-degree 二。故该值桥不授权调用 degree-two Santa 算法，也没有一般 Santa/UM hardness 或 near-two source gap 结论。若只给 (W_{gs}\le1) 而非恰等一，必须先在增广 bonus-resource 系统上重定义 (V)，不能把未增广的 (V) 静默代入 (1)。

# 4. 两份程序的有限后端与实际运行

`degree_two_weighted_menu_backend.py` 仅实现显式 resource 出现于至多两个 distinct groups 的后端。它拒绝空 groups、state 私有总量大于一、state 内重复 incidence、负或非精确浮点时间，以及科学记数法缩写；以整数 scale 表示有理端点。阈值过程先做 forced-largest 剪枝，再在两张 matching 的偶图上迭代 BFS 二染色；核心路径不调用最优值 oracle、穷举、LP、递归 DFS 或外部 solver。

`degree_two_weighted_menu_backend_audit.py` 的实际运行结果保存在 evidence JSON，逐项如下：

- 五个完整 weighted-menu 夹具均通过端到端 `parse → solve → verify`，并与独立原作业枚举及 bonus-normalized 枚举相等；枚举规模分别为 32、16、12/192、768/24576、4 个 assignment。其原始最优峰值依次为 (1,33/17,1,1,2)，其中 `V=0` 夹具准确落在峰值二端点。
- 六个原始后端夹具均满足返回值不低于最优值的一半；其中 rational、zero-opt、无正 item 及强制非对称项覆盖有理和退化边界；1200-agent alternating cycle 以迭代过程完成，无递归栈依赖。
- 六类非法输入全部被拒绝：空 group 域外、即使权为零也出现第三组的资源、私有和超过一、state 内重复资源、不精确浮点和指数简写。

这些是有限实现和输入边界证据，不能把夹具通过升级为对所有 weighted-menu 或一般 UM 的证明。backend 的 W≤1/bonus normalization 也不改变值桥本身的严格域：值桥定理需要每个 state 总质量恰为一，若使用 bonus 归一化必须把新增资源纳入新的 (V)。

# 5. 与既有正文的关系与接续

本批六源补足既有 [加权菜单 Santa 值桥与不相关机转换](../资料/加权菜单Santa值桥与不相关机转换--资料.md) 的 provenance 和独立核验；没有另立第二个同名定理。既有资料正文已经保存了 canonical §1–3 的模型、公式和限制，本页新增：

1. `6db` Exact、`76b` Exact-first、`ef3` Proof、`f6c` Proof read-after 的逐源版本边界和重复字节关系；
2. 两份压缩程序的 source hash、解压副本、可复运行夹具和实际输出；
3. 对度二后端与全无度值桥之间不可互换的明确警告。

第三阶段可把本页作为 `checks`/`supports` 证据连接至稳定对象 `UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1`，并与 `UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2` 的 bonus normalization 形成条件关系；不能把有限后端、五个夹具或 Santa source gap 当成六人 SPE 覆盖目标的证明。

# 6. 处置

六个 source 均为 `integrated`：两份程序归 evidence，Exact/Proof/独立审查归本页审查并链接既有值桥资料。`ef3264...` 与 `f6ca...` 内容相同但阅读阶段不同，保留二者的 provenance 而不重复计定理。数学状态为“显式归一化域内值桥已核验；degree-two 后端有限夹具已通过；一般硬度、近二 gap、六人 SPE 目标仍未由本批解决”。
