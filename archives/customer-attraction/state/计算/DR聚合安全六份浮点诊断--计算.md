---
id: customer-attraction/dr-aggregate-security-six-frozen-floating-diagnostics
kind: computation
type_tag: 计算
title: DR聚合安全六份冻结浮点诊断
topic: customer-attraction
status: 有限浮点诊断；扩大模型；不是CAG证据
truth_status: finite floating diagnostics only; no exact witness, no general theorem, no CAG counterexample
review_level: clean-show-read-and-byte-compared
source_refs:
  - clean:6c9d817c586d116a7ef2:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_groups_repeats.json
  - clean:615b20e056941847ca2d:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_groups_simple_query.json
  - clean:29bbc735344948028c8b:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_groups_simple_query_diag.json
  - clean:e66595d9da26cedb6334:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_groups_third.json
  - clean:4b98a2950c56d94cfbf5:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_n3k3.json
  - clean:8cda73aa604b09b9b171:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_n3k4.json
  - local:archives/customer-attraction/state/障碍/单调递减边际势的强安全聚合障碍--障碍.md
  - local:archives/customer-attraction/tools/evidence/coverage-moment-and-potential-ledger-primary/related/research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_boundary.md
evidence_packet: archives/customer-attraction/tools/evidence/R-2fc-aggregate-security-tail-20261031/
---

# DR 聚合安全六份冻结浮点诊断

本对象登记 R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security 目录下六个冻结 JSON 的逐文件读数。六项顶层 `status` 都是 `floating diagnostic in an enlarged model, not CAG evidence`。它们搜索的是扩大后的单调/DR 边际势模型或其附加线性约束；没有客户类型、support 不变总收益、均分预算、完整客户实例、全策略树证明或有理化后的精确证书。因此这些结果不能改写为 CAG 反例，也不能从浮点最优值推出普遍强/弱聚合定理。

## 实际来源与字节身份

六个 ID 均通过 `clean show <id> --out` 读出原始字节并写入证据包 `archives/customer-attraction/tools/evidence/R-2fc-aggregate-security-tail-20261031/original/`。清单声明的 SHA-256 和大小均匹配；对应 `legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的 `git show` 输出逐字节相同。比较结果及 Git blob 校验在证据包 `replay/compare_frozen_bytes.stdout.txt` 中，程序退出码为 0。JSON 解析也逐项成功，`python3 -m json.tool` 的六个 stderr 均为零字节。

## 六项读数

| ID / 文件 | 参数增量（相对同一 groups 查询） | seed / trials | `best_objective` | 浮点分类 | witness |
|---|---|---:|---:|---|---|
| `615b20e056941847ca2d` / `dr_groups_simple_query.json` | `k=6,n=3`；query `4/15,0,4/15,0,3/15,4/15`；`no_dr=false`；未加 harmonic 对角、重复或三阶正性；policy `groups` | 22112 / 1 | `-0.0003226252477301038` | 有限负浮点近零 | 有；root `[0,3,4]`，query 概率 `[4/15,0,4/15,0,3/15,4/15]`，43 个 policy 项、83 个 state/potential 项；`value_lower=0.002581001981840806`，`welfare=0.007420380697792314` |
| `29bbc735344948028c8b` / `dr_groups_simple_query_diag.json` | 与上一项相同，另加 `harmonic_diagonals=true` | 22112 / 1 | `-0.00028658162935766944` | 有限负浮点近零 | 有；root、query、policy/state 计数相同；`value_lower=0.0022926530348614574`，`welfare=0.006591377475226701` |
| `e66595d9da26cedb6334` / `dr_groups_third.json` | 与基础 groups 查询相同，另加 `third_positive=true` | 22112 / 1 | `-0.0002817921983817029` | 有限负浮点近零 | 有；root、query、policy/state 计数相同；`value_lower=0.0022543375870536595`，`welfare=0.0064812205627792704` |
| `6c9d817c586d116a7ef2` / `dr_groups_repeats.json` | 与基础 groups 查询相同，另加 `harmonic_repeats=true` | 22112 / 1 | `0.0` | 本次有限运行的精确 JSON 零差；不是“不存在反例”证明 | 无 witness 字段；`completed=1` |
| `4b98a2950c56d94cfbf5` / `dr_n3k3.json` | `k=3,n=3` 的随机诊断 | 22101 / 100 | `0.0` | 100 次有限试验的零差汇总；不是普遍结论 | 无 witness 字段 |
| `8cda73aa604b09b9b171` / `dr_n3k4.json` | `k=4,n=3` 的随机诊断 | 22102 / 100 | `0.0` | 100 次有限试验的零差汇总；不是普遍结论 | 无 witness 字段 |

三份带 witness 的六动作输出使用同一个 root、查询分布、策略字典与状态列表；它们的 `potential`、`value_lower` 和 `welfare` 浮点数组各自不同。重复约束版本仅给 `best_objective=0.0`，没有潜势 witness；`n3k3` 与 `n3k4` 只有 100 次试验汇总，不能补足精确策略或客户实例。除上表列出的约束开关和有限参数外，没有从文件推断未记录的搜索空间。

## 与已归档精确对象的关系

已有对象《单调递减边际势的强安全聚合障碍》给出 84 项整数势、完整 43 个有序节点策略、168 项单调差、252 项 DR 差、258 项真实激励比较和静态安全值 `v=56` 的**扩大模型精确有限证书**；实际路径为 `(0,3,4)`，效用 `(0,105,56)`，总收益 `161<3v=168`，并明确说明该势违反 CAG 的 support 不变预算。六个 JSON 是同一研究入口的浮点探索尾部：它们补全了 query、seed、trial、约束开关、`best_objective` 以及有限 witness 读数，但没有改变精确对象的模型边界，也没有把浮点负点升级为新的整数反例。`dr_boundary.md` 中的五个历史数值与本次读取的前三个 `best_objective` 一一对应；此前只作为线索的值现已由冻结 JSON 核对，零差项也仍只保留为诊断。

以下边界必须保留：

- `best_objective<0` 是固定 policy、固定 query、有限浮点 LP 读数；未给出有理化势、整数客户重数、全真实偏离比较、精确静态安全值或 CAG 支持预算。
- `best_objective=0.0` 只说明相应一次或 100 次浮点运行未记录负值；不能证明没有其他 seed、策略、query、人数或精确方向。
- 相同的 `root`、policy/state 计数和 query 只说明这些三个六动作输出来自同一固定策略入口；潜势数组差异不可当作跨实例的精确比较。
- 所有六项都写明 `not CAG evidence`，所以不能用于否定或证明 CAG 的 strong/weak aggregation、half 或真实客户福利命题。

## 可复核运行

证据包包含以下程序及逐项 stdout/stderr：

- `replay/validate_tail.py`：标准库校验六个 JSON 的字节哈希、字段、参数、witness 计数和有限数值；退出 0，见 `validate_tail.stdout.txt` 与 `validate_tail.stderr.txt`。
- `replay/compare_frozen_bytes.py`：读取两份注册提交的原始 blob，与归档字节逐项比较；六项 × 两提交均 `archived_byte_equal=True`、`blob_equal=True`，退出 0，见 `compare_frozen_bytes.stdout.txt` 与 `compare_frozen_bytes.stderr.txt`。
- `python3 -m json.tool`：六个输入均退出 0；每个 stderr 文件为零字节，格式化 stdout 留在 `replay/`。

`manifest.json` 记录六个源 ID、blob、SHA-256、大小、参数、objective、witness 摘要以及上述运行结果。证据包保留原始 JSON，不修改冻结来源。
