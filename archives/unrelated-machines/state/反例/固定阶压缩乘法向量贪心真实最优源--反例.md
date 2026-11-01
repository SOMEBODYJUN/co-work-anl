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
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/polynomial_vector_greedy.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/polynomial_vector_greedy_independent.py"
legacy_ids:
  - "UM-TRUE-MOMENT-VECTOR-GREEDY-LINEAR-GAP-v1"
source_sha256: "f44814c28e337ff312506d6caf6c5c34ce6c6aa78b3c10f5e8f2ae34b5383369"
review_level: "full review read; independent exact reconstruction; finite Fraction audit"
---

## 构造

固定整数 $r\ge1$，令 $d=2r+1$、$B=2d$，取素数 $q>B$。普通机器为 $0,\ldots,q-2$，另有专用机器 $q-1$，总机器数为 $q$。普通任务以 $t\in\mathbb F_q$ 编号，每个都可在全部 $q-1$ 台普通机器上以处理时间一运行，在专用机不可用；另有**一个**anchor任务，仅可在专用机运行，处理时间为 $B$。所以任务数为 $q+1$。这是原稿与规范导出的同一实例；求值点是任务编号，不是另一组机器。规范JSON的 `None` 表示不可用边。

在全部首一 $d$ 次多项式

\[
f(t)=t^d+\sum_{h=0}^{d-1}a_ht^h
\]

上均匀取系数标签 $a\in\mathbb F_q^d$。定义 $g(0)=g(1)=0$，且 $g(y)=y-1$ 对 $2\le y\le q-1$。在这个源态中，将普通任务 $t$ 派到普通机 $g(f(t))$，anchor派到专用机。这里方程决定**源的分配**，没有把其余普通机器从原输入的可用边中删除。

每个 $f(t)-y$ 是非零 $d$ 次多项式，至多有 $d$ 个根。普通机0合并两个求值类，负载至多 $2d=B$；其余普通机至多 $d$；anchor的负载恒为 $B$。因此每个源态都是makespan恰为 $B$ 的合法调度。强制anchor也给任意调度的下界 $B$，故

\[
\mathrm{OPT}=B.\tag{1}
\]

源有 $q^d$ 个等权**带系数标签原子**，不把它们断言为互异调度；若不同标签给同一调度，可合并概率而保持全部 $L^2$ 内积。$q=13,r=1$ 的实际导出即13机器、14任务、一个处理时间6的anchor，及2197个带标签源态。旧正文曾写成按 $(t,y)$ 建机器及 $B$ 个unit anchor，本次依完整原稿和两个规范源码校准其实例身份，不另授新反例。

## 压缩作用与贪心失败

令 (V_r) 为次数不超过 (r) 的乘法特征空间，按每个任务的零均值块作 (L^2) 商。Vandermonde 非奇异性保证：对任意 (h\le d) 个不同求值点，前 (h) 个系数由目标值唯一决定，其余 (d-h) 个自由，因此所有单任务边际严格正，真实源中所有高阶矩同时存在。

若当前向量写成纯次数小于 (r) 的部分 (u) 与纯 (r) 次部分 (v)，新任务 (j) 的类别函数 (h=x_j-p) 满足

\[
P_r(hv)=0,\qquad A_{ji}\psi=p\psi+hu,
\]

这里 $j$ 未处理，$u,v$ 只含已处理任务。乘积 $hv$ 有 $r+1$ 个不同零均值任务块；任何次数不超过 $r$ 的测试项至少漏一个，联合范围至多 $2r+1$ 个任务。因此即使测试项含未来任务，$d=2r+1$ 重独立仍使内积为零，确认的是整个 $V_r$ 上的投影。于是

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

## 规范原程序与有限范围的接续

上方一般证明及独立审查附录中的r1 q7/11/13、r2 q11/13历史检查保持原身份。两份规范程序的范围不同：主程序另有r2 q3的243原子七维真实投影，独立规范程序只审三次源r1，没有r2 q7运行。详细算法、实际输入、两份匹配源SHA的原报告参数及三类核验的区分见[两份规范审计与输入导出](../程序/多项式真实源的两份规范审计与输入导出--程序.md)。本次原程序执行0；旧正文before和逐项修正记录见对应新证据，旧代码、报告及完成记录不改。
