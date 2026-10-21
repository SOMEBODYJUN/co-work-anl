# 静态安全值下界的精确亏量、锐性刚性与纯背景舍入

2026-10-21。对象完全为仓库 CAG-MODEL：有限共同非空主题目录、有限单位客户、n≥1名单位提供者。这里的结果只关于**不观察随机查询的静态安全值**，不假设顺序均衡，亦不推出一般Q-CAG-HALF或任何新的SPE收益保底。解析证明见下文，不以有限扫描为依据。此稿由security_induction撰写，等待母代理独立数学审查；没有外部审查或新颖性认证。

本稿细化现行 `research/current/customer_attraction/oblivious_security.md` 中 minimax、Jensen及共同目录预算的证明：同一非负链的全部松弛可以精确分开，从而推出安全下界取等时的唯一对偶负载及一个定量纯背景舍入界。原静态下界和有限minimax不是此稿新增主张。

## Claim S1：全部亏量的非负精确分解

固定n≥1。主题A与n−1个静态竞争主题组成的有序元组B的查询收益为

\[
f_B(A)=\sum_{x\in A}\frac1{1+H_x(B)},\qquad
v=\max_p\min_B\mathbb E_{A\sim p}f_B(A)
 =\min_Q\max_A\mathbb E_{B\sim Q}f_B(A).
\]

每个p为目录上的概率分布，每个Q为全部合法n−1主题元组上的联合概率分布，B不观察A的抽样。n=1时竞争元组只有空元组。

令O=OPT_n，并**任取**一个达到O的比较元组T_1,…,T_n；令C为其并集，d_x为它在客户x上的覆盖次数。再**任取**一个达到上述对偶最小值的Q。以下所有量依这个Q及比较元组定义：

\[
L_x=\mathbb E_QH_x,
\quad g(A)=\sum_{x\in A}\frac1{1+L_x},
\quad F(A)=\mathbb E_Q f_B(A),
\quad\delta_A=v-F(A),
\quad J_A=F(A)-g(A).
\]

对偶最优性给每个δ_A≥0；Jensen给每个J_A≥0。当n>1时，令q_A为Q中主题A的期望份数除以n−1。因此q为目录分布，且L_x=(n−1)Σ_{A∋x}q_A。n=1时任取一个q；一切含q的项都乘零。

逐客户记

\[
j_x=\mathbb E_Q\frac{(H_x-L_x)^2}{(1+L_x)^2(1+H_x)},
\quad
R_{\rm ov}=\sum_{x\in C}\frac{d_x-1}{1+L_x},
\quad
R_{\rm out}=\sum_{x\notin C}\frac{L_x}{1+L_x}.
\]

这些量均非负；令R=R_ov+R_out、Δ=(2n−1)v−O。则

\[
\boxed{J_A=\sum_{x\in A}j_x,}\tag{1}
\]

\[
\boxed{
\Delta=R+\sum_{j=1}^n(\delta_{T_j}+J_{T_j})
 +(n-1)\sum_Aq_A(\delta_A+J_A).
}\tag{2}
\]

**证明。** 对a=1+L>0、h=H−L使用恒等式

\[
\frac1{a+h}=\frac1a-\frac h{a^2}+\frac{h^2}{a^2(a+h)}.
\]

取期望后线性项消失，得到(1)。另一方面，逐客户求和直接得到

\[
\sum_jg(T_j)+(n-1)\sum_Aq_Ag(A)
=\sum_x\frac{d_x+L_x}{1+L_x}=O+R.
\]

因g(A)=v−δ_A−J_A，移项即得(2)。这同时重新证明Δ≥0，即已有的v≥O/(2n−1)。Q最优这一量词不可删：任意Q的cap未必等于v，也不能一概令δ_A≥0。

例如，令J_C=Σ_{x∈C}j_x，则(2)给R_out+J_C≤Δ，因为d_x≥1于C。还可直接读出

\[
\sum_{x\in C}(d_x-1)\le n\Delta,
\qquad \sum_{x\in C}\operatorname{Var}_Q(H_x)\le n^3\Delta,
\qquad
\mathbb E_Q|\{x\notin C:H_x>0\}|\le nR_{\rm out}.
\tag{3}
\]

前三式分别使用1+L_x≤n、(1+L_x)^2(1+H_x)≤n³，以及Pr(H_x>0)≤L_x≤nL_x/(1+L_x)。这些是定量必要条件，不是SPE预算。

## Claim S2：下界取等强制纯对偶最优背景和唯一最优负载

假设Δ=0，即v=O/(2n−1)。则对于**每个**最优比较元组和**每个**最优对偶Q：

1. d_x=1于C，即比较主题按客户集合两两不交；重复的空主题无妨。
2. Q几乎必然有H_x=L_x于每个x∈C；每个x∉C则H_x=0。因此Q支持中的每个背景具有相同的整个客户负载向量L，且每个支持主题包含于C。
3. 任取Q支持中的B，均有f_B(A)=g(A)≤v于全部合法A，且max_A f_B(A)=v。因此存在纯对偶最优背景，且θ_n=min_B max_A f_B(A)=v。
4. 每个比较主题T_j都有g=v；当n≥2时，q支持中的每个主题A也都有g=v。

**证明。** (2)的每项非负，所以R_ov=R_out=0且J_{T_j}=δ_{T_j}=0。第一项给d=1于C；R_out=0给L=0于C外，非负H遂几乎必然为零。Σ_jJ_Tj=Σ_Cd_xj_x=0给每个x∈C的j_x=0，而(1)中分母严格正，所以H_x=L_x几乎必然。客户有限，故可取共同概率一事件，其中每个客户负载都固定；支持中每个正概率背景均处于此事件。于是全部A的查询值逐一固定为g(A)=F(A)≤v。δ_Tj=0确保max为v，包括v=0情形。最后一点由(2)直接得到。

### 显式原始最优分布及全部最坏回复的刚性

在同一Δ=0假设下，定义合法目录分布

\[
\boxed{p_A=\frac{\#\{j:T_j=A\}+(n-1)q_A}{2n-1}.}\tag{4}
\]

其客户包含率于C为(1+L_x)/(2n−1)，于C外为零。它是安全值最优分布。更强地，对任意合法背景B′、其客户负载h_x，有以下**精确非负分解**：

\[
\boxed{
\mathbb E_{A\sim p} f_{B'}(A)-v
=\frac1{2n-1}\left[
 \sum_{a\in B'}(v-g(a))
 +\sum_{x\notin C}h_x
 +\sum_{x\in C}\frac{(h_x-L_x)^2}{(1+L_x)(1+h_x)}
\right].
}\tag{5}
\]

主题在B′中的份数按重数保留。证明只需逐客户恒等式

\[
\frac{1+L}{1+h}
=1+\frac{L-h}{1+L}+\frac{(h-L)^2}{(1+L)(1+h)}
\]

以及Σ_C L/(1+L)=(n−1)Σq_Ag(A)=(n−1)v、Σ_C h/(1+L)=Σ_{a∈B′}g(a)−Σ_{x∉C}h_x。把它们代入由(4)给出的查询期望，再使用O=(2n−1)v，即得(5)。

(5)的全部项均非负，所以p保证v；Q已有cap v，故p最优。又若h=L于全部客户，则左侧为零；反向左侧为零时平方项与C外项强制h=L。因此该p的**全部纯最坏回复恰为客户负载等于L的背景**。

这还推出：全体最优对偶分布的客户负载向量L唯一。确实，任取另一个最优Q′，对p的查询期望既至少v，又由Q′的全部纯查询cap≤v而至多v；Q′支持中的每个纯背景都必须使(5)取等，故其负载等于原来的L。这里唯一的是客户负载，不是主题计数或有序元组；不同主题组合可以产生相同客户负载。

## Claim S3：近锐安全值的定量纯背景舍入

不再假设Δ=0，仍取Claim S1中的任意最优比较元组和任意最优Q。令

\[
J_C=\sum_{x\in C}j_x,
\qquad F_C=\mathbb E_Q\sum_{x\in C}\frac1{1+H_x}.
\]

则F_C≤nv，且Q支持中存在一个合法纯背景B满足

\[
\boxed{
\max_A f_B(A)
\le v+R_{\rm out}+\frac{J_C+\sqrt{J_CF_C}}2.
}\tag{6}
\]

特别地，

\[
\boxed{
0\le\theta_n-v
\le\Delta+\frac12\sqrt{nv\Delta}.
}\tag{7}
\]

**证明。** 由于d_x≥1于C，F_C≤Σ_jF(T_j)≤nv。对每个客户写

\[
D_x(B)=\frac1{1+H_x(B)}-\frac1{1+L_x}.
\]

记正部为D_x^+=max(D_x,0)。对每个B、每个A同时有

\[
f_B(A)\le g(A)+\sum_{x\in C}D_x^+
 +\sum_{x\notin C}D_x^+
\le v+\sum_{x\in C}D_x^++R_{\rm out}.
\tag{8}
\]

最后一步使用g(A)≤F(A)≤v及逐点D_x^+≤L_x/(1+L_x)。另一方面，E_QD_x=j_x，故

\[
\mathbb E_Q\sum_{x\in C}D_x^+
=\frac12\left[J_C+\mathbb E_Q\sum_{x\in C}|D_x|\right].
\]

Cauchy不等式先用于每个客户的随机性，再用于客户之和，给

\[
\begin{aligned}
\mathbb E_Q|D_x|
&\le\sqrt{j_x\,\mathbb E_Q\frac1{1+H_x}},\\
\mathbb E_Q\sum_{x\in C}|D_x|
&\le\sqrt{J_CF_C}.
\end{aligned}
\]

其中第一步使用

\[
|D_x|=\sqrt{
 \frac{(H_x-L_x)^2}{(1+L_x)^2(1+H_x)}
 \frac1{1+H_x}}.
\]

对(8)先取全部A的最大值，再取Q期望，得到(6)右侧作为期望cap上界；有限支持中必有一个B的cap不超过该平均。由R_out+J_C≤Δ、F_C≤nv即得(7)。下界θ_n≥v为通常弱minimax。

## 全部退化边界与SPE使用限制

n=1时Q仅为空元组、L=H=0、J=R=Δ=0，v=θ_1=O。Claim S2的p为任一最大主题的点质量；(5)两边都为零；(6)--(7)原样成立。无需定义除以n−1的q。

若O=0，则所有主题均无客户，v=θ_n=0，C为空。不可被任何主题覆盖的客户可以保留，它们H=L=d=0。所有和式为零，(4)仍为总质量一的目录分布。反之v=0由已有静态下界必有O=0。因此从未除以O、v、Δ、J_C或F_C；零值时根号为零。空主题、重复主题、同覆盖不同标签与任意最优比较元组均被原和式覆盖。

这些结果不把纯minimax背景当成顺序均衡的实际前缀，也不证明一般纯SPE逐人u_i≥v、聚合W≥nv或W≥nθ_n。已有aggregate-θ反例没有与本稿冲突：其v严格低于θ_n。下一步真正缺的是让完整历史上的真实SPE偏离支付上述静态刚性结构；额外主题仍可任意交叠，最优元组不交不能被偷换成整个目录不交。

一个可用但条件明确的静态推论是：在Δ=0且某完整SPE实际前n−1个行动恰有负载L时，末位BR收益为v，每个前缀主题的g值为v，而每个先前玩家的最终分母H_x+1_{末位覆盖x}≤H_x+1，故其实际收益≥g(自身主题)=v。于是该SPE满足W≥nv。这里只处理实际前缀已经是纯minimax背景的条件情形，不能无条件外推。

## 独立审查状态与接续

母代理已分别独立重构(2)、正部Cauchy舍入、(4)--(5)和唯一对偶负载，并指出初稿n=1的q支持量词需限定n≥2；本版已修。全部解析结果尚待最终审计与正式入库，不提前提升共享Claim。本文只在本研究员工作区写入。探索程序的有限无反例结果与本解析证明无依赖关系。
