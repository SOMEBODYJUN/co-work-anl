---
id: customer-attraction/R105-zero-repair-simplified-source-review-Boss8
kind: review
 type_tag: 审查
 title: R105 zero_repair_simplified 交接源复核
 status: local-draft-awaiting-push
 truth_status: exact-duplicate-encoding-of-finite-obstruction-witness
 review_level: full-source-read-and-cross-comparison
 source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/zero_repair_simplified.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/zero_repair_simplified.json
---

# R105 `zero_repair_simplified.json` 交接源复核

## 1. 来源与实际读取

本次按 cleanup 源 ID `9dc1659211141206f258` 读取冻结文件的完整 406 字节（SHA-256 `7d33861f0ce051b21c01e05d23d3de4083f8d2a8bcb5db633c817217232a213a`）。两个冻结定位均指向相同内容：legacy-cleanup 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 main 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。

文件字段为：`weights`（16 个四主题子集的重数）、`background=0`、`path=[2,1]`、`old_policy=[2,2,1,2]`、`new_policy=[2,3,1,1]`、`total_clients=18` 和用途说明。它没有省略尾部字段；没有客户权重的浮点或随机近似。

## 2. 数学内容和编码核对

把四主题按位掩码 1=A、2=B、4=C、8=D 解释，唯一非零重数是

| mask | 主题集合 | 重数 |
|---:|---|---:|
| 2 | B | 2 |
| 3 | A,B | 2 |
| 4 | C | 2 |
| 6 | B,C | 1 |
| 9 | A,D | 1 |
| 11 | A,B,D | 4 |
| 12 | C,D | 4 |
| 13 | A,C,D | 2 |

重数和为 18，与 `total_clients` 一致。该多重集合逐项等于已冻结并入证据的 `zero_regret_repair_witness.json`（源 ID `4d338c7997d6470a198b`，SHA-256 `4f2397c2ace31a594dcc1f7f36547dd2a33a094f1baf4e1b88c5c66c88e6ba5a`）的八种客户类型。

`old_policy=[2,2,1,2]` 等于完整 witness 的 `old_tail_strategy.last_after_first`，`path=[2,1]` 等于其 `first_action=2` 及实际末位动作；`new_policy=[2,3,1,1]` 等于删背景后的唯一完整尾部策略（首位 3，末位菜单 `[2,3,1,1]`）。`background=0` 是该简化记录的内部索引，不能误读成“无旧背景”：同一记录的用途和配套 witness 明确旧背景为主题 A（mask 1），删除后为空背景。

## 3. 与全仓相关材料的比较

已读并核对下列相关材料：

- `new_cross_branch/README.md`（源 ID `58e131b18738d98732ec`）：说明该工作区是一般合法背景删除修复障碍，不是 Q-CAG-HALF 反例；给出零实际 regret、旧尾福利 17、删后完整 SPE 福利 16 以及整数复制边界。
- `zero_regret_welfare_repair_obstruction.md`（源 ID `1ee4950f653a57911a9b`）：完整收益表和复制论证；明确 A 是合法离轨背景，不是原三人实际根。
- `zero_regret_repair_audit.json`（`737cdb8329d3374e771f`）和 `zero_regret_repair_complete_audit.json`（`a23252287ad31ae4dd2b`）：完整枚举各 1024 个尾部策略，原唯一 SPE 为 `(2,[2,2,1,2])`、删后唯一 SPE 为 `(3,[2,3,1,1])`，实际节点 regret 为 `(0,0)`，福利从 17 降到 16，删后 `OPT_2=17`。
- 父方独立复核 `parent/zero_repair_independent_review.md`（源 ID `6354c5286001337384ec`）及结果 `archives/customer-attraction/state/审查/零实际后悔修复障碍的父方独立复核--审查.md`：独立逐单位重放并保留“合法背景/实际根/可信离轨菜单”边界。
- 现有 canonical 审查 `R105零regret修复JSON完整枚举接续审查--审查.md` 已把 witness、两个 audit JSON 和证据副本纳入正式对象；其证据目录是 `archives/customer-attraction/tools/evidence/R105-zero-regret-json-20261031/`。

比较结论：`zero_repair_simplified.json` 只提供已被正式 witness 表达的同一客户多重集和两份策略的 16-mask 压缩编码；没有新的收益表、策略枚举、根分类、一般量词或反例范围。`path`、`purpose` 与 `total_clients` 是方便复现的元数据，不能升级为新的数学命题。

## 4. 处置判断

处置建议为 **duplicate**，目标是保留其来源追踪而不再创建第二个数学对象：

- `archives/customer-attraction/state/审查/R105零regret修复JSON完整枚举接续审查--审查.md`
- `archives/customer-attraction/tools/evidence/R105-zero-regret-json-20261031/zero_regret_repair_witness.json`

不标为 retired：该文件是真实的、可复现的有限输入编码，且明确记录了上一工作区的简化步骤；只是在语义上与已并入的 witness 严格重复。若后续需要复现 mask 编码，可把本文件作为来源别名引用，但不应把 `background=0` 当作改变模型的独立背景。

本复核确认的数学状态仍是：这是一个有限、精确、可复制放大的“实际节点零 regret 不足以保证任意合法背景下的全树 SPE 福利无损修复”障碍；它不是 Q-CAG-HALF 的反例，也不触及实际根单删版本。任何正面修复定理都必须额外声明原根激励、删后离轨菜单信用、被删玩家收益或其他付款信息。

## 5. 本地交接状态

正文和 receipt 草稿只写入 `cleanup/workspaces/Boss8/handoff_zero_repair/`。本轮未执行 `clean claim`、`clean done`、Git commit 或 push；远端写端点此前被自动审查拦截。待 Boss8 获得可验证写权限后，应先把正式正文/证据 checkpoint 并确认 `pushed`，再按 `receipt-draft.json` 逐源登记 `duplicate`。
