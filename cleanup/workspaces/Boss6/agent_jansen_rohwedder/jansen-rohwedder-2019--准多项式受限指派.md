---
id: "unrelated-machines/jansen-rohwedder-2019-quasi-polynomial-restricted-assignment"
kind: "resource"
type_tag: "资源"
title: "Jansen–Rohwedder 2019：受限指派配置LP与六分之十一准多项式近似"
status: "frozen-paper-fully-read"
summary: "冻结 arXiv:1701.07208v2 的完整文献对象：受限指派配置LP积分间隙至多 11/6，并给出 (11/6+ε) 近似的准多项式组合算法；保留 2+ε 教学算法、有限但指数状态局部搜索、leap/critical/small/non-critical 四层机制及全部模型边界。"
truth_status: "literature-theorem; complete source read; no independent external reproof"
review_level: "30-page PDF text-read end-to-end; definitions, algorithms, dual certificates, all lemmas/theorems and references checked"
scope: "restricted assignment p_ij in {p_j, infinity}; arbitrary finite eligibility sets; makespan minimization"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/jansen_rohwedder_2019_quasi_polynomial_v2.pdf#PDF-pages-1-30"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/jansen_rohwedder_2019_quasi_polynomial_v2.pdf#PDF-pages-1-30"
source_ids:
  - "ae1bf88ade047c378350"
source_sha256: "6371eaf41ed90ec3c92e6626ccf1ff209935d67ced11d918cf85a91719ca244f"
source_size_bytes: 311771
source_title: "A Quasi-Polynomial Approximation for the Restricted Assignment Problem"
authors: "Klaus Jansen; Lars Rohwedder"
source_version: "arXiv:1701.07208v2 [cs.DS], 20 August 2019 (PDF title page 21 August 2019)"
---

# Jansen–Rohwedder 2019：受限指派配置LP与六分之十一准多项式近似

## 来源身份、读取范围与模型

本对象绑定冻结源 `ae1bf88ade047c378350`，路径为
`history/source/literature/unrelated_machines/jansen_rohwedder_2019_quasi_polynomial_v2.pdf`，SHA-256 为
`6371eaf41ed90ec3c92e6626ccf1ff209935d67ced11d918cf85a91719ca244f`，字节数 311771。两冻结提交保存同一源版本，不是两个独立证明。本次导出后完整读取 PDF 的 30 个物理页，覆盖摘要、配置 LP 原/对偶、2+ε 算法、非构造性 11/6 局部搜索、准多项式构造算法、所有定义、Lemma/Claim/Theorem 证明和参考文献；未把论文引用的外部证明当作本对象的独立重证。

输入是有限任务集 (J) 与机器集 (M)。每个任务 (j) 有一个机器无关的处理时间 (p_j)，且只能放到资格集合 (Gamma(j)) 内的一台机器；目标是最小化最大机器负载。这是 **restricted assignment**，等价于一般不相关机器的 (p_{ij}in{p_j,infty}) 特例。论文不要求每个任务只有两个资格端，也没有客户、目录、历史或终局均分量词，因此与六人 Q-CAG-HALF-6 模型保持独立。

源引言记录了经典 3/2 多项式困难性与受限版本的准多项式条件困难性等背景；这些是文献叙述，本文对象不把它们升级为本轮独立的复杂度重证。

## 配置 LP 与对偶停滞证书

给定阈值 (	au)，机器 (i) 的合法配置为
[
  {cal C}(i,	au)=\{S\subseteq J:p(S)\le\tau,;S\subseteq\Gamma^{-1}(i)\}.
]
配置 LP 的一个等价原始形式为
[
\sum_{C\in{cal C}(i,\tau)}x_{i,C}\le1\quad(i\in M),
\qquad
\sum_{i\in M}\sum_{C\ni j}x_{i,C}\ge1\quad(j\in J),
\qquad x\ge0.
]
令 (mathrm{OPT}^{*}) 为该 LP 可行的最小 (	au)。其对偶写成
[
  \min \sum_{i\in M}y_i-\sum_{j\in J}z_j,
  \qquad \sum_{j\in C}z_j\le y_i
  quad(i\in M,C\in{cal C}(i,\tau)),
  \qquad y,z\ge0.
]
若能构造 (sum_i y_i<sum_j z_j) 且满足所有配置约束，则对偶可沿正倍数缩放而无界，因而配置 LP 在 (	au) 不可行。论文 Lemma 1 把这作为所有“无停滞则给证书”论证的统一入口。由于配置族向下封闭，论文的“至少覆盖”写法可与精确覆盖形式互换，但这不替代配置分离或目标搜索的位复杂度证明。

## 2+ε 准多项式算法（方法导入）

第一算法从任意分配 (sigma) 开始。称机器坏若负载 (> (2+\varepsilon)\tau)，好若不超过该值；按层 (L_0,L_1,ldots) 追踪坏机器及其当前任务能到达的资格机器。若在下一层找到负载 (le(1+\varepsilon)\tau) 的目标，就移动一项并重置层。移动后目标负载至多 ((2+\varepsilon)\tau)，所以好机器不会再次变坏。

若层数达到 (log_{1+\varepsilon}|M|)，算法用
[
 y_i=(1+\varepsilon)^{1-k}\quad(i\in L_k),
 qquad z_j=(1+\varepsilon)^{-k}p_j/\tau
]
（(k) 为任务第一次进入层的最小层号，未进入层的 (z_j=0)）构造 Lemma 1 的负对偶证书：每个配置的 (z)-质量不超过所在机器的 (y_i)，而所有任务 (z)-总和严格超过机器 (y)-总和。这说明配置 LP 不可行。以坏机器数、各层任务数及末尾哨兵组成的字典序势严格下降，得到 (n^{O((1/\varepsilon)\log n)}) 的准多项式状态界。该算法只是导入层搜索和对偶证书的教学版本，最终常数仍是 2+ε。

## 非构造性配置 LP 间隙：(11/6)

第二算法令坏机器阈值为 (11\tau/6)，大任务满足 (p_j>\tau/2)，其余为小任务。维护按字典序选择的待定移动列表 (P)。只有当任务在其当前机器被“排斥”（repelled）且目标机器未排斥时才把 move 加入列表；若目标加入后仍不超过 (11\tau/6)，执行 move 并清空列表。小任务 move 会使目标排斥所有任务；大任务 move 按阈值 (W_0) 排斥当前机上小任务和大小不超过 (W_0) 的大任务。

当配置 LP 在 (	au) 可行而仍有坏机器时，若列表既无可执行 move 也不能再添加 move，论文 Lemma 2 用对偶证书矛盾。对所有被当前机器排斥的任务取
[
 z_j=\min\{p_j/\tau,5/6\},
]
其余 (z_j=0)；若机器排斥所有任务则设 (y_i=1)，否则设 (y_i=z(\sigma^{-1}(i)))。配置至多含一个大任务，(W_0) 的最小性和“小任务无其它可行端”保证 (z(C)\le y_i)。Lemma 3 证明排斥所有任务的机器中至少一半是小任务 move 的目标，因而这些机器的对偶质量可以与非小目标机器摊销，得到 (sum_jz_j>sum_i y_i)。

算法确实终止（Lemma 4）：在两次执行 move 的间隔，以坏机器数、被当前机排斥任务数和每个待定 move 的 ((p_j,j,i))、剩余排斥边数等组成有限字典序势，插入/删除与执行都会严格下降。该有限性没有给出多项式步数界。于是 Theorem 5 得到配置 LP 在 restricted assignment 上的积分间隙至多
[
  \mathrm{OPT}\le(11/6)\,\mathrm{OPT}^{*}.
]
这里“非构造性”是指证明只给出可能指数的局部搜索，不是说最终分配不存在；不能改写成多项式时间 (11/6) 输出算法。

## 准多项式构造：(11/6+\varepsilon)

第四节把前述非构造性算法与层法结合。令坏阈值为 ((11/6+2\varepsilon)\tau)。任务分为

- small：(p_j\le\tau/2)；
- medium：(\tau/2<p_j\le5\tau/6)；
- huge：(p_j>5\tau/6)。

先用二部匹配给每台机器至多一个 huge 任务；随后保持这一不变量。huge move 要求目标无 huge 且加入后不坏；non-huge move 或进入无 huge 机器并保持总负载阈值，或进入有一个 huge 的机器且目标的非 huge 部分不超过 ((5/6+2\varepsilon)\tau)。

### Leap 图和四类层

Leap 图 (G(\sigma)) 的顶点是大任务与机器。若 (i\in\Gamma(j_B)\setminus\{\sigma(j_B)\})，且目标机上非 huge 负载加 (p_{j_B}) 不超过 ((11/6+2\varepsilon)\tau)，加入 (j_B\to i)；若 huge 任务 (j_H) 当前在 (i)，加入 (i\to j_H)。沿
[
 j_1,i_1,j_2,i_2,\ldots,j_r,i_r
]
的路径，若末端 move 有效，则可以逆序把整条 huge 链一次性搬移，称为 valid leap。这样避免简单 move 链需要线性层数。

层按四步循环：

1. **leap layer**：从被当前机排斥的大任务出发，在受前缀排斥边约束的 leap 图中加入可达机器；
2. **critical layer**：从尚未被目标排斥的大任务 move 中，用当前顺序 (pi) 选关键 move，并将其移到 (pi) 前端；关键目标机排斥所有任务；
3. **small layer**：加入被当前机排斥而未被目标排斥的小任务 move，目标机排斥所有任务；
4. **non-critical layer**：将尚未选为 critical 且仍未被目标排斥的大任务 move 加入，并只排斥必要的小任务与大小不超过阈值 (W_0) 的大任务。

critical 选择通过已阻塞的小任务量、medium 任务量和“私有可达机器”更新集合 (M)：只有在加入该 critical move 后仍有足够余量的目标才入 critical；每个 critical 目标至少带来一个可摊销的小任务目标。算法在任一层发现 valid move 或 valid leap 时执行并重置层；达到
[
 4\left\lceil\log_{1+\varepsilon}(4|M|)\right\rceil
]
层仍无动作，则触发对偶矛盾。

### 关键正确性与复杂度

Lemma 9 断言：若配置 LP 在 (	au) 可行且仍有坏机器，则在上述层数上限内一定找到 valid move 或 leap。反证时，在每个以 leap layer 结尾的前缀定义 (z_j^{(k)})、(y_i^{(k)})，并以几何系数
[
 z_j^{(\le k)}=\sum_{k'=-1}^{k}(1+\varepsilon)^{-k'}z_j^{(k')},
 \qquad
 y_i^{(\le k)}=\sum_{k'=-1}^{k}(1+\varepsilon)^{-k'}y_i^{(k')}
]
组合。Claim 10 证明每个配置的前缀 (z)-质量不超过下一层 (y)；Claim 11 用坏机器的余量、critical 与 small 目标的成对摊销，证明最终 (sum_jz_j>sum_i y_i)。因此无动作会给 Lemma 1 的不可行证书。

算法终止的 Lemma 14 维护每层不同类型的势：leap 层看排斥边数，critical 层看层大小和未排斥任务数，small 层看未排斥任务数，non-critical 层看排斥边数及未排斥任务数，并在开头比较好机器数和坏机器所排斥任务数。Claim 15 说明每次 move/leap 后该向量字典序严格增加（等价于反向势严格下降）。层数至多 (O((1/\varepsilon)\log n))，每个分量只有多项式多个值，所以总状态数、运行时间为
[
 n^{O((1/\varepsilon)\log n)}.
]
Theorem 16 通过把正文中的 (11/6+2\varepsilon) 参数重标定，得到对任意固定 (
arepsilon>0) 的
[
 (11/6+\varepsilon)
]
准多项式时间实际调度算法。论文强调该算法是组合的，configuration LP 只出现在不可行性分析中；没有声称多项式时间，也没有把配置 LP 的近似求解器实现作为仓库软件交付。

## 与全仓对象的比较及身份边界

- [配置松弛的局部搜索与图平衡界](../配置松弛的局部搜索与图平衡界--资源.md)对应同一作者 2017 年 arXiv:1611.01934v2：已整理 (11/6) 的非构造性间隙、有限终止和 (11/6+\varepsilon) **估值**边界。本源是其扩展联合版本，新增完整的 leap/critical/small/non-critical 分层与 (11/6+\varepsilon) 准多项式构造；两源不可合并成一个版本，也不能把 2017 的估值合同误写为本源的多项式实际输出。
- [配置LP在图平衡及不相关机中的间隙](../配置LP在图平衡及不相关机中的间隙--资源.md)处理一般 (p_{ij})（尤其二端异速）和窄值域特例；本源允许任意大小的 (p_j) 但每个任务跨资格机器同速，11/6 的适用条件不同。共享常数不是同一命题。
- [SantaClaus 调度与受限指派配置界](../SantaClaus调度与受限指派配置界--资源.md)及 [Bamas 升投影 MMDA 与 SantaClaus](../Bamas升投影MMDA与SantaClaus--资料.md)的 leap/局部搜索类比只作来源或启发关系；Santa Claus 是最大化最小值，不能直接迁移本算法的 makespan 对偶。
- [不相关机器与两个调度松弛](../定义/不相关机器与两个调度松弛--定义.md)给一般 (p_{ij}) 的模型与 LST/配置 LP 定义；本对象是其 restricted 子类的文献结果，不能把 restricted 任务无关大小的证明当一般 UM 算法。
- 本对象不含客户价值、共同非空目录、完整有序历史、离轨行动或终局均分，不为六人纯 SPE 覆盖目标提供结论或反例。

## 未决点、复用与处置

可复用的数学结构是：配置 LP 对偶停滞证书；small/medium/huge 分类；huge 任务 leap 图；critical 选择中私有机器摊销；几何层加权的配置约束证明；以及“有限状态字典序”与“准多项式运行时间”分开记录。任何迁移到一般 (p_{ij}) 的尝试必须重建同一任务跨机器同速、每机至多一个 huge 的不变量和对偶收费，本文没有提供该迁移。

配置 LP 分离的近似后端、引用文献的外部复杂度结论和算法的常数重标定均按来源声明保留；本对象没有独立实现或外审。未来要声称更强（如多项式 (11/6+\varepsilon)、一般不相关机 (<2)、或六人 SPE 半覆盖）仍需各自完整证明和输入位长合同。

建议对此冻结源登记 `retained`，目标对象路径：
`archives/unrelated-machines/state/文献/Jansen-Rohwedder-2019--受限指派准多项式近似--文献.md`。

第三阶段可建立以下有解释关系：2017 受限配置 LP 资源对象 → 本源的“改进/构造化扩展”；本源 → 受限模型定义的“特化”；本源与一般 UM 资源对象之间的“模型边界”；本源与 Santa Claus 资源之间的“方法类比”。本轮不直接修改全仓图。
