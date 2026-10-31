---
id: "unrelated-machines/home-unit-cycle-and-joint-capacity-two-source-review"
kind: "review"
type_tag: "审查"
title: "Home-unit 消环与共同容量路线两源精读"
status: "restricted-normalization-and-route-status-read"
summary: "两份审查记录共同确认：给定实际调度可用 home-unit 环回归范式，C<2 时可保留根可达的有向森林并把非达部分送回 home；在简单有向图上 token 需求恒等式扩展到 OPT=2−b*。共同容量路线包含条件流、固定支撑拥塞提取、单汇点宏任务正面合同和多种精确障碍，但一般输入的共同选择与统一 epsilon 仍未闭合。"
source_refs:
  - "clean:ef99b325b48d311f9a45"
  - "clean:6c9920e41973e9559031"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/home_unit_cycle_and_directed_token_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/joint_capacity_route_feasibility_review.md"
---

# 来源与范围

`ef99b325b48d311f9a45`（SHA `fab1f1b04c851007577abc77950a27d76f329a0868fa2709f68994786f7bd5e6`）是 home-unit cycle、root forest 与 directed-token identity 的独立陈述/读后审查；`6c9920e41973e9559031`（SHA `8b149bbba5e56957bccff8c1b5c93813964f1d4edeb3bf2aeeb3d3de2ab6e0f7`）是对所有共同容量路线、局部正面工具和障碍的整合状态审查。两源均经 `clean show` 完整读取，原件与 manifest 位于 `archives/unrelated-machines/tools/evidence/home-unit-capacity-20261031/`，receipt 草稿位于 `cleanup/workspaces/Boss2/home-unit-capacity-receipts-20261031.json`。本页保留“给定调度/限域合同”与一般 UM-TARGET 状态的分离。

# 1. 给定实际调度的 home-unit 消环

H 型任务各有指定 home：home 时间 `a_j∈[0,1]`，其他 finite 端时间恰为 1；U 型任务所有 finite 端时间恰为1。给定合法 assignment σ，选取外送弧形成有向图。

任一简单有向环上的每件 H 同时回到 home：环点恰移出一件外来 unit、移入自己的 home，负载变化 `a_j−1≤0`；反复找环得到无环外送图，并保持每台负载不增。该操作是整体规范化，不是逐任务逐步安全路径；一次并行回环可能增载，必须采用简单环迭代。它不需要 `C<2`，输入任务标签和多重弧均可显式处理。

若 `C<2`，每点“U 数 + 外来 H 入度”≤1。令 R 为有 U 的机器、W 为从 R 可达点；W 内无环、不同 R 根不合并，故外送图是互不交的 out-forest。保留 W 内弧，其余 H 回 home：W 点负载精确保持，W 外点负载是 home 总预算 `b_i`。若只假设非达点 `b_i≤C`（而非全局），就得到完整 C 界；全局 `b_i≤1` 时 C<1 的 U 为空，亦无遗漏。预算条件与 `C<2` 不是装饰，源中给出了移除任一项的反例。

# 2. Directed-token identity 的限域扩展

把输入扩大到显式简单有向图（允许原图有环和根入边），每个正需求点 v 的需求 `k_v` 为二进制整数，零需求点为终端。根 unit `g` 强制 C≥1；正需求点 v 设 `q_v=min(k_v,d_v)` 个 token，每 token home 时间 `1/k_v`、每原 child 时间1，并以 filler 补足 home 负载1。任意 C<2 assignment 的根可达外送子图仍因 root unit/no external root token 而为树；各选中正点 v 的负载

`L_v=1+(q_v−s_v)/k_v+(1−q_v/k_v)=2−s_v/k_v`。

因此最优真实树值满足 `OPT=2−b*`，其中 `b*` 是根可达向外树中最小 `s_v/k_v`（比例截断1）；反向给树按 token 外送、其余归 home，正向由 C<2 规范化和解码。候选阈值只需枚举实际整数 child 数与显式边，规模位多项式；大二进制 `k_v` 不按数值展开。该扩展是新的 directed-simple-graph 身份，不能原位改写旧 DAG claim。

这给出深度/环边界的精确对照：深度本身不是一般 UM 难点，真正开放的是共享资源/无界需求下的共同选择和 general decoder。

# 3. 共同容量路线的真实进展

整合审查按路线区分下列可复用合同：

* 条件 probe、contracted sparse CONFIG 和指定矩重置仍是接受值/解码条件，已有相对 gap；不能当作一般反例或算法。
* 双边界菜单、固定槽、逐机跨度二、给定共同大边 H 的 ordered-slot rounding 都是正面局部工具；H 的选择、跨槽共同容量和一般支撑仍需解决。
* 固定支撑 W 的共同拥塞流可在给定证书后用一次整数流给 `b≥1/(2K−1)` 的树/调度；最小 K 与全支撑 κ* 可算，但未知输入如何选择好 W 仍是主义务。
* 单公共 sink、私有 home 任务组、宏任务每条 finite edge 严格 `>T/2` 的 shared-sink-joint-macro 合同能共同选择全部 macro，给 home≤T、sink≤(1+η)T（FAIL 可靠）；它是限域正面机制，不能扩到多 sink、多 home 身份或任意 small 任务。
* 其它候选（低秩真矩提取、固定 macro 后 tiny repair、独立菜单拼接、跨多预算整匹配）分别有 rank/selection/凸化障碍，未形成统一算法。

这些结果支持“若给共同证书可舍入、若共享耦合可压成一个可加标量则能正面求解”的路线判断；它们没有证明所有路线失败，也没有统一 `2−ε` 保证。

# 4. 障碍的精确量词

低秩真矩：若输入能计算出来自真实 `T=1` 调度、rank `O(log L)` 的 big moments，仿射空间与 Boolean 立方交集至多 `2^r` 候选，可验证实际 assignment；但在已知 half-unit NP 族上，总多项式提取器会蕴含 P=NP。存在 Dirac rank0 不表示可计算。全 tiny 的 PARTITION fixture 还说明精确补全不能免费完成。

独立宏/菜单拼接：固定各子证书后，不同共同资源的容量可能互相冲突；简单森林 DP 可精确，但多选背包/多预算全局核心仍未化为普通匹配。单 sink 的可加成本例外是已入库的正面限域合同，不是一般多 sink 结论。

固定槽与 block-cut：固定 H 的槽损失可证、专用 escape 族的 block cuts 可证，但选择 H、分离全部有效 cuts、保跨机实际容量和总位长进展仍未闭合。任何失败必须是可靠 OPT>T 证书，不能把局部 route 无改善误作全局不可行。

# 5. 有限证据和后续边界

两源关联的 route-composition 审计只在明确小参数、Fraction/整数模型、显式 DAG/仿射支撑上核验局部恒等与有限状态；它不代替一般定理，不认证作者所有代码，也不解决一般共同迁移。home-unit cycle 审计的有限枚举支持给定调度 A/B，但不是目标算法。

本对象独有去向是把“home 消环/森林恒等式”和“共同容量路线真实状态”接在同一审查中，并保留每条路线的正面工具、反例机制与未决义务。引用时必须注明：给定 assignment 的 normalization、simple directed graph token identity、fixed-support/shared-sink 限域和一般 UM-TARGET 的开放状态。不得写成一般近二算法、统一 hardness、外部新颖性或当前六人 SPE 目标的直接证明。
