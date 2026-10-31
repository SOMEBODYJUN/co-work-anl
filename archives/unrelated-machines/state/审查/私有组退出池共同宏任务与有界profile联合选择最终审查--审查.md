---
id: "unrelated-machines/private-group-exit-pool-review"
kind: "review"
type_tag: "审查"
title: "私有组退出池共同宏任务与有界 profile 联合选择最终审查"
status: "integrated-restricted-interface-with-finite-audit"
truth_status: "restricted-shared-sink-and-profile-pool-proof; general-UM-open"
review_level: "full-source-read-cross-object-and-code-audit-comparison"
scope: "shared-sink joint macro assignment §8–10, macro exits, complete pool recovery, bounded profile distortion, and finite exact audits"
summary: "完整读取 c581e93f51990fed11ad 审查记录并比较 shared-sink canonical、price-cover、Hall-flow、private-group finite audits 与单 token/PCSP 边界。限域内无存留 fatal objection：共同宏/home/exit 匹配、单汇点 cover、完整 pool profile 恢复和 one-sided FAIL 成立；一般矩阵结构提取、任意资格容量恢复、UM-TARGET 仍开放。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/private_group_exit_pool_review.md"
  - "clean:c581e93f51990fed11ad"
  - "related-source:dda3c909b1a2bdff9170:research/current/unrelated_machines/shared_sink_joint_macro_assignment.md"
  - "related-source:149e4663ac9c4fc60b45:evidence/runs/unrelated_machines/private_group_exit_pool_audit.json"
  - "related-source:844ea5c699ee6c2cce57:evidence/runs/unrelated_machines/private_group_exit_pool_independent.json"
related_objects:
  - "任意汇点价格覆盖与共同占位联合舍入最终审查--审查.md"
  - "Hall联合组流与共享汇点宏分配双源审查--审查.md"
  - "私有组退出与高阶负相关有限审计--审查.md"
  - "单token共同资格与端点成本--障碍.md"
  - "近单位PCSP蕴含与物理复制义务最终范围审查--审查.md"
  - "rawSH3真困难性流与容量切最终边界--资料.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/private-group-exit-pool-20261031/original/private_group_exit_pool_review.md"
---

# 来源身份、正文版本与审查顺序

本页处理 clean source `c581e93f51990fed11ad`，原路径为 `research/reviews/unrelated_machines/private_group_exit_pool_review.md`，冻结 blob `128c3cad74131c0da41b15f49190bac9d353763b`，源 SHA-256 `4c6c13696554ecdf6802e1df4b8f15a634988bd64823e6f2f6880d2885747ba6`，大小 5,789 B。原文已复制到 `evidence_paths`。

被审 canonical 为 `research/current/unrelated_machines/shared_sink_joint_macro_assignment.md`，最终正文 SHA-256 `8aec1196d16fccdd5dd661d1ebfebd1f1c211d256da021aa02f433304424ef2c`。本批只登记新范围 §8–10 及其依赖的 §2–5；旧 `UM-SHARED-SINK-JOINT-MACRO-v1` 身份和旧审查不被替换。

审查顺序保留证据层级：先有只看合同的 `pool_statement_review` 和独立 floor 重构，再读取冻结正文；`pool_claim_attack` 在首次工具调用已打开旧正文和新实现，因此不是完全盲审；root 后续复核双方重构、代码和精确核验。独立重构是未实现替代推导，不算生产实现；审查不是票决，也没有外部同行评议或新颖性认证。

处置为 **integrated-restricted-interface-with-finite-audit**：把宏退出、共同匹配、完整 pool profile 恢复及有限代码证据接入已有 price-cover/Hall/private-group 对象，严格保留其结构 promise 和一般 UM 开放边界。

# 1. §8 宏任务退出与共同 home/exit 匹配

## 1.1 匹配模型

左右两侧分别有 `b+h` 个点：左侧是 `b` 个真实宏任务和 `h` 个 dummy；右侧是 `h` 个 homes 和 `b` 个互异 exit positions。每个 home 的私有组选择一次；每个宏任务的真实 exit 成本只计算一次；强制私有 sink 成本在匹配外加一次。

一个宏任务允许留在某个 home，也允许退出到一个互异 exit position。宏任务→home 的边成本是该模式的实际 cover 近似成本；宏任务→exit 的边成本是其真实 sink 时间；禁止退出时没有边。dummy→home 的边成本是该 home 的空模式成本，dummy→exit 的边成本为 0。用一个全局最小成本完美匹配同时决定所有宏任务去 home/exit、空 home 和剩余 exit；不能先冻结宏任务身份再独立修微任务。

## 1.2 从真实 T 调度得到全局见证

任意 `T` 调度中，每个 home 至多容纳一个宏任务，因为有限 home 宏边严格大于 `T/2`。设 `k` 个宏任务留在 home，则：

- `b−k` 个宏任务占用 exit positions；
- `h−k` 个 dummy 配空 home；
- 其余 `k` 个 dummy 配余下 `k` 个 exit positions。

于是得到一个完整 `(b+h)×(b+h)` 匹配见证。真实调度的私有撤离集合给出各 home/macro 模式的精确 cover 成本。局部 cover 的 `(1+η)` 误差只作用在可选私有撤离成本；强制私有退出成本和宏任务真实 exit 成本不放大。全局最小匹配的成本不超过该真实见证，因此若 `OPT≤T`，算法不会因为宏退出而错误拒绝。

恢复时每个 home 恰有一个真实或空模式，所有宏任务和私有任务各执行一次，私有组不相交；超过 `(1+η)T` 的实际汇点负载才返回 FAIL。该 FAIL 是 one-sided 的，不表示成功一定达到精确 `T` 可行。

## 1.3 位复杂度和边界

模式数至多 `h(b+1)`；匹配矩阵大小 `b+h`，Hungarian/整数最小成本流需要 `O((b+h)^3)` 整数步骤，成本清分母后的位长多项式。`T=0` 时只有零 sink 边能承载宏任务；空任务、无 home、仅一个端点和零时间任务各有独立分支。宏任务数可超过 home 数，此时匹配无完美匹配并安全 FAIL。机器列表按逐台显式编码；不宣称对仅用二进制整数 `H` 加稀疏描述的更紧凑输入有相同复杂度。

# 2. §9 完整 profile pool 的有界畸变恢复

## 2.1 Profile 输入合同

显式逐台给定不交 `H∪Z`，`Z` 非空；宏任务在任意 homes 可用，所有有限 home 时间严格大于 `T/2`；每个私有任务最多有一个有限 home，指定为其唯一 home `h`。任务要么没有 pool 端点，要么在全部 `Z` 上可用；pool-enabled 任务的 work `c_j` 为非负有理。

给正有理 `a_z`、`rho≥1`、`beta≥0`、`T≥0`、`0<eta≤1`，要求所有 pool-enabled 端点同时满足

\[
a_zc_j\le p_{zj}\le\rho a_zc_j,
\qquad p_{zj}\le\beta T
\]

对全部 `z`。这是统一 profile 畸变合同；不覆盖任意资格、逐任务不完整 pool 或无界端点差。

## 2.2 虚拟单汇点与恢复

令

\[
S=\sum_{z\in Z}\frac1{a_z}>0.
\]

把每个 pool-enabled 任务的虚拟 sink 时间设为 `c_j/S`，保留 home 时间和不可用性，调用 §8 的单汇点算法。若原实例有 `T` 调度，则各 pool 机器承担的 work 满足

\[
\sum_{\sigma(j)=z}c_j\le \frac{L_z}{a_z}\le\frac{T}{a_z},
\]

故总退出 work 不超过 `TS`；原 home 模式、宏去向和私有撤离集合给出虚拟单汇点的 `T` 见证。虚拟算法 FAIL 因而蕴含原实例 `OPT>T`。

虚拟算法成功后得到真实退出集合 `E`，满足

\[
\sum_{j\in E}c_j\le(1+\eta)TS,
\]

所有 home 负载不超过 `T`。恢复时按固定任务编号，将 `E` 中任务逐件放到当前实际 pool 负载最小的机器。令

\[
A=\rho(1+\eta)T.
\]

每次放置前必有某台 pool 机器负载不超过 `A`；否则已分配任务的 work 严格大于 `(1+η)TS`，与退出 work 总量矛盾。被选机器加一件任务后负载至多 `A+βT`，之后不再改变。因此所有 pool 机器同时满足

\[
L_z\le[\rho(1+\eta)+\beta]T,
\]

home 机器保持 `L_h≤T`。关键是按**实际当前负载**选择恢复机器，不最小化 `load/a_z`；profile 上包络正是允许用 scalar work 恢复真实多 sink 负载的必要条件。

## 2.3 位复杂度和零值

`S` 与 `c_j/S` 的有理位长受输入总位长多项式控制；恢复最多 `|J||Z|` 次实际负载比较。`rho`、`T`、`a_z` 的数值大小和分母不增加循环次数，除 `1/eta` 外没有伪多项式循环。

`T=0` 时 pool 边由 `βT` 强制为零；`beta=0`、`c_j=0`、home 空组、H 为空、Z 只有一台机器、pool-only/home-only 任务均分别处理。每任务有零边时可逐件安排零边，保持 `OPT=0` 分支。

# 3. 代码、有限证据与范围

规范代码 SHA-256 为 `64879bbb4daacb4ce603606a7c40850277405f4033fce81222f1e6053113cf14`，复用旧 `shared_sink_joint_assignment.py` 的 cover/Hungarian 原语；没有把复用的同名原语写成新实现。规范审计使用 `private_group_exit_pool_audit.py`，独立实现使用 `private_group_exit_pool_independent.py`，两者均输出精确 Fraction/整数结果。

规范审计覆盖 906 个实际实例，其中 706 个 `T` 可行实例均成功；检查 174,639 份原调度，含 321 个零目标和 6 个非法合同。独立代码用原任务完整分配求 OPT、枚举宏目的地和 cover 子集，并采用不同的顺序阈值恢复 pool：`rho=1` 与 `rho=9/8` 各 700 例，分别枚举 99,518 与 123,701 份原分配，551 与 571 个 `T` 可行例均无误拒，501 个零最优实例保持 0。

这些是有限核验，不是参数空间穷尽，也不替代一般证明。有限脚本不是生产算法中的指数枚举，软件通过、两位内部审查无异议和无 standing fatal 都不能升级为一般 UM theorem。

# 4. 与全仓对象的去重和失败机制

- 与《任意汇点价格覆盖与共同占位联合舍入最终审查》：本页保留同一 price-cover/FPTAS、共同匹配、单侧 FAIL 思路，但独有宏退出与 profile 恢复；不重复 upper-column 空模式漏洞修复的全部细节。
- 与《Hall 联合组流与共享汇点宏分配双源审查》：Hall 源要求同体积共同资格和 q 槽；本页允许单汇点任意逐件资格、宏 exit，或有界 profile 的多 pool 恢复。两者都不覆盖一般输入，不能互相替换。
- 与《私有组退出与高阶负相关有限审计》：其 906/706、独立 `rho` 审计是本页有限证据的计算对象；本页新增的是审查顺序、宏退出/完整 pool 数学接口和失败边界。
- 与《单 token 共同资格与端点成本》：本页仍要求每件任务真实合法 sink 端点和 profile 上包络，不能把逐件资格压成匿名 token 或用最小 task time 替代实际 sink cost。
- 与 near-unit PCSP/raw SH3/token-label：这些来源提供抽象 source、必要 flow 或 aggregate-to-labelled 障碍，但不生成本页唯一 home/完整 pool/profile 结构；本页也不能关闭一般 source compiler。

仍开放：

- 从任意 unrelated-machines 矩阵生成唯一 home、完整 pool、宏 exit 和有界 profile；
- 任意资格下的共同容量恢复器和统一余量；
- 多 pool 无 profile 上包络时的全局匹配/舍入；
- 一般 `UM-TARGET-v1` 的近二算法、hardness、generic LP/SDP 后端和外部新颖性。

# 5. 结论

`c581e93f51990fed11ad` 在声明范围内确认了两个限域合同：

1. 允许宏任务退出时，用真实宏/home/exit/dummy 的一次共同完美匹配同时决定宏任务和私有组；局部 cover 误差只放大可选私有撤离成本，强制成本和真实 exit 成本不放大；
2. 在所有 pool-enabled 任务共享有界 profile `a_zc_j≤p_zj≤rho a_z_j`、`p_zj≤beta T` 时，可用虚拟单汇点 work、§8 共同选择和按实际当前负载恢复，得到 `L_h≤T`、`L_z≤[rho(1+eta)+beta]T`。

这两项需要显式唯一 home、完整接收池、逐件资格/profile、真实任务回溯和 one-sided FAIL 量词。有限审计支持实现回归，不能外推到一般 unrelated-machines、任意多 sink/资格、一般 LP 或 `UM-TARGET-v1`。
