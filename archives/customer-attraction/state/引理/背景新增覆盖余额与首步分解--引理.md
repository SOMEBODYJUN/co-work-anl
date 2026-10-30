---
id: "customer-attraction/background-fresh-coverage-balance-decomposition"
kind: "lemma"
type_tag: "引理"
title: "合法背景下新增覆盖余额的精确首步分解"
status: "complete"
truth_status: "proved-identity-with-refuted-sufficient-invariant"
review_level: "source-reconstruction-and-exact-counterexample-comparison"
scope: "有限单位客户、有限非空共同标签目录；任意合法有序前缀及其完整纯SPE续局；允许零客户、空主题、重复与任意平局"
summary: "G_r=P+Δ−freshOPT_r严格分解为尾部G与u+a+freshOPT_(r−1)−freshOPT_r；恒等式成立，逐步非负候选被23客户反例否定，整体非负候选亦已被另一实际前缀反例否定。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/coverage_opportunity_step_obstruction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_counterexample.md"
---

# 合法背景下新增覆盖余额的精确首步分解

## 对象、定义域与三个不同的量

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)。客户集有限，每名客户价值一；共同目录是有限非空**标签集**，每个标签映到一个客户子集，不同标签允许覆盖同一子集。提供者逐位观察完整有序历史各选一次标签，终局每名客户的价值在全部覆盖者间均分。允许空主题、重复、零客户、任意离轨历史与任意平局。

固定合法有序过去历史 $h$，其客户负载为 $b_x$，已有覆盖集为 $C=\{x:b_x>0\}$，还剩 $r\ge0$ 人。该背景必须来自共同目录中的过去行动；一般不把每个客户的负载独立指定。固定一份定义在这个子博弈全部有序后史上的纯SPE，后续实际行动记为 $A_1,\ldots,A_r$，后续覆盖重数记为 $k_x$。令

\[
P_r(h)=\sum_x\frac{k_x}{b_x+k_x},\qquad
\Delta_r(h)=|\{x:b_x=0,\ k_x>0\}|.
\]

零分子时该项取零，包括分母为零的情形。$P_r$ 是**所有剩余提供者的终局收益之和**，$b_x>0$ 的旧客户仍能向后继提供利润；$\Delta_r$ 只数原来未覆盖而后来被覆盖的客户。因此二者一般不等。

比较对象为只数新客户的最优覆盖

\[
O_r(b)=\max_{T_1,\ldots,T_r\in\mathcal S}
|\{x:b_x=0,\ x\in T_1\cup\cdots\cup T_r\}|,\qquad O_0(b)=0.
\]

主题可重复；非空目录使少于 $r$ 个标签的支持可补齐成恰 $r$ 次选择。这个 $O_r$ 不是[固定背景最优剩余利润](../定义/固定背景剩余收益与税--定义.md) $F_r(b)=\max\sum_x e_x/(b_x+e_x)$，后者还从已有客户获取分数收益。也不能把 $O_r(b)$ 和已经覆盖的总人数相加后仍称剩余利润。

定义候选余额

\[
G_r(h)=P_r(h)+\Delta_r(h)-O_r(b).
\tag{G}
\]

这只是定义；对每个合法背景、每份完整纯SPE声称 $G_r\ge0$ 的加强命题已经为假，见下文当前状态。定义与分解本身仍有效。

## 精确分解及充分归纳的原理

设 $r\ge1$，实际首主题为 $A$，首位在该完整尾局终点的真实收益为 $u$，其新增覆盖为

\[
a=|\{x:b_x=0,\ x\in A\}|,\qquad
b'_x=b_x+\mathbf1_A(x).
\]

尾部固定为原完整策略在有序历史 $hA$ 下的真实子树，记其实际量为 $P_{r-1}(hA),\Delta_{r-1}(hA)$。没有另挑一个更好或更坏的孩子SPE。收益按提供者分拆，新增客户按首次覆盖分拆，分别有

\[
P_r(h)=u+P_{r-1}(hA),\qquad
\Delta_r(h)=a+\Delta_{r-1}(hA).
\]

定义一步余额

\[
L_r(h)=u+a+O_{r-1}(b')-O_r(b).
\tag{L}
\]

直接代入得精确恒等式

\[
\boxed{G_r(h)=G_{r-1}(hA)+L_r(h).}
\tag{Telescope}
\]

不等式或SPE最优性不是此恒等式的前提；只需按同一真实路径计算所有收益与覆盖。它对空主题、零客户和任意平局保持成立。$r=0$ 时 $G_0=0$，故沿任意实际尾路径进一步有

\[
G_r(h)=\sum_{i=1}^{r}L_{r-i+1}(hA_1\cdots A_{i-1}).
\]

因此，若能对全部相应SPE节点证明 $L_r(h)\ge0$，便能归纳得到 $G_r(h)\ge0$。这是充分条件，不是必要条件：单步负值可被稍后正值支付。23客户见证恰好把这种差别显式化，不能把局部失败直接称整体失败。

在无过去行动的根，$b=0$，每个被覆盖客户把价值一完整分给提供者，所以 $P_n=W$ 且 $\Delta_n=W$。从而

\[
G_n(\varnothing)=2W-\operatorname{OPT}_n.
\]

这解释了为什么该背景加强式曾被用作半覆盖归纳候选；它的背景版本失败不等于根半覆盖失败。仅 $r=1$ 的背景版本成立：最后一人的最优收益 $u\ge\max_T|\{x:b_x=0,x\in T\}|=O_1(b)$，因为选择 $T$ 时新客户各给该人一单位，旧客户给非负额外收益；再加 $\Delta_1\ge0$ 即得 $G_1\ge0$。

## 与总覆盖机会损失账本的准确对应

定义包含原覆盖的总覆盖补全

\[
\widehat F_r(C)=\max_{T_1,\ldots,T_r}|C\cup T_1\cup\cdots\cup T_r|
=|C|+O_r(b).
\]

把 $C'=C\cup A$ 代入，并注意 $|C'|-|C|=a$，便得

\[
L_r(h)
=u+\widehat F_{r-1}(C')-\widehat F_r(C)
=u-\delta,\qquad
\delta=\widehat F_r(C)-\widehat F_{r-1}(C').
\]

所以本页的一步余额和[最优首动作菜单账本](最优首动作菜单与真实孩子损失--引理.md)中的总覆盖机会损失使用同一个代数接口，差别在本页显式保留了非零背景及尾部收益。它与[在轨机会损失反例](../反例/在轨最优补全损失的逐期收费--反例.md)、[实际根首步余额族](../反例/任意人数首步补全余额--反例.md)可以比较，但不能因此把这些不同输入、不同失败节点的证据互相替代。

## 两个局部反例与后续整体纠错

[合法背景首步反例](../反例/合法背景首步覆盖机会损失--反例.md)给共同六标签、合法过去历史 $(2,5)$、剩余三人的完整SPE。实际后继为 $(2,1,1)$。两份不同的整数客户输入满足：

| 客户数 | $u$ | $a$ | $O_3(b)$ | $O_2(b')$ | $L_3$ | 尾部 $G_2$ | 整体 $G_3$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
|23|$39/10$|0|14|10|$-1/10$|$24/5$|$47/10$|
|488|84|0|284|195|$-5$|109|104|

每行都有 $G_3=G_2+L_3$；两者都只反驳一步非负充分条件。23客户输入是后来整数压缩，488客户输入由保存的归一化发现点有理恢复后单独精确验证；它们不是同一客户实例的两种写法。

冻结README及主稿说整体 $P+\Delta\ge O_r$ 仍开放，只能作为**当时的记录**保留。实际阅读后续来源
source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_counterexample.md
以及其52客户输入、259节点完整根策略证书和独立审查可知，这个整体加强式也已被反驳，而且失败发生在完整四人根SPE的实际前缀 $(A,B)$：

\[
(u_1,u_2,u_3,u_4)=(8,9,8,9),\quad W=34,\quad \operatorname{OPT}_4=52;
\qquad P_2=17,\quad\Delta_2=0,\quad O_2=18.
\]

本轮另从该原输入逐单位客户算出全部1554项真实行动比较并验证其完整策略，得到 $G_2=-1$；因此当前状态是 **GLOBAL为假**。这个比较还否定任何固定实数 $\lambda$ 的普遍 $P+\lambda\Delta\ge O_r$，因为见证的 $\Delta=0$。根半覆盖在该例仍有 $2W-\operatorname{OPT}_4=16>0$。当前批次只据其核清背景候选状态，未把后续包的参数族、发现过程等其余独有内容重复标为完成。

## 用途与接续

本页可以安全复用的是 (Telescope) 精确恒等式、总覆盖补全之间的换算和最后一人边界。若新方案引入过去收益、已有覆盖信用或跨节点预算，应明确写出新状态，并证明它如何支付负的 $L_r$；不能只将旧README的OPEN改名后重新假定 $G_r\ge0$。

局部23/488证书没有保证过去历史 $(2,5)$ 位于某个根SPE的实际路径；它们已经足以否定“每个合法背景”的一步断言。有限完美信息博弈中，可以固定该完整子树并在其他子树和祖先做逆向选择，把它延伸成某份完整根SPE，但这种延伸不保证祖先选择这条路径。后续52客户证书另行提供了实际路径可达性，两种证据责任应分别登记。

原11源、两个只作运行依赖的源、本轮全部有理比较与后续状态核查见[发现与重放资源](../计算/背景首步反例发现与精确重放--计算.md)。关系证据应分别标为定义依赖、恒等式、局部充分条件反例和后续整体纠错；本批没有把旧关系图导入为完成结果。
