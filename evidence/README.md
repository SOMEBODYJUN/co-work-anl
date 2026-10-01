# 实例证书与有限运行

- [certificates](certificates)保存指定输入的输出。三类程序的字段和客户延续概念不同，须按[运行说明](../USAGE.md)分别复核。
- [runs/2026-09-30](runs/2026-09-30)是已冻结的小规模检查记录；当前测试默认只向终端输出，不覆盖旧报告。
- [certificates/shared/on_path_chord.json](certificates/shared/on_path_chord.json) 是完整三地点游戏中算法选中三名真实混合客户的 C 见证，输入在 [examples/shared/on_path_chord.json](../examples/shared/on_path_chord.json)。它验证一个实例和此前缺少的全游戏分支覆盖，不证明普遍上界。对应 [2026-10-01 运行清单](runs/2026-10-01/on_path_chord.json)列出命令和内容摘要。
- [修正六地点整数例](../examples/shared/sharp_lower_rational.json)的[精确实例证书](certificates/shared/sharp_lower_rational.json)与[运行清单](runs/2026-10-01/sharp_lower_rational.json)记录最优因子 `499750/309017`；全称锐性下界另由[数学证明](../research/current/shared/sharp_phi_lower.md)给出。
- 原始内部审计移入 [history/source/audits](../history/source/audits)，其覆盖范围由[新写的数学分支](../research/current/README.md)逐条引用。

[资产关系](../ASSETS.md)说明每种证据支持哪条命题、不能替代何种证明。测试与实例证书不把“内部候选”升级为“外部复核完成”。

旧版 2026-09-30 冻结 JSON 只记种子、规模和结果，未记录生成时的代码提交、输入摘要、命令和 Python 版本；无法事后可靠补造这些来源。新运行须记录上述信息及检查器版本，并把历史记录视为可重跑的结果概述，而非具有可证明原始快照的实验封存。
