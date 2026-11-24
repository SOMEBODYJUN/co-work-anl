<!-- unit: N-title -->
# 实分析 9：复习笔记

## 目录

1. $G_\delta$ 集、$F_\sigma$ 集与 Borel 集
2. 后续章节随原件逐页识读补入

> [!info] 编排说明
> 普通正文保留原稿内容；蓝色信息块分别标明“补充解释”“补充证明”或“纠错”。原稿明确待填的位置另用红色文字保存。中性编号表示尚待判读的字迹，不表示数学练习。

<!-- unit: N-P001-head -->
## 1. $G_\delta$ 集、$F_\sigma$ 集与 Borel 集

<!-- unit: N-P001-U001 -->
**Def.** 若存在一列开集 $\{G_i\}$ 及闭集列 $\{F_i\}$，使得（拓扑下）：

<!-- unit: N-P001-U002 -->
$$
G=\bigcap_{i=1}^{\infty}G_i,\qquad F=\bigcup_{i=1}^{\infty}F_i,
$$
称 $G$ 为 $G_\delta$ 集，$F$ 为 $F_\sigma$ 集。

<!-- unit: N-P001-U003 -->
这是表示法。

<!-- unit: N-P001-U004 -->
1. 开集是 $G_\delta$，闭集是 $F_\sigma$。

<!-- unit: N-P001-U005 -->
2. $G_\delta$ 不一定是 $F_\sigma$。〔“不一定”按上下文恢复〕

<!-- unit: N-P001-U006 -->
3. $\mathbb Q$ 是 $F_\sigma$，$\mathbb Q^c$ 是 $G_\delta$。

<!-- unit: N-P001-U007 -->
4. $\{x\}=\displaystyle\bigcap_{n=1}^{\infty}B(x,1/n)$。单点是 $G_\delta$ 与 $F_\sigma$。

<!-- unit: N-P001-U008 -->
5. 开集是否是 $F_\sigma$？闭集是否是 $G_\delta$？

右侧旁注：“会有〔疑字 001〕有反例”。

<!-- unit: N-P001-U009 -->
一般距离空间中成立。

<!-- unit: N-P001-U010 -->
设 $F\subset(X,d)$，令
$$
U_n=\{x\in X:d(x,F)<1/n\}.
$$

<!-- unit: N-P001-U011 -->
$$
d(x,F):X\longrightarrow[0,\infty).
$$

<!-- unit: N-P001-U012 -->
$$
F=\bigcap_n U_n.
$$
“开” $\longleftarrow [0,1/n)$ “开”。〔箭头表示以距离函数取逆像。〕

<!-- unit: N-P001-U013 -->
**Prop.** $F_\sigma$、$G_\delta$ 均为 Borel 集。

<!-- unit: N-P001-U014 -->
**Prop.**
$$
\mathcal B(\mathbb R^n)\subsetneq\mathcal M(\mathbb R^n).
$$

<!-- unit: N-P001-S01 -->
> [!info] 补充证明：定义中的基本例子
> 若 $U$ 开，则 $U=\bigcap_{n\ge1}U$；若 $F$ 闭，则 $F=\bigcup_{n\ge1}F$。在度量空间中，单点闭且 $\{x\}=\bigcap_{n\ge1}B(x,1/n)$。把 $\mathbb Q$ 枚举为 $\{q_n:n\ge1\}$，便有 $\mathbb Q=\bigcup_{n\ge1}\{q_n\}$，从而其补集为 $G_\delta$。单点的球交表示用到了度量，不能据此断言任意拓扑空间中的单点均为 $G_\delta$。

<!-- unit: N-P001-S02 -->
> [!info] 补充证明：度量空间中的闭集是 $G_\delta$
> 此处 $F$ 必须为闭集。先设 $F\ne\varnothing$。三角不等式给出
> $$
> |d(x,F)-d(y,F)|\le d(x,y),
> $$
> 所以距离函数连续。$[0,1/n)$ 是 $[0,\infty)$ 的相对开集，因此 $U_n$ 开。又 $F\subset U_n$ 对每个 $n$ 成立；若 $x\notin F$，闭性给出 $r>0$ 使 $B(x,r)\cap F=\varnothing$，选 $1/n\le r$，便有 $x\notin U_n$。于是 $F=\bigcap_nU_n$。$F=\varnothing$ 时直接取 $U_n=\varnothing$。对闭集取补，得到每个开集都是 $F_\sigma$。
>
> 原页写“设 $F\subset(X,d)$”，未重写闭性；此处补明它来自上文“闭是否是 $G_\delta$”这一问题。

<!-- unit: N-P001-S03 -->
> [!info] 补充证明：Borel 性
> Borel $\sigma$ 代数含开集，也含开集的补集即闭集，并对可数并、可数交封闭，因此含全部 $G_\delta$ 和 $F_\sigma$ 集。

<!-- unit: N-P002-head -->
### 1.1 Borel 集与 Lebesgue 可测集的严格区别

<!-- unit: N-P002-U001 -->
$$
\mathcal O(\mathbb R^n)\subset\mathcal M(\mathbb R^n).
$$
包含开集的最小 $\sigma$ 代数是 Borel 代数。

<!-- unit: N-P002-U002 -->
$$
\overline{\overline{\mathcal B(\mathbb R^n)}}=\mathfrak c.
$$

<!-- unit: N-P002-U003 -->
下界：单点集。〔该行左侧有勾。〕

<!-- unit: N-P002-U004 -->
上界：Borel 层级，用超限归纳。

<!-- unit: N-P002-U005 -->
Cantor 集也是 Borel 集，$\exists E\subset C$，但 $E\notin\mathcal B(\mathbb R)$。

<!-- unit: N-P002-U006 -->
反证法：
$$
\overline{\overline{\mathcal P(\mathrm{Cantor})}}
\le\overline{\overline{\mathrm{Borel}}},
$$
矛盾。

<!-- unit: N-P002-U007 -->
不存在外测度 $\mu^*$，s.t. 由 Carathéodory 条件生成 Borel 代数。

<!-- unit: N-P002-U008 -->
可以理解：
$$
\mathrm{Lebesgue}\big|_{\text{Borel 集上}}=\text{Borel 测度}.
$$

<!-- unit: N-P002-U009 -->
Borel 集上，

<!-- unit: N-P002-U010 -->
$$
E=E^\circ\mathbin{\dot\cup}(E\cap\partial E).
$$

<!-- unit: N-P002-U011 -->
**Prop.**
$$
E\in\mathcal M\quad\Longleftrightarrow\quad E\cap\partial E\in\mathcal M.
$$

<!-- unit: N-P002-U012 -->
测度的完备化，局部逼近。开集〔疑字 002〕扩大逼近〔疑字 002〕。

<!-- unit: N-P002-U013 -->
**Lemma.** $E\in\mathcal M$，则下述性质成立。〔接第 3 页。〕

<!-- unit: N-P002-S01 -->
> [!info] 补充证明：$|\mathcal B(\mathbb R^n)|=\mathfrak c$
> 下界来自互不相同的单点 Borel 集：$x\mapsto\{x\}$ 给出 $\mathbb R^n$ 到 Borel 集族的单射。
>
> 上界按原稿提示采用 Borel 层级。$\mathbb R^n$ 有可数基，每个开集都是基元素的某个子族之并，所以开集族的基数不超过 $2^{\aleph_0}=\mathfrak c$。从开集出发，在每个可数序数阶段加入以前各阶段集合的补集和可数并。若已有集合族基数至多 $\mathfrak c$，其可数序列族基数至多 $\mathfrak c^{\aleph_0}=\mathfrak c$；可数极限阶段的并也至多为 $\mathfrak c$。超限归纳得每个可数阶段至多有 $\mathfrak c$ 个集合。全部可数阶段的并对补集和可数并封闭，因为可数个可数序数的上确界仍可数，因此它正是 Borel $\sigma$ 代数。又 $\aleph_1\le\mathfrak c$，全部阶段的集合数仍不超过 $\mathfrak c$，与下界合并即得等式。

<!-- unit: N-P002-S02 -->
> [!info] 补充证明：严格包含
> 取标准三分 Cantor 集 $C$。它闭、测度为零，且 $|C|=\mathfrak c$。若它的每个子集均为 Borel 集，就有 $|\mathcal P(C)|\le|\mathcal B(\mathbb R)|=\mathfrak c$；但 Cantor 定理给出 $|\mathcal P(C)|=2^{\mathfrak c}>\mathfrak c$，矛盾。因此有非 Borel 子集 $E\subset C$。Lebesgue 测度完备，故这个 $E$ 仍然 Lebesgue 可测且测度为零，于是 $\mathcal B(\mathbb R)\subsetneq\mathcal M(\mathbb R)$。在 $\mathbb R^n$ 中使用 $C\times\{0\}^{n-1}$ 得到相同结论。

<!-- unit: N-P002-S03 -->
> [!info] 适用范围核验：外测度与 Borel 代数
> 对 Lebesgue 外测度，上面的非 Borel 零测子集说明，Carathéodory 可测集族严格大于 Borel 集族。原页进一步写了“**不存在外测度**”这一全称断言，未附一般论证；它不能仅由 Lebesgue 外测度这个特例推出。本次首遍保留原断言，并登记数学核验项 M001，等待一般论证的独立核验。

<!-- unit: N-P002-S04 -->
> [!info] 补充证明：只需检查边界上的部分
> 对任意 $E\subset\mathbb R^n$，$E\setminus E^\circ=E\cap\partial E$，两部分不交。由于 $E^\circ$ 开、$\partial E$ 闭，二者都是 Borel 集。若 $E$ 可测，则 $E\cap\partial E$ 可测；反过来，若 $E\cap\partial E$ 可测，则由分解式及可数并封闭性，$E$ 也可测。此处 $\mathcal M$ 可取 Lebesgue 可测集族；同一论证也适用于 Borel 集族。

<!-- unit: N-P003-head -->
## 2. 可测集的开集外逼近与闭集内逼近

以下条件承接原稿引理：$E$ 为 Lebesgue 可测集。

<!-- unit: N-P003-U001 -->
(1) $\forall\varepsilon>0$，$\exists$ 开集 $G\supset E$，s.t.
$$
m(G\setminus E)<\varepsilon.
$$

<!-- unit: N-P003-U002 -->
(2) $\forall\varepsilon>0$，$\exists$ 闭集 $F\subset E$，s.t.
$$
m(E\setminus F)<\varepsilon.
$$

<!-- unit: N-P003-U003 -->
<span style="color:red">原稿提问：与外测度结论区别？</span>

〔问号用蓝色椭圆圈出，原位置未写答。〕

<!-- unit: N-P003-S01 -->
> [!info] 补充解答：与外测度逼近结论的区别
> 外测度定义可对任意集合 $A$ 给出开覆盖，其总体积接近 $m^*(A)$；有限外测度时可得到 $m(G)<m^*(A)+\varepsilon$。本引理以 **$E$ 可测** 为条件，结论直接控制新增部分 $G\setminus E$ 的测度。有限测度时，依靠可测性写成 $m(G\setminus E)=m(G)-m(E)$；无限测度时不能作 $\infty-\infty$ 的减法，需要下面的局部分解与可求和误差。闭集内逼近则由补集的外逼近得到。

<!-- unit: N-P003-U004 -->
**(1) 当 $m(E)<+\infty$。**

<!-- unit: N-P003-U005 -->
$\forall\varepsilon>0$，$\exists\{I_i\}\in\mathcal L_c(E)$，s.t.

<!-- unit: N-P003-U006 -->
$$
E\subset\bigcup_{i=1}^{\infty}I_i,
\qquad\sum_i|I_i|<m(E)+\varepsilon.
$$

<!-- unit: N-P003-U007 -->
$$
G=\bigcup_i I_i\quad\text{开},\qquad
m(G)\le\sum_i|I_i|<m(E)+\varepsilon.
$$

<!-- unit: N-P003-S02 -->
> [!info] 补充证明：有限测度情形的最后一步
> $\mathcal L_c(E)$ 在此表示所用的可数开矩形（开区间）覆盖族；由原稿下一行 $G=\bigcup I_i$ 为开集可见，覆盖元素在本路线中取开。$E\subset G$ 且 $E$ 可测，故 $G=E\mathbin{\dot\cup}(G\setminus E)$。这里 $m(G)<\infty$，从而
> $$
> m(G\setminus E)=m(G)-m(E)<\varepsilon.
> $$

<!-- unit: N-P003-U008 -->
**$m(E)=+\infty$ 时。**

<!-- unit: N-P003-U009 -->
令
$$
B_i=\{x\in\mathbb R^n:|x|\le i\}.
$$

<!-- unit: N-P003-U010 -->
$$
E\cap B_i=E_i,\qquad m(E_i)<+\infty.
$$

<!-- unit: N-P003-U011 -->
$E$ 是 $\sigma$ 有限，再用 $\varepsilon/2^k$。〔此处原稿指数写 $k$，下文片段指标写 $i$。〕

<!-- unit: N-P003-U012 -->
右侧短注：$<i$，$(j>i)$。

<!-- unit: N-P003-U013 -->
$$
G=\bigcup_{i=1}^{\infty}G_i.
$$

<!-- unit: N-P003-U014 -->
$$
\begin{aligned}
G\setminus E
&=\left(\bigcup_{i=1}^{\infty}G_i\right)\cap
\left(\bigcap_{i=1}^{\infty}E_i^c\right)\\
&\subset\bigcup_i(G_i\cap E_i^c)
=\bigcup_{i=1}^{\infty}(G_i\setminus E_i).
\end{aligned}
$$

<!-- unit: N-P003-U015 -->
即可。

<!-- unit: N-P003-S03 -->
> [!info] 补充证明：可求和的局部误差
> 因为 $E=\bigcup_{i\ge1}E_i$，对每个 $E_i$ 应用有限测度结论，选开集 $G_i\supset E_i$，使
> $$
> m(G_i\setminus E_i)<\frac{\varepsilon}{2^i}.
> $$
> 这里把原稿的占位指标 $k$ 统一成对应片段的 $i$。$G=\bigcup_iG_i$ 为包含 $E$ 的开集。原稿给出的集合包含关系与次可加性推出
> $$
> m(G\setminus E)\le\sum_{i=1}^{\infty}m(G_i\setminus E_i)
> <\sum_{i=1}^{\infty}\frac{\varepsilon}{2^i}=\varepsilon.
> $$
> 最后的严格小于成立：每一项的缺口均为正，至少第一项已有严格缺口，而其余项以给定上界估计即可。

<!-- unit: N-P003-U016 -->
**(2)** $E\in\mathcal M\Longleftrightarrow E^c\in\mathcal M$。

<!-- unit: N-P003-U017 -->
由 (1) 得，$\forall\varepsilon>0$，$\exists$ 开集 $G\supset E^c$，s.t.
$$
m(G\setminus E^c)<\varepsilon.
$$
〔接第 4 页。〕

<!-- unit: N-P004-S00 -->
> [!info] 补充证明：闭集内逼近的跨页收尾
> 延续上页对 $E^c$ 的外逼近，令 $F=G^c$。则 $F$ 闭且 $F\subset E$，并且
> $$
> E\setminus F=E\cap G=G\setminus E^c.
> $$
> 所以 $m(E\setminus F)<\varepsilon$，完成闭集内逼近。原稿在上页写到对 $E^c$ 的估计后，本页直接进入下述推论；这里补出省略的取补步骤。

<!-- unit: N-P004-head -->
### 2.1 相差零测集的 Borel 外壳与内核

<!-- unit: N-P004-U001 -->
$E\in\mathcal M$。

<!-- unit: N-P004-U002 -->
(1) 存在 $G_\delta$ 集，s.t. $G\supset E$ 且
$$
m(G\setminus E)=0.
$$

<!-- unit: N-P004-U003 -->
(2) 存在 $F_\delta$ 集，……
$$
m(G\setminus E)=0.
$$
〔这里原稿确写 $F_\delta$，条件处用省略线，并重复上一项的 $G\setminus E$。〕

<!-- unit: N-P004-S01 -->
> [!info] 纠错：第二项应为 $F_\sigma$ 内核
> 与闭集内逼近对应的正确结论是：存在 $F_\sigma$ 集 $F\subset E$，且 $m(E\setminus F)=0$。原稿第二项的 $F_\delta$ 和重复写出的 $m(G\setminus E)=0$ 已在上方保留；这里分别订正为 $F_\sigma$ 与 $m(E\setminus F)=0$。
>
> 证明：对每个 $k\ge1$，选开集 $G_k\supset E$ 使 $m(G_k\setminus E)<1/k$，令 $G=\bigcap_kG_k$，便有 $m(G\setminus E)\le1/k$ 对每个 $k$ 成立，所以为零。再选闭集 $F_k\subset E$ 使 $m(E\setminus F_k)<1/k$，令 $F=\bigcup_kF_k$；同理由 $E\setminus F\subset E\setminus F_k$ 得零测。

<!-- unit: N-P004-U004 -->
实际上，在外测度下，$E\in\mathcal M$ 是和上面的引理等价。

<!-- unit: N-P004-U005 -->
也得到一种判定可测集的方法。

<!-- unit: N-P004-S02 -->
> [!info] 补充证明：逼近条件反推可测性
> 假设对每个 $k$ 有开集 $G_k\supset E$ 且 $m^*(G_k\setminus E)<1/k$。令 $G=\bigcap_kG_k$，则 $G$ 是 Borel 集，且 $m^*(G\setminus E)=0$。零外测度集可测，所以 $E=G\setminus(G\setminus E)$ 可测。由闭集形式也可同样取 $F=\bigcup_kF_k\subset E$，使 $m^*(E\setminus F)=0$，再以 $E=F\cup(E\setminus F)$ 得可测。因而原稿的“外测度下等价”应读作把逼近误差写成外测度后的判别。

<!-- unit: N-P004-head2 -->
### 2.2 由开集、闭集确定测度

<!-- unit: N-P004-U006 -->
**Th. (1)** 设 $E\in\mathcal M$，则

<!-- unit: N-P004-U007 -->
$$
\begin{aligned}
m(E)
&=\inf\{m(G):G\supset E,\ G\text{ 开}\}\\
&=\sup\{m(F):F\subset E,\ F\text{ 闭}\}.
\end{aligned}
$$

<!-- unit: N-P004-U008 -->
(2) $E$ 有界，且 $m^*(E)=m_*(E)$，则 $E\in\mathcal M$。

<!-- unit: N-P004-U009 -->
(1) pf：
