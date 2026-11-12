# v6 求解脚手架：实读源码与改动边界

状态：仅静态准备；Main 尚未释放最终输入 SHA 或一次求解。身份为 Boss1 / six-boss1-20261111 / `/root/visible_joint_v6_solve` / full。

## 实读材料

只读取了冻结 `visible_maximum_joint_v5_solve` 内下表九个 Python 源文件的文本，用于复制并适配程序接口。没有导入或运行其中任何脚本；没有读取旧 exact input、数值输出、primal 点、证书、最优面或来源专属结论。精确路径与 SHA 保存在 `source_reference_pins.json`。

| 冻结源码 | SHA-256 |
| --- | --- |
| `contract.py` | `5cd659955e8464ab1b418a2f0f6f7b828a66664248bbc71fe69f0ba1d01e55a6` |
| `preflight.py` | `bfcefb5d73b19f646f63de73cbe0762cb9168fd005cbd1acfe3bb4884bacbf06` |
| `solve_once.py` | `0ddf70e27f3443d67864f3238d3599486920f20a9d58e080169835e01e420be3` |
| `recover_exact.py` | `6f528b2daa937f57c623ea3a600b2e6f25f0ac559111a3f82aef4ffbd2e1eedb` |
| `verify_certificate.py` | `17b1f54efe303361d01757ca427465ac5eee715bbdc7ee361184930cb95072ba` |
| `analyze_optimal_face.py` | `5880395a045e22669785184807854b45272971e6205f463c9fbd9a0b24aaaf33` |
| `verify_optimal_face.py` | `d111991ab8af5ba1220f56d553a0cdb0fdfaf80944702087685f84f250974a32` |
| `diagnose_true_payments.py` | `3e7d8dda61982678fcde58220d0bcbbde8f8882d77ab470895eee2a77116288f` |
| `freeze_scaffold.py` | `97e5983d04857541be8edd2f8540dfd7fe622fa213e017490383009c2f6a8a20` |

## 新程序的实际适配

- 身份、状态、输入路径和证书 schema 全部切换到独立 v6 求解包；文字上的 literal parent 是 v5 的 3056 行冻结输入，不是旧求解结果。
- 规划完整模型为 4177 原始不等式、513 个独立非负列和 2 条自由等式。分块依次为 3056、230、160、550、180、1；不剪行、列或重复、零行，不固定 K，不改原 objective 或 30 条 rhs=-1 行。
- 前 3056 行要与最终获准父输入逐对象相等，尺度字符串保留。新增前 1120 行除数 25，最后 ROOT270 行除数 1；除数仅用于数值输入，不冒作真实 IC 权重。
- 四个新 λ/δ 包逐行要求原 id、source_row_id、source_row_index、source_package、source_file、全部 source_row_metadata 和 source_row_object_sha256。来源全路径从当前行 metadata 路由；新 row_catalog 逐项核对。ROOT270 原对象保持 literal，不套用四包 wrapper。
- 唯一 linprog 调用前必须通过 Main release、完整 SHA closure、原模型字段和全部来源审计证据；再排他写入并 fsync 消费标记及父目录。固定 highs-ds、presolve=False、60 秒、双容差 1e-9；异常或失败也不重试。
- 精确恢复只使用本次实际结果。原尺度 primal、raw dual 和两条 signed free equality multiplier 全部用有理算术验证；线性代数不唯一或任何精确检查失败即保存 obstacle。
- 独立证书 checker 不导入 builder、solver、recovery 或 SymPy，重新解析原系数并用 Fraction 检查所有 4177 行、513 列、2 等式、目标、互补、原尺度及全量 literal metadata。
- 最优面从全部零对偶余量列建立，保留每条原始参数不等式与所有非负条件；另一个 Fraction RREF checker 独立重算。源函数固定性只是完整面的 signed equality identity，不是普遍非负付款证明。
- 正权行只生成与当前 metadata、catalog 和 source SHA 绑定的待复核队列；不复用旧正权行、旧支持、旧 C 刚性或旧弱零态结论。

## 当前未证事项

此文件不是新来源合法性审核、准备输入核验、数值求解、精确最优值、完整有序纯 SPE 实现或 half 问题定理。输入、freeze_manifest、scaling、catalog、source_pins、source_review 的实际内容与 SHA 均等待 Main 明确发来的最终材料。本轮没有读取 `visible_maximum_joint_v6` 目录。
