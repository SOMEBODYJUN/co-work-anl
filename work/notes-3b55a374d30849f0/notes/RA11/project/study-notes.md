<!-- unit: N-title -->
# 实分析 11：可测函数的简单函数逼近、Egorov 定理与几乎处处收敛

<!-- unit: N-editorial -->
> [!info] 编排说明
> 黑色段落保留原稿内容。蓝色块是基于原稿公式补全的定义、证明步骤或数学订正。原稿明确未完成或字迹不能唯一恢复的位置用红色疑点标记。当前没有提供旧 Markdown，因此本稿只做 PDF 原稿识读。

<!-- unit: N-toc -->
## 目录

1. [非负可测函数的简单函数逼近](#s1)
2. [简单函数积分与一般可测函数](#s2)
3. [几乎处处相等与 $L^1$ 观点](#s3)
4. [一致收敛与 Egorov 定理](#s4)
5. [Egorov 定理的证明](#s5)
6. [集合论表述、等价判别与反例](#s6)
7. [原稿疑点与图形信息](#s7)

<a id="s1"></a>
## 1. 非负可测函数的简单函数逼近

### 1.1 原稿结论

设 $(E,\mathcal M,m)$ 为测度空间，$f:E\to[0,+\infty]$ 可测。原稿构造一列非负简单函数 $(\varphi_k)$，满足
$$
0\le \varphi_k\le \varphi_{k+1}\le f,
\qquad \varphi_k(x)\uparrow f(x)\quad(x\in E).
$$
原稿页边用分层图表示把 $f(x)$ 的取值区间按步长 $2^{-k}$ 切分，再把每个点向下取整。

> [!info] 补充，分层构造的标准写法
> 对 $k\ge1$，令
> $$
> E_{k,j}=\left\{x\in E:\frac{j-1}{2^k}\le f(x)<\frac{j}{2^k}\right\},
> \qquad j=1,\ldots,k2^k,
> $$
> 并令 $A_k=\{x:f(x)\ge k\}$。定义
> $$
> \varphi_k(x)=\sum_{j=1}^{k2^k}\frac{j-1}{2^k}\mathbf1_{E_{k,j}}(x)+k\mathbf1_{A_k}(x).
> $$
> 每个 $E_{k,j}$ 和 $A_k$ 可测，故 $\varphi_k$ 是简单可测函数，且 $0\le\varphi_k\le f$。

### 1.2 单调性与逐点极限

原稿把 $f(x)<+\infty$ 与 $f(x)=+\infty$ 分开讨论。

- 当 $f(x)<+\infty$ 时，取 $k>f(x)$，点 $x$ 落在某个分层区间。分辨率由 $2^{-k}$ 改为 $2^{-(k+1)}$ 后，下端点至多损失一个新的网格步长，因此
  $$
  0\le f(x)-\varphi_k(x)<2^{-k}.
  $$
  令 $k\to\infty$ 得 $\varphi_k(x)\to f(x)$。
- 当 $f(x)=+\infty$ 时，$x\in A_k$ 对所有 $k$ 足够大成立，故 $\varphi_k(x)=k\to+\infty$。

原稿的分层示意图显示横轴为函数值层，纵轴标记逐级上升的 $k$，并以彩色横线标出被截断的函数值。该图只作版面和关系记录，不能替代公式。

<a id="s2"></a>
## 2. 简单函数积分与一般可测函数

原稿在第 2 页将简单函数列逼近与一般非负可测函数的积分联系起来。记号核心是
$$
 f\text{ 可测}
 \Longleftrightarrow
 \exists\ \text{可测简单函数 }\varphi_k\text{ 使 }\varphi_k\uparrow f.
$$
“$\uparrow$”表示逐点单调递增，若教材只要求几乎处处成立，则在相应位置按 a.e. 理解。

> [!info] 补充，为什么这是积分定义的入口
> 对简单函数 $s=\sum_{j=1}^r a_j\mathbf1_{A_j}$（$a_j\ge0$、$A_j$ 可测），定义
> $$
> \int_Es\,dm=\sum_{j=1}^ra_jm(A_j).
> $$
> 对任意非负可测 $f$，用所有满足 $0\le s\le f$ 的简单函数积分的上确界定义
> $$
> \int_Ef\,dm=\sup\left\{\int_Es\,dm:0\le s\le f,\ s\text{ 简单可测}\right\}.
> $$
> 上述 $\varphi_k$ 给出一个递增逼近序列，且
> $$
> \int_E\varphi_k\,dm\uparrow\int_Ef\,dm.
> $$

<a id="s3"></a>
## 3. 几乎处处相等与 $L^1$ 观点

原稿第 3 页提示在测度论中按 a.e. 等价类处理函数。若 $f=g$ a.e.，则
$$
\int_Ef\,dm=\int_Eg\,dm
$$
只要两边均有定义。原稿还写出 $L^1$ 逼近形式
$$
\lim_{n\to\infty}\int_E|f_n-f|\,dm=0,
$$
这表示 $f_n$ 在 $L^1(E)$ 中收敛到 $f$。

> [!info] 补充，三种收敛的区别
> 逐点收敛要求每个固定 $x$ 都有 $f_n(x)\to f(x)$。a.e. 收敛允许在零测集上失败。一致收敛要求
> $$
> \sup_{x\in E}|f_n(x)-f(x)|\to0.
> $$
> $L^1$ 收敛要求误差的积分趋于零。它们之间一般没有无条件的双向蕴含。

<a id="s4"></a>
## 4. 一致收敛与 Egorov 定理

### 4.1 一致收敛的定义

原稿写出
$$
 f_n\to f\text{ 一致}
 \Longleftrightarrow
 \forall\varepsilon>0\ \exists N\ \forall n\ge N\ \forall x\in E,
 \ |f_n(x)-f(x)|<\varepsilon.
$$
等价地，$\sup_{x\in E}|f_n(x)-f(x)|\to0$。

### 4.2 Egorov 定理

> [!info] 定理
> 设 $m(E)<\infty$，且 $f_n\to f$ a.e. 于 $E$。对任意 $\delta>0$，存在可测集 $F_\delta\subset E$，使 $m(F_\delta)<\delta$，并且 $f_n\to f$ 在 $E\setminus F_\delta$ 上一致收敛。

原稿用 $f_n(x)=x^n$（$(0,1)$ 上）作为逐点收敛的例子。端点 $x=1$ 的行为须单独处理，故复习时先明确函数列的定义域和极限函数，再判断是否一致收敛。

<a id="s5"></a>
## 5. Egorov 定理的证明

固定 $\varepsilon>0$，定义误差尾集
$$
E_n(\varepsilon)=\bigcup_{k=n}^{\infty}\{x\in E:|f_k(x)-f(x)|\ge\varepsilon\}.
$$
于是 $E_{n+1}(\varepsilon)\subset E_n(\varepsilon)$，且
$$
\bigcap_{n=1}^{\infty}E_n(\varepsilon)
=\limsup_{n\to\infty}\{|f_n-f|\ge\varepsilon\}.
$$
因为 $f_n\to f$ a.e.，上述交集是零测集。又 $m(E)<\infty$，由测度从上连续性
$$
\lim_{n\to\infty}m(E_n(\varepsilon))=0.
$$

给定 $\delta>0$，对每个 $j\in\mathbb N$ 选择 $n_j$，使
$$
 m\left(E_{n_j}(1/j)\right)<\frac{\delta}{2^j}.
$$
令
$$
F_\delta=\bigcup_{j=1}^{\infty}E_{n_j}(1/j).
$$
则
$$
 m(F_\delta)\le\sum_{j=1}^{\infty}m\left(E_{n_j}(1/j)\right)<\delta.
$$
若 $x\in E\setminus F_\delta$，则对每个 $j$ 和所有 $k\ge n_j$，有 $|f_k(x)-f(x)|<1/j$。给定任意 $\eta>0$，取 $j$ 使 $1/j<\eta$，再取 $k\ge n_j$，便得 $|f_k(x)-f(x)|<\eta$。该 $N=n_j$ 与 $x$ 无关，因此在 $E\setminus F_\delta$ 上一致收敛。

<a id="s6"></a>
## 6. 集合论表述、等价判别与反例

### 6.1 a.e. 收敛的 limsup 判别

令
$$
A_n(\varepsilon)=\{x\in E:|f_n(x)-f(x)|\ge\varepsilon\}.
$$
则
$$
 f_n\to f\ a.e.
 \Longleftrightarrow
 m\left(\limsup_{n\to\infty}A_n(\varepsilon)\right)=0
 \quad(\forall\varepsilon>0).
$$
其中
$$
\limsup_nA_n=\bigcap_{N=1}^{\infty}\bigcup_{n\ge N}A_n
$$
是“误差至少为 $\varepsilon$ 无穷多次发生”的点集。

### 6.2 Egorov 的有限测度限制

原稿第 6 页例子取 $E=(0,+\infty)$，
$$
 f_k(x)=\chi_{(0,k]}(x),\qquad f(x)=1.
$$
对每个固定 $x>0$，当 $k\ge x$ 时 $f_k(x)=1$，故 $f_k(x)\to1$。然而
$$
\sup_{x>0}|f_k(x)-1|=1
$$
对每个 $k$ 都成立，所以不一致收敛。该例说明 Egorov 定理中 $m(E)<\infty$ 是必要条件之一。

<a id="s7"></a>
## 7. 原稿疑点与图形信息

- 第 1 页首行的函数值域措辞和第 3 页“可取到/有限”的字样模糊，暂以中性描述保留。
- 第 1 页分层指标的上界、截断分支及图中横线的具体颜色与字母需按局部裁图二次核对。
- 第 3 页关于 $\bar f$、集合 $S$ 与 $\mathcal B$ 的记号未完全清晰，保留原符号并列入恢复记录。
- 第 4 页顶部的收敛判别式与 Egorov 前的过渡句存在压写，学习稿采用标准一致收敛定义并以蓝色补充标注。
- 第 4 页例 $x^n$ 的定义域和极限函数须回图确认，当前正文只保留原稿可读部分。

<a id="s8"></a>
## 8. 二进分割例子与依测度收敛

### 8.1 二进区间的指示函数

令 $E=(0,1]$、$f=\chi_{(0,1]}$。把 $E$ 分成 $2^n$ 个半开区间
$$
I_{j,n}=\left(\frac{j-1}{2^n},\frac j{2^n}\right],
\qquad j=1,\ldots,2^n.
$$
定义 $f_j^{(n)}=\chi_{I_{j,n}}$。这些函数两两几乎处处不交，且
$$
\sum_{j=1}^{2^n}f_j^{(n)}=f.
$$
固定 $x_0\in(0,1]$ 时，恰有一个 $j$ 使 $x_0\in I_{j,n}$，因此恰有一个 $f_j^{(n)}(x_0)=1$。

> [!info] 原稿图形信息
> 第 7 页没有画坐标轴，而是通过区间端点和分段括号表达分割关系。每一个分段函数只在一个二进区间上取 $1$，其余处取 $0$。

### 8.2 依测度收敛

原稿对误差集合
$$
E_n(\varepsilon)=\{x:|f_j^{(n)}(x)-0|\ge\varepsilon\}
$$
给出
$$
 m(E_n(\varepsilon))=
 \begin{cases}2^{-n},&0<\varepsilon\le1,\\0,&\varepsilon>1,
 \end{cases}
$$
所以 $m(E_n(\varepsilon))\to0$。这正是 $f_j^{(n)}\xrightarrow{m}0$ 的检验。

> [!info] 定义
> 在测度空间 $(E,\mathcal M,m)$ 上，$f_n$ 依测度收敛到 $f$ 是指
> $$
> \forall\varepsilon>0,
> \quad m\{x\in E:|f_n(x)-f(x)|\ge\varepsilon\}\to0.
> $$
> 使用 $>$ 代替 $\ge$ 得到等价定义，边界集合通过从上/从下连续性处理。

### 8.3 概率例子

取
$$
\Omega=\{0,1\}^{\mathbb N},\qquad X_i(\omega)=\omega_i,qquad
X_n=\frac1n\sum_{i=1}^{n}X_i.
$$
在对称 Bernoulli 概率下，原稿写出
$$
P\left(\left|X_n-\frac12\right|>\varepsilon\right)\to0,
$$
即依概率收敛到 $1/2$。这是依测度收敛在概率空间中的对应版本。

<a id="s9"></a>
## 9. 依测度极限的唯一性

> [!info] 命题
> 若 $f_n\xrightarrow{m}f$ 且 $f_n\xrightarrow{m}g$，则 $f=g$ a.e.

证明中令
$$
A_n=\{x:|f-g|>1/n\}.
$$
由三角不等式，
$$
A_n\subset
\left\{|f-f_n|>\frac1{2n}\right\}
\cup
\left\{|f_n-g|>\frac1{2n}\right\}.
$$
右侧两集合测度趋于零，故 $m(A_n)=0$。由于
$$
\{f\neq g\}=\bigcup_{n=1}^{\infty}A_n,
$$
得到 $m(\{f\neq g\})=0$。

<a id="s10"></a>
## 10. 依测度收敛的距离观点与无限测度反例

在可测函数的 a.e. 等价类
$$
F(E)/\!\sim,\qquad f\sim g\iff f=g\ \text{a.e.}
$$
上，原稿给出距离型表达式
$$
 d(f,g)=\int_E\min\{1,|f-g|\}\,dq.
$$
当所用测度 $q$ 有限时，该表达式可以把依测度收敛编码成距离收敛。原稿的测度字母较淡，正式使用时需核对是 $q$ 还是 $\mu$。

例取 $E=(0,+\infty)$、$f_k=\chi_{(0,k)}$、$f=1$。虽然 $f_k(x)\to1$ 对每个固定 $x$ 成立，但
$$
 m\{|f_k-f|\ge1/2\}=m((k,+\infty))=+\infty.
$$
因此无限测度空间中逐点收敛不保证依测度收敛。

<a id="s11"></a>
## 11. a.e. 收敛与依测度收敛

### 11.1 有限测度下的 Egorov 方向

若 $m(E)<\infty$ 且 $f_n\to f$ a.e.，Egorov 定理给出对任意 $\delta>0$，存在 $F_\delta$ 且 $m(F_\delta)<\delta$，使 $f_n\to f$ 在 $E\setminus F_\delta$ 上一致。由
$$
\{|f_n-f|\ge\varepsilon\}
\subset F_\delta\cup
\bigl((E\setminus F_\delta)\cap\{|f_n-f|\ge\varepsilon\}\bigr)
$$
可推出 $f_n\xrightarrow{m}f$。

### 11.2 Riesz 子列定理

若 $f_n\xrightarrow{m}f$，可选递增下标 $n_k$ 使
$$
 m\left(\left\{|f_{n_k}-f|>1/k\right\}\right)<2^{-k}.
$$
令 $E_k=\{|f_{n_k}-f|>1/k\}$。由于 $\sum_km(E_k)<\infty$，Borel–Cantelli 第一引理给出
$$
 m(\limsup_kE_k)=0.
$$
故在补集上仅有限多个 $E_k$ 发生，因而 $|f_{n_k}(x)-f(x)|<1/k$ 最终成立，得到 $f_{n_k}\to f$ a.e.。

### 11.3 “每个子列都有 a.e. 收敛子子列”判别

在通常有限测度假设下，
$$
 f_n\xrightarrow{m}f
\quad\Longleftrightarrow\quad
\text{任意子列 }(f_{n_j})\text{ 都有进一步子列 a.e. 收敛到 }f.
$$
右向左可用反证：若原列不依测度收敛，则存在 $\varepsilon_0>0$、$\eta>0$ 及子列满足误差集测度至少为 $\eta$，任何进一步子列都不可能 a.e. 收敛到 $f$。

<a id="s12"></a>
## 12. 收敛关系总表与原稿问题

在 $m(E)<\infty$ 时，复习时使用以下关系。

- a.e. 收敛 $\Rightarrow$ 依测度收敛。
- 依测度收敛 $\Rightarrow$ 存在子列 a.e. 收敛。
- 依测度极限在 a.e. 等价类意义下唯一。
- 依测度收敛不保证原序列 a.e. 收敛。
- 在无限测度空间，逐点/a.e. 收敛与依测度收敛之间的箭头需要单独检验。

原稿第 13 页以问答式文字讨论“是否存在一种收敛等价于 a.e. 收敛”，并在页中把 Egorov、Riesz、Borel–Cantelli 三个工具并列复习。具体随机变量符号因字迹较淡列入疑点，不把未确认的随机模型强行写入定理。

## 13. 原稿疑点、恢复与图像记录

- 第 7 页 $f_j^{(n)}$ 的端点区间为半开区间。端点 $0$ 是否包含在定义域中需以原图页边为准，当前按 $(0,1]$ 转写。
- 第 8 页“$>$ 与 $\ge$ 的等价性”只写了提要，学习稿补出标准连续性说明，标为蓝色补充。
- 第 8 页概率空间例的坐标函数记号可能为 $\pi_i$ 或 $X_i$，当前正文采用可读的 $X_i$ 并在来源记录中保留原字形疑点。
- 第 10 页距离 $d(f,g)$ 的积分测度记号不能唯一恢复，保留 $q/\mu$ 候选。
- 第 12–13 页关于“每个子列存在 a.e. 收敛子子列”的定理框架可由上下文恢复，原稿正文只写了提要，完整双向论证属于蓝色补充。
- 第 14 页为物理空白页，未发现页边内容。
