# RA12 对抗审计独立盲读

原件为本目录向上两级的 source.pdf，SHA-256 为 832de7c38426479bae23211cf7474ea637963941d73ccc3cb5ce7d35be6f9065。观察者为本轮工具线程 /root/ra12_adversarial。按物理页顺序用 view_image 逐页先看整页，再逐张查看 400 dpi 六区。以下先于两份现稿和现有台账对照保存。括注“ 似 ”或“字形”是读图判断，暂不作数学订正。闭记号均写在子集号上方。

## p0001

**布局。** 上方留白后是题头和三条；例题自左伸到右，结论居中偏左；下半页为开覆盖 Lemma、逆像证明、闭覆盖附论和定义，最后一行以内收尾。

**按行观察。**

1. “Littlewood 3 定律”。1. 每一个可测集几乎是有限个开区间并。2. 每一个可测函数几乎连续。3. 每个可测收敛函数列几乎一致收敛。
2. EX：设 $E\in\mathcal M$，$m(E)<+\infty$，$\forall\varepsilon>0$，$\exists I_i,\ldots,I_n$ 开区间 s.t. $m(E\Delta(\bigcup_{i=1}^n I_i))<\varepsilon$。首个区间下标有点，严格转写可留 $I_i$ 形。
3. Lemma：设 $f:X\to Y$。取 $X$ 之一个开覆盖，$X=\bigcup_{i\in I}X_i$（并号下的指标集合字形草写）；若 $\forall a\in A$，$f_a:X_a\to Y$ 连续，则 $f:X\to Y$ 连续。
4. $f^{-1}(U)=\bigcup_{a\in A}(f^{-1}(U)\cap X_a)\overset{\text{定义}}{=}\bigcup_{a\in A}((f\restriction_{X_a})^{-1}(U))$。第一处逆像的上标窄小，后两个同位置可比。下注“注意到 $f\restriction_{X_a}$ 连续”，$(f\restriction_{X_a})^{-1}(U)\in\tau_{X_a}=V\cap X_a,\ V\in\tau_X$（纸面未明写族的花括号）；由 $X_a$ 都 $\in\tau_X$，$V\cap X_a$ 是 $X$ 中开集。末端有收笔样的结束记号。
5. “但即使是闭覆盖。无限个，但改成局部有限闭覆盖。”紧接“即：给定 $x\in X$，$\exists U\in N(x)$，$U$ 仅与有限个 $X_a$ 相交。可测函数逼近，要求可数个覆盖。”开、闭覆盖在视觉上是分开的语句。

| 区域 | 首见 | 末见 | 核对内容 | 边缘与连续性 |
| --- | --- | --- | --- | --- |
| p0001-r1c1 | Littlewood 3 定律 | EX 行的全称量词起笔 | 三条分别含“有限个开区间并”“几乎连续”“几乎一致收敛”，例题有 $E\in\mathcal M$ 与 $m(E)<+\infty$ | 右接 r1c2 的“并”及 $\varepsilon$；底与 r2c1 重合 EX，标题上方空。 |
| p0001-r1c2 | 第一条尾部“间并” | EX 行的 s.t. | $\forall\varepsilon>0$ 后有存在号及开区间，首个 $I$ 的下标有一点形；无其他标题 | “间并”来自 r1c1，同一 EX 续 r2c2，右上与两行之间大片空。 |
| p0001-r2c1 | EX、$m(E)<+\infty$ | “注意到”行上缘 | 对称差和有限并不等式，Lemma 的 $f:X\to Y$、$f_a:X_a\to Y$ 以及第一段逆像逆标和“定义” | Lemma 开覆盖与等式右端在 r2c2，区底注语接 r3c1，左缘完整。 |
| p0001-r2c2 | $\forall\varepsilon>0$ 及区间串 | 子空间拓扑式的上缘 | “一个开覆盖”、$X=\bigcup X_i$、结论箭头及 $((f\restriction_{X_a})^{-1}(U))$ 的上标 | 符号续 r2c1，右侧各行尾部后为空，子空间拓扑式接 r3c2。 |
| p0001-r3c1 | “注意到 $f\restriction_{X_a}$ 连续” | “可测函数逼近，要求可数个覆盖” | $\tau_X$，交集开性，闭覆盖无限项，局部有限的邻域 $U\in N(x)$ | “局部有限”和相交条件右侧在 r3c2，页脚无后续字。 |
| p0001-r3c2 | $\tau_{X_a}$ 式的交集尾部 | 最后一行“覆盖”尾字 | $V\cap X_a$ 是 $X$ 中开集、行末结束记号、“局部有限闭覆盖”、只与有限个 $X_a$ 相交 | 同 r3c1 合读，右下页边空。 |

## p0002

**布局。** 上方题头 Lusin，前两行题面从左延至近右侧，第三行提出构造；中段 (1) 简单函数，近底一条跨整页误差估计，再起 (2)。

**按行观察。**

1. “Lusin”（草写接近 LuSin）。设 $f$ 是 $E$ 上 a.e. 有限的可测函数，$\forall\delta>0$，$\exists F_\delta\subset E$（闭）；满足 $m(E\setminus F_\delta)<\delta$，s.t. $f\restriction_{F_\delta}\in C(F_\delta)$；“并给出闭集构造 $F_\delta$ 的表达式”。
2. Pf. (1) $f\in S(E)$，$\exists E_1,\ldots,E_\ell\in\mathcal M$，s.t. $E=\bigcup \chi_i$（并号右侧字形像带下标的叉形 χ 或 X，前后的 $E_i$ 另有横画；数学上应为 $E_i$）。$f=\sum_{i=1}^{\ell}c_i\chi_{E_i}$。
3. $\forall\delta$，由 Lebegue（原拼写形）测度内正规性，$\exists F_{i\delta}\subset E_i$（上注“紧闭”），s.t. $m(E_i\setminus F_{i\delta})<\delta/\ell$；令 $F_\delta=\bigcup_{i=1}^{\ell}F_{i\delta}$。
4. $m(E\setminus F_\delta)=m(E\setminus\bigcup F_{i\delta})=m(\bigcup_{i=1}^{\ell}(E_i\setminus F_{i\delta}))=\sum m(E\setminus F_{i\delta})<\delta$。最后求和内的 $E$ 下方看不见附 $i$。
5. (2) $f\in\mathcal M(E)$；则 $\exists\{\varphi_k\}\subset S(E)$，s.t. $\lim_{k\to\infty}\varphi_k(x)=f(x),\ \forall x\in E$。证明接第 3 页。

| 区域 | 首见 | 末见 | 核对内容 | 边缘与连续性 |
| --- | --- | --- | --- | --- |
| p0002-r1c1 | Lusin | “构造 $F_\delta$ 的表达式” | a.e. 有限、可测、$m(E\setminus F_\delta)<\delta$ 及限制符起笔 | 题头上空，右接 r1c2 的量词和 $C(F_\delta)$，底与 r2c1 重合。 |
| p0002-r1c2 | “测函数”尾与 $\forall\delta>0$ | “式”尾画 | $\exists F_\delta\subset E$ 的“闭”上注，$f\restriction_{F_\delta}\in C(F_\delta)$ | 公式左端与 r1c1 共读，右大半无另注。 |
| p0002-r2c1 | 构造“表达式”行上缘 | “令 $F_\delta$”及并号上标 | $f\in S(E)$、和式的 $c_i\chi_{E_i}$、内正规性、“紧闭”及 $F_{i\delta}\subset E_i$ | $E_\ell$ 和误差上界在 r2c2，底续 r3c1。 |
| p0002-r2c2 | “式”尾画 | $m(E_i\setminus F_{i\delta})<\delta/\ell$ | $E=\bigcup$ 后是叉形，下标有一点，和前面 $E_\ell$ 不同；$\delta/\ell$ 清楚 | 与 r2c1 拼接，右边中下大片空，非另题留空。 |
| p0002-r3c1 | “令 $F_\delta=\bigcup F_{i\delta}$” | 简单函数序列及 $\lim$ 起笔 | (1) 第一、第二个误差等号，(2) 的 $f\in\mathcal M(E)$ 与 $\varphi_k$ | 误差后半和逐点极限接 r3c2，证明接 p0003 顶。 |
| p0002-r3c2 | 误差式第二项尾括号 | $\lim_{k\to\infty}\varphi_k(x)=f(x),\forall x\in E$ | 有限并之后是等号，末项肉眼为 $\sum m(E\setminus F_{i\delta})<\delta$ | 纵向两行之间空白无笔迹，结尾与 p0003 连续。 |

## p0003

**布局。** 由页 2 最末的简单函数序列直接续写；中段先有 Egorov 有限测度提示，再有有界化；底部退回有限测度的 Egorov 路线，地脚短横。

**按行观察。**

1. “由 (1) $\forall\delta,\forall k\in\mathbb N^*$”起，$F_\delta\subset E$（闭），s.t. $m(E\setminus F_k)<\delta/2^k$，且 $\varphi_k\in C(F_k)$。第一处末角看似 $\delta$，后同段反复写 $F_k$。
2. 令 $F_\delta=\bigcap_{k=1}^\infty F_k$，则 $m(E\setminus F_\delta)=m(\bigcup_{k=1}^\infty E\setminus F_k)\le\sum\delta/2^k$。$\varphi_k$ 在 $F_k$ 上连续、在 $\bigcap F_k$ 上连续，“下证一致收敛”。旁接“但 Egorov 要求 $m(E)<+\infty$”。
3. 因 $f$ a.e. 有限，$m(E(\lvert f\rvert=+\infty))=0$。令 $g(x)=f(x)/(1+\lvert f(x)\rvert)$，则 $g$ 有界；$\lvert f(x)\rvert=\lvert g(x)\rvert/(1-\lvert g(x)\rvert)$；下一行 $f(x)=g(x)/(1-g(x))$（该行分母两侧初看没有竖线），右边重复“$g(x)$ 有界”。
4. “或用 Egorov 定理”。当 $m(E)<+\infty$，$\exists\varphi_k\to f$；$\forall\delta>0,\ \exists F_\delta\subset E$（闭），s.t. $m(E\setminus F_\delta)$ 后有一短横待填。与 p0004 的 Gδ 部分连续。

| 区域 | 首见 | 末见 | 核对内容 | 边缘与连续性 |
| --- | --- | --- | --- | --- |
| p0003-r1c1 | “由 (1)” | $\varphi_k$ 在交集连续的左半 | $\forall\delta,\forall k\in\mathbb N^*$、闭子集、$\varphi_k\in C(F_k)$；交集和 $E\setminus F_\delta$ 并集估计 | 首行承 p0002，右续 r1c2，页顶空。 |
| p0003-r1c2 | $E$ 与 s.t. | “下证一致收敛” | 严格小于 $\delta/2^k$、闭集交、测度前是 $\le$ 形 | 区左接 r1c1，右边无独立字；底端与 r2c2 共见。 |
| p0003-r2c1 | $\varphi_k$ 在 $F_k$ 连续 | “或用 Egorov 定理”上轮廓 | Egorov 有限测度条件、a.e. 有限与无穷值事件、有界化公式、分母无绝对值的第二个逆式 | 含绝对值的第一个逆式在 r2c2，末尾接 r3c1。 |
| p0003-r2c2 | $\bigcap F_k$ 上连续及下证一致 | 第二个“有界”尾部 | 无穷值事件等于零及 $\lvert f(x)\rvert=\lvert g(x)\rvert/(1-\lvert g(x)\rvert)$ | 该式两只边竖可与 r2c1 无竖的第二式对照；图右半无字。 |
| p0003-r3c1 | “或用 Egorov 定理” | 末行 $m(E\setminus F_\delta)$ 的左部 | 有限测度、大括点 $\exists\varphi_k\to f$、闭集上注与 $\delta>0$ | 末行右接 r3c2 的短横，页 4 上方接续 Egorov。 |
| p0003-r3c2 | 末行 $m(E\setminus F_\delta)$ 右部 | 同行短横 | 横线单独置于右括号后，未写阈值 | 上和下大片无迹，单独横线非页码或裁区线。 |

## p0004

**布局。** 上半接 Egorov，两处横线和闭集构造；中段为两行误差和展开；下段另起无限测度，最后以“需要用局部有限性质”收尾。

**按行观察。**

1. “同 Egorov.”，$\exists G_\delta\subset E$ s.t. $m(E\setminus G_\delta)$ 后短横；$\varphi_k$ 在 $E\setminus G_\delta$ 上写“一致”样简记和 $f$。集合差在 m 行与收敛行均可见。
2. “考虑 $F_\delta\cap(E\setminus G_\delta)$ 由可测的内正规性。” $H_\delta\subset E\setminus G_\delta$（闭），$m((E\setminus G_\delta)\setminus H_\delta)<$ 后有明确长横留填。$\widehat F_\delta=F_\delta\cap H_\delta$。
3. “要求” $m((E\setminus F_\delta)\cup(E\setminus H_\delta))$ 下一行 $<m(E\setminus F_\delta)+m(E\setminus H_\delta)$。其后 $E\setminus H_\delta=(E\setminus G_\delta\setminus H_\delta)\cup(G_\delta\setminus H_\delta)$。正文对 $m(E\setminus F_\delta)$ 第一项的连接号为偏小于形。
4. $m(E)=+\infty$。$A_k=B(0,k)\setminus B(0,k-1)$。$E=\bigcup_{k=1}^\infty(A_k\cap E)$，“但在 $A_k\cap E$ 上取有一个闭集”（前一字为“但”形，句意清楚）；“需要用局部有限性质”。

| 区域 | 首见 | 末见 | 核对内容 | 边缘与连续性 |
| --- | --- | --- | --- | --- |
| p0004-r1c1 | “同 Egorov” | $H_\delta$ 是闭子集及误差式起笔 | $G_\delta\subset E$、两行重复的 $E\setminus G_\delta$、第一短横、考虑交集 | 区右续 r1c2 的内正规性及长横；页顶空，承 p0003。 |
| p0004-r1c2 | 一致行的 $f$ 尾 | $m((E\setminus G_\delta)\setminus H_\delta)<\underline{\phantom{x}}$ | “由可测的内正规性”，长横在小于号右侧，末端完整 | 右上、右边空白；长横与 r2c2 重复。 |
| p0004-r2c1 | $H_\delta$ 闭子集行下缘 | $E\setminus H_\delta$ 展开式至并号 | 帽子 $\widehat F_\delta$，误差的并及左尖比较号，第一个差写连续两个差符 | 最后一式右接 r2c2，底部切入 m(E) 新段前的空隙。 |
| p0004-r2c2 | 双差小于与长横 | $\cup(G_\delta\setminus H_\delta)$ | 长横有明确端点，中间两行是 r2c1 的括号尾，展开保留 $G_\delta\setminus H_\delta$ | 行间及右侧空，公式均由左栏延来。 |
| p0004-r3c1 | $m(E)=+\infty$ | “需要用局部有限性质” | 两球的半径 $k$、$k-1$，$k=1$ 起可数并，闭集句头 | 闭集句与 r3c2 拼接，段后为空，p0005 另起结论。 |
| p0004-r3c2 | $B(0,k-1)$ 末尾 | “在 $A_k\cap E$ 上…一个闭集” | 重复可见交符、闭集后句点 | 大片右边及底边空，局部有限句完整在 r3c1。 |

## p0005

**布局。** 左上独立一句 Lusin 逆定理，下方 Th. 三条横向，Remark 右端近纸边，下一行单列 $C=A\cup B$，下半页新定理及三个编号。

**按行观察。**

1. “Lusin 逆定理也成立”。
2. Th. 设 $(X,\tau)$（拓扑第二符形似 $\tau$ 或 $t$），则“下述等价”。(1) $X$ 正规。
3. (2) $\forall E\subset X$（闭），若 $f\in C(F)$，则 $\exists F\in C(X)$ s.t. $F\restriction_E=f$；下有 “(Tietze)” 附注。$C$ 括号内的字在分区图貌似 $F$，与同笔 $E$ 有区别。
4. (3) $\forall A,B\subset X$（闭），$A\cap B=\varnothing$，则 $\exists$ 连续函数 $f:X\to[0,1)$（右端曲形，括号种类需回图） s.t. $f\restriction_A=0$，且 $f\restriction_B=1$。括注名形 “UrySo/len” 可依数学名识别为 Urysohn，原拼写待核。
5. Remark “外测度中用到”，接 $m^*(A\cup B)$，再接疑似“所以/所…”，至“$A$ 和 $B$ 可被可测集分”附近贴右纸边。右字后是否有“离”字不能从整页读出，下一行为 $C=A\cup B$。
6. 第二个 Th. 设 $f$ 是 $E$ 上几乎处处有限函数，$E\in\mathcal M$。三条依次为 (1) $f$ 可测；(2) $\exists\{\varphi_k\}\subset S(E)$ s.t. $\varphi_k\to f$ 逐点；(3) $\exists\{\varphi_k\}\subset C(\mathbb R^n)$ s.t. $\varphi_k\xrightarrow{\text{a.e.}} f$。第三条的 $f$ 定义域仍为 $E$。本段标题行未见再次写“等价”，p0006 起头注明 (1)⇒(3)。

| 区域 | 首见 | 末见 | 核对内容 | 边缘与连续性 |
| --- | --- | --- | --- | --- |
| p0005-r1c1 | “Lusin 逆定理也成立” | (2) $f\in C(F)$ | 定理开头 $(X,\tau)$、(1)“X 正规”、(2) 中 $E$ 上的“闭”字与 $C(F)$ 字形 | 标题与定理间是普通段间空；“等价”尾与延拓式续 r1c2。 |
| p0005-r1c2 | “下述等价”尾 | $F\restriction_E=f$ | $\exists F\in C(X)$、限制到 $E$，右端为小写 $f$ | 右上整块空；公式延自 r1c1 并与 r2c2 重复。 |
| p0005-r2c1 | (2) 左侧重复 | “Th. 设 $f$ 是 $E$ 上几乎处处… ”上沿 | Tietze 括注、闭集 $A,B$ 与空交、零和一的限制、Remark 开头、下一行 $C=A\cup B$ | 两条等价命题均延到 r2c2，第二定理接 r3c1。 |
| p0005-r2c2 | (2) 延拓结论尾 | 第二定理题面的“有限函数，$E\in\mathcal M$”上沿 | $f:X\to[0,1)$ 样端点、Urysohn 括注、外测度式星号、Remark 右边“可测集分”样笔迹 | Remark 字伸至图像右外缘，右尾不能补作直接字迹；与 r2c1 的独立 $C$ 行相接。 |
| p0005-r3c1 | 第二个 Th. | (3) $\{\varphi_k\}\subset C(\mathbb R^n)$ 与 s.t. | (1) 仅可测，(2) 写“逐点”两字，(3) 字母与 (2) 形相同 | 题面和末尾 a.e. 箭头续 r3c2，证明接 p0006。 |
| p0005-r3c2 | “有限函数，$E\in\mathcal M$” | $\varphi_k\xrightarrow{\mathrm{a.e.}} f$ | 第 (2) 项只见行尾 s.t.，第 (3) 项上标 a.e. 清楚 | 下方无未填横线，左段与 r3c1 接读。 |

## p0006

**布局。** 开头写 (1)⇒(3)，前半集合和连续延拓，后半 Borel-Cantelli 与集合式，主要文字偏左；考虑事件一行在物理左侧还有残笔，末行下方空。

**按行观察。**

1. Pf. (1)⇒(3)。$\exists g\in C(\mathbb R^n)$，$g\restriction_{F_\delta}=f$。$\forall k\in\mathbb N^+$，$\exists F_k\subset E$（闭），$g_k\in C(\mathbb R^n)$，$g\restriction_{F_k}=f$（第二个限制左边也未见 $g$ 的下标笔画）；$m(E\setminus F_k)<1/2^k$。
2. “由 Borel C…tell…”，$m(\limsup_{n\to\infty}E_n)=0$。左边缘一个近“虑”的重复/残写，主行“考虑 $E\{g_k\ne f\}\subset E\setminus F_k)$”中括号不规范，核心关系可辨。
3. “仍有” $m(\limsup_{k\to\infty}E(g_k\ne f))=0$。
4. $m(\bigcap_{n=1}^\infty\bigcup_{k=n}E(g_k\ne f))=0$（该处内并上标初见无 $\infty$）。下一行“（几乎处处）” $x\in\bigcup_{n=1}^\infty\bigcap_{k=n}^\infty E(f=g_k)$。末 $\exists N(x)$ s.t. $k>N,\ f=g_k$ 恒等。上式交在外并在内，下式相反；两类事件符号 $\ne$ 与 $=$ 也互补。

| 区域 | 首见 | 末见 | 核对内容 | 边缘与连续性 |
| --- | --- | --- | --- | --- |
| p0006-r1c1 | Pf. (1)⇒(3) | $m(E\setminus F_k)<1/2^k$ | $g\in C(\mathbb R^n)$，$F_k$ 闭子集，$g_k$ 自身带下标与量词自然数 | 延拓等号在 r1c2；接 p0005 三条件，页顶空。 |
| p0006-r1c2 | $g\restriction_{F_\delta}=f$ 右半 | $g\restriction_{F_k}=f$ | 第二式左 $g$ 与第一同形，下标在限制线右方的 $F_k$，与中段 $g_k$ 区分 | 右侧和区底空，两式左端接 r1c1。 |
| p0006-r2c1 | 几何误差行上缘 | $m(\bigcap\bigcup E(g_k\ne f))$ 上缘 | Borel-Cantelli 名字及 $E_n$，考虑事件包含，第二个 $\limsup$ 的下标；左边单笔组似“虑” | 考虑行贴左缘，等号末端横接 r2c2，展开接 r3c1。 |
| p0006-r2c2 | 包含式右侧 $F_k)$ | 展开测度式零的顶部 | 本区只有左边公式尾，$=0$，之后都与左栏相接 | 中央与右区域整片空，公式尾均来自 r2c1。 |
| p0006-r3c1 | $\bigcap_{n=1}^\infty\bigcup_{k=n}$ | $\exists N(x)$ s.t. $k>N$ 后的 $f$ 起笔 | 两种交并次序（内并未见上端指数）、$\ne$ 对 $=$，括注“几乎处处” | 公式右端和“恒等”接 r3c2，页底大片空。 |
| p0006-r3c2 | 测度式末 $=0$ | $f=g_k$ 恒等 | 交内相等事件右括号，与最末收敛阈值行分离 | 中右侧与整页脚空，p0007 无续笔。 |

## p0007

**布局。** 物理第七页存在，整页无标题、正文、图形、横线、页码或可辨淡笔迹。页 6 的最后一行在页 6 完结。六区逐张核对角、边、中心及重合带。

| 区域 | 首见 | 末见 | 核对内容 | 边缘与连续性 |
| --- | --- | --- | --- | --- |
| p0007-r1c1 | 无 | 无 | 左上角、全宽上半左列及左侧，无字或标题 | 右、下重合带空，纸面均匀。 |
| p0007-r1c2 | 无 | 无 | 右上角、上半右列及右缘，无页码或擦痕 | 左侧与 r1c1、区底与 r2c2 连续空。 |
| p0007-r2c1 | 无 | 无 | 中心偏左及左页边，无箭头、公式或淡墨 | 与上/下左区和右区重叠部分均空。 |
| p0007-r2c2 | 无 | 无 | 中心偏右及右缘，无文字引线或旁注 | 与 r2c1、r1c2、r3c2 重合区空。 |
| p0007-r3c1 | 无 | 无 | 左下角、底栏左侧及底部居中，无页码或签名 | 与 r3c2 和 r2c1 连续空；页 6 公式未跨入。 |
| p0007-r3c2 | 无 | 无 | 右下角、最底与右侧，无续行、分隔线或待填线 | 与 r3c1 和 r2c2 连续空，物理页终止。 |
