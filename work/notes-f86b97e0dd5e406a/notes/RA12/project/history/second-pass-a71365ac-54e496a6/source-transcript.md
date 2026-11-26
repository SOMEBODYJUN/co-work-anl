# 实分析 12｜原稿保真转写

按原 PDF 的 7 个物理页排列。正文保留笔误、重复、旁注和三处原待填横线；蓝色说明用于识读或规范化，红色只标原稿明确留空。原有编号与本文来源编号分别保留。英文姓名按通行拼法排印；手写异体在说明中登记。数学订正及完整补证见独立的《study-notes.md》。

来源：本项目只读的 source.pdf。精确坐标、图片、裁图及双向去向见 manifest.json、source-target-map.json、ledger.json。

## 第 1 页

### Littlewood 3 定律

1. 每一个可测集几乎是有限个开区间并。
2. 每一个可测函数几乎连续。
3. 每〔校读：一〕个可测收敛的〔择优校读：是〕几乎一致收敛。

> [!note] <span style="color:blue">识读与限定校读</span>
>
> 标题尾字按“律”形排印。第三条‘每／个’间确有微短提，与前两条‘一’同位且同向，按平行句式恢复‘一’，置信弱至中等，普通点迹为备选。‘的／几’间另有独立上回折、中竖和右下扫的笔簇，依据同页及第2、5页‘是’的笔形择优校读‘是’，置信低至中等；‘列’语义较顺但欠独立刂，‘也’及改笔候选保留在台账。不声称两字逐笔唯一，也不把这团墨迹省掉。原口语‘收敛的’保留，完整数学意思在学习稿中解释为收敛的可测函数列；原‘几乎’未改成‘几乎处处’。

**Ex.** 设 $E\in M$，$m(E)<+\infty$〔原另有右括样收笔〕。$\forall\varepsilon>0$，$\exists I_i,\ldots,I_n$ 开区间，s.t.

$$
m\bigl(E\mathbin{\Delta}\bigl(\bigcup_{i=1}^n I_i\bigr)<\varepsilon.
$$

> [!note] <span style="color:blue">原笔迹与规范化说明</span>
>
> 题面第一个区间下标形近 $i$；并号下限的等号右仅见水滴点，没有可分辨的竖 $1$。这里将有限列从 $1$ 枚举是上下文规范化，学习稿相应写 $I_1,\ldots,I_n$，不声称已直接读出该数字。统一从别的整数重编号也不改变有限并，数学不能证明这枚点必为 $1$。原式确有两枚左括、仅一枚右括，上式保留这一省写；唯一右括配哪层不强判，学习稿使测度作用于整个对称差并规范闭合。题面有限测度条件后另有右括样弧；‘开区间’末端的右弧与同页‘间’的门框右钩相似，保留字末收笔解释及独立括样笔备选，不赋新数学分组。原运算是对称差，区间确写‘开’。

**Lemma.** 设 $f:X\to Y$。〔择优校读：且〕$X$ $\exists$ 一个开覆盖，$X=\bigcup_{i\in A}X_i$。

若 $\forall a\in A$，$f_a:X_a\to Y$ 连续，则 $f:X\to Y$ 连续。

$$
f^{-1}(U)=\bigcup_{a\in A}\bigl(f^{-1}(U)\cap X_a\bigr)
\overset{\text{定义}}{=}\bigcup_{a\in A}\bigl((f|_{X_a})^{-1}(U)\bigr).
$$

> [!note] <span style="color:blue">识读与上下文恢复</span>
>
> 覆盖的索引全集写出了 $A/\Delta/\Lambda$ 样的不同笔形，本段统一排作 $A$，保留先 $i$ 后 $a$ 的索引变化。首项上标只见短横，减号旁没有可分辨的独立 $1$；据后两项清楚的 $-1$、限制线和等式含义恢复为逆像，不声称首项的 $1$ 已逐笔读出。$f_a=f|_{X_a}$ 是从同段定义等号与限制记号恢复的关系，不是原题另写的一行。
>
> $Y$ 的句点与下一 $X$ 之间另有完整字簇，择优读“且”，中至较高置信；同手第 3 页“且”的左直、右包和下拖支持此读，“因／即／则”等为备选。数学证明只需独立的开覆盖条件，不能证明该字唯一。$X$ 后实见 $\exists$ 样量词，原口语排为“$X$ $\exists$ 一个开覆盖”。末并项的外括与限制函数括各自可见，已保留两枚左括和 $U$ 后两枚右括。
>
> 下一行“注意”右下的小簇有两点及卧钩。视觉、对抗复读更倾向它是“意”的偏位心底；数学复读倾向另一个草写“则”。此处择优保留“注意”，并明确登记小簇及“独立则”备选，不声称已唯一分字，也不把它当不存在。“到”候选欠至和刂的独立结构。两种有据解释均只引出限制连续，不改变证明方向。

注意 $f|_{X_a}$ 连续，

$$
(f|_{X_a})^{-1}(U)\in\tau_{X_a}=C\cap X_a,\qquad C\in\tau_X.
$$

由 $X_a$ 都 $\in\tau_X$，$C\cap X_a$ 是 $X$ 中开集。〔段末证毕样收笔〕

但即使是闭覆盖，无限个，但改成局部有限闭覆盖。

即：给定 $x\in X$，$\exists U\in N(x)$，$U$ 只与有有限个 $X_a$ 相交。

可测函数〔校读：近似〕，要求可数个覆盖。

> [!note] <span style="color:blue">字形校读及解释范围</span>
>
> 1200 dpi 与作者同页‘函’‘数’及走之笔对照后，择优校读‘近似’：前一字有独立低位底捺，后一字更像亻加以，缺少第二条走之，故优于‘逼近’；‘类似’虽符合拼接语境，却欠清楚的米、大结构。此为有依据的字形校读，置信度中等，不称逐笔唯一。‘要求可数个覆盖’可由可测拼接解释，但孤句本身没有给出一条完整的函数近似定理；学习稿中的可测拼接证明单独标为补充。
>
> 邻域句“只与”后实见连续两个“有”形，后接“限、个”，没有独立“多”字；上文保留“只与有有限个”的复写。学习稿用通常说法“只与有限多个”，含义是交到的覆盖成员数量有限。

## 第 2 页

### Lusin

设 $f$ 是 $E$ 上 a.e. 有限的可测函数，则 $\forall\delta>0$，$\exists F_\delta\overset{\text{闭}}{\subset}E$，满足

$$
m(E\setminus F_\delta)<\delta,\qquad \text{s.t.}\ f|_{F_\delta}\in C(F_\delta).
$$

并给出闭集构造 $F_\delta$ 的表达式。

**Pf. (1)** $f\in S(E)$。$\exists E_1,\ldots,E_\ell\in M$，s.t. $E=\cup X_i$，

$$
f=\sum_{i=1}^{\ell}c_i\chi_{E_i}.
$$

$\forall\delta$，由 Lebesgue 的内正规性，

$$
\exists F_{i,\delta}\overset{\text{紧闭}}{\subset}E_i,\qquad\text{s.t.}\,
m(E_i\setminus F_{i,\delta})<\frac{\delta}{\ell}.
$$

> [!note] <span style="color:blue">原记号说明</span>
>
> 覆盖式右端按交叉笔形记 $X_i$，上下文数学对象为 $E_i$；函数展开式的 $f$ 后原见上下两点，本文以等式规范排印，不声称原图有两横。“紧闭”两字可见。原稿暂未区分有限与无限测度，紧集逼近在学习稿中先限定有限测度，随后使用第 4 页局部化。
>
> 原姓名连写近 Lebegue，未见 e 与 g 间独立的 s；上文按所指的内正规性定理统一排作 Lebesgue，不把标准拼法当作逐字原迹。本页紧闭集存在式后及定理限制连续式前的两处 s.t. 保留原位置，缩写的点号按通常形式排印。

令

$$
F_\delta=\bigcup_{i=1}^{\ell}F_{i,\delta}.
$$

$$
\begin{aligned}
m(E\setminus F_\delta)
&=m(E\setminus\cup F_{i,\delta})\\
&=m\bigl(\bigcup_{i=1}^{\ell}\bigl(E\setminus F_{i,\delta}\bigr)
=\sum m(E\setminus F_{i,\delta})<\delta.
\end{aligned}
$$

> [!note] <span style="color:blue">原稿错误标识</span>
>
> 后两个 $E$ 未见下标 $i$，链中的等号保留。这是原稿集合运算错误，不在保真稿内暗改成正确式。
>
> 该并项的原迹是两枚左括、只有一枚右括，上式按原数目排印；唯一右括配哪一层不强判。学习稿使测度作用于整个并并补足分组。补括本身不能纠正差项中漏写下标的 $E$。

**(2)** $f\in M(E)$，则 $\exists\{\varphi_k\}\subset S(E)$，s.t.

$$
\lim_{k\to\infty}\varphi_k(x)=f(x),\qquad\forall x\in E.
$$

## 第 3 页

由 (1)，$\forall\delta$、$\forall k\in\mathbb N^*$，

$$
F_\delta\overset{\text{闭}}{\subset}E,\qquad\text{s.t.}\,
m(E\setminus F_k)<\frac{\delta}{2^k}.
$$

且 $\varphi_k\in C(F_k)$。令 $F_\delta=\bigcap_{k=1}^{\infty}F_k$，则

$$
m(E\setminus F_\delta)
=m\bigl(\bigcup_{k=1}^{\infty}E\setminus F_k\bigr)
\le\sum\frac{\delta}{2k}.
$$

$\varphi_k$ 在 $F_k$ 上连续。$\varphi_k$ 在 $\bigcap F_k$ 上连续，下证一致收敛。

> [!note] <span style="color:blue">识读说明</span>
>
> 首行左侧字面为 $F_\delta$，同一行右侧与下一行是 $F_k$。末和的 $k$ 起笔与 $2$ 近乎等高，按 $2k$ 笔形存留；另有低写指数 $2^k$ 候选，预期几何预算由首行明确的 $2^k$ 恢复。$\varphi_k\in C(F_k)$ 是省写限制。
>
> 后一个测度项的原迹只见 $m$ 后及末 $F_k$ 后的一对括弧，并号与 $E$ 间无独立内左括。上式保留原省写，数学含义为对各个 $E\setminus F_k$ 取并；学习稿可补内括明确作用域。

但 Egorov 要求 $m(E)<+\infty$。

因 $f$ a.e. 有限，$m(E(|f|=+\infty))=0$〔括弧及绝对值左界作规范排印；原迹见下述说明〕。

令

$$
g(x)=\frac{f(x)}{1+|f(x)|}.
$$

则 $g$ 有界。

$$
|f(x)|=\frac{|g(x)|}{1-|g(x)|}.
$$

$$
f(x)=\frac{g(x)}{1-g(x)}.
$$

$g(x)$ 有界。

> [!note] <span style="color:blue">识读说明</span>
>
> Egorov 手写有 Englov/Engrov 样连写，依本段指称统一姓名。带符号逆式分母原未写绝对值，保留原式；模值逆式中确有绝对值。两个“有界”提示都保留。
>
> 零测式在 $+\infty$ 后至等号前只见一枚独立右弧；$m$ 后和 $E$ 后有左弧样轮廓，但 $E$ 后的小弯及短线是否兼作绝对值左界存在分笔歧义，不强判为两个清楚独立的左括。上文完整双层括及 $|f|$ 明示为数学规范化。前文“a.e. 有限”恢复的集合是 $\{x\in E:|f(x)|=\infty\}$；只取 $f=+\infty$ 会漏掉负无穷值。原右弧计数比左界分笔更确定。

或用 Egorov 定理。

当 $m(E)<+\infty$，$\exists\varphi_k\to f$，
$\forall\delta>0$，$\exists F_\delta\overset{\text{闭}}{\subset}E$，s.t.

$$
m(E\setminus F_\delta)\quad\underline{\hspace{1cm}}
$$

<span style="color:red">〔原稿待填 B1：测度后的比较号及界值〕</span>

## 第 4 页

〔校读：用〕Egorov，$\exists G_\delta\subset E$，s.t.

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

要〔校读：求〕

$$
\begin{aligned}
&m\bigl((E\setminus F_\delta)\cup(E\setminus H_\delta)\bigr)\\
&\qquad <m(E\setminus F_\delta)+m(E\setminus H_\delta).
\end{aligned}
$$

$$
E\setminus H_\delta
=(E\setminus G_\delta\setminus H_\delta)\cup(G_\delta\setminus H_\delta).
$$

> [!note] <span style="color:blue">识读说明</span>
>
> 页首字有‘用／同’两候选。与第 3 页‘或用’和本页末‘需要用’对比，内部长轴均下探到右钩之下，且欠‘同’的清楚内口，故择优校读‘用’，另一个候选保留；此处是承接有限测度 Egorov 的选集步骤。估计前的词择优校读‘要求’：第二字右上独点、中央过横的长轴及下钩与第1页‘要求’同构，优于缺少亻加古结构的‘估’及缺少左讠的‘证’，置信中等至较高。引导词的校读不修掉原式的严格小于号；测度次可加位置的数学订正另见学习稿。
>
> 分解式首个并项原只见 $E$ 前、$H_\delta$ 后的一对括弧，$G_\delta$ 到 $H_\delta$ 间只见一条斜竖样笔。上式保留这一省写，按集合差左结合解释；也保留该笔兼作内右括及差集线的连写候选，不声称原有完整的两层分组。

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

> [!note] <span style="color:blue">原稿记号及校读说明</span>
>
> 第 (2) 条括号内的原字为两横的 $F$，第 (3) 条区间右端形如圆括号。两处数学订正分别为 $C(E)$ 和 $[0,1]$，在学习稿标明。两个限制等式之间原有形近 $B$ 的独写连接记号，本文依语法校读为‘且’；该字形与同页字母 $B$、第 3 页‘且’分别比较后仍不称逐笔唯一，不把它当作额外集合运算。

**Remark.** 外测度中不对，$m^*(A\cup B)$〔上下文恢复：除非〕$A\,\&\,B$ 可被可测集分〔本行止于右缘〕。

$$
C=A\cup B.
$$

> [!note] <span style="color:blue">上下文恢复及残句范围</span>
>
> 起句校读为‘外测度中不对’。连接词取优势候选‘除非’：首形的阝与余形连笔、次形双竖及后接条件的语法共同支持，‘所谓’欠斤、讠和胃结构，‘可加性’的字数及笔形不合。其置信度中等，恢复性质已就地标明。右缘只写到‘分’，原 PDF 右页外没有后续绘画路径，故不把‘分开／分隔’补成已写原文。$C=A\cup B$ 原为下一独立行。学习稿仅给出可测分离推出加性的充分条件，不从残句反推无条件的必要性。
>
> $A$ 与 $B$ 间的原符号有交叉斜笔和闭回环，较合手写 &；上文保留为 $\&$，学习解释可译作“和”。备选“及”欠其通常的末捺，不能把中文译写当原字。

**Th.** 设 $f$ 是 $E$ 上几乎处处有限函数，$E\in M$：

1. $f$ 可测。
2. $\exists\{\varphi_k\}\subset S(E)$，s.t. $\varphi_k\to f$ 逐点。
3. $\exists\{\varphi_k\}\subset C(\mathbb R^n)$，s.t. $\varphi_k\xrightarrow{\mathrm{a.e.}}f$。

## 第 6 页

**Pf. (1) $\to$ (3).**

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
>
> 页首的原箭头只有单杆，保真写 $\to$；这里连接的是前页的条件编号，数学上表示从 (1) 推出 (3)，学习稿以 $\Rightarrow$ 规范表示蕴涵。

由 Borel–Cantelli：

$$
m\left(\limsup_{n\to\infty}E_n\right)=0.
$$

〔左缘边字；原矢量补证、择优校读：易〕 考察

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

（几乎〔择优校读：任意〕）

$$
x\in\bigcup_{N=1}^{\infty}\bigcap_{k=N}^{\infty}E(f=g_k).
$$

$$
\exists N(x)\ \text{s.t.}\ k\ge N,\qquad f=g_k\ \text{恒等}.
$$

> [!note] <span style="color:blue">识读与省记说明</span>
>
> 首式的 $E_n$ 没有在这一行定义；后文以失配事件明确其用途。花括／圆括均作原谓词集合写法保存；包含式的右端 $F_k$ 后原另有孤立闭圆括样笔，左端没有成对开括，排式未把它当作运算。上式内并原只有下标 $k=N$，未另写上标无穷；下式两个无穷上标均可见。左缘首字受页面及 Form 裁框截切，在内存放宽裁框后补见原有矢量笔画，未改绘画路径；下部围笔内两处墨迹支持‘易’优于‘另’，上部仍潦草，故取低至中等置信的字形择优校读；左缘边字可能独立于‘考察’，不强行连成一句。‘考察’与第 4 页‘考虑’中的‘考’的对照及宀、示笔形相符。末行阈值择优排作 $k\ge N$，另有 $k>N$ 候选，只差起点平移，均是逐点最终恒等。
>
> 定理名原形近 Borel Cantell，第二词末的 i 未明显成形；本文依可和失配事件的语境采用通行拼法 Borel–Cantelli。“几乎”后有大小不等的两组笔迹：第一组斜起、左短竖和右折，第二组点、叠折及下部卧钩。视觉与对抗复读较支持“任意”，故中等置信择优校读；数学复读提出“大组为在，右侧纵向小字疑为处处／旁补”的备选，另有径读“处处”候选。原两组形态不同于第 5 页两个近同形的“处”，不能称“处处”为清楚直读。候选及审阅分歧均保存，数学只确定整句表示全测度点的量词，不证明某一字值唯一。

## 第 7 页

本物理页为空白页。整页与六个重叠区均无正文、页码、旁注、图形或原待填标记。
