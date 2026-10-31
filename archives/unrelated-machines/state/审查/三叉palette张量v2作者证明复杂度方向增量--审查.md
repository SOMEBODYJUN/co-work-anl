---
id: "unrelated-machines/ternary-palette-tensor-v2-read-after-complexity-direction"
kind: "review"
type_tag: "审查"
title: "三叉 palette 张量 v2 作者证明读后与复杂度方向增量"
status: "integrated-read-after-correction"
truth_status: "core-obstruction-confirmed-with-discussion-erratum"
summary: "全文读取 ternary palette tensor v2 的 read-after 作者证明：树矩阵恒等式、2^k 张量上界/YES 等式、G_k 严格递减和纯收缩障碍均成立；仅第7节把由准多项式 gap 归约与多项式近似器合成得到的 NP⊆QP 方向写反，需在讨论性文字中更正。"
source_refs:
  - "clean:3582819dede8bc331e54"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_read_after_literal_source.md"
related_objects:
  - "unrelated-machines/ternary-palette-tensor-v2-three-source-review"
  - "unrelated-machines/fixed-level-tensor-common-witness-and-candidate-review-scope"
---

# 读取与身份

本源是 v2 read-after literal source；其正文给出作者证明的实际 SHA
`b2b7afdcdd362c8b8b087d97f9ba90e5bcf657d592857a7bbf9308293bc65aaa`，并绑定
Exact SHA `11ead3e74a0d9309174d2ad3dee16a1b30b1691ee03b0493635656f7bd8940df`。
它与已有《三叉 palette 张量 v2 三源精读与放大障碍边界》对象相同一条数学主线；本页只记录本次 read-after 的版本确认和新增勘误，不把作者证明与先行稿算作独立定理。

# 核心结论复核

在显式完整等深三叉树、每个末层父节点至多两色、叶色 tuple equality 的域内，作者证明完整得到

\[
 OPT(P(U))=2-q(U)/d,
\]

其中 (q(U)) 是满彩虹子树的最大分叉度，(d=3^k) 为张量后的分叉度。对齐 Cartesian k 次张量满足
(q(T^{[k]})\le2^k)；若原树含满二叉彩虹子树，则等号成立，故 YES 值为
(2-(2/3)^k)。任意同域树都有 root-path 上界 (2-3^{-k})，其比值

\[
G_k=\frac{2-3^{-k}}{2-(2/3)^k}
\]

满足作者给出的正差恒等式，严格递减，(G_1=5/4)，全体 (G_k\le5/4)。纯 k 层收缩（k≥2 且整除高度）末层 palette 至多
(2\cdot3^{k-1}<3^k-1)，因此也不能制造满 (d-1) 叉彩虹。上述每一步量词和边界在 read-after 中核对无 fatal 缺口；不应扩展至改色、padding、跨副本约束或非对齐操作。

作者还修正了 v1 的两个语义缺口：高度至少 1 以使 root pin 有意义；常量 YES/NO 规范固定为 `(A,B,A)` 与 `(A,A,A)`，不能把任意三色常量都当作两色 palette。

# 讨论性勘误

作者 proof §7 有一句复杂度方向错误。若存在从 NP-complete 源到目标的准多项式规模/时间 gap 归约，且目标有多项式时间近似算法，则合成得到的是

\[
\mathrm{NP}\subseteq\mathrm{QP},
\]

而不是 NP⊇QP。相应的排除假设应写成“NP 不包含于 QP”（通常记 NP\(\not\subseteq\)QP）。该错误不承重于 Exact 四项或树矩阵恒等式；当前对象没有建立所需 gap 归约，故不得用复杂度假设弥补 `G_k≤5/4` 的数学障碍。

# 处置

核心 v2 source 保留并与既有三源对象合并引用；本页的独有内容是 read-after 版本和复杂度包含方向勘误。未新增代码、有限实验、一般 UM 困难性或新颖性认证。
