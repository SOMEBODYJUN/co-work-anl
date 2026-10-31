---
id: "unrelated-machines/afs-2008-santa-claus-hypergraph-matching"
kind: "resource"
type_tag: "资源"
title: "Santa Claus 超图匹配与配置 LP 五分之一界"
status: "retained-literature-read-directly"
summary: "Asadpour–Feige–Saberi 2008 作者稿；在 restricted assignment 的 max-min 分配中定义 configuration LP，并以二部超图匹配和局部搜索证明整数解至少达到 LP 值的 1/5；局部搜索步数并未证明为多项式。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/afs_2008_santa_claus_hypergraph_author.pdf#pp.1-11"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/afs_2008_santa_claus_hypergraph_author.pdf#pp.1-11"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:archives/unrelated-machines/state/定理/私有菜单树有界叶重数配置界--定理.md"
---

# Santa Claus 超图匹配与配置 LP 五分之一界

## 来源身份与实际阅读

冻结文件是 Arash Asadpour、Uriel Feige、Amin Saberi 的作者稿 *Santa Claus Meets Hypergraph Matchings*，日期 2008-06-17，共 11 个 PDF 页。两个冻结来源提交中的路径和字节相同；PDF SHA-256 为
7c95e2140f4180a2edd5affb1917589f75f707b231b5ce5295b9e677f9e501a6，文件大小 191277 字节。本次由 clean show --out 导出后使用 pdftotext -layout 和 PyMuPDF 逐页读取，核对了摘要、引言、configuration LP、Haxell 条件、Theorem 3、局部搜索证明、Theorem 6 及开放问题；不是只凭文件名或已有摘要登记。

本文是文献资源记录，不把作者稿中的结论改写成仓库自己的新定理。已存在的仓库正文“私有菜单树有界叶重数配置界”引用了其中的 Haxell Theorem 2 与 AFS Theorem 3；本页补充完整来源身份、模型范围、1/5 局部搜索结论及其运行时间边界。

## 模型和配置 LP

问题是不可分割物品的 max-min fair allocation。有限物品集合为 \(J\)，玩家集合为 \(P\)，玩家 \(i\) 的价值是线性的 \(f_i(S)=\sum_{j\in S}v_{ij}\)。本文重点是 restricted assignment：每个物品 \(j\) 有一个非负固有值 \(v_j\)，并给出可接受的玩家集合；因此 \(v_{ij}\in\{0,v_j\}\)。需要把物品分给玩家，使最小玩家价值最大，记整数最优值为 \(\mathrm{OPT}\)。

给定阈值 \(t\)，对玩家 \(i\) 只保留价值至少 \(t\) 的配置 \(S\)，配置变量 \(x_{iS}\) 满足

\[
\sum_S x_{iS}=1\quad(i\in P),\qquad
\sum_{i,S:j\in S}x_{iS}\le 1\quad(j\in J),\qquad
x_{iS}\ge0.
\]

配置 LP 的最大可行阈值记作 \(\mathrm{optLP}\)。每个整数分配给出 LP 可行点，所以 \(\mathrm{optLP}\ge\mathrm{OPT}\)。作者沿用 Bansal–Sviridenko 的事实：配置 LP 的值及任意精度可行解可在多项式时间内求得（作者稿没有在本文中重证该算法及所有位复杂度细节）。

## 文献结论

### 二部超图匹配条件

作者引用 Haxell 的定理：若二部超图 \(H=(U\cup V,E)\) 的每条边在资源侧 \(V\) 至多含 \(r-1\) 个点，且对每个 \(C\subseteq U\)，资源侧超图 \(H_C\) 的最小 transversal 大小满足

\[
\tau(H_C)>(2r-3)(|C|-1),
\]

则存在覆盖全部 \(U\) 的匹配。文献明确说这个 Haxell 证明本身是非构造性的；作者稿使用其作为 Section 2 的黑箱，并在 Section 3 给出自足的局部搜索版本。\(r=2\) 时该条件退化为 Hall 定理。

### 组合选择引理

Bansal–Sviridenko 的组合命题考虑 \(p\) 个集合族，每个候选集合大小为 \(k\)，每个底层元素至多出现在 \(l\) 个候选集合中。对每个族选择一个集合，并从中选子集，使每个子集大小至少 \(\beta k\)，且最终各子集两两元素不重叠。作者用上述 Haxell 条件证明

\[
\beta\le\frac{\lfloor k/3\rfloor}{k}
\]

时命题成立；当 \(3\mid k\) 时可取 \(\beta=1/3\)，而 \(k=5\) 的统一下界是 \(1/5\)。证明把每个玩家候选的所有 \(\beta k\)-子集作为超边，令 \(r=\beta k+1\)。对任意 transversal \(T\)，每个候选 \(k\)-集至少有 \((1-\beta)k\) 个元素在 \(T\) 中；按元素出现次数上界 \(l\) 计边数得到

\[
|T|\ge(1-\beta)k|C|
   =\frac{1-\beta}{\beta}(r-1)|C|,
\]

再用 \(\beta\le1/3\) 验证 Haxell 阈值。

### Restricted assignment 的 1/5 舍入

作者把配置 LP 阈值归一为 \(t=1\)。物品分为 fat（\(v_j>1/5\)）和 thin（\(v_j\le1/5\)）；fat 物品值在 LP 变换中截为 1。把每个玩家的正权配置删减为极小满足配置后，只剩两种形状：只含一个 fat 物品的 fat set，或只含 thin 物品的 thin set。对 thin set，枚举价值至少 \(1/5\) 的极小子集；极小性给出其总值至多 \(2/5\)。

据此构造二部超图：玩家是 \(U\) 侧，物品是 \(V\) 侧；fat set 给二元超边，thin set 的每个极小子集给一条超边。Theorem 4 声称该超图存在覆盖全部玩家的匹配，于是每位玩家得到 fat 物品或价值至少 \(1/5\) 的 thin 子集。Lemma 5 是关键：任意当前交替树都能在已触及的玩家中找到一条与当前资源集不相交的新边。证明按交替树内 fat/thin 边的数量分情况，利用 LP 权重守恒、fat 资源数及 thin 边单边至多 \(2/5\) 的值，迫使某个 thin 配置在删除已占资源后仍保留至少 \(1/5\) 的价值。

局部搜索从覆盖 \(n-1\) 个玩家的匹配开始。A 边是待加入边，B 边是当前匹配中阻塞 A 边的边；每条 A 边记录阻塞数 \(m_i\ge1\)。新边若不被当前匹配阻塞，就扩展匹配；若替换一个 B 边，则是 contraction，沿较早的 A 边回退并把相应 \(m_i\) 减一。把 \(m\)-向量补上足够大的末项作为 signature，扩展按字典序增大、收缩使较早坐标下降；总阻塞数有限，故签名不重复，搜索终止。作者给出从空匹配开始至多

\[
\sum_{|M|=0}^{n-1}2^{|M|}<2^n
\]

步（每次从 \(k\) 到 \(k+1\) 的扩展至多 \(2^k\) 次）的局部搜索上界。Theorem 6 因而得到一个达到 \(\mathrm{optLP}/5\) 的可行整数分配；Theorem 1 表述为配置 LP 估计 max-min 最优值达到 \(1/5-\varepsilon\)，其中 \(\varepsilon>0\) 来自配置 LP 只能任意精度求解而非精确求解。

## 证据强度、条件和缺口

1. **完整文献证明范围。** 本次实际读到上述定理和证明文本，文献内部的数学推导、超图构造及签名终止论证属于来源中的完整论证；本页不声称重新独立证明 Haxell 外部定理。
2. **算法时间。** 配置 LP 可在多项式时间内求近似值是作者沿用的前置结果；由局部搜索 signature 得到的是有限、指数上界的步数，作者明确说不知道该搜索在多项式步内收敛。因此它不是一个已知多项式时间的实际 \(1/5\)-近似分配算法。Theorem 1 的“估计”依赖先求 LP 值，作者的局部搜索只是有限但可能指数的舍入过程。
3. **模型边界。** 结论针对 restricted assignment 的线性、非负、不可分割物品；不能直接套到一般玩家物品值、可分物品、共享机器时间、六人 SPE 客户目录或终局均分模型。
4. **近似比方向。** 文献把配置 LP 相对整数最优的间隙表述为至多 \(1/5\) 的可获得比例（等价地 \(\mathrm{optLP}\le5\,\mathrm{OPT}\)），并将已知硬度下界写为不能优于 \(1/2\) 的历史背景。这里的 \(1/5\) 不是“已经证明存在 1/5 间隙实例”，也不是一般调度的 \(2-\varepsilon\) 结论。
5. **外部文献与新颖性。** 本页只登记作者稿及其内部引用（Bansal–Sviridenko、Feige、Haxell 等）的内容和用途；没有对引用论文做本轮逐篇独立核验，也不作全球新颖性或外审认证。

## 与仓库对象的衔接

- [私有菜单树有界叶重数配置界](../定理/私有菜单树有界叶重数配置界--定理.md) 复用 Haxell 型超图匹配阈值和 AFS 的“固定大小子集 + transversal 计数”思路；该对象自身的私有树、CONFIG 边际和 \(2-1/(\mu+2)\) 界由仓库正文承重，不因本资源自动推广到一般 restricted assignment。
- [有向需求与调度的压缩双向任务桥](../定理/有向需求与调度的压缩双向任务桥--定理.md) 使用不同的显式任务桥和 \(\mathrm{OPT}=2-b^*\) 恒等；AFS 文献只能作为 Santa Claus/超图匹配背景，不能替代该桥的两向构造或把其局部搜索当作一般 UM 算法。
- 已有“Santa 无常近似条件反面双源审查”只处理条件复杂度方向；本资源提供的是无条件的 restricted assignment 配置 LP \(1/5\) 舍入文献，但不提供一般 unrelated-machines 的硬度或近二界。

## 处置

该冻结 PDF 作为 retained 文献资源保留。它的独有内容是完整作者稿身份、restricted assignment 配置 LP 定义、Haxell/组合选择证明、fat/thin 局部搜索、\(2^n\) 有限步界及“非已知多项式收敛”的明确限制；相关仓库定理只通过链接复用这些背景，不复制作者稿全文。
