# 混合设施重数与受限相关并行链：精确接口边界

**记录日期：** 2026-10-04
**状态：** 研究障碍与开放义务；不是全输入算法，也不是困难性定理。

## 1. 固定占位下真正需要求解的子问题

固定一个贪心占位。对每个已占地点 \(t\)，设 \(q_t\ge 1\) 为设施数；把客户分配到一个已占地点，令该地点的客户总重为 \(W_t\)。若客户 \(i\)（重 \(w_i\)）当前在 \(t\)，并可改去另一个已占地点 \(v\)，则在地点内对 \(q_t\) 家设施作独立均匀随机化时，精确客户 NE 的必要且充分条件是

\[
       \frac{W_t-w_i}{q_t}\le \frac{W_v}{q_v}.
       \tag{RQ}
\]

这是直接由 MF-MODEL 的条件成本得到的：当前设施的成本为
\(w_i+(W_t-w_i)/q_t\)，目标地点任一设施的成本为
\(w_i+W_v/q_v\)。因此，总目标的未解接口可以明确写成：在给定贪心占位和负载盒
\(q_t\gamma\le W_t\le(q_t+1)\gamma\)（或等价的可用离轨证书）下，输入任意受限选项集，构造满足 (RQ) 的站点分配。

## 2. 可以严格复用的等重数情形

若所有相关地点的重数相同，即 \(q_t=q\)，(RQ) 约化为

\[
             W_t-w_i\le W_v.
\]

这正是受限**相同**并行链/相同机器调度的纯 NE 条件。Gairing、Lücking、Mavronicolas、Monien 的 blocking-flow Nashification 可以从任意给定分配出发，在多项式时间内得到纯 NE，并保持原来的最大负载不增；仓库中的等重数、全异址和等重数分量定理均只在这个接口上调用该结果。

## 3. 不能把“相关并行链”结果直接套进来

受限相关并行链通常用链速度 \(s_t\) 定义客户在 \(t\) 的延迟为总重除以速度；其纯 NE 比较是

\[
             \frac{W_t}{s_t}
             \le \frac{W_v+w_i}{s_v}.
             \tag{RL}
\]

把 \(s_t=q_t\) 代入 (RL) 并不能得到 (RQ)：(RQ) 中客户自己的重数折扣除以**源**地点的 \(q_t\)，而 (RL) 把新客户加到**目标**地点并除以 \(s_v\)。例如取

\[
 q_t=1,\quad q_v=2,\quad w_i=2,\quad W_t=5,\quad W_v=6.
\]

在本模型中，客户从 \(t\) 到 \(v\) 的比较是
\[
 (5-2)/1=3\quad\text{与}\quad 6/2=3,
\]
所以没有严格改善；相关链比较则是
\[
 5/1=5\quad\text{与}\quad (6+2)/2=4,
\]
所以严格改善。这个正整数局部数据已经足以否定“只把地点重数当相关链速度”的直接归约。

反方向的结论也同样不能偷用：相关链的近似排程结果并不自动产生满足 (RQ) 的**精确**站点客户 NE。重数相等时二者一致；重数混合时必须重新证明 blocking-flow 不变量，尤其要处理源客户自重折扣、跨重数返回和负载盒同时保持。

## 4. 文献边界与本项目的精确缺口

上述受限并行链论文明确给出受限相同链的多项式 Nashification，并把受限相关链的精确 NE 计算列为尚未解决的延伸；它只给相关链的社会成本近似。这个事实不能被升级为本模型的复杂度下界，因为本模型的条件 (RQ) 与 (RL) 不同；它能支持的结论是：现有已发表 flow 子程序的适用域在混合 \(q_t\) 处确实结束。

因此，当前最窄且可复核的算法义务是：

> **RQ-MIXED-BOX：** 对贪心产生的任意显式正有理占位，若每个站点满足贪心负载盒，能否在输入位长多项式时间构造满足 (RQ) 的站点分配，或给出一个新的在轨/离轨证书绕开这个盒内选择？

已有的 `SC-K-RANGE-GREEDY-2`、`SC-K-TWO-SITE-COMPONENT-GREEDY-2`、`SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2`、`SC-K-NESTED-ANCHOR-GREEDY-2`、`SC-K-UNIFORM-LIGHT-FLOW-2` 和稀疏关联 DP 都是 RQ-MIXED-BOX 的严格子类。它们不能合并成一般证明；三站以上、混合重数、部分交叠且轻客户重数不同时仍是开放范围。

本记录排除了一个具体的错误 import 路线，但没有证明 RQ-MIXED-BOX 困难，也没有降低任意 \(k\) 因子 2 目标的数学真值。下一步若继续沿 flow 路线，必须先写出适用于 (RQ) 的阻塞流不变量；若不能，应该转向新的占位机制或只控制偏离设施的证书。

## 来源与审查状态

- Gairing–Lücking–Mavronicolas–Monien, *Computing Nash Equilibria for Scheduling on Restricted Parallel Links*, STOC 2004 / Theory of Computing Systems 2010：受限相同链的多项式 Nashification，以及相关链精确计算仍未闭合的范围说明。论文入口：<https://cgi.csc.liv.ac.uk/~gairing/publications/2004-stoc.pdf>。
- 本页的公式 (RQ)、(RL) 和反例只使用整数算术；独立脚本为 `tests/audits/restricted_related_formula.py`。
- 外部同行评审、优先权核查和对 RQ-MIXED-BOX 的复杂度结论均未完成。
