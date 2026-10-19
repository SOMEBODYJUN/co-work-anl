# pDM 的整数阈值调度桥梁与近二反面路线边界

本文把 2026 年关于二值 max-min allocation 的 p-dimensional matching 构造，直接翻译成一个受限的 R∥Cmax 阈值实例。总工作量与整除给出阈值算术内核；原 v1 的完整合法源域仍有下述审查异议。当前证明只给 NO 侧加一的下界，不能把它当作 NO 上界。主目标 UM-TARGET-v1 仍开放。

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

该证明只给出下界

\[
\frac{\mathrm{OPT}_{NO}}{\mathrm{OPT}_{YES}}
\ge \frac{bd+1}{bd}
=1+\frac1{bd}.
\]

当 b 或 d 增大时，这条已证下界趋近 1；这不说明实际 NO 值也趋近该下界。缩放或独立复制本身没有提供更大的可靠 gap。

因此这个构造可以证明受限整数 R∥Cmax 的精确阈值 NP-hard，但不能推出不存在统一 (2−ε) 近似。要把它升级为主目标反面，必须另加真正的 gap amplification，同时保持普通调度中的所有部分分配都被 soundness 控制；这正是现有 pDM/局部 bundle 路线尚未完成的义务。

## 与最新文献的关系

最新 pDM 构造对 max-min allocation 的二值估值给出 pq 对 pq−1 的阈值区别；本文只是把其算术核心按维数 d、低处理时间 d、高处理时间 b 写成一个独立的整数调度桥梁。它不把文献中的近一比率硬度改写成近二硬度，也不把其结果升级成 UM-TARGET-v1 的一般反面。

## 认知层与后续义务

- Paper Fact：二值 max-min allocation 的 pDM 构造有完美匹配时达到 bd、无完美匹配时低于 bd。
- Canonical Record：本文给出对应受限 R∥Cmax 的整数阈值等价和完整位多项式证明。
- Limitation：目前只证明 NO 侧至少 bd+1，未给近二乘性 gap；该下界本身不限制真实 NO 上界。
- 下一义务：寻找不破坏普通任务部分分配的 gap amplification，或证明这类 pDM 阈值构造的乘性放大必然退化。

## 合入审查：原 v1 合同待补，不能误用加一方向

[合法域与间隙方向审查](../../reviews/unrelated_machines/pdm_threshold_domain_and_gap_review.md)指出：主公式尚未处理 `m<n`、孤立源顶点和 `n=m=0`；若 `b` 可作二进制可变参数，dummy 的显式输出规模还须另核。专题账本按固定 `d,b` 解释时后一点没有问题，但完整非退化域仍应写明。原 v1 因而暂记条件性内核，不把补充假设默默加入后继续称全域证明完成。

同一审查还给出已有槽定理的直接推论：本合法编译的 `max p=b=T/d`，assignment LP(T) 不可行可可靠拒绝；可行即实际输出 `C≤(1+1/d)T≤4T/3`。这是限制本形状近二 gap 的真实算法论证，区别于仅从 `OPT_NO≥bd+1` 推断 NO gap“只有加一”。它不是一般 UM 的新近似算法。

## 精确低负载逃逸实例（有限观察）

为检验“没有完美匹配就会自动产生近二 NO 值”的更强直觉，取 `d=3,n=2,m=3,b=4`，三条超边为

\[
e_0=(a_1,b_1,c_1),\qquad e_1=(a_1,b_2,c_2),\qquad e_2=(a_2,b_1,c_2).
\]

任意两条边相交，所以三维实例没有完美匹配。按上面的编译，阈值是 `T=bd=12`，有 6 个顶点任务和 `b(m-n)=4` 个 dummy，所有任务总工作量为 `36=mT`。对这 10 个任务的全部 `2·1·2·1·1·2·3^4=648` 个合法分配用 `Fraction` 穷举，得到

\[
  \operatorname{OPT}=13,
  \qquad (L_0,L_1,L_2)=(12,11,13),
  \qquad \operatorname{OPT}/T=13/12.
\]

因此这里确实没有 `C_max≤T` 的调度，但仍有一个只比阈值高 `1/12` 的调度。这个实例不否定阈值定理；它只反驳把阈值 NO 条件直接当作近二乘性 NO gap 的推断。可复现代码和冻结输出见 [`pdm_escape_counterexample.py`](../../../tests/audits/unrelated_machines/pdm_escape_counterexample.py) 与 [`pdm_escape_counterexample_audit.json`](../../../evidence/runs/unrelated_machines/pdm_escape_counterexample_audit.json)。

## 两值 max-min 硬度传递的常数边界

Vu–Nguyen–Elbassioni–Rothe (arXiv:2610.05237, 2026-10-04) 的 Theorem 2 对互素整数 `q>p≥3` 的二值估值 `{p,q}` 给出：任意 `ρ<pq/(pq-1)` 的 max-min allocation 近似是 NP-hard。BLMRS 的两值等价把 Santa 因子 `α` 与 makespan 因子 `2−1/α` 对接。因此这条预印传递链至多给相应二值调度像的阈值

\[
  2-\frac{1}{pq/(pq-1)}
  = 1+\frac1{pq}.
\]

最小允许的 `pq` 已是 `12`，所以该方向只到 `13/12`，随 `pq` 增大反而趋近 `1`；它既不接近 `2`，也不能替代 UM-TARGET-v1 的一般反面。这里保存的是常数传递边界，不是把外部 max-min 困难性升级为一般 R∥Cmax 困难性。
