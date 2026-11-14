# DEEP-CAP2：末层逐列二倍与正价总池的边界审查

## 结论

本包建立的是一条 checks/context 边：

customer-attraction/positive-source-common-amount-pool-and-position-loss
与
customer-attraction/terminal-multichild-amount-normalized-sharp-column-cap-two
使用同一个逐 sender 的共享 AMOUNT 合同，但承重的输出量词不同。因此，末层的
2p_m(B) 列界不能递归为一般多 cut 的 DEEP-CAP2；正价源池只支付所有 recipient
的合计金额，并不提供每个目标列的独立 charge。DEEP-CAP2 的一般真实 SPE 量词仍开放。

同时保留两项下界事实：

1. 末层完整 SPE 锐族取 m=n+1，每个 sender 取
   λ=(2n−1)/(n+1)，所得列比为
   \[
   {n(2n-1)/(n+1)\over n}=2-{3\over n+1}\xrightarrow[n\to\infty]{}2.
   \]
2. 另读的 registry context《任意固定正尾长的非末位金额列系数二下界》把同一构造接到
   任意固定 r≥1 个真实正尾：m=n+1+r、目标 ℓ=n+1，同一比值
   2−3/(n+1) 仍由完整纯 SPE 和真实同策略后继达到。它只作 context，不是本任务
   coverage 端点，也不把该下界变成 DEEP 上界或 half 反例；该族满足 W=OPT。

## 1. 共同合同与正价总池

对 cut i_α 之前与父叶 B 相同的孩子 W^α，以及
j<i_α、ℓ≥i_α，正价为
\[
q_{\alpha j\ell}=
\sum_{x\in B_j\cap(B_\ell\setminus W^\alpha_\ell)}
{1\over c_B(x)c_\alpha(x)}.
\]
AMOUNT 是跨所有孩子的一份钱包：
\[
\sum_\alpha\lambda_{\alpha j}p_j(W^\alpha)\le p_j(B),\qquad \lambda_{\alpha j}\ge0.
\]

正价源池逐客户定义 suffix 原覆盖者离开数 R_α(x) 与保留项
\[
 e_{\alpha j}=\sum_{x\in B_j}{c_B(x)-R_\alpha(x)\over c_B(x)c_\alpha(x)}\ge0,
\]
从而得到精确等式
\[
\sum_{\ell\ge i_\alpha}q_{\alpha j\ell}+e_{\alpha j}=p_j(W^\alpha).
\]
对全部孩子只可使用一次 AMOUNT，因此
\[
\sum_\ell \mathrm{out}_\ell
 \le \sum_{j<m}p_j(B)=W(B)-p_m(B)
\]
（保留项与正价同池扣款）。位置粗化也只给
\[
\sum_{\alpha,j,\ell}\lambda q
\le\sum_{j<m}{m-j\over m-j+1}p_j(B),
\]
它是总量而非目标列界。

同时，NET 身份为
\[
\sum_\ell q_{\alpha j\ell}
=p_j(W^\alpha)-p_j(B)
 +\sum_{x\in B_j}{A_\alpha(x)\over c_B(x)c_\alpha(x)},
\]
其中 A_α 是新增 suffix 覆盖者数。新增补偿一般非零，正价不能改写为“旧利润净增”。
因此 direct、suffix、retained/e 三类债务若已支取同一 sender 的 AMOUNT，不能再从同一
孩子利润另领一份；把新增补偿另列为新预算也会重复占款。更根本的覆盖债务/OPT 如何合法
初始化为 AMOUNT，仍需真实 IC 的独立证明。

## 2. 末层为什么能得逐列二倍

terminal 定理限定 i_α=m，每个孩子只替换末位。对固定 sender 的每个客户，
孩子负载至多增加一：
\[
c_\alpha(x)\le c_B(x)+1\le2c_B(x),
\qquad p_j(W^\alpha)\ge {1\over2}p_j(B).
\]
所以正利润 sender 的共享预算给出
\[
\sum_\alpha\lambda_{\alpha j}\le2.
\]
固定末位客户 x 时，若 c_B(x)≥2，其 prefix 覆盖者恰有 c_B(x)−1 个；
只要孩子把 x 从末位移走，就有精确等式 c_\alpha(x)=c_B(x)−1。逐 sender 的预算和
因而合并为至多 2/c_B(x)，求和得
\[
\sum_{\alpha,j<m}\lambda_{\alpha j}q_{\alpha jm}
\le2\sum_{x\in B_m:c_B(x)\ge2}{1\over c_B(x)}
\le2p_m(B).
\]
零利润、空主题、重复孩子和 m=1 均直接给零端点；没有除以零。

这里的两处等式正是深层不能复用的地方。若 cut 后有
r=m−i_α+1 个动作变化，只能写
c_\alpha(x)≤c_B(x)+r（或 (r+1)c_B(x)），不再有统一的 sender
预算因子 2。目标客户离开一个位置后，其他后继可继续加入或离开，通常也不再满足
c_\alpha(x)=c_B(x)−1。因此没有逐列 charge 把同一总池分配到每个 ℓ。

## 3. 多 cut 的精确开放接口

DEEP 候选要求对每个目标位置
\[
Q_\ell=
\sum_{\alpha:i_\alpha\le\ell}\sum_{j<i_\alpha}
\lambda_{\alpha j}q_{\alpha j\ell}
\le2p_\ell(B).
\]
固定实例、固定完整策略和固定列的原筛查只得到线性预算下的精确值
\[
\max Q_\ell
=\sum_{j<\ell}p_j(B)
\max_{\alpha:j<i_\alpha\le\ell}
{q_{\alpha j\ell}\over p_j(W^\alpha)}.
\]
不同目标列可选择不同的最大孩子；该式既不是所有 SPE 的上界，也不把多列最大值同时实现。故 TOTAL 和末层 CAP2 都不能闭合一般 DEEP-CAP2。

另读的非末位固定正尾长 context 给真实 SPE 的相反方向：对每个固定 r≥1，同一
目标 ℓ=n+1 有完整真实后继，输出比逼近二。它只排除任何统一系数小于二，不能证明二倍上界；多 cut 的一般合法叶松弛还可出现更大的调和常数，但那不是本边的真实 SPE 结论。

## 4. 证据和执行边界

任务声明的七份 distinct refs 已全文读取并逐 SHA 校对；共同模型、正价程序/引理、R5a
总账、跨枝列优化程序、末层定理及 terminal 原始稿的量词与零端点均核对。registry 中
非末位 fixed-tail lower 只作为 context 阅读，不加入 task coverage endpoint。没有运行原
程序、LP、SPE/IC 搜索或随机重放，没有修改源正文，也没有 checkpoint、commit、push 或
map done；edge-bind --write 与 edge-check 仅作结构和引用绑定验证。
