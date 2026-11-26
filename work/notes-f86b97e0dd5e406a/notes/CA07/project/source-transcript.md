# 交换代数 7 · 原稿逐页转写

按原 PDF 物理页序编排。原内容以普通正文收录，补充与订正使用蓝色提示块；原有明确提问保留红字。初读疑号对应候选记录。

## 物理页 1

代数数： $k/\mathbb Q$ 有限扩张， $\forall a,\ f(x)\in\mathbb Q[x]$

$f(a)=0$

$O_k=\{a\in k\mid f(x)\in\mathbb Z[x]\,$〔后字见初读疑点 P1-02，墨迹暂读“不为多项”〕$\}$

$V(O_k)$ 的根是代数整数，〔首符和“根”待辨〕

曲线尖点奇异〔末字待辨〕。

$X=V(y^2-x^3)$ 在 $\mathbb A^2$ 中〔上标复核〕 的〔后细字待辨〕

〔图：左端尖点浓墨，两支自该点向右上及右下张开，右下枝外一小点。图在 regions/p0001-r2c2.png 左中。〕

$$
k[x,y]/(y^2-x^3)\cong k[t^2,t^3]\subseteq k(t)
$$

〔分母末幂写成上下两段笔，待辨。〕

记 $k[t^2,t^3]$ 中〔两上标位置及首字待辨〕 $t^2-a^2=0$〔字母／指数待辨〕 不〔一字待辨〕 $a\in k$。

整元素

$A\subseteq B,\quad b\in B$

$\exists a_i\in A,\ n\ge1$ $b^n+a_1 b^{n-1}+\cdots+a_n=0$〔中间浅笔和首幂待复核〕

$b$ 整于 $b$

> [!info] 原稿订正
>
> 末尾的字母按原笔迹录为 $b$。定义所称的是 $b$ 整于底环 $A$。

## 物理页 2

循环生成元。 $f(b)=0$ $n=\deg f(x)$〔中间等号上笔很淡〕

$A[b]=\sum_{i=0}^{n}Ab^i$，$A$ 模有限

$A[b]$ 有限 $A$ 模 iff $b$ 在 $A$ 上整。

$\Leftarrow$ $b$ 在 $A$ 上整， $\exists n,\ a_i$ st $f(x)=x^n+a_{n-1}x^{n-1}\cdots a_1x+a_0:0$

$$
f(b)=0\qquad b^n=-\sum_{k=0}^{n-1}a_i b^k
$$

$\forall m\ge n,$ $1,\ldots,b^{n-1}$ 是一组生成元

也可用 $g(b)\in A[b]$ $g(x)\in A[x]$

，$g(x)=g(x)f(x)+r(x)$〔右边商字母待辨〕 $\deg r<\deg f$

$A[b]=\sum_{k=0}^{n-1}Ab^k$〔和式下标形待辨〕

$\Rightarrow$

设 $A[b]=Au_1+\cdots+Au_n.$〔中间浅笔、尾部下标待辨〕

找 $f(x)\in A[x]$

## 物理页 3

$\times b:\ A[b]\longrightarrow A[b]$

$a\longrightarrow b\cdot a$〔右末字母笔形待辨〕

$\varphi_b(a\cdot a)=a\varphi_b(a)$〔点乘右侧、右末括内字形待辨〕

线性：〔草写待辨〕

$\varphi_b(a_i)=d_{i1}a_i+\cdots d_{ni}a_i$〔指标见疑点〕

$D=(d_{ij})_{k\times n}\in M_nA$〔矩阵尺寸首笔待辨〕

$$
\left\{\begin{aligned}bu_1&=d_{11}u_1\cdots d_{1\,\text{〔疑〕}}u_k\\\vdots\quad&=\quad\vdots\\bu_{\text{〔疑〕}}&=\quad\end{aligned}\right.
$$

〔等号与尾项指标待辨。末行右侧仅细竖线和曲笔。〕

$M_n(A)$ 取 $C^*$ $\exists\ \dfrac{C^*C}{\det(C)}=I$〔首符与分子上标待辨〕

<span style="color:red">（找个简〔疑〕的方法）〔原红笔待补〕</span>

〔红括号文字下方偏右另有一枚黑细点，作用待辨。〕

## 物理页 4

eg. $w^2=1+w,$

$\mathbb Z[w]$

$wu_1=u_2$

$wu_2=u_1+u_2$

$\det(TI-D)=T^2-T-1$

$$
D=\begin{pmatrix}0&1\\1&1\end{pmatrix}
$$

〔左上槽位未闭合弯笔，暂读 0。〕

Thm

$(1)$ $b$ 整于 $A$

$(2)$ $A[b]$ 有限 $A$ 模

$(i)$〔原号形待辨〕 $A[b]\subseteq C\subseteq B$， $C$ 有限 $A$ 模

$(4)$ $\exists$ 有限 $A$ 模 $M$， 使 $M$ 是忠实 $A[b]$ 模。

$R$ 环，$M$ 是 $R$ 模， $\mathrm{Ann}=\{r\in R\mid rm=0\}$

当 $\mathrm{Ann}=(0)$ 称 $M$ 是忠实 $R$ 模

$(2)\to(3)\to(4)$〔首号笔形待辨〕

$C=A[b]$ $M=C,$

$(3)\Rightarrow(4)$ $A[b]\subseteq M,$ $M$ 有 $Ab$ 模。〔Ab 未见独立方括〕 $m\in M$，$a\in A[b]$

## 物理页 5

$am$ 在 $C$ 中做乘法，〔做/作字形〕

若 $\exists a$ st $a\in A[b]$ $a\cdot M=0$〔0 下有一细点〕 $a\cdot1=0$

〔黑弯箭头从前一等式下方起，向右上连至 $a\cdot1=0$ 附近。〕

〔原红字：$1$〔三字待辨〕。〕

$M$ 是忠实 $A[b]$ 模， 也是有限生成 $A$ 模

eg. $V$ 是有限维 $k$〔向量空间缩写待辨〕 $\sigma\in\operatorname{End}_k(V)$

$$
k[\sigma]=\{f(\sigma):f\in A[T]\}\qquad f(\sigma)\cdot v=f(\sigma)(v)
$$

〔作用式的大小写和第二括形待核。〕

$V$ 是 $k$ 有限的，〔尾字待核〕 $V$ 有一个 $k[\sigma]$ 模。〔“一/个”待核〕

$V$ 是一个忠实 $k[\sigma]$ 模

$k[t]$ 多项式〔末笔待辨〕

在 $V$ 上有 $k[t]$-模结构〔中 t 字形待核〕

$v\in V,$〔大小写看原迹〕 $T\cdot v=\sigma(v)$〔等号前低点与 T 后笔形待辨〕

## 物理页 6

$m_\sigma:=\{f(x)\mid f(x)=0\}$〔取值与标记待辨，闭括下另有细点〕 $\lhd k[T]$〔关系号与 T 形待辨〕

$k[\sigma]\cong k[T]/\mathrm{Ann}$〔括内笔及分母指称待核〕

$M$ 是 $R$ 模

$\bar R=R/\mathrm{Ann}(R)(M)$〔中间括样是否下标待辨〕

$M$ 是 $R$ 模

$\bar R=R/\mathrm{Ann}_R(M)$〔R 附标待辨〕

Step1. $M$ 是一个 $\bar R$ 模结构〔是/有与 R 旁短笔待辨〕。

Step2: $M$ 的 $\bar R$ 模忠的。〔“忠”和有无“实”待辨〕

有限个整元。 A.

$A[b_1,\ldots,b_s]=\sum A\,b_1^{e_1}\cdots b_s^{e_1}$〔末幂为 $e$ 后短笔。〕

## 物理页 7

有限型，整与模有限。

$A$ 环， $B$ 是 $A$-代数

有限型：$A$ 代数 $\quad A[x_1,\ldots,x_n]\xrightarrow{\varphi}B$

满同态。〔首字待辨〕

$B\cong A[x_1,\ldots,x_n]/\ker\varphi$

有限型 $+$ 整 $\Longleftrightarrow$ 模有限。

$A[b_1,\ldots,b_s]$ $b_1,\ldots,b_s$ 整元 $\Rightarrow$ $A[b_1,\ldots,b_s]$ 有限 $A$ 模，〔末 b 形待辨〕

## 物理页 8

此物理页为空白。
