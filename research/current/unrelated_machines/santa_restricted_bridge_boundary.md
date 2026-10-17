# Santa restricted 边界与需求树桥梁的非保真性

本页修正反面路线中一个容易混淆的文献接口：Santa Claus 的已知常数近似属于 restricted max-min allocation；一般 max-min allocation 仍是不同的无约束价值模型。需求树到不相关机的精确桥梁在需求大于一时不保持 restricted 结构。因此 restricted Santa 的算法或困难性不能直接给出 UM-TARGET-v1 的正面算法或反面证明。

## 1. 两个精确模型

一般 max-min allocation 的输入是孩子集 (C)、物品集 (I) 与任意非负有理价值 (v_{ci})。分配后目标为
\[
\max_\sigma\min_{c\in C}\sum_{i:\sigma(i)=c}v_{ci}.
\]
restricted Santa 另要求每件物品 (i) 存在一个固有值 (p_i)，并且对每个孩子 (c)，
\[
v_{ci}\in\{0,p_i\}.
\]
也就是说，同一物品的所有非零端点价值必须相同；“只在某些端点可用”不改变其非零数值。

**Paper Fact（来源范围）。** Haeupler–Saha–Srinivasan, *New Constructive Aspects of the Lovász Local Lemma*, arXiv:1001.1231 / JACM 2011，§1.1 与 §4 明确定义 Santa 为上述 restricted 版本，并给出随机期望多项式时间常数近似（Theorem 4.9）。Bamas–Lindermayr–Megow–Rohwedder–Schlöter, *Santa Claus meets Makespan and Matroids*, arXiv:2307.08453，摘要则把“一般 Santa 是否存在常数近似”列为开放问题。这里不把 restricted 结果升级为一般模型结果。

## 2. 桥梁不保持 restricted 结构

沿 `UM-DAG-DEGREE-TOKEN-IDENTITY-v1` 的需求树到调度构造。对每个正需求点 (v)，每条外送子任务 (t_{v,a}) 的有限处理时间为
\[
p_{v,t_{v,a}}=1/k_v,\qquad
p_{w,t_{v,a}}=1\quad(w\in N_D^+(v)),
\]
其余机器不可用；若 (k_v>d_v)，还有仅能在 (v) 上执行的填充任务，时间 (1-d_v/k_v)。

若存在一个点 (v) 满足 (k_v>1) 且 (d_v>0)，同一任务 (t_{v,a}) 在其两个有限端点的非零处理时间分别为 (1/k_v) 与 (1)，不可能存在一个物品固有值 (p_{t_{v,a}}) 使全部非零端点都等于它。故该桥梁输出一般 max-min/不相关机实例，而不是 restricted Santa 实例。

这个判断是逐任务、逐边的结构事实，不依赖调度最优性或树值；只要一个这样的 (v) 存在便失败。反例的最小参数是 (k_v=2,d_v=1)：该任务在父机耗时 (1/2)，在唯一孩子机耗时 (1)。

反过来，若所有正需求点都满足 (k_v=1)，则外送任务的所有有限端点时间都为 (1)，且填充任务不存在；桥梁的任务矩阵属于 restricted 类（任务值均为 (1) 或不可用）。但这时每个正需求点的树出度至多一，(b(H)) 只能取 (0) 或 (1)，无法表达近二 gap 所需的连续需求层。于是“把桥梁限制到 restricted”同时删除了反面路线需要的高需求一致性机制。

## 3. 对困难性路线的准确后果

1. 已知 restricted Santa 的常数算法不能反驳一般 UM-TARGET，也不能把一般需求树桥梁变成常数可解的特例；桥梁并不落在该模型中。
2. 由 BLMRS 的 Makespan→Santa 方向得到的条件反面，若要成立，所需的是**一般** max-min allocation 的无常数近似假设（或直接的 (b^*=1) 对 (b^*\le\delta) 真实整数 gap）。restricted Santa 的结果不提供这一假设。
3. 任何声称利用 Santa 文献完成 UM 近二困难性的归约，必须逐任务核对非零端点值是否相同；只核对有限边集合或支持图是不够的。
4. 需求 (k_v>1) 的任务带来跨端点比例 (1/k_v:1)，正是 token 桥梁保持 (operatorname{OPT}=2-b^*) 的机制；删除这些异值边会回到 (k_v=1) 的可达性问题，而不是原始 MMDA。

因此本页没有给出新的无条件硬度；它关闭的是“restricted Santa 常数结果可直接移植”的错误路线，保留的一般缺口仍是跨层整数一致性的真实 (b^*=1) 对 (b^*\le\delta) 归约。`UM-TARGET-v1` 保持 OPEN。

## 4. 可复核证据与限制

独立逐边检查可由以下最小脚本复核：取 (k=2,d=1)，任务有限时间集合为 ({1/2,1})，不存在单一固有值等于二者。该检查只验证模型边界；Haeupler–Saha–Srinivasan 的算法定理和 BLMRS 的一般问题定位仍以原始来源为准，未将其余证明重新声称内化。

**Truth / Mechanism / Value / Ambition。** Truth 是模型不保真命题及其边界证明；Mechanism 是大需求在父端产生 (1/k_v) 而在子端产生 (1) 的异端时间；Value 是防止把 restricted 文献错误导入近二路线；Novelty 未认证；Ambition 不改变一般 UM 主目标。
