# visible_maximum_joint_v6_solve — 静态脚手架冻结回报

**状态：WAITING_FINAL_INPUT_SHA_AND_EXPLICIT_MAIN_RELEASE。** 2026-11-12 UTC 已完成静态准备并停止写入；等待 Main 后续专门 followup。身份为 Boss1 / RUN six-boss1-20261111 / agent `/root/visible_joint_v6_solve` / profile full。

## 已完成

九个 Python 脚本已从获准实读的 v5 冻结源码独立复制并适配到 v6；`source_reference_pins.json` 记录九份实际源码 SHA。未运行或导入任何旧脚本，未读取旧点、旧最优面、旧证书、父输入或新准备输入。准备席发来的接口说明只用于规划绑定，尚未将其最终 SHA 当作 Main 释放。

当前规划是 4177 = 3056 + 230 + 160 + 550 + 180 + 1 原始行、513 非负列、2 条自由等式、30 条 rhs=-1 行。前 3056 个 raw 对象和原尺度字符串保持 literal；四个新 λ/δ 包共 1120 行除数25，最后 ROOT270 行除数1。新来源 metadata/catalog/source-file 路由逐行绑定。原 objective、独立 K、零行和重复都保留。

唯一优化入口先校验 Main release、精确 SHA closure 与完整模型，再排他/fsync 文件和目录消费标记，之后仅允许一次 `highs-ds`：`presolve=False`、`time_limit=60.0`、primal/dual feasibility tolerance均为`1e-9`。本轮没有调用该入口。

精确恢复从实际唯一数值结果出发，以原尺度 Fraction 验证全行、全列、2 条 signed free equality、目标相等与互补。独立证书 checker 不导入 builder/solver/recovery/SymPy；最优面从全部零对偶余量列建模，并保存所有原始参数不等式与513非负条件，另由独立 Fraction RREF 重算。新正权行只生成实际来源复核队列，不继承旧 C 刚性或旧支持。

## 实际静态检查

`preflight.py --static --write-report` 返回 `PASS_STATIC_SCAFFOLD_ONLY_NOT_INPUT_OR_SOURCE_VALIDATION`：九个脚本解析和编译通过；唯一 linprog 调用点；固定方法、参数和 gate→消费标记→调用顺序通过；checker及contract只依赖标准库/contract；SciPy与SymPy未导入。随后 `freeze_scaffold.py` 冻结15项静态资产；最终独立重新核对16条checksum（含manifest）全部相符。

当前优化授权0、实际调用0。`main_release.json`、`single_lp_consumed.json`、数值输出、精确证书与最优面文件均不存在。静态 PASS 不是准备输入认证、来源合法性证书、数值结论或 SPE 定理。

## 交接 SHA-256

| 本包文件 | SHA-256 |
| --- | --- |
| `scaffold_manifest.json` | `4f9f1389eb6fd6fe3030c0ce37c2a20f2a3116152ad9857a9e0314f2f57fbac1` |
| `scaffold_static_check.json` | `8ac7ae1dd9eba9bfe180afb600486bd144970322f0ed9e9381f1d2f5551bdffb` |
| `source_reference_pins.json` | `991605947f93a7544476f12dcbc87fbac5b9c83fe8b9ef8df02c5431e231c7a7` |
| `main_release.template.json` | `7893cccb0be6e4e2f47de000dea4c62d16433fc997bcef2e99b86ad7b3076b75` |
| `SCAFFOLD_SHA256SUMS` | `0216b2c89026e30e478d4ebe8f4b74bea7453a1b58dbbf05c7c567395e9e6588` |

完整代码 SHA 清单见 `scaffold_manifest.json` 的 `code_artifact_sha256`；全部15项资产在 `artifact_sha256` 和 `SCAFFOLD_SHA256SUMS`。

## 下一步条件

Main 先按原计划完成正文/登记/map与研究 clone 同步。随后只有 Main 明确放行、实际最终 JSON 与全部精确 SHA 到位时，才创建完整 `main_release.json` 并进行 released preflight。模板目前授权为0、实际确认与SHA字段为空；需要最终 input/freeze_manifest/scaling/catalog/source_review/source_pins、literal v5 input/scaling、raw-order、scaffold和三种审核证据绑定。

如果唯一数值结果的支持不能唯一确定精确恢复，程序写 `recovery_obstacle.json` 并保留原消费记录；不猜支持、不换旧点、不启动第二个LP。本文没有触碰 Git、RUN、map、registry或旧包。此轮已结束，不轮询输入，不继续写入。
