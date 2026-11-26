# 实分析 12：原稿保真转写

> 识读说明：本稿按 PDF 物理页序排列。黑色文字是原稿可读内容或在同页重复出现的原式。疑字 RA12-Px-Uy 是原笔画无法唯一恢复的位置。页边空白、整页空白和图示按页保留。

## 第 1 页

页首写有 **Littlewood 3 原则**。

1. 每一个可测函数几乎处处连续。[疑字 RA12-P001-U01：原行中“处处”之后的连接字不够清楚，按上下文保留为“连续”。]
2. 每一列函数几乎处处一致收敛。[疑字 RA12-P001-U02：原行“列/列函数”的字形较连，原稿只写了一行原则性短句。]
3. 每一个可测集的近似于有限区间，[原句在逗号处结束，后续留白。]

**Ex：** 设 \(E\in M\)，\(m(E)<+\infty\)，取 \(\varepsilon>0\)，则存在有限个区间 \(I_1,\ldots,I_n\)，使
\[
 m\!\left(E\setminus \bigcup_{i=1}^{n} I_i\right)<\varepsilon .
\]
原稿在 \(I_i\) 的种类（开区间或闭区间）处没有另作说明。[疑字 RA12-P001-U03]

**Lemma.** 页底可辨出“若 \(a\in A\)，则 \(f_a:X_a\to Y\) 连续；若 \(f:X\to Y\) 连续”一类句子；首个对象和其余条件仍有疑字。原稿并在页底写有极限与交集形式的表达式。可辨部分为
\[
 f(u)=\bigcup_{a\to ?} f_a(u\cap x_a),
 \qquad
 (f|_{X_a})^{-1}(u)=\bigcap X_a\subseteq X,
\]
以及“\(X\) 中存在 …”的说明。[疑字 RA12-P001-U04：这一段的对象 \(X_a,X_i,x_a\) 与映射方向在原图中连写，不能唯一恢复。]

页底旁注写道“他们使实值函数近似连续。无限大时，函数在部分有限测度集上可控制。”[疑字 RA12-P001-U05]

原稿右下还有一行例题提示，能辨认出“存在 \(x\in X\)，\(\exists u\in M(X)\)，\(u\) … 有界，要求可测性/测度控制”。[疑字 RA12-P001-U06]

## 第 2 页

页首标题 **Lusin**。

原稿先写定理的开头

> 设 \(f\) 是在 \(E\) 上 a.e. 有限的可测函数，给定 \(\delta>0\)，则存在 \(F_\delta\subset E\)，使
> \[
> m(E\setminus F_\delta)<\delta,
> \qquad f|_{F_\delta}\in C(F_\delta).
> \]

原稿在 \(F_\delta\) 前后可辨出“闭集”字样；其余集合条件与下一页的 \(F_k\) 接续。[疑字 RA12-P002-U01：闭集二字的笔画与行间连写较轻。]

原稿写“等结论由简单函数的表达式”，随后给出简单函数情形。若 \(f\in S(E)\)，则存在 \(E_i\in M\)，并写成
\[
E=\bigcup_{i=1}^{\ell}E_i,
\qquad
f=\sum_{i=1}^{\ell}a_i\chi_{E_i}.
\]
对每个 \(E_i\) 选择 \(F_i\subset E_i\)，使
\[
 m(E_i\setminus F_i)<\frac{\delta}{\ell}.
\]
原稿把 \(F_i\) 的来源记作“由前面结论”。

页中部转入一般可测函数

> 2）\(f\in M(E)\)。则 \(\exists\varphi_k\in S(E)\)，使
> \[
> \lim_{k\to\infty}\varphi_k(x)=f(x),\qquad x\in E.
> \]

“\(f\in M(E)\)”原稿以编号“2）”单列，保留其与上段的分节关系。

## 第 3 页

页首接续上一页的简单函数近似。可读内容为
\[
\text{对每个 }k\in\mathbb N^*，\quad
F_k\subset E,
\qquad
m(E\setminus F_k)<\frac{\delta}{2^k}.
\]
原稿这里先写的是集合关系“\(F_k\subset E\)”，随后才写 \(\varphi_k\in C(F_k)\)。[疑字 RA12-P003-U01：行首的量词和下标仍有连写。]

原稿接着写
\[
\varphi_k\in C(F_k),
\]
并用递减交集构造
\[
F=\bigcap_{k=1}^{\infty}F_k.
\]
对补集的测度估计写成
\[
\begin{aligned}
m(E\setminus F)
 &=m\!\left(E\setminus\bigcap_{k=1}^{\infty}F_k\right) \\
 &=m\!\left(\bigcup_{k=1}^{\infty}(E\setminus F_k)\right) \\
 &\le \sum_{k=1}^{\infty}m(E\setminus F_k)
 <\sum_{k=1}^{\infty}\frac{\delta}{2^k}
 =\delta.
\end{aligned}
\]

原稿在这一段旁边写有“他们使实值函数连续；无限时，函数在部分有界测度集上可逼近”。[疑字 RA12-P003-U02]

页下接续 Egoroff 论证的入口

> 例：设 \(f_n\to f\)，且 \(m(E)<+\infty\)。
> \(\exists\varphi_k\to f\)，并且对给定 \(\delta>0\)，可取 \(F_\delta\subset E\)，使 \(m(E\setminus F_\delta)<\delta\)。

原稿下方另写“令 \(g(x)=f(x)/(1+|f(x)|)\)，则 \(g\) 有界；反之 \(f(x)=g(x)/(1-|g(x)|)\)”。[疑字 RA12-P003-U03：分式分母在原图中为 \(1+|f|\) 与 \(1-|g|\)，前者有清楚的括号，后者可能省略绝对值。]

页末写“放即 Egorov 定理”，并记
\[
m(E)<+\infty,
\qquad
\exists\varphi_k\to f,
\]
以及“若 \(\delta>0\)，则 \(F_\delta\subset E\)，\(m(E\setminus F_\delta)\) …”的待续句。[疑字 RA12-P003-U04]

## 第 4 页

页首标题写 **例 Egor.**。原稿写出目标集合的符号
\[
G_\delta\subset E\ \text{（也可能写作 }\overline E\text{）},
\qquad
m(E\setminus G_\delta)<\delta,
\]
并写“\(\varphi_k\) 在 \(E\setminus G_\delta\) 上 … \(f\)”的接续句。[疑字 RA12-P004-U01]

正文中的可读证明骨架如下。

1. 先对每个 \(k\) 选取 \(F_k\subset E\)，使 \(m(E\setminus F_k)<\delta/2^k\)，并令 \(\varphi_k\) 在 \(F_k\) 上连续。
2. 令 \(F=\bigcap_{k\ge1}F_k\)。由可数次可加性
\[
m(E\setminus F)
\le \sum_{k=1}^{\infty}m(E\setminus F_k)
<\delta.
\]
3. 原稿用“闭集的有限交仍闭”及逐点收敛，说明在 \(F\) 上保留 \(\varphi_k\to f\)。

页中下部另起无限测度的情形，清楚可辨
\[
m(E)=+\infty,
\qquad
A_k=B(0,k)\setminus B(0,k-1),
\]
并用 \(A_k\) 写出对 \(E\) 的分解（并集下标及是否带与 \(E\) 的交仍有省写）。旁注提到“有限测度”。页右下另有一条横线作为证明分隔。

## 第 5 页

页首再次写 **Lusin 逆定理**（“逆定理”三字按原稿保留，可能是“逆定理/逆方向”的课堂标题）。

原稿写

> Th. 设 \((A,\mu)\)，其中 \(A\) 为 …，则下列条件成立。

列出的三条为

1. \(x\in A\)。
2. 可辨为“\(E\subset X\)”（首个集合关系仍带疑字）；若 \(f\in C(X)\)，则 \(\exists F\subset C(X)\) 使 \(F|_E=f\)。（原稿在此处同时出现 \(F\)、\(f\) 与 \(E\)，对象关系不唯一。）
3. 若 \(A,B\subset X\) 为闭集且 \(A\cap B=\varnothing\)，则存在连续函数 \(f:X\to[0,1]\)，满足
\[
f|_A=0,
\qquad
f|_B=1.
\]

第 3 条旁注明确写出 **Urysohn**。

原稿继续写“Remark：另外的定理中有 \(m^*(A\cup B)\) 的闭性/可测性可用”，并给出 \(C=A\cup B\) 的记号。[疑字 RA12-P005-U01]

页底开启 Lusin 证明的下一步

> Th. 设 \(f\) 是在 \(E\) 上有界的函数，且 \(E\in M\)。
> 1）\(f\) 可测；
> 2）\(\exists \varphi_k\in S(E)\)，s.t. \(\varphi_k\to f\)；
> 3）\(\exists\{\varphi_k\}\subset C(I^n)\)，并令 \(\varphi_k\) … 延拓到 \(f\)。

第 3 条中的 \(C(I^n)\) 清楚可读，延拓箭头在页末接到下一页。[疑字 RA12-P005-U02]

## 第 6 页

页首接上页
\[
\varphi_k\in C(I^n)
\quad\Longrightarrow\quad
g\in C(I^n),
\qquad
g|_{F_\delta}=f.
\]
原稿另一行写“对 \(k=1,\ldots,n\)，存在 \(g_k\in C(I^n)\)，使 \(g_k|_{F_k}=f\)”。这里 \(n\) 与 \(k\) 的范围在原图中交替出现。[疑字 RA12-P006-U01]

下一行再给出 \(g_k\) 的限制关系。接着给出测度误差
\[
m(E\setminus F_k)<\frac{1}{2^k}\quad\text{（图面分子像数字 1；与前文的 \(\delta\) 预算不一致）}.
\]
旁注写 **Borel Cantelli**，并记
\[
m\!\left(\limsup_{k\to\infty}(E\setminus F_k)\right)=0
\quad\text{（集合内容按笔画恢复，仍保留疑点）}.
\]
原稿随后写出
\[
m\!\left(\limsup_{k\to\infty}(g_k\ ?\ f)\right)=0,
\]
以及“（几乎处处）\(g_k\to f\)”的说明。原图中 \(g_k\) 与 \(f\) 之间的运算符以及后续并/交集下标无法唯一辨认，故保留“\(?\)”而不以标准公式替换。[疑字 RA12-P006-U02]

页末写“\(g_k\) 在 \(F\) 上一致收敛；\(\exists\) 取 \(g\) 使 …”，证明在此页下缘结束，没有下一页接续。

## 第 7 页

整页空白。页边、中央和底部均未见可辨笔迹或浅色公式。
