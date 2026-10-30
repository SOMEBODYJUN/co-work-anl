---
id: "unrelated-machines/upper-column-budget-matroid-rounding-review"
kind: "review"
type_tag: "审查"
title: "上列预算拟阵基加B舍入双源审查"
status: "finite-exact-evidence-integrated"
truth_status: "upper-only finite audit and explicit statement-first rounding contract; no lower-bound or production-backend claim"
review_level: "full-json-read-code-and-statement-first-comparison"
scope: "parallel-copy transversal-matroid base rounding under nonnegative column budgets"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/upper_column_budget_base_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/upper_column_budget_base_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/upper_column_budget_base_clean_source_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/upper_column_budget_base_clean_source_audit.json"
---

# 对象和精确合同

本审查逐项读取两个冻结 JSON、`tests/audits/unrelated_machines/upper_column_budget_base_audit.py`、其核心依赖和 statement-first 重构稿。库存稳定 ID 为 `7ef9768b487a7b70c354`（文件 SHA `6f2c702fbf3e99d0c8a2e8e40d42c572898f418ef9d04b99a9a7f0874f8a41fe`）与 `09ebde0c2ea41a911f1e`（文件 SHA `470c89070dfe6729111d50b9a8648d2e019dec6325b997c49c8e27ae599d67ed`）。后者只移除了有限 vertex core 末尾一个 LF，报告保留旧 SHA 并明确数学函数字节不变；两者不是两个数学实例。

精确合同是：显式有限基集 (E)，非负有理矩阵 (A\in\mathbb Q_{≥0}^{m\times E})，每列总量 (sum_i A_{ie}\le B)，显式 (b\in\mathbb Q^m)，以及满足 (x\in B(M)\cap\{Ax\le b}) 的分数点。(M) 是显式二分匹配定义的 transversal matroid 的 parallel extension：同一原元素 class 的 copies 至多选一，原元素独立当且仅当可匹配。目标只保证存在实际 base (I) 使
\[
A\mathbf1_I\le b+B\mathbf1.
\]
这是 upper-only 结论；不承诺成本保持、lower bound、未知好基搜索或压缩 copy universe 的显式输出。

## 紧拟阵行和删除安全性

statement-first 稿件的核心计数是：取当前残余 polytope 的原元素投影顶点 (y)，若所有坐标严格分数，则紧拟阵 rank 集族可取一条不可细化链，分块数至多残余 rank；因此顶点所需的紧上列约束至少有 (n-r) 条。对紧 rows (H)，设全选亏缺 (F_i=sum_e A_{ie}(1-y_e))。列总量条件给
\[
sum_{i\in H}F_i\le Bsum_e(1-y_e)=B(n-r),
\]
故存在一条紧 row 的 (F_i\le B)。删除这条 row 对未来任何 0/1 base 都安全：当时已固定部分达到其旧 RHS，所有未来元素总贡献至多分数剩余的全选亏缺 (F_i)，所以最终不超过 (b_i+B)。若坐标为 0 删除元素、坐标为 1 收缩并扣除行 RHS；若全分数则删除安全 row。每步删除一个元素或一条 row，最终得到 base。

这一论证的量词依赖三个假设：系数非负、每列总量统一受 (B) 控制、以及当前点是原元素坐标投影的顶点。它不能用于负列、非统一列预算、或只取 extended LP 任意顶点的版本。拟阵 tight-set 链只用于存在性计数；算法不需枚举所有 tight sets。

## 显式匹配和 parallel-copy 边界

statement-first 重构还给出显式 matching 实现：用原元素/parallel class 的容量约束和二分匹配流构造 extended formulation；保持原 formulation，只加已固定的 (x_e=0/1) 和当前 upper rows。为取得原坐标投影顶点，对 x 坐标逐一 lexicographically 最小化，不能把 extended-space 任意顶点误当成投影顶点，也不能未经证明在 contraction 后重新写一个 transversal presentation。

这是本源最重要的模型边界。有限 audit 中的 `naive_copy_graph_counterexample` 有 actual bases 2、actual resource cost 100，而错误地把 copy 邻接复制到图后得到 fake cost 0；原因是 naive graph 同时选同一 home 的两个 occupied copies，违反 parallel extension。该反例阻止“把每个 copy 当独立资源”这一常见简化。

## 冻结 audit 的实际范围

两个报告均为 `fractions.Fraction` 精确枚举、无浮点裁决，seed `913014`，scope 明确是 finite exact audit only，且显式枚举 integer bases 与 lambda vertices。总计 187 cases（其中 180 random）、283 face checks、1062 vertex candidates、380 integer choices、96 deleted rows、最大删除行数 5；27 个 case 没有 exact-budget integer choice，但所有 case 都有 augmented (B)-budget choice，且 `all_assertions_passed=true`。回归不变量包括：每个 home 有一个 zero-cost empty mode、每个 home 至多一个 occupied copy、tight rank-set chain、(d=\#fractional\ copies-\#blocks)、(sum(1-x)\le d\le\) retained rows、envelope 总量界、support zero 不重新开放、最终真实 row loads (le C+B)、独立 permutation matching recovery。

这组数字验证固定生成器和边界实现，不能替代声明中的多项式有理 LP backend。报告明确未检查 production polynomial rational-LP backend、general-input structure extraction 和 external novelty。`all_assertions_passed` 也不意味着对所有输入自动生成完整 base。

## 与既有内容比较、处置和缺口

1. 与既有 matroid/rounding 讨论：本源把“非负列总量约束下删除上列、最终加 (B)”写成一个上界合同，并把 parallel copies 的正确流模型及错误 copy graph 反例固定下来。
2. 与调度/资源存档：这是把分数配置转成 integer base 的上列证书，未声明 lower/cost 保持，也不等价于完整调度算法或 PNE 构造。
3. 与冻结/增量：`upper_column_budget_base_clean_source_audit.json` 仅做 EOF 清洁版本，保留原报告和旧核心 SHA；其独有内容是字节变化说明，不是新的数学断言。

**可保留的完整结论：** 在显式 parallel-extension matroid、非负矩阵和统一列预算的合同内，紧拟阵行计数支持逐步删除安全上列，有限审计覆盖所列实例。

**有限实验：** 187-case exact audit、顶点/面/整数选择计数、巨大有理分母边界和 naive-copy 反例。

**未解/障碍：** 生产级多项式 LP 实现、压缩而未展开的 copy universe、任何负系数或非统一预算模型、成本保持与 lower bound、以及其在后续调度/近似目标中的完整接续仍未完成。不能以这两个 JSON 宣称一般基舍入算法已经部署，也不能把上界 (+B) 改成更小统一常数；statement-first 稿件的 rank-one 族只说明该常数的上界锐性方向。
