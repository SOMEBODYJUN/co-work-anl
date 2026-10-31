---
id: "unrelated-machines/ternary-rainbow-binary-subtree-three-source-review-20261031"
kind: "review"
type_tag: "审查"
title: "三叉彩虹二叉子树三源精读与原 P 边界"
status: "integrated-v1-exact-proof-independent-cover"
truth_status: "scoped-np-complete-candidate-and-ordinary-matrix-corollary"
review_level: "full-clean-show-read; author-proof-and-independent-cover-roles-separated"
scope: "UM-PRIVATE-TERNARY-RAINBOW-BINARY-SUBTREE-NP-COMPLETE-v1 on explicit complete ternary trees with leaf colors and its specified private tree scheduling matrix"
summary: "三份来源共同固定显式完整三叉树上的 rooted full binary rainbow subtree 问题及一份窄的 ordinary unrelated-machines 矩阵推论。Exact 给出量词；作者 Proof 用彩色 AND/OR、Rigid/Dead/Pad 与共享 lock 颜色完成 3SAT 归约和 4/3 对 5/3 调度边界；independent cover 在未读作者 Proof 的情况下独立重构固定 palette、变量/子句模块、等高合成、NP 见证与调度双向。结论保持在该树对象、5/4 间隙和 v1 处理时间合同，不扩展为一般 UM、near-two hardness 或新颖性。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_rainbow_binary_subtree_v1_author_proof_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/ternary_rainbow_binary_subtree_v1_author_proof_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_rainbow_binary_subtree_v1_exact_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/ternary_rainbow_binary_subtree_v1_exact_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_rainbow_binary_subtree_v1_independent_cover_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/ternary_rainbow_binary_subtree_v1_independent_cover_source.md"
source_ids:
  - "efbab186374493b2d7dd"
  - "04e13c09159d1579b210"
  - "6251876b135f490ba515"
evidence_manifest: "archives/unrelated-machines/tools/evidence/ternary-rainbow-subtree-v1-sources-20261031/manifest.json"
---

# 1. 来源身份和实际阅读

本批对三个冻结来源均执行 `clean show` 后完整阅读。`04e13c09159d1579b210` 是 3,790 字节、SHA-256 `3264ae3c3a2100fe0ef50aff1a729f9282346dba45059e20f9dcdc28d739563d` 的 Exact-only 陈述；它只给对象、NP 量词、原 P 矩阵和 4/3、5/3 推论，不含归约证明。`efbab186374493b2d7dd` 是 9,530 字节、SHA-256 `7609ddc76e434c4e3d7ee5171753ef71dcbf1909d2349e63a15a717cfd6c2510` 的作者 Proof；其身份绑定 Exact 哈希，作者已在审查材料公开后冻结，故记录为 proof-read-after/作者证明，不计新 blind 票。`6251876b135f490ba515` 是 10,347 字节、SHA-256 `e0d8a963d389ac578b799ac30717ca59a25e31bbabd010b9c3e128c96f41bdba` 的 independent cover；它明确先读 Exact、未读作者 Proof，独立构造另一组 palette/lock/AND/OR 模块，再独立核对原 P 的调度双向。

双提交 `legacy-cleanup` 与 `main` 的同路径版本视为同一来源，不把提交复制计成两次独立证明。与既有《三叉彩虹困难与树 Markov 联合审查》相邻但不合并：本批新增 v1 稳定 ID、Exact/Proof/independent cover 的完整原文证据，以及对普通树矩阵和处理时间的明确回算。

# 2. Exact 的精确定义和允许的范围

输入是显式完整 rooted ternary tree `T`，高度 `h≥1`，每个内部节点恰有三个 children，所有叶在深 `h`；只给叶颜色 `chi:L(T)->C`，允许重复颜色和同一 child subtree 内重复。要求的见证是以 root 为根、每个 active internal 恰选两个原 children、所有见证叶仍在原深度的 full binary subtree，并且叶颜色在这 `2^h` 个叶上单射。它不是任意 connected subtree、单一路径的颜色互异或覆盖全部颜色。

等价值 `q(T,chi)` 取最大 `r∈{1,2,3}`，使存在到深 `h` 的 rooted full r-ary rainbow subtree；路径保证 `q≥1`，而 `q≥2` 正是二叉彩虹可行性。输入显式展开，`h` 随输入增长，颜色 ID 位长计入输入长度；不使用隐式指数树、随机化或 oracle。Exact 声称二叉 rainbow 判定是 NP-complete，并可由标准 3SAT 作确定性多项式 many-one 归约，输出高度 `O(log s)`、显式规模 `s^{O(1)}`。

# 3. 作者 Proof 的归约承重链

作者先把每个叶带颜色的中间表达式写成彩色 atom、binary AND、binary OR。变量 `x_i` 的两个 branch 分别收集在该 truth 值下为 false 的 literal occurrence colors；clause 用三个 occurrence colors 的 OR。每个 occurrence 使用独有颜色，即便 literal 重复也不合并。彩色 realization 要求 AND 两边颜色不交、OR 选一边，最后所有选中 atom 颜色互异。满足赋值选一个变量 branch 和一个 true clause occurrence；反向若 clause 选中 false occurrence，其颜色同时出现在对应变量 false bundle，违反全局单射，故得到满足赋值。

然后用三叉树构件把该逻辑保持到完整等高显式树：

- `Rigid(H,S)` 使用两份同色 `A` 子树和一份 `B` 子树，强制任何二叉彩虹见证选 `B` 加一个 `A`，并输出固定颜色集合 `S`；
- `Dead(H,c)` 的所有叶同色，在高度至少 1 时不能被二叉彩虹见证选中；
- `AND(T,U)` 先等高，第三 child 放 `Dead`，强制选 `T`、`U`，颜色不交正好表达逻辑 AND；
- `Pad` 通过与 fresh `Rigid` 组合提升高度，不删约束；
- `OR(T,U)` 用两份只共享一个 fresh guard color `g` 的 Rigid guard 分别与 T/U 合并，再放一个 fresh filler。选两 option 会重复 `g`，只能选一边，保留 OR 语义。

所有 height-0/常量调用都被隔离：作者 v1 证明只在高度至少 1 的逻辑构件调用 Dead，颜色、辅助 filler 和 guard 由全局 fresh 分配器管理，避免父级误碰内部共色。平衡化 AND 使高度 `O(log s)`；每个完整三叉构件显式展开，树规模和颜色 ID 位长多项式。完整见证记录每个 active internal 的两个 child 编号，验证 root、闭包、深度和叶色单射均为多项式，故在 NP 内。

# 4. Independent cover 的独立核对与差异

独立 cover 在未读作者 Proof 的条件下给出另一套固定 palette `G(B)`：递归把恰 `2^t` 个颜色分成 `B0,B1,B0` 三个孩子，任何二叉彩虹见证的颜色集合恰为 `B`。它用共享 lock 与 fixed dummy bundle 实现二选一；用 `A,B,A-copy` 约束 AND；变量模块将 truth branch 的 false occurrence colors 写入相应 palette，clause 模块用 inner/outer lock 选择三个 occurrence 之一；最后平衡 AND 和 fresh padding 合成一个等高完整三叉树。该路线显式处理重复 literal、未出现变量重新编号、空 clause/空 conjunction、常量 YES `(a,b,a)` 与 NO `(a,a,a)`，并给出节点数 `3^{h+1}`、`h=O(log(s+2))`、颜色 ID 位长和实际 copy 的多项式界。

其独有检查是：AND 的 A 与 A-copy 都含同一 anchor，不能借不同内部 option 绕过排斥；所有复制都是实际树节点，不是共享子图；原 P 的 YES 只需 `OPT≤4/3`，不强行写成等号。与作者 Proof 的 Rigid/Dead/OR 具体命名不同，independent cover 支持同一 v1 量词和 P 推论，证明角色仍保持独立。

# 5. 原 ordinary unrelated-machines 矩阵的精确回算

矩阵有每个内部节点一台 private machine、每种实际叶颜色一台 resource machine。root pin 只能在 root private 端，时间 1；每条 parent→internal-child edge 是一个 job，在 parent 端时间 `1/3`、child 端时间 1；每条 parent→leaf edge 是一个独立 job，在 parent 端 `1/3`、其叶颜色 resource 端 1，其余无限。重复颜色叶 jobs 保持不同 job，只共享 resource；所有 original jobs、pin、finite endpoints 和不可用端都保留。

若存在 full binary rainbow subtree，将其所选 edge jobs 向下送，其余 edge jobs 留 parent。每个 active internal（root 计 pin）有一个 unit incoming 和恰一个未选 small edge留 parent，负载 `1+1/3=4/3`；inactive internal 负载至多 1；每个颜色 resource 至多接一枚叶 unit job。因此完整 assignment 满足 `Cmax≤4/3`。

反向若一份完整 assignment 有 `Cmax<5/3`，root 已由 pin 激活。任一带 incoming unit 的 active internal 若保留两枚 small outgoing jobs，private load 至少 `1+2/3=5/3`，所以至少两枚 outgoing jobs 必须下送。按固定 child 顺序递归选两枚，至深 `h` 得到 full binary subtree；其叶 jobs 都在颜色 resources 上，`Cmax<2` 使同一 resource 不可能接两枚 unit，故叶颜色单射。若树没有 binary rainbow，则不存在峰值小于 `5/3` 的 assignment；反之任取一条 root-to-leaf path，把路径 edges 下送、其它 small jobs 留 parent，得到 `Cmax≤5/3`，所以真实 `OPT=5/3`。因此该窄 promise 的 YES/NO 数值为 `4/3` 对 `5/3`，乘性比 `5/4`。

这是指定 private/noninjective tree matrix 的窄推论，不能升级到任意 shared internal DAG、菜单模型、一般 unrelated machines 或 near-two gap。它也没有引入 root-only allocation、fractional relaxation 或未列出的 preloads。

# 6. 真值层级、用途和缺口

在明示树、颜色、height、binary witness 和 P 矩阵合同内，Exact 的 NP-complete 对象、作者的显式 3SAT 归约、独立 cover 的第二条归约路线及 4/3、5/3 调度桥均已完整读取和比较。证明没有依赖其它彩色子树或 Group Steiner 问题的不同目标困难性；作者与 independent cover 都明确未认证外部新颖性。

保留的边界包括：不把叶颜色重新着色、任意分支度、strong `(k−1)` 或任意 `delta` gap、near-two amplification、有限实验或软件实现写进本对象；不声称所有 ternary/rainbow 编译均失败，也不声称 NP-hardness 的外部新颖性。后续若改高度量词、颜色重复规则、tree copy 语义或 machine processing times，必须新建稳定对象并重新做归约。

处置为 `integrated`：三份原字节副本、manifest、SHA 校验脚本和审查正文已落在 evidence/state；每个来源的独有证明内容和未决边界均在本文分别记录。
