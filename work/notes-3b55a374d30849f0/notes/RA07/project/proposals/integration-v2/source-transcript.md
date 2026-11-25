<!-- unit: T-INTRO -->
# 实分析 7：原序保真转写

原件：实分析7.pdf，共 13 物理页。按原稿页序保留公式、旁注、问题、重复及原错误。中性编号标识尚不能唯一恢复的字迹；数学补充不冒充原文。

<!-- unit: T-P001-HEAD -->
## 物理第 1 页

<!-- unit: T-P001-001 -->
$σ$ 代数。

<!-- unit: T-P001-002 -->
$$\Sigma\subseteq\mathcal P(X).$$

<!-- unit: T-P001-003 -->
$$m:\Sigma\longrightarrow\mathbb R^+.$$

<!-- unit: T-P001-004 -->
（1）$m(\varnothing)=0$。

<!-- unit: T-P001-005 -->
（2）$$m\!\left(\bigcup_{i=1}^{\infty}A_i\right)=\sum_i m(A_i).$$

<!-- unit: T-P001-006 -->
旁写条件：$A_i\cap A_j=\varnothing$。

<!-- unit: T-P001-007 -->
Lebesgue：平移不变、正规性。

<!-- unit: T-P001-008 -->
例：counting 测度。
$$E\longmapsto m(E)=|E|.$$

<!-- unit: T-P001-009 -->
Dirac 测度。
$$\delta:2^X\longrightarrow\mathbb R^+.$$

<!-- unit: T-P001-010 -->
$$\delta_x(E)=\begin{cases}1,&x\in E,\\0,&x\notin E.\end{cases}$$

<!-- unit: T-P001-011 -->
任意：$$2^{\mathbb R^n}\longrightarrow\mathbb R^+.$$

<!-- unit: T-P001-012 -->
$$\mathfrak c^{2^{\mathfrak c}}=(2^{\aleph_0})^{2^{\mathfrak c}}=2^{2^{\mathfrak c}}.$$

<!-- unit: T-P001-013 -->
无穷维，不存在〔疑字 RA07-Q001：量词样符号近似“$\wedge m$”〕平移正规性、非平凡测度，？（右端有蓝色圈问号。）

<!-- unit: T-P001-014 -->
Jordan 测度。（有限覆盖）

<!-- unit: T-P001-015 -->
$$U(f,P)=\sum_i\sup f\,\Delta x_i.$$

<!-- unit: T-P001-016 -->
$$L(f,P)=\sum_i\inf f\,\Delta x_i.$$

<!-- unit: T-P002-HEAD -->
## 物理第 2 页

<!-- unit: T-P002-001 -->
$$\sup_P U(f,P)=\inf_P L(f,P)\quad\Rightarrow\quad\text{Rm 可积}. $$

<!-- unit: T-P002-002 -->
可以对应：内外测度。

<!-- unit: T-P002-003 -->
$E\subset\mathbb R^n$，则
$$E\text{ Jordan 可测}\iff m_J^*(\partial E)=0.$$

<!-- unit: T-P002-004 -->
原稿另写提示：$m_J^*:\ \displaystyle\int_a^b f(x)$。

<!-- unit: T-P002-005 -->
**Lemma.** 若 $S$ 在 $[0,1]$ 中稠密，且
$$S\cap[0,1]\subset\bigcup_{i=1}^{n}(a_i,b_i),$$

<!-- unit: T-P002-006 -->
则
$$[0,1]\subset\bigcup_{i=1}^{n}[a_i,b_i].$$

<!-- unit: T-P002-007 -->
Proof：内填外包。

<!-- unit: T-P002-008 -->
对无限集定义求和（网）。

<!-- unit: T-P002-009 -->
**Def（1）** $E\subset\mathbb R^n$，有开区间 $(I_k)$，使得
$$E\subset\bigcup_{k=1}^{\infty}I_k,$$
则称一个 Lebesgue 覆盖。

<!-- unit: T-P002-010 -->
1. $LC(E)\ne\varnothing$，$\forall E\subset\mathbb R^n$。

<!-- unit: T-P002-011 -->
$$I_\alpha=(a_1,b_1)\cdots(a_n,b_n),\qquad a_i,b_i\in\mathbb Z.$$

<!-- unit: T-P002-012 -->
$$\mathbb R^n=\bigcup_\alpha I_\alpha.$$

<!-- unit: T-P002-013 -->
$\forall x\in(x_1,\ldots,x_n)$〔原笔为 ∈ 样弯笔；规范坐标等号见蓝色补充〕，
$$x\in\prod\bigl([x_1]-1,\ldots,[x_n]+1\bigr).$$
（此处保留原稿压缩的乘积记号。）

<!-- unit: T-P003-HEAD -->
## 物理第 3 页

<!-- unit: T-P003-001 -->
或：$\mathbb R^n$ 是 Lindelöf，有遗传性。导出相应区间放大，来证明。

<!-- unit: T-P003-002 -->
2. $\overline{\overline{LC(E)}}$：所有覆盖的族，记为 $LC_E$。
〔$LC(E)$ 上方原有两条横笔；含义暂不强定。〕

<!-- unit: T-P003-003 -->
$\mathcal I=$“$\mathbb R^n$ 中全体开区间”，原稿简记其大小为 $\mathfrak c$，并写
$$\longrightarrow (\mathfrak c\times\cdots\times\mathfrak c),\qquad \mathfrak c^{\mathbb N}.$$

<!-- unit: T-P003-004 -->
$$\mathcal I^{\mathbb N}=\mathfrak c^{\mathbb N}=(2^{\aleph_0})^{\aleph_0}=\mathfrak c.$$

<!-- unit: T-P003-005 -->
由（1）可取 $\{I_k\}\in LC(E)$。

<!-- unit: T-P003-006 -->
$\{I_k\}$ 可覆盖。

**Def（2）** 定义
$$m^*:2^{\mathbb R^n}\longrightarrow[0,+\infty].$$

<!-- unit: T-P003-007 -->
$$E\longmapsto\inf\sum_{k=1}^{\infty}|I_k|,\qquad I_k\in LC_E.$$
约为外测度。

<!-- unit: T-P003-008 -->
**Remark**

（1）$I_n$ 可为 $\varnothing$。

<!-- unit: T-P003-009 -->
（2）$I_n$ 是否可为〔疑字 RA07-Q002：字形候选“闭矩形”〕，可证明。Proof：

<!-- unit: T-P003-010 -->
$\forall\varepsilon$，$\forall\{B_i\}\in\overline{\mathcal B}$，
$$I\subset\bigcup_iB_i.$$

<!-- unit: T-P003-011 -->
$$\sum_i|B_i|<|I|+\varepsilon.$$

<!-- unit: T-P003-012 -->
### 外测度性质

（1）$m^*(\varnothing)=0$。

<!-- unit: T-P003-013 -->
（2）$E\subset F\ \Rightarrow\ m^*(E)\le m^*(F)$。

<!-- unit: T-P004-HEAD -->
## 物理第 4 页

<!-- unit: T-P004-001 -->
（3）$\{E_k\}$：
$$m^*\!\left(\bigcup_kE_k\right)\le\sum_km^*(E_k).$$

<!-- unit: T-P004-002 -->
Proof：$\forall\varepsilon>0$，$\exists\{I_{k,j}\}\in LC(E_k)$（有限时）。

<!-- unit: T-P004-003 -->
$$E_k\subset\bigcup_{j=1}^{\infty}I_{k,j}.$$

<!-- unit: T-P004-004 -->
$$\sum_{j=1}^{\infty}|I_{k,j}|<m^*(E_k)+\frac{\varepsilon}{2^k}\qquad\text{（下确界）}.$$

<!-- unit: T-P004-005 -->
$$\bigcup_kE_k\subset\bigcup_{k=1}^{\infty}\bigcup_{j=1}^{\infty}I_{k,j}.$$

<!-- unit: T-P004-006 -->
$$m^*\!\left(\bigcup_{k=1}^{\infty}E_k\right)\le\sum_{(k,j)}|I_{k,j}|.$$
首个不等式下旁注：“下界”。

<!-- unit: T-P004-007 -->
$$\sum_{(k,j)}|I_{k,j}|<\sum_km^*(E_k)+\sum_{k=1}^{\infty}\frac{\varepsilon}{2k}.$$
〔原笔中此处分母 $k$ 与 $2$ 同基线；上文首次预算写为 $2^k$。〕

<!-- unit: T-P004-008 -->
Tonelli：可交换顺序。

$\varepsilon\to0$，取“$\le$”。

<!-- unit: T-P004-009 -->
**Prop.** $\{x_k\}\subset\mathbb R^n$，$m^*(\{x_k\})=0$。

<!-- unit: T-P004-010 -->
**Cor.** $m^*(\mathbb Q\cap[0,1])=0$。

<!-- unit: T-P004-011 -->
Cantor：$C\subset[0,1]$。
$$C=\bigcap_{n=0}^{\infty}C_n.$$

<!-- unit: T-P004-012 -->
$$m^*(C)\le m^*(C_n)=\left(\frac23\right)^n.$$

<!-- unit: T-P004-013 -->
$$m^*(C)=0.$$
旁注：“势是多少？”答：$\mathfrak c$。

<!-- unit: T-P005-HEAD -->
## 物理第 5 页

<!-- unit: T-P005-001 -->
$I\subset\mathbb R^n$ 是有界区间，则 $m^*(I)=|I|$。

<!-- unit: T-P005-002 -->
若 $I$ 闭，则 $\forall\varepsilon>0$，$\exists I'$ 开，s.t.
$$|I'|<|I|+\varepsilon.$$

<!-- unit: T-P005-003 -->
任意测度 $>0$ 的〔集〕存在不可测子集。

<!-- unit: T-P005-004 -->
### 可测集

引入：$E\subset\mathbb R^n$。

<!-- unit: T-P005-005 -->
取 $G$ 开，$G\supset I\setminus E$。

<!-- unit: T-P005-006 -->
$I\setminus G\subset E$ 中紧集。

<!-- unit: T-P005-007 -->
旁写：$|I|-|I\,/\,G|$。
〔第二项中 $I$ 后为单斜杠样笔画，差集/交集读法未决；不是单独的 $|G|$。〕

<!-- unit: T-P005-008 -->
令 $$m_*(E)=|I|-m^*(I\setminus E).$$

<!-- unit: T-P005-009 -->
若 $m_*(E)=m^*(E)$，则 $E$ 可测。

<!-- unit: T-P005-010 -->
$$|I|=m^*(I\cap E^c)+m^*(E).$$

<!-- unit: T-P005-011 -->
$$|I|=m^*(I\cap E^c)+m^*(E\cap I).$$

<!-- unit: T-P005-012 -->
$\forall I$ 均成立。

<!-- unit: T-P005-013 -->
$E$ 有界：$m^*(E)=m_*(E)$。

<!-- unit: T-P005-014 -->
无界：$E\cap I$ 可测。

<!-- unit: T-P006-HEAD -->
## 物理第 6 页

<!-- unit: T-P006-001 -->
Carathéodory。

<!-- unit: T-P006-002 -->
**Def.** 设 $E\subset\mathbb R^n$，若 $\forall T\subset\mathbb R^n$ 有
$$m^*(T)=m^*(T\cap E)+m^*(T\cap\cdots).$$
〔本行扫描右缘截断；根据本页中部完整复写，可恢复末项为 $m^*(T\cap E^c)$；测试字母原笔呈 T 样。〕

<!-- unit: T-P006-003 -->
则称 $E$ Lebesgue 可测，记 $m^*(E)=m_L(E)$。

〔下标按本行“Lebesgue”语境整理为 $L$；详见记号局部图。〕

<!-- unit: T-P006-004 -->
记全体为 $\mathcal M$。

<!-- unit: T-P006-005 -->
原图：左上较小圆与右下较大圆相交，圆上方写 $E$；右下圆未写名称，没有阴影或箭头。

![原稿中的相交集合图](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/refs/heads/work/notes/work/notes-fc2ba28a26cd495f/notes/RA07/project/evidence/p0006-diagram.png)

<!-- unit: T-P006-006 -->
一般：
$$m^*(T)=m^*(T\cap E)+m^*(T\cap E^c).$$
〔本页完整复写中的测试字母原笔呈 T 样。〕

<!-- unit: T-P006-007 -->
不可测集存在：
$$AC+ZF\ \longrightarrow\ P\text{ 成立}. $$

<!-- unit: T-P006-008 -->
设 $T$ 是一个公理体系。

（1）存在一个 model，s.t. $T+P$。

<!-- unit: T-P006-009 -->
（2）存在另一个 model，s.t. $T+\neg P$。

<!-- unit: T-P006-010 -->
则 $P$ 独立于公理体系。

<!-- unit: T-P006-011 -->
$P$ 在“存在一个不可达基数”情况下：

<!-- unit: T-P006-012 -->
$$ZF\nvdash P,\qquad ZF\nvdash\neg P.$$

<!-- unit: T-P006-013 -->
若 $ZF\to P$，
$$ZFC\to P.$$

<!-- unit: T-P006-014 -->
页左缘另有一段右括号样残弧（约 x=0–25、y=2475–2570）；无法据残笔恢复前文，保留为未定页边残笔。

<!-- unit: T-P007-HEAD -->
## 物理第 7 页

<!-- unit: T-P007-001 -->
**Th.**
$$E\in\mathcal M\iff m^*(I)=m^*(I\cap E)+m^*(I\cap E^c),$$
$\forall I\subset\mathbb R$ 区间（矩形）。

<!-- unit: T-P007-002 -->
〔左边缘另有被裁切的公式尾段，能读出 $E^c)$；没有足够图像恢复其前项。〕

<!-- unit: T-P007-003 -->
**pf.** $\Rightarrow$：显然。

<!-- unit: T-P007-004 -->
$\Leftarrow$：由外测度次可加性，仅证
$$m^*(I)\ge m^*(T\cap E)+m^*(T\cap E^c).$$
〔左端原笔为 I 样，右端两项为 T；数学规范补充见学习稿蓝色块。〕

<!-- unit: T-P007-005 -->
（1）若 $m^*(T)=+\infty$，成立。

<!-- unit: T-P007-006 -->
（2）$\forall\varepsilon>0$，$\exists\{I_k\}\in LC(T)$，s.t.
$$\sum_{k=1}^{\infty}(I_k)<m^*(T)+\varepsilon.$$
〔原笔求和项两侧为圆括号样笔画；体积双竖线是蓝色数学说明。〕

<!-- unit: T-P007-007 -->
$$T\cap E\subset\bigcup_{k=1}^{\infty}(E\cap I_k).$$

<!-- unit: T-P007-008 -->
$$T\cap E^c\subset\bigcup_{k=1}^{\infty}(E^c\cap I_k).$$

<!-- unit: T-P007-009 -->
$$m^*(T\cap E)\le m^*\left(\bigcup_{k=1}^{\infty}(E\cap I_k)\right)
\le\sum_{k=1}^{\infty}m^*(E\cap I_k)<+\infty.$$

<!-- unit: T-P007-010 -->
$$m^*(T\cap E)+m^*(T\cap E^c)
\le\sum_{k=1}^{\infty}m^*(E\cap I_k)+\sum_{k=1}^{\infty}m^*(E^c\cap I_k).$$

<!-- unit: T-P007-011 -->
（“题设”标在下一等号处。）
$$=\sum_{k=1}^{\infty}m^*(I_k)=\sum_{k=1}^{\infty}|I_k|<m^*(T)+\varepsilon.$$

<!-- unit: T-P007-012 -->
$\varepsilon\to0^+$。

<!-- unit: T-P007-013 -->
**Th.** $E\in\mathcal M\iff\forall A\subset E$，且 $B\subset E^c$，有
$$m^*(A\cup B)=m^*(A)+m^*(B).$$

<!-- unit: T-P008-HEAD -->
## 物理第 8 页

<!-- unit: T-P008-001 -->
$\Rightarrow$：令 $T=A\cup B$，则

<!-- unit: T-P008-002 -->
$$T\cap E=A.$$

<!-- unit: T-P008-003 -->
$$T\cap E^c=B.$$

<!-- unit: T-P008-004 -->
因 $E\in\mathcal M$，$m^*(T)=m^*(A)+m^*(B)$。

<!-- unit: T-P008-005 -->
$\Leftarrow$：任取 $T\subset\mathbb R^n$。

<!-- unit: T-P008-006 -->
令 $A=T\cap E$，$B=T\cap E^c$。

<!-- unit: T-P008-007 -->
注意：$A\cap B=\varnothing$，
$$m^*(A\cup B)\ne m^*(A)+m^*(B),$$
$A,B$ 可测成立。

<!-- unit: T-P008-008 -->
若 $d(A,B)>0$，则上式成立。

<!-- unit: T-P008-009 -->
$$A\cap B=\varnothing\quad(A\text{ 闭，}\ B\text{ 紧})\ \Rightarrow\ d(A,B)>0.$$

<!-- unit: T-P008-010 -->
**Proof：**

〔本页该标题以下未写推导，余下大段为空白。〕

<!-- unit: T-P009-HEAD -->
## 物理第 9 页

<!-- unit: T-P009-001 -->
（1）$\varnothing\in\mathcal M$，$\mathbb R^n\in\mathcal M$。

<!-- unit: T-P009-002 -->
（2）不可测，可测。

<!-- unit: T-P009-003 -->
（3）并、交、补，上下极限。

<!-- unit: T-P009-004 -->
**Def.** 外测度为 $0$ 之集，称为零测集。

<!-- unit: T-P009-005 -->
**Prop.** 零测集必可测。

<!-- unit: T-P009-006 -->
$$0\le m^*(T\cap E)\le m^*(E)=0.$$

<!-- unit: T-P009-007 -->
因 $m^*(T)\ge m^*(T\cap E)$。

<!-- unit: T-P009-008 -->
（2）零测集子集是零测集。

<!-- unit: T-P009-009 -->
（3）至多个可数个零测集并是零测集。

<!-- unit: T-P009-010 -->
**Def.** $A\cap B=\varnothing$，$\overline{\overline A}=\alpha$，$\overline{\overline B}=\beta$。

<!-- unit: T-P009-011 -->
（1）$\overline{\overline{A\cup B}}=\alpha+\beta$。

<!-- unit: T-P009-012 -->
（2）$\alpha\cdot\beta=\overline{\overline{A\times B}}$。

<!-- unit: T-P009-013 -->
（3）$\alpha^\beta=\overline{\overline{A^B}}=\{f:B\to A\}$。

<!-- unit: T-P009-014 -->
$$\overline{\overline{2^c}}\le\overline{\overline{\mathcal M}}\le2^c.$$
〔左端 $2$ 上方原有两条短横；上标 C/c 形仍按原笔保留。〕

<!-- unit: T-P009-015 -->
Cantor（上方标 $c$）：任意子集可测，$2^c$。

<!-- unit: T-P010-HEAD -->
## 物理第 10 页

<!-- unit: T-P010-001 -->
**Q.** $A,B$ 不可测，$\overset{?}{\Rightarrow}$ $A\cup B$ 不可测。

<!-- unit: T-P010-002 -->
**Q.** $A$ 可测，$B$ 不可测；$A\cup B$ 不可测。

<!-- unit: T-P010-003 -->
$$A\cup V=A\cup(A\setminus V).$$

<!-- unit: T-P010-004 -->
若 $A$ 可测，$A\cup V$ 可测 $\iff A\setminus V$ 可测。

<!-- unit: T-P010-005 -->
**Cor.** $A$ 可测，$A\cap V=\varnothing$，则 $A\cup V$ 不可测。

<!-- unit: T-P010-006 -->
$$\Phi:2^{[2,3]}\longrightarrow2^{\mathbb R}.$$

〔定义域的底数 $2$ 写在 $[2,3]$ 的左下方，按幂集记号排版。〕

<!-- unit: T-P010-007 -->
$[2,3]\supset A\longmapsto A\cup V$。

<!-- unit: T-P010-008 -->
〔Q003：起首动词及衔接字〕 Vatelli 〔Q003〕 $[2,3]^c$；可测〔子〕集，$2^c$。

〔外文名按可见拼写保留，通常名称为 Vitali。〕

<!-- unit: T-P010-009 -->
凡测度 $>0$ 之集，必 $\exists$ 不可测子集。

<!-- unit: T-P010-010 -->
运算性质。

<!-- unit: T-P010-011 -->
（1）$A,B\in\mathcal M$，$A\cup B\in\mathcal M$。

<!-- unit: T-P011-HEAD -->
## 物理第 11 页

<!-- unit: T-P011-001 -->
$\forall T\subset\mathbb R^n$。

<!-- unit: T-P011-002 -->
$$m^*(T)\ge m^*(T\cap(A\cup B))+m^*(T\cap A\cup B^c).$$

<!-- unit: T-P011-003 -->
原图：三个相交圆分别标 $A$、$B$、$T$；$T$ 圆较大，位于下方。其内部写 1、2、3、4，分别落在仅与 $A$ 相交、三圆公共、仅与 $B$ 相交、与 $A,B$ 都不交的部分。

![原稿三圆四区域图](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/refs/heads/work/notes/work/notes-fc2ba28a26cd495f/notes/RA07/project/evidence/p0011-diagram.png)

<!-- unit: T-P011-004 -->
$(T\cap A\cap B)\cup(T\cap A\cap B^c)\cup(T\cap B\cap A^c)$

<!-- unit: T-P011-005 -->
$=T\cap(A\cup B)$。

<!-- unit: T-P011-006 -->
则取外测度。

<!-- unit: T-P011-007 -->
$$m^*(T\cap A\cap B^c)+m^*(T\cap A\cap B)=m^*(T\cap A).$$

<!-- unit: T-P011-008 -->
〔Q004：公式前的三个衔接字〕
$$m^*(T\cap A)+m^*(T\cap A^c)=m^*(T).$$

<!-- unit: T-P011-009 -->
**Prop.** $S$ 可测，$S^c$ 可测。

<!-- unit: T-P011-010 -->
$$m^*(T\cap S)+m^*(T\cap S^c)
\overset{\text{性质}}{=}m^*(T\cap S^{cc})+m^*(T\cap S^c).$$

〔原稿右边在 $S$ 上连写两个补集符号。〕

<!-- unit: T-P011-011 -->
$A,B$ 可测，$A\cap B$ 可测。

<!-- unit: T-P011-012 -->
**Prop.** $A,B\in\mathcal M$，$A\cap B=\varnothing$。

<!-- unit: T-P011-013 -->
$$m(A\cup B)=m(A)+m(B).$$

<!-- unit: T-P012-HEAD -->
## 物理第 12 页

<!-- unit: T-P012-001 -->
$B\subset A^c$。

<!-- unit: T-P012-002 -->
$A,B\in\mathcal M$，$B\subseteq A$。

<!-- unit: T-P012-003 -->
$m(B)<\infty$。

<!-- unit: T-P012-004 -->
$$m(A\setminus B)=m(A)-m(B).$$
