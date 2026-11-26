# 实分析 12｜原稿保真转写

按原 PDF 的 7 个物理页排列。正文保留笔误、重复、旁注和三处原待填横线；蓝色说明用于识读或规范化，红色只标原稿明确留空。原有编号与本文来源编号分别保留。英文姓名按通行拼法排印；手写异体在说明中登记。数学订正及完整补证见独立的《study-notes.md》。

来源：本项目只读的 source.pdf。精确坐标、图片、裁图及双向去向见 manifest.json、source-target-map.json、ledger.json。

## 第 1 页

### Littlewood 3 定律

1. 每一个可测集几乎是有限个开区间并。
2. 每一个可测函数几乎连续。
3. 每个可测收敛的几乎一致收敛。

> [!note] <span style="color:blue">识读说明</span>
>
> 标题尾字按“律”形排印；第三句的“收敛的”保留原口语省略，数学意思是收敛的可测函数列。此处没有把原“几乎”改写为“几乎处处”。

**Ex.** 设 $E\in M$，$m(E)<+\infty$。$\forall\varepsilon>0$，$\exists I_i,\ldots,I_n$ 开区间，s.t.

$$

m\left(E\mathbin{\Delta}\left(\bigcup_{i=1}^n I_i\right)\right)<\varepsilon.

$$

> [!note] <span style="color:blue">识读说明</span>
>
> 题面第一个区间下标形近 $i$，公式的并从 $1$ 到 $n$；学习稿规范成 $I_1,\ldots,I_n$。原运算是对称差，原区间确写“开”。

**Lemma.** 设 $f:X\to Y$。$X$ 有一个开覆盖，$X=\bigcup_{i\in A}X_i$。

若 $\forall a\in A$，$f_a:X_a\to Y$ 连续，则 $f:X\to Y$ 连续。

$$

f^{-1}(U)=\bigcup_{a\in A}\bigl(f^{-1}(U)\cap X_a\bigr)
\overset{\text{定义}}{=}\bigcup_{a\in A}(f|_{X_a})^{-1}(U).

$$

> [!note] <span style="color:blue">识读与上下文恢复</span>
>
> 覆盖的索引全集写出了 $A/\Delta/\Lambda$ 样的不同笔形，本段统一排作 $A$，保留先 $i$ 后 $a$ 的索引变化。首个逆像上标的 $1$ 笔画极短；后两项的 $-1$ 和限制线共同确认逆像。$f_a=f|_{X_a}$ 是从同段定义等号与限制记号恢复的关系，不是原题另写的一行。

注意 $f|_{X_a}$ 连续，

$$

(f|_{X_a})^{-1}(U)\in\tau_{X_a}=C\cap X_a,\qquad C\in\tau_X.

$$

由 $X_a$ 都 $\in\tau_X$，$C\cap X_a$ 是 $X$ 中开集。〔段末证毕样收笔〕

但即使是闭覆盖，无限个，但改成局部有限闭覆盖。

即：给定 $x\in X$，$\exists U\in N(x)$，$U$ 只与有限多个 $X_a$ 相交。

可测函数〔校读：近似〕，要求可数个覆盖。

> [!note] <span style="color:blue">字形校读及解释范围</span>
>
> 1200 dpi 与作者同页‘函’‘数’及走之笔对照后，择优校读‘近似’：前一字有独立低位底捺，后一字更像亻加以，缺少第二条走之，故优于‘逼近’；‘类似’虽符合拼接语境，却欠清楚的米、大结构。此为有依据的字形校读，置信度中等，不称逐笔唯一。‘要求可数个覆盖’可由可测拼接解释，但孤句本身没有给出一条完整的函数近似定理；学习稿中的可测拼接证明单独标为补充。

## 第 2 页

### Lusin

设 $f$ 是 $E$ 上 a.e. 有限的可测函数。$\forall\delta>0$，$\exists F_\delta\overset{\text{闭}}{\subset}E$，满足

$$

m(E\setminus F_\delta)<\delta,\qquad f|_{F_\delta}\in C(F_\delta).

$$

并给出闭集构造 $F_\delta$ 的表达式。

**Pf. (1)** $f\in S(E)$。$\exists E_1,\ldots,E_\ell\in M$，s.t. $E=\cup X_i$，

$$

f=\sum_{i=1}^{\ell}c_i\chi_{E_i}.

$$

$\forall\delta$，由 Lebesgue 的内正规性，

$$

\exists F_{i,\delta}\overset{\text{紧闭}}{\subset}E_i,\qquad
m(E_i\setminus F_{i,\delta})<\frac{\delta}{\ell}.

$$

> [!note] <span style="color:blue">原记号说明</span>
>
> 覆盖式右端按交叉笔形记 $X_i$，上下文数学对象为 $E_i$；“紧闭”两字可见。原稿暂未区分有限与无限测度，紧集逼近在学习稿中先限定有限测度，随后使用第 4 页局部化。

令

$$

F_\delta=\bigcup_{i=1}^{\ell}F_{i,\delta}.

$$

$$

\begin{aligned}
m(E\setminus F_\delta)
&=m(E\setminus\cup F_{i,\delta})\\
&=m\left(\bigcup_{i=1}^{\ell}(E\setminus F_{i,\delta})\right)
=\sum m(E\setminus F_{i,\delta})<\delta.
\end{aligned}

$$

> [!note] <span style="color:blue">原稿错误标识</span>
>
> 后两个 $E$ 未见下标 $i$，链中的等号保留。这是原稿集合运算错误，不在保真稿内暗改成正确式。

**(2)** $f\in M(E)$，则 $\exists\{\varphi_k\}\subset S(E)$，s.t.

$$

\lim_{k\to\infty}\varphi_k(x)=f(x),\qquad\forall x\in E.

$$

## 第 3 页

由 (1)，$\forall\delta$、$\forall k\in\mathbb N^*$，

$$

F_\delta\overset{\text{闭}}{\subset}E,\qquad
m(E\setminus F_k)<\frac{\delta}{2^k}.

$$

且 $\varphi_k\in C(F_k)$。令 $F_\delta=\bigcap_{k=1}^{\infty}F_k$，则

$$

m(E\setminus F_\delta)
=m\left(\bigcup_{k=1}^{\infty}(E\setminus F_k)\right)
\le\sum\frac{\delta}{2k}.

$$

$\varphi_k$ 在 $F_k$ 上连续。$\varphi_k$ 在 $\bigcap F_k$ 上连续，下证一致收敛。

> [!note] <span style="color:blue">识读说明</span>
>
> 首行左侧字面为 $F_\delta$，同一行右侧与下一行是 $F_k$。末和的 $k$ 起笔与 $2$ 近乎等高，按 $2k$ 笔形存留；另有低写指数 $2^k$ 候选，预期几何预算由首行明确的 $2^k$ 恢复。$\varphi_k\in C(F_k)$ 是省写限制。

但 Egorov 要求 $m(E)<+\infty$。

因 $f$ a.e. 有限，$m(E(|f|=+\infty))=0$。

令

$$

g(x)=\frac{f(x)}{1+|f(x)|},
\qquad |f(x)|=\frac{|g(x)|}{1-|g(x)|}.

$$

则 $g$ 有界。

$$

f(x)=\frac{g(x)}{1-g(x)}.

$$

$g(x)$ 有界。

> [!note] <span style="color:blue">识读说明</span>
>
> Egorov 手写有 Englov/Engrov 样连写，依本段指称统一姓名。带符号逆式分母原未写绝对值，保留原式；模值逆式中确有绝对值。两个“有界”提示都保留。

或用 Egorov 定理。

当 $m(E)<+\infty$，$\exists\varphi_k\to f$，
$\forall\delta>0$，$\exists F_\delta\overset{\text{闭}}{\subset}E$，s.t.

$$

m(E\setminus F_\delta)\quad\underline{\hspace{1cm}}

$$

<span style="color:red">〔原稿待填 B1：测度后的比较号及界值〕</span>

## 第 4 页

用 Egorov，$\exists G_\delta\subset E$，s.t.

$$

m(E\setminus G_\delta)\quad\underline{\hspace{1cm}}

$$

<span style="color:red">〔原稿待填 B2：测度后的比较号及界值〕</span>

$\varphi_k$ 在 $E\setminus G_\delta$ 上一致 $f$。

考虑 $F_\delta\cap(E\setminus G_\delta)$，由可测的内正规性，

$$

H_\delta\overset{\text{闭}}{\subset}E\setminus G_\delta,\qquad
m((E\setminus G_\delta)\setminus H_\delta)<\underline{\hspace{2cm}}.

$$

<span style="color:red">〔原稿待填 B3：不等号后的界值〕</span>

$$

\widehat F_\delta=F_\delta\cap H_\delta.

$$

要估

$$

\begin{aligned}
&m\bigl((E\setminus F_\delta)\cup(E\setminus H_\delta)\bigr)\\
&\qquad <m(E\setminus F_\delta)+m(E\setminus H_\delta).
\end{aligned}

$$

$$

E\setminus H_\delta
=((E\setminus G_\delta)\setminus H_\delta)\cup(G_\delta\setminus H_\delta).

$$

> [!note] <span style="color:blue">识读说明</span>
>
> “要估”对应原引导字的估／求候选，不影响后面的完整公式；测度次可加位置原写严格小于号，学习稿另订正。

$m(E)=+\infty$：

$$

A_k=B(0,k)\setminus B(0,k-1),\qquad
E=\bigcup_{k=1}^{\infty}(A_k\cap E).

$$

但在 $A_k\cap E$ 上的有一个闭集。

需要用局部有限性质。

## 第 5 页

Lusin 逆定理也成立。

**Th.** 设 $(X,\tau)$，则下述等价：

1. $X$ 正规。
2. $\forall E\overset{\text{闭}}{\subset}X$，若 $f\in C(F)$，则 $\exists F\in C(X)$，s.t. $F|_E=f$。（Tietze）
3. $\forall A,B\overset{\text{闭}}{\subset}X$，$A\cap B=\varnothing$，则存在连续函数 $f:X\to[0,1)$，s.t. $f|_A=0$ 且 $f|_B=1$。（Urysohn）

> [!note] <span style="color:blue">原稿记号错误</span>
>
> 第 (2) 条括号内的原字为两横的 $F$，第 (3) 条区间右端形如圆括号。两处数学订正分别为 $C(E)$ 和 $[0,1]$，在学习稿标明。

**Remark.** 外测度中不对，$m^*(A\cup B)$〔上下文恢复：除非〕$A$ 和 $B$ 可被可测集分〔本行止于右缘〕。

$$

C=A\cup B.

$$

> [!note] <span style="color:blue">上下文恢复及残句范围</span>
>
> 起句校读为‘外测度中不对’。连接词取优势候选‘除非’：首形的阝与余形连笔、次形双竖及后接条件的语法共同支持，‘所谓’欠斤、讠和胃结构，‘可加性’的字数及笔形不合。其置信度中等，恢复性质已就地标明。右缘只写到‘分’，原 PDF 右页外没有后续绘画路径，故不把‘分开／分隔’补成已写原文。$C=A\cup B$ 原为下一独立行。学习稿仅给出可测分离推出加性的充分条件，不从残句反推无条件的必要性。

**Th.** 设 $f$ 是 $E$ 上几乎处处有限函数，$E\in M$：

1. $f$ 可测。
2. $\exists\{\varphi_k\}\subset S(E)$，s.t. $\varphi_k\to f$ 逐点。
3. $\exists\{\varphi_k\}\subset C(\mathbb R^n)$，s.t. $\varphi_k\xrightarrow{\mathrm{a.e.}}f$。

## 第 6 页

**Pf. (1) $\Rightarrow$ (3).**

$$

\exists g\in C(\mathbb R^n),\qquad g|_{F_\delta}=f.

$$

$\forall k\in\mathbb N^+$，$\exists F_k\overset{\text{闭}}{\subset}E$，

$$

g_k\in C(\mathbb R^n),\qquad g|_{F_k}=f,\qquad
m(E\setminus F_k)<\frac1{2^k}.

$$

> [!note] <span style="color:blue">识读说明</span>
>
> 量词中的自然数上标按正整数语境恢复为 $+$。存在式写 $g_k$，右侧限制式只见 $g$，保留原漏下标。右端 $f$ 原省写限制。

由 Borel–Cantelli：

$$

m\left(\limsup_{n\to\infty}E_n\right)=0.

$$

〔上下文恢复：易〕考察

$$

E\{g_k\ne f\}\subset E\setminus F_k.

$$

仍有

$$

m\left(\limsup_{k\to\infty}E(g_k\ne f)\right)=0.

$$

$$

m\left(\bigcap_{N=1}^{\infty}\bigcup_{k=N}E(g_k\ne f)\right)=0.

$$

（几乎处处）

$$

x\in\bigcup_{N=1}^{\infty}\bigcap_{k=N}^{\infty}E(f=g_k).

$$

$$

\exists N(x)\ \text{s.t.}\ k\ge N,\qquad f=g_k\ \text{恒等}.

$$

> [!note] <span style="color:blue">识读与省记说明</span>
>
> 首式的 $E_n$ 没有在这一行定义；后文以失配事件明确其用途。花括／圆括均作原谓词集合写法保存；包含式的右端 $F_k$ 后原另有孤立闭圆括样笔，左端没有成对开括，排式未把它当作运算。上式内并原只有下标 $k=N$，未另写上标无穷；下式两个无穷上标均可见。左缘首字受页面及 Form 裁框截切，在内存放宽裁框后补见原有矢量笔画，未改绘画路径；下部围笔内两处墨迹支持‘易’优于‘另’，上部仍潦草，故取中等置信的上下文恢复。‘考察’与前页‘考’的对照及宀、示笔形相符。末行阈值择优排作 $k\ge N$，另有 $k>N$ 候选，只差起点平移，均是逐点最终恒等。

## 第 7 页

本物理页为空白页。整页与六个重叠区均无正文、页码、旁注、图形或原待填标记。
