# 实分析 10｜复习笔记

> 本稿把原稿按“Borel 可测性 → 乘积空间与圆柱集合 → 坐标函数 → 上确界/下确界映射”的依赖顺序编排。黑色是原稿内容的规范化转写，蓝色是补全证明、明确数学条件或修正原稿中可能省略的步骤，红色保留原稿明确不可判定的位置。

## 目录

1. Borel 可测函数与原像判据
2. 可数集运算与圆柱集合
3. 可数乘积空间和坐标投影
4. 坐标函数刻画乘积可测性
5. 上确界、下确界与逐点极值
6. 原稿疑点与来源索引

## 1. Borel 可测函数与原像判据

### 1.1 定义

设 `(X,\mathcal M)` 与 `(Y,\mathcal N)` 为可测空间。函数 `f:X→Y` 可测，是指对每个 `B∈\mathcal N` 都有

$$
f^{-1}(B)=\{x\in X:f(x)\in B\}\in\mathcal M.
$$

当 `Y=\mathbb R` 且 `\mathcal N=\mathcal B(\mathbb R)` 时，称 `f` 为 Borel 可测。原稿在第 1 页页首写作 `\mathcal B(X)→\mathcal B(\mathbb R)` 与 “Borel 可测”。

> [!info] 蓝色补充｜生成族判据
> 若 `\mathcal C` 生成 `\mathcal B(\mathbb R)`，即 `\sigma(\mathcal C)=\mathcal B(\mathbb R)`，则只需验证 `f^{-1}(C)∈\mathcal M` 对所有 `C∈\mathcal C` 成立。常用生成族是开射线 `(-\infty,a)` 或 `(a,+\infty)`，以及开区间 `(a,b)`。

### 1.2 有限并、有限交和补

若 `E_1,\dots,E_n∈\mathcal M`，则

$$
\bigcup_{j=1}^{n}E_j\in\mathcal M,
\qquad
\bigcap_{j=1}^{n}E_j\in\mathcal M,
\qquad
X\setminus E_j\in\mathcal M.
$$

第 1 页把集合 `F_1,\dots,F_n`、`E=\bigcup_jF_j` 作为有限并的例子，并在蓝笔中重复写出 `E_j` 的有限并构造。重复出现的路线在复习稿中保留，因为它们对应原稿中的黑笔与蓝笔两次说明。

> [!info] 蓝色补充｜有限并的归纳证明
> `σ`-代数按定义对补和可数并封闭。有限并是可数并的特例。有限交由德摩根律得到
> `\bigcap_{j=1}^{n}E_j=X\setminus\bigcup_{j=1}^{n}(X\setminus E_j)`。

### 1.3 Borel `σ`-代数的区间生成

原稿第 4 页写出开区间生成 Borel `σ`-代数的形式，可整理为

$$
\mathcal B(\mathbb R)=\sigma\bigl(\{(a,b):a<b\}\bigr).
$$

等价地，

$$
\mathcal B(\mathbb R)
=\sigma\bigl(\{(a,+\infty):a\in\mathbb R\}\bigr)
=\sigma\bigl(\{(-\infty,a):a\in\mathbb R\}\bigr).
$$

> [!info] 蓝色补充｜为什么开射线足够
> 对任意 `a<b`，`(a,b)=(a,+\infty)\cap(-\infty,b)`。反过来，`(a,+\infty)=\bigcup_{m\ge1}(a,a+m)`，所以任一生成族都能得到另一族。

## 2. 可数集运算与圆柱集合

### 2.1 坐标投影

设 `X=\prod_{n=1}^{\infty}X_n`，第 `n` 个坐标投影为

$$
\pi_n:X\to X_n,
\qquad
\pi_n(x_1,x_2,\ldots)=x_n.
$$

对 `A_n\subseteq X_n`，其投影原像为

$$
\pi_n^{-1}(A_n)
= X_1\times\cdots\times X_{n-1}\times A_n\times X_{n+1}\times\cdots.
$$

这类集合称为圆柱集合。第 2、3 页反复写 `\pi_n^{-1}(u_n)` 及其有限交。

### 2.2 有限交的形状

若只限制前两个坐标，则

$$
\pi_1^{-1}(A_1)\cap\pi_2^{-1}(A_2)
=A_1\times A_2\times X_3\times X_4\times\cdots.
$$

一般地，对有限指标集 `F\subset\mathbb N`，

$$
\bigcap_{n\in F}\pi_n^{-1}(A_n)
=\{x\in X:x_n\in A_n\text{ 对所有 }n\in F\}.
$$

原稿第 3 页把 `\pi_1^{-1}(u_1)`、`\pi_2^{-1}(u_2)` 和两者的交逐项写出。每条公式都保留为独立来源单元。

> [!info] 蓝色补充｜圆柱集合的直观含义
> 圆柱集合只检查有限多个坐标，其余坐标任意。因此有限交仍是圆柱集合。它们构成乘积 `σ`-代数的一个自然生成族。

## 3. 可数乘积空间和坐标投影

### 3.1 乘积 `σ`-代数

给每个 `X_n` 配备 `σ`-代数 `\mathcal M_n`。定义

$$
\bigotimes_{n=1}^{\infty}\mathcal M_n
=\sigma\left(\left\{\pi_n^{-1}(A):n\in\mathbb N,\ A\in\mathcal M_n\right\}\right).
$$

当 `X_n=\mathbb R` 且 `\mathcal M_n=\mathcal B(\mathbb R)` 时，记为

$$
\mathcal B(\mathbb R)^{\otimes\mathbb N}
\quad\text{或}\quad
\bigotimes_{n=1}^{\infty}\mathcal B(\mathbb R).
$$

原稿第 3、4 页分别使用 `\mathcal S`、`\mathcal B` 记号描述生成族和有限交族。原稿符号的上划线、帽号位置有不确定处，正文用标准乘积记号补齐，并在疑点表保留原形。

### 3.2 投影的可测性

若 `A∈\mathcal M_n`，则

$$
\pi_n^{-1}(A)\in\bigotimes_{k=1}^{\infty}\mathcal M_k
$$

按乘积 `σ`-代数的定义成立。因此每个投影 `\pi_n` 都是可测映射

$$
\pi_n:
\left(X,\bigotimes_{k=1}^{\infty}\mathcal M_k\right)
\to(X_n,\mathcal M_n).
$$

## 4. 坐标函数刻画乘积可测性

### 4.1 从乘积空间映射到实数列空间

设 `(E,\mathcal M)` 是可测空间，且对每个 `n` 有可测函数

$$
F_n:(E,\mathcal M)\to(\mathbb R,\mathcal B(\mathbb R)).
$$

定义坐标映射

$$
\Phi:E\to\mathbb R^{\mathbb N},
\qquad
\Phi(x)=(F_1(x),F_2(x),\ldots).
$$

则 `\Phi` 对乘积 `σ`-代数

$$
\bigotimes_{n=1}^{\infty}\mathcal B(\mathbb R)
$$

可测。其原因是

$$
\pi_n\circ\Phi=F_n
$$

对每个 `n` 可测，而乘积 `σ`-代数由各坐标投影的原像生成。

### 4.2 完整证明

取任意生成圆柱集合

$$
C=\pi_n^{-1}(B),\qquad B\in\mathcal B(\mathbb R).
$$

则

$$
\Phi^{-1}(C)
=\Phi^{-1}\bigl(\pi_n^{-1}(B)\bigr)
=(\pi_n\circ\Phi)^{-1}(B)
=F_n^{-1}(B)\in\mathcal M.
$$

由于原像运算保持补、可数并和可数交，`\Phi^{-1}(A)∈\mathcal M` 对乘积 `σ`-代数中所有 `A` 成立。因此 `\Phi` 可测。

原稿第 4、5 页还写出反向表述。一个映射 `F:E→\mathbb R^{\mathbb N}` 可测，当且仅当每个坐标函数 `F_n=\pi_n\circ F` 可测。原稿中的“可测 `⇔`”和投影复合公式完整保留。

### 4.3 原稿中关于极限的省略

第 2 页页首与第 3 页页首出现“复合、积分、极限”的短句，但没有完整条件。可复习使用的标准补充如下。

> [!info] 蓝色补充｜可测函数的逐点极限
> 若 `f_n:E→\overline{\mathbb R}` 均可测，且 `f_n(x)→f(x)` 对每个 `x` 成立，则 `f` 可测。可用
> `\limsup_n f_n` 与 `\liminf_n f_n` 的可数上确界、下确界表示证明。

<span style="color:red">原稿短句 `[RA10-P002-U01]` 的具体积分符号和极限方向仍待进一步判字，蓝色段落只作为明确标注的标准补充。</span>

## 5. 上确界、下确界与逐点极值

### 5.1 序列上确界映射

设

$$
S:\mathbb R^{\mathbb N}\to\overline{\mathbb R},
\qquad
S(x)=\sup_{n\ge1}x_n.
$$

原稿第 5 页定义 `S`，第 6 页使用开射线原像证明其 Borel 可测性。对任意 `a∈\mathbb R`，有

$$
\begin{aligned}
S^{-1}((a,+\infty))
&=\left\{x:\sup_{n\ge1}x_n>a\right\}\\
&=\bigcup_{n=1}^{\infty}\{x:x_n>a\}\\
&=\bigcup_{n=1}^{\infty}\pi_n^{-1}((a,+\infty)).
\end{aligned}
$$

右端是乘积 `σ`-代数中的可数并，所以 `S` 可测。

> [!info] 蓝色补充｜端点检查
> 若要处理闭射线 ` [a,+\infty)`，不能直接把 `\sup x_n\ge a` 写成 `\bigcup_n\{x_n\ge a\}`，因为上确界可能等于 `a` 而没有某一项等于 `a`。可写成
> `\{\sup_nx_n\ge a\}=\bigcap_{m\ge1}\bigcup_n\{x_n>a-1/m\}`。
> 原稿图像更接近开射线 `(a,+\infty)`，所以正文把开射线作为原稿路线，并把闭端点的谨慎处理列为补充。

### 5.2 逐点上确界

若 `f_n:E→\overline{\mathbb R}` 均可测，定义

$$
F(x)=\sup_{n\ge1}f_n(x),
$$
则 `F` 可测。证明可直接写为

$$
F^{-1}((a,+\infty))
=\bigcup_{n=1}^{\infty}f_n^{-1}((a,+\infty))\in\mathcal M.
$$

这一结论也可看作坐标映射 `\Phi(x)=(f_1(x),f_2(x),\ldots)` 与可测映射 `S` 的复合

$$
F=S\circ\Phi.
$$

第 6 页蓝笔的“`f∘S` 可测”按数学关系整理为“可测映射的复合可测”。若原稿确实把复合方向写反，保真转写仍保留原字形，学习稿使用正确方向。

### 5.3 逐点下确界

同理，若 `f_n` 均可测，则

$$
G(x)=\inf_{n\ge1}f_n(x)
$$

可测。因为

$$
G^{-1}((-\infty,a))
=\bigcup_{n=1}^{\infty}f_n^{-1}((-\infty,a)).
$$

原稿第 6 页末尾以“`inf` 同理”收束，学习稿把完整公式补在相邻位置。

## 6. 原稿疑点与来源索引

| 疑点编号 | 页区 | 原稿片段 | 当前处理 |
| --- | --- | --- | --- |
| RA10-P001-U01 | p0001-r1c1 至 r2c2 | “可测函数的有限……/原像……” | 保留候选，学习稿使用一般原像判据并标蓝补充 |
| RA10-P002-U01 | p0002-r1c1 | 页首积分、复合和极限短句 | 原样保留可辨字，完整条件列为蓝色标准补充 |
| RA10-P003-U01 | p0003-r1c1 至 r3c1 | `S,t`、`ω/\bar n`、`u(S)` | 按原图保留，中性标识，未据数学合理性强行定字 |
| RA10-P004-U01 | p0004-r1c1 至 r3c2 | Borel 生成族与乘积 `σ`-代数符号 | 标记上下文恢复，标准记号置于蓝色说明 |
| RA10-P005-U01 | p0005-r1c1 至 r3c1 | 积分、`max/min` 旁注 | 保留旁注并标未决 |
| RA10-P006-U01 | p0006-r1c1 | `(a,+∞)` 与 `[a,+∞)` 端点 | 按图选开射线，附闭射线的蓝色修正证明 |

### 页区与图形信息

- P001–P006 均有正文、公式和页边空白，P007 近似空白。
- 现有图形信息主要是第 4 页的坐标投影/圆柱集合布局和公式排列，第 5 页的序列点 `x=(x_1,x_2,\ldots)` 与第 6 页上确界集合关系。原稿没有独立几何图，故以原位公式和来源裁图保留。
- 所有物理页和六分区图保存在 `project/pages/` 与 `project/regions/`。小字与端点公式另有定向裁图 `project/crops/p0001-target-700dpi.png`，供复核回溯。
