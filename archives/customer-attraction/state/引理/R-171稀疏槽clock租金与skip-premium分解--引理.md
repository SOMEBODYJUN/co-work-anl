# R-171 稀疏槽 clock 租金与 skip-premium 分解

## 来源与对象

- 主要来源：`94bf0c2e1187fd8ae253`（一般推导）和 `2a3ae62cdcb1da780b81`（Fraction 审计）；背景范围来自 `b3335acda0d4782bca24`、`9022a7d09f082f7bf7de`。原文和脚本冻结在 `R-171-coupling-20261031/original/`。
- 固定任意实际路径 `S_1,...,S_m`，允许重复主题、空主题和零客户；`b_t(x)` 是客户 `x` 的真实累计 hit，`c_x=b_m(x)`，`W` 是终局覆盖客户数。对每个前缀 `j` 任选稀疏未来槽 `I_j⊆{j+1,...,m}`、非负全行权 `theta_j` 和 `rho>0`，定义 `Gamma=max_t sum_{j:t∈I_j} j theta_j`。

## 可证明的 clock 上界

把不重置真实 hit 排名的时钟费用定义为
\[
 E_j^{clock}=\sum_{t\in I_j}\sum_{x\in S_t}
 \frac{b_j(x)}{(\rho+b_{t-1}(x))(\rho+b_t(x))}.
\]
固定客户的真实 hit 槽位 `t_1<...<t_c` 后，按 hit 排名交换有限和；首 hit 的系数因 `b_j(x)=0` 消失，其余每一项的行权内层不超过 `Gamma`，故
\[
 \sum_j\theta_jE_j^{clock}
 \le \Gamma\sum_{x:c_x>0}\left(\frac1{\rho+1}-\frac1{\rho+c_x}\right)
 \le \frac{\Gamma W}{\rho+1}.
\]
这一步只用同一客户的真实排名，不需要槽位几何连续性。

## reset 的精确分解

对第 `j` 行和客户 `x`，第 `k` 个被选中的 hit 的虚拟排名为 `a=b_j(x)+k`，真实排名为 `b=b_{t_{j,k}}(x)≥a`。reset 系数和 clock 系数之差恰为
\[
 p_{j,k,x}=\frac{b_j(x)(b-a)(2\rho+a+b-1)}
 {(\rho+a-1)(\rho+a)(\rho+b-1)(\rho+b)}\ge0.
\]
因此
\[
 E_j^{reset}=E_j^{clock}+P_j,\qquad P_j=\sum_{x,k}p_{j,k,x}\ge0.
\]
当每个被收费客户的选中 hit 前没有跳过实际 hit（特别是连续窗口）时 `P_j=0`；一般稀疏集合只要满足这一客户级条件也可为零。于是共同拥塞只能直接支付 clock，reset 的剩余必须另由真实激励、抵销或其他信用支付。

## 完整 SPE 障碍中的定位

在上页的两客户完整 SPE 族、`rho=1`、`I_j={q+1+j}` 时，
\[
 \sum_{j=1}^{q-1}\frac{E_j^{clock}}j
 =\frac14-\frac1{2q(q+1)},
\]
而
\[
 \sum_{j=1}^{q-1}\frac{P_j}j
 =\frac{H_{q-1}}6-\frac14+\frac1{2q(q+1)}\to\infty.
\]
所以该反例桥的无界项完全来自 skip-premium；不能把 reset 直接改写成 clock 并删掉 `P_j`。

## 状态与用途

这是一个一般代数引理和一个完整 SPE 族上的失败机制。脚本 `audit_chronological_sparse_rent.py` 穷举 `m≤8` 的全部二元路径/稀疏子集、三种 `rho` 和若干非均匀族，并核对 `q=2,...,99` 的闭式。它不产生全树支付、不证明 Q-CAG-HALF，也不迁移到 unrelated-machines。后续需要真实激励到 clock 的运输或对 premium 的支付。
