# 加权拥塞结构用于决策：成稿、方法与复现

**定位：本包是基于 main 现有资产重建的决策方法专题。** [上一轮范围对照](previous_structure_scope_comparison.md)保留原交付缺口；随后新增的[自足结构重建](../structural_reconstruction/README.md)另含近次数主结果、类型森林、稳定集合及权深度桥，按自己的证明和审查登记。

本成果包把既有局部势、共同尺度和修复结构用于原游戏的稳定决策与成本优化。专题正文见[决策方法成稿](structure_to_decision.md)，再按当前任务进入详细证明或可运行工具。已有全状态线性下界和英文主论文独立保留，见[来源恢复](source_recovery.md)。

## 结果与适用范围

| 精确身份 | 结果 | 使用条件与边界 |
| --- | --- | --- |
| WC-FINITE-COMMON-SCALE-CALIBRATION-v1 | 三层有理校准LP、独立原始/对偶核验、严格改善下降 | NO仅否定指定校准接口；紧凑输入不保证多项式 |
| WC-STRUCTURE-WELFARE-REGULARIZATION-v1 | Φ+ηW同时给稳定倍率及社会成本界，并可按目标倍率选η | 共同尺度和有效包络；福利部分需全局最小性或有证据的目标gap |
| WC-EXISTING-CLOCK-FRONT-DECISION-v1 | 原游戏α-PNE恰为全部前沿端点sink，给解或全状态出口证书 | 原实例已有完整支配时钟；固定类数、显式有理稠密多项式输入可位多项式决策 |
| WC-ONE-ROOT-FROZEN-PRICE-LIFT-v1 | 单根模块以冻结延续报价消去，固定lift保max(α,β)稳定 | 给定完整报价证书；单向提升，核心NO不否定原游戏 |
| WC-EXPLICIT-STABILITY-COST-FRONTIER-v1 | 精确稳定集合、两种社会目标前沿、完整无解或预算排除证书 | 全状态枚举；实际工具有规模上限，超限不称无解 |
| WC-POTENTIAL-QUALITY-SEPARATION-v1 | 最小势可选更贵精确均衡；另有稳定预算不可兼得的锐二状态例 | 明确仿射实例，不是一般性能支配 |
| WC-CALIBRATION-EXISTENCE-SEPARATION-v1 | 精确PNE和改善无环仍可没有共同尺度成本差校准 | 明确两玩家x/x²实例；阻止把接口NO误报为原问题NO |

这些是各自范围内的内部已审证明、算法接口或反例。完整对象、量词、依赖、证据及异议见[命题账本](../../../weighted_congestion_frontier/CLAIMS.md)；[独立审查](../../../reviews/weighted_congestion/decision_methods_review.md)明确审查覆盖和已修补的固定背景问题。

## 文件地图

| 仓库完整路径 | 内容、为何存在与读取时机 |
| --- | --- |
| research/current/weighted_congestion/decision_methods/previous_structure_scope_comparison.md | 旧主线与新专题的逐项差别、两种森林定义及接续目标；判断是否已恢复旧工作时先读 |
| research/current/weighted_congestion/decision_methods/structure_to_decision.md | 连续成稿：需求→校准→稳定与成本拼装→原游戏修复→实例比较；向新读者说明方法价值时首先读取 |
| research/current/weighted_congestion/decision_methods/calibration.md | 共同正尺度、三类LP、精确Farkas与负圈、端点及局部资源包解析例；实现校准器前读 |
| research/current/weighted_congestion/decision_methods/decision_quality.md | 正则化定理、背景恢复、η选择、路径峰值、稳定集合下界及社会切线证书；制定质量/预算目标时读 |
| research/current/weighted_congestion/decision_methods/repair.md | 原实例支配时钟的精确前沿决策、完整NO样例、冻结模块报价lift；缩减状态空间前核对全部条件 |
| research/current/weighted_congestion/decision_methods/runner.md | 有理JSON合同、CLI、两种成本、基线、全部输出与规模限制；实际跑输入时读 |
| research/current/weighted_congestion/decision_methods/baselines.md | 七份一手方法原文及三个应用合同；比较稳定、时间、成本时读，避免忽略低次和小权比基线 |
| research/current/weighted_congestion/decision_methods/source_recovery.md、source_recovery.json | 既有论文/证明的原始hash、恢复基准和缺失旧稿范围；接续前期成果时读 |
| research/reviews/weighted_congestion/decision_methods_review.md | 先独立重构后攻击的真实记录、反例、背景修复和代码检查范围；提升或引用本轮结果前读 |
| tests/audits/weighted_congestion/decision_methods/ | 决策器、校准API、质量与修复审计及第二实现攻击；只依赖Python标准库 |
| examples/weighted_congestion/decision_methods/ | 实际输入：零费用、空策略、单玩家、异权非线性和既有二次三人例；学习JSON合同或回归时用 |
| evidence/runs/weighted_congestion/decision_methods/ | 从正式路径重跑的有理证据、源代码hash、参数/seed及审查迁移hash对应；复现时另写新文件 |

## 从仓库根复现

先用[运行说明](runner.md)理解JSON字段。下列命令输出完整证书；添加`--summary`可同时在stderr看简报。

```sh
python3 tests/audits/weighted_congestion/decision_methods/decision_runner.py examples/weighted_congestion/decision_methods/quadratic_triad.json --alpha 1 --alpha 286/267 --summary
python3 tests/audits/weighted_congestion/decision_methods/decision_quality_audit.py --check evidence/runs/weighted_congestion/decision_methods/decision_quality_audit.json
python3 tests/audits/weighted_congestion/decision_methods/repair_audit.py
python3 tests/audits/weighted_congestion/decision_methods/independent_attack_check.py
```

校准与runner审计需要创建新记录时，使用从未存在过的输出路径：

```sh
python3 tests/audits/weighted_congestion/decision_methods/calibration_audit.py --output ../new-calibration-audit.json
python3 tests/audits/weighted_congestion/decision_methods/decision_runner_audit.py --output ../new-runner-audit.json
```

全部运算为整数或Fraction；有限PASS只支持所列代码与输入，通用结论由书面证明承担。新工作应优先在这些合同内比较真实决策质量和可计算性，新增状态、费用或结构范围则另立版本。
