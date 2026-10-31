---
id: UM-ROOTED-DAG-HOME-CYCLE-BRIDGES-AUDIT-v1
kind: 审查
type_tag: 审查
title: 根树流、环正规化与有向需求桥冻结审查
status: 已整理，结构选择与主目标仍开放
summary: 逐篇复核根树需求桥、共同拥塞流证书、单位 home 环消除及任意简单有向环境扩展；保留精确恒等、参数算法、有限边界和匿名 token 的矩层限制。
source_refs:
  - source:8b3dc46ce30e0eb0977257326f98a2b395650b19:research/current/unrelated_machines/rooted_dag_congestion_flow.md
  - source:8b3dc46ce30e0eb0977257326f98a2b395650b19:research/current/unrelated_machines/rooted_dag_degree_token_bridge.md
  - source:8b3dc46ce30e0eb0977257326f98a2b395650b19:research/current/unrelated_machines/home_unit_cycle_elimination_and_directed_token_bridge.md
---

# 阅读与归类范围

本批通过 `clean show` 取得并全文读取三篇正文，随后从冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 读取相应的 `rooted_dag_congestion_review.md`、`rooted_dag_token_bridge_review.md` 和 `home_unit_cycle_and_directed_token_review.md`。三篇正文共享“结构已给定时可构造，结构选择仍是瓶颈”的主题，但对象、输入量词和失败边界不同，以下分别登记。

## 1. 有向需求树到实际不相关机的 token 桥

### 1.1 精确对象

`UM-DAG-DEGREE-TOKEN-IDENTITY-v1` 的输入是显式简单 DAG、根 (r) 入度为零、二进制非负需求 (k_v)，且 (k_v=0) 只允许在原终端。输出根树 (H) 包含 (r)，正需求点即使成为叶也要支付其需求。定义
\[
 b(H)=\min\bigl(\{1\}\cup\{\deg_H^+(v)/k_v:k_v>0\}\bigr),
 \qquad b^*=\max_H b(H).
\]
构造每台机器一枚根任务 (g)（只在 (r) 以 1 执行）；每个正需求点 (v) 有 (q_v=\min(k_v,\deg_D^+(v))) 枚互异 token，每枚在 home (v) 以 (1/k_v)，在任一原孩子以 1 执行；若 (q_v<k_v)，另放一件只可在 (v) 执行、时间 (1-q_v/k_v) 的 filler。所有正需求点的 home 总量恰为 1，零需求机没有 token。

完整双向结论是
\[
 \operatorname{OPT}(P(D,k))=2-b^*.
\]
给定任意峰值 (C<2) 的真实调度，根任务使 (C\ge1)，而每台非根机器至多接收一个时间 1 的外来 token。由根任务所在位置向外读取 token 目的地，得到真实根树；若 (s_v) 个 token 从 (v) 外送，则该机负载精确为
\[
 1+(q_v-s_v)/k_v+(1-q_v/k_v)=2-s_v/k_v.
\]
因此 (b(H)\ge2-C)。反向给定 (H)，逐点只保留至多 (min(k_v,\deg_H^+(v))) 个孩子并删除被删孩子整棵子树；保留 token 外送、其余 token/filler 留 home，即得峰值至多 (2-b(H))。根终端、正需求死端、不可达分量和任意大二进制需求都在合同内。

`UM-TARGET-IMPLIES-DAG-DEGREE-v1` 是条件推论：若一般 UM-TARGET-v1 有固定 ((2-\varepsilon)) 算法，则对每个 τ 属于
\[
 \Gamma=\{1\}\cup\{h/k_v:1\le h\le\min(k_v,\deg_D^+(v))\}
\]
把需求改为 (\lceil\tau k_v\rceil)，调用该算法并解码，便能在总位多项式时间得到 (b(H)\ge\varepsilon b^*)。候选数至多 (1+|E|)，不按需求数值展开。它不是已构造的近似算法，也没有把“条件归约”写成主目标已解。

### 1.2 浅层正面扩展与独立攻击

正文还登记 `UM-DEPTH-TWO-HALF-v1`：只对深度二、显式层状 DAG 做阈值星包装和半比例贪心，输出 (b(H)\ge b^*/2)，并给二分之三负载界。该结果应保留为局部推论，不能推广为一般 DAG 或一般 UM。

冻结审查确认 token 任务数至多 (1+|E|+|V|)，filler 只有一件，不随二进制 (k_v) 展开。独立审计实际枚举至多四顶点 DAG、需求 0/1/(d)/(d+1)/128 位大数，共 6,807 个需求实例、34,797 棵根树、374,250 个合法调度，并逐项解码 10,372 个 (C<2) 调度；另检查 18,645 个阈值。审查曾发现任意根参数未传入规范 `candidate_thresholds` 的实现缺口，后续修补为显式传 `root`，并以非零根、终端和巨大需求边界调用核对；这是实现修复记录，不改变数学量词。

## 2. 共同拥塞流与高点支撑选择

### 2.1 固定合同与流证书

`UM-DAG-CONGESTION-FLOW-v1` 接受给定简单 DAG、根、需求 (k)、候选支撑 (W)、整数 (K\ge1) 和 (W) 内非负有理边流 (f)。原合同中高点 (k\ge K) 需输出至少 (k)，非根低点守恒、低根至少输出 (K)、所有非根输入至多 (K)。拆点后把高点输入与重新供给分离，低点使用容量 1 的守恒转接，根使用一个源，终端吸收；对每个源弧做路径分解、删去过剩流，再取整数最大流。由于每个非根入度至多一，取根可达部分得到真实根树；高点的供给和接收分离是避免深度累计的关键。

令评分为 (b=k^{-1}) 的树，固定 (K\ge1/b) 即可按树边容量 (K) 贪心外送，得到该流合同的整数证书。提取器的普遍比例为
\[
 b(H)\ge 1/(2K-1),
\]
并由 (k=qK+s) 证明该常数。对每个整数 (K\ge2)，相邻层完全二部的尖锐族实现恰 (1/(2K-1))；这证明的是该证书合同的精确锐界，而非一般 UM 近二硬度。

### 2.2 激活走廊障碍与守恒区间增量

`UM-DAG-ACTIVATION-CORRIDOR-GAP-v1` 给出 (q\ge2) 的显式走廊：父点和中间点需求分别为 1、(q)，汇点需求 1，激活 LP 满足父激活上界和边容量，但任一真实根树的评分仍至多 (1/q)。障碍来自低需求汇流把边际质量相加；该 LP 不是共同拥塞证书。

正文后续另立 `UM-DAG-TRANSIT-CONGESTION-v1`，把高点改为 (k\ge2K)，守恒点扩为 (1\le k\le2K-1)，并保留 (1/(2K-1)) 保障。新增 `UM-DAG-NONUNIT-PARAMETER-EXACT-v1` 令 (h=|\{v:k_v\ge2\}|)，枚举高点子集与显式阈值集合，在 (2^h\operatorname{poly}(B_{in})) 时间精确求 (b^*)。这是参数化精确算法；当 (h) 随输入增长时仍是指数，不能改写成一般多项式算法。

审查对固定支撑、巨大二进制流、K 单调和阈值算法做了独立核验：小 DAG 1,566 个证书/596 个对象；240 个有理走廊和汇流例（含 60 个大二进制 (K)）；固定支撑 finder 5,350 个实例、最小 K 对照 1,516 次；尖锐族 (K=2\ldots18)，激活走廊 (q=2\ldots25)，给定正评分树证书构造 5,279 次，以及小图 (\kappa^*,b^*) 夹逼 396 个对象。所有这些是实现和有限边界证据，一般结论仍由流/树证明承担。

## 3. 单位 home 任务的消环和根森林正规化

### 3.1 无界峰值下的逐机不增消环

`UM-HOME-UNIT-CYCLE-ELIMINATION-v1` 的输入含 home 任务 (J) 与固定位置的 unit 任务 (U)。每个 (J) 的 home 时间 (a_j\in[0,1])，所有非 home 有限端时间恰为 1；给定完整实际调度 σ，把每个离开 home 的任务记为带任务标签的有向弧。每次找一条简单有向环，同时把环上任务退回各自 home。环点的负载变化精确为 (a_j-1\le0)，其他机器不变；每轮删除至少一条弧，至多 |J| 轮得到 DAG，保留全部任务身份和资格。该算法不要求 (C<2)，但只保证整批变换逐机不增，不保证逐任务迁移路径逐步不增。

### 3.2 (C<2) 的 unit 根森林

`UM-HOME-UNIT-ROOTED-FOREST-v1` 在给定 (C<2) 的 σ 上定义 (R) 为从每件 (U) 的实际目的地向前可达的全部机器。因为每台机器的外来 unit 数加上 U 数至多 1，(R) 内的外送弧已经是以 U 目的地为根的互不相交朝外树；把 (R) 外的 J 全部退回 home，得到
\[
 L_i(\tau_U)=
 \begin{cases}L_i(\sigma),&i\in R,\\ b_i,&i\notin R,\end{cases}
 \quad b_i=\sum_{h_j=i}a_j.
\]
若 (R) 外每机 home 预算 (b_i\le C)，则正规化后仍峰值至多 C；全局 (b_i\le1) 是足够承诺。审查特别保留了边界：没有 home 预算时 (R) 外可能增载；若 (C\ge2)，一次性把所有环弧退回 home 也可能增载，所以必须使用反复简单环算法。

### 3.3 任意简单有向环境图的 token 恒等

`UM-DIRECTED-DEGREE-TOKEN-IDENTITY-v1` 把环境从 DAG 扩至显式简单无自环有向图，允许原入根边和反馈环，但根任务自动排除根外来 token，根可达的实际外送子图仍是树。沿用每正需求点 (q_v=\min(k_v,d_v)) token 与 filler；任意 (C<2) 调度仍可由根任务所在位置读出真实根树，负载恒等式仍是
\[
 L_v=2-s_v/k_v,
\]
因此 “环境图有环” 不会改变 \(\operatorname{OPT}=2-b^*\) 的桥梁恒等。反向树构造只依赖输出本身是树，不依赖环境 DAG。该扩展必须使用新的身份，不能原位改写旧 DAG Claim。

### 3.4 匿名 token 的 M1/M2 限制

正文末尾另立 `UM-ANONYMOUS-TOKEN-M1-LIFT-M2-NONEXTENSION-v1`。删去原任务标签后，一个共同次数至多四的 functional 在 Boolean 方程、共同 M2 PSD 和组内 head 容量条件下，可以通过下降阶乘替换提升到原标签的 M1 Gram；证明按 home/head 计数分解 contrasts，所需平方项只用共同 M2 PSD。该命题只保证 M1，不保证 M2。

精确 (k=4) 的有符号 beta 例给出一个抽象共同 M2 PSD functional，但不能扩展为原身份的完整真实 law；非扩展量词是“该给定聚合 functional 无原身份扩展”，不是原调度实例不可行，也不是近二间隙或困难性。该对象必须与上面的真实 token 调度恒等分开归档。

有限审查对 home/环/token 桥枚举 26,349 个 (C<2) 合法调度，其中 23,571 个满足 home 预算并通过根森林负载重算；所有列定范围通过。它只验证实现和边界，不把匿名 functional 的非扩展升级为真实调度反例。

# 交叉结论、证据去向与未解义务

1. 根树 token 桥、共同拥塞流和 home 根森林都以“联合结构已给定”为前提；它们说明如何同时处理分叉、汇流、低需求走廊和任务身份，却没有给一般处理时间矩阵一个可多项式提取共同结构的办法。
2. `UM-DAG-NONUNIT-PARAMETER-EXACT-v1` 的 (2^h) 因子是诚实的参数复杂度边界；不能把固定小 (h) 的精确搜索包装成一般算法。
3. 激活走廊 LP、匿名 token 的 M2 非扩展和同容量森林反例分别属于不同层次：前者是边际容量不够，第二者是标签提升的矩障碍，第三者是环境环/共享端的真实负载边界。没有一条可自动升级为 UM-TARGET-v1 的 hardness。
4. 所有正文都保留根终端、正需求死端、空 U、不可达高点、巨大二进制需求和任意平局等边界；后续复用时不能只读取摘要或旧图。

本批原文副本和 manifest 保存在 `archives/unrelated-machines/tools/evidence/rooted-dag-home-cycle-20261030/`。正文只引用冻结提交与稳定身份；有限运行、实现修复和独立审查不被写成外部评审或全球新颖性。一般 UM-TARGET-v1、共同根位置选择和统一近二算法仍开放。
