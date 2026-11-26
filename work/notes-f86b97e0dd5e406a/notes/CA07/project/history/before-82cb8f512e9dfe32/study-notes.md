# 交换代数 7 · 整元素与模有限性

黑字保留原课文，蓝块标出释义、补证及订正，红字沿用原稿的明确提问。中性疑号对应首读候选。

## 目录

1. [整元素、代数数与记号](#整元素代数数与记号)
2. [单生成代数的有限模判据](#单生成代数的有限模判据)
3. [中间环与忠实模判据](#中间环与忠实模判据)
4. [二次例题与尖点曲线](#二次例题与尖点曲线)
5. [线性算子与零化子商环](#线性算子与零化子商环)
6. [有限多个整元、有限型与代数整数的运算](#有限多个整元有限型与代数整数的运算)

## 整元素、代数数与记号

代数数：$k/\mathbb Q$ 有限扩张，$\forall a$〔量词短笔待核〕，$f(x)\in\mathbb Q[x]$。

$$
f(a)=0.
$$

$$
O_k=\{a\in k\mid f(x)\in\mathbb Z[x]\;\text{〔后竖笔及多项式短句待辨〕}\}.
$$

集合首符号为带 $k$ 下标的圈形〔疑 M1.2〕。

整元素。

$A\subseteq B$，$b\in B$。$\exists a_i\in A$，$n\ge1$。

$$
b^n+a_1b^{\,\text{〔n−1 形待核〕}}+\cdots+a_n=0.
$$

$b$ 整于 $b$。

> [!note] 补充｜整元素与代数整数
>
> 环采用带单位的交换环，同一包含中的单位一致。设 $A\subseteq B$，$b\in B$。若某个 $n\ge1$ 和 $a_1,\ldots,a_n\in A$ 满足
>
> $$
> b^n+a_1b^{n-1}+\cdots+a_n=0,
> $$
>
> 就称 $b$ 在 $A$ 上整，或称 $b$ 整于 $A$。这里的基环是 $A$，首一多项式的首项系数为 $1$。
>
> 当 $[k:\mathbb Q]=d<\infty$ 时，任意 $a\in k$ 的 $1,a,\ldots,a^d$ 在 $\mathbb Q$ 上线性相关，关系的系数不全为零，故存在非零 $f\in\mathbb Q[x]$ 满足 $f(a)=0$。在 $\mathbb Q[x]$ 中可用首项系数归一化。
>
> $k$ 中的代数整数要求同一个求根多项式具有整系数且首一。可规范记作 $\mathcal O_k=\{a\in k\mid \exists f\in\mathbb Z[x]\text{ 首一},\,f(a)=0\}$。例如 $1/2$ 满足 $2x-1=0$。若它满足首一次数 $n\ge1$ 的整系数式，乘以 $2^n$ 即得 $1$ 加偶数等于 $0$ 的矛盾。

> [!note] 术语表
>
> | 记号或术语 | 含义 |
> | --- | --- |
> | $A[b_1,\ldots,b_s]$ | 由 $A$ 与这些元素生成的子代数。对一般结构映射 $A\to B$，其中的 $A$ 指其像。 |
> | 有限 $A$ 模、模有限 | 有限生成的 $A$ 模，允许生成元之间有关系。 |
> | 有限型 $A$ 代数 | 有限多个元素连同 $A$ 的像通过加法、乘法生成整个目标环。 |
> | $B$ 整于 $A$ | $B$ 中每个元素都满足系数来自 $A$ 的首一关系。 |
> | $\operatorname{Ann}_R(M)$ | $\{r\in R\mid rm=0\ \text{对所有 }m\in M\}$。 |
> | 忠实 $R$ 模 | $\operatorname{Ann}_R(M)=(0)$。 |
> | $R/I$ | $R$ 对理想 $I$ 的商环，元素为陪集 $r+I$。 |
> | $\operatorname{End}_A(M)$ | $A$ 线性自映射组成的环，乘法为复合。 |

## 单生成代数的有限模判据

〔循环／给示，疑 M2.1〕生成元。$f(b)=0$，$n\text{〔=／横〕}\deg f(x)$。

$$
A[b]=\sum_{i=0}^{n}Ab^i.
$$

$A$ 模〔有限／生成，疑 M2.1〕。

$A[b]$ 有限 $A$ 模 iff $b$ 在 $A$ 上整。

> [!note] 补充｜两个证明工具
>
> 除以首一 $f(T)\in A[T]$ 时，若被除多项式当前最高项是 $cT^d$ 且 $d\ge\deg f$，减去 $cT^{d-\deg f}f(T)$ 可消掉最高项。有限次后得到 $g=qf+r$，其中 $r=0$ 或 $\deg r<\deg f$。如果有两组商和余数，则 $f(q-q')=r'-r$。当 $q-q'\ne0$ 时，左边因 $f$ 首一而有次数 $\deg f+\deg(q-q')$，与右边矛盾，故商和余数唯一。
>
> 设 $C$ 是带单位交换环上的方阵。按行、列展开行列式，由余子式组成的转置矩阵 $\operatorname{adj}(C)$ 满足 $\operatorname{adj}(C)C=\det(C)I$。积的对角项为通常的余子式展开，非对角项为含两条相同行或列的行列式，因而为零。只有 $\det(C)$ 为单位时，$\det(C)^{-1}\operatorname{adj}(C)$ 才给出原环上的逆矩阵。

$\Leftarrow$，$b$ 在 $A$ 上整，$\exists n,a_{\text{〔i 形〕}}\ \mathrm{s.t.}$

$$
f(x)=x^n+a_{n-1}x^{n-1}\cdots a_1x+a_0\text{〔点形〕}0.
$$

$$
f(b)=0,\qquad b^n=-\sum_{k=0}^{n-1}a_i b^k.
$$

$\forall m\ge n$，$1,\ldots,b^{n-1}$ 是一组生成元。

> [!note] 补证与订正｜路线一 · 降幂归纳
>
> 式中把求和系数统一作 $a_k$。取 $f(x)=x^n+\sum_{k=0}^{n-1}a_kx^k$，其关系为 $f(b)=0$。出现的零值应施加于 $b$ 处的求值。
>
> 设 $S=A+Ab+\cdots+Ab^{n-1}$。幂次 $m<n$ 时 $b^m\in S$。若 $m\ge n$，用首一关系得到
>
> $$
> b^m=-\sum_{k=0}^{n-1}a_kb^{m-n+k}.
> $$
>
> 指数 $m-n+k$ 非负且小于 $m$，强归纳法给出 $b^m\in S$。而 $A[b]$ 的每个元素是有限个幂的 $A$ 线性组合，所以 $A[b]=S$。额外把 $b^n$ 加入生成元也给出同一 $A$ 模，开头的上限 $n$ 可以是冗余生成式。

也可〔用／以〕，$g(b)\in A[b]$，$g(x)\in A[x]$。

，$g(x)=\text{〔g/q〕}(x)f(x)+r(x)$，$\deg r<\deg f$。

$$
A[b]=\sum_{\text{〔k/l 形〕}=0}^{n-1}Ab^k.
$$

> [!note] 补证｜路线二 · 首一多项式除法
>
> 任取 $u=g(b)\in A[b]$，其中 $g(x)\in A[x]$。由前面的首一除法有 $g=qf+r$，这里用 $q$ 命名商，$r=0$ 或 $\deg r<n$。在 $b$ 处求值，得 $u=q(b)f(b)+r(b)=r(b)$，故 $u$ 落在 $1,b,\ldots,b^{n-1}$ 的 $A$ 线性包中。这些幂本来就在 $A[b]$，所以得到 $A[b]=\sum_{k=0}^{n-1}Ab^k$。

$\Rightarrow$

设 $A[b]=Au_1+\cdots+Au_n$。〔中间连接淡，末下标待核。〕

找 $f(x)\in A[x]$。

$$
\times b\colon A[b]\longrightarrow A[b],\qquad a\longrightarrow b\cdot\text{〔a/q 形〕}.
$$

$\varphi_b(a\cdot\text{〔a/q 形〕})=\text{〔a/n 形〕}\,\varphi_b(\text{〔a/q 形〕})$。〔疑 M3.1〕

〔线性／对比，疑 M3.2〕：

$$
\varphi_b(a_i)=d_{i,1}a_i+\cdots+d_{ni}a_i,\qquad
D=(d_{ij})_{k\times n}\in M_nA.
$$

原括号列式：

$$
\left\{
\begin{aligned}
bu_1&=d_{11}u_1\ \cdots\ d_{1,\text{〔疑〕}}u_k\\
\vdots\ &={}\ \vdots\\
bu_{\text{〔3/k 形〕}}&={}
\end{aligned}
\right.
$$

最末行右边有细竖线和曲笔。〔疑 M3.3〕

$$
M_n(A)\ \text{〔取／求形〕}\ C^*\qquad
\text{〔∃形〕}\ \frac{C^*C}{\det(C)}=I.
$$

〔下方红括注右下另有一枚孤立黑点，未辨出与附近公式相连。〕

<span style="color:red">原待填｜（找〔一〕个简〔易字待核〕的方法）</span>

> [!note] 补证与订正｜行列式技巧回答原待填
>
> 记 $\varphi_b(u)=bu$。对 $\lambda\in A$、$u,v\in A[b]$，分配律给出 $\varphi_b(u+v)=\varphi_b(u)+\varphi_b(v)$，交换律给出 $\varphi_b(\lambda u)=\lambda\varphi_b(u)$，所以 $\varphi_b$ 是 $A$ 线性自映射。
>
> 对每个 $i=1,\ldots,n$ 选定 $d_{ij}\in A$ 使 $bu_i=\sum_{j=1}^n d_{ij}u_j$。用行表示「第 $i$ 个生成元的像」，令 $D=(d_{ij})_{1\le i,j\le n}$，$U=(u_1,\ldots,u_n)^{\mathsf T}$。于是
>
> $$
> (bI_n-D)U=0.
> $$
>
> 在 $A[b]$ 中用伴随矩阵左乘，得到 $\det(bI_n-D)U=0$。本步使用 $\operatorname{adj}(C)C=\det(C)I$，适用于行列式为零或非单位。$F(T)=\det(TI_n-D)\in A[T]$ 首一，行列式展开中 $T^n$ 只来自主对角线上各取一个 $T$。求值与行列式展开可交换，所以 $F(b)u_i=0$。由于 $1\in A[b]$，存在 $\lambda_i\in A$ 使 $1=\sum_i\lambda_i u_i$。因此 $F(b)=\sum_i\lambda_i F(b)u_i=0$，证得 $b$ 在 $A$ 上整。生成元不必是基，矩阵 $D$ 也可以随所选系数而变。

## 中间环与忠实模判据

Thm

1. $b$ 整于 $A$。
2. $A[b]$ 有限 $A$ 模。〔原编号笔形待核。〕
3. $A[b]\subseteq C\subseteq B$，$C$ 有限 $A$ 模。〔原编号近 i 形。〕
4. $\exists$ 有限 $A$ 模 $M$，使 $M$ 是忠实 $A[b]$ 模。

$R$ 环，$M$ 是 $R$ 模，$\operatorname{Ann}=\{r\in R\mid rm=0\}$。〔疑 M4.3〕

当 $\operatorname{Ann}=(0)$，称 $M$ 是忠实 $R$ 模。

> [!note] 释义｜定理中的环、标量与零化子
>
> 第（3）条的 $C$ 取中间子环，单位与 $A[b]$ 一致。第（4）条的 $A$ 模作用是限制 $A[b]$ 作用到 $A$ 得到的。
>
> 零化子是对所有 $m\in M$ 同时要求 $rm=0$ 的那些 $r$。若 $r,s$ 均零化 $M$，则 $(r-s)m=0$ 对所有 $m$ 成立。对任意 $u\in R$ 也有 $(ur)m=u(rm)=0$，故零化子是 $R$ 的理想。忠实性还等价于作用同态 $R\to\operatorname{End}_R(M)$，$r\mapsto(m\mapsto rm)$，是单射。

$(2)\to(3)\to(4)$。〔首号笔形待核。〕$C=A[b]$，$M=C$。

$(3)\Rightarrow(4)$。$A[b]\subseteq M$，$M$ 有 $Ab$ 模〔方括形疑 M4.4〕，$m\in M$，$a\in A[b]$。

$am$ 在 $C$ 中做〔或作〕乘法。若 $\exists a$ s.t. $a\in A[b]$，原式写 $a\cdot M=0$ 和 $a\cdot1=0$。前一式的 $0$ 下方另见细点。黑弯箭自前式下方起，向右上指到后一式附近。

<span style="color:red">原问｜1 哪来的〔后三字待核〕</span>

> [!note] 补证｜取中间环本身作模
>
> $(2)\Rightarrow(3)$ 取 $C=A[b]$。给定（3），取 $M=C$，并把 $a\in A[b]$ 对 $m\in C$ 的作用定义成 $C$ 中的乘积 $am$。因为 $C$ 是子环，这一积仍在 $C$ 中，并满足模公理。又因为 $C$ 作为 $A$ 模有限生成，$M$ 满足（4）的有限性要求。
>
> 这里的 $1$ 是 $A[b]\subseteq C=M$ 中的单位 $1_C$。若 $aM=0$，取模中的元素 $m=1_C$，即得 $0=a\cdot1_C=a$。所以 $M=C$ 是忠实的 $A[b]$ 模。对（4）中任意给出的模，证明要用忠实性，不能直接取一个默认存在的模元 $1$。

$M$ 是忠实 $A[b]$ 模，也是有限生成 $A$ 模。

> [!note] 补证｜从忠实模推出首一关系
>
> 给定（4），取有限 $A$ 生成元 $u_1,\ldots,u_n$。若 $M=0$，忠实性推出 $A[b]$ 为零环，可用首一关系 $T$；否则可取 $n\ge1$。按乘以 $b$ 的作用选 $d_{ij}\in A$，使 $b u_i=\sum_j d_{ij}u_j$，记 $D=(d_{ij})$。与前面相同，$\operatorname{adj}(bI-D)(bI-D)U=0$，于是 $F(b)u_i=0$，其中 $F(T)=\det(TI-D)\in A[T]$ 首一。
>
> 每个 $m\in M$ 是这些 $u_i$ 的 $A$ 线性组合，故 $F(b)m=0$ 对所有 $m$ 成立。由忠实性，$F(b)=0$ 在 $A[b]$ 中成立，所以（4）推出（1）。连同两条 $(1)\Rightarrow(2)$ 的证明和原稿的 $(2)\Rightarrow(3)\Rightarrow(4)$，四条等价。

## 二次例题与尖点曲线

eg. $w^2=1+w$〔亦读 $\omega$，疑 M4.1〕，$\mathbb Z[w]$〔右括旁有重笔〕。

$$
wu_1=u_2,\qquad wu_2=u_1+u_2.
$$

左下的矩阵与位于它右上方的行列式：

$$
D=\begin{pmatrix}\text{〔0 形〕}&1\\1&1\end{pmatrix},\qquad
\det(TI-D)=T^2-T-1.
$$

> [!note] 解答｜用乘法矩阵求二次关系
>
> 把这一例中的二次根记为 $\omega$，取 $u_1=1$，$u_2=\omega$。关系 $\omega^2=1+\omega$ 使所有更高幂都能归约为 $1,\omega$ 的整数线性组合，所以这两元生成 $\mathbb Z[\omega]$。两个像的系数给出
>
> $$
> D=\begin{pmatrix}0&1\\1&1\end{pmatrix},\qquad
> TI-D=\begin{pmatrix}T&-1\\-1&T-1\end{pmatrix}.
> $$
>
> 展开得 $T(T-1)-(-1)(-1)=T^2-T-1$。代入 $\omega$ 得 $\omega^2-\omega-1=0$，也检验了原起点。若把 $\omega$ 取为复数中的任一根，则它不在 $\mathbb Q$，因为有理根定理给出的 $\pm1$ 都不是根。于是 $1,\omega$ 在 $\mathbb Q$ 及 $\mathbb Z$ 上独立，此处也确实构成 $\mathbb Z[\omega]$ 的 $\mathbb Z$ 基。

曲线尖点奇异〔末字及题头读法待核〕。

$X=V(y^2-x^3)$ 在 $\mathbb A^2$ 中〔上标待核〕，其后的短字疑为「的……」或「也是……」。〔疑 M1.4〕

〔原图〕左侧一尖点有浓墨，两支从这个接点分别向右上和右下张开，右下枝外另有一小点。无坐标轴或文字标注。

$$
k[x,y]/(y^2-x^3)\cong k[t^2,t^3]\subseteq k(t).
$$

〔商式分母末幂有上下两段笔。〕

〔记／在〕$k[t^{\text{〔?〕}},t^{\text{〔?〕}}]$ 中，$t^2-a^2=0$〔字母及指数待核〕，不〔后字待核〕，〔末变量疑 M1.5〕$\in k$。

> [!note] 解答｜参数环中的整元素
>
> 记 $R=k[t^2,t^3]$。把 $x,y$ 分别映成 $t^2,t^3$，所得 $k$ 代数同态 $k[x,y]\to k[t]$ 的像为 $R$，且消去 $y^2-x^3$。在 $k[x][y]$ 中除以这个关于 $y$ 的首一式后，余式为 $P(x)+yQ(x)$。它映为 $P(t^2)+t^3Q(t^2)$。第一项只含偶数次数，第二项只含不小于 $3$ 的奇数次数，互相不能抵消。若像为零，则 $P=Q=0$，所以同态的核恰为 $(y^2-x^3)$，得到原商环的同构。
>
> $t=t^3/t^2\in\operatorname{Frac}(R)$，所以 $\operatorname{Frac}(R)=k(t)$。$R$ 中的多项式没有一次项，故 $t\notin R$。但在形式变量 $T$ 中，$T^2-t^2\in R[T]$ 首一，在 $T=t$ 处为零。因此 $t$ 对 $R$ 整。按「在分式域中整于 $R$ 的元素都属于 $R$」定义整闭，这个 $R$ 不是整闭的。
>
> 若原句是考虑 $t^2-a^2=0$ 且 $a\in k$，因为 $t$ 是不定元，次数为 $2$ 的多项式不能与常数相等。即便取 $a\in R$，在域 $k(t)$ 中也有 $(t-a)(t+a)=0$，故只可能 $a=\pm t$，这两者都不属于 $R$。这与在扩环中让 $t$ 满足首一关系并不冲突。
>
> 在实数参数的示意图中，$x=t^2$ 非负，$t$ 的两种符号给出上下各一支。对 $t\ne0$ 有 $y/x=t$。当 $t\to0$ 时这个斜率趋于 $0$，两支沿 $x$ 轴在原点相接。
>
> 如果题头所指的是原点的奇异性，可以按局部环定义检验。记坐标环中的原点理想为 $\mathfrak m=(x,y)$。定义关系 $y^2-x^3$ 在 $(x,y)^2$ 中，所以 $\mathfrak m/\mathfrak m^2$ 仍有两个独立的一次类 $x,y$。坐标环作为 $k[x]$ 模由 $1,y$ 生成。任一非零素理想 $\mathfrak p$ 含某个非零的 $P(x)+yQ(x)$，与 $P(x)-yQ(x)$ 相乘得到仍非零的 $P(x)^2-x^3Q(x)^2\in\mathfrak p\cap k[x]$。这里另一因子非零可用同一唯一余式，两个因子的积非零来自已证的整域性质。
>
> 因此 $R/\mathfrak p$ 是有限维的 $k$ 代数且为整域。每个非零元素的乘法在这个有限维空间里是单射，故也是满射，于是可逆，$R/\mathfrak p$ 是域。每个非零素理想都极大，故原点局部环的维数为 $1$。局部化后，$\mathfrak m/\mathfrak m^2$ 上的非零分母只通过其在原点的非零值作用，所以一次空间仍为二维。极大理想由 $x,y$ 生成，任何生成集的像都必须张成该二维空间。因此极大理想的最少生成数为 $2$，超过局部环的维数，原点不正则，即此曲线的原点是奇点。

## 线性算子与零化子商环

$M$ 是 $R$ 模。

$$
\overline R=R/\operatorname{Ann}(R)(M)\quad\text{〔括号层级疑 M6.3〕}.
$$

$M$ 是 $R$ 模。

$$
\overline R=R/\operatorname{Ann}_R(M).
$$

Step 1. $M$ 〔是／具〕一个 $\overline R$ 模结构。〔$\overline R$ 旁有细曲笔。〕

Step 2. $M$ 的 $\overline R$ 模忠〔有无“实”待核〕的。〔疑 M6.4〕

> [!note] 补证｜商环作用与忠实性
>
> 令 $I=\operatorname{Ann}_R(M)$。在同一个加法群 $M$ 上定义 $(r+I)\cdot m=rm$。若 $r+I=r'+I$，则 $r-r'\in I$，因此 $(r-r')m=0$，作用与代表元无关。两条分配律、结合律和 $(1+I)m=m$ 均由原 $R$ 作用继承，例如 $((r+I)(s+I))m=(rs)m=r(sm)$。这给出第 1 步。
>
> 若 $r+I$ 在此作用下使每个 $m$ 都变零，则 $r\in I$，陪集 $r+I=0+I$。所以 $M$ 对 $\overline R$ 忠实，这给出第 2 步。此处原稿重复写的两个商式都对应同一个商环 $R/I$。

eg. $V$ 是有限维 $k$ 空间〔原简称疑 M5.2〕，$\sigma\in\operatorname{End}_k(V)$〔End 左上有短划〕。

$$
k[\sigma]=\{f(\sigma)\mid f\in A[T]\},\qquad f(\sigma)\cdot v=f(\sigma)(v).
$$

〔后一式字母的大小写与右端两括待核。〕

$V$ 是 $k$〔有限的／生成的〕，$V$ 有一〔个字形待核〕 $k[\sigma]$ 模。

$V$ 是一个忠实 $k[\sigma]$ 模。

> [!note] 解答与订正｜算子子代数作用
>
> 例的系数来自 $k$。把 $f(T)=\sum_i a_iT^i\in k[T]$ 送到 $\sum_i a_i\sigma^i$，其常数项作 $a_0\operatorname{id}_V$。这些算子组成 $k[\sigma]$。标量自同态和 $\sigma$ 可交换，因此这个像虽处在可能不交换的 $\operatorname{End}_k(V)$ 中，仍是交换的。
>
> 用算子在向量上的求值定义作用。对算子 $S,U\in k[\sigma]$，$(SU)\cdot v=S(U(v))$，恒等算子作用为恒等，两条分配律来自算子加法和线性性，故得到模。若 $S$ 使每个 $v$ 都变为零，则 $S$ 本身就是零映射，证得 $V$ 忠实。$V$ 有有限 $k$ 基，故满足有限 $k$ 模条件。

$k[t]$ 多项式〔末笔待核〕。

在 $V$ 上有 $k[\text{〔t/u/σ 形〕}]$ 模结构〔疑 M5.3〕。

$$
v\in V,\qquad T\cdot v=\sigma(v).
$$

〔两个 $v/V$ 形的大小及作用式点迹待核。〕

$$
m_{\text{〔σ/b 形〕}}:=\{f(x)\mid f(x)=0\}\ \lhd\ k[T],\qquad
k[\sigma]\cong k[T]/\operatorname{Ann}.
$$

〔理想式闭括下有细点，关系尾与第二个实参待核。〕

> [!note] 解答与订正｜评价同态的核
>
> 把 $v\in V$ 上的作用定义为 $f(T)\cdot v=f(\sigma)(v)$，于是 $T\cdot v=\sigma(v)$。定义 $\operatorname{ev}_\sigma\colon k[T]\to k[\sigma]$ 为 $f\mapsto f(\sigma)$，加法显然保留，乘法由 $\sigma^i\sigma^j=\sigma^{i+j}$ 及系数与 $\sigma$ 交换得到。它按像的定义满射。
>
> 商环的分母是这个同态的核
>
> $$
> I_\sigma=\{f(T)\in k[T]\mid f(\sigma)=0\text{ 作为算子}\}
> =\operatorname{Ann}_{k[T]}(V).
> $$
>
> 两个多项式的值相同恰当它们之差属于 $I_\sigma$。因此 $f+I_\sigma\mapsto f(\sigma)$ 良定义、单射且满射，给出 $k[T]/I_\sigma\cong k[\sigma]$。把纸面 $f(x)=0$ 读成多项式恒等式只会留下零多项式，无法给出此核。例如 $\sigma=0$ 且 $V\ne0$ 时，$T$ 已在核中。
>
> 若 $\dim_kV=d>0$，则 $1,\sigma,\ldots,\sigma^{d^2}$ 在维数 $d^2$ 的 $\operatorname{End}_k(V)$ 中线性相关，故 $I_\sigma$ 含非零多项式。选其中最低次数的首一式 $m_\sigma(T)$，任一 $g\in I_\sigma$ 除以 $m_\sigma$ 的余式仍在核中，若非零则次数矛盾。因此 $I_\sigma=(m_\sigma)$。$V=0$ 时核是整个 $k[T]$，可取 $m_\sigma=1$。这也解释了 $V$ 对 $k[T]$ 的作用与对其像 $k[\sigma]$ 的忠实作用之间的关系。

## 有限多个整元、有限型与代数整数的运算

有限个整元。$A$。

$$
A[b_1,\ldots,b_s]=\sum A\,b_1^{e_1}\cdots b_s^{e_{\text{〔1/s 形〕}}}.
$$

$A[b_1,\ldots,b_s]$，$b_1,\ldots,b_s$ 整元 $\Rightarrow A[b_1,\ldots,\text{〔b/d〕}_s]$ 有限 $A$ 模，〔疑 M7.2〕

> [!note] 补证｜幂积的有限指数范围
>
> 分别给每个 $b_i$ 选一个次数为 $n_i\ge1$ 的首一关系。任一元素是 $b_1^{e_1}\cdots b_s^{e_s}$ 的有限 $A$ 线性组合。对第 $i$ 个因子应用单元素的降幂关系，把所有 $e_i\ge n_i$ 的幂逐次降到低于 $n_i$ 的 $A$ 线性组合。由于环交换，可以把各因子的展开相乘，得到
>
> $$
> A[b_1,\ldots,b_s]=\sum_{0\le e_i<n_i\, (1\le i\le s)}
>    A\,b_1^{e_1}\cdots b_s^{e_s}.
> $$
>
> 这些幂积本来就在左边，故等式两包含都成立，且最多有 $\prod_i n_i$ 个生成元。若 $s=0$，空乘积对应 $1$，代数是 $A$。

有限型，整与模有限。

$A$ 环，$B$ 是 $A$-代数。有限型：$A$ 代数。

$$
A[x_1,\ldots,x_{\text{〔n/s 形〕}}]\xrightarrow{\varphi}B
$$

箭头下小注「满同态。」〔首字待核。〕

$$
B\cong A[x_1,\ldots,x_{\text{〔n/s 形〕}}]/\ker\varphi.
$$

有限型＋整 $\Leftrightarrow$ 模有限。

> [!note] 补证｜有限型、整与模有限的等价
>
> 设结构同态为 $\iota\colon A\to B$。若 $B$ 由 $b_1,\ldots,b_s$ 作为 $A$ 代数生成，替换变量 $x_i\mapsto b_i$、系数 $a\mapsto\iota(a)$ 就定义了满的 $A$ 代数同态 $\varphi\colon A[x_1,\ldots,x_s]\to B$。反过来给这样的满同态，$b_i=\varphi(x_i)$ 生成 $B$。$\varphi$ 的核是理想，两个原像多项式映到同一个元素恰当它们之差在核中，于是 $f+\ker\varphi\mapsto\varphi(f)$ 给出商环同构。
>
> 若 $B$ 有限型且整于 $A$，有限代数生成元 $b_i$ 都满足首一关系。前一节的有界幂积为出发点，直接给出 $B$ 的有限 $A$ 模生成元。
>
> 若 $B$ 是有限 $A$ 模，取 $y_1,\ldots,y_r$ 为模生成元。含 $\iota(A)$ 和全部 $y_j$ 的子代数含它们的每个 $A$ 线性组合，故等于 $B$，给出有限型。任取 $b\in B$，以 $A'=\iota(A)$，$C=B$，中间环有限模判据给出 $b$ 在 $A'$ 上整。首一式低次系数可逐一沿 $\iota$ 提升为 $A$ 的元素，首项用 $1_A$，所以 $b$ 在 $A$ 上整。此处 $A$ 的作用只通过 $A'$，因此有限性在两环表述下相同。

$\text{〔U/V 形〕}(O_k)$ 的〔根／和〕是代数整数，〔疑 M1.3〕

> [!note] 补充｜代数整数的和、积及首一方程的根
>
> 设 $\alpha,\beta\in\mathcal O_k$。两者各自满足一个首一整系数关系，故 $\mathbb Z[\alpha,\beta]\subseteq k$ 由有界幂积生成，作为 $\mathbb Z$ 模有限。若 $\gamma=\alpha+\beta$ 或 $\gamma=\alpha\beta$，则 $\mathbb Z[\gamma]\subseteq\mathbb Z[\alpha,\beta]$，以该有限中间环应用判据，得到 $\gamma\in\mathcal O_k$。
>
> $0,1$ 分别满足 $T$ 和 $T-1$。若 $\alpha$ 满足次数 $n$ 的首一式 $f(T)$，则 $-\alpha$ 满足首一式 $(-1)^nf(-T)$，故这些代数整数构成 $k$ 的子环。上述运算中，整数均指代数整数。
>
> 若原行的字是「根」，一种成立的表述是代数整数系数的首一式的根仍是代数整数。设系数 $c_1,\ldots,c_n$ 都是代数整数，$F(T)=T^n+c_1T^{n-1}+\cdots+c_n$ 且 $F(\gamma)=0$。先取 $A=\mathbb Z[c_1,\ldots,c_n]$，它由有限多个 $\mathbb Z$ 模生成元 $v_i$ 张成。再用 $F(\gamma)=0$ 得 $A[\gamma]$ 由 $1,\gamma,\ldots,\gamma^{n-1}$ 作为 $A$ 模生成。于是所有 $v_i\gamma^j$（$0\le j<n$）是 $A[\gamma]$ 的一组有限 $\mathbb Z$ 模生成元。选中间环 $A[\gamma]$，按单元素判据得到 $\gamma$ 也对 $\mathbb Z$ 整。

原 PDF 的物理第 8 页为空白。
