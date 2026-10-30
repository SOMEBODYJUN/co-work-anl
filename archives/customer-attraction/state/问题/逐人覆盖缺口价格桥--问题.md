---
id: "customer-attraction/individual-deficit-price-bridge-open"
kind: "open-problem"
type_tag: "问题"
title: "逐人覆盖缺口价格桥"
status: "open"
truth_status: "candidate-sufficient-bridge-not-proved"
review_level: "full-source-read-and-related-budget-comparison"
scope: "任意有限共同目录、任意人数、完整有序历史纯SPE；候选逐人B(u_i)≤W及其整数特例；不把有限探针当证明"
summary: "候选若每个实际位置都能用实际福利支付其逐人覆盖价格缺口B(u_i)，则直接推出half；末位和倒二已有条件接口，最小收益早期位置的真实偏离后继付款仍未闭合。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-077c0cacfba24288be91dee1acf6d484/terminal_menu/individual_deficit_candidate.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-077c0cacfba24288be91dee1acf6d484/terminal_menu/individual_deficit_candidate.md"
---

# 逐人覆盖缺口价格桥

这是一个仍开放的充分桥候选。它把“每个实际位置都能支付一份覆盖缺口”与 \(\operatorname{OPT}_m\le2W\) 直接连接起来，同时明确当前证明缺在哪里。候选本身不是结论，也没有因为有限 LP 探针未发现负值而变成定理。

## 1. 分数价格定义与充分性

对任意非负目录权重 \(z\)，定义
\[
C(z)=\sum_x\min\!\left(1,\sum_{T\ni x}z_T\right),\qquad
\tau=\sum_Tz_T,
\]
以及
\[
B(t)=\sup_{z\ge0}\{C(z)-t\tau\}.
\]
目录有限时这是一个有限线性规划；对偶可写为寻找 \(0\le y_x\le1\)，使每个主题的剩余价值
\[
\sum_{x\in T}(1-y_x)\le t
\]
且 \(\sum_xy_x\) 尽量小。价格 \(y\) 只是静态分数向量，不要求来自真实竞争主题分布、独立查询或合法偏离。

候选桥是：每个实际位置 \(i\) 都满足
\[
B(u_i)\le W. \tag{D}
\]
取 \(m\) 个最优主题的整数权重 \(z_T\in\{0,1\}\)，则 \(\tau=m\)、\(C(z)=\operatorname{OPT}_m\)，从而
\[
\operatorname{OPT}_m-mu_i\le B(u_i)\le W.
\]
取最小收益位置 \(i\)，因为 \(mu_i\le\sum_ju_j=W\)，得到
\[
\operatorname{OPT}_m\le W+mu_i\le2W.
\]
因此 (D) 是足以推出 half 的位置逐一桥。

更强地，对任意 \(k\) 个比较主题的并集覆盖量 \(O_k\)，若能证明
\[
O_k\le W+ku_i
\]
则可得到相应的 \(k\)-主题版本；它严格保留重复主题的索引权重和客户截断。

## 2. 已知末位和倒二层级

最后一人真实最佳回复给
\[
u_m=\max_A\sum_{x\in A}\frac1{b_x+1}.
\]
令 \(y_x=1-\frac1{b_x+1}\)，则每个主题的剩余价值不超过 \(u_m\)，而价格总和正好是根前缀客户的实际覆盖价值，故末位候选桥可直接建立。

倒二有更强的真实尾部投影接口：在固定前缀后的两人完整子博弈中，已有保底可给
\[
B(u_{m-1})\le W-\frac{u_m}{2}-\frac{\mathrm{fresh}(A)}4,
\]
其中 \(A\) 是倒二实际主题、fresh(A) 是其在更早前缀外的新客户数。这个接口仍只承担最后两人，不能把双线性比较自动搬到倒三或更早位置。

## 3. 真正的开放义务

在位置 \(i\) 改选主题 \(T\) 后，真实后继会形成依赖 \(T\) 的完整分支
\[
Q_{i+1}(T),\ldots,Q_m(T).
\]
当前 IC 只比较 \(u_i\) 与这条真实后继分支的收益。要证明 (D)，需要把这些不同分支共同覆盖的比较客户收费给同一份实际 \(W\) 与 \(mu_i\)，并同时保留每条后继分支自己的最佳回复。固定前缀最坏拥挤保底、固定尾深完整子树或各主题独立静态价格，都没有完成这一步。

这也解释了为什么把收益按大小排序没有解决问题：较大收益位置自动更容易满足 \(B(u_i)\le W\)，最小收益通常是更早位置，恰是后继分支最多的节点。

在静态 PNE 中可以冻结其他玩家并得更强的 \(k\)-主题式，但顺序 SPE 不能冻结后继；因此该静态推导不适用于当前全历史目标。

## 4. 真值边界与接续

已有银行目录族已经否定“所有剩余人数都逐人支付额外质量门槛”的更强普遍说法；这不否定本页的价格桥，也不证明它。前缀幽灵租金和固定尾深障碍分别否定另一些无权或弱化预算接口，不能替代对 (D) 的直接证明。

下一步若继续此问题，应构造合法完整SPE下的早期真实偏离价格、证明一个共同客户价格或其他全局对偶；任何有限浮点负值都必须有理化并逐历史验收。当前状态仍是 OPEN。
