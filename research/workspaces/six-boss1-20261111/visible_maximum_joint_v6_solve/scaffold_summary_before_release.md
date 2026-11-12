# visible_maximum_joint_v6_solve：释放前静态准备

状态：`WAITING_FINAL_INPUT_SHA_AND_EXPLICIT_MAIN_RELEASE`。本包只准备独立新 4177 全系统的一次求解与精确恢复路径；当前优化授权为 0，实际优化调用为 0。

| 标识 | 值 |
| --- | --- |
| owner | Boss1 |
| RUN | six-boss1-20261111 |
| agent | /root/visible_joint_v6_solve |
| profile | full |
| 写入范围 | 本目录及同名外部 summary；不触碰 Git、RUN、map、registry 或旧包 |
| 当前输入 SHA | 未释放；未读取输入 |

## 规划模型，尚非实际输入认证

| 块 | 原始行位置（0-based，右端不含） | 行数 | 数值除数 |
| --- | --- | ---: | --- |
| literal_v5_raw | [0, 3056) | 3056 | 冻结父尺度逐字符串保留 |
| source2_lambda_strip | [3056, 3286) | 230 | 25 |
| source2_lambda_anchor_complete | [3286, 3446) | 160 | 25 |
| later_sources_lambda_cells | [3446, 3996) | 550 | 25 |
| source2_conditional_redistribution | [3996, 4176) | 180 | 25 |
| ROOT270_STRICT_C_OUTSIDE | [4176, 4177) | 1 | 1 |

全域为 513 非负列（512 个完整九位 customer 类型加独立 K）、2 条自由等式，原 objective 不变，30 条 rhs=-1 原始行保留。所有零行、重复和 metadata 保留；不存在固定 K、支持受限 LP、第二 LP 或旧 23676/734 phase-I 入口。

## 文件职责与释放门槛

`contract.py` 只在完整 Main release 通过后读取最终输入或来源。`main_release.template.json` 的授权为 0，所有最终 SHA、确认项和实际审计证据为空。Main 后续须明确释放一次调用，并从实际 JSON 填写：6 项主要准备资产 SHA、raw order SHA、scaffold SHA、literal v5 父输入/尺度 SHA、完整 source-validity scope、准确维度/块/尺度和三个证据角色（main_preflight、source_legality、all_raw_column_audit）。模板存在、输入文件存在或静态 PASS 均不授予授权。

`preflight.py --static --write-report` 只检查本包，解析/编译九个脚本，不导入数值引擎；核查唯一优化调用点、固定参数、释放门→消费标记→优化顺序、独立 checker imports、空授权模板与规划算术。`freeze_scaffold.py` 只哈希该静态包，写 `scaffold_manifest.json` 和 `SCAFFOLD_SHA256SUMS`。

只有最终释放后，才依 `expected_outputs.json` 顺序进行 released preflight、唯一完整 LP、精确恢复、独立 Fraction 证书核验、全部零余量列的完整最优面、独立 Fraction RREF 核验，再生成新正权行的实际来源复核队列。消费标记一旦写成永久保留；异常、超时、失败或精确恢复障碍均不得引出第二次优化。

精确恢复目前采用本次返回支持上的精确线性代数，并对全域重检。若返回支持不足以唯一确定精确解，则报告具体 obstacle，不自行猜旧支持或启动新 LP。完整最优面不受该代表点支持限制；全部零余量列及所有原不等式、非负条件都必须出现。

本包不预判目标值、primal/dual 支持、正权新行、K、C 结构或真实 SPE 结论。当前 source_review 只审查已实读的冻结程序接口；新来源与实际完整输入合法性由 Main 的最终实读证据闭合。

完成静态报告和哈希冻结后，本代理结束本轮并停止写入，等待 Main 后续专门 followup；不会轮询。
