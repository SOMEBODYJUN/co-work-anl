# pDM 的整数阈值调度桥梁与近二反面路线边界

本文把 2026 年关于二值 max-min allocation 的 p-dimensional matching 构造，直接翻译成一个受限的 R∥Cmax 阈值实例。它给出一个精确的整数可行性等价，但其 NO 间隙只有加一，乘性比趋近 1，因此不能单独支撑统一低于 2 的反面证明。主目标 UM-TARGET-v1 仍开放。

## 精确对象

取固定维数 d≥3。给一个 d-dimensional matching 实例：

- d 个互不相交的顶点集，每个大小为 n；
- 超边集合 E，大小为 m；
- 每条超边 e 恰含每个部件各一个顶点；
- 问是否存在 n 条两两顶点不交的超边。

取整数 b>d 且 gcd(b,d)=1。设机器集合为超边机器 m_e，共 m 台。

构造任务：

1. 每个顶点 v 产生一个顶点任务 g_v，共 dn 个；
2. 对每个超边机器 e，若 v∈e，则 g_v 在 m_e 上处理时间 b；在其他机器上不可用；
3. 产生 b(m−n) 个 dummy 任务，每个 dummy 在每台机器上处理时间 d。

这是一个整数处理时间的受限指派 R∥Cmax 实例，任务数和机器数均为源实例显式规模的多项式。

## 精确阈值定理

**UM-PDM-THRESHOLD-EXACT-v1。** 上述调度实例满足：

- 若源 d-dimensional matching 有完美匹配，则 OPT≤bd；
- 若存在 makespan≤bd 的调度，则源 d-dimensional matching 有完美匹配；
- 因而无完美匹配时 OPT≥bd+1。

### 完备性

取完美匹配 F。对每个 e∈F，把 e 的 d 个顶点任务放在 m_e，机器负载为 db。对每个未被 F 选中的机器，放 b 个 dummy，机器负载为 bd。所有任务恰好分配，故 OPT≤bd。

### 可靠性

所有顶点任务只能放在包含其顶点的超边机器上，并在该机器上耗时 b；dummy 在任意机器上耗时 d。设某台机器收到 k 个顶点任务和 ℓ 个 dummy，则其负载为

\[
bk+d\ell .
\]

若整个调度的 makespan≤bd，则总处理量为

\[
dn\cdot b+b(m-n)\cdot d=bdm,
\]

等于 m 台机器容量 bd 的总和。因此每台机器都必须恰好负载 bd，得到

\[
bk+d\ell=bd.
\]

由于 gcd(b,d)=1，d 整除 k。每台超边机器最多能收到 d 个 incident 顶点任务，所以 k∈{0,d}。所有 dn 个顶点任务都必须被接收，因此恰有 n 台机器取 k=d；它们对应的超边两两顶点不交并覆盖全部顶点，构成完美匹配。

若源实例没有完美匹配，则不存在 makespan≤bd 的调度。处理时间为整数，所以 OPT≥bd+1。

## 为什么这不能直接突破统一 2 壁垒

该桥只给出

\[
\frac{\mathrm{OPT}_{NO}}{\mathrm{OPT}_{YES}}
\ge \frac{bd+1}{bd}
=1+\frac1{bd}.
\]

当 b 或 d 增大时，这个比率趋近 1，而不是趋近 2。缩放所有处理时间只同时缩放 bd 与加一，不能改善乘性比。独立复制若保持 makespan 最大值，也不会把加性一自动变成乘性常数。

因此这个构造可以证明受限整数 R∥Cmax 的精确阈值 NP-hard，但不能推出不存在统一 (2−ε) 近似。要把它升级为主目标反面，必须另加真正的 gap amplification，同时保持普通调度中的所有部分分配都被 soundness 控制；这正是现有 pDM/局部 bundle 路线尚未完成的义务。

## 与最新文献的关系

最新 pDM 构造对 max-min allocation 的二值估值给出 pq 对 pq−1 的阈值区别；本文只是把其算术核心按维数 d、低处理时间 d、高处理时间 b 写成一个独立的整数调度桥梁。它不把文献中的近一比率硬度改写成近二硬度，也不把其结果升级成 UM-TARGET-v1 的一般反面。

## 认知层与后续义务

- Paper Fact：二值 max-min allocation 的 pDM 构造有完美匹配时达到 bd、无完美匹配时低于 bd。
- Canonical Record：本文给出对应受限 R∥Cmax 的整数阈值等价和完整位多项式证明。
- Limitation：NO 侧只有 bd+1；没有统一低于 2 的乘性 gap。
- 下一义务：寻找不破坏普通任务部分分配的 gap amplification，或证明这类 pDM 阈值构造的乘性放大必然退化。
