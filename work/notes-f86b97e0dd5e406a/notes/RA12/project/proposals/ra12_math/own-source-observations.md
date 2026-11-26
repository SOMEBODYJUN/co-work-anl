# RA12 原件独立观察

数学上下文恢复员 /root/ra12_math，模型 gpt-6.2-sol / max。独立阶段读取了任务、项目规程、原件的 manifest 图像定位、原 PDF 的物理页及生成的裁图。正文、既有台账、恢复计划与他人报告尚未打开。原件 SHA-256 为 832de7c38426479bae23211cf7474ea637963941d73ccc3cb5ce7d35be6f9065。物理页 7 页。整页先看，区域后看，以下 42 个区域和所列 16 个放大裁图均以 view_image 实际查看。颜色意义在成稿处理，以下保留原稿写法及观察强度。文中的 $E$ 大多用离体顶横书写，勿普遍误作 $\bar E$。差集的手写竖线按 $\setminus$ 排版，在关键歧义处另外说明。

## p0001

全页从 Littlewood 三定律起，下接有限个开区间的例题，底半为开覆盖判连续的 Lemma、原像证明、局部有限闭覆盖的变式和可测性一句。没有图表，开集说明末有画过的证毕式涂记。

- r1c1：头部白边后为 Littlewood 3 定律，逐行是每个可测集几乎是有限个开区间并、每个可测函数几乎连续、每个可测收敛函数列几乎一致收敛。底端例题左部 $E\in\mathcal M$、$m(E)<+\infty$，接 r1c2、r2c1。
- r1c2：大片白边中只有第一条的“间并”尾与例题另一半。$\forall\varepsilon>0$，存在 $I_1,\ldots,I_n$ 开区间，接下一行对称差。两个符号是斜曲线形的手写 $I$。
- r2c1：例题再次出现于重叠最上，核对 $m(E\triangle(\bigcup_{i=1}^{n}I_i))<\varepsilon$。Lemma 起始为设 $f:X\to Y$，右向箭头，第一出现的 $Y$ 上叉与下干分两笔。下行直接见 $f_\alpha:X_\alpha\to Y$。等式左为 $f^{-1}(U)$，并集第一项为 $f^{-1}(U)\cap X_\alpha$，旁标“定义”。
- r2c2：例题右段与 r1c2 重叠。Lemma 上行“[由/且] $X$ 有一个开覆盖，$X=\bigcup_{i\in I}X_i$”；下行右部“则 $f:X\to Y$ 连续”；并集内为 $(f|_{X_\alpha})^{-1}(U)$。两行的覆盖索引写法切换，数学变量可在学习稿统一。最下与 r3c2 共见子空间拓扑的 $C\cap X_\alpha$、$C\in\tau_X$。
- r3c1：从“注意 $f|_{X_\alpha}$ 连续”起。下一行 $X_\alpha$ 本身属于 $\tau_X$；$C\cap X_\alpha$ 的开性说明越到右区。下写“但开换成/是闭覆盖。无限个，便/但改成局部有限闭覆盖”；“即，给定 $x\in X$，$\exists U\in\mathcal N(x)$”；末行更像“可测也类似，要求可取（一个）覆盖”。后无指定空位。
- r3c2：子空间拓扑行的右部和“$X$ 中开集”及笔形证毕记号。其下“改成局部有限闭覆盖”，$U$ 只与有限个 $X_\alpha$ 相交，末尾为“个覆盖”，白边结束。比较新裁图后确认“相交”，并非“包含有限个”。

放大回图中，Lemma 开覆盖属于 $X$，诸箭头均向共同的 $Y$。$f_\alpha=f|_{X_\alpha}$ 由后面明画的限制竖线与复合原像等式恢复。子空间拓扑那行表面写 $\tau_{X_\alpha}=C\cap X_\alpha,\ C\in\tau_X$，把单个开集和开集族并写。词形与数学意思在拟稿分别落地。

## p0002

全页“Lusin”命题后分 (1) 简单函数、(2) 一般可测函数，(2) 的逐点逼近去下页继续。原稿在此处还没有写有界变换和 Egorov。

- r1c1：页首留白，Lusin 标题，$f$ 在 $E$ 上 a.e. 有限、Lebesgue 可测，$m(E\setminus F_\delta)<\delta$ 左半，“开始，闭集构造 $F_\delta$ 的表达式”。
- r1c2：接定理的“可测函数”后半，$\forall\delta>0$，$\exists F_\delta$ 闭 $\subset E$，以及 $f|_{F_\delta}\in C(F_\delta)$。“表达式”尾重叠，其余白。
- r2c1：开始一行的左部与 r1c1 重合，(1) $f\in S(E)$，$f=\sum_{i=1}^{\ell} c_i\chi_{E_i}$，由 Lebesgue 测度内正规性取 $F_{i,\delta}\subset E_i$，上方“紧/闭”笔迹叠连，$F_\delta$ 并集下半越下区。
- r2c2：接 $E_1,\ldots,E_\ell\in\mathcal M$，右方原稿 $E=\bigcup X_i$ 风格的交叉字母，形状与 p1 $X_i$ 同、与同一行 $E_i$ 不同；宜保留原式，在数学稿明确取值层 $E_i$。核对 $m(E_i\setminus F_{i,\delta})<\delta/\ell$，右下白。
- r3c1：$F_\delta=\bigcup_{i=1}^{\ell}F_{i,\delta}$；差集估计第一半，再出现 (2) $f\in\mathcal M(E)$，$\{\varphi_k\}\subset S(E)$，$s.t.$ 后接右区。
- r3c2：原测度链写了 $m(\bigcup_{i=1}^{\ell}(E\setminus F_{i,\delta}))=\sum_i m(E\setminus F_{i,\delta})<\delta$，前述 $F_\delta$ 是并集，链中没有把并改成交的字迹，也没有把此行 $E$ 写成 $E_i$。末有 $\lim_{k\to\infty}\varphi_k(x)=f(x),\ \forall x\in E$，没有一致字样。

## p0003

上接 p2 的逐点简单逼近。第一段用闭集交保证各项连续，再问如何一致收敛；其后写 Egorov 的有限测度条件、有界化公式、另用 Egorov 的有限测度路线。末留一根紧接 $m(E\setminus F_\delta)$ 的填空横线，续 p4。不是空白物理页。

- r1c1：顶留白后，“由 (1) $\forall\delta,\forall k\in\mathbb N^*$”；标题行字面在闭 $\subset E$ 前像 $F_\delta$，与同一行差集中的 $F_k$ 并写，未见清楚的 $\exists$ 独立笔形；次行“则 $\varphi_k\in C(F_k)$”“令 $F_\delta=\bigcap_{k=1}^{\infty} F_k$”，跨 r1c2。估计有 $E\setminus F_\delta$ 与并差集。底部“$\varphi_k$ 在 $F_k$ 上连续”接 r2c1、r1c2。
- r1c2：第一行清楚见 $m(E\setminus F_k)<\delta/2^k$；第二行重复闭集交右部；第三行其右部为小于等于式样与 $\sum\delta/2^k$。最下“$\bigcap F_k$ 上连续，$f$ 还一致收敛”连左区。
- r2c1：顶部连续性与上一格重叠，继写 Egorov“要求 $m(E)<+\infty$”。再写 $f$ a.e. 有限和 $m(E(\lvert f\rvert=+\infty))=0$ 的简略字形。$g(x)=f(x)/(1+|f(x)|)$，则 $g$ 有界。下一行 $f(x)=g(x)/(1-g(x))$ 分母没绝对值，旁写 $g(x)$ 有界。末端“或用 Egorov 定理”越至下区。
- r2c2：连续性末字和有限性零测式右端之后大部白；原图的绝对值逆式 $|f(x)|=|g(x)|/(1-|g(x)|)$ 在此，双竖笔与下一行无双竖笔形成鲜明对照。
- r3c1：“或用 Egorov 定理”，先 $m(E)<+\infty$，$\exists\varphi_k\to f$，“$\forall\delta>0,\ \exists F_\delta$ 闭 $\subset E$”，测度差在底端跨右区。
- r3c2：白区中近下端仅 $m(E\setminus F_\delta)\underline{\quad}$ 右尾，横线无界值和小于号。

## p0004

有限测度的 Egorov 证明继续。顶部 $G_\delta$，闭集 $H_\delta$，再取 $\widehat F_\delta$，三项估计可以接住原稿的两个待填线（上缘 $m(E\setminus G_\delta)$ 后、$m((E\setminus G_\delta)\setminus H_\delta)<$ 后）。底部另讨论 $m(E)=+\infty$，使用环带和局部有限性。

- r1c1：顶部白边后“用 Egorov，$\exists G_\delta\subset E$ s.t.”，下一行 $m(E\setminus G_\delta)\underline{\quad}$，再是 $\varphi_k$ 在 $E\setminus G_\delta$ 上“一致 $f$”，说明 $G_\delta$ 承担例外集。考虑 $F_\delta\cap(E\setminus G_\delta)$，右接“由可测的内正规性”，闭的 $H_\delta\subset E\setminus G_\delta$ 左部在区末。
- r1c2：头部基本空白，从“一致 $f$”最后的 $f$ 开始有字；“由可测的内正规性”；$m((E\setminus G_\delta)\setminus H_\delta)<\underline{\quad}$ 的明显长线，右白边收束。
- r2c1：顶部和 r1c1 相接。$\widehat F_\delta=F_\delta\cap H_\delta$，以及要求估计 $m((E\setminus F_\delta)\cup(E\setminus H_\delta))$，原稿下一行手写严格 $<$。其下 $E\setminus H_\delta=((E\setminus G_\delta)\setminus H_\delta)\cup(G_\delta\setminus H_\delta)$ 跨 r2c2。
- r2c2：顶部重叠含第三空线；用上确界限的两行右括号在左侧；末为分解式的 $G_\delta\setminus H_\delta$；其他留白。
- r3c1：换到 $m(E)=+\infty$，$A_k=B(0,k)\setminus B(0,k-1)$；$E=\bigcup_{k=1}^{\infty}(A_k\cap E)$；底行“需要用局部有限性”，相承 p1 的闭粘合变式。
- r3c2：仅环带定义右尾和“在 $A_k\cap E$ 上的一个闭集”的右部，最后无红色待填标记。环带本身未标闭，后续用的是包含其中的闭集。

## p0005

从“Lusin 逆定理也成立”开始。上为正规空间、Tietze、Urysohn 三等价；旁记外测度和可测分隔；下为 a.e. 有限函数可测的三等价，第三条件的证明续往 p6。

- r1c1：白边后“Lusin 逆定理也成立”，下为 “Th. 设 $(X,\tau)$，则下述等价”，(1) $X$ 正规，(2) $\forall E$ 闭 $\subset X$，若 $f\in C(F)$ 开头。
- r1c2：广大空白中“等价”结尾、(2) 右式 $\exists F\in C(X)$ s.t. $F|_E=f$，与下一行 (Tietze) 相接。
- r2c1：(2) 中 $f\in C(F)$ 的字母是竖加两横、无 E 的底横，800 dpi 亦如此。(3) $A,B$ 闭且不交；核对 $f|_A=0$、$f|_B=1$。Remark “外测度中[用到]”越到右区，下一行 $C=A\cup B$；区底是下一个定理开端。
- r2c2：拓扑 (2) 右版与 r1c2 重叠；(3) 明画向右箭头 $f:X\to$ 区间，左符号有离体短横和下托，右符号曲笔似 $)$，1200 dpi 仍缺独立右上横，与 0、1 的赋值连读应两端含。页边 “$m^*(A\cup B)$，所谓 $A$ 和 $B$ 可被可测集分”可见到“分”，右端几乎抵纸边，不能认定原稿又写了最后“隔/开”字。
- r3c1：第二个定理条件“设 $f$ 是 $E$ 上几乎处处有限函数，$E\in\mathcal M$”；(1) $f$ 可测；(2) $\{\varphi_k\}\subset S(E)$ 且逐点趋于 $f$；(3) $\{\varphi_k\}\subset C(\mathbb R^n)$。末公式右半跨 r3c2。
- r3c2：接 $E\in\mathcal M$，中间白；最下 (3) 为 $\varphi_k\xrightarrow{\mathrm{a.e.}}f$，箭头上 a.e. 清楚，未出现一致字样。$\mathbb R^n$ 手写似普通 R。

## p0006

从 $\mathrm{Pf.}\ (1)\Rightarrow(3)$ 起，Lusin 的 $F_\delta,F_k$ 和连续延拓 $g,g_k$，用 Borel–Cantelli 及补集写成最终在几乎每一点恒等。本页没有一致收敛或仅有子列结论。左边贴页边有一笔字，右大半留白，底部正常留白。

- r1c1：白边后 “Pf. $(1)\Rightarrow(3)$”，$\exists g\in C(\mathbb R^n)$ 且 $g|_{F_\delta}=f$；$\forall k\in\mathbb N^*$ $\exists F_k$ 闭 $\subset E,\ g_k\in C(\mathbb R^n)$，下方 $m(E\setminus F_k)<1/2^k$。
- r1c2：接左右跨区的限制式 $g|_{F_\delta}=f$，第二行看见写成 $g|_{F_k}=f$，同一行前一项是 $g_k$；限制的符号缺下标可以作为原稿省笔，复习稿明确写 $g_k|_{F_k}=f|_{F_k}$。其余白。
- r2c1：先重复估计右尾，再“由 Borel Cantell”及 $m(\limsup_{n\to\infty}E_n)=0$；下一行“[页边一字] 考虑 $E\{g_k\ne f\}\subset E\setminus F_k)$”。800/1200 dpi 看到 $E$ 后是一个形如左括号的弯折和对称右括界，之间无额外相交或差集算符。右侧 $E,F_k$ 间是与其他差集处相同的竖线。下一行的 $m(\limsup E(g_k\ne f))=0$ 跨右区；再下是交并展开。
- r2c2：最左只有 r2c1 旁注的 $F_k)$、$\limsup$ 等式的 $=0$，及下一行的 0 边缘，空段未发现其他笔迹。
- r3c1：$m(\bigcap_{n=1}^{\infty}\bigcup_{k=n}^{\infty}E(g_k\ne f))=0$。下一行手写“（几乎任意）$x\in\bigcup_{n=1}^{\infty}\bigcap_{k=n}^{\infty}E(f=g_k)$”。原稿确实交换并交并改换谓词。末行 $\exists N(x)\ \mathrm{s.t.}\ k>N$ 后接右区。
- r3c2：交并行 $=0$ 右部、等号谓词行的右括号、最后 $f=g_k$“恒等”；后半留白。

在 800 dpi 回图中，$E_n$ 顶端的短横与其他 $E$ 的顶横同式，不能仅凭上画一横理解成拓扑闭包。$E(g_k\ne f)$ 与 $E(f=g_k)$ 的成对用法支持“在 $E$ 上使谓词为真的点”的记法。仅当右边 $F_k$ 为相应 $g_k$ 的一致集时该包含直接成立。

## p0007

整页与六区两种尺度均只见白底，未见标题、文字、淡笔迹、边注、图形或待填标记。页 6 后没有继续证明。

- r1c1：左上白，页顶和中央的竖带均空。
- r1c2：右上白，与上一格交界也空。
- r2c1：左中及中心重叠区白。
- r2c2：右中及中心重叠区白。
- r3c1：左下至底边白，无末尾续写。
- r3c2：右下及底边白，无编号和角注。

## 放大裁图

16 个文件的页码、400 dpi 基准像素定位、800/1200 dpi 输出和哈希见 [crop-index.json](crop-index.json)。第 1 页 3 张是引理陈述、原像证明和局部有限，页 2 两张是层集与测度链，页 3 三张是 $\varphi_k$ 与域、连续性行、有界变换，页 4 两张是 Egorov 上段与误差式，页 5 三张是 Tietze 字母、Urysohn 余域、可测分隔，页 6 三张是 Borel–Cantelli 旁注、左集合符号及下方交并。第 5 页 Remark 右边缘及第 6 页旁注左边缘见实际贴页边，不凭数学猜补卷外墨迹。
