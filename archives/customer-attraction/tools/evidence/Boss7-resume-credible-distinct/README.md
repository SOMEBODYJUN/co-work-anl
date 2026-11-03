# 可信子树试验与DP交叉记录：源证据

四主源及两份必要相关源码逐字节保存，完整来源提交、blob、SHA-256、size及本地路径在[source-manifest.json](source-manifest.json)。主源共776416字节；两冻结提交中的各主文件相同，不借后来的README覆盖原数值状态。related源码仅用于理解接口，不额外登记主源完成。

数学正文为[可信续局试验与动态规划交叉核对](../../../state/审查/可信续局试验与动态规划交叉核对--审查.md)。完整历史与局部子树、所选精确对偶与浮点全支持扫描、端点与锥最优、DP有限记录与未知原输入均在那里分开。

[inspect_report_structure.py](inspect_report_structure.py)本轮运行一次，仅用标准库读原件；[complete-data-read-index.json](complete-data-read-index.json)保全部非大动作表字段、40项DP原字段、每个正类型、层内行动分布、同计数不同动作示例、七根枝路径与全部14个子树digest核对。全部5602个动作记录和254个重数位置均逐项遍历，完整键域恰等有序树。原动作表/全部零坐标始终在原件中，未丢任何唯一内容。索引是数据阅读证据，未自称数学检查器。

运行输出：`PASS_FROZEN_REPORT_STRUCTURE_AND_COMPLETE_DATA_READING`；trial_action_records=5602，trial_clone_entries=254，dp_records=40，mathematical_checks_replayed=0。没有导入原模块、运行原main、重新求DP/SPE集合、回放原Fraction激励检查、求LP/MILP、抽样或重跑既有成功审计。根枝路径只依照存储的动作表读取，客户支持与覆盖/收益结论由正文中显式单位客户输入直接计算。

原报告的`independent_check.verified`、精确原始/对偶字段及原HiGHS状态按历史声明保留；结构核对不替代它们，也未制造新的原argv、stdout、计时或生成器绑定。尤其dp_crosscheck只有40项计数摘要，search_security.py无其输出入口，不将二者强行绑定。
