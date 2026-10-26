# 六人势路线：严格支持分支边界与 ZZ 独审

**本目录没有反驳六人势候选，也没有证明或反驳 six-half。**
无新增数学信息的策略锥阴性探测及发现中间件已清理，只保留两项可复用结果。

## 1. 势最优支持上的选枝与平均均不足

唯一正文：[supported_branch_obstruction.md](supported_branch_obstruction.md)。
六个单位客户、四主题、恰六人完整历史纯 SPE，实际路径 `(3,3,3,2,0,0)`。
实际前缀 `(3,3,3)` 后，局部预算 `14/3`、真最大相对势 `13/3`；
最优支持恰为 `{0,1}`，两条支持分支的到达势加子局预算都为 `29/6>14/3`。
故只选择势最优首主题、或对它们任取凸平均，均不能修补直接预算归纳。
根在两条偏离上还有严格 `1/6` 收益优势。失效来自丢弃子局预算的 `1/2` 松弛。

完整精确证据：[supported_branch_audit.json](supported_branch_audit.json)、
[supported_branch_six_full_policy.json](supported_branch_six_full_policy.json)。
确定性构造和逐历史 Fraction 核验：[verify_supported_branch.py](verify_supported_branch.py)。
1365 个决策历史、5460 个行动比较全部通过；完整历史依赖与离轨平局均保留。
父方另从完整动作表独立核验，见 `../parent/audit_supported_branch.py` 与
`../parent/supported_branch_independent_exact.json`；审查同样覆盖全部历史、比较及两条局部预算失败。

## 2. 共同原子点新增 60 ZZ 行的独立字面重算

唯一正文：[closure_independent_review.md](closure_independent_review.md)。
独立按 27 原子×66×66 字面标签计算全部 60 ZZ 行，117612 次比较全部精确通过。
共同原子诱导四态、隐式 00 与 RR，逐列匹配旧 schema 全部 1905 列；
另用冻结旧库重放 1083 原始行和 2806 上界行通过。
输入点只是指定 1143 原始行图的精确停界点，`O=1,W≈0.4939735107`，不是 SPE。
同 orbit 位相等仅是此见证采用的受限共同赋值，没有被误当必要模型约束。

实现：[review_joint_atoms_independent.py](review_joint_atoms_independent.py)。
精确结果：[closure_independent_review.json](closure_independent_review.json)。
代码不导入 `joint_atoms.py` 或其 audit；独立重算范围与旧库复放范围在正文明确分开。
