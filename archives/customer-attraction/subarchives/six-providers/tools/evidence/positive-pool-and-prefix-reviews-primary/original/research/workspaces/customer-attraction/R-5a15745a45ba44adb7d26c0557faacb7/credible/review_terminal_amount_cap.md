# TERMINAL-CAP2独立重构审查及DEEP-CAP2准确范围

2026-10-24。审查对象为同actor个人区`parent/terminal_amount_cap.md`，只审其末层一般引理并核对更深候选身份；没有审过或证明一般Q-CAG-HALF。

## 1. 审查结论

**TERMINAL-CAP2证明正确。** 它适用于任意有限单位客户、任意共同目录、任意人数以及任意多末位强制孩子，不使用SPE。多个孩子必须共同满足原文AMOUNT；不能对各孩子各给一份完整sender利润后再相加。

独立推导如下。固定原完整叶B，孩子Wα仅把末位Bm换成Tα。旧sender j<m的主题在每个孩子保持Bj。对每个x∈Bj，有cB(x)>=1且

\[
c_\alpha(x)\le c_B(x)+1\le2c_B(x).
\]

所以pj(Wα)>=pj(B)/2。若pj(B)>0，AMOUNT直接给Σαλ_(α,j)<=2。若pj(B)=0，则Bj没有单位客户，所有相关正价q均为0；无需也不能用除零推出λ总和界。

固定x∈Bm。设c=cB(x)。c=1时没有prefix sender覆盖x，正价总贡献为0。c>=2时恰有c−1名prefix sender覆盖x。只有Tα不含x的孩子在q中记x，而它们都满足cα(x)=c−1。因此其总贡献至多

\[
\frac1{c(c-1)}\sum_{j<m:x\in B_j}\sum_\alpha\lambda_{\alpha,j}
\le\frac{2(c-1)}{c(c-1)}=\frac2c.
\]

逐客户求和得原文第一界，再由Bm全利润的非负客户份额得第二界。m=1时sender集为空；零客户、空主题、重复主题与相同覆盖的不同标签均不改变论证。这是一段全量词代数证明，未用有限核验替代一般性。

## 2. 不能移用到DEEP的具体两步

更深分支α=(i,T)是在真实原策略σ的实际前缀处强制T后，沿同一σ完成的真实叶Wα。对于j<i，sender主题仍是Bj，但多个后继动作均可能改变。因此一般不再有cα<=cB+1；某recipient l的旧客户被移走时，也不再有cα=cB−1。

所以末层引理没有给任意深度cap2。原文将下式保留为候选是准确的：

\[
\sum_{\alpha:i_\alpha\le l}\sum_{j<i_\alpha}
\lambda_{\alpha,j}
\sum_{x\in B_j\cap(B_l\setminus W_l^\alpha)}
\frac1{c_B(x)c_\alpha(x)}
\stackrel{?}{\le}2p_l(B),
\]

其中每个sender j的AMOUNT预算为Σ_(α:j<iα)λ_(α,j)pj(Wα)<=pj(B)。必须保留Wα是真实完整SPE后继，不能用任意合法叶的失败宣布DEEP-CAP2反驳。

若固定有限实例和完整策略，且只优化这些既定分支的λ，则每个sender的最优贡献确为

\[
p_j(B)\max_{\alpha:j<i_\alpha\le l}
\frac{q_{\alpha,j,l}}{p_j(W^\alpha)}.
\]

当该sender主题非空，分母严格正；主题空时原利润与全部q均为0。没有分支则最大贡献按0计。不同sender预算独立，所以对j求和恢复精确最坏AMOUNT输入。该有限闭式不处理σ、客户数或目录的一般量词。

## 3. 本次范围内的停点

未得到DEEP-CAP2的一般证明或真实全历史反例。没有据旧锥阴性检验提升其真值，也没有把末层cap2视为一般half的支付。即便将来DEEP成立，还需要独立证明一般覆盖债务能合法输入AMOUNT且原sender利润没有被其他direct/suffix账重复使用。

Hres、同枝退款与压缩背景停止点另见本目录`residual_background_induction.md`。这些候选没有与末层cap2拼成目标证明。
