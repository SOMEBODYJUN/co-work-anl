# R-44b24 true_counterexample 前三个源实读回执（隔离草稿）

## 来源与冻结指纹

- `a607df1fe2b98e17868c` — `true_counterexample/README.md`, SHA-256 `805470d973c28b39aca717c4850864564ae41ff727edb48c776f532a31b467bb`，6193 B。
- `1ecdd1273661490c6299` — `true_counterexample/audit_saved_policies.py`, SHA-256 `c150ed13bf2faec26b34ed084b404020639b3252b2cad19ca1c207f49a59cdf7`，3164 B。
- `c18e27c5f56908a85700` — `true_counterexample/audit_warm_start.py`, SHA-256 `98480ec43518838e857d1e01e2e81060ad236384e99d05ce3ee9d44fb715fd73`，3471 B。

三源均由 `work.py clean show` 从冻结提交导出；没有把当前结果分支的缺失工作区路径误当成已读。

## 实读结论

README 的准确身份是“完整终局证人 DAG 的可行热启动与真实反例搜索”。它明确写出一般 Q-CAG-HALF 未闭合、本组没有目标反例，内容是 SciPy/HiGHS `setSolution` 热启动、完整历史策略展开、固定实例的有限精确回放及后续搜索边界。核心数值为五人七主题自由重数的 9/5 证人（9 客户、W=5、OPT=9）和根 `(4,1)` 的 23/14 证人（46 客户、W=28、OPT=46）；均有 `2W-OPT>0`，不是 half 反例。README 还明确 `--radius` 与 `--restrict-outcomes` 是合法子域限制，浮点 MIP 状态不是有理证书，不能推出一般上界/反例。

`audit_saved_policies.py` 不导入规范包或优化器，直接从 `warm_m5p7.json` 与 `warm_m5p7_41.json` 的 `integer_clones`、完整 `strategy.actions` 和声明字段，逐单位客户以 `Fraction` 重放所有有序历史的一步偏离，再重构覆盖类商策略并核其偏离。两个动作表各有 `1+7+49+343+2401=2801` 节点、每节点 6 个非规定行动共 16806 次比较。程序输出与冻结 `saved_policy_audit.json`（source id `8999985a037cb0e7965c`）逐字节相同，SHA-256 均为 `9110d5ffe648b7e6e2b6577bab856d970d4a2a31f5388e95c09bd26e3e76a5a3`。结果：

| 输入 | 单位客户 | W | OPT | 比值 | 覆盖类 | 商节点/偏离 | half margin |
|---|---:|---:|---:|---|---:|---:|---:|
| `warm_m5p7.json` | 9 | 5 | 9 | 9/5 | 5 | 781 / 3124 | 1 |
| `warm_m5p7_41.json` | 46 | 28 | 46 | 23/14 | 7 | 2801 / 16806 | 10 |

因此这是两份指定完整策略的精确有限审计与覆盖商重构，不是全部策略的上界，也不是七个不同主题的普遍结论。

`audit_warm_start.py` 先用 `warm_dag_search.initial_vector` 构造终局菜单 seed，再以 `only_check` stub 替换 MILP 优化器，检查完整稀疏模型的行界、变量界、二元整性，并保留完整非计数历史的非 Markov 选择。为运行它，隔离导出了冻结的 `warm_dag_search.py`、完整 `customer_attraction`/旧 DAG 依赖及 `markov_obstruction_report.json`；不修改仓库。实跑结果为：42 个正福利有限输入通过、2 个无效 seed 边界拒绝、已知三人五主题非 Markov 根 023 被接受，且同计数不同动作确实存在；`row_lower` 最大为 `1.1102230246251565e-16`，其余残差为 0。生成的 `warm_seed_audit.json` 与冻结 source id `23c8f24257358e43f87d` 逐字节相同，SHA-256 均为 `d2e4d1bb5e0404b6d8b5845a9b7166d78ee7713762211829ae5b60cfd0f734f6`。

## 与现有正文的比较

结果分支已有三份自足 canonical 对象，均明确引用并覆盖本批来源：

1. `archives/customer-attraction/subarchives/six-providers/state/计算/保存策略的单位客户重放与覆盖类商--计算.md`：覆盖 README 与 `audit_saved_policies.py` 的固定策略、单位客户 Fraction 回放、覆盖类商和量词边界。
2. `archives/customer-attraction/subarchives/six-providers/state/计算/热启动全模型残差与非计数种子回归--计算.md`：覆盖 `audit_warm_start.py`、`warm_dag_search.py`、依赖闭包、42-case seed-only 残差审计和非 Markov 回归边界。
3. `archives/customer-attraction/subarchives/six-providers/state/计算/五人热启动保存策略的单位客户与认证范围--计算.md`：覆盖 README 所述三份保存策略、9/5 与 23/14 固定实例、完整历史解析边界及浮点/固定锥/搜索层级。

逐段比较未发现需要新增 canonical 数学对象：三源的独有内容已经由上述对象以正确的有限/审计/候选边界收入；没有把有限证据升级为一般 Q-CAG-HALF、六人 half、普遍 MIP 最优或反例。

## 建议处置

- `a607df1fe2b98e17868c`：`integrated`，目标为上述三份计算正文（主落点为“保存策略的单位客户重放与覆盖类商--计算.md”和“五人热启动保存策略的单位客户与认证范围--计算.md”）。
- `1ecdd1273661490c6299`：`integrated`，目标为“保存策略的单位客户重放与覆盖类商--计算.md”，并保留原程序作为可复现资源引用。
- `c18e27c5f56908a85700`：`integrated`，目标为“热启动全模型残差与非计数种子回归--计算.md”，并保留原程序及精确输出哈希。

这些是实际全文阅读、运行与比较后的建议；没有执行远端 `clean done`，不代替根工作树的串行 checkpoint 与登记。
