# 实分析 10｜原稿保真转写

> 说明：本文件按 PDF 物理页序转写。黑色普通段落对应原稿可见内容。蓝色说明是编辑者对符号、上下文或数学结构的补充。红色片段表示原稿字迹或公式仍不能唯一恢复。原稿未提供对应旧稿。

## 第 1 页

来源：`RA10-P001`，整页图 `project/pages/p0001.png`，六个重叠分区 `p0001-r1c1` 至 `p0001-r3c2`。

- `B(X) → B(ℝ)`，Borel 可测。
- `Prop.` 可测函数的原像也是可测的。
- 图中随后写有 `f^{-1}(\cdot)` 的原像可测说明；邻接的集合有限并和指标公式属于同一证明。
- `proof`（蓝笔）。
- 取一列集合 `F_1, …, F_n`，令 `E = ⋃_{j=1}^n F_j`。原稿接着写“任意 `x∈E` …”及有限并/有限交的说明。
- 令 `E_i` 为一族可测集合，原稿给出
  $$
  E=\bigcup_{j=1}^{n}E_j,
  $$
  并写出 `E_i` 的指标与 `x` 的归属关系。
- 蓝笔补充了有限并的记号，并写有
  $$
  E_j=\bigcup_{i=1}^{n}E_{ij},
  $$
  以及“可测”的结论。
- 原稿底部写有“例：……”但后续内容在下一页继续。

<span style="color:#1f5fbf">[RA10-P001-U01 已解决] 600 dpi 定向/紧裁图读作“可测函数的原像也是可测的”，并由相邻 `f^{-1}(\cdot)`、`proof` 与有限并公式完成前向/反向核验；“有限线性组合”保留为被排除候选。</span>

## 第 2 页

来源：`RA10-P002`，整页图 `project/pages/p0002.png`，六个重叠分区 `p0002-r1c1` 至 `p0002-r3c2`。

- 页首是关于复合映射连续性/可测性的短句，能辨出“复合”“连续/可测”等词，但具体积分、极限方向及完整条件不能逐字恢复。
- 原稿继续讨论若 (f) 可测，复合映射（图中出现 (Phicirc f) 一类记号）保持可测；复合顺序及对象的个别帽号按疑字保留。
- 页中下部可辨出乘积拓扑的起始记号
  \[
  (X_n,\tau_n),\qquad X=\prod_{n=1}^{\infty}X_n,
  \qquad \bar\pi_n:X\to X_n,
  \]
  以及 (x\mapsto\bar\pi_n(x)) 的坐标投影说明。
- 页底写有“下一页继续”式的乘积空间/投影接续。完整的投影逆像族与有限交公式在第 3 页出现，不能提前归入本页。

<span style="color:red">[RA10-P002-U01] 页首复合、连续/可测短句的积分或极限词序不能唯一恢复；保留可辨关键词，不把标准定理写回黑色原文。</span>

## 第 3 页

来源：`RA10-P003`，整页图 `project/pages/p0003.png`，六个重叠分区 `p0003-r1c1` 至 `p0003-r3c2`。

- 页首有 `S,t` 开头的短行及一个含求和/并集样式的未定记号；原图不支持确定写成 (\varepsilon=omega/\bar n)，故不作唯一恢复。
- 中段清楚出现带上划线的坐标投影逆像
  \[
  \bar\pi_n^{-1}(u_n)\subset X,
  \qquad
  \mathcal S=\{\bar\pi_n^{-1}(u_n):n\in\mathbb N, u_n\in\bar X_n\},
  \]
  以及有限交族
  \[
  \mathcal B=\left\{\bigcap_{n\in F}\bar\pi_n^{-1}(u_n):F\subset\mathbb N\text{ 有限}\right\}.
  \]
  上划线、帽号和 (u_n) 的具体对象按图面保留为候选。
- 原稿逐项列出
  \[
  \bar\pi_1^{-1}(u_1)=\{u_1\}\times X_2\times X_3\times\cdots,
  \qquad
  \bar\pi_2^{-1}(u_2)=X_1\times\{u_2\}\times X_3\times\cdots,
  \]
  及其交集
  \[
  \bar\pi_1^{-1}(u_1)\cap\bar\pi_2^{-1}(u_2)
  =\{u_1\}\times\{u_2\}\times X_3\times\cdots.
  \]
- 页下半部可辨出
  \[
  \bar X=\prod_{n=1}^{\infty}\bar X_n,
  \]
  以及 (f,g) 与逐坐标投影逆像有关的映射行；蓝笔写有逐 (n) 的可测性判据和 `proof`。具体 (\bar\Sigma)、映射方向及上划线位置不能完全定稿。

<span style="color:red">[RA10-P003-U01] 页首 `S,t` 与未定求和/并集符号、以及页下 `\bar X_n`、`\bar\pi_n` 的帽号和映射方向仍有疑字；不以数学标准式替换。</span>

## 第 4 页

来源：`RA10-P004`，整页图 `project/pages/p0004.png`，六个重叠分区 `p0004-r1c1` 至 `p0004-r3c2`。

- 页首进入扩展实数列空间，能辨出
  \[
  \overline{\mathbb R}^{\mathbb N}=\{f:\mathbb N\to\overline{\mathbb R}\}
  \]
  一类对象及其 Borel/乘积 \(\sigma\)-代数记号。
- 主体讨论映射
  \[
  F:(X,\mathcal M)\longrightarrow
  (\overline{\mathbb R}^{\mathbb N},\bigotimes_{n=1}^{\infty}\mathcal B(\mathbb R)),
  \]
  并写“\(F\) 可测当且仅当各坐标函数 \(F_n=\pi_n\circ F\) 可测”。
- 蓝笔定义
  \[
  D=\{A\subset\overline{\mathbb R}^{\mathbb N}:F^{-1}(A)\in\mathcal M\},
  \]
  并通过
  \[
  F^{-1}(\pi_n^{-1}(u_n))=(F_n)^{-1}(u_n)\in\mathcal M
  \]
  说明 (D) 含有坐标生成族，进而包含乘积 \(\sigma\)-代数。
- 本页未见前页那样的 `\bar\pi_1^{-1}(u_1)`、`\bar\pi_2^{-1}(u_2)` 显式乘积展开；这些只在第 3 页按图保留。

<span style="color:red">[RA10-P004-U01] 扩展实数列空间的具体 Borel 记号及 (D) 的上下标有轻微疑字；黑色只保留图面可辨对象，标准乘积写法另见学习稿蓝色补充。</span>

## 第 5 页

来源：`RA10-P005`，整页图 `project/pages/p0005.png`，六个重叠分区 `p0005-r1c1` 至 `p0005-r3c2`。

- `例：` 对每个 (n)，原稿写 (F_n:(E,\mathcal M)\to(\mathbb R,\mathcal B(\mathbb R))) 均为可测，并以坐标函数构造 \(Phi\)；复合可测的主线清楚。
- 坐标映射可辨为
  \[
  \Phi:E\to\mathbb R^{\mathbb N},
  \qquad
  \Phi(x)=(F_1(x),F_2(x),\ldots),
  \]
  并写由坐标函数可测得到 (Phi) 可测。
- 黑笔随后讨论可测函数的复合、\(\max(f,0)\)、\(\min(f,0)\)、\(|f|\) 的可测/可积方向，具体句子未完成；不能确定为完整积分公式。
- 页下有 (f:[0,1]\to\mathbb R) 的二值函数例，按图可见为在两个子集/区间上取不同常值的分段定义；集合名和端点不唯一，保留“二值分段例”而不擅自展开。
- 页末定义
  \[
  S(x)=\sup_{n\ge1}x_n,
  \qquad x=(x_1,x_2,\ldots),
  \]
  下一页继续其可测性证明。

<span style="color:red">[RA10-P005-U01] 可测运算与二值函数例子的部分集合名、端点和复合顺序无法唯一恢复；原稿没有足够证据支持具体积分式。</span>

## 第 6 页

来源：`RA10-P006`，整页图 `project/pages/p0006.png`，六个重叠分区 `p0006-r1c1` 至 `p0006-r3c2`。

- 继续证明 (S(x)=\sup_{n\ge1}x_n) 的可测性。前两行清楚写出
  \[
  S^{-1}((a,+\infty))
  =\{x:\sup_n x_n>a\}
  =\bigcup_{n=1}^{\infty}\pi_n^{-1}((a,+\infty)).
  \]
- 右端为可数并的坐标原像，故 (S) 可测；原稿下方写“\(\inf\) 同理”。
- 末项在图面更接近
  \[
  \bar\pi_n^{-1}((-infty,a])
  \]
  的闭射线/反向射线写法，与前两行的开射线方向不一致，作为疑点保留，不强行统一。
- 蓝笔写有 (S) 与函数复合可测的说明，方向可能是 (S\circ f) 或 (S\circ F)，不确定；学习稿只使用正确的一般复合定理。
- 页末无新的独立内容。

<span style="color:red">[RA10-P006-U01] 末项区间端点和方向、蓝笔复合的左右顺序与前两行不完全一致；标准开射线证明放在学习稿蓝色补充，不能冒充图面原式。</span>

## 第 7 页

来源：`RA10-P007`。页面整体接近空白，仅见扫描边缘/浅色痕迹，未发现可读数学正文。六个区域均已保留于 manifest，作为空白页证据记录。
