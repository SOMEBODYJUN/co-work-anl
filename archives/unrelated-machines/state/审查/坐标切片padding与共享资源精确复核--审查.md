---
id: unrelated-machines/coordinate-slice-padding-and-shared-resource-review
kind: review
type_tag: 审查
title: 坐标切片 padding 与共享资源精确复核
status: independent-reconstruction-read; restricted-source-compiler-only
truth_status: source-note-mathematical-reconstruction; no-author-proof-or-software-rerun
review_level: full-source-read-version-comparison
summary: "完整读取 coordinate-slice independent source 与 private-output-padding addendum，复核 A–D/E–G 的收费、padding、资源互斥、全任务负载及 OPT=1/1+1/D 边界；不扩展为一般 UM 编译或 hardness 定理。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/coordinate_slice_initial_independent_source.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/coordinate_slice_padding_independent_source.md
source_ids: [96101bfe19f784a7a971, b27c184c6199c16db3b2]
source_sha256:
  - 31b04eafa400809d69db35fa2dcad0dfde7f590895855e351bbf44e4c1733714
  - 8abe3bf7eb704ad41acffae69ed0f0fd1eb1a824fb9b0216698815c455331d7
source_sizes: [5488, 4831]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/coordinate-slice-padding-20261031/manifest.json
---

# 来源关系和读域

两份来源是同一 coordinate-slice 编译对象的独立数学重构：第一份给出 A–D（收费、完整 YES、显式近满子树、全部任务负载），第二份在不读取作者证明/canonical 的前提下新增 E–G（padding 保真、完整 \((D-1))-叉证书、精确 OPT）。两份都明确没有外部审查、新颖性认证或程序执行；本页只处置其书面数学推导。

## 1. A–D：原坐标切片结构

### 独立收费（A）

每份 copy 中，左标签 `ell_j` 只能覆盖一个对应右点 `b_(c,j)`，其总覆盖边数不超过左侧 ell 标签总收费；剩余被覆盖边只能由右点上的 `p_i` 覆盖，每个 `p_i` token 至多对应一个左邻居。于是覆盖边总数不超过两侧标签总收费。多 copy 之间顶点、资源预算互不共享，因此同符号复用不破坏计费。映射把 ell_j 映到 0，其余符号映到 p_i，保证 0 属于每条边的投影像；没有声称相同左标签在所有边上均投影 0。

### 完整 YES（B）

对一致单标签 \((\alpha_a,\beta_b)\)，每位玩家取其 alpha 状态的完整 D 分叉树；固定右点 b 的邻居使用互异坐标 \(x_{\beta_b}=i\)，故同一资源块内不相交。所有玩家得到完整状态树，叶映射单射，构成 perfect YES。

### 独立近满子树（C）

统一选原始状态 alpha=0；在 \(a_{(c,i)},b_{(c,j)}\) 上投影为 \(p_i\)，而不是 0。每个左点选 D−1 个邻居；对固定 b，状态树把本玩家固定坐标保留为 i，对其余 p_l 坐标删除对应对角值，对 0/ell 坐标固定删除一个值，于是每层恰有 D−1 个孩子。资源 `(b,x)` 的对角相等索引集合只有本玩家 i，不能被另一位玩家使用；不同 b/c 块天然不交。该构造不依随机性或 PCP。

### 全任务与负载（D）

每位玩家 root 放 selector；保留子树弧下传，全部其它弧（包括未选状态和未保留分支）留在父机。保留内部节点负载为 `1+1/D`，未保留节点为 1；资源机至多接收一枚 unit 叶弧。所有资格合法、没有删除任务；YES 时完整状态树给出负载 1。由于至少一枚 selector，OPT≥1；没有声称 NO 实例 OPT≥1+1/D。

## 2. E–G：private-output padding 修订

### Padding 保真（E）

每个左点在共享右点上的邻居至多 \(D(D-1)\)，可用 \(s\le D(D-1)+1\) 色作 proper coloring。固定 b 的 D 个邻居颜色全异。新增左标签只映到右侧 \(p_{\chi(a)}\)；旧标签覆盖的边收费小于 \(\rho_0M\)，新增标签覆盖边每个右 token 至多一条，收费不超过 \(gN\)，合计小于 \(\rho M\)，其中 \(\rho\le\rho_0+2g/D\)。新字母表大小至多 \(Q_0+D(D-1)+2\)，padding 只需显式输入图上的 O(nD²) 枚举和贪心着色；不按 g、rho 数值展开。

旧 perfect YES 保持不变；simple、regular、balanced 属性由原图保留。新增映射保证投影落在全字母表，但不声称满射或均匀纤维。

### 完整 \((D-1)\)-叉证书（F）

所有玩家选新增状态 alpha*，根层任选 D−1 邻居。对每个保留 b，逐坐标删除一个值：其它邻居的 p 坐标删除其局部 index，剩余自由坐标任删一个值。proper coloring 保证每坐标至多删一次；故每层恰 D−1 个孩子。若两邻居共享资源，后一方的固定 p 坐标值会被前一方切片规则禁止，矛盾；资源互斥成立。按 D 的任务规范下传全部保留弧、其余留父，负载仍为 `1+1/D` 或 1。

### 精确 OPT（G）

若旧源是 E 的 NO，padding 后任意 perfect 单标签覆盖成本小于 \(\rho M\le M\)，故不能 perfect；实际构造负载 `1+1/D`，给出 OPT 恰为该值。若旧源 perfect YES，保留旧 perfect 分配，selector 使 OPT≥1，实际负载 1，故 OPT 恰为 1。该精确值只针对保留的坐标切片 promise 和 padding 结构。

## 3. 作用域和未完成义务

两份独立笔记均把 D、Q 的可变情形标为非 uniform 原输入多项式：D^Q 或 D^(2D+1) 的显式展开不能被偷写成 bit-polynomial。A–G 也没有证明一般 Santa/UM hardness、没有执行作者 canonical/proof 软件、没有覆盖额外纤维正则性要求的归约。它们可作为第三阶段的 restricted compiler/near-one certificate 关系证据；不得并入一般 unrelated-machines 结论。
