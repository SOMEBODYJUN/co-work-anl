# 家庭离线计算器

直接打开 calculator.html。首次载入的家庭金额为空。选择“载入合成示例”后可查看一组明确标记的人工家庭。填写起始可用现金和最低生活支出后运行 120 个月，切换“方案比较”“逐月台账”“逆向压力”。金额可在元和万元间换算，日期以第几个月表示。

家庭与人工情景一起存入导出的 JSON。策略 CSV 包含全部已运行候选及各路径结果。所有方案月表 CSV 足额导出每个候选、情景与月份，失败后空列并标 truncated。当前选择的策略与情景可单独导出月表。导出动作仅在本地生成文件。

| 文件 | 用途 |
|---|---|
| calculator.html | 可单独复制、离线运行的完整成品 |
| engine.js | 浏览器及 Node 共用的计算和排序引擎 |
| ui.html、ui.js、build.py | 页面模板、纯本地控件、可重复构建程序 |
| input_schema.md | 原始 JSON 字段、情景与函数契约 |
| scenarios.json、synthetic_household.json、build_examples.js | 三条人工路径、标记明确的示例、确定性生成器 |
| checks.js、checks.json | 回归代码与实际结果；同时生成样例策略和逐月结果 |
| loan_input.json、loan_work_reference.json、compare_python.py、python_reference_checks.json | 仓库统一方法入口及独立逐期合同对照 |
| sample_summary.json、synthetic_strategy_results.csv、sample_baseline_severe_months.json、legacy_cash_stress.json | 500 条规则及分币级逐月轨迹的三路径比较、第 101 月截断的基准台账、18 万元对照 |
| verify_offline_ui.py | 在可用真实浏览器上的离线操作回放 |
| implementation_notes.md、task_package.md、freeze_sha256.json | 清算顺序、覆盖理由、结果解释、作者回执与内容版本 |

在此目录执行 python build.py 生成同样的离线页面。node checks.js 重放全套工程算例。独立合同对照使用仓库研究环境运行 compare_python.py，脚本内部通过 work.py methods run --name loan 执行统一方法。
