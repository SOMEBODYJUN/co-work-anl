# 同一子枝全部前缀利润 claim 的共同回推

2026-10-24，credible7。适用任意人数、任意有限共同目录。正文是一般逐客户恒等式与共同系数容量，不要求有限规模或特殊目录。root 收到精确陈述后独立核对恒等式、非负退款与列和；coupling7 在未读本文时从陈述独立重构，见[盲重构审查](../coupling/joint_prefix_claim_transfer_blind_review.md)。**没有证明跨多个子枝的共同容量、一般 HALF 或 actual cap1/cap2。**

## 1. 精确输入与目的

固定同一实例的两个完整行动叶 B、W，取切点 i，要求

\[
B_j=W_j\quad(j<i).
\]

两个叶均合法，但本节本身不要求两叶来自 SPE。记 c_B(x)、c_W(x) 为负载，p_j(B)、p_j(W) 为角色 j 的利润。

给同一个 W 的每个前缀角色 j<i 一个完整利润 claim 系数 lambda_j≥0；输入金额是

\[
F=\sum_{j<i}\lambda_jp_j(W).
\]

希望将它**精确、非负**地写成 parent B 的完整角色利润 claim，且控制每个 B 角色的系数。本节不按客户重权使用任何 IC。

## 2. 单前缀角色的安全退款

对 j<i、l≥i，定义

\[
q^+_{jl}=\sum_{x\in B_j\cap(B_l\setminus W_l)}
\frac1{c_B(x)c_W(x)},
\qquad
q^-_{jl}=\sum_{x\in B_j\cap(W_l\setminus B_l)}
\frac1{c_B(x)c_W(x)},
\]

以及 N_j=Σ_(l≥i)q^-_jl。所有分母只用于 x∈B_j=W_j，所以均为正。

同一前缀动作不变，负载差仅由 l≥i 的行动变化产生，故

\[
p_j(W)-p_j(B)=
\sum_{l\ge i}q^+_{jl}-N_j. \tag{DIFF}
\]

对 x∈B_j，令 r_x 为 B、W 全部共同覆盖者数，a_x 为 W 中新加、B 中没有的覆盖者数。则 c_W(x)=r_x+a_x，且 r_x≥1，因为 j 是共同覆盖者。因此

\[
p_j(B)-N_j
=\sum_{x\in B_j}\frac{r_x}{c_B(x)c_W(x)}
\ge0. \tag{SAFE-PREFIX}
\]

它也不超过 p_j(B)。所以全部负项可以从**同一个 B 角色 j 的完整利润行**安全退去，不把负项假配到另一个角色或客户的 actual 钱包。得到非负恒等式

\[
p_j(W)=\bigl[p_j(B)-N_j\bigr]
       +\sum_{l\ge i}q^+_{jl}. \tag{POSITIVE}
\]

## 3. 同一 W 全部前缀 claim 共同使用 B 的后段容量

令 b_x=|{j<i:x∈B_j}|；B、W 的前缀相同，所以 b_x≤c_W(x)。对每个 l≥i，全部前缀角色共同给 l 的正价满足

\[
\begin{aligned}
\sum_{j<i}q^+_{jl}
&=\sum_{\substack{x\in B_l\setminus W_l\\ b_x>0}}
\frac{b_x}{c_B(x)c_W(x)}\\
&\le\sum_{\substack{x\in B_l\setminus W_l\\ b_x>0}}\frac1{c_B(x)}
\le p_l(B).
\end{aligned} \tag{COLUMN}
\]

这是共同使用同一份 B_l 利润容量的关键：不是给每个过去 j 各一份 B_l。若 b_x=0，该客户的分子为零；不会使用 c_W(x)=0 的无意义分母。等价写法只对 b_x>0 的客户求和。

现在定义输出的完整行系数

\[
\kappa_j=
\lambda_j\frac{p_j(B)-N_j}{p_j(B)}\quad(j<i),
\qquad
\kappa_l=
\frac{\sum_{j<i}\lambda_jq^+_{jl}}{p_l(B)}\quad(l\ge i).
\]

当分母为零，相应分子也为零，定义系数为零。POSITIVE 给精确等式

\[
F=\sum_{l=1}^{m}\kappa_l p_l(B). \tag{PUSHBACK}
\]

若 0≤lambda_j≤L 对全部 j<i 成立，则 SAFE-PREFIX 与 COLUMN 同时给

\[
0\le\kappa_l\le L\quad\text{对全部 }l. \tag{COMMON-CAP}
\]

因此一份固定子叶 W 的**全部前缀 claim 可共同回推**，不会增加最大的完整角色利润系数。可以将算子写成非负矩阵 T，行 j<i、列 l：T_jj=(p_j(B)−N_j)/p_j(B)，T_jl=q^+_jl/p_l(B) 当 l≥i，其余为零。其每列和≤1；lambda 行向量变为 kappa=lambda T，是这个列次随机合同。单输入行的系数总和未必≤1；本命题控制的是每个输出角色的共同系数上界。

### 同一 parent 的后缀利润与单调价格推论

每份输入 j 的金额只留在原 j 或进入 l≥i>j。因此对任意非负非减角色价格 z，输入的加权金额不大于输出的加权金额。再用 COMMON-CAP 得

\[
\sum_{j<i}z_j\lambda_jp_j(W)
\le\sum_lz_l\kappa_lp_l(B)
\le L\sum_lz_lp_l(B). \tag{INCREASING-PRICE}
\]

特别取 lambda_j=1、z_l=1_(l≥k)，对每个 k<i 得

\[
\sum_{j=k}^{i-1}p_j(W)\le\sum_{l=k}^{m}p_l(B). \tag{SUFFIX-PROFIT}
\]

这里 INCREASING-PRICE 的方向与 source-time coupling 的非增价格式不同：本式还使用输出共同系数≤L；只靠不回溯支持会给相反方向的输入/输出价格比较。两者仍是各自固定资金的合同，不能分开收款后合计。

## 4. 真实 SPE context 的合法域

重要接法是：B 是从某个最后强制角色 k 后沿原完整 SPE 的规定叶，i>k，并令

\[
W=\operatorname{finish}_\sigma(B_{<i},d)
\]

为同一有序前缀下在 i 强制 d 后的真实规定续局。W 在 i 之后的真实角色 context 合法；但 W 中 j<i 的 payoff 一般含未来强制动作，不能购买该 j 的 IC。

PUSHBACK 不购买这种假 IC。它把 W 中过去 j 的 claim 送回 B：

- 所有新增正 recipient l≥i>k 在 B 中均是原策略的真实规定 context，规定叶就是 B；l=i 也合法，因为 B_i 是 parent 在该节点的原规定动作。
- parent 上 j>k 的同角色保留项也是真实规定利润。
- j≤k 的保留项若仍带更早的未来强制动作，应继续向 parent 的 parent 回推，不能直接称真实规定利润。

若保存一条严格递增强制位置的 branch stack

\[
L^0=Z,\qquad
L^r=\operatorname{finish}_\sigma(L^{r-1}_{<i_r},d_r),
\qquad i_1<\cdots<i_s,
\]

则对一个过去 payoff claim 的这种纯 ancestry 回推，每次待修复的同角色项减少一个 stack 层；新增正 recipient 在它所落的 parent 叶最后强制位置之后，因而已经是真实规定利润。到根实际叶 Z 后，所有实际利润均合法。故**单次 ancestry 规范化的域修复是有限的**，无需在含未来 query 的过去角色上调用 IC。

## 5. 容量边界与循环风险

COMMON-CAP 是一份固定 W、同一 parent B、同一组前缀 claim 的共同合同。它不允许以下额外免费合并：

1. B 的未来角色若已有另一份 claim，不能把该份系数与本次新增 kappa 相加后仍声称≤L。
2. 来自多个不同 W 子枝的投影不能各占一次同一 B 钱包，再合计保持 L；需要额外 source-disjointness 或共同列容量。
3. 单次 ancestry 回推虽有有限深度，把产生的真实 B context 再送进 off-history-IC/反向债务展开，可能重新生成原 W 义务。全局反向网络可能有环；本文没有给其谱半径、吸收性或跨来源容量。

因此本命题修复的是此前 multi-force prefix 中过去利润的**真实域及一个固定子枝的多角色共同系数**。它不是把全部 history 的债务放进一个已经有界的 actual 钱包，也未将 off-IC 的额外项支付掉。Q-CAG-HALF 仍 OPEN。
