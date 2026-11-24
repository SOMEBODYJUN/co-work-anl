# 实分析 10｜原稿保真转写

> 说明：本文件按 PDF 物理页序转写。黑色普通段落对应原稿可见内容。蓝色说明是编辑者对符号、上下文或数学结构的补充。红色片段表示原稿字迹或公式仍不能唯一恢复。原稿未提供对应旧稿。

## 第 1 页

来源：`RA10-P001`，整页图 `project/pages/p0001.png`，六个重叠分区 `p0001-r1c1` 至 `p0001-r3c2`。

- `B(X) → B(ℝ)`，Borel 可测。
- `Prop.` 可测函数的有限……
- `f` 的原像也是可测的；图中写有“原像可测/值域可测”一类说明。
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

<span style="color:red">[RA10-P001-U01] 命题标题中“有限……/原像……/值域……”的个别字形无法唯一恢复，保留原位置及候选。公式中的部分指标 `i,j` 与集合符号依据上下文恢复。</span>

## 第 2 页

来源：`RA10-P002`，整页图 `project/pages/p0002.png`，六个重叠分区 `p0002-r1c1` 至 `p0002-r3c2`。

- 页首原稿写有“对复合（或复函数），若 `∫ g`，取之连续/极限，求导”一类句子，原字迹不完整。
- `prop.` 可测函数的原像/原函数仍可测。
- 例：
  $$
  f:(X,\Sigma_X)\to(\overline{\mathbb R},\mathcal B(\overline{\mathbb R})),
  $$
  以及
  $$
  \Phi:(\overline{\mathbb R},\mathcal B(\overline{\mathbb R}))
  \to(\mathbb R,\mathcal B(\mathbb R)),
  $$
  原稿写“`Φ` 可测/保持可测”。
- 设 `f` 可测，原稿写出 `f^{-1}(B)` 与 Borel 集 `B` 的关系。
- 设一列投影 `π_n`，原稿写
  $$
  \pi_n:X\to X_n,
  \qquad
  \pi_n^{-1}(u_n)\subset X,
  $$
  并定义由这些原像生成的集合族 `𝒮`。
- 原稿写有
  $$
  \mathcal S=\{\pi_n^{-1}(u_n):n\in\mathbb N,\ u_n\in\bar X_n\}
  $$
  （其中 `\bar X_n` 的帽号/上划线是原稿笔迹）。
- 另写集合 `B` 为有限交形式
  $$
  B=\left\{\bigcap_{n\in F}\pi_n^{-1}(u_n):F\subset\mathbb N\text{ 有限}\right\}.
  $$

<span style="color:red">[RA10-P002-U01] 页首积分与极限句子无法逐字恢复；保留可辨认的“复合/积分/极限/可测”候选。`\bar X_n`、`u_n` 的帽号和下标按局部笔画及后页投影记号恢复。</span>

## 第 3 页

来源：`RA10-P003`，整页图 `project/pages/p0003.png`，六个重叠分区 `p0003-r1c1` 至 `p0003-r3c2`。

- 原稿写“取 `S,t`，所有这些……然后……”。`S,t` 可能是集合或参数名。
- 蓝/黑笔写出一个趋于零的量
  $$
  \varepsilon=\frac{\omega}{\bar n}
  $$
  （分母上方带 `n` 的上划线）。
- 对每个 `n∈ℕ`，原稿写
  $$
  \pi_n:X\to X_n
  \quad\Longrightarrow\quad
  \forall u_n\in\bar X_n,
  \pi_n^{-1}(u_n)\subset X.
  $$
- 定义圆柱集合族
  $$
  \mathcal S=\{\pi_n^{-1}(u_n):n\in\mathbb N,\ u_n\in\bar X_n\}.
  $$
- 写出 `u(S)=\bar u` 一类记号，以及
  $$
  \mathcal B
  =\left\{\bigcap_{n\in F}\pi_n^{-1}(u_n):F\subset\mathbb N\text{ 有限},\ u_n\in\bar X_n\right\}.
  $$
- 原稿逐项列出投影原像的有限交，例如
  $$
  \pi_1^{-1}(u_1)=X_1\times\cdots\times X_{n-1}\times\{u_1\}\times X_{n+1}\times\cdots,
  $$
  $$
  \pi_2^{-1}(u_2)=X_1\times\{u_2\}\times X_3\times\cdots,
  $$
  $$
  \pi_1^{-1}(u_1)\cap\pi_2^{-1}(u_2)=\{u_1\}\times\{u_2\}\times X_3\times\cdots.
  $$
- 页末写“整集有某种 `σ` 结构，令 `f`、`g` 为相应映射”，并说明每个投影原像属于 `𝒳`。

<span style="color:red">[RA10-P003-U01] 页首 `S,t`、`ω/\bar n` 与 `u(S)=\bar u` 的具体定义不清。圆柱集合的有限交和坐标位置可由后续公式恢复，但原稿中是否写到 `X_n` 或 `\bar X_n` 的上划线仍需回图复核。</span>

## 第 4 页

来源：`RA10-P004`，整页图 `project/pages/p0004.png`，六个重叠分区 `p0004-r1c1` 至 `p0004-r3c2`。

- 页首：`ℝ`；写有 `f: X→ℝ`。
- 原稿说明 `f` 与 Borel 集之间的可测性，并写“有界……为 Borel 可测/有界函数可测”一类句子。
- 写出
  $$
  \mathcal B(\mathbb R)=\sigma\bigl(\{(a,b):a<b\}\bigr)
  $$
  或等价的开区间生成形式。
- 蓝笔 `proof`。
- 原稿写无限乘积空间的投影
  $$
  X=\prod_{n=1}^{\infty}X_n,
  \qquad
  \mathcal E=\bigotimes_{n=1}^{\infty}\mathcal B(X_n).
  $$
- 定义
  $$
  F:(X,\mathcal M)\longrightarrow
  \left(\mathbb R,\bigotimes_{n=1}^{\infty}\mathcal B(\mathbb R)\right),
  $$
  并说明对每个坐标投影 `π_n`，复合
  $$
  f_n=\pi_n\circ F
  $$
  可测。
- 原稿继续写“可测 `⇔` 对每个 `n`，`F_n(X_n,\mathcal M)→(ℝ,mathcal B(ℝ))` 可测”，并得到 `F_n=π_n∘F`。
- 令
  $$
  D=\{A\subset\mathbb R:A\text{ 为 Borel 集}},
  $$
  写出 `D` 是 `σ`-代数且含有各坐标原像，因而包含乘积 `σ`-代数。
- 页末写“连续映射/投影的逆像仍可测”，并列出
  $$
  \bar\pi_1^{-1}(u_1)=X_1\times\cdots\times X_n,\qquad
  \bar\pi_2^{-1}(u_2)=X_1\times X_2\times\cdots,
  $$
  以及有限交的圆柱形式。

<span style="color:red">[RA10-P004-U01] 页首“有界……Borel 可测”的主语和“`\mathcal E`/`\mathcal M`”的字形不完全清晰。乘积 `σ`-代数及坐标投影公式为直接可读与上下文恢复混合。</span>

## 第 5 页

来源：`RA10-P005`，整页图 `project/pages/p0005.png`，六个重叠分区 `p0005-r1c1` 至 `p0005-r3c2`。

- `例：` 对每个 `n`，原稿写
  $$
  F_n:(E,\mathcal M)\to(\mathbb R,\mathcal B(\mathbb R))
  $$
  均为可测函数。
- 定义坐标映射
  $$
  \Phi:(E,\mathcal M)\to
  \left(\mathbb R^{\mathbb N},\bigotimes_{n=1}^{\infty}\mathcal B(\mathbb R)\right),
  $$
  并写“由坐标函数可测，`Φ` 可测”。
- 另一行写
  $$
  \int g\,d\mu\quad\text{或}\quad\int f\,d\mu
  $$
  与 `max(g)`、`min(f)` 一类极值记号，原稿句子未完成。
- 设
  $$
  f:(\mathbb R^{\mathbb N},\otimes\mathcal B(\mathbb R))\to\mathbb R,
  \qquad
  x=(x_1,\ldots,x_n,\ldots),
  $$
  定义
  $$
  S(x)=\sup_{n\ge1}x_n.
  $$
- 原稿写 `S` 为 Borel 可测，并以开射线原像证明，下一页继续。
- 另有例：`f:(\bar E,\mathcal M)→ℝ`，并写“`f` 为 Borel 可测”；页边保留“可积/可测”字样。

<span style="color:red">[RA10-P005-U01] “积分与 `max/min`”的段落缺少上下文，不能确认是例题还是旁注。`\mathbb R^{\mathbb N}` 的上标和乘积 `σ`-代数是由前后页恢复。</span>

## 第 6 页

来源：`RA10-P006`，整页图 `project/pages/p0006.png`，六个重叠分区 `p0006-r1c1` 至 `p0006-r3c2`。

- 继续证明 `S(x)=\sup_{n\ge1}x_n` 的 Borel 可测性。原稿写
  $$
  S^{-1}((a,+\infty))
  =\{x=(x_1,\ldots,x_n,\ldots):\sup x_n>a\}
  $$
  以及
  $$
  S^{-1}((a,+\infty))
  =\bigcup_{n=1}^{\infty}\pi_n^{-1}((a,+\infty)).
  $$
- 因为右端是可数并的圆柱集合，得到 `S` 可测。
- 原稿写
  $$
  f_n:E\to\mathbb R\quad\text{均可测},
  $$
  从而
  $$
  \sup_{n\ge1}f_n
  $$
  可测。
- 蓝笔写“`f∘S` 可测”或“`f,S` 可测”的补充。
- 页末写“`inf` 同理”。

<span style="color:red">[RA10-P006-U01] 第一行左端的区间端点是 `(a,+∞)` 还是 `[a,+∞)`，以原图看更接近开射线，故按 `(a,+∞)` 转写。若原稿确实使用闭射线，证明需改为 `\bigcap_{m\ge1}\bigcup_n\pi_n^{-1}([a+1/m,+\infty))` 等价形式。</span>

## 第 7 页

来源：`RA10-P007`。页面整体接近空白，仅见扫描边缘/浅色痕迹，未发现可读数学正文。六个区域均已保留于 manifest，作为空白页证据记录。
