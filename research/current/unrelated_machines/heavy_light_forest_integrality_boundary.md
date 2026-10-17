# 重轻自洽 saddle 在森林残余上的整数补全边界

本文登记 `UM-HEAVY-LIGHT-FOREST-INTEGRALITY-BARRIER-v1`。它给出一个可参数化的
精确反例：重轻自洽对偶证书、残余支撑森林和 `R(H)<=T` 仍不能替代整数容量
补全；该分数—整数缺口本身可趋近二。反例与 `UM-INCIDENCE-FEEDBACK-EXACT-v1`
相容：森林叶消元会正确输出 `FAIL`，而残余分数 LP 不能承担这个结论。主目标
仍 OPEN。

## 精确实例族

取任意 `m>=2`、有理 `beta∈[1/2,1)`、`T=1`。令中心任务 `z` 在每台机器上的
处理时间都为 `beta`；每台机器 `i` 另有私有任务 `u_i`，它只有机器 `i` 这一
条有限边，处理时间
\[
 a=1-\frac{\beta}{m}.
\]
按重边严格定义 `p>beta T` 分类：中心边始终为 light；私有边若 `a>beta` 则
是唯一 heavy 端并被 `H` 强制选中，若 `a<=beta` 则也是 light，因而两种情形的
admissible heavy placement 都唯一。残余 light 关联图是星（第二种情形为带私有
叶的树；第一种情形固定私有边后只剩星）。

最小审计特例是 `m=2,beta=2/3`。把所有处理时间同时乘以 `3`，得到 `T=3`
且所有有限边时间为 `2` 的三任务实例：中心任务是 `j_0`，两枚私有任务是
`j_1,j_2`。

## 分数 saddle 与整数失败

对上述族，私有任务按其唯一端点处理；若私有边为 heavy，它们已在 `H` 中固定，
否则在残余 LP 中仍被唯一端点强制。把 `z` 以 `1/m` 的比例分到各台机器，
每台机器的残余总负载都是
\[
 a+\frac{\beta}{m}=1=T.
\]
总处理量下界给出 `R(H)=1`。取均匀价格 `lambda_i=1/m`，残余对偶对私有任务
贡献 `a`、对 `z` 贡献 `beta/m`，所以 `g(H,lambda)=a+beta/m=1=R(H)`；由于
admissible `H` 唯一，它同时是该价格下的全局最小 placement。这是纯自洽 saddle。
对任意价格 `lambda∈Δ_m`，同一目标写成
`g(H,lambda)=a+beta·min_i lambda_i≤a+beta/m=1`，故均匀价格确为最优对偶。

但 `z` 必须完整地放到某一台机器；该机还必须承担自己的私有任务。因此任何
整数分配的最大负载都是
\[
 OPT(P)=a+\beta=1+\beta-\frac{\beta}{m}.
\]
令 `m→∞` 且 `beta→1`，此比值趋近 `2`，尽管残余分数值始终恰为 `T`。
若希望 `H` 非空，可取 `beta=(m-2)/m`、`m>=4`；此时
`a=1-beta/m>beta`，每个私有边都是被强制选入的 heavy 边，而同一公式给出
`OPT=2-3/m+2/m^2 -> 2`。

在 `m=2,beta=2/3` 的等比例缩放写法中，`T=3`、三条任务均为时间 `2`：

\[
 p_{m_0,j_0}=p_{m_1,j_0}=2,\qquad
 p_{m_1,j_1}=2,\qquad p_{m_0,j_2}=2.
\]

残余 LP 的见证为
\[
 x_{m_0,j_0}=x_{m_1,j_0}=1/2,
 \quad x_{m_1,j_1}=1,
 \quad x_{m_0,j_2}=1.
\]
两台机器的分数负载都等于 `3`，对偶价格均为 `1/2`，每个任务的最小价格贡献
均为 `1`，故 `R(H)=T=3` 且 `OPT=4`。更一般地写价格为
`lambda=(u,1-u)` 时，对偶目标是
`g(u)=2+2 min(u,1-u)≤3`，等号唯一在 `u=1/2` 取得，故该价格确为最优对偶。

## 边界含义

该族的残余机器—任务关联图是森林（最小例有 `|E|-|V|+1=0` 个反馈边）；因此
反馈边精确算法在阈值上走森林叶消元并可靠拒绝。反例只否定以下错误推理：

\[
  \text{残余支撑是森林} + R(H)\le T
  \Longrightarrow \text{整数 }T\text{-补全}.
\]

森林结构保证的是整数阈值问题可用叶交换精确判定，而不是残余 assignment LP
具有整数性。要把 saddle 路线接到主目标，必须再给出一个可计算的整数容量证书、
直接调用反馈边/配置结构，或一个可靠的 `FAIL=>OPT>T` 机制；纯残余分数值和
价格 fixed point 都不够。

## Truth / Value / Novelty / Ambition

Truth：参数族的分数值、对偶值、森林结构和整数负载公式由 Fraction 审计核对；
`R(H)=T` 的最优性还由总处理量平均下界给出。Value：它把 saddle 路线与反馈边
精确算法的接口缺口具体化，并显示该接口缺口可趋近二。Novelty：最小例和参数族的
外部优先权未核查。Ambition：这是方法边界，不是一般近二困难性；`UM-TARGET-v1`
仍 OPEN。

Related files：`heavy_light_saddle_certificate_and_cycle.md`、
`incidence_cycle_rank_exact.md`、`tests/audits/unrelated_machines/heavy_light_forest_integrality_boundary.py`。
