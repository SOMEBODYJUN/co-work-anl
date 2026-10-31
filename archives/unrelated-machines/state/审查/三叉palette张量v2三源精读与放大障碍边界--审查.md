---
id: "unrelated-machines/ternary-palette-tensor-v2-three-source-review"
kind: "review"
type_tag: "审查"
title: "三叉 palette 张量 v2 三源精读与放大障碍边界"
status: "integrated-v2-obstruction-and-version-scope"
truth_status: "exact-aligned-tree-obstruction; no-general-amplification-impossibility"
review_level: "full-clean-show-read-cross-object-comparison"
summary: "三份 ternary-palette v2 来源共同保留一个精确的树级限制：在完整等深三叉树每个末层父节点至多两色的前提下，对齐 Cartesian k 次张量的 rainbow branching 至多 2^k；若原树有二叉 rainbow 则恰为 2^k；对应普通树矩阵 OPT=2-q/d，任何同域 NO 上包络 gap G_k 严格递减且 G_k≤5/4。k≥2 的纯 k 层收缩还满足 q≤2·3^(k−1)<3^k−1。结论只针对显式树、tuple-equality 颜色和保叶色收缩；不排除改色、非对齐、跨副本一致性、padding 或其它任务接口。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_author_proof_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_author_proof_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_exact_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_exact_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_final_composition_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_final_composition_source.md"
source_ids:
  - "dd4f3c34acf1daf73724"
  - "8c2804a0beb477d28a85"
  - "9a6e1a8776a66d04304f"
related_objects:
  - "unrelated-machines/ternary-rainbow-hardness-and-tree-markov-review"
  - "unrelated-machines/bare-cartesian-read-after-normal-form-palette-scope"
  - "unrelated-machines/fixed-level-tensor-common-witness-and-candidate-review-scope"
evidence_manifest: "../../tools/evidence/ternary-palette-v2-sources-20261031/source-manifest.json"
---

# 1. 来源身份、版本与实际阅读

本批直接 `clean show` 并逐字阅读三份冻结来源。双冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的同路径版本视为同一材料，不把两提交计成两次独立证据。原字节副本与 manifest 位于 `archives/unrelated-machines/tools/evidence/ternary-palette-v2-sources-20261031/`。

| 稳定 ID | 冻结路径 | 字节 / SHA-256 | 角色 |
|---|---|---:|---|
| `8c2804a0beb477d28a85` | `history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_exact_source.md` | 2754 / `11ead3e74a0d9309174d2ad3dee16a1b30b1691ee03b0493635656f7bd8940df` | Exact v2：定义域、张量/收缩操作、gap 上包络和边界 |
| `dd4f3c34acf1daf73724` | `history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_author_proof_source.md` | 10852 / `b2b7afdcdd362c8b8b087d97f9ba90e5bcf657d592857a7bbf9308293bc65aaa` | Author Proof v2：树矩阵恒等式、末层不变量、张量上界/等式、G_k、收缩证明 |
| `9a6e1a8776a66d04304f` | `history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_final_composition_source.md` | 3048 / `4a1db7cce9cd835eb1cf0b6974233164b1f4165404612a3b59ba01bd8ae1e58c` | Final composition：T1–T7 字节/版本核对、常量与 NP⊆QP 方向修正、范围保留 |

三份来源是同一 obstruction 对象的互补版本，不是三次独立证明：Exact 只陈述对象，Proof 给出承重推导，Final composition 做知情后置的章节/字节一致性核对。与已有《三叉彩虹困难与树 Markov 联合审查》相比，本批独有的是三个新稳定 ID 的 v2 原文处置、作者 v2 证明的完整 tensor/pure-contraction 范围，以及旧 v1 常量/高度措辞的修正。与《裸菜单读后与保值降度及调色板障碍》相比，当前对象是完整三叉树和普通树矩阵，不是 normalized flat menu Cartesian re-coupling；两者的 gap 失真机制必须分开。

# 2. v2 精确定义域与普通树矩阵

输入是显式完整三叉有根树 `T`，所有叶同深 `h>=1`，叶带可重复 binary color IDs。每个深 `h-1` 父节点的三个叶至多两种颜色；这是末层 palette 前提，不是全树颜色重数≤2 的全局条件。令 `q(T)` 为最大整数 `r`，使存在包含 root、全叶深 h、每个活跃内部节点恰选 r 个原 child 且所有叶色不同的满 r 叉彩虹子树；至少 `q>=1`，因为 root-to-leaf path 是满 1 叉。

给 `k>=1`，定义对齐 Cartesian 张量 `T^[k]`：深 `ell` 的节点是 T 深 `ell` 节点的有序 k 元组，孩子逐坐标继承；共同分叉度 `d=3^k`，高度仍 h，不收缩任何层。叶色是有序 k 颜色 tuple，只有 tuple 完全相等才视为同色，不能用可能碰撞的 hash 或额外 recolor 替代。

对任意完整 d 叉等深着色树 U（d≥2、H≥1）定义普通 P(U)：每个 internal node 一台 private machine，每种实际颜色一台 resource machine；root 有唯一 finite 的 unit pin；每条树边是一件不同 job，父端时间 `1/d`，internal child 端或叶颜色 resource 端时间 1，其余端无穷。所有 jobs 必须执行，包含 pin 和全部树边；不能把下端改成抽象 token。

# 3. 普通树矩阵恒等式 OPT(P(U))=2−q(U)/d

**上界。** 若有满 r 彩虹子树 F，选中边 jobs 全送真实下端，其余边 jobs 留父端，root pin 留 root。每个活跃 internal 恰有一枚 incoming unit（root 是 pin）并留下 `d-r` 枚 outgoing small，负载 `1+(d-r)/d=2-r/d`；非活跃 internal 负载 1；每个颜色 resource 因彩虹性至多接一枚 unit。所有原 jobs 都按真实有限端点回填，故 `C<=2-r/d`。

**下界。** 任意完整 schedule 若 `C>=2`，不等式平凡；只看 C<2。root pin 使 root 活跃；任意带 incoming unit 的 active internal 若真正下送 t 枚 outgoing small，则 private load `1+t/d<=C`，所以至少
\[
r=\lceil d(2-C)\rceil
\]
枚 outgoing jobs 真正下送。沿真实下送边逐层任取 r 条，到叶后其 unit jobs 只能进入颜色 resources；每资源不能接两枚 unit，于是获得满 r 叉 rainbow subtree。故 `q(U)>=ceil(d(2-C))>=d(2-C)`，即 `C>=2-q(U)/d`。两向合并得
\[
\operatorname{OPT}(P(U))=2-q(U)/d.
\]
此式是该显式树矩阵的实际 optimum 恒等式，不是把 q 当作已知算法或把它推广给共享内部机器/DAG/菜单。

任意 U 的一条 root-to-leaf path 给 q≥1，从而存在完整调度 `C<=2-1/d`。这只是普适上界，不是 YES/NO 语义或复杂度结论。

# 4. 末层两色不变量与对齐张量

作者 Proof v2 先验证现有 ternary SAT 编译族确实满足 palette 前提：v1 Rigid(1) 与 v2 R_1(S) 的三叶是 `(a,b,a)`；Dead 的三叶同色；更高 Rigid/R_H、AND、OR、Pad 只在高度至少 1 的子树上方拼接，不从不同构件的裸 height-0 叶混成新末层星。因此每个输出的每个末层父节点至多两种颜色。常量分支需显式规范：h=1 的 `(A,B,A)` 作为 YES、`(A,A,A)` 作为 NO；不能把任意合法常量颜色映射都写成已满足前提，例如 `(A,B,C)` 不满足。

取任一张量末层父节点 `(u_1,...,u_k)`。第 i 坐标的三叶颜色集合 `C_i` 大小≤2；张量父节点的全部 `3^k` children 的 tuple 颜色集合恰为 `C_1×...×C_k`，大小≤`2^k`。任意满 r 彩虹子树至少包含一个活跃末层父节点，且该节点选中的 r 个叶 tuple 必须互异，故
\[
q(T^{[k]})\le2^k.
\]

若 `q(T)>=2`，取一棵原满二叉 rainbow 子树 F；每个坐标限制到 F 的二 child，逐节点 Cartesian product 形成 `T^[k]` 中满 `2^k` 叉子树。任意两个不同叶元组至少在一个坐标的原 F 叶不同，而 F 叶色单射，因此 tuple 颜色不同。于是
\[
q(T^{[k]})=2^k,
\qquad
\operatorname{OPT}(P(T^{[k]}))=2-(2/3)^k.
\]
这是真实普通 P 的精确值，不是仅一份弱 YES 调度。k≥2 时 `2^k<3^k-1`，所以 YES 张量本身也没有满 `(d-1)` 叉彩虹子树；这直接阻断把“原二叉”放大成强 `(d-1)` 完备性。

# 5. 任意同域 NO 的 gap 上包络 G_k

无论张量后的 NO 树是否保留原 SAT 谓词，任意同域 d=3^k 树 U 都有 root path 调度 `OPT(P(U))<=2-3^{-k}`。若某个 YES 树来自 `q(T)>=2`，其 exact value为 `A_k=2-(2/3)^k`。因此任何意图通过本对齐张量/重编 P 产生 YES/NO 乘性 gap，其比值最多
\[
G_k=\frac{2-3^{-k}}{2-(2/3)^k}
=\frac{2\cdot3^k-1}{2\cdot3^k-2^k}.
\]
作者 Proof 给出相邻差的正通式
\[
G_k-G_{k+1}
=\frac{2\cdot3^k(2^k-2)+2^k}{(2\cdot3^k-2^k)(6\cdot3^k-2^{k+1})}>0,
\]
对 `k>=1` 严格递减；`G_1=5/4`，所以全 k 均≤5/4，并趋近 1。此上包络不需要 NO 保留原谓词，也不声称任何特定 NO 家族实际达到上界。v2 仅报告精确代数限制，不能用更强复杂度假设填补缺失 gap。

若原树大小为 N，张量完整展开的节点数为
\[
\frac{3^{k(h+1)}-1}{3^k-1};
\]
颜色 tuple 也须显式记录。故不按 binary k 承诺多项式输出；k=O(log N) 时可有准多项式展开，但这是规模允许，不是近似 gap 的复杂度证明。

# 6. 纯 k 层收缩的独立完备性障碍

当 `k>=2` 且 `k|h`，保留深 `0,k,2k,...,h` 原节点为 macro nodes；原 k 步后代成为 macro children，保留原叶色，macro 分叉度仍 `d=3^k`、高度 h/k≥1。该操作随后以 macro tree 重新定义 P，并不声称旧 physical tree-edge jobs 资格逐项保留。

每个末层 macro-parent 对应一个原高度-k 子树，包含 `3^{k-1}` 个原末层三叶星，每星≤2种颜色；全部新直接 children 的颜色集合大小至多
\[
2\cdot3^{k-1}=(2/3)d.
\]
任意 macro rainbow 子树在某个末层 macro-parent 必选互异颜色，故
\[
q(\operatorname{contract}_k(T))
\le2\cdot3^{k-1}<3^k-1=d-1.
\]
严格不等式来自 `3^{k-1}>1`。它对原 YES 族同样成立，故纯收缩不可能把二叉 YES 变成满 `(d-1)` 叉彩虹；`k=1` 只给 `2=d-1`，本障碍不覆盖。若不整除、补高度、改色或加入跨副本约束，就不属于本条操作，必须重证。

# 7. 与旧来源和相邻障碍的边界

- v2 修正 v1 的两个规范缺口：显式规定 U 高度 H≥1，使 root pin 有意义；显式固定常量 YES/NO 叶色 `(A,B,A)` / `(A,A,A)`，不把任意合法常量分支包进末层两色前提。
- 与三叉彩虹困难审查的关系：v2 的末层不变量、普通树矩阵 `OPT=2-q/d`、受限 NP-hardness 和 `(5/4)` 原始树承诺可并入既有对象；本批新增的是 aligned tensor 的精确 `2^k` 上界/YES 等式、严格递减 `G_k` 和纯收缩 `<d-1` 障碍。
- 与裸 Cartesian menu amplification 的关系：裸菜单的失败来自 partial label 重选、NO 值下降及后续保值降度；当前 palette tensor 是完整三叉树、tuple equality 和普通 tree-edge/resource P，失败来自末层颜色容量限制。两者不能合并为“所有张量失败”。
- 与 fixed-level tensor/common-witness 对象的关系：后者研究固定层三轴 matching 的共同 guard 和 source-to-UM 缺口；当前对象研究树分叉和叶色，不能用一个对象的共同见证替换另一个对象的任务资格。
- 与 tree-Markov recoupling 对象的关系：tree-Markov 处理配置 pair 边际和非树兼容性；当前 palette obstruction 不使用 Markov law，也不提供五机耦合反例。

# 8. 真值层级、用途与未决义务

**精确已证。** 在显式等深三叉树、末层两色、对齐 Cartesian tuple-equality 张量和保叶色纯 k 层收缩的明示域内，作者 Proof 的树矩阵恒等式、`q(T^[k])<=2^k`、原二叉 YES 时的等式、`G_k` 严格递减及收缩 `q<d-1` 均有完整推导。

**障碍用途。** 这些结论用于否定一条特定 amplification route：不能仅以对齐张量把原二叉彩虹 gap 放大到接近 2，也不能仅以纯 k 层收缩达到满 `(d-1)` 彩虹。它们不否定重新着色、非对齐乘积、跨副本一致性约束、padding、不同任务端点或其它编译器。

**未认证项。** 本批没有新代码或有限实验；作者文中 Fraction sanity 只属其记录。没有一般 UM hardness、NP-hardness 的新升级、外审、新颖性或论文价值认证；SAT/palette 原始受限问题和其它来源保持独立身份。不能按 binary k 把显式张量当作多项式大小，也不能用 `NP⊄QP` 等假设弥补缺失 gap。

三源均已完整读取、比较并写证据/manifest/receipt；暂不执行 commit、push 或 clean done。
