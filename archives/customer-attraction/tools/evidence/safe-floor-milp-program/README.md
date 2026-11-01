# 非可信保底菜单MILP与九客户边界点

两主源分别为[2216B原程序](original/safe_floor_milp.py) `a5598cc1012110ebe8cf` 和[773B原报告](original/safe_floor_m3p6.json) `68f3fa9288cd960ab86f`。[完整程序/数据对象](../../../state/程序/非可信保底菜单的混合整数松弛与九客户边界点--程序.md)自足给全部约束、量词、输出和异常。

原默认p6/m3模型有63连续客户质量与90二元菜单变量，247行。每当前主题单独选不含它的二人背景，要求当前收益≤1、后继≥1；没有完整策略或后继最佳回复。大常数和质量cap均为18。目标是前三主题覆盖，原浮点value/dual_bound约9、时间7.604846477508545秒仅为旧记录。原完整x、残差和环境未保存，本轮原MILP执行0。

本包新做一次标准库[定义级核](audit_point.py)，不import原码、提取AST或调用MILP/BI。从模型直接构[247行有理系数](coefficient-rows.json)，再核显示小数零补点和另行定义的整数修复。[精确报告](exact-audit.json)与[九单位客户/六菜单/42支持](point-and-menus.json)保完整结果。后继行按排序列出，独立账本行号不冒原浮点CSR下标。

修复点mask10/20/33各3，总9客户，所有菜单三人收益(1,1,1)，每个末位可改独立块得3，故非SPE。所有247行与变量界精确满足，前三主题覆盖9；选中菜单query≤1及每客负载≤3使每主题大小≤3，目标并集≤9，故精确达到本规范化模型最优。总质量cap18在此余9，不能用它证明目标9。目标保护floor为OPT/6=3/2，菜单后继1未达到；阈值1下当前也没有严格下降。

原显示小数作精确十进制、未显示质量补0、显示选择z设1时，四个后继行略负；value减显示目标429/10^16。这不认定未保存的完整HiGHS向量有相同差，也不把近似数免费改成精确3。源输出过滤w≤1e−7，故可见数据不足恢复原完整向量。

[执行记录](execution.json)保唯一新审计、实际执行脚本SHA与输入；未单独安装计时器，不编造当前耗时。[执行历史及勘误](run-history/README.md)保原执行代码/首报告：首次解释误把18写9，实际矩阵与运算一直用18，后只修上界说明并披露，数学运行数仍1。请以当前正文和exact-audit为正确结论。

[来源清单](source-manifest.json)、[全仓比较](comparison-manifest.json)、[阅读记录](review-record.json)、[运行范围](execution-scope.json)区分两主源、相关README/解析障碍、新证据和未做事项。[十八主题保护审计](../../../state/计算/十八主题保底保护松弛的精确审计--计算.md)才给正确目标floor的严格非可信反例；它同样不是完整SPE。对应[全局研究入口](../../../state/资源/全局保底研究入口的充分桥障碍与未成熟菜单边界--资源.md)已保原t1探索的未成熟边界。

未来若另有需要，可运行当前修订后的标准库审计到新的不存在目录：

```sh
python3 -I -B audit_point.py --input original/safe_floor_m3p6.json --output-dir /absolute/new/audit-directory
```

它不执行原MILP；当前修订只更正说明，未来新结果应记为新事件。此包已经有一次完整数学核，不需重复。`python3 -I -B check_package.py`仅做[静态封包检查](check_package.py)：哈希、语法、已存账本结构/说明勘误及链接，不重算收益或求解。[成果指纹](artifact-manifest.json)排除自身与[self-check](self-check.json)避免循环。
