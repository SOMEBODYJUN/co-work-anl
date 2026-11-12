# solver-v2 来源接口修复审阅

实际身份仍为 `/root/visible_joint_v6_solve`，Boss1 / six-boss1-20261111 / full。新包目录为 `visible_maximum_joint_v6_solve_v2`；不是新输入或新数学系统。

## 原事实与授权范围

原 Main release 经 SHA 核对后，本席实际运行了旧 `preflight.py --released`。它读取了获准的冻结 v6 资产，在 source_pins 接口检查前消费为0；没有进入 solve_once，没有调用优化器，没有读旧 primal/dual/face。原错误是代码要求 `sources` 字典，而实际冻结文档为 `v6_exact_read_set_pins_v1`，只有 schema/read_scope/files，files 有44项。原失败回执、九个代码及所有原静态资产哈希另行冻结，原 release 已由 Main 撤回。本页不声称从未接触输入或来源。

Main 随后明确允许在本新目录修复这个固定接口，并允许零优化的完整加载检查。`repair_read_plan.json` 是本席对这条授权的记录，不是本席伪造的 Main release。

## 严格接口修复

九个 core 逐个从原冻结目录复制；所有逐行改动见 `core_interface_patch.diff`。source-pin parser 只接受精确 schema、精确 read_scope、仅 schema/read_scope/files 三个顶层字段；files 必须恰44项，每项仅 path/sha256/bytes。路径须是44个实际已冻结、顺序一致、唯一的规范 repo-relative 路径，SHA 必须64位小写完整值并等于已冻结值，bytes 必须是同一非负整数（拒绝bool）。缺失、重复、未知、路径别名、错误SHA/大小和多余字段均拒绝。

先通过整个清单的结构及精确44项对比，再逐文件读内容、核完整 SHA 和字节数，最后只在内存建立 sources 映射。没有改写 source_pins，没有递归追旧 source/release metadata，没有跳过任何文件。原新行 source_package/source_file 路由仍必须落在该已核映射内。

## 原模型与程序边界

4177 原行、513非负列、2自由等式、3056字面父行、30条rhs=-1、全部零行/重复、原objective、K及原数值除数都不变。修复不从数值结果或旧支持导出模型。

独立X旁挂更正与Main语义释放现在也由加载入口直接核SHA并纳入pins：X在固定actual前四负载P下，一次从整个共同合法目录选择argmax f_P，随后处处沿用同一X；C是最大裸覆盖标签；新增局部任意合法T只可特化为该X，不能取消父行最大性前提。

`solve_once.py` 仍只有唯一原 linprog 调用，仍调用 `load_released`；它无法使用 `load_repair_read_only`。新正式 gate 要求新solver-v2 schema和package、Main标识、准确新scaffold SHA及全套原证据。旧release被读取时只提取input/evidence pins；旧schema、status、authorizer、instruction及optimizer权限都不复制，修复bundle写明optimizer权限0。

两套独立 checker、精确恢复和完整零余量最优面数学逻辑不变。未经Main新release不生成消费标记、不导入优化器。最终冻结要求实际完整零优化repair检查通过并与全部9core SHA一致。

## 本次实际零优化加载结果

`repair_preflight_result.json` 返回 `PASS_ZERO_OPTIMIZER_REPAIR_FULL4177_SOURCE_PIN_INTERFACE`。全部44文件内容SHA及bytes验证通过；全4177原行、513非负列、2自由等式、3056字面父行、30条rhs=-1、4177条catalog和新来源路由通过。零系数行索引[45]以及全部560类精确重复约束保留在报告中。全读入pins共83项，包含独立X更正、语义释放、输入资产和全部来源；未递归展开旧来源metadata。原/新消费标记均不存在、新Main release不存在、累计优化调用0。
