# 共享外端四任务环：Exact-only 全部调度独立审查

候选对象：`shared_outside_four_job_query_return_cycle_exact_v1.md`。

日期：2026-10-18。只实际读取指定 Exact；没有读取同名 Proof、其它 agent 策略或 root 的后续交换推导。此记录独立重构全部四原 jobs 的合法 assignments、所有阈值边界和参数编码。

## 实际源与结论

路径：`/workspace/scratch/038d9dcc4cac/shared_outside_four_job_query_return_cycle_exact_v1.md`。

实际字节数 3,707；实际核对 SHA256：

`c2f73db04495292714a6a083029b707f3c4c246647e4975f1f58bfdcaf15fe19`。

**PASS；未发现 fatal。** 五项精确结论全部成立。在 `0<epsilon<1` 上，完整矩阵的 16 个合法 job-to-machine assignments 恰分为：两种峰 1、三种峰 `2-epsilon`、十一种峰 2。特别，非指定的其它 partial internal subsets 已全部覆盖，没有借“只考虑列出的五个模式”省略其它 assignments。

此处按普通 UM 的 assignment 及各机处理时间和定义 C。若把无意义 idle/start-time 参数也计作不同 schedule，“两份”应读作两个 assignment/destination 模式；本次认证的是原 Exact 所用的实际目的地与负载合同。

## 完整矩阵及全部 assignments 的代数编码

原 jobs 恰为 `q_1,q_2,b_1,b_2`。每个 q_i 只可去 H 或 E_i，耗时都为 1；b_1 只可去 I 或 E_1，耗时都为 1；b_2 只可去 I 耗时 `1-epsilon`，或 E_2 耗时 1。没有其它 jobs、preloads 或有限资格。

令 x_i=1 表示 q_i 在 H，否则 q_i 在 E_i。令 y_i=1 表示 b_i 在 I，否则 b_i 在 E_i。四个布尔值唯一确定一个合法完整 assignment；反过来每个合法 assignment 都被唯一编码。其四个实际机器负载精确为

\[
\begin{aligned}
L_H&=x_1+x_2,\\
L_I&=y_1+(1-\epsilon)y_2,\\
L_{E_1}&=2-x_1-y_1,\\
L_{E_2}&=2-x_2-y_2,
\end{aligned}
\]

\[
C=\max\{L_H,L_I,L_{E_1},L_{E_2}\}.
\tag{1}
\]

E_i 的两个相应原 jobs 真正共享同一机，外部峰完整计入；没有把两个 jobs 的外部位置拆成私有机器。

## 16 种完整模式表

下表行表示内部 query 集合，列表示内部 return 集合。其余原 jobs 全部执行在各自唯一 E_i，不能删除。表内是完整实际峰。

| H 内 query 集合 | I 内空集 | I 内 `{b_1}` | I 内 `{b_2}` | I 内 `{b_1,b_2}` |
|---|---:|---:|---:|---:|
| 空集 | 2 | 2 | 2 | `2-epsilon`（inactive） |
| `{q_1}` | 2 | 2（cross(1,2)） | 1（aligned_1） | `2-epsilon` |
| `{q_2}` | 2 | 1（aligned_2） | 2（cross(2,1)） | `2-epsilon` |
| `{q_1,q_2}` | 2 | 2 | 2 | 2 |

因 `1<2-epsilon<2`，这给精确的 `2+3+11` 个 assignments 分类。固定一个内部模式后，每 job 的目的地其实已唯一确定，所以 inactive 和 cross 的“该模式内最小 makespan”就是表中精确值，没有隐藏的其它内部或外部资格可优化。

## 不依赖模式枚举的严格低峰推导

假设某完整 assignment 满足 `C<2-epsilon<2`。

1. `x_1+x_2<=1`，否则 H 上两件 unit queries 直接给峰 2。
2. 两个外部负载都小于 2；由(1)得 `x_i+y_i>=1`，i=1,2。也就是每条 shared outside 端上至少有一个对应原 job 移入内部。
3. 若 queries 一个都不在内部，即 x_1=x_2=0，则第2步迫使 y_1=y_2=1，I 负载 `2-epsilon`，与严格阈值冲突。所以 query 恰有一个内部。
4. 若 x_1=1,x_2=0，则 y_2=1。若再有 y_1=1，I 又为 `2-epsilon`，故 y_1=0。这精确给 aligned_1。对称地 x_1=0,x_2=1 精确给 aligned_2。

两种 aligned 的负载分别为

\[
(L_H,L_I,L_{E_1},L_{E_2})=(1,1-\epsilon,1,1),
\]

和 `(1,1,1,1)`，故完整峰都恰为 1。q_1 在任何 eligible machine 上时间都是 1，也给所有完整 assignments 的全局下界 C>=1。因此真实 `OPT=1`。

两个 cross 在 E_1 或 E_2 恰放两件 unit jobs，直接给峰 2；其他各机负载至多 2，所以精确为 2。inactive 的 I 承两件 return、负载 `2-epsilon`，其它有负载的两机各为 1，亦精确。

## 阈值、等号与非指定模式

- 对 `1<=B<2-epsilon`，所有 `C<=B` assignments 恰是两种 aligned。
- 在等号 `B=2-epsilon`，除两 aligned 外还接纳三种完整 assignments：内部 `{b_1,b_2}`、`{q_1,b_1,b_2}`、`{q_2,b_1,b_2}`。所以不能把严格 `<2-epsilon` 擅自改为 `<=2-epsilon`。
- 对 `2-epsilon<=B<2`，也恰是这五种 assignments；B>=2 时所有16种都可接受；B<1 时没有合法峰。
- query 为空、两个 queries 均内部、零/一个/两个 returns 的所有组合已在布尔参数和表中覆盖。没有假定内部集大小必须为二。
- 低峰时恰一个 q_i 在 H，因此可由实际目的地唯一解码其索引。没有依赖原 optimum schedule、另一侧 witness 或预先给定的 hidden source 解。

epsilon=0 不属正式域，但其 unit 环极限的关系确仍成立：两 aligned 峰1，其余14种峰2。epsilon=1 则不在域且会改变 strict1 模式数，不能用闭端点替换 `epsilon<1`。此例的两份 unit witnesses 中四台机均被正负载占用；未出现一个可供任意新 query 免费读取的闲置 machine。

## 参数映射和位复杂度

给任意 binary rational `delta in (0,1)`，令 `epsilon=delta/3`、`B=2-delta`。有 `1<B<2-epsilon`，两 aligned 峰1，任何非aligned assignment 的峰至少

\[
2-\epsilon=2-\delta/3>2-\delta=B,
\]

strict gap 恰为 `2delta/3`。这没有用参数极限替代有限有理严格不等式。

若 delta=a/b，取 0<a<b，则 epsilon=a/(3b)、`1-epsilon=(3b-a)/(3b)`、`B=(2b-a)/b`，分子分母位长都为 `O(bitlen(delta))`。图和矩阵始终四机四 jobs，没有按 delta 数值、分母、`1/delta` 或 gap 复制对象。精确比较及输出机器标识显然总位多项式。

## Scope 与状态

这只认证一个标准交替 matching 环的实际外部共享边界。它可以阻止某个内部 job-set exchange 的全球扩展，但不因此反驳一个并不承诺共享外部扩展的内部交换定理。

没有认证任意 query 的空闲读取接口、其它环/locks 上的资源识别、级联、clause connection、固定 source embedding、YES 保持、任意规模 soundness、费用摊销或 near-2 hardness。E_1/E_2 若与其它机器同一化，必须重新核完整新矩阵。这里不需要异权 medium 新机制；不能以这个常数大小例子申请一般匹配或困难性新定理。

本结论由完整公式和case proof 得出，有限枚举只可作辅助。未读作者 Proof 或其它 agent 策略，未写 repo/Git/Work，也未向其它 agent 发送任何证明。
