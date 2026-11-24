<!-- unit: N-INTRO -->
# 实分析 7：测度与 Lebesgue 外测度

## 阅读约定

普通正文保留原稿内容与原有路线。蓝色 `info` 块按“补充”“补证”“纠错”说明新增内容；红色只标原稿明确未答位置。中性疑字编号见独立疑点表。

## 目录

1. [一、测度公理与典型测度](#n-sec-01)
2. [二、基数记号与集合函数的数量](#n-sec-02)
3. [三、Jordan 内容、Darboux 判据与稠密有限覆盖](#n-sec-03)
4. [四、非负求和、Lebesgue 覆盖及两条存在性路线](#n-sec-04)
5. [五、Lebesgue 外测度及可列次可加性](#n-sec-05)
6. [六、矩形体积、可数点集与 Cantor 集](#n-sec-06)
7. [七、Carathéodory 可测性与切分图](#n-sec-07)
8. [八、矩形测试与跨内外加性：完整原证明](#n-sec-08)
9. [九、正距离加性与闭集、紧集的分离](#n-sec-09)
10. [十、可测族封闭运算：完整补证与原稿四块路线](#n-sec-10)
11. [十一、有限可加性与差集的有限性条件](#n-sec-11)
12. [十二、零测集、完备性与可测集合族的势](#n-sec-12)
13. [十三、内测度、开集外逼近与紧集内逼近](#n-sec-13)
14. [十四、不可测子集、并集问题与不可测集合族的势](#n-sec-14)
15. [十五、选择公理与 Solovay 模型旁注](#n-sec-15)
16. [十六、无穷维平移测度原问题及两个相关补证](#n-sec-16)

<!-- unit: N-SEC-01 -->
<a id="n-sec-01"></a>

## 一、测度公理与典型测度

<!-- unit: N-P001-001 -->
$σ$ 代数。

<!-- unit: N-P001-002 -->
$$\Sigma\subseteq\mathcal P(X).$$

<!-- unit: N-P001-002-S1 -->
> [!info] 补充：$σ$ 代数的定义
> 这里标题所指的是：$X\in\Sigma$；若 $A\in\Sigma$，则 $X\setminus A\in\Sigma$；若 $A_1,A_2,\ldots\in\Sigma$，则 $\bigcup_{i=1}^{\infty}A_i\in\Sigma$。原稿本页只写了 $\Sigma\subseteq\mathcal P(X)$，没有逐项重列这些封闭条件。

<!-- unit: N-P001-003 -->
$$m:\Sigma\longrightarrow\mathbb R^+.$$

<!-- unit: N-P001-003-S1 -->
> [!info] 补充：值域约定
> 为同时容纳本页的计数测度、后文的无穷外测度以及空集的零值，后续完整论证把值域解释为 $[0,+\infty]$。原稿写的是 $\mathbb R^+$；不能把它未经说明地理解为仅含严格正的有限实数。

<!-- unit: N-P001-004 -->
（1）$m(\varnothing)=0$。

<!-- unit: N-P001-005 -->
（2）$$m\!\left(\bigcup_{i=1}^{\infty}A_i\right)=\sum_i m(A_i).$$

<!-- unit: N-P001-006 -->
旁写条件：$A_i\cap A_j=\varnothing$。

<!-- unit: N-P001-006-S1 -->
> [!info] 补充：量词
> 上式要求 $A_i\in\Sigma$，且当 $i\ne j$ 时 $A_i\cap A_j=\varnothing$。原稿省略了 $i\ne j$；若也取 $i=j$，条件将错误地强制每个 $A_i$ 为空。

<!-- unit: N-P001-007 -->
Lebesgue：平移不变、正规性。

<!-- unit: N-P001-007-S1 -->
> [!info] 补充：术语范围
> 保留课堂用语“正规性”。本页没有给出该词定义，因此不把它静默替换成“归一化”或“正则性”的某一个特定版本。通常 Lebesgue 测度还满足单位方体体积为 $1$，并可由开集从外、紧集从内逼近；这些是不同性质。

<!-- unit: N-P001-008 -->
例：counting 测度。
$$E\longmapsto m(E)=|E|.$$

<!-- unit: N-P001-008-S1 -->
> [!info] 补充：计数的无穷值
> 当 $E$ 有限时 $m(E)$ 是元素个数；当 $E$ 无限时，实值测度记号下取 $m(E)=+\infty$，而不取某个无穷基数。若可列个集合互不相交，有限情形由计数相加得到；若并集无限，要么某一项已经无限，要么有无穷多个非空项，右侧均为 $+\infty$。

<!-- unit: N-P001-009 -->
Dirac 测度。
$$\delta:2^X\longrightarrow\mathbb R^+.$$

<!-- unit: N-P001-010 -->
$$\delta_x(E)=\begin{cases}1,&x\in E,\\0,&x\notin E.\end{cases}$$

<!-- unit: N-P001-010-S1 -->
> [!info] 补证：Dirac 测度的可列可加性
> 固定 $x\in X$。对互不相交的 $A_i$，$x$ 至多属于其中一个集合。若不属于任何一个集合，则并集及各项的 Dirac 测度全为 $0$；若属于某个 $A_k$，则并集的测度为 $1$，右侧恰有第 $k$ 项为 $1$。因此定义确实给出测度。

<!-- unit: N-SEC-02 -->
<a id="n-sec-02"></a>

## 二、基数记号与集合函数的数量

<!-- unit: N-P009-010 -->
**Def.** $A\cap B=\varnothing$，$\overline{\overline A}=\alpha$，$\overline{\overline B}=\beta$。

<!-- unit: N-P009-010-S1 -->
> [!info] 补充：双横线表示基数
> 这里 $\overline{\overline A}=|A|$ 表示集合的势，不是拓扑闭包。设 $\alpha=|A|$、$\beta=|B|$，以下三式定义基数的加法、乘法与幂。为定义加法可先取不交的带标记副本，故 $A\cap B=\varnothing$ 不限制可定义的两个基数。

<!-- unit: N-P009-011 -->
（1）$\overline{\overline{A\cup B}}=\alpha+\beta$。

<!-- unit: N-P009-012 -->
（2）$\alpha\cdot\beta=\overline{\overline{A\times B}}$。

<!-- unit: N-P009-013 -->
（3）$\alpha^\beta=\overline{\overline{A^B}}=\{f:B\to A\}$。

<!-- unit: N-P009-013-S1 -->
> [!info] 纠错：函数集与其基数
> 原稿把函数集合直接接在基数的等号之后。应分为 $A^B=\{f\mid f:B\to A\}$ 和 $\alpha^\beta=|A^B|$。例如幂集 $\mathcal P(B)$ 与 $\{0,1\}^B$ 由特征函数一一对应，所以 $|\mathcal P(B)|=2^{|B|}$。

<!-- unit: N-P001-011 -->
任意：$$2^{\mathbb R^n}\longrightarrow\mathbb R^+.$$

<!-- unit: N-P001-012 -->
$$\mathfrak c^{2^{\mathfrak c}}=(2^{\aleph_0})^{2^{\mathfrak c}}=2^{2^{\mathfrak c}}.$$

<!-- unit: N-P001-012-S1 -->
> [!info] 补充：基数算式说明
> 对有限的正整数 $n$，$|\mathbb R^n|=\mathfrak c$，故其幂集大小为 $2^{\mathfrak c}$。到一个大小为 $\mathfrak c$ 的值域的所有函数共有 $\mathfrak c^{2^{\mathfrak c}}$ 个。利用 $(\kappa^\lambda)^\mu=\kappa^{\lambda\mu}$ 以及 $\aleph_0\cdot2^{\mathfrak c}=2^{\mathfrak c}$，得到原式。此处只计算所有集合函数的数量，并没有断言这些函数全是测度。

<!-- unit: N-SEC-03 -->
<a id="n-sec-03"></a>

## 三、Jordan 内容、Darboux 判据与稠密有限覆盖

<!-- unit: N-P001-014 -->
Jordan 测度。（有限覆盖）

<!-- unit: N-P001-015 -->
$$U(f,P)=\sum_i\sup f\,\Delta x_i.$$

<!-- unit: N-P001-015-S1 -->
> [!info] 补充：上和的完整记号
> 对分割 $P:a=x_0<x_1<\cdots<x_N=b$，令 $I_i=[x_{i-1},x_i]$、$\Delta x_i=x_i-x_{i-1}$，则 $U(f,P)=\sum_{i=1}^N(\sup_{I_i}f)\Delta x_i$。原稿的 $\sup f$ 未在本行标出取上确界的区间。

<!-- unit: N-P001-016 -->
$$L(f,P)=\sum_i\inf f\,\Delta x_i.$$

<!-- unit: N-P001-016-S1 -->
> [!info] 补充：下和与 Jordan 内容
> 同一分割下 $L(f,P)=\sum_{i=1}^N(\inf_{I_i}f)\Delta x_i$。对有界集合的示性函数，上下和对应有限网格中外包与内含区间的总体积；Jordan 理论使用有限分割，后文 Lebesgue 外测度则允许可列覆盖。

<!-- unit: N-P002-001 -->
$$\sup_P U(f,P)=\inf_P L(f,P)\quad\Rightarrow\quad\text{Rm 可积}. $$

<!-- unit: N-P002-001-S1 -->
> [!info] 纠错：Darboux 判据中的上下确界
> 原稿把标准判据的 $\inf$ 与 $\sup$ 对调了。对于闭区间上的有界函数，正确的充要条件是
> $$\inf_P U(f,P)=\sup_P L(f,P).$$
> 左侧是上积分，右侧是下积分。对任意两个分割 $P,Q$，取共同加细 $R$ 得 $L(f,P)\le L(f,R)\le U(f,R)\le U(f,Q)$，故下积分不大于上积分；若相等，则可选分割分别使上、下和离共同值小于 $\varepsilon/2$，再共同加细，得到 $U-L<\varepsilon$。反过来，存在任意小的上、下和差时，二者的差只能为零。
>
> 原写的等式是过强的条件，仍能推出可积，但不能用作一般可积函数的判据。例如 $f(x)=x$ 在 $[0,1]$ 上可积，而单区间分割给出 $U=1,L=0$，所以 $\sup_PU=1\ne0=\inf_PL$。

<!-- unit: N-P002-002 -->
可以对应：内外测度。

<!-- unit: N-P002-003 -->
$E\subset\mathbb R^n$，则
$$E\text{ Jordan 可测}\iff m_J^*(\partial E)=0.$$

<!-- unit: N-P002-003-S1 -->
> [!info] 补充：有界性与判据说明
> Jordan 可测通常限定在有界集合。精确命题是：有界 $E\subset\mathbb R^n$ Jordan 可测，当且仅当其边界 $\partial E$ 的 Jordan 外内容为零。
>
> 取包含 $\overline E$ 的闭长方体 $R$。$E$ 的 Jordan 可测性等价于 $1_E$ 的上、下 Darboux 积分相等。网格中同时接触 $E$ 与 $E^c$ 的小长方体使 $1_E$ 的振幅为 $1$，其他小长方体使振幅为 $0$，因而上、下和之差就是这些混合小长方体体积的和。
>
> 若边界可被总体积任意小的有限个开长方体覆盖，由 $\partial E$ 的紧致性，可以选择足够细的网格，使每个接触边界的小长方体都留在这些开长方体的并中。混合小长方体必接触边界，故上、下和差任意小。
>
> 反过来，若上、下和差任意小，则混合小长方体覆盖除网格分割面外的全部边界。有限个网格分割面可用总体积任意小的薄长方体覆盖；再把混合小长方体略微扩大成开长方体，总体积仍可任意小。因此 $m_J^*(\partial E)=0$。

<!-- unit: N-P002-004 -->
原稿另写提示：$m_J^*:\ \displaystyle\int_a^b f(x)$。

<!-- unit: N-P002-004-S1 -->
> [!info] 补充：提示的规范含义
> 对有界 $E\subset[a,b]$，Jordan 外内容对应示性函数的上 Darboux 积分 $\overline{\int_a^b}1_E(x)\,dx$；内内容对应下积分。原稿此行未写被积函数应取 $1_E$、上下积分标记及 $dx$，这里补明对应关系。

<!-- unit: N-P002-005 -->
**Lemma.** 若 $S$ 在 $[0,1]$ 中稠密，且
$$S\cap[0,1]\subset\bigcup_{i=1}^{n}(a_i,b_i),$$

<!-- unit: N-P002-006 -->
则
$$[0,1]\subset\bigcup_{i=1}^{n}[a_i,b_i].$$

<!-- unit: N-P002-007 -->
Proof：内填外包。

<!-- unit: N-P002-007-S1 -->
> [!info] 补证：有限性的作用
> 因为 $S\cap[0,1]$ 在 $[0,1]$ 中稠密，$[0,1]\subseteq\overline{S\cap[0,1]}$。有限个闭区间的并是闭集，而
> $$S\cap[0,1]\subseteq\bigcup_{i=1}^n(a_i,b_i)\subseteq\bigcup_{i=1}^n[a_i,b_i].$$
> 对包含关系取闭包即可得到结论。这里不能把有限并未经检验换成可列并，因为可列个闭集的并不必闭。

<!-- unit: N-SEC-04 -->
<a id="n-sec-04"></a>

## 四、非负求和、Lebesgue 覆盖及两条存在性路线

<!-- unit: N-P002-008 -->
对无限集定义求和（网）。

<!-- unit: N-P002-008-S1 -->
> [!info] 补充：非负族的求和
> 对任意指标集 $I$ 上的非负数族 $(a_i)$，定义 $\sum_{i\in I}a_i=\sup\{\sum_{i\in F}a_i:F\subset I\text{ 有限}\}$。有限子集按包含关系构成有向集，这些有限部分和构成递增网。此说明只补足“网”的含义，不给原稿额外附加一个未写出的定理。

<!-- unit: N-P002-009 -->
**Def（1）** $E\subset\mathbb R^n$，有开区间 $(I_k)$，使得
$$E\subset\bigcup_{k=1}^{\infty}I_k,$$
则称一个 Lebesgue 覆盖。

<!-- unit: N-P002-009-S1 -->
> [!info] 补充：高维区间和覆盖族
> 在 $\mathbb R^n$ 中，“开区间”指有界开长方体 $I=\prod_{j=1}^n(a_j,b_j)$，$a_j<b_j$。将 $E$ 的全部可列此类覆盖组成的族记作 $LC(E)$；一个族中的元素本身是一列开长方体。

<!-- unit: N-P002-010 -->
1. $LC(E)\ne\varnothing$，$\forall E\subset\mathbb R^n$。

<!-- unit: N-P002-011 -->
$$I_\alpha=(a_1,b_1)\cdots(a_n,b_n),\qquad a_i,b_i\in\mathbb Z.$$

<!-- unit: N-P002-011-S1 -->
> [!info] 补充：可列性
> 只取 $a_i<b_i$。每个长方体由一个整数 $2n$ 元组确定，而 $\mathbb Z^{2n}$ 可列，因此全部这类开长方体可列。原稿的并集下标仅为简记，这里用 $\alpha$ 表示枚举指标。

<!-- unit: N-P002-012 -->
$$\mathbb R^n=\bigcup_\alpha I_\alpha.$$

<!-- unit: N-P002-013 -->
$\forall x\in(x_1,\ldots,x_n)$〔原笔为 ∈ 样弯笔；规范坐标等号见蓝色补充〕，
$$x\in\prod\bigl([x_1]-1,\ldots,[x_n]+1\bigr).$$
（此处保留原稿压缩的乘积记号。）

<!-- unit: N-P002-013-S1 -->
> [!info] 补全记号：逐坐标选取开区间
> $[x_j]$ 表示取整 $\lfloor x_j\rfloor$。准确地说，
> $$x\in\prod_{j=1}^{n}\bigl(\lfloor x_j\rfloor-1,\lfloor x_j\rfloor+1\bigr).$$
> 因为 $\lfloor x_j\rfloor\le x_j<\lfloor x_j\rfloor+1$，每个坐标都严格落在所选开区间内。所选端点为整数，故该长方体属于上述可列族。这样证明了它们覆盖 $\mathbb R^n$，也就覆盖任意 $E\subset\mathbb R^n$。

<!-- unit: N-P003-001 -->
或：$\mathbb R^n$ 是 Lindelöf，有遗传性。导出相应区间放大，来证明。

<!-- unit: N-P003-001-S1 -->
> [!info] 补证：保留的第二条覆盖路线
> 欧氏空间有可数拓扑基：端点为有理数的开长方体。任意子空间 $E\subset\mathbb R^n$ 也有由这些基元素与 $E$ 的交组成的可数基，所以 $E$ 的任意相对开覆盖有可列子覆盖。证明是：对每个包含于某个覆盖成员的基元素，选一个这样的覆盖成员；最多选可列多个，且覆盖全部 $E$。
>
> 对每个 $x\in E$ 先选一个包含 $x$ 的有界开长方体；上述性质给出可列子覆盖，于是 $LC(E)\ne\varnothing$。若从相对开集出发，可将它们写成环境开集与 $E$ 的交，再在环境开集中选小开长方体。这补全原稿的“相应区间”提示。
>
> 这里遗传性来自欧氏空间的第二可数性；一般 Lindelöf 空间的任意子空间未必 Lindelöf。

<!-- unit: N-P003-002 -->
2. $\overline{\overline{LC(E)}}$：所有覆盖的族，记为 $LC_E$。
〔$LC(E)$ 上方原有两条横笔；含义暂不强定。〕

<!-- unit: N-P003-003 -->
$\mathcal I=$“$\mathbb R^n$ 中全体开区间”，原稿简记其大小为 $\mathfrak c$，并写
$$\longrightarrow (\mathfrak c\times\cdots\times\mathfrak c),\qquad \mathfrak c^{\mathbb N}.$$

<!-- unit: N-P003-003-S1 -->
> [!info] 补充：基数与对象区分
> 一个开长方体由 $2n$ 个实数端点编码，因此 $|\mathcal I|\le\mathfrak c^{2n}=\mathfrak c$；仅改变一条边的一个端点已给出连续统多个不同长方体，故 $|\mathcal I|=\mathfrak c$。覆盖族 $LC(E)$ 是可列开长方体序列空间 $\mathcal I^{\mathbb N}$ 的子族。原稿用族本身代写基数，以下加绝对值以分清两者。

<!-- unit: N-P003-004 -->
$$\mathcal I^{\mathbb N}=\mathfrak c^{\mathbb N}=(2^{\aleph_0})^{\aleph_0}=\mathfrak c.$$

<!-- unit: N-P003-004-S1 -->
> [!info] 补充：规范算式
> 上式按基数理解为 $|\mathcal I^{\mathbb N}|=\mathfrak c^{\aleph_0}=2^{\aleph_0\cdot\aleph_0}=\mathfrak c$。因此全部可列覆盖构成一个集合，并且其基数不超过连续统。

<!-- unit: N-P003-005 -->
由（1）可取 $\{I_k\}\in LC(E)$。

<!-- unit: N-SEC-05 -->
<a id="n-sec-05"></a>

## 五、Lebesgue 外测度及可列次可加性

<!-- unit: N-P003-006 -->
$\{I_k\}$ 可覆盖。

**Def（2）** 定义
$$m^*:2^{\mathbb R^n}\longrightarrow[0,+\infty].$$

<!-- unit: N-P003-007 -->
$$E\longmapsto\inf\sum_{k=1}^{\infty}|I_k|,\qquad I_k\in LC_E.$$
约为外测度。

<!-- unit: N-P003-007-S1 -->
> [!info] 补全记号：Lebesgue 外测度
> $$m^*(E)=\inf_{(I_k)\in LC(E)}\sum_{k=1}^{\infty}|I_k|,\qquad |I_k|=\prod_{j=1}^n(b_{kj}-a_{kj}).$$
> 下确界遍历整个覆盖序列 $(I_k)$；原稿 $I_k\in LC_E$ 是省略族括号的写法。每项体积非负，允许总和为 $+\infty$。因为覆盖族非空，该定义给出 $[0,+\infty]$ 中的确定数值。

<!-- unit: N-P003-008 -->
**Remark**

（1）$I_n$ 可为 $\varnothing$。

<!-- unit: N-P003-008-S1 -->
> [!info] 补充：空项约定
> 约定 $|\varnothing|=0$，允许用空集补齐有限覆盖，使其成为可列序列。这里不要求每一个编号都对应非空长方体。

<!-- unit: N-P003-009 -->
（2）$I_n$ 是否可为〔疑字 RA07-Q002：字形候选“闭矩形”〕，可证明。Proof：

<span style="color:red">〔原稿提出覆盖对象是否可以替换的问题，所写 Proof 仅有下方起步条件，未完成结论。〕</span>

<!-- unit: N-P003-010 -->
$\forall\varepsilon$，$\forall\{B_i\}\in\overline{\mathcal B}$，
$$I\subset\bigcup_iB_i.$$

<!-- unit: N-P003-011 -->
$$\sum_i|B_i|<|I|+\varepsilon.$$

<!-- unit: N-P003-011-S1 -->
> [!info] 补证：以闭长方体替代开长方体的版本
> 原问题中形状的逐字读法尚待复核。以下完成候选“闭矩形”对应的命题，并保留上面的覆盖与体积控制路线。
>
> 记 $m_o^*$ 为开长方体覆盖定义的外测度，$m_c^*$ 为闭长方体覆盖定义的数值。任一开长方体可用自己的闭包覆盖，体积不变，所以 $m_c^*(E)\le m_o^*(E)$。反方向，给定闭长方体覆盖 $(B_i)$ 和 $\varepsilon>0$，逐个把边向外扩大，得到开长方体 $J_i\supset B_i$，并使 $|J_i|<|B_i|+\varepsilon2^{-i}$；这由有限乘积对边长的连续性保证。于是 $E\subset\bigcup_iJ_i$ 且 $\sum_i|J_i|\le\sum_i|B_i|+\varepsilon$，故 $m_o^*(E)\le m_c^*(E)+\varepsilon$。令 $\varepsilon\downarrow0$，得两种定义相同；若相应下确界为无穷，按上述不等式直接处理。
>
> 更一般地，只要两类基本覆盖对象能按原稿所示方式互相覆盖，并把总体积误差分配成 $\varepsilon2^{-i}$，就能以同一比较论证证明定义相同。

<!-- unit: N-P003-012 -->
### 外测度性质

（1）$m^*(\varnothing)=0$。

<!-- unit: N-P003-013 -->
（2）$E\subset F\ \Rightarrow\ m^*(E)\le m^*(F)$。

<!-- unit: N-P004-001 -->
（3）$\{E_k\}$：
$$m^*\!\left(\bigcup_kE_k\right)\le\sum_km^*(E_k).$$

<!-- unit: N-P004-002 -->
Proof：$\forall\varepsilon>0$，$\exists\{I_{k,j}\}\in LC(E_k)$（有限时）。

<!-- unit: N-P004-002-S1 -->
> [!info] 补充：有限与无穷分支
> 先补上两个初步性质的证明。空集可由全为空集的序列覆盖，总体积为零，故 $m^*(\varnothing)=0$。若 $E\subset F$，每个 $F$ 的覆盖也是 $E$ 的覆盖，即 $LC(F)\subseteq LC(E)$，下确界遂满足 $m^*(E)\le m^*(F)$。
>
> 对次可加性，若 $\sum_km^*(E_k)=+\infty$，待证不等式直接成立。否则每个 $m^*(E_k)<\infty$，因此能按下确界的定义选择下面的近最优覆盖。“有限时”应在这个总和有限的分支使用。

<!-- unit: N-P004-003 -->
$$E_k\subset\bigcup_{j=1}^{\infty}I_{k,j}.$$

<!-- unit: N-P004-004 -->
$$\sum_{j=1}^{\infty}|I_{k,j}|<m^*(E_k)+\frac{\varepsilon}{2^k}\qquad\text{（下确界）}.$$

<!-- unit: N-P004-005 -->
$$\bigcup_kE_k\subset\bigcup_{k=1}^{\infty}\bigcup_{j=1}^{\infty}I_{k,j}.$$

<!-- unit: N-P004-005-S1 -->
> [!info] 补充：可列覆盖仍合法
> $\mathbb N\times\mathbb N$ 是可列集，所以全部 $I_{k,j}$ 可以排成一个序列；这个序列属于 $LC(\bigcup_kE_k)$。此处只使用开长方体覆盖的定义，没有预先假设可列次可加性。

<!-- unit: N-P004-006 -->
$$m^*\!\left(\bigcup_{k=1}^{\infty}E_k\right)\le\sum_{(k,j)}|I_{k,j}|.$$
首个不等式下旁注：“下界”。

<!-- unit: N-P004-007 -->
$$\sum_{(k,j)}|I_{k,j}|<\sum_km^*(E_k)+\sum_{k=1}^{\infty}\frac{\varepsilon}{2k}.$$
〔原笔中此处分母 $k$ 与 $2$ 同基线；上文首次预算写为 $2^k$。〕

<!-- unit: N-P004-008 -->
Tonelli：可交换顺序。

$\varepsilon\to0$，取“$\le$”。

<!-- unit: N-P004-008-S1 -->
> [!info] 补证：非负双重和的换序及结论
> 对 $a_{k,j}=|I_{k,j}|\ge0$，把总和定义为所有有限指标子集部分和的上确界，则
> $$\sum_{(k,j)}a_{k,j}=\sum_k\sum_ja_{k,j}.$$
> 一方面每个有限指标子集只涉及有限个 $k$，其和不超过右侧；另一方面，任取有限个 $k$，各行和都可用有限部分和从下逼近，故这些行和的总和不超过左侧，再对有限个 $k$ 取上确界。这个初等非负求和论证就是此处调用 Tonelli 的具体内容。
>
> 因为 $\sum_{k=1}^{\infty}2^{-k}=1$，可得 $m^*(\bigcup_kE_k)\le\sum_km^*(E_k)+\varepsilon$。对任意 $\varepsilon>0$ 成立，遂得所列性质（3）。

<!-- unit: N-SEC-06 -->
<a id="n-sec-06"></a>

## 六、矩形体积、可数点集与 Cantor 集

<!-- unit: N-P005-001 -->
$I\subset\mathbb R^n$ 是有界区间，则 $m^*(I)=|I|$。

<!-- unit: N-P005-002 -->
若 $I$ 闭，则 $\forall\varepsilon>0$，$\exists I'$ 开，s.t.
$$|I'|<|I|+\varepsilon.$$

<!-- unit: N-P005-002-S1 -->
> [!info] 补证：有界长方体的外测度公式
> 上界：将 $\overline I$ 的每条边稍向外扩大，得到 $I'\supseteq I$，且体积小于 $|I|+\varepsilon$。故 $m^*(I)\le|I|$。原稿省写了包含关系，补为 $I\subset I'$。
>
> 下界先对闭长方体 $K$ 证明。任取可列开长方体覆盖 $(J_k)$，紧致性给出有限子覆盖 $J_{k_1},\ldots,J_{k_N}$。有限覆盖的体积满足 $|K|\le\sum_{r=1}^N|J_{k_r}|$：用 $K$ 和这些长方体的所有坐标端点作共同网格，每个落在 $K$ 内的小格内部均落在至少一个覆盖成员内，按格子体积相加即可；有限个分割面不贡献体积。于是 $|K|\le\sum_k|J_k|$，对覆盖取下确界得 $|K|\le m^*(K)$。
>
> 对任意开、闭或半开有界长方体 $I$，若体积为零，上界已经给出结论；若体积为正，在其内部取边长逐渐增大的闭长方体 $K_r$，使 $|K_r|\to|I|$。单调性给出 $m^*(I)\ge m^*(K_r)=|K_r|$，再令 $r\to\infty$。两侧合并，$m^*(I)=|I|$。

<!-- unit: N-P004-009 -->
**Prop.** $\{x_k\}\subset\mathbb R^n$，$m^*(\{x_k\})=0$。

<!-- unit: N-P004-009-S1 -->
> [!info] 补证：单点与可列点集
> 固定 $x\in\mathbb R^n$，用以 $x$ 为中心、边长 $2r$ 的开立方体覆盖它，得 $0\le m^*(\{x\})\le(2r)^n$。令 $r\downarrow0$ 得单点外测度为零。然后用可列次可加性：
> $$0\le m^*(\{x_k:k\ge1\})\le\sum_{k=1}^{\infty}m^*(\{x_k\})=0.$$

<!-- unit: N-P004-010 -->
**Cor.** $m^*(\mathbb Q\cap[0,1])=0$。

<!-- unit: N-P004-011 -->
Cantor：$C\subset[0,1]$。
$$C=\bigcap_{n=0}^{\infty}C_n.$$

<!-- unit: N-P004-011-S1 -->
> [!info] 补充：Cantor 构造与所需体积上界
> $C_0=[0,1]$，每一步从保留的每个闭区间中删去中间三分之一开区间。于是 $C_n$ 由 $2^n$ 个长度为 $3^{-n}$ 的闭区间组成。对任何有限个闭区间，可把它们略微扩大为开区间，总长度只增加任意给定的 $\eta>0$；因此其并的外测度不超过原总长度。此上界直接从外测度定义得到，不需要先调用有限可加性。

<!-- unit: N-P004-012 -->
$$m^*(C)\le m^*(C_n)=\left(\frac23\right)^n.$$

<!-- unit: N-P004-012-S1 -->
> [!info] 补充：此处只需不等式
> 原稿写了 $m^*(C_n)=(2/3)^n$，该等式由本节矩形体积公式和后面将证明的有限可加性得到。当前证明只需已说明的 $m^*(C_n)\le 2^n3^{-n}$。故对每个 $n$，$0\le m^*(C)\le(2/3)^n$；让 $n\to\infty$ 即得结论。

<!-- unit: N-P004-013 -->
$$m^*(C)=0.$$
旁注：“势是多少？”答：$\mathfrak c$。

<!-- unit: N-P004-013-S1 -->
> [!info] 补证：零外测度不等于可数
> 每个二进制序列 $(a_j)_{j\ge1}\in\{0,1\}^{\mathbb N}$ 给出 Cantor 点 $x=\sum_{j=1}^{\infty}2a_j3^{-j}$，因为其每一步都落在保留的闭区间中。若两个序列首次在第 $j$ 位不同，则主项差为 $2\cdot3^{-j}$，其后尾和差的绝对值至多 $3^{-j}$，所以所得两点不同。这给出 $\{0,1\}^{\mathbb N}$ 到 $C$ 的单射，故 $|C|\ge2^{\aleph_0}=\mathfrak c$；又 $C\subset\mathbb R$，故 $|C|=\mathfrak c$。

<!-- unit: N-SEC-07 -->
<a id="n-sec-07"></a>

## 七、Carathéodory 可测性与切分图

<!-- unit: N-P006-001 -->
Carathéodory。

<!-- unit: N-P006-002 -->
**Carathéodory 条件。** 设 $E\subset\mathbb R^n$。若对每个测试集合 $T\subset\mathbb R^n$，都有
$$m^*(T)=m^*(T\cap E)+m^*(T\cap E^c),$$
则称 $E$ 为 Lebesgue 可测集。

（测试字母原笔呈 T 样；定义行末项由本页后面的完整复写恢复。）

<!-- unit: N-P006-002-S1 -->
> [!info] 补充：测试集不限于区间
> 此处原稿继续沿用字母 $I$，但量词写的是任意子集 $I\subset\mathbb R^n$，不能只把它理解为前一节的长方体。为避免混淆，后面的补证也用 $A$ 表示任意测试集合。由于 $A=(A\cap E)\cup(A\cap E^c)$，次可加性总给出“$\le$”；验证可测性时只须证明反向“$\ge$”。

<!-- unit: N-P006-003 -->
则称 $E$ Lebesgue 可测，记 $m^*(E)=m_L(E)$。

〔下标按本行“Lebesgue”语境整理为 $L$；详见记号局部图。〕

<!-- unit: N-P006-003-S1 -->
> [!info] 补充：限制外测度
> 对可测集定义 $m(E)=m^*(E)$，得到 Lebesgue 测度；这里也保留原稿的 $m_L$ 记号。$\mathcal M$ 上的可列可加性将在后续可测集性质中证明，而不是由“定义”一词直接获得。

<!-- unit: N-P006-004 -->
记全体为 $\mathcal M$。

<!-- unit: N-P006-005 -->
原图：左上较小圆与右下较大圆相交，圆上方写 $E$；右下圆未写名称，没有阴影或箭头。

![原稿中的相交集合图](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/refs/heads/work/notes/work/notes-fc2ba28a26cd495f/notes/RA07/project/evidence/p0006-diagram.png)

<!-- unit: N-P006-005-S1 -->
> [!info] 补充：图与公式的对应
> 这幅图用于提示“一个测试集被 $E$ 切成内外两部分”。可以把另一圆视为测试集 $I$，其位于 $E$ 内的部分是 $I\cap E$，位于外面的部分是 $I\cap E^c$；这个名称对应是编者解释，原图没有给另一圆标字。

<!-- unit: N-P006-006 -->
一般：
$$m^*(T)=m^*(T\cap E)+m^*(T\cap E^c).$$
〔本页完整复写中的测试字母原笔呈 T 样。〕

<!-- unit: N-SEC-08 -->
<a id="n-sec-08"></a>

## 八、矩形测试与跨内外加性：完整原证明

<!-- unit: N-P007-001 -->
**Th.**
$$E\in\mathcal M\iff m^*(I)=m^*(I\cap E)+m^*(I\cap E^c),$$
$\forall I\subset\mathbb R$ 区间（矩形）。

<!-- unit: N-P007-001-S1 -->
> [!info] 补充：定理的精确范围
> 在 $\mathbb R^n$ 中，只对所有有界开矩形（开长方体）$I=\prod_{j=1}^n(a_j,b_j)$ 检查分割等式，就足以推出对任意测试集 $T\subset\mathbb R^n$ 的 Carathéodory 条件。原稿在条件行写 $\mathbb R$，并附“矩形”；以下覆盖证明对任意维数 $n$ 同样适用。必要性直接来自定义。

<!-- unit: N-P007-002 -->
〔左边缘另有被裁切的公式尾段，能读出 $E^c)$；没有足够图像恢复其前项。〕

<!-- unit: N-P007-003 -->
**pf.** $\Rightarrow$：显然。

<!-- unit: N-P007-004 -->
$\Leftarrow$：由外测度次可加性，仅证
$$m^*(I)\ge m^*(T\cap E)+m^*(T\cap E^c).$$
〔左端原笔为 I 样，右端两项为 T；数学规范补充见下方蓝色块。〕

<!-- unit: N-P007-004-S1 -->
> [!info] 补证：固定任意测试集
> 任取 $T\subset\mathbb R^n$。因为 $T=(T\cap E)\cup(T\cap E^c)$，次可加性已给出 $m^*(T)\le m^*(T\cap E)+m^*(T\cap E^c)$；所以下面只需得到相反方向，不能把 $T$ 预先假设为矩形。

<!-- unit: N-P007-005 -->
（1）若 $m^*(T)=+\infty$，成立。

<!-- unit: N-P007-005-S1 -->
> [!info] 补充：扩展实数的这一分支
> 当 $m^*(T)=+\infty$ 时，所需“$\ge$”自动成立；已有的“$\le$”又迫使右端也是 $+\infty$，因此得到等式。后面的取覆盖步骤是在 $m^*(T)<\infty$ 的分支中进行。

<!-- unit: N-P007-006 -->
（2）$\forall\varepsilon>0$，$\exists\{I_k\}\in LC(T)$，s.t.
$$\sum_{k=1}^{\infty}(I_k)<m^*(T)+\varepsilon.$$
〔原笔求和项两侧为圆括号样笔画；体积双竖线是蓝色数学说明。〕

<!-- unit: N-P007-007 -->
$$T\cap E\subset\bigcup_{k=1}^{\infty}(E\cap I_k).$$

<!-- unit: N-P007-008 -->
$$T\cap E^c\subset\bigcup_{k=1}^{\infty}(E^c\cap I_k).$$

<!-- unit: N-P007-009 -->
$$m^*(T\cap E)\le m^*\left(\bigcup_{k=1}^{\infty}(E\cap I_k)\right)
\le\sum_{k=1}^{\infty}m^*(E\cap I_k)<+\infty.$$

<!-- unit: N-P007-009-S1 -->
> [!info] 补证：最后一个严格界与补集对应式
> 每个 $E\cap I_k\subset I_k$，所以 $\sum_km^*(E\cap I_k)\le\sum_km^*(I_k)=\sum_k|I_k|<m^*(T)+\varepsilon<\infty$。同样，$m^*(T\cap E^c)\le\sum_km^*(E^c\cap I_k)<\infty$。这里使用了上一节“矩形的外测度等于体积”，没有先用待证的可测性。

<!-- unit: N-P007-010 -->
$$m^*(T\cap E)+m^*(T\cap E^c)
\le\sum_{k=1}^{\infty}m^*(E\cap I_k)+\sum_{k=1}^{\infty}m^*(E^c\cap I_k).$$

<!-- unit: N-P007-011 -->
（“题设”标在下一等号处。）
$$=\sum_{k=1}^{\infty}m^*(I_k)=\sum_{k=1}^{\infty}|I_k|<m^*(T)+\varepsilon.$$

<!-- unit: N-P007-011-S1 -->
> [!info] 补证：等号为何合法
> 非负级数可逐项相加，故两串和合成 $\sum_k[m^*(E\cap I_k)+m^*(E^c\cap I_k)]$。每个 $I_k$ 是题设允许检验的矩形，方括号内恰等于 $m^*(I_k)$。再用矩形体积定理与近最优覆盖估计，即得所需的 $\varepsilon$ 上界。

<!-- unit: N-P007-012 -->
$\varepsilon\to0^+$。

<!-- unit: N-P007-012-S1 -->
> [!info] 补证：收尾
> 左端 $m^*(T\cap E)+m^*(T\cap E^c)$ 与 $\varepsilon$ 无关；对每个 $\varepsilon>0$ 它都不超过 $m^*(T)+\varepsilon$，故令 $\varepsilon\downarrow0$ 得到反向不等式。与次可加性合并，任意 $T$ 都满足分割等式，所以 $E\in\mathcal M$。

<!-- unit: N-P007-013 -->
**Th.** $E\in\mathcal M\iff\forall A\subset E$，且 $B\subset E^c$，有
$$m^*(A\cup B)=m^*(A)+m^*(B).$$

<!-- unit: N-P007-013-S1 -->
> [!info] 补证：与定义双向等价
> 若 $E$ 可测，取测试集 $T=A\cup B$；由于 $A\subset E$、$B\subset E^c$，有 $T\cap E=A$、$T\cap E^c=B$，即得等式。反之，对任意 $T$ 取 $A=T\cap E$、$B=T\cap E^c$，题设恰给出 Carathéodory 等式。本页原稿只列定理，故此处将两步直接补全。

<!-- unit: N-P008-001 -->
$\Rightarrow$：令 $T=A\cup B$，则

<!-- unit: N-P008-002 -->
$$T\cap E=A.$$

<!-- unit: N-P008-003 -->
$$T\cap E^c=B.$$

<!-- unit: N-P008-004 -->
因 $E\in\mathcal M$，$m^*(T)=m^*(A)+m^*(B)$。

<!-- unit: N-P008-005 -->
$\Leftarrow$：任取 $T\subset\mathbb R^n$。

<!-- unit: N-P008-006 -->
令 $A=T\cap E$，$B=T\cap E^c$。

<!-- unit: N-P008-006-S1 -->
> [!info] 补证：原稿省略的最后代回
> 两集合满足 $A\subset E$、$B\subset E^c$，且 $A\cup B=T$。把它们代入前页所列的加性条件，得到 $m^*(T)=m^*(T\cap E)+m^*(T\cap E^c)$。由于 $T$ 任意，$E$ 可测。本页是前页定理的原稿证明，虽与编者前附的解释相同，仍按原有路线完整保留。

<!-- unit: N-P008-007 -->
注意：$A\cap B=\varnothing$，
$$m^*(A\cup B)\ne m^*(A)+m^*(B),$$
$A,B$ 可测成立。

<!-- unit: N-P008-007-S1 -->
> [!info] 纠错：原稿的不等号表示“不保证等号”
> 不能把此处 $\ne$ 理解为“任意两个不交集合都严格不等”；例如 $A=\varnothing$ 时必相等。准确说法是：仅知 $A\cap B=\varnothing$，不能推出外测度可加；若 $A,B$ 可测则等号成立。实际上只要其中一个可测，取 $T=A\cup B$ 使用它的 Carathéodory 条件就足够。
>
> 若存在不可测集 $E$，按定义存在测试集 $T$ 使分割等式失败。令 $A=T\cap E$、$B=T\cap E^c$，它们不交，而次可加性结合“不相等”给出 $m^*(A\cup B)<m^*(A)+m^*(B)$，这说明条件不能省掉。

<!-- unit: N-P006-014 -->
> [!info] 页边残笔（原图位置：第6页左缘）
> 可见一段右括号样弧线，约在 x=0–25、y=2475–2570；无法从残笔唯一恢复其配对或公式，故仅作来源记录，不解释为数学符号。

<!-- unit: N-SEC-09 -->
<a id="n-sec-09"></a>

## 九、正距离加性与闭集、紧集的分离

<!-- unit: N-P008-008 -->
若 $d(A,B)>0$，则上式成立。

<!-- unit: N-P008-008-S1 -->
> [!info] 补充：此处“上式成立”指等号成立
> 对 $d(A,B)=\inf\{|a-b|:a\in A,b\in B\}>0$，结论是
> $$m^*(A\cup B)=m^*(A)+m^*(B).$$
> 这是 Lebesgue 外测度的度量可加性，$A,B$ 均不必可测。原稿上一行写了 $\ne$，这里按上下文恢复成欲说明的加性结论，纠正单独标出。

<!-- unit: N-P008-008-S2 -->
> [!info] 补证：小直径覆盖给出度量可加性
> 设 $\delta=d(A,B)>0$。若 $m^*(A\cup B)=\infty$，次可加性已迫使两外测度的和为 $\infty$，等式成立。以下设有限。给定 $\varepsilon>0$，取 $A\cup B$ 的开矩形覆盖，其体积和小于 $m^*(A\cup B)+\varepsilon/2$。
>
> 可将覆盖中的第 $k$ 个有界矩形细分成有限个直径小于 $\delta/2$ 的闭小矩形；这些小矩形总体积等于原矩形体积，再各自微量放大成直径小于 $\delta$ 的开矩形，使第 $k$ 组新增总体积小于 $\varepsilon/2^{k+1}$。这样得到全部直径小于 $\delta$、总体积小于 $m^*(A\cup B)+\varepsilon$ 的可数开覆盖。
>
> 每个小矩形不可能同时碰到 $A$ 与 $B$，否则其中两点距离小于 $\delta$。把相交于 $A$ 的矩形和相交于 $B$ 的矩形分为互不重叠的两组，分别覆盖 $A,B$；完全不相交的矩形可弃去。因此
> $$m^*(A)+m^*(B)\le\sum_{I\text{ 属于两组}}|I|<m^*(A\cup B)+\varepsilon.$$
> 令 $\varepsilon\downarrow0$，再结合次可加性，等式得证。这里分的是覆盖的指标组，并未假定覆盖矩形彼此不交。

<!-- unit: N-P008-009 -->
$$A\cap B=\varnothing\quad(A\text{ 闭，}\ B\text{ 紧})\ \Rightarrow\ d(A,B)>0.$$

<!-- unit: N-P008-010 -->
**Proof：**

<span style="color:red">〔原稿待填：该 Proof 标题后未写证明；下一物理页已转入零测集等新主题。〕</span>

<!-- unit: N-P008-010-S1 -->
> [!info] 补证：闭集与紧集的正距离
> 若其中一个集合为空，按 $\inf\varnothing=\infty$ 结论成立。否则，对每个 $b\in B$，因为 $A$ 闭且 $b\notin A$，存在 $r_b>0$ 使 $B(b,r_b)\cap A=\varnothing$，故 $d(b,A)>0$。函数 $b\mapsto d(b,A)$ 为 $1$-Lipschitz：由三角不等式有 $d(b,A)\le|b-b'|+d(b',A)$，交换 $b,b'$ 即得绝对值估计。它在非空紧集 $B$ 上取得最小值；取得该值的点也不在 $A$，故最小值严格正，即 $d(A,B)>0$。
>
> 紧性不可随意去掉：$A=\{n:n\ge1\}$ 与 $B=\{n+1/(n+1):n\ge1\}$ 都是 $\mathbb R$ 中的闭集且不交，但两者距离为 $0$。

<!-- unit: N-SEC-10 -->
<a id="n-sec-10"></a>

## 十、可测族封闭运算：完整补证与原稿四块路线

<!-- unit: N-P009-001 -->
（1）$\varnothing\in\mathcal M$，$\mathbb R^n\in\mathcal M$。

<!-- unit: N-P009-001-S1 -->
> [!info] 补证：空集与全空间
> 对任意测试集 $T$，用 $\varnothing$ 切分时得到 $\varnothing$ 与 $T$，用 $\mathbb R^n$ 切分时得到 $T$ 与 $\varnothing$。因为 $m^*(\varnothing)=0$，两次都满足定义中的等式。

<!-- unit: N-P009-002 -->
（2）不可测，可测。

<!-- unit: N-P009-002-S1 -->
> [!info] 补充：提纲式原文
> 本行只有“不可测，可测”两个词，没有写关系或完整命题，故按提纲片段保留；后面关于封闭运算的完整表述另补如下。

<!-- unit: N-P009-003 -->
（3）并、交、补，上下极限。

<!-- unit: N-P009-003-S1 -->
> [!info] 补充：可测集族的封闭运算
> 精确命题是：$\mathcal M$ 对补、可数并、可数交封闭，从而对可测集列的上极限、下极限也封闭。任意不可数并、交一般不能由这条命题推出。下面给出全部步骤，原稿此处仅列关键词。

<!-- unit: N-P009-003-S2 -->
> [!info] 补证：补与有限运算
> 若 $E$ 可测，把分割等式中的 $E,E^c$ 交换即知 $E^c$ 可测。若 $E,F$ 可测，对任意 $T$ 先用 $E$ 分割，再用 $F$ 分割 $T\cap E$，得到
> $$m^*(T)=m^*(T\cap E\cap F)+m^*(T\cap E\cap F^c)+m^*(T\cap E^c).$$
> 因为后两块并成 $T\cap(E\cap F)^c$，次可加性使上式右端不小于 $m^*(T\cap E\cap F)+m^*(T\cap(E\cap F)^c)$。再结合通常的相反不等式，即得 $E\cap F$ 可测。由 De Morgan 律，有限并和差集也可测。整个推导没有作 $\infty-\infty$。

<!-- unit: N-P009-003-S3 -->
> [!info] 补证：可数并与可数可加性
> 先设 $E_k$ 两两不交且可测，令 $E=\bigcup_{k\ge1}E_k$、$F_N=\bigcup_{k=1}^NE_k$。反复使用有限次分割等式，并用 $T\setminus E\subset T\setminus F_N$，得
> $$m^*(T)=\sum_{k=1}^Nm^*(T\cap E_k)+m^*(T\setminus F_N)
> \ge\sum_{k=1}^Nm^*(T\cap E_k)+m^*(T\setminus E).$$
> 对非负部分和取上确界，结合 $m^*(T\cap E)\le\sum_{k\ge1}m^*(T\cap E_k)$，得到 $m^*(T)\ge m^*(T\cap E)+m^*(T\setminus E)$。次可加性给另一方向，所以 $E$ 可测。一般可测集列 $A_k$ 可改写成不交列 $E_1=A_1$、$E_k=A_k\setminus\bigcup_{j<k}A_j$，并集不变，故可数并封闭；可数交再由补和 De Morgan 律得到。
>
> 在两两不交的情形中取 $T=E$，上述有限部分和估计给出 $m(E)\ge\sum_km(E_k)$；次可加性给反向，故 $m(E)=\sum_km(E_k)$。这同时证明 $m=m^*|_{\mathcal M}$ 是测度。

<!-- unit: N-P009-003-S4 -->
> [!info] 补证：上下极限
> 对集合列 $E_k$，
> $$\limsup_{k\to\infty}E_k=\bigcap_{N=1}^{\infty}\bigcup_{k\ge N}E_k,\qquad
> \liminf_{k\to\infty}E_k=\bigcup_{N=1}^{\infty}\bigcap_{k\ge N}E_k.$$
> 前者由“无穷多次属于”这些集合的点组成，后者由“从某项起每次属于”的点组成。两式都只用可数并交，因此当各 $E_k$ 可测时，上下极限可测。

<!-- unit: N-P010-010 -->
运算性质。

<!-- unit: N-P010-011 -->
（1）$A,B\in\mathcal M$，$A\cup B\in\mathcal M$。

<!-- unit: N-P011-001 -->
$\forall T\subset\mathbb R^n$。

<!-- unit: N-P011-002 -->
$$m^*(T)\ge m^*(T\cap(A\cup B))+m^*(T\cap A\cup B^c).$$

<!-- unit: N-P011-002-S1 -->
> [!info] 纠错：补集的括号范围
> 这一行承接前页 $A,B$ 可测、欲证 $A\cup B$ 可测。末项原写没有给 $A\cup B$ 加成对括号，若按通常运算优先次序读成 $m^*((T\cap A)\cup B^c)$，便不是所需命题。正确目标应写为
> $$m^*(T)\ge m^*(T\cap(A\cup B))+m^*(T\cap(A\cup B)^c).$$
> 其相反不等式总由次可加性成立。以下分块证明的是这个补全括号后的目标。

<!-- unit: N-P011-003 -->
原图：三个相交圆分别标 $A$、$B$、$T$；$T$ 圆较大，位于下方。其内部写 1、2、3、4，分别落在仅与 $A$ 相交、三圆公共、仅与 $B$ 相交、与 $A,B$ 都不交的部分。

![原稿三圆四区域图](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/refs/heads/work/notes/work/notes-fc2ba28a26cd495f/notes/RA07/project/evidence/p0011-diagram.png)

<!-- unit: N-P011-003-S1 -->
> [!info] 补充：图中编号的集合表达
> 令 $D_1=T\cap A\cap B^c$、$D_2=T\cap A\cap B$、$D_3=T\cap A^c\cap B$、$D_4=T\cap A^c\cap B^c$。四块两两不交且并为 $T$；其中 $D_1\cup D_2\cup D_3=T\cap(A\cup B)$，$D_4=T\cap(A\cup B)^c$。这是把图上编号翻译成公式，原图没有给四块另写 $D_i$ 名字。

<!-- unit: N-P011-004 -->
$(T\cap A\cap B)\cup(T\cap A\cap B^c)\cup(T\cap B\cap A^c)$

<!-- unit: N-P011-005 -->
$=T\cap(A\cup B)$。

<!-- unit: N-P011-006 -->
则取外测度。

<!-- unit: N-P011-007 -->
$$m^*(T\cap A\cap B^c)+m^*(T\cap A\cap B)=m^*(T\cap A).$$

<!-- unit: N-P011-007-S1 -->
> [!info] 补证：该等号的依据
> 将测试集 $T\cap A$ 代入 $B$ 的可测性条件，即得本行等式。它在图上对应 $m^*(D_1)+m^*(D_2)=m^*(T\cap A)$；此时 $T\cap A$ 本身无需预先被判为可测。

<!-- unit: N-P011-008 -->
〔Q004：公式前的三个衔接字〕
$$m^*(T\cap A)+m^*(T\cap A^c)=m^*(T).$$

<!-- unit: N-P011-008-S1 -->
> [!info] 补证：补齐第三、第四块后完成有限并证明
> 还应把 $T\cap A^c$ 作为测试集代入 $B$ 的可测性，得到 $m^*(D_3)+m^*(D_4)=m^*(T\cap A^c)$。再与原稿已写的两式合并，
> $$\sum_{i=1}^{4}m^*(D_i)=m^*(T\cap A)+m^*(T\cap A^c)=m^*(T).$$
> 次可加性给 $m^*(D_1\cup D_2\cup D_3)\le\sum_{i=1}^{3}m^*(D_i)$，故
> $$m^*(T\cap(A\cup B))+m^*(T\cap(A\cup B)^c)\le\sum_{i=1}^{4}m^*(D_i)=m^*(T).$$
> 与开头的一般反向界合并，即证 $A\cup B$ 可测。这条四块路线与前面的有限交路线均保留。衔接语 Q004 不影响两条完整原公式的含义。

<!-- unit: N-P011-009 -->
**Prop.** $S$ 可测，$S^c$ 可测。

<!-- unit: N-P011-010 -->
$$m^*(T\cap S)+m^*(T\cap S^c)
\overset{\text{性质}}{=}m^*(T\cap S^{cc})+m^*(T\cap S^c).$$

〔原稿右边在 $S$ 上连写两个补集符号。〕

<!-- unit: N-P011-010-S1 -->
> [!info] 补证：改写成补集的定义式
> $S^{cc}=(S^c)^c=S$，而 $S$ 可测使本行两边都等于 $m^*(T)$。交换右边两项即可写成 $m^*(T\cap S^c)+m^*(T\cap(S^c)^c)=m^*(T)$，这对每个 $T$ 成立，故 $S^c$ 可测。

<!-- unit: N-P011-011 -->
$A,B$ 可测，$A\cap B$ 可测。

<!-- unit: N-P011-011-S1 -->
> [!info] 补证：用已证的并与补
> 由 $A^c,B^c$ 可测以及有限并封闭知 $A^c\cup B^c$ 可测，再取补得 $(A^c\cup B^c)^c=A\cap B$ 可测。它与前面直接切分测试集证明有限交的路线等价。

<!-- unit: N-SEC-11 -->
<a id="n-sec-11"></a>

## 十一、有限可加性与差集的有限性条件

<!-- unit: N-P011-012 -->
**Prop.** $A,B\in\mathcal M$，$A\cap B=\varnothing$。

<!-- unit: N-P011-013 -->
$$m(A\cup B)=m(A)+m(B).$$

<!-- unit: N-P011-013-S1 -->
> [!info] 补证：不交有限可加
> 用 $A$ 的可测性测试 $T=A\cup B$，有 $T\cap A=A$、$T\cap A^c=B$，从而 $m^*(A\cup B)=m^*(A)+m^*(B)$。三者都可测，故可以将 $m^*$ 写为 $m$。多于两个集合的有限不交可加性由归纳得到，且允许各项等于 $\infty$。

<!-- unit: N-P012-001 -->
$B\subset A^c$。

<!-- unit: N-P012-001-S1 -->
> [!info] 补充：与上一命题的接续
> 这一行承接上一页 $A\cap B=\varnothing$，二者等价。取测试集 $T=A\cup B$ 时，正因为 $B\subset A^c$ 才有 $T\cap A^c=B$。下方改讨论 $B\subset A$ 的差集命题，不能把两种包含关系误合成同一组假设。

<!-- unit: N-P012-002 -->
$A,B\in\mathcal M$，$B\subseteq A$。

<!-- unit: N-P012-003 -->
$m(B)<\infty$。

<!-- unit: N-P012-004 -->
$$m(A\setminus B)=m(A)-m(B).$$

<!-- unit: N-P012-004-S1 -->
> [!info] 补证：为什么只需被减项有限
> 因 $A\setminus B=A\cap B^c$ 可测，且 $A=B\,\dot\cup\,(A\setminus B)$，有限可加性给
> $$m(A)=m(B)+m(A\setminus B).$$
> 若 $m(A)<\infty$，从这个实数等式减去有限的 $m(B)$ 即得公式；若 $m(A)=\infty$ 而 $m(B)<\infty$，则上式迫使 $m(A\setminus B)=\infty$，也与 $\infty-m(B)=\infty$ 一致。
>
> 有限条件不能删去后仍写减法。例如 $A=B=\mathbb R$ 时差集为 $\varnothing$、测度为 $0$，而 $m(A)-m(B)=\infty-\infty$ 没有定义。总能使用的是不含减法的等式 $m(A)=m(B)+m(A\setminus B)$。

<!-- unit: N-SEC-12 -->
<a id="n-sec-12"></a>

## 十二、零测集、完备性与可测集合族的势

<!-- unit: N-P009-004 -->
**Def.** 外测度为 $0$ 之集，称为零测集。

<!-- unit: N-P009-005 -->
**Prop.** 零测集必可测。

<!-- unit: N-P009-006 -->
$$0\le m^*(T\cap E)\le m^*(E)=0.$$

<!-- unit: N-P009-007 -->
因 $m^*(T)\ge m^*(T\cap E)$。

<!-- unit: N-P009-007-S1 -->
> [!info] 纠错及补证：第二行还需补集部分
> 原稿第二行末项确写 $T\cap E$，没有可辨的补集上标。该不等式虽真，只能说明 $m^*(T)\ge0$，尚不足以得到分割等式。正确收尾是由单调性
> $$m^*(T)\ge m^*(T\cap E^c)=m^*(T\cap E)+m^*(T\cap E^c),$$
> 其中最后一步用已证的 $m^*(T\cap E)=0$。再由次可加性得到相反不等式，故 $E$ 可测。对 $m^*(T)=\infty$ 仍合法，因为没有作减法。

<!-- unit: N-P009-008 -->
（2）零测集子集是零测集。

<!-- unit: N-P009-008-S1 -->
> [!info] 补证：完备性
> 若 $A\subset E$ 且 $m^*(E)=0$，单调性给出 $0\le m^*(A)\le0$，所以 $A$ 也是零测集；上一命题又说明 $A$ 可测。Lebesgue 测度因而是完备测度，即每个可测零测集的任意子集仍可测。

<!-- unit: N-P009-009 -->
（3）至多个可数个零测集并是零测集。

<!-- unit: N-P009-009-S1 -->
> [!info] 补证：可数并
> 把“至多个可数个”整理为“至多可数个”。若 $m^*(E_k)=0$，则 $0\le m^*(\bigcup_kE_k)\le\sum_km^*(E_k)=0$。有限并可补上空集成为可数列；空并也是空集。不可数并不能照此推出，例如所有单点的并可为整个 $[0,1]$。

<!-- unit: N-P009-014 -->
$$\overline{\overline{2^c}}\le\overline{\overline{\mathcal M}}\le2^c.$$
〔左端 $2$ 上方原有两条短横；上标 C/c 形仍按原笔保留。〕

<!-- unit: N-P009-015 -->
Cantor（上方标 $c$）：任意子集可测，$2^c$。

<!-- unit: N-P009-015-S1 -->
> [!info] 补证：为什么可测集族有 $2^c$ 个元素
> 三分 Cantor 集 $C$ 的外测度是 $0$、势为 $c$，前面已分别证明。因此 $\mathcal P(C)\subset\mathcal M$，而 $|\mathcal P(C)|=2^c$，给出下界。另一方面 $\mathcal M\subset\mathcal P(\mathbb R^n)$，且有限维欧氏空间的势为 $c$，故 $|\mathcal M|\le2^c$。由两边夹逼，$|\mathcal M|=2^c$。
>
> 这里说的是“可测集本身所组成的集合族”有多大；并不表示每个可测集都具有相同的势，也不把所有 $\mathbb R^n$ 的子集都判为可测。

<!-- unit: N-SEC-13 -->
<a id="n-sec-13"></a>

## 十三、内测度、开集外逼近与紧集内逼近

<!-- unit: N-P005-004 -->
### 可测集

引入：$E\subset\mathbb R^n$。

<!-- unit: N-P005-004-S1 -->
> [!info] 补证：本节先备的开集、闭集可测性
> 先用矩形测试判据证明半空间 $H=\{x:x_j<a\}$ 可测：任意有界开矩形 $J$ 被超平面 $x_j=a$ 切成两个矩形（允许空或退化），两部分的外测度等于其体积，而体积之和是 $|J|$。所以 $H$ 满足矩形测试条件。闭半空间为其补，亦可测。
>
> 对于 $\{x:x_j>a\}$ 同样以切矩形证明可测；有界开矩形是这两类开半空间的有限交，故可测。每个开集 $G\subset\mathbb R^n$ 都等于包含于它的有理端点开矩形之并：对 $x\in G$ 先取小球包含于 $G$，再在球内围绕 $x$ 选有理端点矩形；全部有理端点矩形只有可数个。因此开集可测，闭集作为开集的补也可测，特别地紧集可测。这些结论只用前面已证的矩形外测度公式、矩形判据与可数并交封闭。

<!-- unit: N-P005-005 -->
取 $G$ 开，$G\supset I\setminus E$。

<!-- unit: N-P005-005-S1 -->
> [!info] 补证：外测度的开集外逼近
> 对任意 $S\subset\mathbb R^n$，有
> $$m^*(S)=\inf\{m(G):S\subset G,\ G\text{ 开}\}.$$
> 单调性给出左端不超过每个候选 $m(G)$。若 $m^*(S)<\infty$，取开矩形覆盖使总体积小于 $m^*(S)+\varepsilon$，令 $G$ 为这些矩形的并，则 $S\subset G$，且 $G$ 开、可测，$m(G)\le\sum_k|I_k|<m^*(S)+\varepsilon$。令 $\varepsilon\downarrow0$ 得反向。若 $m^*(S)=\infty$，每个含它的开集也有无限测度，公式仍成立。
>
> 因而原稿这里的 $G$ 不仅可以取开覆盖，也可使其测度尽量接近 $m^*(I\setminus E)$。

<!-- unit: N-P005-006 -->
$I\setminus G\subset E$ 中紧集。

<!-- unit: N-P005-006-S1 -->
> [!info] 补充：紧性所需条件
> 此处应先假设 $E$ 有界，并取包含 $E$ 的闭有界长方体 $I$。因为 $G$ 开，$I\setminus G$ 是紧集；由 $G\supset I\setminus E$ 得 $I\setminus G\subset E$。原稿在引入行没有重新写这些条件。

<!-- unit: N-P005-007 -->
旁写：$|I|-|I\,/\,G|$。
〔第二项中 $I$ 后为单斜杠样笔画，差集/交集读法未决；不是单独的 $|G|$。〕

<!-- unit: N-P005-007-S1 -->
> [!info] 补充：孤立差式的两种字形解释
> 原笔第二项不是单独的 $|G|$，而是在 $G$ 前出现 $I$ 样笔画及斜杠。若将其读作差集 $I\setminus G$，则在 $I$ 有限可测、$G$ 开时
> $$m(I\setminus G)=|I|-m(I\cap G).$$
> 若局部斜杠实际意在表示交集，也只能在补全该交号后得到相应的交集公式；原图没有足够拱顶笔画让两者唯一。无论哪一候选，都不能把原笔静默改写成 $|I|-|G|$。

<!-- unit: N-P005-008 -->
令 $$m_*(E)=|I|-m^*(I\setminus E).$$

<!-- unit: N-P005-008-S1 -->
> [!info] 补证：内测度等于紧集内逼近，因而与外框无关
> 设 $E$ 有界，固定闭长方体 $I\supset E$。定义式中的两项有限，且 $0\le m^*(I\setminus E)\le|I|$。我们证明
> $$m_*(E)=\sup\{m(K):K\subset E,\ K\text{ 紧}\}.$$
> 若 $K\subset E$ 紧，则 $I\setminus E\subset I\setminus K$，单调性及有限差公式给 $m^*(I\setminus E)\le |I|-m(K)$，故 $m(K)\le m_*(E)$。
>
> 反向，给定 $\varepsilon>0$，按开集外逼近取 $G\supset I\setminus E$，使 $m(G)<m^*(I\setminus E)+\varepsilon$。则 $K=I\setminus G$ 是 $E$ 中紧集，且
> $$m(K)=|I|-m(I\cap G)\ge |I|-m(G)>m_*(E)-\varepsilon.$$
> 因而上确界不小于 $m_*(E)$，公式得证。右侧不提外框 $I$，所以定义与所选包含 $E$ 的闭长方体无关。又由各 $K\subset E$ 的单调性，$m_*(E)\le m^*(E)$。

<!-- unit: N-P005-009 -->
若 $m_*(E)=m^*(E)$，则 $E$ 可测。

<!-- unit: N-P005-009-S1 -->
> [!info] 补证：有界集合的内外测度判据与 Carathéodory 定义等价
> 若 $E$ 可测，则 $I\setminus E$ 也可测，有限可加性给 $|I|=m(E)+m(I\setminus E)$，所以 $m_*(E)=m(E)=m^*(E)$。
>
> 反之设 $m_*(E)=m^*(E)=s$，其中 $s<\infty$。由紧集内逼近，对每个 $j\ge1$ 取紧集 $K_j\subset E$，使 $m(K_j)>s-1/j$。令 $K=\bigcup_jK_j$，则 $K$ 可测且包含于 $E$。将任意 $K_j$ 的可测性用于测试集 $E$，有
> $$s=m^*(E)=m(K_j)+m^*(E\setminus K_j),$$
> 故 $m^*(E\setminus K)\le m^*(E\setminus K_j)<1/j$。令 $j\to\infty$，得到 $E\setminus K$ 零测，因完备性可测。于是 $E=K\cup(E\setminus K)$ 可测。取 $s=0$ 时同样成立，可取空紧集；没有遗漏零测情形。

<!-- unit: N-P005-010 -->
$$|I|=m^*(I\cap E^c)+m^*(E).$$

<!-- unit: N-P005-011 -->
$$|I|=m^*(I\cap E^c)+m^*(E\cap I).$$

<!-- unit: N-P005-012 -->
$\forall I$ 均成立。

<!-- unit: N-P005-012-S1 -->
> [!info] 补充：两行恒等式的量词
> 当 $E\subset I$ 时，$E\cap I=E$，所以上面的两种写法相同。对于不一定包含 $E$ 的测试长方体 $I$，应使用第二种写法：$|I|=m^*(I\cap E)+m^*(I\cap E^c)$。本复习稿前面已给出对任意测试集合 $A$ 的分割条件；原稿下一物理页从这一引入过渡到该定义。

<!-- unit: N-P005-013 -->
$E$ 有界：$m^*(E)=m_*(E)$。

<!-- unit: N-P005-014 -->
无界：$E\cap I$ 可测。

<!-- unit: N-P005-014-S1 -->
> [!info] 补充：无界时的量词与定义
> 对无界集合，原稿的局部说法应理解为：对每个有界长方体 $I$，$E\cap I$ 可测。也可以只检查一列覆盖全空间的有界闭长方体 $[-N,N]^n$。这样避免在 $m_*(E)$ 中使用没有定义的 $+\infty-(+\infty)$。等价的统一定义是本复习稿前面已给出的 Carathéodory 条件。

<!-- unit: N-P005-014-S2 -->
> [!info] 补证：局部判据的双向推导
> 若 $E$ 可测，则对每个有界闭长方体 $I$，交集 $E\cap I$ 可测。反之，若每个 $E\cap[-N,N]^n$ 可测，则
> $$E=\bigcup_{N=1}^{\infty}\bigl(E\cap[-N,N]^n\bigr)$$
> 是可数个可测集之并，故可测。因而原稿的无界局部描述与统一的 Carathéodory 定义一致。

<!-- unit: N-SEC-14 -->
<a id="n-sec-14"></a>

## 十四、不可测子集、并集问题与不可测集合族的势

<!-- unit: N-P005-003 -->
任意测度 $>0$ 的〔集〕存在不可测子集。

<!-- unit: N-P005-003-S1 -->
> [!info] 补充：旁注的精确范围
> 这是关于 Lebesgue 测度（在选择公理下）的陈述，不能把“任意测度”误读为任意测度空间中的任意测度。例如定义在全部子集上的计数测度不存在不可测子集。完整构造在复习稿后面的“不可测子集”补证中给出；原稿此处只有这一行旁注。

<!-- unit: N-P010-009 -->
凡测度 $>0$ 之集，必 $\exists$ 不可测子集。

<!-- unit: N-P010-009-S1 -->
> [!info] 补充：命题的范围与平移引理
> 这里的测度指 Lebesgue 测度，构造使用选择公理。实际上若 $E\subset\mathbb R^n$ 满足 $m^*(E)>0$，即使尚未知道 $E$ 可测，也含有不可测子集。
>
> 先补本构造及上一基数论证使用的平移性质：将覆盖 $E$ 的每个开矩形平移向量 $t$，总体积不变，得到 $m^*(E+t)\le m^*(E)$；再平移 $-t$ 得反向，所以 $m^*(E+t)=m^*(E)$。若 $E$ 可测，把任意 $T-t$ 代入其分割等式，并将两部分平移 $t$，可得 $E+t$ 的分割等式。因此可测性和平移后的测度都保持。

<!-- unit: N-P010-009-S2 -->
> [!info] 补证：不可测子集的完整构造
> 取整数 $N\ge1$ 使 $F=E\cap[-N,N]^n$ 满足 $m^*(F)>0$。这样的 $N$ 必存在；否则 $E$ 是一列零外测度集合的并，次可加性将给出 $m^*(E)=0$。
>
> 在 $F$ 上定义 $x\sim y\iff x-y\in\mathbb Q^n$。用选择公理从每个等价类中选一点，组成 $V\subset F$。设 $D=\mathbb Q^n\cap[-2N,2N]^n$，则 $D$ 为可数无限集，且
> $$F\subset\bigcup_{q\in D}(V+q)\subset[-3N,3N]^n.$$
> 第一包含因为每个 $x\in F$ 与所选代表 $v\in F$ 相差一个属于 $D$ 的有理向量，第二包含来自坐标界。
>
> 这些平移两两不交：若 $v_1+q_1=v_2+q_2$，则 $v_1-v_2\in\mathbb Q^n$，代表选择迫使 $v_1=v_2$，继而 $q_1=q_2$。若 $V$ 可测，则各 $V+q$ 可测且测度同为 $a=m(V)$。如果 $a=0$，可数次可加性与第一包含给出 $m^*(F)=0$，矛盾；如果 $a>0$，任取 $D$ 中 $K$ 个不同向量，有限可加性及第二包含给出 $Ka\le m^*([-3N,3N]^n)=(6N)^n$，让 $K$ 任意大又矛盾。因此 $V$ 不可测。
>
> 取 $E=[0,1]$ 即给出前面问题所需的 Vitali 型例子；取任意正外测度 $E$ 则给出本页和第 5 页旁注的结论。

<!-- unit: N-P010-001 -->
**问题 1（原稿）。** $A,B$ 不可测，是否推出 $A\cup B$ 不可测？

<span style="color:red">〔原稿提问处未写一般情形答案。〕</span>

<!-- unit: N-P010-001-S1 -->
> [!info] 补充：答案与反例
> 不推出。取一个不可测集 $V\subset\mathbb R$，令 $A=V$、$B=V^c$。若 $V^c$ 可测，则其补集 $V$ 也可测，矛盾；所以两者均不可测，但 $A\cup B=\mathbb R$ 可测。另一方面令 $A=B=V$，并集仍不可测，说明一般情况下两种结果都可能。

<!-- unit: N-P010-002 -->
**问题 2（原稿）。** $A$ 可测、$B$ 不可测，$A\cup B$ 是否不可测？

<span style="color:red">〔原稿以 Q 引出，后面只讨论附加条件与推导路线。〕</span>

<!-- unit: N-P010-002-S1 -->
> [!info] 补充：一般结论仍不成立
> 令 $A=\mathbb R$、$B=V$ 为不可测集，则并为可测的 $\mathbb R$；令 $A=\varnothing$ 则并为不可测的 $V$。正确的判断要看 $B$ 在 $A$ 之外的部分，下面保留原稿路线并修正差集方向。

<!-- unit: N-P010-003 -->
$$A\cup V=A\cup(A\setminus V).$$

<!-- unit: N-P010-003-S1 -->
> [!info] 纠错：差集方向写反
> 原式右端恒等于 $A$，一般不等于左端；取 $A=\varnothing$、$V\ne\varnothing$ 即得到反例。正确的分解是
> $$A\cup V=A\cup(V\setminus A),\qquad A\cap(V\setminus A)=\varnothing.$$
> 这里原稿的错误等式仍在上方保留，蓝色公式是编者修正。

<!-- unit: N-P010-004 -->
若 $A$ 可测，$A\cup V$ 可测 $\iff A\setminus V$ 可测。

<!-- unit: N-P010-004-S1 -->
> [!info] 纠错及补证：正确的等价条件
> 在 $A\in\mathcal M$ 下，正确命题是
> $$A\cup V\in\mathcal M\iff V\setminus A\in\mathcal M.$$
> 若左端成立，作可测差集 $(A\cup V)\setminus A=V\setminus A$ 即得右端。若右端成立，由上一条正确分解，两个可测集之并可测，得到左端。原写 $A\setminus V$ 则不对：仍取 $A=\varnothing$、$V$ 不可测，右边可测而左边不可测。

<!-- unit: N-P010-005 -->
**Cor.** $A$ 可测，$A\cap V=\varnothing$，则 $A\cup V$ 不可测。

<!-- unit: N-P010-005-S1 -->
> [!info] 补充及补证：承接的假设
> 这里须承接 $V$ 不可测。由于 $V\setminus A=V$，正确等价式立即说明 $A\cup V$ 不可测。也可反设并可测，再作差 $(A\cup V)\setminus A=V$，得到矛盾。仅有“$A$ 可测且不交”而不要求 $V$ 不可测，结论当然不成立。

<!-- unit: N-P010-006 -->
$$\Phi:2^{[2,3]}\longrightarrow2^{\mathbb R}.$$

〔定义域的底数 $2$ 写在 $[2,3]$ 的左下方，按幂集记号排版。〕

<!-- unit: N-P010-007 -->
$[2,3]\supset A\longmapsto A\cup V$。

<!-- unit: N-P010-008 -->
〔Q003：起首动词及衔接字〕 Vatelli 〔Q003〕 $[2,3]^c$；可测〔子〕集，$2^c$。

〔外文名按可见拼写保留，通常名称为 Vitali。〕

<!-- unit: N-P010-008-S1 -->
> [!info] 补充：由相邻映射恢复数学意图
> 相邻两行清楚给出 $A\subset[2,3]$ 及 $A\mapsto A\cup V$，本行又有 $[2,3]^c$。可据此按“固定一个位于 $[2,3]^c$ 的不可测 Vitali 集 $V$”恢复论证，但起首及衔接字的确切字形仍记 Q003，不把数学通顺当成已经读清原字。可具体选 $V\subset[0,1]$。

<!-- unit: N-P010-008-S2 -->
> [!info] 补证：不可测集也有 $2^c$ 个
> 原映射可在 $[2,3]$ 的所有子集上定义。为证明它给出 $2^c$ 个不可测集合，只需限制到 $C_0=C+2\subset[2,3]$ 的所有子集，其中 $C$ 是三分 Cantor 集。平移不改变外测度，所以 $C_0$ 仍零测、势为 $c$，其 $2^c$ 个子集 $A$ 全可测，且都与固定的不可测 $V\subset[0,1]$ 不交。前一推论说明每个 $A\cup V$ 不可测。
>
> 若 $A_1\cup V=A_2\cup V$，两边与 $[2,3]$ 相交，集合恒等式给 $A_1=A_2$，因此映射为单射。不可测集合族的势至少 $2^c$，而它包含于 $\mathcal P(\mathbb R)$，势至多 $2^c$；故恰为 $2^c$。这里求交只是证明两个集合相等的操作，不依赖先断言该区间可测。
>
> 也可直接证明原映射在整个 $\mathcal P([2,3])$ 上都取不可测值：任取 $A\subset[2,3]$，若 $A\cup V$ 可测，则与已知可测的 $[0,1]$ 相交，得到 $(A\cup V)\cap[0,1]=V$ 可测，矛盾。由前述求交单射性，这直接给出 $2^c$ 个不同的不可测集。此路线不要求 $A$ 自身可测；前面的 Cantor 子集路线则保留了“可测集与不交不可测集之并”的推论用法。

<!-- unit: N-SEC-15 -->
<a id="n-sec-15"></a>

## 十五、选择公理与 Solovay 模型旁注

<!-- unit: N-P006-007 -->
不可测集存在：
$$AC+ZF\ \longrightarrow\ P\text{ 成立}. $$

<!-- unit: N-P006-007-S1 -->
> [!info] 补充：命题P的含义
> 此处 $P$ 指“存在非 Lebesgue 可测的实数集”。$AC$ 是选择公理，$ZF+AC=ZFC$。选择公理用于从有理差等价类中选代表，Vitali 构造说明 $ZFC\vdash P$。

<!-- unit: N-P006-008 -->
设 $T$ 是一个公理体系。

（1）存在一个 model，s.t. $T+P$。

<!-- unit: N-P006-009 -->
（2）存在另一个 model，s.t. $T+\neg P$。

<!-- unit: N-P006-010 -->
则 $P$ 独立于公理体系。

<!-- unit: N-P006-010-S1 -->
> [!info] 补证：模型与不可证明性
> 若有模型 $M_+\models T+P$ 和 $M_-\models T+\neg P$，则 $T$ 不能证明 $P$，否则由逻辑可靠性 $M_-$ 也应满足 $P$；同理，$T$ 不能证明 $\neg P$，否则 $M_+$ 矛盾。因此 $T\nvdash P$ 且 $T\nvdash\neg P$。原稿这里的 $T+P$ 表示模型满足合并后的全部公理。

<!-- unit: N-P006-011 -->
$P$ 在“存在一个不可达基数”情况下：

<!-- unit: N-P006-012 -->
$$ZF\nvdash P,\qquad ZF\nvdash\neg P.$$

<!-- unit: N-P006-012-S1 -->
> [!info] 补充：相对一致性前提须写清
> 这里是模型存在性下的结论。Solovay 的原论文 Theorem 1 以“存在 $ZFC+$存在不可达基数的传递模型”为假设，构造满足 $ZF+DC$ 且所有实数集 Lebesgue 可测的传递模型；$DC$ 是依赖选择。该模型满足 $\neg P$，而一个 $ZFC$ 模型通过 Vitali 构造满足 $P$。因此在上述模型存在假设下，$P$ 对 $ZF$ 独立。
>
> 来源：[Robert M. Solovay, *A Model of Set-Theory in Which Every Set of Reals is Lebesgue Measurable* (1970), Theorem 1](https://www.liutianren.com/discrete/ref/Logic%20and%20Set%20Theory/Solovay-ModelSetTheoryEvery-1970.pdf)，以及[期刊原始书目](https://annals.math.princeton.edu/1970/92-1/p01)。原稿并未给出 forcing 构造；这里补的是准确假设和结论，不把深层模型定理伪装成课堂已证。

<!-- unit: N-P006-013 -->
若 $ZF\to P$，
$$ZFC\to P.$$

<!-- unit: N-P006-013-S1 -->
> [!info] 纠错：这两行没有导出矛盾
> 因为 $ZFC$ 包含 $ZF$，这个推导本身成立；但 $ZFC\vdash P$ 原本就是已知结论，所以不能据此证明 $ZF\nvdash P$。要排除 $ZF\vdash P$，应使用满足 $ZF+\neg P$ 的 Solovay 模型。要排除 $ZF\vdash\neg P$，则可反设它成立，推出 $ZFC\vdash\neg P$，与一致的 $ZFC$ 中 $P$ 的证明冲突。原稿的正负号原样保留于上方。

<!-- unit: N-SEC-16 -->
<a id="n-sec-16"></a>

## 十六、无穷维平移测度原问题及两个相关补证

<!-- unit: N-P001-013 -->
原稿问题：“无穷维，不存在〔疑字 RA07-Q001：量词样符号〕平移正规性、非平凡测度，？”

<span style="color:red">原稿明确留问号，未在此处作答。</span>

<!-- unit: N-P001-013-S1 -->
> [!info] 补充与补证：无限维空间中的平移测度
> 原稿句首经回图比较更接近“无穷维”；中间量词样符号尚未唯一恢复。下面明确给出一个适用范围，不把补入前提冒充原字迹：**无限维可分赋范空间上，非零、平移不变的 Borel 测度不可能局部有限。**
>
> 先补一个工具：**有限维线性子空间是闭的。** 若 $Y=\operatorname{span}\{v_1,\ldots,v_d\}$，其中 $v_i$ 线性无关，令 $A(t)=\sum_i t_iv_i$。三角不等式给出 $\|A(t)\|\le C\|t\|_2$，故 $t\mapsto\|A(t)\|$ 连续；它在紧致的欧氏单位球面上处处为正，因而有正最小值 $c$。于是 $c\|t\|_2\le\|A(t)\|$。若 $A(t_n)\to y$，则由下界，$(t_n)$ 为欧氏空间中的 Cauchy 列，收敛于某 $t$；由上界 $A(t_n)\to A(t)$，故 $y=A(t)\in Y$。复数情形把 $\mathbb C^d$ 视为 $\mathbb R^{2d}$ 即可；零子空间显然闭。
>
> 再证明所需的 Riesz 引理：若 $Y$ 是赋范空间中的真闭线性子空间，$0<\theta<1$，取 $z\notin Y$，令 $d=d(z,Y)>0$；由距离下确界定义，选 $y_0\in Y$ 使 $\|z-y_0\|<d/\theta$。则单位向量 $u=(z-y_0)/\|z-y_0\|$ 满足 $d(u,Y)=d/\|z-y_0\|>\theta$。
>
> 假设这样的测度 $\mu$ 局部有限。取 $R>0$ 使 $\mu(B(0,R))<\infty$。有限维线性子空间是闭的，逐次对已选向量的线性包应用 Riesz 引理（$\theta=1/2$），得到两两距离大于 $1/2$ 的单位向量列 $u_k$。令 $x_k=(R/2)u_k$，则 $\|x_k-x_l\|>R/4=2(R/8)$（$k\ne l$），故 $B(x_k,R/8)$ 两两不相交；其中每个点的范数小于 $R/2+R/8=5R/8<R$，所以这些球全在 $B(0,R)$ 内。由平移不变性，每个小球测度同为 $c=\mu(B(0,R/8))$；故任意 $N$ 都有 $Nc\le\mu(B(0,R))<\infty$，从而 $c=0$。可分性保证全空间能由可列个半径 $R/8$ 的球覆盖，于是 $\mu(X)=0$，矛盾。
>
> 命题范围已由 [USC 大学讲义《Wiener Measure》](https://dornsife.usc.edu/sergey-lototsky/wp-content/uploads/sites/211/2023/06/Week8-ByDiogo.pdf) 中的无限维说明核验；上文给出了固定半径的完整证明。仅“平移不变、非平凡”仍允许计数测度，局部有限性不能省略。

<!-- unit: N-P001-013-S2 -->
> [!info] 补充与补证：一个精确的相关命题
> 下面是另一个可独立验证的相关命题，讨论有限维实直线的全幂集；它不是前面无限维原问题的答案，也不是其逐字恢复。在选择公理下，不存在定义于 $\mathcal P(\mathbb R)$、可列可加、平移不变、且满足 $m([0,1))=1$ 的测度。
>
> 在 $[0,1)$ 上按 $x\sim y\iff x-y\in\mathbb Q$ 分成等价类，每类选一个代表，组成 $V$。令 $Q=\mathbb Q\cap(-1,1)$。各 $V+q$（$q\in Q$）互不相交：若 $v+q=w+r$，则 $v-w\in\mathbb Q$，代表唯一性给出 $v=w$，进而 $q=r$。同时 $[0,1)\subseteq\bigcup_{q\in Q}(V+q)\subseteq(-1,2)$。
>
> 由平移不变性和可列可加性，并集测度是可列无穷个相同的 $m(V)$ 之和。若 $m(V)=0$，则并集测度为 $0$，与包含 $[0,1)$ 矛盾；若 $m(V)>0$（包括无穷），则该和为 $+\infty$，与并集包含于 $(-1,2)$ 且 $m((-1,2))\le3$ 矛盾。这里 $(-1,2)\subset[-1,0)\cup[0,1)\cup[1,2)$，三个半开单位区间都是 $[0,1)$ 的平移，故测度总和为 $3$。
>
> “非平凡、平移不变”本身不足以得到不存在性：计数测度就是定义在全部子集上的反例。必须保留归一化或适当局部有限性的条件；本页“正规性”的确切课堂定义仍需后续复核。
