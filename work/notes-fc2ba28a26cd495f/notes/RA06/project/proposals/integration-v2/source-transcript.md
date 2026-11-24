<!-- unit: T-title -->
# 实分析 6：保真转写

<!-- unit: T-p1-heading -->
## 原稿第 1 页

<!-- unit: T-p1-01 -->
### 紧性

<!-- unit: T-p1-02 -->
Lindeloff（空间）：任意开覆盖有可数子覆盖。

<!-- unit: T-p1-03 -->
第二可数 $\Rightarrow X$ 是 Lindeloff，逆不真。

<!-- unit: T-p1-04 -->
右上浅色旁注：$\Rightarrow$ 反证法，构造子列；$\Leftarrow$ 已知是距离空间。

<!-- unit: T-p1-05 -->
**Ex：**示出整个思路，在 $\mathbb R^n$ 中有界闭集 $\Longleftrightarrow$ 紧。

<!-- unit: T-p1-06 -->
**Th：**设 $M\subset(X,d)$，$M$ 紧，则 $M$ 是有界闭集。（至少是距离空间。）

<!-- unit: T-p1-07 -->
先证 $M^c$ 开。设 $x\in M^c$，即证存在 $\delta$，使 $B(x,\delta)\subset M^c$。

<!-- unit: T-p1-08 -->
由 $T_1$，$\forall y\in M$，由 $T_2$，$\exists\delta_y>0$，
$$
B(x,\delta_y)\cap B(y,\delta_y)=\varnothing.\tag{*}
$$

<!-- unit: T-p1-09 -->
$$
M\subset\bigcup_{y\in M}B(y,\delta_y).
$$
又因 $M$ 紧，
$$
M\subset\bigcup_{i=1}^{m}B(y_i,\delta_{y_i})\qquad\text{（有界）}.
$$

<!-- unit: T-p1-10 -->
令 $\delta=\min\{\delta_{y_1},\ldots,\delta_{y_m}\}$，则由 $(*)$，
$$
B(x,\delta)\cap\left(\bigcup_{i=1}^{m}B(y,\delta_{y_i})\right)=\varnothing
\qquad\text{（闭集）}.
$$

<!-- unit: T-p1-11 -->
$$
X=\{a,b\},\qquad\mathcal T=\{\varnothing,X,\{a\}\}.
$$
$\{a\}$ 紧，是开集。

<!-- unit: T-p2-heading -->
## 原稿第 2 页

<!-- unit: T-p2-01 -->
有限[Q006]：iff 列紧 $\Longleftrightarrow$ 闭集有界。

可以定义有限[Q006]（某些教材）。

<!-- unit: T-p2-02 -->
（闭传递性）〔按局部笔画恢复；恢复依据另存 Q001。〕

**lemma.** $(X,\tau)$，$M$ 紧，$F$ 是 $M$ 闭子集，$F$ 是紧。

<!-- unit: T-p2-03 -->
**Hine Borel.** 设 $M\subset(\mathbb R^n,\|\cdot\|)$，$M$ 有界闭，则 $M$ 紧。

<!-- unit: T-p2-04 -->
**pf.** $M$ 有界，$\exists a>0$，s.t.
$$
M\subset[-a,\text{[Q002a]}]^{\text{[Q002b]}}.
$$
〔Q002a、Q002b 分别定位原式的右端点与指数；左端点 $-a$ 可读。〕

<!-- unit: T-p2-05 -->
仅证 $[-a,a)^n$ 是紧的。

<!-- unit: T-p2-06 -->
任取 $\{G_i\}$。

若不然，$Q_0$ 无有限子覆盖。

<!-- unit: T-p2-07 -->
等分 $Q_0$，$2^n$ 个，存在一个闭集，无有限子覆盖，记作 $Q_m$。

<!-- unit: T-p2-08 -->
归纳地，将 $Q_m$，$2^n$ 等分，存在 $Q_{m+1}$ 无有限子覆盖。

<!-- unit: T-p2-09 -->
$$
Q_0\supset\cdots\supset Q_{m+1}\supset\cdots.
$$

<!-- unit: T-p2-10 -->
$$
\operatorname{diam}(Q_m)\leq\frac{2a\sqrt n}{2^m}.
$$

<!-- unit: T-p3-heading -->
## 原稿第 3 页

<!-- unit: T-p3-01 -->
$$
\exists x_{m+1}\in Q_m\setminus Q_{m+1}.
$$

<!-- unit: T-p3-02 -->
$$
\{x_m\}\subset Q_0.
$$

<!-- unit: T-p3-03 -->
$$
\exists x_{m_k}\to x_0\in\mathbb R^n,\qquad x_0\in Q_0.
$$

<!-- unit: T-p3-04 -->
$$
x_0\in Q\subset\bigcup_{\lambda\in\Lambda}G_\lambda.
$$

<!-- unit: T-p3-05 -->
从而 $\exists\lambda_0$，$x\in G_{\lambda_0}$。

<!-- unit: T-p3-06 -->
$$
\exists B(x_0,\delta)\subset G_{\lambda_0}.
$$
〔Q007：$\delta$ 右下有点状附笔，是否为下标尚未唯一辨定；此处保留可辨主符号。〕

<!-- unit: T-p3-07 -->
当 $k$ 充分大，
$$
\|x_{m_k}-x_0\|<\frac\delta2,
\qquad\operatorname{diam}(Q_{m_k})<\frac\delta2.
$$

<!-- unit: T-p3-08 -->
由 $Q_{m_k}\subset B(x_0,\delta)\subset G_{\lambda_0}$。

<!-- unit: T-p3-09 -->
自密：$E\subset E'$，闭集是 $E'\subset E$。

<!-- unit: T-p3-10 -->
$$
E^{(n)}\subset(E^{n-1})'.
$$

<!-- unit: T-p3-11 -->
proof：$E^{(n)}\subset E^{(n-1)}$。

<span style="color:red">原稿待证：此处写出 proof 与下降关系，未给出推导。</span>

<!-- unit: T-p3-12 -->
自密 $\Longleftrightarrow E\subset(X,d)$，$\operatorname{Iso}(E)=\varnothing$。

<!-- unit: T-p3-13 -->
原稿右下浅色旁注，$\Rightarrow$ 方向：
$$
\overline E=E'=E'\cup\operatorname{Iso},
\qquad\operatorname{Iso}\notin E'.
$$

<!-- unit: T-p3-14 -->
右下浅色旁注，$\Leftarrow$ 方向：
$$
E'=\overline E=E\cup E'
\quad\Rightarrow\quad E\subset E'.
$$

<!-- unit: T-p3-15 -->
浅色补记：〔Q008：起首连接语〕（$E'$ 是闭），（闭）$'\subset$（闭）。

<!-- unit: T-p3-16 -->
闭，
$$\overline E=E=E^{\text{[Q009]}}\cup\partial E.$$
〔Q009 定位并号前 $E$ 的小上标；起首“闭”按原笔保留。〕

<!-- unit: T-p3-16-b -->
原稿浅色下一行另记
$$E'\subset E.$$

<!-- unit: T-p4-heading -->
## 原稿第 4 页

<!-- unit: T-p4-01 -->
perfect set $\Longleftrightarrow E=E'$，自密闭集。

<!-- unit: T-p4-02 -->
**Ex 1.** $\mathbb R$ 能[Q003]拓扑；$2^c$。

<!-- unit: T-p4-03 -->
$\forall\varnothing=U\subset(\mathbb R,|\cdot|)$，包含号下记“开”。

<!-- unit: T-p4-04 -->
右侧浅色：$(\mathbb R,\tau)$，$\mathcal P(\mathbb R)=2^c$（$2^c$ 被框起）；$\mathcal U\subseteq\mathcal P(\mathbb R)$。

<!-- unit: T-p4-05 -->
$Q_1$：$x\in U$，$B(x,\delta)\subset U$ 有多少个？

<!-- unit: T-p4-06 -->
$Q_2$：有无最大？

<!-- unit: T-p4-07 -->
**Ex 2.** $(\mathbb R,|\cdot|)$ 有 $2^c$ 种基。

<!-- unit: T-p4-08 -->
浅色：$\mathcal P(A)=2^c\Rightarrow$。

<!-- unit: T-p4-09 -->
基，$\bigcup\{G_i\}=\mathbb R$；

$\bigl(\forall x\in G_i\ \exists x\in G_k\subset G_i\bigr)$。

<!-- unit: T-p4-10 -->
$$
G_x=\{(a,b)\mid x\in(a,b)\subset U\}.
$$

<!-- unit: T-p4-11 -->
$$
\alpha=\inf a,\qquad\beta=\sup b.
$$

<!-- unit: T-p4-12 -->
断言 $(\alpha,\beta)\in G_x$。

<!-- unit: T-p4-12-b -->
且〔Q004：本行右半关系式尚未唯一辨定〕。

原笔可辨 $\beta$ 及其后的 $\notin$；前半变量、第一关系符和两处 $G$ 的下标另存候选与精确局部图位置。

<!-- unit: T-p4-13 -->
**pf：**$x\in(\alpha,\beta)$。

$\forall y\in(\alpha,\beta)$。

<span style="color:red">原稿未完证明：写到任取 y 的起步，尚未写出区间包含于 U 的推导。</span>

<!-- unit: T-p4-14 -->
且 $\alpha\notin U$，$\beta\notin U$。

反证，若不然。

<span style="color:red">原稿未完反证：写到“若不然”，未继续推出端点矛盾。</span>

<!-- unit: T-p5-heading -->
## 原稿第 5 页

<!-- unit: T-p5-01 -->
设 $G\subset\mathbb R$，若 $(a,b)\subset G$。

<!-- unit: T-p5-02 -->
$a\notin G$，$b\notin G$，$(a,b)$ 是 $G$ 的构成区间。

<!-- unit: T-p5-03 -->
**prop：**开集 $G$ 的不同构成区间互不相交。

<!-- unit: T-p5-04 -->
蓝笔补记：反证，可以用两个构成区间。

<span style="color:red">原稿未完反证：只保留了使用两个构成区间的提示，没有写出矛盾步骤。</span>

<!-- unit: T-p5-05 -->
**Cor：**若 $x_0\ne y_0$，包含 $x_0$、$y_0$ 的构成区间
$$
\begin{cases}
\text{相等},\\
\text{不相交}.
\end{cases}
$$
两种情形在原稿右侧用左大括号分列。

<!-- unit: T-p5-06 -->
得到了开区间的唯一表示。

<!-- unit: T-p5-07 -->
$\mathbb R^n$，中可表示为 $(a,b)$ 可数个，且表示不唯一。

<!-- unit: T-p5-08 -->
**Thm：**$(X,\tau)$ 是第二可数，局部连通，$\forall U\subset(X,\tau)$。

<!-- unit: T-p5-09 -->
可表示为至多可数个连通分支的并。

<!-- unit: T-p5-10 -->
**Ex 1：**实区间[Q010]。

<!-- unit: T-p5-11 -->
**pf：**$p$ 进制小数至多有两种展开。

〔中间字词依局部笔画恢复，记录见 Q005；首符按字母 $p$ 排版。〕

<span style="color:red">原稿未完证明：此处只有进制展开提示，没有继续写推导。</span>
