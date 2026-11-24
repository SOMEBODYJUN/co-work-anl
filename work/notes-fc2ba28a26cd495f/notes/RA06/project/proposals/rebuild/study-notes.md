<!-- unit: N-title -->
# 实分析 6：紧性与度量空间

<!-- unit: N-editorial -->
原稿内容按黑色正文保留；蓝色信息块标明补充、补证或纠错；红色仅标示原稿明确待填的位置。原稿使用的拼写 Lindeloff 在正文中保留，通常拼作 Lindelöf。

<!-- unit: N-p1-01 -->
## 1. 紧性与 Lindeloff 性

<!-- unit: N-p1-definition -->
> [!info] 补充：开覆盖与紧性
> 设 $M$ 是拓扑空间 $X$ 的子集。一族 $X$ 中的开集 $\{U_\alpha\}_{\alpha\in A}$ 若满足 $M\subset\bigcup_{\alpha\in A}U_\alpha$，就称为 $M$ 的开覆盖。若每个开覆盖都有有限子覆盖，就称 $M$ 紧。用子空间中的开覆盖定义紧性，所得概念相同：子空间开集可写作 $M\cap U_\alpha$。

<!-- unit: N-p1-02 -->
**原定义。**Lindeloff（空间）：任意开覆盖有可数子覆盖。

<!-- unit: N-p1-03 -->
**原命题。**第二可数 $\Rightarrow X$ 是 Lindeloff，逆不一定。

<!-- unit: N-p1-countable-proof -->
> [!info] 补证：第二可数蕴含 Lindeloff
> 第二可数指存在可数拓扑基 $\{V_n:n\in\mathbb N\}$。给定开覆盖 $\mathcal U$，对每个满足“存在 $U\in\mathcal U$ 使 $V_n\subset U$”的 $n$，选定这样一个 $U_n$。所选开集至多可数。
> 对任意 $x\in X$，先取覆盖中的 $U$ 使 $x\in U$，再由基的定义选 $V_n$ 使 $x\in V_n\subset U$。该 $n$ 参与上述选择，所以 $x\in V_n\subset U_n$。因此 $\{U_n\}$ 覆盖 $X$。

<!-- unit: N-p1-04 -->
**原旁注。**$\Rightarrow$ 反证法，构造子列；$\Leftarrow$ 已知是距离空间。

<!-- unit: N-p1-margin-explanation -->
> [!info] 补充：旁注的范围及度量空间中的逆命题
> 原稿将这两条方向提示写在页右上，没有画线指向某个完整公式，故保留其原位置关系而不强行指定所证命题。与本页命题相关的准确结论是：度量空间中，Lindeloff 性也蕴含第二可数。
> 对每个正整数 $n$，从覆盖 $\{B(x,1/n):x\in X\}$ 中选可数子覆盖，记所选中心集为 $D_n$。则 $D=\bigcup_nD_n$ 可数且稠密：给定 $x$ 及 $\varepsilon>0$，取 $1/n<\varepsilon$，有某个 $d\in D_n$ 使 $d(x,d)<1/n<\varepsilon$。
> 集合族 $\{B(d,q):d\in D,\ q\in\mathbb Q_{>0}\}$ 是可数基。若 $x\in U$ 且 $B(x,\varepsilon)\subset U$，选 $d\in D$ 使 $d(x,d)<\varepsilon/3$，再选有理数 $q$ 使 $d(x,d)<q<\varepsilon-d(x,d)$。于是 $x\in B(d,q)\subset B(x,\varepsilon)\subset U$。

<!-- unit: N-p1-nonconverse -->
> [!info] 补充：一般拓扑空间中逆命题的反例
> 在不可数集合 $X$ 上取余可数拓扑：开集为 $\varnothing$ 和所有补集至多可数的集合。任给开覆盖，选其中一个非空开集 $U$；$X\setminus U$ 至多可数，再为其中每一点各选一个覆盖成员，就得到可数子覆盖。
> 它不满足第二可数。若在 $x$ 处有可数局部基 $\{V_n\}$，每个 $V_n$ 都不可数，可递归选互异的 $x_n\in V_n\setminus\{x\}$。开集 $X\setminus\{x_n:n\in\mathbb N\}$ 含 $x$，却不包含任何 $V_n$，矛盾。

<!-- unit: N-p1-06 -->
## 2. 度量空间中的紧集必有界且闭

**原定理。**设 $M\subset(X,d)$ 且 $M$ 紧，则 $M$ 是有界闭集。原稿括注：“至少是距离空间”。

<!-- unit: N-p1-07 -->
### 2.1 原稿路线：用有限子覆盖证明闭性

先证 $M^c$ 开。固定 $x\in M^c$，目标是找到 $\delta>0$ 使 $B(x,\delta)\subset M^c$。

<!-- unit: N-p1-08 -->
由 $T_2$，对每个 $y\in M$，存在 $\delta_y>0$，使
$$
B(x,\delta_y)\cap B(y,\delta_y)=\varnothing.\tag{2.1}
$$
原稿在这一句中重复写了两次“由 $T_2$”。

<!-- unit: N-p1-radius -->
> [!info] 补充：共同半径的具体选择
> 因 $x\notin M$、$y\in M$，有 $d(x,y)>0$，可取 $\delta_y=d(x,y)/3$。若某点同时属于两个球，三角不等式给出 $d(x,y)<2d(x,y)/3$，矛盾。此处“$T_2$”表示 Hausdorff 分离性；在一般 Hausdorff 空间中可改用两组不交开邻域证明紧子集闭，但“有界”需要度量等额外结构。

<!-- unit: N-p1-09 -->
这些球给出开覆盖
$$
M\subset\bigcup_{y\in M}B(y,\delta_y).
$$
因 $M$ 紧，存在 $y_1,\ldots,y_m\in M$，使
$$
M\subset\bigcup_{i=1}^{m}B(y_i,\delta_{y_i}).
$$

<!-- unit: N-p1-10 -->
令
$$
\delta=\min\{\delta_{y_1},\ldots,\delta_{y_m}\}>0.
$$
由式 (2.1)，
$$
B(x,\delta)\cap\left(\bigcup_{i=1}^{m}B(y_i,\delta_{y_i})\right)=\varnothing.
$$
因此 $B(x,\delta)\subset M^c$，所以 $M^c$ 开，$M$ 闭。

<!-- unit: N-p1-empty -->
> [!info] 补充：空集边界情形
> 若 $M=\varnothing$，闭性和有界性都直接成立，不需要取上述有限个半径的最小值。

<!-- unit: N-p1-11 -->
### 2.2 原稿反例：一般拓扑空间中的紧集未必闭

$$
X=\{a,b\},\qquad\mathcal T=\{\varnothing,X,\{a\}\}.
$$
原稿结论：$\{a\}$ 紧，是开集。

<!-- unit: N-p1-example-explain -->
> [!info] 补充：反例的完整核验
> $\{a\}$ 的任意开覆盖必有一个成员含 $a$，单取这一成员就是有限子覆盖，故 $\{a\}$ 紧。它属于 $\mathcal T$，所以开；但其补集 $\{b\}$ 不在 $\mathcal T$ 中，所以它不闭。此空间不是 Hausdorff：含 $b$ 的唯一开邻域是 $X$，必与含 $a$ 的开邻域相交。因此去掉分离性后，紧子集闭的结论确实会失效。

<!-- unit: N-p1-05 -->
## 3. 原稿练习：欧氏空间中的 Heine–Borel 结论

**题目。**示出整个思路，在 $\mathbb R^n$ 中有界闭集 $\Longleftrightarrow$ 紧。

<!-- unit: N-p1-exercise-answer -->
> [!info] 补证：练习的完整解答
> 正向先证明闭长方体 $Q\subset\mathbb R^n$ 紧。若有开覆盖没有有限子覆盖，将 $Q$ 每条边二等分；在所得有限个小长方体中，至少一个仍不能被有限个覆盖成员盖住。递归得到嵌套闭长方体 $Q_1\supset Q_2\supset\cdots$，其直径趋于零。每个坐标区间的端点单调且有界，故存在唯一公共点 $x\in\bigcap_kQ_k$。取一个覆盖成员 $U$ 含 $x$，由开性存在 $\varepsilon>0$ 使 $B(x,\varepsilon)\subset U$。当 $k$ 足够大，$\operatorname{diam}Q_k<\varepsilon$，且 $x\in Q_k$，故 $Q_k\subset U$，与选择矛盾。
> 现在设 $F\subset\mathbb R^n$ 有界且闭。选闭长方体 $Q$ 包含 $F$。给 $F$ 的任意开覆盖补上开集 $\mathbb R^n\setminus F$，就成为 $Q$ 的开覆盖。从中取有限子覆盖，删去补上的开集后，剩余成员仍覆盖 $F$，故 $F$ 紧。
> 反向的闭性已由 §2.1 证明。证明有界性：若 $F\ne\varnothing$，固定 $x_0\in F$。开球族 $\{B(x_0,k):k\in\mathbb N_{>0}\}$ 覆盖 $F$，紧性给出有限子覆盖，取所用整数的最大值 $N$，即得 $F\subset B(x_0,N)$。空集的情形直接成立。
