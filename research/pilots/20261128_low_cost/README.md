# 八篇正文的低成本提炼试跑

执行者：实际子代理gpt-6-luna，low；没有在脚本中调用付费API。
输入：B20、B23P、P15、P26、S24、W25、Z24、Z26的完整段落，共98,526字符，
不是98,526 token。正文取得与策选由前置阅读者完成；这个试跑检查提炼到写作链路。

先读[短分析](brief.txt)和[思维上下文](thinking_context.txt)。
[结果](result.json)有17个命题、4条分类型关系；[候选阅读图](reading-graph.json)
共28节点，不等于28个已确立的经济判断，也没有自动合并进旧工作区的正式裁决图。
[图的用途](graph_use.txt)记录由查询产生的实际后续调查。

原稿的实质错误由实际独立读者发现，见[independent_review_01.json](independent_review_01.json)。
原result、brief与执行记录保存在baseline_01_*，编辑前正文在brief_pre_edit.txt。
[semantic_repairs.json](semantic_repairs.json)记录逐项修复。最终局部复核见
[independent_review_02.json](independent_review_02.json)。

本批实跑的是：实读→提炼经济认识/主体模型→精确命题→候选机制→图查询→调查任务→
短分析→独立挑错→返修→对改动项复核。已修复同一时点自证、复合后件、伪对手、
账面承接与最终承损混淆、未获段落支持的家庭储蓄动机，以及观测/解释混写。

程序检查只核结构和出处。此次独立复核只通过局部提炼范例，未核实当前中国宏观
机制的相对贡献，也没有宣布完整思维上下文、48项研究或中国危机报告完成。

输入出处、正文哈希和阅读范围见execution.json、packet_metadata.json及
../../program/article_selection.json。第三方原始全文保留在本地研究缓存，公开交付是
原文链接、定位与研究笔记。新环境先取全文并生成自己的packet；只有输入正文及段落
版本相同才能复用本次结果。正文变化就重新核读，不能为绕过绑定只改结果的输入哈希。

本轮工程检查：默认环境缺少锁定的statsmodels与patsy；在隔离测试目录安装后，
完整65项回归通过。这个结果只表明工程回归通过，不是经济研究质量分数。
旧boss 1工作区的17/20原状态保留。本批没有替它登记新阶段或发布旧报告。
