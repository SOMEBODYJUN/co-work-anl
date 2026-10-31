---
id: "customer-attraction/complete-pair-incidence-lp-root-obstruction"
kind: "obstruction"
type_tag: "障碍"
title: "完全二主题关联LP根预算障碍"
status: "retained"
truth_status: "proved-template-obstruction-not-game-counterexample"
review_level: "source-read-and-exact-arithmetic-checked; no-external-review"
scope: "s≥m≥2; K_s pair-incidence maximal catalogue; empty-prefix routed LP; one-deviation/single nonnegative incidence multiplier interface"
summary: "For the complete pair-incidence family, the root LP has B(m)=ms/2 and exactly pays the union of all s maxima, so this interface has no m-theme-sensitive credit. This is a proof-interface obstruction, not a low-welfare SPE or Q-CAG-HALF counterexample."
legacy_ids:
  - "CA-PAIR-INCIDENCE-LP-OBSTRUCTION-v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/representation/complete_pair_incidence_lp_obstruction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/representation/complete_pair_incidence_lp_obstruction.md"
related_objects:
  - "../定理/极大关联LP动态预算半覆盖--定理.md"
  - "../定理/六极大无私有强化覆盖界--定理.md"
  - "../定理/九人以上六极大强化覆盖界--定理.md"
---

# 完全二主题关联LP根预算障碍

## 构造与最优的 $m$ 主题值

固定整数 $s\ge m\ge2$。对每个无序对 $1\le j<k\le s$ 放一个单位客户 $x_{jk}$，并令共同目录的 $s$ 个极大主题为

\[
B_j=\{x_{jk}:k\ne j\},\qquad j=1,\ldots,s.
\]

不加入私有客户或其他主题。每个客户恰属于两个极大主题，极大关联超图正是 $K_s$。选择 $m$ 个主题等价于选择 $m$ 个顶点；其并集覆盖全部至少一个端点的边，因此

\[
\operatorname{OPT}_m
={s\choose2}-{s-m\choose2}
=ms-\frac{m(m+1)}2.
\tag{1}
\]

当 $m=s$ 时这就是全部 $s(s-1)/2$ 个客户。

## 根 LP 的精确值

在空前缀的单偏离路由记账中取 \(p_j=0\)、剩余人数 \(r=m\)。每个极大主题的当前偏离份额为

\[
f_j(0,m)=\sum_{k\ne j}\frac1m=\frac{s-1}{m}.
\tag{2}
\]

关联 LP 对每条边 \(\{j,k\}\) 施加

\[
\beta_j+\beta_k\ge m,
\]

并最小化 $\sum_j\beta_j$。将所有 ${s\choose2}$ 条约束相加，每个 $\beta_j$ 出现 $s-1$ 次，得

\[
(s-1)\sum_j\beta_j
\ge m\frac{s(s-1)}2,
\]

所以 $\sum_j\beta_j\ge ms/2$。令所有 $\beta_j=m/2$ 即达成，故

\[
B(m)=\frac{ms}{2},\qquad D_0=B(m),\qquad
D_0\max_j f_j(0,m)=\frac{s(s-1)}2.
\tag{3}
\]

式 (3) 恰等于全部 \(s\) 个极大主题的并集大小，说明此根计数行对 \(U={s\choose2}\) 是紧的；它没有利用比较最优只允许 \(m\) 个主题这一额外上限。

## 接口层面的障碍

若尝试只用“每个行动路由到一个极大主题、当前偏离收益由 $f_j$ 控制、未覆盖比较客户由同一组非负 $\beta$ 统一付款”的模板，则其根 LP 预算被 (3) 锁定在 $ms/2$。直接使用一步预算的形式

\[
\operatorname{OPT}_m\le2m\max_j f_j(0,m)
\]

在本族中要求右侧为 $2(s-1)$，而 (1) 在 $s\gg m$ 时为阶 $ms$，故该更强的 $m$-敏感形式失败一个阶-$m$ 因子。用动态预算 $D_0=B(m)$ 的宽松形式则得到右侧 $s(s-1)$：它是合法但随 $s$ 增长的过宽上界，而不是数值反例。比如 $s=4m$ 时 (1) 与其“双倍根信用”的比值趋于 $7/32$，$s\gg m$ 时趋于 $m/s$。

因此可准确排除的是该单偏离/单乘子模板作为**利用 \(m\) 个可选主题上限的独立闭合机制**；不能由此排除加入跨枝续局信用、边负载流平衡、或直接使用 (1) 的证明。

## 状态、非主张与接续

本构造没有给出低福利 SPE，也没有给出 Q-CAG-HALF 反例。它只说明完整 pair-incidence 的 LP 对偶在根部已经把所有极大主题的并集计数耗尽，因而一个单一非负关联乘子向量不会自动产生 \(m\)-主题敏感的半覆盖支付。该结论与[极大关联LP动态预算半覆盖](../定理/极大关联LP动态预算半覆盖--定理.md)的通用 \(B(r)\) 定义和边界观察相容；有界极大主题数的额外闭合定理使用了不同的路径/续局机制。

来源冻结路径为 `research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/representation/complete_pair_incidence_lp_obstruction.md`，源 SHA-256 为 `802fcfd996656278cab1a96870c46e1a14504ba5a453f75b86066e242afd9fb1`（blob `b7a7e945f7c6f5c3e25a91653d6d5bc0c212ed13`）。本对象保留原量词、假设和障碍状态；未做外审或新颖性认证。

