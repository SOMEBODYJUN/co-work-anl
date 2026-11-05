---
id: "customer-attraction/disjoint-theme-related-machine-pure-spe-isomorphism-and-ratio-distortion"
kind: "equivalence"
type_tag: "等价"
title: "不交主题与单位任务相关机的纯SPE同构及倍率失真"
status: "complete-explicit-encoding-proofs"
truth_status: "exact-pure-strategy-isomorphism-in-stated-subclass; approximation-ratios-not-preserved"
review_level: "original-independent-analytic-review; this-cleanup-complete-reconstruction-and-one-original-finite-audit"
scope: "任意正人数；有限非空且两两不交非空主题；顺序单位任务相关机；另有一般共同客户平移"
summary: "保全部有序历史和纯平局的收益倒数同构，任意m趋二覆盖族却映成最优调度；共同客户平移同样保IC却令福利比趋一，不排除其它归约。"
legacy_ids: ["EA-RECIPROCAL-RELATED-v1", "EA-RECIPROCAL-OBJECTIVE-NO-v1", "EA-COMMON-BASELINE-DISTORTION-v1"]
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c90acbef8c6a45f28bf33b5f639d6e99/equivalence_audit/direct_encoding_claims.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c90acbef8c6a45f28bf33b5f639d6e99/equivalence_audit/direct_encoding_claims.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c90acbef8c6a45f28bf33b5f639d6e99/equivalence_audit/astra_relationship_report.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c90acbef8c6a45f28bf33b5f639d6e99/equivalence_audit/astra_relationship_report.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c90acbef8c6a45f28bf33b5f639d6e99/equivalence_audit/astra_independent_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c90acbef8c6a45f28bf33b5f639d6e99/equivalence_audit/astra_independent_review.md"
---

# 不交主题与单位任务相关机的纯SPE同构及倍率失真

## 1. 固定编码、模型和正反方向

原共同目录模型见[完整历史定义](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同**标签**目录、单位提供者顺序观察所有有序历史后各选一次，客户单位价值在终局覆盖者间均分。空覆盖、同覆盖别名、重复行动、零客户及全部离轨平局在一般模型中保留。

本节的 `EA-RECIPROCAL-RELATED-v1` 特别限于目录 $S_1,\ldots,S_L$ **非空且两两不交**，$L\ge1$，人数 $m\ge1$。令 $w_j=|S_j|>0$。此处不删一般模型的空主题，而是明确只建立一个受限子类的同构；不对全零主题做倒数，也不声称重叠主题有相同关系。

构造一个顺序调度**博弈**：有 $L$ 台相关机，速度 $s_j=w_j$；$m$ 个不可拆分单位工作量任务作为玩家，依同一顺序观察全部有序机器选择历史，各选一台机器。任务 $i$ 的个人目标是最小化其最终所在机器的总负载，不是由中央调度算法选择输出。每个任务在机器 $j$ 的处理时间均为 $1/w_j$，与任务身份无关。

保留原行动标签与每个完整有序历史的策略映射。终局中机器/主题 $j$ 的使用数为 $n_j$，选它的玩家有

\[
u_i=\frac{w_j}{n_j}>0,\qquad d_i=\frac{n_j}{w_j}=\frac1{u_i}.
\tag{1}
\]

这取的是**整个个人收益**的倒数，不能把一般重叠主题的多个客户项分别取倒数后相加。

固定任一完整纯策略，在任意有序历史处强制任一替代行动后，继续的是同一张原策略表，两侧终局标签一致且两个人收益都正。于是逐条

\[
u_i(\mathrm{actual})\ge u_i(\mathrm{deviation})
\iff d_i(\mathrm{actual})\le d_i(\mathrm{deviation}).
\tag{2}
\]

所以同一动作表是 CAG 的完整纯SPE，当且仅当它是该调度博弈的完整纯SPE；两个策略集合在标签/历史身份映射下一一对应，所有平局和离轨历史都保持。对剩余深度逆归纳或直接按每节点真实比较即可得双向结论，不需要匿名计数策略净化。

这个对应没有产生一般不相关机的任意矩阵 $p_{ji}$，仅有每行恒为 $1/w_j$ 的单位任务相关机子类；更不自动给计算SPE或好调度的多项式算法。纯结果逐点递减变换也不保证混合期望最优性：一般 $\mathbb E(1/U)\ne1/\mathbb E U$，本页不把(2)扩成混合策略定理。

## 2. 同构的社会目标并非同一个量

对应终局的社会量分别为

\[
W(n)=\sum_{j:n_j>0}w_j,\qquad
C_{\max}(n)=\max_j\frac{n_j}{w_j}.
\tag{3}
\]

前者按启用主题求和，后者取机器峰值。保持每人的偏好序和全部SPE，不蕴含两个目标的效率倍率保持。以下 `EA-RECIPROCAL-OBJECTIVE-NO-v1` 对任意 $m\ge2$ 给严格见证。

取一主题 $A$ 大小 $m$，另有 $m-1$ 个互不相交且在 $A$ 外的单客户主题。规定**每位玩家在每个历史都选 $A$**。在第 $i$ 位任意历史，已有 $b\le i-1$ 次 $A$；当前也选 $A$ 后的收益为

\[
\frac{m}{b+1+m-i}\ge1.
\]

若改某单例，已有 $r$ 位选它时收益为 $1/(r+1)\le1$；原后继仍全选 $A$。因此该策略在全部历史最优，包含重复单例离轨和平局。实际覆盖 $W=m$，最优用一次 $A$ 加全部单例覆盖 $2m-1$，故

\[
\frac{\operatorname{OPT}_{\rm cov}}{W}=2-\frac1m.
\tag{4}
\]

对应调度有一台速度 $m$、$m-1$ 台速度1的机器。全选快机的峰值为1。任何峰值严格小于1的调度都不能使用慢机，全部 $m$ 个单位任务在快机又恰需1，因此调度OPT也为1，实际倍率**恰为1**。

特别 $m=2$ 的覆盖倍率 $3/2$ 对应最优调度，不能把它当 LST 的 $3/2$ 近似困难性来源。任意 $m$ 的覆盖构造归属 Deng 等 [arXiv:2307.07174v2，Example 2](https://arxiv.org/html/2307.07174v2)；本页保存源稿补出的完整历史证明和调度目标对照，不认领构造新颖性。现有[六人全大主题见证](../计算/六人全大主题纯SPE下界见证--计算.md)是同族 $m=6$，$W=6,OPT_6=11$，不是六人half反例。

结论精确限于这个明示身份映射不保持性能倍率；没有由此证明任意复杂编码、辅助结构或条件归约都不可能。

## 3. 另一个精确保策略却扭曲倍率的操作

`EA-COMMON-BASELINE-DISTORTION-v1` 对一般共同目录实例成立，不要求不交。取新的一组 $B\in\mathbb Z_{\ge0}$ 个单位客户，与旧客户不交，**同时加入每个主题**，玩家数仍为 $m\ge1$，每个原标签映成扩充后的同标签。

每个新客户在每个终局都恰被 $m$ 个槽覆盖。每个人在每个有序终局统一增益 $B/m$，因此每个历史的规定/偏离比较两侧加同一常数，完整纯SPE及全部平局精确保持。原别名关系保持；不同旧覆盖集合加同一新客户组后仍不同。原空主题可以变成非空，但一般模型不要求必须存在空主题。

对每个终局及最优值，

\[
W'=W+B,\qquad OPT'_m=OPT_m+B.
\tag{5}
\]

固定 $W>0$ 的实例，覆盖损失变成 $(OPT_m+B)/(W+B)$，随 $B\to\infty$ 趋1。全零旧实例、$B=0$、零客户直接使用(5)及IC差为零的乘法/加法陈述，不定义 $0/0$。

这说明哪怕辅助客户完全不扰动激励，仍需额外证明社会差额/倍率的传递。它只审计公共背景这一明确操作；不排除经过补偿和准确解码的其它gadget。该公共平移的任意实例结论完全由逐客户证明承担，下面原有限代码并没有运行它。

## 4. 原内审、有限证据及本轮边界

原 Astra 独立审读逐条检查以上三项，明确没有执行根代码，也不扩为外审/新颖性。原标准库审计对 $m=2,\ldots,6$ 检查全历史恒选大主题策略，枚举全部无序可重复终局的覆盖和相关机峰值，并逐玩家核(1)；它没有对任意输入、所有策略或混合策略穷举。

本轮完整实读全部主源后，对这份原5225B程序只执行一次，stdout与原3002B报告逐字节相同；没有另跑现有六人见证或新写数学核。全部计数、源码合同、真实执行和复现入口见[不交主题与单位任务相关机的纯SPE同构及倍率失真](<不交主题与单位任务相关机的纯SPE同构及倍率失真--等价.md>)。模型桥与一般 CAG/UM 目标间仍缺的量词、算法和位长合同见[联系审查](../审查/客户吸引与不相关机的归约边界及原文献核对--审查.md)。
