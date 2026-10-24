# 任意路径阈值预算：独立树值重构与未闭合义务

2026-10-24。精确候选 TB-ANY，未证明、未反驳；不改变 Q-CAG-HALF 的 OPEN 状态。本页没有有限扫描或新代码证据。

## 候选及树值的准确含义

固定原 CAG-MODEL 实例与人数 m。给任意有序路径 z（不要求 SPE），位置 i 的前缀为 h_i。对合法主题 A，令 R(h_i,A) 为固定当前 A 后，全部完整可信子 SPE 所实现的完整终局集合。令

\[
L_i(A)=\min_{z'\in R(h_i,A)}u_i(z'),\qquad
\Theta(h_i)=\max_A L_i(A).
\]

候选为

\[
\operatorname{OPT}_m\le W(z)+\sum_{i=1}^m\Theta(h_i)
\quad\text{对每条任意路径 }z.
\tag{TB-ANY}
\]

\(\Theta(h)\) **恰为**历史 h 后全部纯 SPE 中当前玩家的最小可实现收益。必要性：任一 SPE 对每个孩子 A 的真实收益至少为该孩子的最小值 L(A)，所以当前最优收益至少 max L。充分性：取达到 max L 的孩子 A*，在每个孩子独立选达到 L(A) 的完整子 SPE；A* 的当前收益恰为 max L，且优于所有其他孩子，故可粘合为完整 SPE。这里子树在有序历史上独立选择，不需固定或匿名平局。

因此 TB-ANY 的 SPE 限制确实推出 half：实际每位 \(u_i\ge\Theta(h_i)\)，并且 \(\sum_i u_i=W\)。但任意路径版强于这个限制，不能免费把任意指定后缀当作可信续局。

## 任意路径的精确 Bellman 攻击

对合法主题计数前缀 k，\(\Theta(k)\) 可由全部可信续局集合计算；它依计数是因为这里取的是全部可实现集合，不是限制一份给定策略必须匿名。令

\[
J(k)=\begin{cases}
W(k),&|k|=m,\\
\Theta(k)+\min_A J(k+e_A),&|k|<m.
\end{cases}
\]

则 J(0) 恰为任意路径 TB 右端的最小值。因此一个严格 \(J(0)<\operatorname{OPT}_m\) 的完整精确见证就否定 TB-ANY，但不自动否定 Q-CAG-HALF。general_induction 分支已有该 DP 的实现和有限诊断，本分支不重复扫描。

## 最简必要子候选及已知停界

若目录含空主题，取全空路径。每个前缀的客户负载仍为零，故必要地有

\[
\operatorname{OPT}_m\le\sum_{r=1}^m\alpha_r,
\qquad \alpha_r=\min_{\sigma\in\operatorname{SPE}_r}u_1(\sigma).
\tag{NULL-PATH}
\]

右边是同一目录上不同剩余人数的真实最坏首位收益。这个子候选仍未证/未反驳；不能仅凭一份 SPE 首位低于静态安全值就否定它，其他人数可能补偿。

局部望远镜捷径 \(\Theta_r(0)\ge\operatorname{OPT}_r-\operatorname{OPT}_{r-1}\) 已被既有 61 客户 root_tax 反例击穿：r=4 时覆盖增量 10，而真实阈值为 9。本轮已把该停界告知 branch_transport，避免重新推导同一失败组件。局部失败不否定 TB-ANY 或 NULL-PATH。

目前没有从各孩子的真实 max-min 首位收益得到跨多个实际前缀的共同支付。新关系必须保留：完整孩子最优性、任意路径的后缀可能非可信、以及各前缀阈值可重新选择最坏旁枝。仅证明局部静态价格界或分别重写 \(\Theta\) 的逆向递归，尚未填补该缺口。
