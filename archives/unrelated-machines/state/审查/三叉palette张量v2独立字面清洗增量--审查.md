---
id: "unrelated-machines/ternary-palette-tensor-v2-independent-literal-increment"
kind: "review"
type_tag: "审查"
title: "三叉 palette 张量 v2 独立字面清洗增量"
status: "independently-read-finite-audit-complete"
truth_status: "scoped-obstruction-confirmed; no-general-amplification-impossibility"
summary: "逐字读取 Boss6 已认领的 v2 independent-literal source，核对 v2 Exact、作者证明、Final composition 与既有三叉/裸菜单/固定层张量对象；在明确树、叶调色板、对齐 tuple 张量及纯整层收缩域内复核恒等式、2^k 上界、G_k 包络和 d−1 障碍，并加入可复运行的小树枚举审计。"
source_refs:
  - "clean:e35e81596d14506bd5c6"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_independent_literal_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_independent_literal_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_exact_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_author_proof_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_final_composition_source.md"
related_objects:
  - "unrelated-machines/ternary-palette-tensor-v2-three-source-review"
  - "unrelated-machines/ternary-palette-tensor-v2-read-after-complexity-direction"
  - "unrelated-machines/ternary-rainbow-hardness-and-tree-markov-review"
  - "unrelated-machines/bare-cartesian-read-after-normal-form-palette-scope"
  - "unrelated-machines/fixed-level-tensor-common-witness-and-candidate-review-scope"
evidence_manifest: "../../tools/evidence/ternary-palette-v2-independent-literal-boss6/README.md"
---

## 来源身份、实际阅读和语义去向

本次实际使用 `python3 work.py clean show e35e81596d14506bd5c6` 读完目标来源。稳定源 ID 为 `e35e81596d14506bd5c6`，路径为
`history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v2_independent_literal_source.md`，冻结于 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`；源字节 2722，SHA-256 为
`950164f0ce3c2d9f32096bd3f80b58857243865761f51d70f94a81152b5c493a`。该独立稿引用的 v2 Exact SHA-256 是 `11ead3e74a0d9309174d2ad3dee16a1b30b1691ee03b0493635656f7bd8940df`，作者 Proof SHA-256 是 `b2b7afdcdd362c8b8b087d97f9ba90e5bcf657d592857a7bbf9308293bc65aaa`。三份 v2 源的尺寸、SHA 和定位也由 `archives/unrelated-machines/tools/evidence/ternary-palette-v2-sources-20261031/source-manifest.json` 交叉核对。

随后逐字读取了 manifest 中的 Exact、作者证明和 Final composition，并读取现有《三叉 palette 张量 v2 三源精读与放大障碍边界》《三叉 palette 张量 v2 作者证明复杂度方向增量》《三叉彩虹困难与树 Markov 联合审查》《裸菜单读后与保值降度及调色板障碍》《固定层张量逃逸的共同见证与候选接口》。独立稿与 v2 三源对象是同一数学主线，不产生第二个定理身份；它的独有去向是本增量中的“独立字面处置记录”以及 `tools/evidence/ternary-palette-v2-independent-literal-boss6/` 下的可复运行有限核验。现有 canonical 对象保留原 v2 证明与关系边界，不被本页覆盖或重写。

## 准确模型、量词和承重假设

令 `T` 是显式完整三叉有根树，所有叶恰深 `h≥1`，叶色允许重复。每个深 `h−1` 父节点的三个直接叶至多有两种色；这是局部末层调色板条件，不是整棵树全局每色重数≤2。`q(T)` 是最大 `r`，使存在包含原 root、每个活跃内部节点恰选 `r` 个原 child、所有叶仍在深 `h` 且叶色两两不同的满 `r` 叉彩虹子树；root-to-leaf 路径保证 `q≥1`。

对整数 `k≥1`，`T^[k]` 的深 `ℓ` 节点是 `T` 深 `ℓ` 节点的有序 `k` 元组，孩子按坐标逐一继承，因而是同高 `d=3^k` 叉树；叶色是有序颜色 tuple，只有 tuple 完全相等才视为同色，不使用可能碰撞的 hash 或额外重着色。另给任意完整同深 `d` 叉树 `U`（`d≥2`、高度 `H≥1`），定义普通 `P(U)`：每个内部节点一台私有机，每个实际颜色一台资源机；root 有唯一有限端为 root、处理时间 1 的 pin job；每条树边是一件不同 job，父端时间 `1/d`，下端若是内部 child 则为该 child machine 时间 1，否则为该叶色 resource 时间 1，其它资格无穷。所有 jobs（包括 pin、所有树边）必须执行。

这些假设不能删掉：若 `H=0`，root pin/内部树矩阵不再是当前对象；若把下端换成抽象 token、共享内部机、DAG、改变任务端点或只保留部分 jobs，下面的等式不自动适用。v2 对 SAT 构件的承重范围还固定 `h=1` 常量 YES 为 `(A,B,A)`（`A≠B`）、NO 为 `(A,A,A)`；不能将未指定的三色常量 `(A,B,C)` 包入两色前提。

## 逐步证明复核

### 普通树矩阵恒等式

对任一满 `r` 彩虹子树，把选中边 jobs 全部送真实下端，其余边 jobs 留在真实父端，pin 留 root。每个活跃内部机接一枚 incoming unit（root 接 pin）并保留 `d−r` 枚 outgoing small，负载为 `1+(d−r)/d=2−r/d`；不活跃内部机负载 1；彩虹性保证每台颜色资源至多接一枚 unit。因此
\[
\operatorname{OPT}(P(U))\le 2-q(U)/d.
\]

反向取任意完整调度峰值 `C<2`（`C≥2` 时下界显然）。root pin 使 root 活跃；任一有 incoming unit 的活跃内部机若真正下送 `t` 枚 outgoing jobs，则父机负载 `1+t/d≤C`，故至少
\[
r=\left\lceil d(2-C)\right\rceil
\]
条 outgoing jobs 真正下送。沿真实下送边递归任选 `r` 条，至末层把 leaf jobs 看作真实颜色资源的 unit jobs；一台资源不能接两枚 unit，于是得到满 `r` 叉彩虹子树。故 `q(U)≥r≥d(2−C)`，从而 `C≥2−q(U)/d`。两向合并为精确恒等式
\[
\operatorname{OPT}(P(U))=2-q(U)/d.
\]
路径给所有 `U` 的可行上界 `OPT≤2−1/d`，但不提供 NO 语义、算法或复杂度结论。

### 对齐张量的末层界和 YES 等式

张量末层父节点 `(u_1,…,u_k)` 的第 `i` 坐标色集大小≤2，故其 `3^k` 个直接 child 的 tuple 色集为 `C_1×⋯×C_k`，大小≤`2^k`。任何满 `r` 彩虹子树在某个活跃末层父节点都必须选 `r` 个互异 tuple 色，因此
\[
q(T^{[k]})\le2^k.
\]
若 `q(T)≥2`，取一棵实际满二叉彩虹子树 `F`，在每个坐标限制到 `F` 的两 child，逐层 Cartesian 形成 `T^[k]` 中满 `2^k` 叉彩虹子树：任意两个不同叶 tuple 至少有一坐标的原 `F` 叶不同，原叶色单射故 tuple 色不同。于是
\[
q(T^{[k]})=2^k,\qquad
\operatorname{OPT}(P(T^{[k]}))=2-(2/3)^k.
\]
`k≥2` 时 `2^k<3^k−1`，所以这些 YES 输入自身也不含满 `(d−1)` 叉虹彩子树。

### 任意同域 NO 的 gap 上包络

不要求张量后的 NO 继续保持原 SAT 谓词。任意同域 `d=3^k` 树都有路径调度 `OPT≤2−3^{-k}`，而 YES 值是 `A_k=2−(2/3)^k`，因此任何意图只靠此对齐张量/重编 `P` 放大 gap 的比值至多
\[
G_k=\frac{2-3^{-k}}{2-(2/3)^k}
=\frac{2\cdot3^k-1}{2\cdot3^k-2^k}.
\]
作者的通分给出
\[
G_k-G_{k+1}
=\frac{2\cdot3^k(2^k-2)+2^k}
 {(2\cdot3^k-2^k)(6\cdot3^k-2^{k+1})}>0
\]
（`k≥1`）；故 `G_1=5/4`、全体 `G_k≤5/4`、并随 `k→∞` 趋于 1。这里是普遍上包络，不声称存在达到上包络的特定 NO，也不以 `NP\not\subseteq QP` 等复杂度假设填补未给出的 gap 归约。Final composition/既有 read-after 另指出一处讨论性文字：准多项式 gap 归约与多项式近似算法合成的方向应为 `NP⊆QP`，不是 `NP⊇QP`；这不改变上述代数结论。

### 纯 `k` 层收缩

若 `k≥2` 且 `k|h`，保留深 `0,k,2k,…,h` 的原节点为 macro，原 `k` 步后代为 macro children，保留原叶色。每个末层 macro-parent 包含 `3^{k−1}` 个原末层三叶星，每星至多两色，故直接 children 总色数至多
\[
2\cdot3^{k-1}<3^k-1=d-1.
\]
所以
\[
q(\operatorname{contract}_k(T))\le2\cdot3^{k-1}<d-1,
\]
连 YES 也达不到满 `(d−1)` 叉。这里随后按 macro-tree 重新定义普通 `P`；不声称旧 physical tree-edge jobs 的资格和负载合同逐项保留。`k=1` 只有 `2=d−1`，不在该障碍内；不整除、补高度、改色、padding、跨副本一致性也不在该量词内。

## 有限可复核证据

本轮新增标准库审计位于 `archives/unrelated-machines/tools/evidence/ternary-palette-v2-independent-literal-boss6/`：

- `audit.py`：精确 Fraction 检查 `G_1=5/4`、`k=1..30` 严格递减、`G_k≤5/4`，并检查 `2^k<3^k−1`（`k=2..30`）。
- 同一脚本穷举所有 `k≤4` 的至多两色三叉局部调色板积，确认 tuple 色数≤`2^k`。
- 对两个显式 `d=3,h=2` 树（底层星分别为 `[0,1,0],[2,3,2],[4,5,4]` 与三个单色星），穷举全部 `2^9` 树边父端/真实下端选择，独立计算实际峰值，分别得到 `q=2, OPT=4/3` 与 `q=1, OPT=5/3`，均与 `2−q/d` 精确相等。
- `audit.json` 是本次运行输出，状态 `pass`；脚本/输出/README SHA-256 分别为 `8414593f681195a3f5b8541786dd070272a22be0dcdbf62e751a195ac440a2d3`、`2f12a48dbdde0be7052cb8bfa67762a2efc989e7a38810484a1173166a7c0300`、`a4c0f1b8ca728a9db2fbbc724c4cf3b98010b45d61ebf3bbbb1e6ad50d23dcbd`。

这些是有限实例/有限参数审计，不能替代任意高度恒等式、SAT 归约、NP 完全性或复杂度声明，也没有测试重着色、非对齐积、padding、跨副本约束或更改任务接口。

## 与相关正式对象的边界及接续

- 《三叉 palette 张量 v2 三源精读与放大障碍边界》已经保存 Exact/Proof/Final 的核心证明；本页只补独立 literal source 的版本处置与独立有限核验，不复制为第二个数学对象。
- 《三叉 palette 张量 v2 作者证明复杂度方向增量》给出 `NP⊆QP` 方向勘误；本页把该纠错挂入相应讨论性边界，不把它写成新定理。
- 《三叉彩虹困难与树 Markov 联合审查》含 v1 归约、全局重数 2/3 门槛和同一张量障碍；本页不将重复的旧图/旧边当作完成证据。
- 《裸菜单读后与保值降度及调色板障碍》所述裸 Cartesian 菜单对象具有不同对象身份和不同失真方向（NO 值下降 vs. 本树模型 YES 分叉受限），不得把两者合并为“所有张量失败”。
- 《固定层张量逃逸的共同见证与候选接口》处理固定层三轴 matching 的共同 guards，不提供当前树叶颜色矩阵的证明或 UM 接口；本页不借其候选接口升级本对象。

本页的明确接续是：若要研究近二放大，必须另证非对齐/重着色/跨副本一致性或新任务接口的完整量词、输出规模和调度双向性；当前来源只完成上述狭域的精确放大障碍。
