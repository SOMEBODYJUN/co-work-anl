# RA12 数学上下文恢复报告

角色为数学上下文恢复员，实际线程 /root/ra12_math，模型 gpt-6.2-sol / max。先独立通过整页、6 区重叠图和从 PDF 重新渲染的定向图完成原件观察，在打开两份旧工作稿、台账、审计和待恢复记录之前保存了 [own-source-observations.md](own-source-observations.md)，SHA-256 为 58b9b97a6d205dbe153d8753f77d29f304646da4ed89abccfaed39edd681e36d。逐区范围是 p0001–p0007 与每页 r1c1、r1c2、r2c1、r2c2、r3c1、r3c2。第 7 页全白。16 个新图的 PDF 页坐标、dpi、哈希和路径见 [crop-index.json](crop-index.json)。

结论为全页全区核对且有新发现。三条原报数学含义均可恢复。原稿存在多处实际省笔、错式和三个明确留空，需在保真稿原地存留，在复习稿逐处补证或订正。第 5 页右边界可见到“可测集分”，可按上下文恢复“分隔”的语义，卷面剩余墨迹无从确认。Urysohn 右界笔形近圆括，数学命题必用闭区间。

## 现有版本与标识

| 核对对象 | 实际读到的 SHA-256 |
| --- | --- |
| source.pdf | 832de7c38426479bae23211cf7474ea637963941d73ccc3cb5ce7d35be6f9065 |
| manifest.json | eac453760dc29b8a0c66f3cb89c07bd6f9f062a0fc0095fe67fcea405c9f4219 |
| source-transcript.md | 91eedd11e0cb5c512ba7e7aa5203038b29ee1508ae9cb8eadbd9669d7afc13ce |
| study-notes.md | afd2c2d18f11f1a4844bdcbe21a65d9280f236c81a5f7e5c2ecae16d6fa4ef14 |
| ledger.json | 7f9c28d79264d469389bbd09f1eb166ee4c816a5847142d92924bfbabd8c8b17 |
| audit-report.json | 01f6478a85ff12e457895a8dfe1a58abaffac1eebac368cfa6ebc815af3cd9d7 |
| current.json | 37c5031492fe584ee15dadc4f918262f4a03b11562bbd0e28cb9077fc2782030 |
| autonomous-recovery/recovery-plan.json | 2945fd84392b0c25abb8b0cb7258addabe9305b7c1b488a6c598abbe50ff4253 |

两份状态报告均指向快照 9f47081baf13fe48c5d23ca673d53e14acbe8ec66e34fe3ac6a78ffb3e0ff901，三条 open issue 和终审轮数不足。当前 ledger 仅有按物理页整页装入的七条源条目，恢复记录尚空。旧正文内的 U04/U02 等疑字定位标是语义位置，需要随重切源单元实际绑定。两份既有工作稿在本轮作为待订正材料，真实上传旧 Markdown 为空。

## RA12-P001-U04，开覆盖上的限制映射

**回图。** 页 1 底引理陈述和紧邻原像式的新 800 dpi 图中，先有右向 $f:X\to Y$，后有 $f_\alpha:X_\alpha\to Y$、则 $f:X\to Y$ 连续。$X$ 有一个开覆盖，原纸上行用 $i$ 型下标，后切为 $\alpha$ 型。原像式有 $-1$、与 $X_\alpha$ 的交，以及明确的 $f|_{X_\alpha}$。最后关于 $C\cap X_\alpha$ 的解释以 $\tau_X$ 和“$X$ 中开集”收束。原图右箭头、原像和承载开覆盖的空间三者一致。

| 候选 | 证据和判断 |
| --- | --- |
| A．已定义 $f:X\to Y$，$\{X_\alpha\}$ 是 $X$ 的开覆盖；$f_\alpha=f|_{X_\alpha}:X_\alpha\to Y$ 连续，则 $f$ 连续 | 首尾直接可读。限制关系由同一页明写的 $f|_{X_\alpha}$、原像和取交推知。置信度很高。 |
| B．覆盖属于 $Y$，局部箭头形如 $Y_\alpha\to X$ 或 $f|_{f^{-1}(Y_\alpha)}$ 仅随目标分片连续 | 局部 $Y$ 的连笔容易被旧式误判为反向。开覆盖句、$X=\bigcup_iX_i$ 和 $f^{-1}(U)\cap X_\alpha$ 都把分片定位在定义域。 |
| C．原稿把若干事先任取的 $f_\alpha$ 直接并起来定义 $f$，而相交处没有一致性条件 | 未写拼接选择，作者直接“设 $f$”。独立局部映射另需在重叠处一致，原像公式本身以既有 $f$ 为前提。 |

**正向。** 令 $U$ 为 $Y$ 中任意开集。$\{X_\alpha\}$ 覆盖 $X$，故 $f^{-1}(U)=\bigcup_\alpha(f^{-1}(U)\cap X_\alpha)=\bigcup_\alpha(f|_{X_\alpha})^{-1}(U)$。每一项是 $X_\alpha$ 中开集，等于 $C_\alpha\cap X_\alpha$，$C_\alpha$、$X_\alpha$ 都在 $X$ 中开；于是原像开。有限模拟取 $X=\{0,1,2\}$、两片 $\{0,1\},\{1,2\}$、$f$ 值 $7,9,7$、$U=\{7\}$，Python 得全局原像和局部并同为 $\{0,2\}$。

**逆向。** 从 $f$ 连续可通过取交恢复各受限映射的连续性。若按目标覆盖读到“局部映射连续”，取 $X=\mathbb R$、$Y=\{0,1\}$ 离散、$f=\mathbf1_{[0,\infty)}$。两个目标开单点的原像上限制各为常数，两片原像未必在 $X$ 中开，原 $f$ 在 0 不连续。若直接胶合任取函数，给交点两个不同值即可否决。页 4 用原稿闭覆盖变式处理环带各自得到的闭集，也排除了需对靶空间开覆盖的读法。

**两稿。** 原序保留开覆盖、原式、子空间行、局部有限闭覆盖及“可测也类似”旁注。$\tau_{X_\alpha}=C\cap X_\alpha$ 原式应保留，严格含义为 $\tau_{X_\alpha}=\{C\cap X_\alpha:C\in\tau_X\}$。学习稿补局部有限闭覆盖证明，供 p4 的无限测度 Lusin 分块调用。

## RA12-P003-U01，$\varphi_k$、$F_k$ 与连续限制

**回图。** 页 2 底按 (2) 写 $\{\varphi_k\}\subset S(E)$ 及 $\lim_k\varphi_k(x)=f(x)$，旁标 $\forall x\in E$。页 3 的 800 dpi 首图第一行量词可读“由 (1) $\forall\delta,\forall k\in\mathbb N^*$”，闭 $\subset E$ 左侧字面似 $F_\delta$，同一行的误差式直接见 $F_k$ 与 $2^k$。紧下一行 $\varphi_k\in C(F_k)$ 和 $F_\delta=\bigcap_{k\ge1}F_k$ 可读。第二张图清楚重复“$\varphi_k$ 在 $F_k$ 上连续。$\varphi_k$ 在 $\bigcap F_k$ 上连续，$f$ 还一致收敛”。后写有界化和“或用 Egorov 定理”，保留为不同论证路线。

| 候选 | 证据和判断 |
| --- | --- |
| A．应用简单函数步骤给每个 $\varphi_k$ 取一块闭的 $F_k\subset E$，$\varphi_k\in C(F_k)$ 是限制写法；所有闭块取交得到 $F_\delta$ | 字面 $C(F_k)$、后重复两次“上连续”，并接 p4 Egorov 取好集。数学语义置信很高。首行的 $F_\delta/F_k$ 省笔另录，在原序可两者并存。 |
| B．$\varphi_k\in C(E)$，或每个 $F_k$ 上连续的直接是 $f$ | $C(\cdot)$ 内有 F 和下标。页 2 (1) 只对给定简单函数生效，页 3 只从逐点极限连接到一般 $f$。 |
| C．由同一个固定 $F_\delta$ 一次满足所有 $m(E\setminus F_\delta)<\delta2^{-k}$，或全部简单函数只须逐点收敛便在共同闭集一致 | 第一行 $F_\delta$ 容易被误解为固定同一块。右侧 $F_k$、各 $k$ 求交、后文 Egorov 和变换说明每项先另选闭块，再解决一致收敛。 |

**正向。** 对已经给定的 $\delta>0$ 和每个 $k$，在简单函数步骤里用误差 $\delta/2^k$，得到闭 $F_k\subset E$、$m(E\setminus F_k)<\delta/2^k$ 及 $\varphi_k|_{F_k}\in C(F_k)$。令 $F_\delta=\bigcap_kF_k$，因 $F_\delta\subset F_k$ 有 $\varphi_k|_{F_\delta}\in C(F_\delta)$，而
$$
m(E\setminus F_\delta)\le\sum_{k\ge1}m(E\setminus F_k)<\sum_{k\ge1}\delta2^{-k}=\delta.
$$
严格号可由首项严格、其余项弱上界得出。对有界 $g$ 取水平网格量化，$\psi_k=2^{-k}\lfloor2^kg\rfloor$ 有限值、统一误差小于或等于 $2^{-k}$，相应 $F_\delta$ 上才能用一致极限定理。对无界 $f$ 先保留原稿 $g=f/(1+|f|)$ 路线或有限测度 Egorov 路线。

**逆向。** $E=[2,3]\cup\{0,1,1/2,\ldots\}$，令 $\varphi_k$ 为有限孤立点集 $\{1/j:1\le j\le k\}$ 的示性函数。可取每个 $F_k=E$，$\varphi_k$ 在整个共同闭域连续，误差集测度 0。逐点极限 $f=\mathbf1_{\{1/j:j\ge1\}}$ 在 0 不连续，在 $1/(k+1)$ 上误差始终为 1；Python 检过 $(k,x)=(1,1/2),(3,1/4),(7,1/8),(15,1/16)$。因此逐点逼近配逐项连续不会自动产生一致收敛。若把首行同一个固定 $F_\delta$ 代进所有递减误差界，则须 $m(E\setminus F_\delta)=0$。对 $E=[-1,1]$，一个闭的满测度子集只能为 $E$，在 $x=0$ 的阶跃即反例。

**两稿。** 原序写“$\varphi_k\in C(F_k)$”并存紧接的口语两句、第一行字面 $F_\delta$ 与右端 $F_k$。学习稿用 $\varphi_k|_{F_k}\in C(F_k)$，明确量词和共同闭集。不要把现稿加的 $G_k=\bigcap_{j\le k}F_j$ 说成作者的必要步骤。还原 p3 中部原稿两种逆式。$|f|=|g|/(1-|g|)$ 正确，另一个 $f=g/(1-g)$ 对 $f<0$ 失效，例如 Python 以 $f=-2$ 得 $g=-2/3$，误式给 $-2/5$，修正式 $g/(1-|g|)$ 给 $-2$。应在蓝色块修为后者，并说明删 $\{|f|=\infty\}$ 后逐点 $|g|<1$ 保证可连续反变换。

## RA12-P006-U02，Borel–Cantelli 邻行的谓词集

**回图。** 页 6 中部 800 dpi 选区可见先写 $m(\limsup_{n\to\infty}E_n)=0$，再“考虑 $E\{g_k\ne f\}\subset E\setminus F_k)$”。左式的 1200 dpi 放大中，$E$ 与 $g_k$ 之间只有一条带上、下转折的左界笔迹，右端有相配的右界。未见像右侧 $E$ 与 $F_k$ 中间的独立直竖差集号。下方 800 dpi 裁图可见 $E(g_k\ne f)$ 与 $E(f=g_k)$ 成对，先 $\bigcap_n\bigcup_{k\ge n}$，再“（几乎任意）”$\bigcup_n\bigcap_{k\ge n}$。最后 $N(x)$ 和“恒等”保留。先行 $E_n$ 上横与手写 E 顶横同式，可在蓝块明确取 $E_k=E\setminus F_k$。

| 候选 | 证据和判断 |
| --- | --- |
| A．$E\{g_k\ne f\}=E(g_k\ne f)=\{x\in E:g_k(x)\ne f(x)\}$，所写包含是 $E(g_k\ne f)\subset E\setminus F_k$ | 谓词左右括界和后两行的相反谓词有直接证据，集合的外显写法属上下文恢复，置信度很高。 |
| B．$E\setminus\{g_k\ne f\}\subset E\setminus F_k$ | 容易把左括界的一条长笔当差集，但 1200 dpi 见连续转折。语义会把有相等保证的 $F_k$ 放进误差集，且后面交并和谓词反而矛盾。 |
| C．左边是 $E(g_k=f)$，或 Borel–Cantelli 只对 $\liminf$ 失配成立 | 旁注 $\ne$ 的穿刺与下一段“$f=g_k$”的两横不同。作者将零测集合展开为交后并，正好对应 $\limsup$。 |

**正向。** 页 5 条件 (1) 接 Lusin 与 Tietze 得 $g_k|_{F_k}=f|_{F_k}$，所以失配集 $D_k=E(g_k\ne f)\subset E\setminus F_k$。页 6 的新预算是 $m(E\setminus F_k)<2^{-k}$，每个尾并的测度至多 $\sum_{k\ge N}2^{-k}$，故 $m(\bigcap_N\bigcup_{k\ge N}D_k)=0$。在该零测集的相对补集，$x\in\bigcup_N\bigcap_{k\ge N}E(f=g_k)$，即从某项起 $g_k(x)=f(x)$。原句 $k>N(x)$ 和规范式 $k\ge N(x)$ 可由指数起点换算。

**逆向。** 从几乎任意 $x$ 终究相等反推，该点恰落在末行好集并交中，故坏集必须是 $D_k$ 的上极限。有限检验取 $E=\{0,1,2\},F_k=\{0,1\},f=0,g_k(0)=g_k(1)=0,g_k(2)=1$。Python 得 $D_k=E\setminus F_k=\{2\}$，候选 B 的左集合为 $\{0,1\}$，包含失败。把“仅有限次失配”和“一直未永久失配”区分也可逐点检验。若某点在偶数项失配，它不在 $\liminf D_k$，却仍出现无穷次失配，故仅 $\liminf$ 零测不能推出最终恒等。

**两稿。** 保真保留 $E_n$、$E\{g_k\ne f\}$、两步零测、好集并交及 $N(x)$ 结尾。学习稿给失配谓词的定义并将 $g|_{F_k}=f$ 的原稿漏下标归于蓝订正。在 $\mathbb R^n$ 上延拓得到的是整列 $g_k$ 在 $E$ 上几乎处处最终成立逐点恒等，因而几乎处处极限，后面无统一的 $N$ 假设。原预算 $2^{-k}$ 为新选 $\delta_k$，与 p3 的独立估计各有用途。

## 逐页新问题与修订落点

| 页 | 现稿位置 | 原图与数学核对 | 建议 |
| --- | --- | --- | --- |
| 1 | 转写 7–29、学习 20–39 | 三原则从可测集、可测函数、可测收敛函数列依次排列。例要求有限个开区间且用对称差 $\triangle$。开、局部有限闭粘合及可测旁注漏失，页底并非控制有界函数的例题。 | 按原顺序修正例，用开覆盖的有限首段估计两个差集的并，补开/闭粘合和可数可测覆盖证明。 |
| 2 | 转写 35–64、学习 43–85 | 定理原述未限 $m(E)$；首行明确闭 $\subset E$。简单函数取 $c_i$，有限并和下方原错误链漏失，内正规性明写。$E=\bigcup X_i$ 的交叉字形与 $E_i$ 有别。 | 黑色保留字形代用、错误测度链和各项上界，在蓝块取 $\ell$ 个不交值层 $E_i$，以 $\bigcup (E_i\setminus F_{i,\delta})$ 订正。 |
| 3 | 转写 68–112、学习 87–128、176–182 | 交的各块与下标、原文“还一致收敛”均有笔迹，旧稿的递减 $G_k$ 及“实值函数连续”旁注缺原图依据。存在有界化两行逆式，后另起 Egorov。底部横线是空位。 | 见 U01 恢复，补有界路线，记录原无绝对值式，新增对其订正，保留页末一项红色空位并与下页两项一起按误差分配。 |
| 4 | 转写 116–141、学习 174–192 | 现稿省失 $G_\delta$ 例外、$H_\delta$ 内正规逼近、$\widehat F_\delta$、并集估计、$E\setminus H_\delta$ 的分解。$E=\bigcup (A_k\cap E)$ 明写。左右普通空白无证明分隔线。 | 两根明确待填线应红标。保证 $m(G_\delta)<\delta/3$，原空第一式 $m(E\setminus G_\delta)>m(E)-\delta/3$。联合上界规范为 $\le$，$G_\delta\setminus H_\delta=G_\delta$。环带这一段完成全局 Lusin，依赖闭粘合与各块可求和预算。 |
| 5 | 转写 145–173、学习 196–232 | 原题是 $(X,\tau)$ 三条等价。$X$ 正规、Tietze、Urysohn 都直接可读，$f\in C(F)$ 的 F 确为两横，右边 $F\in C(X)$、$F|_E=f$。Urysohn 余域笔形近 $[0,1)$。Remark 是外测度与“可被可测集分…”及 $C=A\cup B$。第二定理为 a.e. 有限、简单函数逐点、$\mathbb R^n$ 连续函数 a.e.。 | 删旧稿 $x\in A$、$(A,\mu)$ 和紧方块 $I^n$ 的误读；黑色保留 $C(F)$ 与区间原笔形，蓝色明确 $C(E)$ 和 $[0,1]$。补正规三等价、外测度可测分隔、Lusin 逆、可测性三等价各证。不要把原稿未写的 Tietze 证明用红色标成待填。 |
| 6 | 转写 177–202、学习 234–255 | $\mathrm{Pf.}(1)\Rightarrow(3)$、$g\in C(\mathbb R^n)$ 及 $g_k$、$\forall k\in\mathbb N^*$、原第二个限制式 $g$ 缺 k。尾部 $x$ 相关 $N(x)$、逐点最终恒等，而非稿中的一致收敛或另取 $g$。 | 见 U02 恢复。数学稿完整保留交并反转、$\limsup$ 证明和最终恒等，即使直接用 $E\setminus F_k$ 作异常集也应同时保留失配集合原行。 |
| 7 | 转写 204–206、学习 268–270 | 整页和六个重叠区白，无接续。 | 保留普通来源描述。 |

## 附加边界检验

- 简单情形的原链 $E\setminus(\bigcup_iF_{i,\delta})=\bigcup_i(E\setminus F_{i,\delta})$ 失效。Python 用计数版 $E=\{0,1,2\}$、$E_1=\{0\},E_2=\{1,2\},F_1=\{0\},F_2=\{1\}$，左侧 $\{2\}$，原写全局差集的并 $\{0,1,2\}$，用值层差集 $E_i\setminus F_i$ 的并恢复 $\{2\}$。类比 Lebesgue $E=[0,1]\cup[2,3]$、$F_i=E_i$ 时，原链左 0，原并为 $E$，严格矛盾。
- 第 4 页可把预算分成三项各 $\delta/3$。若以 $E\setminus G_\delta$ 为小集，则 $F_\delta\cap H_\delta$ 也只落在小集内，无法覆盖大部 $E$。在 $E=[0,1]$、$\delta<1/2$ 时，若同时要求 $m(E\setminus G_\delta)<\delta$ 与 $m(E\setminus(F_\delta\cap H_\delta))<\delta$，由 $F_\delta\cap H_\delta\subset E\setminus G_\delta$ 得两部分测度和小于 1，矛盾。原稿第一界值可以按保留符号的等价下界补完。
- $\bigcup(E\setminus F_k)$ 的测度未必为零，页 6 正确是交后并的尾部上极限。Egorov 对无限测度集没有这条全局一致结论，例如 $[0,\infty)$ 上 $\mathbf1_{[k,\infty)}$ 逐点趋 0，而删任一有限测度集后每项仍存在值 1。第 4 页环带论证目标是限制函数连续。
- 三个真实原缺项的位置为 p3 最后 $m(E\setminus F_\delta)$ 后、p4 第一行 $m(E\setminus G_\delta)$ 后、p4 的 $m((E\setminus G_\delta)\setminus H_\delta)<$ 后。P5 字迹歧义用中性位置或所见笔形说明，普通空白不作为待填。
