# 实分析 12：Littlewood 三原则、Egoroff 与 Lusin

> [!info] 版本与颜色
> 黑色段落保留原稿内容。蓝色段落是为复习补出的定义、完整证明、记号解释或数学订正。红色只保留原稿明确的待填位置。本 PDF 未提供旧版 Markdown，因此本稿没有旧稿独有内容。

## 目录

1. [Littlewood 三原则](#1-littlewood-三原则)
2. [有限测度集合的区间近似](#2-有限测度集合的区间近似)
3. [Lusin 定理](#3-lusin-定理)
   1. [定理表述](#31-定理表述)
   2. [简单函数情形](#32-简单函数情形)
   3. [一般可测函数情形](#33-一般可测函数情形)
4. [Egoroff 定理](#4-egoroff-定理)
5. [Urysohn 引理与 Lusin 证明中的连续延拓](#5-urysohn-引理与-lusin-证明中的连续延拓)
6. [原稿疑点与图形信息](#6-原稿疑点与图形信息)

## 1. Littlewood 三原则

原稿页首写 **Littlewood 3 原则**，并列出三条经验性概括

1. 每一个可测函数几乎处处连续。
2. 每一列函数几乎处处一致收敛。
3. 每一个可测集可以用有限个区间近似。

<span style="color:#1f5fbf">[补充：三条原则分别对应 Lusin 定理、Egoroff 定理和 Lebesgue 测度的正则性。第二条需要有限测度条件，第一条通常表述为在任意给定误差下删去一个小测度集合后，函数在剩余闭集上连续。]</span>

## 2. 有限测度集合的区间近似

### 2.1 原稿例题

设 \(E\in\mathcal M\)，且 \(m(E)<+\infty\)。给定 \(\varepsilon>0\)，原稿要构造有限个区间 \(I_1,\dots,I_n\)，使
\[
m\!\left(E\setminus\bigcup_{i=1}^n I_i\right)<\varepsilon.
\]

### 2.2 复习用完整说明

<span style="color:#1f5fbf">[补充证明] 由 Lebesgue 测度的外正则性，可取开集 \(G\supset E\)，使 \(m(G\setminus E)<\varepsilon\)。把 \(G\) 写成至多可数个互不相交开区间的并。由于 \(m(E)<\infty\)，可先截去远处的尾部，再保留有限多个区间，使遗漏部分的测度小于 \(\varepsilon\)。于是得到有限区间并 \(U=\bigcup_{i=1}^n I_i\)，满足 \(m(E\setminus U)<\varepsilon\)。若课堂约定区间必须闭或半开，只需把每个开区间稍微缩短或扩大，并把新增边界的总长度控制在剩余误差内。</span>

## 3. Lusin 定理

### 3.1 定理表述

**Lusin 定理。** 设 \(E\in\mathcal M\)，\(m(E)<+\infty\)，\(f:E\to\mathbb R\) 可测且几乎处处有限。给定 \(\delta>0\)，存在闭集 \(F_\delta\subset E\)，使
\[
m(E\setminus F_\delta)<\delta,
\qquad
f|_{F_\delta}\in C(F_\delta).
\]

<span style="color:#1f5fbf">[补充：若 \(f\) 只在扩展实数意义下可测，先删去 \(\{x:f(x)=\pm\infty\}\) 这个零测集，再在剩余集合上应用定理。若 \(m(E)=+\infty\)，定理应在有限测度子集上局部使用，或先取 \(E_j=E\cap[-j,j]\) 再逐步拼接。]</span>

### 3.2 简单函数情形

设
\[
f=\sum_{i=1}^{\ell}a_i\chi_{E_i},
\qquad
E=\bigcup_{i=1}^{\ell}E_i,
\qquad
E_i\in\mathcal M.
\]
给定 \(\delta>0\)。对每个 \(i\)，由测度的内正则性选取闭集 \(F_i\subset E_i\)，使
\[
m(E_i\setminus F_i)<\frac{\delta}{\ell}.
\]
原稿把这个闭集记作 \(F_\delta\)：

令
\[
F_\delta=\bigcup_{i=1}^{\ell}F_i.
\]
有限个闭集的并仍为闭集。又因为 \(E_i\) 覆盖 \(E\)，有
\[
E\setminus F
\subset \bigcup_{i=1}^{\ell}(E_i\setminus F_i),
\]
所以
\[
m(E\setminus F)
\le \sum_{i=1}^{\ell}m(E_i\setminus F_i)
<\ell\frac{\delta}{\ell}=\delta.
\]
在每个 \(F_i\) 上 \(f=a_i\) 为常数，因此 \(f|_{F_\delta}\) 连续。原稿在此处写“由简单函数的表达式”。

### 3.3 一般可测函数情形

取简单函数列 \(\varphi_k\in S(E)\)，使
\[
\varphi_k(x)\longrightarrow f(x)\qquad (x\in E)
\]
在几乎处处有限的集合上成立。对每个 \(k\)，应用简单函数情形选取闭集 \(F_k\subset E\)，使
\[
m(E\setminus F_k)<\frac{\delta}{2^k},
\qquad
\varphi_k|_{F_k}\in C(F_k).
\]
为使集合递减，可令
\[
G_k=\bigcap_{j=1}^{k}F_j.
\]
那么 \(G_{k+1}\subset G_k\)，每个 \(G_k\) 为闭集，且
\[
m(E\setminus G_k)
\le \sum_{j=1}^{k}m(E\setminus F_j)
<\delta.
\]
令
\[
F=\bigcap_{k=1}^{\infty}G_k.
\]
则 \(F\) 为闭集。由于 \(F=\bigcap_{j=1}^{\infty}F_j\)，有
\[
E\setminus F=\bigcup_{j=1}^{\infty}(E\setminus F_j),
\]
从而由可数次可加性
\[
m(E\setminus F)\le \sum_{j=1}^{\infty}m(E\setminus F_j)
<\sum_{j=1}^{\infty}\frac{\delta}{2^j}=\delta.
\]
<span style="color:#1f5fbf">[订正说明] 原稿把 \(m(E\setminus F_k)<\delta/2^k\) 直接与 \(F=\cap F_k\) 合并。严格写法需要先使用 \(G_k=\cap_{j\le k}F_j\)，或者直接从 \(F=\cap F_k\) 写 \(E\setminus F=\cup_k(E\setminus F_k)\)。前者同时保留“递减闭集”的课堂结构。</span>

为了保证严格的函数连续性，在 \(F\) 上使用限制函数
\[
f|_F=\lim_{k\to\infty}\varphi_k|_F.
\]
<span style="color:#1f5fbf">[补充条件] 需要在 \(F\) 上取得一致收敛，或在课程所采用的近似构造中直接让 \(f|_F\) 与某个连续代表相同。仅有逐点收敛并不能自动推出极限连续，故原稿的“\(\varphi_k\in C(F_k)\)”之后还隐含使用了统一收敛或分层选择。</span>

## 4. Egoroff 定理

**Egoroff 定理。** 设 \(m(E)<+\infty\)，\(f_n:E\to\mathbb R\) 可测，并且
\[
f_n(x)\longrightarrow f(x)\quad\text{a.e. on }E.
\]
给定 \(\delta>0\)，存在可测集 \(G_\delta\subset E\)，使
\[
m(E\setminus G_\delta)<\delta,
\]
且 \(f_n\to f\) 在 \(G_\delta\) 上一致收敛。

### 4.1 按原稿的误差集合证明

对 \(r\in\mathbb N\)，定义
\[
A_{r,N}
=\bigcup_{n\ge N}\left\{x\in E:|f_n(x)-f(x)|\ge \frac1r\right\}.
\]
对于固定 \(r\)，集合 \(A_{r,N}\) 随 \(N\) 递减。由于 \(f_n\to f\) 几乎处处，
\[
m\!\left(\bigcap_{N=1}^{\infty}A_{r,N}\right)=0.
\]
且 \(m(E)<+\infty\)，所以可取 \(N_r\) 使
\[
m(A_{r,N_r})<\frac{\delta}{2^r}.
\]
令
\[
G_\delta=E\setminus\bigcup_{r=1}^{\infty}A_{r,N_r}.
\]
则
\[
m(E\setminus G_\delta)
\le \sum_{r=1}^{\infty}m(A_{r,N_r})
<\sum_{r=1}^{\infty}\frac{\delta}{2^r}
=\delta.
\]
若 \(x\in G_\delta\)，给定 \(\varepsilon>0\)，取 \(r\) 使 \(1/r<\varepsilon\)。当 \(n\ge N_r\) 时，\(x\notin A_{r,N_r}\)，故
\[
|f_n(x)-f(x)|<\frac1r<\varepsilon.
\]
\(N_r\) 只依赖于 \(\varepsilon\)，不依赖于 \(x\in G_\delta\)，因而 \(f_n\to f\) 在 \(G_\delta\) 上一致收敛。

### 4.2 与原稿的交集构造对应

原稿用 \(F_k\) 和 \(F=\cap_kF_k\) 的形式表达同一思想。每个 \(F_k\) 控制误差 \(2^{-k}\delta\)，交集的补集由可数次可加性控制。原稿页边还写出函数变换
\[
g(x)=\frac{f(x)}{1+|f(x)|},
\qquad
f(x)=\frac{g(x)}{1-|g(x)|},
\]
用于把扩展实值函数转化为有界函数再应用有限值结论。后一个等式只在 \(|g(x)|<1\) 的点上成立。

### 4.3 原稿的无限测度段

<span style="color:#111">原稿第 4 页下半部另起 \(m(E)=+\infty\) 的情形，写出球壳
\[
A_k=B(0,k)\setminus B(0,k-1),
\]
并用 \(A_k\) 对 \(E\) 作可数分解；是否每一项还与 \(E\) 取交在图上省写。旁注强调先在有限测度块上处理。</span>

<span style="color:#1f5fbf">[复习补充] 当 \(m(E)=+\infty\) 时，不能直接把 Egoroff 的全局结论套在 \(E\) 上。可先取 \(E_j=E\cap B(0,j)\) 或 \(E_j=E\cap(A_1\cup\cdots\cup A_j)\)，在每个有限测度 \(E_j\) 上应用 Egoroff，再根据需要作局部化或对角线选择。</span>

## 5. Urysohn 引理与 Lusin 证明中的连续延拓

### 5.0 原稿的“Lusin 逆定理”页

<span style="color:#111">原稿第 5 页先写标题“Lusin 逆定理”，随后给出 \((A,\mu)\) 的定理开头和三条编号条件。第 1 条可辨为 \(x\in A\)；第 2 条的首个关系可辨为 \(E\subset X\)，随后出现 \(f\in C(X)\)、\(\exists F\subset C(X)\) 和 \(F|_E=f\)，但量词与对象层级仍有疑字。原稿旁注还保留 \(m^*(A\cup B)\) 以及 \(C=A\cup B\) 的 Remark。以下黑色记录按图面保留；标准拓扑前提和延拓解释放在蓝色补充中。</span>

<span style="color:red">[原稿待定] 条件 1、2 的完整逻辑关系、\((A,\mu)\) 后的空间性质及 \(E\subset X\) 的量词不能从现有笔画唯一恢复。</span>

### 5.1 原稿列出的引理

若 \(A,B\) 是正规空间 \(X\) 中的两个不交闭集，则存在连续函数 \(u:X\to[0,1]\)，满足
\[
u|_A=0,
\qquad
u|_B=1.
\]
原稿旁注写 **Urysohn**。

### 5.2 用于简单函数的连续近似

设
\[
f=\sum_{i=1}^{\ell}a_i\chi_{E_i}
\]
且已经在每个 \(E_i\) 内选出闭集 \(F_i\subset E_i\)。若这些闭集两两不交，Urysohn 引理可为每个 \(F_i\) 构造连续的截断函数 \(u_i\)，使 \(u_i=1\) 在 \(F_i\) 上，且在其余闭集上按需要取 \(0\)。令
\[
g=\sum_{i=1}^{\ell}a_i u_i.
\]
则 \(g\) 连续，并在 \(F=\cup_iF_i\) 上满足 \(g=f\)。原稿第 5–6 页把这一延拓写为
\[
\varphi_k\in C(I^n),
\qquad
\exists g\in C(I^n),\quad g|_{F_\delta}=f,
\qquad
\exists g_k\in C(I^n),
\qquad
g_k|_{F_k}=f.
\]
<span style="color:#1f5fbf">[补充] 这里的 \(I^n\) 是一个包含 \(E\) 的紧方块。先在闭集 \(F_k\) 上得到连续函数，再用 Tietze 延拓定理或 Urysohn 型构造把它延拓到 \(I^n\)。</span>

### 5.3 Borel–Cantelli 型零测集控制

原稿页 6 的图面写出
\[
m(E\setminus F_k)<\frac{1}{2^k}
\]
（分子看作数字 \(1\)，与前文的 \(\delta\) 预算不一致），并在旁边标记 **Borel Cantelli**。原稿随后把一个 limsup 零测集合写成含 \(F_k\) 补集的形式，但运算符不完整。令
\[
H=\limsup_{k\to\infty}(E\setminus F_k)
=\bigcap_{N=1}^{\infty}\bigcup_{k\ge N}(E\setminus F_k).
\]
则
\[
m(H)=0,
\]
因为
\[
m\!\left(\bigcup_{k\ge N}(E\setminus F_k)\right)
\le \sum_{k\ge N}\frac{\delta}{2^k}
\xrightarrow[N\to\infty]{}0.
\]
因此对几乎处处的 \(x\in E\)，只有有限多个 \(k\) 使 \(x\notin F_k\)。这给出蓝色的标准数学恢复；原稿黑色行只明确到“几乎处处 \(g_k\to f\)”及页底“\(g_k\) 在 \(F\) 上一致收敛，\(\exists g\) 使 …”的未完成结论，不能把标准 \(H\) 公式冒充为原式。

## 6. 原稿疑点与图形信息

- RA12-P001-U01 至 U02：Littlewood 第 1、2 条的连接词与“几乎处处”后的短语字形连写。正文按标准术语恢复，同时在转写中保留疑点。
- RA12-P001-U03：有限区间 \(I_i\) 的端点约定未明。学习稿保留“区间”这一课堂用语。
- RA12-P001-U04 至 U06：页底 Lemma 的空间、索引和映射关系不唯一。没有把标准定理强行写回黑色原文。
- RA12-P002-U01：原图可见 \(F_\delta\) 前后的“闭集”字样，但笔画较轻；学习稿按定理条件保留。
- RA12-P003-U01：原图先写 \(F_k\subset E\)，再写 \(\varphi_k\in C(F_k)\)；学习稿不把函数误作集合。
- RA12-P003-U03：有界化变换的逆式分母绝对值记号省略。学习稿明确 \(|g|<1\) 的适用条件。
- RA12-P004-U01：Egoroff 标题下的 \(G_\delta\subset E\)（或 \(\overline E\)）及 \(\varphi_k\) 接续句在页边处不完整；学习稿把标准误差集合证明明确标为补充。
- RA12-P005-U01 至 U02：Lusin 逆定理标题、Urysohn 条件和 \(C(I^n)\) 延拓的对象在原稿中交错。保真稿逐字记录，学习稿分成引理和应用两节。
- RA12-P006-U01 至 U02：原稿先写 \(g|_{F_\delta}=f\)，再写 \(g_k|_{F_k}=f\)；误差式分子看似 \(1\) 而非 \(\delta\)，limsup 内的差异/并交运算符号省写。学习稿把 \(H=\limsup(E\setminus F_k)\) 明确标为数学恢复。
- RA12-P007：整页为空白，未发现图形、页边字或淡色笔迹。

图形信息方面，第 1–6 页没有几何图形，只有公式分隔线、集合交并的括号和第 5 页的 Urysohn 条件记号。第 7 页为普通空白物理页。
