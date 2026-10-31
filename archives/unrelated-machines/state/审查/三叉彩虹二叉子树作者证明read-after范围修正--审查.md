---
id: "unrelated-machines/ternary-rainbow-binary-subtree-author-proof-read-after-scope"
kind: "review"
type_tag: "审查"
title: "三叉彩虹二叉子树作者证明 read-after 范围修正"
status: "integrated-v1-object-with-scope-correction"
truth_status: "scoped-proof-consistent-no-fatal-objection"
review_level: "full-source-read-and-cross-archive-comparison"
summary: "冻结的作者证明读后源逐段核对三叉完整树上的彩色 AND/OR 归约、显式展开、NP 见证和 4/3 对 5/3 私有矩阵桥；结果与既有 v1 三源对象一致，补充 root pin 单资格措辞修正。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/ternary_rainbow_binary_subtree_v1_read_after_cover_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/ternary_rainbow_binary_subtree_v1_read_after_cover_source.md"
source_id: "8a5fdbc4b867d2d71b02"
source_sha256: "473561d27fc536a391ebfc6e682a93e2367a3d074729956da03f4cb68edca2e4"
source_size_bytes: 7750
related_objects:
  - "archives/unrelated-machines/state/审查/三叉彩虹二叉子树三源精读与原P边界--审查.md"
  - "archives/unrelated-machines/tools/evidence/ternary-rainbow-subtree-v1-sources-20261031/manifest.json"
  - "archives/unrelated-machines/tools/evidence/ternary-rainbow-subtree-v1-read-after-20261031/manifest.json"
---

# 来源身份

该源是作者冻结证明的 read-after-cover 审查，不是新的 Exact 陈述。读取顺序保留：先冻结并独立重构 Exact，再读取作者的 Dead-AND 方案；不能把作者方案倒填成独立先验。冻结源 SHA 为 `473561d27fc536a391ebfc6e682a93e2367a3d074729956da03f4cb68edca2e4`，证据副本与 manifest 位于 `tools/evidence/ternary-rainbow-subtree-v1-read-after-20261031/`。

# 实质核对

- **彩色逻辑。** 每个 literal occurrence 保留独立颜色；变量 truth branch 收集该赋值下为假的 occurrence，clause 选择一个 occurrence。重复 literal 不合并，空 false bundle 用 private neutral atom。因 false occurrence 同时出现在变量 false bundle 与 clause，彩虹叶色单射恰好给出 SAT 等价。
- **构件边界。** `Rigid` 的两份同色 A 与一份 B 强制选 B 加一份 A；`Dead(H,c)` 只有在 `H≥1` 时才不可选；Atom 从高度 1 的 Rigid 开始。`AND` 用等高后的 Dead 第三子树，`Pad` 逐层补高，`OR` 用两 guard 集合交于一个 fresh color 并加 filler，保证只能选一边。辅助颜色必须在全表达式命名空间中 fresh；Rigid 内部的模板复制不等于跨构件复用。
- **显式复杂度。** balanced AND/OR 给逻辑深度 `O(log(s+2))`，每个三叉树构件显式展开，树节点、颜色 ID 和见证验证均为多项式规模；没有隐式 DAG、指数树或 oracle。故 v1 的 NP 归约与 NP 见证边界保持。
- **原作业矩阵。** 选中的 binary rainbow subtree 将 edge jobs 下送，其余留父；active private machine 的负载为 `4/3`，颜色资源至多接一枚 unit。反向若完整 assignment 的峰值 `<5/3`，每个带 unit 的 active node 至少下送两个 outgoing jobs，递归得到完整 binary subtree；`C<2` 保证叶颜色单射。无 binary rainbow 时 root-to-leaf 路径给 `C≤5/3`，因此该窄对象的 YES/NO 桥为 `OPT≤4/3` 对 `OPT=5/3`，乘性比 `5/4`。

# 与既有三源审查的关系

作者证明采用 Dead-AND；既有 independent cover 使用公共 anchor 的 A-copy AND。两条构造承重不变量不同，但都指向同一 Exact 对象和同一 ordinary-job 矩阵。该 read-after 源不产生第二个 theorem，也不把 v1 的 4/3、5/3 桥推广到一般 unrelated-machines、shared DAG、任意颜色规则或 near-two gap。

# 需保留的修正与缺口

作者末尾“每个 job 两资格”按字面不适用于 root pin；准确表述应为“除 root pin 的单资格外，其余 jobs 至多两资格”。这只是文字范围修正，前面的完整 P 定义、负载计算与 NP 见证没有被破坏。源未运行代码、未做有限枚举、未核外部文献新颖性，也没有提供一般 hardness、算法或近二放大。

建议将本源 `integrated` 到既有《三叉彩虹二叉子树三源精读与原 P 边界》并保留本页作为 proof-read-after 版本证据；第三阶段建立 provenance 边，不创建新数学对象。
