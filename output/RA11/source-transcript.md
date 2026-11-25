<!-- unit: T-title -->
# 实分析 11：保真转写

<!-- unit: T-p1-heading -->
## 原稿第 1 页

<!-- unit: T-p1-01 -->
设 $f$ 是非负可测函数，且 $\varphi_k$ 是逐点递增的简单函数列。可见原稿写有
$$
\varphi_k(x)\le \varphi_{k+1}(x)\le f(x),\qquad \lim_{k\to\infty}\varphi_k(x)=f(x)
$$
（顶部关于“函数的取值范围”的开场语已回看原图并保留为编辑性说明；不把难辨字形擅改为黑色正文。）

<!-- unit: T-p1-02 -->
当 $k\in\mathbb N^*$ 时，将 $[0,k)$ 按步长 $2^{-k}$ 等分（行末下标读作 $j=1,\ldots,k2^k$）作为分段尺度。旁注给出
$$
E_{k,j}=E\!\left[\frac{j-1}{2^k}\le f<\frac j{2^k}\right],
$$
并画出一条把函数值分层的示意图；800 dpi 定向裁图与同页 $f(x)\ge k$ 截断分支共同排除仅 $2^k$ 层的读法。

<!-- unit: T-p1-03 -->
定义简单函数
$$
\varphi_k(x)=
\begin{cases}
\dfrac{j-1}{2^k},&x\in E_{k,j},\\
 k,&x\in E\setminus\{f<k\},
\end{cases}
$$
原稿第一行的第二个分支写法略有涂改，意思是对 $f(x)\ge k$ 的点取截断值 $k$。

<!-- unit: T-p1-04 -->
原稿注明“$\varphi_k(x)$ 逐点递增”，并写出证明的开头。若 $f(x)\ge k+1$，则
$$
\varphi_{k+1}(x)\ge k+1>k\ge\varphi_k(x).
$$
若 $f(x)<k+1$，则存在相邻的分层指标 $j$ 使 $f(x)$ 落在相应区间，故分辨率加倍后下端点不下降。

<!-- unit: T-p1-05 -->
原稿在页底写明：$\varphi_k(x)\uparrow f(x)$，并列出两类情形。第一类是 $f(x)<+\infty$，第二类是 $f(x)=+\infty$。

<!-- unit: T-p2-heading -->
## 原稿第 2 页

<!-- unit: T-p2-01 -->
补充说明：若 $f(x)=+\infty$，则 $\varphi_k(x)\to+\infty$；若 $f(x)<+\infty$，则存在 $k$ 使 $f(x)\le k$。对足够大的 $k$，有
$$
\frac{j-1}{2^k}\le f(x)<\frac j{2^k},
\qquad
\varphi_k(x)\le f(x)\le \frac j{2^k}
$$
（原稿中该行的两个分数分母均为 $2^k$，分子为相邻整数）。

<!-- unit: T-p2-02 -->
原稿写道：对 $x\in E$，选取分层指标后可得
$$
\varphi_k(x)\le f(x)\le \varphi_k(x)+2^{-k},
$$
故当 $k\to\infty$ 时趋于 $f(x)$。

<!-- unit: T-p2-03 -->
对任意 $f\in M^+(E)$，原稿写出“$f^{-1}$（或 $f$ 的逆像）保持可测”的判断，并记
$$
f\text{ 可测}\Longleftrightarrow \exists\{\varphi_k\}\text{ 可测简单函数，}\ \varphi_k\uparrow f\quad\text{处处/几乎处处}.
$$
右侧有“至少可测”的旁注。

<!-- unit: T-p2-04 -->
原稿接着转入“简单函数，一般收敛”的说明，指出简单函数是构造一般非负可测函数积分的基础。下方给出一段“补充/remark”，文字含义是一般可测函数可由简单函数列逼近。

<!-- unit: T-p2-05 -->
原稿举例说明几乎处处相等的函数可以视作同一个 $L^1$ 元素：若 $f=g$ a.e.，则 $f-g=0$ a.e.，并在后续积分中不区分二者。

<!-- unit: T-p3-heading -->
## 原稿第 3 页

<!-- unit: T-p3-01 -->
页首旁注：在“测度意义”下不妨把相等理解为 a.e. 相等。

<!-- unit: T-p3-02 -->
**Def.** 设 $f$ 是可取到（原稿此处字迹疑为“有限”）的函数。若存在简单函数列，使其积分逼近 $f$，则称其可积。原稿写有
$$
\lim_{n\to\infty}\int_E |f_n(x)-f(x)|\,dx=0
$$
一类 $L^1$ 逼近条件（积分符号和积分域在原稿中有简写）。

<!-- unit: T-p3-03 -->
“从本性出发”后，原稿记
$$
\bar f:E\to\overline{\mathbb R},\qquad
\bar f(x)=f(x)\quad(x\in E),
$$
并提示把值域扩充为扩展实数，以容许 $+\infty$。

<!-- unit: T-p3-04 -->
原稿对每个 $x\in E$ 讨论 $f(x)$ 落在相邻的层间，并令
$$
S=\{f(x):x\in E\},\qquad \mathcal B=\{0,1\}
$$
（集合符号与第二个集合的记号在图中较淡）。

<!-- unit: T-p3-05 -->
页末说明：对 $f$ 的值域作分层，把每一层的原像作为可测集合，便可写成简单函数。最后一句是“对 $f$（或 $f$ 的值域）剖分为 $U_j$，其中 $f(x)$ 落入相应层”。

<!-- unit: T-p4-heading -->
## 原稿第 4 页

<!-- unit: T-p4-01 -->
页首写出函数列趋于函数的一个判别式，形如
$$
f_n\to f\quad\Longleftrightarrow\quad
\forall \varepsilon>0\ \exists N\ \text{使得}\ n\ge N\Rightarrow |f_n-f|<\varepsilon,
$$
并在下面标注“（一致收敛）”。

<!-- unit: T-p4-02 -->
原稿另写“$f_n\to f$（一致）$\Longleftrightarrow f_n$ 逐点趋于 $f$ 且误差在 $E$ 上一致控制”，随后进入 Egorov 定理。

<!-- unit: T-p4-03 -->
**Egorov.** 设 $f_n,f$ 在 $E$ 上几乎处处收敛，且 $m(E)<+\infty$。

<!-- unit: T-p4-04 -->
原稿的两个方向/结论框架为：给定 $\delta>0$，可找到可测集合 $F_\delta\subset E$，满足 $m(F_\delta)<\delta$，使得 $f_n\to f$ 在 $E\setminus F_\delta$ 上一致收敛；反向的“有限测度条件”在页边有提示。

<!-- unit: T-p4-05 -->
原稿以 $f_n(x)=x^n$（区间 $(0,1)$）作为例子，指出逐点收敛到极限函数，但在全区间上一致收敛性需要从端点行为单独检查。

<!-- unit: T-p5-heading -->
## 原稿第 5 页

<!-- unit: T-p5-01 -->
继续 Egorov 证明。先固定 $\varepsilon>0$，定义
$$
E_n(\varepsilon)=\bigcup_{k=n}^{\infty}\{x\in E:\ |f_k(x)-f(x)|\ge\varepsilon\}.$
$$
原稿页边的横向笔画是 $E$ 的上横/省写痕迹，不构成闭包或补集运算；按同页递减尾集证明定稿为无横线 $E_n(\varepsilon)$。

<!-- unit: T-p5-02 -->
由几乎处处收敛，
$$
\bigcap_{n=1}^{\infty}E_n(\varepsilon)
=\limsup_{n\to\infty}\{|f_n-f|\ge\varepsilon\}
$$
为零测集。故由测度的连续性（从上连续性），
$$
\lim_{n\to\infty}m(E_n(\varepsilon))=0.
$$

<!-- unit: T-p5-03 -->
因此给定 $\delta>0$，对每个 $j\in\mathbb N$ 可选 $n_j$ 使
$$
 m\bigl(E_{n_j}(1/j)\bigr)<\frac{\delta}{2^j}.
$$
令
$$
F_\delta=\bigcup_{j=1}^{\infty}E_{n_j}(1/j),
$$
则
$$
 m(F_\delta)\le\sum_{j=1}^{\infty}m(E_{n_j}(1/j))<\delta.
$$

<!-- unit: T-p5-04 -->
若 $x\in E\setminus F_\delta$，则对每个 $j$ 与所有 $k\ge n_j$，有 $|f_k(x)-f(x)|<1/j$。这给出在 $E\setminus F_\delta$ 上的一致收敛。

<!-- unit: T-p6-heading -->
## 原稿第 6 页

<!-- unit: T-p6-01 -->
定义余集
$$
E\setminus F_\delta
=E\cap\left(\bigcup_{j=1}^{\infty}E_{n_j}(1/j)\right)^c
=E\cap\bigcap_{j=1}^{\infty}E_{n_j}(1/j)^c.
$$
原稿写出该集合及补集运算，强调对每个 $j$ 均避开误差集合。

<!-- unit: T-p6-02 -->
原稿给出一个等价叙述：若 $f_n\to f$ a.e. 于 $\bar E$，令
$$
E_n(\varepsilon)=\{x\in E:\ |f_n(x)-f(x)|\ge\varepsilon\},
$$
则
$$
 f_n\to f\ a.e.
\Longleftrightarrow
m\left(\limsup_{n\to\infty}E_n(\varepsilon)\right)=0\quad(\forall\varepsilon>0).
$$
页边写有“con”并提示逆向说明。

<!-- unit: T-p6-03 -->
原稿最后指出 Egorov 型结论的有限测度条件不可去。例：$E=(0,+\infty)$，取
$$
 f_k(x)=\chi_{(0,k]}(x),\qquad f(x)=1\quad(x\in E).
$$
则对每个固定 $x$，$f_k(x)\to f(x)$，但在整个 $E$ 上不一致收敛，因为对每个 $k$ 都有 $\sup_{x>0}|f_k(x)-1|=1$。原稿末尾标注“Egorov 定理逆命题不成立/条件有限”。

<!-- unit: T-p7-heading -->
## 原稿第 7 页

<!-- unit: T-p7-01 -->
**eg.** 令 $f=\chi_{(0,1]}$。原稿先写两段函数
$$
f^{(1)}_1(x)=
\begin{cases}1,&x\in(0,\tfrac12],\\0,&x\in(\tfrac12,1],\end{cases}
\qquad
f^{(1)}_2(x)=
\begin{cases}1,&x\in(\tfrac12,1],\\0,&x\in(0,\tfrac12],\end{cases}
$$
作为把区间分段的示例。

<!-- unit: T-p7-02 -->
将 $E=(0,1]$ 等分为 $2^n$ 段。对 $j=1,\ldots,2^n$，原稿定义
$$
f_j^{(n)}(x)=
\begin{cases}
1,&x\in\left(\dfrac{j-1}{2^n},\dfrac j{2^n}\right],\\
0,&x\notin\left(\dfrac{j-1}{2^n},\dfrac j{2^n}\right].
\end{cases}
$$

<!-- unit: T-p7-03 -->
原稿说明把上述 $2^n$ 个分段函数相加，得到在 $E$ 上取值为 $1$ 的函数。即
$$
\sum_{j=1}^{2^n}f_j^{(n)}(x)=\chi_{(0,1]}(x)=f(x).
$$

<!-- unit: T-p7-04 -->
给定 $x_0\in(0,1]$，总存在唯一的 $j$ 使
$$
x_0\in\left(\frac{j-1}{2^n},\frac j{2^n}\right],
$$
于是 $f_j^{(n)}(x_0)=1$，其余分段函数在 $x_0$ 处为 $0$。页末写有“$f_j^{(n)}(x_0)$ 有唯一的取值/分段”一类说明。

<!-- unit: T-p8-heading -->
## 原稿第 8 页

<!-- unit: T-p8-01 -->
原稿继续用第 7 页的分段函数说明依测度收敛。对 $\varepsilon>0$ 定义误差集
$$
E_n(\varepsilon)=\{x:|f_j^{(n)}(x)-0|\ge\varepsilon\}.
$$
当 $0<\varepsilon\le1$ 时，该集合就是一个长度为 $2^{-n}$ 的二进区间；当 $\varepsilon>1$ 时为空集。因此
$$
m(E_n(\varepsilon))=
\begin{cases}
2^{-n},&0<\varepsilon\le1,\\
0,&\varepsilon>1,
\end{cases}
\qquad m(E_n(\varepsilon))\to0.
$$

<!-- unit: T-p8-02 -->
**Def.** 设 $f_n,f$ 是 $E$ 上可测函数。若对每个 $\varepsilon>0$ 都有
$$
\lim_{n\to\infty}m\bigl(E\cap\{|f_n-f|\ge\varepsilon\}\bigr)=0,
$$
则称 $f_n$ 依测度收敛于 $f$，记为 $f_n\xrightarrow{m}f$。原稿在不等号处同时写有 $>$ 的版本。

<!-- unit: T-p8-03 -->
原稿备注：用 $>|\varepsilon$ 或 $\ge\varepsilon$ 定义依测度收敛是等价的。可利用
$$
\{|f_n-f|\ge\varepsilon\}
=\bigcap_{r=1}^{\infty}\{|f_n-f|>\varepsilon-1/r\}
$$
及测度的连续性互相转换（具体边界集需依实际测度条件核对）。

<!-- unit: T-p8-04 -->
页底引入概率空间例子。令
$$
\Omega=\{0,1\}^{\mathbb N}
=\{(u_1,u_2,\ldots):u_i\in\{0,1\}\},
$$
并取坐标函数 $X_i(u)=u_i$。原稿定义平均值
$$
X_n(u)=\frac{X_1(u)+\cdots+X_n(u)}{n}.
$$

<!-- unit: T-p9-heading -->
## 原稿第 9 页

<!-- unit: T-p9-01 -->
概率例子的结论写作
$$
\lim_{n\to\infty}P\left(\left|X_n-\frac12\right|>\varepsilon\right)=0,
$$
即 $X_n$ 依概率收敛到 $1/2$。原稿在旁边写有“依概率收敛（大数定律）”和两个带问号的极限标记。

<!-- unit: T-p9-02 -->
原稿提出问题：依测度收敛/依概率收敛的极限是否唯一。随后写出
$$
 f_n\xrightarrow{m}f,\quad f_n\xrightarrow{m}g
\quad\Longrightarrow\quad f=g\ \text{a.e.}
$$

<!-- unit: T-p9-03 -->
证明使用三角不等式
$$
|f-g|\le |f-f_n|+|f_n-g|.
$$
令
$$
E_n=\{x\in E:|f-g|>1/n\}.
$$
若 $x\in E_n$，则至少有一个不等式成立：
$$
|f-f_n|>\frac1{2n}
\quad\text{或}\quad
|f_n-g|>\frac1{2n}.
$$
故
$$
E_n\subset
\{|f-f_n|>1/(2n)\}\cup\{|f_n-g|>1/(2n)\}.
$$

<!-- unit: T-p9-04 -->
右侧两个集合的测度都趋于零，所以 $m(E_n)=0$。又
$$
\{f\ne g\}=\bigcup_{n=1}^{\infty}E_n,
$$
从而 $m(\{f\ne g\})=0$，故 $f=g$ a.e.。

<!-- unit: T-p10-heading -->
## 原稿第 10 页

<!-- unit: T-p10-01 -->
页首重复结论：集合 $\{|f-g|\ge1/n\}$ 的测度为零。原稿随后进入“实际上，定义”一段，令
$$
F(E)=\{f:E\to\mathbb R\mid f\text{ 可测}\},
$$
并令 $f\sim g$ 表示 $f=g$ a.e.，考虑商集 $F(E)/\!\sim$。

<!-- unit: T-p10-02 -->
原稿写出依测度收敛所对应的距离型表达式
$$
 d(f,g)=\int_E\min\{1,|f(x)-g(x)|\}\,dq(x),
$$
其中积分测度的字母在图中为 $q$ 或 $\mu$，暂记为 $q$。该表达式用于把依测度收敛转化为距离收敛。

<!-- unit: T-p10-03 -->
原稿说明：在 $f_n\to f$ a.e. 的情况下，依测度收敛可写成对所有 $\varepsilon>0$ 有误差集测度趋于零；a.e. 收敛与依测度收敛的相互关系还要结合测度空间的有限性。

<!-- unit: T-p10-04 -->
例：$E=(0,+\infty)$，取
$$
 f_k(x)=\chi_{(0,k)}(x),\qquad f(x)=1.
$$
对每个固定 $x$，有 $f_k(x)\to f(x)$，但
$$
 m\left(\{|f_k-f|\ge\tfrac12\}\right)=m((k,+\infty))=+\infty,
$$
因此在无限测度空间上不依测度收敛。原稿末尾写“依测度收敛，但不依测度收敛/需有限测度条件”的对照句。

<!-- unit: T-p11-heading -->
## 原稿第 11 页

<!-- unit: T-p11-01 -->
页首写“协同/配套结论”：若 $f_n\to f$ a.e. 于 $E$ 且 $m(E)<+\infty$，则可推出依测度收敛。原稿记作
$$
 f_n\xrightarrow{m}f.
$$

<!-- unit: T-p11-02 -->
随后给出 Riesz 子列结论：若 $f_n\xrightarrow{m}f$，则存在子列 $f_{n_k}$ 使
$$
 f_{n_k}(x)\to f(x)\quad\text{a.e. 于 }E.
$$
页边写有 Riesz、Borel–Cantelli 两个名字。

<!-- unit: T-p11-03 -->
证明采用 Borel–Cantelli。选取递增的下标 $n_k$，令
$$
E_k=\left\{x\in E:\left|f_{n_k}(x)-f(x)\right|>\frac1k\right\},
$$
并令 $n_k$ 足够大，使
$$
 m(E_k)<2^{-k}.
$$

<!-- unit: T-p11-04 -->
于是
$$
\sum_{k=1}^{\infty}m(E_k)<\infty,
$$
从而
$$
 m\left(\limsup_{k\to\infty}E_k\right)=0.
$$
原稿写出估计
$$
 m\left(\bigcap_{n=1}^{\infty}\bigcup_{k=n}^{\infty}E_k\right)
\le \lim_{n\to\infty}\sum_{k=n}^{\infty}m(E_k)=0.
$$

<!-- unit: T-p11-05 -->
对不在 $\limsup E_k$ 中的 $x$，存在 $N(x)$ 使得 $k\ge N(x)$ 时 $|f_{n_k}(x)-f(x)|<1/k$，因而 $f_{n_k}(x)\to f(x)$。这完成子列几乎处处收敛。

<!-- unit: T-p12-heading -->
## 原稿第 12 页

<!-- unit: T-p12-01 -->
原稿把选子列的步骤写成：给定 $\varepsilon>0$，由 $f_n\xrightarrow{m}f$，存在 $N(\varepsilon)$ 使对 $n\ge N(\varepsilon)$，
$$
 m\left(E\cap\{|f_n-f|\ge\varepsilon\}\right)<\varepsilon.
$$
依次取 $n_s$，满足 $n_s>n_{s-1}$ 且
$$
 m\left(E\cap\left\{|f_{n_s}-f|\ge\frac1s\right\}\right)<\frac1{2^s}.
$$
原稿蓝色补字提示“自选（自定义补充）”。

<!-- unit: T-p12-02 -->
令
$$
E_s=E\cap\left\{|f_{n_s}-f|\ge\frac1s\right\}.
$$
则 $\sum_s m(E_s)<\infty$，故
$$
 m(\limsup_sE_s)=0.
$$
这正是上页 Borel–Cantelli 论证的具体实现。

<!-- unit: T-p12-03 -->
原稿写出一个定理框架：在适当的有限测度条件下，$f_n\xrightarrow{m}f$ 与“每个子列存在进一步子列 a.e. 收敛到 $f$”等价。充分性方向由上面的子列构造给出，必要性方向利用反证和误差集测度不趋于零。

<!-- unit: T-p12-04 -->
页末再次写出
$$
 f_{n_{k_j}}\to f\quad\text{a.e. 于 }E,
$$
并注明“依测度收敛推出子列几乎处处收敛”。

<!-- unit: T-p13-heading -->
## 原稿第 13 页

<!-- unit: T-p13-01 -->
页首是一个问题：“是否存在一种收敛使得……”原稿可辨识的主式为
$$
 f_n\xrightarrow{\,?\,}f
 \quad\Longleftrightarrow\quad
 f_n\to f\quad\text{a.e.}?
$$
问题后的结论写作“实际上不存在”。

<!-- unit: T-p13-02 -->
原稿以随机变量/函数列作讨论，写出
$$
X_n\xrightarrow{m}X,\qquad \lambda_n\to\lambda,
$$
以及“$X_n$ 是否有处处/几乎处处收敛”的问句；具体分布参数未写出，保留原稿范围，不外推随机模型。

<!-- unit: T-p13-03 -->
页中部总结各收敛之间的关系：
$$
 f_n\to f\text{ a.e.}
 \Longrightarrow
 f_n\xrightarrow{m}f\quad(m(E)<\infty),
$$
而
$$
 f_n\xrightarrow{m}f
 \Longrightarrow
 \text{存在子列 }f_{n_k}\to f\text{ a.e.}
$$
后一个箭头只对“存在子列”成立，不能推出原列本身 a.e. 收敛。

<!-- unit: T-p13-04 -->
原稿把 Egorov 定理、Riesz 子列定理及 Borel–Cantelli 估计集中列在一起，作为本节“定理关系”的复习提要。页脚再次写“重温 Egorov 定理（证明用 Borel–Cantelli/连续性）”。

<!-- unit: T-p14-heading -->
## 原稿第 14 页

<!-- unit: T-p14-01 -->
整页为空白，无可读正文、图形或页边旁注。
