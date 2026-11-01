# R-105 静态最优指派独立审计：清洗草稿

## 对象身份、冻结版本和读取范围

本草稿只处理同一对象 R-105 的三份冻结来源。三份来源均来自两个冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12`（`legacy-cleanup`）和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（`main`）；两提交内容相同。读取方式是结果仓库根的 `python3 work.py clean show <ID> --out <临时文件>`，未执行认领、done、checkpoint、push 或任何 Git 写入。

| source ID | 冻结路径（相对结果仓库根） | blob / SHA-256 | 内容 |
|---|---|---|---|
| `ec52aba43557844bf416` | `research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/terminal_query/independent_assignment_audit.json` | `b1115b083f672e419851a4bc7b8f5ca6110ecbdb` / `a860f144805263ece3aa034a2e66f1e54adc740d38777cdad6713bd1df997d29` | 247215 字节，完整输出 JSON |
| `58b02396c94ecbef5549` | `research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/terminal_query/independent_assignment_audit.md` | `47ef7cf97eba15f759074c50a57db987900bf638` / `8649c01950883ede8eaceebe66096ec698aa89e1bdc71646c8e48f94b2ea064b` | 5762 字节，审计说明 |
| `c9ed1adac413b4127fc0` | `research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/terminal_query/independent_assignment_audit.py` | `cc97ab31d0e2c31ecb5dbb21ddc39aef3b19d2e1` / `1a4d5aabe8922f6cc03bd2a8e1c8508ef24653663ddee6f5adc47848655b9c5f` | 12527 字节，292 行标准库审计程序 |

程序声明并在输出中保留的两个原始依赖是：

- `research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/assignment_instance.json`，SHA-256 `2ae935f6980037f3526eee447021a6e2d8d5987e0bb2b2c31d4017afad7126c4`；
- `research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/assignment_full_policy.json`，SHA-256 `1c59b0406e8fdd56e01fc4a2d1c03b9dd15a9aefc0748a556fb08cf593fa27ac`。

依赖路径中的绝对前缀指向旧工作区；冻结身份应以相对路径、提交版本和上述哈希为准。归档后续副本位于 `archives/customer-attraction/tools/evidence/r105-json/original/independent_assignment_audit.json`、`archives/customer-attraction/tools/evidence/r105-audit-md/original/independent_assignment_audit.md` 和 `archives/customer-attraction/tools/evidence/r105-code/original/independent_assignment_audit.py`。

本次还通读并用于比较的相关正文/后续更新包括：

- `archives/customer-attraction/state/反例/静态最优主题排列的冻结后缀失败--反例.md`（已有有限反例正文）；
- `archives/customer-attraction/state/计算/动态交换完整策略与assignment证书--计算.md`（原七源整理）；
- `archives/customer-attraction/state/审查/静态最优指派桥盲审的双求值与量词核对--审查.md`；
- `archives/customer-attraction/state/算法/全历史策略与最优静态指派的双通路精确审计--算法.md`；
- `archives/customer-attraction/state/计算/静态最优指派独立JSON的全字段精确核验--计算.md`；
- `archives/customer-attraction/state/计算/静态指派与因果单删的单位客户原审计--计算.md`；
- `archives/customer-attraction/state/计算/静态指派两代见证的精确回放与编译分界--计算.md`；
- `archives/customer-attraction/state/障碍/真实分支替代与静态排列的量词缺口--障碍.md`；
- 后续证据包 `archives/customer-attraction/tools/evidence/r105-code/`、`r105-json/`、`r105-audit-md/`、`r105-causal/` 和 `r105-zero/` 的 README、manifest、运行报告及边界说明。

## 定义域和量词

程序合同的接受域是有限玩家数 `m>=1`、有限且标签不同的共同主题目录 `p>=1`、非负整数客户重数。每一行客户类型表示该兴趣集合的若干个相互不同单位客户；允许零重数、重复兴趣行、空兴趣集合、零客户和空覆盖主题。策略文件必须恰好给出所有有序历史

`H = union_{k=0}^{m-1} {0,...,p-1}^k`，

包括离轨历史、重复动作历史和自身比较；每个动作都必须在目录中。客户被 `k` 名选择其兴趣主题的玩家覆盖时，每人获得 `1/k`，总福利是被至少一人覆盖的客户数。程序不暗中加入目录外的空主题，也不枚举所有策略，只检查输入的这一份完整策略。

被审计并被否定的静态桥是

`for every finite instance and every full-history pure SPE terminal z, there exists an optimal m-topic tuple T and a permutation pi such that sum_i u_i(T_{pi(i)}, z_{-i}) <= W(z)`.

这里 `u_i(T,z_{-i})` 是只把实际终局 `z=(S_1,...,S_m)` 的第 `i` 个行动换成 `T`、冻结其他实际行动所得的查询收益。它不是在偏离历史上让后继按策略响应的真实 SPE 偏离收益。三份源只需要一个 `m=3` 实例即可反驳这个全实例/全人数静态断言；它没有把量词升级为“恰六人”或一般 Q-CAG-HALF 的反例。

固定实例的真实域是三名玩家、六个主题、63 个正重数兴趣类型、1953 个单位客户、每主题 992 个客户。六个主题均非空且不同。完整策略有 `1+6+6^2=43` 个决策历史；允许重复和离轨平局。实际终局为 `(0,3,4)`。

## 算法、证据和可复现性

`c9ed1adac413b4127fc0` 只使用 Python 标准库、`Fraction`、`itertools`、`hashlib` 和 `json`，不导入项目模型、求解器、作者审计或数值库。它有两条逐终局求值路径：

1. 将每个客户重数展开成不同单位客户，按每个终局的客户负载直接计数；收益乘 `lcm(1,...,m)=6` 后为整数。
2. 直接遍历压缩兴趣类型，以 `Fraction(count, number_of_liking_players)` 分配客户份额。

程序在全部 `p^m=216` 个有序三主题终局（包含重复动作）上比较两条路径的每位收益和覆盖，并核对收益总和等于福利。随后对全部43个历史、每个历史的6个强制动作回放同一策略，得到 `43*6=258` 个真实比较；偏离动作之后允许后继按偏离历史响应，不冻结实际后缀。最后枚举每个最优有序元组及其全部槽位排列，逐项计算静态查询和，并确认输入原字节未改变。

归档的后续真实复跑见 `archives/customer-attraction/tools/evidence/r105-code/replay/run-manifest.json` 和 `.../stdout.txt`：Python 3.12.14、断言开启、exit 0、一次运行，1953 客户输入得到 `spe_violations=0`、`W=1735`、`OPT=1740`、最小静态和 `1736`。运行报告去除仅有运行位置的两个 `raw_inputs.*_path` 字段后与冻结 JSON 相同。冻结 JSON 的定义级重建见 `archives/customer-attraction/tools/evidence/r105-json/verify_frozen_json.py` 和 `verification-report.json`：216 终局、648 个收益坐标、258 行真实比较、36 个指派行均通过；该核验不执行原审计程序。

代码合同的边界已由 r105-code 探针保留：非SPE低福利输入可以使 `q_cag_half_is_refuted_by_this_input=true`，但因7项IC违规不构成SPE反例；缺一个离轨历史会以 `AssertionError: policy must cover exactly every legal history` 退出且不写报告；零客户单主题边界可正常处理。这些探针用于校验接口，不是新数学对象。

## 冻结数值结论

- 216 个终局的双通路结果全部一致；每个终局的收益和等于覆盖。
- 最优福利 `OPT_3=1740`；恰有 `(1,2,5)` 的6个有序排列，唯一最优无序支持 `{1,2,5}`。
- 完整策略的258项真实比较均非负；215项非自身比较中154项严格、61项平局，最小非自身松弛为0，故这份策略是给定输入上的完整有序历史纯SPE。
- 实际终局 `z=(0,3,4)`，收益 `(1733/3,1736/3,1736/3)`，`W=1735`。
- 静态替代矩阵（每项乘3，行是代入主题1、2、5，列是实际玩家1、2、3）为

  ```text
  topic 1: (1736, 1739, 1736)
  topic 2: (1733, 1736, 1736)
  topic 5: (1736, 1739, 1736)
  ```

- “6个最优有序元组 × 6个槽位排列”共36个检查，归并为6个玩家指派，静态和依次为 `1736, 1737, 1736, 1736, 1737, 1736`。因此最小静态和 `1736=W+1`，该单实例严格否定静态存在指派桥。
- 同一实例的 half 量为 `2W-OPT_3=3470-1740=1730>0`，所以它不是 Q-CAG-HALF 反例。JSON 中 `general_q_cag_half_status: OPEN` 与 `novelty_claim: false` 只能作为来源自述范围保留，不能当一般定理证明。

## 与已有对象的差异和关系

1. 与 `customer-attraction/frozen-suffix-optimal-topic-assignment-counterexample`（`archives/customer-attraction/state/反例/静态最优主题排列的冻结后缀失败--反例.md`）相比，三份新源是同一固定实例的独立双通路审计材料：JSON保存全216覆盖、258比较和36指派；MD明确静态/动态量词；PY给出可复现实现。它们没有第二个实例或新命题。
2. 与 `customer-attraction/dynamic-exchange-assignment-certificate` 相比，原对象保留七源正文/输入/策略/witness/作者 exact 报告；本三源不替换 witness，也不证明 Möbius 生成器。独立代码只从冻结 input/policy 重算，故独立性是“给定原始字节的实现复核”，不是独立发现或外审。
3. 与 `customer-attraction/independent-static-optimal-assignment-audit-quantifiers`、`customer-attraction/full-history-policy-and-optimal-static-assignment-dual-evaluator` 相比，本三源正是这两个后续对象的主源，增加了全字段核对、缺失历史/非SPE探针和一次真实复跑的可复现证据；仍只认证给定输入/策略。
4. `静态指派两代见证的精确回放与编译分界`区分了35坐标/37历史的辅助小 witness 与正客户编译后的43历史/258比较完整输入；本三源只审后一份1953客户输入，不把辅助 fresh 域直接当完整SPE。
5. `静态指派与因果单删的单位客户原审计`、`终局冻结钱包原程序及完整策略复跑`、`跨角色替换门原程序的依赖与精确复跑`提供同一输入的其他固定接口检查。它们的真实分支/删除/容量对象有不同收益和量词；不能把其有限数值并入本静态指派桥，也不能把本静态矩阵失败写成真实动态预算失败。
6. `r105-causal` 的单客户因果包络和 `r105-zero` 的18客户零后悔删除修复障碍是相关但不同对象；前者只给松弛标量包络，后者只给固定背景删除修复反例，均不应合并为 R-105 静态指派反例或 half 结论。

## 缺口、复现限制和不应外推之处

- 这是一个给定三人、六主题、1953客户、给定完整策略的有限检查；没有枚举任意输入、任意策略、任意人数，也没有六人实例。
- 两条求值路径共享同一原始输入与 Python 运行时，不能替代模型级独立证明；作者“只先读两份 raw”的历史声明不能由 JSON 布尔字段独立认证，且后续审查已读作者对象，不能再次称本轮盲审。
- 原程序使用 Python `assert`，在 `python -O` 下断言可被关闭；其输入检查也不是完整 JSON schema（例如 `bool` 属于 Python `int`，JSON 重复键由解析器处理）。复现必须保持断言开启并使用新输出路径。
- 报告只保存了经过核验的全字段/汇总，不应把程序的“exit 0”或 half 状态位单独解释为SPE或半覆盖结论。
- 没有复杂度保证、全局搜索保证或新颖性/外部同行评审。有限静态桥失败不推出 FTA、ROW、聚合安全值、真实菜单信用或任何全局支付接口失败。

## 建议处置

| source | 建议 | 理由 |
|---|---|---|
| `ec52aba43557844bf416` JSON | **integrated + retained** | 将全字段结果接入 `customer-attraction/independent-static-optimal-assignment-audit-quantifiers` 与 `...full-history-policy-and-optimal-static-assignment-dual-evaluator`；在 `archives/customer-attraction/tools/evidence/r105-json/original/` 保留原字节。与 r105-json replay 是同一结果的派生副本，可标 duplicate-of-replay（仅关系标注），不退休原冻结源。 |
| `58b02396c94ecbef5549` MD | **integrated + retained** | 将定义域、静态/动态量词差异、1953纠正、36项存在量词穷尽接入现有审查和反例正文；`r105-audit-md/original/` 保留来源。与既有反例正文叙述有内容重叠，但历史来源独立，标 narrative-duplicate-of-existing-object，不删除。 |
| `c9ed1adac413b4127fc0` PY | **integrated + retained** | 将双通路算法、完整历史策略合同、静态枚举和边界探针接入算法对象；`r105-code/original/` 与一次 replay 保留。它与作者 `audit_assignment_witness.py` 不是同一实现，不能标为代码重复；仅其 replay JSON 与 `ec52...` 结果字段可标派生重复。 |

不建议把三份来源标 `retired`：它们分别承担结果、量词说明和可执行算法证据。也不建议新建第二个静态桥反例对象；已有反例对象应作为主数学对象，三源作为独立审计/算法/全字段证据接入。与 r105-causal、r105-zero 等后续对象保持 `related-but-distinct`，不要合并或互相升级结论。

**最终范围判断：**三源共同支持“该固定三人输入中的完整纯SPE严格反驳冻结终局的最优静态指派存在桥”，并支持其可复现性和输入身份；它们不支持一般 Q-CAG-HALF 结论、六提供者结论、真实动态分支支付不可能性或新颖性声明。
