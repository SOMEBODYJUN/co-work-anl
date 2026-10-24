# 最优首动作菜单：真实孩子机会损失与无重复信用恒等式

2026-10-24。对象为一般 **Q-CAG-HALF**：任意有限单位客户、有限非空共同主题目录、任意单位提供者人数及每份完整有序历史依赖纯 SPE。允许空主题、重复行动、零客户和任意历史平局。

**身份：CA-OPTIMAL-FIRST-ACTION-BRANCH-GAP-v1。** 本文给出从单一真实当前 IC 和静态同尾补全可推出的全输入精确恒等式及其非负余项。Boss21、recurrence2、exchange2 已各自从覆盖与分享定义重构。独立内部审查另列，外部同行审查与新颖性未认证。它加强并简化了最优补全私有块的交换债务关系，但**未支付不同真实孩子的总机会损失，未闭合 half**。没有使用 half、归纳假设、静态均衡或后继冻结。

## 1. 一个完整有序历史及其最优首动作菜单

固定任意原模型实例和任意一份完整纯 SPE \(\sigma\)。取任意合法完整有序历史 \(h\)，尚余 \(r\ge1\) 人；过去主题并集为 \(P\)，过去客户负载为 \(b_x\)。记当前按 \(\sigma\) 选择的主题为 \(S\)，当前在从 \(h\) 沿 \(\sigma\) 所得完整终局的收益为 \(u\)。这里 \(S,u\) 都属于这个精确的有序历史，不把同负载历史合并。

对任意客户集 \(Q\) 及整数 \(k\ge0\)，定义总覆盖最优补全

\[
F_k(Q)=\max_{T_1,\ldots,T_k\in\mathcal S}
 \left|Q\cup\bigcup_{\ell=1}^kT_\ell\right|,
\qquad F_0(Q)=|Q|.
\]

写

\[
G=F_r(P),\qquad H=F_{r-1}(P\cup S),\qquad
\delta=G-H\ge0.
\]

定义**最优首动作菜单**

\[
\mathcal A^*(h)=\{A\in\mathcal S:
F_{r-1}(P\cup A)=G\}.
\tag{1}
\]

有限目录保证最优补全存在，故菜单非空。它恰是至少出现在某个最优 \(r\) 元组中的主题集合。因为 \(S\) 是实际动作而非覆盖最大化动作，不能默认 \(S\in\mathcal A^*(h)\)；准确地说，\(S\in\mathcal A^*(h)\) 当且仅当 \(\delta=0\)。

固定任意 \(A\in\mathcal A^*(h)\)。在**同一份原策略**中，只强制当前玩家改选 \(A\)，以后全部沿原 \(\sigma\)；记其真实 \(r-1\) 个后继主题的并集为 \(Y_A\)，偏离者收益为 \(d_A\)。过去主题仍为原来的 \(h\)。真实当前 IC 给

\[
\Gamma_A=u-d_A\ge0.
\tag{2}
\]

后继随 \(A\) 任意改变，并且每个后继历史的原 SPE 最优性全部保留；本文没有将它们替换成实际 \(S\) 孩子的规定动作。

## 2. 全部非负信用的定义

定义

\[
\begin{aligned}
\rho_A&=G-|P\cup A\cup Y_A|,\\
M_A&=|A\setminus(P\cup S)|,\\
t_A&=|A\setminus(P\cup S\cup Y_A)|,\\
f_A&=|S\setminus(P\cup A\cup Y_A)|,\\
\theta_A&=M_A-\delta,\\
\xi_A&=H-|P\cup S\cup Y_A|,\\
\eta_A&=r d_A-M_A-(r-1)t_A.
\end{aligned}
\tag{3}
\]

所有这些量均非负。除 \(d_A,\Gamma_A,\eta_A\) 可为有理数外，其余为非负整数。逐项说明：

- \(\rho_A\ge0\)，因为 \((A,Y_A)\) 是从 \(P\) 出发的合法 \(r\) 槽补全；由 \(A\in\mathcal A^*(h)\)，它同时等于强制 \(A\) 后真实孩子的覆盖机会损失
  \(F_{r-1}(P\cup A)-|P\cup A\cup Y_A|\)。
- \(\xi_A\ge0\)，因为 \(Y_A\) 的 \(r-1\) 个真实主题在背景 \(P\cup S\) 下也是静态合法补全。\(\xi_A\) 只描述把这个主题元组搬到背景 \(S\) 后的**静态**补全松弛；它通常不等于实际 \(S\) 孩子的机会损失，也没有声称搬动后的动作仍然是 SPE。
- \(\theta_A\ge0\)：取任意与 \(A\) 合成最优 \(r\) 元组的 \(r-1\) 个主题 \(T\)。将 \(A\) 换成 \(S\) 最多失去 \(M_A\) 个客户，故
  \(H\ge|P\cup S\cup T|\ge G-M_A\)，即 \(\delta\le M_A\)。
- \(t_A\le M_A\)，且这 \(t_A\) 个客户既无过去覆盖，也无后继覆盖，每个全归当前偏离者。其余 \(M_A-t_A\) 个客户没有过去覆盖，最终负载至多 \(r\)，故其当前份额至少 \(1/r\)。\(A\cap(P\cup S)\) 上的收益非负。因此

  \[
  d_A\ge t_A+\frac{M_A-t_A}{r},
  \qquad \eta_A\ge0.
  \tag{4}
  \]

\(M_A\) 包含 \(A\) 内相对 \(P\cup S\) 的**全部新客户**，不只某个最优比较元组中的私有客户。因此其定义不依赖选了哪一个包含 \(A\) 的最优补全。

## 3. 精确恒等式及可直接引用的不等式

两个同尾并集的大小之差精确为

\[
|P\cup A\cup Y_A|-|P\cup S\cup Y_A|=t_A-f_A.
\]

代入 \(G-H=\delta\) 得

\[
\boxed{\delta=\rho_A+t_A-f_A-\xi_A.}
\tag{5}
\]

另一方面，(3) 的分享余项和真实 IC 给

\[
r u=M_A+(r-1)t_A+\eta_A+r\Gamma_A.
\tag{6}
\]

使用 \(M_A=\delta+\theta_A\)，并用 (5) 消去 \(t_A\)，得到本文主关系

\[
\boxed{
r(\delta-u)
=(r-1)\rho_A-\theta_A-(r-1)f_A
 -(r-1)\xi_A-\eta_A-r\Gamma_A.
}
\tag{7}
\]

所有被扣项均来自同一个当前完整收益或静态交换松弛，没有把 \(u\) 重复付给多个客户块。特别地，丢弃 \(\xi_A,\eta_A\) 给

\[
\boxed{
\delta-u\le\frac{r-1}{r}\rho_A
-\frac{\theta_A}{r}
-\frac{r-1}{r}f_A-\Gamma_A.
}
\tag{8}
\]

若只需较短引用，还可丢弃 \(f_A\)，保留
\(\delta-u\le(r-1)\rho_A/r-\theta_A/r-\Gamma_A\)。\(\rho_A\) 必须始终是原策略强制 \(A\) 后的真实孩子损失。

## 4. 与最优补全私有块信用的关系

任取含 \(A=T_j\) 的最优 \(r\) 元组，按
[来源交换债务分解](../../workspaces/customer-attraction/R-2f6cae284faf43fea7a09c0a4fe7c679/branch_budget/optimal_completion_exchange_debt.md) 定义其比较元组私有块 \(D_j\)、目录外收益 \(e\) 和单交换松弛 \(\varepsilon_j\)。其恒等式为

\[
|D_j\setminus S|=\delta+e+\varepsilon_j.
\]

由于 \(D_j\setminus S\subseteq A\setminus(P\cup S)\)，本文保留的信用满足

\[
\boxed{\theta_A\ge e+\varepsilon_j.}
\tag{9}
\]

因此 (8) 逐动作不弱于只扣 \((e+\varepsilon_j)/r\) 的对应 \(\rho\) 界，并且不再依赖比较元组的选择。不能把 \(\theta_A\) 与 \(e+\varepsilon_j\) 再相加；后者已经包含在前者中。

## 5. 非均匀选择及全路径共同支付的准确剩余义务

对 \(\mathcal A^*(h)\) 上任意概率分布 \(p\)，(7) 可取期望。不同有序历史可采用完全不同的 \(p\)，不对真实策略作任何随机化。选最优补全再非均匀选槽位所产生的任何动作分布，都只是此菜单上的一种 \(p\)；\(\rho_A,\theta_A,\xi_A,\eta_A,\Gamma_A\) 均只由历史和动作 \(A\) 决定。

在原根 SPE 的实际路径上，记 \(r_i=m-i+1\)。每位置任取其菜单分布 \(p_i\)，则最优补全机会损失望远镜与 \(\sum_i u_i=W\) 给

\[
\begin{aligned}
\operatorname{OPT}_m-2W
=\sum_i\Big[&\frac{r_i-1}{r_i}\mathbb E\rho_{i,A}
-\frac{\mathbb E\theta_{i,A}}{r_i}
-\frac{r_i-1}{r_i}\mathbb E f_{i,A}\\
&-\frac{r_i-1}{r_i}\mathbb E\xi_{i,A}
-\frac{\mathbb E\eta_{i,A}}{r_i}
-\mathbb E\Gamma_{i,A}\Big].
\end{aligned}
\tag{10}
\]

(10) 精确保留全部信用，故右侧与分布选择无关；声称其非正仍是原 half 问题本身。一个更强、尚未证明的充分支付义务是能选择 \(p_i\) 使

\[
\sum_i\frac{r_i-1}{r_i}\mathbb E\rho_{i,A}
\le
\sum_i\left[\frac{\mathbb E\theta_{i,A}}{r_i}
+\frac{r_i-1}{r_i}\mathbb E f_{i,A}
+\mathbb E\Gamma_{i,A}\right].
\tag{11?}
\]

本文没有证明 (11?)。不同 \(\rho_{i,A}\) 来自不同真实孩子；不能将其尾利润或覆盖损失直接替换为实际路径的对应量。选菜单、最优补全或非均匀分布本身不提供跨枝付款。

## 6. 任意合法动作的带覆盖损失版本

若要比较一个不属于最优首动作菜单的合法动作 \(A\)，仍沿原 \(\sigma\) 定义 \(Y_A,d_A,\Gamma_A,M_A,t_A,f_A,\xi_A,\eta_A\)，但改记

\[
G_A=F_{r-1}(P\cup A),\qquad
\lambda_A=G-G_A\ge0,\qquad
R_A=G_A-|P\cup A\cup Y_A|\ge0,
\]

\[
\widehat\theta_A=M_A+\lambda_A-\delta\ge0.
\tag{12}
\]

最后一个非负性来自取实现 \(G_A\) 的 \(r-1\) 尾元组，并把 \(A\) 换成 \(S\)：\(H\ge G_A-M_A\)。\(\lambda_A\) 是强制 \(A\) 的第一步静态覆盖机会损失；\(R_A\) 是其真实孩子之后的机会损失，两者须分开。

同样的逐客户与同尾代数精确给

\[
\boxed{
r(\delta-u)=r\lambda_A+(r-1)R_A-\widehat\theta_A
 -(r-1)f_A-(r-1)\xi_A-\eta_A-r\Gamma_A.
}
\tag{13}
\]

当 \(A\in\mathcal A^*(h)\) 时，\(\lambda_A=0\)、\(R_A=\rho_A\)，退回 (7)。特别地，当前按策略选的 \(S\) 一般有 \(\lambda_S=\delta\)，不能在 (13) 中漏掉这份覆盖损失。此扩展允许追踪一个高收益后继主题是否落在菜单外，但没有免费消掉其 \(\lambda_A\)。

## 7. 边界

当 \(r=1\) 时 \(Y_A=\varnothing\)、\(\rho_A=0\)、\(\xi_A=0\)。菜单动作 \(A\) 最大化 \(|P\cup A|\)，但当前玩家按带旧背景分母的收益最优，不一定选择菜单动作。此时 \(\eta_A=d_A-M_A\ge0\)，(7) 精确为 \(\delta-u=-\theta_A-\eta_A-\Gamma_A\)，故末期机会损失由当期收益支付。

客户全零时所有集合计数和收益为零，所有式子按乘法不等式或恒等式成立，不定义效率比。空主题、空的 \(M_A,t_A,f_A\)、重复最优主题与重复后继均未被排除；所有并集及逐客户分母证明仍有效。固定历史可以离轨；(2) 由完整 SPE 在该精确历史保证，其后继保持原有有序历史依赖和平局。

**当前下一步。** 需要利用真实后继 IC 证明类似 (11?) 的共同付款，或保留 \(\xi,\eta\) 构造更弱而可闭合的总账；不能由本恒等式反向假设 half 已成立。

## 来源与审查

原始推导：[最优首动作菜单工作稿](../../workspaces/customer-attraction/R-2f6cae284faf43fea7a09c0a4fe7c679/exchange2/optimal_first_action_menu_credit.md)，以及[私有块版本独立重构](../../workspaces/customer-attraction/R-2f6cae284faf43fea7a09c0a4fe7c679/recurrence2/child_loss_recurrence.md)。[内部解析审查](../../reviews/customer_attraction/optimal_first_action_branch_gap.md)区分一般代数、真实IC、非均匀选择与尚未支付的共同预算。没有新增有限扫描或计算证明声明。
