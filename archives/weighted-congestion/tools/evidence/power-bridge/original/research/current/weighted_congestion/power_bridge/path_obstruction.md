# 固定次线性幂乘子：两尺度路径比障碍

作者：R2 内部研究成员 dense_scales；2026-10-14。主对话负责独立审查、账本登记及 Git 写入。

## Claim 身份

- **ID/version：** `WC-R2-POWER-PATH-OBSTRUCTION v1`。
- **Exact Statement：** 对每个固定实数 `0 <= p < 1` 和每个有限 `alpha >= 1`，存在一个有限潜在玩家集合 `U`、仅两种正权及线性费用 `c(x)=x`，使得不存在集合函数 `F:2^U -> R` 和共同常数 `lambda>0` 满足：对每个 `S subset U` 和 `i in S`，

  `lambda w_i^p c(W(S)) <= F(S)-F(S\{i}) <= alpha lambda w_i^p c(W(S))`。

  此外，两种权重各自的玩家数均可任意大。
- **Objects：** 一个资源上的任意集合势；乘子 `h_i=w_i^p`；`W(S)=sum_{i in S}w_i`。
- **Domain / Quantifiers：** 全部有限玩家集合、全部正权；参数 `p` 固定，随后任给有限 `alpha`；反例允许人数及权重比依赖 `p,alpha`。
- **Assumptions：** 边际下界和上界使用同一个与玩家、集合无关的正缩放 `lambda`；每个潜在用户子集均须满足比较。
- **Scope：** 资源局部边际证书的障碍；已经在 `c(x)=x`、即任意最大次数界 `d>=1` 的模型内成立。
- **Conclusion：** 固定 `p<1` 的共同 power 乘子无法仅靠更换集合敏感势覆盖任意密度的混合尺度资源。
- **Dependencies：** 有限路径求和；等差数列求和。数学证明不依赖外部定理。
- **Evidence：** 下列一般证明；独立精确有理回归及独立审查由主对话添加。
- **Counterevidence / Objections：** 不排除改变乘子、限制可出现子集、引入状态相关比较、或采用其他全局存在论证；不是近似均衡非存在下界。
- **Status：** 一般证明完成，独立先重构及主对话核验通过；规范身份在 research/current/weighted_congestion/power_bridge.md。新颖性未认证。
- **Related Files：** 本目录的主对话核验脚本与 review 文件（由主对话按实际文件名登记）。

## 1. 任意集合势必须满足的路径比条件

令 `h_i>0`。若 `F` 的边际介于 `lambda h_i c(W(S))` 和 `alpha lambda h_i c(W(S))`，则对任一终集 `U` 的任一排列 `pi`，定义

`T(pi)=sum_{k=1}^{|U|} h_{pi(k)} c(sum_{j=1}^k w_{pi(j)})`。

从空集依排列逐个加入玩家并求和，得到

`lambda T(pi) <= F(U)-F(empty) <= alpha lambda T(pi)`。

因此任意两个排列 `pi,rho` 满足

`T(pi) / T(rho) <= alpha`。

这里分母在后述构造中严格为正。共同缩放 `lambda` 消去；允许 `F` 任意依赖整个集合也不能绕过此必要条件。该条件只被用作必要条件，未声称它足以保证集合势存在。

## 2. 一个重玩家与一个密集轻组

一个重玩家权为 `1`，`N` 个轻玩家权均为 `epsilon>0`。取 `c(x)=x` 和 `h_i=w_i^p`。记

`S=N epsilon`,

`Q=epsilon^(p+1) N(N+1)/2`。

先重后轻与先轻后重的路径和恰为

`T_HL = 1 + N epsilon^p + Q`,

`T_LH = 1 + S + Q`。

故每个所要求的集合势必须满足

`alpha >= (1+N epsilon^p+Q)/(1+N epsilon+Q)`。

**统一参数。** 任取实数 `t>=4`，令

`a=(1+2p)/(1-p)`, `b=3/(1-p)`,

`N=ceil(t^a)`, `epsilon=t^(-b)`。

由于 `a-bp=1`、`a-b=-2`、`2a-b(p+1)=-1`，以及 `N<=2t^a`、`N+1<=3t^a`，有

`N epsilon^p >= t`,

`S <= 2/t^2`,

`Q <= 3/t`。

于是

`T_HL/T_LH >= (1+t)/(1+2/t^2+3/t) > t/2`。

最后一步等价于 `t>1+2/t`，由 `t>=4` 保证。令 `t>2alpha` 即得矛盾。`p=0` 完全包含在该计算中；所有玩家权始终严格为正，且构造始终有限。

**一个精确有理子族。** 对 `p=1/2`、整数 `t>=2`，也可取 `N=t^4`、`epsilon=t^(-6)`，此时 `epsilon^p=t^(-3)`，

`T_HL=1+t+(t^(-1)+t^(-5))/2`,

`T_LH=1+t^(-2)+(t^(-1)+t^(-5))/2`。

两式均为有理数，路径比趋于 `t`。该子族适合独立精确算术回归。

## 3. 两个权组都任意密集

一般取 `M` 个权为 `1` 的重玩家和 `N` 个权为 `epsilon` 的轻玩家。记 `B=M(M+1)/2`，路径和变为

`T_HL=B+MN epsilon^p+Q`,

`T_LH=B+MN epsilon+Q`。

固定任意大的整数 `M` 并令上节 `t` 趋于无穷，路径比仍趋于无穷。这已说明重组不能被预先给定的密度阈值排除。

若要求两个计数沿同一序列都趋于无穷，可取整数 `t>=4`，令

`M=t`, `N=ceil(t^(2a))`, `epsilon=t^(-2b)`。

将上节的基准参数替换为 `t^2`，有

`N epsilon^p>=t^2`, `N epsilon<=2/t^4`, `Q<=3/t^2`。

因此

`T_HL/T_LH >= (B+t^3)/(B+2/t^3+3/t^2) > t`。

最后一步由

`B+t^3-t(B+2/t^3+3/t^2) = (t^3+t)/2 - 2/t^2 - 3/t > 0`

得到。此时两组人数都趋于无穷，而且每组内部权比恰为 `1`。

## 4. 对 multiscale 拼接接口的含义

单个近等权资源上的排序离散积分，及低 multiplicative-bin occupancy 资源上的 power 势，可以分别成功。但是，若同一资源同时含有本例的两个密集精确权组，任何以共同 `h_i=w_i^p` 为目标、并对所有潜在用户子集给统一边际夹逼的桥梁都失败。失败无需高次数、无需多项式混合项、无需三个以上权尺度，且不依赖候选势的公式形式。

分别对两个权组建立局部势再相加时，轻组在重组已加入后的总目标增量是 `MN epsilon^p`；反序中重组受轻组影响的总目标增量是 `MN epsilon`。当 `p<1`，这两个跨组贡献的失配可以任意大。任何合法集合势从空集到同一终集的增量必须与顺序无关，这就是无法修复的接口冲突。

该结果并未否定为给定有限实例选择 `p` 随权比、人数变化的方案；它说明固定次线性 power 接口不具有所需普遍保证。也不否定共享乘子改用非 power、依实例选取的正值。但这类替代乘子必须重新证明跨资源兼容性，而不能直接引用现有 power 资源比较。

`p=1` 不被本论证否定。事实上对线性费用，

`F(S) = (W(S)^2 + sum_{i in S} w_i^2)/2`

恰有 `F(S)-F(S\{i})=w_i W(S)`，故本例也直接检查了结论的 `p<1` 边界。

这不是 `alpha`-PNE 非存在结论。一个只有该资源和空策略的游戏甚至有平凡均衡；本文件只否定一种拟用于任意多资源策略的局部充分证书。它也不否定只需在实例实际可达子集上成立的证书，除非这些子集包含本证明所使用的路径。

## 5. 文献检查范围

2026-10-14 用网页检索检查了 weighted congestion games、approximate potential、number of weight classes，以及 two weight types 相关条目，并打开一手来源。以下文献的公开摘要核实了通用 `d` 近似势基线和加权博弈近似势背景：

- Caragiannis–Fanelli, *On Approximate Pure Nash Equilibria in Weighted Congestion Games with Polynomial Latencies*, ICALP 2019, https://doi.org/10.4230/LIPIcs.ICALP.2019.133 。
- Giannakopoulos–Poças, *A Unifying Approximate Potential for Weighted Congestion Games*, https://arxiv.org/abs/2005.10101 。

尝试读取 `arxiv.org/html/2002.07466v3` 和 `arxiv.org/html/1902.07173` 时页面获取失败；失败不构成任何数学证据。未在本轮检索中认证上述路径障碍的新颖性，也未将搜索不到视为不存在既有结果。本文件一般证明不引用未读取的外部定理。


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
