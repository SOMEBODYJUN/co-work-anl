---
id: "unrelated-machines/truncated-multiplication-vector-greedy-true-source"
kind: "counterexample"
type_tag: "反例"
title: "固定阶压缩乘法向量贪心的真实最优源反例"
status: "exact-family-established-with-finite-audit"
truth_status: "analytic fixed-r family; finite checks are supporting evidence only"
summary: "对固定阶 r 的真实有限源，压缩到次数不超过 r 的乘法向量并逐任务最大化下一作用范数的贪心规则，在显式 anchor 约束下拥有 OPT=B，却对全部普通任务选中同一普通机，产生峰值 q；近似比 q/B 可随大域增长。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/truncated_vector_greedy_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/truncated_vector_greedy_review.md"
legacy_ids:
  - "UM-TRUE-MOMENT-VECTOR-GREEDY-LINEAR-GAP-v1"
source_sha256: "f44814c28e337ff312506d6caf6c5c34ce6c6aa78b3c10f5e8f2ae34b5383369"
review_level: "full review read; independent exact reconstruction; finite Fraction audit"
---

## 构造

固定 (r\ge1)，令 (d=2r+1)、(B=2d)，取素数 (q>B)。对所有首一的 (d) 次多项式

\[
f(t)=t^d+c_{d-1}t^{d-1}+\cdots+c_0
\]

均匀取系数向量 (c\in\mathbb F_q^d)。对每个求值点 (t\in\mathbb F_q) 和目标值 (y\in\{0,1\}) 建立普通机器；任务按求值方程 (f(t)=y) 归入可用端。另有一个 anchor 机器，所有 anchor 作业只在此处以一处理时间执行，共 (B) 件。每个系数状态是完整合法调度：方程至多 (d) 个根，合并 (0,1) 后每个普通机器至多 (2d=B) 个 unit 作业；anchor 给出所有调度的下界 (B)，故

\[
\mathrm{OPT}=B. \tag{1}
\]

这是固定 (r)、显式源族的真实最优值恒等式；不同系数标签代表同一实际调度时可合并概率质量，不改变 (L^2) 内积。

## 压缩作用与贪心失败

令 (V_r) 为次数不超过 (r) 的乘法特征空间，按每个任务的零均值块作 (L^2) 商。Vandermonde 非奇异性保证：对任意 (h\le d) 个不同求值点，前 (h) 个系数由目标值唯一决定，其余 (d-h) 个自由，因此所有单任务边际严格正，真实源中所有高阶矩同时存在。

若当前向量写成纯次数小于 (r) 的部分 (u) 与纯 (r) 次部分 (v)，新任务 (j) 的类别函数 (h=x_j-p) 满足

\[
P_r(hv)=0,\qquad A_{ji}\psi=p\psi+hu,
\]

其中 (P_r) 是 (V_r) 投影。测试整个 (V_r) 需要至多 (r+1\) 个新鲜任务块；(d=2r+1) 的独立性足以使未覆盖零均值因子消失。于是

\[
\|A_{ji}\psi\|^2=p\|u\|^2+p^2\|v\|^2. \tag{2}
\]

取普通机 0 的边际 (p_0=2/q)，其他普通机的边际 (p_1=1/q)，评分差为

\[
\|u\|^2/q+3\|v\|^2/q^2>0
\]

对每个非零 (\psi) 严格为正。所以无论任务顺序，贪心都把所有普通任务选到机器 0；anchor 任务只能选 anchor。机器 0 的峰值为 (q)，而 (1) 给出 OPT (=B=2(2r+1))，故比值

\[
q/B
]

可随 (q) 增长，不能由固定阶压缩乘法评分推出统一常数近似。

## 证据与限制

独立 Fraction 审查重建了正交分块、全空间投影、固定阶位复杂度和上述真实源；有限运行完整枚举了 (r=1,q\in\{7,11,13\}) 与 (r=2,q\in\{11,13\}) 的系数态。(r=1) 逐项核所有线性测试残差；(r=2) 核实际源、范数和有限独立性，但未形成完整 (V_2) 矩阵。它们支持而不替代全称解析证明。

该反例只针对固定 (r)、次数截断和“最大化下一作用范数”的特定规则。它不证明所有矩方法、SOS/LS、配置松弛或一般调度算法失败，也不把 (r) 随输入增长时的次数依赖写成统一多项式。源审查确认原文的零值措辞已限于给定最优源 (T=\mathrm{OPT}) 的承诺；一般 OPT=0 但输入源不支持零端时，规则仍可能输出正负载。
