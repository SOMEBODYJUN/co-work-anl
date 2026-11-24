<!-- unit: N-title -->
# 实分析 6：紧性、导集与开集分解

<!-- unit: N-editorial -->
原稿内容按黑色正文保留；蓝色信息块标明补充、补证或纠错；红色仅标示原稿明确待填的位置。原稿使用的拼写 Lindeloff 在正文中保留，通常拼作 Lindelöf。

<!-- unit: N-toc -->
## 目录

- [1. 紧性与 Lindeloff 性](#s1)
- [2. 度量空间中的紧集必有界且闭](#s2)
  - [2.1 原稿路线：用有限子覆盖证明闭性](#s2-1)
  - [2.2 原稿反例：一般拓扑空间中的紧集未必闭](#s2-2)
  - [2.3 补证：紧集必有界](#s2-3)
  - [2.4 证明工具：紧空间的闭子集仍紧](#s2-4)
- [3. 原稿练习：欧氏空间中的 Heine–Borel 结论](#s3)
  - [3.1 完整解答：嵌套方块的公共点路线](#s3-1)
  - [3.2 原稿的等价关系提要](#s3-2)
  - [3.3 子列工具：有限维 Bolzano–Weierstrass 定理](#s3-3)
  - [3.4 原稿路线：二分闭方块证明 Heine–Borel](#s3-4)
- [4. 导集、自密集与孤立点](#s4)
  - [4.1 完全集](#s4-1)
- [5. 实轴开集、局部区间与基的计数](#s5)
  - [5.1 原稿 Ex 1 与计数旁注](#s5-1)
  - [5.2 点的邻域：原稿两问及解答](#s5-2)
  - [5.3 原稿路线：构造含点的最大开区间](#s5-3)
  - [5.4 原稿 Ex 2：通常实轴的拓扑基有多少种](#s5-4)
- [6. 构成区间与开集的唯一分解](#s6)
  - [6.1 先备例题：实区间连通](#s6-1)
  - [6.2 构成区间的定义](#s6-2)
  - [6.3 不同构成区间不相交](#s6-3)
  - [6.4 唯一分解及可数性](#s6-4)
  - [6.5 原旁注：高维的表示不唯一](#s6-5)
- [7. 第二可数、局部连通空间中的开集分解](#s7)

<!-- unit: N-p1-01 -->
<a id="s1"></a>
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
<a id="s2"></a>
## 2. 度量空间中的紧集必有界且闭

**原定理。**设 $M\subset(X,d)$ 且 $M$ 紧，则 $M$ 是有界闭集。原稿括注：“至少是距离空间”。

<!-- unit: N-p1-07 -->
<a id="s2-1"></a>
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
<a id="s2-2"></a>
### 2.2 原稿反例：一般拓扑空间中的紧集未必闭

$$
X=\{a,b\},\qquad\mathcal T=\{\varnothing,X,\{a\}\}.
$$
原稿结论：$\{a\}$ 紧，是开集。

<!-- unit: N-p1-example-explain -->
> [!info] 补充：反例的完整核验
> $\{a\}$ 的任意开覆盖必有一个成员含 $a$，单取这一成员就是有限子覆盖，故 $\{a\}$ 紧。它属于 $\mathcal T$，所以开；但其补集 $\{b\}$ 不在 $\mathcal T$ 中，所以它不闭。此空间不是 Hausdorff：含 $b$ 的唯一开邻域是 $X$，必与含 $a$ 的开邻域相交。因此去掉分离性后，紧子集闭的结论确实会失效。

<!-- unit: N-compact-bounded-proof -->
<a id="s2-3"></a>
### 2.3 补证：紧集必有界

> [!info] 补证：把有界性的论证置于调用前
> 若 $M=\varnothing$，结论成立。否则固定 $x_*\in M$，开球族 $\{B(x_*,k):k\in\mathbb N_{>0}\}$ 覆盖 $M$。紧性给出有限子覆盖。取其中所用半径的最大值 $N$，就有 $M\subset B(x_*,N)$，故 $M$ 有界。

<!-- unit: N-p2-02 -->
<a id="s2-4"></a>
### 2.4 证明工具：紧空间的闭子集仍紧

原稿括注：“闭[Q001]性”。原引理：在 $(X,\tau)$ 中，$M$ 紧，$F$ 是 $M$ 的闭子集，则 $F$ 紧。

<!-- unit: N-p2-closed-proof -->
> [!info] 补证：闭子集引理
> 给定 $F$ 的相对开覆盖 $\{U_\alpha\}$，可将各成员写为 $F\cap V_\alpha$，其中 $V_\alpha$ 在 $M$ 中开。因 $F$ 在 $M$ 中闭，$M\setminus F$ 在 $M$ 中开。于是 $\{V_\alpha\}\cup\{M\setminus F\}$ 是紧空间 $M$ 的开覆盖。选出有限子覆盖后删去 $M\setminus F$，对应的有限个 $U_\alpha$ 仍覆盖 $F$。
> 这通常称为紧性的闭遗传性。原稿括注中间的两个字尚在独立识读记录 Q001 中保留候选，不影响引理正文和证明。

<!-- unit: N-p1-05 -->
<a id="s3"></a>
## 3. 原稿练习：欧氏空间中的 Heine–Borel 结论

**题目。**示出整个思路，在 $\mathbb R^n$ 中有界闭集 $\Longleftrightarrow$ 紧。

<!-- unit: N-p1-exercise-answer -->
<a id="s3-1"></a>
### 3.1 完整解答：嵌套方块的公共点路线

> [!info] 补证：练习的完整解答
> 正向先证明闭长方体 $Q\subset\mathbb R^n$ 紧。若有开覆盖没有有限子覆盖，将 $Q$ 每条边二等分；在所得有限个小长方体中，至少一个仍不能被有限个覆盖成员盖住。递归得到嵌套闭长方体 $Q_1\supset Q_2\supset\cdots$，其直径趋于零。每个坐标区间的端点单调且有界，故存在唯一公共点 $x\in\bigcap_kQ_k$。取一个覆盖成员 $U$ 含 $x$，由开性存在 $\varepsilon>0$ 使 $B(x,\varepsilon)\subset U$。当 $k$ 足够大，$\operatorname{diam}Q_k<\varepsilon$，且 $x\in Q_k$，故 $Q_k\subset U$，与选择矛盾。
> 现在设 $F\subset\mathbb R^n$ 有界且闭。选闭长方体 $Q$ 包含 $F$。给 $F$ 的任意开覆盖补上开集 $\mathbb R^n\setminus F$，就成为 $Q$ 的开覆盖。从中取有限子覆盖，删去补上的开集后，剩余成员仍覆盖 $F$，故 $F$ 紧。
> 反向的闭性已由 §2.1 证明。证明有界性：若 $F\ne\varnothing$，固定 $x_0\in F$。开球族 $\{B(x_0,k):k\in\mathbb N_{>0}\}$ 覆盖 $F$，紧性给出有限子覆盖，取所用整数的最大值 $N$，即得 $F\subset B(x_0,N)$。空集的情形直接成立。

<!-- unit: N-p2-01 -->
<a id="s3-2"></a>
### 3.2 原稿的等价关系提要

原稿写：“有限性：iff 列紧 $\Longleftrightarrow$ 闭集有界。可以定义有限性（某些教材）。”

<!-- unit: N-p2-scope -->
> [!info] 补充：提要的适用范围
> 此处保留原稿“有限性”的用词；结合本页后面的 Heine–Borel 定理，这一提要讨论的是有限子覆盖所定义的紧性。对于 $\mathbb R^n$ 的子集，紧、列紧、有界闭三者等价。在一般度量空间中，紧与列紧等价，但“有界闭”不能单独推出紧；例如无限集合配离散度量 $d(x,y)=1$（$x\ne y$），整个空间有界且闭，单点开集组成的覆盖却没有有限子覆盖。

<!-- unit: N-sequential-equivalence-proof -->
> [!info] 补证：度量空间中紧与列紧等价
> 列紧指每个点列都有收敛到空间内某点的子列。
> **紧 $\Rightarrow$ 列紧。**给定点列 $(x_n)$。若每一点都有一个只含有限多个点列指标的邻域，紧性选出的有限子覆盖就只能包含有限多个指标，与点列有无限多个指标矛盾。所以存在 $x$，使每个 $B(x,1/k)$ 都含有无限多个点列指标。可递归选 $n_1<n_2<\cdots$ 且 $x_{n_k}\in B(x,1/k)$，从而 $x_{n_k}\to x$。
> **列紧 $\Rightarrow$ 紧。**先证对每个 $\varepsilon>0$ 有有限个半径 $\varepsilon$ 的球覆盖空间，否则可递归选点，使任意两点的距离至少为 $\varepsilon$，这种点列没有收敛子列，矛盾。
> 再给定任意开覆盖 $\mathcal U$，证明存在 $\delta>0$，使每个球 $B(x,\delta)$ 都包含于某个覆盖成员。如果不存在，选 $x_n$ 使 $B(x_n,1/n)$ 不包含于任何成员。列紧给出 $x_{n_k}\to x$；取 $U\in\mathcal U$ 含 $x$，再取 $r>0$ 使 $B(x,r)\subset U$。当 $k$ 足够大时，$d(x_{n_k},x)<r/2$ 且 $1/n_k<r/2$，便有 $B(x_{n_k},1/n_k)\subset U$，矛盾。
> 最后用第一步选有限个半径 $\delta$ 的球覆盖空间，每个球都包含于一个覆盖成员，故取出有限子覆盖。上述球和开集均可理解为空间自身或给定子空间中的球和开集。

<!-- unit: N-bw-tool -->
<a id="s3-3"></a>
### 3.3 子列工具：有限维 Bolzano–Weierstrass 定理

> [!info] 补证：有界点列有收敛子列
> 一维情形中，把含有界数列所有项的闭区间二等分，选一个含无限多个指标的闭半区间；持续二分，得到嵌套闭区间 $I_k=[a_k,b_k]$，各含无限多个点列指标，长度趋于零。
> 由实数完备性，$x=\sup_k a_k$ 存在。对每个固定 $k$，所有左端点都不超过 $b_k$，故 $a_k\le x\le b_k$，于是 $x\in\bigcap_k I_k$；长度趋零保证公共点唯一。递归选递增指标 $n_k$，使第 $n_k$ 项落在 $I_k$ 中，便有 $|x_{n_k}-x|\le b_k-a_k\to0$。
> 对 $\mathbb R^n$ 中的有界点列，先按第一坐标抽取收敛子列，再从此子列按第二坐标抽取子列，直到第 $n$ 坐标。最后的子列每个坐标都收敛，因而在欧氏范数下收敛。该论证只用实数完备性和有限次抽列，不依赖 Heine–Borel 定理。

<!-- unit: N-norm-equivalence-tool -->
> [!info] 补充：题设若取任意范数
> 设 $\|\cdot\|$ 是 $\mathbb R^n$ 的任意范数，$e_i$ 为标准基。由三角不等式与 Cauchy–Schwarz 不等式，
> $$
> \|x\|\le\sum_{i=1}^n|x_i|\|e_i\|\le C\|x\|_2,
> \qquad C=\left(\sum_i\|e_i\|^2\right)^{1/2}.
> $$
> 也存在 $c>0$ 使 $c\|x\|_2\le\|x\|$。否则可取 $\|x_k\|_2=1$ 而 $\|x_k\|\to0$；刚证明的 Bolzano–Weierstrass 定理给出欧氏收敛子列 $x_{k_j}\to x$，其中 $\|x\|_2=1$。上界估计给出 $\|x_{k_j}-x\|\to0$，再由反三角不等式得 $\|x\|=0$，矛盾。
> 所以两种范数给出相同的开集、收敛、闭集和有界性，紧性结论也相同。原稿直径公式中的 $\sqrt n$ 对应欧氏范数；任意范数时可再乘上常数 $C$。

<!-- unit: N-p2-03 -->
<a id="s3-4"></a>
### 3.4 原稿路线：二分闭方块证明 Heine–Borel

原稿标题拼作“Hine Borel”。设 $M\subset(\mathbb R^n,\|\cdot\|)$，$M$ 有界且闭，则 $M$ 紧。

<!-- unit: N-p2-04 -->
原稿从有界性开始：$\exists a>0$，使 $M\subset[-a,a]^{\text{[Q002]}}$。这里指数笔形不清，留中性编号；下一行明确出现指数 $n$。

<!-- unit: N-p2-05 -->
原稿下一行写“仅证 $[-a,a)^n$ 是紧的”，右端点的括号形状保留如原图。

<!-- unit: N-p2-cube-exponent -->
> [!info] 上下文恢复：方块的指数
> 原稿上一行的指数据 $M\subset\mathbb R^n$、后续 $2^n$ 等分及直径公式恢复为 $n$；这属于数学语境恢复，不能单凭证明正确就判定原笔画。

<!-- unit: N-p2-cube-correction -->
> [!info] 纠错：必须使用闭方块
> 此证明应取 $Q_0=[-a,a]^n$。
> 若按半开方块 $[-a,a)^n$ 理解，则它不是紧集：在第一坐标中取趋向被排除端点 $a$ 的点列，其极限不属于该集合。后面使用嵌套闭区间的步骤也要求各 $Q_m$ 闭。因此学习时统一采用闭方块，保真转写另存原括号形状。
> 由 §2.4，只需证明 $Q_0$ 紧，因为 $M$ 是 $Q_0$ 的相对闭子集。直径中 $\sqrt n$ 的常数对应欧氏范数；若题设范数任意，须使用有限维范数等价或相应的常数估计。

<!-- unit: N-p2-06 -->
任取开覆盖 $\{G_i\}$。反设 $Q_0$ 无有限子覆盖。

<!-- unit: N-p2-07 -->
将 $Q_0$ 等分成 $2^n$ 个小方块，至少存在一个小方块仍无有限子覆盖。原稿此处将所取小方块记为 $Q_m$。

<!-- unit: N-p2-first-index -->
> [!info] 纠错：首次细分的编号
> 为使递归编号连贯，第一次选择应记为 $Q_1$。若每个小方块都有有限子覆盖，把这有限多个有限族并起来就能覆盖 $Q_0$，与反设矛盾。

<!-- unit: N-p2-08 -->
归纳地，把 $Q_m$ 等分为 $2^n$ 个小方块，再选其中一个无有限子覆盖的方块 $Q_{m+1}$。

<!-- unit: N-p2-09 -->
于是
$$
Q_0\supset Q_1\supset\cdots\supset Q_m\supset Q_{m+1}\supset\cdots.
$$

<!-- unit: N-p2-10 -->
且
$$
\operatorname{diam}(Q_m)\leq\frac{2a\sqrt n}{2^m}.
$$
原稿证明接续下一物理页。

<!-- unit: N-p3-01 -->
原稿接续：在相邻方块的差集中选点，
$$
x_{m+1}\in Q_m\setminus Q_{m+1}.
$$

<!-- unit: N-p3-02 -->
于是 $\{x_m\}\subset Q_0$。

<!-- unit: N-p3-03 -->
原稿再取收敛子列：
$$
x_{m_k}\longrightarrow x_0\in\mathbb R^n,
\qquad x_0\in Q_0.
$$

<!-- unit: N-p3-subsequence-explain -->
> [!info] 补充：为何能取子列、为何极限留在方块中
> 方块 $Q_0$ 有界，所以点列有界；有限维 Bolzano–Weierstrass 定理给出收敛子列。$Q_0$ 是闭集，故子列极限仍在 $Q_0$ 中。这里使用的是有界点列的子列定理，尚未把“闭有界集紧”作为前提，避免循环论证。

<!-- unit: N-p3-04 -->
原稿写 $x_0\in Q\subset\bigcup_{\lambda\in\Lambda}G_\lambda$，此处 $Q$ 承接初始方块 $Q_0$。

<!-- unit: N-p3-05 -->
从而存在 $\lambda_0$ 使 $x_0\in G_{\lambda_0}$（原行在 $x$ 处省略下标 $0$）。

<!-- unit: N-p3-06 -->
由覆盖成员的开性，存在 $\delta>0$，使
$$
B(x_0,\delta)\subset G_{\lambda_0}.
$$

<!-- unit: N-p3-07 -->
原稿继续写：当 $k$ 充分大时，
$$
\|x_{m_k}-x_0\|<\frac\delta2,
\qquad\operatorname{diam}(Q_{m_k})<\frac\delta2.
$$

<!-- unit: N-p3-08 -->
原稿末行：$Q_{m_k}\subset B(x_0,\delta)\subset G_{\lambda_0}$。

<!-- unit: N-p3-index-repair -->
> [!info] 纠错与补证：下标错位及矛盾的完整结束
> 按前面所选 $x_{m+1}\in Q_m\setminus Q_{m+1}$，只能保证 $x_{m_k}\in Q_{m_k-1}$，原稿末行不能直接用 $Q_{m_k}$ 的直径控制它与方块内各点的距离。保留原选点路线时，应选 $k$ 充分大，使
> $$
> \|x_{m_k}-x_0\|<\frac\delta2,
> \qquad\operatorname{diam}(Q_{m_k-1})<\frac\delta2.
> $$
> 对任意 $y\in Q_{m_k-1}$，由三角不等式，
> $$
> \|y-x_0\|\le\|y-x_{m_k}\|+\|x_{m_k}-x_0\|
> \le\operatorname{diam}(Q_{m_k-1})+\|x_{m_k}-x_0\|<\delta.
> $$
> 所以 $Q_{m_k-1}\subset B(x_0,\delta)\subset G_{\lambda_0}$。一个覆盖成员就盖住了 $Q_{m_k-1}$，与它无有限子覆盖的选择矛盾。故 $Q_0$ 紧，再由闭子集引理得 $M$ 紧。
> 另一种等价修订是从开始直接取 $x_m\in Q_m$，这样原稿末尾的 $Q_{m_k}$ 下标可以保留。两种修订都只修复下标，不改变“二分—子列—开球”的证明路线。

<!-- unit: N-derived-heading -->
<a id="s4"></a>
## 4. 导集、自密集与孤立点

<!-- unit: N-derived-definition -->
> [!info] 补充：导集与孤立点的记号
> 以下在度量空间 $(X,d)$ 内讨论。$E'$ 表示 $E$ 的导集：点 $x$ 属于 $E'$，是指每个去心球 $B(x,r)\setminus\{x\}$ 都与 $E$ 相交。$\operatorname{Iso}(E)$ 表示 $E$ 的孤立点集合，即满足某个 $r>0$ 使 $B(x,r)\cap E=\{x\}$ 的点 $x\in E$。$\overline E$ 是闭包，$E^\circ$ 是内部，$\partial E$ 是边界。

<!-- unit: N-p3-09 -->
**原定义与判别。**自密：$E\subset E'$。闭集的判别：$E'\subset E$。

<!-- unit: N-derived-basic-proof -->
> [!info] 补证：闭包分解与闭集判别
> 若 $x\in\overline E\setminus E$，则每个球都与 $E$ 相交，而 $x\notin E$，所以 $x\in E'$。反之，$E\subset\overline E$ 且 $E'\subset\overline E$，于是 $\overline E=E\cup E'$。因此 $E$ 闭当且仅当 $\overline E=E$，也当且仅当 $E'\subset E$。
> 对 $x\in E$，不是聚点就意味着存在某个球只在 $x$ 处与 $E$ 相交，即 $x$ 是孤立点。因此 $E\setminus E'=\operatorname{Iso}(E)$，并且
> $$
> \overline E=E'\mathbin{\dot\cup}\operatorname{Iso}(E).
> $$
> 点上方的点并符号表示不交并。这一公式即原稿浅色旁注所用的分解。

<!-- unit: N-p3-12 -->
**原等价命题。**对于度量空间中的集合 $E$，
$$
E\text{ 自密}\quad\Longleftrightarrow\quad\operatorname{Iso}(E)=\varnothing.
$$

<!-- unit: N-p3-13 -->
原稿的 $\Rightarrow$ 浅色旁证写：$\overline E=E'\mathbin{\dot\cup}\operatorname{Iso}$，并记“$\operatorname{Iso}\notin E'$”。

<!-- unit: N-p3-forward-repair -->
> [!info] 说明与补证：孤立点集和导集不交
> 原记号把集合与元素的“不属于”混用；准确写法是 $\operatorname{Iso}(E)\cap E'=\varnothing$。若 $E$ 自密，则 $E\subset E'$；又 $\operatorname{Iso}(E)\subset E$，因此孤立点集同时包含于 $E'$ 且与它不交，只能为空。

<!-- unit: N-p3-14 -->
原稿的 $\Leftarrow$ 浅色旁证写：
$$
E'=\overline E=E\cup E'\quad\Rightarrow\quad E\subset E'.
$$

<!-- unit: N-p3-backward-explain -->
> [!info] 补证：无孤立点蕴含自密
> 前提是 $\operatorname{Iso}(E)=\varnothing$。把它代入闭包的不交分解，得到 $\overline E=E'$；再由 $E\subset\overline E$ 得 $E\subset E'$。这正是原稿右向回推中省略的前提。

<!-- unit: N-p3-15 -->
原稿另外记：“前文证过（$E'$ 是闭），（闭）$'\subset$（闭）”。

<!-- unit: N-derived-closed-proof -->
> [!info] 补证：度量空间中导集是闭集
> 设 $x\notin E'$。存在 $r>0$，使 $(B(x,r)\setminus\{x\})\cap E=\varnothing$。若 $y\in B(x,r/2)$ 且 $y\ne x$，可取 $0<\rho<\min\{d(x,y),r-d(x,y)\}$。于是 $B(y,\rho)\subset B(x,r)\setminus\{x\}$，故这个球与 $E$ 不交，所以 $y\notin E'$。而 $x$ 本来不在 $E'$，故 $B(x,r/2)\subset X\setminus E'$。补集开，导集闭。

<!-- unit: N-p3-10 -->
原稿写出的高阶导集关系为
$$
E^{(n)}\subset(E^{n-1})'.
$$
原式右侧上标没有括号，包含号照原式保留。

<!-- unit: N-p3-11 -->
原稿随后要求 proof：$E^{(n)}\subset E^{(n-1)}$。

<!-- unit: N-derived-iteration -->
> [!info] 补充与限定：高阶导集的定义和下降性
> 按通常递归记号，令 $E^{(0)}=E$，$E^{(1)}=E'$，并令 $E^{(n)}=(E^{(n-1)})'$。因此原稿前一行的包含关系实际可写成等号。
> 对 $n\ge2$，$E^{(n-1)}$ 已是某个集合的导集，所以闭；由闭集判别得
> $$
> E^{(n)}=(E^{(n-1)})'\subset E^{(n-1)}.
> $$
> 对 $n=1$，$E'\subset E$ 需要额外假设 $E$ 闭，一般不能直接成立。例如 $E=(0,1)\subset\mathbb R$ 时，$E'=[0,1]\not\subset E$。若原命题从闭集 $E$ 开始，则下降关系对所有 $n\ge1$ 成立。

<!-- unit: N-p3-16 -->
原稿另记
$$
\overline E=E=E^\circ\cup\partial E,
\qquad E'\subset E.
$$

<!-- unit: N-p3-closure-scope -->
> [!info] 补充：这条旁注的闭集条件
> 这里第一处等号 $\overline E=E$ 明确需要 $E$ 闭。在此条件下，$\overline E=E^\circ\cup\partial E$ 给出内部与边界的分解，而 $E'\subset E$ 是同一个闭性条件的导集表述。

<!-- unit: N-p4-01 -->
<a id="s4-1"></a>
### 4.1 完全集

**原定义。**perfect set $\Longleftrightarrow E=E'$，即自密闭集。

<!-- unit: N-perfect-proof -->
> [!info] 补证与例子
> $E=E'$ 同时给出 $E\subset E'$ 和 $E'\subset E$，分别表示自密与闭。反过来，这两个包含关系一起给出相等。因此完全集就是没有孤立点的闭集。
> 例如 $[0,1]\subset\mathbb R$ 是完全集：每个点（包括两个端点）都是它的聚点，且区间闭；$(0,1)$ 自密但不闭；$\{0\}\cup\{1/n:n\ge1\}$ 闭，但各 $1/n$ 是孤立点，所以不完美。按 $E=E'$ 的定义，空集也满足；某些教材另把非空写入定义，使用时应看具体约定。

<!-- unit: N-open-heading -->
<a id="s5"></a>
## 5. 实轴开集、局部区间与基的计数

<!-- unit: N-p4-02 -->
<a id="s5-1"></a>
### 5.1 原稿 Ex 1 与计数旁注

原题首行写“$\mathbb R$ 能[Q003]拓扑；$2^c$”。中间字词和所数对象尚未唯一确定，保留原句与原数值。

<!-- unit: N-p4-04 -->
原稿右侧同时记 $(\mathbb R,\tau)$、$\mathcal P(\mathbb R)=2^c$、$\mathcal U\subseteq\mathcal P(\mathbb R)$，并把 $2^c$ 框起强调。

<!-- unit: N-cardinality-distinction -->
> [!info] 说明与可确定部分的完整解答
> 令 $c=|\mathbb R|=2^{\aleph_0}$。$|\mathcal P(\mathbb R)|=2^c$ 计算的是实数集的所有子集；“通常拓扑中的开集数”“通常拓扑的基有多少种”与“在同一底集上能赋予多少个拓扑”是不同问题，不能互换。
> 通常拓扑的开集恰有 $c$ 个。设 $\mathcal B_0=\{(p,q):p,q\in\mathbb Q,p<q\}$；这是可数基，每个开集都是其中某个子族的并，故开集总数不超过 $2^{\aleph_0}=c$。而不同实数 $a$ 给出不同开集 $(-\infty,a)$，所以至少有 $c$ 个，合得恰为 $c$。
> 原题若询问的是所有拓扑结构，单凭 $|\mathcal P(\mathbb R)|=2^c$ 并不能得出原行结论；本稿保留 Q003 的对象歧义，不把后面的开集和基计数冒作该题的字面恢复。

<!-- unit: N-topology-count-candidate -->
> [!info] 候选题意的完整解答：若问实数底集上的全部拓扑
> 若 Ex 1 的题意是“实数集上能赋予多少个拓扑”，答案为 $2^{2^c}$。这与原稿的 $2^c$ 不同；以下证明只回答这一明确的数学问题，不把它当作 Q003 字形已确认的依据。该计数结论可参见 Tycho Neve 的 [《Theorems on ultrafilters》](https://math.leidenuniv.nl/scripties/NeveBach.pdf)，Corollary 2.6（正文第9页）；下面直接给出所需构造。
>
> **先构造有限独立集族。**设 $K$ 为无限集，$|K|=\kappa$，令
> $$D=\{(s,H):s\subset K\text{ 有限},\ H\subset\mathcal P(s)\}.$$
> 每个固定有限 $s$ 只有有限多个 $H$，而 $K$ 的有限子集共有 $\kappa$ 个，故 $|D|=\kappa$。对每个 $A\subset K$ 定义
> $$I_A=\{(s,H)\in D:A\cap s\in H\}.$$
> 给定有限多个不同的 $A_i$，并指定每个 $I_{A_i}$ 取自身还是取补集。在每对 $A_i,A_j$ 的对称差中各取一点，合为有限集 $s$，就使所有 $A_i\cap s$ 两两不同。令 $H$ 恰好由指定取自身的那些迹组成，则 $(s,H)$ 同时属于指定的每个集合或补集。因此每个这样的有限交都非空。空有限交取 $D$。不同 $A$ 给出不同 $I_A$，所以该独立族有 $2^\kappa$ 个成员。
>
> **由方向选择产生不同拓扑。**对每个函数 $\varepsilon:\mathcal P(K)\to\{0,1\}$，令 $J_A=I_A$（当 $\varepsilon(A)=1$）或 $J_A=D\setminus I_A$（当 $\varepsilon(A)=0$）。用这些 $J_A$ 的有限交为基，定义
> $$\mathcal F_\varepsilon=\{U\subset D:\text{某个有限交 }J_{A_1}\cap\cdots\cap J_{A_r}\subset U\}.$$
> 有限独立性保证 $\varnothing\notin\mathcal F_\varepsilon$；该族含 $D$、向上封闭、对有限交封闭。这样的集合族称为真滤子。于是 $\tau_\varepsilon=\mathcal F_\varepsilon\cup\{\varnothing\}$ 是拓扑：有限交封闭已证；非空族的并包含其中任一成员，因而由向上封闭仍在该族中；空族之并则是空集。
> 若 $\varepsilon\ne\eta$，选 $A$ 使二者在 $A$ 处不同。不妨 $\varepsilon(A)=1$、$\eta(A)=0$，则 $I_A\in\mathcal F_\varepsilon$，而 $D\setminus I_A\in\mathcal F_\eta$。真滤子不能同时含一个集合及其补集，否则含空集；故 $I_A\notin\mathcal F_\eta$，两拓扑不同。方向函数共有 $2^{2^\kappa}$ 个，所以拓扑数至少如此多。
> 另一方面，每个拓扑都是 $\mathcal P(D)$ 的子集，故总数至多为 $|\mathcal P(\mathcal P(D))|=2^{2^\kappa}$。上下界相等，再用固定双射将拓扑搬回原底集，得到所求结论。取 $\kappa=c$，即得 $2^{2^c}$。
> 这里计数的是固定底集上的全部拓扑，没有再要求可度量、Hausdorff 或第二可数，也不是按同胚分类。通常实轴的开集数仍为 $c$，其拓扑基的种数则为 $2^c$，后者另见 §5.4。

<!-- unit: N-p4-03 -->
<a id="s5-2"></a>
### 5.2 点的邻域：原稿两问及解答

设 $\varnothing\ne U$ 是 $(\mathbb R,|\cdot|)$ 的开集。

<!-- unit: N-p4-05 -->
**$Q_1$：**给定 $x\in U$，满足 $B(x,\delta)\subset U$ 的球有多少个？

<!-- unit: N-ball-count-answer -->
> [!info] 补证：$Q_1$ 的完整解答
> 由开性可取 $r>0$，使 $B(x,r)\subset U$。每个 $0<\delta\le r$ 都给出一个符合条件的球，且在实轴上不同半径的球不同。因此至少有 $c$ 个。所有候选半径组成 $(0,\infty)$ 的子集，总数不超过 $c$，故恰有 $c$ 个。

<!-- unit: N-p4-06 -->
**$Q_2$：**有无最大？

<!-- unit: N-ball-max-answer -->
> [!info] 补证：分清“同心球”与“含点开区间”的最大性
> 若仍指 $Q_1$ 中以固定 $x$ 为中心的球，当 $U\ne\mathbb R$ 时，令 $r_*=\inf\{|x-z|:z\in\mathbb R\setminus U\}$。开性保证 $r_*>0$，补集非空保证 $r_*<\infty$。若 $|y-x|<r_*$ 则 $y\in U$，故 $B(x,r_*)\subset U$；若 $r>r_*$，由下确界定义可找补集中的 $z$ 满足 $|x-z|<r$，故 $B(x,r)\not\subset U$。因此最大球是 $B(x,r_*)$。当 $U=\mathbb R$ 时半径可任意增大，没有最大有限半径球。
> 原稿后续改用所有含 $x$ 的开区间，它们不必以 $x$ 为中心。该集合族有唯一最大成员，端点允许为 $\pm\infty$。下面完整保留原稿构造路线。

<!-- unit: N-p4-10 -->
<a id="s5-3"></a>
### 5.3 原稿路线：构造含点的最大开区间

对 $x\in U$，原稿定义
$$
G_x=\{(a,b)\mid x\in(a,b)\subset U\}.
$$

<!-- unit: N-p4-11 -->
记
$$
\alpha=\inf\{a:(a,b)\in G_x\},
\qquad
\beta=\sup\{b:(a,b)\in G_x\}.
$$
原稿简写为“$\alpha=\inf a$，$\beta=\sup b$”。

<!-- unit: N-p4-12 -->
原稿断言 $(\alpha,\beta)\in G_x$；同一行后半的符号保留为 Q004，不能唯一辨定的部分另存精确位置。

<!-- unit: N-p4-family-notation -->
> [!info] 补充：集合族与最大区间的记号
> 原稿 $G_x$ 此时是“区间组成的集合族”。为避免后面把它当作点集，以下另用
> $$
> I_x=\bigcup_{J\in G_x}J=(\alpha,\beta)
> $$
> 表示最大区间。若端点无界，就允许 $\alpha=-\infty$ 或 $\beta=+\infty$；这种情形下，严格说应把原族扩充到允许无穷端点的开区间，或把原稿的“属于”改为“这个并仍为开区间”。

<!-- unit: N-p4-13 -->
原稿证明开头：$x\in(\alpha,\beta)$；再任取 $y\in(\alpha,\beta)$。

<!-- unit: N-component-construction-proof -->
> [!info] 补证：把开头补成完整构造证明
> 由 $U$ 开，至少有一个 $(a_0,b_0)\in G_x$，所以 $\alpha\le a_0<x<b_0\le\beta$，即 $x\in(\alpha,\beta)$。
> 对任意 $y\in(\alpha,\beta)$，若 $y<x$，由下确界定义可选 $(a,b)\in G_x$ 使 $a<y$；又 $b>x>y$，故 $y\in(a,b)\subset U$。若 $y>x$，由上确界定义可选 $(a,b)\in G_x$ 使 $b>y$，又 $a<x<y$，同样得 $y\in U$。$y=x$ 已知。因此 $(\alpha,\beta)\subset U$。
> 每个 $(a,b)\in G_x$ 都有 $\alpha\le a<b\le\beta$，故包含于 $(\alpha,\beta)$。所以 $I_x=(\alpha,\beta)$ 就是所有这些区间的并，也是含 $x$ 且包含于 $U$ 的唯一最大开区间。

<!-- unit: N-p4-14 -->
原稿再写：且 $\alpha\notin U$、$\beta\notin U$；“反证，若不然”。

<!-- unit: N-component-endpoint-proof -->
> [!info] 补证：有限端点不属于开集
> 若 $\alpha\in\mathbb R$ 且 $\alpha\in U$，由开性有 $\varepsilon>0$ 使 $(\alpha-\varepsilon,\alpha+\varepsilon)\subset U$。它与 $I_x$ 相交，二者并成的开区间仍在 $U$ 内且含 $x$，但左端点小于 $\alpha$，与 $\alpha$ 的下确界性质矛盾。右端点 $\beta$ 的证明相同。因此有限端点都不在 $U$。无穷端点不是实数，不应把 $\pm\infty\notin U$ 当作额外拓扑结论。

<!-- unit: N-p4-07 -->
<a id="s5-4"></a>
### 5.4 原稿 Ex 2：通常实轴的拓扑基有多少种

**题目。**$(\mathbb R,|\cdot|)$ 有 $2^c$ 种基。

<!-- unit: N-p4-08 -->
原稿浅色提示：$\mathcal P(A)=2^c\Rightarrow$。

<!-- unit: N-basis-count-proof -->
> [!info] 补证：上界与下界都要证明
> 通常实轴的开集族 $\tau$ 有 $c$ 个成员，而每个拓扑基都是 $\tau$ 的子集，故基的种数不超过 $2^c$。
> 固定可数基 $\mathcal B_0$。集合 $\tau\setminus\mathcal B_0$ 仍有 $c$ 个元素。对它的每个子集 $A$，$\mathcal B_0\cup A$ 都是同一个通常拓扑的基：所添元素本来就是开集，而原基已能细化每个开邻域。不同的 $A$ 给出不同的基，故至少有 $2^c$ 种。与上界合并即得恰有 $2^c$ 种。

<!-- unit: N-p4-09 -->
原稿还列出基的覆盖条件 $\bigcup\{G_i\}=\mathbb R$，并简记 $\forall x\in G_i\ \exists x\in G_k\subset G_i$。

<!-- unit: N-basis-criterion -->
> [!info] 补充：基的准确局部条件
> 对已经给定的拓扑 $\tau$，开集族 $\mathcal B\subset\tau$ 是基，当且仅当每个开集 $U$、每个 $x\in U$ 都能找到 $B\in\mathcal B$ 使 $x\in B\subset U$。原稿简记若只用同一族的 $G_i$，条件会退化为取 $G_k=G_i$，不足以表述对全部开邻域的细化。
> 若从一个集合族出发定义拓扑，则须检查它覆盖 $X$，并且对任意 $B_1,B_2\in\mathcal B$ 与 $x\in B_1\cap B_2$，存在 $B_3\in\mathcal B$ 使 $x\in B_3\subset B_1\cap B_2$。这时所有基元的任意并组成拓扑。


<!-- unit: N-components-heading -->
<a id="s6"></a>
## 6. 构成区间与开集的唯一分解

<!-- unit: N-p5-10 -->
<a id="s6-1"></a>
### 6.1 先备例题：实区间连通

**原题。**实区间均连。

<!-- unit: N-p5-11 -->
原稿的证明提示：“$p$ 进制小数[Q005]展开。”

<!-- unit: N-interval-connected-proof -->
> [!info] 补证：任意实区间连通
> 原题中的“连”按通常用法理解为连通。设区间 $I$ 不连通，存在不交、非空的相对开集 $A,B$，使 $I=A\cup B$。选 $a\in A$、$b\in B$；交换名称后可设 $a<b$。由于 $I$ 是区间，$[a,b]\subset I$。
> 令 $c=\sup(A\cap[a,b])$，则 $c\in[a,b]\subset I$。如果 $c\in A$，由 $A$ 相对开及 $b\notin A$，有 $c<b$，且某个 $c$ 右侧的点仍属于 $A\cap[a,b]$，与上确界矛盾。如果 $c\in B$，则 $c\ne a$；由 $B$ 相对开，某个 $c$ 左侧邻域与 $A$ 不交，却与 $c$ 为 $A\cap[a,b]$ 的上确界矛盾。两种情形均不可能，所以 $I$ 连通。单点区间与空区间按定义也连通。
> 原稿最后一句的中间字形尚未唯一辨定，不能据此声称它已经给出了完整证明。若意在使用进制展开，应另行说明展开规则及它如何推出区间不可分；上述上确界证明给出了本题独立可用的完整解答。

<!-- unit: N-connected-subset-interval -->
> [!info] 补充：实直线的连通子集必为区间
> 若 $C\subset\mathbb R$ 含 $a<b$，却漏掉某个 $t\in(a,b)$，则 $C\cap(-\infty,t)$ 与 $C\cap(t,\infty)$ 是两个非空、不交的相对开集，其并为 $C$，故 $C$ 不连通。因此连通子集必包含任意两点之间的所有点，即为区间。结合前题，实直线的连通子集恰为区间。

<!-- unit: N-p5-01 -->
<a id="s6-2"></a>
### 6.2 构成区间的定义

原稿设 $G\subset\mathbb R$，$(a,b)\subset G$。

<!-- unit: N-p5-02 -->
若 $a\notin G$、$b\notin G$，则称 $(a,b)$ 为 $G$ 的构成区间。

<!-- unit: N-component-definition-scope -->
> [!info] 补充：开集、无穷端点与最大性
> 以下取 $G$ 为开集。允许端点属于扩充实数 $\overline{\mathbb R}=\mathbb R\cup\{-\infty,+\infty\}$；当端点有限时要求它不在 $G$ 中，无穷端点不作为实点讨论。构成区间可以是有界开区间、开射线或整个 $\mathbb R$。
> §5 中对每个 $x\in G$ 构造的最大开区间 $I_x=(\alpha_x,\beta_x)$ 就是一个构成区间。反之，端点条件保证 $(a,b)$ 不能向任何一侧扩大而仍留在 $G$ 中，所以它是包含其任一点的最大开区间。实直线的连通子集都是区间，因此这些最大区间恰好是 $G$ 的连通分支。

<!-- unit: N-p5-03 -->
<a id="s6-3"></a>
### 6.3 不同构成区间不相交

**原命题。**开集 $G$ 的不同构成区间互不相交。

<!-- unit: N-p5-04 -->
**原证明提示。**反证，可以用两个构成区间。

<!-- unit: N-components-disjoint-proof -->
> [!info] 补证：保留原反证路线
> 设两个构成区间 $I=(a,b)$、$J=(c,d)$ 相交，却不相等。它们的并是一个开区间，而且仍包含于 $G$。这个并严格包含至少一个原区间，与构成区间的最大性矛盾。因此相交的构成区间必相等，不同的构成区间必不相交。
> 也可以直接用端点：不妨设 $a\le c$。相交意味着 $c<b$。若 $a<c$，有限端点 $c$ 就属于 $(a,b)\subset G$，与 $c\notin G$ 矛盾，故 $a=c$；同理可得 $b=d$。这同时给出端点条件的直观作用。

<!-- unit: N-p5-05 -->
**原推论。**若 $x_0\ne y_0$，包含 $x_0$ 与 $y_0$ 的构成区间只有两种可能：相等，或不相交。原稿以大括号并列这两个分支。

<!-- unit: N-components-corollary-proof -->
> [!info] 补证
> 每一点各属于唯一的最大区间 $I_{x_0}$、$I_{y_0}$。若二者有交点，则上一命题给出二者相等；否则二者不相交。$x_0\ne y_0$ 不表示两个区间必不同，例如 $G=(0,1)$ 中任意两点都在同一构成区间里。

<!-- unit: N-p5-06 -->
<a id="s6-4"></a>
### 6.4 唯一分解及可数性

原稿写：“得到了开区间的唯一表示。”

<!-- unit: N-open-decomposition-proof -->
> [!info] 纠错与补证：应为开集的构成区间表示
> 此处承接的是开集 $G$ 的分解。每个 $x\in G$ 都在其最大开区间 $I_x\subset G$ 中，所以 $G=\bigcup_{x\in G}I_x$。删除相同的区间后，各区间两两不交。
> 每个非空开区间都含有有理数。固定 $\mathbb Q$ 的枚举，在每个构成区间里选择枚举次序最小的有理数；不相交区间选出的数不同，因而构成区间至多可数。于是
> $$
> G=\mathop{\dot\bigcup}_{j\in J}(a_j,b_j),\qquad J\text{ 至多可数}.
> $$
> 这是按构成区间作出的唯一分解，唯一性指忽略编号后的区间族唯一：任何构成区间中的点，其最大开区间已经由 $G$ 确定。若另给两两不交的非空开区间分解，它们也必须是这些最大区间，因为一个连通的最大区间不能被两个以上相对开且不交的非空部分分开。空开集对应空区间族。
> 例：$G=(-2,-1)\cup(0,1)\cup(1,3)$ 有三个构成区间，其中 $(0,1)$ 与 $(1,3)$ 不能合并，因为中间点 $1\notin G$。

<!-- unit: N-p5-07 -->
<a id="s6-5"></a>
### 6.5 原旁注：高维的表示不唯一

原稿写：“$\mathbb R^n$，中可表示为 $(a,b)$ 可数个，且表示不唯一。”

<!-- unit: N-rn-boxes-proof -->
> [!info] 说明与补证：可数个开长方体之并
> 这句省略了所讨论集合及并的符号。与前后开集内容相容的准确表述是：$\mathbb R^n$ 的每个开集都能表示为至多可数个开长方体的并，此种表示通常不唯一。记
> $$
> (a,b)=\prod_{i=1}^n(a_i,b_i),\qquad a_i<b_i.
> $$
> 所有端点均为有理数的开长方体构成可数基。给定开集 $G$ 及 $x\in G$，取 $r>0$ 使 $B(x,r)\subset G$，再在各坐标上选有理端点，得到 $x\in(a,b)\subset B(x,r)\subset G$。因此把所有包含于 $G$ 的有理端点长方体并起来就得到 $G$，所用集合至多可数。
> 表示不唯一，例如 $(0,1)^n$ 既是一个长方体，也等于
> $$
> \bigl((0,2/3)\times(0,1)^{n-1}\bigr)\ \cup\
> \bigl((1/3,1)\times(0,1)^{n-1}\bigr).
> $$
> 这里的长方体可以重叠；这种表示和前面的唯一“构成区间分解”并非同一条件。在 $n\ge2$ 时，连通分支还未必是长方体，例如圆盘的唯一连通分支就是圆盘本身。

<!-- unit: N-p5-08 -->
<a id="s7"></a>
## 7. 第二可数、局部连通空间中的开集分解

**原定理条件。**$(X,\tau)$ 是第二可数、局部连通，原稿随后写 $\forall U\subset(X,\tau)$。

<!-- unit: N-p5-09 -->
**原结论。**可表示为至多可数个连通分支的并。

<!-- unit: N-local-connected-definition -->
> [!info] 补充：连通分支与局部连通
> 集合的连通分支是其中极大的非空连通子集。每个点所在的分支可以定义为所有含该点的连通子集之并：这些集合共有该点，它们的并仍连通。若一个分离把此并分成两个相对开部分，含公共点的每个连通集合都只能落在同一部分，另一部分便为空。因此分支存在；相交的两个分支之并连通，由极大性二者相等，所以分支划分原集合。
> 局部连通指每一点都有由连通开邻域组成的邻域基。因而对于开集 $U$ 中的每个 $x$，可找到连通开集 $V$ 使 $x\in V\subset U$。

<!-- unit: N-local-connected-theorem-proof -->
> [!info] 纠错与完整证明：必须要求 $U$ 开
> 准确结论：若 $X$ 第二可数且局部连通，则每个开集 $U\subset X$ 都是至多可数个两两不交的连通开集的并，这些集合正是 $U$ 的连通分支。
> 先证每个分支 $C$ 在 $X$ 中开。任取 $x\in C$，由局部连通取连通开集 $V_x$ 使 $x\in V_x\subset U$。由于 $V_x$ 与 $C$ 有交点，$V_x\cup C$ 连通，分支的极大性给出 $V_x\subset C$。因此 $C=\bigcup_{x\in C}V_x$ 开。
> 再证分支至多可数。取 $X$ 的可数基 $\{B_m:m\in\mathbb N\}$。每个非空开分支 $C$ 都含有某个非空基元素；选满足 $\varnothing\ne B_m\subset C$ 的最小 $m$。不同分支互不相交，因此不会选中同一基元素。这样把分支族单射到 $\mathbb N$，证明了可数性。分支本来就划分 $U$，故所求分解成立且分支族唯一。
> 原稿的包含号旁未明确写“开”。若把 $U$ 当作任意子集，结论错误：取 $X=\mathbb R$、$U=\mathbb R\setminus\mathbb Q$，$X$ 第二可数且局部连通，而 $U$ 的每个连通分支都是单点，且这样的分支不可数。因为任意两个不同无理数之间都有有理数，含两个点的子集不可能是实区间；再用 §6.1 的连通子集判别即可。
> $\mathbb R^n$ 是第二可数、局部连通的，所以其每个开集的连通分支至多可数且各自开；这与 §6.5 中任意长方体表示的不唯一性相容。
