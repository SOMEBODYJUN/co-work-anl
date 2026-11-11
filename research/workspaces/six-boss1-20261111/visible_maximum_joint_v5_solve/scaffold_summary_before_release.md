# 可见最大 C 联合 v5：静态求解骨架待释放

Boss1；RUN `six-boss1-20261111`；profile `full`；实际 agent `/root/visible_joint_v5_solve`。

**状态：WAITING_FINAL_INPUT_SHA_AND_EXPLICIT_MAIN_RELEASE。当前优化授权 0、实际调用 0。**

本阶段只读取经冻结 manifest 校验的 v4 程序接口。没有读取、列举或轮询 v5 输入目录及其仍活跃来源；没有读取旧输入/旧点、导入旧求解器、创建 Main 授权、消费标记或数值结果。

| 静态文件 | 职责 |
|---|---|
| `contract.py` | 最终 Main 释放、精确 SHA 闭包、manifest 计数、完整模型、literal 1586 前缀、30 个 rhs=-1 和原缩放门禁 |
| `preflight.py` | 当前静态检查；未来释放后的全域预检，二者明确分开 |
| `solve_once.py` | 唯一一次完整矩阵 highs-ds；60 秒、presolve false、tols 1e-9，排他消费后调用 |
| `recover_exact.py` | 本次返回支持上的有理恢复，全部原付款、仿射 rhs 和自由等式 |
| `verify_certificate.py` | 独立 Fraction 全 raw/513 列/2 等式/原尺度/互补核验 |
| `analyze_optimal_face.py` | 全零对偶余量列的完整面，保留全部原行与非负参数条件 |
| `verify_optimal_face.py` | 独立 Fraction 消元、全域面与全列固定泛函恒等式核验 |
| `diagnose_true_payments.py` | 本次实际正付款的完整来源诊断队列；具体真分支公式待释放后实读实施 |
| `freeze_scaffold.py` | 仅冻结静态骨架的指纹，不能创建输入冻结或授权 |
| `main_release.template.json` | 空授权模板，实际确认字段为 null，所有权限为 false/0 |
| `expected_outputs.json` | 未来真实输出合同，不是已产生的结果 |
| `source_reference_pins.json` | 冻结 v4 程序接口来源及 SHA 校验记录 |
| `source_review.md` | 完整数学、门禁、运行与诊断边界说明 |

规划为 `1586+181+28+28+1096+137=3056` raw、513 非负列、2 自由等式。它尚未认证为实际输入。Main 最终输入、manifest、计数、分段任一不符都立即停止，不自行放松合同。新增 1470 行逐条 numerical divisor 为 25；真实 IC 权重独立解释。C-only 等式改写允许自由乘子为负，一般 8T/ordered 保留未消元 K。

不固定 K、不缩小优化支持、不补全旧点、不做 phase I、不启动第二 LP。面诊断不继承旧正付款、旧弱零态或旧效用/K 等号。当前没有新福利界、面可达性结论或 SPE；原 half 目标仍 **OPEN**。

Main 下一步须给出最终精确 input/manifest/scaling/source/evidence SHA、确认计数和明确一次释放。具体字段见 `source_review.md`。`scaffold_manifest.json` 与 `SCAFFOLD_SHA256SUMS` 仅描述本次静态准备。
