---
id: "unrelated-machines/signed-port-downset-and-single-home-cascade-review"
kind: "review"
type_tag: "审查"
title: "单端口向下闭集与单home级联双源审查"
status: "finite-exact-evidence-integrated"
truth_status: "two self-contained restricted-interface statements retained; no general UM hardness or universal construction inferred"
review_level: "full-json-read-current-proof-code-and-sharp-boundary-comparison"
scope: "one-internal-endpoint signed-port projection and single-home cascade query separation"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/signed_one_job_port_downset_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/signed_one_job_port_downset_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/single_home_cascade_query_patterns_v2.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/single_home_cascade_query_patterns_v2.json"
---

# 读取范围和对象边界

本审查逐项读取两个冻结 JSON、对应规范/独立程序、当前数学正文及既有 review。稳定 ID 和文件 SHA 为 `34738e052f61cf677039`（`signed_one_job_port_downset_audit.json`，SHA `5ed5290a52eed67dc4907bd132113a40e78c86658fb2e6b76b54e6925cb72320`）与 `d34fcd209fe4567c1e65`（`single_home_cascade_query_patterns_v2.json`，SHA `846ec8efc0e0b3ea2f92e71a548ea4b62aaef60f40c2d74ed2ef8cd001dcf286`）。legacy-cleanup 与 main 绑定同一路径版本，不计成两次实验。

## 1. 单内部端口投影是向下闭集

第一个对象含非空有限内部机器集 (I)、辅助任务 (J) 和 (k) 枚真实端口任务。每个端口任务只有一个内部端点 (i_j)，有理非负时间 (w_j)，另有固定外部端点；符号 (s_j\in\{0,1\}) 指定哪一位使任务进入内部。给定阈值 (T)，外部容量、外部已有任务和外部联合约束全部排除在投影之外。关系 (R_T) 由存在辅助任务实际内部调度 (sigma) 且每台内部机器满足
\[
\sum_{h\in J:\sigma(h)=i}p_{ih}+\sum_{j:i_j=i}w_j\mathbf1[x_j=s_j]\le T
\]
定义。

若 (x\in R_T)，把任意入向端口改派外部只删除非负项，原辅助调度仍可用，因此入向支持集 (D_T=\{y(x):x\in R_T\}) 是布尔格向下闭集。若 (0^k,1^k\in R_T)，令 (a_0=|\{j:s_j=0\}|)，则
\[
|R_T|\ge2^{a_0}+2^{k-a_0}-1
\ge2^{\lfloor k/2\rfloor}+2^{\lceil k/2\rceil}-1.
\]
更细地，若 (z) 个端口为零时间，正时间端口两符号数为 (a,b)，则
\[
|R_T|\ge2^z(2^a+2^b-1),
\]
且每个 (T>0,a,b,z) 的参数组都有达到例：两台内部机器各承载一个 (T)-时长辅助任务，端口时间分别按 (T/a,T/b) 分摊。正位关系正好是
\((\{0\}^a\times\{0,1\}^b)\cup(\{0,1\}^a\times\{0\}^b))，再自由补入零时间位。

当 (T=0) 且两一致态可行时，所有端口时间必须为零，关系为整个立方体。(k\ge2) 时，从任一一致见证翻转一个入向位即可得到混合态；但 (k=0) 或 (k=1) 不产生该混合结论。于是本接口不能实现“严格端只接受两个等值状态、弱端仍只接受这两个状态”的复制合同；任何 (
ho\ge1) 的放松关系 (R_T\subseteq R_{\rho T}) 都继承这项边界。

这是真实任务身份和内部容量的精确接口障碍，适用于任意辅助图拓扑和任意多个内部端口；它没有排除多任务一致性码、外部联合容量、源约束与一致性共置或只要求可解码而非等值的编码。

### 证据和控制样例

规范审计 `UM-SIGNED-ONE-JOB-PORT-DOWNSET-v1` 使用 Fraction，seed 1729，630 个 random instances、140 个 both-uniform、44 个 mixed witnesses；注册锐例含 64 个 sharp fixtures、7 个 zero-bound cases、521 位分母的巨大有理端口和若干内部双端 negative controls。独立程序另有 450 个 random internal instances、176 个 two-full-state cases、250 个 uniform matching cases、66 个 sharp signed counts、165 个 zero refinements，以及 PCSP 参数替换检查。两份 scope 都明确是有限 actual-assignment/internal-capacity audit，不是普遍定理或 hardness 证明。

尤其要保留两个负控制：当任务两个端点都在内部且没有 external occurrence slot 时，内部投影不必服从单端口 downset；当外部联合容量加回时，原本三个 projected profiles 中可能只剩两个。因此单端口、外部容量排除是定理的承重假设。

## 2. 单home级联：任务身份保留的查询支持分解

第二个对象 `UM-SINGLE-HOME-CASCADE-QUERY-SEPARATION-v2` 在同一显式 unrelated-machines 矩阵上输入两份完整实际调度 (sigma_0,sigma_1)，峰值均不超过 1。任务分为：全部有限端时间为 1、端数不限的 unit 任务 (U)；每个只有唯一正小端 (h(j))、时间 (a_j\in(0,1))，其余有限端只能为 0 或 1 的小端任务 (J)。(sigma_0) 把全部 (J) 留在 home，给定非空 query 集 (Q\subseteq J)，(sigma_1) 把全部 (Q) 放到 unit 端。设 (D) 为 (sigma_1) 中落在 unit 端的任务、(Z) 为落在零端的任务；只在 (D\setminus Q) 上给固定非负权 (w_j)。

机器弧图删去 query 弧后，每个 query 的 unit 目标是零入度根；入度至多 1，根的前向可达域 (R_q) 两两不交。令
\[
A_q=\{d\in D\setminus Q:h(d)\in R_q\},
\]
则 (A_q) 两两不交。对任意 (S\subseteq Q)，只把 (S\cup A(S)) 送到其 (sigma_1) unit 端，(Z) 固定到 (sigma_1) 零端，其余小端留在 home，unit 任务按两份见证原端重排，可构造完整调度 (	au_S) 满足
\[
C_{\max}(\tau_S)\le1+\delta(S),
\qquad
\delta(S)=\max_i\sum_{q\in Q\setminus S:h(q)=i}a_q.
\]
给 (c_q=\sum_{j\in A_q}w_j)，有
\[
\operatorname{fee}(\tau_S)=\sum_{q\in S}c_q,
\qquad
\sum_{q\in Q}c_q\le W=\sum_{j\in D\setminus Q}w_j.
\]
因此所有 (S) 同时可用同一批互不相交支持，(S=Q) 时峰值回到 1，至少一枚 query 的单查询支持费不超过 (W/|Q|)。费用是指定的非查询 unit 改派费；不代表最优费用函数，也不计 U 重排、零端移动或其它收费。

证明的关键是任务标签弧和 unit 目标唯一性：删 query 弧后每个根向前的可达树不相交，R(S) 内每台机器恰接一个选中 unit，未选 query 只留下其小端残余，所以负载最多 (1+delta(S))。这是允许多级 home→unit 级联而仍保持原任务身份的结构性结果；它并没有寻找未知的两份 YES 见证，见证必须作为输入。

### 冻结 JSON 的具体回归

`single_home_cascade_query_patterns_v2.json` 的 `all_checks_passed=true`、Fraction 无浮点、脚本 SHA `c52eb5be01a64e7d13f1e80a7ad1cb5711ed187f0a8ad1000269847d004d59cd`、输入 SHA `cfb25856400d6d0ee6b6cea9cb100d8545c97fe2025643f8a62260763fc69573`，显式请求 8 个 patterns。normal form 共有 14 台机器、14 个 jobs、3 个 queries；(D) 含 q1/q2/q3、f1–f6、g、r0、r1，(Z=\{z\})，且审计核对 `A_q_pairwise_disjoint_checked=true`。典型支持为 (A_{q1}=\{f1,f2,f3,f5,f6\})、(A_{q2}=\{f4\})、(A_{q3}=\{g\})，相应 (c_q=34,7,17)，全量构造费用 58，(sigma_1) 非查询 unit 费为 100。

8 个 pattern 覆盖空 query、单 query、两 query、三 query，以及带共享级联、零端和额外 unused endpoints 的边界；单 query 例的回算峰值包括 19/16、9/8 和 1，全部 `all_original_jobs_checked`、`all_original_machine_loads_checked`、`load_bound_checked`、`fee_additivity_checked` 均通过。有限回归只核这些显式输入，正文的一般性来自弧图证明，不把 8 个样例当成全量词证明。

## 与既有对象的比较和处置

1. 与三主机 (3/2) selector、two-witness query separation：单端口对象给出复制的向下闭集障碍；单home级联对象在更强的唯一正小端、两严格见证合同下保留 query 任务身份并获得费用可加支持。两者量词不同，不能互相替换。
2. 与 PCSP/近二困难性路线：单端口 downset 说明直接用一个内部端点复制布尔否定/等值关系会产生大量混合状态；PCSP 的源困难性不能自动转成该调度模型。级联结果也只说明给定两个 YES witness 的支持分解，尚未提供未知 witness 搜索或源问题 decoder。
3. 与外部容量和零时间对象：两篇正文都把外部 joint capacity、零端移动收费和其它物理成本列为独立边界；不能将内部投影或指定 fee 直接当完整成本模型。

**完整/条件结论：** 单端口关系的向下闭集与精确状态下界/达到例；单home级联在唯一正小端、两份严格见证和指定费用下的 (A_q) 两两不交、(1+delta(S)) 负载和费用和界。

**有限实验：** 两个 JSON 的 Fraction 回归、锐例、巨大分母、负控制、8 个 cascade patterns 和具体 normal form。它们服务于重放和回归。

**障碍和后续：** 多任务共同容量、多个正小端、只有弱阈值的见证、未知 YES 的寻找、一般源 decoder、其它费用模型和全局 UM hardness/近二算法仍开放。`UM-TARGET-v1` 不因这两个来源改变状态。
