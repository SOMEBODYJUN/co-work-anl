<!-- unit: T-title -->
# 实分析 6：保真转写

<!-- unit: T-p1-heading -->
## 原稿第 1 页

<!-- unit: T-p1-01 -->
### 紧性

<!-- unit: T-p1-02 -->
Lindeloff（空间）：任意开覆盖有可数子覆盖。

<!-- unit: T-p1-03 -->
第二可数 $\Rightarrow X$ 是 Lindeloff，逆不一定。

<!-- unit: T-p1-04 -->
右上浅色旁注：$\Rightarrow$ 反证法，构造子列；$\Leftarrow$ 已知是距离空间。

<!-- unit: T-p1-05 -->
**Ex：**示出整个思路，在 $\mathbb R^n$ 中有界闭集 $\Longleftrightarrow$ 紧。

<!-- unit: T-p1-06 -->
**Th：**设 $M\subset(X,d)$，$M$ 紧，则 $M$ 是有界闭集。（至少是距离空间。）

<!-- unit: T-p1-07 -->
先证 $M^c$ 开。设 $x\in M^c$，即证存在 $\delta$，使 $B(x,\delta)\subset M^c$。

<!-- unit: T-p1-08 -->
由 $T_2$，$\forall y\in M$，由 $T_2$，$\exists\delta_y>0$，
$$
B(x,\delta_y)\cap B(y,\delta_y)=\varnothing.\tag{*}
$$

<!-- unit: T-p1-09 -->
$$
M\subset\bigcup_{y\in M}B(y,\delta_y).
$$
又因 $M$ 紧，
$$
M\subset\bigcup_{i=1}^{m}B(y_i,\delta_{y_i})\qquad\text{（有限）}.
$$

<!-- unit: T-p1-10 -->
令 $\delta=\min\{\delta_{y_1},\ldots,\delta_{y_m}\}$，则由 $(*)$，
$$
B(x,\delta)\cap\left(\bigcup_{i=1}^{m}B(y_i,\delta_{y_i})\right)=\varnothing
\qquad\text{（闭集）}.
$$

<!-- unit: T-p1-11 -->
$$
X=\{a,b\},\qquad\mathcal T=\{\varnothing,X,\{a\}\}.
$$
$\{a\}$ 紧，是开集。
