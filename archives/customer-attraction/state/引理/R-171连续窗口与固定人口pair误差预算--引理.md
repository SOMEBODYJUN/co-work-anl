# R-171 连续窗口与固定人口 pair 误差预算

## 来源

本页合并 `76f1b4aca47880716a5c`（固定人口 pair 误差预算）、`164240d4e9248cd962b6`（有限审计输出）和 `747065dc4abd4929807d`（path interval rent budget）。冻结原文在 `R-171-coupling-interval-20261031/original/`。

## 连续窗口的普遍支付

任意实际主题路径 `S_1,...,S_m`、窗口 `I_j={j+1,...,j+ell_j}`、非负权 `theta_j` 和 `rho>0` 下，旧群体租金
\[
 E_j^{(\rho)}=\sum_x b_j(x)\left[\frac1{b_j(x)+\rho}-\frac1{b_j(x)+\rho+q_j(x)}\right]
\]
满足
\[
 \sum_j\theta_jE_j^{(\rho)}
 \le \Gamma\sum_{x:c_x>0}\left(\frac1{\rho+1}-\frac1{\rho+c_x}\right)
 \le \frac{\Gamma W}{\rho+1},
\]
其中 `Gamma=max_t Σ_{j:t∈I_j} j theta_j`。证明按每个客户真实 hit 排名展开；首 hit 系数为零，后续内层用 `b_j≤j` 和同一槽位拥塞控制。宽 2、`rho=1`、`theta_j=1/j` 给 `Gamma≤2`，总租金不超过 `W`。

连续性是承重条件。若跳过中间实际 hit，只保留每槽一次，单客户路径仍可产生 `H_q/[(rho+1)(rho+2)]` 的无界租金；有限审计还排除了错误的 rank-2 加强。因此根路径来自 SPE 本身不能删除窗口条件。

## 固定人口 pair-circuit 接口

对合法前缀 `H`、整数 `r>s≥1` 和两个主题 `a,b`，四种客户会员系数给出精确非负误差 `E_H^{r,s}(a,b)`，并有
\[
 0\le E_H^{r,s}(a,b)\le(r-s)(r-1)E_H^{2,1}(a,b).
\]
若对实际路径的前缀 `j≤m-3` 取 `r_j+s_j=m-j`，再令 `alpha_j=1/[j(r_j-s_j)(r_j-1)]`，宽 2 连续窗口预算给
\[
 \sum_{j=1}^{m-3}\frac{E_{H_j}^{r_j,s_j}(S_{j+1},S_{j+2})}{j(r_j-s_j)(r_j-1)}\le W.
\]
`(r,s)` 两个多重集可具有恰 `m` 人，但短项 `f_H(b)` 仍是代数量，不自动等于原 m 人 SPE 的真实偏离收益。因此这只是局部根路径预算接口，尚未构成全树运输。

## 状态

一般 Q-CAG-HALF 仍 OPEN。独立 Fraction 审计验证有限定义和边界；任意规模结论来自逐客户证明与连续窗口引理，而非有限枚举。后续必须证明真实 SPE 偏离可嵌入同一窗口并控制 `Gamma`，或另建可支付 skip-premium 的守恒运输；不迁移 unrelated-machines。
