# 共同倒数第二主题的完整历史半覆盖定理

## 精确身份与状态

**CA-COMMON-PENULTIMATE-HALF-v1。** 完整解析证明，独立内部解析重构及精确审计通过；不是一般 Q-CAG-HALF 的完整证明，不声称外审、新颖性或锐性。

对象为 CAG-MODEL 的有限单位客户、共同有限非空目录与 m 名单位权玩家。固定任意完整历史依赖纯 SPE，量化所有离轨历史及任意平局。若 m≥3，真实在轨倒数第二主题 A 满足

\[
A\subseteq A_j\qquad(1\le j\le m-2),
\tag{H}
\]

其中 A_j 为各早期真实主题，而真实末位主题记 B，则

\[
2W\ge\operatorname{OPT}_m.
\]

没有限制整个目录的极大主题数或其他离轨主题。特别地包括任意目录、任意人数的路径 A^{m-1}B；早期主题也可以是 A 的任意不同超集。m=1,2 已由既有一般定理覆盖。假设 (H) 是新的结构范围，不能删去后仍引用本证明。

## 真实末两人菜单

固定原有序前缀 (A_1,...,A_{m-2})，写客户负载 p_x。任取 m 个合法比较主题 T_1,...,T_m，允许重复，令 O 为它们并集大小。记 R_i 为给定原 SPE 在该固定前缀后观察到 T_i 时的真实末位回复。定义

\[
U_p(X,Y)=\sum_{x\in X}\frac1{p_x+1+1_Y(x)}.
\]

真实末两人收益 u_A=U_p(A,B)、u_B=U_p(B,A)。以下全部是真实最优性给出的非负量：

\[
S=\sum_i[u_A-U_p(T_i,R_i)]\ge0,
\]

\[
Z=\sum_i[u_B-U_p(R_i,A)]\ge0,
\]

\[
V=\sum_{i\ne j}[U_p(R_i,T_i)-U_p(R_j,T_i)]\ge0.
\]

S 在实际倒数第二节点比较 T_i；Z 在实际末位节点比较 R_i；V 在真实历史 (原前缀,T_i) 的末位节点比较合法主题 R_j。相同 T_i 的历史及其 R_i 自然一致，证明不要求标签互异或计数 Markov 策略。

使用统一非负组合

\[
G=S+\frac1{2m}Z+\frac1mV\ge0.\tag{1}
\]

V 是全部 m(m−1) 个有序比较的和，没有额外平均归一化。

## 逐客户恒等式与消去交集

固定客户，记 a=1_A,b=1_B，p 为原前缀负载，d=Σ_i1_{T_i}, ell=Σ_i1_{R_i}, h=Σ_i1_{T_i}1_{R_i}，o=1_{d>0}，w=1_{p+a+b>0}。记该客户给真实末两人的份额为 α=a/(p+a+b)、β=b/(p+a+b)，零分子定义为零。D=(p+1)(p+2)。直接展开

\[
S_x=m\alpha-\frac d{p+1}+\frac hD,
\qquad
Z_x=m\beta-\frac{\ell}{p+a+1},
\qquad
V_x=\frac{d\ell-mh}{D}.
\]

因此 h 项严格消去，

\[
G_x=m\alpha+\frac\beta2-\frac d{p+1}
-\frac{\ell}{2m(p+a+1)}+\frac{d\ell}{mD}.
\]

令

\[
\rho=2w-o-m\alpha-\frac\beta2+\frac d{p+1}
+\frac{\ell}{2m(p+a+1)}-\frac{d\ell}{mD}.
\tag{2}
\]

即有精确恒等式

\[
2W-O=G+\sum_x\rho_x.\tag{3}
\]

## 全部参数的非负证明

### a=0,p=0

式 (2) 为

\[
\rho=\frac32b-o+d+\frac{\ell(1-d)}{2m}.
\]

d=0 时非负；1≤d≤m 时，ell≤m 给 rho≥3b/2+(d−1)/2≥0。

### a=0,p≥1

此时 w=1，α=0，0≤β≤1，且

\[
\frac d{p+1}-\frac{d\ell}{m(p+1)(p+2)}
=\frac d{p+1}\left(1-\frac\ell{m(p+2)}\right)\ge0.
\]

式 (2) 余下的 ell 项非负，故 rho≥2−o−β/2≥1/2。

### a=1

假设 (H) 强制 p=m−2，w=1，α=1/(m−1+b)，β=b/m。因此

\[
\rho=2-o-\frac m{m-1+b}-\frac b{2m}
+\frac d{m-1}
+\frac{\ell(m-1-2d)}{2m^2(m-1)}.
\tag{4}
\]

当 d=0，式 (4) 关于 ell 递增；b=0 的最小值为 (m−2)/(m−1)，b=1 的最小值为 1−1/(2m)，均非负。

当 1≤d≤m，式 (4) 关于 (d,ell) 双线性，矩形 [1,m]×[0,m] 的最小值在四个角点。全部八个角值如下：

| b | d=1,ell=0 | d=1,ell=m | d=m,ell=0 | d=m,ell=m |
|---|---|---|---|---|
|0|0|(m−3)/(2m(m−1))|1|1−(m+1)/(2m(m−1))|
|1|(m+1)/(2m(m−1))|1/m|m/(m−1)−1/(2m)|1|

对全部整数 m≥3 这些值非负。最后一项在 b=0 时有分子 2m²−3m−1=2(m−3)²+9(m−3)+8>0。故所有客户均有 rho≥0。

式 (3) 完成对任意比较元组 O 的半覆盖证明，再取最大值得目标结构结论。零客户、空主题、重复主题及任意历史平局均被同一非严格恒等式包括。

## 机制、意义与剩余缺口

这个证明不把高末位收益用一个全局标量支付。它通过同一原前缀下 m 条真实 T_i→R_i 菜单及其两两最优性消去交集 h；假设 (H) 只在 A 客户上的背景 p=m−2 一处承重。早期不同超集已经覆盖的额外客户得到正余项。

对一般实际前缀，a=1 时 p 可能显著小于 m−2，式 (4) 中 mα 无法由两个实际覆盖单位支付。例如 p=0,b=0,d=1,ell=0 时，rho=2−m，m≥3 为负。因此直接删去 (H) 无法延伸此证书；这只是本证书的机制边界，并非反例或一般定理不可能。

下一步应结合较早节点的真实回复支付这些低负载 A 客户；只增加末位主题收益的标量预算不是本证明的延伸。

## 证据、身份与接续

正式身份为 `CA-COMMON-PENULTIMATE-HALF-v1`；个人发现稿原临时标签
`B1-COMMON-PENULTIMATE-HALF-v1`指同一陈述，不改变任何量词或假设。
[独立审查](../../reviews/customer_attraction/penultimate_menu_half.md)逐条核对同一原策略的真实比较，
并从定义重算全部余项。仓库根运行：

```sh
python3 tests/audits/customer_attraction_common_penultimate.py
```

默认只打印；`--output`拒绝覆盖。冻结结果位于
`evidence/runs/2026-10-21/customer_attraction_common_penultimate.json`。
有限检查审计公式，任意人数结论来自上面的显式非负证明。

新的[少量早期遗漏平方阈值定理](penultimate_few_exceptions.md)加入早期角色与实际末位的联合比较，
放宽共同包含条件；它有独立身份和明确阈值。
发现与审查来源保存在个人区
`research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/direct_global/`
及同工作区`independent_review/`。外审、新颖性及锐性未认证。
